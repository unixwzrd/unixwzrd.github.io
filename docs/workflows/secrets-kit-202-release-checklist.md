# Secrets Kit 2.0.2: release-day checklist

This is preparation, not authorization to release. Keep `production_release_ready: false` while development and qualification continue. Do not merge, tag, push, deploy, announce, open Checkout or activate live billing as part of the website review. The site target is `v2.0.2`; it is not proof of an approved production artifact. No release date has been promised.

## Evidence boundary

This review used the development workspace, not GitHub main or historical releases. The client install guide and RSS customer guide still identify some material as beta, and the checkout contains uncommitted development work. Source behavior is not installed-release qualification. Bind final approval to the actual production artifact and exact documentation revision.

The macOS declaration follows the governance customer targets. Linux compatibility is described by architecture and GNU libc rather than by an exclusive distribution list. The October 28 working installer and dependency manifest contain an ARM64 binary path that is newer than the master installation/native-dependency documents, which still describe ARM as internal-only. Reconcile that documented policy and the packaged wheel provenance before final customer signoff; the private governance research note `LINUX_COMPATIBILITY_RESEARCH_2026-10-28.md` records the discrepancy, upstream baselines and dependency-resolution results. Distribution-specific qualification hosts remain evidence, not a distribution restriction. No master architecture or product source was changed for this website work.

Confirmed source references for the site copy:

- Client `LICENSE`, `pyproject.toml` license metadata: MIT. The Hermes skill's own metadata is separate.
- Client `docs/INSTALL.md`, prerequisites and installation sections: Bash/utilities/downloader/network bootstrap, managed Python 3.12, intended OS/architecture targets, per-user manual installation, and Linux service considerations. Read its architecture limits alongside the governance public-target matrix; its beta labeling does not make implemented platform support a planned feature.
- Client `integrations/hermes/install-secrets-kit-for-hermes/README.md`: separate install/configuration/verification decisions, explicit credential choices, preserved existing configuration and optional model-visible retrieval.
- Client `docs/SECURITY_MODEL.md` and `docs/REMOTE_SECRET_SYNC_ADR.md`: local keys, destination-encrypted payloads, non-authoritative forwarding and ordered relay failover.
- Client `docs/CLI_REFERENCE.md`, non-SSH peer invitations, and `protocol/peer_invitation_mailbox.py`: short-lived encrypted onboarding-message exchange; expiry is separate from a provider-wide deletion commitment.
- Client `docs/RSS_CUSTOMER_GUIDE.md`, device and lifecycle sections: existing-subscription quantity increase, payment verification, slot enforcement, revocation distinct from purchased quantity, inactive-entitlement suspension and forwarding termination. It does not settle cancellation effective dates or refund eligibility.

## Decisions required before availability

- [ ] Verify the Linux kernel/libc/CPU baseline and service prerequisites against final-artifact receipts on x86_64 and ARM64, including clean installs and upgrades without a native compiler. Resolve the stale ARM-only-internal/native-wheel policy text through the authoritative master documents and synchronize approved derivatives. Do not derive a certified kernel minimum solely from a wheel tag or Rust target. Only after artifact signoff set `compatibility.approved_for_202: true` in `html/_data/secrets_kit.yml`.
- [ ] Approve an RSS metadata inventory covering account/payment and authorization records, network/connection information, operational logs and metrics, support submissions, and encrypted invitation messages. Reconcile the summary with the actual production configuration.
- [ ] Approve retention/deletion rules for those records and backups, including the difference between invitation expiry, primary-store cleanup, backup erasure, account archival and deletion requests. Do not promise erasure from a timer or equate cancellation with deletion.
- [ ] Approve the complete production provider list and processing locations for payments, hosting/networking, support/email and monitoring. Stripe and GitHub appear in the documented workflow; that is not a complete provider disclosure.
- [ ] Decide whether cancellation is immediate or period-end, and confirm payment-failure handling. Implementation support for either timing does not choose the customer policy.
- [ ] Decide refund eligibility, deadlines and credit/proration behavior for cancellation and quantity changes, including reductions below currently enrolled quantity. Preserve the two-connection offer minimum and the separation between revocation and purchased quantity.
- [ ] Confirm support coverage and channels. Do not add a response-time, uptime or recovery-time promise without approval.
- [ ] Replace the prelaunch/undecided sections in the scoped policy page with approved terms and an approved effective date. Preserve the existing Safari-extension policies. Then set `service_policies_approved: true`.

## Prepared release-day change — do not execute yet

- [ ] Verify the immutable `v2.0.2` release and its `install.sh`, install documentation, complete Hermes integration, security model, RSS customer/device guide anchors and client license. Verify installation on each approved platform. Do not substitute GitHub main, old stable or a beta download.
- [ ] Choose the actual release-announcement post or discussion destination and put it in `release_announcement_url`. A draft announcement or planned URL is not evidence of publication; announcement publication is a separate action.
- [ ] Confirm the advertised hosted service and its billing environment are approved and available. Verify checkout, billing portal, entitlement/capacity enforcement and cancellation separately from the client install. Do not activate billing from website tooling.
- [ ] In one reviewed website change, set `production_release_ready: true` only after the above gates. This removes the coming-soon notice and homepage teaser, enables the primary Get Started action, exposes versioned documentation/installer/license links, enables the concise agent handoff and copy control, and shows the installed-client subscription instructions. Release updates then use the chosen announcement URL.
- [ ] Update the remaining prelaunch prose and catalog availability text in `html/projects/Secrets-Kit.md`, `html/_data/repos.yml` and generated catalog, the policy page, and any editorial homepage copy. Keep historical 1.x posts intact and labeled as history. The shared flag cannot approve unresolved policy prose by itself.
- [ ] Refresh comparison prices only if the review date/offer needs it; retain the tables, directory, qualifications and sources. Product behavior still comes from the approved 2.0.2 workspace/artifact, not competitors or historical posts.
- [ ] Validate production and preview into isolated destinations. Run focused product and reader-experience checks, internal links and anchors, permalink/redirect checks, and a search build. Inspect desktop/narrow-screen layouts, light/dark contrast, keyboard navigation/table scrolling, every directory expansion/filter and empty results, and the ready-state installation handoff.
- [ ] Review the diff and obtain any required release/publishing approval. Commit, push, deployment, product promotion, public announcement and billing activation remain distinct actions.

## Link classification during staging

- The landing page links to `/projects/Secrets-Kit/credential-risks/` for the full research. Security leads with product answers and preserves its old research anchors as onward links. Keep that separation and those links when activating the release.
- Product navigation is Overview, Compare, Pricing, Guides, Security, GitHub and More, with a separate Get Started/Explore action. GitHub source precedes More, which contains Help, Remote Sync and Updates; Help and Policies remain in the footer. Verify the mobile "Secrets Kit pages" disclosure and the native no-JavaScript fallback when reviewing release-day changes.
- **Available:** product navigation, product-policy anchors, comparison section jumps, historical posts, GitHub Issues/Discussions and private contact. These must resolve normally.
- **Intentionally unavailable:** 2.0.2 installers, versioned repository documentation, Hermes setup and the versioned repository license. They render as labeled forthcoming text or are withheld. They must not masquerade as links to the release-status notice.
- **Broken:** any available link or anchor that fails. An intentionally unavailable future destination does not excuse a broken product-navigation link.
