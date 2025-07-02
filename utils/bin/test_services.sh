#!/usr/bin/env bash

set -e

# Comprehensive test for jekyll-site and file_watcher services

echo "=== 1. Clean start: stop everything ==="
utils/bin/jekyll-site stop || true
utils/bin/file_watcher stop || true

echo "=== 2. Start both services (OG refresh enabled) ==="
utils/bin/jekyll-site start
utils/bin/file_watcher start

echo "=== 3. Check processes ==="
ps aux | grep -E "(jekyll|file_watcher)" | grep -v grep || echo "No processes found."

echo "=== 4. Restart both services (OG refresh enabled) ==="
utils/bin/jekyll-site restart
utils/bin/file_watcher restart

echo "=== 5. Restart both services (OG refresh disabled) ==="
utils/bin/jekyll-site restart -n
utils/bin/file_watcher restart

echo "=== 6. Stop both services ==="
utils/bin/jekyll-site stop
utils/bin/file_watcher stop

echo "=== 7. Check for orphans ==="
ps aux | grep -E "(jekyll|file_watcher)" | grep -v grep || echo "No processes found."

echo "=== 8. Try stopping again (should be idempotent) ==="
utils/bin/jekyll-site stop || true
utils/bin/file_watcher stop || true

echo "=== 9. Try invalid argument ==="
set +e
utils/bin/jekyll-site bogus || true
utils/bin/file_watcher bogus || true
set -e

echo "=== 10. Custom watcher dir test ==="
utils/bin/file_watcher start --target-dir html --watchers-dir utils/bin/watchers
utils/bin/file_watcher stop

echo "=== All tests complete! ===" 