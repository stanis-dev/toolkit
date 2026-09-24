"""Run the card's guard 5× on its workspace, from the card's tree as it is now.

Usage:
  guard.py <agent> <n> [--regressions] [--pages <dir>]

The guard is the strategy answer's guard.id. The run goes to strategy/runs/guard-now.json and .id, beside the
strategy's guard-red.json from before the fix, which it leaves alone; a copy goes to strategy/history/<stamp>.guard-now.json,
which the card's history event points to. On a simulation's card, a failing replay of the run becomes the card's
conversation, so the next steps read a failure of the tree as it is. strategy/guard.json holds the run's state while
it works and its result after; the Sim Strategy is rendered again.

With --regressions it runs the strategy answer's regression sims 5× instead: the run goes to
strategy/runs/regressions-now.json and .id, beside the before-the-fix regressions.json, with a copy under history/;
strategy/regressions-run.json holds its state; the card shows each sim's count before › now.

replays() gives the page's guard drawer both runs with their replays, each replay copied into the agent's conversation
cache so the transcript and context drawers read it like any call.
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
import simcard  # noqa: E402
import source  # noqa: E402
from setup import AGENT_DIR  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write(path, d):
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1)
    os.replace(path + ".tmp", path)


def replays(pages, agent, n):
    """[{name, run, passed, total, replays: [{id, passed, why}]}] for guard-red, then guard-now, those that ran."""
    base = paths.agent(pages, agent)
    setup = json.load(open(paths.status(base, n, "setup"), encoding="utf-8"))
    agent_dir = os.path.join(setup["worktree"], AGENT_DIR[agent])
    out = []
    for name in ("guard-red", "guard-now"):
        run = paths.guard_red(base, n, name)
        if not run:
            continue
        rows = []
        for rdir in simcard.results(agent_dir, setup["name"], run):
            res = json.load(open(os.path.join(rdir, "result.json"), encoding="utf-8"))
            rid = res.get("id") or os.path.basename(rdir)
            if not os.path.isdir(paths.conversation(base, rid)):
                shutil.copytree(rdir, paths.conversation(base, rid))
            why = simcard.failed(res)
            rows.append({"id": rid, "passed": res.get("status") == "PASSED", "status": res.get("status"), "why": why})
        out.append({"name": name, **run, "replays": rows})
    return out


def regressions(base, n, pages, setup, stamp):
    """The regression sims 5× on the card's workspace: the history event's text and the kept run file."""
    reg = (json.load(open(paths.answer(base, n, "strategy"), encoding="utf-8")).get("regressions") or {}).get("sims") or []
    ids = [r["id"] for r in reg if r.get("id")]
    if not ids:
        raise RuntimeError("the strategy answer lists no regression sims")
    agent_dir = os.path.join(setup["worktree"], AGENT_DIR[setup["agent"]])
    runs = paths.runs(base, n, "strategy")
    os.makedirs(runs, exist_ok=True)
    sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
    path = os.path.join(runs, "regressions-now.json")
    with open(path, "w") as out:
        subprocess.run([sierra, "-C", agent_dir, "test", setup["name"], "--names", *ids, "--num-runs", "5", "--json", "-y",
                        "--run-id-file", os.path.join(runs, "regressions-now.id")], stdout=out, stderr=subprocess.PIPE, check=False)
    try:
        d = json.load(open(path, encoding="utf-8"))
    except ValueError:
        d = {}
    tests = d.get("tests") or []
    if not tests:
        raise RuntimeError(f"the run of the regression sims matched no simulation: {path}")
    kept = paths.history(base, n, "strategy", stamp, "regressions-now.json")
    os.makedirs(os.path.dirname(kept), exist_ok=True)
    shutil.copy(path, kept)
    reds = [f"{t['name']} {t['passed']}/{t['total']}" for t in tests if t.get("passed") != t.get("total")]
    what = (f"ran the {len(tests)} regression sims 5×: {len(tests) - len(reds)}/{len(tests)} green, run {d.get('simulationRunId')}"
            + (f"; red: {', '.join(reds)}" if reds else ""))
    return what, kept, {"passed": len(tests) - len(reds), "total": len(tests), "run": d.get("simulationRunId")}


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    agent, n = argv[0], argv[1]
    reg_mode = "--regressions" in argv
    argv = [a for a in argv if a != "--regressions"]
    opts = dict(zip(argv[2::2], argv[3::2]))
    pages = paths.pages_dir(opts.get("--pages"))
    base = paths.agent(pages, agent)
    state_path = os.path.join(paths.card_dir(base, n), "strategy", "regressions-run.json" if reg_mode else "guard.json")
    state = {"state": "working", "started": now(), "ended": None, "pid": os.getpid(), "error": None}
    write(state_path, state)
    try:
        setup = json.load(open(paths.status(base, n, "setup"), encoding="utf-8"))
        if reg_mode:
            stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
            what, kept, result = regressions(base, n, pages, dict(setup, agent=agent), stamp)
            subprocess.run([sys.executable, os.path.join(HERE, "card.py"), "ss", agent, n, "--pages", pages, "--repo", setup["worktree"]],
                           capture_output=True, check=True)
            cardlog.add(pages, agent, n, "engineer", what, [cardlog.rel(pages, agent, kept)])
            state.update(state="done", ended=now(), **result)
            write(state_path, state)
            sys.exit(0)
        guard = (json.load(open(paths.answer(base, n, "strategy"), encoding="utf-8")).get("guard") or {}).get("id")
        if not guard:
            raise RuntimeError("the strategy answer names no guard")
        repo, workspace = setup["worktree"], setup["name"]
        agent_dir = os.path.join(repo, AGENT_DIR[agent])
        runs = paths.runs(base, n, "strategy")
        os.makedirs(runs, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
        with open(os.path.join(runs, "guard-now.json"), "w") as out:
            subprocess.run([sierra, "-C", agent_dir, "test", workspace, "--names", guard, "--num-runs", "5", "--json", "-y",
                            "--run-id-file", os.path.join(runs, "guard-now.id")], stdout=out, stderr=subprocess.PIPE, check=False)
        now_run = paths.guard_red(base, n, "guard-now")
        if not now_run:
            raise RuntimeError(f"the run of {guard} matched no simulation: {os.path.join(runs, 'guard-now.json')}")
        kept = paths.history(base, n, "strategy", stamp, "guard-now.json")
        os.makedirs(os.path.dirname(kept), exist_ok=True)
        shutil.copy(os.path.join(runs, "guard-now.json"), kept)
        what = f"ran the guard {guard} 5×: {now_run['passed']}/{now_run['total']} pass, run {now_run['run']}"
        if (source.load(base, n) or {}).get("kind") == "sim" and now_run["passed"] < now_run["total"]:
            simcard.adopt(base, n, agent_dir, workspace, now_run)
            what += "; a failing replay of it is the card's conversation now"
        subprocess.run([sys.executable, os.path.join(HERE, "card.py"), "ss", agent, n, "--pages", pages, "--repo", repo],
                       capture_output=True, check=True)
        cardlog.add(pages, agent, n, "engineer", what, [cardlog.rel(pages, agent, kept)])
        state.update(state="done", ended=now(), **now_run)
    except Exception as ex:
        state.update(state="failed", ended=now(), error=f"{type(ex).__name__}: {ex}")
    write(state_path, state)
    sys.exit(0 if state["state"] == "done" else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
