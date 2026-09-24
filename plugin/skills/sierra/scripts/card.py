"""Render card sections from data, no model in the loop.

Usage:
  card.py ia <agent> <n> [--analysis <file>] [--out <file>|-] [--pages <dir>]
  card.py ss <agent> <n> [--strategy <file>] [--out <file>|-] [--pages <dir>] [--repo <dir>]
  card.py oc <agent> <n> [--context <file>] [--out <file>|-] [--pages <dir>] [--repo <dir>] [--state proposed|applied]
  card.py rs <agent> <n> [--report <file>] [--out <file>|-] [--pages <dir>]

`ia` renders the Analysis section (sections/issue-analysis.html) from the issue-analysis skill's JSON
and the pages-dir cache, and, until the context step has answered, the Studio Context section with the two items the
answer names (the instruction meant to produce the good turn as A, the one that won as B): the issue file for the
reported line, the conversation (source.py) for the turns and tags, debug.log for the tool calls. `call_rows()` gives the whole call
to the page's transcript drawer through the server, the same parse. By default the JSON is `agents/<agent>/cards/<n>/analysis/answer.json` and the section is spliced into
`agents/<agent>/cards/<n>/card.html`, replacing the existing `.ia` block or opening the card after its state
comments. `--out -` prints the section instead.

`ss` renders the Sim Strategy section (sections/sim-changes.html) from the sim-strategy skill's JSON,
`agents/<agent>/cards/<n>/strategy/answer.json`, resolving simulation ids to names and groups in the repo's `*.tests.ts`. Pass
counts stay empty; runs fill them later, except the guard's own 5× run before any edit, shown as its count. `oc` renders the Studio Context and the Studio Context Edit sections
(sections/studio-context.html, studio-context-edit.html) from the context-edit skill's JSON,
`agents/<agent>/cards/<n>/context/answer.json`: the context is the analysis's two items plus the answer's `also` items and `tool`,
the edit is its `edit`; item text, numbering and gates come from the block files in the repo, an item the analysis
marked with the text that holds its marks: the edit's old text, the tree's, or the commit the context step started from.
`rs` renders the Resolution section from the issue-resolution skill's report, `agents/<agent>/cards/<n>/resolve/report.md`:
headings, paragraphs, lists and code blocks, nothing more. `--repo` is the repository root, the working directory by
default.
"""
import csv
import difflib
import glob
import html
import json
import os
import re
import subprocess
import sys
import paths
import source

TOOL_ICON = {"user": "ti-user", "assistant": "ti-robot"}


def fail(msg):
    sys.stderr.write(msg.rstrip() + "\n")
    sys.exit(1)


def pages_dir(override=None):
    return override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues")


def esc(s):
    return html.escape(s or "", quote=False)


def load_json(path):
    if not os.path.exists(path):
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------- the call ----------

def turns_of(details):
    """Speaker turns: consecutive messages of one role form one turn, numbered from 1."""
    turns, cur = [], None
    for e in details["events"]:
        if e.get("type") != "message":
            continue
        role = e.get("role")
        if cur and cur["role"] == role:
            cur["msgs"].append(e)
        else:
            cur = {"n": len(turns) + 1, "role": role, "msgs": [e]}
            turns.append(cur)
    return turns


def locate(turns, turn):
    for t in turns:
        for m in t["msgs"]:
            if m.get("turn") == turn:
                return t, m
    return None, None


def tool_calls(conv_dir, turns):
    """Tool calls from debug.log, {name, args}, keyed by the index of the message they follow. A call belongs to the
    agent turn it precedes, so it is keyed just before that turn's message, found by its spoken text: around a barge-in
    the log orders the customer's line differently from the transcript, so counting rows would drift. Arguments come
    from the agent's own «Invoking tool» log line when it has one (source.tool_args)."""
    path = os.path.join(conv_dir, "debug.log")
    out = {}
    if not os.path.exists(path):
        return out
    flat = [m for t in turns for m in t["msgs"]]
    norm = lambda x: re.sub(r"\s+", " ", x or "").strip()
    pending, pos = [], 0
    args = source.tool_args(conv_dir)
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            kind, msg = row["event_type"], row["message"]
            if kind == "TOOL_CALL":
                pending.append({"name": msg, "args": args.get(row["seq"])})
            elif kind == "AGENT_MSG" and pending:
                spoken = norm(msg)
                j = next((k for k in range(pos, len(flat)) if flat[k].get("role") == "assistant" and norm(flat[k].get("text")) == spoken), None)
                if j is None:
                    continue
                out.setdefault(j - 1, []).extend(pending)
                pending, pos = [], j + 1
    if pending and flat:  # calls after the last spoken line, a closing tool for instance
        out.setdefault(len(flat) - 1, []).extend(pending)
    return out


def tool_text(t):
    """A call as the transcript prints it: name, then its arguments as JSON."""
    return t["name"] + (" " + json.dumps(t["args"], ensure_ascii=False) if t.get("args") is not None else "")


def tool_html(t, spans=(), cls="del", whole_if_none=False):
    """The call as the transcript prints it, the name then the JSON arguments in the arg style, with the spans marked
    where they fall; when none of them matches and whole_if_none, the whole call is marked."""
    args = json.dumps(t["args"], ensure_ascii=False) if t.get("args") is not None else ""
    text = tool_text(t)
    spans = [x for x in spans if x and x in text]
    if not spans and whole_if_none:
        return f'<span class="{cls}">{esc(t["name"])}' + (f' <span class="arg">{esc(args)}</span>' if args else "") + "</span>"
    out = mark_spans(t["name"], [x for x in spans if x in t["name"]], cls)
    if args:
        out += f' <span class="arg">{mark_spans(args, [x for x in spans if x in args], cls)}</span>'
    return out


def parse_path(path):
    """failure.path → (kind, k, arg): ("text", None, None), ("tool", k, None), ("tool", k, argument) or, for a call the
    turn needed and did not make, ("new", None, None)."""
    if (path or "").strip() == "tools[new]":
        return "new", None, None
    m = re.fullmatch(r"tools\[(\d+)\](?:\.([\w.-]+))?", (path or "text").strip())
    if not m:
        return "text", None, None
    return "tool", int(m.group(1)), m.group(2)


def unspoken(conv_dir, turns):
    """The unspoken rest of each agent message the customer cut off, keyed by message index: debug.log holds the
    model's whole reply (GOALSDK_RESPOND «LLM response») and what was spoken (AGENT_MSG); a spoken text that is a
    proper prefix of the reply was interrupted there. Matched by the spoken text, since around a barge-in the log
    orders the customer's line before the agent line it cut."""
    path = os.path.join(conv_dir, "debug.log")
    if not os.path.exists(path):
        return {}
    norm = lambda x: re.sub(r"\s+", " ", x or "").strip()
    replies, by_text = [], {}
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            kind, msg = row["event_type"], row["message"]
            if kind == "GOALSDK_RESPOND" and msg.startswith("LLM response: "):
                replies.append(norm(msg[len("LLM response: "):].strip().strip('"')))
            elif kind == "AGENT_MSG":
                spoken = norm(msg)
                full = next((r for r in reversed(replies[-4:]) if r.startswith(spoken) and len(r) > len(spoken)), None)
                if full:
                    by_text.setdefault(spoken, []).append(full[len(spoken):].strip())
    out = {}
    for i, m in enumerate(m for t in turns for m in t["msgs"]):
        rest = by_text.get(norm(m.get("text"))) if m.get("role") == "assistant" else None
        if rest:
            out[i] = rest.pop(0)
    return out


def cut_html(rest):
    """The never-spoken rest of an interrupted agent message, muted after a scissors mark."""
    if not rest:
        return ""
    return (' <span class="cut" title="The customer cut in here; the rest was never spoken">'
            f'<i class="ti ti-scissors" aria-hidden="true"></i>{esc(rest)}</span>')


def message_index(turns, msg):
    i = 0
    for t in turns:
        for m in t["msgs"]:
            if m is msg:
                return i
            i += 1
    return -1


def call_rows(conv_dir):
    """The whole call for the page's transcript drawer, one parse for both: rows in order, a message as {n (on a
    turn's first message), role, turn, text, cut (the unspoken rest), tools (the calls made right before it,
    {name, args} with args as JSON text)}, the agent's tags as {tags}, calls after the last line as a trailing {tools}."""
    details = source.details(conv_dir)
    turns = turns_of(details)
    tools = tool_calls(conv_dir, turns)
    cuts = unspoken(conv_dir, turns)
    flat = [m for t in turns for m in t["msgs"]]
    index = {id(m): i for i, m in enumerate(flat)}
    first = {id(t["msgs"][0]): t["n"] for t in turns}
    calls = lambda k: [{"name": t["name"], "args": json.dumps(t["args"], ensure_ascii=False) if t.get("args") is not None else None}
                       for t in tools.get(k, [])]
    rows = []
    for e in details["events"]:
        if e.get("type") == "agent_tags":
            rows.append({"tags": e.get("tags") or []})
        elif e.get("type") == "message":
            i = index[id(e)]
            rows.append({"n": first.get(id(e)), "role": e.get("role"), "turn": e.get("turn"), "text": e.get("text") or "",
                         "cut": cuts.get(i), "tools": calls(i - 1)})
    if flat and tools.get(len(flat) - 1):
        rows.append({"tools": calls(len(flat) - 1)})
    return {"metadata": details.get("metadata") or {}, "rows": rows}


# ---------- text marking ----------

def mark_spans(text, spans, cls):
    """Wrap each span (an exact substring) of text in <span class=cls>, escaped; a span given as (text, cls) takes
    its own class."""
    if not spans:
        return esc(text)
    of = {}
    for x in spans:
        t, c = x if isinstance(x, tuple) else (x, cls)
        if t:
            of.setdefault(t, c)
    pat = "|".join(re.escape(t) for t in sorted(of, key=len, reverse=True))
    out, pos = [], 0
    for m in re.finditer(pat, text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<span class="{of[m.group(0)]}">{esc(m.group(0))}</span>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def words(s):
    return s.split()


def join(ws):
    return " ".join(ws)


def diff_rows(bad_text, good_text, bad_spans):
    """Return (kind, bad_html, good_html): kind is 'same', 'diff' (one row) or 'replace' (bad + good rows)."""
    if bad_text.strip() == good_text.strip():
        return "same", mark_spans(bad_text, bad_spans, "del"), None
    a, b = words(bad_text), words(good_text)
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    tags = {op for op, *_ in ops if op != "equal"}
    if tags <= {"insert"} or tags <= {"delete"}:
        parts = []
        for op, i1, i2, j1, j2 in ops:
            if op == "equal":
                parts.append(esc(join(a[i1:i2])))
            elif op == "insert":
                parts.append(f'<span class="ins">{esc(join(b[j1:j2]))}</span>')
            else:
                parts.append(f'<span class="del">{esc(join(a[i1:i2]))}</span>')
        return "diff", " ".join(parts), None
    spans = bad_spans or [bad_text]
    shared = sum(i2 - i1 for op, i1, i2, _, _ in ops if op == "equal")
    if shared < len(b) / 2:
        return "replace", mark_spans(bad_text, spans, "del"), f'<span class="ins">{esc(good_text)}</span>'
    # an equal run of one or two words between two changes reads as part of the change
    kinds = []
    for k, (op, i1, i2, j1, j2) in enumerate(ops):
        if op == "equal" and i2 - i1 <= 2 and 0 < k < len(ops) - 1:
            op = "insert"
        kinds.append((op, j1, j2))
    good, buf = [], []
    def flush():
        if buf:
            good.append(f'<span class="ins">{esc(join(buf))}</span>'); buf.clear()
    for op, j1, j2 in kinds:
        if op == "equal":
            flush(); good.append(esc(join(b[j1:j2])))
        elif op in ("insert", "replace"):
            buf.extend(b[j1:j2])
    flush()
    return "replace", mark_spans(bad_text, spans, "del"), " ".join(good)


# ---------- rows ----------

def row(cls, n, icon, body):
    num = str(n) if n else ""
    ic = f'<i class="ti {icon}" aria-hidden="true"></i>' if icon else ""
    c = f' class="row{(" " + cls) if cls else ""}"'
    return f'<div{c}><span class="n">{num}{ic}</span><span>{body}</span></div>'


def gap(n):
    if n <= 0:
        return ""
    return row("sys gap", None, None, f"{n} turn{'s' if n != 1 else ''}")


def clause_rows(then):
    """What follows from the good turn, one row each, in their own style: not an elision, not a note."""
    return [row("then", None, "ti-corner-down-right", esc(c)) for c in then or [] if c and c.strip()]


def tags_row(details, analysis):
    tags = [t for t in details.get("metadata", {}).get("tags", []) if t.startswith(("resultado:", "resolucion:", "motivo"))]
    shown = " · ".join(esc(t.replace(":", ": ", 1)) for t in tags)
    m = re.search(r"wanted: `([^`]+)`, actual: `([^`]+)`", analysis.get("verdict", ""))  # the tag verdict's fixed wording
    if m:
        return row("diff", None, "ti-webhook", f'<span class="del">{esc(m.group(2))}</span> <span class="ins">{esc(m.group(1))}</span>' + (f" · {shown}" if shown else ""))
    return row("", None, "ti-webhook", shown) if shown else ""


# ---------- the section ----------

def render_ia(agent, n, analysis, pages):
    base = os.path.join(pages, "agents", agent)
    src = source.load(base, n) or {}
    fid = source.failure_turn(analysis)
    convs = src.get("conversations") or []
    examples = [(c["id"], x) for c in convs for x in c.get("marked") or []]
    conv_id = next((c["id"] for c in convs if any(x.get("turn") == fid for x in c.get("marked") or [])), None)
    # the conversation that holds the failure turn: first the one with the reported line, then every other
    candidates = ([conv_id] if conv_id else []) + [c["id"] for c in convs if c["id"] != conv_id]
    details = turns = ft = fm = None
    for cid in candidates:
        p = source.conv_dir(base, n, cid)
        if not os.path.isdir(p):
            continue
        d = source.details(p)
        t = turns_of(d)
        ft, fm = locate(t, fid)
        if ft:
            details, turns, conv_id = d, t, cid
            break
    if not ft:
        fail(f"failure turn {fid} not found in any cached conversation of {agent} {n}")
    conv_dir = source.conv_dir(base, n, conv_id)
    tools = tool_calls(conv_dir, turns)
    cuts = unspoken(conv_dir, turns)
    flat = [m for t in turns for m in t["msgs"]]
    turn_of_msg = {id(m): t for t in turns for m in t["msgs"]}
    fi = message_index(turns, fm)

    reported = {x["turn"]: x for cid, x in examples if cid == conv_id}
    # the customer turn before the failure
    prev_i = next((i for i in range(fi - 1, -1, -1) if flat[i].get("role") == "user"), None)

    prev_turn = {message_index(turns, m) for m in turn_of_msg[id(flat[prev_i])]["msgs"]} if prev_i is not None else set()
    before = sorted({i for i, m in enumerate(flat) if m.get("turn") in reported and i < fi} | prev_turn)
    after = sorted(i for i, m in enumerate(flat) if m.get("turn") in reported and i > fi)

    numbered = set()

    def turn_row(i, cls=""):
        m = flat[i]
        t = turn_of_msg[id(m)]
        num = None if t["n"] in numbered else t["n"]
        numbered.add(t["n"])
        ex = reported.get(m.get("turn"))
        body = mark_spans(m.get("text") or "", [ex["text"]] if ex and ex["text"] and ex["text"] != (m.get("text") or "") else [], "hl") if ex else esc(m.get("text") or "")
        if ex and ex.get("text") == (m.get("text") or ""):
            body = f'<span class="hl">{body}</span>'
        return row(cls, num, TOOL_ICON.get(m.get("role"), "ti-robot"), body + cut_html(cuts.get(i)))

    fkind, fk, farg = parse_path(analysis["failure"].get("path"))
    bad = analysis["failure"].get("bad") or []
    good_tools = analysis["good"].get("tools") or []

    def tool_rows(i, failing=False):
        """The calls that follow message i; when failing, the pointed call is red and the good row follows it."""
        rows_ = []
        for k, t in enumerate(tools.get(i, [])):
            if failing and k == fk:
                spans = bad or ([json.dumps(t["args"].get(farg), ensure_ascii=False)] if farg and isinstance(t.get("args"), dict) and farg in t["args"] else [])
                rows_.append(row("bad tool", None, "ti-tool", tool_html(t, spans, whole_if_none=True)))
                fix = good_tools[fk] if fk < len(good_tools) else None
                rows_.append(row("good tool", None, "ti-tool", tool_html(fix, cls="ins", whole_if_none=True) if fix
                                 else f'<span class="ins">{esc(analysis["good"]["text"])}</span>'))
            else:
                rows_.append(row("", None, "ti-tool", tool_html(t)))
        return rows_

    rows = []
    shown_turns = lambda idx: turn_of_msg[id(flat[idx])]["n"]
    last = 0  # turn number of the last shown turn
    for i in before:
        if shown_turns(i) != last:
            rows.append(gap(shown_turns(i) - 1 - last))
        rows.append(turn_row(i))
        rows += tool_rows(i, failing=(fkind == "tool" and i == fi - 1))
        last = shown_turns(i)
    rows.append(gap(ft["n"] - 1 - last))
    # the failure turn: earlier messages of the same turn plain, the pointed message marked
    for m in ft["msgs"]:
        if m is fm:
            break
        rows.append(turn_row(message_index(turns, m)))
    if fkind == "tool":
        # the calls sit under the message before the turn, which is shown when it is the customer's turn before it;
        # otherwise they are drawn here, right above the turn
        if fi - 1 not in before:
            rows += tool_rows(fi - 1, failing=True)
        rows.append(turn_row(fi))
    else:
        # the calls the good turn adds to the ones the turn made, drawn right above it
        made = [tool_text(t) for t in tools.get(fi - 1, [])]
        for t in good_tools:
            if tool_text(t) not in made:
                rows.append(row("good tool", None, "ti-tool", tool_html(t, cls="ins", whole_if_none=True)))
        fm_text, good_text, rest = fm.get("text") or "", analysis["good"]["text"], cuts.get(fi)
        squash = lambda x: re.sub(r"\s+", " ", x or "").strip()
        if rest and squash(good_text) == squash(fm_text + " " + rest):
            good_text = fm_text  # the model wrote the good turn and the customer cut it: nothing to add, the cut mark tells it
        kind, bad_html, good_html = diff_rows(fm_text, good_text, bad)
        bad_html += cut_html(rest)
        num = None if ft["n"] in numbered else ft["n"]
        numbered.add(ft["n"])
        if kind == "same":  # the failing turn is always marked as such, span or no span
            rows.append(row("bad", num, "ti-robot", bad_html))
        elif kind == "diff":
            rows.append(row("diff", num, "ti-robot", bad_html))
        else:
            rows.append(row("bad", num, "ti-robot", bad_html))
            rows.append(row("good", None, "ti-robot", good_html))
    if analysis["failure"].get("moved"):
        rows.append(row("moved", None, "ti-arrow-back-up", esc(analysis["failure"]["moved"])))
    rows += clause_rows(analysis["good"].get("then"))
    last = ft["n"]
    for i in after:
        rows.append(gap(shown_turns(i) - 1 - last))
        rows.append(turn_row(i))
        last = shown_turns(i)
    rows.append(tags_row(details, analysis))

    verdict = re.sub(r"`([^`]+)`", lambda m: f"<code>{esc(m.group(1))}</code>", esc(analysis["verdict"]))
    out = ['<div class="ia">']
    out.append(f'\n<div class="top2">\n  <div>\n    <div class="said">{verdict}</div>\n  </div>\n</div>')
    out.append(f'\n<div class="part" data-conv="{html.escape(conv_id, quote=True)}">\n  <h4>Conversation</h4>\n  <div class="body">')
    out += ["    " + r for r in rows if r]
    out.append("  </div>\n</div>\n</div>")
    return "\n".join(out) + "\n"


def block_end(text, start):
    """Index just past the </div> that closes the div opening at start, by counting div tags."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", text[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            end = start + m.end()
            return end + 1 if text[end:end + 1] == "\n" else end
    return len(text)


SECTION_START = re.compile(r'\n[ \t]*<div class="(ss|so|si|oc)\b')
SECTION_CLASS = re.compile(r'<div class="(ss|so|si|oc)\b')


def block_children(text, start):
    """(begin, end) of each direct child div of the div opening at start, by counting div tags."""
    depth, out, begin = 0, [], None
    for m in re.finditer(r"<div\b|</div>", text[start:]):
        if m.group(0) == "<div":
            depth += 1
            if depth == 2:
                begin = start + m.start()
        else:
            depth -= 1
            if depth == 1 and begin is not None:
                out.append((begin, start + m.end()))
                begin = None
            if depth == 0:
                break
    return out


def _splice_text(text, section):
    """Replace the .ia block, or open the card with it after its state comments. Hand-written cards come in three
    shapes: the block closed before the next section; the sections nested inside the block, where every child of
    the block that holds a section stays and the rest goes; the block left unclosed, bounded by the next section."""
    i = text.find('<div class="ia">')
    if i >= 0:
        close = block_end(text, i)
        nxt = SECTION_START.search(text, i + 1)
        start_next = nxt.start() + 1 if nxt else len(text)
        if start_next >= close - 2:
            return text[:i] + section + text[close:]
        children = block_children(text, i)
        kept = "".join(text[b:e] + "\n" for b, e in children if SECTION_CLASS.search(text, b, e))
        balanced = len(re.findall(r"<div\b", text)) == len(re.findall(r"</div>", text))
        tail = close if balanced else (children[-1][1] if children else start_next)  # an unclosed block has no closer to skip
        return text[:i] + section + kept + text[tail:]
    head = re.match(r"(?:<!--.*?-->\n)*", text).group(0)
    return head + section + text[len(head):]


AGENT_DIR = {"cobranzas": "agents/base", "openpay": "agents/openpay", "hipotecarios": "agents/hipotecarios"}


# ---------- Sim Strategy ----------

def sim_index(agent_dir):
    """id -> (name, group, file) from the agent's *.tests.ts."""
    idx = {}
    for f in sorted(glob.glob(os.path.join(agent_dir, "**", "*.tests.ts"), recursive=True)):
        if "node_modules" in f or ".composer" in f:
            continue
        t = open(f, encoding="utf-8").read()
        g = re.search(r'describe\(\s*"([^"]+)"', t)
        group = g.group(1) if g else os.path.basename(f)
        rel = os.path.relpath(f, agent_dir)
        for m in re.finditer(r'\bid:\s*"([^"]+)"[\s\S]{0,400}?\bname:\s*"([^"]+)"', t):
            idx.setdefault(m.group(1), (m.group(2), group, rel))
        for m in re.finditer(r'test\(\s*"([^"]+)",\s*\{[\s\S]{0,200}?\bname:\s*"([^"]+)"', t):
            idx.setdefault(m.group(1), (m.group(2), group, rel))
    return idx


def text_diff(old, new):
    return f'<span class="del">{esc(old)}</span> <span class="ins">{esc(new)}</span>'


def render_ss(agent, n, strategy, pages, repo):
    idx = sim_index(os.path.join(repo, AGENT_DIR.get(agent, agent)))
    chev = '<i class="ti ti-chevron-right" aria-hidden="true"></i>'
    out = ['<div class="ss">']
    red = paths.guard_red(paths.agent(pages, agent), n)
    guard = (strategy.get("guard") or {}).get("id")

    def head(cls, name_html, group, res="", gist="", open_=False):
        return (f'<details class="sim {cls}"{" open" if open_ else ""}>\n  <summary>\n    <div class="n">{res}</div>\n'
                f'    <div><div class="nmrow"><div class="nm">{chev}<span>{name_html}</span></div>'
                + (f'<div class="crumb"><i class="ti ti-folder" aria-hidden="true"></i>{esc(group)}</div>' if group else "") + '</div>'
                + (f'<div class="gist">{esc(gist)}</div>' if gist else "") + "</div>\n  </summary>")

    def exp(body):
        return f'      <div class="exp"><span class="n"></span><span>{body}</span></div>'

    for k, sim in enumerate(strategy.get("sims", [])):
        known = idx.get(sim.get("id") or "", (None, None, None))
        name = sim.get("name") or {}
        old, new = name.get("old") or known[0], name.get("new")
        group = sim.get("group") or known[1] or ""
        action = sim.get("action")
        cls = {"add": "add", "modify": "mod", "delete": "del"}.get(action, action)
        if action == "add":
            name_html = esc(new or old or sim.get("id"))
        elif new and old and new != old:  # a renamed modification stays in the modify colour; the old name is an aside
            name_html = f'{esc(new)} <s class="old">{esc(old)}</s>'
        else:
            name_html = esc(old or new or sim.get("id"))
        res = '<span class="res"></span>'
        if red and sim.get("id") == guard:
            tone = "ok" if red["passed"] == red["total"] else "flaky" if red["passed"] else "ko"
            res = f'<span class="res {tone}" title="before the fix · {esc(red["run"] or "")}">{red["passed"]}/{red["total"]}</span>'
        out.append(head(cls, name_html, group, res if action != "delete" else "", sim.get("gist") or "", open_=k == 0))
        if action == "delete":
            out.append(f'  <div class="body">\n    <div class="line"><span class="k">covered by</span><span class="gist">{esc(sim.get("covered_by"))}</span></div>\n  </div>\n</details>')
            continue
        pe = sim.get("persona") or {}
        prow = []
        if pe.get("why"):
            prow.append(exp(f'<span class="judge">{esc(pe["why"])}</span>'))
        if pe.get("instructions"):
            prow.append(exp(f'<span class="ins">{esc(pe["instructions"])}</span>'))
        for ch in pe.get("changes") or []:
            prow.append(exp(text_diff(ch.get("old", ""), ch.get("new", ""))))
        for j, t in enumerate(pe.get("openingTurns") or []):
            prow.append(exp(f'<span class="k">opening {j + 1}</span> <span class="ins">{esc(t)}</span>'))
        if pe.get("mockUserId"):
            prow.append(f'      <div class="exp"><span class="n"></span><span class="tags"><span class="k">mock user</span><span class="tag">{esc(pe["mockUserId"])}</span></span></div>')
        if prow:
            out.append('  <div class="so">\n  <details class="part">\n    <summary><h4>' + chev + 'Persona</h4></summary>\n    <div class="body">')
            out += prow
            out.append('    </div>\n  </details>\n  </div>')
        ex = sim.get("expectations") or {}
        rows = []
        for e in ex.get("kept", []):
            rows.append(exp(esc(e)))
        for e in ex.get("reworded", []):
            rows.append(exp(text_diff(e.get("old", ""), e.get("new", ""))))
        for e in ex.get("added", []):
            rows.append(exp(f'<span class="ins">{esc(e)}</span>'))
        for e in ex.get("removed", []):
            rows.append(exp(f'<span class="del">{esc(e)}</span>'))
        tg = sim.get("tags") or {}
        tags = ([f'<span class="tag">{esc(t)}</span>' for t in tg.get("kept", [])]
                + [f'<span class="tag rm">{esc(t)}</span>' for t in tg.get("removed", [])]
                + [f'<span class="tag ins">{esc(t)}</span>' for t in tg.get("added", [])])
        if tags:
            rows.append(f'      <div class="exp"><span class="n"></span><span class="tags">{"".join(tags)}</span></div>')
        out.append('  <div class="so">\n  <details class="part">\n    <summary><h4>' + chev + 'Expectations</h4></summary>\n    <div class="body">')
        out += rows
        out.append('    </div>\n  </details>\n  </div>\n</details>')
    reg = strategy.get("regressions") or {}
    if reg.get("sims"):  # the simulations the change could break, with their baseline counts when the run file is there
        base_path = os.path.join(paths.runs(paths.agent(pages, agent), n, "strategy"), "regressions.json")
        base_file = load_json(base_path) if os.path.exists(base_path) else {}
        counts = {t.get("name"): t for t in base_file.get("tests") or []}
        rows, green, known_n = [], 0, 0
        for r in reg["sims"]:
            nm = idx.get(r.get("id") or "", (None,))[0] or r.get("id")
            t = counts.get(nm) or {}
            res = '<span class="res"></span>'
            if t.get("total"):
                known_n += 1
                full = t.get("passed") == t.get("total")
                green += full
                res = f'<span class="res {"ok" if full else "flaky" if t.get("passed") else "ko"}">{t.get("passed")}/{t.get("total")}</span>'
            rows.append(head("reg", esc(nm), "", res))
            rows.append(f'  <div class="body"><div class="gist">{esc(r.get("why"))}</div></div>\n</details>')
        top = f'<span class="res {"ok" if known_n and green == known_n else "flaky"}">{green}/{known_n}</span>' if known_n else '<span class="res"></span>'
        out.append(head("reg", "Regression list", "", top))
        out += rows
        out.append("</details>")
    for red in strategy.get("expected_reds", []):
        known = idx.get(red.get("id") or "", (None, None, None))
        out.append(head("reg", esc(known[0] or red.get("id")), known[1] or "", '<span class="res"></span>'))
        out.append(f'  <div class="body">\n    <div class="line"><span class="k">expected red</span><span class="gist">{esc(red.get("why"))}</span></div>\n  </div>\n</details>')
    out.append("</div>")
    return "\n".join(out) + "\n"


# ---------- Studio Context ----------

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks as _blocks  # noqa: E402

KIND_ICON = {"section": "ti-folder", "journey": "ti-route", "component": "ti-puzzle", "rules": "ti-list-check",
             "condition": "ti-git-branch", "glossary": "ti-book", "policies": "ti-gavel",
             "response_phrasing": "ti-message-language"}


def block_rows(repo, agent, file, at=None):
    """All outline rows of one block file: list of (names, ords, ptr, text), plus the file's kind. With at, the file as
    that commit has it."""
    path = os.path.join(repo, AGENT_DIR.get(agent, agent), file)
    if at:
        r = subprocess.run(["git", "-C", repo, "show", f"{at}:{os.path.join(AGENT_DIR.get(agent, agent), file)}"], capture_output=True, text=True)
        if r.returncode:
            fail(f"missing {file} at {at}")
        d = json.loads(r.stdout)
    elif not os.path.exists(path):
        fail(f"missing {path}")
    else:
        d = _blocks.load(path)
    if "/components/" in path.replace(os.sep, "/"):
        top, kind = os.path.basename(os.path.dirname(path)), "component"
    else:
        top, kind = d.get("name") or d.get("entry_name") or d.get("type"), d.get("type") or "section"
    return list(_blocks.walk(d, [top] if top else [], [], "")), kind


def find_row(rows, pointer):
    for r in rows:
        if r[2] == pointer:
            return r
    for r in rows:
        if r[2].startswith(pointer) and r[2][len(pointer):] in (".value", ".item", ".text"):
            return r
    fail(f"pointer {pointer} not in block")


def siblings(rows, row):
    """Rows at the same list level as row, in order."""
    ptr = row[2]
    m = re.match(r"^(.*)\[\d+\]([^\[\]]*)$", ptr)
    if not m:
        return [row]
    pat = re.compile("^" + re.escape(m.group(1)) + r"\[\d+\]" + re.escape(m.group(2)) + "$")
    return [r for r in rows if pat.match(r[2])]


def gate_of(rows, row):
    """The nearest `si` row whose names prefix the row's names: list of (keyword, text)."""
    best = None
    for r in rows:
        if r[1] and r[1][-1] == "si" and row[0][:len(r[0])] == r[0] and r[2].rsplit(".condition", 1)[0] and row[2].startswith(r[2].rsplit(".condition", 1)[0]):
            if best is None or len(r[0]) >= len(best[0]):
                best = r
    if not best:
        return []
    text = best[3]
    parts = re.split(r" (O|Y) ", text)
    out, kw = [], "if"
    for i, p in enumerate(parts):
        if p in ("O", "Y"):
            kw = "or" if p == "O" else "and"
            continue
        out.append((kw, p))
    return out


def item_html(text, spans=None, cls=None):
    """Item text with {{tool:…:Name}} as mono and the spans marked in the role's class."""
    body = mark_spans(text or "", spans or [], cls or "a")
    return re.sub(r"\{\{tool:[^}]*:([^}:]+)\}\}", lambda m: f'<span class="tool">{m.group(1)}</span>', body)


def sentences(text):
    return [x for x in re.split(r"(?<=[.;:!?])\s+", text.strip()) if x]


def elided(text, spans=None, cls=None, limit=240):
    """A long item read at a glance: the sentences that hold a span stay, marked; without spans the first sentence
    stays; each run of the rest folds into «(…)» that shows it on hover. A short item stays whole."""
    text = text or ""
    if len(text) <= limit:
        return item_html(text, spans, cls)
    ss = sentences(text)
    flat = [s[0] if isinstance(s, tuple) else s for s in spans or []]
    keep = [any(t and (t in x or x in t) for t in flat) for x in ss] if spans else [i == 0 for i in range(len(ss))]
    if all(keep) or not any(keep):  # a span across sentences: the whole item, marked
        return item_html(text, spans, cls)
    out, buf, run = [], [], []
    def flush():
        if buf:
            out.append(f'<span class="el" title="{html.escape(" ".join(buf), quote=True)}">(…)</span>'); buf.clear()
        if run:
            out.append(item_html(" ".join(run), spans, cls)); run.clear()
    for x, k in zip(ss, keep):
        if k:
            if buf:
                flush()
            run.append(x)
        else:
            if run:
                flush()
            buf.append(x)
    flush()
    return " ".join(out)


def edit_diff(old, new):
    """The edited item read once: sentence-level diff, a rewritten sentence as one del and one ins, a lightly
    touched sentence as a word diff inside it."""
    a, b = sentences(old), sentences(new)
    parts = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            parts.append(item_html(" ".join(a[i1:i2])))
            continue
        if op == "replace" and i2 - i1 == 1 and j2 - j1 == 1:
            wa, wb = words(a[i1]), words(b[j1])
            sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
            if sm.ratio() >= 0.6:
                inner = []
                for wop, x1, x2, y1, y2 in sm.get_opcodes():
                    if wop == "equal":
                        inner.append(item_html(join(wa[x1:x2])))
                    else:
                        if x2 > x1:
                            inner.append(f'<span class="del">{item_html(join(wa[x1:x2]))}</span>')
                        if y2 > y1:
                            inner.append(f'<span class="ins">{item_html(join(wb[y1:y2]))}</span>')
                parts.append(" ".join(inner))
                continue
        if i2 > i1:
            parts.append(f'<span class="del">{item_html(" ".join(a[i1:i2]))}</span>')
        if j2 > j1:
            parts.append(f'<span class="ins">{item_html(" ".join(b[j1:j2]))}</span>')
    return " ".join(parts)


def num_of(row):
    o = row[1]
    return f"{o[-1]}." if o and isinstance(o[-1], int) else "-"


def crumb(names, kind):
    parts = []
    for i, nm in enumerate(names):
        last = i == len(names) - 1
        icon = KIND_ICON.get(kind, "ti-folder") if i == 0 else "ti-file-text"
        parts.append(f'<span{" class=\"cur\"" if last else ""}><i class="ti {icon}" aria-hidden="true"></i>{esc(nm)}</span>')
    return '<h3 class="crumb">' + '<span class="sep">›</span>'.join(parts) + "</h3>"


def gate_html(gate):
    if not gate:
        return ""
    ps = "".join(f'<p><span class="k"><i class="ti ti-eye" aria-hidden="true"></i>{kw}</span><span>{esc(t)}</span></p>' for kw, t in gate)
    return f'    <div class="gate">{ps}</div>\n'


def item_row(cls, r, body):
    return f'    <div class="row {cls}"><span class="n">{num_of(r)}</span><span>{body}</span></div>'


def section_rows(rows, target, on_html):
    """Rows of one block body: the on rows (on_html is one html for the target, or {pointer: html} for several
    items of the same list), their neighbours dim and elided, the rest collapsed into gap rows."""
    ons = on_html if isinstance(on_html, dict) else {target[2]: on_html}
    sibs = siblings(rows, target)
    if target not in sibs:
        sibs = [target]
    nb = set()
    for i, r in enumerate(sibs):
        if r[2] in ons:
            nb |= {sibs[j][2] for j in (i - 1, i + 1) if 0 <= j < len(sibs)}
    out, skipped = [], 0
    def flush():
        nonlocal skipped
        if skipped:
            out.append(f'    <div class="row gap"><span class="n"></span><span>{skipped} item{"s" if skipped != 1 else ""}</span></div>')
            skipped = 0
    for r in sibs:
        if r[2] in ons:
            flush(); out.append(item_row("on", r, ons[r[2]]))
        elif r[2] in nb:
            flush(); out.append(item_row("dim", r, elided(r[3])))
        else:
            skipped += 1
    flush()
    return out


def composer_file(file):
    """An analysis answer's file as the agent directory holds it: a block file, which the outline names without
    .composer/, under .composer/; a code file as given."""
    return os.path.join(".composer", file) if file and file.endswith(".json") else file


def context_of_analysis(analysis):
    """The Studio Context entries an issue-analysis answer carries: the instruction meant to produce the good turn as
    role A, the one that produced the bad turn as role B. A `new` behaviour has no item and draws nothing."""
    ctx = analysis.get("context") or {}
    out = []
    w = ctx.get("wanted") or {}
    if w.get("pointer") and w.get("file") and w.get("state") != "new":
        e = {"file": composer_file(w["file"]), "pointer": w["pointer"], "role": "A", "spans": [w["span"]] if w.get("span") else []}
        if w.get("present") is False:
            e["note"] = "absent at the turn"
        elif w.get("state") == "tangential":
            e["note"] = "tangential"
        out.append(e)
    b = ctx.get("won") or {}
    if b.get("pointer") and b.get("file"):
        out.append({"file": composer_file(b["file"]), "pointer": b["pointer"], "role": "B", "spans": [b["span"]] if b.get("span") else []})
    return out


def before_edit(repo, agent, entry, target, edit, at):
    """The item's text as the turn had it: the first of the edit's old text (when the edit is on this item), the tree's text
    and the text at commit at that holds every span of the entry; the tree's when none does."""
    spans = [x for x in entry.get("spans") or [] if x]
    if not spans:
        return target
    def holds(t):
        t = " ".join((t or "").split())
        return all(" ".join(x.split()) in t for x in spans)
    texts = []
    ep = edit.get("pointer") or ""
    if edit.get("file") == entry["file"] and edit.get("old") and ep and (target[2] == ep or target[2][len(ep):] in (".value", ".item", ".text") and target[2].startswith(ep)):
        texts.append(edit["old"])
    texts.append(target[3])
    if at:
        try:
            texts.append(find_row(block_rows(repo, agent, entry["file"], at)[0], entry["pointer"])[3])
        except SystemExit:
            pass
    return next((t for t in texts if holds(t)), target[3])


def render_oc(agent, n, ctx, pages, repo, state="proposed", at=None):
    """(Studio Context html, Studio Context Edit html) from {context: [{file, pointer, role, spans, note}], tool,
    edit, cause}. The Studio Context's items are the tree's, each on item's text the one before_edit finds. Entries of one list of items share a section; the on item is marked in its role's colour, its
    neighbours are dim and elided, the rest of the list is a count."""
    sections = []
    groups = []
    edit0 = ctx.get("edit") or {}
    for entry in ctx.get("context", []):
        rows, kind = block_rows(repo, agent, entry["file"])
        target = find_row(rows, entry["pointer"])
        role = (entry.get("role") or "A").lower()
        spans = [(x, role) for x in entry.get("spans") or []]
        text = before_edit(repo, agent, entry, target, edit0, at)
        g = next((g for g in groups if g["file"] == entry["file"] and target in siblings(g["rows"], g["target"])), None)
        if g:
            g["spans"][target[2]] = g["spans"].get(target[2], []) + spans
            g["on"][target[2]] = elided(text, g["spans"][target[2]], role)
            g["notes"] += [entry["note"]] if entry.get("note") else []
            continue
        groups.append({"file": entry["file"], "rows": rows, "kind": kind, "target": target,
                       "spans": {target[2]: spans}, "on": {target[2]: elided(text, spans, role)},
                       "notes": [entry["note"]] if entry.get("note") else []})
    for g in groups:
        rows, target = g["rows"], g["target"]
        gate = gate_html(gate_of(rows, target))
        body = section_rows(rows, target, g["on"])
        note = "".join(f'<span class="state">{esc(t)}</span>' for t in g["notes"])
        sections.append(f'<section class="sec">\n  <header>{crumb(target[0], g["kind"])}{note}</header>\n  <div class="body">\n{gate}' + "\n".join(body) + "\n  </div>\n</section>")
    tool = ctx.get("tool") or {}
    if tool.get("name"):
        code = f'<code>{esc(tool["file"])}</code>' if tool.get("file") else ""
        text = tool.get("text") or tool.get("why") or ""
        sections.append(f'<section class="sec">\n  <header><h3 class="crumb"><span class="cur"><i class="ti ti-tool" aria-hidden="true"></i>{esc(tool["name"])}</span></h3>{code}</header>\n  <div class="body">\n    <div class="row on"><span class="n"></span><span>{esc(text)}</span></div>\n  </div>\n</section>')
    context = '<div class="oc ctx">\n' + "\n".join(sections) + "\n</div>\n"

    edit = ctx.get("edit") or {}
    edit_html = ""
    if edit.get("file"):
        rows, kind = block_rows(repo, agent, edit["file"])
        if edit.get("old") is not None:
            target = find_row(rows, edit["pointer"])
            if edit.get("new") is None:
                on = f'<span class="del">{item_html(edit["old"])}</span>'
            else:
                on = edit_diff(edit["old"], edit["new"])
            body = section_rows(rows, target, on)
            gate = gate_html(gate_of(rows, target))
            names = target[0]
        else:
            after = find_row(rows, edit["after"]) if edit.get("after") else None
            on = f'<span class="ins">{item_html(edit.get("new"))}</span>'
            body = []
            if after:
                body.append(item_row("dim", after, elided(after[3])))
            body.append(f'    <div class="row on"><span class="n">-</span><span>{on}</span></div>')
            gate = gate_html(gate_of(rows, after)) if after else ""
            names = after[0] if after else [edit.get("path") or ""]
        label = " · ".join(x for x in (ctx.get("cause"), state) if x)  # why the edit, then its state
        edit_html = (f'<div class="oc edit">\n<section class="sec">\n  <header>{crumb(names, kind)}<span class="state">{esc(label)}</span></header>\n'
                     f'  <div class="body">\n{gate}' + "\n".join(body) + "\n  </div>\n</section>\n</div>\n")
    return context, edit_html


def md_html(text):
    """Headings, paragraphs, bullet lists and fenced code of a short report; inline code and bold."""
    def inline(t):
        t = esc(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    out, para, items, code = [], [], [], None
    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"); items = []
    for line in text.splitlines():
        if code is not None:
            if line.startswith("```"):
                out.append("<pre>" + esc("\n".join(code)) + "</pre>"); code = None
            else:
                code.append(line)
            continue
        if line.startswith("```"):
            flush(); code = []
        elif re.match(r"#{1,6} ", line):
            flush(); level = min(len(line) - len(line.lstrip("#")), 4)
            out.append(f"<h{level}>{inline(line.lstrip('#').strip())}</h{level}>")
        elif re.match(r"\s*[-*] ", line):
            if para:
                flush()
            items.append(re.sub(r"^\s*[-*] ", "", line))
        elif not line.strip():
            flush()
        else:
            if items:
                items[-1] += " " + line.strip()
            else:
                para.append(line.strip())
    if code is not None:  # a fence left open: its lines are still the report's
        out.append("<pre>" + esc("\n".join(code)) + "</pre>")
    flush()
    return "\n".join(out)


def render_rs(report):
    return '<div class="rs">\n<div class="body">\n' + md_html(report) + "\n</div>\n</div>\n"


def splice_class(text, cls, section):
    """Replace the first top-level <div class="cls"> block with section, or append section at the end."""
    i = text.find(f'<div class="{cls}">')
    if i >= 0:
        close = block_end(text, i)
        nxt = SECTION_START.search(text, i + 1)
        balanced = len(re.findall(r"<div\b", text)) == len(re.findall(r"</div>", text))
        end = close if balanced or not nxt else min(close, nxt.start() + 1)
        return text[:i] + section + text[end:]
    if not section:
        return text
    return text.rstrip("\n") + ("\n\n" if text.strip() else "") + section


def write_out(out, pages, agent, n, pieces):
    """pieces: list of (class, section html). --out - prints; else splice each into the card."""
    if out == "-":
        sys.stdout.write("".join(sec for _, sec in pieces))
        return
    card = out or paths.card(paths.agent(pages, agent), n)
    os.makedirs(os.path.dirname(card), exist_ok=True)
    text = open(card, encoding="utf-8").read() if os.path.exists(card) else ""
    for cls, sec in pieces:
        text = _splice_text(text, sec) if cls == "ia" else splice_class(text, cls, sec)
    with open(card, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(card)
    if not out:
        source.link(paths.agent(pages, agent), n)


def pre_edit(repo, base, n):
    """The commit the context step started from, the tree before its edit, when the repository still has it."""
    try:
        at = json.load(open(paths.status(base, n, "context"), encoding="utf-8")).get("commit")
    except (OSError, ValueError):
        return None
    ok = at and subprocess.run(["git", "-C", repo, "cat-file", "-e", f"{at}^{{commit}}"], capture_output=True).returncode == 0
    return at if ok else None


def main(argv):
    if len(argv) < 3 or argv[0] not in ("ia", "ss", "oc", "rs"):
        fail(__doc__)
    view, agent, n = argv[0], argv[1], argv[2]
    opts = dict(zip(argv[3::2], argv[4::2]))
    pages = pages_dir(opts.get("--pages"))
    repo = opts.get("--repo") or os.getcwd()
    base = os.path.join(pages, "agents", agent)
    if view == "ia":
        analysis = load_json(opts.get("--analysis") or paths.answer(base, n, "analysis"))
        pieces = [("ia", render_ia(agent, n, analysis, pages))]
        entries = context_of_analysis(analysis)
        # the analysis's two items stand in for the Studio Context until the context step writes the fuller one
        if not os.path.exists(paths.answer(base, n, "context")):
            context = render_oc(agent, n, {"context": entries}, pages, repo)[0] if entries else ""
            pieces.append(("oc ctx", context))  # empty: a stale section from an earlier answer goes
    elif view == "ss":
        strategy = load_json(opts.get("--strategy") or paths.answer(base, n, "strategy"))
        pieces = [("ss", render_ss(agent, n, strategy, pages, repo))]
    elif view == "rs":
        path = opts.get("--report") or paths.step_file(base, n, "resolve", "md")
        if not os.path.exists(path):
            fail(f"missing {path}")
        pieces = [("rs", render_rs(open(path, encoding="utf-8").read()))]
    else:
        ctx = load_json(opts.get("--context") or paths.answer(base, n, "context"))
        # the Studio Context is the analysis's two items, plus what the context-edit answer adds in `also` and `tool`
        analysis_path = paths.answer(base, n, "analysis")
        entries = context_of_analysis(load_json(analysis_path)) if os.path.exists(analysis_path) else []
        entries += [{"file": a["file"], "pointer": a["pointer"], "role": a.get("role") or "A",
                     "spans": [a["span"]] if a.get("span") else []} for a in ctx.get("also") or [] if a.get("file") and a.get("pointer")]
        context, edit = render_oc(agent, n, {"context": entries, "tool": ctx.get("tool"), "edit": ctx.get("edit"), "cause": ctx.get("cause")},
                                  pages, repo, opts.get("--state") or "proposed", pre_edit(repo, base, n))
        pieces = ([("oc ctx", context)] if entries or (ctx.get("tool") or {}).get("name") else []) + ([("oc edit", edit)] if edit else [])
    write_out(opts.get("--out"), pages, agent, n, pieces)


if __name__ == "__main__":
    main(sys.argv[1:])
