#!/usr/bin/env bash

BASE_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../..")"

outfile="$BASE_DIR/unified_source.md"
cat /dev/null > "$outfile"

generate_markdown() {
    source_file="$1"
    markdown_type="$2"
    (
        echo; echo
        echo "Filename ==>  $source_file"
        echo "\`\`\`$markdown_type"
        cat "$source_file"
        echo >> "$outfile"
        echo "\`\`\`"
    ) >> "$outfile"
}





files="$(find . -type f | grep -v .ico | grep -v manifest | grep -v DS_ | grep -v .svg | grep -v .png | grep -v tmp | grep -v .git | grep -v _site | grep -v pdf | grep -v JPG | grep -v htaccess | grep -v webp | grep -v .jekyll | grep -E ",bd|.html|.yml" | sort )"

(
    echo "Generating unified source..."
    echo; echo
    echo "Jekyll filesystem directory structure"
    echo "\`\`\`text"
    filetree --exclude tmp .git
    echo
    echo "\`\`\`"
) >> "$outfile"

for file in $files
do
    case "$file" in
        *".md") filetype="markdown";;
        *".yml") filetype="yaml";;
        *".html") filetype="html";;
        *".rb") filetype="ruby";;
        *".sh") filetype="bash";;
        *".txt") filetype="text";;
        *".py") filetype="python";;
        *".js") filetype="javascript";;
        *".css") filetype="css";;
        *".json") filetype="json";;
        *".sass") filetype="sass";;
        *".scss") filetype="scss";;
        *) echo "File type not recognized: $file" && filetype="unknown";;
    esac
    generate_markdown "$file" "$filetype"
done