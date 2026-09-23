#!/usr/bin/env python3
"""Send a card back for a second pass with what the batch's check found.

  reopen.py <agent> <n> --batch <batch> --evidence <file> [--pages <dir>] [--server <url>]

Appends {"t", "batch", "evidence"} (the file's text) to <pages>/agents/<agent>/resolve/<n>.reopen.json, records
`review reopened` with a one-line note in the card's stage log, then hands the evidence to the card's resolution session
through the issues page's server (default http://127.0.0.1:8489): the session is resumed on its last file when it is not
running, and the evidence goes in as the next prompt, after the current turn when one is running. Exit 1 when the server is down or refuses; the card's files are
written either way, so the page shows it reopened."""
import json, os, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS = ("cobranzas", "openpay", "hipotecarios")


def call(server, path, body=None):
    req = urllib.request.Request(server + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="GET" if body is None else "POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as ex:
        return {"error": f"{ex.code} {ex.read().decode(errors='replace')[:300]}"}
    except (urllib.error.URLError, OSError) as ex:
        return {"error": str(ex)}


def message(batch, evidence):
    return (f"# Reopened by batch {batch}'s check\n\nThe combined check of the batch found a failure this card owns. "
            "Take the card through a second pass: repro on your workspace, fix, regressions, merge, recording each "
            "stage as issue-resolution says. Weigh the evidence as feedback.md says: when it does not hold, say why "
            "with `stage.py … review contested --step context --note`.\n\n" + evidence)


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith("--")}
    args = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1].startswith("--"))]
    if len(args) != 2 or args[0] not in AGENTS or not args[1].isdigit() or not opts.get("--batch") or not opts.get("--evidence"):
        sys.exit(__doc__)
    agent, n, batch = args[0], args[1], opts["--batch"]
    evidence = open(opts["--evidence"], encoding="utf-8").read().strip()
    if not evidence:
        sys.exit("the evidence file is empty")
    pages = os.path.abspath(opts.get("--pages") or os.path.expanduser("~/.claude/bbva-issues"))
    server = (opts.get("--server") or "http://127.0.0.1:8489").rstrip("/")
    path = os.path.join(pages, "agents", agent, "resolve", f"{n}.reopen.json")
    try:
        log = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        log = []
    log.append({"t": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "batch": batch, "evidence": evidence})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)
    first = next((l.strip("# ").strip() for l in evidence.splitlines() if l.strip()), "")[:160]
    subprocess.run([sys.executable, os.path.join(HERE, "stage.py"), agent, n, "review", "reopened",
                    "--note", f"batch {batch}: {first}", "--pages", pages], check=True)
    state = call(server, f"/chat/{agent}/{n}/state")
    if "error" in state:
        print("the issues page's server did not answer: " + state["error"]); return 1
    if not state.get("running"):
        out = call(server, f"/chat/{agent}/{n}/start", {"resume": bool(state.get("resumable"))})
        if "error" in out:
            print("starting the card's session failed: " + out["error"]); return 1
        for _ in range(60):
            if call(server, f"/chat/{agent}/{n}/state").get("running"):
                break
            time.sleep(1)
        else:
            print("the card's session did not come up within a minute"); return 1
    busy = call(server, f"/chat/{agent}/{n}/state").get("streaming")
    out = call(server, f"/chat/{agent}/{n}/send", {"message": message(batch, evidence), "mode": "follow_up" if busy else "prompt"})
    if "error" in out:
        print("sending the evidence failed: " + out["error"]); return 1
    print(f"{agent} {n}: reopened by batch {batch}; the evidence went to its resolution session")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
