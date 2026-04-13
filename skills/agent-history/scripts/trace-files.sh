#!/usr/bin/env bash
set -euo pipefail

DB="$HOME/.cursor/ai-tracking/ai-code-tracking.db"
CONV_ID="${1:-}"

if [ -z "$CONV_ID" ]; then
  echo "Usage: trace-files.sh <conversation-uuid>" >&2
  exit 1
fi

if [ ! -f "$DB" ]; then
  echo "Database not found: $DB" >&2
  exit 1
fi

result=$(sqlite3 "$DB" "
  SELECT fileName, source,
    datetime(min(timestamp)/1000,'unixepoch','localtime') as first_modified,
    datetime(max(timestamp)/1000,'unixepoch','localtime') as last_modified,
    count(*) as changes
  FROM ai_code_hashes
  WHERE conversationId = '$CONV_ID'
  GROUP BY fileName
  ORDER BY min(timestamp);
")

if [ -z "$result" ]; then
  echo "No file modifications found for this conversation." >&2
else
  echo "$result"
fi
