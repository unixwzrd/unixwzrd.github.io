#!/bin/bash

# Periodic Site Reliability Monitor
# Runs periodically to check site health

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT"

echo "⏰ Periodic site monitoring started at $(date)"

# Run the site reliability monitor in periodic mode
python3 utils/bin/site_reliability_monitor.py \
    --mode periodic \
    --config utils/etc/site_monitor_config.json

echo "✅ Periodic monitoring completed at $(date)" 