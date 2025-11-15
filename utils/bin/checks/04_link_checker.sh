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

# Function to URL decode a string
urldecode() {
    local url_encoded="${1//+/ }"
    printf '%b' "${url_encoded//%/\\x}"
}

# Record a page as linked if it exists
record_linked_page() {
    local candidate="$1"
    if [ -n "$candidate" ] && [ -e "$candidate" ]; then
        echo "$candidate" >> "$LINKED_PAGES"
    fi
}

# Attempt to resolve pretty permalinks (e.g. /category/yyyy/mm/dd/slug/)
resolve_pretty_permalink() {
    local trimmed="$1"

    IFS='/' read -r -a parts <<< "$trimmed"
    local count=${#parts[@]}

    if (( count < 4 )); then
        return 1
    fi

    local slug="${parts[count-1]}"
    local day="${parts[count-2]}"
    local month="${parts[count-3]}"
    local year="${parts[count-4]}"

    if [[ ! "$year" =~ ^[0-9]{4}$ ]] || [[ ! "$month" =~ ^[0-9]{2}$ ]] || [[ ! "$day" =~ ^[0-9]{2}$ ]]; then
        return 1
    fi

    local prefix=""
    if (( count > 4 )); then
        prefix=$(printf "/%s" "${parts[@]:0:count-4}")
        prefix="${prefix:1}"
    fi

    local base_dir="html"
    if [ -n "$prefix" ]; then
        base_dir="$base_dir/$prefix"
    fi

    local slug_file="${year}-${month}-${day}-${slug}"
    for ext in md markdown html; do
        local post_path="$base_dir/_posts/${slug_file}.${ext}"
        if [ -f "$post_path" ]; then
            printf '%s' "$post_path"
            return 0
        fi
    done

    return 1
}

resolve_target_path() {
    local base_target="$1"
    local target_no_slash="${base_target#/}"

    case "$target_no_slash" in
        about/credentials)
            if [ -f "html/about/sullivan-michael-creds.md" ]; then
                printf '%s' "html/about/sullivan-michael-creds.md"
                return 0
            fi
            ;;
    esac

    if [ -z "$target_no_slash" ]; then
        for candidate in html/index.md html/index.html; do
            if [ -f "$candidate" ]; then
                printf '%s' "$candidate"
                return 0
            fi
        done
        return 1
    fi

    local candidates=(
        "html/${target_no_slash}"
        "html/${target_no_slash}.md"
        "html/${target_no_slash}.html"
        "html/${target_no_slash}/index.md"
        "html/${target_no_slash}/index.html"
    )

    for candidate in "${candidates[@]}"; do
        if [ -f "$candidate" ]; then
            printf '%s' "$candidate"
            return 0
        fi
    done

    if [[ "$target_no_slash" == *.html ]]; then
        local base_without_ext=${target_no_slash%.html}
        for ext in md markdown; do
            local alt="html/${base_without_ext}.${ext}"
            if [ -f "$alt" ]; then
                printf '%s' "$alt"
                return 0
            fi
        done
    fi

    if [ -d "html/${target_no_slash}" ]; then
        for candidate in html/${target_no_slash}/index.md html/${target_no_slash}/index.html; do
            if [ -f "$candidate" ]; then
                printf '%s' "$candidate"
                return 0
            fi
        done
    fi

    local resolved
    if resolved=$(resolve_pretty_permalink "$target_no_slash"); then
        printf '%s' "$resolved"
        return 0
    fi

    return 1
}

process_internal_link() {
    local raw_target="$1"
    local source_file="$2"

    if [ -z "$raw_target" ]; then
        return
    fi


    if [[ "$raw_target" == *'{{'* ]] || [[ "$raw_target" == *'}}'* ]]; then
        return
    fi
    raw_target=$(echo "$raw_target" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    case "$raw_target" in
        http*|https*|mailto:*|tel:*|javascript:*|ftp:*|news:*|data:*|\//* )
            return
            ;;
    esac

    if [[ "$raw_target" == \#* ]]; then
        return
    fi

    local decoded_target=$(urldecode "$raw_target")

    if [[ "$decoded_target" != /* ]]; then
        local absolute_target
        absolute_target=$(python3 - "$source_file" "$decoded_target" <<'PY'
import os
import sys

source_file = os.path.abspath(sys.argv[1])
raw_target = sys.argv[2]
base_dir = os.path.abspath('html')

candidate = os.path.normpath(os.path.join(os.path.dirname(source_file), raw_target))

if not candidate.startswith(base_dir):
    print(candidate, end='')
else:
    rel = os.path.relpath(candidate, base_dir)
    print('/' + rel.replace(os.sep, '/'), end='')
PY
)
        decoded_target="$absolute_target"
    fi

    local without_anchor="${decoded_target%%#*}"
    if [ -z "$without_anchor" ]; then
        without_anchor="$decoded_target"
    fi

    if [[ "$without_anchor" != / ]]; then
        without_anchor="${without_anchor%/}"
    fi

    local resolved_path
    if resolved_path=$(resolve_target_path "$without_anchor"); then
        record_linked_page "$resolved_path"
    else
        echo "⚠️ Broken link in $source_file: $raw_target" >> "$BROKEN_LINKS"
    fi
}

# Find all pages
find html -type f \( -name "*.md" -o -name "*.html" \) ! -path "*/\.*" ! -path "*/_site/*" -print > "$ALL_PAGES"

# Initialize linked pages file
touch "$LINKED_PAGES"

# Check for broken links and collect linked pages
echo "🔗 Checking for broken links..."
quote=$'"'
while IFS= read -r file; do
    grep -o '\[[^]]*\]([^)]*)' "$file" 2>/dev/null | while read -r link; do
        target=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
        process_internal_link "$target" "$file"
    done

    grep -o 'href="[^"]*"' "$file" 2>/dev/null | while read -r href; do
        target=${href#href=$quote}
        target=${target%$quote}
        process_internal_link "$target" "$file"
    done

    grep -o '\[.*\](http[^)]*)' "$file" 2>/dev/null | while read -r link; do
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
    found_orphan=0
    while IFS= read -r page; do
        if [[ "$page" == *"/.jekyll-cache/"* ]] || \
           [[ "$page" == *"/_includes/"* ]] || \
           [[ "$page" == *"/_layouts/"* ]] || \
           [[ "$page" == *"/_sass/"* ]] || \
           [[ "$page" == *"/_plugins/"* ]] || \
           [[ "$page" == *"/_data/"* ]] || \
           [[ "$page" == *"/_drafts/"* ]] || \
           [[ "$page" == html/*.md ]] || \
           [[ "$page" == html/projects/*.md ]] || \
           [[ "$page" == *"/_posts/"* ]]; then
            continue
        fi
        # Exclude certain pages that are okay to be "orphaned"
        if [[ ! "$page" =~ (404|index|README|CHANGELOG).*(md|html)$ ]]; then
            if (( found_orphan == 0 )); then
                echo "⚠️ Found potentially orphaned pages (not linked from any other page):"
                found_orphan=1
            fi
            echo "   $page"
        fi
    done < "$ORPHAN_PAGES"
fi

exit 0
