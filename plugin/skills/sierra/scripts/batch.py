#!/usr/bin/env python3
"""Give a batch its own checkout and Studio workspace, or take them away.

  batch.py create <agent> <MMDD> --branch <branch> [--pages <dir>] [--repo <dir>]
  batch.py delete <agent> <MMDD> [--pages <dir>] [--repo <dir>]

create: the branch must exist, locally or on origin, and be checked out nowhere else. A linked worktree at
<repo>/.claude/worktrees/<name> on it, <name> being the branch with every / as -, the repo hook skipped; the main
checkout's untracked state shared and pnpm install, as setup.py does; the Studio workspace <name> connected or created;
Ghostwriter bound to it and the branch's Studio content pushed there. An existing worktree or workspace of that name is
adopted. When done, agents/<agent>/batches.json holds {"<MMDD>": {"base": <branch>, "workspace": <name>, "worktree":
<path>}}; a batch that had another worktree and workspace before loses them then.

delete: the workspace deleted, the worktree removed, every card of the batch moved to no batch, the batch taken out of
batches.json. Refused while the worktree has changes other than the files setup copies in. The branch stays.

Status in agents/<agent>/batches/<MMDD>.status.json: state working/done/failed, pid, times, the steps done, the error
tail. Every command's output goes to stdout (the page's run.log)."""
import json, os, re, signal, sys, time

import setup
from setup import AGENT_DIR, NULL_HOOKS, log, now, sh, write_json


class Batch(setup.Setup):
    def __init__(self, action, agent, batch, pages, repo, branch):
        self.action, self.agent, self.batch, self.pages, self.repo = action, agent, batch, pages, repo
        self.batches_path = os.path.join(pages, "agents", agent, "batches.json")
        self.entry = self.load().get(batch) or {}
        self.branch = branch or self.entry.get("base") or ""
        self.name = self.branch.replace("/", "-")
        self.wt = os.path.join(repo, ".claude", "worktrees", self.name)
        self.agent_rel = AGENT_DIR[agent]
        self.agent_dir = os.path.join(self.wt, self.agent_rel)
        self.sierra = os.path.join(self.agent_dir, "node_modules", ".bin", "sierra")
        self.status_path = os.path.join(pages, "agents", agent, "batches", f"{batch}.status.json")
        self.status = {"state": "working", "action": action, "pid": os.getpid(), "started": now(), "batch": batch,
                       "branch": self.branch, "name": self.name, "worktree": self.wt, "steps": []}
        write_json(self.status_path, self.status)

    def load(self):
        try:
            return json.load(open(self.batches_path))
        except Exception:
            return {}

    def save(self, entry):
        data = self.load()
        if entry is None:
            data.pop(self.batch, None)
        else:
            data[self.batch] = entry
        write_json(self.batches_path, data)

    def _worktree(self):
        if os.path.exists(os.path.join(self.wt, ".git")):
            log("adopting the existing worktree", self.wt)
            head = sh(["git", "-C", self.wt, "rev-parse", "--abbrev-ref", "HEAD"])[1]
            if head != self.branch:
                raise RuntimeError(f"{self.wt} is on {head}, not {self.branch}")
            return
        if sh(["git", "-C", self.repo, "rev-parse", "--verify", "--quiet", "refs/heads/" + self.branch], check=False)[0] != 0:
            sh(["git", "-C", self.repo, "fetch", "--quiet", "origin", self.branch], check=False)
            if sh(["git", "-C", self.repo, "rev-parse", "--verify", "--quiet", "refs/remotes/origin/" + self.branch], check=False)[0] != 0:
                raise RuntimeError(f"no branch {self.branch}, locally or on origin")
            sh(["git", "-C", self.repo, "branch", "--track", self.branch, "origin/" + self.branch])
        holder = checked_out_at(self.repo, self.branch)
        if holder:
            raise RuntimeError(f"{self.branch} is checked out at {holder}: move that checkout to another branch first")
        sh(["git", "-C", self.repo] + NULL_HOOKS + ["worktree", "add", self.wt, self.branch])

    def teardown(self, name, wt):
        """Delete workspace <name> and remove worktree <wt>; refused while the worktree has changes of its own."""
        agent_dir = os.path.join(wt, self.agent_rel)
        if os.path.exists(os.path.join(wt, ".git")):
            copied = {f"{self.agent_rel}/.composer/pnpm-lock.yaml", f"{self.agent_rel}/.composer/.gitignore"}
            dirty = [l for l in sh(["git", "-C", wt, "status", "--porcelain"])[1].splitlines() if l[3:] not in copied]
            if dirty:
                raise RuntimeError(f"{wt} has changes, commit or drop them first: " + "; ".join(dirty[:5]))
        if name and os.path.exists(os.path.join(agent_dir, ".targets", name)):
            self.step("delete workspace " + name)
            sh([os.path.join(agent_dir, "node_modules", ".bin", "sierra"), "-C", agent_dir, "delete-workspace", name])
        if os.path.exists(os.path.join(wt, ".git")):
            self.step("remove worktree")
            sh(["git", "-C", self.repo, "worktree", "remove", "--force", wt])

    def create(self):
        old = self.entry if self.entry.get("worktree") and self.entry.get("worktree") != self.wt else None
        self.worktree(); self.share(); self.install(); self.workspace(); self.ghostwriter()
        if old:
            self.teardown(old.get("workspace"), old["worktree"])
        self.save({"base": self.branch, "workspace": self.name, "worktree": self.wt})

    def delete(self):
        if self.entry.get("worktree"):
            self.teardown(self.entry.get("workspace"), self.entry["worktree"])
        self.step("move the batch's cards to no batch")
        cards = os.path.join(self.pages, "agents", self.agent, "cards")
        for f in sorted(os.listdir(cards)) if os.path.isdir(cards) else []:
            path = os.path.join(cards, f)
            text = open(path, encoding="utf-8").read()
            new = re.sub(r"\A\s*<!--\s*batch:\s*" + self.batch + r"\s*-->\s*\n?", "", text)
            if new != text:
                with open(path + ".tmp", "w", encoding="utf-8") as out:
                    out.write(new)
                os.replace(path + ".tmp", path)
                log("moved", f)
        self.save(None)

    def run(self):
        try:
            if self.action == "create":
                if not self.branch:
                    raise RuntimeError("no branch")
                self.create()
            else:
                self.delete()
            self.status.update(state="done")
        except Exception as ex:
            self.status.update(state="failed", error=str(ex)[-600:])
            log("FAILED", ex)
        finally:
            self.status.pop("step", None)
            self.status.update(ended=now(), seconds=int(time.time() - self.t0))
            write_json(self.status_path, self.status)
        return 0 if self.status["state"] == "done" else 1


def checked_out_at(repo, branch):
    """The worktree that has <branch> checked out, or None."""
    path = None
    for line in sh(["git", "-C", repo, "worktree", "list", "--porcelain"])[1].splitlines():
        if line.startswith("worktree "):
            path = line[9:]
        elif line == "branch refs/heads/" + branch:
            return path
    return None


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    if len(args) < 3 or args[0] not in ("create", "delete") or args[1] not in AGENT_DIR or not re.fullmatch(r"\d{4}", args[2]):
        sys.exit(__doc__)
    pages = os.path.abspath(opts.get("--pages") or os.getcwd())
    repo = os.path.abspath(opts.get("--repo") or os.getcwd())
    b = Batch(args[0], args[1], args[2], pages, repo, opts.get("--branch"))
    b.t0 = time.time()

    def on_term(signum, frame):
        b.status.pop("step", None)
        b.status.update(state="failed", error="stopped from the page", ended=now(), seconds=int(time.time() - b.t0))
        write_json(b.status_path, b.status)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        os.killpg(os.getpgid(0), signal.SIGTERM)
    signal.signal(signal.SIGTERM, on_term)
    return b.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
