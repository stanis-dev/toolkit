#!/usr/bin/env python3
"""Extract user queries from a Cursor agent transcript JSONL file."""
import json, re, sys

if len(sys.argv) < 2:
    print("Usage: extract-queries.py <path-to-jsonl> [max-chars]", file=sys.stderr)
    sys.exit(1)

max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 0

for line in open(sys.argv[1]):
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
