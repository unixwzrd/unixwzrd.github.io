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
| [bin/article-audio](bin/article-audio) | Check rendered posts for missing or stale public MP3 narration and generate only the files whose cleaned prose or public narration profile changed. |
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

Development-mode post pages display a small player at the bottom of the viewport. Select article text and press **Play** to hear only that selection. With no selection, click within the article and press **Play** to continue from that cursor position to the end. If no article cursor has been established, **Play** starts with the complete article. **Restart** always begins again at the article title, while **Pause**, **Resume**, and **Stop** act on the in-browser queue. Leaving the page stops playback.

The browser sends sentence-aware chunks to the relay on `127.0.0.1:11441`. The relay accepts only the local Jekyll origins by default, keeps the configured bridge endpoint and voice out of page JavaScript, and never writes browser-playback audio to disk. Each short WAV response is decoded in browser memory and the next chunk is prepared while the current one plays. This is buffered chunk playback rather than byte-level streaming because the current TTS Bridge completes each WAV response before returning it.

The player is excluded from production Jekyll builds. If the local site or relay uses a different port, repeat `--allow-origin` when starting the relay and set `articleTtsRelayUrl` in browser local storage to the new loopback relay URL.

The shared `post` layout injects this development player into every local blog post. It does not depend on `audio` front matter and it never appears in a production build.

### Generate retained MP3 narration

`article-audio` uses the same rendered-prose extractor as `article-tts`, but it publishes only the joined MP3 and a privacy-safe identity manifest. It compares the hash of the cleaned rendered article text, the narration profile name, the chunk size, and the MP3 hash. File timestamps are not used, so a metadata-only edit does not force expensive synthesis and touching an unchanged file does not make its narration stale.

Check one post without contacting the TTS Bridge:

```bash
utils/bin/article-audio --check \
  html/_posts/technology/2025-04-08-Remote-Debugging-With-VSCode.md
```

Check every publishable post that the local Jekyll server can render:

```bash
utils/bin/article-audio --check --all
```

Generate or refresh one MP3 while the local Jekyll server and TTS engine are available:

```bash
TTS_BRIDGE_URL="http://127.0.0.1:11440/v1" \
TTS_BRIDGE_VOICE="narrator" \
utils/bin/article-audio --generate \
  html/_posts/technology/2025-04-08-Remote-Debugging-With-VSCode.md
```

Use `--generate --all` for an intentional batch. Current MP3s are reused; only missing or stale items call TTS. `--force` regenerates selected audio even when the manifest is current. A failed synthesis occurs in a temporary directory and leaves the last complete published MP3 untouched.

Tracked public defaults live in `utils/etc/article-audio.defaults.json`. The file contains no bridge endpoint, model, or voice alias. Supply those private values through `TTS_BRIDGE_URL`, `TTS_BRIDGE_VOICE`, and optional `TTS_BRIDGE_MODEL`. Change the public `profile` value when the intended narration voice, model, or synthesis policy changes and every old manifest should become stale.

Generated files use this layout:

```text
html/assets/audio/blog/<category>/YYYY-MM-DD-<slug>.mp3
html/assets/audio/blog/<category>/YYYY-MM-DD-<slug>.audio.json
```

Generation does not edit post front matter. After listening to and approving an MP3, add the printed `audio` path to that post. The production player appears only after this opt-in.

---

## Repo root scripts (outside `utils/`)

Jekyll-specific helpers live next to the site config, not under `utils/`:

- [scripts/backfill_short_url_front_matter.rb](../scripts/backfill_short_url_front_matter.rb) - sync `short_url` front matter with `/s/<code>/` rules. Documented in [docs/templates/blog-templates.md](../docs/templates/blog-templates.md).

**Updated:** 2026-05-02
