# Project issue forms and support routing

Product bug reports and feature requests belong in the product's own GitHub repository. Private inquiries, billing questions, security concerns, and help for people without a GitHub account remain available through the website's private contact form. No inquiry is automatically posted publicly.

## Website routing

`html/_data/project_help.yml` enables the maintained public products and supplies their optional guide links. Repository URLs and display names come from `html/_data/github_projects.yml`; do not maintain a second list of repository URLs. Before adding a product, verify that its public repository has Issues enabled. Private, hidden, and unconfigured projects are excluded.

The shared `project_help.html` include provides product-specific help in page footers. Ordinary project pages and posts use their existing `category`; ancillary pages use `support_project`. A `prominent_guide` setting places the guide callout below the project title, before the artwork. Secrets Kit retains its existing product-specific support component.

The Contact page lists all supported products without JavaScript. Its selector progressively filters those existing links; it never creates a URL from visitor input, submits a form, collects inquiry content, or opens an issue automatically.

## Template review and publication

The website repository contains the shared [bug report form](../../../.github/ISSUE_TEMPLATE/bug_report.yml), [feature request form](../../../.github/ISSUE_TEMPLATE/feature_request.yml), and [issue chooser configuration](../../../.github/ISSUE_TEMPLATE/config.yml). Forms ask for the version, environment, reproduction steps, expected and actual behavior, and optional sanitized diagnostics. Feature requests describe the problem, desired result, and alternatives. Neither form requests an email address or a complete diagnostic archive. No labels or assignees are applied automatically.

Copies are staged, uncommitted, in the existing LogGPT, UnicodeFix, Extract Chat, WebReader, and Secrets Kit checkouts. Each copy's issue chooser links to that product's guide or overview and to private contact. No runtime or release files were changed.

LogGPT now has specialized bug, feature, and support-question forms. The bug form separately requests the app version/build, device model, operating-system version, optional Safari version, Basic/Plus edition, and conversation type. Its chooser disables blank issues to make the structured forms the normal route. Run `ruby scripts/check-issue-forms.rb` in the LogGPT repository to validate those forms. Do not overwrite them with the generic copies here. Ordinary support belongs in GitHub; email is a fallback for people unable to access GitHub and remains available for private billing, account, or security matters.

This directory also contains the reusable review packages for the remaining supported public projects. Copies are staged in their public working checkouts:

- `LLM-Ops-Kit/.github/ISSUE_TEMPLATE/`: bug report, feature request, and chooser configuration.
- `localops-ui-kit/.github/ISSUE_TEMPLATE/`: bug report, feature request, and chooser configuration in the public toolkit checkout.
- `code-analytics/.github/ISSUE_TEMPLATE/`: feature request and chooser configuration alongside the existing bug report form in the public Code Analysis checkout.

Review each destination's current templates before copying or merging these files. Forms become available only after they reach that repository's default branch. Publish the repository templates before, or alongside, the website routing. Until then, the website's `/issues/new/choose` links still use GitHub's existing issue-creation flow rather than depending on unpublished template filenames. Nothing has been committed, pushed, deployed, or filed as an issue by this work.

GitHub documents [issue form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms). The generic forms retain blank issues as an escape hatch; LogGPT uses its specialized structured-support chooser instead. Retain private contact for sensitive matters.

## Owner-wide defaults

GitHub also supports [default community files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) in a public repository named `.github` under the owner account. That is an optional future way to maintain common forms centrally; no such repository was created or changed here. A repository with its own valid issue forms or chooser configuration does not inherit that default issue-template folder, so adopting owner-wide defaults requires an explicit migration of existing per-project forms. Preserve project-specific forms such as Code Analysis's bug report.

## Validation

The website's `utils/tests/ruby/test_reader_experience.rb` checks the shared forms and these review packages as YAML, validates required form fields and unique IDs, and checks project filtering, private fallbacks, prominent guide placement, and rendered repository links. Use the normal local Jekyll build and internal-link checks before publication. GitHub's live issue chooser can only be accepted after the templates have been pushed; local validation is not a claim that the forms are already active on GitHub.


