#!/usr/bin/env bash
# Sync ~/.codex/skills/ to mirror skills/ in this repo.
#
# For every dir in skills/<name>, ensure ~/.codex/skills/<name> is a symlink
# to it. Purge dangling symlinks that point anywhere under this repo's
# skills/ tree. Leave unrelated entries alone (other skill sources, .system).
#
# Idempotent: safe to run any time. Output lists adds, repoints, removes.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="${REPO_ROOT}/skills"
DEST_DIR="${HOME}/.codex/skills"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "error: source skills dir missing: $SRC_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

added=() repointed=() removed=() kept=0

# Add/repoint: every skill in source should have a matching symlink.
for src in "$SRC_DIR"/*/; do
  [[ -d "$src" ]] || continue
  name="$(basename "$src")"
  target="${src%/}"
  link="${DEST_DIR}/${name}"

  if [[ -L "$link" ]]; then
    current="$(readlink "$link")"
    if [[ "$current" == "$target" ]]; then
      kept=$((kept + 1))
      continue
    fi
    rm "$link"
    ln -s "$target" "$link"
    repointed+=("$name ($current -> $target)")
  elif [[ -e "$link" ]]; then
    echo "warn: $link exists and is not a symlink; leaving alone" >&2
    continue
  else
    ln -s "$target" "$link"
    added+=("$name")
  fi
done

# Remove: any symlink in dest that points into our skills/ tree but whose
# source no longer exists, or whose source name is no longer in skills/.
# Unrelated symlinks (pointing elsewhere) and real directories are untouched.
for link in "$DEST_DIR"/*; do
  [[ -L "$link" ]] || continue
  target="$(readlink "$link")"
  case "$target" in
    "$SRC_DIR"/*)
      name="$(basename "$link")"
      if [[ ! -d "${SRC_DIR}/${name}" ]]; then
        rm "$link"
        removed+=("$name -> $target")
      fi
      ;;
  esac
done

echo "codex skills sync: ${kept} kept, ${#added[@]} added, ${#repointed[@]} repointed, ${#removed[@]} removed"
for n in ${added[@]+"${added[@]}"};         do echo "  + $n"; done
for n in ${repointed[@]+"${repointed[@]}"}; do echo "  ~ $n"; done
for n in ${removed[@]+"${removed[@]}"};     do echo "  - $n"; done
