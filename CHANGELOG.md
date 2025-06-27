# Changelog

## 20250626_08-rel: File Watcher System Testing and Verification

### Testing Implementation
- ADDED: Comprehensive test suite for file watcher system (`utils/bin/test_file_watcher.py`)
  - Tests file watcher startup and shutdown
  - Tests dynamic watcher script reloading
  - Tests watcher script execution
  - Tests Jekyll service integration
  - Tests error handling with broken scripts
- ADDED: Quick test script for fast verification (`utils/bin/quick_test.py`)
  - Basic functionality tests for rapid feedback
  - Suitable for CI/CD pipelines and development workflow
- ADDED: Comprehensive testing documentation (`docs/guides/testing.md`)
  - Manual testing procedures
  - Automated test suite usage
  - Troubleshooting guide
  - Success/failure indicators

### Verification Results
- VERIFIED: File watcher system works correctly in all tested scenarios
- CONFIRMED: Jekyll service integration with `-j` and `-w` flags functions properly
- TESTED: Dynamic script loading detects new watcher scripts automatically
- VALIDATED: Image path fixer watcher processes files correctly in real-time
- CONFIRMED: Error handling prevents watcher crashes from broken scripts

### Documentation Updates
- UPDATED: Testing procedures and verification methods
- DOCUMENTED: Manual testing steps for ongoing development
- PROVIDED: Troubleshooting guide for common issues
- ESTABLISHED: Testing standards for future development

## 20250626_07-rel: File Watcher System Implementation

### New Features
- ADDED: General file watcher system for automatic script execution on file changes
  - Main watcher: `utils/bin/file_watcher.py`
  - Watcher scripts directory: `utils/bin/watchers/`
  - Automatically runs scripts when files in `html/` directory change
- ADDED: Image path fixer watcher script (`utils/bin/watchers/image_path_fixer.py`)
  - Automatically fixes image paths in Markdown files when they are modified
  - Runs during development to catch image path issues in real-time
- ADDED: Comprehensive documentation for the watcher system
  - README in `utils/bin/watchers/` explaining how to add new watchers
  - Updated operations guide with file watcher system documentation
- INTEGRATED: File watcher with Jekyll service script
  - File watcher starts/stops automatically with Jekyll server
  - Added `-W` and `-J` flags for selective service control
  - Proper PID management for both services

### Technical Details
- USED: watchdog library for file system monitoring
- IMPLEMENTED: Debouncing to prevent multiple rapid executions
- PROVIDED: Environment variables to watcher scripts (WATCHER_FILE, WATCHER_EVENT, WATCHER_NAME)
- SUPPORTED: Easy addition of new watchers by dropping Python scripts in watchers directory
- ENHANCED: Jekyll service script with selective service management

## 20250626_06-rel: Incremental Image Path Check & Pre-commit Performance Planning

### Enhancements
- IMPROVED: Image path check script now uses incremental mode with timestamp tracking
  - Only scans Markdown files modified since the last check, greatly improving pre-commit speed
  - Timestamp file stored in utils/etc/.image_paths_last_check
  - Full scan can be forced with --full option
- PLANNED: Added TODO for performance review and optimization of all check scripts and pre-commit hooks
  
## 20250626_05-rel: Image Path Fix for VenvUtil Blog Post

### Bug Fixes
- FIXED: Image display issue in VenvUtil Summer Update blog post
  - Converted Markdown image syntax inside HTML div to proper HTML img tag
  - Changed `![Order From Chaos](/projects/venvutil/images/Ordering_Venvs.png)` to `<img src="/projects/venvutil/images/Ordering_Venvs.png" alt="Order From Chaos">`
  - Image now displays correctly instead of appearing briefly and disappearing

### Technical Details
- USED: `utils/bin/fix_image_paths.py` script to automatically detect and fix the issue
- CONFIRMED: Site builds successfully with the corrected image syntax
- VERIFIED: Image path is correct and image file exists in expected location

## 20250626_04-rel: Service Script Improvements and Sass Reversion

### Critical Fixes
- FIXED: Jekyll service script process management and restart functionality
- REVERTED: Failed Sass migration attempt back to working `@import` and `adjust-color()` syntax
- FIXED: Service script now properly handles missing PID files and port conflicts

### Service Script Improvements
- IMPROVED: `utils/bin/jekyll-service` with better process management
- ADDED: Port conflict detection and automatic cleanup of existing processes
- ADDED: Graceful handling of missing PID files during restart operations
- ENHANCED: Process termination with both SIGTERM and SIGKILL fallback
- VERIFIED: Service script now works reliably for start/stop/restart operations

### Sass/SCSS Status
- REVERTED: All SCSS files back to working `@import` syntax
- MAINTAINED: `adjust-color()` functions (deprecation warnings accepted for now)
- DECIDED: To address Sass modernization as separate planned project
- CONFIRMED: Site builds and serves correctly with current Sass setup

### Technical Details
- UPDATED: Service script to check for port conflicts before starting
- IMPROVED: Error handling for process management edge cases
- MAINTAINED: Working site functionality while planning future Sass improvements
- DOCUMENTED: Decision to accept deprecation warnings temporarily

## 20250626_03-rel: Sass Migration Attempt (REVERTED)

### Note: This migration was attempted but reverted due to compatibility issues
- ATTEMPTED: Migration to Dart Sass module system with `@use "sass:color"`
- ENCOUNTERED: Jekyll Sass converter compatibility issues with Dart Sass modules
- REVERTED: Back to working `@import` and `adjust-color()` syntax
- DECIDED: To address Sass modernization as separate planned project

## 20250626_02-home-blog-improvements: Home Page and Blog Index Enhancements

### Improvements
- Home page now uses index.md for proper Markdown rendering and formatting
- Added 'Latest Updates' section to home page with 7 most recent blog post headlines (no excerpts)
- Added 'View all blog posts' link to consolidated blog index at the bottom of the home page
- Blog index (/blog/) now lists all posts from all sources with excerpts
- Improved navigation and user experience for blog discovery

### Fixes
- Resolved issues with Markdown not rendering on home page
- Ensured only one root index file exists for correct Jekyll processing 

## 20250626_01-rel: Critical Build Fixes and Image Path Corrections

### Critical Fixes
- FIXED: Missing jekyll-seo-tag plugin causing build failures
- FIXED: Image path reference in Case-Analytics related post
  - Corrected `/assets/images/boy-robot-road-unizwzrd-mia-watching.png` to `/projects/Case-Analytics/images/boy-robot-road-unizwzrd-mia-watching.png`

### Build System
- ADDED: jekyll-seo-tag plugin to Gemfile for proper SEO functionality
- VERIFIED: Site builds successfully without critical errors
- CONFIRMED: All external links are functioning (social media rate limiting is expected)

### Documentation
- UPDATED: Pre-commit checklist with resolved issues
- DOCUMENTED: False positive Liquid syntax warning in footer template

## 20250320_01-rel: Link Checker Improvements and Blog Fixes

### Bug Fixes
- FIXED: Link checker to properly handle URL-encoded characters like %20 (spaces)
- FIXED: Blog post date issue where future-dated posts weren't showing correctly
- FIXED: Image display in project tables to avoid cropping

### Improvements
- IMPROVED: Project image styling with consistent rounded corners and hover effects
- IMPROVED: Project link organization for both public and private repositories
- UPDATED: Ensured all projects link to project blog (both title and image)

## 20240223_02-rel: Blog Layout and Template Fixes

### Bug Fixes
- FIXED: Blog post layout issue where titles and dates weren't displaying correctly
- FIXED: Post layout template now correctly uses page variables instead of post variables
- FIXED: Join Us include file formatting issues
- FIXED: Liquid syntax in footer template
- FIXED: Dependabot URL gem vulnerability

### Documentation
- UPDATED: Documentation to reflect latest changes
- IMPROVED: Worklog with details about template fixes

## 20240223_01-rel: Unified Blog System and Pagination

### Blog System Improvements
- FIXED: Blog display on home page with proper pagination (5 posts per page)
- MOVED: Latest Updates section to home layout template
- ADDED: Proper pagination navigation
- FIXED: Project blog integration
- UPDATED: Templates for consistent blog display across site

## 20240220_01-rel: Major Site Structure and Process Updates

### Blog System Improvements
- NEW: Unified blog list component for consistent display across site
- IMPROVED: Blog styling and organization
  - Consistent post date and excerpt formatting
  - Unified "Read More" link styling
  - Better heading hierarchy

### Project Structure
- NEW: Standardized project directory structure
  - Added _drafts and _posts directories for each project
  - Created template system for new posts
  - Improved project asset management
- IMPROVED: Project integration and navigation

### Security and Build Process
- SECURITY: Updated nokogiri from 1.16.7 to 1.18.3
- NEW: Comprehensive pre-commit check system
  - Permalink validation
  - Front matter checking
  - Link validation
  - Build verification
- IMPROVED: Jekyll service management and build process

### Documentation
- NEW: Comprehensive documentation in docs/ directory
  - Tool documentation
  - Workflow guides
  - Templates
  - Maintenance procedures
- IMPROVED: Development process documentation

### Breaking Changes
- Project blog posts must use new directory structure
- All commits must pass pre-commit checks
- Stricter permalink and front matter requirements

### Migration Required
- Update existing project posts to new structure
- Set up pre-commit hooks
- Update permalinks to meet new requirements
- Add required front matter to all pages


