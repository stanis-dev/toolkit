#!/usr/bin/env python3
"""Take in main when it has moved: merge origin/main into a worktree's branch and make its workspace hold the result.

  mainsync.py <agent> <worktree>

Every Studio workspace receives what merges to main, so after a merge to main a pull shows main's newer content as
changes the branch never had. In the worktree:
1. git fetch origin main; nothing to merge when origin/main is already in the branch.
2. git merge origin/main. Where both sides add a simulation at the same place, both are kept; any other conflict is
   aborted, exit 3, the files named.
3. pnpm install when the merge changed the lockfile or a package.json.
4. Ghostwriter pull. A changed Studio file whose new version the branch has had (main's included, after the merge) is
   restored from the branch; a version it never had, or a new Studio file, is a Studio edit: printed, restored, exit 2.
5. Lint, push --replace, pull; a Studio file the last pull changes means the workspace does not hold the branch: exit 4.
Exit 0: the branch holds main and the workspace holds the branch. Every command's output goes to stdout. The branch
is pushed to no git remote. batchmerge.py uses steps 1 to 3 before each merge into a batch."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stepgit
from setup import AGENT_DIR

CONFLICT = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)


def run(argv, cwd=None):
    print("$ " + " ".join(argv), flush=True)
    r = subprocess.run(argv, capture_output=True, text=True, stdin=subprocess.DEVNULL, cwd=cwd)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(out, flush=True)
    return r.returncode, out


def both_sims(text):
    """The file with every conflict joined when each is two simulations added at the same place, else None."""
    ok = True

    def join(m):
        nonlocal ok
        ours, theirs = m.group(1), m.group(2)
        if not (ours.lstrip().startswith("id:") and theirs.lstrip().startswith("id:")):
            ok = False
            return m.group(0)
        return ours + "    });\n\n    scenarioSimulation({\n" + theirs

    joined = CONFLICT.sub(join, text)
    return joined if ok and "<<<<<<< " not in joined else None


def merge_main(wt):
    """Steps 1 to 3. (0, what happened) or (3, the conflicting files)."""
    run(["git", "-C", wt, "fetch", "-q", "origin", "main"])
    return merge_ref(wt, "origin/main")


def merge_ref(wt, ref):
    """Steps 2 and 3 with ref in place of origin/main. (0, what happened) or (3, the conflicting files)."""
    if subprocess.run(["git", "-C", wt, "merge-base", "--is-ancestor", ref, "HEAD"]).returncode == 0:
        return 0, ref + " is already in the branch"
    before = stepgit.git(wt, "rev-parse", "HEAD").strip()
    code, _ = run(["git", "-C", wt] + stepgit.NO_HOOKS + ["merge", "--no-edit", ref])
    if code:
        files = [f for f in stepgit.git(wt, "diff", "--name-only", "--diff-filter=U").split() if f]
        if not files:
            return 3, "the working tree (git refused to start the merge)"
        left = []
        for f in files:
            path = os.path.join(wt, f)
            joined = both_sims(open(path, encoding="utf-8").read()) if f.endswith(".tests.ts") else None
            if joined is None:
                left.append(f)
            else:
                open(path, "w", encoding="utf-8").write(joined)
                stepgit.git(wt, "add", "--", f)
                print(f"{f}: both sides added a simulation at the same place; kept both")
        if left:
            run(["git", "-C", wt, "merge", "--abort"])
            return 3, ", ".join(left)
        stepgit.git(wt, "commit", "--no-edit")
    changed = stepgit.git(wt, "diff", "--name-only", before, "HEAD").split()
    if any(os.path.basename(f) in ("pnpm-lock.yaml", "package.json") for f in changed):
        run(["pnpm", "-C", wt, "install", "--frozen-lockfile"])
    return 0, f"merged {ref} at " + stepgit.git(wt, "rev-parse", "--short", "HEAD").strip()


def studio(wt, composer_rel):
    """Tracked changed paths under the agent's .composer, and untracked files there."""
    changed = [p for p in stepgit.dirty(wt) if p.startswith(composer_rel + "/")]
    new = sorted(p for p in stepgit.untracked(wt) if p.startswith(composer_rel + "/") and not stepgit.setup_copy(p))
    return changed, new


def known_blobs(wt, path):
    out = stepgit.git(wt, "log", "-m", "--full-history", "--no-abbrev", "--raw", "--format=", "HEAD", "--", path)
    return {f for line in out.splitlines() if line.startswith(":") for f in line.split()[2:4]}


def pull_and_sort(wt, sierra, agent_dir, composer_rel):
    """Step 4: 0, 1 when the pull failed, or 2 on a Studio edit; the worktree ends on the branch's content."""
    code, _ = run([sierra, "-C", agent_dir, "ghostwriter", "pull"])
    if code:
        return 1
    changed, new = studio(wt, composer_rel)
    edits = []
    for p in changed:
        if stepgit.git(wt, "hash-object", "--", p).strip() in known_blobs(wt, p):
            print(f"{p}: the workspace holds an older version of the branch's file; restored from the branch")
        else:
            edits.append(p)
    if edits or new:
        print("The workspace has Studio changes neither the branch nor main ever had:")
        for p in edits:
            print(stepgit.git(wt, "diff", "--", p))
        for p in new:
            print("new file " + p)
    if changed:
        stepgit.git(wt, "checkout", "--", *changed)
    for p in new:
        os.remove(os.path.join(wt, p))
    return 2 if edits or new else 0


def push_and_check(wt, sierra, agent_dir, composer_rel):
    """Step 5: 0, or 4 when the workspace does not hold the branch."""
    for cmd in (["lint"], ["push", "--replace", "-y"], ["pull"]):
        code, _ = run([sierra, "-C", agent_dir, "ghostwriter"] + cmd)
        if code:
            print(f"ghostwriter {cmd[0]} failed; the workspace may not hold the branch")
            return 4
    changed, new = studio(wt, composer_rel)
    if changed or new:
        for p in changed:
            print(stepgit.git(wt, "diff", "--", p))
        print("after the push, the workspace still differs from the branch: " + ", ".join(changed + new))
        return 4
    return 0


def main(argv):
    if len(argv) != 2 or argv[0] not in AGENT_DIR or not os.path.isdir(argv[1]):
        print(__doc__); return 64
    agent, wt = argv[0], os.path.abspath(argv[1])
    agent_rel = AGENT_DIR[agent]
    agent_dir, composer_rel = os.path.join(wt, agent_rel), agent_rel + "/.composer"
    sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
    code, what = merge_main(wt)
    if code:
        print("merging origin/main conflicts in " + what + ": aborted, nothing merged"); return 3
    print(what)
    code = pull_and_sort(wt, sierra, agent_dir, composer_rel) or push_and_check(wt, sierra, agent_dir, composer_rel)
    if code == 0:
        print("the branch holds origin/main and the workspace holds the branch")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
