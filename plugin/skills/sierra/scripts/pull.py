#!/usr/bin/env python3
"""Pull an issue's workspace into its worktree, taking what main brought as base.

  pull.py <agent> <worktree>

Runs `ghostwriter pull` in the worktree's agent directory, then commits as base each changed or new Studio file whose
content is a version origin/main has had (main's merges reach every workspace as they land). Everything else the pull
changed stays uncommitted: the card's work. Prints the files taken as base and the files left as the card's. Exit 1
when the pull fails. Use it for every pull in an issue's worktree, in place of `ghostwriter pull`."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stepgit
from setup import AGENT_DIR


def main(argv):
    if len(argv) != 2 or argv[0] not in AGENT_DIR or not os.path.isdir(argv[1]):
        print(__doc__); return 64
    agent, wt = argv[0], os.path.abspath(argv[1])
    agent_dir = os.path.join(wt, AGENT_DIR[agent])
    composer_rel = AGENT_DIR[agent] + "/.composer"
    r = subprocess.run([os.path.join(agent_dir, "node_modules", ".bin", "sierra"), "-C", agent_dir, "ghostwriter", "pull"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(out)
    if r.returncode:
        return 1
    base = stepgit.absorb_main(wt, composer_rel)
    left = [p for p in stepgit.dirty(wt) if p.startswith(composer_rel + "/")]
    print("taken as base, from main: " + (", ".join(base) if base else "nothing"))
    print("the card's work, uncommitted: " + (", ".join(left) if left else "nothing"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
