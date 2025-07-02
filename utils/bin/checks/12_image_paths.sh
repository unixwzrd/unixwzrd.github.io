#!/bin/bash

# Image Path Checker - Incremental Mode
# Automatically fixes image paths and case sensitivity issues for local development or production
# Uses timestamp tracking to only check modified files since last run

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
cd "$PROJECT_ROOT"

# Timestamp file for tracking last check
TIMESTAMP_FILE="utils/etc/.image_paths_last_check"
TARGET_DIR="html"

# Detect environment
if [[ "$JEKYLL_ENV" == "production" ]] || [[ "$1" == "--production" ]]; then
    BASE_URL="https://unixwzrd.ai"
    ENV_NAME="production"
elif [[ "$1" == "--local" ]]; then
    BASE_URL="http://localhost:4000"
    ENV_NAME="local"
else
    # Auto-detect: if we're in a git hook or CI, use production
    if [[ -n "$GIT_HOOK" ]] || [[ -n "$CI" ]] || [[ "$1" == "--pre-commit" ]]; then
        BASE_URL="https://unixwzrd.ai"
        ENV_NAME="production (auto-detected)"
    else
        BASE_URL="http://localhost:4000"
        ENV_NAME="local (auto-detected)"
    fi
fi

echo "🔍 Checking image paths and case sensitivity for $ENV_NAME environment (base URL: $BASE_URL)"

# Function to run image path fixes
run_image_path_fixes() {
    local files_to_check="$1"
    local check_type="$2"
    
    echo "🔧 Running $check_type image path fixes..."
    
    if [[ -n "$files_to_check" ]]; then
        # Process specific files
        echo "$files_to_check" | while read -r file; do
            if [[ -n "$file" ]]; then
                echo "  📝 Processing: $file"
                python3 utils/bin/fix_image_paths.py --base-url "$BASE_URL" --target-dir "$TARGET_DIR" --file-filter "$(basename "$file")"
            fi
        done
    else
        # Process all files
        python3 utils/bin/fix_image_paths.py --base-url "$BASE_URL" --target-dir "$TARGET_DIR"
    fi
}

# Function to run case sensitivity checks
run_case_sensitivity_checks() {
    local files_to_check="$1"
    local check_type="$2"
    
    echo "🔍 Running $check_type case sensitivity checks..."
    
    if [[ -n "$files_to_check" ]]; then
        # Process specific files
        echo "$files_to_check" | while read -r file; do
            if [[ -n "$file" ]]; then
                echo "  📝 Checking case sensitivity in: $file"
                python3 utils/bin/fix_image_case_sensitivity.py --target-file "$file"
            fi
        done
    else
        # Process all files
        python3 utils/bin/fix_image_case_sensitivity.py
    fi
}

# Check if we should run incremental or full scan
if [[ "$1" == "--full" ]] || [[ "$2" == "--full" ]]; then
    echo "📋 Running full image path and case sensitivity scan..."
    run_image_path_fixes "" "full"
    run_case_sensitivity_checks "" "full"
    echo "$(date +%s)" > "$TIMESTAMP_FILE"
    echo "✅ Full image path and case sensitivity check completed"
else
    # Incremental mode - only check files modified since last run
    if [[ -f "$TIMESTAMP_FILE" ]]; then
        LAST_CHECK=$(cat "$TIMESTAMP_FILE")
        if [[ -n "$LAST_CHECK" ]] && [[ "$LAST_CHECK" =~ ^[0-9]+$ ]]; then
            LAST_CHECK_DATE=$(date -r "$LAST_CHECK" 2>/dev/null || echo "unknown time")
        else
            LAST_CHECK_DATE="unknown time"
        fi
        echo "📋 Running incremental image path and case sensitivity scan (since $LAST_CHECK_DATE)..."
        
        # Find modified Markdown files since last check
        MODIFIED_FILES=$(find "$TARGET_DIR" -name "*.md" -newer "$TIMESTAMP_FILE" 2>/dev/null || true)
        
        if [[ -n "$MODIFIED_FILES" ]]; then
            echo "📝 Found modified files:"
            echo "$MODIFIED_FILES" | while read -r file; do
                echo "  - $file"
            done
            
            # Run image path fixes on modified files
            run_image_path_fixes "$MODIFIED_FILES" "incremental"
            
            # Run case sensitivity checks on modified files
            run_case_sensitivity_checks "$MODIFIED_FILES" "incremental"
        else
            echo "📝 No modified Markdown files found since last check"
        fi
    else
        echo "📋 No previous check timestamp found, running full scan..."
        run_image_path_fixes "" "full"
        run_case_sensitivity_checks "" "full"
    fi
    
    # Update timestamp
    echo "$(date +%s)" > "$TIMESTAMP_FILE"
    echo "✅ Incremental image path and case sensitivity check completed"
fi 