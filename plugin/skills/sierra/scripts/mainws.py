#!/usr/bin/env python3
"""Give a batch's driver a checkout of main alone and a Studio workspace that holds it, to count a simulation on main.

  mainws.py <agent> <batch> [--pages <dir>] [--repo <dir>]

A linked worktree at <repo>/.claude/worktrees (repo: the main checkout of the current directory's repository)/stan-<prefix>-main-<batch>, detached at origin/main (fetched first), the
main checkout's untracked state shared and pnpm install run as setup.py does; the Studio workspace of the same name
connected or created; Ghostwriter bound to it; then pull, restore the tree, lint, push --replace, pull, restore. Run again,
it moves the worktree to the latest origin/main and pushes that. Refused while the worktree has tracked changes.

Writes agents/<agent>/driver/<batch>.main.json: state working/done/failed, worktree, workspace url, the main commit it
holds, times, the error tail. Every command's output goes to stdout."""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import setup
import paths
from setup import PREFIX, AGENT_DIR, NULL_HOOKS, sh, now, write_json


class MainWorkspace(setup.Setup):
    def __init__(self, agent, batch, pages, repo):
        self.agent, self.n, self.pages, self.repo = agent, batch, pages, repo
        self.name = f"stan-{PREFIX[agent]}-main-{batch}"
        self.wt = os.path.join(repo, ".claude", "worktrees", self.name)
        self.agent_rel = AGENT_DIR[agent]
        self.agent_dir = os.path.join(self.wt, self.agent_rel)
        self.sierra = os.path.join(self.agent_dir, "node_modules", ".bin", "sierra")
        self.status_path = paths.step_file(paths.agent(pages, agent), batch, "driver", "main.json")
        self.status = {"state": "working", "pid": os.getpid(), "started": now(), "name": self.name, "worktree": self.wt,
                       "batch": batch, "steps": []}
        self.t0 = time.time()
        write_json(self.status_path, self.status)

    def _worktree(self):
        sh(["git", "-C", self.repo, "fetch", "--quiet", "origin", "main"])
        if os.path.exists(os.path.join(self.wt, ".git")):
            dirty = sh(["git", "-C", self.wt, "status", "--porcelain", "--untracked-files=no"])[1]
            dirty = [l for l in dirty.splitlines() if not l[3:].endswith(("content-types.ts", "platform-types.tsx"))]
            if dirty:
                raise RuntimeError("the main worktree has tracked changes: " + "; ".join(dirty))
            sh(["git", "-C", self.wt, "checkout", "--", "."])
            sh(["git", "-C", self.wt] + NULL_HOOKS + ["checkout", "--detach", "origin/main"])
        else:
            sh(["git", "-C", self.repo] + NULL_HOOKS + ["worktree", "add", "--detach", self.wt, "origin/main"])
        self.status["commit"] = sh(["git", "-C", self.wt, "rev-parse", "--short", "HEAD"])[1]

    def ghostwriter(self):
        composer_rel = os.path.join(self.agent_rel, ".composer")
        steps = setup.sync_sequence(self.sierra, self.agent_dir, self.wt, composer_rel)
        steps = [(t, c + ["--replace", "-y"] if t == "ghostwriter push" else c) for t, c in steps]
        meta = os.path.join(self.agent_dir, ".composer", "build", "workspace-meta.json")
        try:
            bound = json.load(open(meta)).get("targetUrl")
        except Exception:
            bound = None
        if bound != self.status.get("workspace"):
            steps = [("ghostwriter init", [self.sierra, "-C", self.agent_dir, "ghostwriter", "init", self.name])] + steps
        for title, cmd in steps:
            self.step(title)
            sh(cmd)


def main(argv):
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    if len(args) != 2 or args[0] not in AGENT_DIR:
        sys.exit(__doc__)
    pages = os.path.abspath(opts.get("--pages") or os.path.expanduser("~/.claude/bbva-issues"))
    repo = opts.get("--repo") or os.path.dirname(sh(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"])[1])
    repo = os.path.abspath(repo)
    return MainWorkspace(args[0], args[1], pages, repo).run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
