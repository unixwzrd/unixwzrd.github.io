# Jekyll Site Tooling Series Review Journal

Preserve entries and prepend new ones. Planning, technical review, editorial approval, and publication authority are separate decisions.

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
