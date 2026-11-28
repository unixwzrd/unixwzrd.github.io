# Local development environment

Use the project's existing Ruby and Conda environments. Do not let a GUI Git client silently fall back to a system Python, uv-managed interpreter, or unrelated Ruby installation.

## Expected local environments

- RVM: project gemset ext-ruby-3.3.4@unixwzrd.github.io.
- Conda: python-website-dev.
- Bundler: dependencies pinned by Gemfile.lock.
- Python: package versions declared by requirements.txt.

The shared helper at utils/lib/site-environment.sh selects the existing project RVM gemset and Conda environment for local Git clients when available. If not available, it preserves the caller's environment. It does not change RVM defaults, activate global shell state, create environments, or install packages.

## GUI Git clients

When Cursor or another GUI client was launched during startup before the intended shell environment was ready, its Git hook may inherit the wrong PATH. Close and relaunch the client from a terminal where the expected Conda and RVM environments are active, or perform the commit from that terminal. The hook's read-only environment check prints the selected executables and fails if required dependencies are absent.

    conda activate python-website-dev
    rvm use ext-ruby-3.3.4@unixwzrd.github.io
    utils/bin/check-site test

Do not use pip against an externally managed system/uv Python, do not use --break-system-packages, and do not allow the hook to install requirements. Repair the intended environment explicitly using its normal project workflow.

## Validate installation

    ruby --version
    python --version
    bundle check
    python -m pip check
    utils/bin/check-site test

The full environment check also validates installed requirement versions. When bundle check reports a missing locked gem, install the lockfile-defined bundle in the intended RVM environment with bundle install. Do not run bundle update as generic maintenance; dependency updates should be deliberate, reviewed, and reflected in the lockfile.

## CI environment

GitHub Actions provisions its own Ruby and Python versions, installs the repository's declared dependencies in its runner, and builds/deploys from that isolated environment. Local environment-selection behavior is for developer machines and does not change CI.

See [pre-commit checks](../tools/pre-commit-checks.md), [testing](testing.md), and the [utility catalog](../../utils/README.md).

