# Site maintenance utilities (`utils/`)

- [Site maintenance utilities (`utils/`)](#site-maintenance-utilities-utils)
  - [Validation and pre-commit](#validation-and-pre-commit)
  - [Builds and local services](#builds-and-local-services)
  - [OpenGraph, thumbnails, and project data](#opengraph-thumbnails-and-project-data)
  - [Monitoring and scheduled ops](#monitoring-and-scheduled-ops)
  - [Fixes and one-off maintenance](#fixes-and-one-off-maintenance)
  - [Misc / social / tests](#misc--social--tests)
  - [Repo root scripts (outside `utils/`)](#repo-root-scripts-outside-utils)


Scripts and configs used to **validate**, **build**, **refresh project metadata** (OpenGraph thumbnails, `github_projects.yml`), and **monitor** the Jekyll site. Paths below are relative to this folder unless noted.

**Full operator reference:** [docs/guides/reference-utilities.md](../docs/guides/reference-utilities.md)
**Pre-commit / check pipeline:** [docs/tools/pre-commit-checks.md](../docs/tools/pre-commit-checks.md)
**Repo documentation index:** [docs/README.md](../docs/README.md)

---

## Validation and pre-commit

| Resource | Purpose |
|----------|---------|
| [bin/check_site.sh](bin/check_site.sh) | Run the numbered check suite (env, permalinks, links, Jekyll build, images, ...). |
| [bin/check-site](bin/check-site) | Convenience entry (if present) for the same flow. |
| [bin/checks/](bin/checks/) | Individual checks: `01_environment.sh`, `02_permalinks.sh`, `04_link_checker.sh`, `05_site_link_checker.sh` (HTMLProofer on `_site/`), `07_jekyll_build.sh`, `12_image_paths.sh`, `06_external_link_checker.sh` (opt-in / network), and others. |
| [bin/check_nested_slashless_links.py](bin/check_nested_slashless_links.py) | Deep link sanity helper. |
| [bin/validate_frontmatter.py](bin/validate_frontmatter.py) | Front matter checks. |
| [bin/validate_permalink_consistency.py](bin/validate_permalink_consistency.py) | Permalink consistency. |

---

## Builds and local services

| Resource | Purpose |
|----------|---------|
| [bin/jekyll-site](bin/jekyll-site) | Production-style Jekyll build wrapper (often with post-build checks). |
| [bin/site-service](bin/site-service) | Start/stop/restart local Jekyll (and related dev helpers). |
| [bin/file_watcher](bin/file_watcher) / [bin/file_watcher.py](bin/file_watcher.py) | File watching during development. |
| [bin/watch_image_paths.py](bin/watch_image_paths.py) | Watch / fix image path issues. |
| [bin/watchers/](bin/watchers/) | Watcher helpers ([watchers/README.md](bin/watchers/README.md)). |

---

## OpenGraph, thumbnails, and project data

| Resource | Purpose |
|----------|---------|
| [bin/fetch_og.py](bin/fetch_og.py) | Fetches OG metadata and images; merges with [html/_data/repos.yml](../html/_data/repos.yml); writes [html/_data/github_projects.yml](../html/_data/github_projects.yml). **Do not hand-edit** `github_projects.yml`. |
| [bin/test_fetch_og.py](bin/test_fetch_og.py) | Tests for the OG pipeline. |
| [bin/checks/05_update_project_data.sh](bin/checks/05_update_project_data.sh) | Hook in the check suite for refreshing project data when appropriate. |

---

## Monitoring and scheduled ops

| Resource | Purpose |
|----------|---------|
| [bin/site_reliability_monitor.py](bin/site_reliability_monitor.py) | Health checks, deployment verification hooks, optional alerts. |
| [bin/manage_monitoring_pages.py](bin/manage_monitoring_pages.py) | Manage tracked pages for monitoring. |
| [bin/scheduled_tasks.py](bin/scheduled_tasks.py) | Periodic maintenance tasks. |
| [bin/setup_site_monitoring.sh](bin/setup_site_monitoring.sh) | Initial monitoring setup. |
| [bin/setup_crontab.sh](bin/setup_crontab.sh) | Example crontab wiring. |
| [bin/post_commit_monitor.sh](bin/post_commit_monitor.sh) | Post-push verification helper. |
| [bin/periodic_monitor.sh](bin/periodic_monitor.sh) | Periodic monitor entry. |
| [bin/test_external_links.py](bin/test_external_links.py) | External link testing utility. |
| [etc/site_monitor_config.json](etc/site_monitor_config.json) | Monitor configuration (JSON). |
| [etc/scheduled_tasks_config.json](etc/scheduled_tasks_config.json) | Scheduled task config. |

---

## Fixes and one-off maintenance

| Resource | Purpose |
|----------|---------|
| [bin/fix_image_case_sensitivity.py](bin/fix_image_case_sensitivity.py) | Case-correct image paths (macOS vs Linux). |
| [bin/fix_image_paths.py](bin/fix_image_paths.py) | Path repairs. |
| [bin/fix_internal_links.py](bin/fix_internal_links.py) / [bin/fix_broken_links.py](bin/fix_broken_links.py) | Link repair helpers. |
| [bin/fix_frontmatter.py](bin/fix_frontmatter.py) / [bin/fix_all_frontmatter.py](bin/fix_all_frontmatter.py) | Front matter cleanup. |
| [bin/site_crawl_check.py](bin/site_crawl_check.py) | Crawl-oriented checks. |

---

## Misc / social / tests

| Resource | Purpose |
|----------|---------|
| [bin/article-tts](bin/article-tts) | Extract the prose from a rendered post, divide it into paragraph-aware chunks, and optionally send it to the configured TTS Bridge for playback and retained WAV/MP3 artifacts. Use `--dry-run` to inspect exactly what would be spoken. |
| [bin/push-twitter](bin/push-twitter) / [bin/push-social-media](bin/push-social-media) | Social publish helpers (operator use). |
| [bin/test_services.sh](bin/test_services.sh) | Service smoke tests. |
| [bin/test_email.py](bin/test_email.py) | Email / alert tests. |
| [bin/quick_test.py](bin/quick_test.py) / [bin/test_file_watcher.py](bin/test_file_watcher.py) | Dev tests. |
| [output/](output/) | Generated reports (e.g. dependency graphs) when produced. |
| [log/](log/) | Local log output directory (gitignored where applicable). |

### Read a rendered article through the TTS Bridge

The default extractor reads only `.post-content.e-content`. It keeps the title, headings, paragraphs, list items, blockquotes, visible link text, and inline code words. It omits URLs, HTML tags, series context and navigation, diagrams, captions, tables, code blocks, source disclosures, support material, forms, audio, video, and comments.

Inspect the exact text and chunk sizes without calling TTS:

```bash
utils/bin/article-tts \
  http://127.0.0.1:4000/technology/2026/09/08/voice-cloning-across-hosts-making-tts-operational/ \
  --dry-run
```

Generate, play, and retain the article audio:

```bash
TTS_BRIDGE_URL="http://127.0.0.1:11440/v1" \
TTS_BRIDGE_VOICE="narrator" \
utils/bin/article-tts \
  http://127.0.0.1:4000/technology/2026/09/08/voice-cloning-across-hosts-making-tts-operational/ \
  --play
```

Without `--output-dir`, the tool creates a new system temporary directory and prints its location. Supply an explicit directory to retain the extracted article, chunk text, chunk WAV files, joined WAV, MP3, and manifest. Reusing a directory resumes completed WAV chunks whose files remain present.

For editorial listening in the browser, start the loopback relay in a separate terminal:

```bash
TTS_BRIDGE_URL="http://127.0.0.1:11440/v1" \
TTS_BRIDGE_VOICE="narrator" \
utils/bin/article-tts --browser-server
```

Development-mode post pages display a small player at the bottom of the viewport. Select article text and press **Play** to hear only that selection, or press **Play** without a selection to hear the complete article body. **Pause**, **Resume**, and **Stop** act on the in-browser queue. Leaving the page stops playback.

The browser sends sentence-aware chunks to the relay on `127.0.0.1:11441`. The relay accepts only the local Jekyll origins by default, keeps the configured bridge endpoint and voice out of page JavaScript, and never writes browser-playback audio to disk. Each short WAV response is decoded in browser memory and the next chunk is prepared while the current one plays. This is buffered chunk playback rather than byte-level streaming because the current TTS Bridge completes each WAV response before returning it.

The player is excluded from production Jekyll builds. If the local site or relay uses a different port, repeat `--allow-origin` when starting the relay and set `articleTtsRelayUrl` in browser local storage to the new loopback relay URL.

---

## Repo root scripts (outside `utils/`)

Jekyll-specific helpers live next to the site config, not under `utils/`:

- [scripts/backfill_short_url_front_matter.rb](../scripts/backfill_short_url_front_matter.rb) - sync `short_url` front matter with `/s/<code>/` rules. Documented in [docs/templates/blog-templates.md](../docs/templates/blog-templates.md).

**Updated:** 2026-05-02
