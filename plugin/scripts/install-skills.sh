#!/usr/bin/env bash
# Install per-skill symlinks so agent tools read each authored skill live
# from this plugin's skills/ directory.
#
# ~/.agents/skills stays a REAL directory and only the individual skill
# dirs inside it are symlinks. Tools that sync their own skills into it
# (e.g. Sierra Agent Studio) then write machine-local copies instead of
# writing through a directory symlink into this repo.
#
# Claude Code is deliberately not linked at all: it gets these skills via
# the toolkit plugin (stan-marketplace), and ~/.claude/skills must stay a
# real directory for machine-local skills.
#
# Idempotent: re-running is safe.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="$(cd "$SCRIPT_DIR/.." && pwd)/skills"

TARGET="$HOME/.agents/skills"

# A leftover whole-directory symlink would route tool writes into the repo.
if [[ -L "$TARGET" ]]; then
  echo "  ↻ $TARGET  (was a directory symlink; replacing with real dir)"
  rm "$TARGET"
fi
mkdir -p "$TARGET"

linked=0
skipped=0

for skill in "$CANONICAL"/*/; do
  name="$(basename "$skill")"
  path="$TARGET/$name"
  if [[ -L "$path" && "$(readlink "$path")" == "${skill%/}" ]]; then
    echo "  ✓ $path  (already linked)"
    ((skipped++))
    continue
  fi
  ln -sfn "${skill%/}" "$path"
  echo "  + $path"
  ((linked++))
done

echo
echo "Done. linked=$linked  skipped=$skipped"
