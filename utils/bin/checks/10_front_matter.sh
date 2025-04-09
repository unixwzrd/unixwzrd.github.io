#!/usr/bin/env bash

# Description: Ensures all markdown posts have required front matter fields:
#              image, title, and excerpt.
#              Auto-inserts default values if missing.

echo "📄 Checking and fixing front matter fields: image, title, excerpt..."

# Configurable defaults
DEFAULT_IMAGE="/assets/images/default-og-image.png"

# Base directories
PROJECT_DIR="html/projects"
BLOG_DIR="html/_posts"

# Track which files were modified
modified_files=()

process_file() {
    local file="$1"
    local modified=false

    # Read front matter block
    frontmatter=$(awk '/^---/{f=!f; next} f' "$file")

    # Check and add missing image
    if ! grep -q "^image:" <<< "$frontmatter"; then
        # Create a temporary file for the sed operation
        sed "/^---$/a\\
image: $DEFAULT_IMAGE" "$file" > "${file}.tmp" && \
        mv "${file}.tmp" "$file"
        echo "➕ Added default image to $file"
        modified=true
    fi

    # Check and add missing title
    if ! grep -q "^title:" <<< "$frontmatter"; then
        # Extract title from first H1 heading or use default
        title=$(awk '/^# /{print substr($0,3); exit}' "$file")
        title=${title:-"Untitled Post"}
        # Escape any double quotes in the title
        title=${title//\"/\\\"}
        # Create a temporary file for the sed operation
        sed "/^---$/a\\
title: \"$title\"" "$file" > "${file}.tmp" && \
        mv "${file}.tmp" "$file"
        echo "➕ Added inferred title to $file"
        modified=true
    fi

    # Check and add missing excerpt
    if ! grep -q "^excerpt:" <<< "$frontmatter"; then
        # Extract first non-empty line after front matter or use default
        excerpt=$(awk '/^---/{f=!f; next} f==0 && NF > 0 {print; exit}' "$file")
        excerpt=${excerpt:-"No excerpt provided."}
        # Escape any double quotes in the excerpt
        excerpt=${excerpt//\"/\\\"}
        # Create a temporary file for the sed operation
        sed "/^---$/a\\
excerpt: \"$excerpt\"" "$file" > "${file}.tmp" && \
        mv "${file}.tmp" "$file"
        echo "➕ Added default excerpt to $file"
        modified=true
    fi

    [[ "$modified" == true ]] && modified_files+=("$file")
}

echo "Checking project blog posts..."
# Find all markdown files in project _posts and _drafts directories
while IFS= read -r -d '' file; do
    process_file "$file"
done < <(find "$PROJECT_DIR" -type d \( -name "_posts" -o -name "_drafts" \) -exec find {} -name "*.md" -print0 \;)

echo "Checking general blog posts..."
# Find all markdown files in the main _posts directory
while IFS= read -r -d '' file; do
    process_file "$file"
done < <(find "$BLOG_DIR" -name "*.md" -print0 2>/dev/null || true)

if [[ "${#modified_files[@]}" -gt 0 ]]; then
    echo "✅ Updated front matter in the following files:"
    printf ' - %s\n' "${modified_files[@]}"
else
    echo "✅ All posts already contain required front matter."
fi