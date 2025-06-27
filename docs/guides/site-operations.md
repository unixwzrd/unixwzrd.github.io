# Site Operations Guide

*Last Updated: 2025-06-26*
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
    - [Using the Jekyll Service Script](#using-the-jekyll-service-script)
      - [Available Commands](#available-commands)
      - [Command Line Options](#command-line-options)
      - [What the Service Script Does](#what-the-service-script-does)
      - [Service Status](#service-status)
  - [Development Workflow](#development-workflow)
    - [Daily Development](#daily-development)
    - [Content Updates](#content-updates)
    - [Production Deployment](#production-deployment)
  - [Environment Variables and Configuration](#environment-variables-and-configuration)
    - [Project Environment (`.env/project.env`)](#project-environment-envprojectenv)
    - [Jekyll Configuration (`_config.yml`)](#jekyll-configuration-_configyml)
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
    - [What It Does](#what-it-does)
    - [Future Integration](#future-integration)
    - [Why This Matters](#why-this-matters)
    - [Next Steps](#next-steps)
  - [Google Analytics \& SEO Status](#google-analytics--seo-status)
    - [Current Setup](#current-setup)
    - [Critical Issues Found](#critical-issues-found)
    - [What's Working](#whats-working)
    - [What Needs to be Done](#what-needs-to-be-done)
    - [Priority Actions](#priority-actions)

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

### Using the Jekyll Service Script

The `utils/bin/jekyll-service` script provides automated Jekyll management:

#### Available Commands
```bash
# Start the Jekyll server (with OpenGraph refresh)
./utils/bin/jekyll-service start

# Start without OpenGraph refresh (faster)
./utils/bin/jekyll-service start --no-refresh

# Stop the server
./utils/bin/jekyll-service stop

# Restart the server
./utils/bin/jekyll-service restart

# Build only (no server)
./utils/bin/jekyll-service build

# Refresh OpenGraph data only
./utils/bin/jekyll-service refresh

# Help
./utils/bin/jekyll-service --help
```

#### Command Line Options
- `-n, --no-refresh`: Skip OpenGraph data refresh (faster startup)
- `build`: Build the site without starting server
- `start`: Start the Jekyll server
- `stop`: Stop the running server
- `restart`: Restart the server
- `refresh`: Only refresh OpenGraph data

#### What the Service Script Does
1. **Environment Setup**: Sources project environment variables
2. **OpenGraph Refresh**: Runs `fetch_og.py` to update project metadata (unless `--no-refresh`)
3. **Cache Clearing**: Removes Jekyll cache and build artifacts
4. **Site Building**: Builds the Jekyll site with verbose output
5. **Server Start**: Starts Jekyll server on port 4000
6. **PID Management**: Stores server PID for proper shutdown

#### Service Status
- **PID File**: `utils/etc/jekyll.pid`
- **Server URL**: `http://localhost:4000`
- **Logs**: Check terminal output for build and server logs

---

## Development Workflow

### Daily Development
```bash
# 1. Activate Python environment
conda activate python-website-dev
# OR using VenvUtil
cact python-website-dev

# 2. Start development server
./utils/bin/jekyll-service start

# 3. Make changes to content/templates

# 4. Server auto-reloads (or restart if needed)
./utils/bin/jekyll-service restart

# 5. Run pre-commit checks before committing
./utils/bin/check_site.sh
```

### Content Updates
```bash
# For content-only changes (no OpenGraph refresh needed)
./utils/bin/jekyll-service start --no-refresh

# For project updates (refresh OpenGraph data)
./utils/bin/jekyll-service start
```

### Production Deployment
```bash
# 1. Run full validation
./utils/bin/check_site.sh

# 2. Build for production
./utils/bin/jekyll-service build

# 3. Deploy (GitHub Pages or other hosting)
```

---

## Environment Variables and Configuration

### Project Environment (`.env/project.env`)
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
export JEKYLL_SERVE_HOST=0.0.0.0
export JEKYLL_SERVE_PORT=4000
```

### Jekyll Configuration (`_config.yml`)
Key settings for operations:
- **Source**: `html/` (site source directory)
- **Destination**: `_site/` (build output)
- **Pagination**: Disabled (no blog posts on homepage)
- **Collections**: Projects and project posts
- **Plugins**: Email protection, feed, SEO, sitemap

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
./utils/bin/jekyll-service restart
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
./utils/bin/jekyll-service start

# Quick content update
./utils/bin/jekyll-service start --no-refresh

# Full validation
./utils/bin/check_site.sh

# Environment setup
source .env/project.env
```

### File Locations
- **Service Script**: `utils/bin/jekyll-service`
- **Environment**: `.env/project.env`
- **PID File**: `utils/etc/jekyll.pid`
- **Site Source**: `html/`
- **Build Output**: `_site/`

### URLs
- **Development**: `http://localhost:4000`
- **Production**: `https://unixwzrd.ai`

---

## Image Path Automation for Social Sharing

To ensure all images (front matter and embedded Markdown) use absolute URLs for social sharing and local development, use the script:

    utils/bin/fix_image_paths.py

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

### What It Does
- Rewrites both front matter `image:` fields and Markdown-embedded images (`![alt](/path/to/image.png)`) to use the specified base URL.
- Only rewrites links that start with `/` and not already with the base URL.

### Future Integration
- We plan to integrate this script with a file watcher (e.g., watchdog) so it runs automatically on Markdown changes during local dev.
- The script will also be part of the pre-commit workflow to ensure all images are correct before publishing.

### Why This Matters
- Ensures local and production environments are consistent.
- Prevents broken images and missing social previews on Twitter, LinkedIn, etc.
- Catches issues before they go live.

### Next Steps
- Test the script on your next new post.
- After validation, integrate with a file watcher and the Jekyll service script.
- See TODO and site-improvement-checklist for tracking progress.

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

*This documentation should be updated whenever the operational procedures change.* 