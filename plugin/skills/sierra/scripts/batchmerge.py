#!/usr/bin/env python3
"""Merge one issue's branch into its batch and make the batch workspace hold the result.

  batchmerge.py <agent> <MMDD> <issue-branch> [--pages <dir>]

In the batch worktree from agents/<agent>/batches.json, one merge at a time (a lock under batches/):
1. Refused while the worktree has uncommitted tracked changes other than setup's copies and the SDK's generated files.
2. Ghostwriter pull. A tracked file the pull changes to a version the batch branch had before is the workspace running
   behind the branch (a merge not yet pushed): it is restored from the branch. A version the branch never had, or a
   new Studio file, is a Studio edit: printed, restored from the branch, exit 2, nothing merged.
3. git merge of the issue branch; a conflict is aborted, exit 3.
4. Lint, push --replace, pull; a tracked file the last pull changes means the workspace does not hold the branch: exit 4.
Every command's output goes to stdout. The branch is pushed nowhere."""
import fcntl, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stepgit
from setup import AGENT_DIR


def run(argv):
    print("$ " + " ".join(argv), flush=True)
    r = subprocess.run(argv, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(out, flush=True)
    return r.returncode, out


def studio(wt, composer_rel):
    """Tracked changed paths under the agent's .composer, and untracked files there."""
    changed = [p for p in stepgit.dirty(wt) if p.startswith(composer_rel + "/")]
    new = sorted(p for p in stepgit.untracked(wt) if p.startswith(composer_rel + "/") and not stepgit.setup_copy(p))
    return changed, new


def known_blobs(wt, path):
    out = stepgit.git(wt, "log", "-m", "--full-history", "--no-abbrev", "--raw", "--format=", "HEAD", "--", path)
    return {f for line in out.splitlines() if line.startswith(":") for f in line.split()[2:4]}


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

    code, _ = run([sierra, "-C", agent_dir, "ghostwriter", "pull"])
    if code:
        return 1
    changed, new = studio(wt, composer_rel)
    edits = []
    for p in changed:
        blob = stepgit.git(wt, "hash-object", "--", p).strip()
        if blob in known_blobs(wt, p):
            print(f"{p}: the workspace holds an older version of the branch's file; restored from the branch")
        else:
            edits.append(p)
    if edits or new:
        print("The batch workspace has Studio changes the batch branch never had:")
        for p in edits:
            print(stepgit.git(wt, "diff", "--", p))
        for p in new:
            print("new file " + p)
    if changed:
        stepgit.git(wt, "checkout", "--", *changed)
    for p in new:
        os.remove(os.path.join(wt, p))
    if edits or new:
        print("Nothing merged; the worktree is back on the branch's content.")
        return 2

    code, _ = run(["git", "-C", wt] + stepgit.NO_HOOKS + ["merge", "--no-edit", branch])
    if code:
        run(["git", "-C", wt, "merge", "--abort"])
        print("merge conflict: aborted, nothing merged"); return 3

    for cmd in (["lint"], ["push", "--replace", "-y"], ["pull"]):
        code, _ = run([sierra, "-C", agent_dir, "ghostwriter"] + cmd)
        if code:
            print(f"ghostwriter {cmd[0]} failed; the merge stays, the workspace may not hold it"); return 4
    changed, new = studio(wt, composer_rel)
    if changed or new:
        for p in changed:
            print(stepgit.git(wt, "diff", "--", p))
        print("after the push, the batch workspace still differs from the branch: " + ", ".join(changed + new))
        return 4
    print("merged " + branch + " at " + stepgit.git(wt, "rev-parse", "--short", "HEAD").strip()
          + "; the batch workspace holds the branch's Studio content")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
