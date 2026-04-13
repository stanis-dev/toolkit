#!/usr/bin/env bash
set -euo pipefail

PLATFORM="all"
PEEK=false
SEARCH_TERM=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) PLATFORM="$2"; shift 2 ;;
    --peek) PEEK=true; shift ;;
    *) SEARCH_TERM="$1"; shift ;;
  esac
done

CURSOR_ROOT="$HOME/.cursor/projects"
CLAUDE_ROOT="$HOME/.claude/projects"
CODEX_SESSIONS="$HOME/.codex/sessions"
CODEX_ARCHIVED="$HOME/.codex/archived_sessions"
OPENCODE_DB="$HOME/.local/share/opencode/opencode.db"

peek_cursor() {
  local f="$1"
  python3 -c "
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
" 2>/dev/null || echo "(no query found)"
}

peek_claude() {
  local f="$1"
  python3 -c "
import json, sys
for line in open(sys.argv[1]):
    line = line.strip()
    if not line: continue
    d = json.loads(line)
    if d.get('type') != 'user': continue
    content = d.get('message', {}).get('content', '')
    if isinstance(content, str):
        print(content[:120])
    elif isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'text':
                print(c['text'][:120]); break
            elif isinstance(c, str):
                print(c[:120]); break
    raise SystemExit
" "$f" 2>/dev/null || echo "(no query found)"
}

peek_codex() {
  local f="$1"
  python3 -c "
import json
for line in open('$f'):
    line = line.strip()
    if not line: continue
    d = json.loads(line)
    if d.get('type') != 'event_msg': continue
    p = d.get('payload', {})
    if p.get('type') == 'user_message':
        print(p.get('message', '')[:120])
        raise SystemExit
" 2>/dev/null || echo "(no query found)"
}

peek_opencode() {
  local sid="$1"
  local safe_sid="${sid//\'/\'\'}"
  sqlite3 "$OPENCODE_DB" "
    SELECT json_extract(p.data, '$.text')
    FROM part p
    JOIN message m ON p.message_id = m.id
    WHERE p.session_id = '${safe_sid}'
      AND json_extract(p.data, '$.type') = 'text'
      AND json_extract(m.data, '$.role') = 'user'
    ORDER BY p.time_created
    LIMIT 1;
  " 2>/dev/null | head -c 120 || echo "(no query found)"
}

list_cursor() {
  for d in "$CURSOR_ROOT"/*/agent-transcripts; do
    [ -d "$d" ] || continue
    project="$(basename "$(dirname "$d")")"
    count="$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
    echo "[cursor] $project: $count conversations"
  done
}

list_claude() {
  for d in "$CLAUDE_ROOT"/*/; do
    [ -d "$d" ] || continue
    project="$(basename "$d")"
    count="$(find "$d" -maxdepth 1 -name '*.jsonl' 2>/dev/null | wc -l | tr -d ' ')"
    [ "$count" -gt 0 ] && echo "[claude] $project: $count sessions"
  done
}

list_codex() {
  local active archived
  active="$(find "$CODEX_SESSIONS" -name '*.jsonl' 2>/dev/null | wc -l | tr -d ' ')"
  archived="$(find "$CODEX_ARCHIVED" -name '*.jsonl' 2>/dev/null | wc -l | tr -d ' ')"
  echo "[codex] $active active sessions, $archived archived"
}

list_opencode() {
  if [ -f "$OPENCODE_DB" ]; then
    local count
    count="$(sqlite3 "$OPENCODE_DB" "SELECT COUNT(*) FROM session;" 2>/dev/null)"
    echo "[opencode] $count sessions"
  fi
}

search_cursor() {
  local matches
  matches=$(rg --no-heading -l "$SEARCH_TERM" "$CURSOR_ROOT"/*/agent-transcripts/*/*.jsonl 2>/dev/null || true)
  [ -z "$matches" ] && return
  echo "$matches" | while IFS= read -r f; do
    slug=$(echo "$f" | sed -E 's|.*/projects/([^/]+)/agent-transcripts/([^/]+)/.*|\1/\2|')
    if [ "$PEEK" = true ]; then
      echo "[cursor] $slug: $(peek_cursor "$f")"
    else
      echo "[cursor] $f"
    fi
  done
}

search_claude() {
  local matches
  matches=$(rg --no-heading -l "$SEARCH_TERM" "$CLAUDE_ROOT"/*/*.jsonl 2>/dev/null || true)
  [ -z "$matches" ] && return
  echo "$matches" | while IFS= read -r f; do
    slug=$(echo "$f" | sed -E 's|.*/projects/([^/]+)/([^/]+)\.jsonl|\1/\2|')
    if [ "$PEEK" = true ]; then
      echo "[claude] $slug: $(peek_claude "$f")"
    else
      echo "[claude] $f"
    fi
  done
}

search_codex() {
  local matches
  matches=$(rg --no-heading -l "$SEARCH_TERM" -g '*.jsonl' "$CODEX_SESSIONS" "$CODEX_ARCHIVED" 2>/dev/null || true)
  [ -z "$matches" ] && return
  echo "$matches" | while IFS= read -r f; do
    name=$(basename "$f" .jsonl)
    if [ "$PEEK" = true ]; then
      echo "[codex] $name: $(peek_codex "$f")"
    else
      echo "[codex] $f"
    fi
  done
}

search_opencode() {
  if [ ! -f "$OPENCODE_DB" ]; then return; fi
  local results safe_term
  safe_term="${SEARCH_TERM//\'/\'\'}"
  results=$(sqlite3 "$OPENCODE_DB" "
    SELECT DISTINCT s.id, s.title
    FROM session s
    JOIN part p ON p.session_id = s.id
    WHERE p.data LIKE '%${safe_term}%'
    ORDER BY s.time_created DESC;
  " 2>/dev/null || true)
  [ -z "$results" ] && return
  echo "$results" | while IFS='|' read -r sid title; do
    if [ "$PEEK" = true ]; then
      echo "[opencode] $sid ($title): $(peek_opencode "$sid")"
    else
      echo "[opencode] $sid ($title)"
    fi
  done
}

if [ -z "$SEARCH_TERM" ]; then
  case "$PLATFORM" in
    cursor)   list_cursor ;;
    claude)   list_claude ;;
    codex)    list_codex ;;
    opencode) list_opencode ;;
    all)      list_cursor; list_claude; list_codex; list_opencode ;;
    *) echo "Unknown platform: $PLATFORM" >&2; exit 1 ;;
  esac
else
  case "$PLATFORM" in
    cursor)   search_cursor ;;
    claude)   search_claude ;;
    codex)    search_codex ;;
    opencode) search_opencode ;;
    all)      search_cursor; search_claude; search_codex; search_opencode ;;
    *) echo "Unknown platform: $PLATFORM" >&2; exit 1 ;;
  esac
fi
