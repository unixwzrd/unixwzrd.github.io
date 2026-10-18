# Blog System and Templates

## Overview

The blog system consists of several components that work together to display posts across the site:

1. **Post Layout**: The main template for displaying individual blog posts
2. **Blog List Component**: A reusable component for displaying lists of blog posts
3. **Pagination**: System for breaking up long lists of posts into pages
4. **Project Blog Integration**: Special handling for project-specific blog posts

## Post Layout

The post layout (`_layouts/post.html`) is used to render individual blog posts. It handles:

- Post title and metadata display
- Content formatting
- Author information
- Date formatting
- Footer content

### Important Variables

When working with the post layout, remember that all frontmatter variables are accessed through the `page` object:

```liquid
{{ page.title }}
{{ page.date }}
{{ page.author }}
{{ page.categories }}
{{ page.tags }}
{{ page.content_type }}
```

The canonical tag vocabulary lives in `html/_data/tag_taxonomy.yml`. List it from the repository root with `bundle exec ruby scripts/list_tags.rb`. Use `content_type` for introductions, releases, updates, and reference posts rather than adding those values to `tags`.

### Contents navigation and optional discussion prompts

Regular and project blog posts get build-time contents navigation automatically. Individual posts may opt out, and discussion prompts remain optional:

```yaml
toc: false # Only needed to suppress this post's contents navigation
discussion_prompt: "What has worked in your setup, and where have you run into trouble?"
```

`toc` defaults to true for both `posts` and `project_posts` in `_config.yml`. The post layout adds an initially collapsed **On this page** disclosure after the series context and before the article prose. It lists rendered H2 and H3 headings with existing IDs, nests H3 entries under their preceding H2, and omits headings inside quotations, figures, navigation, and disclosures. It does not create or change heading IDs, needs no JavaScript, and renders nothing when no eligible headings exist. The contents block is excluded from Pagefind indexing. Existing Jekyll processes must load the defaults and Ruby hook on their next normal restart; an older watcher omits the contents block rather than repeating the article.

No per-post setting or include is needed for main-site or project articles using `layout: post`, and there is no need to maintain the list by hand. Set `toc: false` only when an article should not show it; short posts without suitable headings already omit it automatically. Project landing pages and blog indexes are unaffected. When renaming an existing section, preserve its formerly shared fragment with a unique `<div id="former-heading-id"></div>` immediately before the new heading; this keeps old links working without adding duplicate contents entries or an empty Markdown paragraph.

`discussion_prompt` is optional Markdown displayed with the discussion section. Use the author's conversational technical voice for article prompts. Shared interface text and company/project introductions should remain professional and organization-appropriate, not first-person personal narration. Existing article prose does not need rewriting to enable either feature.

The engagement order is discussion, RSS subscription, then support. The existing neutral GitHub Discussions explanation remains when no prompt is supplied. `comments: false` hides the discussion and prompt; `show_support: false` hides the support section and its divider. RSS remains available independently. Giscus continues to use its configured repository, category, and pathname mapping, so layout changes do not create a new discussion identity.

### Optional project introduction

Project landing pages can supply a short Markdown introduction before their update history, without moving the complete description below it:

```yaml
project_intro: |
  A concise description of what the project does and who it helps.

  Start with the [installation and usage documentation](https://example.com/docs/).
```

This field is opt-in; pages without it retain their previous content order. LogGPT and Extract Chat are the initial examples. Keep introductions factual, professional, and brief, and link to authoritative getting-started instructions rather than repeating release details.

### Theme and reader-experience validation

The site follows the browser's light/dark preference using paired CSS custom properties, with no JavaScript preference or theme switch. `html/assets/css/style.scss` must retain its empty YAML front matter so Jekyll compiles it in place of the theme's stylesheet. It imports Minima initialization and the active skin before emitting custom components exactly once. The auto-loaded `custom-styles.scss` hook is intentionally non-emitting. Palette inputs and early variable bindings live in `custom-variables.scss`; additional component/code tokens live in `custom_theme.scss`.

Run focused fixture tests with `bundle exec ruby scripts/test_reader_experience.rb`. Set `READER_SITE=/absolute/path/to/built/site` to add rendered integration checks; optional `READER_BASELINE=/absolute/path/to/prior/build` also compares original heading anchors and canonical links. Against an already served isolated build, open its SSH article with Playwright CLI and run `playwright-cli run-code --filename scripts/check_reader_experience_browser.js`. The browser check uses the current page's origin, exercises both appearances at desktop and mobile widths, checks rendered text/control contrast, source disclosures, and contents keyboard/fragment navigation with and without JavaScript, and saves ignored screenshots under `output/playwright/`. It never submits forms or comments. This is targeted regression coverage, not a full accessibility certification.

The Pages workflow builds the Pagefind index after Jekyll and before uploading `_site`, using the versions in `requirements.txt` and the same selectors/language as `jekyll-site`. It checks the search entry files and a nonempty English index, runs the reader fixture/rendered tests and standalone permalink validator, and checks internal links and fragments with HTMLProofer. The internal check allows HTML5 named anchors without `href`; it does not perform network-dependent external-link checks. Browser checks remain a local validation step and now exercise a real search query, query-string preservation, and a reachable result in both appearances and widths. Generate the search index before running those browser checks.

### Optional retained article audio

The local development build adds the dynamic proofreading player to every post automatically. Public narration is separate and opt-in. Once a generated MP3 has been reviewed, add either a simple path:

```yaml
audio: /assets/audio/blog/technology/2026-09-12-example-post.mp3
```

or the expanded form:

```yaml
audio:
  src: /assets/audio/blog/technology/2026-09-12-example-post.mp3
  type: audio/mpeg
  title: "Listen to this article"
  duration: "18 minutes"
  download: true
```

The shared post layout places the static player below the hero image and above the article body. It renders nothing when `audio` is absent. Generate and check retained narration with `utils/bin/article-audio`; see `utils/README.md` for the workflow. Do not add front matter until the MP3 has been reviewed and its narration manifest is current.

### Important Variables

When working with the post layout, remember that all frontmatter variables are accessed through the `page` object:

```liquid
{{ page.title }}
{{ page.date }}
{{ page.author }}
{{ page.categories }}
{{ page.tags }}
```

### Post-publish updates and series

See **[workflows/post-updates-and-ordering.md](../workflows/post-updates-and-ordering.md)** for the full policy. Summary:

| Tier | Fields | Discovery lists |
|---|---|---|
| Silent fix | (none) | No change |
| Technical correction | `corrected_at`, `correction_note` | No promotion |
| Major update | `update_notice`, `last_modified_at` | Promoted via `list_sort_key` |

Series index pages sort by **`series_order`** (e.g. `10`, `20`, `25` for part `2A`), not publish date. Navigation uses `series_previous_url` / `series_next_url`.

Build plugin: [`html/_plugins/02_post_list_metadata.rb`](../../html/_plugins/02_post_list_metadata.rb) (runs as a Jekyll generator after post dates are parsed). List UI: [`post_list_meta.html`](../../html/_includes/post_list_meta.html).

### Common Issues

- Using `post.` variables instead of `page.` variables in the layout
- Missing frontmatter in blog posts
- Incorrect date formatting

## Blog List Component

The blog list component (`_includes/blog_list.html`) provides a consistent way to display lists of blog posts across the site. It can be included in any page with parameters:

```liquid
{% include blog_list.html
   heading="Latest Posts"
   limit=5
   category="project-name"
%}
```

### Parameters

- `heading`: The heading to display above the list (optional)
- `limit`: Maximum number of posts to display (default: 5)
- `category`: Filter posts by category (optional)
- `tag`: Filter posts by tag (optional)
- `series`: Restrict to one exact series name (optional).
- `series_only`: Include any post with nonempty series front matter (optional).
- `exclude_series`: Exclude series articles and companions (optional).

The ordered section configuration is `html/_data/blog_sections.yml`. The blog hub's Series Recent list uses `series_only: true` across every series, while Hands-On includes both standalone tutorials and series companions. Technology remains standalone-only. A companion may intentionally appear in both Recent lists; the three-entry limit, publication exclusions, and shared update-aware sort remain unchanged. The featured-series callout is a separate editorial choice.

## Pagination

Pagination is configured in `_config.yml`:

```yaml
paginate: 5
paginate_path: "/blog/page:num/"
```

To use pagination, the template must be an HTML file (not Markdown) and must include pagination logic:

```liquid
{% if paginator.total_pages > 1 %}
<div class="pagination">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path | relative_url }}">&laquo; Prev</a>
  {% endif %}

  {% for page in (1..paginator.total_pages) %}
    {% if page == paginator.page %}
      <span class="current-page">{{ page }}</span>
    {% else %}
      <a href="{% if page == 1 %}{{ '/blog/' | relative_url }}{% else %}{{ site.paginate_path | relative_url | replace: ':num', page }}{% endif %}">{{ page }}</a>
    {% endif %}
  {% endfor %}

  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path | relative_url }}">Next &raquo;</a>
  {% endif %}
</div>
{% endif %}
```

## Project Blog Integration

Project blogs are integrated through:

1. Project-specific blog directories: `projects/[project-name]/_posts/`
2. Category-based filtering: `{% include blog_list.html category=page.category %}`
3. Consistent styling through shared CSS classes

### Project Blog Structure

```
projects/
├── Project1/
│   ├── _drafts/
│   │   └── template-blog-entry.md
│   └── _posts/
│       └── YYYY-MM-DD-project1-title.md
```

### Project post URL slug (`permalink_slug`)

Every project post must freeze its canonical URL segment independently of its title and source filename:

```yaml
permalink_slug: launchd-seckit-run-and-invisible-env-vars
```

Use lowercase letters, numbers, and single hyphens. Never change `permalink_slug` after publication. If an older canonical path must continue working, preserve it separately:

```yaml
legacy_project_permalink: /projects/Example/2026/08/20/former-title-based-path/
```

The project permalink plugin merges that compatibility path into `redirect_from` without replacing existing redirects or the post's short URL.

## Source code disclosures

Use ordinary fenced code blocks for short commands and excerpts that belong directly in the article. Use the shared source-code disclosure for a complete public source file:

```liquid
{% include source_code.html
   source="/assets/code/example/tool.py"
   language="python"
   title="tool.py" %}
```

The source file must live below `html/assets/code/`. The build reads that same file, applies server-side Rouge highlighting, and places it inside a collapsed `<details>` element. Readers can inspect the complete file without downloading it; the component provides a separate, explicitly labeled download action.

This keeps one source of truth for the rendered and downloadable code. Do not paste a second copy of a complete file into the post. Continue using normal fenced blocks for the commands that demonstrate how to run it.

All code presentation uses the shared post-skin rules in `html/_sass/minima/customizations/custom_code.scss`. Inline code, ordinary fenced blocks, and full-file disclosures should retain the coordinated light/dark surfaces, spacing, scrollbar behavior, and accessible Rouge token palettes. Do not add per-article background or token-color overrides; add a missing language token to the shared theme instead.

## Blog diagrams

Keep the Mermaid or Graphviz source with the publication material and generate both SVG and PNG assets. Embed the SVG through the shared diagram include; retain the PNG as a fallback or social-production asset.

When readers should inspect and download the exact diagram source, place the `.dot` or `.mmd` under `html/assets/code/` and show it with the shared `source_code.html` disclosure. Render from that same public file so the article does not maintain a second source copy. Part 6 follows this convention.

For an explicit local render, `python3 utils/bin/render-blog-diagram.py SOURCE OUTPUT_STEM` generates both formats from a `.dot` or `.mmd` source. `OUTPUT_STEM` omits the extension. The helper requires the Graphviz `dot` executable for `.dot` or Mermaid CLI `mmdc` for `.mmd`; it does not install either tool or run automatically as part of Jekyll. Its Mermaid path also gives the SVG numeric dimensions from its `viewBox` for the viewer.

```liquid
{% include blog_diagram.html
   src="/assets/images/blog/example/architecture.svg"
   alt="A concise description of the diagram's meaning and flow."
   variant="series" %}
```

Use `variant="series"` for a larger architecture diagram and `variant="compact"` for a small procedural figure. The include constrains the inline preview, supplies accessible alternative text, and makes both the image and its **Open full-size diagram** caption link to a dark, full-browser SVG viewer in a new tab. The viewer provides zoom controls and click-drag panning, while touch devices retain their normal pan and pinch-to-zoom behavior. Readers can select **Close** or press Escape to leave the viewer.

The site uses a near-black background, so generated diagrams must not use a white canvas. Prefer a transparent background with near-white connector lines, arrowheads, group labels, and edge labels. Colored node fills and their contrasting internal text can remain unchanged. Mermaid diagrams should use the shared publication convention represented by these values:

```text
canvas: transparent
connectors and arrowheads: #e5e7eb
free-standing and group text: #f9fafb
edge-label backing: #040404
```

Render Mermaid with `mmdc -b transparent`. Mermaid commonly emits `width="100%"` without an intrinsic height; the publication renderer replaces that percentage with explicit dimensions from the SVG `viewBox` so browsers preserve the diagram's aspect ratio inside the clickable figure. The shared diagram preview retains a dark canvas, matching the full-size viewer, so existing transparent diagrams remain readable in either page appearance without recoloring the artwork. Before publication, inspect the SVG inside the actual article under both browser appearance preferences rather than relying on an image previewer's default background.

Diagrams must also be constrained by the article stylesheet instead of expanding automatically to the full content width. Compare related diagrams in the browser and normalize their Mermaid base font when different native view-box proportions would otherwise make one figure's boxes and labels substantially smaller than another's.

## Troubleshooting

### Post Title Not Displaying

Check that:
- The post has proper frontmatter with a title
- The layout is using `page.title` (not `post.title`)
- There are no Liquid syntax errors in the template

### Pagination Not Working

Ensure that:
- The template file is HTML (not Markdown)
- Pagination is enabled in `_config.yml`
- The paginator object is being used correctly

### Blog List Not Showing Posts

Verify that:
- Posts have the correct category/tag if filtering is used
- Posts have proper frontmatter
- Posts are in the correct directory
- Posts have a future date if `future: false` is set in config

## Social short URLs (`/s/`)

Posts, plus pages that opt in with `short_link: true`, get a deterministic short link for cut-and-paste on social:

- **Front matter:** immutable `short_link_basis: "/path/used/when-created.md"` plus `short_url: "https://unixwzrd.ai/s/<10 hex chars>/"`. Pages also set `short_link: true`.
- **Mechanism:** [`html/_plugins/01_short_link_injector.rb`](../../html/_plugins/01_short_link_injector.rb) (via [`case_preserving_permalinks.rb`](../../html/_plugins/case_preserving_permalinks.rb)) appends `/s/<code>/` to `redirect_from` using `SHA256(short_link_origin + short_link_basis)`. The source path is the compatibility fallback when the basis is absent. Once frozen, the basis survives directory moves and must not be rewritten. [`jekyll-redirect-from`](https://github.com/jekyll/jekyll-redirect-from) serves the redirect.
- **Config:** `short_link_origin` in [`_config.yml`](../../_config.yml) (default `https://unixwzrd.ai`).

**Backfill** front matter when creating eligible content or before moving older content that does not yet have `short_link_basis`:

```bash
bundle exec ruby scripts/backfill_short_url_front_matter.rb --dry-run
bundle exec ruby scripts/backfill_short_url_front_matter.rb
```

**Staged eligible content only** (fast; use from pre-commit or by hand):

```bash
bundle exec ruby scripts/backfill_short_url_front_matter.rb html/projects/MyProject/_posts/2026-01-01-example.md
bundle exec ruby scripts/backfill_short_url_front_matter.rb --staged   # git index: cached paths only
```

**Check without writing** (CI or sanity check):

```bash
bundle exec ruby scripts/backfill_short_url_front_matter.rb --check
bundle exec ruby scripts/backfill_short_url_front_matter.rb --check --staged
```

**Pre-commit:** optional [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) runs the script with `pass_filenames: true`. It updates staged posts and pages opted in with `short_link: true`; unrelated pages are ignored. Jekyll still loads the full site once for collision checks.

**Local test:** `bundle exec jekyll serve` then open `http://localhost:4000/s/<code>/` (code from a post's `short_url`, or list `_site/s/` after build). Posts dated in the future are skipped until their date unless `future: true` in config or you run `jekyll build --future`.

**Verify:** `bundle exec jekyll build` (should succeed); optional `ls _site/s/` for redirect folders; open one `_site/s/<code>/index.html` and confirm canonical target URL.

**Updated:** 2026-08-18
