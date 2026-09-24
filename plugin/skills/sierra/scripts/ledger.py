#!/usr/bin/env python3
"""What each ticket has cost: one entry per model run, kept in <pages>/agents/<agent>/cost/<n>.json (a JSON list).

  ledger.py <agent> <n> [--pages <dir>]     prints the ticket's entries and total
  ledger.py backfill [--pages <dir>]        adds the runs recorded before the ledger existed; safe to repeat

An entry is {t, step, model, effort, state, in, cached, out, reasoning, commands, cost}; run.py adds one when an
answer's run ends, the pages server when a resolution session ends. Cost is the model provider's list price as pi
reports it. backfill takes the last run of each step from its status file and the last resolution session's log; runs
older than those left no record."""
import fcntl, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

KEYS = ("in", "cached", "out", "reasoning", "commands", "cost")


def path_of(pages, agent, n):
    return paths.cost(paths.agent(pages, agent), n)


def load(pages, agent, n):
    try:
        return json.load(open(path_of(pages, agent, n), encoding="utf-8"))
    except (OSError, ValueError):
        return []


def add(pages, agent, n, entry):
    """Append one entry under a lock, so run.py and the server can both write."""
    path = path_of(pages, agent, n)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        data = load(pages, agent, n) + [entry]
        with open(path + ".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(path + ".tmp", path)


def entry(t, step, status, usage):
    u = usage or {}
    return dict({"t": t, "step": step, "model": status.get("model"), "effort": status.get("effort"),
                 "state": status.get("state")}, **{k: round(u.get(k) or 0, 6) if k == "cost" else u.get(k) or 0 for k in KEYS})


def total(entries):
    """{cost, runs, by step {step: cost}}."""
    by = {}
    for e in entries:
        by[e["step"]] = round(by.get(e["step"], 0) + (e.get("cost") or 0), 6)
    return {"cost": round(sum(by.values()), 6), "runs": len(entries), "steps": by}


def backfill(pages):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from run import usage_of
    root = os.path.join(pages, "agents")
    for agent in sorted(os.listdir(root)):
        base = paths.agent(pages, agent)
        for step in ("analysis", "strategy", "context", "resolve"):
            for n in paths.numbers(base, step):
                st = json.load(open(paths.status(base, n, step), encoding="utf-8"))
                if st.get("state") == "working":
                    continue
                seen = {(e["step"], e["t"]) for e in load(pages, agent, n)}
                if step == "resolve":  # earlier sessions' logs are the server's own, recorded when they ended
                    lf = os.path.join(paths.runs(base, n, step), "out.jsonl")
                    u = usage_of(lf)
                    t = st.get("ended") or st.get("started")
                    if u.get("cost") and not any(x[:2] == (step, t) for x in seen):
                        add(pages, agent, n, dict(entry(t, step, st, u), backfill=True))
                        print(agent, n, step, u["cost"])
                elif (st.get("usage") or {}).get("cost") and not any(s[0] == step and s[1] == st.get("ended") for s in seen):
                    add(pages, agent, n, dict(entry(st.get("ended") or st.get("started"), step, st, st["usage"]), backfill=True))
                    print(agent, n, step, st["usage"]["cost"])


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    pages = os.path.abspath(opts.get("--pages") or os.path.expanduser("~/.claude/bbva-issues"))
    if args == ["backfill"]:
        backfill(pages); return
    if len(args) != 2:
        sys.exit(__doc__)
    entries = load(pages, *args)
    for e in entries:
        print(f'{e["t"]}  {e["step"]:<9} {e.get("model") or "":<14} {e.get("state") or "":<8} ${e.get("cost") or 0:.4f}')
    print(json.dumps(total(entries)))


if __name__ == "__main__":
    main(sys.argv[1:])
