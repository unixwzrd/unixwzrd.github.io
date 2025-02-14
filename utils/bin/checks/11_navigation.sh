#!/usr/bin/env bash

# Description: Checks navigation consistency by verifying menu items exist

echo "🧭 Checking navigation consistency..."
# Extract menu items from _config.yml
menu_items=$(grep "^  -" "_config.yml" | sed -n '/header_pages:/,/^[^ ]/p' | grep "^  -" | sed 's/^  - //')

# Check each menu item exists
for item in $menu_items; do
    if [ ! -f "html/$item" ]; then
        echo "⚠️ Warning: Navigation menu item '$item' does not exist"
    fi
done

exit 0 