#!/usr/bin/env python3
"""The card's history: one event per line in <pages>/agents/<agent>/cards/<n>/log.jsonl, and the index the briefs print.

  cardlog.py <agent> <n> [--pages <dir>]

prints the index. An event is {"t", "who", "what", "refs"}: who acted (engineer, a step, a script), one line on what
happened, and the files behind it: paths under agents/<agent>/, absolute paths, git:<commit> in the issue's worktree,
a path@L<k> for line k of a log. The files an event points to are not rewritten afterwards. The scripts that act
append; nothing else writes the file."""
import fcntl, json, os, sys
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

WIDTH = 220
KEEP = 30
STEPS = ("analysis", "strategy", "context")


def pages_dir(override=None):
    return os.path.abspath(override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues"))


def path_of(pages, agent, n):
    return paths.log(paths.agent(pages, agent), n)


def line(what):
    what = " ".join(str(what or "").split())
    return what if len(what) <= WIDTH else what[:WIDTH - 1] + "…"


def add(pages, agent, n, who, what, refs=(), t=None, **extra):
    """Appends one event. Never raises: a card's history is not worth failing the step that writes it."""
    ev = dict({"t": t or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "who": who, "what": line(what),
               "refs": [r for r in refs if r]}, **extra)
    try:
        path = path_of(pages, agent, n)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    except OSError:
        pass


def load(pages, agent, n):
    out = []
    try:
        for raw in open(path_of(pages, agent, n), encoding="utf-8"):
            try:
                out.append(json.loads(raw))
            except ValueError:
                pass
    except OSError:
        pass
    return sorted(out, key=lambda e: e.get("t") or "")


def rel(pages, agent, path):
    """path as an event keeps it: under agents/<agent>/ relative, else absolute."""
    base = os.path.abspath(paths.agent(pages, agent)) + os.sep
    path = os.path.abspath(path)
    return path[len(base):] if path.startswith(base) else path


def summary(step, answer, base, n):
    """One line of a step's answer."""
    a = answer if isinstance(answer, dict) else {}
    if step == "analysis":
        out = a.get("verdict") or "answered"
    elif step == "strategy":
        red = paths.guard_red(base, n)
        out = f"guard {(a.get('guard') or {}).get('id') or '?'}" + (f", red {red['passed']}/{red['total']}" if red else "")
        k = len((a.get("regressions") or {}).get("sims") or [])
        out += f"; {k} regression sims" if k else ""
    elif step == "context":
        es = a.get("edits") or []
        out = f"{a.get('cause') or '?'}: " + ("; ".join(f"{e.get('kind') or 'item'} {e.get('path') or e.get('pointer') or e.get('file')}" for e in es) if es else "no edit")
        out += f" (+{len(a['also'])} also)" if a.get("also") else ""
    else:
        out = "answered"
    fb = a.get("feedback") or {}
    return out + (f" · feedback {fb['verdict']}" if fb.get("verdict") else "")


def stamp(t):
    return (t or "")[5:16].replace("T", " ")


def index(pages, agent, n, keep=KEEP, bare=None):
    """The card's history as the briefs print it: the last `keep` events one per line, older ones folded into counts.
    An answer a later run of the same step replaced is marked superseded; the events of step bare print without their
    files. Empty when the card has no history."""
    events = load(pages, agent, n)
    if not events:
        return ""
    last = {}
    for k, e in enumerate(events):
        if e.get("who") in STEPS and e.get("answer"):
            last[e["who"]] = k
    older, recent = events[:-keep], events[-keep:]
    start = len(older)
    head = (f"# Card history · {agent} {n}\n\nOldest first. Paths are under `{os.path.join(pages, 'agents', agent)}`; "
            f"git: names a commit in the issue's worktree; @L<k> is line k of that log.\n")
    lines = [head]
    if older:
        counts = Counter(e.get("who") for e in older)
        lines.append("earlier: " + ", ".join(f"{w} ×{c}" for w, c in counts.items())
                     + f" (until {stamp(older[-1].get('t'))}; every event in `log/{n}.jsonl`)")
    width = max(len(e.get("who") or "") for e in recent)
    for k, e in enumerate(recent, start):
        old = e.get("who") in STEPS and e.get("answer") and last.get(e["who"]) != k
        refs = [] if bare and e.get("who") == bare else e.get("refs") or []
        lines.append(f"{stamp(e.get('t'))}  {(e.get('who') or '').ljust(width)}  {e.get('what')}"
                     + (" · superseded" if old else "") + (" → " + ", ".join(refs) if refs else ""))
    return "\n".join(lines) + "\n"


def card_of(pages, agent, **match):
    """The issue number whose setup status has every field in match (worktree, branch), else None."""
    base = paths.agent(pages, agent)
    for n in paths.numbers(base, "setup"):
        try:
            st = json.load(open(paths.status(base, n, "setup"), encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if all(st.get(k) and os.path.normpath(str(st[k])) == os.path.normpath(str(v)) for k, v in match.items()):
            return n
    return None


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    if len(args) != 2 or not args[1].isdigit():
        sys.exit(__doc__)
    sys.stdout.write(index(pages_dir(opts.get("--pages")), *args) or "no history\n")


if __name__ == "__main__":
    main(sys.argv[1:])
