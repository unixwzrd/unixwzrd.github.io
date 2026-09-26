# Jekyll Site Tooling Blog Series Handoff

## Project Status

Updated September 25, 2026. The Publisher has published Part 1 and asked to finish Part 2 and add a Hands-On companion where useful. Part 2 is already in the Jekyll post tree; Hands-On 2A now accompanies it in the local preview. Their October 1 dates are provisional until the Publisher settles publication timing. The source packet and visual assets are linked below.

- [Source inventory and evidence boundaries](jekyll-site-tooling-inventory.md)
- [Review journal](jekyll-site-tooling-review.md)
- [Part 1 evidence packet and narrative outline](jekyll-site-tooling-part-01-packet.md)
- [Part 1 review draft](jekyll-site-tooling-part-01-draft.md)
- [Series landing review draft](jekyll-site-tooling-series-landing-draft.md)
- [Part 1 visual assets and render sources](jekyll-site-tooling-visual-assets.md)
- [Part 2 evidence packet and local draft handoff](jekyll-site-tooling-part-02-packet.md)

The editorial spine is a concrete publishing problem, the implementation it produced, and its remaining limits. Keep ten main installments. Companions are optional and should earn their place through an independently useful exercise.

## Working Title

**Beyond Static: Building a Publication System Around Jekyll**

This is a provisional title. The series should sound like an engineering story about a site that accumulated real operational needs, not a generic Jekyll tutorial or a list of scripts.

## Purpose

The site began as a conventional Jekyll publication and gradually acquired a set of tools for previewing future work, validating metadata, preserving URLs, presenting technical artifacts, proofreading by ear, checking releases, monitoring the deployed site, and reducing the amount of manual work surrounding publication.

The series should explain why those tools became necessary, how they fit together, which ones are dependable today, and where the workflow still contains historical or experimental pieces. It should give readers useful patterns they can adapt without pretending this repository is a reusable site generator or a finished publishing product.

The narrative belongs in first person. The interesting story is not that Jekyll can render Markdown. It is how a static site became easier to operate after repeated publishing mistakes, browser differences, future-post review problems, link drift, diagram scaling, source-code downloads, and the discovery that listening to an article catches problems that visual proofreading misses.

## Audience

The primary audience is an experienced developer, technical writer, independent publisher, or small team running a static site without a full content-management system. Posts should remain approachable to readers who understand Markdown and Git but may not know Liquid, Ruby plugins, browser audio behavior, or GitHub Actions.

Lean technical when a choice needs teeth, but keep the argument readable. Explain the operational problem before showing implementation detail. Tables, diagrams, command examples, and short source excerpts are welcome when they reduce ambiguity.

## Publication Boundary

The Publisher has authorized local post-tree drafts and browser previews for this series. Part 1 has been published by the Publisher. This does not authorize commits, pushes, deployment, or remote publication of Part 2.

Keep research and review packets under `docs/publication/`. Parts 1 and 2 and the landing page are in the Jekyll source tree; their exact paths are in the linked packets. Do not rebuild or restart the watched local Jekyll server merely to make a source edit visible. Do not create alternate build destinations inside the repository. Commit, push, deployment, and remote publication remain separate decisions.

Before describing any tool as current, tested, deployed, automatic, or reliable, verify that claim against its present source, documentation, tests, workflow configuration, and retained operational evidence. The repository contains older utilities, backups, derived output, runtime files, and documentation that may no longer describe the active path.

## Initial Source Map

Start with these source groups. Narrow the list for each post rather than reading the whole repository indiscriminately.

### Governing and historical material

- `CHANGELOG.md`
- `README.md`
- `_config.yml`
- `Gemfile` and `Gemfile.lock`
- `docs/PROJECT_OVERVIEW.md`
- `docs/workflows/blog-publishing.md`
- `docs/workflows/post-updates-and-ordering.md`
- `docs/tools/pre-commit-checks.md`
- `docs/guides/`
- `docs/templates/blog-templates.md`
- `.github/workflows/jekyll.yml`

### Local service and preview tooling

- `utils/bin/jekyll-site`
- `utils/bin/site-service`
- `utils/bin/check-site`
- `utils/bin/check_site.sh`
- `utils/bin/checks/`
- `utils/README.md`

### Content structure and presentation

- `html/_layouts/`
- `html/_includes/`
- `html/_plugins/`
- `html/blog/`
- Representative posts under `html/_posts/`, selected only when needed to verify rendered conventions
- Site styles and JavaScript referenced by the applicable layouts or includes

### Metadata, taxonomy, and URL integrity

- `scripts/backfill_short_url_front_matter.rb`
- `scripts/check_tag_taxonomy.rb`
- `scripts/list_tags.rb`
- `scripts/verify_short_url_redirects.rb`
- `scripts/verify_project_permalink_redirects.rb`
- `html/_plugins/00_project_post_permalink.rb`
- `html/_plugins/01_short_link_injector.rb`
- `html/_plugins/02_post_list_metadata.rb`
- `html/_plugins/03_tag_taxonomy_validator.rb`
- `html/_plugins/permalink_validator.rb`
- `html/_plugins/normalize_internal_links.rb`
- `html/_data/tag_taxonomy.yml`

### Project publishing and search

- `utils/bin/fetch_og.py` and `utils/bin/test_fetch_og.py`
- `html/_data/repos.yml`, reviewed for private entries before quoting
- `html/_data/github_projects.yml`, generated project metadata
- Project layouts, listings, and scaffolded pages under `html/`
- `utils/bin/checks/05_update_project_data.sh`
- `html/assets/js/site-search.js`
- `run_pagefind_index` in `utils/bin/jekyll-site`, compared with the deployment workflow

### Technical-artifact presentation

- `html/_includes/blog_diagram.html`
- `html/_includes/source_code.html`
- `html/_plugins/source_code_filter.rb`
- `html/tools/diagram-viewer.html`
- Diagram-related styles and JavaScript
- `docs/diagrams/`
- `utils/bin/render-jekyll-template-graph`

### Proofreading and retained narration

- `utils/bin/article-tts`
- `utils/bin/article_tts.py`
- `utils/bin/article-audio`
- `utils/bin/article_audio.py`
- `utils/etc/article-audio.defaults.json`
- `utils/bin/test_article_tts.py`
- `utils/bin/test_article_audio.py`
- `html/_includes/post_audio.html`
- The development-only proofreader integration in the applicable post layout and assets

### Monitoring, maintenance, and publishing support

- `utils/bin/site_crawl_check.py`
- `utils/bin/site_reliability_monitor.py`
- `utils/bin/manage_monitoring_pages.py`
- `utils/bin/periodic_monitor.sh`
- `utils/bin/post_commit_monitor.sh`
- `utils/bin/scheduled_tasks.py`
- `utils/bin/setup_site_monitoring.sh`
- `utils/bin/setup_crontab.sh`
- `utils/bin/push-social-media`
- `utils/bin/push-twitter`
- `utils/etc/site_monitor_config.json`, read only after privacy review
- `html/_includes/support_block.html`
- `html/_includes/giscus_comments.html`
- `html/_includes/content_footer.html`

Treat `utils/output/`, PID files, logs, caches, `.DS_Store`, `__pycache__`, backups, and generated site output as derived or runtime material unless current source explicitly makes them part of a documented interface.

## Revised Ten-Part Outline

### 1. Jekyll, One Problem at a Time

Tell the cumulative story through several concrete problems and the changes that answered them. The Publisher describes Jekyll as increasingly frustrating until extending the site became the practical way forward. Use the older CHANGELOG entries to establish the sequence: shared blog lists, project directories and templates, early pagination and check work; then link and image corrections, preview and URL repairs; then frozen identities, metadata, technical artifacts, listening, and the complete archive. The CHANGELOG records changes, not verified deployment dates or a single turning point. Explain why editing Markdown became only one part of publishing without reciting every feature or claiming all historical tooling remains in use.

The architecture diagram should show the authoring tree, local operational tools, Jekyll build, validation gates, generated site, and deployed site without implying that every historical utility is in the active path.

### 2. A Local Jekyll Server I Can Actually Operate

Tell the story of wrapping Jekyll startup, restart, process checks, future-post display, draft review, environment selection, and optional refresh work in a predictable command. The wrapper defaults to future, draft, and unpublished content; `--current` removes those inclusion flags. Both serving modes use the development environment, so current-content preview is not identical to a production build. Explain why ordinary content changes should not trigger manual rebuilds or restarts. Do not infer a public `status` command from internal process checks.

Inspect `jekyll-site`, PID handling, and documented service behavior. The Publisher confirms that FileWatcher is not in use; exclude it from the active workflow and do not spend further research on it. If explaining `site-service`, distinguish its optional watcher orchestration from actual operator use. Keep process-management claims bounded to the current scripts and tested operating systems.

**Hands-On 2A:** Build a small, isolated Jekyll fixture in current and review modes with a two-choice wrapper and a check of the generated HTML. It deliberately exercises the inclusion flags without starting a server or copying this site's operational side effects.

### 3. Building the Site from Shared Layouts, Includes, and Data

Explain the template hierarchy first: project pages inherit the project layout, which inherits page and then default; default supplies the shared site shell. Trace how includes reuse project lookup, navigation, post filtering, list metadata, and pagination instead of copying presentation into each page. Use the existing template-dependency graph as a research aid, verifying its edges against current source before reuse. Then cover the metadata contract behind layouts, categories, content types, tags, images, dates, update notices, series fields, and audio. Explain why permissive YAML is not enough once multiple listings, taxonomies, feeds, comments, social metadata, and automated checks depend on those fields.

This post should address the difference between current canonical validators and older scripts whose assumptions may have drifted. Do not hide conflicting validators; identify which path the build and CI actually enforce.

**Possible Hands-On 3A:** Validate a small set of invented posts against a closed tag taxonomy and required front-matter contract.

### 4. Stable URLs in a Repository That Keeps Moving

Explain the transition from title-derived project paths to required immutable `permalink_slug`, compatibility redirects, immutable `short_link_basis`, deterministic short URLs, and publication dates as part of canonical identity. Show why a source file can move while a public URL and discussion identity must remain stable. Leave update-driven list ordering to Part 5.

Use the permalink and short-link plugins, backfill script, redirect verifiers, and update-ordering documentation as the primary sources. Clearly separate canonical URLs, redirect paths, and social short links.

**Possible Hands-On 4A:** Generate and verify deterministic short links without relying on a hosted shortening service.

### 5. From a YAML Project Catalog to a Project Publishing System

Make one new project the main narrative example: define it in the YAML catalog, generate its metadata and local card, scaffold its landing page and blog directories, then let shared Liquid consumers place it in project listings and navigation. Explain public, private, and undisplayed project choices as presentation states, with private repository links omitted and `none` entries filtered from the inspected lists. Do not describe these fields as access controls or assume they remove generated pages. Trace catalog order through generation to display.

Cover series metadata, main articles, lettered Hands-On companions, previous and next navigation, series landing pages, category separation, discovery lists, excerpts, and update-aware ordering. The story should focus on helping readers move coherently through related material while keeping tutorials out of the general Technology stream.

Extend the story to project publishing: repository configuration, fetched GitHub and OpenGraph metadata, manual overrides, cached images, generated cards, and scaffolded project files. Identify which values the author owns and which outputs the generator maintains. Use `fetch_og.py` and its tests as primary evidence without implying every build refreshes project data. The Publisher reports that GitHub thumbnail rate limiting motivated locally generated cards; use that as attributed engineering history. The implementation still fetches repository metadata and retains fallback image paths. Scaffolding runs from the main generator when the project landing page is absent; it is not an unconditional repair of every missing child file. The starter introduction is a draft-marked template requiring editorial work, not an automatically completed article.

Use the complete `/blog/all/` archive to demonstrate reuse: source labels resolve through section/project data, page-size choices come from configuration, and ordinary links preserve pagination state in the URL. The archive uses the shared update-aware discovery sort; do not call it strictly ordered by original publication date. Explain the separate Technology index and its exclusion of series without implying a category or URL change.

Include a data-flow diagram showing how authored metadata and generated project data reach landing pages, series indexes, navigation, and discovery lists. Explain publication order, series order, and update-driven discovery as separate decisions. Treat Pagefind search as a bounded subsection: the local wrapper invokes indexing, but the inspected deployment workflow does not. Resolve that evidence gap before claiming production search works. Avoid presenting Liquid conventions as universally applicable outside this site.

**Possible Hands-On 5A:** Combine invented repository metadata and manual overrides into a project card without network access.

### 6. Diagrams and Source Code That Behave Like Editorial Content

Explain why raw ASCII diagrams, unconstrained SVGs, forced downloads, and inconsistent code blocks were not good enough. Cover reproducible Mermaid or Graphviz sources, dark-background rendering, constrained responsive presentation, click-to-expand viewing, Escape-safe overlays, centered captions, and collapsed source viewers with explicit download actions.

The key distinction is between the editorial diagram, the reproducible source, the generated SVG or PNG, and the viewer. For source code, show that the inline highlighted view reads the downloadable artifact itself, with real-path containment under `assets/code`. This avoids maintaining a separate excerpt but does not prove the program works. Verify the separate viewer page and overlay behavior before describing either interaction.

**Possible Hands-On 6A:** Add a responsive, accessible SVG viewer and a collapsed source-code disclosure to a minimal Jekyll site.

### 7. Proofreading a Blog by Listening to It

Tell the story of noticing voice, rhythm, repeated phrasing, and first-person inconsistencies only after hearing an article aloud. Explain rendered-body extraction, removal of page furniture, raw URLs, code blocks, tables, and media while retaining visible link text and inline code words, paragraph-aware chunking, selection and cursor playback, pause and restart controls, Safari behavior, the loopback relay, and why dynamic browser playback should remain ephemeral.

Keep the main article centered on the editing experience. Introduce retained narration as a separate publication decision and move its implementation detail to companion 7B. Freshness checks include cleaned prose, source identity, a public narration profile, chunk size, and the MP3 hash. Private voice or model changes require an intentional profile change; the manifest does not automatically discover them.

Describe staged replacement precisely: the MP3 and manifest are replaced separately, not as one atomic transaction. A synthesis failure before replacement preserves the previous MP3; broader crash-recovery claims require additional evidence.

Do not publish private TTS endpoints, voice samples, transcripts, model paths, voice aliases, or cloned identities. Do not imply byte-level streaming if the active implementation buffers complete audio chunks.

**Possible Hands-On 7A:** Extract readable article prose from rendered HTML and produce a dry-run chunk manifest without invoking a speech engine.

**Possible Companion 7B: From Proofreading to Published Narration.** Explain manifests, temporary synthesis artifacts, freshness, replacement failure boundaries, and author-approved `audio` front matter. A model-free exercise can compare invented manifests and fixture audio hashes.

### 8. Checks, Repairs, and the Gates Before Deployment

Map the local checks and GitHub workflow: environment, permalinks, Jekyll doctor, internal and external links, large files, builds, required files, Liquid syntax, front matter, navigation, image paths, taxonomy, short URLs, and redirects. Explain the value and cost of layering quick focused checks ahead of a full production build.

Separate observational checks from source repairs, generated-data refreshes, Git staging, and build-output replacement. The numbered suite includes mutating steps and must not be recommended as a read-only audit. Show the GitHub Actions gates separately from the broader local suite and optional pre-commit configuration. Hook configuration does not prove installation. Identify duplicate, historical, or partially overlapping checks rather than claiming the directory is a perfectly unified framework. Report commands and pass counts only after current execution against an identified revision.

**Possible Hands-On 8A:** Construct a small fail-fast prepublication check runner with independent, diagnosable gates.

### 9. Monitoring a Static Site After Deployment

Cover critical-page checks, crawling, image and link validation, missing-page tracking, scheduled execution, logging, and notification boundaries. Explain why a successful build does not prove that the deployed site, redirects, remote assets, or external dependencies remain healthy.

Separate implemented monitoring from configured scheduling and from any currently active daemon or cron job. Identify placeholder maintenance methods that log completion and return success without performing the named work; exclude them from capability claims. Let runtime evidence determine this article's depth. Do not expose recipient addresses, credentials, OAuth data, internal paths, private endpoints, or operational logs.

### 10. Closing the Publishing Loop Without Pretending It Is a CMS

Bring the workflow together: drafting, technical review, local preview, diagrams and code, TTS proofreading, taxonomy and URL checks, social drafts, support and discussion blocks, future dates, commit and push boundaries, GitHub Pages deployment, and post-publication monitoring.

End with what is still manual and why. Human review, publication authority, social posting, donation messaging, and editorial judgment should remain visible rather than being described as defects awaiting total automation.

The final diagram should be a lifecycle with explicit human gates, not a fully automatic conveyor belt.

## Editorial Rules

- Write natural Markdown without hard-wrapping prose.
- Use first person and tell the engineering story through concrete problems and corrections.
- Favor prose over outline-like bullet accumulation in the finished articles.
- Avoid em dashes and en dashes in narrative prose.
- Use tables when they clarify contracts, state distinctions, or tool ownership.
- Use reproducible Mermaid, Graphviz, or native site diagrams rather than ASCII art in published posts.
- Give diagrams a dark or transparent canvas appropriate for the site, constrained display sizing, full-screen viewing where useful, accessible alternative text, and centered captions when the caption labels the figure.
- Keep code examples small enough to understand. Put substantial runnable material into reviewed companion packages and expose it through the site's source viewer.
- Do not invent benchmark results, test counts, versions, dates, deployment state, causality, or reliability claims.
- Do not describe a script as automatic merely because it can be scheduled.
- If sources conflict, stop and record the conflict instead of silently choosing the most convenient account.
- End each main installment with `Current State` and `Next Work`.
- Prepare social drafts, a distinct series-consistent banner, diagrams, and optional Hands-On material only after the canonical article is technically approved.
- Return drafts for human review. Do not publish, commit, push, deploy, restart services, or change site behavior without explicit authorization.

## Privacy and Security Review

Every review packet must identify and remove or generalize:

- Usernames, home directories, private repository paths, temporary paths, and mounted-volume names
- Hostnames, LAN addresses, public addresses, ports that reveal private topology, peer identifiers, and tunnel destinations
- API keys, OAuth material, cookies, session values, webhook URLs, SSH material, environment-variable values, and credential assignments
- Email addresses, notification recipients, analytics identifiers, private social account details, donation account internals, and unpublished customer or supporter information
- TTS endpoints, private voice aliases, recordings, transcripts, model paths, and cloned voice identities
- Draft text, private conversations, prompts, unpublished articles, model-generated artifacts, and operational logs not approved for publication
- Local service state, PID files, schedules, and monitoring configuration that could expose the workstation or deployment environment

Commands in public prose should use neutral placeholders such as `site.example`, `user`, `project-root`, and `127.0.0.1` only where loopback is truly part of the public design. Sanitization must not change a technical claim about ownership, scope, or behavior.

## Required Pre-Draft Packet for Each Post

Before drafting an installment, produce:

1. A source inventory listing the files, tests, workflow runs, and commits actually used.
2. A fact table separating implemented, tested, locally used, deployed, proposed, historical, and deferred behavior.
3. A privacy review covering every private value or artifact that must be omitted or generalized.
4. A conflict and drift report identifying documentation, scripts, tests, and runtime assumptions that disagree.
5. A detailed narrative outline describing the problem, turning point, implementation, limits, Current State, and Next Work.

Use Git history only when the post needs to explain why behavior changed, when current documentation points to a change requiring verification, or when a specific claim cannot be established from the current tree. Do not turn routine archaeology into filler.

## Suggested Review Workflow

Maintain the [series review journal](jekyll-site-tooling-review.md), preserving existing entries and prepending new ones. Each entry should include local date, time, time zone, author, role, decision, evidence reviewed, changes requested or made, and the next gate.

Keep technical approval, editorial approval, and publication authority separate. A technically correct draft is not automatically authorized for the Jekyll post tree, and a locally rendered post is not automatically authorized for deployment.

## Next Assignment

The [initial inventory](jekyll-site-tooling-inventory.md) records the source review and open evidence gaps. The maintenance CHANGELOG has been reconciled, and the Publisher has published Part 1. Part 2 and Hands-On 2A are in the Jekyll source tree for local review, with the [Part 2 packet](jekyll-site-tooling-part-02-packet.md), downloadable lab, and visuals. Next collect the Publisher's voice and factual edits, settle both publication dates, and review the final rendered pair before any remote publication. For later installments, continue to answer:

- Which commands are current entry points and which are backups, compatibility paths, or historical utilities?
- Which scripts have tests, and what do those tests actually prove?
- Which tools are invoked locally, by Git hooks, by GitHub Actions, by cron or service management, or only by explicit operator choice?
- Which generated files are retained artifacts and which are disposable runtime output?
- Which documentation reflects current behavior and which instructions have drifted?
- Which ten-part boundaries should be merged, split, or reordered after the evidence is known?

Maintain the inventory, fact taxonomy, privacy map, and outline within the authorized series documents. Investigate site behavior read-only; record tooling and operator-documentation corrections for later implementation. Planning approval is not technical approval of an article.

## Handoff Prompt

```markdown
You are preparing a technical blog series about turning a Jekyll site into a practical publication system through local tooling, metadata contracts, stable URLs, technical-artifact presentation, TTS proofreading, validation, deployment checks, and monitoring.

Read `docs/publication/jekyll-site-tooling-blog-series.md` and its linked inventory and review journal. Follow the Next Assignment without repeating completed discovery. Use the current repository as the primary authority and distinguish active behavior from historical scripts, generated output, configuration, documentation, and proposed work.

Before drafting any post, produce the required source inventory, fact table, privacy review, conflict and drift report, and detailed narrative outline. Do not expose private configuration, credentials, topology, paths, voice material, analytics data, conversations, unpublished drafts, or operational logs. Do not invent test results, deployment state, dates, versions, causality, or reliability claims.

Write in a natural first-person engineering voice, with prose carrying the story and tables, diagrams, and code supporting it. Avoid em dashes and en dashes in narrative prose. Use reproducible dark-site diagrams instead of ASCII art. End articles with Current State and Next Work.

Keep evidence packets and review material under `docs/publication/`. The Publisher has authorized local browser drafts under the Jekyll post tree; use a provisional future date until the publication date is settled. Do not commit, push, deploy, or remote-publish without Publisher direction. Do not rebuild or restart the watched Jekyll server merely to make an ordinary source edit visible.
```
