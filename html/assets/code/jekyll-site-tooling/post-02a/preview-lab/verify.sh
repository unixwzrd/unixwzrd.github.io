#!/usr/bin/env bash
set -euo pipefail

lab_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"$lab_dir/preview.sh" current
"$lab_dir/preview.sh" review

current="$lab_dir/out/current/index.html"
review="$lab_dir/out/review/index.html"
markers=(CURRENT-POST-MARKER FUTURE-POST-MARKER DRAFT-POST-MARKER UNPUBLISHED-POST-MARKER)

for marker in "${markers[@]}"; do
  if ! grep -Fq "$marker" "$review"; then
    printf 'review view is missing %s\n' "$marker" >&2
    exit 1
  fi
done

if ! grep -Fq CURRENT-POST-MARKER "$current"; then
  printf 'current view is missing its ordinary post\n' >&2
  exit 1
fi

for marker in "${markers[@]:1}"; do
  if grep -Fq "$marker" "$current"; then
    printf 'current view unexpectedly contains %s\n' "$marker" >&2
    exit 1
  fi
done

printf 'PASS: current has one post; review has all four\n'
