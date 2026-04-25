#!/usr/bin/env bash
# Install symlinks from each agent tool's expected global instruction path
# to the toolkit's canonical file (plugin/global.md by default).
#
# Idempotent: re-running is safe.
# Existing regular files are backed up to <path>.bak.<timestamp> before replacement.
# Existing symlinks pointing elsewhere are repointed.
#
# Verified in April 2026 against:
#   - Claude Code  (~/CLAUDE.md, walks up from cwd)
#   - Cursor       (~/CLAUDE.md, imports from Claud)
#   - OpenCode     (~/AGENTS.md, walks up from cwd)
#   - Pi           (~/AGENTS.md, walks up from cwd)
#   - Cursor agent (~/AGENTS.md, walks up from cwd)
#   - Codex        (~/.codex/AGENTS.md, global slot — does NOT walk up)

set -euo pipefail

# Canonical source is always ../global.md
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="$(cd "$SCRIPT_DIR/.." && pwd)/global.md"

if [[ ! -f "$CANONICAL" ]]; then
  echo "ERROR: canonical file not found: $CANONICAL" >&2
  exit 1
fi

TARGETS=(
  "$HOME/AGENTS.md"
  "$HOME/CLAUDE.md"
  "$HOME/.codex/AGENTS.md"
)

TS="$(date +%Y%m%d-%H%M%S)"
linked=0
skipped=0
backed_up=0

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

echo
echo "Done. linked=$linked  skipped=$skipped  backed_up=$backed_up"
