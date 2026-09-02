#!/bin/sh
# Run the full Brain test suite. Any failure exits non-zero so build.sh can gate on it.
set -e
cd "$(dirname "$0")/.."

VENV_PY=".venv/bin/python3"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

echo "== Swift: meeting detection heuristics =="
swiftc -swift-version 5 src/MeetingDetectionHeuristics.swift scripts/test_meeting_detection.swift -o "$SCRATCH/meet_tests"
"$SCRATCH/meet_tests"

echo "== Swift: Slack log parser =="
swiftc -swift-version 5 src/SlackLogParser.swift scripts/test_slack_log_parser.swift -o "$SCRATCH/slack_tests"
"$SCRATCH/slack_tests"

if [ ! -x "$VENV_PY" ]; then
  echo "ERROR: $VENV_PY missing. Build the venv: python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

echo "== Python: export helpers (Teams timestamps, Slack host) =="
"$VENV_PY" scripts/test_export_helpers.py

echo "== Python: chat export storage + rendering =="
"$VENV_PY" scripts/test_chat_exports.py

echo "All tests passed."
