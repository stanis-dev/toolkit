#!/usr/bin/env bash
# Point every agent tool's global instruction slot at this plugin's global.md.
# AGENTS.md is the one name; the only CLAUDE.md written is a one-line pointer.
#
# Idempotent: re-running is safe.
# Existing regular files are backed up to <path>.bak.<timestamp> before replacement.
# Existing symlinks pointing elsewhere are repointed.
#
# Who reads what (verified September 2026, Claude Code 2.1.278):
#   - Claude Code   ~/.claude/CLAUDE.md is the only user-scope slot and it is
#                   written here as "@$HOME/AGENTS.md". That import loads in every
#                   cwd, including outside $HOME, and Claude dedupes the
#                   ~/AGENTS.md it also finds by walking up, so the rules load once.
#                   The default "claude-md-or-agents-md" mode is fine with this.
#   - OpenCode / Pi / Cursor  ~/AGENTS.md, walks up from cwd
#   - Codex 0.153.4           ~/.codex/AGENTS.md, global slot. Project docs are read from
#                             the git root down to cwd only, so ~/AGENTS.md is never seen.
#
# Legacy symlinks into this repo (~/CLAUDE.md, the old ~/.agents hub, Gemini)
# are removed so nothing loads twice and nothing unused lingers.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="$(cd "$SCRIPT_DIR/.." && pwd)/global.md"

if [[ ! -f "$CANONICAL" ]]; then
  echo "ERROR: canonical file not found: $CANONICAL" >&2
  exit 1
fi

TARGETS=(
  "$HOME/AGENTS.md"
  "$HOME/.codex/AGENTS.md"
)

POINTER="$HOME/.claude/CLAUDE.md"
POINTER_CONTENT="@$HOME/AGENTS.md"

LEGACY=(
  "$HOME/CLAUDE.md"
  "$HOME/.gemini/GEMINI.md"
  "$HOME/.agents/AGENTS.md"
)

TS="$(date +%Y%m%d-%H%M%S)"
linked=0
skipped=0
backed_up=0
removed=0

realpath_py() {
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"
}

for path in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$path")"

  if [[ -L "$path" ]]; then
    current="$(readlink "$path")"
    if [[ "$current" == "$CANONICAL" ]]; then
      echo "  ✓ $path  (skipped)"
      ((skipped++))
      continue
    fi
    echo "  ↻ $path  (was symlink to $current; repointing)"
    rm "$path"
  elif [[ -e "$path" ]]; then
    backup="${path}.bak.${TS}"
    mv "$path" "$backup"
    echo "  ⚠ $path  (regular file backed up to $backup)"
    ((backed_up++))
  else
    echo "  + $path  (creating)"
  fi

  ln -s "$CANONICAL" "$path"
  ((linked++))
done

# Claude Code user-scope pointer
mkdir -p "$(dirname "$POINTER")"
if [[ -L "$POINTER" ]]; then
  echo "  ↻ $POINTER  (was symlink to $(readlink "$POINTER"); replacing with import pointer)"
  rm "$POINTER"
elif [[ -f "$POINTER" ]] && [[ "$(cat "$POINTER")" == "$POINTER_CONTENT" ]]; then
  echo "  ✓ $POINTER  (skipped)"
  ((skipped++))
elif [[ -e "$POINTER" ]]; then
  backup="${POINTER}.bak.${TS}"
  mv "$POINTER" "$backup"
  echo "  ⚠ $POINTER  (regular file backed up to $backup)"
  ((backed_up++))
fi
if [[ ! -e "$POINTER" ]]; then
  printf '%s\n' "$POINTER_CONTENT" > "$POINTER"
  echo "  + $POINTER  (import pointer written)"
  ((linked++))
fi

for path in "${LEGACY[@]}"; do
  [[ -L "$path" ]] || continue
  if [[ "$(realpath_py "$path")" == "$CANONICAL" ]]; then
    rm "$path"
    echo "  − $path  (legacy symlink removed)"
    ((removed++))
  else
    echo "  ! $path  (symlink to $(readlink "$path"); not ours, left alone)"
  fi
done

echo
echo "Done. linked=$linked  skipped=$skipped  backed_up=$backed_up  removed=$removed"
