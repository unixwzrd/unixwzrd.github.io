# Project Overview: UnixWzrd Website

## Current Status: July 2025

This document provides a high-level overview of the UnixWzrd website project, its current state, and roadmap. For detailed information, see the linked documentation.

## 🎯 Project Mission

A Jekyll-based website showcasing AI projects, technical content, and resources focused on:
- AI/ML development tools and utilities
- Parental alienation detection and prevention
- Technical tutorials and guides
- Open source contributions

## 📊 Current State

### 🎯 Recent Accomplishments (July 2025)
- **Enhanced Site Reliability Monitor**: Improved output formatting, summary counts, verbose mode, and early exit logic
- **Service Script Improvements**: Added `-r|--refresh` and `-n|--no-refresh` flags with smart defaults
- **Redirect System**: Implemented Jekyll redirects for old URLs to maintain link integrity
- **Smart Page Management**: Automatic sorting of critical pages and improved conflict handling
- **404 Page Handling**: Fixed image checking logic to properly handle 404 pages

### ✅ Completed Systems

#### 1. **Core Website Infrastructure**
- **Status**: ✅ Production Ready
- **Location**: [html/](../html/) directory
- **Features**:
  - Jekyll-based static site generation
  - Responsive design with custom CSS
  - Blog system with multiple categories
  - Project showcase pages
  - SEO optimization
  - Redirect system for URL changes
- **Documentation**: [docs/guides/site-operations.md](guides/site-operations.md)

#### 2. **Image Path Management System**
- **Status**: ✅ Production Ready
- **Location**: [utils/bin/fix_image_case_sensitivity.py](../utils/bin/fix_image_case_sensitivity.py)
- **Features**:
  - Automatic case sensitivity detection
  - Cross-platform compatibility (macOS/Linux)
  - Pre-commit integration
  - File watcher for development
- **Documentation**: [docs/guides/testing.md](guides/testing.md)

#### 3. **Pre-commit Quality Assurance**
- **Status**: ✅ Production Ready
- **Location**: [utils/bin/](../utils/bin/) (multiple scripts)
- **Features**:
  - Image path validation
  - Case sensitivity checks
  - Link validation
  - Code quality checks
- **Documentation**: [docs/tools/pre-commit-checks.md](tools/pre-commit-checks.md)

#### 4. **Site Reliability Monitoring**
- **Status**: ✅ Production Ready
- **Location**: [utils/bin/site_reliability_monitor.py](../utils/bin/site_reliability_monitor.py)
- **Features**:
  - Health checks and availability monitoring
  - Post-commit deployment verification
  - External link validation
  - Email alerts and GitHub issue creation
  - Missing page tracking and management
  - Summary counts and verbose mode
  - Early exit logic for site downtime
  - Smart 404 page handling
- **Documentation**: [docs/guides/monitoring.md](guides/monitoring.md)

#### 5. **Service Management System**
- **Status**: ✅ Production Ready
- **Location**: [utils/bin/site-service](../utils/bin/site-service), [utils/bin/jekyll-site](../utils/bin/jekyll-site), [utils/bin/file_watcher](../utils/bin/file_watcher)
- **Features**:
  - Orchestrated service management
  - Smart OG data refresh control (`-r|--refresh`, `-n|--no-refresh`)
  - Individual service control (`-j|--jekyll`, `-w|--watcher`)
  - Conflict resolution and warnings
  - Fast restart defaults
- **Documentation**: [docs/guides/site-operations.md](guides/site-operations.md)

#### 6. **Automated Maintenance System**
- **Status**: ✅ Production Ready
- **Location**: [utils/bin/scheduled_tasks.py](../utils/bin/scheduled_tasks.py)
- **Features**:
  - Log rotation and compression
  - Daily/weekly/monthly/quarterly tasks
  - Configurable maintenance schedules
  - Automated cleanup operations
- **Documentation**: [docs/guides/site-operations.md](guides/site-operations.md)

#### 7. **GitHub Actions Integration**
- **Status**: ✅ Production Ready
- **Location**: [.github/workflows/](../.github/workflows/)
- **Features**:
  - Automated site health checks
  - Post-commit verification
  - Issue creation for problems
  - Periodic monitoring
- **Documentation**: [docs/workflows/blog-publishing.md](workflows/blog-publishing.md)

### 🔄 Active Projects

#### 1. **LogGPT - ChatGPT Chat History Export**
- **Status**: 🚀 In Development
- **Location**: [projects/LogGPT/](../html/projects/LogGPT/)
- **Description**: Safari extension for exporting ChatGPT conversations
- **Progress**: Submitted to Apple App Store, awaiting review
- **Documentation**: [projects/LogGPT/](../html/projects/LogGPT/)

#### 2. **Case Analytics - Parental Alienation Detection**
- **Status**: 🔬 Research & Development
- **Location**: [projects/Case-Analytics/](../html/projects/Case-Analytics/)
- **Description**: AI-powered system for detecting patterns in legal cases
- **Progress**: Alpha testing phase
- **Documentation**: [projects/Case-Analytics/](../html/projects/Case-Analytics/)

#### 3. **TorchDevice - PyTorch Device Management**
- **Status**: 🛠️ Active Development
- **Location**: [projects/TorchDevice/](../html/projects/TorchDevice/)
- **Description**: Python utility for managing PyTorch device configurations
- **Progress**: Beta release 0.5.2 available
- **Documentation**: [projects/TorchDevice/](../html/projects/TorchDevice/)

#### 4. **VenvUtil - Virtual Environment Management**
- **Status**: 🛠️ Active Development
- **Location**: [projects/venvutil/](../html/projects/venvutil/)
- **Description**: Python utility for managing virtual environments
- **Progress**: Summer 2024 update released
- **Documentation**: [projects/venvutil/](../html/projects/venvutil/)

### 📚 Documentation Structure

```
docs/
├── guides/                    # How-to guides and tutorials
│   ├── site-operations.md     # Site maintenance and operations
│   ├── site-reliability-monitoring.md  # Monitoring system guide
│   ├── testing.md            # Testing procedures
│   └── monitoring-strategy.md # Monitoring best practices
├── tools/                     # Tool documentation
│   └── pre-commit-checks.md   # Pre-commit system guide
├── workflows/                 # Process documentation
│   └── blog-publishing.md     # Publishing workflow
└── templates/                 # Templates and examples
    └── blog-templates.md      # Blog post templates
```

## 🗺️ Roadmap

### Q1 2025 - System Optimization
- [ ] **Refactor site reliability monitor** (High Priority)
  - Break monolithic script into modular components
  - Improve maintainability and testing
  - Update all dependent scripts and documentation

- [ ] **Enhanced Content Management**
  - Implement automated content scheduling
  - Add content performance analytics
  - Improve SEO optimization

### Q2 2025 - Feature Expansion
- [ ] **Advanced Monitoring Features**
  - Real-time performance monitoring
  - User experience tracking
  - Advanced alerting systems

- [ ] **Project Portfolio Enhancement**
  - Interactive project demos
  - Live status indicators
  - Community feedback integration

### Q3-Q4 2025 - Scale and Growth
- [ ] **Community Features**
  - Comment system integration
  - User contribution workflows
  - Newsletter and subscription management

- [ ] **Advanced Analytics**
  - User behavior analysis
  - Content performance optimization
  - A/B testing framework

## 🔧 Technical Stack

### Core Technologies
- **Static Site Generator**: Jekyll (Ruby)
- **Hosting**: GitHub Pages
- **Monitoring**: Custom Python scripts
- **CI/CD**: GitHub Actions
- **Email**: SMTP with OAuth2 support

### Development Tools
- **Pre-commit**: Quality assurance automation
- **Python**: Monitoring and utility scripts
- **Bash**: Automation and deployment scripts
- **CSS/SCSS**: Custom styling with Minima theme

## 📋 Quick Reference

### Daily Operations
1. **Content Updates**: Edit files in [html/_posts/](../html/_posts/) or [html/projects/](../html/projects/)
2. **Site Testing**: Run `utils/bin/site_reliability_monitor.py --mode health`
3. **Pre-commit Checks**: Automatic via git hooks
4. **Monitoring**: Automated via GitHub Actions and cron jobs

### Emergency Procedures
- **Site Down**: Check [docs/guides/site-reliability-checklist.md](guides/site-reliability-checklist.md)
- **Broken Links**: Run external link validation
- **Image Issues**: Use case sensitivity fix script
- **Deployment Problems**: Review GitHub Actions logs

### Key Files
- **Configuration**: [utils/etc/site_monitor_config.json](../utils/etc/site_monitor_config.json)
- **Monitoring**: [utils/bin/site_reliability_monitor.py](../utils/bin/site_reliability_monitor.py)
- **Maintenance**: [utils/bin/scheduled_tasks.py](../utils/bin/scheduled_tasks.py)
- **Documentation**: [docs/guides/](guides/) directory

## 🤝 Contributing

### For Developers
1. Follow the pre-commit guidelines in [docs/tools/pre-commit-checks.md](tools/pre-commit-checks.md)
2. Test changes locally before committing
3. Update documentation for any new features
4. Follow the monitoring checklist in [docs/guides/site-reliability-checklist.md](guides/site-reliability-checklist.md)

### For Content Creators
1. Use templates from [docs/templates/blog-templates.md](templates/blog-templates.md)
2. Follow the publishing workflow in [docs/workflows/blog-publishing.md](workflows/blog-publishing.md)
3. Ensure images follow case sensitivity guidelines
4. Test content locally before publishing

## 📞 Support and Maintenance

### Regular Maintenance Tasks
- **Daily**: Automated health checks via GitHub Actions
- **Weekly**: Manual review of monitoring reports
- **Monthly**: Content audit and link validation
- **Quarterly**: System updates and security reviews

### Contact and Resources
- **Documentation**: See [docs/](.) directory for detailed guides
- **Issues**: Use GitHub Issues for bug reports
- **Monitoring**: Check [utils/log/](../utils/log/) for system logs
- **Configuration**: Review [utils/etc/](../utils/etc/) for settings

## Deployment Branches (Summary)

For details on how GitHub Pages deployment branches work (including `gh-pages` and best practices), see [Site Operations Guide](guides/site-operations.md#github-pages-deployment-branches).

---

*Last Updated: July 2025*
*Next Review: August 2025* 