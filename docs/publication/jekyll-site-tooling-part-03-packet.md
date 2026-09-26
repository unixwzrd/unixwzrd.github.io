# Part 3: Building the Site from Shared Layouts, Includes, and Data

Status: source review and local browser draft prepared September 25, 2026. The October 8 post date is provisional. The Publisher asked to proceed from Part 2 to Part 3, then explicitly asked that the prose be humanized in his own voice and requested a Hands-On draft. A second editorial pass used his 2024 account of building this site, his 2026 scope-creep post, and published Part 1 as voice references. It tied the opening and navigation story to his documented experience without copying old errors or inventing incidents. Hands-On 3A is now a local browser draft. No remote publication is claimed.

## Source inventory and fact boundaries

| Source | Supported claim | Boundary |
| --- | --- | --- |
| `html/_layouts/project.html`, `page.html`, `default.html` | Project page inherits page and then default; project resolves generated data, lists its posts, and adds project content | This is the project-page path, not every site page |
| `html/_includes/project_lookup.html`, `blog_list.html`, `filter_discovery_posts.html`, `post_list_meta.html` | Project lookup uses `page.category`; a shared list filters, sorts, paginates, and labels eligible posts | Conditional branches and browser pagination are not all exercised on every page |
| `html/_includes/header.html`, `navigation.html`, `projects_list.html`; `html/projects.md` | Navigation and Projects page consume generated project data, with visibility-based presentation filtering | Visibility is not file access control; source does not prove all search/feed routes suppress hidden pages |
| `html/_layouts/post.html`, `html/_includes/series_context.html`, `series_navigation.html`; `html/_data/blog_sections.yml` | Post layout uses title, dates, image, audio, series fields, and engagement; series metadata drives reading context and navigation | A value in front matter can affect multiple views; no claim that all required fields are formally validated |
| `html/_data/tag_taxonomy.yml`, `html/_plugins/03_tag_taxonomy_validator.rb`, `scripts/check_tag_taxonomy.rb` | Closed canonical tags and content types for publishable/scheduled `_posts`; the build plugin and focused runner enforce them | Actual drafts under `_drafts` are skipped by this validator for preview; it does not enforce a complete post schema |
| `.pre-commit-config.yaml`, `.github/workflows/jekyll.yml` | Taxonomy check is configured in pre-commit and CI; CI also checks short-link and redirect rules | Configuration is not evidence of every local hook installation or of successful deployment |
| `utils/bin/checks/10_front_matter.sh` | Older check can add missing image/title/excerpt fields | It mutates files and is not the strict canonical taxonomy validator; do not present it as a fail-closed publication contract |
| `docs/diagrams/site-architecture/jekyll-template-dependencies.dot` | Static reference graph supports source navigation | Conditional edges are combined; verify current edges in templates before claiming a runtime call path |

## Conflict and privacy review

The post distinguishes authored front matter, generated project data, Liquid rendering, and checks. It does not expose catalog rows, environment values, host paths, credentials, or unpublished project descriptions. It uses a generic project page and current series metadata as examples. `visibility: private` is described only as a presentation choice; it is not access control. The current taxonomy generator rejects unknown or aliased tags and unknown `content_type` values in publishable posts but does not enforce title, image, excerpt, or every series field. The older front-matter script repairs a few fields and is not represented as a CI gate.

## Narrative outline

Open with the frustration of fixing the same piece of presentation in several pages. Follow one project page through `project → page → default`, then branch into `project_lookup`, `blog_list`, shared filtering and metadata, and the data-driven navigation and Projects page. Explain that reuse shifts complexity into metadata: `category` connects the project page and posts to generated data; `categories`, series fields, images, update notices, and optional audio change other views. Distinguish flexible rendering defaults from checked contracts. End with the actual taxonomy and CI boundary, then lead to Part 4's stable URL problem.

The main article is in the local Jekyll post tree with a banner and two source-backed diagrams. The Publisher requested Hands-On 3A; it is also in the local post tree, linked from Part 3, and listed beside it on the series landing page.

## Hands-On 3A companion

The companion source is `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-08-hands-on-find-the-limits-of-a-jekyll-metadata-check.md`, rendered at `/hands-on/2026/10/08/hands-on-find-the-limits-of-a-jekyll-metadata-check/`. The lab source, ZIP, and SHA-256 file live under `html/assets/code/jekyll-site-tooling/post-03a/`.

The package contains a byte-for-byte snapshot of the current `03_tag_taxonomy_validator.rb` plugin, SHA-256 `f8734a26c65ece8d1c206ffa0a1d4756d6fdadaeb73af56c96f356d8369e39d7`, a tiny invented taxonomy, and seven invented post cases. A clean extraction passed checksum verification and the lab runner: valid, missing-series-order, and old-tag draft cases were accepted; unknown, aliased, duplicate-tag, and unknown-content-type cases were rejected. The runner checks both exit status and expected diagnostic text and retains case logs under its extracted `out/` directory. The lab does not exercise the full site layouts, series index, project generator, hooks, CI, or remote deployment. In particular, acceptance of missing series order proves only that this plugin does not check it; it does not prove where the real site's series index would place that post.
