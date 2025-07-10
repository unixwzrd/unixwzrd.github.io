# Changelog

## 2025-07-10: Documentation Refactor and Consistency Improvements

### Major Documentation Overhaul
- Refactored: Monolithic site operations guide into modular documentation structure
  - Split 702-line [`site-operations.md`](docs/guides/site-operations.md) into 8 focused guides for better maintainability
  - Created logical separation: environment, services, deployment, troubleshooting, maintenance, security, reference, monitoring
  - Each guide contains detailed, up-to-date instructions with cross-navigation
  - Preserved all original content with 100% migration verification
- Consolidated: Multiple checklists into single comprehensive checklist
  - Merged [`site-improvement-checklist.md`](docs/guides/checklist.md) and [`site-reliability-checklist.md`](docs/guides/checklist.md) into unified [`checklist.md`](docs/guides/checklist.md)
  - Eliminated duplicate content and conflicting task tracking
  - Organized tasks by priority: urgent, high, medium, low
  - Added maintenance schedules, troubleshooting procedures, and success metrics
- Streamlined: File naming convention for clarity and consistency
  - Renamed files to 2-3 word descriptions: [`checklist.md`](docs/guides/checklist.md), [`monitoring.md`](docs/guides/monitoring.md), [`github-actions.md`](docs/guides/github-actions.md), [`strategy.md`](docs/guides/strategy.md)
  - Removed verbose, sentence-like filenames for better navigation
  - Updated all cross-references and navigation links

### Consistency Improvements
- Removed: All emojis from section headers for professional consistency
- Standardized: Section naming across all documentation guides
- Eliminated: Date stamps from section headers for cleaner presentation
- Removed: Duplicate content (GitHub Pages deployment section now only in [`deployment.md`](docs/guides/deployment.md))
- Updated: Main site operations guide with comprehensive navigation to all sub-guides

### Documentation Structure
- Core Operations: [`environment-setup.md`](docs/guides/environment-setup.md), [`service-management.md`](docs/guides/service-management.md), [`deployment.md`](docs/guides/deployment.md), [`blog-pagination.md`](docs/guides/blog-pagination.md), [`troubleshooting.md`](docs/guides/troubleshooting.md), [`maintenance.md`](docs/guides/maintenance.md), [`security.md`](docs/guides/security.md), [`reference-utilities.md`](docs/guides/reference-utilities.md)
- Supporting Guides: [`monitoring.md`](docs/guides/monitoring.md), [`github-actions.md`](docs/guides/github-actions.md), [`strategy.md`](docs/guides/strategy.md), [`testing.md`](docs/guides/testing.md), [`checklist.md`](docs/guides/checklist.md)
- Archive: Preserved original [`site-operations-archive-2025-07-09.md`](docs/guides/site-operations-archive-2025-07-09.md) for reference
- Navigation: Each guide includes "Back to Site Operations Guide" link for easy navigation

### Benefits
- Better Organization: Logical separation of concerns makes information easier to find
- Improved Maintainability: Smaller, focused files are easier to update and maintain
- Reduced Confusion: Single checklist eliminates duplicate/conflicting task tracking
- Professional Presentation: Consistent naming and formatting throughout
- Complete Coverage: All original content preserved with enhanced organization

### Technical Details
- Verified: 100% content migration from original guide to new structure
- Tested: All cross-references and navigation links work correctly
- Maintained: All operational procedures and technical details preserved
- Enhanced: Added missing sections that were overlooked in initial migration
- Documented: Comprehensive audit trail of all changes and improvements

## 2025-07-09
- Unified blog listing: main blog now shows all posts (main + project).
- Added client-side JavaScript pagination for blog listings (configurable post count per page, smooth navigation, URL updates with ?page=).
- Pagination controls styled for dark backgrounds and accessibility.
- Excerpts now strip images and are truncated to a configurable word count.
- Blog and project blog post limits are configurable in [`_config.yml`](_config.yml) and can be overridden in page front matter.
- Blog list template and CSS updated for consistent, modern look.

## 20250701_03-rel: Redirect System Implementation & Script Modularization

### Major Accomplishments
- Implemented: Comprehensive redirect system to fix 404 errors
  - Fixed URL mismatches between site monitor config and actual Jekyll permalinks
  - Created static HTML redirect files at correct output paths
  - Implemented proper HTTP status codes (301/302) for SEO
  - Added `published: false` to redirect posts to prevent duplicate content
  - Aligned front matter dates with filenames for consistency
- Separated: Monolithic jekyll-service script into modular components
  - [`jekyll-site`](utils/bin/jekyll-site): Standalone Jekyll site management with OpenGraph refresh
  - [`file_watcher`](utils/bin/file_watcher): Standalone file system monitoring and change detection
  - [`site-service`](utils/bin/site-service): Future orchestration script (placeholder)
  - Added command-line options for flexible configuration
  - Improved process management and cleanup
- Enhanced: Site reliability monitoring with comprehensive testing
  - Updated site monitor configuration with corrected URLs
  - Fixed permalink mismatches in critical pages list
  - Implemented comprehensive testing for all components
  - Added health check mode for quick validation
  - Created test scripts for email functionality and crontab setup

### Technical Implementation
- Created: Email testing script ([`test_email.py`](utils/bin/test_email.py)) for notification system
- Created: Crontab setup script ([`setup_crontab.sh`](utils/bin/setup_crontab.sh)) for automated monitoring
- Updated: Site monitor configuration ([`site_monitor_config.json`](utils/etc/site_monitor_config.json)) with corrected URLs and improved structure
- Implemented: Proper process cleanup to prevent orphaned file watcher processes
- Enhanced: Error handling and logging across all monitoring components

### Documentation Updates
- Updated: [`worklog.md`](worklog.md) with comprehensive documentation of recent accomplishments
- Updated: [`TODO.md`](TODO.md) to reflect completed work and current priorities
- Organized: Project documentation structure for better maintainability
- Cleaned: Temporary files and deprecated content

### Benefits
- Fixed 404 Errors: All critical pages now accessible with proper redirects
- Modular Architecture: Easier maintenance and testing of individual components
- Automated Monitoring: Ready for email notifications and scheduled checks
- Better Documentation: Clear record of accomplishments and next steps
- Clean Codebase: Removed deprecated content and organized structure

## 20250127_01-rel: Site Reliability System Enhancement & Documentation

### Major Enhancements
- Enhanced: Site reliability monitor with external link validation and missing page tracking
- Added: Page management utilities and comprehensive documentation
- Improved: Email authentication with OAuth2 support
- Created: Project overview and status tracking documents

*See detailed documentation in [`PROJECT_OVERVIEW.md`](docs/PROJECT_OVERVIEW.md) and [`README.md`](docs/README.md)*

## 20250701_02-rel: Site Reliability Monitor Enhancements & Service Script Improvements

### Major Enhancements
- Enhanced: Site reliability monitor with improved output formatting and smart defaults
  - Summary Counts: Shows totals for pages, images, and links checked
  - Verbose Mode: `-V` flag shows all checked items in detail
  - Early Exit Logic: Stops checking if site is down to avoid timeouts
  - Smart 404 Handling: Properly handles 404 pages without false image errors
  - Final Summary: Warm fuzzy feeling when all checks pass
- Improved: Service management scripts with smart refresh control
  - New Flags: `-r|--refresh` and `-n|--no-refresh` for OG data control
  - Smart Defaults: Restart defaults to fast mode, start defaults to complete mode
  - Conflict Resolution: `-n` takes precedence when both flags specified
  - Shortened Flags: `-j|--jekyll` and `-w|--watcher` for service selection
- Added: Jekyll redirect system for URL changes
  - Redirect Support: Uses `jekyll-redirect-from` plugin for clean redirects
  - URL Integrity: Maintains old links while allowing URL structure changes
  - Automatic Sorting: Critical pages list automatically sorted for consistency

### Service Script Improvements
- Updated: [`jekyll-site`](utils/bin/jekyll-site) with enhanced flag handling and help
  - Added `-r|--refresh` flag for explicit OG data refresh
  - Improved conflict handling with warnings instead of exits
  - Better help messages with examples and default behaviors
  - Smart defaults: restart = fast mode, start = complete mode
- Updated: [`site-service`](utils/bin/site-service) with improved orchestration
  - Passes through refresh flags to jekyll-site
  - Added shortened service selection flags (`-j`, `-w`)
  - Enhanced help messages with comprehensive examples
  - TODO comment for future watcher config file approach
- Enhanced: Output formatting and user experience
  - Clear status indicators (success, failure, slow)
  - Informative messages about default behaviors
  - Conflict warnings that allow operation to continue

### Technical Improvements
- Fixed: Image checking logic to properly handle 404 pages
  - 404 pages with `alt="404"` no longer flagged as broken images
  - Separate logic for 404 pages vs other pages
- Added: Automatic sorting of critical pages in config
  - Pages sorted alphabetically when config loaded
  - Consistent ordering for easier debugging and maintenance
- Improved: Monitor output with summary counts
  - "X pages checked and passed" format
  - "X failed out of Y checked" for failures
  - Clean, professional output suitable for automation

### Documentation Updates
- Updated: [`PROJECT_OVERVIEW.md`](docs/PROJECT_OVERVIEW.md) with recent accomplishments
- Updated: [`site-operations.md`](docs/guides/site-operations.md) with new service management
- Updated: [`site-reliability-monitoring.md`](docs/guides/monitoring.md) with output examples
- Added: Comprehensive help messages to all service scripts

### Benefits
- Faster Development: Smart defaults reduce unnecessary OG refreshes
- Better UX: Clear output formatting and helpful messages
- Flexible Control: Explicit flags for when you need complete vs fast mode
- Maintainable: Sorted configs and improved error handling
- Professional: Clean output suitable for CI/CD and monitoring

## 20250626_08-rel: File Watcher System Testing and Verification

### Testing Implementation
- Added: Comprehensive test suite for file watcher system ([`test_file_watcher.py`](utils/bin/test_file_watcher.py))
  - Tests file watcher startup and shutdown
  - Tests dynamic watcher script reloading
  - Tests watcher script execution
  - Tests Jekyll service integration
  - Tests error handling with broken scripts
- Added: Quick test script for fast verification ([`quick_test.py`](utils/bin/quick_test.py))
  - Basic functionality tests for rapid feedback
  - Suitable for CI/CD pipelines and development workflow
- Added: Comprehensive testing documentation ([`testing.md`](docs/guides/testing.md))
  - Manual testing procedures
  - Automated test suite usage
  - Troubleshooting guide
  - Success/failure indicators

## 20250701_01-rel: Site Reliability Monitoring System

### New Features
- Added: Comprehensive Site Reliability Monitoring System
  - Automated Health Checks: Monitors site availability, critical pages, response times, and images
  - Post-Commit Verification: Automatically checks site after deployments with configurable delay
  - Periodic Monitoring: Scheduled health checks with email alerts for issues
  - Email Alerting: Configurable SMTP alerts for deployment success/failure and ongoing issues
- Added: Site reliability monitor script ([`site_reliability_monitor.py`](utils/bin/site_reliability_monitor.py))
  - Three monitoring modes: health, post-commit, periodic
  - Configurable critical pages and response time thresholds
  - Custom health check support
  - Comprehensive logging to file and console
- Added: Automation scripts for monitoring integration
  - Post-commit monitor ([`post_commit_monitor.sh`](utils/bin/post_commit_monitor.sh))
  - Periodic monitor ([`periodic_monitor.sh`](utils/bin/periodic_monitor.sh))
  - Setup script ([`setup_site_monitoring.sh`](utils/bin/setup_site_monitoring.sh))
- Added: Configuration system ([`site_monitor_config.json`](utils/etc/site_monitor_config.json))
  - Email settings for Gmail and other SMTP providers
  - Configurable health check parameters
  - Deployment timing settings
- Added: Comprehensive documentation ([`monitoring.md`](docs/guides/monitoring.md))
  - Quick start guide
  - Configuration instructions
  - Integration with git hooks and CI/CD
  - Troubleshooting guide

### Benefits
- **Proactive Issue Detection**: Catches problems before users report them
- **Automated Verification**: Eliminates need for manual page-by-page checking
- **Performance Monitoring**: Tracks response times and identifies degradation
- **Deployment Confidence**: Verifies deployments work correctly before users notice issues
- **Immediate Alerts**: Email notifications with detailed issue descriptions

### Integration
- COMPATIBLE: Works alongside existing pre-commit checks and file watcher system
- FLEXIBLE: Supports git hooks, CI/CD pipelines, and cron scheduling
- EXTENSIBLE: Custom health check support for specific needs
- CONFIGURABLE: Adjustable thresholds and monitoring parameters

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


