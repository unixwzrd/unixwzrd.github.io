# Part 5: From a YAML Project Catalog to a Project Publishing System

Status: source-reviewed local draft, September 26, 2026. October 22 is a provisional preview date. The Publisher authorized the next installment and local browser review; remote publication remains a separate decision.

## Source and claim review

| Source | Supported claim | Boundary |
| --- | --- | --- |
| `utils/bin/fetch_og.py`, `utils/bin/test_fetch_og.py` | Ordered `repos.yml` input, GitHub metadata or fallback, manual overrides, local card generation/fallback, `github_projects.yml` output, first-page scaffolding | Generator runs separately from a normal Jekyll build; failed entries can be skipped; scaffolding is conditional on an absent landing page |
| `html/_includes/navigation.html`, `html/projects.md`, `html/_includes/projects_list.html` | Projects menu follows generated order after fixed All Projects; page splits private/public groups; `none` filtered in these views | Visibility is presentation, not access control; catalog order is preserved only among successfully processed entries and within each page group |
| `html/_data/blog_sections.yml`, `html/blog.md`, `html/blog/series.md` | Visible Blog sections follow YAML order after fixed links; hidden General is absent from menu/hub; series directory reads all landing pages | Blog hub's configured Series recent list is currently Local First AI only; hidden section's content is not deleted |
| `html/_layouts/project.html`, `html/_includes/project_lookup.html`, shared blog/discovery includes | Project `category` connects landing page to generated data and its update list | Draft introduction needs editing; a generated page is not a reviewed article |
| Series posts and metadata/discovery plugins | Series reading order and update-aware discovery are distinct from project and section order | Front-matter keys act only when consumed; tag taxonomy check is narrower than a complete schema |

## Privacy and drift

The public examples use only invented project and owner names. The article does not quote private rows from `repos.yml` or generated project data. `fetch_og.py` remains in the reusable MIT-licensed `utils` tree; the lab includes a frozen copy with SHA-256 `2fef10276b714e4aad3aedc38c301cb66fe24c3577b7bad5658939898580a0e9`. The lab makes no network call and writes only into a temporary directory. Its baseline, `--reorder`, and `--show-hidden` runs print the generated order and fields. It is a teaching snapshot, not an installable package or an offline proof of image rendering.

The Publisher's history of GitHub thumbnail rate limiting is attributed as motivation. Current source still fetches repository metadata and has image fallbacks. The blog/series landing page's discovery behavior is separate from the Blog hub's configured recent list. FileWatcher is not an active workflow. Pagefind's local-versus-deployment indexing gap is deliberately left out of this installment's claims.

## Local handoff

The main post is `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-22-from-a-yaml-project-catalog-to-a-project-publishing-system.md`. Its companion is `2026-10-22-hands-on-follow-a-project-through-the-catalog.md` in the same directory. Both use the new Part 5 banner and data-flow diagram. The editable diagram is `docs/publication/diagrams/src/jekyll-post-05-publishing-paths.dot`; SVG and PNG renders are in `html/assets/images/blog/jekyll-site-tooling/`. The lab and checksum are under `html/assets/code/jekyll-site-tooling/post-05a/`.

## Local validation, September 26

The existing watched server returned HTTP 200 for the series landing, both Part 5 posts, banner, SVG diagram, lab ZIP, and checksum. A separate future-inclusive Jekyll build completed successfully in `/tmp/jekyll-part05-preview` and rendered both entries in the series index. The short-link front-matter check passed for both posts; the taxonomy check passed for 79 published and scheduled posts. All 12 current `test_fetch_og.py` tests passed. The lab ZIP passed its checksum and clean extraction; the extracted runner passed its ordering, override, visibility, and scaffolding assertions without network access. The diagram parsed as SVG XML, and `git diff --check` passed.

Playwright showed the main article and companion with their series context, images, source viewer, and links. At 390px, the Blog dropdown opened and displayed the fixed links followed by the visible sections in YAML order; General was absent. The only browser console errors observed were Giscus 404s for discussions that do not yet exist for these preview routes. None of these checks asserts remote publication.

On the Publisher's September 26 request for the hands-on, the companion gained two explicit variations. The baseline, `--reorder`, and `--show-hidden` runs passed; the lab ZIP and checksum were refreshed. The Publisher restarted the local server, and the revised page, ZIP, and runner source returned HTTP 200. Playwright showed the revised commands and explanation in the page.
