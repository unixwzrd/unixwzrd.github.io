# Blog Listing & Pagination

[← Back to Site Operations Guide](site-operations.md)

- [Blog Listing \& Pagination](#blog-listing--pagination)
  - [Configuration](#configuration)
  - [Excerpt \& Image Handling](#excerpt--image-handling)
  - [Client-Side Pagination](#client-side-pagination)
  - [Styling](#styling)

This section covers how blog listings and pagination work, including configuration, customization, and client-side navigation.

## Blog Listing & Pagination
- `/blog/` is the section and discovery hub; `/blog/all/` is the complete chronological archive of visible main and project posts.
- Main blog, complete archive, and project blog post limits are configurable in `_config.yml` (`site_blogs_count`, `archive_posts_count`, and `project_blog_count`). The archive's selectable sizes come from `archive_page_sizes`.
- Excerpts are auto-generated from post content, strip images, and are truncated to a configurable word count (`excerpt_word_limit`).
- Pagination is handled client-side via JavaScript and Liquid, not by Jekyll's built-in `paginate` feature. Page links use bookmarkable URLs such as `?page=2` and work with browser Back and Forward navigation.
- Pagination controls are styled for dark backgrounds and accessibility.

### Configuration
- Set `site_blogs_count`, `archive_posts_count`, and `project_blog_count` in `_config.yml` to control the number of posts per page for main blog listings, the complete archive, and project blogs respectively.
- Set `archive_page_sizes` to the permitted choices in the archive's Posts per page selector. Keep `archive_posts_count` among those choices.
- Set `excerpt_word_limit` in `_config.yml` to control the number of words in each excerpt.
- The shared `blog_list.html` include also accepts `limit` for a fixed-size listing or `posts_per_page` for a complete paginated listing.

### Excerpt & Image Handling
- Excerpts are generated from the first part of the post content.
- All image tags (Markdown and HTML) are stripped from excerpts.
- Excerpts are truncated to the configured word limit.

### Client-Side Pagination
- Pagination is implemented with JavaScript and Liquid.
- The page number and non-default page size are reflected in the URL, for example `?per_page=25&page=2`.
- Previous and Next are ordinary links, so reloads, bookmarks, and browser history behave predictably.

### Styling
- Pagination controls are styled for dark backgrounds.
- Links and page information are spaced and accessible.
