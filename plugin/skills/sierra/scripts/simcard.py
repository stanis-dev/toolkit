"""Open a card from one failing simulation replay.

Usage:
  simcard.py <agent> <result-dir> [--pages <dir>]

<result-dir> is one results/<result> folder of a downloaded run (.composer/simulations/replaytestrunset-<id>/results/
replaytestresult-<id>/). The card gets the next number from 10001 up, the tracker's numbers staying below. Into the
card folder go a copy of that one replay under conversations/<result>/ (debug.log, result.json, traces/) and
source.json (see source.py): the simulation's name, what failed (the unmet expectations with the judge's reasoning,
the tag misses), and its definition from the run's test ref. Prints the card's number. Everything else the card
recreates itself: its steps run the simulation again.
"""
import glob
import json
import os
import shutil
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


def main(argv):
    if len(argv) < 2:
        fail(__doc__)
    agent, rdir = argv[0], os.path.abspath(argv[1])
    opts = dict(zip(argv[2::2], argv[3::2]))
    base = paths.agent(paths.pages_dir(opts.get("--pages")), agent)
    rp = os.path.join(rdir, "result.json")
    if not os.path.exists(rp) or not os.path.exists(os.path.join(rdir, "debug.log")):
        fail(f"{rdir} is not a replay: it needs result.json and debug.log")
    res = json.load(open(rp, encoding="utf-8"))
    what = failed(res)
    if not what:
        fail(f"{res.get('id')} did not fail: every expectation met, no tag miss")
    sims_dir = os.path.dirname(os.path.dirname(os.path.dirname(rdir)))
    d = definition(sims_dir, res.get("replayTestId") or "")
    names = json.load(open(os.path.join(sims_dir, "test-names.json"), encoding="utf-8")) if os.path.exists(os.path.join(sims_dir, "test-names.json")) else {}
    n = str(next_number(base))
    cd = paths.card_dir(base, n)
    rid = res.get("id") or os.path.basename(rdir)
    os.makedirs(os.path.join(cd, "conversations"))
    shutil.copytree(rdir, os.path.join(cd, "conversations", rid))
    src = {"kind": "sim", "number": int(n), "title": d.get("name") or names.get(res.get("replayTestId")) or res.get("replayTestId") or "",
           "description": what, "comments": [],
           "ref": {"test": res.get("replayTestId"), "run": res.get("runSetId"), "result": rid, "status": res.get("status")},
           "definition": d,
           "conversations": [{"id": rid, "timestamp": res.get("creationTime") or "", "marked": []}]}
    with open(source.path(base, n), "w", encoding="utf-8") as f:
        json.dump(src, f, ensure_ascii=False, indent=1)
    open(paths.card(base, n), "a").close()
    print(n)


if __name__ == "__main__":
    main(sys.argv[1:])
