# Site maintenance

Keep routine maintenance small and evidence-driven. The [utilities catalog](../../utils/README.md) is the source for current commands, inputs, and side effects.

## Routine review

- Run the deterministic suite with utils/bin/check-site test before committing.
- For site-content or layout changes, build a local review version and run utils/bin/check-site test --site PATH against the existing build.
- Review GitHub Actions after push; the workflow builds, indexes search, validates, and deploys a Pages artifact.
- Check release metadata and product notices when a product publishes a new public version. Preserve article publication dates and historical permalinks.
- Review monitoring state and configuration only when maintaining the local monitoring service.

Do not schedule indiscriminate dependency upgrades. Dependabot or an identified compatibility/security issue may motivate a targeted update; review the exact lockfile change and run the relevant checks.

## Browser artifacts

Browser screenshots and logs can be useful review evidence. They are not automatically disposable. The artifact command scans only output/playwright/ and .playwright-cli/, and lists files older than 30 days by default:

    utils/bin/check-site artifacts

It is report-only by default. To stage deletion candidates for review, create an exclusive manifest:

    utils/bin/check-site artifacts --manifest /path/to/review-manifest.json

Inspect the manifest before explicitly applying it:

    utils/bin/check-site artifacts --apply /path/to/review-manifest.json

Apply permanently deletes the manifest's listed files after validating the complete selection. Tracked content, symlinks, path escapes, active or pinned runs, and run metadata are protected. Place .active in a browser run while work is in progress and .keep in evidence that should be retained. Failed browser audits are pinned automatically.

The CI workflow reports artifact counts but does not delete files. Cleanup is not a general CI task and does not include published graphics, audio/narration, utils/etc/, logs, or unrelated output files. Preserve artifacts needed for ongoing review or investigation.

## Local logs and monitoring

Monitoring tools may send email, crawl the network, or interact with local services. These actions are manual/operational and separate from automated tests. Check current monitoring configuration and service state before starting or stopping services; do not assume an old schedule or stale checklist is still active.

## Dependencies

Keep Ruby and Python dependencies aligned with their committed manifests. Environment checks are read-only; use the intended RVM/Conda environment and perform any deliberate dependency change as its own reviewed update. Avoid blanket cache deletion or recurring bundle update commands.

See [testing](testing.md), [deployment](deployment.md), [environment setup](environment-setup.md), and [pre-commit checks](../tools/pre-commit-checks.md).

