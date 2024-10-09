#!/bin/bash

# shell_scripts/update_structure.sh

# Set the base directory
[[ -e .env/project.env ]] && source .env/project.env || { echo "Error: .env/project.env file not found."; exit 1; }

WEB_ROOT="html"

# 1. Move existing style.scss to _overrides.scss if it exists
if [ -f "$WEB_ROOT/assets/css/style.scss" ]; then
  mv "$WEB_ROOT/assets/css/style.scss" "$WEB_ROOT/assets/css/_overrides.scss"
fi

# 2. Create the new SCSS partials if they don't exist
touch "$WEB_ROOT/assets/css/_variables.scss"
touch "$WEB_ROOT/assets/css/_base.scss"
touch "$WEB_ROOT/assets/css/_layout.scss"
touch "$WEB_ROOT/assets/css/_components.scss"

# 3. Create style.scss that imports the partials
cat <<EOL > "$WEB_ROOT/assets/css/style.scss"
---
---

@import
  "minima/skins/{{ site.minima.skin | default: 'auto' }}",
  "minima/initialize",
  "variables",
  "base",
  "layout",
  "components",
  "overrides";
EOL

# 4. Remove existing project markdown files and directories (optional)
read -r -p "Do you want to remove existing project markdown files and directories in html/projects/? (y/n): " choice
if [ "$choice" == "y" ]; then
  find "$WEB_ROOT/projects/" -type f -name "*.md" -not -name "projects.md" -delete
  find "$WEB_ROOT/projects/" -type d -not -path "$WEB_ROOT/projects/" -exec rm -r {} +
fi

# 5. Ensure necessary directories exist
mkdir -p "$WEB_ROOT/_layouts"
mkdir -p "$WEB_ROOT/_includes"
mkdir -p "$WEB_ROOT/_data"

# 6. Copy the new layout and include files
# Assuming you have the new files in a directory called 'new_files'
cp new_files/_layouts/project.html "$WEB_ROOT/_layouts/"
cp new_files/_includes/projects_list.html "$WEB_ROOT/_includes/"

# 7. Copy updated SCSS partials
cp new_files/assets/css/_variables.scss "$WEB_ROOT/assets/css/"
cp new_files/assets/css/_base.scss "$WEB_ROOT/assets/css/"
cp new_files/assets/css/_layout.scss "$WEB_ROOT/assets/css/"
cp new_files/assets/css/_components.scss "$WEB_ROOT/assets/css/"
cp new_files/assets/css/_overrides.scss "$WEB_ROOT/assets/css/"

echo "File structure updated successfully."