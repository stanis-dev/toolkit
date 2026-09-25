#!/usr/bin/env python3
"""Keep a card current with its batch: merge the batch branch into the card's worktree, the card's uncommitted work
kept on top, and make the card's workspace hold the result.

  cardsync.py <agent> <n> [--pages <dir>]

The batch is the card's (card.html's batch line), its branch from batches.json. In the card's worktree:
1. Nothing to do when the batch branch is already in HEAD: exit 0, no event.
2. Refused, exit 5, while a prep step, the guard or the regressions run on the card, or when Ghostwriter is not bound
   to the card's workspace.
3. Ghostwriter pull. A Studio file the pull changes to a version origin/main has had is committed as base (pull.py);
   any other change means the workspace holds something the tree does not: the tree is put back, exit 2.
4. The card's work that the merge would touch (changed or new files the batch also changed) is set aside, the rest
   stays in place. git merge of the batch branch; two simulations added at the same place are both kept, any other
   conflict is aborted, exit 3, the card's work put back.
5. Each file set aside is merged three ways onto the new HEAD (base: the old HEAD); two simulations added at the same
   place are both kept. Any other conflict takes the merge back (git reset --keep), puts the card's work back, exit 3.
6. pnpm install when the merge changed the lockfile or a package.json.
7. Lint, push --replace, pull; a Studio file the last pull changes means the workspace does not hold the tree: exit 4.
Exit 0: HEAD holds the batch, the card's work is uncommitted on top, the workspace holds the tree. Every command's
output goes to stdout. The outcome, merged or why not, is one event of the card's history (cardlog.py). The run's
status is cards/<n>/sync/status.json: state working, done, refused (exit 5) or failed; head, the batch commit it started
from; merged, whether it took the batch in; what, the history line; error. The pages server runs it for every card
behind its batch that nothing works on, and not again at the same head after a failure."""
import json, os, re, subprocess, sys, tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cardlog, paths, stepgit
from mainsync import both_sims, known_blobs, merge_ref, run
from setup import AGENT_DIR


def alive(pid):
    try:
        os.kill(pid, 0); return pid > 0
    except OSError:
        return False


def busy(base, n):
    """What runs on the card's tree now, or None."""
    for step in ("analysis", "strategy", "context"):
        st = stepgit.load(paths.status(base, n, step))
        if st.get("state") == "working" and alive(int(st.get("pid") or 0)):
            return step + " is running"
    for f, what in (("guard.json", "the guard"), ("regressions-run.json", "the regressions")):
        st = stepgit.load(os.path.join(paths.card_dir(base, n), "strategy", f))
        if st.get("state") == "working" and alive(int(st.get("pid") or 0)):
            return what + " is running"
    return None


def batch_branch(pages, agent, n):
    """(batch, its branch) of the card; the branch setup forked from when batches.json has none."""
    base = paths.agent(pages, agent)
    try:
        head = open(paths.card(base, n), encoding="utf-8").read(400)
    except OSError:
        head = ""
    m = re.match(r"\s*<!--\s*batch:\s*(\d{4}(?:-\d)?)\s*-->", head)
    batch = m.group(1) if m else ""
    entry = stepgit.load(os.path.join(base, "batches.json")).get(batch) or {}
    if entry.get("archived"):
        return batch, ""
    return batch, entry.get("base") or stepgit.load(paths.status(base, n, "setup")).get("base") or ""


def behind(wt, branch):
    """How many commits of branch HEAD lacks; None when either is unknown."""
    r = subprocess.run(["git", "-C", wt, "rev-list", "--count", "HEAD.." + branch], capture_output=True, text=True)
    return int(r.stdout) if r.returncode == 0 and r.stdout.strip().isdigit() else None


def snapshot(wt, composer_rel):
    """{path: blob} of every changed or new Studio file of the tree."""
    out = {}
    for p in [p for p in stepgit.dirty(wt) if p.startswith(composer_rel + "/")] + \
             sorted(p for p in stepgit.untracked(wt) if p.startswith(composer_rel + "/") and not stepgit.setup_copy(p)):
        full = os.path.join(wt, p)
        out[p] = stepgit.git(wt, "hash-object", "--", p).strip() if os.path.exists(full) else None
    return out


def workspace_matches(wt, sierra, agent_dir, composer_rel):
    """Step 3: 0, 1 when the pull failed, 2 when the workspace holds something the tree does not (the tree put back).
    A clean file the pull brings back to a version the branch has had is the workspace running behind: restored."""
    before = snapshot(wt, composer_rel)
    saved = {p: open(os.path.join(wt, p), "rb").read() for p, b in before.items() if b}
    code, _ = run([sierra, "-C", agent_dir, "ghostwriter", "pull"])
    if code:
        return 1
    absorbed = set(stepgit.absorb_main(wt, composer_rel))
    after = snapshot(wt, composer_rel)
    differ = []
    for p in sorted(set(before) | set(after)):
        if p in absorbed or before.get(p) == after.get(p):
            continue
        if p not in before and after.get(p) and after[p] in known_blobs(wt, p):
            stepgit.git(wt, "checkout", "HEAD", "--", p)
            print(f"{p}: the workspace holds an older version of the branch's file; restored from the branch")
        else:
            differ.append(p)
    if not differ:
        return 0
    print("the workspace holds Studio content the tree does not: " + ", ".join(differ))
    for p in differ:
        print(stepgit.git(wt, "diff", "--", p, check=False))
        full = os.path.join(wt, p)
        if p in saved:
            open(full, "wb").write(saved[p])
        elif in_head(wt, p):
            stepgit.git(wt, "checkout", "HEAD", "--", p)
        elif os.path.exists(full):
            os.remove(full)
    return 2


def in_head(wt, p):
    return subprocess.run(["git", "-C", wt, "cat-file", "-e", "HEAD:" + p], capture_output=True).returncode == 0


def card_work(wt):
    """The card's work: tracked files with changes and new files, the setup copies and generated files left out."""
    return stepgit.dirty(wt) + sorted(p for p in stepgit.untracked(wt) if not stepgit.setup_copy(p))


def generated_changes(wt):
    """Tracked files the Sierra SDK generates that have changes, staged or not: the next build writes them again."""
    work = set(stepgit.dirty(wt))
    return [p for p in stepgit.dirty(wt, keep_generated=True) if p not in work]


def merge_three(ours, base, theirs):
    """(text, clean) of git merge-file ours base theirs, texts in and out."""
    with tempfile.TemporaryDirectory() as d:
        files = []
        for name, text in (("ours", ours), ("base", base), ("theirs", theirs)):
            files.append(os.path.join(d, name))
            open(files[-1], "wb").write(text)
        r = subprocess.run(["git", "merge-file", "-p", "-L", "card", "-L", "base", "-L", "batch"] + files, capture_output=True)
        return r.stdout, r.returncode == 0


def blob(wt, rev, p):
    r = subprocess.run(["git", "-C", wt, "show", f"{rev}:{p}"], capture_output=True)
    return r.stdout if r.returncode == 0 else b""


def sync(agent, n, pages):
    """(exit code, [history line, refs…] or None)."""
    base = paths.agent(pages, agent)
    st = stepgit.load(paths.status(base, n, "setup"))
    wt = st.get("worktree")
    if st.get("state") != "done" or not wt or not os.path.isdir(wt):
        print("the card has no worktree"); return 5, None
    batch, branch = batch_branch(pages, agent, n)
    if not branch:
        print("the card has no batch branch, or its batch is archived"); return 5, None
    if subprocess.run(["git", "-C", wt, "merge-base", "--is-ancestor", branch, "HEAD"]).returncode == 0:
        print(f"{branch} is already in the card's branch"); return 0, None
    why = busy(base, n)
    agent_rel = AGENT_DIR[agent]
    agent_dir, composer_rel = os.path.join(wt, agent_rel), agent_rel + "/.composer"
    try:
        stepgit.binding(pages, agent, n, agent_dir)
    except stepgit.Refused as ex:
        why = why or str(ex)
    if why:
        print("not now: " + why); return 5, None
    sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
    code = workspace_matches(wt, sierra, agent_dir, composer_rel)
    if code:
        return code, [f"did not take batch {batch} in: " + ("the pull failed" if code == 1 else
                      "the card's workspace holds Studio content its tree does not; pull.py first")]

    before = stepgit.git(wt, "rev-parse", "HEAD").strip()
    touched = set(stepgit.git(wt, "diff", "--name-only", f"HEAD...{branch}").split())
    for p in generated_changes(wt):
        if p in touched:
            stepgit.git(wt, "reset", "-q", "--", p)
            stepgit.git(wt, "checkout", "HEAD", "--", p)
            print(f"{p}: generated; the batch's version is taken, the next build writes it again")
    aside = {}
    for p in card_work(wt):
        if p in touched:
            full = os.path.join(wt, p)
            aside[p] = open(full, "rb").read() if os.path.exists(full) else None
            if in_head(wt, p):
                stepgit.git(wt, "checkout", "HEAD", "--", p)
            elif os.path.exists(full):
                os.remove(full)

    def put_back():
        for p, text in aside.items():
            full = os.path.join(wt, p)
            if text is None:
                if os.path.exists(full):
                    os.remove(full)
            else:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                open(full, "wb").write(text)

    try:
        return take_in(wt, batch, branch, before, aside, put_back, sierra, agent_dir, composer_rel)
    except Exception:
        if os.path.exists(os.path.join(wt, stepgit.git(wt, "rev-parse", "--git-path", "MERGE_HEAD").strip())):
            stepgit.git(wt, "merge", "--abort", check=False)
        if stepgit.git(wt, "rev-parse", "HEAD").strip() != before:
            for p in aside:
                if in_head(wt, p):
                    stepgit.git(wt, "checkout", "HEAD", "--", p, check=False)
                elif os.path.exists(os.path.join(wt, p)):
                    os.remove(os.path.join(wt, p))
            stepgit.git(wt, "reset", "-q", "--keep", before, check=False)
        put_back()
        raise


def take_in(wt, batch, branch, before, aside, put_back, sierra, agent_dir, composer_rel):
    """Steps 4 to 7, from the merge on."""
    code, what = merge_ref(wt, branch)
    if code:
        put_back()
        print(f"merging {branch} conflicts in {what}: aborted, the card's work put back")
        return 3, [f"did not take batch {batch} in: the batch conflicts with the card's branch in {what}"]

    left = []
    for p, text in aside.items():
        if text is None:
            left.append(p)
            continue
        merged, clean = merge_three(text, blob(wt, before, p), blob(wt, "HEAD", p))
        if not clean and p.endswith(".tests.ts"):
            joined = both_sims(merged.decode("utf-8"))
            merged, clean = (joined.encode("utf-8"), True) if joined is not None else (merged, False)
        if clean:
            full = os.path.join(wt, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "wb").write(merged)
            print(f"{p}: the card's work merged onto the batch's change")
        else:
            left.append(p)
    if left:
        for p in aside:
            if in_head(wt, p):
                stepgit.git(wt, "checkout", "HEAD", "--", p)
            elif os.path.exists(os.path.join(wt, p)):
                os.remove(os.path.join(wt, p))
        packages = any(os.path.basename(f) in ("pnpm-lock.yaml", "package.json")
                       for f in stepgit.git(wt, "diff", "--name-only", before, "HEAD").split())
        stepgit.git(wt, "reset", "-q", "--keep", before)
        if packages:
            run(["pnpm", "-C", wt, "install", "--frozen-lockfile"])
        put_back()
        print("the card's work conflicts with the batch in " + ", ".join(left) + ": the merge taken back, the card's work put back")
        return 3, [f"did not take batch {batch} in: the card's uncommitted work conflicts with it in " + ", ".join(left)]

    head = stepgit.git(wt, "rev-parse", "--short", "HEAD").strip()
    kept = "; the card's work merged onto it in " + ", ".join(os.path.basename(p) for p in aside) if aside else ""
    tree = snapshot(wt, composer_rel)
    for cmd in (["lint"], ["push", "--replace", "-y"], ["pull"]):
        code, _ = run([sierra, "-C", agent_dir, "ghostwriter"] + cmd)
        if code:
            print(f"ghostwriter {cmd[0]} failed; the workspace may not hold the tree")
            return 4, [f"took batch {batch} in at {head}{kept}, but ghostwriter {cmd[0]} failed: the workspace may not hold it", "git:" + head]
    after = snapshot(wt, composer_rel)
    if after != tree:
        differ = sorted(p for p in set(tree) | set(after) if tree.get(p) != after.get(p))
        print("after the push, the workspace still differs from the tree: " + ", ".join(differ))
        return 4, [f"took batch {batch} in at {head}{kept}, but the workspace differs from the tree in " + ", ".join(differ), "git:" + head]
    print(f"{what}; the card's work is uncommitted on top and the workspace holds the tree")
    return 0, [f"took batch {batch} in: {what}{kept}; the workspace holds the tree", "git:" + head]


def main(argv):
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1] == "--pages")]
    if len(args) != 2 or args[0] not in AGENT_DIR or not args[1].isdigit():
        print(__doc__); return 64
    agent, n = args
    pages = cardlog.pages_dir(argv[argv.index("--pages") + 1] if "--pages" in argv[:-1] else None)
    path = paths.status(paths.agent(pages, agent), n, "sync")
    st = {"state": "working", "pid": os.getpid(), "started": stamp(), "head": head_of(pages, agent, n)}
    save(path, st)
    try:
        code, what = sync(agent, n, pages)
    except Exception as ex:
        code, what = 1, [f"did not take the batch in: {type(ex).__name__}: {ex}"]
    if what:
        cardlog.add(pages, agent, n, "cardsync", what[0], what[1:])
    st.update(state="done" if code == 0 else "refused" if code == 5 else "failed", code=code, ended=stamp(),
              merged=bool(code == 0 and what), what=what[0] if what else "")
    if code and code != 5:
        st["error"] = what[0] if what else f"exit {code}"
    save(path, st)
    return code


def stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def head_of(pages, agent, n):
    """The batch branch's commit the run starts from: a failure is not retried until the batch moves on."""
    wt = stepgit.load(paths.status(paths.agent(pages, agent), n, "setup")).get("worktree")
    branch = batch_branch(pages, agent, n)[1]
    if not wt or not branch or not os.path.isdir(wt):
        return None
    r = subprocess.run(["git", "-C", wt, "rev-parse", "--verify", "-q", branch + "^{commit}"], capture_output=True, text=True)
    return r.stdout.strip() or None


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
