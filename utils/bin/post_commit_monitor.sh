#!/bin/bash

# Post-Commit Site Reliability Monitor
# Runs after a commit to verify the site deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT"

# Get the commit hash
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MESSAGE=$(git log -1 --pretty=format:"%s")

echo "🚀 Post-commit monitoring triggered for commit: $COMMIT_HASH"
echo "📝 Commit message: $COMMIT_MESSAGE"

# Run the site reliability monitor in post-commit mode
# This will wait for deployment and then check the site
python3 utils/bin/site_reliability_monitor.py \
    --mode post-commit \
    --commit-hash "$COMMIT_HASH" \
    --config utils/etc/site_monitor_config.json

echo "✅ Post-commit monitoring completed" 