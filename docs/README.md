# Documentation Index

*Your central hub for all project documentation*

## 🚀 Quick Start

### For New Contributors
1. **Project Overview** → `PROJECT_OVERVIEW.md` - High-level summary, current status, and roadmap
2. **Getting Started** → `guides/site-operations.md` - How to work with the site
3. **Active Tasks** → `../TODO.md` - What's being worked on

### For Daily Operations
1. **Site Health Check** → `guides/site-reliability-checklist.md` - Emergency procedures
2. **Content Publishing** → `workflows/blog-publishing.md` - How to publish content
3. **Testing** → `guides/testing.md` - How to test changes

## 📚 Documentation Structure

### 🎯 **Project Overview & Status**
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project summary, current status, roadmap, and technical stack
- **[TODO.md](../TODO.md)** - Active tasks and priorities

### 🛠️ **Guides & How-To**
- **[guides/site-operations.md](guides/site-operations.md)** - Site maintenance and daily operations
- **[guides/site-reliability-monitoring.md](guides/site-reliability-monitoring.md)** - Monitoring system setup and usage
- **[guides/site-reliability-checklist.md](guides/site-reliability-checklist.md)** - Emergency procedures and troubleshooting
- **[guides/testing.md](guides/testing.md)** - Testing procedures and validation
- **[guides/monitoring-strategy.md](guides/monitoring-strategy.md)** - Monitoring best practices and strategies

### 🔧 **Tools & Systems**
- **[tools/pre-commit-checks.md](tools/pre-commit-checks.md)** - Pre-commit quality assurance system
- **[workflows/blog-publishing.md](workflows/blog-publishing.md)** - Content publishing workflow
- **[templates/blog-templates.md](templates/blog-templates.md)** - Blog post templates and examples

## 🔍 Navigation by Task

### I want to...
- **Understand the project** → `PROJECT_OVERVIEW.md`
- **See what's happening now** → `PROJECT_OVERVIEW.md` (Current State section)
- **Fix a broken site** → `guides/site-reliability-checklist.md`
- **Publish content** → `workflows/blog-publishing.md`
- **Set up monitoring** → `guides/site-reliability-monitoring.md`
- **Test changes** → `guides/testing.md`
- **Configure pre-commit** → `tools/pre-commit-checks.md`
- **Add new features** → `../TODO.md`

### I need to...
- **Check site health** → `guides/site-reliability-checklist.md`
- **Fix image issues** → `guides/testing.md` (image path section)
- **Monitor external links** → `guides/site-reliability-monitoring.md`
- **Update documentation** → `guides/site-operations.md`
- **Deploy changes** → `workflows/blog-publishing.md`

## 📋 Quick Reference

### Essential Commands
```bash
# Site health check
utils/bin/site_reliability_monitor.py --mode health

# Test external links
utils/bin/test_external_links.py

# Fix image paths
utils/bin/fix_image_case_sensitivity.py

# Manage missing pages
utils/bin/manage_missing_pages.py --list
```

### Key Files
- **Configuration**: `utils/etc/site_monitor_config.json`
- **Monitoring**: `utils/bin/site_reliability_monitor.py`
- **Maintenance**: `utils/bin/scheduled_tasks.py`
- **Logs**: `utils/log/` directory

### Emergency Contacts
- **Site Down**: `guides/site-reliability-checklist.md`
- **Broken Images**: `guides/testing.md`
- **Broken Links**: `guides/site-reliability-monitoring.md`
- **Build Issues**: `guides/site-operations.md`

## 🔄 Documentation Maintenance

### Update Frequency
- **PROJECT_OVERVIEW.md** - After each development session or major changes
- **TODO.md** - Continuously as tasks are added/completed
- **Guides** - When procedures change
- **CHANGELOG.md** - After each release/update

### Contributing to Documentation
1. Update relevant guides when procedures change
2. Add new guides for new systems/processes
3. Update this index when adding new documentation
4. Keep PROJECT_OVERVIEW.md current with recent work and status
5. Update TODO.md as tasks are completed or added

## 📖 Related Documentation

### External Resources
- **[CHANGELOG.md](../CHANGELOG.md)** - Complete change history
- **[TODO.md](../TODO.md)** - Active tasks and priorities
- **[.project-planning/site-improvement-checklist.md](../.project-planning/site-improvement-checklist.md)** - Site improvement checklist
- **[.project-planning/Site-automation-article-thoughts.md](../.project-planning/Site-automation-article-thoughts.md)** - Automation article planning
- **[Gemfile](../Gemfile)** - Ruby dependencies
- **[requirements.txt](../requirements.txt)** - Python dependencies

### Project Structure
```
docs/
├── README.md                    # This file - Documentation index
├── PROJECT_OVERVIEW.md          # High-level project summary and current status
├── guides/                      # How-to guides and procedures
├── tools/                       # Tool documentation
├── workflows/                   # Process documentation
└── templates/                   # Templates and examples
```

---

*This index is maintained to provide clear navigation through all project documentation. Update it when adding new docs or reorganizing existing ones.* 