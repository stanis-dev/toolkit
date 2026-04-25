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

# Resolve canonical source: defaults to the plugin's global.md, two dirs up
# from this script (plugin/scripts/install-symlinks.sh -> plugin/global.md).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="${1:-${SCRIPT_DIR}/../global.md}"
CANONICAL="$(cd "$(dirname "$CANONICAL")" && pwd)/$(basename "$CANONICAL")"

if [[ ! -f "$CANONICAL" ]]; then
  echo "ERROR: canonical file not found: $CANONICAL" >&2
  exit 1
fi

# target_path : human label
TARGETS=(
  "$HOME/AGENTS.md"
  "$HOME/CLAUDE.md"
  "$HOME/.codex/AGENTS.md"
)

TS="$(date +%Y%m%d-%H%M%S)"
linked=0
skipped=0
backed_up=0

echo "Canonical source: $CANONICAL"
echo

for entry in "${TARGETS[@]}"; do
  path="${entry%%|*}"
  label="${entry#*|}"
  parent="$(dirname "$path")"

  # Ensure parent dir exists.
  mkdir -p "$parent"

  if [[ -L "$path" ]]; then
    current="$(readlink "$path")"
    if [[ "$current" == "$CANONICAL" ]]; then
      echo "  ✓ $path  (already linked) — $label"
      ((skipped++))
      continue
    fi
    echo "  ↻ $path  (was symlink to $current; repointing) — $label"
    rm "$path"
  elif [[ -e "$path" ]]; then
    backup="${path}.bak.${TS}"
    mv "$path" "$backup"
    echo "  ⚠ $path  (regular file backed up to $backup) — $label"
    ((backed_up++))
  else
    echo "  + $path  (creating) — $label"
  fi

  ln -s "$CANONICAL" "$path"
  ((linked++))
done

echo
echo "Done. linked=$linked  skipped=$skipped  backed_up=$backed_up"
