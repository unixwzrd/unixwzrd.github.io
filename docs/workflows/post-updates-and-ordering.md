# Post updates, corrections, and list ordering

Policy and implementation for how published articles are surfaced after edits, how series order is preserved, and what must **never** change after publish (permalinks and short links).

**Related:** [blog-publishing.md](blog-publishing.md), [templates/blog-templates.md](../templates/blog-templates.md)

---

## Principles

1. **Publish `date` is permanent** — it anchors the permalink. Do not change it after publish.
2. **Filename and slug are permanent** — they help anchor the canonical permalink. Directory moves are safe only after `short_link_basis` has been frozen.
3. **Three tiers of post-publish change** — silent fix, technical correction, major update (see below).
4. **Discovery lists ≠ series lists** — homepage and section blogs may promote major updates; series index pages always follow reading order.

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

**When:** Typo, broken link, wording tweak — nothing a reader needs to be told about.

**Front matter:** None required.

**Effect:** Content changes only. No list reorder, no badge, no extra dates on the page.

---

## Tier 2: Technical correction

**When:** Wrong command, incorrect port, factual error in a code sample — worth recording, not a rewrite.

**Front matter:**

```yaml
date: 2025-04-08                    # unchanged
corrected_at: 2026-08-10            # date only is fine; time/timezone optional
correction_note: "Fixed the attach port example (5678 → 5679)."
```

**Effect:**

- Article header: `Published … · Technical correction …`
- Subtle `post-correction-notice` on the article page when `correction_note` is set
- **No** promotion in homepage or section blog lists
- **No** “Updated” badge

Optional: set `last_modified_at` for schema.org `dateModified` in structured data; it does **not** show in the header unless `update_notice` is also set.

---

## Tier 3: Major update

**When:** Substantial rewrite, new sections, companion tutorial, or anything worth resurfacing.

**Front matter:**

```yaml
date: 2025-04-08                    # unchanged
last_modified_at: 2026-08-15        # date only is fine
update_notice_title: "Updated August 2026"
update_notice: "I rewrote this article around SSH key authentication…"
```

**Effect:**

- Article header: publish date + **Updated** date (when `last_modified_at` is set)
- Prominent `post-update-notice` callout on the article page
- **Promoted** in discovery lists (homepage “Latest Updates”, `blog_list.html` sections) via `list_sort_key`
- **Updated** badge in those list views

`update_notice` is the opt-in signal for promotion. No separate `promote_update` flag.

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
| `list_date` | Effective date for display when promoted |
| `list_sort_key` | Numeric sort key for Liquid (`list_date` + `sequence` tiebreaker) |

**Rules:**

- Default: `list_date` = publish `date`
- If `update_notice` is set and `last_modified_at` is later than `date`, `list_date` = `last_modified_at`
- Same-day ties: lower `sequence` sorts first (e.g. PA Awareness introduction → part 5 on 2025-09-25)
- `list_sort_key` is a **zero-padded inverted epoch string** so Liquid's `sort` filter (lexicographic, ascending) yields newest-first

**Used by:**

- [`html/_includes/filter_discovery_posts.html`](../../html/_includes/filter_discovery_posts.html) — shared publishability filter (excludes drafts, `_drafts/`, `*-social-posts.txt` sources, `published: false`, `list_exclude: true`)
- [`html/_includes/discovery_post_list.html`](../../html/_includes/discovery_post_list.html) — homepage Latest Updates
- [`html/_includes/blog_list.html`](../../html/_includes/blog_list.html) — section and project blogs
- [`html/_includes/post_list_meta.html`](../../html/_includes/post_list_meta.html) — shared list metadata + Updated badge

**Not used by:**

- Series index pages (use `series_order`)
- Tag pages (`topics.md` — still chronological by publish `date`)
- Prev/next series navigation (`series_previous_url` / `series_next_url`)

---

## Series ordering

Series reading order is **not** publish date. Use explicit navigation URLs plus a numeric sort key on the series index page.

| Field | Role |
|---|---|
| `series` | Series title (must match across posts) |
| `series_part` | Display label (`1`, `2`, `2A`, …) |
| `series_order` | Sort key on the series index (gaps of 10: `10`, `20`, `25`, `30`) |
| `series_previous_url` / `series_next_url` | Prev/next navigation chain |
| `series_companion_of` | Optional — hands-on companion to part N |

**Example** (Local First AI and Agent Operations):

| Part | `series_part` | `series_order` |
|---|---|---|
| Main installment 1 | `1` | `10` |
| Main installment 2 | `2` | `20` |
| Hands-on companion | `2A` | `25` |
| Main installment 3 | `3` | `30` |

Series index: [`html/blog/series/local-first-ai-and-agent-operations.md`](../../html/blog/series/local-first-ai-and-agent-operations.md) sorts by `series_order`.

Major updates to a series post **do not** change its position on the series index — it stays Part N.

---

## URLs and short links after edits

| Change | Permalink | `short_url` |
|---|---|---|
| Edit body / add `update_notice` | Unchanged | Unchanged |
| Change publish `date` | **Breaks** | Unchanged |
| Rename/move `.md` file | May break | **Breaks** — re-run backfill |
| Add `redirect_from` | Old paths redirect | Unchanged |

See [templates/blog-templates.md](../templates/blog-templates.md#social-short-urls-s) for short-link backfill and CI checks.

---

## Quick reference

| Intent | Set | List promotion | On-page signal |
|---|---|---|---|
| Typo fix | (nothing) | No | None |
| Technical correction | `corrected_at`, `correction_note` | No | Header + subtle notice |
| Major rewrite | `update_notice`, `last_modified_at` | Yes | Header + update callout + list badge |
| Series installment | `series_order`, nav URLs | By publish/update rules | Series context block |

---

**Updated:** 2026-08-15
