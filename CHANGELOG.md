# Changelog

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