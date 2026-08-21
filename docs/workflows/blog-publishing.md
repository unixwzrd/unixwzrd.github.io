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
   tags: [tag1, tag2]
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
   tags: [tag1, tag2]
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
- Use relevant categories
- Add descriptive tags
- Be consistent with naming
- Check existing tags for ideas

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
