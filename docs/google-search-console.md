# Google Search Console and Search Visibility

## What Google Search Console Is

Google Search Console (GSC) is Google's site-owner tool for understanding how
your site appears in Google Search. It complements GA4:

- GA4 shows what visitors do once they arrive.
- GSC shows how Google discovers, indexes, and presents your site.

Use it to monitor:

- search queries and impressions
- page clicks and CTR
- indexing and crawl issues
- sitemap status
- canonical and coverage problems

## Initial Setup

1. Add the canonical property for `https://unixwzrd.ai`.
2. Verify ownership.
3. Submit `https://unixwzrd.ai/sitemap.xml`.
4. Confirm the sitemap is processed without errors.

Recommended verification order:

1. DNS verification at the domain level when possible.
2. HTML tag verification if you want page-level ownership confirmation.

## Sitemap Notes

The site already builds `sitemap.xml` via `jekyll-sitemap`.

- `robots.txt` advertises the sitemap location.
- Hidden utility content should stay out of the sitemap.
- New public posts and project pages should appear automatically after deploy.

Operational checks:

- verify `https://unixwzrd.ai/sitemap.xml` returns `200`
- inspect a newly published URL in GSC after deploy
- monitor the `Pages` report for excluded or broken URLs

## Suggested GSC Workflow

### Weekly

- check `Performance` for new queries and rising pages
- review `Pages` for indexing errors or unexpected exclusions
- inspect any newly published post that does not appear after a reasonable crawl window

### After Publishing New Content

- confirm the page is in the sitemap
- run URL Inspection
- request indexing only if the page is important and not discovered quickly

### When 404s Rise

- compare GSC crawl errors with GA4 `404_error` events
- add redirects for high-value legacy URLs
- fix internal links or stale external references

## GA4 Custom Definitions to Add

For the new analytics events to be useful in reports, add GA4 custom dimensions
for these event parameters:

- `page_type`
- `page_category`
- `page_tags`
- `page_hostname`
- `visitor_type`
- `not_found_path`
- `not_found_query`
- `not_found_referrer`
- `referrer_host`
- `destination_url`
- `destination_hostname`
- `link_text`
- `search_term`
- `result_url`
- `result_count_bucket`
- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_term`
- `utm_content`

## Recommended GA4 Reports

### 404 analysis

- event name = `404_error`
- dimensions: `not_found_path`, `not_found_query`, `referrer_host`, `visitor_type`

### outbound engagement

- event name = `outbound_click`
- dimensions: `destination_hostname`, `destination_url`, `page_type`

### internal search

- event names:
  - `site_search`
  - `site_search_zero_results`
  - `site_search_result_click`
- dimensions: `search_term`, `result_count_bucket`, `result_url`, `visitor_type`
