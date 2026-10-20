---
layout: project
title: "LocalOps UI Kit"
category: localops-ui-kit
permalink: /projects/localops-ui-kit/
short_link: true
short_link_basis: "/projects/localops-ui-kit.md"
short_url: "https://unixwzrd.ai/s/8ab660876d/"
image: /assets/images/projects/localops-ui-kit/localops-ui-kit-banner.png
excerpt: "Python-first operator interfaces with native browser components and Textual/Rich renderers, without a Node or frontend build pipeline."
project_intro: |
  LocalOps UI Kit provides reusable interfaces for local-first operational applications. Strict Python models define shared UI meaning; native browser components and optional Textual/Rich renderers present it without taking over the application's backend, authorization, or domain logic.

  [Try the widget showcase](https://unixwzrd.ai/localops-ui-kit/) or start with the [installation instructions](https://github.com/unixwzrd/localops-ui-kit#install-from-github). Version 0.2.0 is a pre-1.0 preview, with renderer capabilities and limitations documented explicitly.
---

## Operator Interfaces Without a Frontend Build Pipeline

Operational tools need more than a collection of attractive controls. They need clear task state, usable tables, predictable navigation, readable results, and interaction that remains understandable when something fails. **LocalOps UI Kit** supplies those presentation primitives while leaving application behavior with the application.

The browser implementation uses standards-based JavaScript ES modules and CSS. A Python application can serve those files unchanged, and the Python wheel includes the same assets. There is no Node runtime, npm installation, transpiler, bundler, or frontend framework required by the toolkit. The browser-only showcase can also run on a static host without a Python service.

## Why Another UI Kit?

LocalOps UI Kit addresses a specific recurring need: local operational applications that need task progress, inspectable data, logs, results, and predictable controls across more than one project. It combines Python-owned semantic contracts, directly served browser assets, and optional terminal renderers without making the presentation layer responsible for application policy. It is not intended to replace general-purpose web frameworks or provide every kind of application interface.

The goal is to share interface mechanics while keeping each application's operations and authority separate. Components and contracts will continue to evolve as they are exercised in different projects; compatibility information and the capability matrix document the integration boundary and its current limits.

## One Semantic Foundation, Different Presentations

Strict Pydantic models provide the shared UI specifications and state contracts. The WebUI, Textual TUI, and Rich CLI renderers use that foundation rather than inventing separate meanings for the same task or control. Revisioned snapshots and patches reject stale updates instead of silently replacing newer state.

The renderers do not promise identical capabilities. A browser table can offer interactions that a static terminal table cannot, and direct browser components such as the results reader, draft editor, and content panel do not have dedicated terminal equivalents. The [capability matrix](https://github.com/unixwzrd/localops-ui-kit/blob/main/docs/capability-matrix.md) distinguishes native support, fallbacks, and unsupported behavior.

## Components and Integration Boundaries

The toolkit includes layouts and navigation, buttons and state displays, forms, dialogs, data tables, task monitors, and logs. Direct browser components add results reading, bounded draft editing, and modal content panels. Keyboard navigation, visible focus, dialog focus containment, Escape handling, and focus recovery are part of the component behavior.

Applications supply data and actions through adapters and callbacks. They retain ownership of routes, transport, credentials, authorization, filesystem policy, persistence, and the meaning of an operation's result. A task monitor can display progress and expose an injected cancel action; it does not decide what a task is allowed to do. An editor can offer a draft or export intent; it does not acquire permission to write source files or execute them.

The separate `localops-ui-testkit` package supports rendered-layout checks through Python Playwright, including overflow, clipping, occlusion, hit testing, and reachability. It provides evidence about the interface, not a substitute for consumer-specific accessibility and usability review.

## Getting Started

Python **3.12 or newer** and Git are required for the documented Git-based installation:

~~~sh
python -m pip install "localops-ui @ git+https://github.com/unixwzrd/localops-ui-kit.git@main"
~~~

For both optional terminal renderers:

~~~sh
python -m pip install "localops-ui[all] @ git+https://github.com/unixwzrd/localops-ui-kit.git@main"
~~~

Use `[cli]` for Rich alone or `[tui]` for Textual alone. Neither the toolkit nor its separate test kit is published to PyPI; these are GitHub installation commands. Installing the toolkit does not start a server. Applications should pin a qualified full commit for reproducible deployments rather than depend on the moving `main` branch.

Start with the [widget guide](https://github.com/unixwzrd/localops-ui-kit/blob/main/docs/widget-guide.md), then the [adoption guide](https://github.com/unixwzrd/localops-ui-kit/blob/main/docs/adoption-guide.md) for integration contracts. The [live showcase](https://unixwzrd.ai/localops-ui-kit/) uses synthetic data and in-memory adapters; its examples do not execute shell commands or access the visitor's filesystem.

## Preview Status

Version **0.2.0** is a public-preview preparation release under the **MIT license**, not a production-readiness or consumer-adoption claim. Package, component API, and manifest schema versions are tracked separately. Check the [README](https://github.com/unixwzrd/localops-ui-kit), [changelog](https://github.com/unixwzrd/localops-ui-kit/blob/main/CHANGELOG.md), and capability matrix before choosing an integration baseline.
