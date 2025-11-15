#!/usr/bin/env bash
#
# Runs HTMLProofer against the generated Jekyll site (_site) to check
# external links for broken URLs, timeouts, and HTTPS compliance.
#
# Note: This script is opt-in (skipped by default) due to:
#   - Network dependency (can fail due to temporary outages)
#   - Slower execution time (requires HTTP requests)
#   - Rate limiting from external sites
#
# To enable external link checking:
#   - Set CHECK_EXTERNAL_LINKS=1 environment variable, OR
#   - Run manually: ./utils/bin/checks/06_external_link_checker.sh

set -euo pipefail

# Skip by default unless explicitly enabled
if [ "${CHECK_EXTERNAL_LINKS:-0}" != "1" ]; then
    echo "⏭️  Skipping external link check (set CHECK_EXTERNAL_LINKS=1 to enable)"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(realpath "${SCRIPT_DIR}/../../..")"

cd "${BASE_DIR}"

echo "🏗️ Building production site for HTMLProofer..."
"${BASE_DIR}/utils/bin/jekyll-site" build -n

if [ ! -d "_site" ]; then
    echo "❌ _site directory not found after build. Please investigate." >&2
    exit 1
fi

echo "🔎 Running HTMLProofer external link check against _site..."
echo "   (This may take a while as it checks each external URL)"

# Check external links with:
#   - HTTPS enforcement (fail on HTTP links)
#   - Only report 4xx errors (client errors like 404, not server errors like 500)
#   - Allow hash hrefs (for anchor links)
#   - Check internal hashes (for completeness)
#   - Allow missing href (for anchor tags used as IDs)
#   - Cache results (speeds up repeated runs)
bundle exec htmlproofer ./_site \
    --enforce-https \
    --only-4xx \
    --allow-hash-href \
    --check-internal-hash \
    --allow-missing-href \
    --cache '{ "timeframe": { "external": "30d" } }' \
    --log-level warn

echo "✅ HTMLProofer external link check finished."

