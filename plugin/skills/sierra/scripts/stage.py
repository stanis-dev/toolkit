#!/usr/bin/env python3
"""Record where an issue's resolution stands, for the issues page's sidebar.

  stage.py <agent> <n> <stage> <state> [--step <step>] [--note "one line"] [--pages <dir>]

Stages and their states, in order:
  review       working holds wrong
  repro        writing reproduces does-not-reproduce wrong-reason
  fix          applying solved refine misguided
  regressions  running found fixing clean
  merge        ready merged

review wrong and fix misguided need --step, the step to blame: analysis, strategy or context.

Appends {"t", "stage", "state", "step", "note"} to <pages>/agents/<agent>/resolve/<n>.stage.json (a JSON list) and refuses a
stage or state outside the table. The pages dir defaults to ~/.claude/bbva-issues."""
import json, os, sys
from datetime import datetime, timezone

STAGES = {
    "review": ("working", "holds", "wrong"),
    "repro": ("writing", "reproduces", "does-not-reproduce", "wrong-reason"),
    "fix": ("applying", "solved", "refine", "misguided"),
    "regressions": ("running", "found", "fixing", "clean"),
    "merge": ("ready", "merged"),
}
AGENTS = ("cobranzas", "openpay", "hipotecarios")
BLAME = {("review", "wrong"), ("fix", "misguided")}
BLAMED = ("analysis", "strategy", "context")


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    if len(args) != 4 or args[0] not in AGENTS or not args[1].isdigit():
        sys.exit(__doc__)
    agent, n, stage, state = args
    if stage not in STAGES:
        sys.exit(f"no stage {stage!r}: one of {', '.join(STAGES)}")
    if state not in STAGES[stage]:
        sys.exit(f"no state {state!r} for {stage}: one of {', '.join(STAGES[stage])}")
    step = opts.get("--step")
    if (stage, state) in BLAME and step not in BLAMED:
        sys.exit(f"{stage} {state} needs --step, the step to blame: one of {', '.join(BLAMED)}")
    if step and (stage, state) not in BLAME:
        sys.exit(f"--step goes only with {' or '.join(' '.join(b) for b in sorted(BLAME))}")
    pages = os.path.abspath(opts.get("--pages") or os.path.expanduser("~/.claude/bbva-issues"))
    path = os.path.join(pages, "agents", agent, "resolve", f"{n}.stage.json")
    try:
        log = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        log = []
    log.append({"t": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": stage, "state": state,
                "step": step, "note": opts.get("--note")})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)
    print(f"{agent} {n}: {stage} {state}" + (f" ({step})" if step else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
