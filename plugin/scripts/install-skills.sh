#!/usr/bin/env bash
# Install directory symlinks so every supported agent tool reads skills from
# this plugin's skills/ directory.
#
# Idempotent: re-running is safe.
# Existing real directories at the target paths are backed up to
# <path>.bak.<timestamp> before being replaced by the symlink.
#
# Verified in April 2026 against:
#   - ~/.agents/skills/   read by Codex, OpenCode, Pi, Cursor
#   - ~/.claude/skills/   read by Claude Code (and OpenCode/Cursor as fallback)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="$(cd "$SCRIPT_DIR/.." && pwd)/skills"

# Ensure canonical exists (skills can be added later).
mkdir -p "$CANONICAL"

TARGETS=(
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
)

TS="$(date +%Y%m%d-%H%M%S)"
linked=0
skipped=0
backed_up=0

echo "Canonical source: $CANONICAL"
echo

for path in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$path")"

  if [[ -L "$path" ]]; then
    current="$(readlink "$path")"
    if [[ "$current" == "$CANONICAL" ]]; then
      echo "  ✓ $path  (already linked)"
      ((skipped++))
      continue
    fi
    echo "  ↻ $path  (was symlink to $current; repointing)"
    rm "$path"
  elif [[ -e "$path" ]]; then
    backup="${path}.bak.${TS}"
    mv "$path" "$backup"
    echo "  ⚠ $path  (existing dir backed up to $backup)"
    ((backed_up++))
  else
    echo "  + $path  (creating)"
  fi

  ln -s "$CANONICAL" "$path"
  ((linked++))
done

echo
echo "Done. linked=$linked  skipped=$skipped  backed_up=$backed_up"
