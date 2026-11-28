# Testing and validation

Use the repository's supported entry points rather than running old one-off checks by memory. The complete canonical file catalog and side-effect notes are in [utils/README.md](../../utils/README.md).

## Fast deterministic regressions

From the repository root:

    utils/bin/check-site test

This discovers the canonical Ruby and Python suites under utils/tests/. These tests are intended to be deterministic and offline. It does not build the Jekyll site, send email, crawl public sites, start/stop services, or run browser automation.

For a rendered-site regression run, point at an already built site:

    utils/bin/check-site test --site _site

The rendered mode runs the source tests plus permalink, taxonomy, project/short-link redirect, short-link front-matter, and offline HTMLProofer checks against that build. It does not itself build the site or run browser tests. For a clean validation build that will not overwrite the shared preview:

    review_dir=$(mktemp -d /tmp/dts-site-review.XXXXXX)
    JEKYLL_ENV=production bundle exec jekyll build --destination "$review_dir/site" --disable-disk-cache
    python -m pagefind --site "$review_dir/site" --output-subdir pagefind --root-selector '[data-pagefind-body]' --exclude-selectors '[data-pagefind-ignore]' --force-language en
    utils/bin/check-site test --site "$review_dir/site"

Use a task-owned temporary directory for longer review workflows and remove only that directory after confirming no process is using it.

## Local ordered checks

    utils/bin/check-site checks --list
    utils/bin/check-site checks
    utils/bin/check-site checks --run 02_permalinks,07_jekyll_build

The local check suite is broader than the deterministic test suite. Some checks may update metadata or source files; inspect the script and review git diff afterward. Network-dependent external-link checking is optional. The Jekyll doctor check may report case-only URL differences on case-insensitive macOS volumes; read its diagnostic rather than assuming a build failure.

The project Git hook invokes the local check workflow. Keep it enabled; do not work around a failing check by bypassing the hook. If a GUI client starts with the wrong environment, restart it from the intended Conda/RVM context or use a terminal with that context. The environment helper selects existing environments and validates packages; it never installs dependencies.

## Browser regressions

Browser coverage is separate from the offline suites and requires a running local site plus the supported Playwright CLI. Use:

    utils/bin/check-browser reader-experience --url http://localhost:4000/

Other suite names are local-reader, secrets-kit-product, and short-link-attribution; the attribution suite needs a local URL ending in the generated redirects data path. The runner owns and closes its browser session, blocks outbound requests, rejects production targets, and records screenshots in a timestamped browser output directory. Failed runs are pinned for later review. Do not run against production or use production analytics as test traffic.

### Known browser-audit findings from November 27, 2026

The production build, search indexing, and deterministic/rendered regressions passed during the tooling migration. The unchanged `reader-experience` browser function still reported a mobile Projects-dropdown failure after its desktop/scroll/resize sequence; a fresh mobile-page toggle worked. The existing `local-reader` mocked-audio audit also timed out waiting for its simulated playback to finish. These remain separate browser-harness/navigation/playback investigations, not waived assertions or evidence that all browser audits passed. Failed receipts are pinned under ignored browser output. No navigation or playback implementation was changed as part of the tooling migration.

The active shared preview was missing its Pagefind bundle during the audit. Search checks used an isolated production build with a freshly generated index instead; the running Jekyll service was not restarted or modified. If local search is unavailable, verify that the served build includes its Pagefind output before diagnosing the search UI.

## Manual diagnostics are not tests

utils/bin/diagnostics/ contains probes for external links, email, services, and file watchers. They can contact network endpoints, send messages, or interact with running processes. Run them only when that side effect is the purpose of the investigation. They are not discovered by check-site test.

## CI coverage

GitHub Actions runs a production build, creates the Pagefind search index, then runs utils/bin/check-site test --site "$GITHUB_WORKSPACE/_site" against that build and reports old browser-artifact candidates. Search-index creation remains a separate workflow step and is not replaced by the local test runner. The workflow does not run public-site crawls, external-link checks, or artifact deletion.

## Where to look when a check fails

- Environment/package selection: [environment setup](environment-setup.md) and [pre-commit checks](../tools/pre-commit-checks.md).
- Permalinks, redirects, and page links: [utilities catalog](../../utils/README.md#automated-checks-binchecks).
- Build or deploy: [troubleshooting](troubleshooting.md) and [deployment](deployment.md).
- Tool list and safety boundaries: [utils/README.md](../../utils/README.md).

