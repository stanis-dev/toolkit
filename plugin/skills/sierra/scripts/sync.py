"""Refresh the pages-dir cache of one agent's issues from the tracker, and the calls they link.

Usage:
  sync.py <agent> [--pages <dir>] [--repo <dir>]

Lists every issue through the Sierra MCP server named in the repo's .mcp.json (cobranzas = sierra-base, openpay =
sierra, hipotecarios = sierra-hipotecarios), then, for issues that are not closed (FIXED, DUPLICATE, WONT_FIX) or whose status changed, saves
`get_issue_details` verbatim to `agents/<agent>/issues/<n>.json` when the file is missing or older than the issue's
last activity. For each linked call of those issues it saves `get_conversation_details` to
`conversations/<id>/details.json` and downloads the runtime record (debug.log, summary.json, traces/) with
`sierra ghostwriter --download-conversations`, copied from the agent's `.composer/conversations/`.
Progress is `agents/<agent>/sync.status.json`, which the issues page polls.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

AGENT_DIR = {"cobranzas": "agents/base", "openpay": "agents/openpay", "hipotecarios": "agents/hipotecarios"}
MCP_SERVER = {"cobranzas": "sierra-base", "openpay": "sierra", "hipotecarios": "sierra-hipotecarios"}
CLOSED = {"FIXED", "DUPLICATE", "WONT_FIX"}
TARGET = "bbva.sierra.ai/default"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pages_dir(override=None):
    return override or os.environ.get("BBVA_ISSUES_DIR") or os.path.expanduser("~/.claude/bbva-issues")


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(path + ".tmp", path)


class Mcp:
    """The Sierra MCP server over plain HTTP. It shows the issue tools only to a client that presents itself as
    claude-code, so the User-Agent says so."""

    def __init__(self, cfg):
        self.url = cfg["url"]
        self.headers = dict(cfg.get("headers") or {})
        self.headers.update({"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                             "User-Agent": "claude-code/2.0.0"})
        self.sid = None
        self.n = 0
        r = self.post({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "bbva-issues-sync", "version": "1"}}})
        self.post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def post(self, body):
        h = dict(self.headers)
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=h)
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode()
            self.sid = r.headers.get("Mcp-Session-Id") or self.sid
        if not raw.strip():
            return None
        m = re.search(r"^data: (.*)$", raw, re.M)
        return json.loads(m.group(1) if m else raw)

    def call(self, name, args):
        self.n += 1
        d = self.post({"jsonrpc": "2.0", "id": self.n, "method": "tools/call", "params": {"name": name, "arguments": args}})
        if "error" in d:
            raise RuntimeError(f"{name}: {d['error']}")
        res = d["result"]
        text = "".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise RuntimeError(f"{name}: {text[:300]}")
        return text


def list_issues(mcp):
    out, after = [], None
    while True:
        args = {"limit": 100}
        if after:
            args["after"] = after
        d = json.loads(mcp.call("get_issues", args))
        out.extend(d.get("issues", []))
        pi = d.get("pageInfo") or {}
        if not pi.get("hasNextPage") or not pi.get("endCursor"):
            return out
        after = pi["endCursor"]


def ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0


def main(argv):
    if not argv:
        sys.exit(__doc__)
    agent = argv[0]
    opts = dict(zip(argv[1::2], argv[2::2]))
    pages = pages_dir(opts.get("--pages"))
    repo = os.path.abspath(opts.get("--repo") or os.getcwd())
    base = os.path.join(pages, "agents", agent)
    status_path = os.path.join(base, "sync.status.json")
    t0 = time.time()
    status = {"state": "working", "phase": "listing issues", "started": now(), "ended": None, "seconds": None,
              "pid": os.getpid(), "issues": 0, "fetched": [], "calls": 0, "downloaded": 0, "error": None}

    def save(**kw):
        status.update(kw)
        write_json(status_path, status)

    def fail(msg):
        save(state="failed", ended=now(), seconds=round(time.time() - t0), error=msg)
        sys.exit(1)

    save()
    try:
        cfg = json.load(open(os.path.join(repo, ".mcp.json")))["mcpServers"][MCP_SERVER[agent]]
        mcp = Mcp(cfg)
        issues = list_issues(mcp)
        save(issues=len(issues), phase="issue details")
        # which issues to (re)fetch
        todo = []
        for it in issues:
            n = it["number"]
            p = os.path.join(base, "issues", f"{n}.json")
            cached = None
            if os.path.exists(p):
                try:
                    cached = json.load(open(p, encoding="utf-8"))
                    if isinstance(cached, str):
                        cached = json.loads(cached)
                except Exception:
                    cached = None
            if cached is None:
                if it["status"] not in CLOSED:
                    todo.append(it)
            elif cached["issue"].get("status") != it["status"] or ts(it.get("lastActivityAt") or "") > os.path.getmtime(p) + 1:
                todo.append(it)
        fetched = []
        for k, it in enumerate(todo, 1):
            n = it["number"]
            save(phase=f"issue details {k}/{len(todo)}")
            text = mcp.call("get_issue_details", {"issueNumber": n})
            json.loads(text)  # must parse; saved verbatim
            write_text(os.path.join(base, "issues", f"{n}.json"), text)
            fetched.append(n)
            save(fetched=fetched)
        # linked calls of every open issue in the cache
        wanted = []
        for p in glob.glob(os.path.join(base, "issues", "*.json")):
            try:
                d = json.load(open(p, encoding="utf-8"))
                if isinstance(d, str):
                    d = json.loads(d)
            except Exception:
                continue
            if d["issue"].get("status") in CLOSED:
                continue
            for l in d.get("linkedLogs") or []:
                if l.get("id") and l["id"] not in wanted:
                    wanted.append(l["id"])
        need_details = [c for c in wanted if not os.path.exists(os.path.join(base, "conversations", c, "details.json"))]
        calls = 0
        for k, c in enumerate(need_details, 1):
            save(phase=f"calls {k}/{len(need_details)}")
            text = mcp.call("get_conversation_details", {"conversationId": c})
            json.loads(text)
            write_text(os.path.join(base, "conversations", c, "details.json"), text)
            calls += 1
            save(calls=calls)
        # the runtime record, downloaded into the agent's .composer/conversations and copied over
        agent_dir = os.path.join(repo, AGENT_DIR[agent])
        src_root = os.path.join(agent_dir, ".composer", "conversations")
        need_dl = [c for c in wanted if not os.path.exists(os.path.join(base, "conversations", c, "debug.log"))]
        downloaded = 0
        for k in range(0, len(need_dl), 20):
            batch = need_dl[k:k + 20]
            save(phase=f"downloading calls {k + 1}-{k + len(batch)}/{len(need_dl)}")
            missing = [c for c in batch if not os.path.exists(os.path.join(src_root, c, "debug.log"))]
            if missing:
                r = subprocess.run(["pnpm", "--dir=" + agent_dir, "exec", "sierra", "ghostwriter", TARGET,
                                    "--download-conversations", "--ids", ",".join(missing)],
                                   capture_output=True, text=True, cwd=agent_dir, stdin=subprocess.DEVNULL)
                if r.returncode != 0:
                    fail("ghostwriter: " + (r.stderr or r.stdout).strip()[-600:])
            for c in batch:
                src = os.path.join(src_root, c)
                if os.path.exists(os.path.join(src, "debug.log")):
                    shutil.copytree(src, os.path.join(base, "conversations", c), dirs_exist_ok=True)
                    downloaded += 1
            save(downloaded=downloaded)
        save(state="done", phase=None, ended=now(), seconds=round(time.time() - t0))
    except SystemExit:
        raise
    except Exception as ex:
        fail(f"{type(ex).__name__}: {ex}")


if __name__ == "__main__":
    main(sys.argv[1:])
