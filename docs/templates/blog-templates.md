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
```

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

### Project post URL slug (`slug`)

Permalinks for project posts are built from **`title`**, so a heading like `Secrets Kit 1.2:` becomes `secrets-kit-1-2-...` in the path. To use a shorter, stable segment without changing the visible title, set an explicit slug:

```yaml
slug: launchd-seckit-run-and-invisible-env-vars
```

(`slug` is normalized the same way as title-derived slugs: lowercased, non-alphanumeric → hyphens.)

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

All code presentation uses the shared post-skin rules in `html/_sass/minima/customizations/custom_code.scss`. Inline code, ordinary fenced blocks, and full-file disclosures should retain that common dark surface, spacing, scrollbar behavior, and accessible Rouge token palette. Do not add per-article background or token-color overrides; add a missing language token to the shared theme instead.

## Blog diagrams

Keep the Mermaid or Graphviz source with the publication material and generate both SVG and PNG assets. Embed the SVG through the shared diagram include; retain the PNG as a fallback or social-production asset.

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

Render Mermaid with `mmdc -b transparent`. Mermaid commonly emits `width="100%"` without an intrinsic height; the publication renderer replaces that percentage with explicit dimensions from the SVG `viewBox` so browsers preserve the diagram's aspect ratio inside the clickable figure. Before publication, inspect the SVG inside the actual article on the dark site rather than relying on an image previewer's default white background.

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

Posts get a deterministic short link for cut-and-paste on social:

- **Front matter:** `short_url: "https://unixwzrd.ai/s/<10 hex chars>/"` (optional but recommended; the build **validates** it if present).
- **Mechanism:** [`html/_plugins/01_short_link_injector.rb`](../../html/_plugins/01_short_link_injector.rb) (via [`case_preserving_permalinks.rb`](../../html/_plugins/case_preserving_permalinks.rb)) appends `/s/<code>/` to `redirect_from` using `SHA256(short_link_origin + "/" + <relative path>)`, where the relative path is the post file under `html/` (e.g. `projects/Foo/_posts/2026-01-01-slug.md`). Title, date, `slug`, and permalink edits do **not** change the code; **renaming or moving** the `.md` file does. [`jekyll-redirect-from`](https://github.com/jekyll/jekyll-redirect-from) serves the redirect.
- **Config:** `short_link_origin` in [`_config.yml`](../../_config.yml) (default `https://unixwzrd.ai`).

**Backfill** front matter after adding the plugin, changing `short_link_origin`, or **renaming/moving** post files:

```bash
bundle exec ruby scripts/backfill_short_url_front_matter.rb --dry-run
bundle exec ruby scripts/backfill_short_url_front_matter.rb
```

**Staged posts only** (fast; use from pre-commit or by hand):

```bash
bundle exec ruby scripts/backfill_short_url_front_matter.rb html/projects/MyProject/_posts/2026-01-01-example.md
bundle exec ruby scripts/backfill_short_url_front_matter.rb --staged   # git index: cached paths only
```

**Check without writing** (CI or sanity check):

```bash
bundle exec ruby scripts/backfill_short_url_front_matter.rb --check
bundle exec ruby scripts/backfill_short_url_front_matter.rb --check --staged
```

**Pre-commit:** optional [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) runs the script with `pass_filenames: true`, so only **staged** files under `html/**/_posts/` are updated. Jekyll still loads the full site once (~1s) for collision checks; it does **not** rescan every post on disk unless you run a **full** backfill with no path arguments.

**Local test:** `bundle exec jekyll serve` then open `http://localhost:4000/s/<code>/` (code from a post's `short_url`, or list `_site/s/` after build). Posts dated in the future are skipped until their date unless `future: true` in config or you run `jekyll build --future`.

**Verify:** `bundle exec jekyll build` (should succeed); optional `ls _site/s/` for redirect folders; open one `_site/s/<code>/index.html` and confirm canonical target URL.

**Updated:** 2026-05-02
