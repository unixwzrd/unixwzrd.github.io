# TODO List

## Completed
- [x] Fix blog post layout to correctly display titles and dates
- [x] Fix Liquid syntax issues in footer template
- [x] Correct formatting in join_us.html include
- [x] Implement proper pagination on home page
- [x] Create unified blog styling
- [x] Fix project blog integration
- [x] Update documentation for blog system
- [x] Fix link checker to handle URL-encoded characters
- [x] Improve project image display and styling
- [x] Update pre-commit tool documentation
- [x] Home page now uses index.md for proper Markdown rendering and formatting
- [x] Added 'Latest Updates' section to home page with 7 most recent blog post headlines (no excerpts)
- [x] Added 'View all blog posts' link to consolidated blog index at the bottom of the home page
- [x] Blog index (/blog/) now lists all posts from all sources with excerpts
- [x] Improved navigation and user experience for blog discovery
- [x] Resolved issues with Markdown not rendering on home page
- [x] Ensured only one root index file exists for correct Jekyll processing
- [x] Create unified blog list component
- [x] Standardize project directory structure
- [x] Add pre-commit checks
- [x] Update nokogiri for security
- [x] Create documentation structure
- [x] **Service Script Improvements**
  - [x] Enhanced Jekyll service script with better process management
  - [x] Added port conflict detection and automatic cleanup
  - [x] Fixed restart functionality with missing PID file handling
  - [x] Improved error handling for process termination
- [x] **Image Path Management**
  - [x] Review and test image path fixer script (utils/bin/fix_image_paths.py)
  - [x] Fixed image display issue in VenvUtil Summer Update blog post
  - [x] Fixed 3 additional image path issues across the site (localhost URLs to absolute paths)
  - [x] Verified all image links are working correctly across the site
  - [x] Integrate image fixer script into pre-commit workflow
  - [x] Set up file watcher (watchdog) to run image fixer script on Markdown changes during local dev
- [x] **Google Analytics Setup & Optimization**
  - [x] Create missing google-analytics.html include file with proper GA4 tracking code
  - [x] Verify GA4 measurement ID (G-QZSHSBP292) is correctly configured
  - [x] Add enhanced tracking for blog posts, project pages, and user interactions
- [x] **File Watcher System Implementation & Testing**
  - [x] Implemented comprehensive file watcher system with dynamic script loading
  - [x] Integrated file watcher with Jekyll service script
  - [x] Created comprehensive test suite for file watcher system
  - [x] Verified all functionality works correctly in real-world scenarios
  - [x] Documented testing procedures and troubleshooting guides
- [x] **SEO Optimization (Partial)**
  - [x] Add structured data (JSON-LD) for blog posts and projects
  - [x] Implement breadcrumb navigation for better SEO
- [x] **Content & Documentation**
  - [x] Create project blog templates
  - [x] Complete all tool documentation
  - [x] Create workflow guides
  - [x] Write contribution guidelines
  - [x] Document release process
  - [x] Update README files
- [x] **Script Architecture Refactoring (COMPLETED)**
  - [x] Decoupled monolithic jekyll-service into separate components
  - [x] Created jekyll-site script for Jekyll management
  - [x] Created file_watcher script for file monitoring
  - [x] Created site-service orchestration script
  - [x] All scripts tested and working correctly
  - [x] Improved process management and cleanup
  - [x] Enhanced error handling and logging
- [x] **Site Reliability Monitor Enhancements**
  - [x] Improved logging message alignment using f-strings
  - [x] Fixed 404 error reporting for existing pages
  - [x] Enhanced URL checking logic and error handling
  - [x] Added better process cleanup for file watchers
- [x] **Monitoring Infrastructure Setup**
  - [x] Created GitHub Actions workflow for site health checks
  - [x] Added comprehensive monitoring documentation
  - [x] Created utility scripts for testing and automation
  - [x] Set up monitoring strategy and reliability checklists

## High Priority

### Site Reliability & Monitoring (COMPLETED ✅)
- [x] **Site Reliability Monitoring System**
  - [x] Implemented comprehensive site monitoring with `site_reliability_monitor.py`
  - [x] Added health checks for critical pages, images, and external links
  - [x] Created periodic monitoring with configurable intervals
  - [x] Implemented detailed logging with emoji-based status indicators
  - [x] Added response time monitoring and performance tracking
  - [x] Created external link monitoring with failure tracking

- [x] **Redirect System Implementation**
  - [x] Fixed 404 errors caused by URL mismatches between config and actual permalinks
  - [x] Implemented Jekyll redirect system using static HTML files
  - [x] Created redirect generator plugin for automated redirect creation
  - [x] Added proper front matter handling for redirect posts
  - [x] Set `published: false` on redirect posts to prevent duplicate content
  - [x] Aligned front matter dates with filenames for consistency

- [x] **Script Separation and Modularization**
  - [x] Separated combined `jekyll-service` script into standalone components
  - [x] Created `jekyll-site` for Jekyll management with OpenGraph refresh
  - [x] Created `file_watcher` for file system monitoring
  - [x] Created `site-service` orchestration script (placeholder)
  - [x] Added command-line options for flexible configuration
  - [x] Improved process management and cleanup

### Email & Automation Implementation (NEXT PHASE)
- [ ] **Email Alert System**
  - [ ] Configure email credentials in `utils/etc/site_monitor_config.json`
  - [ ] Test email functionality with `utils/bin/test_email.py`
  - [ ] Implement email notifications for site monitoring alerts
  - [ ] Create email templates for different alert types
  - [ ] Add email rate limiting to prevent spam
- [ ] **Cron Job Automation**
  - [ ] Set up automated site monitoring via `utils/bin/setup_crontab.sh`
  - [ ] Configure periodic health checks every 6 hours
  - [ ] Implement automated reporting and log rotation
  - [ ] Create monitoring dashboard
  - [ ] Set up alert escalation procedures

### Documentation & Cleanup (CURRENT)
- [ ] **Documentation Updates**
  - [x] Updated Worklog.md with current accomplishments
  - [ ] Update project documentation with current status
  - [ ] Clean up temporary files and deprecated scripts
  - [ ] Organize documentation structure
  - [ ] Update TODO.md with completed items
- [ ] **Code Cleanup**
  - [ ] Remove deprecated scripts and temporary files
  - [ ] Organize utility scripts by function
  - [ ] Update script documentation
  - [ ] Clean up configuration files
- [ ] **Email Alert System**
  - [ ] Implement email notifications for site monitoring alerts
  - [ ] Configure SMTP settings for reliable delivery
  - [ ] Create email templates for different alert types
  - [ ] Add email rate limiting to prevent spam
  - [ ] Test email delivery in development environment
- [ ] **Cron Job Automation**
  - [ ] Set up automated site monitoring via cron
  - [ ] Configure periodic health checks
  - [ ] Implement automated reporting
  - [ ] Create monitoring dashboard
  - [ ] Set up alert escalation procedures

### Content Creation & Management
- [ ] **Project Content Review & Updates**
  - [ ] Review and update all project content for accuracy and completeness
  - [ ] Complete project landing page content for all projects
  - [ ] Write Case Analytics introduction blog post
  - [ ] Create initial blog entries for each project before product release
  - [ ] Write ChatGPT Chat Log Export tutorial
  - [ ] Update venvutil usage examples and documentation
- [ ] **Automation Series Articles** (Future Content)
  - [ ] Write 8-part technical series on our automation journey
  - [ ] Cover: mindset, image management, monitoring, testing, deployment
  - [ ] Include code examples and implementation details
  - [ ] Target technical audience for SEO and consulting opportunities
- [ ] **Permalink & Front Matter Audit**
  - [ ] Update all permalinks to meet new requirements
  - [ ] Add required front matter to all pages
  - [ ] Verify all permalinks are working correctly
- [ ] **SEO Optimization & Enhancement**
  - [ ] Review and enhance meta descriptions for all pages
  - [ ] Optimize page titles and headings for better search visibility
  - [ ] Add Open Graph and Twitter Card meta tags optimization
  - [ ] Set up Google Search Console integration and monitoring

### Technical Infrastructure
- [ ] **Sass Modernization (Planned Project)**
  - [ ] Research Jekyll Sass converter compatibility with Dart Sass modules
  - [ ] Plan migration strategy for `@import` to `@use` syntax
  - [ ] Test Dart Sass module system with Jekyll in isolated environment
  - [ ] Create rollback plan before attempting migration
  - [ ] Address deprecation warnings systematically
- [ ] **Image Path Management**
  - [ ] Overhaul image management and standardize image handling for posts and projects
  - [ ] Verify all image links are working correctly across the site

### Launch Preparation
- [ ] **Social Media & Marketing**
  - [ ] Develop social media strategy
  - [ ] Plan content calendar
  - [ ] Prepare social media announcements for site launch
- [ ] **Pre-commit Setup**
  - [ ] Set up pre-commit hooks on all development machines

### Site Reliability Monitor Refactoring
- [ ] **Refactor `site_reliability_monitor.py` into smaller modules**
  - Current file is ~1000 LOC and too monolithic
  - Break into logical modules:
    - `monitor_core.py` - Main monitoring logic
    - `health_checks.py` - Health check implementations
    - `link_validator.py` - External/internal link checking
    - `email_alerts.py` - Email notification system
    - `page_tracker.py` - Missing page tracking
    - `config_manager.py` - Configuration management
  - Maintain backward compatibility
  - Update all documentation and scripts

### File Watcher System Enhancement
- [ ] **Make file watcher configurable and centralized**
  - Create single configurable watcher instead of individual file watchers

### Excerpt Processing Issues
- [ ] **Fix image tags breaking excerpts in blog listings**
  - Current `strip_images` filter enhanced to handle links but image tags still causing issues
  - Need to investigate why image tags are still appearing in excerpts despite filter
  - May need to adjust filter order or add additional processing steps
  - Add configuration file for watcher events and scripts
  - Support multiple event types (create, update, delete) per script
  - Ensure only one watcher process runs at a time
  - Make it easy to add new capabilities without restarting
  - Support dynamic script loading from watchers directory

## Medium Priority

### User Experience & Functionality
- [ ] **Search & Navigation**
  - [ ] Add search functionality
  - [ ] Create tag-based navigation for blog posts
  - [ ] Implement search functionality across all blogs
- [ ] **Mobile & Responsiveness**
  - [ ] Improve mobile responsiveness
  - [ ] Optimize image loading and compression

### Content Organization (Future)
- [ ] **Blog Structure Enhancement**
  - [ ] Build tag-based index page for all blog posts
  - [ ] Create chronological index of all posts
  - [ ] Add category-based filtering and navigation
  - [ ] Create "Recent Posts" sections for each blog type
- [ ] **Blog Separation (Long-term)**
  - [ ] Create separate technical blog for AI/ML/development content
  - [ ] Create separate personal blog for Parental Alienation content
  - [ ] Update navigation to reflect separate blog sections
  - [ ] Ensure proper audience targeting for each blog

### Technical Performance
- [ ] **Build & Performance Optimization**
  - [ ] Improve build performance
  - [ ] Review and optimize performance of all check scripts and pre-commit hooks
  - [ ] Audit runtime of each check script
  - [ ] Identify and refactor any slow operations
  - [ ] Ensure pre-commit workflow is as fast as possible for developer experience

## Periodic Tasks & Automation

### Monthly Tasks
- [ ] **Security & Dependency Updates**
  - [ ] Check for Ruby gem updates (bundle outdated)
  - [ ] Check for Python package updates (pip list --outdated)
  - [ ] Review and update security dependencies
  - [ ] Test site functionality after updates
- [ ] **Content & Link Health**
  - [ ] Run full link checker across entire site
  - [ ] Check for broken image links
  - [ ] Verify all external links are still working
  - [ ] Review and update outdated content references
- [ ] **Performance Monitoring**
  - [ ] Run performance tests on key pages
  - [ ] Check Google PageSpeed Insights scores
  - [ ] Review and optimize slow-loading resources
  - [ ] Monitor build times and optimize if needed

### Quarterly Tasks
- [ ] **SEO & Analytics Review**
  - [ ] Review Google Analytics data and trends
  - [ ] Check Google Search Console for issues
  - [ ] Review and update meta descriptions
  - [ ] Analyze search performance and optimize
- [ ] **Content Audit**
  - [ ] Review all blog posts for accuracy and relevance
  - [ ] Update outdated project information
  - [ ] Check for broken internal links
  - [ ] Review and update project status and links
- [ ] **Technical Debt Assessment**
  - [ ] Review Jekyll deprecation warnings
  - [ ] Check for Sass/SCSS modernization opportunities
  - [ ] Review and update documentation
  - [ ] Assess build system performance

### Automation Opportunities
- [ ] **Automated Testing & Validation**
  - [ ] Create automated test suite for site functionality
  - [ ] Set up automated link checking (weekly)
  - [ ] Automate image path validation
  - [ ] Create automated build and deployment testing
- [ ] **Automated Monitoring**
  - [ ] Set up automated performance monitoring
  - [ ] Create automated security scanning
  - [ ] Implement automated dependency update checking
  - [ ] Set up automated backup and recovery testing
- [ ] **Automated Content Management**
  - [ ] Create automated content freshness checking
  - [ ] Implement automated social media posting
  - [ ] Set up automated SEO monitoring and alerts
  - [ ] Create automated content backup and versioning
- [ ] **Automated Maintenance**
  - [ ] Create automated monthly task runner
  - [ ] Implement automated quarterly audit scripts
  - [ ] Set up automated reporting for site health
  - [ ] Create automated rollback procedures for failed updates

### Scripts to Create
- [ ] **Monthly Maintenance Script**
  - [ ] `utils/bin/monthly_maintenance.py` - Run all monthly tasks
  - [ ] `utils/bin/quarterly_audit.py` - Run all quarterly tasks
  - [ ] `utils/bin/automated_testing.py` - Run comprehensive test suite
  - [ ] `utils/bin/performance_monitor.py` - Monitor and report performance
- [ ] **Automation Infrastructure**
  - [ ] `utils/bin/automated_link_checker.py` - Automated link validation
  - [ ] `utils/bin/content_freshness_checker.py` - Check content age and relevance
  - [ ] `utils/bin/seo_monitor.py` - Monitor SEO metrics and alert on issues
  - [ ] `utils/bin/dependency_updater.py` - Automated dependency management

## Low Priority

### User Interface Enhancements
- [ ] **Visual & Interactive Features**
  - [ ] Implement dark mode toggle
  - [ ] Add comment system for blog posts
  - [ ] Create author profile pages
  - [ ] Add related posts feature

### Technical Debt & Maintenance
- [ ] **System Monitoring & Testing**
  - [ ] Add automated testing for templates
  - [ ] Review and fix Jekyll server deprecation warnings in logs
  - [ ] **Sass Deprecation Warnings** (Accepted temporarily)
    - [ ] Monitor for Jekyll Sass converter updates
    - [ ] Plan systematic migration when compatibility improves
    - [ ] Document current warnings for future reference

### Future Enhancements
- [ ] **Automation & Process Improvements**
  - [ ] Implement automated post generation
  - [ ] Add category management system
  - [ ] Add tag support
  - [ ] Enhance search capabilities
  - [ ] Add automated testing
  - [ ] Implement performance monitoring
  - [ ] Add deployment checks
  - [ ] Automate release notes generation
  - [ ] Enhance build validation
  - [ ] Improve error handling
  - [ ] Implement continuous deployment

## External Link Monitoring Improvements

### 🤖 Robots.txt Bypass Strategies
- **User-Agent Rotation**: Implement rotating user agents to bypass robots.txt restrictions
  - Googlebot, Bingbot, curl, custom user agents
  - Respectful delays between requests (2-5 seconds)
- **Respectful Bypass**: Only bypass when failure count exceeds threshold
  - Check robots.txt first, then decide if bypass is needed
  - Use different IPs if available
- **Cloudflare Detection**: Handle Cloudflare bot detection
  - Implement browser-like headers
  - Consider using selenium or playwright for problematic sites
- **Alternative Checking Methods**:
  - DNS resolution (ping the domain)
  - Port scanning (check if port 80/443 is open)
  - Third-party services (UptimeRobot API, etc.)

### 🚫 Exclude List Feature
- **Configurable exclude list**: Allow excluding certain sites from external link checks
- **Silent failures**: Don't count excluded sites in failure totals
- **Manual verification mode**: Flag excluded sites for manual review
- **Separate reporting**: Distinguish between excluded vs genuinely down sites

### 📊 Enhanced Threshold Management
- **Double threshold**: When failure count reaches 2x the critical threshold, consider auto-exclusion
- **No-checklist**: Sites that consistently fail get moved to manual review list
- **Ignore list**: Configurable list of sites to permanently exclude
- **Smart escalation**:
  - Regular failure → "INVESTIGATE!"
  - Critical threshold → "🚨 CRITICAL: INVESTIGATE IMMEDIATELY!"
  - Double threshold → Consider auto-exclusion

### 🔧 Technical Improvements
- **Config validation**: Ensure all required config fields exist
- **Error recovery**: Handle missing config gracefully
- **Performance optimization**: Parallel link checking with rate limiting
- **Historical analysis**: Track patterns over time to identify problematic sites

### 📝 Monitoring Strategy
1. **Initial check**: Standard HTTP request with proper user agent
2. **Robots.txt check**: If site blocks us, check robots.txt
3. **Bypass attempt**: If failure count > threshold, try bypass methods
4. **Escalation**: Increase urgency based on failure count
5. **Auto-exclusion**: Consider excluding sites that consistently fail
6. **Manual review**: Flag sites for human investigation

## Current Status
- ✅ Basic external link monitoring implemented
- ✅ Source page tracking working
- ✅ Configurable thresholds added
- ✅ Meaningful error messages restored
- ✅ Critical investigation alerts working
- 🔄 Robots.txt bypass strategies (TODO)
- 🔄 Exclude list feature (TODO)
- 🔄 Enhanced threshold management (TODO)
