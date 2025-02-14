#!/usr/bin/env bash

# Description: Verifies that all required files exist in the repository

echo "📁 Checking required files..."
required_files=(
    "html/_data/repos.yml"
    "html/_data/github_projects.yml"
    "_config.yml"
    "html/_includes/join_us.html"
    "html/_includes/getintouch.html"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

exit 0 