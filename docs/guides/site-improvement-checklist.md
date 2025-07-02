# Site Improvement Checklist

*Last Updated: July 01, 2025*

## Overview
This document outlines a comprehensive plan to address warnings, improve site structure, and enhance the overall quality of the Jekyll website. It has been updated to reflect our current status and recent accomplishments.

---

## ✅ **Recently Completed (January 2025)**

### Site Reliability & Monitoring
- [x] **Comprehensive Site Reliability Monitoring System**
  - [x] Automated health checks and availability monitoring
  - [x] Post-commit deployment verification
  - [x] External link validation with performance monitoring
  - [x] Missing page tracking and management
  - [x] Email alerts with OAuth2 support
  - [x] GitHub Actions integration for CI/CD monitoring

### Documentation & Organization
- [x] **Complete Documentation Overhaul**
  - [x] Created comprehensive project overview (`docs/PROJECT_OVERVIEW.md`)
  - [x] Established documentation index (`docs/README.md`)
  - [x] Updated all monitoring guides and checklists
  - [x] Eliminated documentation overlap and redundancy
  - [x] Created task-based navigation system

### Image Management
- [x] **Image Path Management System**
  - [x] Case sensitivity detection and fixing
  - [x] Pre-commit integration
  - [x] File watcher for development
  - [x] Cross-platform compatibility (macOS/Linux)

---

## 🔧 **Critical Issues to Address (URGENT)**

### 1. **Broken Images on Live Website**
- [ ] **URGENT: Fix broken images on production site**
  - [ ] Run `utils/bin/fix_image_case_sensitivity.py` to detect issues
  - [ ] Verify all image paths are correct for production environment
  - [ ] Test site locally before pushing to production
  - [ ] Check for case sensitivity issues between macOS and Linux

### 2. **Liquid Syntax Warning**
- [ ] **Fix missing `endif` in footer template**
  - [ ] Check `html/_includes/_site/footer.html` for syntax errors
  - [ ] Review all Liquid templates for similar issues
  - [ ] Test site build after fixes

### 3. **Push Current Updates**
- [ ] **Deploy all recent changes to production**
  - [ ] Commit all recent monitoring and documentation updates
  - [ ] Test site health after deployment
  - [ ] Verify monitoring systems are working in production

---

## 🏗️ **Site Structure Improvements**

### 4. **Navigation and Linking**
- [x] **Breadcrumb navigation** - Implemented for better SEO and UX
- [x] **Sitemap generation** - Enabled with jekyll-sitemap plugin
- [x] **Robots.txt configuration** - Properly configured with sitemap reference
- [ ] **Add "Related Posts"** sections to blog posts
- [ ] **Review main navigation** - ensure all important pages are accessible

### 5. **Content Organization**
- [ ] **Review project pages** - ensure all have consistent structure
- [ ] **Add project categories/tags** for better organization
- [ ] **Create project index page** with all projects listed
- [ ] **Add search functionality** (optional enhancement)

### 6. **Blog Organization and Separation** *(Future Enhancement)*
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

---

## 🔍 **Quality Assurance**

### 7. **Automated Checks Enhancement**
- [x] **Image validation** - Integrated into pre-commit checks
- [x] **Broken link detection** - External link validation implemented
- [x] **Case sensitivity checks** - Image path validation
- [ ] **Add spell checking** for content
- [ ] **Add accessibility checks** (alt text for images, etc.)

### 8. **Performance Optimization**
- [ ] **Image optimization** - compress images without quality loss
- [ ] **CSS/JS minification** for production builds
- [ ] **Add lazy loading** for images
- [ ] **Consider CDN** for static assets

---

## 📁 **Orphaned Pages Management**

### 9. **Expected Orphans (No Action Needed)**
- [x] **Includes and Layouts** - These are expected to be "orphaned" - they're templates
- [x] **Drafts** - These are intentionally not linked until published
- [x] **Hidden pages** - Like `html/hidden/sitemap.md` - these serve specific purposes

### 10. **Orphans to Review**
- [ ] **`html/_drafts/2025-04-27-VSCode-Shell-Integration-Breaks-Virtual-Environments.md`** - Should this be published or deleted?
- [ ] **`html/_posts/2024-08-16-Testing-markdown-formatting-with-our-changes.md`** - Test post, consider removing
- [ ] **`html/_posts/2025-02-20-building-a-modern-jekyll-site.md`** - Check if this should be linked from somewhere
- [ ] **Project blog posts** - Ensure all published project posts are linked from their project pages

---

## 📚 **Documentation and Standards**

### 11. **Content Guidelines**
- [x] **Create post templates** - Available in `docs/templates/blog-templates.md`
- [x] **Document the build and deployment process** - Available in `docs/guides/site-operations.md`
- [ ] **Create content style guide** for consistent writing
- [ ] **Document image requirements** (sizes, formats, naming)

### 12. **Maintenance Procedures**
- [x] **Emergency procedures** - Available in `docs/guides/site-reliability-checklist.md`
- [x] **Regular content audits** - Automated via monitoring system
- [x] **Dependency updates** - Tracked in TODO.md
- [x] **Backup procedures** - Integrated with monitoring system

---

## 🚀 **Future Enhancements**

### 13. **Optional Improvements**
- [ ] **Add comments system** for blog posts
- [ ] **Add newsletter signup** functionality
- [ ] **Add social sharing** buttons
- [ ] **Add reading time** estimates for posts
- [ ] **Add table of contents** for long posts

### 14. **Content Marketing**
- [ ] **Automation Series Articles** (Planned)
  - [ ] Write 8-part technical series on our automation journey
  - [ ] Cover: mindset, image management, monitoring, testing, deployment
  - [ ] Include code examples and implementation details
  - [ ] Target technical audience for SEO and consulting opportunities

---

## **Priority Order:**

### **URGENT (Do First):**
1. Fix broken images on live website
2. Fix Liquid syntax errors  
3. Push current updates to production

### **High Priority:**
4. Site reliability monitor refactoring
5. Orphaned page review
6. Navigation improvements

### **Medium Priority:**
7. Content organization
8. Performance optimization
9. Future enhancements

### **Low Priority:**
10. Blog separation and organization
11. Advanced indexing and search features

---

## **Notes:**
- This checklist has been updated to reflect our current status and recent accomplishments
- Many items from the original checklist have been completed through our automation and monitoring work
- The site reliability monitoring system has significantly improved our ability to detect and prevent issues
- Documentation has been completely reorganized for better navigation and maintenance
- Focus should be on the urgent items first, then the high-priority technical improvements

---

*Last Updated: July 01, 2025* 