# Project overview: unixwzrd.ai

This repository builds the Distributed Thinking Systems website at [unixwzrd.ai](https://unixwzrd.ai). Jekyll source lives under [html/](../html/); canonical operational and authoring tools live under [utils/](../utils/). The [documentation index](README.md) is the entry point, and [utils/README.md](../utils/README.md) is the verified command catalog.

## Repository responsibilities

| Area | Responsibility |
| --- | --- |
| [html/](../html/) | Jekyll pages, layouts, includes, collections, posts, product content, and site assets. |
| [utils/bin/](../utils/bin/) | Maintained authoring, validation, site-service, monitoring, and operator commands. |
| [utils/bin/checks/](../utils/bin/checks/) | Ordered local check scripts and rendered-site validators. Some checks intentionally edit source; consult the catalog. |
| [utils/lib/](../utils/lib/) | Shared support for environment selection, regression test execution, browser runs, and artifact handling. |
| [utils/tests/](../utils/tests/) | Ruby and Python automated regressions plus local-only browser tests. |
| [utils/bin/diagnostics/](../utils/bin/diagnostics/) | Manual service, email, watcher, and network diagnostics; not the automated test suite. |
| [.github/workflows/jekyll.yml](../.github/workflows/jekyll.yml) | GitHub Actions production build, search-index generation, local rendered checks, artifact report, and Pages artifact deployment. |

## Build and deployment model

All maintained tools live under utils/. The former root scripts directory and compatibility aliases have been removed, and repository instructions refer directly to the canonical tool paths.

Local source changes are reviewed and validated in the working tree. The Actions workflow builds Jekyll in production mode, generates Pagefind search data, runs the rendered-site test suite against the build output, and reports browser artifact retention. It uploads the completed site as a Pages artifact and deploys that artifact with the Pages deployment action; publication is not driven by a gh-pages source branch. See [deployment](guides/deployment.md) and [GitHub Actions](guides/github-actions.md).

The local utils/bin/check-site command provides targeted workflows: checks invokes the ordered local check suite, test runs deterministic Ruby/Python tests, test --site PATH adds rendered-site checks to an existing build, and local/remote/all crawl a site. These commands do not deploy. utils/bin/jekyll-site owns local build/serve conveniences. A LAN preview requires explicit binding and exposes drafts without authentication; use only on a trusted network.

## Environment and dependency handling

Local Git clients can inherit the wrong Python or Ruby if started outside the expected shell. The shared environment helper selects the existing project RVM gemset and Conda python-website-dev environment when available, otherwise honoring the caller environment. It does not modify shell defaults or install packages. The environment check validates the frozen Ruby bundle and Python requirement versions without attempting pip install; resolve a mismatch in the intended environment rather than mutating system/uv Python. See [environment setup](guides/environment-setup.md) and [troubleshooting](guides/troubleshooting.md).

## Content and product operations

- Blog list order uses publication dates, not editorial update timestamps. Release notices can be driven by explicit product release metadata; historical article URLs and publication dates remain intact. See [post updates and ordering](workflows/post-updates-and-ordering.md).
- Short-link redirects use canonical mappings and preserve destination behavior; their source tooling is cataloged at [utils/bin/backfill_short_url_front_matter.rb](../utils/bin/backfill_short_url_front_matter.rb).
- Project help routes ordinary product reports toward the relevant public GitHub issue tracker, with private contact retained for sensitive matters. Issue-form examples are reusable source material and may need to be copied into each product repository.
- The LogGPT project includes an illustrated iPhone/iPad user guide as product documentation, not a blog entry.
- Current product release status is defined by each product's public page and its source repository; this overview is not a release qualification record.

## Validation and cleanup boundaries

Automated regressions are separate from manual diagnostics. check-site test discovers only the canonical Ruby/Python test suites; browser tests are local-only and block external requests and production URLs. Do not substitute email/network/service probes for automated and rendered-site checks.

The browser artifact utility only considers old files inside output/playwright/ and .playwright-cli/. The default is a report; deletion requires an exclusive manifest and explicit --apply. Tracked files, symlinks, active/pinned runs, and path escapes are protected. CI reports but does not delete artifacts. Published images, diagrams, narration, logs, utils/etc/, and arbitrary output/ data are outside this cleanup workflow. See [utilities catalog](../utils/README.md#artifact-retention).

## Documentation map

- [Documentation index](README.md)
- [Site operations hub](guides/site-operations.md)
- [Deployment](guides/deployment.md)
- [Testing](guides/testing.md) and [pre-commit checks](tools/pre-commit-checks.md)
- [Utilities catalog](../utils/README.md)
- [Maintenance](guides/maintenance.md)
- [Change history](../CHANGELOG.md)

**Last updated:** 2026-11-27

