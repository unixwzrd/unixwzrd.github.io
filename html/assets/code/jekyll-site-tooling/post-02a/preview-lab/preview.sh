#!/usr/bin/env bash
set -euo pipefail

lab_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mode="${1:-}"

if [[ "$#" -ne 1 || ( "$mode" != "current" && "$mode" != "review" ) ]]; then
  printf 'usage: %s current|review\n' "${0##*/}" >&2
  exit 64
fi

source_dir="$lab_dir/site"
output_dir="$lab_dir/out/$mode"
mkdir -p "$lab_dir/out"

flags=()
if [[ "$mode" == "review" ]]; then
  flags=(--future --drafts --unpublished)
fi

cd "$lab_dir"
bundle exec jekyll build \
  --source "$source_dir" \
  --destination "$output_dir" \
  --config "$source_dir/_config.yml" \
  --disable-disk-cache \
  "${flags[@]}" \
  --quiet

printf '%s view: %s\n' "$mode" "$output_dir/index.html"
