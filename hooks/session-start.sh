#!/usr/bin/env bash
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GLOBAL_CONTEXT_FILE="${PLUGIN_ROOT}/context/global.md"
START_DIR="${PWD:-$(pwd)}"

GLOBAL_CONTEXT=""
if [[ -f "$GLOBAL_CONTEXT_FILE" ]]; then
  GLOBAL_CONTEXT=$(cat "$GLOBAL_CONTEXT_FILE")
fi

PROJECT_DOCS=()
find_project_docs() {
  local dir="$1"
  while [[ -n "$dir" && "$dir" != "/" ]]; do
    for name in "CLAUDE.md" "CLAUDE.local.md"; do
      local candidate="${dir}/${name}"
      if [[ -f "$candidate" ]]; then
        PROJECT_DOCS+=("$candidate")
      fi
    done
    dir="$(dirname "$dir")"
  done
}

find_project_docs "$START_DIR"

PROJECT_CONTEXT=""
if [[ "${#PROJECT_DOCS[@]}" -gt 0 ]]; then
  for (( idx=${#PROJECT_DOCS[@]}-1; idx>=0; idx-- )); do
    doc_path="${PROJECT_DOCS[$idx]}"
    if [[ -n "$PROJECT_CONTEXT" ]]; then
      PROJECT_CONTEXT="${PROJECT_CONTEXT}

---"
    fi
    PROJECT_CONTEXT="${PROJECT_CONTEXT}

[Project Doc: ${doc_path}]
$(cat "$doc_path")"
  done
fi

SKILLS="Stan's personal toolkit plugin is active. Available skills:

SIERRA WORKFLOWS:
- sierra-powertool: Full sierras CLI reference (auto-loads when working on Sierra agents)
- sierra-best-practices: Development guidelines, workspace discipline, debug workflows
- deep-eval: Thoroughness override protocol for deep evaluation passes

SKILL & PROMPT ENGINEERING:
- skill-engineer: Create, review, analyze, improve and challenge AI agent skills and prompts
- wiki-editorial: Gated knowledge-wiki workflow for proposing, publishing, and linting canonical knowledge

PLUGIN DEVELOPMENT:
- plugin-dev: How to modify, extend, and propagate changes to this plugin

AGENTS:
- personal-assistant: Dedicated session agent for operational awareness, reply drafting, and communication coaching

PERSONAL:
- codex-proxy: Direct ChatGPT API proxy (~24 token overhead vs ~31K through Codex CLI)
- deep-research-prompt: Generate context-enriched research prompts
- question-crystallization: Move from vague intuitions to clear questions
- music-discovery: Music recommendations, Plex history, SoulSync downloads
- homelab-ssh: Homelab server reference (SSH, Docker, storage)
- mini-ssh: Mac Mini / Plex server reference (SSH, Plex API)
- cursor-chat-history: Find and reconstruct Cursor agent chat histories"

if [[ -n "$GLOBAL_CONTEXT" ]]; then
  CONTEXT="$GLOBAL_CONTEXT"
else
  CONTEXT=""
fi

if [[ -n "$PROJECT_CONTEXT" ]]; then
  if [[ -n "$CONTEXT" ]]; then
    CONTEXT="${CONTEXT}

---"
  fi
  CONTEXT="${CONTEXT}${PROJECT_CONTEXT}"
fi

if [[ -n "$SKILLS" ]]; then
  if [[ -n "$CONTEXT" ]]; then
    CONTEXT="${CONTEXT}

---"
  fi
  CONTEXT="${CONTEXT}

${SKILLS}"
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
