#!/usr/bin/env python3
"""Read downloaded simulation runs and conversations from .composer.

Usage:
  runset.py <run-id>                         one line per result
  runset.py <run-id> --failed                judge reasoning and tag misses per failed result
  runset.py <run-id> --transcript <result>   turn list; <result> is a result id, a test id or a name substring
  runset.py conv <conversation-id>           summary line plus turn list of a downloaded conversation
  runset.py names <file>                     import test names from a saved `sierra test --json` output
  runset.py summary <file>… [--vs <file>…]   what `sierra test --json` wrote: per sim passed/total, judge
                                             lines, run ids; `--vs` files are the baseline

`summary` reads only the files `sierra test <ws> --names … --num-runs 5 --json > <file>` wrote; several
files add up (two passes of five, or a batch split). Transcripts, tags and traces are not in that
file: download the run and use the views above.

Run ids accept both `01M...` and `replaytestrunset-01M...`. The .composer directory is found by
walking up from the working directory, or under agents/*/ when run from the repository root.
"""

import csv
import glob
import json
import os
import sys

csv.field_size_limit(sys.maxsize)

RUN_PREFIX = "replaytestrunset-"
RESULT_PREFIX = "replaytestresult-"
NAMES_FILE = "test-names.json"
TURN_EVENTS = {"USER_MSG": "U", "AGENT_MSG": "A"}
ASIDE_EVENTS = {"TOOL_CALL": "tool", "TAGS": "tags", "OBSERVATIONS": "obs"}


def fail(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)


def composer_candidates():
    here = os.getcwd()
    seen = []
    d = here
    while True:
        c = os.path.join(d, ".composer")
        if os.path.isdir(c):
            seen.append(c)
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    seen.extend(sorted(glob.glob(os.path.join(here, "agents", "*", ".composer"))))
    return seen


def find_composer(relative_target):
    candidates = composer_candidates()
    if not candidates:
        fail("no .composer directory found from " + os.getcwd())
    for c in candidates:
        if os.path.exists(os.path.join(c, relative_target)):
            return c
    fail(
        f"{relative_target} is not downloaded in any of:\n  "
        + "\n  ".join(candidates)
        + "\nDownload it from the agent directory; the command is in"
        " .composer/docs/agent-traces-reference.md, with the full-domain target after `ghostwriter`."
    )


def normalize_run_id(raw):
    return raw if raw.startswith(RUN_PREFIX) else RUN_PREFIX + raw


def load_names(composer):
    names = {}
    for f in glob.glob(os.path.join(composer, "simulations", "test_refs", "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        if "id" in d and "name" in d:
            names[d["id"]] = d["name"]
    cache = os.path.join(composer, "simulations", NAMES_FILE)
    if os.path.exists(cache):
        names.update(json.load(open(cache, encoding="utf-8")))
    return names


def load_results(composer, run_id):
    run_dir = os.path.join(composer, "simulations", run_id)
    results = []
    for f in sorted(glob.glob(os.path.join(run_dir, "results", "*", "result.json"))):
        d = json.load(open(f, encoding="utf-8"))
        d["_dir"] = os.path.dirname(f)
        results.append(d)
    if not results:
        fail(f"{run_dir} has no results")
    return results


def tag_misses(result):
    tags = set(result.get("tags") or [])
    expectations = result.get("tagExpectations") or {}
    missing = [t for t in expectations.get("present") or [] if t not in tags]
    unexpected = [t for t in expectations.get("absent") or [] if t in tags]
    return missing, unexpected


def unmet_outcomes(result):
    return [o for o in result.get("outcomeEvalResults") or [] if not o.get("metExpectation", False)]


def result_name(result, names):
    return names.get(result["replayTestId"], result["replayTestId"])


def sort_key(result, names):
    return (result_name(result, names), result["status"] != "FAILED", result["id"])


def print_table(results, names):
    for r in sorted(results, key=lambda r: sort_key(r, names)):
        missing, unexpected = tag_misses(r)
        unmet = len(unmet_outcomes(r))
        notes = []
        if unmet:
            notes.append(f"{unmet} unmet")
        if missing:
            notes.append("missing " + ", ".join(missing))
        if unexpected:
            notes.append("unexpected " + ", ".join(unexpected))
        print(f"{r['status']:<7} {result_name(r, names)}  {r['id']}" + (f"  [{'; '.join(notes)}]" if notes else ""))
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("\n" + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) + f", {len(results)} results")


def print_failed(results, names):
    failed = [r for r in results if r["status"] != "PASSED"]
    if not failed:
        print("no failed results")
        return
    for r in sorted(failed, key=lambda r: sort_key(r, names)):
        print(f"== {r['status']} {result_name(r, names)}  {r['id']}")
        for o in unmet_outcomes(r):
            print(f"  expected: {o.get('expectedOutcome', '')}")
            print(f"  judge:    {o.get('reasoning', '')}")
        missing, unexpected = tag_misses(r)
        if missing:
            print("  missing tags:    " + ", ".join(missing))
        if unexpected:
            print("  unexpected tags: " + ", ".join(unexpected))
        details = r.get("statusDetails")
        if details:
            print(f"  status details:  {details}")
        if not unmet_outcomes(r) and not missing and not unexpected and not details:
            print("  no unmet expectation recorded in result.json")
        print()


def print_transcript(debug_log):
    with open(debug_log, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            kind = row["event_type"]
            message = row["message"]
            if kind in TURN_EVENTS:
                print(f"{TURN_EVENTS[kind]}: {message}")
            elif kind in ASIDE_EVENTS:
                if kind == "OBSERVATIONS" and not message.startswith("Activated"):
                    continue
                print(f"   [{ASIDE_EVENTS[kind]}] {message}")


def select_results(results, names, selector):
    wanted = selector.lower()
    picked = [
        r
        for r in results
        if r["id"] in (selector, RESULT_PREFIX + selector)
        or r["replayTestId"] == selector
        or wanted in result_name(r, names).lower()
    ]
    if not picked:
        fail(f"no result matches {selector}")
    return sorted(picked, key=lambda r: sort_key(r, names))


def cmd_run(args):
    run_id = normalize_run_id(args[0])
    composer = find_composer(os.path.join("simulations", run_id))
    names = load_names(composer)
    results = load_results(composer, run_id)
    flags = args[1:]
    if not flags:
        print_table(results, names)
    elif flags == ["--failed"]:
        print_failed(results, names)
    elif len(flags) == 2 and flags[0] == "--transcript":
        for r in select_results(results, names, flags[1]):
            print(f"== {r['status']} {result_name(r, names)}  {r['id']}")
            print_transcript(os.path.join(r["_dir"], "debug.log"))
            print()
    else:
        fail(__doc__)


def cmd_conv(args):
    if len(args) != 1:
        fail(__doc__)
    conv_id = args[0]
    composer = find_composer(os.path.join("conversations", conv_id))
    conv_dir = os.path.join(composer, "conversations", conv_id)
    summary_path = os.path.join(conv_dir, "summary.json")
    if os.path.exists(summary_path):
        s = json.load(open(summary_path, encoding="utf-8"))
        print(
            f"== {s.get('id')}  messages={s.get('message_count')} ended={s.get('has_conversation_ended')}"
            f" transfer={s.get('has_agent_transfer')} handle={s.get('agent_handle_time_seconds')}s"
            f" locale={s.get('locale')}"
        )
        print("   tags: " + ", ".join(s.get("tags") or []))
    print_transcript(os.path.join(conv_dir, "debug.log"))


def cmd_names(args):
    if len(args) != 1:
        fail(__doc__)
    text = open(args[0], encoding="utf-8").read()
    start = text.find('{"')
    if start < 0:
        fail(f"{args[0]} holds no JSON object")
    payload = json.loads(text[start : text.rfind("}") + 1])
    tests = payload.get("tests") or []
    imported = {t["testId"]: t["name"] for t in tests if t.get("testId") and t.get("name")}
    if not imported:
        fail(f"{args[0]} has no tests with testId and name")
    run_id = payload.get("simulationRunId")
    candidates = composer_candidates()
    downloaded = [c for c in candidates if run_id and os.path.isdir(os.path.join(c, "simulations", run_id))]
    if downloaded:
        composer = downloaded[0]
    elif len(candidates) == 1:
        composer = candidates[0]
    else:
        fail(
            f"run {run_id} is not downloaded, so the agent these names belong to is ambiguous:\n  "
            + "\n  ".join(candidates)
            + "\nRun this from the agent directory, or download the run first."
        )
    cache = os.path.join(composer, "simulations", NAMES_FILE)
    names = json.load(open(cache, encoding="utf-8")) if os.path.exists(cache) else {}
    names.update(imported)
    json.dump(names, open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    print(f"{len(imported)} names imported, {len(names)} cached in {cache}")


def load_run_file(path):
    """A `sierra test --json` output file. Empty means the launch failed before the run started."""
    text = open(path, encoding="utf-8").read()
    start = text.find('{"')
    if start < 0:
        fail(
            f"{path} holds no run: `sierra test` failed before starting; its message went to stderr."
            " The frequent causes: the workspace positional was left out («Multiple workspaces match»),"
            " several names were passed as one quoted or comma-joined argument, --num-runs above 5."
        )
    payload = json.loads(text[start : text.rfind("}") + 1])
    if not payload.get("tests"):
        fail(
            f"{path}: the run matched no simulations. `--names` takes space-separated display names"
            " or id slugs, as `sierra test <ws> --list --json` prints them."
        )
    payload["_file"] = path
    return payload


def add_up(payloads):
    """Per test id across files: name, passed, total, and each judge line with how often it appeared."""
    sims = {}
    for p in payloads:
        for t in p["tests"]:
            s = sims.setdefault(t["testId"], {"name": t["name"], "passed": 0, "total": 0, "judge": {}})
            s["passed"] += t.get("passed", 0)
            s["total"] += t.get("total", 0)
            for line in t.get("statusDetails") or []:
                s["judge"][line] = s["judge"].get(line, 0) + 1
    return sims


def cmd_summary(args):
    if "--vs" in args:
        cut = args.index("--vs")
        now_files, base_files = args[:cut], args[cut + 1 :]
    else:
        now_files, base_files = args, []
    if not now_files or ("--vs" in args and not base_files):
        fail(__doc__)
    now = add_up([load_run_file(f) for f in now_files])
    base = add_up([load_run_file(f) for f in base_files]) if base_files else None
    ids = sorted(set(now) | set(base or {}), key=lambda i: ((now.get(i) or base.get(i))["name"]))
    ids.sort(key=lambda i: now[i]["passed"] == now[i]["total"] if i in now else True)
    width = max(len((now.get(i) or base.get(i))["name"]) for i in ids)
    for i in ids:
        score = f"{now[i]['passed']}/{now[i]['total']}" if i in now else "—"
        if base is not None:
            before = f"{base[i]['passed']}/{base[i]['total']}" if i in base else "—"
            score = f"{before} → {score}"
        print(f"{score:>13}  {(now.get(i) or base.get(i))['name']}")
        for line, n in sorted((now.get(i) or {}).get("judge", {}).items(), key=lambda kv: -kv[1]):
            print(f"{'':>13}  ✗ {'×' + str(n) + ' ' if n > 1 else ''}{line}")
    print()
    for label, files in (("now", now_files), ("baseline", base_files)):
        for f in files:
            p = load_run_file(f)
            sm = p.get("summary") or {}
            print(
                f"{label:<8} {p.get('simulationRunId')}  {sm.get('expectedResultCount', '?')} results"
                f"  {p.get('durationSeconds', '?')}s  {p.get('simulationRunUrl', '')}"
            )


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return
    if argv[0] == "conv":
        cmd_conv(argv[1:])
    elif argv[0] == "names":
        cmd_names(argv[1:])
    elif argv[0] == "summary":
        cmd_summary(argv[1:])
    else:
        cmd_run(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
