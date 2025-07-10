# Reference & Utilities

[← Back to Site Operations Guide](site-operations.md)

<!-- TOC will be auto-generated here -->

This guide contains essential reference material and utility documentation for maintaining and operating the Distributed Thinking Systems website.

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

 