#!/usr/bin/env python3
"""Extract user queries from an agent session transcript. Auto-detects platform from path."""
import json, re, sys, os, subprocess

def detect_platform(path):
    if "/.cursor/" in path:
        return "cursor"
    if "/.claude/" in path:
        return "claude"
    if "/.codex/" in path:
        return "codex"
    return None

def extract_cursor(path, max_chars):
    for line in open(path):
        d = json.loads(line)
        if d.get("role") != "user":
            continue
        for c in d["message"]["content"]:
            if c.get("type") != "text":
                continue
            m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", c["text"], re.DOTALL)
            if m:
                text = m.group(1)
                print(text if max_chars == 0 else text[:max_chars])

def extract_claude(path, max_chars):
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("type") != "user":
            continue
        content = d.get("message", {}).get("content", "")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = next(
                (c["text"] for c in content if isinstance(c, dict) and c.get("type") == "text"),
                next((c for c in content if isinstance(c, str)), ""),
            )
        else:
            continue
        if text:
            print(text if max_chars == 0 else text[:max_chars])

def extract_codex(path, max_chars):
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("type") != "event_msg":
            continue
        p = d.get("payload", {})
        if p.get("type") == "user_message":
            text = p.get("message", "")
            print(text if max_chars == 0 else text[:max_chars])

def extract_opencode(session_id, max_chars):
    db = os.path.expanduser("~/.local/share/opencode/opencode.db")
    if not os.path.exists(db):
        print("OpenCode DB not found", file=sys.stderr)
        sys.exit(1)
    import sqlite3 as sql
    conn = sql.connect(db)
    rows = conn.execute("""
        SELECT json_extract(p.data, '$.text')
        FROM part p
        JOIN message m ON p.message_id = m.id
        WHERE p.session_id = ?
          AND json_extract(p.data, '$.type') = 'text'
          AND json_extract(m.data, '$.role') = 'user'
        ORDER BY p.time_created;
    """, (session_id,)).fetchall()
    conn.close()
    for (text,) in rows:
        if text:
            print(text if max_chars == 0 else text[:max_chars])

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: extract-queries.py <path> [max-chars]", file=sys.stderr)
        print("       extract-queries.py --session-id <id> --platform opencode [max-chars]", file=sys.stderr)
        sys.exit(1)

    session_id = None
    platform = None
    path = None
    max_chars = 0

    i = 0
    while i < len(args):
        if args[i] == "--session-id":
            session_id = args[i + 1]; i += 2
        elif args[i] == "--platform":
            platform = args[i + 1]; i += 2
        elif args[i].isdigit():
            max_chars = int(args[i]); i += 1
        else:
            path = args[i]; i += 1

    if session_id and platform == "opencode":
        extract_opencode(session_id, max_chars)
    elif path:
        detected = platform or detect_platform(path)
        if detected == "cursor":
            extract_cursor(path, max_chars)
        elif detected == "claude":
            extract_claude(path, max_chars)
        elif detected == "codex":
            extract_codex(path, max_chars)
        else:
            print(f"Cannot detect platform from path: {path}", file=sys.stderr)
            print("Use --platform cursor|claude|codex", file=sys.stderr)
            sys.exit(1)
    else:
        print("Provide a file path or --session-id with --platform opencode", file=sys.stderr)
        sys.exit(1)
