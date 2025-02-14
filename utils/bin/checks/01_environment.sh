#!/usr/bin/env bash

# Description: Checks for required environment dependencies and Python packages

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check environment and dependencies
echo "🔧 Checking environment..."
if ! command_exists bundle; then
    echo "❌ Ruby Bundler not found. Please install bundler."
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Check Python dependencies
echo "📦 Checking Python dependencies..."
if [ -f requirements.txt ]; then
    python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt').readlines())" 2>/dev/null || {
        echo "❌ Missing Python dependencies. Running: pip install -r requirements.txt"
        pip install -r requirements.txt
    }
fi

exit 0 