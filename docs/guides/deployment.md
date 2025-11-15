# Deployment

[← Back to Site Operations Guide](site-operations.md)

- [Deployment](#deployment)
  - [Development Workflow](#development-workflow)
    - [Daily Development](#daily-development)
    - [Content Updates](#content-updates)
    - [Production Deployment](#production-deployment)
  - [Environment Variables and Configuration](#environment-variables-and-configuration)
    - [Project Environment (.env/project.env)](#project-environment-envprojectenv)
    - [Jekyll Configuration (\_config.yml)](#jekyll-configuration-_configyml)
  - [GitHub Pages Deployment Branches](#github-pages-deployment-branches)
    - [What is the `gh-pages` Branch?](#what-is-the-gh-pages-branch)
    - [Why is it Parallel to `main`?](#why-is-it-parallel-to-main)
    - [How is it Created and Updated?](#how-is-it-created-and-updated)
    - [Best Practices](#best-practices)
    - [Why This Approach?](#why-this-approach)
  - [Production Deployment](#production-deployment-1)
  - [Best Practices](#best-practices-1)

This section covers steps and best practices for deploying the site to production, including GitHub Actions and manual deployment.

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

# 2. Build for production (complete mode + link verification)
./utils/bin/jekyll-site build -c

# 3. Deploy (GitHub Pages or other hosting)
```

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

## Production Deployment

```bash
# 1. Run full validation
./utils/bin/check_site.sh

# 2. Build for production (complete mode + link verification)
./utils/bin/jekyll-site build -c

# 3. Deploy (GitHub Pages or other hosting)
```

## Best Practices

- Always validate the site before deploying
- Use complete mode for production builds
- Keep dependencies up to date
- Review and update documentation regularly
