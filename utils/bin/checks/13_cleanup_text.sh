#!/usr/bin/env bash
# Description: Clean Unicode quirks and normalize text formatting in changed files

set -e

echo "🧹 Cleaning up text formatting in changed files..."

# Get list of changed files (staged and unstaged)
changed_files=$(git diff --name-only --cached 2>/dev/null || true)
unstaged_files=$(git diff --name-only 2>/dev/null || true)
all_changed_files=$(echo -e "${changed_files}\n${unstaged_files}" | sort -u | grep -v '^$')

if [ -z "$all_changed_files" ]; then
    echo "✅ No changed files to clean up"
    exit 0
fi

# Filter for text files that should be cleaned
text_files=""
for file in $all_changed_files; do
    # Skip binary files and certain directories
    if [[ "$file" =~ \.(md|txt|py|sh|yml|yaml|json|html|css|scss|js|rb)$ ]] && \
       [[ ! "$file" =~ ^(_site|node_modules|vendor)/ ]] && \
       [ -f "$file" ]; then
        text_files="$text_files $file"
    fi
done

if [ -z "$text_files" ]; then
    echo "✅ No text files to clean up"
    exit 0
fi

echo "📝 Processing text files: $text_files"

# Process each file
for file in $text_files; do
    if [ -f "$file" ]; then
        echo "  Cleaning: $file"

        # Create a temporary file
        temp_file=$(mktemp)

        # Use cleanup-text as a filter
        if cat "$file" | cleanup-text > "$temp_file" 2>/dev/null; then
            # Check if the file actually changed
            if ! cmp -s "$file" "$temp_file"; then
                # File changed, replace it
                mv "$temp_file" "$file"
                echo "    ✅ Cleaned: $file"

                # If file was staged, re-stage it
                if git diff --cached --name-only | grep -q "^$file$"; then
                    git add "$file"
                    echo "    📝 Re-staged: $file"
                fi
            else
                echo "    ℹ️  No changes needed: $file"
                rm "$temp_file"
            fi
        else
            echo "    ⚠️  Warning: Could not process $file (may be binary or corrupted)"
            rm "$temp_file"
        fi
    fi
done

echo "✅ Text cleanup completed" 