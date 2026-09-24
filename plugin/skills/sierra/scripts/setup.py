#!/usr/bin/env python3
"""Give one issue its own checkout and its own Studio workspace, so the issue's steps run there in parallel with others.

  setup.py <agent> <n> [--pages <dir>] [--repo <dir>] [--base <branch>] [--batch <MMDD>]

Per issue <prefix>-<n> (cob-, opp-, hip-): a linked worktree at <repo>/.claude/worktrees/<prefix>-<n> on branch
stan/<prefix>-<n> forked from --base, the batch's branch (default: the main checkout's HEAD; a base branch that exists
neither locally nor on origin is created off main first), the repo hook skipped; the main checkout's
untracked state shared the way that hook shares it (skills and .targets linked, composer lockfile and .gitignore copied),
pnpm install in the agent dir; the Studio workspace <prefix>-<n> connected or created (`sierra add-workspace --create`);
Ghostwriter bound to it and the worktree's Studio content pushed there (init, pull, restore the tree, lint, push, pull).
Existing worktree, branch or workspace of that name are adopted, never replaced.

Writes agents/<agent>/setup/<n>.status.json for the page: state working/done/failed, pid, times, the lane's name, worktree,
branch, base commit, workspace url, the steps done, the error tail. Every command's output goes to stdout (the page's
run.log). Nothing else on disk changes; the worktree is left for `git worktree remove` when the issue is done."""
import fcntl, json, os, re, signal, subprocess, sys, time
from datetime import datetime, timezone
import paths

AGENT_DIR = {"cobranzas": "agents/base", "openpay": "agents/openpay", "hipotecarios": "agents/hipotecarios"}
PREFIX = {"cobranzas": "cob", "openpay": "opp", "hipotecarios": "hip"}
STUDIO_AGENT = {"cobranzas": "Cobranzas", "openpay": "Openpay", "hipotecarios": "Hipotecarios"}
NULL_HOOKS = ["-c", "core.hooksPath=/dev/null"]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)


def sh(cmd, cwd=None, check=True):
    """Run a command, echo its output, return (rc, output). check=True raises on failure with the output's tail."""
    log("$", " ".join(cmd) + (f"   (in {cwd})" if cwd else ""))
    r = subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(out, flush=True)
    if check and r.returncode:
        raise RuntimeError(f"{os.path.basename(cmd[0])} {cmd[1] if len(cmd) > 1 else ''}".strip() + " failed: " + out[-400:])
    return r.returncode, out


def link_entries(src_dir, dst_dir):
    """One symlink per entry of src_dir that dst_dir lacks (the hook's link_entries)."""
    if not os.path.isdir(src_dir):
        return
    os.makedirs(dst_dir, exist_ok=True)
    for name in os.listdir(src_dir):
        if name == ".DS_Store":
            continue
        dst = os.path.join(dst_dir, name)
        if not os.path.lexists(dst):
            os.symlink(os.path.join(src_dir, name), dst)


def copy_if_missing(src, dst):
    if os.path.exists(src) and not os.path.lexists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(src, "rb") as a, open(dst, "wb") as b:
            b.write(a.read())


def sync_sequence(sierra, agent_dir, wt, composer_rel):
    """The Ghostwriter commands that make the bound workspace hold the tree's Studio content: pull, restore the tree,
    lint, push, pull, restore. (title, argv) pairs."""
    return [
        ("ghostwriter pull", [sierra, "-C", agent_dir, "ghostwriter", "pull"]),
        ("restore the tree's studio files", ["git", "-C", wt, "checkout", "--", composer_rel]),
        ("ghostwriter lint", [sierra, "-C", agent_dir, "ghostwriter", "lint"]),
        ("ghostwriter push", [sierra, "-C", agent_dir, "ghostwriter", "push"]),
        ("ghostwriter pull after push", [sierra, "-C", agent_dir, "ghostwriter", "pull"]),
        ("restore the tree's studio files after the pull", ["git", "-C", wt, "checkout", "--", composer_rel]),
    ]


class Setup:
    def __init__(self, agent, n, pages, repo, base, batch):
        self.agent, self.n, self.pages, self.repo = agent, n, pages, repo
        self.name = f"{PREFIX[agent]}-{n}"
        self.branch = f"stan/{self.name}"
        self.wt = os.path.join(repo, ".claude", "worktrees", self.name)
        self.agent_rel = AGENT_DIR[agent]
        self.agent_dir = os.path.join(self.wt, self.agent_rel)
        self.sierra = os.path.join(self.agent_dir, "node_modules", ".bin", "sierra")
        self.base_ref = base
        self.status_path = paths.status(paths.agent(pages, agent), n, "setup")
        self.status = {"state": "working", "pid": os.getpid(), "started": now(), "name": self.name, "worktree": self.wt,
                       "branch": self.branch, "batch": batch, "steps": []}
        write_json(self.status_path, self.status)

    def step(self, title):
        log("==", title)
        self.status["steps"].append(title)
        self.status["step"] = title
        write_json(self.status_path, self.status)

    def worktree(self):
        """Under one lock per repository: setups of one batch share the base branch and the main checkout's .git, and
        two of them creating the branch or adding a worktree at once would trip each other."""
        self.step("worktree")
        lock_path = os.path.join(self.repo, ".claude", "worktrees", ".setup.lock")
        os.makedirs(os.path.dirname(lock_path), exist_ok=True)
        with open(lock_path, "w") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                self.step("waiting for another setup")
                fcntl.flock(lock, fcntl.LOCK_EX)
                self.step("worktree")
            self._worktree()

    def _worktree(self):
        if os.path.isdir(os.path.join(self.wt, ".git")) or os.path.isfile(os.path.join(self.wt, ".git")):
            log("adopting the existing worktree", self.wt)
        else:
            rc, _ = sh(["git", "-C", self.repo, "rev-parse", "--verify", "--quiet", "refs/heads/" + self.branch], check=False)
            if rc == 0:
                log("branch exists, checking it out")
                sh(["git", "-C", self.repo] + NULL_HOOKS + ["worktree", "add", self.wt, self.branch])
            else:
                base = self.base_ref or sh(["git", "-C", self.repo, "rev-parse", "--abbrev-ref", "HEAD"])[1]
                if self.base_ref:
                    self.base_branch(base)
                sh(["git", "-C", self.repo] + NULL_HOOKS + ["worktree", "add", "-b", self.branch, self.wt, base])
                self.status["base"] = base
        self.status["commit"] = sh(["git", "-C", self.wt, "rev-parse", "--short", "HEAD"])[1]

    def base_branch(self, base):
        """Make sure the batch's base branch exists locally: as is, tracking origin's, or new off main."""
        if sh(["git", "-C", self.repo, "rev-parse", "--verify", "--quiet", "refs/heads/" + base], check=False)[0] == 0:
            return
        sh(["git", "-C", self.repo, "fetch", "--quiet", "origin", base], check=False)
        if sh(["git", "-C", self.repo, "rev-parse", "--verify", "--quiet", "refs/remotes/origin/" + base], check=False)[0] == 0:
            log("base branch exists on origin, tracking it")
            sh(["git", "-C", self.repo, "branch", "--track", base, "origin/" + base])
            return
        log("base branch is new, creating it off main")
        sh(["git", "-C", self.repo, "branch", base, "main"])
        self.status["base_created"] = True

    def share(self):
        self.step("share main's local state")
        link_entries(os.path.join(self.repo, ".claude", "skills"), os.path.join(self.wt, ".claude", "skills"))
        link_entries(os.path.join(self.repo, self.agent_rel, ".targets"), os.path.join(self.agent_dir, ".targets"))
        for f in ("pnpm-lock.yaml", ".gitignore"):
            copy_if_missing(os.path.join(self.repo, self.agent_rel, ".composer", f), os.path.join(self.agent_dir, ".composer", f))

    def install(self):
        self.step("pnpm install")
        if os.path.exists(self.sierra):
            log("node_modules present, skipping")
            return
        sh(["pnpm", "--dir", self.agent_dir, "install", "--prefer-offline", "--silent"])
        if not os.path.exists(self.sierra):
            raise RuntimeError("pnpm install left no sierra CLI at " + self.sierra)

    def workspace(self):
        self.step("studio workspace")
        target = os.path.join(self.agent_dir, ".targets", self.name)
        if os.path.exists(target):
            log("target exists", target)
        else:
            sh([self.sierra, "-C", self.agent_dir, "add-workspace", "bbva", STUDIO_AGENT[self.agent], self.name, "--create"])
            if not os.path.exists(target):
                raise RuntimeError("add-workspace wrote no target at " + target)
        self.status["workspace"] = open(target, encoding="utf-8").read().strip()

    def ghostwriter(self):
        """Bind the worktree's Ghostwriter to the lane workspace and push the tree's content there (the lanes.py sequence)."""
        composer_rel = os.path.join(self.agent_rel, ".composer")
        meta = os.path.join(self.agent_dir, ".composer", "build", "workspace-meta.json")
        try:
            bound = json.load(open(meta))
        except Exception:
            bound = {}
        if bound.get("targetUrl") == self.status.get("workspace"):
            self.step("ghostwriter already bound")
            return
        for title, cmd in [("ghostwriter init", [self.sierra, "-C", self.agent_dir, "ghostwriter", "init", self.name])] + \
                sync_sequence(self.sierra, self.agent_dir, self.wt, composer_rel):
            self.step(title)
            sh(cmd)

    def run(self):
        try:
            self.worktree(); self.share(); self.install(); self.workspace(); self.ghostwriter()
            self.status.update(state="done")
        except Exception as ex:
            self.status.update(state="failed", error=str(ex)[-600:])
            log("FAILED", ex)
        finally:
            self.status.pop("step", None)
            self.status.update(ended=now(), seconds=int(time.time() - self.t0))
            write_json(self.status_path, self.status)
            import cardlog
            st = self.status
            cardlog.add(self.pages, self.agent, self.n, "setup",
                        f"worktree {st.get('worktree')} on {st.get('branch')} off {st.get('base') or 'its existing branch'}, "
                        f"workspace {st.get('name')}" if st["state"] == "done" else "failed: " + str(st.get("error")),
                        ["git:" + st["commit"]] if st.get("commit") else [])
        return 0 if self.status["state"] == "done" else 1


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    if len(args) < 2 or args[0] not in AGENT_DIR or not re.fullmatch(r"\d+", args[1]):
        sys.exit(__doc__)
    pages = os.path.abspath(opts.get("--pages") or os.getcwd())
    repo = os.path.abspath(opts.get("--repo") or os.getcwd())
    s = Setup(args[0], args[1], pages, repo, opts.get("--base"), opts.get("--batch") or "")
    s.t0 = time.time()

    def on_term(signum, frame):  # the page's stop button: mark the run, then end this process group, children included
        s.status.pop("step", None)
        s.status.update(state="failed", error="stopped from the page", ended=now(), seconds=int(time.time() - s.t0))
        write_json(s.status_path, s.status)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        os.killpg(os.getpgid(0), signal.SIGTERM)
    signal.signal(signal.SIGTERM, on_term)
    return s.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
