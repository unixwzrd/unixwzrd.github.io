#!/usr/bin/env bash
#
# Runs HTMLProofer against the generated Jekyll site (_site) to catch
# broken internal links, including fragment (anchor) references.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(realpath "${SCRIPT_DIR}/../../..")"

cd "${BASE_DIR}"

echo "🏗️ Building production site for HTMLProofer..."
"${BASE_DIR}/utils/bin/jekyll-site" build -n

if [ ! -d "_site" ]; then
    echo "❌ _site directory not found after build. Please investigate." >&2
    exit 1
fi

echo "🔎 Running HTMLProofer against _site..."

bundle exec htmlproofer ./_site \
    --disable-external \
    --allow-hash-href \
    --check-internal-hash \
    --allow-missing-href

echo "🔎 Checking for nested internal links missing trailing slashes..."
python3 "${BASE_DIR}/utils/bin/check_nested_slashless_links.py"

echo "✅ HTMLProofer finished with no internal link errors."
