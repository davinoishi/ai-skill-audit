#!/usr/bin/env bash
# Apply the media-use SSRF + .env patch to every installed copy of the skill.
#
#   bash install.sh
#
# Safe by design: a file is only touched when it still matches the exact version
# this patch was built against (sha256 checked), every replaced file is backed up,
# and the result is verified and tested afterwards. Re-running it is a no-op.
#
# Requires: bash, patch, node (for the tests), shasum.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCHFILE="$HERE/media-use.patch"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$HERE/backups/$STAMP"

# Add or remove copies here if your install differs.
COPIES=(
  "$HOME/.claude/skills/media-use"
  "$HOME/.agents/skills/media-use"
  "$HOME/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/media-use"
)
# relative path | sha256 before | sha256 after
FILES=(
  "scripts/lib/freeze.mjs|77e664bb548cdcaba779f602754a0430df28a613fd940e093e383428a7bc620c|c89209df5a2ddb37746beed016cbda7011bc0370bab7b48a76d4ce043e8f2627"
  "audio/scripts/lib/heygen.mjs|ab6d3f3bceaec3aebc4196c1a356afcfe1931027fad4bdc183c7efcac9e0cc62|7be4ad29e9b15fa51e2a4e1124f99afd850f2aa6b88c318ee244527c904a48cf"
)

sha() { shasum -a 256 "$1" | awk '{print $1}'; }
[[ -f "$PATCHFILE" ]] || { echo "ABORT: media-use.patch not found next to this script"; exit 1; }

installed=0; skipped=0; warned=0; patched_copies=()
for copy in "${COPIES[@]}"; do
  [[ -d "$copy" ]] || { echo "-- not installed: $copy"; continue; }
  real="$(cd "$copy" && pwd -P)"
  echo "== $copy"

  ready=1
  for f in "${FILES[@]}"; do
    IFS="|" read -r rel before after <<<"$f"
    target="$real/$rel"
    if [[ ! -f "$target" ]]; then echo "   MISSING $rel"; ready=0; warned=$((warned+1)); continue; fi
    cur="$(sha "$target")"
    if [[ "$cur" == "$after" ]]; then echo "   already patched: $rel"; skipped=$((skipped+1)); ready=0; continue; fi
    if [[ "$cur" != "$before" ]]; then
      echo "   WARNING $rel does not match the reviewed version (sha $cur) — probably updated upstream. NOT changed."
      ready=0; warned=$((warned+1))
    fi
  done
  [[ $ready -eq 1 ]] || continue

  ( cd "$real" && patch -p1 --dry-run --silent < "$PATCHFILE" ) || { echo "   ABORT: patch would not apply cleanly"; exit 1; }
  for f in "${FILES[@]}"; do
    IFS="|" read -r rel before after <<<"$f"
    mkdir -p "$BACKUP$real/$(dirname "$rel")"
    cp -p "$real/$rel" "$BACKUP$real/$rel"
  done
  ( cd "$real" && patch -p1 --silent < "$PATCHFILE" )
  for f in "${FILES[@]}"; do
    IFS="|" read -r rel before after <<<"$f"
    [[ "$(sha "$real/$rel")" == "$after" ]] || { echo "   ERROR: $rel did not verify after patching"; exit 1; }
    echo "   patched: $rel"
    installed=$((installed+1))
  done
  patched_copies+=("$real")
done

if [[ ${#patched_copies[@]} -gt 0 ]] && command -v node >/dev/null; then
  echo "== Testing the patched files"
  t="$(mktemp -d "${TMPDIR:-/tmp}/media-use-patch-XXXXXX")" || t=""
  [[ -n "$t" ]] && cp "${patched_copies[0]}/scripts/lib/freeze.mjs" "${patched_copies[0]}/audio/scripts/lib/heygen.mjs" "$t/"
  [[ -n "$t" ]] && PATCH_DIR="$t" node --test "$HERE/patch.test.mjs" 2>&1 | grep -E "^# (pass|fail)" || true
  [[ -n "$t" ]] && rm -rf "$t"
fi

echo
echo "Done: $installed file(s) patched, $skipped already patched, $warned warning(s)."
[[ $installed -gt 0 ]] && echo "Backups: $BACKUP"
[[ $warned -gt 0 ]] && echo "Review the warnings above before relying on the patch."
exit 0
