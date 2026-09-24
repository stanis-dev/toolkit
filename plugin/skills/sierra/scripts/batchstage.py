#!/usr/bin/env python3
"""Record where a batch stands after its cards are done, for the issues page's batch view.

  batchstage.py <agent> <batch> <stage> <state> [--note "one line"] [--pages <dir>]

Stages and their states, in order:
  align  working done conflict
  check  running clean found
  sort   done
  route  sent waiting back
  pr     written pushed

Appends {"t", "stage", "state", "note"} to <pages>/agents/<agent>/driver/<batch>.stage.json (a JSON list) and refuses a
stage or state outside the table. The pages dir defaults to ~/.claude/bbva-issues."""
import json, os, re, sys
from datetime import datetime, timezone
import paths

STAGES = {
    "align": ("working", "done", "conflict"),
    "check": ("running", "clean", "found"),
    "sort": ("done",),
    "route": ("sent", "waiting", "back"),
    "pr": ("written", "pushed"),
}
AGENTS = ("cobranzas", "openpay", "hipotecarios")


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    if len(args) != 4 or args[0] not in AGENTS or not re.fullmatch(r"\d{4}(-\d)?", args[1]):
        sys.exit(__doc__)
    agent, batch, stage, state = args
    if stage not in STAGES:
        sys.exit(f"no stage {stage!r}: one of {', '.join(STAGES)}")
    if state not in STAGES[stage]:
        sys.exit(f"no state {state!r} for {stage}: one of {', '.join(STAGES[stage])}")
    pages = os.path.abspath(opts.get("--pages") or os.path.expanduser("~/.claude/bbva-issues"))
    path = paths.step_file(paths.agent(pages, agent), batch, "driver", "stage.json")
    try:
        log = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        log = []
    log.append({"t": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": stage, "state": state,
                "note": opts.get("--note")})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)
    print(f"{agent} {batch}: {stage} {state}")


if __name__ == "__main__":
    main(sys.argv[1:])
