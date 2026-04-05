#!/usr/bin/env bash
set -euo pipefail

TRANSCRIPTS_ROOT="$HOME/.cursor/projects"
PEEK=false

if [ "${1:-}" = "--peek" ]; then
  PEEK=true
  shift
fi

SEARCH_TERM="${1:-}"

if [ -z "$SEARCH_TERM" ]; then
  for d in "$TRANSCRIPTS_ROOT"/*/agent-transcripts; do
    [ -d "$d" ] || continue
    project="$(basename "$(dirname "$d")")"
    count="$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
    echo "$project: $count conversations"
  done
else
  matches=$(rg --no-heading -l "$SEARCH_TERM" "$TRANSCRIPTS_ROOT"/*/agent-transcripts/*/*.jsonl 2>/dev/null || true)
  [ -z "$matches" ] && exit 0

  if [ "$PEEK" = false ]; then
    echo "$matches"
  else
    echo "$matches" | while IFS= read -r f; do
      slug=$(echo "$f" | sed -E 's|.*/projects/([^/]+)/agent-transcripts/([^/]+)/.*|\1/\2|')
      query=$(python3 -c "
import json, re
for line in open('$f'):
    d = json.loads(line)
    if d.get('role') != 'user': continue
    for c in d['message']['content']:
        if c.get('type') != 'text': continue
        m = re.search(r'<user_query>\s*(.*?)\s*</user_query>', c['text'], re.DOTALL)
        if m:
            print(m.group(1)[:120])
            raise SystemExit
" 2>/dev/null || echo "(no user query found)")
      echo "$slug: $query"
    done
  fi
fi
