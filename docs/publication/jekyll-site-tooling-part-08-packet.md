# Part 8: Checks, Repairs, and the Gates Before Deployment

Status: local review draft for the Jekyll post tree, October 11, 2026. At the Publisher's direction, the post and companion now carry October 11 front-matter dates after Part 7. The Publisher explicitly reserved the push until after review and validation. They are eligible for the next production build but are not live yet.

## Source and claim boundaries

| Source | What it establishes | Limit |
| --- | --- | --- |
| `utils/bin/check_site.sh` and `utils/bin/checks/*.sh` | Filename-order runner with `--list`, `--run`, and `--skip`; individual checks cover dependencies, links, builds, metadata, images, and cleanup | Several steps install, regenerate, rewrite, stage, or rebuild; warnings from Liquid and navigation steps do not fail the suite |
| Installed `.git/hooks/pre-commit` | Calls `check_site.sh --skip 05_update_project_data.sh` | Runner compares extensionless names, so the skip misses; this local hook is not a versioned repository contract |
| `.pre-commit-config.yaml` | Defines optional focused short-link and tag hooks | Configuration does not prove installation in a clone |
| `utils/bin/jekyll-site` and link-check scripts | Production build wrapper; `-c` opts into HTMLProofer, while external checking needs explicit opt-in | Builds replace generated output; external checks depend on network state |
| `.github/workflows/jekyll.yml` | Push-to-main/manual production build, short-link/project redirect checks, tag check, Pages upload/deploy | Does not run the whole numbered local suite, crawl the live site, or rebuild merely because a future post date has arrived |
| `html/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py` | Runnable Python fixture with front-matter, local-link, and image gates | Teaching exercise only; no Jekyll, Ruby plugin, external service, or site-repository check is run |

## Editorial boundaries

The article opens with the problem a successful build can miss, then names the different local and CI gates. It calls out the observed hook skip mismatch instead of repeating the stale outline claim that refresh is skipped. The generated-data, front-matter, image, and cleanup steps are described as mutating. The companion uses invented files in a caller-chosen new directory and never invokes the site's check suite. The diagram is explanatory, not a runtime trace.

Do not present a clean build as editorial acceptance or deployment proof. Do not present the installed hook as a push hook or the optional pre-commit configuration as installed. A future-dated post is excluded from production builds until it is eligible and a new build runs.

On October 11, direct requests to the live site returned HTTP 200 for Parts 1 and 2 and HTTP 404 for Parts 3, 4, and 7. Part 3's October 8 date had already passed. `gh run list --workflow jekyll.yml` showed that the last successful Pages run, [37534099551](https://github.com/unixwzrd/unixwzrd.github.io/actions/runs/37534099551), was created October 6 at 21:28 UTC from `38d7e2e`. The workflow has no schedule. The article uses this as a dated real example of why a future date does not cause publication.

## Local validation

The lab's clean scenario passed all three gates. Its missing-title, broken-link, and missing-image scenarios each exited 1 at the intended gate and retained their fixture. Short-link front matter was generated and checked through the repository's Ruby backfill tool. The future-inclusive development Jekyll build passed; the article, companion, both short routes, the source file, and the SVG are present in its output, and the series landing lists both posts. After moving dates, a production build passed and includes Parts 4 through 8 and their companions on October 11. All nine old dated routes produce redirects to their new canonical routes; all nine short-link identities are unchanged and resolve to October 11. The short-link front-matter, generated redirects, project redirects, and tag taxonomy validators passed; the taxonomy checker accepted 87 published and scheduled posts. Playwright opened the moved Part 7, Part 8, and Hands-On 8A routes. It showed the Part 8 banner, series context, diagram and editable-source links; verified Part 7's forward link and Part 8's companion link; and confirmed the companion's source disclosure expands to a download link. The new article's Giscus requests returned 404 in preview because no discussion exists for it yet. No Pages push or live-speech request occurred.

The focused `check_site.sh --run 03_jekyll_doctor` pass returned 0 through its wrapper, while Jekyll doctor itself exited 1 after warning about case-only URL pairs on the macOS filesystem. The wrapper explicitly treats that result as nonfatal unless `STRICT_JEKYLL_DOCTOR=1` is set. The article says so rather than counting the wrapper exit as a clean doctor result.
