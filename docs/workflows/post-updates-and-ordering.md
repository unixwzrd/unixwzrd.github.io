# Post updates, corrections, and list ordering

Policy and implementation for how published articles are surfaced after edits, how series order is preserved, and what must **never** change after publish (permalinks and short links).

**Related:** [blog-publishing.md](blog-publishing.md), [templates/blog-templates.md](../templates/blog-templates.md)

---

## Principles

1. **Publish `date` is permanent** - it anchors the permalink. Do not change it after publish.
2. **Filename and slug are permanent** - they help anchor the canonical permalink. Directory moves are safe only after `short_link_basis` has been frozen.
3. **Three tiers of post-publish change** - silent fix, technical correction, major update (see below).
4. **Discovery lists ≠ series lists** - homepage, project, and section blogs follow original publication dates; series index pages always follow reading order. Edits and release notices never promote old articles.

---

## What must not change after publish

| Field / file | Why |
|---|---|
| `date` (publish date) | Permalink path (`/YYYY/MM/DD/slug/`) |
| Filename | Canonical post slug unless overridden explicitly |
| `slug` / `permalink` (if set) | Canonical URL |
| `short_link_basis` | Immutable `short_url` hash input |

Once `short_link_basis` is present, a source-directory reorganization does not change the short link. Do not rewrite the basis to match the new location.

Content edits, new sections, and optional front matter below are safe.

---

## Tier 1: Silent fix

**When:** Typo, broken link, wording tweak - nothing a reader needs to be told about.

**Front matter:** None required.

**Effect:** Content changes only. No list reorder, no badge, no extra dates on the page.

---

## Tier 2: Technical correction

**When:** Wrong command, incorrect port, factual error in a code sample - worth recording, not a rewrite.

**Front matter:**

```yaml
date: 2025-04-08                    # unchanged
corrected_at: 2026-08-10            # date only is fine; time/timezone optional
correction_note: "Fixed the attach port example (5678 → 5679)."
```

**Effect:**

- Article header: `Published ... · Technical correction ...`
- Subtle `post-correction-notice` on the article page when `correction_note` is set
- **No** promotion in homepage or section blog lists
- **No** "Updated" badge

Optional: set `last_modified_at` for schema.org `dateModified` in structured data; it does **not** show in the header unless `update_notice` is also set.

---

## Tier 3: Major update

**When:** Substantial rewrite, new sections, or other editorial changes worth recording.

**Front matter:**

```yaml
date: 2025-04-08                    # unchanged
last_modified_at: 2026-08-15        # date only is fine
update_notice_title: "Updated August 2026"
update_notice: "I rewrote this article around SSH key authentication..."
```

**Effect:**

- Article header: publish date + **Updated** date (when `last_modified_at` is set)
- Prominent `post-update-notice` callout on the article page
- **No promotion** in discovery lists (homepage "Latest Updates", `blog_list.html` sections)
- **Updated** badge in those list views when an explicit modified date is supplied

`update_notice` records an editorial change. It does not affect sorting; do not change `date` to resurface an article.

**Example:** [Remote Debugging with VS Code](/technology/2025/04/08/Remote-Debugging-With-VSCode/).

---

## Date format in front matter

Date-only values work and are preferred when time of day does not matter:

```yaml
date: 2025-04-08
last_modified_at: 2026-08-15
corrected_at: 2026-08-10
```

Jekyll treats them as midnight in the site timezone. Use `sequence` when multiple posts share the same publish day (see below). Full timestamps with timezone are optional.

---

## Discovery list sorting

**Plugin:** [`html/_plugins/02_post_list_metadata.rb`](../../html/_plugins/02_post_list_metadata.rb)

At build time each post gets:

| Field | Purpose |
|---|---|
| `list_date` | Original publication date |
| `list_sort_key` | Numeric sort key for Liquid (`list_date` + `sequence` tiebreaker) |

**Rules:**

- Always: `list_date` = publish `date`, regardless of `update_notice`, `last_modified_at`, or automatic release notices
- Same-day ties: lower `sequence` sorts first (e.g. PA Awareness introduction → part 5 on 2025-09-25)
- `list_sort_key` is a **zero-padded inverted epoch string** so Liquid's `sort` filter (lexicographic, ascending) yields newest-first

**Used by:**

- [`html/_includes/filter_discovery_posts.html`](../../html/_includes/filter_discovery_posts.html) - shared publishability filter (excludes drafts, `_drafts/`, `*-social-posts.txt` sources, `published: false`, `list_exclude: true`)
- [`html/_includes/discovery_post_list.html`](../../html/_includes/discovery_post_list.html) - homepage Latest Updates
- [`html/_includes/blog_list.html`](../../html/_includes/blog_list.html) - section and project blogs
- [`html/_includes/post_list_meta.html`](../../html/_includes/post_list_meta.html) - shared list metadata + Updated badge

**Not used by:**

- Series index pages (use `series_order`)
- Tag pages (`topics.md` - still chronological by publish `date`)
- Prev/next series navigation (`series_previous_url` / `series_next_url`)

---

## Automatic product release notices

For a shipped release announcement under `html/projects/<Product>/_posts/`, add these fields to the new post:

```yaml
release_version: "1.3.5"
release_status: released
```

Jekyll selects the newest published, explicitly released announcement for each product by its original publication date. If publishing multiple releases on the same day, give their `date` fields full timestamps so their order is unambiguous. The shared `product_release_notice.html` include adds the existing blue-accent callout to older product announcements, linking to the product overview first and the selected release announcement second. Its feature summary comes from the selected post's `excerpt`, or an optional `release_summary`. Future releases require metadata on the new announcement only: do not edit every older post or add a manual supersession notice.

Use `release_status: preview` for coming-soon or review-stage announcements. A version number or `content_type: release` alone never qualifies a post as shipped. Drafts, unpublished posts, future-dated announcements, hidden products, and list-excluded/social-post sources cannot become release targets, even in an inclusive local preview. The product overview must exist before a notice is generated. This selects the latest released announcement on the site; it does not poll GitHub or the App Store, modify product versions, or publish anything.

Older posts with `content_type: release`, `update`, or `introduction` receive the notice automatically. For legacy posts without a content type, use `release_version` or `release_notice: true` to opt in. Use `release_notice: false` to suppress it on an individual article. Unclassified case studies and tutorials are left alone. The selected release, later previews, and articles covering the same version do not receive a misleading older-release notice.

Keep genuine editorial `update_notice` and modification dates when the article itself changes; those remain independent of automatic release pointers. Automatic notices do not create an "Updated" badge, alter article bodies, or change publication dates, permalinks, or short links. Implementation: `html/_plugins/product_release_notices.rb`. Regression checks run through `scripts/test_reader_experience.rb`, including in GitHub CI.

## Series ordering

Series reading order is **not** publish date. Use explicit navigation URLs plus a numeric sort key on the series index page.

| Field | Role |
|---|---|
| `series` | Series title (must match across posts) |
| `series_part` | Display label (`1`, `2`, `2A`, ...) |
| `series_order` | Sort key on the series index (gaps of 10: `10`, `20`, `25`, `30`) |
| `series_previous_url` / `series_next_url` | Prev/next navigation chain |
| `series_companion_of` | Optional - hands-on companion to part N |

**Example** (Local First AI and Agent Operations):

| Part | `series_part` | `series_order` |
|---|---|---|
| Main installment 1 | `1` | `10` |
| Main installment 2 | `2` | `20` |
| Hands-on companion | `2A` | `25` |
| Main installment 3 | `3` | `30` |

Series index: [`html/blog/series/local-first-ai-and-agent-operations.md`](../../html/blog/series/local-first-ai-and-agent-operations.md) sorts by `series_order`.

Major updates to a series post **do not** change its position on the series index - it stays Part N.

---

## URLs and short links after edits

| Change | Permalink | `short_url` |
|---|---|---|
| Edit body / add `update_notice` | Unchanged | Unchanged |
| Change publish `date` | **Breaks** | Unchanged |
| Rename/move `.md` file | May break | **Breaks** - re-run backfill |
| Add `redirect_from` | Old paths redirect | Unchanged |

See [templates/blog-templates.md](../templates/blog-templates.md#social-short-urls-s) for short-link backfill and CI checks.

---

## Quick reference

| Intent | Set | List promotion | On-page signal |
|---|---|---|---|
| Typo fix | (nothing) | No | None |
| Technical correction | `corrected_at`, `correction_note` | No | Header + subtle notice |
| Major rewrite | `update_notice`, `last_modified_at` | No | Header + update callout + list badge |
| Product release | `release_version`, `release_status: released` | No | Automatic pointers on older announcements |
| Series installment | `series_order`, nav URLs | By publish date | Series context block |

---

**Updated:** 2026-11-26

