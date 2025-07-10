# Environment Setup

[← Back to Site Operations Guide](site-operations.md)

- [Environment Setup](#environment-setup)
  - [Prerequisites](#prerequisites)
  - [Initial Environment Setup](#initial-environment-setup)
    - [1. RVM and Ruby Setup](#1-rvm-and-ruby-setup)
    - [2. Python Environment Setup](#2-python-environment-setup)
    - [3. Project Dependencies](#3-project-dependencies)
    - [4. Environment Variables](#4-environment-variables)

This section covers how to configure your local and production environments, including Ruby, Python, Node.js, and all project dependencies.

## Prerequisites
- macOS (primary development environment)
- Ruby 3.3.4 (managed via RVM)
- Python 3.x with virtual environment support
- Conda or VenvUtil for Python environment management
- Node.js (for some build tools)
- Git

## Initial Environment Setup

### 1. RVM and Ruby Setup
```bash
# Install RVM if not already installed
curl -sSL https://get.rvm.io | bash -s stable

# Restart shell or source RVM
source ~/.rvm/scripts/rvm

# Install Ruby 3.3.4
rvm install 3.3.4
rvm use 3.3.4 --default

# Create gemset for this project
rvm gemset create unixwzrd.github.io
rvm use 3.3.4@unixwzrd.github.io --default
```

### 2. Python Environment Setup
```bash
# Option A: Using Conda
conda activate python-website-dev

# Option B: Using VenvUtil (recommended)
cact python-website-dev

# Verify Python environment
python --version
which python
```

### 3. Project Dependencies
```bash
# Install Jekyll and dependencies
bundle install

# Verify installation
bundle exec jekyll --version
```

### 4. Environment Variables
The project uses `.env` files for environment configuration:

```bash
# Source the project environment
source .env/project.env

# This sets up:
# - RVM environment
# - Project paths
# - Development variables
``` 