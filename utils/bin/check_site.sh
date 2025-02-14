#!/usr/bin/env bash

# Exit on error
set -e

echo "Running pre-commit Jekyll site checks..."

# Store the current directory and site root
CURRENT_DIR=$(pwd)
SITE_ROOT=$(git rev-parse --show-toplevel)

# Function to cleanup and exit
cleanup() {
    cd "$CURRENT_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ Checks failed! Please fix the issues before committing."
        exit 1
    fi
}

# Set up trap for cleanup
trap cleanup EXIT

# Navigate to the site root directory
cd "$SITE_ROOT"

# Directory containing check scripts
CHECKS_DIR="utils/bin/checks"

# Default to running all checks if none specified
CHECKS_TO_RUN=()
SKIP_CHECKS=()

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --run)
            shift
            IFS=',' read -ra CHECKS_TO_RUN <<< "$1"
            ;;
        --skip)
            shift
            IFS=',' read -ra SKIP_CHECKS <<< "$1"
            ;;
        --list)
            echo "Available checks:"
            for check in "$CHECKS_DIR"/*.sh; do
                name=$(basename "$check")
                description=$(head -n3 "$check" | grep "# Description:" | cut -d':' -f2-)
                echo "  ${name%.sh}: ${description:-No description available}"
            done
            exit 0
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --run check1,check2,...    Run only specified checks"
            echo "  --skip check1,check2,...   Skip specified checks"
            echo "  --list                     List available checks"
            echo "  --help                     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
    shift
done

# Function to should_run_check
should_run_check() {
    local check=$1
    
    # If specific checks are specified, only run those
    if [ ${#CHECKS_TO_RUN[@]} -gt 0 ]; then
        [[ " ${CHECKS_TO_RUN[@]} " =~ " ${check} " ]] && return 0 || return 1
    fi
    
    # If check is in skip list, don't run it
    [[ " ${SKIP_CHECKS[@]} " =~ " ${check} " ]] && return 1 || return 0
}

# Run all check scripts in numerical order
for check in "$CHECKS_DIR"/*.sh; do
    if [ -f "$check" ]; then
        check_name=$(basename "$check" .sh)
        if should_run_check "$check_name"; then
            echo "Running check: $check_name"
            chmod +x "$check"
            if ! "$check"; then
                echo "❌ Check $check_name failed"
                exit 1
            fi
        else
            echo "Skipping check: $check_name"
        fi
    fi
done

echo "✅ All checks passed successfully!" 