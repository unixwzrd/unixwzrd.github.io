# Documentation index

Entry point for site setup, publishing, monitoring, and tooling.

**Utilities index (clickable file list):** [../utils/README.md](../utils/README.md)

## Quick start

### New contributors
1. **Project overview** → [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
2. **Day-to-day site work** → [guides/site-operations.md](guides/site-operations.md)
3. **Active tasks** → [../TODO.md](../TODO.md)

### Publishing and posts
1. **Blog workflow** → [workflows/blog-publishing.md](workflows/blog-publishing.md)
2. **Templates, `slug`, short URLs (`/s/...`)** → [templates/blog-templates.md](templates/blog-templates.md)
3. **Deploy / production build** → [guides/deployment.md](guides/deployment.md)

### Operations and quality
1. **Checklist & triage** → [guides/checklist.md](guides/checklist.md)
2. **Testing** → [guides/testing.md](guides/testing.md)
3. **Pre-commit (site checks)** → [tools/pre-commit-checks.md](tools/pre-commit-checks.md) - plus optional [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) for `short_url` on staged posts only

## Documentation structure

### Project Overview & Status
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project summary, current status, roadmap, and technical stack
- **[TODO.md](../TODO.md)** - Active tasks and priorities

### Guides
- **[guides/site-operations.md](guides/site-operations.md)** - Maintenance and navigation to other guides
- **[guides/deployment.md](guides/deployment.md)** - Builds and GitHub Pages
- **[guides/monitoring.md](guides/monitoring.md)** - Monitoring and alerting
- **[guides/checklist.md](guides/checklist.md)** - Improvement checklist and triage
- **[guides/testing.md](guides/testing.md)** - Validation and HTMLProofer
- **[guides/strategy.md](guides/strategy.md)** - Monitoring cadence and practices

### Tools and workflows
- **[../utils/README.md](../utils/README.md)** - Catalog of `utils/bin` scripts (checks, OG fetch, monitoring, fixes)
- **[tools/pre-commit-checks.md](tools/pre-commit-checks.md)** - `utils/bin/check_site.sh` and check scripts
- **[workflows/blog-publishing.md](workflows/blog-publishing.md)** - Publishing workflow
- **[templates/blog-templates.md](templates/blog-templates.md)** - Post templates, `slug`, short links, backfill

## By task
- **Project status** → [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- **Broken build or deploy** → [guides/troubleshooting.md](guides/troubleshooting.md), [guides/deployment.md](guides/deployment.md)
- **New or edited blog post** → [workflows/blog-publishing.md](workflows/blog-publishing.md), [templates/blog-templates.md](templates/blog-templates.md)
- **Short link / `short_url` drift** → [templates/blog-templates.md](templates/blog-templates.md) (`backfill_short_url_front_matter.rb`, `--check`)
- **Monitoring** → [guides/monitoring.md](guides/monitoring.md)
- **Pre-commit** → [tools/pre-commit-checks.md](tools/pre-commit-checks.md), [`.pre-commit-config.yaml`](../.pre-commit-config.yaml)
- **What runs in `utils/bin`?** → [../utils/README.md](../utils/README.md), [guides/reference-utilities.md](guides/reference-utilities.md)

## Quick Reference

### Common commands
```bash
# Full validation (see tools/pre-commit-checks.md)
./utils/bin/check_site.sh

# Production build (same as GitHub Actions - run from repo root)
JEKYLL_ENV=production bundle exec jekyll build --trace

# Verify short_url front matter matches computed /s/ codes (no writes)
bundle exec ruby scripts/backfill_short_url_front_matter.rb --check

# Site health (if monitoring tools are configured)
utils/bin/site_reliability_monitor.py --mode health
```

### Key Files
- **Configuration**: [utils/etc/site_monitor_config.json](../utils/etc/site_monitor_config.json)
- **Monitoring**: [utils/bin/site_reliability_monitor.py](../utils/bin/site_reliability_monitor.py)
- **Maintenance**: [utils/bin/scheduled_tasks.py](../utils/bin/scheduled_tasks.py)
- **Logs**: [utils/log/](../utils/log/) directory

## Documentation maintenance

- Update guides when procedures or tooling change (build commands, hooks, Actions).
- Add links in this index when new top-level docs are added.
- [CHANGELOG.md](../CHANGELOG.md) and [TODO.md](../TODO.md) for history and tasks.

## Related Documentation

### External Resources
- **[CHANGELOG.md](../CHANGELOG.md)** - Complete change history
- **[TODO.md](../TODO.md)** - Active tasks and priorities
- **[.project-planning/checklist.md](../.project-planning/checklist.md)** - Site improvement checklist
- **[.project-planning/Site-automation-article-thoughts.md](../.project-planning/Site-automation-article-thoughts.md)** - Automation article planning
- **[Gemfile](../Gemfile)** - Ruby dependencies
- **[requirements.txt](../requirements.txt)** - Python dependencies

### Project Structure
```
docs/
├── README.md                    # This file
├── PROJECT_OVERVIEW.md          # High-level summary
├── guides/                      # How-to guides
├── tools/                       # Tool documentation
├── workflows/                   # Processes
└── templates/                   # Templates
../utils/README.md               # Index of validation / OG / monitoring scripts
../scripts/                      # Jekyll helpers (e.g. short_url backfill)
```

---

**Updated:** 2026-05-02

