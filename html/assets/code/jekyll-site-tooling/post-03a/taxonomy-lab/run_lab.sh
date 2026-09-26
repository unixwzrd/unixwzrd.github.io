#!/usr/bin/env bash
set -euo pipefail

lab_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$lab_dir/out"
cd "$lab_dir"

run_case() {
  local name="$1" expected="$2" message="${3:-}"
  local root="$lab_dir/out/$name"
  rm -rf "$root"
  mkdir -p "$root/site/_posts" "$root/site/_drafts"
  cp -R "$lab_dir/site/." "$root/site/"

  local flags=()
  if [[ "$name" == "draft-with-old-tag" ]]; then
    cp "$lab_dir/cases/$name.md" "$root/site/_drafts/$name.md"
    flags=(--drafts)
  else
    cp "$lab_dir/cases/$name.md" "$root/site/_posts/2020-01-01-$name.md"
  fi

  local status=0
  bundle exec jekyll build \
    --source "$root/site" \
    --destination "$root/rendered" \
    --config "$root/site/_config.yml" \
    --disable-disk-cache \
    "${flags[@]}" \
    --quiet >"$root/build.log" 2>&1 || status=$?

  if [[ "$expected" == "accepted" ]]; then
    if [[ "$status" -ne 0 ]]; then
      cat "$root/build.log" >&2
      printf 'FAIL %s: expected acceptance\n' "$name" >&2
      exit 1
    fi
  else
    if [[ "$status" -eq 0 ]] || ! grep -Fq "$message" "$root/build.log"; then
      cat "$root/build.log" >&2
      printf 'FAIL %s: expected rejection containing %s\n' "$name" "$message" >&2
      exit 1
    fi
  fi
  printf 'PASS %s: %s\n' "$name" "$expected"
}

run_case valid accepted
run_case unknown-tag rejected 'unknown tag'
run_case alias-tag rejected 'is an alias'
run_case duplicate-tag rejected 'duplicate tags'
run_case unknown-content-type rejected 'unknown content_type'
run_case missing-series-order accepted
run_case draft-with-old-tag accepted
