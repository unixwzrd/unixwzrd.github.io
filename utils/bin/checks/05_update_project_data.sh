#!/usr/bin/env bash

# Description: Updates project data by fetching latest information from GitHub

echo "📊 Updating project data..."
python3 utils/bin/fetch_og_data.py

# Check if any files were modified by fetch_og_data.py
if [[ -n $(git status -s | grep '_data/github_projects.yml\|projects/\|assets/images/projects/') ]]; then
    echo "📝 Project data was updated. Adding changes to commit..."
    # Stage the changes made by fetch_og_data.py
    git add html/_data/github_projects.yml
    git add html/projects/
    git add html/assets/images/projects/
fi

exit 0 