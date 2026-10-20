---
layout: project
title: "Code Analysis Suite"
category: code-analytics
permalink: /projects/code-analytics/
short_link: true
short_link_basis: "/projects/code-analytics.md"
short_url: "https://unixwzrd.ai/s/bbabdc366a/"
image: /assets/images/projects/code-analytics/code-analysis-banner.png
excerpt: "Evidence-backed architecture analysis for Python, JavaScript/JSX, and Ruby, with retained reports, CLI exports, and a beta local WebUI."
project_intro: |
  Code Analysis Suite turns source structure into portable evidence for architecture review and refactoring. Inspect symbols, dependencies, complexity, contracts, duplication, and change impact through saved reports, the CLI, an optional terminal interface, or a local browser UI.

  The CLI analysis and artifact-generation workflows are the established starting point. The WebUI is still in beta and undergoing usability work. Start with the [installation guide](https://github.com/unixwzrd/code-analytics#installation) or the [Python beginner investigation](https://github.com/unixwzrd/code-analytics/blob/main/tutorials/python/beginner/README.md), and review the [beta scope](https://github.com/unixwzrd/code-analytics/blob/main/docs/beta.md) before relying on a particular capability.
---

## See the Architecture Before You Change It

**Code Analysis Suite** provides evidence for understanding a codebase before deciding how to change it. It collects structural observations, binds them to source locations and hashes, and retains them in a validated JSON report. Tables, diagrams, comparisons, and review packets are views of that saved evidence, not reasons to keep rescanning the same source.

The project is in beta, with **0.2.0b1** as the documented candidate version. Command-line scanning, report generation, and exports are the established workflows. The local browser interface is actively being tested and refined; beta feedback is particularly useful for confusing navigation, source investigation, and finding the right evidence. This is not a stable API or report-format compatibility promise.

## What It Examines

- **Structure and dependencies:** source roots, modules, symbols, spans, local imports, import cycles, and complexity metrics.
- **Contracts and data flow:** Python contracts, dictionary shapes, validation, lifecycle evidence, and bounded producer/consumer relationships.
- **Refactoring review:** clone/commonality evidence, state and side effects, responsibility groups, and bounded proposals with explicit evidence limits.
- **Change and test evidence:** static test impact, explicitly requested Git history, imported coverage, and opt-in Python profiling.
- **Investigation and presentation:** saved-report queries, comparisons, tables, graphs, review packets, and hash-verified source browsing.

Python has the broadest analytical coverage through its standard-library AST frontend. JavaScript/JSX collection uses optional Tree-sitter dependencies; Ruby uses an existing Ruby/Prism installation through a parser driver. Capabilities differ by language, and reports preserve partial, unsupported, and unavailable evidence. **TypeScript/TSX and automatic source refactoring are not supported.**

## Evidence You Can Keep and Revisit

The authoritative `code-analysis-report` JSON retains source-relative paths, SHA-256 source hashes, configuration identity, provider status, diagnostics, completeness, limitations, and stable evidence IDs. Saved evidence can be queried, compared, and exported without another source scan. Browsing original source separately requires matching files and hashes.

The CLI can produce reports and projections in formats including Markdown, tables, DOT, Mermaid, and graphics where supported by the selected view. SVG/PNG graph rendering requires an available Graphviz executable. Missing providers and renderers remain explicit; an unavailable tool does not become an empty successful result. The [report and diagram catalog](https://github.com/unixwzrd/code-analytics/blob/main/docs/report-and-diagram-catalog.md) documents individual views and their limitations.

A finding is a reason to investigate, not permission to edit. High complexity does not establish an extraction boundary, an import cycle is not automatically a defect, and static observations cannot prove runtime behavior or semantic equivalence.

## Local Browser and Terminal Investigation

The loopback WebUI supports saved-report exploration, comparisons, verified source navigation, contextual offline help, and session-only editing drafts. Its shared browser components come from [LocalOps UI Kit](/projects/localops-ui-kit/); the application retains ownership of analytical meaning and operational behavior. The optional Textual interface provides another route into saved evidence.

Opening the browser UI does not start a scan. Use `--no-collection` when browsing saved reports without collection-launch capability. Closing a browser tab does not stop its background session; use the application's stop control or `code-analysis ui-stop` as documented in the [UI guide](https://github.com/unixwzrd/code-analytics/blob/main/docs/ui-guide.md).

## Getting Started

Python **3.12 or newer** is required. Install from the source repository in an isolated environment rather than assuming a PyPI release:

~~~sh
git clone https://github.com/unixwzrd/code-analytics.git
cd code-analytics
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install .
code-analysis doctor
~~~

From a project directory, the basic workflow is:

~~~sh
code-analysis scan .
code-analysis
~~~

For a named report and a dependency graphic:

~~~sh
code-analysis refactor . --json-compact -o refactor.json
code-analysis summary refactor.json
code-analysis export refactor.json --projection dependencies --format svg -o dependencies.svg
code-analysis ui refactor.json --source-root . --no-collection
~~~

The `refactor` command generates analytical evidence and proposals; it does not rewrite source. Install Graphviz separately if using the SVG command. Optional JavaScript parsing, terminal UI, and runtime capabilities have explicit extras described in the [README](https://github.com/unixwzrd/code-analytics). Run `doctor` and `providers` to see what is actually available.

## Try an Investigation Before Scanning Your Own Project

The repository includes [nine Fawlty Towers-inspired tutorials](https://github.com/unixwzrd/code-analytics/blob/main/tutorials/README.md): beginner, intermediate, and advanced investigations for Python, JavaScript, and Ruby. Each includes a working sample application, saved source-bound evidence, an independent investigation, optional hints, and separate solutions. They are supplied in the source checkout, not as a tutorial browser bundled in the wheel.

Start with the [Python reservation desk](https://github.com/unixwzrd/code-analytics/blob/main/tutorials/python/beginner/README.md). Opening its saved report requires neither running the sample application nor rescanning its source.

## Safety and Beta Feedback

Static analysis parses source without importing or executing the target application. By default it writes owned reports and caches under a self-ignored `.code-analysis/` workspace; use `--no-workspace` or an explicitly selected alternative for read-only targets. Runtime profiling and coverage execution are separate, authorized workflows that run a supplied workload with the operator's permissions; they are not a sandbox.

Analysis is local, but reports can still disclose source names, literals, relationships, and diagnostics. Review artifacts before sharing them. Report nonsensitive issues through [GitHub](https://github.com/unixwzrd/code-analytics/issues), including the version, platform, interpreter/browser, command or UI task, expected result, actual diagnostics, and a minimal synthetic reproduction. Follow the repository's [security policy](https://github.com/unixwzrd/code-analytics/blob/main/SECURITY.md) for sensitive reports.

The project is **MIT-licensed**. The [beta notes](https://github.com/unixwzrd/code-analytics/blob/main/docs/beta.md), [CLI reference](https://github.com/unixwzrd/code-analytics/blob/main/docs/cli.md), and [changelog](https://github.com/unixwzrd/code-analytics/blob/main/CHANGELOG.md) distinguish current capabilities from planned work.
