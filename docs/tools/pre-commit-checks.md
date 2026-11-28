# Local checks and pre-commit

The installed repository hook invokes the portable repository wrapper at utils/bin/pre-commit. The wrapper selects the existing local project environments where available and invokes utils/bin/check-site checks while explicitly skipping 05_update_project_data.sh, which makes network requests and stages generated files. The check-site CLI delegates the local suite to utils/bin/check_site.sh.

The installed .git/hooks/pre-commit file is local Git configuration and is not replaced by the repository documentation or by the wrapper. Keep the hook enabled. If a check fails, diagnose and fix the underlying environment or test failure instead of bypassing the hook.

## Environment selection

For GUI Git clients, the shared environment helper can select the existing ext-ruby-3.3.4@unixwzrd.github.io RVM gemset and python-website-dev Conda environment when those environments are available. Otherwise the caller's environment is used. The helper does not change shell defaults or install dependencies.

The environment check verifies Bundler's locked dependencies and Python package versions from requirements.txt. It never runs pip install. If packages are missing, activate the intended environment and install only through the project's established dependency workflow; do not modify a uv-managed or system Python and do not use --break-system-packages. On this checkout, addressable 2.9.1 is already installed in the bundle at the locked version; do not run bundle update merely to satisfy the hook.

Environment-selection regression coverage:

    bundle exec ruby utils/tests/ruby/test_check_site_environment.rb

## Running checks

    utils/bin/check-site checks --list
    utils/bin/check-site checks
    utils/bin/check-site checks --run 01_environment,02_permalinks

The ordered checks include environment validation, permalink/source checks, Jekyll doctor, link checks, build checks, image/navigation/front-matter checks, and other repository validations. Some individual checks can modify source data or metadata; inspect the corresponding script and review git diff after running a mutating check. The full manual run includes 05_update_project_data.sh, which fetches project data and stages matching generated files. It also includes 05_site_link_checker.sh, which rebuilds the shared _site directory before HTMLProofer; avoid that check while another process depends on the shared preview. Use an isolated build followed by check-site test --site PATH for non-disruptive rendered validation.

The pre-commit environment check is read-only with respect to package installation. External link validation is network-dependent and optional. Jekyll doctor can report case-only URL collisions on case-insensitive macOS filesystems; inspect the message and distinguish that warning from an actual build or link-test failure.

## Regression suite and rendered site

Run deterministic source regressions:

    utils/bin/check-site test

Run the same suite plus checks against an existing rendered output:

    utils/bin/check-site test --site _site

The latter expects an existing index.html and does not build or overwrite it. It adds permalink, taxonomy, redirect, short-link front-matter, and offline HTMLProofer checks.

## Optional staged-content hook

The separate .pre-commit-config.yaml hook can check/backfill short-link metadata for staged site content. It is not the installed shell hook and is not required to run the full site checks. See [blog templates](../templates/blog-templates.md) for read-only --check and scoped backfill behavior.

## If the hook fails

1. Keep the complete failure output and identify the failing check.
2. Confirm the GUI client inherited the expected Conda and RVM context, or reproduce from a terminal started in that context.
3. Verify the locked bundle and Python requirements without installing packages through the hook.
4. Run the narrow failing test/check, fix the root cause, then run the required full hook/check again.
5. Review the working-tree diff, especially after checks that may update files.

The canonical file list and each check's effects are in [utils/README.md](../../utils/README.md).

