# Part 9: Monitoring a Static Site After Deployment

Status: local article and Hands-On 9A draft for Publisher review, dated October 11, 2026. No commit or push in this drafting turn.

## Pre-draft source inventory

| Source | Evidence used | Boundary |
| --- | --- | --- |
| `utils/bin/site_crawl_check.py` | Reads the served sitemap; fetches same-host sitemap pages, links, and images; reports HTTP failures | Follows redirects but does not verify the destination; skips other-host assets and does not parse every linked page unless the sitemap lists it |
| `utils/bin/site_reliability_monitor.py` and `utils/bin/test_site_reliability_monitor.py` | Source-derived critical-page discovery, response checks, images, Markdown external-link checks, log/config writes, email paths; two focused discovery tests passed on October 11 | It does not perform a separate rendered internal-link crawl; source discovery is incomplete for nested series posts and can include unpublished source; post-commit mode checks immediately despite stale help text |
| `utils/bin/periodic_monitor.sh`, `post_commit_monitor.sh`, `setup_crontab.sh`, `setup_site_monitoring.sh` | Callable wrappers and setup instructions exist | The scripts' presence is not proof of an installed schedule or successful alert delivery; setup writes local configuration and is outside this review |
| `utils/bin/manage_monitoring_pages.py`, `scheduled_tasks.py` | Page-management interface and maintenance methods inspected | Page-management calls `list_missing_pages` and `remove_pages_from_monitoring`, which the current monitor class lacks; several scheduled maintenance methods only log success and return true |
| `.github/workflows/jekyll.yml`, `docs/guides/monitoring.md`, `docs/guides/strategy.md` | Pages workflow only builds, verifies, and deploys; guides describe recommended cron/post-commit monitoring | Guides say post-commit mode waits and imply automatic schedules; current code checks immediately and workflow has no monitoring job |
| `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-11-12-checks-repairs-and-the-gates-before-deployment.md` | Part 8's local/Pages gate distinction and forward title | Part 9 must begin on the other side of deployment and avoid repeating the whole pre-commit inventory |
| GitHub Pages workflow run `38173106123` and live Part 8 URL, checked October 11 | Run for commit `186bfa7` completed successfully; live Part 8 returned HTTP 200 | One successful build and one HTTP request do not establish ongoing reliability or full-route health |

## Fact status and drift

| Claim | Status | Editorial treatment |
| --- | --- | --- |
| The served-site crawler can find missing same-host sitemap pages, linked pages, and images | Implemented; a local fixture exercise will be validated separately | Show it as an explicit command, not an automatic post-deploy gate |
| The reliability monitor can check configured/source-derived pages and images and source Markdown external links | Implemented; only its two discovery unit tests were run for this draft | Distinguish source-derived checks from a crawl of the deployed HTML |
| Monitoring is scheduled and emails reach the Publisher | Not established | Describe the available wrappers and configuration without claiming active scheduling or delivery |
| Post-commit mode waits for deployment | Documented but contradicted by current method body | Say it checks immediately; a commit event is not a deployment-complete signal |
| The page-management script tracks and removes missing pages | Not implemented end to end in the inspected class | Do not offer it as a working operator workflow |
| Every named scheduled maintenance task performs its named audit or repair | False for multiple current methods | Omit those methods from monitoring capability claims |

## Privacy and artifact boundary

Public prose uses repository-relative utility names and generic loopback fixture URLs. Do not print the ignored monitor JSON, SMTP values, addresses, recipients, passwords, OAuth material, runtime logs, user crontab, machine-specific paths, or internal hostnames. The local lab binds to loopback and uses invented pages; it does not send email, alter monitor configuration, or crawl a public site. Any discussion of the October 11 live check names only the public site and workflow run.

## Narrative outline

1. Start with the successful Pages run and the narrower fact it proves. A page may be missing later, or a redirect may land on the wrong page.
2. Explain the deployed-site crawler from the reader's side: sitemap seed, HTTP fetches, same-host links and images, failure report, and blind spots.
3. Contrast the source-derived reliability monitor: core/project pages, image probes, external links extracted from Markdown, local state and optional email. Explain the cost and incomplete discovery rather than calling it comprehensive.
4. Separate callable monitoring, configured schedules, actual invocation, and human investigation. Correct the stale post-commit waiting claim and note that Pages does not run either monitor.
5. Offer a small loopback lab with a healthy page, missing image, and a redirect to the wrong destination. It demonstrates why status and destination are separate assertions without touching the real monitor.
6. End with Current State and Next Work, handing the human publication loop to Part 10.

## Validation and next gate

The two existing monitor discovery tests passed on October 11. The isolated lab's healthy scenario exited 0; its missing-image and wrong-redirect scenarios each exited 1 for the expected reason. The DOT source rendered to SVG and PNG and was inspected visually. The short-link front-matter check passed for both new posts; taxonomy accepted 89 published and scheduled posts. A production Jekyll build and a future-inclusive development build passed. Both post routes, both generated short routes, the downloadable lab, and the diagram assets exist in the production output; the new post routes, lab source, and SVG returned HTTP 200 from the local preview. The generated short-link and project-permalink redirect verifiers passed against production output. Playwright showed Part 9's banner, series context, diagram and source link, Current State/Next Work, the Part 8 forward link, and the Hands-On 9A source disclosure with a download link. Giscus reported no discussions yet for these local-only routes. `git diff --check` passed. Publisher review remains the next editorial gate; no commit or push occurred in this drafting turn.
