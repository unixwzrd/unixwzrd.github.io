# Documentation index

Start here for site publishing, operations, validation, and tool references. The canonical executable catalog is [`utils/README.md`](../utils/README.md); it lists tools by their current paths and explains side effects.

## Common tasks

| Task | Guide |
| --- | --- |
| Understand the repository and current operating model | [Project overview](PROJECT_OVERVIEW.md) |
| Run the local checks and regression suites | [Testing](guides/testing.md), [pre-commit checks](tools/pre-commit-checks.md) |
| Build and deploy the public site | [Deployment](guides/deployment.md), [GitHub Actions](guides/github-actions.md) |
| Set up local Ruby and Python environments | [Environment setup](guides/environment-setup.md) |
| Start or inspect local services | [Service management](guides/service-management.md) |
| Investigate a build, check, or deployment failure | [Troubleshooting](guides/troubleshooting.md) |
| Review maintenance and retained browser artifacts | [Maintenance](guides/maintenance.md), [`utils/README.md`](../utils/README.md#artifact-retention) |
| Operate monitoring | [Monitoring](guides/monitoring.md) |
| Use the current utilities | [Utilities catalog](../utils/README.md), [utilities reference](guides/reference-utilities.md) |

## Publishing and site behavior

- [Blog publishing workflow](workflows/blog-publishing.md)
- [Post updates, publication dates, and list ordering](workflows/post-updates-and-ordering.md)
- [Blog templates, slugs, and short links](templates/blog-templates.md)
- [Analytics attribution](guides/analytics-attribution.md)
- [Blog pagination](guides/blog-pagination.md)

## Other project documentation

- [Site operations hub](guides/site-operations.md)
- [Security](guides/security.md)
- [Operational checklist](guides/checklist.md) - review before treating dated checklist entries as current work.
- [Strategy](guides/strategy.md)
- [Historical July 2025 operations snapshot](guides/site-operations-archive-2025-07-09.md)
- [Change history](../CHANGELOG.md)
- [Root README](../README.md)

## Operating rules

- Keep site source, local preview, CI validation, and public deployment distinct. A successful local build does not publish anything.
- Use the existing Conda and RVM environments. Checks report missing dependencies; they do not install packages or change global defaults.
- Treat manual diagnostics as side-effecting unless proven otherwise. They are separate from the offline regression suite.
- Artifact cleanup is a local review workflow only. CI reports aged browser artifacts but does not delete them; published assets, audio, logs, and configuration are not cleanup targets.
- Keep changes uncommitted until reviewed when a task requests local review. Do not bypass pre-commit as a routine response to a failing check.

**Updated:** 2026-11-27

