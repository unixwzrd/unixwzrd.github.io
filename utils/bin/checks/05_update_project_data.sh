#!/usr/bin/env bash

# Description: Updates project data by fetching latest information from GitHub

resolve_python() {
 if command -v python >/dev/null 2>&1; then
 command -v python
 elif command -v python3 >/dev/null 2>&1; then
 command -v python3
 else
 return 1
 fi
}

echo "📊 Updating project data..."
python_cmd="$(resolve_python)" || {
 echo "❌ No usable Python interpreter found for project data update."
 exit 1
}
"${python_cmd}" utils/bin/fetch_og.py

# Check if any files were modified by fetch_og.py
if [[ -n $(git status -s | grep '_data/github_projects.yml\|projects/\|assets/images/projects/') ]]; then
 echo "📝 Project data was updated. Adding changes to commit..."
 # Stage the changes made by fetch_og.py
 git add html/_data/github_projects.yml
 git add html/projects/
 git add html/assets/images/projects/
fi

exit 0
