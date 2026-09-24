"""Run the card's guard 5× on its workspace, from the card's tree, as the Sim Strategy's red run.

Usage:
  guard.py <agent> <n> [--pages <dir>]

The guard is the strategy answer's guard.id. The run replaces strategy/runs/guard-red.json and .id; the ones it
replaces go to strategy/history/<stamp>.guard-red.*. strategy/guard.json holds the run's state while it works and
its result after, the Sim Strategy is rendered again and the run is one event of the card's history.
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cardlog  # noqa: E402
import paths  # noqa: E402
from setup import AGENT_DIR  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write(path, d):
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1)
    os.replace(path + ".tmp", path)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    agent, n = argv[0], argv[1]
    opts = dict(zip(argv[2::2], argv[3::2]))
    pages = paths.pages_dir(opts.get("--pages"))
    base = paths.agent(pages, agent)
    state_path = os.path.join(paths.card_dir(base, n), "strategy", "guard.json")
    state = {"state": "working", "started": now(), "ended": None, "pid": os.getpid(), "error": None}
    write(state_path, state)
    try:
        setup = json.load(open(paths.status(base, n, "setup"), encoding="utf-8"))
        guard = (json.load(open(paths.answer(base, n, "strategy"), encoding="utf-8")).get("guard") or {}).get("id")
        if not guard:
            raise RuntimeError("the strategy answer names no guard")
        repo, workspace = setup["worktree"], setup["name"]
        agent_dir = os.path.join(repo, AGENT_DIR[agent])
        runs = paths.runs(base, n, "strategy")
        os.makedirs(runs, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        for ext in ("json", "id"):
            f = os.path.join(runs, "guard-red." + ext)
            if os.path.exists(f):
                h = paths.history(base, n, "strategy", stamp, "guard-red." + ext)
                os.makedirs(os.path.dirname(h), exist_ok=True)
                shutil.move(f, h)
        sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
        with open(os.path.join(runs, "guard-red.json"), "w") as out:
            subprocess.run([sierra, "-C", agent_dir, "test", workspace, "--names", guard, "--num-runs", "5", "--json", "-y",
                            "--run-id-file", os.path.join(runs, "guard-red.id")], stdout=out, stderr=subprocess.PIPE, check=False)
        red = paths.guard_red(base, n)
        if not red:
            raise RuntimeError(f"the run of {guard} matched no simulation: {os.path.join(runs, 'guard-red.json')}")
        subprocess.run([sys.executable, os.path.join(HERE, "card.py"), "ss", agent, n, "--pages", pages, "--repo", repo],
                       capture_output=True, check=True)
        cardlog.add(pages, agent, n, "engineer", f"ran the guard {guard} 5×: {red['passed']}/{red['total']} pass, run {red['run']}",
                    [cardlog.rel(pages, agent, os.path.join(runs, "guard-red.json"))])
        state.update(state="done", ended=now(), **red)
    except Exception as ex:
        state.update(state="failed", ended=now(), error=f"{type(ex).__name__}: {ex}")
    write(state_path, state)
    sys.exit(0 if state["state"] == "done" else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
