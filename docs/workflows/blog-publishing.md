# Blog Publishing Guide

## Overview
This guide covers the process of creating and publishing blog posts, both for general blogs and project-specific blogs.

## Directory Structure
```
html/
├── _posts/                    # General blog posts
│   ├── series/Series-Slug/   # Series membership takes precedence
│   └── category/             # Standalone posts by primary category
└── projects/
    └── ProjectName/
        ├── _drafts/          # Work in progress posts
        │   └── draft.md
        └── _posts/           # Published project posts
            └── YYYY-MM-DD-project-name-title.md
```

## Creating a New Post

### General Blog Post

The ordered blog landing-page cards, recent-post sections, and Blog navigation entries are configured in `html/_data/blog_sections.yml`. Move an entry to reorder it or set `visible: false` to hide it from those discovery surfaces without changing its posts, category, page, or URLs.

1. Create the dated file under `html/_posts/series/<series-slug>/` for a series article, or `html/_posts/<primary-category>/` for a standalone article:
   ```
   YYYY-MM-DD-descriptive-title.md
   ```

2. Add front matter:
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   date: YYYY-MM-DD HH:MM:SS -0500
   categories: [category1, category2]
   tags: [ai, developer-workflow]
   ---
   ```

3. Add content with excerpt marker:
   ```markdown
   Brief introduction (this will appear in previews).

   <!--more-->

   Rest of your post content...
   ```

### Project blog post

1. Create draft in `html/projects/ProjectName/_drafts/`, then move to `_posts/` with a dated name when ready:
   ```bash
   mv _drafts/title.md _posts/YYYY-MM-DD-short-descriptive-title.md
   ```
2. Set the immutable **`permalink_slug:`** for every project post. It controls the canonical URL independently of the title and filename and must not change after publication. See [templates/blog-templates.md](../templates/blog-templates.md).
3. Optional but recommended: add **`short_url`** after the first build or run:
   ```bash
   bundle exec ruby scripts/backfill_short_url_front_matter.rb html/projects/ProjectName/_posts/YYYY-MM-DD-....md
   ```
   The backfill freezes `short_link_basis` and derives `short_url` from it. Normal edits and later directory moves do not invalidate the code. Do not change the basis after publishing.

4. Example front matter:
   ```yaml
   ---
   layout: post
   title: "Your Project Post Title"
   permalink_slug: your-project-post-title
   date: YYYY-MM-DD
   category: ProjectName
   content_type: release
   tags: [python, developer-tools]
   ---
   ```

5. Add content with the same `<!--more-->` excerpt pattern as general posts.

## Post Guidelines

### Content Structure
1. Start with brief introduction
2. Use `<!--more-->` to mark excerpt end
3. Use clear headings (h2, h3)
4. Include relevant links
5. Add images if helpful

### Formatting
1. Use markdown for formatting
2. Include code blocks with syntax highlighting:
   ````markdown
   ```python
   def example():
       print("Hello, World!")
   ```
   ````
3. Use lists and tables as needed
4. Add images with alt text:
   ```markdown
   ![Alt text](/path/to/image.png)
   ```

### Categories and Tags
- Categories select the editorial section; project categories associate project posts with their project.
- `series` identifies an ordered article series.
- `content_type` describes what the post is: `introduction`, `release`, `update`, or `reference`. Omit it for an ordinary article.
- Choose approximately 2-6 topical tags from `html/_data/tag_taxonomy.yml`; do not invent an alias in post front matter.
- Run `bundle exec ruby scripts/list_tags.rb` to see the valid tags without opening the website.
- A Jekyll build fails when a published or scheduled post uses an unknown, retired, or aliased tag.

## Secrets Kit product section

The existing `/projects/Secrets-Kit/` URL is the product entry point, with the project blog under `#updates`. Its `product_hub: secrets-kit` marker activates the shared overview when Get Started is a loaded product page. Navigation is derived from loaded destinations and ordered by `product_nav_order`; no deployment flags or plugins are required.

The seven supporting pages under `html/projects/Secrets-Kit/` are `get-started.md`, `guides.md`, `remote-sync.md`, `pricing.md`, `compare.md`, `security.md`, and `support.md`. They are now `published: true` so a normal production build can publish the **coming-soon announcement**. This is separate from making the software or subscriptions available. The local server can still preview unpublished material; do not add `--unpublished` to deployment. Unpublished source committed to a public repository remains readable on GitHub.

`html/_data/secrets_kit.yml` holds the selected website release target, `release_tag: v2.0.2`, and `production_release_ready: false`. While readiness is false, Get Started explains final testing, release links and the copy control are withheld, documentation references lead to the local release-status explanation, and pricing is identified as planned launch pricing. Visitors can follow updates in project Discussions and report bugs in project Issues. Private material goes to Contact. No installer falls back to version 1, a beta, or `releases/latest`.

After testing and the product's existing promotion process are complete, verify that the immutable `v2.0.2` production release contains the approved installer, documentation, and complete Hermes integration. Verify the one-URL Hermes setup against that exact artifact, including the removal of beta-only configuration. This website setting does not create a tag, merge DEV into main, publish a release, or activate billing. Those are separate authorized actions in their respective repositories and services.

For actual availability, set `production_release_ready: true` only after both the production artifact and the advertised hosted service are approved and available. Documentation, installer, and concise agent handoff links then use the shared release tag automatically. Refresh prices and source dates, verify platform coverage, terms, recovery and cancellation behavior, and update the landing-page fallback/excerpt and persistent catalog description in `html/_data/repos.yml` (then refresh the generated catalog using the existing workflow). Update availability assertions for that reviewed status change. The $5/connection/month, minimum-two offer is a content baseline, not proof of live billing.

The comparison has two feature matrices and a searchable catalog of 32 alternatives and adjacent tools. Its primary-source notes, architectural qualifications, pricing units and periods, availability labels, and design observations are maintained in `html/_data/secrets_kit_competitors.yml`. Keep early-access, experimental, historical, and unresolved offerings distinct from available services. Key wrapping, threshold splitting, account recovery, server-side encryption, offline caching, and failover are separate properties. Never turn an unverified feature into a negative checkmark or imply independent security testing from a documentation review.

To withdraw the product section, unpublish all seven supporting pages together. Removing Get Started from loaded pages restores the landing-page fallback and previous blog placement; the fallback now describes the upcoming release rather than the superseded version 1/beta offer. Git commits, pushes, announcements, product promotion, and live billing activation remain separate actions.

Validate isolated production and unpublished-preview builds without replacing the running local server's output. Run `SECKIT_PRODUCTION_SITE=/path/to/production SECKIT_PREVIEW_SITE=/path/to/preview bundle exec ruby scripts/test_secrets_kit_product.rb`, the reader-experience suite, and the existing permalink, redirect, taxonomy, and internal-link checks. Verify that ordinary production includes the public teaser pages without future installer/tag links. Inspect desktop/mobile layouts, keyboard access, support routes, search/category filtering, empty states, and the catalog without JavaScript. The eventual ready state and short handoff are also covered by focused fixture assertions. `bundle exec ruby scripts/test_secrets_kit_product.rb` runs source and fixture checks without a build.

## Publishing Process

1. **Draft Stage**
   - Write post in _drafts
   - Preview locally
   - Get feedback if needed

2. **Pre-publish Checks**
   - Run spell check
   - Verify front matter
   - Check links
   - Test code samples

3. **Publishing**
   - Move to _posts with date
   - Run pre-commit checks
   - Commit changes
   - Push to repository

4. **Post-publish**
   - Verify on site
   - Check links work
   - Share on social media

## Post-publish updates

After a post is live, **do not change** publish `date`, filename, `slug`, permalink, or `short_link_basis`. A directory-only move is safe when the basis is retained. See **[post-updates-and-ordering.md](post-updates-and-ordering.md)** for the full policy.

| Change type | Front matter | List order |
|---|---|---|
| Silent fix | (none) | Unchanged |
| Technical correction | `corrected_at`, `correction_note` | Unchanged |
| Major rewrite | `update_notice`, `last_modified_at` | Promoted on homepage / section blogs |

Date-only values (`2026-08-15`) are fine; time and timezone are optional.

## Common Issues

### Front Matter
- Missing required fields
- Incorrect date format
- Invalid categories/tags

### Content
- Missing excerpt marker
- Broken links
- Invalid markdown
- Missing alt text

### Build
- Date in future (use `jekyll build --future` locally if needed)
- Duplicate permalinks
- Invalid front matter
- **`short_url` mismatch** - run `scripts/backfill_short_url_front_matter.rb` (see [templates/blog-templates.md](../templates/blog-templates.md))

## Tips and Tricks
1. Use templates for consistency
2. Preview locally before publishing
3. Keep drafts organized
4. Use meaningful file names
5. Follow naming conventions
