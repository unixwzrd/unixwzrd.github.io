# Project overview: unixwzrd.ai

**Current status:** May 2026

This is a working Jekyll repo for **[unixwzrd.ai](https://unixwzrd.ai)** - static site under [`html/`](../html/), plus operator tooling under [`utils/`](../utils/) and [`scripts/`](../scripts/). It is a **private workspace**, not a generic site template; see the root [README.md](../README.md) for license scope and contribution expectations.

**Documentation entry point:** [docs/README.md](README.md)

---

## What ships here

| Area | Role |
|------|------|
| [`html/`](../html/) | Jekyll source (layouts, posts, projects, assets). |
| [`utils/bin/`](../utils/bin/) | Validation (`check_site.sh` + `checks/`), local services, `fetch_og.py`, monitoring, fix-up scripts. |
| [`scripts/`](../scripts/) | Jekyll helpers (e.g. [`backfill_short_url_front_matter.rb`](../scripts/backfill_short_url_front_matter.rb)). |
| [`.github/workflows/`](../.github/workflows/) | CI - production Jekyll build and GitHub Pages deploy. |

**Utilities catalog (clickable index):** [utils/README.md](../utils/README.md)

---

## Recent changes (2025-2026)

- **Short links (`/s/<code>/`)** - Deterministic redirects; hash tied to each post **file path** under `html/` (edits to title/date/slug do not change the code). Plugins: [`html/_plugins/01_short_link_injector.rb`](../html/_plugins/01_short_link_injector.rb), [`00_project_post_permalink.rb`](../html/_plugins/00_project_post_permalink.rb) (optional `slug:`). Ops: [templates/blog-templates.md](templates/blog-templates.md), optional [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) for staged posts.
- **`utils/README.md`** - Central index of maintenance scripts with relative links.
- **Root `README` + `LICENSE`** - README centers on tooling; MIT applies to `utils/` and `scripts/` only; `html/` remains all rights reserved (see [LICENSE](../LICENSE)).
- **Docs refresh** - [guides/deployment.md](guides/deployment.md) (CI parity, `short_url`), [README.md](README.md) index, troubleshooting and publishing notes aligned with current behavior.
- **Monitoring / checks** - Existing stack documented in [guides/monitoring.md](guides/monitoring.md) and [tools/pre-commit-checks.md](tools/pre-commit-checks.md); behavior unchanged at a high level.

---

## Operational systems (summary)

All are "in use" for day-to-day maintenance unless noted.

1. **Site** - Jekyll + Minima-derived styling; project blogs under `html/projects/`; [site-operations.md](guides/site-operations.md).
2. **Checks** - [`utils/bin/check_site.sh`](../utils/bin/check_site.sh) and [`utils/bin/checks/`](../utils/bin/checks/).
3. **Project cards / OG** - [`utils/bin/fetch_og.py`](../utils/bin/fetch_og.py) + [`html/_data/repos.yml`](../html/_data/repos.yml) → `github_projects.yml` (generated).
4. **Local dev** - [`utils/bin/site-service`](../utils/bin/site-service), [`jekyll-site`](../utils/bin/jekyll-site), watchers as needed.
5. **Monitoring** - [`utils/bin/site_reliability_monitor.py`](../utils/bin/site_reliability_monitor.py), config under [`utils/etc/`](../utils/etc/).
6. **CI/CD** - GitHub Actions build + Pages; see [deployment.md](guides/deployment.md) and [github-actions.md](guides/github-actions.md).

Image-path and link hygiene tools remain listed in [utils/README.md](../utils/README.md) and [testing.md](guides/testing.md).

---

## Project pages on the site

Landing pages for individual efforts live under [`html/projects/`](../html/projects/) (e.g. LogGPT, Case Analytics, TorchDevice, VenvUtil, Secrets Kit, and others). **Source of truth for shipping status** is each project's own repo and its site page - not this overview. Use the site navigation or repo tree for the current list.

---

## Documentation layout

```
docs/
├── README.md                 # Index (start here)
├── PROJECT_OVERVIEW.md       # This file
├── guides/
│   ├── site-operations.md    # Hub for ops guides
│   ├── deployment.md         # Build & Pages
│   ├── monitoring.md         # Reliability monitor
│   ├── testing.md            # Validation & HTMLProofer
│   ├── troubleshooting.md    # Common failures
│   ├── checklist.md          # Improvement / triage list
│   ├── github-actions.md     # Workflow overview
│   └── ...                     # environment, security, strategy, etc.
├── tools/
│   └── pre-commit-checks.md  # check_site.sh / checks/
├── workflows/
│   └── blog-publishing.md
└── templates/
    └── blog-templates.md     # Posts, slug, short URLs
```

Historical snapshot (July 2025): [guides/site-operations-archive-2025-07-09.md](guides/site-operations-archive-2025-07-09.md)

---

## Direction / backlog

Priorities drift with actual projects; treat this as **ideas**, not a dated commitment.

- **Monitor & checks** - Optional modularization of the reliability monitor; keep docs and `utils/README` in sync when scripts move.
- **Content** - Ongoing posts and project updates via normal publishing flow ([workflows/blog-publishing.md](workflows/blog-publishing.md)).
- **Hygiene** - Image optimization, a11y, spell-check: see [checklist.md](guides/checklist.md).

Large "community platform" items (comments, newsletters, A/B testing) remain **out of scope** unless explicitly reprioritized.

---

## Technical stack (short)

- **Jekyll** (Ruby), **GitHub Pages**, **GitHub Actions**
- **Python** - monitoring, `fetch_og`, many utilities
- **Bash** - `check_site.sh`, check scripts, glue

---

## Quick reference

| Task | Where |
|------|--------|
| Full check suite | `./utils/bin/check_site.sh` (repo root) |
| Production-style build | `JEKYLL_ENV=production bundle exec jekyll build` |
| OG / project YAML | `python utils/bin/fetch_og.py` (see [reference-utilities.md](guides/reference-utilities.md)) |
| Short URL drift | `bundle exec ruby scripts/backfill_short_url_front_matter.rb --check` |
| Broken build | [troubleshooting.md](guides/troubleshooting.md), [deployment.md](guides/deployment.md) |
| Triage / ideas | [checklist.md](guides/checklist.md) |

---

## Contributing

Aligned with the root [README.md](../README.md): **tooling and automation** (`utils/`, `scripts/`, docs for those) are the useful surface for outsiders; **site copy and design** in `html/` are not solicited as drive-by PRs.

---

## Maintenance rhythm

- **Automated** - GitHub Actions builds; optional cron / monitor per your machine setup ([monitoring.md](guides/monitoring.md)).
- **Manual** - Periodic pass over [checklist.md](guides/checklist.md), dependency bumps, link audits when needed.

**Logs / config** - [`utils/log/`](../utils/log/), [`utils/etc/`](../utils/etc/) (adjust paths if you relocate them).

---

## Deployment (GitHub Pages)

Branch and workflow behavior is summarized in [guides/deployment.md](guides/deployment.md#github-pages-deployment-branches) and linked from [site-operations.md](guides/site-operations.md).

---

**Last updated:** 2026-05-02
**Next review:** When major tooling or hosting changes - or quarterly, whichever comes first.

