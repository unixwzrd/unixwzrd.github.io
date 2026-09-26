# Part 4: Stable URLs in a Repository That Keeps Moving

Status: source-reviewed local draft, September 25, 2026. October 15 is a provisional preview date. The Publisher authorized continuing the series and has not set a remote publication date.

Publisher correction: the short-link feature was motivated by sharing articles on X/Twitter, Bluesky, and other character-limited social posts. Keeping redirects in the Jekyll site avoided relying on an external shortening service. This first-person motivation is now in the main article and Hands-On introduction; the current plugin and Jekyll redirect generation support the implementation claim.

Publisher clarification: ownership is a principal advantage, not just shorter copy. The site controls `/s/` redirects and can keep a shared short address unchanged through a deliberate page-naming change by retaining `short_link_basis`. A changed old canonical page URL still needs its own declared redirect; the short-link mechanism does not preserve every former full-length path automatically.

## Source inventory

| Source | Current evidence | Limit |
| --- | --- | --- |
| `html/_plugins/00_project_post_permalink.rb` and `case_preserving_permalinks.rb` | Project posts require normalized `permalink_slug`; their front-matter date and project directory form the canonical route; an explicitly declared legacy route joins `redirect_from` | This is specific to project-scoped posts; it does not freeze the date or project directory if an editor changes them |
| `html/_plugins/01_short_link_injector.rb` and `_config.yml` | Eligible posts and opted-in pages get a 10-hex `/s/` path from SHA-256 of `short_link_origin + short_link_basis`; the path joins `redirect_from`; a declared `short_url` mismatch fails the build | Absent `short_link_basis` falls back to the current source path, so a move can change the code |
| `scripts/backfill_short_url_front_matter.rb`, `scripts/verify_short_url_redirects.rb`, `scripts/verify_project_permalink_redirects.rb` | Backfill stores or checks identity fields; post-build verifiers check generated redirect files and declared project legacy targets | A file's existence is a build-artifact check, not a remote reachability check |
| `.github/workflows/jekyll.yml` | Production build and the three URL checks are configured before Pages artifact upload and deployment | Configuration alone does not establish a successful deployment |
| `CHANGELOG.md` August 18 and 21, 2026 entries | Records source reorganization, frozen short-link basis, frozen project slugs, and 26 compatibility redirects | Changelog dates describe recorded work, not independently verified deployment dates |
| Representative project front matter and current series posts | Shows real `permalink_slug`, `legacy_project_permalink`, `short_link_basis`, and `short_url` use | Examples are editorial evidence, not a claim that every old external URL is redirected |

## Fact and drift review

**Implemented:** Project-post canonical routes use project directory, front-matter date, and normalized slug. The optional legacy route and generated `/s/` route are redirects to that canonical page. The short-link plugin runs after project permalinks are assigned. All posts are short-link eligible; pages opt in. The short-link hash uses the configured origin and immutable basis when provided.

**Configured checks:** The GitHub Pages workflow builds the production site and runs the short-link front-matter check plus short-link and project-redirect output verifiers. Local pre-commit wiring is separate. A checker finding a generated file is not an HTTP check against the deployed domain.

**Historical:** Earlier project routes came from titles, and the changelog says 26 were retained as redirects when slugs were frozen. The August 18 source reorganization prompted a stable short-link basis. Neither entry proves every former link or deployment date.

**Drift to keep visible:** The fallback short-link basis is a source path and is move-sensitive; the main article must not promise stability without explicit front matter. `permalink_slug` freezes the slug segment but changing a project's directory or the post date changes its canonical path. `legacy_project_permalink` preserves only the route declared there. Ordinary series posts follow their own date/category/filename-derived routes; the project slug rule does not apply to them. A local preview of future-dated posts is not remote publication.

## Privacy review

The article uses generic path examples and discusses the public site domain only where it is part of the actual short-link format. It omits home directories, private repository names and values, credentials, local topology, unpublished project catalog rows, logs, and discussion identifiers. The companion lab uses invented paths and a frozen copy of the public short-link module; it does not ingest the site's posts.

## Narrative outline

Open with the cost of changing a title or moving a file after someone has the link, and the original need for compact links in character-limited social posts. Explain the canonical project-post contract first: project directory, date, and frozen slug. Walk an old title-based route into its explicitly declared redirect, then give the independent short link its own identity through `short_link_basis` and explain why keeping the redirect on this site matters. Show the plugin's ordering and the three checks without calling a local build proof of remote reachability. Distinguish ordinary series posts from project posts. End with the current boundary and lead into Part 5's project catalog.

Hands-On 4A demonstrates the current short-link module with invented objects: fixed basis through a simulated source move, changing fallback without a basis, and a declared URL mismatch. It is an isolated mechanism exercise, not a full Jekyll build.

## Local handoff

The main post is `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-15-stable-urls-in-a-repository-that-keeps-moving.md`, and Hands-On 4A is `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-15-hands-on-keep-a-short-link-through-a-source-move.md`. The main article links the companion, and both share the Part 4 banner and URL diagram. Lab source, ZIP, and checksum live under `html/assets/code/jekyll-site-tooling/post-04a/`.

The lab's module is byte-for-byte copied from the current `html/_plugins/01_short_link_injector.rb` at SHA-256 `cacfe9889ff7dd5c23e745fcbe42f124ed8bb4531a2a074bb21bd507b7cd3051`. The lab avoids a nested `_posts` directory under the site's assets, which had caused the previous exercise's invented posts to enter the main build before the fixture path was excluded.

**Validation, September 25:** The ZIP passed SHA-256 verification after clean extraction; all three lab cases passed. Both post routes, the series index, main short redirect, diagram, ZIP, and individual source links returned HTTP 200 locally. Playwright showed the Part 4 article and Hands-On 4A with their series context, source viewers, and Current State/Next Work sections. The only console failures were Giscus requests for discussions that do not yet exist for these local routes. The source-bound short-link check and canonical taxonomy check passed for 77 published and scheduled posts; the future-inclusive post-build short-link and project-redirect verifiers passed against the local development output. The diagram parsed as SVG XML, and `git diff --check` passed. These checks do not assert a remote deployment.
