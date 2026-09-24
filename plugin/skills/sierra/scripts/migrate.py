"""Move a pages dir from the step-first layout (analysis/<n>.json, resolve/runs/<n>/, log/<n>.jsonl, …) to one folder
per card (cards/<n>/…, see paths.py), and rewrite the paths the card's records name.

Usage:
  migrate.py [--pages <dir>] [--agent <agent>] [--apply]

Without --apply it prints what it would move and rewrite, and changes nothing. With --apply it refuses while any step,
session, sequence or driver of the agent runs; otherwise it first writes a backup of the agent's folder (issues and
conversations left out, they do not move) to <pages>/backups/<agent>-<stamp>.tgz, moves the files, rewrites the paths
in the card records (the step answers, status and stage files, runs.json, reopen.json, the history log, the cost
ledger, the chain state, and the driver's and batches' JSON), links each card to its source, removes the step folders
it emptied, and writes the list of moves to <pages>/backups/<agent>-<stamp>.moves.json. Run transcripts (out.jsonl,
prompt.md, session files) keep the paths they were written with.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402
import source  # noqa: E402

STEPS = paths.STEPS
OLD_DIRS = STEPS + ("log", "cost", "chain")
NAME = {"json": "answer.json", "md": "report.md"}


def plan(base):
    """[(old, new)] relative to base, files and whole runs/ folders; and the names left in the old folders."""
    moves, left = [], []
    cards = os.path.join(base, "cards")
    for f in sorted(os.listdir(cards)) if os.path.isdir(cards) else []:
        m = re.fullmatch(r"(\d+)\.html", f)
        if m:
            moves.append((f"cards/{f}", f"cards/{m.group(1)}/card.html"))
    for step in STEPS:
        d = os.path.join(base, step)
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            m = re.fullmatch(r"(\d+)\.(.+)", f)
            if m and os.path.isfile(os.path.join(d, f)):
                n, ext = m.groups()
                moves.append((f"{step}/{f}", f"cards/{n}/{step}/{NAME.get(ext, ext)}"))
            elif f not in ("runs", "history"):
                left.append(f"{step}/{f}")
        for sub in ("runs", "history"):
            sd = os.path.join(d, sub)
            for f in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
                if sub == "runs" and f.isdigit():
                    moves.append((f"{step}/runs/{f}", f"cards/{f}/{step}/runs"))
                elif sub == "history" and re.fullmatch(r"\d+\..+", f):
                    n, rest = f.split(".", 1)
                    moves.append((f"{step}/history/{f}", f"cards/{n}/{step}/history/{rest}"))
                else:
                    left.append(f"{step}/{sub}/{f}")
    for kind, name in (("log", "log"), ("cost", "cost"), ("chain", "chain")):
        d = os.path.join(base, kind)
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            m = re.fullmatch(r"(\d+)\.(.+)", f)
            if m and os.path.isfile(os.path.join(d, f)):
                moves.append((f"{kind}/{f}", f"cards/{m.group(1)}/{name}.{m.group(2)}"))
            elif not (kind == "chain" and f == "runs"):
                left.append(f"{kind}/{f}")
    d = os.path.join(base, "chain", "runs")
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = re.fullmatch(r"(\d+)\.log", f)
        if m:
            moves.append((f"chain/runs/{f}", f"cards/{m.group(1)}/chain.log"))
        else:
            left.append(f"chain/runs/{f}")
    return moves, left


def rewriter(base, moves):
    """A function that replaces every old path of moves in a text: under base's absolute path, under agents/<agent>/,
    or relative at the start of a token. Longest first, so a runs/ folder's files follow the folder."""
    new = dict(moves)
    alt = "|".join(re.escape(o) for o in sorted(new, key=len, reverse=True))
    pre = re.escape(os.path.abspath(base) + "/") + "|" + re.escape("agents/" + os.path.basename(base) + "/")
    rx = re.compile(r"(?P<pre>" + pre + r")?(?P<old>" + alt + r")(?![\w-])")

    def fix(text):
        out, last = [], 0
        for m in rx.finditer(text):
            s = m.start("old")
            if not m.group("pre") and s > 0 and text[s - 1] not in " \t\n\"'`([,=:":
                continue
            out += [text[last:s], new[m.group("old")]]
            last = m.end("old")
        return "".join(out) + text[last:]
    return fix


def records(base):
    """The card records whose paths get rewritten, after the move."""
    out = []
    cards = os.path.join(base, "cards")
    for n in sorted(os.listdir(cards)) if os.path.isdir(cards) else []:
        d = os.path.join(cards, n)
        if not (n.isdigit() and os.path.isdir(d)):
            continue
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if f.endswith((".json", ".jsonl")) and os.path.isfile(p) and not os.path.islink(p):
                out.append(p)
        for step in STEPS:
            sd = os.path.join(d, step)
            for f in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
                p = os.path.join(sd, f)
                if f.endswith((".json", ".md")) and os.path.isfile(p):
                    out.append(p)
    for sub in ("driver", "batches"):
        d = os.path.join(base, sub)
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.endswith(".json"):
                out.append(os.path.join(d, f))
    if os.path.exists(paths.batches(base)):
        out.append(paths.batches(base))
    return out


def running(base):
    """The status files of the agent whose process is alive."""
    out = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ("conversations", "issues", "runs", "history", "backups")]
        for f in files:
            if not f.endswith(".json"):
                continue
            p = os.path.join(root, f)
            try:
                st = json.load(open(p, encoding="utf-8"))
                pid = int(st.get("pid") or 0) if isinstance(st, dict) and st.get("state") == "working" else 0
            except (OSError, ValueError, TypeError, AttributeError):
                continue
            if pid > 0:
                try:
                    os.kill(pid, 0)
                    out.append(paths.rel(base, p))
                except OSError:
                    pass
    return out


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--") and argv[k] != "--apply"}
    apply = "--apply" in argv
    pages = os.path.abspath(paths.pages_dir(opts.get("--pages")))
    agents = [opts["--agent"]] if opts.get("--agent") else sorted(os.listdir(os.path.join(pages, "agents")))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    for a in agents:
        base = paths.agent(pages, a)
        moves, left = plan(base)
        clash = [n for o, n in moves if os.path.lexists(os.path.join(base, n))]
        print(f"== {a}: {len(moves)} moves" + (f", {len(left)} left in place" if left else ""))
        for o, n in moves:
            print(f"  {o} -> {n}")
        for f in left:
            print(f"  left: {f}")
        if clash:
            sys.exit(f"{a}: already there: " + ", ".join(clash[:10]))
        if not apply or not moves:
            continue
        live = running(base)
        if live:
            sys.exit(f"{a}: still running, stop them first: " + ", ".join(live))
        bdir = os.path.join(pages, "backups")
        os.makedirs(bdir, exist_ok=True)
        tgz = os.path.join(bdir, f"{a}-{stamp}.tgz")
        subprocess.run(["tar", "-czf", tgz, "--exclude", "./conversations", "--exclude", "./issues", "-C", base, "."], check=True)
        print(f"  backup {tgz}")
        for o, n in moves:
            dst = os.path.join(base, n)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(os.path.join(base, o), dst)
        fix = rewriter(base, moves)
        changed = []
        for p in records(base):
            text = open(p, encoding="utf-8").read()
            new = fix(text)
            if new != text:
                if p.endswith(".json"):
                    json.loads(new)
                with open(p + ".tmp", "w", encoding="utf-8") as f:
                    f.write(new)
                os.replace(p + ".tmp", p)
                changed.append(paths.rel(base, p))
        for n in paths.cards(base):
            source.link(base, n)
        for d in OLD_DIRS + tuple(f"{s}/runs" for s in STEPS) + tuple(f"{s}/history" for s in STEPS) + ("chain/runs",):
            p = os.path.join(base, d)
            if os.path.isdir(p) and not os.listdir(p):
                os.rmdir(p)
        for d in OLD_DIRS:
            p = os.path.join(base, d)
            if os.path.isdir(p) and not os.listdir(p):
                os.rmdir(p)
        json.dump({"moves": moves, "rewritten": changed, "backup": tgz}, open(os.path.join(bdir, f"{a}-{stamp}.moves.json"), "w"), indent=1)
        print(f"  moved {len(moves)}, rewrote paths in {len(changed)} records")


if __name__ == "__main__":
    main(sys.argv[1:])
