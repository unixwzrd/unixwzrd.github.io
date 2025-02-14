#!/usr/bin/env bash

# Description: Checks for proper front matter in markdown files

echo "📄 Checking front matter..."
find html -name "*.md" | while read -r file; do
    if [[ ! "$file" =~ README.md$ ]] && [[ ! "$file" =~ CHANGELOG.md$ ]]; then
        if ! grep -A1 "^---$" "$file" | grep -q "^title:\|^layout:"; then
            echo "⚠️ Warning: Missing title or layout in front matter of $file"
        fi
    fi
done

exit 0 