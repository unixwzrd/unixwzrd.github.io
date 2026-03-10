#!/usr/bin/env bash

# Description: Checks for required environment dependencies and Python packages

# Function to check if command exists
command_exists() {
 command -v "$1" >/dev/null 2>&1
}

resolve_python() {
 if command_exists python; then
 command -v python
 elif command_exists python3; then
 command -v python3
 else
 return 1
 fi
}

# Check environment and dependencies
echo "🔧 Checking environment..."
if ! command_exists bundle; then
 echo "❌ Ruby Bundler not found. Please install bundler."
 exit 1
fi

if ! command_exists python && ! command_exists python3; then
 echo "❌ Python 3 not found. Please install Python 3."
 exit 1
fi

# Check Python dependencies
echo "📦 Checking Python dependencies..."
if [ -f requirements.txt ]; then
 python_cmd="$(resolve_python)" || {
 echo "❌ No usable Python interpreter found."
 exit 1
 }
 "${python_cmd}" -c "import pkg_resources; pkg_resources.require(open('requirements.txt').readlines())" 2>/dev/null || {
 echo "❌ Missing Python dependencies. Running: pip install -r requirements.txt"
 "${python_cmd}" -m pip install -r requirements.txt
 }
fi

exit 0
