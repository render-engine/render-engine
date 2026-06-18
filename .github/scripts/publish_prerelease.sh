#!/usr/bin/env bash
set -euo pipefail

# --- fetch latest version, PEP 440-correct, straight from the API (no checkout-depth increase) ----
# {owner}/{repo} are resolved by gh from the current repo context.
LATEST="$(gh api "repos/{owner}/{repo}/tags" --paginate --jq '.[].name' |
  grep -E '^[0-9]{4}\.[0-9]+\.[0-9]+([ab][0-9]+)?$' |
  uvx --with packaging python -c \
    'import sys; from packaging.version import Version; print(max(sys.stdin.read().split(), key=Version))')"
echo "Latest tag: $LATEST" >&2

# --- Determine whether to bump the exising or next minor
if [[ "$LATEST" =~ [ab][0-9]+$ ]]; then
  part=pre_n # continue alpha/beta serial
else
  part=minor # final -> next minor, resets to a1
fi
echo "Bumping part: $part" >&2

# --- run BMV and then gh release
NEXT="$(uvx bump-my-version bump "$part" \
  --current-version "$LATEST" \
  --dry-run --allow-dirty --no-configured-files -v 2>&1 |
  grep -oE "New version will be '[^']+'" |
  grep -oE "[0-9]{4}\.[0-9]+\.[0-9]+[ab][0-9]+")"

# expose to later workflow steps when running in Actions
if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "version=$NEXT" >>"$GITHUB_OUTPUT"
fi

# Run dry run with DRY_RUN=true bash ./.github/scripts/publish_prerelease.sh
if [[ "${DRY_RUN:-false}" == "true" ]]; then
  echo "DRY_RUN: would run gh release create $NEXT --prerelease --generate-notes" >&2
  echo "$NEXT"
  exit 0
fi

cmd='gh release create "$NEXT" --prerelease --generate-notes --title "$NEXT"'
echo "$NEXT"
