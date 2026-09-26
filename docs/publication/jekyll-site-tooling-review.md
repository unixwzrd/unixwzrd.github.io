# Jekyll Site Tooling Series Review Journal

Preserve entries and prepend new ones. Planning, technical review, editorial approval, and publication authority are separate decisions.

## 2026-09-26 09:18 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Hands-On 5A editor. **Decision:** Make the existing offline lab directly inspectable after the Publisher asked for the companion.

**Evidence reviewed:** Current Hands-On 5A post and packaged runner, the project generator, the lab's baseline result, and the local preview state. The Publisher is restarting the Jekyll server, so Codex did not start or stop it.

**Changes:** Added `--reorder` and `--show-hidden` runs to the invented lab, printed generated order, repository-link presence, override result, and starter-file summary, updated the post and README instructions, and refreshed the ZIP and checksum. The live generator and catalog were untouched.

**Validation:** Baseline and both variations passed with no network access. ZIP checksum and archive integrity passed. After the Publisher restarted the server, the Hands-On route, ZIP, and runner source returned HTTP 200. Playwright showed the new command sequence and comparison text in the rendered page. `git diff --check` passed.

**Next gate:** Publisher reviews the companion's voice and exercise size in the local browser.

## 2026-09-26 05:58 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 5 author and local reviewer. **Decision:** Put the next main installment and an offline Hands-On 5A in the Jekyll post tree for the Publisher's browser review. October 22 remains a provisional local preview date.

**Evidence reviewed:** Current `fetch_og.py` and tests, project and Blog YAML consumers, navigation and project layouts, series/discovery paths, prior installments, the Publisher's corrections, and the pushed series state. The [Part 5 packet](jekyll-site-tooling-part-05-packet.md) records the claim limits and privacy boundary.

**Changes:** Added Part 5 and Hands-On 5A, linked Part 4 forward, generated a series-consistent banner and editable project/Blog data-flow diagram, and packaged an invented offline generator lab with source and checksum. Updated the series handoff and visual record. No production generator, template, menu, or deployment behavior changed.

**Validation:** Future-inclusive Jekyll build, short-link check, taxonomy check for 79 posts, all 12 `fetch_og.py` tests, extracted lab assertions, ZIP checksum, SVG parse, local HTTP routes, mobile Blog dropdown, and `git diff --check` passed. Playwright found only Giscus 404s for discussions missing on the local preview routes. No commit, push, or remote deployment occurred.

**Next gate:** Publisher reviews the Part 5 pair for voice, factual emphasis, lab size, and dates before any remote publication decision.

## 2026-09-25 22:05 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 3 editorial and Part 5 architecture reviewer. **Decision:** Give YAML-driven dropdown ordering and custom front-matter fields explicit treatment in the series, following the Publisher's corrections.

**Evidence reviewed:** `navigation.html`, `header.html`, `blog_sections.yml`, Blog hub, Projects page and list include, generated project data flow in `fetch_og.py`, series index, discovery metadata plugin, post layout and audio include, and responsive dropdown styles. Project and Blog menus have different data and ordering rules; front-matter extensions require Liquid or plugin consumers.

**Changes:** Added a first-person paragraph to Part 3 explaining that custom front-matter fields acquire behavior through site code, with verified series, update, and audio examples. Expanded Part 5's outline to trace the two YAML-to-dropdown paths, project grouping, fixed menu links, distinct ordering rules, and build-time generation. Updated the source inventory with those distinctions.

**Validation:** The revised Part 3 paragraph rendered in the watched local preview. Source review confirmed the menu and front-matter consumers; `git diff --check` passed. No menu behavior, service, commit, push, or deployment changed.

**Next gate:** Publisher reviews Part 3's added paragraph. Before drafting Part 5, verify the responsive menu behavior in a browser and use invented project data in public examples.

## 2026-09-25 22:02 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Reuse and packaging reviewer. **Decision:** Record a candidate path for readers to reuse selected Jekyll tools, starting with the short-link mechanism after an explicit package license is chosen. Do not present the existing Hands-On archives as installable software.

**Evidence reviewed:** Hands-On 2A/3A/4A archives and source, active short-link and taxonomy plugins, source-viewer filter, project generator, local service wrapper, repository README and LICENSE, and official Jekyll documentation for `_plugins`, gem-based plugins, and themes.

**Changes:** Added the [reuse packaging plan](jekyll-site-tooling-reuse-packaging.md) and linked it from the series outline. It ranks short links, taxonomy, project publishing, technical-content presentation, and local operations by extraction effort; defines a short-link pilot with a clean sample site and output checks; and records that `html/` is currently all rights reserved while `utils/` and `scripts/` are MIT-licensed. No license, production code, archive, or site behavior changed.

**Validation:** Checked the archive contents, repository license text, and plugin/wrapper dependencies; `git diff --check` passed. This is a packaging proposal, not a released or independently installable component.

**Next gate:** Publisher decides which component and license, if any, to prepare for external reuse. Build and test a concrete isolated package before any publication decision.

## 2026-09-25 21:59 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Series architecture and editorial reviewer. **Decision:** Make the multi-section publication model and operating automation explicit across later installments, following the Publisher's direction.

**Evidence reviewed:** `blog_sections.yml`, Blog hub, Technology/Hands-On/Series and archive pages, shared discovery filter, project layout and listing, `fetch_og.py` scaffolding path, `jekyll-site`, `check_site.sh`, this checkout's installed Git pre-commit hook, `.pre-commit-config.yaml`, and the Pages workflow. General is configured but currently hidden from the Blog hub. The installed hook invokes the numbered check suite with project-data refresh skipped; the separate pre-commit framework config and CI workflow have different scopes.

**Changes:** Added a cross-series map to the outline. Part 5 now leads with distinct article sections, series, and project update blogs before following one YAML-defined project through generation, landing page, navigation, and its posts. Part 2 explicitly owns service lifecycle; Part 8 compares local commit checks, opt-in link checks, and CI; Part 10 joins the different content routes in the editorial lifecycle. The next assignment now carries that structure forward. No Jekyll source or scripts changed.

**Validation:** Rechecked the outlined routes and tool boundaries against current source; `git diff --check` passed. This was a planning change, not a test of every configured check or a remote deployment. No service was restarted, committed, pushed, or deployed.

**Next gate:** Publisher reviews the revised series emphasis. Before drafting Part 5 or Part 8, refresh the specific source and operational evidence those articles will claim.

## 2026-09-25 21:55 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 4 editorial reviewer. **Decision:** Make site ownership and redirect control the central short-link advantage, following the Publisher's clarification.

**Evidence reviewed:** The Publisher's statement that the site controls its own short links and can maintain them when page-naming conventions change; the current `short_link_basis` and redirect behavior; existing Part 4 and Hands-On 4A drafts.

**Changes:** Added the ownership rationale to the article opening, explained how a frozen basis preserves the shared `/s/` path while a changed full-length URL needs a separate redirect, and echoed that motivation in Hands-On 4A. Updated the Part 4 packet and series outline to retain the distinction.

**Validation:** Both local pages rendered the revised paragraphs, and `git diff --check` passed. No service was restarted, committed, pushed, or deployed.

**Next gate:** Publisher reviews the Part 4 pair for voice and technical emphasis before deciding publication timing.

## 2026-09-25 21:53 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 4 editorial reviewer. **Decision:** Put the Publisher's stated reason for building short links into the article, ahead of the hashing mechanics.

**Evidence reviewed:** The Publisher's correction that short links serve X/Twitter, Bluesky, and other character-limited social posts and were built into this Jekyll site instead of delegated to an external shortening service; current Part 4 and Hands-On 4A prose; the existing short-link plugin and redirect flow reviewed in the Part 4 packet.

**Changes:** Reworked the main article's opening and short-link section in the Publisher's first-person voice, and added the same motivation to the Hands-On introduction. Updated the Part 4 packet and series outline so later editing retains the distinction between why the feature exists and how its code works.

**Validation:** Both edited articles rendered the new wording in the watched local Jekyll preview. `git diff --check` passed. No service was restarted, committed, pushed, or deployed.

**Next gate:** Publisher reviews the revised Part 4 pair and settles publication timing.

## 2026-09-25 21:40 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 4 and Hands-On 4A author and local reviewer. **Decision:** Continue the series with a source-bound explanation of canonical project URLs, declared legacy redirects, and deterministic short links. Keep October 15 as a provisional local review date.

**Evidence reviewed:** Current project-permalink and short-link plugins, backfill and generated-output verifiers, Pages workflow, representative front matter, August 18 and 21 changelog entries, prior installments, and the Publisher's instruction to continue. The [Part 4 packet](jekyll-site-tooling-part-04-packet.md) separates implemented behavior, configured checks, historical claims, drift, and privacy limits.

**Changes:** Added Part 4 and Hands-On 4A to the local Jekyll post tree, linked Part 3 forward, created a series-consistent banner and editable Graphviz URL diagram, and packaged an isolated three-case Ruby lab using a byte-for-byte snapshot of the active short-link module. Updated the series outline and visual record. No production plugin or URL behavior changed.

**Validation:** Clean extraction passed the lab ZIP checksum and all three cases. The main post, companion, series listing, short redirect, diagram, ZIP, and source-viewer assets returned HTTP 200. Playwright showed both articles with their expected series context and sections; its console errors came from Giscus looking for discussions that do not yet exist for these local routes. The short-link front-matter check, taxonomy check for 77 published and scheduled posts, future-inclusive generated short-link and project redirect verifiers, SVG XML parse, and `git diff --check` passed. No commit, push, or deployment occurred.

**Next gate:** Publisher reviews Part 4 and 4A for voice, technical emphasis, and exercise size before dates or remote publication are decided.

## 2026-09-25 21:13 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Hands-On 3A author and local reviewer. **Decision:** Add a runnable companion to Part 3 that shows the current taxonomy plugin's actual limits. Keep the October 8 date provisional for local browser review.

**Evidence reviewed:** Current `html/_plugins/03_tag_taxonomy_validator.rb`, the site's taxonomy data, series metadata and source-code include conventions, Part 3's metadata diagram, the existing Hands-On 2A package pattern, and the author's published voice references.

**Changes:** Added a first-person Hands-On 3A post and linked it from Part 3. Packaged a byte-for-byte snapshot of the active taxonomy plugin with invented data and seven cases, an isolated runner, retained build logs, a ZIP, and a SHA-256 checksum. Reused Part 3's banner and metadata diagram. Updated the Part 3 packet, series outline, and visual record. No site tooling or production content was changed.

**Validation:** A clean extracted archive passed SHA-256 verification and all seven cases. Valid metadata, a missing series order, and an old-tag draft were accepted; unknown, aliased, and duplicate tags and an unknown content type were rejected. The lab's accepted missing series order proves only that this plugin does not check it; the fixture has no series index. The local Hands-On post, parent companion link, series listing, code viewers, ZIP, and checksum rendered over HTTP. Playwright showed the article and linked assets; its only console errors were Giscus 404s for a discussion that does not yet exist on the new route. Short-link and tag-taxonomy checks passed for 77 published and scheduled posts, as did shell syntax, copied-plugin comparison, and `git diff --check`. No commit, push, or deployment occurred.

**Next gate:** Publisher reviews Part 3 and 3A in the local browser for voice, exercise size, and technical emphasis, then settles publication timing.

## 2026-09-25 21:06 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 3 editorial reviewer. **Decision:** Rewrite Part 3's prose in a more personal, candid first-person voice at the Publisher's request, retaining the verified technical claims.

**Evidence reviewed:** The Publisher's 2024 *Building This Site With AI* account of Jekyll's learning curve and early navigation trouble; the 2026 *Scope Creep Has Never Been This Easy* post's pacing and direct asides; published Part 1; current Part 3 draft; current navigation and layout source.

**Changes:** Reworked the opening, headings, transitions, and conclusions around the author's frustration with repeated markup and the moment Jekyll's hierarchy became useful. Added a source-backed link to his earlier site-building account and connected its navigation rabbit hole to today's generated project menu. Kept the YAML example, layout chain, metadata details, diagrams, and validation limits. Added a voice note to the series handoff for later installments.

**Validation:** The local Part 3 article and its linked 2024 post returned HTTP 200. The running Jekyll preview rebuilt the article after the edit and rendered the revised opening and menu paragraph. `git diff --check` passed. No service was restarted, committed, pushed, or deployed during this pass.

**Next gate:** Publisher reads the revised local article for voice and any factual correction before choosing a publication date.

## 2026-09-25 21:02 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 3 author and local reviewer. **Decision:** Draft Part 3 around a single project page's verified layout and include path, then explain the metadata contract and its actual validation boundary. Keep October 8 as a provisional local preview date.

**Evidence reviewed:** Current `project`, `page`, `default`, and `post` layouts; project lookup, header/navigation, projects list, blog list, discovery filter, post metadata, and series includes; generated-data consumers; tag taxonomy data and validator; configured pre-commit and Pages checks; older mutating front-matter script; published Part 1 and local Part 2 voice. The [Part 3 packet](jekyll-site-tooling-part-03-packet.md) records source locators, limits, and privacy review.

**Changes:** Added a first-person Part 3 article to the Jekyll post tree, a series-consistent banner, and two Graphviz source diagrams with SVG/PNG renders. Linked Part 2 and Hands-On 2A forward to the provisional Part 3 route. Updated the series handoff and visual-asset record. No site behavior or tooling code was changed.

**Validation:** The local article and series listing returned HTTP 200, as did the banner and both SVGs. Playwright showed the article title, Part 3 series context, both full-size diagram links, Current State, and Next Work. The browser console's 404s came from Giscus finding no discussion for the new local route; its client reports one will be created on first comment. The source-bound short-link check and canonical tag-taxonomy check passed (76 published and scheduled posts). Both SVGs parsed as XML, the post has one excerpt marker, and `git diff --check` passed. No commit, push, or deployment occurred.

**Next gate:** Publisher reviews Part 3 for voice, factual emphasis, and diagram clarity. Its publication date remains provisional; Hands-On 3A is optional and should be drafted only if it adds a useful exercise.

## 2026-09-25 20:56 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Hands-On 2A source reviewer and editor. **Decision:** Clarify that the lab models the active site's preview inclusion flags, then show the remaining operational stages it deliberately omits.

**Evidence reviewed:** Current `utils/bin/jekyll-site` start and restart paths; Hands-On 2A post, packaged README, and its extracted archive; local rendered companion route. The wrapper uses a production build and Pagefind pass before either development serve mode. The default serve assignment includes `--future --drafts --unpublished`, and `--current` replaces it with an assignment without those flags.

**Changes:** Added a read-only source-inspection command and a direct mapping from lab modes to the site's `start` and `start --current` behavior. Explained the optional OG refresh, output replacement, production build, Pagefind index, development server, and PID management that are outside the lab. Updated the package README and regenerated its ZIP and checksum.

**Validation:** The revised ZIP passed SHA-256 verification and `verify.sh` from a clean extraction. The local article rendered the new mapping section and the revised package returned HTTP 200. `git diff --check` passed. No live wrapper operation or service restart was run.

**Next gate:** Publisher reviews whether the closer connection to the actual site operation answers the 2A concern and whether any further voice edits are needed.

## 2026-09-25 20:52 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 2 and Hands-On 2A author/reviewer. **Decision:** Keep the already-committed Part 2 as the main narrative and add a small runnable companion for the current/review content switch. The Publisher requested local site review; the October 1 dates remain provisional.

**Evidence reviewed:** Current Part 2 source and rendered route, Jekyll series metadata and companion conventions, `jekyll-site` inclusion flags, isolated fixture behavior under installed Jekyll 4.3.4, extracted archive, and local browser render. The [Part 2 packet](jekyll-site-tooling-part-02-packet.md) records the lab's boundary.

**Changes:** Added Hands-On 2A under the Jekyll post tree and linked it from Part 2. Added a ten-source-file lab with a two-mode build wrapper and generated-HTML verifier, plus a ZIP and checksum. Reused the Part 2 banner and preview diagram; no production script, configuration, or layout changed.

**Validation:** The clean extracted ZIP passed its SHA-256 check and `verify.sh`: current output contained the ordinary post, and review output contained all four fixture posts. Changing the future post's date to the past produced the expected verification failure. The local Hands-On article, parent companion link, series listing, ZIP, checksum, and source-viewer assets returned HTTP 200. Playwright showed Part 2A, its download links, source viewers, diagram, and article sections. The only browser console errors were Giscus 404 responses for a discussion that does not exist for this new local route; Giscus says one will be created on first comment. The source-bound short-link check, taxonomy validation for 75 published and scheduled posts, `bash -n`, and `git diff --check` passed. No remote publication was performed.

**Next gate:** Publisher reviews the Part 2/2A pair in the local browser, especially voice and exercise size, then settles dates and any edits before remote publication.

## 2026-09-23 15:55 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Part 2 author and local reviewer. **Decision:** Draft Part 2 in the Publisher's first-person, problem-by-problem voice, using the now-published Part 1 as the tonal reference. Keep the October 1 source date provisional and the article local for review.

**Evidence reviewed:** Current `jekyll-site` command parser and build/serve paths; Jekyll config restart note; series index and navigation includes; maintenance CHANGELOG and service guide with drift bounded by the Publisher's FileWatcher correction; published Part 1 prose and navigation; running local preview. The [Part 2 packet](jekyll-site-tooling-part-02-packet.md) records the fact, privacy, and conflict review.

**Changes:** Added the Part 2 post, a generated editorial banner, and a source-backed Graphviz preview-path diagram with SVG and PNG renders. Added a next route and scheduled date to Part 1 navigation, and updated the series handoff and visual record. No service, script, template, or configuration behavior was changed.

**Validation:** The local Part 2 article, landing-page entry, previous/next navigation, banner, and SVG returned HTTP 200. A Playwright browser snapshot showed the title, banner, series context, article sections, diagram, and footer. The source-bound short-link check passed; the taxonomy validator accepted 72 published and scheduled posts. The SVG parsed as XML and the post has one excerpt marker. The browser console's two 404s came from Giscus looking for a discussion for the new local route; it reports that a discussion will be created if someone comments. The browser session was closed. No commit, push, or deployment occurred.

**Next gate:** Publisher voice and factual review of Part 2, then settle its publication date and final metadata before any remote publication.

## 2026-09-22 15:57 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Visual author and browser reviewer. **Decision:** Add a distinctive banner and two explanatory diagrams to Part 1 at the Publisher's request.

**Evidence reviewed:** Existing Local First AI hero size and style; current Part 1 prose, `blog_diagram.html` and viewer behavior, project generator and Liquid flow, project permalink and short-link plugins, and the running local Jekyll page. The [visual asset record](jekyll-site-tooling-visual-assets.md) retains the generation prompt and reproducible diagram commands.

**Changes:** Copied the built-in imagegen banner into `html/assets/images/blog/jekyll-site-tooling/` and selected it for both the article and landing page. Added two Graphviz DOT sources and SVG/PNG renders for project publishing flow and project-post URL identity. Inserted the SVGs with the existing diagram include, alternative text, captions, and full-size viewer links. No site template or stylesheet was changed.

**Validation:** The running article loaded both SVGs and the banner in a real browser. Desktop viewport inspection showed the figures separating the relevant prose; a 390-pixel viewport showed both images constrained to the page width, with labels small enough that the full-size viewer is the useful reading path. All three consumed asset routes returned HTTP 200. XML parsing passed for both SVGs; focused checks found no trailing whitespace, unbalanced Markdown fences, or broken local document links across the series materials. The source-bound short-link check passed for the article and landing page, and the taxonomy validator passed for 71 published and scheduled posts under the checkout's RVM Ruby. `git diff --check` passed. The browser automation session was closed after inspection.

**Next gate:** Publisher reviews the local article's visual composition and artwork. Revisions can be made before commit or remote publication.

## 2026-09-22 15:45 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Local site integration. **Decision:** Move Part 1 into the Jekyll post tree at the Publisher's request so the article and landing page can be reviewed in the running browser preview. No remote publication decision is recorded.

**Evidence reviewed:** Local First AI post front matter and series metadata; `series_context.html`, `series_navigation.html`, `series_index.html`, the short-link plugin and backfill verifier, the taxonomy validator, and the active local site.

**Changes:** Added the dated post under `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/`, with its series URL, planned part count, next-part label, default image, and stable short-link basis. Added the landing page's own short-link metadata. Marked the review copies under `docs/publication/` as superseded and updated the packet and handoff status. The user-requested local publication date and art remain reviewable choices before any remote publication.

**Validation:** The local article, landing page, and both short-link routes returned HTTP 200. The landing page rendered Part 1 in Main Series; the article rendered the series context, Current State, Next Work, and forthcoming next-part label. The source-bound short-link check passed for the new post, and the taxonomy validator passed for 71 published and scheduled posts under the checkout's RVM Ruby. No service was restarted, committed, pushed, or deployed.

**Next gate:** Browser and editorial review of the locally rendered article and landing page. Resolve requested revisions before any remote publication.

## 2026-09-22 15:42 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Site integration and source reviewer. **Decision:** Place the series landing page in the Jekyll source tree so the existing Series directory discovers it. Part 1 remains a review draft.

**Evidence reviewed:** `html/blog/series.md` filters `site.pages` by `series_landing: true` and sorts by `series_order`. The Local First AI landing page establishes location, front matter, and optional series index inclusion. The Jekyll server was already running locally.

**Changes:** Added `html/blog/series/beyond-static-building-a-publication-system-around-jekyll.md` with `series_landing: true`, explicit permalink, order after Local First AI, default image, and a conditional series index. Until a post is transferred, the page says the opening installment is in review. Marked the docs landing draft as a superseded copy and updated the packet and series boundary.

**Validation:** The existing local server returned HTTP 200 for `/blog/series/` and the new landing URL; the Series directory rendered a link to the new page, and the landing page rendered its title and review notice without empty series headings. `bundle exec ruby scripts/check_tag_taxonomy.rb` passed under the checkout's RVM Ruby environment for 70 published and scheduled posts. `git diff --check` passed. No local service was restarted or deployment triggered.

**Next gate:** Continue reviewing Part 1's article before moving it into the Jekyll post tree. The landing page source is present locally; commit, push, and public publication remain separate Publisher decisions.

## 2026-09-22 15:34 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Draft author and source reviewer. **Decision:** Submit the first review round as Part 1 and a series landing page under `docs/publication/`. Neither draft is technically or editorially approved.

**Evidence reviewed:** The Part 1 packet and earlier inventory; Local First AI Part 1 and series landing for structure; current Giscus, contact form, mail draft JavaScript, shared footer and comments includes; current project, URL, preview, blog, and artifact sources already identified in the packet. The Publisher supplied the personal account of Jekyll frustrations, local project-card motivation, and no observed discussion use.

**Changes:** Added a narrative Part 1 draft and a short series landing draft. Updated the packet to include the engagement/contact claim boundaries, draft privacy review, and post-tree handoff fields. No site source behavior or published posts changed.

**Validation:** Focused checks passed for all six series documents: no trailing whitespace, balanced code fences, and resolvable local Markdown links. The article has one excerpt marker, Current State and Next Work sections, review-stage metadata without a publication date, and no FileWatcher claim. The maintenance CHANGELOG SHA-256 remains `52c79b6c39c80fb32038331a051eeb0d45de242ef32eabe67c615547ad0d32f7`. `git diff --check` passed. No Jekyll build or browser test was run for documents outside the post tree.

**Next gate:** Source and editorial review of both drafts; then any requested revisions. Banner, diagrams, social copy, Jekyll transfer, and publication remain later steps.

## 2026-09-22 15:27 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Researcher and editorial planner. **Decision:** Retitle Part 1 **Jekyll, One Problem at a Time** to distinguish it from the existing “When...” installment, and ground its cumulative narrative in selected CHANGELOG entries and the Publisher's firsthand account. The overall series working title remains unchanged.

**Evidence reviewed:** Publisher direction and account of repeated Jekyll frustration; CHANGELOG entries from `20240220_01-rel` through the September 2026 updates, with source limitations already recorded in the inventory. The older file contains out-of-order entries, superseded paths, and a reverted Sass attempt, so no continuous deployment timeline is inferred.

**Changes:** Revised the series outline and Part 1 packet's opening and section beats; added a chronological problem-and-response table with explicit current-state limits. No site source, maintenance CHANGELOG content, or generated artifacts were changed.

**Next gate:** Draft Part 1 in first person within the updated packet's claim boundaries, then return it for technical and editorial review.

## 2026-09-22 15:20 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Researcher and editorial planner. **Decision:** Lift the CHANGELOG dependency following the Publisher's completion notice. Reconciliation and Part 1's pre-draft packet are complete; prose remains to be drafted and reviewed.

**Evidence reviewed:** CHANGELOG working-tree diff and SHA-256 recorded in the inventory; unchanged tracked source `8c8846a`; complete archive, Technology page, shared blog list and source labels, navigation, taxonomy, and pagination guide. Prior source findings are reused with their existing limits.

**Changes:** Added archive/pagination coverage to Part 5, recorded update-aware archive ordering, updated current status and next assignment, and prepared Part 1's source inventory, claim table, privacy review, conflict dispositions, and narrative outline. Preserved the maintenance agent's CHANGELOG edits.

**Next gate:** Draft Part 1 from the packet, then technical and editorial review. No additional planning authorization is needed. Public assets follow prose approval; post-tree transfer and publication remain separate decisions.

## 2026-09-22 14:56 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Researcher and editorial planner. **Decision:** Incorporate the Publisher's operating corrections and elevate project generation and Liquid reuse in the series. Keep Part 1 on hold for completion of the maintenance CHANGELOG update.

**Evidence reviewed:** Publisher report that FileWatcher is unused, pre-commit/system checks are used, and GitHub thumbnail rate limiting motivated local cards. Read-only follow-up at tracked source `8c8846a` inspected project generation, catalog serialization, project/page/default layouts, project lookup/listing, navigation/header, shared blog filtering and pagination, and the existing template dependency graph.

**Changes:** Removed FileWatcher from active research scope; reframed Part 3 around layout inheritance and includes and Part 5 around the YAML-driven project lifecycle. Added source-supported data flow and limits to the inventory, including presentation-only visibility, scaffold entry conditions, preserved catalog ordering, and the unresolved search execution evidence. Operator reports remain attributed rather than being displaced by narrower CI configuration evidence.

**Next gate:** Await the Publisher's CHANGELOG completion notice before advancing Part 1. Reconcile maintenance changes and then prepare its evidence packet. No site code, generated data, services, hooks, or maintenance-agent files were changed.

## 2026-09-22 12:16 CDT (America/Chicago, UTC-05:00)

**Author:** Codex, primary series agent. **Role:** Researcher and editorial planner. **Decision:** Revise the planning documents under the Publisher's current authorization; retain ten main installments. No article approval or publication decision recorded.

**Authorization:** Following the initial source review, the Publisher assigned ownership of the series and authorized updates to its documents and outlines. This permits the planning revisions here without another confirmation request.

**Evidence reviewed:** Tracked source at `8c8846a9d1b98d967f9eee5c6da28db2bad035a7`; original handoff; service and check wrappers; URL and metadata plugins; project-data generator; diagram and source includes; narration implementation and test inventory; post layout; pre-commit and Pages workflow configuration; monitoring and scheduled-task source; operator documentation and changelog. The [inventory](jekyll-site-tooling-inventory.md) records source locators, limits, and outstanding work. No current test execution or deployment evidence was collected.

**Changes:** Expanded Part 5 to project generation and bounded search coverage; separated retained narration into optional companion 7B; reframed Part 8 around checks, repairs, and deployment gates; clarified preview defaults, URL identity, extraction behavior, narration replacement boundaries, and placeholder maintenance. Added the initial evidence taxonomy, privacy/artifact map, drift register, and next assignment. Site behavior and operator documentation were not changed.

**Validation:** A focused Python 3 check passed for all three series files: local Markdown links resolve, code fences balance, and no trailing whitespace is present. It also confirmed ten ordered main installments and removal of the obsolete First Assignment reference. `git diff --check` passed; because these documents are untracked, the explicit file checks provide their formatting evidence. `git status --short` showed only the untracked `docs/publication/` directory. Runtime tests and site builds were not run.

**Next gate:** Prepare Part 1's pre-draft packet and detailed narrative outline, then draft for technical and editorial review. Resolve only the evidence gaps needed for that installment. Transfer to the post tree and publication remain separate Publisher decisions.
