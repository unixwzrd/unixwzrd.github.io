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
- [x] **Service Script Improvements**
  - [x] Enhanced Jekyll service script with better process management
  - [x] Added port conflict detection and automatic cleanup
  - [x] Fixed restart functionality with missing PID file handling
  - [x] Improved error handling for process termination

## High Priority
- [ ] **Sass Modernization (Planned Project)**
  - [ ] Research Jekyll Sass converter compatibility with Dart Sass modules
  - [ ] Plan migration strategy for `@import` to `@use` syntax
  - [ ] Test Dart Sass module system with Jekyll in isolated environment
  - [ ] Create rollback plan before attempting migration
  - [ ] Address deprecation warnings systematically
- [ ] **Image Path Management**
  - [ ] Review and test image path fixer script (utils/bin/fix_image_paths.py)
  - [ ] Integrate image fixer script into pre-commit workflow
  - [ ] Set up file watcher (watchdog) to run image fixer script on Markdown changes during local dev
  - [ ] Overhaul image management and standardize image handling for posts and projects
  - [ ] Verify all image links are working correctly across the site
- [ ] Review and update all project content
- [ ] Create content for project landing pages
- [ ] Write blog entries for each project before product release
- [ ] Prepare social media announcements for site launch
- [ ] **Google Analytics Setup & Optimization**
  - [x] Create missing google-analytics.html include file with proper GA4 tracking code
  - [ ] Verify GA4 measurement ID (G-QZSHSBP292) is correctly configured
  - [ ] Add enhanced tracking for blog posts, project pages, and user interactions
  - [ ] Set up conversion tracking for key user actions (contact form, resource downloads)
- [ ] **SEO Optimization & Enhancement**
  - [ ] Review and enhance meta descriptions for all pages
  - [x] Add structured data (JSON-LD) for blog posts and projects
  - [ ] Optimize page titles and headings for better search visibility
  - [x] Implement breadcrumb navigation for better SEO
  - [ ] Add Open Graph and Twitter Card meta tags optimization
  - [ ] Set up Google Search Console integration and monitoring

## Medium Priority
- [ ] Improve mobile responsiveness
- [ ] Add search functionality
- [ ] Enhance SEO metadata
- [ ] Create tag-based navigation for blog posts

## Low Priority
- [ ] Implement dark mode toggle
- [ ] Add comment system for blog posts
- [ ] Create author profile pages
- [ ] Add related posts feature

## Content Organization (Future)
- [ ] **Split main blog into separate blogs:**
  - [ ] Create separate technical blog for AI/ML/development content
  - [ ] Create separate personal blog for Parental Alienation content
  - [ ] Update navigation to reflect separate blog sections
  - [ ] Ensure proper audience targeting for each blog
- [ ] **Create blog index and collection pages:**
  - [ ] Build tag-based index page for all blog posts
  - [ ] Create chronological index of all posts
  - [ ] Add category-based filtering and navigation
  - [ ] Implement search functionality across all blogs
  - [ ] Create "Recent Posts" sections for each blog type

## Technical Debt
- [ ] Optimize image loading and compression
- [ ] Improve build performance
- [ ] Add automated testing for templates
- [ ] Review and fix Jekyll server deprecation warnings in logs
- [ ] **Sass Deprecation Warnings** (Accepted temporarily)
  - [ ] Monitor for Jekyll Sass converter updates
  - [ ] Plan systematic migration when compatibility improves
  - [ ] Document current warnings for future reference

## Content Creation
- [ ] Write Case Analytics introduction blog post
- [ ] Create TorchDevice documentation
- [ ] Update venvutil usage examples
- [ ] Write ChatGPT Chat Log Export tutorial

## Immediate Tasks
- [ ] Complete project landing page content
- [ ] Create initial blog entries for each project
- [ ] Set up pre-commit hooks on all development machines
- [ ] Update all permalinks to meet new requirements
- [ ] Add required front matter to all pages

## Content Tasks
- [ ] Write project introductions
- [x] Create project blog templates
- [ ] Develop social media strategy
- [ ] Plan content calendar
- [ ] Create project documentation

## Documentation
- [ ] Complete all tool documentation
- [ ] Create workflow guides
- [ ] Write contribution guidelines
- [ ] Document release process
- [ ] Update README files

## Future Enhancements
- [ ] Implement automated post generation
- [ ] Add category management system
- [ ] Add tag support
- [ ] Enhance search capabilities
- [ ] Add automated testing
- [ ] Implement performance monitoring
- [ ] Add deployment checks

## Process Improvements
- [ ] Automate release notes generation
- [ ] Enhance build validation
- [ ] Improve error handling
- [ ] Add automated testing
- [ ] Implement continuous deployment

## Completed Tasks
- [x] Create unified blog list component
- [x] Standardize project directory structure
- [x] Add pre-commit checks
- [x] Update nokogiri for security
- [x] Create documentation structure 