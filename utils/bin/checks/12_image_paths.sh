#!/bin/bash

# Image Path Checker
# Automatically fixes image paths for local development or production

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
cd "$PROJECT_ROOT"

# Detect environment
if [[ "$JEKYLL_ENV" == "production" ]] || [[ "$1" == "--production" ]]; then
    BASE_URL="https://unixwzrd.ai"
    ENV_NAME="production"
elif [[ "$1" == "--local" ]]; then
    BASE_URL="http://localhost:4000"
    ENV_NAME="local"
else
    # Auto-detect: if we're in a git hook or CI, use production
    if [[ -n "$GIT_HOOK" ]] || [[ -n "$CI" ]] || [[ "$1" == "--pre-commit" ]]; then
        BASE_URL="https://unixwzrd.ai"
        ENV_NAME="production (auto-detected)"
    else
        BASE_URL="http://localhost:4000"
        ENV_NAME="local (auto-detected)"
    fi
fi

echo "🔍 Checking image paths for $ENV_NAME environment (base URL: $BASE_URL)"

# Run the image path fixer
python3 utils/bin/fix_image_paths.py --base-url "$BASE_URL" --target-dir html

echo "✅ Image path check completed for $ENV_NAME environment" 