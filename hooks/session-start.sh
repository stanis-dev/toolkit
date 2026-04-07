#!/usr/bin/env bash
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GLOBAL_CONTEXT_FILE="${PLUGIN_ROOT}/context/global.md"

GLOBAL_CONTEXT=""
if [[ -f "$GLOBAL_CONTEXT_FILE" ]]; then
  GLOBAL_CONTEXT=$(cat "$GLOBAL_CONTEXT_FILE")
fi

SKILLS="Stan's personal toolkit plugin is active. Available skills:

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

SKILL & PROMPT ENGINEERING:
- skill-engineer: Create, review, analyze, improve and challenge AI agent skills and prompts
- wiki-editorial: Gated knowledge-wiki workflow for proposing, publishing, and linting canonical knowledge

PLUGIN DEVELOPMENT:
- plugin-dev: How to modify, extend, and propagate changes to this plugin

PERSONAL:
- communication-copilot: Tighten pasted drafts for authority, clarity, and low-friction communication
- codex-proxy: Direct ChatGPT API proxy (~24 token overhead vs ~31K through Codex CLI)
- deep-research-prompt: Generate context-enriched research prompts
- question-crystallization: Move from vague intuitions to clear questions
- music-discovery: Music recommendations, Plex history, SoulSync downloads
- homelab-ssh: Homelab server reference (SSH, Docker, storage)
- mini-ssh: Mac Mini / Plex server reference (SSH, Plex API)
- cursor-chat-history: Find and reconstruct Cursor agent chat histories"

if [[ -n "$GLOBAL_CONTEXT" ]]; then
  CONTEXT="${GLOBAL_CONTEXT}

---

${SKILLS}"
else
  CONTEXT="$SKILLS"
fi

CONTEXT_ESCAPED=$(printf '%s' "$CONTEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": ${CONTEXT_ESCAPED}
  }
}
EOF
