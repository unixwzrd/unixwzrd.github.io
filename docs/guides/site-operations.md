# Site Operations Guide

This guide is the central resource for running, maintaining, and troubleshooting the Distributed Thinking Systems website. It is intended for developers, maintainers, and anyone involved in site operations.

Below you'll find an overview of each major area of site operations, with links to detailed guides for each topic.

## Sections

- **[Environment Setup](environment-setup.md)**
   How to configure your local and production environments, including Ruby, Python, Node.js, and all project dependencies.

- **[Service Management](service-management.md)**
   Scripts and workflows for starting, stopping, and monitoring Jekyll and related services.

- **[Deployment](deployment.md)**
   Deploy and build (GitHub Actions, local production build, GitHub Pages branches).

- **[Blog Listing & Pagination](blog-pagination.md)**
   How blog listings and pagination work, including configuration, customization, and client-side navigation.

- **[Troubleshooting](troubleshooting.md)**
   Common issues, error messages, and their solutions for both development and production environments.

- **[Maintenance](maintenance.md)**
   Regular tasks, performance optimization, and keeping the site healthy and up-to-date.

- **[Security](security.md)**
   Access control, internal documentation, and best practices for keeping the site and data secure.

- **[Reference & Utilities](reference-utilities.md)**
   Essential reference material, quick commands, and utility documentation.

- **[Monitoring](monitoring.md)**
   Site reliability monitoring system, health checks, and automated alerting.

- **[GitHub Actions](github-actions.md)**
   Setup and configuration for GitHub Actions workflows and CI/CD.

- **[Strategy](strategy.md)**
   Monitoring strategy, check frequency guidelines, and optimization recommendations.

- **[Testing](testing.md)**
   Testing procedures, validation methods, and quality assurance processes.

- **[Checklist](checklist.md)**
   Comprehensive checklist for site improvements, maintenance tasks, and project tracking.

- **[Blog templates & short links](../templates/blog-templates.md)**
   Post structure, optional `slug` for project URLs, `/s/<code>/` short links (hash uses the post **path under `html/`**, not the live permalink), backfill script, and optional pre-commit hook (repo root [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml)).

- **[Post updates & list ordering](../workflows/post-updates-and-ordering.md)**
   Major updates, technical corrections, series `series_order`, and discovery-list promotion without changing permalinks or short links.

Each section contains detailed instructions and is maintained in smaller files for easier updates.

