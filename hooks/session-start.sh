#!/usr/bin/env bash
set -euo pipefail

CONTEXT="Stan's personal toolkit plugin is active. Available skills:

SIERRA WORKFLOWS:
- sierra-powertool: Full sierras CLI reference (auto-loads when working on Sierra agents)
- sierra-best-practices: Development guidelines, workspace discipline, debug workflows
- sierra-bootstrap: Start issue work (branch, workspace, issue fetch, sim coverage, Linear ticket)
- sierra-triage: Classify Agent Studio issues into prioritized buckets
- sierra-phrasing-eval: Manual phrasing evaluation workflow (10-run minimum)
- sierra-wrap-up-issue: Generate client report, PR, and documentation for completed issues
- deep-eval: Thoroughness override protocol for deep evaluation passes

SIERRA AGENTS:
- phrasing-eval: Read-only subagent for phrasing evaluation against guardrails
- replay-analyzer: Read-only subagent for evidence-first replay analysis

PERSONAL:
- deep-research-prompt: Generate context-enriched research prompts
- question-crystallization: Move from vague intuitions to clear questions
- music-discovery: Music recommendations, Plex history, SoulSync downloads
- homelab-ssh: Homelab server reference (SSH, Docker, storage)
- mini-ssh: Mac Mini / Plex server reference (SSH, Plex API)
- cursor-chat-history: Find and reconstruct Cursor agent chat histories"

CONTEXT_ESCAPED=$(printf '%s' "$CONTEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": ${CONTEXT_ESCAPED}
  }
}
EOF
