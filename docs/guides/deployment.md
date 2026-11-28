# Build and deployment

Treat local preview, CI validation, and public deployment as separate stages. A local build or passing check does not publish the site. The source workflow is [.github/workflows/jekyll.yml](../../.github/workflows/jekyll.yml).

## Local review

Start the site's configured local service with utils/bin/site-service or use the Jekyll wrapper:

    utils/bin/jekyll-site build
    utils/bin/jekyll-site serve

For draft-inclusive preview on a trusted LAN, pass the explicit bind address/hostname supported by the wrapper. LAN mode has no authentication and exposes local draft content; keep it on a private trusted network. The default remains local-only. Do not point a browser audit at the public site.

To build into a separate destination and run rendered checks without overwriting a shared preview:

    JEKYLL_ENV=production bundle exec jekyll build --destination /tmp/unixwzrd-site-review
    utils/bin/check-site test --site /tmp/unixwzrd-site-review

The site test command requires an existing rendered index.html. It does not build, install dependencies, start services, or deploy.

## GitHub Pages deployment

The workflow runs on pushes to main and can be manually dispatched. It checks out the repository, installs the locked Ruby bundle and Python requirements in GitHub-hosted runners, removes only the workflow runner's generated _site and Jekyll cache, builds with production settings, generates and verifies the Pagefind index, then runs rendered tests and offline link validation. It reports browser artifact retention without deleting local or repository data, uploads _site with the Pages artifact action, and deploys that artifact with the Pages deployment action.

Deployment is artifact-based; it is not configured as a branch publishing workflow from gh-pages. The production build/search checks and local developer checks are related but not identical. In particular, search-index generation is a distinct CI step and external-link checking is not part of the rendered offline suite.

## Before a reviewed push

1. Inspect the complete working-tree diff.
2. Run the repository pre-commit/site checks in the intended local Conda/RVM environment.
3. Build and inspect the changed pages locally, including responsive layouts when presentation changed.
4. Run the appropriate rendered checks; use a separate destination if another preview shares _site.
5. Push only after local review. GitHub Actions performs the actual Pages deployment.

## Rollback and diagnosis

If Actions fails, use the failing workflow step and [troubleshooting](troubleshooting.md) to classify the failure before changing content or dependencies. A successful build does not prove the deployment completed; verify the Actions deployment result and then inspect the public URL. Restore content or workflow changes through a reviewed Git change rather than editing generated output.

See [GitHub Actions](github-actions.md), [testing](testing.md), and [pre-commit checks](../tools/pre-commit-checks.md).

