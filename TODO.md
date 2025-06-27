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

## High Priority

### Content Creation & Management
- [ ] **Project Content Review & Updates**
  - [ ] Review and update all project content for accuracy and completeness
  - [ ] Complete project landing page content for all projects
  - [ ] Write Case Analytics introduction blog post
  - [ ] Create initial blog entries for each project before product release
  - [ ] Write ChatGPT Chat Log Export tutorial
  - [ ] Update venvutil usage examples and documentation
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
