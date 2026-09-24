"""Open a card from one failing simulation replay.

Usage:
  simcard.py <agent> <result-dir> [--pages <dir>]

<result-dir> is one results/<result> folder of a downloaded run (.composer/simulations/replaytestrunset-<id>/results/
replaytestresult-<id>/). The card gets the next number from 10001 up, the tracker's numbers staying below. Into the
card folder go a copy of that one replay under conversations/<result>/ (debug.log, result.json, traces/) and
source.json (see source.py): the simulation's name, what failed (the unmet expectations with the judge's reasoning,
the tag misses), its definition from the run's test ref, and the branch of the checkout the run was downloaded into:
setup forks the card's worktree from it, so the simulation is in the card's tree. Setup then runs the simulation 5× on
the card's workspace (reproduce): that run is the Sim Strategy's red run, and one of its failing replays replaces the
first one, so every step reads a failure of the card's own tree. Prints the card's number. Everything else the card
recreates itself: its steps run the simulation again.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402
import source  # noqa: E402

FIRST = 10001


def fail(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def definition(sims_dir, test_id):
    """The run's test ref for the simulation, matched on the id's last part (the ref's id carries a variant infix)."""
    tail = test_id.rsplit("-", 1)[-1]
    for f in sorted(glob.glob(os.path.join(sims_dir, "test_refs", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if str(d.get("id", "")).rsplit("-", 1)[-1] == tail:
            return d
    return {}


def failed(res):
    """What failed, as text: each unmet expectation with the judge's reasoning, then the tag misses."""
    out = []
    for o in res.get("outcomeEvalResults") or []:
        if not o.get("metExpectation", False):
            out += [f"- Expected: {o.get('expectedOutcome', '')}", f"  Judge: {o.get('reasoning', '')}"]
    tags = set(res.get("tags") or [])
    exp = res.get("tagExpectations") or {}
    missing = [t for t in exp.get("present") or [] if t not in tags]
    unexpected = [t for t in exp.get("absent") or [] if t in tags]
    if missing:
        out.append("- Missing tags: " + ", ".join(missing))
    if unexpected:
        out.append("- Unexpected tags: " + ", ".join(unexpected))
    return "\n".join(out)


def next_number(base):
    d = os.path.join(base, "cards")
    taken = [int(f) for f in os.listdir(d) if f.isdigit()] if os.path.isdir(d) else []
    return max([FIRST - 1] + [k for k in taken if k >= FIRST]) + 1


def replay(base, n, rdir, branch):
    """The card's source from one failing replay: its copy under conversations/<result>/ replaces any earlier one."""
    res = json.load(open(os.path.join(rdir, "result.json"), encoding="utf-8"))
    sims_dir = os.path.dirname(os.path.dirname(os.path.dirname(rdir)))
    d = definition(sims_dir, res.get("replayTestId") or "")
    names = json.load(open(os.path.join(sims_dir, "test-names.json"), encoding="utf-8")) if os.path.exists(os.path.join(sims_dir, "test-names.json")) else {}
    rid = res.get("id") or os.path.basename(rdir)
    conv = os.path.join(paths.card_dir(base, n), "conversations")
    if os.path.isdir(conv):
        shutil.rmtree(conv)
    os.makedirs(conv)
    shutil.copytree(rdir, os.path.join(conv, rid))
    src = {"kind": "sim", "number": int(n), "title": d.get("name") or names.get(res.get("replayTestId")) or res.get("replayTestId") or "",
           "description": failed(res), "comments": [],
           "ref": {"test": res.get("replayTestId"), "run": res.get("runSetId"), "result": rid, "status": res.get("status"),
                   "branch": branch},
           "definition": d,
           "conversations": [{"id": rid, "timestamp": res.get("creationTime") or "", "marked": []}]}
    with open(source.path(base, n), "w", encoding="utf-8") as f:
        json.dump(src, f, ensure_ascii=False, indent=1)


def reproduce(base, n, agent_dir, workspace):
    """Run the card's simulation 5× on its own workspace as the Sim Strategy's red run, then make a failing replay of
    that run the card's conversation. Returns the run's {run, passed, total}."""
    src = source.load(base, n)
    runs = paths.runs(base, n, "strategy")
    os.makedirs(runs, exist_ok=True)
    sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
    with open(os.path.join(runs, "guard-red.json"), "w") as out:
        subprocess.run([sierra, "-C", agent_dir, "test", workspace, "--names", src["title"], "--num-runs", "5", "--json", "-y",
                        "--run-id-file", os.path.join(runs, "guard-red.id")], stdout=out, check=False)
    red = paths.guard_red(base, n)
    if not red:
        raise RuntimeError(f"the run of «{src['title']}» matched no simulation: {os.path.join(runs, 'guard-red.json')}")
    if red["passed"] < red["total"]:
        adopt(base, n, agent_dir, workspace, red)
    return red


def results(agent_dir, workspace, run):
    """The result folders of run {run, passed, total}, oldest first, downloaded into the checkout's .composer when
    fewer than its total are there."""
    pat = os.path.join(agent_dir, ".composer", "simulations", f"replaytestrunset-{run['run']}", "results", "*", "result.json")
    if len(glob.glob(pat)) < run["total"]:
        sierra = os.path.join(agent_dir, "node_modules", ".bin", "sierra")
        subprocess.run([sierra, "-C", agent_dir, "ghostwriter", "bbva.sierra.ai/" + workspace, "--download-simulations",
                        "--run-id", run["run"]], stdout=subprocess.DEVNULL, check=True)
    found = [(json.load(open(f, encoding="utf-8")), os.path.dirname(f)) for f in glob.glob(pat)]
    return [d for _, d in sorted(found, key=lambda x: x[0].get("creationTime") or "")]


def adopt(base, n, agent_dir, workspace, run):
    """Download run {run, passed, total} and make its first failing replay the card's conversation."""
    src = source.load(base, n)
    for rdir in results(agent_dir, workspace, run):
        if failed(json.load(open(os.path.join(rdir, "result.json"), encoding="utf-8"))):
            replay(base, n, rdir, src["ref"]["branch"])
            return
    raise RuntimeError(f"run {run['run']} has {run['total'] - run['passed']} failures but no failing replay was downloaded")


def main(argv):
    if len(argv) < 2:
        fail(__doc__)
    agent, rdir = argv[0], os.path.abspath(argv[1])
    opts = dict(zip(argv[2::2], argv[3::2]))
    base = paths.agent(paths.pages_dir(opts.get("--pages")), agent)
    rp = os.path.join(rdir, "result.json")
    if not os.path.exists(rp) or not os.path.exists(os.path.join(rdir, "debug.log")):
        fail(f"{rdir} is not a replay: it needs result.json and debug.log")
    if not failed(json.load(open(rp, encoding="utf-8"))):
        fail(f"{rdir} did not fail: every expectation met, no tag miss")
    git = subprocess.run(["git", "-C", rdir, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    if git.returncode != 0 or git.stdout.strip() in ("", "HEAD"):
        fail(f"{rdir} is not in a checkout on a branch: the card's worktree forks from the run's branch")
    n = str(next_number(base))
    replay(base, n, rdir, git.stdout.strip())
    open(paths.card(base, n), "a").close()
    print(n)


if __name__ == "__main__":
    main(sys.argv[1:])
