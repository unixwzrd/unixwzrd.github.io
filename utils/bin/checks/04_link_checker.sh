#!/usr/bin/env bash

# Description: Checks for broken internal links and orphaned pages

# Create temporary files for link checking
TEMP_DIR=$(mktemp -d)
LINKED_PAGES="$TEMP_DIR/linked_pages.txt"
ALL_PAGES="$TEMP_DIR/all_pages.txt"
ORPHAN_PAGES="$TEMP_DIR/orphan_pages.txt"
BROKEN_LINKS="$TEMP_DIR/broken_links.txt"

# Cleanup temporary files on exit
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "🔍 Running comprehensive link checks..."

# Find all pages
find html -type f \( -name "*.md" -o -name "*.html" \) ! -path "*/\.*" ! -path "*/_site/*" -print > "$ALL_PAGES"

# Initialize linked pages file
touch "$LINKED_PAGES"

# Check for broken links and collect linked pages
echo "🔗 Checking for broken links..."
while IFS= read -r file; do
    # Extract all internal links from the file
    grep -o "\[.*\]([^)]*)" "$file" | grep -v "^http" | grep -v "^#" | while read -r link; do
        target=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
        if [[ $target == /* ]]; then
            # Remove trailing slash and add potential extensions
            base_target=${target%/}
            # Add the target to linked pages
            echo "html${base_target}" >> "$LINKED_PAGES"
            echo "html${base_target}.md" >> "$LINKED_PAGES"
            echo "html${base_target}/index.md" >> "$LINKED_PAGES"
            echo "html${base_target}.html" >> "$LINKED_PAGES"
            
            # Check if the target exists
            if [ ! -f "html${base_target}" ] && [ ! -f "html${base_target}.md" ] && \
               [ ! -f "html${base_target}/index.md" ] && [ ! -f "html${base_target}.html" ]; then
                echo "⚠️ Broken link in $file: $target" >> "$BROKEN_LINKS"
            fi
        fi
    done

    # Check for external links (just warn about them)
    grep -o "\[.*\](http[^)]*)" "$file" | while read -r link; do
        echo "ℹ️ External link in $file: $link"
    done
done < "$ALL_PAGES"

# Find orphan pages
echo "🔍 Checking for orphan pages..."
sort -u "$LINKED_PAGES" > "${LINKED_PAGES}.sorted"
sort -u "$ALL_PAGES" > "${ALL_PAGES}.sorted"
comm -23 "${ALL_PAGES}.sorted" "${LINKED_PAGES}.sorted" > "$ORPHAN_PAGES"

# Report findings
if [ -s "$BROKEN_LINKS" ]; then
    echo "❌ Found broken internal links:"
    cat "$BROKEN_LINKS"
    exit 1
fi

if [ -s "$ORPHAN_PAGES" ]; then
    echo "⚠️ Found potentially orphaned pages (not linked from any other page):"
    while IFS= read -r page; do
        # Exclude certain pages that are okay to be "orphaned"
        if [[ ! "$page" =~ (404|index|README|CHANGELOG).*(md|html)$ ]]; then
            echo "   $page"
        fi
    done < "$ORPHAN_PAGES"
fi

exit 0 