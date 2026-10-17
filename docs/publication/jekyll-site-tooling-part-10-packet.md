# Part 10: Closing the Publishing Loop Without Pretending It Is a CMS

Status: local Part 10 and Hands-On 10A drafts, October 16, 2026. Part 9 and Hands-On 9A are committed in `3325443`; the Pages run for that commit succeeded, and a focused public request to Part 9 returned HTTP 200. The final pair remains uncommitted and unpublished pending Publisher review.

## Pre-draft source inventory

| Source | What it establishes | Limit |
| --- | --- | --- |
| `html/_posts/technology/`, the series post tree, and project `_posts/`; `html/_layouts/post.html`, `project.html`, `html/_includes/series_context.html`, `series_navigation.html` | Standalone, series, and project updates enter through different metadata and reader routes; post layout brings series links and engagement together | A project catalog entry can scaffold a landing page and starter draft, but it is not a finished article |
| `utils/bin/jekyll-site`, `.git/hooks/pre-commit`, `.pre-commit-config.yaml`, `.github/workflows/jekyll.yml`, Parts 2 and 8 | Local preview, focused and broad checks, human commit/push, production Pages build and validation | The numbered suite includes repairs; optional hooks are not proof of installation; Pages does not run every local check |
| `html/_includes/engagement.html`, `support_block.html`, `giscus_comments.html`, `getintouch.html`, `content_footer.html`, `_config.yml` | Shared support and public-discussion blocks on post/project layouts; contact link in shared footer; Giscus enabled with pathname mapping | The site does not own the GitHub Discussions service; configuration does not prove reader participation |
| `html/contact.md`, `html/_includes/contact_form.html`, `html/assets/js/contact-form.js` | Required fields, browser validation, encoded `mailto:` subject/body, fallback email link | The site does not submit form data to a site backend; the visitor must have a working mail client and send the draft. The generated draft includes page URL, referrer, and timestamp |
| `utils/bin/push-social-media`, `push-twitter`, `utils/README.md` | Operator-callable historical social helper scripts exist | No current workflow invokes them; do not call social posting automatic or describe these helpers as the present publication gate |
| `docs/workflows/blog-publishing.md`, current series posts, series outline and review journal | Post metadata/update policy and the established first-person series structure | The older generic `_drafts` workflow does not describe how this series was locally reviewed in the post tree |
| [Giscus documentation](https://giscus.app/) | Giscus maps page paths to GitHub Discussions and creates a discussion on first comment/reaction if none matches | Third-party behavior can change; article should describe this site's current `pathname` choice, not promise a discussion exists for each post |

## Fact status and drift

| Claim | Status | Treatment |
| --- | --- | --- |
| The post/project layouts append shared support and Giscus blocks | Implemented in current Liquid | Explain as common site presentation, with `comments: false` and `show_support: false` as opt-outs |
| The contact form is a static handoff to a local mail client | Implemented in current HTML/JavaScript | Say it composes a draft; do not call a click a sent message or a stored lead |
| Public comments remain attached after a canonical path changes | Not guaranteed with current pathname mapping | Connect discussion identity to stable URLs and redirect decisions |
| Social posts are automatically sent after deployment | Not established; no current Pages step invokes the old helpers | Describe short links as controlled sharing tools and posting as a human decision |
| Production build, live route, and reader response are one completed event | False | Separate source review, build, deployment, public checks, and subsequent contact/discussion |

## Privacy review

Public prose can name the public contact page and GitHub Discussions, but should not reproduce contact addresses, phone numbers, repository IDs, OAuth details, credential files, local paths, logs, or private project rows. A published form draft includes user-entered content plus page URL, referrer, and timestamp; the article may describe those fields without quoting any submission. The downloadable companion uses an invented post and placeholders only. The live-site check is a single public HTTP observation, not an assertion of complete site health or message delivery.

## Narrative outline

1. Open with the inadequacy of “write Markdown, push” as a description of this site. Return to the repeated problems that prompted the series.
2. Show three source paths: standalone article, series installment, and project update. Explain the front-matter contracts and Liquid views they enter, then converge them at author review.
3. Follow a concrete article through local preview, diagrams/code, listening, URL/taxonomy and production checks, changed-file review, and the human push decision. A lifecycle diagram marks those gates clearly.
4. Cross the Pages boundary and verify the served route, short/legacy redirect, and assets. A future date requires a later build; a successful job is not a reader-side crawl.
5. Explain the two reader-response paths: public GitHub Discussions through Giscus, keyed by pathname, and private contact through a JavaScript-created `mailto:` draft with a direct-link fallback. Place support and social sharing as optional human choices.
6. Offer a one-page publishing record template and companion exercise so readers can adapt the handoffs to their own site without running this repository's mutating suite or sending mail.
7. End with Current State and Next Work: the workflow is more dependable, but editorial acceptance, publication, correspondence, and maintenance remain human responsibilities.

## Validation and next gate

The article and companion were added to the Jekyll post tree with October 16 dates, forward navigation from Part 9, a 2:1 generated banner, editable Graphviz source with SVG/PNG renders, and a downloadable Markdown publication record. The diagram render was inspected. The short-link front-matter check and taxonomy check passed; the latter accepted 92 published and scheduled posts. An isolated production build to a temporary directory passed, with existing Sass deprecation warnings. The two post routes, both short redirects, diagram source and image, banner, and template exist in that output. Generated short-link and project-permalink redirect verifiers passed against the isolated build. Part 9 and the series landing page link to Part 10 in rendered HTML. The watched local server returned HTTP 200 for both new posts, the SVG, the template, and the series landing page. Playwright rendered both post routes; the main page showed series context, banner, diagram viewer link, source disclosure, companion link, support/discussion, and contact footer. Giscus returned a discussion-not-found warning for the unpublished local route, which is expected and not evidence of a site failure. No message was sent, discussion created, deployment performed, or server restarted. `git diff --check` passed.

Publisher review of voice, technical claims, visuals, links, and date is the next gate. No commit or push in this drafting turn.
