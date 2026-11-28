#!/usr/bin/env bash
# Description: Check short-link source metadata using the same verifier as CI

echo "Checking short-link front matter..."
if bundle exec ruby utils/bin/backfill_short_url_front_matter.rb --check; then
    exit 0
fi

echo "If metadata is missing or stale, backfill the reported file, review the diff, and stage it again:" >&2
echo "  bundle exec ruby utils/bin/backfill_short_url_front_matter.rb html/path/to/post.md" >&2
exit 1

