"""Run one workflow step skill on one issue, headless, and render its answer onto the card.

Usage:
  run.py <agent> <n> [analysis|strategy|context] [--pages <dir>] [--repo <dir>] [--model <id>] [--effort <level>]
         [--feedback <text> [--from resolver|engineer|ruling]]

`analysis` runs the issue-analysis skill and writes `agents/<agent>/analysis/<n>.json`; `strategy` runs the sim-strategy
skill on that answer and writes `agents/<agent>/strategy/<n>.json`; `context` runs the context-edit skill and writes
`agents/<agent>/context/<n>.json`. Below, <step> is that folder.

Model and reasoning effort come from the skill's frontmatter metadata (`model`, `reasoning-effort`); the options override.

Steps: build the brief (brief.py --step <step>), prepend the body of the step's skill, plugin/skills/<name>/SKILL.md, run pi
on it (json mode, prompt on stdin, read and bash tools, no skills, extensions or context files), check the answer against
the skill's schema.json, once asking the same session to correct it, keep the previous answer and the previous card under
`<step>/history/`, write the new JSON to `agents/<agent>/<step>/<n>.json` and splice the section into the card with
card.py.
Progress lives in `agents/<agent>/cards/<n>/<step>/status.json`, which the issues page polls: state working, done or
failed, with times, the repo commit, token usage, how long the model has been silent and the error tail. Run files sit
in `<step>/runs/<n>/`: prompt.md (the whole message sent), system.md (the system prompt), out.jsonl (every pi event, deltas coalesced), err.log.
When the run ends, done or failed, those files and the answer are copied to `<step>/runs/<n>/<start stamp>/`, which later
runs leave alone, and the run is one event of the card's history (cardlog.py) pointing there.
A SIGTERM from the page's stop button ends pi and everything it started, and marks the run stopped.

The repo is the issue's worktree. Git is left alone: the card's work stays uncommitted there until the resolution
commits it at merge, so HEAD is the branch before the card's work and the tree is the work so far. A context step
needs the worktree's Ghostwriter bound to the issue workspace, since it pushes there. pi's session is kept in runs/<n>/session/; a fresh run moves the previous one aside to
session.<stamp>/. --feedback continues that session (-c) with one message, the feedback;
without a session it runs fresh with the feedback under a heading at the end of the prompt. feedback.md keeps the text.
--from says whose it is, engineer by default: a claim the step weighs (the answer's `feedback` field, required non-null
then), or a ruling, which it applies (every point accepted).
"""
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
import paths

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.environ.get("SIERRA_PLUGIN") or os.path.abspath(os.path.join(HERE, "..", "..", ".."))
# step name = its folder under agents/<agent>/; skill = folder under plugin/skills/; view = card.py view. What the brief
# holds and what may be read from disk is the skill text's to say.
STEPS = {
    "analysis": {"skill": "issue-analysis", "view": "ia"},
    "strategy": {"skill": "sim-strategy", "view": "ss"},
    "context": {"skill": "context-edit", "view": "oc"},
}
PI = os.environ.get("SIERRA_PI") or shutil.which("pi") or "/opt/homebrew/bin/pi"
PROVIDER = os.environ.get("SIERRA_RUN_PROVIDER") or "openai-codex"
STALL = int(os.environ.get("SIERRA_RUN_STALL") or 180)  # seconds without a byte from the model before the run is failed
RESULT_CAP = 20000  # chars of one tool result kept in out.jsonl


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pages_dir(override=None):
    return override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues")


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)


def watch(proc, status, status_path, lock, stopped, act):
    """Every 5 s: how long pi's event stream has been silent and whether a tool it started is still running, written to
    status["live"] for the page. Silence for STALL seconds ends the run, unless a tool is running: a simulation run
    keeps the model silent for minutes. act is the stream loop's {"last": time of the last event, "tools": open calls}."""
    while proc.poll() is None:
        time.sleep(5)
        if proc.poll() is not None:
            break
        quiet = round(time.time() - act["last"])
        live = {"at": now(), "quiet": quiet, "tool": act["tools"] > 0}
        with lock:
            status["live"] = live
            write_json(status_path, status)
        if quiet >= STALL and act["tools"] <= 0:
            stopped.append(f"no data from the model for {quiet} s")
            os.killpg(proc.pid, signal.SIGTERM)
            break


def skill(name):
    """(frontmatter dict, body) of plugin/skills/<name>/SKILL.md."""
    text = open(os.path.join(PLUGIN, "skills", name, "SKILL.md"), encoding="utf-8").read()
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    import yaml
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def linked_docs(name, body):
    """The sierra reference documents the skill text links, as prompt sections: they travel with the prompt like schema.json."""
    out = []
    for rel in dict.fromkeys(re.findall(r"\]\(((?:\.\./)+sierra/references/[^)\s]+\.md)\)", body)):
        path = os.path.normpath(os.path.join(PLUGIN, "skills", name, rel))
        out.append(f"# {os.path.basename(rel)}\n\nThe document the skill text links as {os.path.basename(rel)}.\n\n"
                   + open(path, encoding="utf-8").read().strip())
    return "".join("\n\n" + d for d in out)


# ---------- the answer ----------

def span_errors(step, answer, agent, repo, base, n):
    """The spans the schema calls exact substrings, checked against what they mark: the item text in the block file,
    a tool description's source file, or the failure turn's text or tool call in the call's cache."""
    sys.path.insert(0, HERE)
    import brief, card
    out = []

    def item(path, file, pointer, span):
        if not (file and span):
            return
        if not file.endswith(".json"):
            src = os.path.join(repo, brief.AGENT_DIR.get(agent, agent), file.split(":")[0])
            if os.path.exists(src) and span not in open(src, encoding="utf-8").read():
                out.append(f"{path} is not an exact substring of {file}")
            return
        try:
            rows, _ = card.block_rows(repo, agent, file)
            r = card.find_row(rows, pointer or "")
        except SystemExit:
            out.append(f"{path}: {file} {pointer} is not an item the outline prints")
            return
        if span not in r[3]:
            out.append(f"{path} is not an exact substring of the item at {file} {pointer}")

    if step == "analysis":
        ctx = answer.get("context") or {}
        w = ctx.get("wanted") or {}
        if w.get("state") != "new":
            item("$.context.wanted.span", w.get("file"), w.get("pointer"), w.get("span"))
        b = ctx.get("won") or {}
        item("$.context.won.span", b.get("file"), b.get("pointer"), b.get("span"))
        f = answer.get("failure") or {}
        iss = brief.load(paths.issue(base, n))
        for cid in brief.call_of_analysis(base, iss, answer):
            conv_dir = paths.conversation(base, cid)
            details = brief.load(os.path.join(conv_dir, "details.json"))
            turns = card.turns_of(details)
            turn, msg = card.locate(turns, f.get("logEntryId"))
            if not turn:
                out.append(f"$.failure.logEntryId {f.get('logEntryId')} is not a message of the linked call")
                break
            kind, k, _ = card.parse_path(f.get("path"))
            if kind == "text":
                text = msg.get("text") or ""
                where = "the failure turn's text"
            else:
                calls = card.tool_calls(conv_dir, turns).get(card.message_index(turns, msg) - 1, [])
                if k >= len(calls):
                    out.append(f"$.failure.path {f.get('path')}: the turn has {len(calls)} tool calls")
                    break
                text = card.tool_text(calls[k])
                where = f"the call as the transcript prints it, {text[:80]}"
            for i, s in enumerate(f.get("bad") or []):
                if s not in text:
                    out.append(f"$.failure.bad[{i}] is not an exact substring of {where}")
    elif step == "context":
        for i, a in enumerate(answer.get("also") or []):
            item(f"$.also[{i}].span", a.get("file"), a.get("pointer"), a.get("span"))
    return out


def parse_answer(text):
    """The JSON object in the model's final text: bare, or inside a code fence, or the first {...} block."""
    text = (text or "").strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    try:
        return json.loads(text)
    except ValueError:
        pass
    a, b = text.find("{"), text.rfind("}")
    if a >= 0 and b > a:
        return json.loads(text[a:b + 1])
    raise ValueError("no JSON object in the reply")


def feedback_errors(answer, feedback, source):
    """`feedback` is filled exactly when the run carries feedback, and a ruling's points are all accepted."""
    fb = answer.get("feedback") if isinstance(answer, dict) else None
    if feedback and not fb:
        return ["$.feedback: the run carries feedback; weigh it as feedback.md says and fill feedback"]
    if not feedback and fb:
        return ["$.feedback: the run carries no feedback; it is null"]
    if fb and source == "ruling" and (fb.get("verdict") != "accepted" or any(p.get("verdict") != "accepted" for p in fb.get("points") or [])):
        return ["$.feedback: a ruling settles its points; apply it and accept every point"]
    return []


def violations(value, schema, path="$"):
    """What in value breaks the schema: the subset of JSON Schema the step schemas use (type incl. lists with null,
    required, properties, additionalProperties false, enum, items)."""
    out = []
    types = schema.get("type")
    if types:
        types = types if isinstance(types, list) else [types]
        ok = any((t == "null" and value is None) or (t == "object" and isinstance(value, dict))
                 or (t == "array" and isinstance(value, list)) or (t == "string" and isinstance(value, str))
                 or (t == "boolean" and isinstance(value, bool))
                 or (t == "integer" and isinstance(value, int) and not isinstance(value, bool))
                 or (t == "number" and isinstance(value, (int, float)) and not isinstance(value, bool)) for t in types)
        if not ok:
            return [f"{path}: expected {' or '.join(types)}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        out.append(f"{path}: {json.dumps(value, ensure_ascii=False)} is not one of {json.dumps(schema['enum'], ensure_ascii=False)}")
    if isinstance(value, dict):
        props = schema.get("properties") or {}
        for k in schema.get("required") or []:
            if k not in value:
                out.append(f"{path}.{k}: missing")
        if schema.get("additionalProperties") is False:
            for k in value:
                if k not in props:
                    out.append(f"{path}.{k}: not in the schema")
        for k, sub in props.items():
            if k in value:
                out += violations(value[k], sub, f"{path}.{k}")
    if isinstance(value, list) and "items" in schema:
        for i, v in enumerate(value):
            out += violations(v, schema["items"], f"{path}[{i}]")
    return out


# ---------- pi ----------

def trim(ev):
    """The event as out.jsonl keeps it: the prompt and the duplicated message copies shortened, tool results capped."""
    t = ev.get("type")
    if t in ("message_start", "message_end"):
        m = ev.get("message") or {}
        if m.get("role") == "user":
            n = sum(len(c.get("text") or "") for c in m.get("content") or [] if isinstance(c, dict))
            ev = dict(ev, message={"role": "user", "chars": n, "timestamp": m.get("timestamp")})
        elif m.get("role") == "toolResult":
            ev = dict(ev, message={"role": "toolResult", "toolCallId": m.get("toolCallId"), "toolName": m.get("toolName"),
                                   "isError": m.get("isError"), "timestamp": m.get("timestamp")})
    elif t == "turn_end":
        ev = {"type": "turn_end"}
    elif t == "agent_end":
        ev = {"type": "agent_end"}
    elif t == "tool_execution_update":
        ev = {"type": t, "toolCallId": ev.get("toolCallId"), "toolName": ev.get("toolName")}
    elif t == "tool_execution_end":
        res = ev.get("result")
        if isinstance(res, dict):
            parts = []
            for c in res.get("content") or []:
                if isinstance(c, dict) and isinstance(c.get("text"), str):
                    parts.append(c["text"])
            text = "\n".join(parts)
            if len(text) > RESULT_CAP:
                text = text[:RESULT_CAP] + f"\n… {len(text) - RESULT_CAP} more chars"
            ev = dict(ev, result={"text": text})
    elif t == "message_update":
        ev = {"type": t, "assistantMessageEvent": ev.get("assistantMessageEvent")}
    return ev


DELTAS = ("text_delta", "thinking_delta", "toolcall_delta")


def usage_of(out_jsonl):
    u = {"in": 0, "cached": 0, "out": 0, "reasoning": 0, "commands": 0, "cost": 0.0}
    if not os.path.exists(out_jsonl):
        return u
    for line in open(out_jsonl, encoding="utf-8"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "message_end" and (e.get("message") or {}).get("role") == "assistant":
            x = e["message"].get("usage") or {}
            u["in"] += x.get("input", 0) or 0
            u["cached"] += x.get("cacheRead", 0) or 0
            u["out"] += x.get("output", 0) or 0
            u["reasoning"] += x.get("reasoning", 0) or 0
            u["cost"] += (x.get("cost") or {}).get("total", 0) or 0
        if e.get("type") == "tool_execution_end":
            u["commands"] += 1
    u["cost"] = round(u["cost"], 4)
    return u


def tail(path, n=12):
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return ""
    return "\n".join(lines[-n:])[-1500:]


def keep_run(runs, started, feedback, answer_path=None):
    """This run's files, and its answer when it has one, copied to runs/<n>/<start stamp>/: the card's history points
    there. The copied paths."""
    dest = base = os.path.join(runs, started.replace(":", ""))
    k = 1
    while os.path.exists(dest):  # two runs started within one second
        k += 1
        dest = f"{base}-{k}"
    os.makedirs(dest)
    kept = []
    for f in ("answer.json", "feedback.md", "prompt.md", "out.jsonl", "err.log"):
        src = answer_path if f == "answer.json" else os.path.join(runs, f)
        if src and os.path.exists(src) and (f != "feedback.md" or feedback):
            shutil.copy(src, os.path.join(dest, f))
            kept.append(os.path.join(dest, f))
    return kept


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    agent, n = argv[0], argv[1]
    rest = argv[2:]
    step = rest.pop(0) if rest and not rest[0].startswith("--") else "analysis"
    opts = dict(zip(rest[::2], rest[1::2]))
    feedback = (opts.get("--feedback") or "").strip()
    if opts.get("--from") not in (None, "resolver", "engineer", "ruling"):
        sys.exit("--from is resolver, engineer or ruling")
    if step not in STEPS:
        sys.exit(f"unknown step {step}")
    s = STEPS[step]
    pages = pages_dir(opts.get("--pages"))
    repo = os.path.abspath(opts.get("--repo") or os.getcwd())
    fm, body = skill(s["skill"])
    meta = fm.get("metadata") or {}
    model = opts.get("--model") or meta.get("model") or "gpt-5.6-terra"
    effort = opts.get("--effort") or meta.get("reasoning-effort") or "high"
    base = paths.agent(pages, agent)
    runs = paths.runs(base, n, step)
    status_path = paths.status(base, n, step)
    answer_path = paths.answer(base, n, step)
    card_path = paths.card(base, n)
    schema_path = os.path.join(PLUGIN, "skills", s["skill"], "schema.json")
    os.makedirs(runs, exist_ok=True)
    started = now()
    t0 = time.time()
    status = {"step": step, "state": "working", "started": started, "ended": None, "seconds": None, "commit": None,
              "model": model, "effort": effort, "pid": os.getpid(), "thread": None, "usage": None, "live": None, "error": None,
              "feedback": bool(feedback), "continued": False}
    write_json(status_path, status)
    lock = threading.Lock()
    stopped = []
    holder = {}  # the pi process while one runs, in its own process group with everything it starts

    def record():  # the ticket's cost ledger: one entry per run
        sys.path.insert(0, HERE)
        import ledger
        ledger.add(pages, agent, n, ledger.entry(status["ended"], step, status, status["usage"]))

    def history(what, answer=None):
        sys.path.insert(0, HERE)
        import cardlog
        try:
            kept = keep_run(runs, started, feedback, answer_path if answer is not None else None)
        except OSError:
            kept = []
        head = {"resolver": "the resolution agent's feedback", "engineer": "the engineer's feedback",
                "ruling": "the engineer's ruling"}[opts.get("--from") or "engineer"]
        first = next((l.strip() for l in feedback.splitlines() if l.strip()), "")[:80]
        cardlog.add(pages, agent, n, step, (f"rerun on {head} («{first}»): " if feedback else "") + what,
                    [cardlog.rel(pages, agent, k) for k in kept if not k.endswith(("prompt.md", "err.log"))],
                    answer=answer is not None)

    def fail(msg):
        with lock:
            status.update(state="failed", ended=now(), seconds=round(time.time() - t0), error=msg,
                          usage=usage_of(os.path.join(runs, "out.jsonl")))
            write_json(status_path, status)
            record()
        history("failed: " + msg)
        sys.exit(1)

    def on_term(signum, frame):  # the page's stop button sends SIGTERM to this process
        stopped.append("stopped from the page")
        proc = holder.get("proc")
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)  # the stream loop sees the end and fails the run with the reason above
        else:
            fail(stopped[0])
    signal.signal(signal.SIGTERM, on_term)

    session_dir = os.path.join(runs, "session")  # pi's own record: the retry and a later --feedback continue it
    try:
        sys.path.insert(0, HERE)
        import stepgit, setup as setup_mod
        agent_rel = setup_mod.AGENT_DIR[agent]
        agent_dir = os.path.join(repo, agent_rel)
        if step == "context":
            try:
                stepgit.binding(pages, agent, n, agent_dir)
            except stepgit.Refused as ex:
                fail(str(ex))
        status["commit"] = stepgit.git(repo, "rev-parse", "--short", "HEAD").strip()
        write_json(status_path, status)
        continued = bool(feedback) and os.path.isdir(session_dir) and any(f.endswith(".jsonl") for f in os.listdir(session_dir))
        if not continued and os.path.isdir(session_dir) and os.listdir(session_dir):
            stamp = datetime.fromtimestamp(os.path.getmtime(session_dir), timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
            shutil.move(session_dir, f"{session_dir}.{stamp}")
        os.makedirs(session_dir, exist_ok=True)
        status["continued"] = continued
        if feedback:
            open(os.path.join(runs, "feedback.md"), "w", encoding="utf-8").write(feedback + "\n")
        where = "The checkout holds the card's work so far, uncommitted; HEAD is the branch before it."
        brief = subprocess.run([sys.executable, os.path.join(HERE, "brief.py"), agent, n, "--step", step, "--pages", pages, "--repo", repo],
                               capture_output=True, text=True)
        if brief.returncode != 0:
            fail("brief: " + brief.stderr.strip()[-800:])
        schema = json.load(open(schema_path, encoding="utf-8"))
        # the skill text opens the message; its schema.json, the documents it links and the brief follow, so nothing is on disk
        prompt = (f"{body}\n\n# schema.json\n\n```json\n{json.dumps(schema, ensure_ascii=False, indent=1)}"
                  f"\n```{linked_docs(s['skill'], body)}\n\n# Brief · {agent} {n}\n\n{brief.stdout}")
        head = {"resolver": "Feedback from the resolution agent", "engineer": "Feedback from the engineer",
                "ruling": "The engineer's ruling"}[opts.get("--from") or "engineer"]
        weigh = "Apply it: a ruling settles its points. " if opts.get("--from") == "ruling" else "Weigh it as feedback.md says. "
        if continued:
            prompt = (f"{head} on your answer:\n\n{feedback}\n\n{where} {weigh}Do the step again on the tree as it is now, "
                      "and return only the JSON object schema.json describes.")
        elif feedback:
            prompt += f"\n\n# {head} on the previous run\n\n{feedback}\n\n{where} {weigh.strip()}\n"
        open(os.path.join(runs, "prompt.md"), "w", encoding="utf-8").write(prompt)
        system = ("You run one step of an unattended issue workflow. The user message carries the whole task: instructions, "
                  "the output schema and the data.")
        open(os.path.join(runs, "system.md"), "w", encoding="utf-8").write(system)
        base_cmd = [PI, "-p", "--mode", "json", "--no-skills", "--no-extensions", "--no-context-files", "--no-prompt-templates",
                    "--system-prompt", system,
                    "--session-dir", session_dir, "--thinking", effort, "--model", f"{PROVIDER}/{model}", "--tools", "read,bash"]
        final = {"text": None, "stop": None, "error": None}
        act = {"last": time.time(), "tools": 0}  # what the watch thread reads: last event time, tool calls still open

        def on_line(ev):
            if ev.get("type") == "session" and not status.get("thread"):
                with lock:
                    status["thread"] = ev.get("id")
                    write_json(status_path, status)
            if ev.get("type") == "message_end" and (ev.get("message") or {}).get("role") == "assistant":
                m = ev["message"]
                final["stop"] = m.get("stopReason")
                final["error"] = m.get("errorMessage")
                text = "".join(c.get("text") or "" for c in m.get("content") or [] if isinstance(c, dict) and c.get("type") == "text")
                if text.strip():
                    final["text"] = text

        answer, errors = None, []
        with open(os.path.join(runs, "out.jsonl"), "w", encoding="utf-8") as out, open(os.path.join(runs, "err.log"), "w") as err:
            for attempt in range(2):
                if attempt == 0 and continued:  # pi reads stdin with -c too, and joins it with the argument
                    cmd = base_cmd + ["-c", "The feedback is the text above."]
                elif attempt == 0:  # the prompt goes in on stdin: pi is killed at start by an argument past ~1000 chars
                    cmd = base_cmd + ["The instructions, the schema and the brief are the text above."]
                else:
                    cmd = base_cmd + ["-c", "Your reply was not the JSON object schema.json describes. Problems: "
                                      + "; ".join(errors[:12]) + ". Return only the corrected JSON object, nothing else."]
                    out.write(json.dumps({"type": "retry", "problems": errors[:12], "t": now()}, ensure_ascii=False) + "\n")
                final.update(text=None, stop=None, error=None)
                act.update(last=time.time(), tools=0)
                proc = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=err,
                                        stdin=subprocess.PIPE if attempt == 0 else subprocess.DEVNULL,
                                        text=True, encoding="utf-8", errors="replace", start_new_session=True)
                holder["proc"] = proc
                if stopped:  # the stop arrived between the check and the spawn
                    os.killpg(proc.pid, signal.SIGTERM)
                if attempt == 0:
                    def feed(pipe, text):
                        try:
                            pipe.write(text)
                            pipe.close()
                        except OSError:
                            pass
                    threading.Thread(target=feed, args=(proc.stdin, prompt), daemon=True).start()
                threading.Thread(target=watch, args=(proc, status, status_path, lock, stopped, act), daemon=True).start()
                # stream events
                buf = None

                def flush():
                    nonlocal buf
                    if buf:
                        out.write(json.dumps(buf[1], ensure_ascii=False) + "\n")
                        out.flush()
                        buf = None
                for line in proc.stdout:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        ev = json.loads(line)
                    except ValueError:
                        flush()
                        out.write(line + "\n")
                        continue
                    on_line(ev)
                    act["last"] = time.time()
                    if ev.get("type") == "tool_execution_start":
                        act["tools"] += 1
                    elif ev.get("type") == "tool_execution_end":
                        act["tools"] -= 1
                    ev = trim(ev)
                    ev["t"] = now()
                    ame = ev.get("assistantMessageEvent") if ev.get("type") == "message_update" else None
                    if ame and ame.get("type") in DELTAS:
                        key = (ame["type"], ame.get("contentIndex"))
                        if buf and buf[0] == key:
                            buf[1]["assistantMessageEvent"]["delta"] += ame.get("delta") or ""
                            continue
                        flush()
                        buf = (key, ev)
                        continue
                    flush()
                    out.write(json.dumps(ev, ensure_ascii=False) + "\n")
                    out.flush()
                flush()
                rc = proc.wait()
                if stopped:
                    fail(stopped[0])
                if rc != 0:
                    fail(f"pi exit {rc}: " + tail(os.path.join(runs, "err.log")))
                if final["stop"] == "error" or final["error"]:
                    fail("model: " + str(final["error"] or final["stop"]))
                if not final["text"]:
                    fail("no reply text: " + tail(os.path.join(runs, "err.log")))
                try:
                    candidate = parse_answer(final["text"])
                    errors = (violations(candidate, schema) or ("feedback" in (schema.get("properties") or {}) and feedback_errors(candidate, feedback, opts.get("--from")))
                              or span_errors(step, candidate, agent, repo, base, n))
                except ValueError as ex:
                    candidate, errors = None, [str(ex)]
                if not errors:
                    answer = candidate
                    break
            if answer is None:
                fail("answer does not match schema.json: " + "; ".join(errors[:6]))
        # keep the previous answer and the previous card
        os.makedirs(os.path.dirname(paths.history(base, n, step, "", "json")), exist_ok=True)
        if os.path.exists(answer_path):
            stamp = datetime.fromtimestamp(os.path.getmtime(answer_path), timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
            shutil.move(answer_path, paths.history(base, n, step, stamp, "json"))
        if os.path.exists(card_path):
            shutil.copy(card_path, paths.history(base, n, step, started.replace(':', ''), "card.html"))
        write_json(answer_path, answer)
        render = subprocess.run([sys.executable, os.path.join(HERE, "card.py"), s["view"], agent, n, "--pages", pages, "--repo", repo],
                                capture_output=True, text=True)
        if render.returncode != 0:
            fail("card.py: " + render.stderr.strip()[-800:])
        with lock:
            status.update(state="done", ended=now(), seconds=round(time.time() - t0), usage=usage_of(os.path.join(runs, "out.jsonl")))
            write_json(status_path, status)
            record()
        sys.path.insert(0, HERE)
        import cardlog
        history(cardlog.summary(step, answer), answer)
    except SystemExit:
        raise
    except Exception as ex:
        fail(f"{type(ex).__name__}: {ex}")


if __name__ == "__main__":
    main(sys.argv[1:])
