#!/usr/bin/env python3
"""Merge one issue's branch into its batch and make the batch workspace hold the result.

  batchmerge.py <agent> <MMDD> <issue-branch> [--pages <dir>]

In the batch worktree from agents/<agent>/batches.json, one merge at a time (a lock under batches/):
1. Refused while the worktree has uncommitted tracked changes other than setup's copies and the SDK's generated files.
2. When main has moved, origin/main is merged into the batch first, as mainsync.py does: two simulations added at the
   same place are both kept; any other conflict is aborted, exit 5, nothing merged.
3. Ghostwriter pull. A tracked file the pull changes to a version the batch branch has had (main's included) is the
   workspace running behind or ahead of the branch: it is restored from the branch. A version the branch never had,
   or a new Studio file, is a Studio edit: printed, restored from the branch, exit 2, the issue not merged.
4. git merge of the issue branch; a conflict is aborted, exit 3.
5. Lint, push --replace, pull; a tracked file the last pull changes means the workspace does not hold the branch: exit 4.
Every command's output goes to stdout. The branch is pushed to no git remote."""
import fcntl, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stepgit
from mainsync import merge_main, pull_and_sort, push_and_check, run
from setup import AGENT_DIR


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    if len(args) != 3:
        print(__doc__); return 64
    agent, batch, branch = args
    pages = opts.get("--pages") or os.path.expanduser("~/.claude/bbva-issues")
    entry = json.load(open(os.path.join(pages, "agents", agent, "batches.json"))).get(batch) or {}
    wt = entry.get("worktree")
    if not wt or not os.path.isdir(wt):
        print(f"batch {batch} has no worktree"); return 1
    agent_rel = AGENT_DIR[agent]
    agent_dir, composer_rel = os.path.join(wt, agent_rel), agent_rel + "/.composer"
    sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")

    lock_path = os.path.join(pages, "agents", agent, "batches", batch + ".merge.lock")
    os.makedirs(os.path.dirname(lock_path), exist_ok=True)
    lock = open(lock_path, "w")
    t0 = time.time()
    while True:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB); break
        except BlockingIOError:
            if time.time() - t0 > 900:
                print("another merge into this batch has held the lock for 15 minutes"); return 1
            if int(time.time() - t0) % 60 == 0:
                print("waiting for another merge into this batch", flush=True)
            time.sleep(1)

    why = stepgit.refusal(wt)
    if why:
        print("batch " + why); return 1

    code, what = merge_main(wt)
    if code:
        print("merging origin/main into the batch conflicts in " + what + ": aborted, nothing merged"); return 5
    print(what)

    code = pull_and_sort(wt, sierra, agent_dir, composer_rel)
    if code:
        if code == 2:
            print("Nothing merged; the worktree is back on the branch's content.")
        return code

    code, _ = run(["git", "-C", wt] + stepgit.NO_HOOKS + ["merge", "--no-edit", branch])
    if code:
        run(["git", "-C", wt, "merge", "--abort"])
        print("merge conflict: aborted, nothing merged"); return 3

    code = push_and_check(wt, sierra, agent_dir, composer_rel)
    if code:
        return code
    print("merged " + branch + " at " + stepgit.git(wt, "rev-parse", "--short", "HEAD").strip()
          + "; the batch workspace holds the branch's Studio content")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
