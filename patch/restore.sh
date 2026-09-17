#!/usr/bin/env bash
# Undo the media-use patch using the most recent backup made by install.sh.
#   bash ~/Documents/Projects-AI/HomeNetwork/inventory/skills/remediation-2026-09-16/media-use-patch/restore.sh
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LATEST="$(ls -1d "$HERE"/backups/*/ 2>/dev/null | tail -1)"
[[ -n "$LATEST" ]] || { echo "No backups found in $HERE/backups"; exit 1; }
echo "Restoring from $LATEST"
cd "$LATEST"
find . -type f | while read -r f; do
  target="/${f#./}"
  cp -p "$f" "$target"
  echo "  restored $target"
done
echo "Done."
