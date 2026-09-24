"""Where the pages dir keeps each file: an agent's issues and calls, a card's folder, a batch's files. Every script and
the dashboard build their paths here, so the layout lives in one place. `base` is an agent's folder, agent(pages, a);
the dashboard, which runs in the pages dir, passes agent('', a). `n` is a card's number, `step` one of setup, analysis,
strategy, context, resolve; `driver` keys its files by batch the same way.

    issues/<n>.json               the tracker's issue, sync.py's
    conversations/<call>/         a call's files, sync.py's; one call can belong to several issues
    cards/<n>/
      card.html  log.jsonl  cost.json  chain.json  chain.stop  chain.log
      source.json (source.py's), conversations/<id>: a link to a call in conversations/, or a replay's own copy
      <step>/  status.json  answer.json  report.md  stage.json  runs.json  reopen.json  runs/  history/
    batches.json  batches/<batch>.status.json  batches/<batch>/  driver/<batch>.<ext>  driver/runs/<batch>/
"""
import glob
import json
import os
import re


STEPS = ("setup", "analysis", "strategy", "context", "resolve")
NAME = {"json": "answer.json", "md": "report.md"}  # a step file's name in the step's folder, by its old extension


def pages_dir(override=None):
    return override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues")


def agent(pages, a):
    return os.path.join(pages, "agents", a)


# ---------- the agent's own ----------

def issue(base, n):
    """The tracker's issue as sync.py wrote it."""
    return os.path.join(base, "issues", f"{n}.json")


def issues(base):
    """The numbers of the issues sync.py has written, sorted."""
    d = os.path.join(base, "issues")
    return sorted((f[:-5] for f in os.listdir(d) if re.fullmatch(r"\d+\.json", f)), key=int) if os.path.isdir(d) else []


def conversation(base, cid):
    return os.path.join(base, "conversations", cid)


def sop(base):
    return os.path.join(base, "sop", "sop.md")


# ---------- a card ----------

def card_dir(base, n):
    return os.path.join(base, "cards", str(n))


def card(base, n):
    return os.path.join(card_dir(base, n), "card.html")


def cards(base):
    """The numbers of the agent's cards, sorted."""
    d = os.path.join(base, "cards")
    return sorted((f for f in os.listdir(d) if f.isdigit() and os.path.isfile(card(base, f))), key=int) if os.path.isdir(d) else []


def status(base, n, step):
    return step_file(base, n, step, "status.json")


def answer(base, n, step):
    return step_file(base, n, step, "json")


def step_file(base, n, step, ext):
    """One of the step's files of the card, by its kind: `status.json`, `json` (the answer), and for resolve
    `stage.json`, `runs.json`, `reopen.json`, `md` (the report). The driver's are per batch, in driver/."""
    if step == "driver":
        return os.path.join(base, "driver", f"{n}.{ext}")
    return os.path.join(card_dir(base, n), step, NAME.get(ext, ext))


def numbers(base, kind, ext="status.json"):
    """The card numbers (batches for driver and batches) that have that file: a step's (`status.json`, `json`,
    `stage.json`, …), `cost`'s or `chain`'s `json`, `log`'s `jsonl`. Sorted as strings."""
    if kind in ("driver", "batches"):
        d = os.path.join(base, kind)
        suffix = "." + ext
        return sorted(f[:-len(suffix)] for f in os.listdir(d)
                      if f.endswith(suffix) and re.fullmatch(r"\d+(?:-\d)?", f[:-len(suffix)])) if os.path.isdir(d) else []
    d = os.path.join(base, "cards")
    at = {"cost": lambda n: cost(base, n), "log": lambda n: log(base, n), "chain": lambda n: chain(base, n, ext)}.get(
        kind, lambda n: step_file(base, n, kind, ext))
    return sorted(f for f in os.listdir(d) if f.isdigit() and os.path.exists(at(f))) if os.path.isdir(d) else []


def runs(base, n, step):
    """The step's working folder for the card: the current run's files, and one folder per ended run."""
    if step == "driver":
        return os.path.join(base, "driver", "runs", str(n))
    return os.path.join(card_dir(base, n), step, "runs")


def guard_red(base, n, name="guard-red"):
    """The Sim Strategy's 5× run of the guard before the fix (name guard-now: the latest 5× run on the card's tree),
    {run, passed, total}, or None before it ran."""
    f = os.path.join(runs(base, n, "strategy"), name + ".json")
    try:
        j = json.load(open(f, encoding="utf-8"))
    except (OSError, ValueError):
        return None
    tests = j.get("tests") or []
    return {"run": j.get("simulationRunId"), "passed": sum(t.get("passed") or 0 for t in tests),
            "total": sum(t.get("total") or 0 for t in tests)} if tests else None


def history(base, n, step, stamp, ext):
    """An earlier version of the step's answer (`json`) or of the card (`card.html`), kept when a run replaced it."""
    return os.path.join(card_dir(base, n), step, "history", f"{stamp}.{ext}")


def histories(base, n, step):
    """The card's history files of the step, oldest first."""
    return sorted(glob.glob(os.path.join(card_dir(base, n), step, "history", "*")))


def log(base, n):
    """The card's history, one event per line."""
    return os.path.join(card_dir(base, n), "log.jsonl")


def cost(base, n):
    return os.path.join(card_dir(base, n), "cost.json")


def chain(base, n, ext="json"):
    """The step sequence's state (`json`) and stop request (`stop`)."""
    return os.path.join(card_dir(base, n), f"chain.{ext}")


def chain_log(base, n):
    return os.path.join(card_dir(base, n), "chain.log")


def card_files(base, n):
    """Every file of the card as (group, path), in reading order: where it came from (source.json, the tracker's issue
    when there is one, the conversations), the card itself, then each step's own files, its runs and its history."""
    out = []

    def add(group, p):
        if os.path.isfile(p):
            out.append((group, p))
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs.sort()
                out.extend((group, os.path.join(root, f)) for f in sorted(files))
    d = card_dir(base, n)
    add("source", os.path.join(d, "source.json"))
    add("source", issue(base, n))
    cd = os.path.join(d, "conversations")
    for c in sorted(os.listdir(cd)) if os.path.isdir(cd) else []:
        add("source", os.path.join(cd, c))
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if f not in STEPS and f not in ("source.json", "conversations"):
            add("card", os.path.join(d, f))
    for step in STEPS:
        sd = os.path.join(d, step)
        for f in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
            if f not in ("runs", "history"):
                add(step, os.path.join(sd, f))
        add(step, runs(base, n, step))
        add(step, os.path.join(sd, "history"))
    return out


def rel(base, path):
    """path relative to the agent's folder, as the card's history keeps it."""
    return os.path.relpath(path, base)


# ---------- a batch ----------

def batches(base):
    return os.path.join(base, "batches.json")


def batch_file(base, batch, ext):
    """batches/<batch>.<ext>: `status.json`, `merge.lock`."""
    return os.path.join(base, "batches", f"{batch}.{ext}")


def batch_dir(base, batch):
    """batches/<batch>/: the check runs and the batch's other files."""
    return os.path.join(base, "batches", batch)


def batch_ids(base):
    """The batches with a batch.py status file, sorted."""
    return numbers(base, "batches")


def batch_runs(base, batch):
    return os.path.join(base, "batches", "runs", batch)
