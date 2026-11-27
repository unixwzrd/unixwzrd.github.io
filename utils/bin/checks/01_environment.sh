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

echo "💎 Checking Ruby bundle: $(command -v bundle)"
if ! bundle check; then
    echo "❌ Locked Ruby gems are missing. Activate the project Ruby gemset and run bundle install explicitly." >&2
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
    echo "🐍 Python: ${python_cmd}"
    if ! "${python_cmd}" - <<'PY'
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys

try:
    from packaging.requirements import Requirement
except ImportError:
    sys.exit("Missing packaging: activate the project's Conda environment before checking requirements.")

errors = []
for line in Path("requirements.txt").read_text().splitlines():
    requirement = line.split("#", 1)[0].strip()
    if not requirement:
        continue
    try:
        req = Requirement(requirement)
        if req.marker and not req.marker.evaluate():
            continue
        installed = version(req.name)
        if not req.specifier.contains(installed):
            errors.append(f"{req}: installed {installed}")
    except PackageNotFoundError:
        errors.append(f"{requirement}: not installed")
    except ValueError as exc:
        errors.append(f"{requirement}: {exc}")
if errors:
    sys.exit("Unsatisfied Python requirements:\n  " + "\n  ".join(errors))
print("Python requirements satisfied.")
PY
    then
        echo "❌ Python dependency check failed. Activate python-website-dev and resolve its requirements explicitly; no packages were installed." >&2
        exit 1
    fi
fi

exit 0


