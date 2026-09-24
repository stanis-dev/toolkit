#!/usr/bin/env python3
"""Report where a running step is, for the card: one line per call.

  progress.py <agent> <n> <step> "<line>" [--pages <dir>]

Appends {"t", "text"} to <step>/runs/progress.jsonl of the card; run.py puts the latest line in the step's
status.json, which the card shows next to the running chip, and keeps the file with the run."""
import json, os, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

STEPS = ("analysis", "strategy", "context")


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    if len(args) != 4 or args[2] not in STEPS or not args[1].isdigit() or not args[3].strip():
        sys.exit(__doc__)
    agent, n, step, text = args
    runs = paths.runs(paths.agent(paths.pages_dir(opts.get("--pages")), agent), n, step)
    os.makedirs(runs, exist_ok=True)
    line = {"t": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "text": " ".join(text.split())[:300]}
    with open(os.path.join(runs, "progress.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    print("reported")


if __name__ == "__main__":
    main(sys.argv[1:])
