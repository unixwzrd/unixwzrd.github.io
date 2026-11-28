# Troubleshooting

Start with the exact failing command and its first meaningful error. The current tool paths and side effects are listed in [utils/README.md](../../utils/README.md).

## Pre-commit: missing Python package or externally managed environment

The hook should validate the existing environment and must not install packages. Activate the project Conda environment and project RVM gemset, then rerun the targeted check:

    conda activate python-website-dev
    rvm use ext-ruby-3.3.4@unixwzrd.github.io
    utils/bin/check-site test

If a GUI client has stale PATH state after reboot or automatic startup, close it and relaunch it from the prepared shell. Do not use uv/system Python for this project, do not pass --break-system-packages, and do not bypass the hook as a routine fix.

## Bundler cannot find a locked gem

First verify which Ruby/Bundler are active and run bundle check. A missing gem is an environment setup problem, not a reason to modify Gemfile.lock. Install the exact locked bundle in the intended RVM environment using the established project workflow, then rerun the failing test. Do not run bundle update without a specific dependency change being reviewed.

## Permission denied for a check script

Inspect the path and file mode before changing anything:

    ls -l utils/bin/check_site.sh utils/bin/pre-commit
    git ls-files --stage utils/bin/check_site.sh

The portable hook wrapper is intended to invoke the script through Bash, so the check does not depend on an executable bit being preserved by an unrelated editor. If a tracked executable script lost its mode, restore the expected executable bit as a scoped Git change and inspect the resulting mode diff. Do not chmod broad directories.

## Local build fails

Use the failing Jekyll/Liquid output to identify the source file. Check front matter, include paths, and template syntax. Build to a separate destination if a shared local preview is running:

    JEKYLL_ENV=production bundle exec jekyll build --destination /tmp/unixwzrd-site-review --trace

Do not delete the shared _site or Jekyll caches as a first response. Preserve logs and generated artifacts needed to diagnose the failure.

## Rendered checks fail

Confirm that --site points to the build you intended and that index.html exists. Run the specific permalink, taxonomy, redirect, or HTMLProofer command listed in the utility catalog. Internal hash failures often identify stale anchors; don't fix the test fixture by weakening assertions unless the rendered behavior itself changed intentionally.

External link checks are network-dependent and may be affected by remote rate limits or outages. Distinguish a remote request failure from a broken local page.

## Search index or Pages deployment fails

Inspect the first failed workflow step. Search-index generation is a separate step after the production Jekyll build, and Pages deployment consumes the uploaded artifact. A failed index assertion, rendered link check, artifact upload, and deploy action have different causes. Do not diagnose this as a gh-pages branch problem.

## LAN preview is unreachable

The default local server binds to loopback. LAN access requires an explicit private-network bind option and a trusted network; the preview is unauthenticated and can include drafts. Confirm the chosen local address and firewall rules before exposing it to another host. Do not bind to public interfaces or add router/firewall holes.

## Artifact cleanup question

Ignored or untracked does not mean disposable. The report scans only designated browser artifact directories and deletes nothing. Review each candidate manifest and use explicit apply only for files you recognize and no longer need. Keep active or failed evidence pinned. Never remove all of output/ or use a broad cleanup command as a diagnostic.

Related guides: [testing](testing.md), [environment setup](environment-setup.md), [deployment](deployment.md), [pre-commit checks](../tools/pre-commit-checks.md).

