#!/usr/bin/env bash

# Description: Checks for common Liquid syntax issues like missing endfor/endif tags

echo "💧 Checking Liquid syntax..."
find html -name "*.md" -o -name "*.html" | while read -r file; do
    if grep -l "{%\s*for\s*.*%}" "$file" > /dev/null; then
        if ! grep -l "{%\s*endfor\s*%}" "$file" > /dev/null; then
            echo "⚠️ Warning: Possible missing endfor in $file"
        fi
    fi
    if grep -l "{%\s*if\s*.*%}" "$file" > /dev/null; then
        if ! grep -l "{%\s*endif\s*%}" "$file" > /dev/null; then
            echo "⚠️ Warning: Possible missing endif in $file"
        fi
    fi
done

exit 0 