# Website operations and tooling

This is the canonical catalog for maintained website commands and their support files. Paths in tool lists are relative to `utils/`. Use `utils/bin/check-site` for the supported entry point. Each implementation has one location; commands and tutorials use it directly without compatibility symlinks.

## Tool layout and safety boundaries

- `bin/` contains authoring and operator commands, services, monitoring, migration helpers, and the local quality-check runner.
- `bin/checks/` contains ordered checks used by the local pre-commit/site-validation workflow. Some checks can update repository files; inspect their descriptions before running them individually.
- `lib/` contains shared runtime helpers used by commands and tests.
- `tests/ruby/` and `tests/python/` contain offline automated regressions. `tests/browser/` contains local rendered-site browser regressions.
- `bin/diagnostics/` contains manual diagnostics, including network, email, service, and watcher probes. These are not part of the deterministic test suite and may contact external services or inspect running services.
- `bin/watchers/` contains the runtime image-path watcher plugin and its fixture probe.
- `bin/backup/` holds a retained one-off repair script, not a supported routine command.

The former root scripts directory and moved test/diagnostic aliases have been removed. Use the canonical targets below. The Git hook installed at `.git/hooks/pre-commit` is user-local; `utils/bin/pre-commit` is its portable repository wrapper. Do not bypass hooks as a routine workaround.

## Main command

Commit the consolidation as one coherent change: canonical implementation files, removal of old paths, updated callers/tutorials/workflow, and their tests must travel together. A partial commit can leave a fresh checkout with missing tools. The migration does not install or replace a developer's active Git hooks automatically.

| Path | Purpose, invocation, and effects |
| --- | --- |
| [`bin/check-site`](bin/check-site) | Main CLI: `local`, `remote`, `all`, `checks`, `test [--site PATH]`, `artifacts`, and `help`. Local/remote crawl the corresponding served site; `checks` runs the local shell suite; `test` runs deterministic Ruby/Python tests and adds rendered-site checks when given an existing site directory; `artifacts` reports aged browser output unless explicit reviewed-manifest deletion is requested. |
| [`bin/check-browser`](bin/check-browser) | Runs one of the local browser suites (`local-reader`, `reader-experience`, `secrets-kit-product`, `short-link-attribution`) through an owned Playwright CLI session; blocks external requests, rejects production URLs, records screenshots in a timestamped output run, and pins failures. |
| [`bin/check_site.sh`](bin/check_site.sh) | Local ordered check runner. Supports `--list`, `--run`, and `--skip`; several checks can write site metadata or repair content, so review a check before running it. |
| [`bin/pre-commit`](bin/pre-commit) | Portable wrapper invoked by the repository hook. Delegates to local site checks; does not install dependencies. |
| [`lib/site-environment.sh`](lib/site-environment.sh) | Selects an existing project RVM gemset and Conda `python-website-dev` environment for local GUI clients when available, otherwise uses the caller environment. Performs no package installation and does not alter shell defaults. |
| [`lib/run_tests.py`](lib/run_tests.py) | Discovers and runs canonical Ruby and Python regression suites. `--site PATH` adds rendered-site validation, permalink/taxonomy/redirect checks, browser-reader and product checks as configured, plus offline HTMLProofer; it does not build the site or run network diagnostics. |
| [`lib/artifacts.py`](lib/artifacts.py) | Reports browser artifacts older than 30 days under `output/playwright/` and `.playwright-cli/`. `--manifest PATH` writes an exclusive review manifest; `--apply MANIFEST` permanently removes only the reviewed, revalidated regular files. Tracked files, symlinks, path escapes, `.keep`, `.active`, and run metadata are protected. Never use this for broad generated-file cleanup. |
| [`bin/cleanup-artifacts`](bin/cleanup-artifacts) | Shell entry point for the artifact report/manifest workflow. Default is report-only. |
| [`bin/checks/14_artifact_report.sh`](bin/checks/14_artifact_report.sh) | Local check-suite artifact report; report-only and non-failing based on age. CI also reports but does not delete artifacts. |

## Automated checks (`bin/checks/`)

| Path | Purpose and effect |
| --- | --- |
| [`bin/checks/01_environment.sh`](bin/checks/01_environment.sh) | Checks selected Ruby/Python executables, locked bundle availability, and installed Python requirements. Does not install packages. |
| [`bin/checks/02_permalinks.sh`](bin/checks/02_permalinks.sh) | Validates permalink definitions and collision constraints. |
| [`bin/checks/02_short_link_metadata.sh`](bin/checks/02_short_link_metadata.sh) | Verifies the working-tree short-link metadata with the same check as GitHub CI; does not edit or stage posts. |
| [`bin/checks/03_jekyll_doctor.sh`](bin/checks/03_jekyll_doctor.sh) | Runs Jekyll doctor; case-only URL warnings on a case-insensitive macOS volume are reported, with strict behavior controlled by the script. |
| [`bin/checks/04_link_checker.sh`](bin/checks/04_link_checker.sh) | Checks source-level internal references and reports relevant link issues. |
| [`bin/checks/05_site_link_checker.sh`](bin/checks/05_site_link_checker.sh) | Builds production output through `utils/bin/jekyll-site build -n`, replacing the shared `_site/`, then runs HTMLProofer and nested-slash link checks. Avoid during another shared preview; use an isolated build plus `check-site test --site PATH` for non-disruptive rendered checks. |
| [`bin/checks/05_update_project_data.sh`](bin/checks/05_update_project_data.sh) | Fetches project/repository metadata and, when matching generated files changed, stages the metadata, project pages, and project images with `git add`. This is a networked, staging side effect; review staged and unstaged diffs before committing. |
| [`bin/checks/06_external_link_checker.sh`](bin/checks/06_external_link_checker.sh) | Optional network-dependent external-link check; may be slow or affected by remote throttling. |
| [`bin/checks/06_large_files.sh`](bin/checks/06_large_files.sh) | Reports large repository files for review. |
| [`bin/checks/07_jekyll_build.sh`](bin/checks/07_jekyll_build.sh) | Runs a Jekyll build as part of local validation. |
| [`bin/checks/08_required_files.sh`](bin/checks/08_required_files.sh) | Checks required repository/site files. |
| [`bin/checks/09_liquid_syntax.sh`](bin/checks/09_liquid_syntax.sh) | Checks Liquid syntax and template errors. |
| [`bin/checks/10_front_matter.sh`](bin/checks/10_front_matter.sh) | Validates and may normalize eligible front matter; inspect the diff after execution. |
| [`bin/checks/11_navigation.sh`](bin/checks/11_navigation.sh) | Checks configured navigation references. |
| [`bin/checks/12_image_paths.sh`](bin/checks/12_image_paths.sh) | Checks image path case and references; its documented full/incremental mode determines scan scope. |
| [`bin/checks/13_cleanup_text.sh`](bin/checks/13_cleanup_text.sh) | Applies configured text cleanup to selected files and preserves file modes; inspect modifications before accepting them. |
| [`bin/checks/check_permalinks.rb`](bin/checks/check_permalinks.rb) | Shared permalink validator used in local and rendered-site validation. |
| [`bin/checks/check_tag_taxonomy.rb`](bin/checks/check_tag_taxonomy.rb) | Validates tag taxonomy and expected tag data. |
| [`bin/checks/verify_project_permalink_redirects.rb`](bin/checks/verify_project_permalink_redirects.rb) | Verifies project permalink redirect coverage in rendered output. |
| [`bin/checks/verify_short_url_redirects.rb`](bin/checks/verify_short_url_redirects.rb) | Verifies generated short-link redirect pages in rendered output. |

## Authoring, rendering, and site data (`bin/`)

| Path | Purpose, invocation, and effects |
| --- | --- |
| [`bin/article-audio`](bin/article-audio) | Generates or checks approved public MP3 narration for posts; generation calls the configured local TTS Bridge and writes public audio plus identity metadata. |
| [`bin/article-tts`](bin/article-tts) | Extracts rendered article prose for dry-run, local playback, browser relay, or retained audio workflows; TTS actions contact the configured local bridge. |
| [`bin/article_audio.py`](bin/article_audio.py) | Python implementation behind the `article-audio` command. |
| [`bin/article_tts.py`](bin/article_tts.py) | Python implementation behind the `article-tts` command. |
| [`bin/backfill_short_url_front_matter.rb`](bin/backfill_short_url_front_matter.rb) | Checks or backfills short-link metadata in opted-in posts/pages; use `--check` for read-only verification. |
| [`bin/check_nested_slashless_links.py`](bin/check_nested_slashless_links.py) | Finds nested links that omit expected trailing slashes. |
| [`bin/fetch_og.py`](bin/fetch_og.py) | Fetches project OpenGraph/repository metadata and updates generated project data; network access and source edits are expected. |
| [`bin/fix_all_frontmatter.py`](bin/fix_all_frontmatter.py) | Bulk front-matter repair helper; mutates matching source files, so review scope and diff first. |
| [`bin/fix_broken_links.py`](bin/fix_broken_links.py) | Applies configured broken-link corrections to site source; review before accepting changes. |
| [`bin/fix_frontmatter.py`](bin/fix_frontmatter.py) | Front-matter repair helper for selected content. |
| [`bin/fix_image_case_sensitivity.py`](bin/fix_image_case_sensitivity.py) | Finds/fixes image path casing against files on disk. |
| [`bin/fix_image_paths.py`](bin/fix_image_paths.py) | Repairs image paths in eligible content; writes source changes. |
| [`bin/fix_internal_links.py`](bin/fix_internal_links.py) | Repairs selected internal links in source; review its target selection and diff. |
| [`bin/jekyll-site`](bin/jekyll-site) | Build/serve wrapper for Jekyll, including optional local rendered-site checks. Serving on a LAN requires an explicit bind address/hostname and exposes draft-inclusive preview content without authentication; keep it on a trusted network. |
| [`bin/list_tags.rb`](bin/list_tags.rb) | Lists configured/published tag values for editorial inspection. |
| [`bin/render-blog-diagram.py`](bin/render-blog-diagram.py) | Renders one Graphviz or Mermaid diagram source to image output; requires the corresponding renderer on `PATH`. |
| [`bin/render-jekyll-template-graph`](bin/render-jekyll-template-graph) | Produces a graph of Jekyll template/include relationships for inspection. |
| [`bin/validate_frontmatter.py`](bin/validate_frontmatter.py) | Validates front matter and reports errors without being a general content repair tool. |
| [`bin/validate_permalink_consistency.py`](bin/validate_permalink_consistency.py) | Checks permalink consistency across source files. |

## Services, monitoring, and scheduled operations (`bin/`)

| Path | Purpose, invocation, and effects |
| --- | --- |
| [`bin/site-service`](bin/site-service) | Starts/stops/status-checks the configured local site service; service changes affect the user's local process state. |
| [`bin/site_reliability_monitor.py`](bin/site_reliability_monitor.py) | Runs configured health, crawl, and post-deployment monitoring modes; network/email modes can contact external endpoints. |
| [`bin/site_crawl_check.py`](bin/site_crawl_check.py) | Crawls a supplied base URL and reports reachable/missing site paths. |
| [`bin/manage_monitoring_pages.py`](bin/manage_monitoring_pages.py) | Manages the monitor's known-page inventory and associated state. |
| [`bin/periodic_monitor.sh`](bin/periodic_monitor.sh) | Shell entry point for scheduled monitoring. |
| [`bin/post_commit_monitor.sh`](bin/post_commit_monitor.sh) | Runs configured post-commit/deployment monitoring and can generate notifications. |
| [`bin/scheduled_tasks.py`](bin/scheduled_tasks.py) | Executes configured scheduled maintenance/monitoring tasks; review configuration before enabling schedules. |
| [`bin/setup_crontab.sh`](bin/setup_crontab.sh) | Installs or updates local cron entries; changes user scheduling configuration. |
| [`bin/setup_site_monitoring.sh`](bin/setup_site_monitoring.sh) | Configures local site monitoring and related notification setup; may write local configuration. |
| [`bin/file_watcher`](bin/file_watcher) | Command wrapper for the local file watcher. |
| [`bin/file_watcher.py`](bin/file_watcher.py) | Watches site source and dispatches configured local watcher plugins. |
| [`bin/watch_image_paths.py`](bin/watch_image_paths.py) | Runs the image-path watcher workflow for local authoring. |
| [`bin/watchers/README.md`](bin/watchers/README.md) | Documents watcher plugin contract and setup. |
| [`bin/watchers/image_path_fixer.py`](bin/watchers/image_path_fixer.py) | Watcher plugin that repairs image paths for changed files. |
| [`bin/watchers/test_watcher.py`](bin/watchers/test_watcher.py) | Example/fixture watcher for validating event dispatch; not the canonical automated test suite. |

## Social publishing (`bin/`)

| Path | Purpose and effect |
| --- | --- |
| [`bin/push-social-media`](bin/push-social-media) | Publishes prepared social content through configured integrations; an external publication action. |
| [`bin/push-twitter`](bin/push-twitter) | Legacy/specific social publishing command retained for its configured workflow; external publication action. |

## Automated test suites (`tests/`)

These suites are invoked through `utils/bin/check-site test`; do not use the manual diagnostics below as a substitute. Browser runs are local-only, block external requests, and reject production targets. Failed browser runs are pinned for inspection.

### Ruby (`tests/ruby/`)

| Path | Coverage |
| --- | --- |
| [`tests/ruby/test_check_site_environment.rb`](tests/ruby/test_check_site_environment.rb) | Environment selection and missing-dependency behavior. |
| [`tests/ruby/test_jekyll_site.rb`](tests/ruby/test_jekyll_site.rb) | Jekyll wrapper argument/build behavior. |
| [`tests/ruby/test_reader_experience.rb`](tests/ruby/test_reader_experience.rb) | Rendered reader/player behavior and integration expectations. |
| [`tests/ruby/test_secrets_kit_product.rb`](tests/ruby/test_secrets_kit_product.rb) | Secrets-Kit page structure, links, data tables, and product-page requirements. |
| [`tests/ruby/test_short_link_attribution.rb`](tests/ruby/test_short_link_attribution.rb) | Short-link redirect and query/attribution behavior. |

### Python (`tests/python/`)

| Path | Coverage |
| --- | --- |
| [`tests/python/test_article_audio.py`](tests/python/test_article_audio.py) | MP3 generation/check logic and manifests. |
| [`tests/python/test_article_tts.py`](tests/python/test_article_tts.py) | Article extraction, chunking, and TTS helper behavior. |
| [`tests/python/test_artifacts.py`](tests/python/test_artifacts.py) | Artifact reporting, manifest validation, and cleanup safety guards. |
| [`tests/python/test_browser_run.py`](tests/python/test_browser_run.py) | Browser URL policy, owned-session lifecycle, and retained evidence behavior. |
| [`tests/python/test_fetch_og.py`](tests/python/test_fetch_og.py) | OpenGraph/project metadata fetch behavior. |
| [`tests/python/test_site_reliability_monitor.py`](tests/python/test_site_reliability_monitor.py) | Reliability monitoring logic. |
| [`tests/python/test_tooling_layout.py`](tests/python/test_tooling_layout.py) | Canonical tool layout and catalog coverage. |

### Browser (`tests/browser/`)

| Path | Coverage |
| --- | --- |
| [`tests/browser/check_local_reader_browser.js`](tests/browser/check_local_reader_browser.js) | Local reader visibility and playback controls in the local site. |
| [`tests/browser/check_reader_experience_browser.js`](tests/browser/check_reader_experience_browser.js) | Reader behavior across representative rendered pages. |
| [`tests/browser/check_secrets_kit_product_browser.js`](tests/browser/check_secrets_kit_product_browser.js) | Secrets-Kit navigation, layout, and interactive product content. |
| [`tests/browser/check_short_link_attribution_browser.js`](tests/browser/check_short_link_attribution_browser.js) | Local short-link redirect behavior in a browser. |
| [`lib/browser_run.py`](lib/browser_run.py) | Shared browser session orchestration called by `bin/check-browser`; owns/closes its session, enforces local-only routing, and records run evidence. |

## Manual diagnostics (`bin/diagnostics/`)

These are intentionally not auto-discovered by `check-site test`; some contact networks, send email, or inspect/restart services. Run them only when that side effect is intended.

| Path | Purpose and effects |
| --- | --- |
| [`bin/diagnostics/quick_test.py`](bin/diagnostics/quick_test.py) | Manual quick integration probe; may depend on configured local services. |
| [`bin/diagnostics/test_email.py`](bin/diagnostics/test_email.py) | Sends or verifies configured email notifications. |
| [`bin/diagnostics/test_external_links.py`](bin/diagnostics/test_external_links.py) | Contacts external websites to check links. |
| [`bin/diagnostics/test_file_watcher.py`](bin/diagnostics/test_file_watcher.py) | Manually exercises the file watcher against local files/services. |
| [`bin/diagnostics/test_services.sh`](bin/diagnostics/test_services.sh) | Manual local service smoke test; may interact with running services. |

## Retained one-off repair

| Path | Purpose |
| --- | --- |
| [`bin/backup/fix_critical_links.py`](bin/backup/fix_critical_links.py) | Historical one-off link repair retained for audit/reference; not a routine maintenance command. |

## Artifact retention

The only automatically reportable browser-output locations are `output/playwright/` and `.playwright-cli/`. The local report check and CI report do not delete. To review aged candidates, run `utils/bin/check-site artifacts`; to prepare an exclusive manifest, supply `--manifest PATH`, inspect the manifest, then explicitly run `--apply PATH` only if deletion is intended. Mark active work with `.active`; pin useful or failed evidence with `.keep`. This does not cover published graphics, narration, `utils/etc/`, logs, or arbitrary `output/` content. No broad CI cleanup is configured.

## Related operator documentation

- [Pre-commit checks](../docs/tools/pre-commit-checks.md)
- [Testing](../docs/guides/testing.md)
- [Deployment](../docs/guides/deployment.md)
- [Environment setup](../docs/guides/environment-setup.md)
- [Maintenance](../docs/guides/maintenance.md)


