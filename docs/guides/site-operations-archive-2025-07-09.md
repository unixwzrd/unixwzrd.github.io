# Site Operations Guide

*Last Updated: 2025-07-09*
- [Site Operations Guide](#site-operations-guide)
  - [Overview](#overview)
  - [Environment Setup](#environment-setup)
    - [Prerequisites](#prerequisites)
    - [Initial Environment Setup](#initial-environment-setup)
      - [1. RVM and Ruby Setup](#1-rvm-and-ruby-setup)
      - [2. Python Environment Setup](#2-python-environment-setup)
      - [3. Project Dependencies](#3-project-dependencies)
      - [4. Environment Variables](#4-environment-variables)
  - [Jekyll Service Management](#jekyll-service-management)
    - [Using the Service Management Scripts](#using-the-service-management-scripts)
      - [1. **Site Service (Orchestrator)**](#1-site-service-orchestrator)
      - [2. **Jekyll Site (Standalone)**](#2-jekyll-site-standalone)
      - [3. **File Watcher (Standalone)**](#3-file-watcher-standalone)
    - [Service Management Options](#service-management-options)
      - [Refresh Control Flags](#refresh-control-flags)
      - [Service Selection Flags](#service-selection-flags)
      - [Default Behaviors](#default-behaviors)
    - [What the Service Scripts Do](#what-the-service-scripts-do)
      - [Site Service (Orchestrator)](#site-service-orchestrator)
      - [Jekyll Site (Standalone)](#jekyll-site-standalone)
      - [File Watcher (Standalone)](#file-watcher-standalone)
    - [Service Status and Monitoring](#service-status-and-monitoring)
  - [Development Workflow](#development-workflow)
    - [Daily Development](#daily-development)
    - [Content Updates](#content-updates)
    - [Production Deployment](#production-deployment)
  - [Environment Variables and Configuration](#environment-variables-and-configuration)
    - [Project Environment (.env/project.env)](#project-environment-envprojectenv)
    - [Jekyll Configuration (\_config.yml)](#jekyll-configuration-_configyml)
  - [Blog Listing \& Pagination (2025-07-09)](#blog-listing--pagination-2025-07-09)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
      - [RVM Issues](#rvm-issues)
      - [Jekyll Build Issues](#jekyll-build-issues)
      - [Port Conflicts](#port-conflicts)
      - [OpenGraph Refresh Issues](#opengraph-refresh-issues)
    - [Service Management Issues](#service-management-issues)
      - [Server Won't Start](#server-wont-start)
      - [Server Won't Stop](#server-wont-stop)
  - [Maintenance Tasks](#maintenance-tasks)
    - [Regular Maintenance](#regular-maintenance)
    - [Performance Optimization](#performance-optimization)
  - [Security Considerations](#security-considerations)
    - [Internal Documentation](#internal-documentation)
    - [Access Control](#access-control)
  - [Quick Reference](#quick-reference)
    - [Essential Commands](#essential-commands)
    - [File Locations](#file-locations)
    - [URLs](#urls)
  - [Image Path Automation for Social Sharing](#image-path-automation-for-social-sharing)
    - [Usage](#usage)
    - [Incremental Pre-commit Integration](#incremental-pre-commit-integration)
    - [What It Does](#what-it-does)
    - [Why This Matters](#why-this-matters)
    - [Next Steps](#next-steps)
  - [File Watcher System](#file-watcher-system)
    - [Overview](#overview-1)
    - [Usage](#usage-1)
    - [Available Watchers](#available-watchers)
    - [Adding New Watchers](#adding-new-watchers)
    - [Example Watcher](#example-watcher)
    - [Integration with Development Workflow](#integration-with-development-workflow)
    - [Jekyll Service Integration](#jekyll-service-integration)
  - [Google Analytics \& SEO Status](#google-analytics--seo-status)
    - [Current Setup](#current-setup)
    - [Critical Issues Found](#critical-issues-found)
    - [What's Working](#whats-working)
    - [What Needs to be Done](#what-needs-to-be-done)
    - [Priority Actions](#priority-actions)
  - [GitHub Pages Deployment Branches](#github-pages-deployment-branches)
    - [What is the `gh-pages` Branch?](#what-is-the-gh-pages-branch)
    - [Why is it Parallel to `main`?](#why-is-it-parallel-to-main)
    - [How is it Created and Updated?](#how-is-it-created-and-updated)
    - [Best Practices](#best-practices)
    - [Why This Approach?](#why-this-approach)

## Overview
This guide covers all technical operations for running and maintaining the Distributed Thinking Systems website. This is **internal documentation only** and should not be publicly served.

---

## Environment Setup

### Prerequisites
- macOS (primary development environment)
- Ruby 3.3.4 (managed via RVM)
- Python 3.x with virtual environment support
- Conda or VenvUtil for Python environment management
- Node.js (for some build tools)
- Git

### Initial Environment Setup

#### 1. RVM and Ruby Setup
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

#### 2. Python Environment Setup
```bash
# Option A: Using Conda
conda activate python-website-dev

# Option B: Using VenvUtil (recommended)
cact python-website-dev

# Verify Python environment
python --version
which python
```

#### 3. Project Dependencies
```bash
# Install Jekyll and dependencies
bundle install

# Verify installation
bundle exec jekyll --version
```

#### 4. Environment Variables
The project uses `.env` files for environment configuration:

```bash
# Source the project environment
source .env/project.env

# This sets up:
# - RVM environment
# - Project paths
# - Development variables
```

---

## Jekyll Service Management

### Using the Service Management Scripts

The project now uses a modular service management system with three main scripts:

#### 1. **Site Service (Orchestrator)**
The [utils/bin/site-service](../utils/bin/site-service) script manages both Jekyll and file watcher services:

```bash
# Start both services
./utils/bin/site-service start

# Start both services (fast mode, no OG refresh)
./utils/bin/site-service start -n

# Start both services (complete mode, with OG refresh)
./utils/bin/site-service start -r

# Restart both services (fast mode by default)
./utils/bin/site-service restart

# Restart both services (complete mode)
./utils/bin/site-service restart -r

# Stop both services
./utils/bin/site-service stop

# Manage individual services
./utils/bin/site-service -j start    # Jekyll only
./utils/bin/site-service -w start    # File watcher only
./utils/bin/site-service -j restart  # Restart Jekyll only

# Help
./utils/bin/site-service --help
```

#### 2. **Jekyll Site (Standalone)**
The [utils/bin/jekyll-site](../utils/bin/jekyll-site) script manages Jekyll independently:

```bash
# Start Jekyll server (complete mode)
./utils/bin/jekyll-site start

# Start Jekyll server (fast mode)
./utils/bin/jekyll-site start -n

# Restart Jekyll server (fast mode by default)
./utils/bin/jekyll-site restart

# Restart Jekyll server (complete mode)
./utils/bin/jekyll-site restart -r

# Build only (complete mode)
./utils/bin/jekyll-site build

# Build only (fast mode)
./utils/bin/jekyll-site build -n

# Stop Jekyll server
./utils/bin/jekyll-site stop

# Help
./utils/bin/jekyll-site --help
```

#### 3. **File Watcher (Standalone)**
The [utils/bin/file_watcher](../utils/bin/file_watcher) script manages file watching independently:

```bash
# Start file watcher
./utils/bin/file_watcher start

# Restart file watcher
./utils/bin/file_watcher restart

# Stop file watcher
./utils/bin/file_watcher stop

# Help
./utils/bin/file_watcher --help
```

### Service Management Options

#### Refresh Control Flags
- `-n, --no-refresh`: Skip OpenGraph data refresh (faster builds)
- `-r, --refresh`: Force OpenGraph data refresh (slower builds)
- **Note**: `-n` and `-r` are incompatible. If both specified, `-n` takes precedence.

#### Service Selection Flags
- `-j, --jekyll`: Manage only Jekyll service
- `-w, --watcher`: Manage only file watcher service
- (default: manage both services)

#### Default Behaviors
- **`start`**: Complete mode (with OG refresh)
- **`restart`**: Fast mode (no OG refresh) - optimized for speed
- **`build`**: Complete mode (with OG refresh)

### What the Service Scripts Do

#### Site Service (Orchestrator)
1. **Service Coordination**: Manages both Jekyll and file watcher
2. **Flag Passing**: Passes refresh flags to Jekyll service
3. **Parallel Management**: Starts/stops services in parallel
4. **Error Handling**: Continues operation even if one service fails

#### Jekyll Site (Standalone)
1. **Environment Setup**: Sources project environment variables
2. **OpenGraph Control**: Conditionally runs `fetch_og.py` based on flags
3. **Cache Clearing**: Removes Jekyll cache and build artifacts
4. **Site Building**: Builds the Jekyll site with verbose output
5. **Server Management**: Starts/stops Jekyll server on port 4000
6. **PID Management**: Stores server PID for proper shutdown

#### File Watcher (Standalone)
1. **File Monitoring**: Watches for changes in specified directories
2. **Action Execution**: Runs configured actions on file changes
3. **Process Management**: Manages watcher processes independently

### Service Status and Monitoring
- **Jekyll PID File**: [utils/etc/jekyll.pid](../utils/etc/jekyll.pid)
- **Watcher PID File**: [utils/etc/file_watcher.pid](../utils/etc/file_watcher.pid)
- **Server URL**: `http://localhost:4000`
- **Logs**: Check terminal output for build and server logs
- **Health Monitoring**: Use [utils/bin/site_reliability_monitor.py](../utils/bin/site_reliability_monitor.py) --mode health --local

---

## Development Workflow

### Daily Development
```bash
# 1. Activate Python environment
conda activate python-website-dev
# OR using VenvUtil
cact python-website-dev

# 2. Start development server (fast mode)
./utils/bin/site-service start -n

# 3. Make changes to content/templates

# 4. Server auto-reloads (or restart if needed)
./utils/bin/site-service restart

# 5. Run pre-commit checks before committing
./utils/bin/check_site.sh
```

### Content Updates
```bash
# For content-only changes (fast mode, no OG refresh)
./utils/bin/site-service start -n

# For project updates (complete mode, with OG refresh)
./utils/bin/site-service start -r

# Quick restart for content changes
./utils/bin/site-service restart
```

### Production Deployment
```bash
# 1. Run full validation
./utils/bin/check_site.sh

# 2. Build for production (complete mode)
./utils/bin/jekyll-site build

# 3. Deploy (GitHub Pages or other hosting)
```

---

## Environment Variables and Configuration

### Project Environment ([.env/project.env](../../.env/project.env))
```bash
# RVM Configuration
export PATH="$HOME/.rvm/bin:$PATH"
source "$HOME/.rvm/scripts/rvm"
rvm use 3.3.4@unixwzrd.github.io --default

# Project paths
export BASE_DIR="/path/to/project"
export HTML_DIR="$BASE_DIR/html"
export SITE_DIR="$BASE_DIR/_site"

# Development variables
export JEKYLL_ENV=development
export JEKYLL_SERVE_HOST=localhost
export JEKYLL_SERVE_PORT=4000
```

### Jekyll Configuration ([_config.yml](../../_config.yml))
Key settings for operations:
- **Source**: [html/](../../html/) (site source directory)
- **Destination**: [_site/](../../_site/) (build output)
- **Pagination**: Disabled (no blog posts on homepage)
- **Collections**: Projects and project posts
- **Plugins**: Email protection, feed, SEO, sitemap

## Blog Listing & Pagination (2025-07-09)
- The main blog page now lists all posts (main + project) with unified styling.
- Blog and project blog post limits are configurable in `_config.yml` (`site_blogs_count`, `project_blog_count`) and can be overridden in page front matter.
- Excerpts are auto-generated from post content, strip images, and are truncated to a configurable word count (`excerpt_word_limit`).
- Pagination is handled client-side via JavaScript and Liquid, not by Jekyll's built-in `paginate` feature. The number of posts per page is configurable, and navigation is smooth with URL updates (e.g., `?page=2`).
- Pagination controls are styled for dark backgrounds and accessibility.

---

## Troubleshooting

### Common Issues

#### RVM Issues
```bash
# If RVM not found
source ~/.rvm/scripts/rvm

# If gemset not found
rvm gemset create unixwzrd.github.io
rvm use 3.3.4@unixwzrd.github.io --default
bundle install
```

#### Jekyll Build Issues
```bash
# Clear all caches
rm -rf _site/
rm -rf html/.jekyll-cache/
rm -rf html/.sass-cache/

# Rebuild
bundle exec jekyll build --trace
```

#### Port Conflicts
```bash
# Check if port 4000 is in use
lsof -i :4000

# Kill process if needed
kill -9 <PID>
```

#### OpenGraph Refresh Issues
```bash
# Manual OpenGraph refresh
python3 utils/bin/fetch_og.py

# Check for API rate limits or network issues
```

### Service Management Issues

#### Server Won't Start
```bash
# Check if PID file exists but process is dead
rm -f utils/etc/jekyll.pid

# Restart service
./utils/bin/site-service restart
```

#### Server Won't Stop
```bash
# Force kill by PID
cat utils/etc/jekyll.pid | xargs kill -9
rm -f utils/etc/jekyll.pid
```

---

## Maintenance Tasks

### Regular Maintenance
- **Weekly**: Run `./utils/bin/check_site.sh` for validation
- **Monthly**: Update dependencies (`bundle update`)
- **Quarterly**: Review and update documentation

### Performance Optimization
- **Image Optimization**: Compress images before adding
- **Cache Management**: Clear caches if build issues occur
- **Dependency Updates**: Keep Jekyll and plugins updated

---

## Security Considerations

### Internal Documentation
- This guide is for internal use only
- Do not commit sensitive information
- Use environment variables for secrets

### Access Control
- Limit access to production deployment
- Use SSH keys for server access
- Regular security updates for dependencies

---

## Quick Reference

### Essential Commands
```bash
# Activate Python environment
conda activate python-website-dev
# OR using VenvUtil
cact python-website-dev

# Start development
./utils/bin/site-service start

# Quick content update
./utils/bin/site-service start -n

# Full validation
./utils/bin/check_site.sh

# Environment setup
source .env/project.env
```

### File Locations
- **Service Script**: [utils/bin/site-service](../utils/bin/site-service)
- **Environment**: [.env/project.env](../../.env/project.env)
- **PID File**: [utils/etc/jekyll.pid](../utils/etc/jekyll.pid)
- **Site Source**: [html/](../../html/)
- **Build Output**: [_site/](../../_site/)

### URLs
- **Development**: `http://localhost:4000`
- **Production**: `https://unixwzrd.ai`

---

## Image Path Automation for Social Sharing

*Last updated 2024-06-26: Now uses incremental checking with timestamp tracking for pre-commit speed.*

To ensure all images (front matter and embedded Markdown) use absolute URLs for social sharing and local development, use the script:

[utils/bin/fix_image_paths.py](../utils/bin/fix_image_paths.py)

### Usage

- **Local development:**
  ```bash
  python3 utils/bin/fix_image_paths.py --base-url http://localhost:4000
  ```
  This rewrites all image links to use localhost, so you can verify images render correctly before publishing.

- **Pre-commit/production:**
  ```bash
  python3 utils/bin/fix_image_paths.py --base-url https://unixwzrd.ai
  ```
  This rewrites all image links to use the production domain for correct social previews.

### Incremental Pre-commit Integration
- The image path check now runs in **incremental mode** by default during pre-commit checks.
- Only Markdown files modified since the last check are scanned, greatly improving speed.
- The last check timestamp is stored in [utils/etc/.image_paths_last_check](../utils/etc/.image_paths_last_check).
- To force a full scan (e.g., after a mass refactor), run:
  ```bash
  ./utils/bin/checks/12_image_paths.sh --full
  ```

### What It Does
- Rewrites both front matter `image:` fields and Markdown-embedded images (`![alt](/path/to/image.png)`) to use the specified base URL.
- Only rewrites links that start with `/` and not already with the base URL.

### Why This Matters
- Ensures local and production environments are consistent.
- Prevents broken images and missing social previews on Twitter, LinkedIn, etc.
- Catches issues before they go live.

### Next Steps
- Test the script on your next new post.
- After validation, integrate with a file watcher and the Jekyll service script.
- See TODO and site-improvement-checklist for tracking progress.

---

## File Watcher System

*Last updated 2024-06-26: General file watcher system for automatic script execution on file changes.*

The file watcher system automatically runs scripts when files change during development, providing real-time feedback and automation.

### Overview

- **Main Watcher**: [utils/bin/file_watcher.py](../utils/bin/file_watcher.py)
- **Watcher Scripts**: [utils/bin/watchers/](../utils/bin/watchers/)/*.py
- **Target Directory**: [html/](../../html/) (configurable)

### Usage

```bash
# Start the file watcher
python utils/bin/file_watcher.py

# List available watchers
python utils/bin/file_watcher.py --list-watchers

# Watch a different directory
python utils/bin/file_watcher.py --target-dir some/other/dir
```

### Available Watchers

- **image_path_fixer.py**: Automatically fixes image paths in Markdown files
- Add more watchers by creating Python scripts in `utils/bin/watchers/`

### Adding New Watchers

1. Create a Python script in `utils/bin/watchers/`
2. Script should accept: `file_path` and `event_type` arguments
3. Script receives environment variables: `WATCHER_FILE`, `WATCHER_EVENT`, `WATCHER_NAME`
4. Use `print()` for success messages
5. Return 0 for success, non-zero for failure

### Example Watcher

```python
#!/usr/bin/env python3
import os
import sys

def main():
    file_path = sys.argv[1]
    event_type = sys.argv[2]

    if not file_path.endswith('.md'):
        return

    print(f"Processing {file_path}")
    # Your watcher logic here

if __name__ == "__main__":
    main()
```

### Integration with Development Workflow

- Run the file watcher alongside your Jekyll development server
- Watchers provide immediate feedback on file changes
- Automatically catch and fix common issues during development
- No need to manually run scripts after each file change

### Jekyll Service Integration

The file watcher is now integrated with the Jekyll service script for seamless management:

```bash
# Start both Jekyll server and file watcher (default)
./utils/bin/site-service start

# Start only Jekyll server
./utils/bin/site-service start -j

# Start only file watcher
./utils/bin/site-service start -w

# Stop both services
./utils/bin/site-service stop

# Stop only Jekyll server
./utils/bin/site-service stop -j

# Stop only file watcher
./utils/bin/site-service stop -w

# Restart both services
./utils/bin/site-service restart
```

This integration ensures that:
- File watcher starts automatically with Jekyll development server
- Both services are properly managed with PID tracking
- Clean shutdown of both services when stopping
- Easy selective control of individual services
- **Dynamic watcher reloading**: New watcher scripts are automatically detected and loaded without restarting the file watcher

---

## Google Analytics & SEO Status

### Current Setup
- **Google Analytics ID**: `G-QZSHSBP292` (configured in `_config.yml`)
- **SEO Plugin**: `jekyll-seo-tag` installed and active
- **Sitemap**: `jekyll-sitemap` plugin generating `/sitemap.xml`
- **Robots.txt**: Configured with sitemap reference
- **Social Meta Tags**: Basic implementation in `social-meta.html`

### Critical Issues Found
1. **Missing Google Analytics Include File**: The `html/_includes/google-analytics.html` file is missing, so GA tracking is not working despite the ID being configured.
2. **Basic SEO Implementation**: While the SEO plugin is installed, we're not using advanced features like structured data or enhanced meta descriptions.

### What's Working
- Basic SEO plugin functionality
- Sitemap generation
- Robots.txt configuration
- Social media meta tags (Open Graph, Twitter Cards)

### What Needs to be Done
1. **Create Google Analytics Include File**: Add proper GA4 tracking code
2. **Enhanced SEO**: Add structured data, optimize meta descriptions, implement breadcrumbs
3. **Conversion Tracking**: Set up goals for contact form submissions, resource downloads
4. **Google Search Console**: Integrate for monitoring and optimization

### Priority Actions
1. **High Priority**: Create the missing `google-analytics.html` file to enable tracking
2. **Medium Priority**: Enhance SEO with structured data and better meta descriptions
3. **Low Priority**: Set up advanced tracking and conversion goals

See TODO.md and site-improvement-checklist.md for detailed task breakdown.

---

## GitHub Pages Deployment Branches

### What is the `gh-pages` Branch?
- The `gh-pages` branch is a special branch used by GitHub Pages to serve your static website.
- When you use deployment actions (like `peaceiris/actions-gh-pages`), your built site (the contents of `_site/`) is pushed to the `gh-pages` branch.
- GitHub then serves the content of that branch at your site's URL (e.g., `https://unixwzrd.github.io`).

### Why is it Parallel to `main`?
- Your `main` branch contains your source code, markdown, scripts, and configuration.
- The `gh-pages` branch contains only the built static site (HTML, CSS, JS, etc.), not your source files.
- They are intentionally separate: you never edit `gh-pages` directly; it's overwritten by the deploy action.

### How is it Created and Updated?
- The deployment workflow (like `peaceiris/actions-gh-pages`) builds your site and pushes the result to `gh-pages`.
- If you switch your GitHub Pages settings to deploy from the `gh-pages` branch, GitHub will serve the site from there.
- If you use the newer "GitHub Actions" deployment source, GitHub manages the deployment branch for you (sometimes as a hidden branch).

### Best Practices
- **Never edit `gh-pages` directly.** Let the deploy action handle it.
- **Keep your source and content in `main`.**
- **If you see files in `main` that look like built site artifacts (HTML, redirect files, etc.),** they probably leaked in from a bad merge or crash and should be removed.
- **Never merge between `main` and `gh-pages`.**

### Why This Approach?
- This separation ensures your source code and your deployed site are isolated.
- If anything goes wrong with the build or deployment, your source (`main`) is unaffected.
- You can always rebuild and redeploy without risking your main branch.

*This documentation should be updated whenever the operational procedures change.*
