"""Where the pages dir keeps each file: an agent's issues and calls, a card's step files, a batch's. Every script and the
dashboard build their paths here, so the layout lives in one place. `base` is an agent's folder, agent(pages, a); the
dashboard, which runs in the pages dir, passes agent('', a). `n` is a card's number, `step` one of setup, analysis,
strategy, context, resolve; `driver` keys its files by batch the same way."""
import glob
import json
import os
import re


def pages_dir(override=None):
    return override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues")


def agent(pages, a):
    return os.path.join(pages, "agents", a)


# ---------- the agent's own ----------

def issue(base, n):
    """The tracker's issue as sync.py wrote it."""
    return os.path.join(base, "issues", f"{n}.json")


def conversation(base, cid):
    return os.path.join(base, "conversations", cid)


def sop(base):
    return os.path.join(base, "sop", "sop.md")


# ---------- a card ----------

def card(base, n):
    return os.path.join(base, "cards", f"{n}.html")


def issues(base):
    """The numbers of the issues sync.py has written, sorted."""
    d = os.path.join(base, "issues")
    return sorted((f[:-5] for f in os.listdir(d) if re.fullmatch(r"\d+\.json", f)), key=int) if os.path.isdir(d) else []


def cards(base):
    """The numbers of the agent's cards, sorted."""
    d = os.path.join(base, "cards")
    return sorted((f[:-5] for f in os.listdir(d) if re.fullmatch(r"\d+\.html", f)), key=int) if os.path.isdir(d) else []


def status(base, n, step):
    return step_file(base, n, step, "status.json")


def answer(base, n, step):
    return step_file(base, n, step, "json")


def step_file(base, n, step, ext):
    """One of the step's files of the card: `status.json`, `json` (the answer), and for resolve `stage.json`,
    `runs.json`, `reopen.json`, `md` (the report)."""
    return os.path.join(base, step, f"{n}.{ext}")


def numbers(base, kind, ext="status.json"):
    """The card numbers (batches for driver) that have that file: a step's (`status.json`, `json`, `stage.json`, …),
    `cost`'s or `chain`'s `json`, `log`'s `jsonl`. Sorted as strings."""
    d = os.path.join(base, kind)
    suffix = "." + ext
    return sorted(f[:-len(suffix)] for f in os.listdir(d)
                  if f.endswith(suffix) and re.fullmatch(r"\d+(?:-\d)?", f[:-len(suffix)])) if os.path.isdir(d) else []


def runs(base, n, step):
    """The step's working folder for the card: the current run's files, and one folder per ended run."""
    return os.path.join(base, step, "runs", str(n))


def history(base, n, step, stamp, ext):
    """An earlier version of the step's answer (`json`) or of the card (`card.html`), kept when a run replaced it."""
    return os.path.join(base, step, "history", f"{n}.{stamp}.{ext}")


def histories(base, n, step):
    """The card's history files of the step, oldest first."""
    return sorted(glob.glob(os.path.join(base, step, "history", f"{n}.*")))


def log(base, n):
    """The card's history, one event per line."""
    return os.path.join(base, "log", f"{n}.jsonl")


def cost(base, n):
    return os.path.join(base, "cost", f"{n}.json")


def chain(base, n, ext="json"):
    """The step sequence's state (`json`) and stop request (`stop`)."""
    return os.path.join(base, "chain", f"{n}.{ext}")


def chain_log(base, n):
    return os.path.join(base, "chain", "runs", f"{n}.log")


STEPS = ("setup", "analysis", "strategy", "context", "resolve")


def card_files(base, n):
    """Every file of the card as (group, path), in reading order: where it came from (the issue and its linked calls),
    the card itself, then each step's own files, its runs and its history."""
    out = []

    def add(group, p):
        if os.path.isfile(p):
            out.append((group, p))
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs.sort()
                out.extend((group, os.path.join(root, f)) for f in sorted(files))
    add("source", issue(base, n))
    try:
        iss = json.load(open(issue(base, n), encoding="utf-8"))
        iss = json.loads(iss) if isinstance(iss, str) else iss
    except (OSError, ValueError):
        iss = {}
    for link in iss.get("linkedLogs") or []:
        add("source", conversation(base, link["id"]))
    for p in (card(base, n), log(base, n), cost(base, n), chain(base, n), chain(base, n, "stop"), chain_log(base, n)):
        add("card", p)
    for step in STEPS:
        for p in sorted(glob.glob(os.path.join(base, step, f"{n}.*"))):
            add(step, p)
        add(step, runs(base, n, step))
        for p in histories(base, n, step):
            add(step, p)
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
