# Part 1: Jekyll, One Problem at a Time

Status: pre-draft packet prepared September 22, 2026. The Publisher has since published Part 1. Its post and the series landing page live in Jekyll's source tree; the two drafts under this directory are superseded review copies. Series: **Beyond Static: Building a Publication System Around Jekyll**. See the [inventory](jekyll-site-tooling-inventory.md) for the source review and [journal](jekyll-site-tooling-review.md) for decisions.

## Editorial intent

Show an experienced developer how repeated publishing problems led to a connected set of Jekyll extensions. The project catalog supplies a current example of what those changes grew into; the CHANGELOG supplies a bounded history of earlier fixes. The reader should understand the system's responsibilities and why the rest of the series is worth following.

Use first-person authorial prose. The Publisher has supplied the project-catalog workflow, pre-commit/system-check usage, unused FileWatcher status, rate-limit motivation for local cards, and a firsthand account of Jekyll becoming frustrating enough to warrant extensions. That supports a candid opening, but does not establish a founding date, one dramatic migration, measured time saved, or a specific deployment incident. Present architectural interpretation as interpretation rather than undocumented personal history.

Target approximately 1,400 to 1,800 words. No runnable companion is needed for the introduction. Avoid turning the article into a directory listing or compressing all ten installments into miniature tutorials.

## Source inventory and identity

Tracked source: `8c8846a9d1b98d967f9eee5c6da28db2bad035a7`. Updated, uncommitted `CHANGELOG.md`: SHA-256 `52c79b6c39c80fb32038331a051eeb0d45de242ef32eabe67c615547ad0d32f7`. Series documents are separate working material. No workflow runs, browser sessions, tests, builds, or deployments are claimed by this packet. Source findings below reuse the recorded review and the targeted CHANGELOG follow-up.

| Source group | Purpose in Part 1 |
| --- | --- |
| `CHANGELOG.md`; Publisher's account | Recorded evolution and explicitly attributed motivation; dates are not verified deployment dates. Use the 20240220 and 20240223 entries, then selected 2025 and 2026 entries for the narrative arc |
| `utils/bin/fetch_og.py`: `load_repository_config`, `create_project_entry`, `generate_project_card`, `generate_project_files`, `main` | Project definition, local cards, override rules, and conditional scaffolding |
| `html/_layouts/project.html`, `page.html`, `default.html`; `html/_includes/project_lookup.html`, `header.html`, `navigation.html`, `projects_list.html` | Layout inheritance, shared catalog consumers, menu and project placement |
| `html/_includes/blog_list.html`, `filter_discovery_posts.html`, `post_list_source.html`; `html/blog/all.md`, `technology.md` | Project blogs, complete discovery archive, focused sections, and reused list policy |
| `html/_plugins/00_project_post_permalink.rb`, `01_short_link_injector.rb`, `02_post_list_metadata.rb` | Separate URL identity, short links, and discovery order |
| `utils/bin/jekyll-site`; `.pre-commit-config.yaml`; `utils/bin/check_site.sh`; `.github/workflows/jekyll.yml` | Preview, configured checks, and deployment responsibilities |
| `html/_includes/blog_diagram.html`, `source_code.html`; `html/_plugins/source_code_filter.rb`; `html/_layouts/post.html`; `utils/bin/article_audio.py` | Shared artifact presentation and optional audio workflows |
| `utils/bin/test_fetch_og.py`, `test_article_tts.py`, `test_article_audio.py`, `test_site_reliability_monitor.py` | Test inventory only, not passing-test evidence; no numerical or reliability claims in Part 1 |
| `html/_includes/engagement.html`, `giscus_comments.html`, `contact_form.html`, `getintouch.html`; `html/assets/js/contact-form.js`; `html/contact.md` | Configured discussion route and a client-side form that opens a prepared mail draft; Publisher reports no observed discussion use |

## Claim table

| Proposed claim | Evidence status | Wording limit |
| --- | --- | --- |
| A YAML catalog drives project publishing | Implemented; Publisher reports use | Describe the refresh/generation step before Liquid consumes generated data; an edit is not an instantaneous live-site deployment |
| New projects receive page/blog scaffolding | Implemented | Main entry calls scaffolding when the landing page is absent. Starter content still requires authoring and metadata review |
| Cards are generated locally after GitHub thumbnail rate limiting motivated a change | Implemented local generator; motivation supplied by Publisher | Metadata requests and fallback images remain; do not claim independence from GitHub |
| Layout inheritance and includes avoid duplicating presentation | Implemented | Use one concrete dependency chain, not a universal claim that no duplication remains |
| Visibility controls project presentation | Implemented | Private projects can be publicly described; `none` suppresses inspected listings, not proven access or output removal |
| Project blogs and the archive reuse list machinery | Implemented | Ordering is update-aware; client-side pagination is not server-side pagination |
| Public URL identity can survive source reorganization | Implemented under explicit metadata conditions | Frozen project slug, retained basis, and publication date matter; avoid universal rename guarantees |
| Editorial preview can show upcoming work | Implemented | Both serving modes are development-mode; production is a separate build path |
| Pre-commit and system checks are used | Publisher report plus inspected configured paths | Exact installed invocation chain remains to be traced for Part 8; local checks and CI are not interchangeable |
| Figures, source, and narration are shared publishing features | Implemented | Describe responsibilities; avoid unverified browser compatibility and audio reliability assertions |
| Publication still includes human editorial decisions | Publisher instructions and opt-in audio mechanism | Do not imply the CI workflow implements every review gate described by the author |
| Posts offer GitHub Discussions comments; contact form opens a mail draft | Implemented in includes and browser JavaScript; Publisher reports no observed use | A `mailto:` handoff depends on the visitor's mail client; no claim that the site delivered or stored the message |

## Recorded problem and response sequence

These are selected CHANGELOG entries for the introduction, not a claim that each item remains active or that the heading date is a deployment date. The entries are arranged by the chronology they record; the file itself contains some older sections out of order.

| Recorded entry | Publishing problem and recorded response | Current-claim boundary |
| --- | --- | --- |
| `20240220_01-rel` | Inconsistent blog display and project layout led to a shared blog list, standard project directories, templates, and pre-commit check work | Verify today's list, project hierarchy, and installed check path independently |
| `20240223_01-rel` and `_02-rel` | Home pagination, project blog integration, and incorrect layout variables prompted template and include fixes | Illustrates iterative corrections, not today's exact pagination implementation |
| `20250320_01-rel` | URL-encoded link handling, future-dated posts, and project image presentation needed targeted repairs | Do not claim these were the only causes of later wrappers or validators |
| `20250626_01-rel`, `_02-home-blog-improvements`, and `_03-rel` | A missing SEO plugin broke builds; discovery was revised; a Sass modernization attempt was reverted after compatibility trouble | The reverted Sass work is a useful example of limits, not a feature in today's site |
| `20250701_03-rel` | Redirect mismatches and service complexity led to redirect and script changes | The same historical entry includes FileWatcher, which the Publisher says is unused now |
| `2026-08-16`, `2026-08-18`, and `2026-08-21` | Update-aware discovery, source reorganization, stable short links, frozen project URLs, and compatibility redirects addressed different kinds of identity drift | Source and URL contracts must be described separately |
| `2026-08-25` through `2026-09-22` | Taxonomy, listening, retained narration, diagram presentation, focused listings, and a complete archive expanded editorial and reader workflows | The 2026-09-22 archive sorts by effective discovery date, including promoted updates |

The Publisher's “problem, let's solve it” account is the narrative thread. The table supports a cumulative argument; it does not prove a single linear design plan, a time-saving metric, or uninterrupted use of every historical component.

## Conflict dispositions and exclusions

- Archive chronology: say update-aware discovery order. The shared sort can promote revised articles.
- Older short-link documentation: use current immutable-basis behavior, with fallback limitations; do not repeat the obsolete move-breaks-link table.
- FileWatcher: excluded by the Publisher's correction. Jekyll's own content watching is a separate mechanism.
- Search: omit claims of a working deployed index or project-specific search filter. Local indexing and deployment configuration differ in the inspected source.
- Monitoring: mention as an area for later investigation, without declaring a running schedule or treating placeholder methods as working checks.
- Check runners: do not offer broad execution instructions in this introduction; some steps repair, refresh, stage, or replace files.
- Historical timestamps: the updated changelog supports recorded evolution, not verified deployment timing. Its dirty-tree identity is explicitly retained above.
- The older CHANGELOG is not strictly chronological and includes superseded approaches, including FileWatcher and a reverted Sass migration. Select events by their relevance to the currently explained behavior; label superseded work when mentioned.

These dispositions allow the introductory narrative to proceed without speculative fixes or an exhaustive runtime audit.

## Privacy review

Use a fictional project named **Example Tool**, a neutral repository owner, and `site.example` if a public URL is needed. Explain catalog fields through a minimal invented example rather than quoting private entries. Repository-relative implementation paths may identify the mechanism; omit absolute workstation paths, environment contents, hostnames, ports, credentials, analytics identifiers, recipients, voice identities, and real audio manifests.

No unpublished project descriptions, unrelated article prose, logs, voice recordings, or conversations belong in the article. The Publisher's workflow comments may be paraphrased as author-supplied history. Inspect final prose for accidental private values before technical review.

The drafts use no recipient address, repository identifier, discussion identifier, analytics value, hostname, private endpoint, or project catalog entry. They mention GitHub Discussions and a mail-client handoff as public mechanisms, and attribute the lack of observed participation to the Publisher's report rather than site analytics.

## Detailed narrative outline

### Opening: Adding a project means more than adding a page

Open with the Publisher's own observation that Jekyll was becoming frustrating as ordinary publishing exposed repeated problems. Give a short, concrete sequence grounded in the CHANGELOG: inconsistent blog/project presentation led to shared lists and templates; later, future dates, links, images, and builds demanded additional checks and fixes. Then use adding a project to the catalog as the present-day example: card, index and menu placement, landing page, and blog home now come from one connected workflow. Do not invent a single incident as the cause of the whole architecture.

### 1. The catalog became a publishing input

Briefly connect the early recorded move to project directories and templates with the current catalog workflow. Describe authored repository settings and overrides, generated project metadata, and the refresh step connecting them. Explain public/private/undisplayed presentation choices without suggesting authentication. Introduce the rate-limit motivation for local cards as another example of solving a problem as it arose. Save rendering and cache details for Part 5.

### 2. Learning the hierarchy changed how I built pages

Follow `project` through `page` to `default`. Show the shared header/menu on one branch and project lookup/blog list on another. Explain how each page supplies content and metadata while shared templates supply repeated structure. Connect this to the CHANGELOG's early template and layout corrections without implying today's hierarchy arrived in one change. Jekyll's hierarchy becomes the organizing structure for a growing publication.

### 3. One body of writing needs several ways in

Move from a project's own blog to focused editorial sections, series reading order, and the complete archive. Explain why an updated article may reappear in discovery without changing its original date or series position. Use archive source labels and configurable pagination as brief examples of shared machinery serving different views. Preserve the distinction between organization and URL identity.

### 4. The work around the build matters too

Describe upcoming-content preview, author-used pre-commit/system checks, and the narrower configured CI build and verification path. Link these to recorded future-post, link, image, build, and permalink corrections across the CHANGELOG. Keep the sequence honest: local repair/refresh tools, human review, and CI are different responsibilities, not one automatically enforced conveyor belt. Introduce stable links as a promise that survives routine editorial work.

### 5. Technical articles bring their own artifacts

Connect shared diagram viewing and source disclosures to reader needs. Explain that the highlighted code comes from the downloadable artifact. Introduce listening as another way to review rendered prose, and distinguish it from opting into retained public narration. Keep implementation details for Parts 6 and 7.

### Current State

Describe the result as a Jekyll site with a project catalog, reusable presentation, editorial views, and surrounding publication tools. It has accumulated conventions and some older utilities; the series will explain the paths actually used and mark unresolved evidence honestly. Avoid a feature-count scorecard or an operational certification claim.

### Next Work

Lead into Part 2's local preview workflow, then indicate that the series will work inward through templates and project data and outward through validation and publication. End with the next concrete question: how to review upcoming material while keeping the current publication view clear. Do not promise a reusable CMS or a wholesale rewrite.

## Figure brief and current assets

The Publisher requested visual assets during local review. The article now uses a shared banner and two source-backed diagrams: [visual asset record](jekyll-site-tooling-visual-assets.md). The project diagram connects authored catalog input to generation, scaffolding, shared Liquid, and visible project views. The URL diagram explains frozen project-post identity and redirects. Both were rendered from Graphviz sources and inserted where the corresponding prose appears. The wider publication and operations lifecycle remains a possible figure for the closing installment; do not imply FileWatcher, unverified schedules, private services, or an automatic human-approval gate in CI.

## Draft acceptance criteria

The draft should use the project lifecycle as its organizing example, distinguish authored inputs from generated outputs, explain the template hierarchy, preserve all claim limits above, and end with Current State and Next Work. It should remain first-person narrative with no invented incidents, timings, metrics, test results, or deployment claims. Review prose before commissioning banners, social copy, figures, or companion material.

## Review-draft handoff fields

At the Publisher's request, the article now lives at `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-09-22-jekyll-one-problem-at-a-time.md`, and the landing page lives at `html/blog/series/beyond-static-building-a-publication-system-around-jekyll.md`. The review copies in this folder are superseded. Local browser preview uses the September 22 source date, default image, permalink, short-link identities, and series navigation metadata. Those values should be reviewed before any commit or remote publication. The post is included in the landing page's Main Series list and has not been technically or editorially approved.
