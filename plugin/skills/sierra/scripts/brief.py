"""Print the brief a workflow step skill reads for one issue, so it explores nothing.

Usage:
  brief.py <agent> <n> [--step analysis|strategy|context|resolve] [--pages <dir>] [--repo <dir>] [--calls <k>] [--history 0]
  brief.py <agent> --batch <batch> [--pages <dir>] [--repo <dir>]
  brief.py <agent> --replay <result-dir>

Static first, so a prompt cache shares the prefix across issues of one agent. For `analysis` (the default):
  1. the agent's Studio content as blocks.py prints it, path, text and JSON pointer per item, render order;
  2. the agent's SOP (agents/<agent>/sop/sop.md in the pages dir) when it has one, without its example conversations;
  3. the card's source (source.py), readable: for an issue its name, status, description, comments, and per linked
     call the reporter's highlighted lines with their turn; for a failing simulation its name, what failed and its
     definition;
  3. up to <k> of the source's conversations (3 by default), the one with the highlighted line first, then newest
     first, each as a numbered transcript with each line's turn, tool calls and activated observations inline, tags
     at the end; a simulation's one replay;
  4. the compiled request the model saw at the reported turn, when the source marks one: its system part and tool
     schemas, from the trace the GOALSDK_RESPOND row names in debug.log.
For `strategy`:
  1. the agent's suite as an index, one line per simulation, id, name and categories as `sierra test --list` reports
     them, under the file that declares it; then `simulations/harness.ts` verbatim;
  2. the tags the agent can emit: every tag literal in the agent's source with the file that declares it, and the
     tags the suite already asserts;
  3. the source as above;
  4. the Analysis answer, `agents/<agent>/cards/<n>/analysis/answer.json` in the pages dir (the step fails without it);
  5. the conversation the analysis names, the one holding its failure turn, as a transcript; <k> is 1 here.
For `context`:
  1. the Studio content as for `analysis`;
  2. the source;
  3. the Analysis answer, and the Sim Strategy answer when it exists;
  4. the conversation the analysis names, as a transcript with the activated observations inline;
  5. the compiled request at the failure turn the analysis names, as for `analysis`.
For `resolve`, the opening message of the interactive session: where everything lives, the source, and the three
step answers in full; the analysis must exist, the other two are marked when missing.
Every step's brief ends with the card's history as cardlog.py indexes it, when the card has one.
With --batch, the batch driver's opening message: the batch's values, then per card its state, branch, guard,
regression list and every run of it (the strategy's before the fix, the resolution's), each with its time, the main
commit its workspace held then (main's merges reach every workspace as they land) and per-simulation counts; then
main's merges since the oldest of those runs.
With --replay, one simulation replay (a results/<result> folder of a downloaded run) as a transcript, each line
addressed by its debug.log seq.
Everything comes from the pages dir ($BBVA_ISSUES_DIR, else ~/.claude/bbva-issues) except the tree and the
simulation files, read from the repository given by --repo, the working directory by default.
"""
import ast
import contextlib
import csv
import glob
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks  # noqa: E402
import cardlog  # noqa: E402
import paths  # noqa: E402
import source  # noqa: E402

AGENT_DIR = {"cobranzas": "agents/base", "openpay": "agents/openpay", "hipotecarios": "agents/hipotecarios"}


def fail(msg):
    sys.stderr.write(msg.rstrip() + "\n")
    sys.exit(1)


def pages_dir(override=None):
    return override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues")


def load(path):
    if not os.path.exists(path):
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def norm(s):
    """Comparable text: redaction markers of both records removed, case and spacing folded."""
    s = re.sub(r"\[REDACTED[^\]]*\]|•+", " ", s or "")
    return re.sub(r"[^\w¿?¡!,.]+", " ", s).strip().lower()


def same(a, b):
    a, b = norm(a), norm(b)
    return a == b or (len(a) >= 12 and len(b) >= 12 and (a.startswith(b[:24]) or b.startswith(a[:24])))


# ---------- 1. the tree ----------

def tree(repo, agent, at=None):
    """The Studio content outline of the tree, or with at, as that commit has it (the card's uncommitted work left out)."""
    composer = os.path.join(repo, AGENT_DIR.get(agent, agent), ".composer")
    if not os.path.isdir(composer):
        fail(f"missing {composer}")
    buf = io.StringIO()
    if at:
        with tempfile.TemporaryDirectory() as tmp:
            rel = os.path.join(AGENT_DIR.get(agent, agent), ".composer")
            arch = subprocess.run(["git", "-C", repo, "archive", at, rel], capture_output=True)
            if arch.returncode:
                fail(f"git archive {at} {rel}: " + arch.stderr.decode(errors="replace")[-300:])
            subprocess.run(["tar", "-x", "-C", tmp], input=arch.stdout, check=True)
            with contextlib.redirect_stdout(buf):
                blocks.outline(os.path.join(tmp, rel))
        return buf.getvalue()
    with contextlib.redirect_stdout(buf):
        blocks.outline(composer)
    return buf.getvalue()


# ---------- 2. the source ----------

def listed(v):
    """A test ref's list field, which the CLI writes as a list, as JSON text or as Python list text."""
    if isinstance(v, str) and v.startswith("["):
        for parse in (json.loads, ast.literal_eval):
            try:
                return parse(v)
            except (ValueError, SyntaxError):
                pass
    return v if isinstance(v, list) else ([v] if v else [])


def source_text(src):
    """The card's source, readable: an issue's name, status, description, comments and highlighted lines; a failing
    simulation's name, what failed and its definition."""
    ref = src.get("ref") or {}
    if src.get("kind") == "sim":
        out = [f"# Simulation · {src.get('title') or ''}".rstrip(" ·"),
               f"run: {ref.get('run')} · result: {ref.get('result')} · {ref.get('status')}",
               "", "## What failed", "", src.get("description") or "(nothing recorded)"]
        d = src.get("definition") or {}
        if d:
            out += ["", "## Definition", "", f"group: {d.get('groupDescription') or ''} · categories: {', '.join(d.get('categories') or [])}",
                    "", "### Persona instructions", ""] + [str(m) for m in listed(d.get("messages"))]
            out += ["", "### Expected outcomes", ""] + [f"- {x}" for x in listed(d.get("expectedOutcomes"))]
            out += ["", "### Tag expectations", "", ", ".join(listed(d.get("tagExpectations"))) or "(none)"]
        out += ["", "## Replay"] + [f"- {c['id']}" for c in src.get("conversations") or []]
        return "\n".join(out) + "\n"
    out = [f"# Issue #{src.get('number')} · {src.get('title') or ''}".rstrip(" ·"), f"status: {ref.get('status')}"]
    if ref.get("severity"):
        out.append(f"severity: {ref['severity']}")
    if ref.get("category"):
        out.append(f"category: {ref['category']}")
    out.append("")
    out.append(src.get("description") or "(no description)")
    for c in src.get("comments") or []:
        out.append("")
        out.append(f"## Comment · {c.get('author')} · {c.get('time')}".rstrip(" ·"))
        out.append(c.get("text") or "")
    out.append("")
    out.append("## Linked calls and highlighted lines")
    for c in src.get("conversations") or []:
        out.append(f"- {c['id']}")
        for x in c.get("marked") or []:
            out.append(f"    - {x.get('author')} `{x.get('turn')}`: {x.get('text')}")
    return "\n".join(out) + "\n"


def conversation_part(base, src, cid):
    """One conversation of the source as the briefs print it: header, where it is cached, the transcript."""
    d = source.conv_dir(base, src["number"], cid)
    what = "Replay" if src.get("kind") == "sim" else "Call"
    if not os.path.isdir(d):
        return f"# {what} {cid}\n\n(not cached)\n"
    det = source.details(d)
    rel = det["metadata"].get("release")
    return f"# {what} {cid}" + (f" · release {rel}" if rel else "") + f"\n\ncached at `{d}/`\n\n" + transcript(d, det)


# ---------- 3. the calls ----------

def debug_rows(conv_dir):
    p = os.path.join(conv_dir, "debug.log")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def transcript(conv_dir, details):
    msgs = [e for e in details["events"] if e.get("type") == "message"]
    rows = debug_rows(conv_dir)
    # align debug.log message rows to details messages by text, in order
    aside = {}  # details message index -> list of aside lines that came after it
    di, last_obs = 0, None
    pending, tools = [], []  # tools: the calls of the agent turn being built, numbered tools[0], tools[1], …
    args = source.tool_args(conv_dir)
    def flush(with_tools):
        # observations go under the line they followed; tool calls wait for the agent turn they belong to (a
        # customer line can land between the call and that turn)
        nonlocal pending, tools
        lines = [f"    tools[{k}] {t['name']}" + (f" {json.dumps(t['args'], ensure_ascii=False)}" if t.get("args") is not None else "")
                 for k, t in enumerate(tools)] if with_tools else []
        out, pending = pending + lines, []
        if with_tools:
            tools = []
        return out
    for r in rows:
        k = r["event_type"]
        if k in ("USER_MSG", "AGENT_MSG"):
            j = next((x for x in range(di, min(di + 4, len(msgs))) if same(msgs[x].get("text"), r["message"])), None)
            if j is not None:
                aside.setdefault(j - 1, []).extend(flush(k == "AGENT_MSG"))
                di = j + 1
        elif k == "TOOL_CALL":
            tools.append({"name": r["message"], **({"args": args[r["seq"]]} if r["seq"] in args else {})})
        elif k == "OBSERVATIONS" and r["message"].startswith("Activated"):
            if r["message"] != last_obs:
                pending.append(f"    [obs] {r['message'][len('Activated: '):]}")
            last_obs = r["message"]
    aside.setdefault(len(msgs) - 1, []).extend(flush(True))
    out = []
    turn, role = 0, None
    for i, m in enumerate(msgs):
        if m.get("role") != role:
            turn += 1
            role = m.get("role")
        who = "A" if role == "assistant" else "U"
        out.append(f"{turn} {who} `{m.get('turn')}`: {(m.get('text') or '').replace(chr(10), ' ')}")
        out.extend(aside.get(i, []))
    tags = [t for t in details.get("metadata", {}).get("tags", []) if not t.startswith(("^", "~"))]
    out.append("")
    out.append("tags: " + ", ".join(tags))
    return "\n".join(out) + "\n"


def replay_transcript(result_dir):
    """A simulation replay as a numbered transcript, each line addressed by its debug.log seq."""
    return transcript(result_dir, source.details(result_dir))


SOP_EXAMPLE = re.compile(r"(?ms)^#+ Ejemplo de conversación.*?(?=^#+ |^\*\*\d)")


def sop_text(base):
    """The agent's SOP as markdown, agents/<agent>/sop/sop.md in the pages dir, when the agent has one, without its
    example conversations."""
    p = paths.sop(base)
    return SOP_EXAMPLE.sub("", open(p, encoding="utf-8").read()).strip() + "\n" if os.path.exists(p) else ""


def call_order(src, base, k):
    ids = [c["id"] for c in src.get("conversations") or []]
    with_line = [c["id"] for c in src.get("conversations") or [] if c.get("marked")]
    rest = [i for i in ids if i not in with_line]

    def ts(cid):
        d = source.conv_dir(base, src["number"], cid)
        return source.details(d)["metadata"].get("timestamp") or "" if os.path.isdir(d) else ""
    rest.sort(key=ts, reverse=True)
    return (with_line + rest)[:k]


# ---------- 4. the request ----------

def request_at(conv_dir, turn=None):
    """The compiled request of one agent turn: (request dict, trace seq, the agent message, error). With no turn, the
    conversation's first agent turn; with a customer line's, the first agent turn after it (or the last agent turn when
    the line is the tail)."""
    details = source.details(conv_dir)
    msgs = [e for e in details["events"] if e.get("type") == "message"]
    if turn is None:
        idx = next((i for i, m in enumerate(msgs) if m.get("role") == "assistant"), None)
        if idx is None:
            return None, None, None, "no agent turn in the call"
    else:
        idx = next((i for i, m in enumerate(msgs) if m.get("turn") == turn), None)
        if idx is None:
            return None, None, None, f"line {turn} not in the conversation"
    start = idx
    while idx < len(msgs) and msgs[idx].get("role") != "assistant":
        idx += 1
    if idx >= len(msgs):  # the reporter pointed at the call's tail: the agent's last turn before it
        idx = next((i for i in range(start, -1, -1) if msgs[i].get("role") == "assistant"), None)
        if idx is None:
            return None, None, None, "no agent turn in the call"
    target = msgs[idx]
    rows = debug_rows(conv_dir)
    # the k-th agent message of details.json is the k-th AGENT_MSG row; the text check guards the alignment
    k = sum(1 for m in msgs[:idx] if m.get("role") == "assistant")
    seq, last, seen = None, None, 0
    for r in rows:
        if r["event_type"] == "GOALSDK_RESPOND":
            last = r["seq"]
        elif r["event_type"] == "AGENT_MSG":
            if seen == k:
                if not same(r["message"], target.get("text")):
                    return None, None, target, f"debug.log agent message {seen} does not match {target.get('turn')}"
                seq = last
                break
            seen += 1
    if not seq:
        return None, None, target, f"no GOALSDK_RESPOND row before agent message {target.get('turn')}"
    trace = load(os.path.join(conv_dir, "traces", f"{seq}.trace"))
    for ev in trace.get("traces", []):
        lc = ev.get("llm_chat")
        if isinstance(lc, dict) and "raw_request" in lc:
            rr = lc["raw_request"]
            return (json.loads(rr) if isinstance(rr, str) else rr), seq, target, None
    return None, seq, target, f"traces/{seq}.trace has no llm_chat.raw_request"


def message_text(m):
    c = m.get("content")
    if isinstance(c, list):
        return "\n".join(p.get("text", "") for p in c if isinstance(p, dict))
    return c or ""


def compiled_request(base, n, conv_id, turn=None):
    """The request as the page explores it: the system parts, the tools, the conversation messages, and the
    conversation's agent turns so the page can step through them."""
    conv_dir = source.conv_dir(base, n, conv_id)
    details = source.details(conv_dir)
    turns = [{"turn": e.get("turn"), "text": e.get("text") or ""}
             for e in details["events"] if e.get("type") == "message" and e.get("role") == "assistant"]
    if turn is None:  # the first agent turn the model produced; scripted greetings have no request
        rr = seq = target = err = None
        for t in turns:
            rr, seq, target, err = request_at(conv_dir, t["turn"])
            if rr is not None:
                break
    else:
        rr, seq, target, err = request_at(conv_dir, turn)
    if err and err.startswith("no GOALSDK_RESPOND row"):
        err = "no model call before this agent line: a scripted or verbatim turn"
    out = {"conversation": conv_id, "turn": target.get("turn") if target else None, "trace": seq, "turns": turns, "error": err}
    if rr is None:
        return out
    msgs = rr.get("messages") or rr.get("input") or []
    out["model"] = rr.get("model")
    out["settings"] = {k: rr[k] for k in ("temperature", "reasoning", "max_output_tokens", "service_tier") if k in rr}
    out["system"] = [{"role": m["role"], "text": message_text(m)} for m in msgs if m.get("role") in ("system", "developer")]
    out["messages"] = [{"role": m.get("role") or m.get("type"), "text": message_text(m)} for m in msgs if m.get("role") not in ("system", "developer")]
    tools = []
    for tdef in rr.get("tools") or []:
        f = tdef.get("function", tdef)
        tools.append({"name": f.get("name"), "description": f.get("description") or "", "parameters": f.get("parameters")})
    out["tools"] = tools
    return out


def request_at_reported(base, src, conv_id, turn=None):
    """The compiled request of the agent turn the reporter pointed at: the highlighted line when it is the agent's,
    else the first agent message after it. With turn, that turn instead."""
    conv_dir = source.conv_dir(base, src["number"], conv_id)
    if turn is None:
        ex = next((x for c in src.get("conversations") or [] if c["id"] == conv_id for x in c.get("marked") or []), None)
        if not ex:
            return None, "no highlighted line in this conversation"
        turn = ex.get("turn")
    rr, seq, target, err = request_at(conv_dir, turn)
    if err:
        return None, err
    out = [f"turn: `{target.get('turn')}` · trace: `{os.path.join(conv_dir, 'traces', f'{seq}.trace')}`", ""]
    for m in rr.get("messages") or rr.get("input") or []:
        if m.get("role") in ("system", "developer"):
            out.append(f"## {m['role']}")
            out.append(message_text(m))
            out.append("")
    tools = rr.get("tools") or []
    if tools:
        out.append("## tools")
        for tdef in tools:
            f = tdef.get("function", tdef)
            out.append(f"### {f.get('name')}")
            out.append(f.get("description") or "")
            params = f.get("parameters")
            if params:
                out.append("```json")
                out.append(json.dumps(params, ensure_ascii=False))
                out.append("```")
            out.append("")
    return "\n".join(out) + "\n", None


# ---------- 5. the suite ----------

TAG_RE = re.compile(r'"(!?[a-z][a-z0-9_]*:[a-z0-9_.-]+)"')
CATEGORY_PREFIXES = ("sop:", "path:", "type:", "covers:", "area:")


def suite_files(repo, agent):
    d = os.path.join(repo, AGENT_DIR.get(agent, agent), "simulations")
    if not os.path.isdir(d):
        fail(f"missing {d}")
    files = sorted(f for f in os.listdir(d) if f.endswith(".ts"))
    return [(f, open(os.path.join(d, f), encoding="utf-8").read())
            for f in sorted(files, key=lambda f: (not f.startswith("harness"), f))]


def suite_index(repo, agent, files):
    """One line per simulation, id, name and categories as the CLI lists them, under the file whose text declares the
    id; then harness.ts verbatim. The agent reads the file of the group it picks from disk."""
    agent_dir = os.path.join(repo, AGENT_DIR.get(agent, agent))
    r = subprocess.run([os.path.join(agent_dir, "node_modules", ".bin", "sierra"), "test", "--list", "--json"],
                       cwd=agent_dir, capture_output=True, text=True)
    try:
        sims = json.loads(r.stdout)
    except ValueError:
        fail(f"sierra test --list failed in {agent_dir}: " + (r.stderr or r.stdout).strip()[-400:])
    tests = [(f, text) for f, text in files if f.endswith(".tests.ts")]
    by_file = {}
    for s in sims:
        f = next((f for f, text in tests if f'"{s["id"]}"' in text), "declared outside simulations/")
        by_file.setdefault(f, []).append(s)
    out = []
    for f in [f for f, _ in tests] + [k for k in by_file if k not in dict(tests)]:
        if f not in by_file:
            continue
        out.append(f"## simulations/{f}" if f in dict(tests) else f"## {f}")
        out += [f"- `{s['id']}` · {s['name']} · " + " ".join(s.get("categories") or []) for s in by_file[f]]
        out.append("")
    for f, text in files:
        if not f.endswith(".tests.ts"):
            out += [f"## simulations/{f}", "```ts", text.rstrip("\n"), "```", ""]
    return "\n".join(out) + "\n"


def tags_text(repo, agent, files):
    """Tag literals in the agent's source (not the simulations), each with the file that holds it, and the tags the
    suite asserts."""
    root = os.path.join(repo, AGENT_DIR.get(agent, agent))
    declared = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [x for x in dirnames if x not in ("node_modules", ".composer", "simulations", "build", "alias")
                       and not x.startswith(".")]
        for fn in filenames:
            if not fn.endswith((".ts", ".tsx")) or fn.endswith((".test.ts", ".tests.ts", ".d.ts")):
                continue
            p = os.path.join(dirpath, fn)
            try:
                text = open(p, encoding="utf-8").read()
            except OSError:
                continue
            for m in TAG_RE.finditer(text):
                t = m.group(1).lstrip("!")
                if t.startswith(CATEGORY_PREFIXES):
                    continue
                declared.setdefault(t, set()).add(os.path.relpath(p, root))
    asserted = {}
    for f, text in files:
        for m in TAG_RE.finditer(text):
            t = m.group(1).lstrip("!")
            if not t.startswith(CATEGORY_PREFIXES):
                asserted.setdefault(t, set()).add(f)
    out = ["Declared in the agent's source:", ""]
    for t in sorted(declared):
        out.append(f"- `{t}` · {', '.join(sorted(declared[t]))}")
    out.append("")
    out.append("Asserted by the suite:")
    out.append("")
    for t in sorted(asserted):
        mark = "" if t in declared else " · not in the source"
        out.append(f"- `{t}` · {', '.join(sorted(asserted[t]))}{mark}")
    return "\n".join(out) + "\n"


def call_of_analysis(base, src, analysis):
    """The conversation that holds the analysis's failure turn, else the first of call_order."""
    want = source.failure_turn(analysis) if isinstance(analysis, dict) else None
    for c in src.get("conversations") or []:
        d = source.conv_dir(base, src["number"], c["id"])
        if want and os.path.isdir(d):
            if any(e.get("turn") == want for e in source.details(d)["events"] if e.get("type") == "message"):
                return [c["id"]]
    return call_order(src, base, 1)


# ---------- main ----------

def main(argv):
    if len(argv) < 2:
        fail(__doc__)
    if argv[1] == "--replay":
        d = os.path.abspath(argv[2])
        sys.stdout.write(f"# Replay {os.path.basename(d)}\n\ncached at `{d}/`\n\n" + replay_transcript(d))
        return
    if argv[1] == "--batch":
        opts = dict(zip(argv[1::2], argv[2::2]))
        sys.stdout.write(batch_brief(argv[0], opts["--batch"], os.path.join(pages_dir(opts.get("--pages")), "agents", argv[0])))
        return
    agent, n = argv[0], argv[1]
    opts = dict(zip(argv[2::2], argv[3::2]))
    step = opts.get("--step") or "analysis"
    pages = pages_dir(opts.get("--pages"))
    repo = opts.get("--repo") or os.getcwd()
    k = int(opts.get("--calls") or 3)
    base = os.path.join(pages, "agents", agent)
    iss = source.load(base, n)
    if not iss:
        fail(f"{agent} {n} has no source: no issue in the cache and no source.json in the card")
    history = cardlog.index(pages, agent, n) if opts.get("--history") != "0" else ""
    history = "\n" + history if history else ""
    if step == "strategy":
        sys.stdout.write(strategy_brief(agent, n, base, repo, iss) + history)
        return
    if step == "context":
        sys.stdout.write(context_brief(agent, n, base, repo, iss) + history)
        return
    if step == "resolve":
        sys.stdout.write(resolve_brief(agent, n, base, repo, iss) + history)
        return
    if step != "analysis":
        fail(f"unknown step {step}")
    parts = []
    parts.append(f"# Studio content · {agent} · outline, as HEAD has it\n\n" + tree(repo, agent, "HEAD"))
    sop = sop_text(base)
    if sop:
        parts.append(f"# SOP · {agent}\n\n" + sop)
    parts.append(source_text(iss))
    calls = call_order(iss, base, k)
    for cid in calls:
        parts.append(conversation_part(base, iss, cid))
    if calls and any(c.get("marked") for c in iss.get("conversations") or []):
        req, err = request_at_reported(base, iss, calls[0])
        parts.append("# Request at the reported turn\n\n" + (req if req else f"(unavailable: {err})\n"))
    sys.stdout.write("\n".join(parts) + history)


def run_text(agent, n, base, repo, step):
    """The issue's values for the step skill's Run section: checkout, agent dir, CLI, workspace, the step's runs folder,
    scripts."""
    status_path = paths.status(base, n, "setup")
    st = load(status_path) if os.path.exists(status_path) else {}
    ws = st.get("name") if st.get("state") == "done" and st.get("workspace") else None
    head = f"# Lane · {agent} {n}\n\nThe values the skill's Run section names.\n\n"
    if not ws:
        return head + "This issue has no Studio workspace of its own yet.\n"
    agent_dir = os.path.join(repo, AGENT_DIR.get(agent, agent))
    return head + "\n".join([
        f"- `<agent>`: `{agent}`",
        f"- `<checkout>`: `{repo}`",
        f"- `<agent-dir>`: `{agent_dir}`",
        f"- `<sierra>`: `{os.path.join(agent_dir, 'node_modules', '.bin', 'sierra')}`",
        f"- `<workspace>`: `{ws}`",
        f"- `<runs>`: `{paths.runs(base, n, step)}`",
        f"- `<scripts>`: `{os.path.dirname(os.path.abspath(__file__))}`",
    ]) + "\n"


def strategy_brief(agent, n, base, repo, iss):
    analysis_path = paths.answer(base, n, "analysis")
    if not os.path.exists(analysis_path):
        fail(f"no Analysis yet for {agent} {n}: run the analysis step first ({analysis_path})")
    analysis = load(analysis_path)
    files = suite_files(repo, agent)
    parts = [f"# Simulations · {agent}\n\n" + suite_index(repo, agent, files),
             f"# Tags · {agent}\n\n" + tags_text(repo, agent, files),
             source_text(iss),
             f"# Analysis · {agent} {n}\n\n`{analysis_path}`\n\n```json\n" + json.dumps(analysis, ensure_ascii=False, indent=1) + "\n```\n"]
    for cid in call_of_analysis(base, iss, analysis):
        parts.append(conversation_part(base, iss, cid))
    parts.append(run_text(agent, n, base, repo, "strategy"))
    before = before_fix(base, n)
    if before:
        parts.append(before)
    return "\n".join(parts)


def baseline_files(base, n):
    """The Sim Strategy's before-the-fix regression runs: its first run's list, then the runs of simulations a rerun added."""
    d = paths.runs(base, n, "strategy")
    first = os.path.join(d, "regressions.json")
    added = sorted(glob.glob(os.path.join(d, "regressions-added-*.json")))
    return ([first] if os.path.exists(first) else []) + added


def before_fix(base, n):
    """For a rerun of the Sim Strategy: the guard's red run and the regression runs recorded before the fix, which stay."""
    files = baseline_files(base, n)
    red = paths.guard_red(base, n)
    if not files and not red:
        return ""
    lines = ["# Before the fix · already recorded", "",
             "An earlier run of this step recorded these on the agent before the fix; they stay the card's before counts."]
    if red:
        lines.append(f"- guard red: {red['passed']}/{red['total']} · run {red['run']}")
    for f in files:
        sims = [t.get("name") for t in (load(f).get("tests") or [])]
        lines.append(f"- `{f}`: " + ", ".join(x for x in sims if x))
    k = len([f for f in files if "regressions-added-" in f]) + 1
    lines.append(f"- the next added regression run goes to `{os.path.join(paths.runs(base, n, 'strategy'), f'regressions-added-{k}.json')}`")
    return "\n".join(lines) + "\n"



def context_brief(agent, n, base, repo, iss):
    analysis_path = paths.answer(base, n, "analysis")
    if not os.path.exists(analysis_path):
        fail(f"no Analysis yet for {agent} {n}: run the analysis step first ({analysis_path})")
    analysis = load(analysis_path)
    parts = [f"# Studio content · {agent} · outline\n\n" + tree(repo, agent),
             source_text(iss),
             f"# Analysis · {agent} {n}\n\n`{analysis_path}`\n\n```json\n"
             + json.dumps(analysis, ensure_ascii=False, indent=1) + "\n```\n"]
    strategy_path = paths.answer(base, n, "strategy")
    if os.path.exists(strategy_path):
        parts.append(f"# Sim Strategy · {agent} {n}\n\n`{strategy_path}`\n\n```json\n"
                     + json.dumps(load(strategy_path), ensure_ascii=False, indent=1) + "\n```\n")
    else:
        parts.append(f"# Sim Strategy · {agent} {n}\n\n(not run yet)\n")
    calls = call_of_analysis(base, iss, analysis)
    for cid in calls:
        parts.append(conversation_part(base, iss, cid))
    if calls:
        want = source.failure_turn(analysis)
        req, err = request_at_reported(base, iss, calls[0], want)
        parts.append("# Request at the failure turn\n\n" + (req if req else f"(unavailable: {err})\n"))
    parts.append(run_text(agent, n, base, repo, "context"))
    return "\n".join(parts)


def resolve_brief(agent, n, base, repo, iss):
    analysis_path = paths.answer(base, n, "analysis")
    if not os.path.exists(analysis_path):
        fail(f"no Analysis yet for {agent} {n}: run the analysis step first ({analysis_path})")
    agent_dir = os.path.join(repo, AGENT_DIR.get(agent, agent))
    scripts = os.path.dirname(os.path.abspath(__file__))
    st = load(paths.status(base, n, "setup")) if os.path.exists(paths.status(base, n, "setup")) else {}
    ws = st.get("name") if st.get("state") == "done" and st.get("workspace") else None
    baselines = baseline_files(base, n)
    card = paths.card(base, n)
    m = re.match(r"\s*<!--\s*batch:\s*(\d{4}(?:-\d)?)\s*-->", open(card, encoding="utf-8").read(400)) if os.path.exists(card) else None
    batch = m.group(1) if m else None
    entry = (load(paths.batches(base)) if os.path.exists(paths.batches(base)) else {}).get(batch) or {}
    unset = "none yet: the batch has no worktree and workspace; set it up in the sidebar before merging"
    batch_wt = entry.get("worktree")
    parts = [f"# Lane · {agent} {n}\n\nThe values the skill text names.\n\n"
             f"- `<checkout>`: `{repo}`\n"
             f"- `<agent-dir>`: `{agent_dir}`\n"
             f"- `<sierra>`: `{os.path.join(agent_dir, 'node_modules', '.bin', 'sierra')}`\n"
             f"- `<workspace>`: " + (f"`{ws}`" if ws else "none yet: the issue has no Studio workspace of its own, nothing can run") + "\n"
             f"- `<runs>`: `{paths.runs(base, n, 'resolve')}`\n"
             f"- `<agent>`: `{agent}`; `<n>`: `{n}`\n"
             f"- `<baseline>`: " + (" ".join(f"`{b}`" for b in baselines) if baselines else "none: the Sim Strategy wrote no regression run, so there is nothing to compare regressions against") + "\n"
             f"- `<batch>`: " + (f"`{batch}`" if batch else "none: the card is in no batch") + "\n"
             f"- `<batch-branch>`: " + (f"`{entry['base']}`" if entry.get("base") else ("none: the card is in no batch" if not batch else f"none: batch {batch} has no branch")) + "\n"
             f"- `<batch-workspace>`: " + (f"`{entry['workspace']}`" if entry.get("workspace") else unset) + "\n"
             f"- `<batch-worktree>`: " + (f"`{batch_wt}`" if batch_wt else unset) + "\n"
             f"- `<batch-agent-dir>`: " + (f"`{os.path.join(batch_wt, AGENT_DIR.get(agent, agent))}`" if batch_wt else unset) + "\n"
             f"- `<pages>`: `{base}`\n"
             f"- `<scripts>`: `{scripts}`\n"
             f"- `<references>`: `{os.path.abspath(os.path.join(scripts, '..', 'references'))}`\n",
             source_text(iss)]
    for step, title in (("analysis", "Analysis"), ("strategy", "Sim Strategy"), ("context", "Studio Context Edit")):
        path = paths.answer(base, n, step)
        if os.path.exists(path):
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            parts.append(f"# {title} · {agent} {n}\n\n`{path}`, modified {mtime}\n\n```json\n" + json.dumps(load(path), ensure_ascii=False, indent=1) + "\n```\n")
        else:
            parts.append(f"# {title} · {agent} {n}\n\n(not run yet: `{path}` is missing)\n")
    return "\n".join(parts)


def git_out(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def per_sim(path):
    """name -> "passed/total" from a `sierra test --json` file."""
    try:
        tests = json.load(open(path, encoding="utf-8")).get("tests") or []
    except (OSError, ValueError, AttributeError):
        return {}
    return {t.get("name"): f"{t.get('passed') or 0}/{t.get('total') or 0}" for t in tests}


def batch_brief(agent, batch, base):
    batches = load(paths.batches(base)) if os.path.exists(paths.batches(base)) else {}
    entry = batches.get(batch)
    if not entry or not entry.get("worktree") or not os.path.isdir(entry["worktree"]):
        fail(f"batch {batch} has no worktree: set it up first")
    wt = entry["worktree"]
    scripts = os.path.dirname(os.path.abspath(__file__))
    git_out(wt, "fetch", "-q", "origin", "main")
    main_ws = load(paths.step_file(base, batch, "driver", "main.json")) if os.path.exists(paths.step_file(base, batch, "driver", "main.json")) else {}
    pr = subprocess.run(["gh", "pr", "list", "--head", entry.get("base", ""), "--state", "open", "--json", "number,isDraft,url", "-q", ".[0]"],
                        cwd=wt, capture_output=True, text=True).stdout.strip()
    none_main = "none yet: run mainws.py to make it"
    parts = [f"# Batch · {agent} {batch}\n\nThe values the skill text names.\n\n"
             f"- `<agent>`: `{agent}`; `<batch>`: `{batch}`\n"
             f"- `<batch-branch>`: `{entry.get('base')}`\n"
             f"- `<batch-worktree>`: `{wt}`\n"
             f"- `<batch-workspace>`: `{entry.get('workspace')}`\n"
             f"- `<main-worktree>`: " + (f"`{main_ws['worktree']}`" if main_ws.get("worktree") else none_main) + "\n"
             f"- `<main-workspace>`: " + (f"`{main_ws['workspace']}`" if main_ws.get("workspace") else none_main) + "\n"
             f"- `<pr>`: " + (pr or "none yet") + "\n"
             f"- the batch holds origin/main: " + ("yes" if subprocess.run(["git", "-C", wt, "merge-base", "--is-ancestor", "origin/main", "HEAD"]).returncode == 0 else "no") + "\n"
             f"- check runs go in `{os.path.join(paths.batch_dir(base, batch), 'check')}`\n"
             f"- `<pages>`: `{base}`\n"
             f"- `<scripts>`: `{scripts}`\n"
             f"- `<references>`: `{os.path.abspath(os.path.join(scripts, '..', 'references'))}`\n"]
    oldest = None
    for n in paths.cards(base):
        m = re.match(r"\s*<!--\s*batch:\s*(\d{4}(?:-\d)?)\s*-->", open(paths.card(base, n), encoding="utf-8").read(400))
        if not m or m.group(1) != batch:
            continue
        iss = source.load(base, n) or {}
        setup = load(paths.status(base, n, "setup")) if os.path.exists(paths.status(base, n, "setup")) else {}
        stage = load(paths.step_file(base, n, "resolve", "stage.json")) if os.path.exists(paths.step_file(base, n, "resolve", "stage.json")) else []
        strat = load(paths.answer(base, n, "strategy")) if os.path.exists(paths.answer(base, n, "strategy")) else {}
        gid = (strat.get("guard") or {}).get("id")
        last = stage[-1] if stage else {}
        lines = [f"## #{n} · {iss.get('title', '')}",
                 f"- state: " + (f"{last.get('stage')} {last.get('state')}" + (f" ({last['note']})" if last.get("note") else "") if last else "no resolution yet"),
                 f"- branch: `{setup.get('branch')}`, worktree `{setup.get('worktree')}`",
                 f"- guard: " + (f"`{gid}`" if gid else "none"),
                 "- regression list: " + (", ".join(f"`{x['id']}`" for x in (strat.get("regressions") or {}).get("sims") or []) or "none")]
        runs = []
        red = paths.guard_red(base, n)
        sst = load(paths.status(base, n, "strategy")) if os.path.exists(paths.status(base, n, "strategy")) else {}
        if red:
            runs.append((sst.get("ended") or "", "strategy guard, before the fix", f"{red['passed']}/{red['total']} · run {red['run']}", {}))
        for bl in baseline_files(base, n):
            t = (sst.get("ended") or "") if bl.endswith("/regressions.json") else datetime.fromtimestamp(os.path.getmtime(bl), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            runs.append((t, "strategy regression baseline", f"`{bl}`", per_sim(bl)))
        rr = load(paths.step_file(base, n, "resolve", "runs.json")) if os.path.exists(paths.step_file(base, n, "resolve", "runs.json")) else []
        for r in rr:
            runs.append((r.get("t") or "", f"resolution, stage {r.get('stage')}", f"{r.get('passed')}/{r.get('total')} over {r.get('sims')} sims · run {r.get('run')} · `{r.get('file')}`", per_sim(r.get("file") or "")))
        for t, what, head, sims in runs:
            at = git_out(wt, "rev-list", "-1", "--first-parent", f"--before={t}", "origin/main") if t else ""
            if at and (oldest is None or t < oldest[0]):
                oldest = (t, at)
            lines.append(f"- run {t} · {what} · main at {at[:8] or '?'} · {head}")
            for name, c in sims.items():
                lines.append(f"  - {c} {name}")
        parts.append("\n".join(lines) + "\n")
    if oldest:
        log = git_out(wt, "log", "--first-parent", "--format=%h %cI %s", f"{oldest[1]}..origin/main")
        parts.append("# Main since the oldest card run\n\n" + (log or "(nothing merged since)") + "\n")
    return "\n".join(parts)


if __name__ == "__main__":
    main(sys.argv[1:])
