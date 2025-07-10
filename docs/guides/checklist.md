# Site Improvement Checklist

*Last Updated: July 01, 2025*

## Overview
This document outlines a comprehensive plan to address warnings, improve site structure, and enhance the overall quality of the Jekyll website. It consolidates both site improvements and reliability monitoring tasks into one unified checklist.

---

## Completed Tasks

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

### Core System Setup
- [x] **Site Reliability Monitor**: Created comprehensive monitoring system
- [x] **Email Configuration**: Added OAuth2 and traditional SMTP support
- [x] **Log Management**: Set up proper log directory (`utils/log/`)
- [x] **Configuration Files**: Created JSON configs for all components
- [x] **External Link Validation**: Added comprehensive external link checking
- [x] **Image Path Validation**: Enhanced with case sensitivity checking
- [x] **Auto-Discovery**: Pages automatically discovered and added to monitoring
- [x] **Page Management**: Smart tracking and removal of missing pages with alerts

### Scheduled Tasks Framework
- [x] **Scheduled Tasks Manager**: Created framework for periodic maintenance
- [x] **Log Rotation**: Automated log rotation with compression
- [x] **Daily Tasks**: Temp file cleanup, disk space checking
- [x] **Weekly Tasks**: Build cleanup, image optimization
- [x] **Monthly Tasks**: System audit, performance review, security check
- [x] **Quarterly Tasks**: Major cleanup, dependency updates, config review
- [x] **Crontab Setup Script**: Automated crontab configuration

### GitHub Actions Integration
- [x] **GitHub Actions Workflow**: Created `.github/workflows/site-health-check.yml`
- [x] **Periodic Health Checks**: Every 6 hours automated monitoring
- [x] **Post-Commit Verification**: 15-minute delay deployment verification
- [x] **GitHub Issues**: Automatic issue creation on failures
- [x] **Built-in Notifications**: Uses GitHub's native notification system
- [x] **Log Artifacts**: Workflow logs stored as artifacts

### Documentation
- [x] **Setup Guides**: Comprehensive setup documentation
- [x] **GitHub Actions Guide**: Step-by-step GitHub Actions setup
- [x] **Monitoring Guide**: Complete monitoring system documentation
- [x] **External Link Guide**: External link validation documentation

### Testing & Validation
- [x] **Test Scripts**: Created test scripts for all components
- [x] **External Link Testing**: Validated external link functionality
- [x] **Email Testing**: Verified email configuration
- [x] **Health Check Testing**: Confirmed all monitoring components work

---

## Critical Issues to Address (URGENT)

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

## Immediate Next Steps

### Email Configuration (Priority: HIGH)
- [ ] **Configure Email Settings**: Run `./utils/bin/setup_site_monitoring.sh`
- [ ] **Set Up Gmail App Password**: Create app password for Gmail
- [ ] **Test Email Alerts**: Verify email notifications work
- [ ] **Configure OAuth2** (Optional): Set up OAuth2 for enhanced security

### Local Monitoring Setup (Priority: HIGH)
- [ ] **Set Up Crontab**: Run `./utils/bin/setup_crontab.sh`
- [ ] **Test Scheduled Tasks**: Verify daily/weekly/monthly tasks work
- [ ] **Configure Log Rotation**: Ensure logs don't fill disk space
- [ ] **Test Health Checks**: Run manual health checks

### GitHub Actions Setup (Priority: MEDIUM)
- [ ] **Enable GitHub Actions**: Enable in repository settings
- [ ] **Test Workflow**: Run manual workflow execution
- [ ] **Configure Notifications**: Set up GitHub notification preferences
- [ ] **Monitor First Run**: Watch first automated health check

---

## Site Structure Improvements

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

## Quality Assurance

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

## Orphaned Pages Management

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

## Documentation and Standards

### 11. **Content Guidelines**
- [x] **Create post templates** - Available in `docs/templates/blog-templates.md`
- [x] **Document the build and deployment process** - Available in `docs/guides/site-operations.md`
- [ ] **Create content style guide** for consistent writing
- [ ] **Document image requirements** (sizes, formats, naming)

### 12. **Maintenance Procedures**
- [x] **Emergency procedures** - Available in `docs/guides/site-operations.md`
- [x] **Regular content audits** - Automated via monitoring system
- [x] **Dependency updates** - Tracked in TODO.md
- [x] **Backup procedures** - Integrated with monitoring system

---

## Future Enhancements

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

### 15. **Advanced Monitoring Features**
- [ ] **Performance Metrics**: Add detailed performance tracking
- [ ] **Uptime Monitoring**: Track site availability over time
- [ ] **Response Time Trends**: Monitor performance trends
- [ ] **Custom Health Checks**: Add project-specific health checks
- [ ] **Database Monitoring** (if applicable): Monitor any databases
- [ ] **SSL Certificate Monitoring**: Check certificate expiration

### 16. **Integration Enhancements**
- [ ] **Slack/Discord Integration**: Add chat notifications
- [ ] **Webhook Support**: Allow external system integration
- [ ] **API Endpoints**: Create REST API for monitoring data
- [ ] **Dashboard**: Create web dashboard for monitoring status
- [ ] **Metrics Export**: Export monitoring data for analysis

### 17. **Security & Compliance**
- [ ] **Security Scanning**: Add security vulnerability checks
- [ ] **Content Security Policy**: Monitor CSP violations
- [ ] **Privacy Compliance**: Check GDPR/privacy compliance
- [ ] **Accessibility Testing**: Add accessibility compliance checks
- [ ] **SEO Health Checks**: Monitor SEO-related issues

### 18. **Automation Improvements**
- [ ] **Auto-Fix Capabilities**: Automatically fix common issues
- [ ] **Backup Verification**: Verify backup integrity
- [ ] **Dependency Updates**: Automated dependency management
- [ ] **Content Validation**: Check content quality and consistency
- [ ] **Link Maintenance**: Automated broken link reporting

---

## Maintenance Tasks

### Regular Maintenance (Weekly)
- [ ] **Review Health Check Results**: Check for patterns or trends
- [ ] **Update Critical Pages**: Add new important pages to monitoring
- [ ] **Review External Links**: Check for new external references
- [ ] **Clean Up Logs**: Ensure log rotation is working
- [ ] **Test Email Alerts**: Verify notification system

### Periodic Maintenance (Monthly)
- [ ] **Update Dependencies**: Keep monitoring tools updated
- [ ] **Review Configurations**: Update settings as needed
- [ ] **Performance Review**: Analyze response time trends
- [ ] **Security Review**: Check for security issues
- [ ] **Backup Verification**: Test backup and recovery procedures

### Annual Maintenance (Yearly)
- [ ] **System Audit**: Comprehensive system review
- [ ] **Documentation Update**: Update all documentation
- [ ] **Configuration Review**: Review and optimize all settings
- [ ] **Capacity Planning**: Assess monitoring system capacity
- [ ] **Technology Updates**: Evaluate new monitoring technologies

---

## Troubleshooting Checklist

### Common Issues
- [ ] **Email Not Working**: Check SMTP settings and app passwords
- [ ] **Health Checks Failing**: Review logs and configuration
- [ ] **External Links Broken**: Update or remove broken links
- [ ] **GitHub Actions Failing**: Check workflow permissions and secrets
- [ ] **Log Files Growing**: Verify log rotation is working
- [ ] **Performance Issues**: Check response times and optimize

### Emergency Procedures
- [ ] **Site Down**: Check monitoring system and site status
- [ ] **Email Alerts Not Working**: Verify email configuration
- [ ] **GitHub Actions Down**: Check GitHub status and workflow
- [ ] **Configuration Issues**: Review and fix configuration files
- [ ] **Log Corruption**: Restore from backup and investigate

---

## Success Metrics

### Key Performance Indicators
- [ ] **Uptime**: Target 99.9%+ availability
- [ ] **Response Time**: Target <2 seconds average
- [ ] **Broken Links**: Target 0 broken external links
- [ ] **Email Delivery**: Target 100% alert delivery
- [ ] **False Positives**: Target <5% false positive rate

### Monitoring Coverage
- [ ] **All Critical Pages**: 100% of important pages monitored
- [ ] **All External Links**: 100% of external links validated
- [ ] **All Images**: 100% of images verified
- [ ] **All Internal Links**: 100% of internal links checked
- [ ] **24/7 Monitoring**: Continuous monitoring coverage

---

## Priority Order

### **URGENT (Do First):**
1. Fix broken images on live website
2. Fix Liquid syntax errors
3. Push current updates to production

### **High Priority:**
4. Email configuration setup
5. Local monitoring setup
6. Orphaned page review
7. Navigation improvements

### **Medium Priority:**
8. GitHub Actions setup
9. Content organization
10. Performance optimization
11. Future enhancements

### **Low Priority:**
12. Blog separation and organization
13. Advanced indexing and search features

---

## Notes
- This checklist consolidates both site improvements and reliability monitoring tasks
- Many items from the original checklist have been completed through our automation and monitoring work
- The site reliability monitoring system has significantly improved our ability to detect and prevent issues
- Documentation has been completely reorganized for better navigation and maintenance
- Focus should be on the urgent items first, then the high-priority technical improvements

---

*Last Updated: July 01, 2025* 