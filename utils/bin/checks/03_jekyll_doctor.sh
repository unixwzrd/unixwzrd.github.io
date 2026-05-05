#!/usr/bin/env bash
# Description: Runs Jekyll doctor (deprecations and URL sanity). Non-zero is treated
# as a warning unless STRICT_JEKYLL_DOCTOR=1, because doctor can fail on macOS
# "URLs only differ by case" while jekyll build still succeeds and production
# (Linux Pages) is case-sensitive.

echo "🔍 Running Jekyll doctor..."
set +e
out=$(bundle exec jekyll doctor 2>&1)
code=$?
printf '%s\n' "$out"
set -e

if [[ "$code" -eq 0 ]]; then
  exit 0
fi

echo ""
echo "⚠️  jekyll doctor exited with status $code."
echo "   This often happens on case-insensitive disks when Jekyll reports URL pairs that differ only by case."
echo "   Your site may still build and deploy normally. To treat doctor as fatal, run:"
echo "   STRICT_JEKYLL_DOCTOR=1 ./utils/bin/check_site.sh --run 03_jekyll_doctor"
echo ""

if [[ "${STRICT_JEKYLL_DOCTOR:-}" == "1" ]]; then
  exit "$code"
fi

exit 0


