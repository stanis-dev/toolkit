"""What a card works from, in one shape whatever it came from: a tracker issue (issues/<n>.json, sync.py's) or a
failing simulation (one replay, copied into the card by simcard.py). Every reader of a card's source and its
conversations goes through here, so only this module and simcard.py know the difference.

The card's source.json:

    kind          "issue" | "sim"
    number        the card's number
    title         the issue's name | the simulation's name
    description   the reporter's text | the failed expectations with the judge's reasoning, the tag misses
    comments      [{author, time, text}], the tracker's
    ref           issue: {status, severity, category, owner, created}; sim: {test, run, result, status}
    conversations [{id, timestamp, marked: [{turn, author, text}]}]: the linked calls with the reporter's highlighted lines |
                  the one replay, nothing marked

A conversation, as details() gives it: {"metadata": {id, timestamp, tags}, "events": [{type: "message", role, text,
turn}, {type: "agent_tags", tags}]}. `turn` addresses a line: a call's logEntryId, a replay's debug.log seq.
"""
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

csv.field_size_limit(sys.maxsize)


def _load(p):
    d = json.load(open(p, encoding="utf-8"))
    return json.loads(d) if isinstance(d, str) else d


def path(base, n):
    return os.path.join(paths.card_dir(base, n), "source.json")


def from_issue(n, iss):
    d = iss.get("issue") or {}
    comments = [{"author": c.get("creatorName") or ((c.get("author") or {}).get("name") if isinstance(c.get("author"), dict) else c.get("author")) or c.get("authorName") or "",
                 "time": c.get("createdAt") or c.get("createdTime") or c.get("created") or "",
                 "text": c.get("body") or c.get("text") or c.get("content") or ""} for c in d.get("comments") or []]
    return {"kind": "issue", "number": int(d.get("number") or n), "title": (d.get("name") or "").strip(),
            "description": d.get("description") or "", "comments": comments,
            "ref": {"status": d.get("status") or "OPEN", "severity": d.get("severity") or "", "category": d.get("issueCategoryLabel") or "",
                    "owner": (d.get("owner") or {}).get("name") or "", "created": d.get("createdTime") or ""},
            "conversations": [{"id": l["id"], "timestamp": l.get("timestamp") or "", "marked": [{"turn": x.get("logEntryId"), "author": x.get("author"), "text": x.get("text")}
                                                         for x in l.get("examples") or []]}
                              for l in iss.get("linkedLogs") or []]}


def load(base, n):
    """The card's source, None when it has none. An issue card's is rebuilt from the tracker's record each time and
    kept in source.json when it changed, so the file shows what the steps read."""
    p = path(base, n)
    have = None
    if os.path.isfile(p) and not os.path.islink(p):
        try:
            have = _load(p)
        except ValueError:
            have = None
        if have and have.get("kind") != "issue":
            return have
    if not os.path.exists(paths.issue(base, n)):
        return have
    src = from_issue(n, _load(paths.issue(base, n)))
    if src != have and os.path.isdir(paths.card_dir(base, n)):
        if os.path.islink(p):
            os.remove(p)
        with open(p + ".tmp", "w", encoding="utf-8") as f:
            json.dump(src, f, ensure_ascii=False, indent=1)
        os.replace(p + ".tmp", p)
    return src


def all_sources(base):
    """{n: source} for every tracker issue and every card with a source of another kind."""
    out = {}
    for n in paths.issues(base):
        try:
            out[n] = from_issue(n, _load(paths.issue(base, n)))
        except (OSError, ValueError):
            pass
    for n in paths.cards(base):
        if n not in out:
            s = load(base, n)
            if s:
                out[n] = s
    return out


def link(base, n):
    """The card folder's source.json and its conversations/<id> links to the calls sync.py has fetched. Idempotent."""
    os.makedirs(paths.card_dir(base, n), exist_ok=True)
    src = load(base, n)
    for c in (src or {}).get("conversations") or []:
        conv = paths.conversation(base, c["id"])
        dst = os.path.join(paths.card_dir(base, n), "conversations", c["id"])
        if os.path.isdir(conv) and not os.path.lexists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.symlink(os.path.relpath(conv, os.path.dirname(dst)), dst)


def conv_dir(base, n, cid):
    """A conversation's folder: the card's own copy or link, else the agent's cache."""
    d = os.path.join(paths.card_dir(base, n), "conversations", cid)
    return d if os.path.isdir(d) else paths.conversation(base, cid)


def details(d):
    """The conversation in one shape: a call's details.json, or a replay rebuilt from its debug.log and result.json."""
    p = os.path.join(d, "details.json")
    if os.path.exists(p):
        raw = _load(p)
        events = []
        for e in raw.get("events") or []:
            if e.get("type") == "message":
                e = {"type": "message", "role": e.get("role"), "text": e.get("text") or "", "turn": e.get("logEntryId")}
            events.append(e)
        return {"metadata": raw.get("metadata") or {}, "events": events}
    res = _load(os.path.join(d, "result.json")) if os.path.exists(os.path.join(d, "result.json")) else {}
    events = []
    log = os.path.join(d, "debug.log")
    if os.path.exists(log):
        with open(log, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["event_type"] in ("USER_MSG", "AGENT_MSG"):
                    events.append({"type": "message", "role": "assistant" if r["event_type"] == "AGENT_MSG" else "user",
                                   "text": r["message"], "turn": r["seq"]})
    tags = res.get("tags") or []
    if tags:
        events.append({"type": "agent_tags", "tags": tags})
    return {"metadata": {"id": res.get("id") or os.path.basename(d), "timestamp": res.get("creationTime") or "", "tags": tags},
            "events": events}


def failure_turn(analysis):
    """The analysis's failure turn; answers written before the rename name it logEntryId."""
    f = (analysis or {}).get("failure") or {}
    return f.get("turn") or f.get("logEntryId")


def tool_args(d):
    """{TOOL_CALL row seq: args} from the agent's «Invoking tool» log lines. A call's log writes the invocation after
    the call, a replay's before it, with a spoken line between either way: each invocation goes to the nearest call of
    that tool not yet paired."""
    log = os.path.join(d, "debug.log")
    if not os.path.exists(log):
        return {}
    calls, invokes = [], []
    with open(log, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["event_type"] == "TOOL_CALL":
                calls.append((int(r["seq"]), r["message"]))
            elif r["event_type"] == "AGENT_LOG" and "Invoking tool: " in r["message"]:
                m = re.match(r".*Invoking tool: (\S+) (\{.*\})\s*$", r["message"], re.S)
                if m:
                    try:
                        args = json.loads(m.group(2))
                    except ValueError:
                        args = m.group(2)
                    invokes.append((int(r["seq"]), m.group(1), args))
    pairs = sorted((abs(cs - s), cs, k) for k, (s, name, _) in enumerate(invokes) for cs, cn in calls if cn == name)
    out, used = {}, set()
    for _, cs, k in pairs:
        if cs not in out and k not in used:
            out[cs] = invokes[k][2]
            used.add(k)
    return {str(k): v for k, v in out.items()}
