#!/usr/bin/env bash

# Description: Checks for files larger than 5MB that might cause issues with Git

echo "📦 Checking for large files..."
find . -type f -size +5M ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./_site/*" ! -path "./.project-planning/*" -exec ls -lh {} \; | while read -r large_file; do
    echo "⚠️ Warning: Large file detected: $large_file"
done

exit 0 