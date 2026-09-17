#!/bin/sh
# Run the full Brain test suite. Any failure exits non-zero so build.sh can gate on it.
set -e
SCRIPT_DIR="$(dirname "$0")"
BRAIN_DIR="$SCRIPT_DIR/.."

VENV_PY="$BRAIN_DIR/.venv/bin/python3"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

echo "== Swift: meeting detection heuristics =="
swiftc -swift-version 5 "$BRAIN_DIR/src/MeetingDetectionHeuristics.swift" "$SCRIPT_DIR/test_meeting_detection.swift" -o "$SCRATCH/meet_tests"
"$SCRATCH/meet_tests"

echo "== Swift: Slack log parser =="
swiftc -swift-version 5 "$BRAIN_DIR/src/SlackLogParser.swift" "$SCRIPT_DIR/test_slack_log_parser.swift" -o "$SCRATCH/slack_tests"
"$SCRATCH/slack_tests"

if [ ! -x "$VENV_PY" ]; then
  echo "ERROR: $VENV_PY missing. Build the venv: python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

echo "== Python: export helpers (Teams timestamps, Slack host) =="
"$VENV_PY" "$SCRIPT_DIR/test_export_helpers.py"

echo "== Python: chat export storage + rendering =="
"$VENV_PY" "$SCRIPT_DIR/test_chat_exports.py"

echo "== Google Chat: browser parsing, reply coverage, safe export replacement =="
node --test "$SCRIPT_DIR/test_google_chat_browser.mjs"
"$VENV_PY" "$SCRIPT_DIR/test_google_chat_export.py"

echo "== Brain control: local socket and command client =="
swiftc -swift-version 5 "$BRAIN_DIR/src/ControlServer.swift" "$SCRIPT_DIR/test_control_server.swift" -o "$SCRATCH/control_tests"
BRAIN_CONTROL_TEST_HOST="$SCRATCH/control_tests" "$VENV_PY" "$SCRIPT_DIR/test_brainctl.py"

echo "All tests passed."
