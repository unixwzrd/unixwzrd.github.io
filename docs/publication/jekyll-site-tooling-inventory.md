# Jekyll Series: Source Inventory and Evidence Boundaries

Initial source review: September 22, 2026. Tracked source identity: `8c8846a9d1b98d967f9eee5c6da28db2bad035a7`. The series documents are working material outside that committed snapshot. This is a source-level inventory, not operational qualification. No builds, tests, crawls, speech requests, service changes, or deployment checks were executed for this review.

See the [series outline](jekyll-site-tooling-blog-series.md) and [review journal](jekyll-site-tooling-review.md). Paths below are repository-relative source locators, not public examples of workstation paths.

## Fact taxonomy

Evidence labels are independent, not successive stages. A feature can be implemented, configured in CI, and still lack current execution evidence.

| Label | Evidence required |
| --- | --- |
| Implemented | Inspected executable logic; identify its conditions and side effects |
| Configured | An inspected caller, workflow, or configuration selects the behavior; does not prove execution |
| Test present | Test source exists; inspect assertions before describing its coverage |
| Tested | Recorded command, environment, source identity, result, and retained output |
| Locally used | Current runtime evidence or an explicitly attributed operator report |
| Deployed | Identified deployed artifact and evidence of the claimed behavior |
| Historical | Dated source or history establishes earlier behavior; age or filename alone is insufficient |
| Proposed / deferred | Intended work with no implementation claim |
| Placeholder | A callable path lacks the named operation, even if it returns success |
| Unknown | Evidence absent or unresolved; never silently convert this to success or inactivity |

## Entry points and ownership

| Area and primary sources inspected | Source-supported behavior | Boundary or next evidence |
| --- | --- | --- |
| `utils/bin/jekyll-site`, `utils/bin/site-service` | Build/serve lifecycle, optional project refresh, production build followed by development serving; review-inclusive defaults and `--current` | Wrapper sources local environment and replaces build output. Do not run casually for inspection. No public status command established. Runtime and portability unverified |
| `utils/bin/file_watcher`, `utils/bin/watchers/README.md` | Separate watcher launcher and documented image-repair extension | Distinct from Jekyll's own watching. Publisher confirmed September 22 that FileWatcher is not used. Excluded from active workflow and further investigation |
| `html/_plugins/00_project_post_permalink.rb`, `01_short_link_injector.rb` | Required frozen project slug, legacy redirects, deterministic short links, collision and mismatch failures | Short-link source-path fallback still exists when immutable basis is missing. Do not generalize stability to all metadata changes |
| `html/_plugins/02_post_list_metadata.rb`, `docs/workflows/post-updates-and-ordering.md` | Update notices can promote discovery dates without changing publication dates | Series reading order and navigation remain separate; inspect each consuming Liquid include for Part 5 |
| `html/_plugins/03_tag_taxonomy_validator.rb`, `utils/bin/validate_frontmatter.py`, `utils/bin/checks/10_front_matter.sh` | Multiple metadata paths with different contracts; numbered front-matter step repairs files | Canonical taxonomy is not a comprehensive schema for all metadata |
| `utils/bin/fetch_og.py`, `utils/bin/checks/05_update_project_data.sh` | Repository/manual data, project images and cards, YAML output and scaffolding; check step can stage generated changes | Inspect overwrite/preservation rules before publishing commands. Do not hand-author generated data as an example |
| `html/_includes/blog_diagram.html`, `html/tools/diagram-viewer.html` | Shared diagram presentation and a separate viewer with same-origin SVG restriction | Browser accessibility and interaction are not verified by source inspection |
| `html/_includes/source_code.html`, `html/_plugins/source_code_filter.rb` | Highlighted inline source and download share an artifact; resolved paths constrained to `assets/code` | Presentation does not qualify the companion program |
| `utils/bin/article_audio.py`, audio/TTS test sources, `html/_layouts/post.html`, `utils/README.md` | Retained narration freshness, separate staged replacements, opt-in production audio; proofreader script omitted in production | Full relay/browser review remains per-article work. Private synthesis changes require public profile invalidation |
| `utils/bin/check-site`, `utils/bin/check_site.sh`, `.pre-commit-config.yaml`, `.github/workflows/jekyll.yml` | Crawl/suite dispatcher; numbered local suite; configured short-link and taxonomy hooks; production build and URL/taxonomy verification before Pages deployment | Local suite includes writes and staging. Hook installation and workflow success are unverified |
| `utils/bin/jekyll-site`, `html/assets/js/site-search.js`, `.github/workflows/jekyll.yml` | Local wrapper invokes Pagefind; browser code consumes it; inspected workflow contains no indexing step | Generated index availability and search after watched rebuilds or deployment remain unknown |
| `utils/bin/site_reliability_monitor.py`, `utils/bin/scheduled_tasks.py` | Monitoring and scheduling implementations exist; several maintenance methods are placeholders | Invocation map, actual schedule, daemon state, alerts, and deployed health remain unverified |

The deployment workflow triggers on pushes to `main` and manual dispatch. Its build uses Jekyll directly, not the local wrapper or numbered check suite. The pre-commit file configures short-link synchronization and taxonomy validation; it does not establish that the full suite runs on commit.

Backups, archive documentation, and one-off repair scripts are discovery leads, not established active paths. Do not delete or relabel them as unused without caller and history evidence. Social helper internals and notification configuration were not reviewed for operational behavior.

## Test evidence

Test names and selected source were reviewed; none were executed. These are candidate assertions to verify, not pass claims.

| Test file | Candidate evidence for the article |
| --- | --- |
| `utils/bin/test_fetch_og.py` | Overrides, private-repository scaffolding, cached-image reuse, rate-limit fallback, card regeneration, YAML formatting |
| `utils/bin/test_article_tts.py` | Prose extraction, chunking, endpoint handling, fixture synthesis, relay origins, dry-run reuse |
| `utils/bin/test_article_audio.py` | Post discovery, current/stale/tampered audio, private synthesis values excluded from manifests |
| `utils/bin/test_site_reliability_monitor.py` | Frozen project routes and legacy redirect discovery |

Watcher/service test files were discovered but their coverage is not established. FileWatcher is out of scope following the Publisher's correction. Ruby URL and taxonomy verifier scripts are configured checks; execution against identified source and generated output is needed before claiming they pass. Python fixture tests alone cannot establish Safari playback or deployed health.

## Drift and claims requiring care

1. `docs/workflows/post-updates-and-ordering.md` says source moves break short URLs. The current plugin uses retained `short_link_basis` when present. Explain the fallback and immutable basis rather than repeating the older table.
2. `utils/README.md` describes `check-site` as a convenience entry for the suite. Its actual subcommands distinguish local/remote crawling from `checks`.
3. The numbered project-data check can write and stage files; the front-matter check can repair content. A command described as a check is not necessarily observational.
4. Several methods in `scheduled_tasks.py`, including audit, security review, and backup verification, log or return success without implementing the named work. Describe these as placeholders.
5. Pagefind indexing appears in the local build wrapper, not the inspected deployment workflow. This is a source-path discrepancy, not proof of a live-site failure.
6. `article_audio.py` replaces the MP3 before replacing its manifest. Individual replacement operations do not create a transaction spanning both files. Freshness includes source path/URL, schema, prose, profile, chunk size, and audio hash.
7. The proofreader layout condition is non-production, broader than an exact development-only comparison. `--current` changes included content, not that environment condition.

Record these distinctions in article evidence packets. This planning change does not repair operator documentation or tooling.

## Artifact and privacy map

| Material | Ownership and treatment |
| --- | --- |
| Posts, metadata inputs, diagram sources, companion source | Authored material; inspect only examples needed for the article and confirm permission before quoting unpublished prose |
| Generated project YAML, cards, scaffolded pages | Generator-maintained outputs with publication significance; do not classify as disposable caches |
| SVG/PNG figures, companion packages, approved MP3 and audio manifest | Retained publication artifacts; verify correspondence to source and review state |
| `_site`, caches, PID files, logs, temporary synthesis intermediates | Derived/runtime material; classification does not authorize removal; may contain unpublished content or private values |
| `.env`, monitoring/scheduling settings, social credentials, voice settings | Sensitive inputs; do not copy into evidence packets or public examples |
| Analytics/comment identifiers, recipients, hostnames, paths, voice aliases | Generalize or omit from public prose; preserve the technical relationship with neutral placeholders |

Private runtime configuration was not needed for this source inventory. Before operational review, inspect only the values required for the specific claim and retain sanitized evidence. Use invented content for companion fixtures.

## Next evidence and editorial decisions

Keep the ten-part order. Broaden Part 5 to include project generation and search; keep retained narration detail in optional 7B; use Part 8 to distinguish checks, repairs, and deployment gates. Part 9's scope depends on evidence of implemented and used monitoring.

Next prepare Part 1's pre-draft packet: a small verified source inventory, claim table, privacy review, conflict list, and narrative outline. The opening should follow an article from authored source through preview, identity, presentation, review, and deployment configuration. Use one architecture figure after prose approval. Treat the origin story and personal observations as author-supplied history until corroborated; current code alone cannot establish why or when a decision was made.

Further runtime work should be selected per article. First inspect test side effects and dependencies; then retain focused results. Do not execute the broad mutating suite to fill an evidence table. Review production search, monitoring schedules, and browser audio only when their respective articles need those claims. The Publisher confirmed completion of the maintenance CHANGELOG update on September 22. Reconciliation and Part 1's pre-draft packet are complete; see the follow-up below.

## Publisher clarification and Liquid follow-up: September 22, 2026

The Publisher confirms that FileWatcher is not in use, that pre-commit and system checks are part of the operating workflow, and that GitHub thumbnail rate limiting motivated locally generated project cards. These are attributed operator/history reports. Preserve them alongside the configured paths already inspected; the exact installed pre-commit chain and current system-check invocation still need evidence before documenting drop-in commands.

The project catalog and Liquid composition are central to the series, rather than incidental presentation around utility scripts. Follow-up source inspection established:

| Stage | Source and behavior |
| --- | --- |
| Catalog input | `fetch_og.py:load_repository_config` reads the ordered `repositories` list from `html/_data/repos.yml`; actual private catalog values need not be quoted |
| Metadata and images | `create_project_entry` combines fetched data with `overrides` (legacy fallback `manual_data`), visibility, and image overrides. Without an image override on the fetched-data path, it tries a locally generated card before fallback images |
| Local cards | `generate_project_card` creates a 1200 by 600 PNG, compares cached card metadata, and uses `wkhtmltoimage`; local image generation does not eliminate upstream metadata requests |
| Scaffolding | `main` invokes `generate_project_files` when the landing page is absent. The helper creates image, project, `_drafts`, and `_posts` directories, a landing page, a draft template, and a dated draft-marked introduction; existing target files are preserved |
| Generated catalog | `write_projects_data` writes the processed list to `github_projects.yml` without sorting it. The inspected listing and menu loops consume that order |
| Project listing | `html/projects.md` invokes `projects_list.html` separately for private and public groups. The include selects matching visibility and excludes `none` |
| Projects menu | `navigation.html`, included by `header.html`, places fixed "All Projects" first, then iterates generated projects in retained catalog order and excludes `none` |
| Blog menu and hub | `blog_sections.yml` supplies ordered visible section entries to `navigation.html` and `blog.md`; fixed Blog Home, All Posts, and Topics links surround the dropdown's data-driven entries. `visible: false` hides a section from these views without removing its page or posts |
| Menu interaction | `custom_layout.scss` presents a checkbox-driven dropdown on narrow layouts and hover/focus-driven dropdowns at wider layouts; source defines behavior but browser interaction still needs review before article claims |
| Template hierarchy | `_layouts/project.html` inherits `page`, which inherits `default`; `default` supplies head, header, content, and footer. Project layout uses `project_lookup.html` to match `page.category` against generated project names |
| Project blogs | Project layout invokes `blog_list.html category=page.category`; that shared include delegates selection to `filter_discovery_posts.html`, sorts discovery results, and adds shared metadata and pagination |
| Discovery policy | Shared filtering excludes draft/unpublished/list-excluded material and posts belonging to `none` projects. The project blog include also suppresses a hidden project's list |
| Search boundary | Project/page layouts contain Pagefind body and exclusion markers. This establishes indexing intent, not a verified project-specific search filter or deployed index |
| Front-matter extensions | `series_order` controls series indexes; `update_notice` with a later `last_modified_at` promotes discovery order; `audio` enables the post audio include; project `category` connects a page to generated data. These fields work because current Liquid or plugin consumers read them, not because arbitrary YAML keys acquire behavior on their own |

Visibility here controls presentation. Private projects can still have publicly presented descriptions and project blogs while their repository links are omitted. `none` filters the inspected lists and menu; this review does not establish removal of pages, feeds, sitemaps, or search entries. No access-control claim should follow from those flags.

The existing `docs/diagrams/site-architecture/jekyll-template-dependencies.dot` maps static layout/include references and explicitly combines conditional branches. It is a useful research index, not a runtime execution trace; verify source edges before using a derived diagram in the series.

Editorial adjustment: Part 3 now establishes layout inheritance and reusable includes before metadata contracts. Part 5 follows one project through catalog input, generation, visibility grouping, navigation, and its dedicated blog, then connects that structure to series and discovery. This keeps the internal Jekyll architecture visible alongside the operational pipeline.

## CHANGELOG reconciliation: September 22, 2026

The Publisher confirmed the maintenance update is complete. The tracked code remains at `8c8846a9d1b98d967f9eee5c6da28db2bad035a7`; `CHANGELOG.md` is a separate working-tree modification, SHA-256 `52c79b6c39c80fb32038331a051eeb0d45de242ef32eabe67c615547ad0d32f7`. This review did not edit it. The diff adds three dated sections, not new runtime changes in this working tree.

- September 22: archive, source labels, pagination, and configuration agree at source level with `html/blog/all.md`, `html/_includes/blog_list.html`, `post_list_source.html`, `navigation.html`, `_config.yml`, and `docs/guides/blog-pagination.md`. Browser behavior has not been exercised here.
- September 17: `html/blog/technology.md` invokes the shared list with `exclude_series=true`. It filters discovery without changing the article category or canonical URL.
- September 13: optional captions exist in `blog_diagram.html`; `agent-skills` and `automation` exist in `html/_data/tag_taxonomy.yml`. No new rendered styling or accessibility qualification was performed.

The archive's description as chronological needs qualification: it calls the shared list, which sorts by `list_sort_key`, allowing update-notice promotion through `PostListMetadata`. Part 5 should describe effective discovery ordering rather than promise strict original-date chronology. Pagination is client-side over rendered entries, not separate Jekyll-generated page files.

The changelog explicitly distinguishes recorded changes from verified deployment dates. Retain that distinction, along with the existing unresolved search, operational invocation, and historical-documentation questions. None blocks a source-bounded introductory article.

[Part 1's packet](jekyll-site-tooling-part-01-packet.md) provides the next narrative outline and scoped evidence.

## Part 1 title and history follow-up: September 22, 2026

The Publisher asked for a Part 1 title distinct from the existing series installment “When a Local AI Stack Becomes an Operations System” and supplied a candid account of repeated Jekyll frustrations leading to extensions. Part 1 is now **Jekyll, One Problem at a Time**. The [packet](jekyll-site-tooling-part-01-packet.md) records selected earlier CHANGELOG entries as a problem-and-response sequence, including the initial shared blog/project structure, layout corrections, future-post/link/image fixes, a reverted Sass attempt, redirects, stable URLs, and later editorial features. The history remains source-bounded: recorded dates are not verified deployment dates, old FileWatcher work is not current use, and motivations beyond the Publisher's account are not inferred.
