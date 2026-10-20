---
layout: post
title: "Introducing Code Analysis Suite: Evidence Before Refactoring"
date: 2026-10-20
category: code-analytics
content_type: introduction
tags: [python, developer-tools, testing, local-first, open-source]
permalink_slug: "code-analysis-suite-introduction"
short_link_basis: "/projects/code-analytics/_posts/2026-10-20-code-analysis-suite-introduction.md"
short_url: "https://unixwzrd.ai/s/7e7b007908/"
excerpt: "Code Analysis Suite turns source structure into saved evidence for architecture review and refactoring. The CLI is working; the local WebUI is in beta, and I am looking for feedback."
image: /assets/images/projects/code-analytics/code-analysis-banner.png
discussion_prompt: "When you investigate an unfamiliar codebase, what evidence do you need before you are comfortable changing it? If you try the beta, where does the interface help or get in your way?"
published: true
---

Before I start moving functions around in a codebase, I would like to know what they do, what depends on them, what state they touch, and what evidence supports the proposed change. A long function is not automatically a bad function, and dividing it into six shorter ones does not automatically make the software better. Sometimes it just gives the same problem six addresses.

**Code Analysis Suite** is built around that distinction. It turns source structure into evidence I can inspect, keep, compare, and use when deciding what to change. The command-line analysis and artifact generation are working, and I am opening the project up for beta feedback. The WebUI is still rough in places, and I am working through that rather than pretending the presence of a browser makes the interface finished.

<!--more-->

## Understand the Code Before Rearranging It

The suite examines modules, symbols, dependencies, import cycles, complexity, duplication, state and side effects, and change/test relationships. Python analysis also covers contracts, dictionary shapes, validation, and bounded producer/consumer relationships. Those observations have source locations and evidence behind them; they are not a list of instructions to apply blindly.

Python has the broadest coverage, using the standard-library AST without importing the target application. JavaScript/JSX has an optional Tree-sitter frontend, and Ruby uses an existing Ruby/Prism parser installation. They do not have feature parity. Unsupported constructs and unavailable providers stay visible in the report instead of turning into reassuring empty sections. TypeScript/TSX is not supported, and the tool does not automatically refactor your source.

That last point is deliberate. I want help understanding an extraction boundary, not a tool deciding that a line-count threshold has given it permission to redesign the application. A finding should lead me back to ownership, data flow, dependencies, state, or compatibility. It should not bypass those questions.

## Collect the Evidence, Then Keep Working With It

The central artifact is a validated JSON report, with source-relative paths, SHA-256 hashes, provider states, diagnostics, completeness, limitations, and stable evidence IDs. Tables, diagrams, comparisons, and review packets are views of that retained evidence. Once I have collected a report, changing the presentation should not require running the analysis again.

That makes the command-line workflow useful on its own. I can collect evidence, inspect a summary, export a dependency view, or compare a baseline and candidate report without starting the WebUI. For example, after installing the suite and Graphviz for SVG rendering:

~~~sh
code-analysis refactor . --json-compact -o refactor.json
code-analysis summary refactor.json
code-analysis export refactor.json --projection dependencies --format svg -o dependencies.svg
~~~

Despite the command's name, `refactor` generates analysis and proposals; it does not edit the source. Other supported views can be exported as tables, Markdown, DOT, Mermaid, and graphics according to the selected projection. Missing evidence and renderers remain explicit. I would much rather get a useful failure than a beautifully rendered diagram of information the tool never collected.

## The Browser Is Another Way Into the Same Evidence

The local browser interface provides saved-report exploration, comparisons, hash-verified source navigation, offline contextual help, and session-only drafts. It uses [LocalOps UI Kit](/projects/localops-ui-kit/) for its shared interface components, while Code Analysis Suite remains responsible for what the evidence means and which operations are available. The UI-kit work was one of the dependencies that needed to come together; having those components available does not mean every application workflow has suddenly become intuitive.

This is where I particularly want other people to try it. The CLI is solid enough to collect reports and generate the artifacts; the WebUI still has rough edges that I am testing and fixing. Automated checks are useful, but they do not tell me whether somebody unfamiliar with the project can find a relationship, understand why evidence is missing, or get back to the source without wondering what the hell just happened.

Starting the UI does not start a scan. You can explicitly open a saved report without collection-launch capability:

~~~sh
code-analysis ui refactor.json --source-root . --no-collection
~~~

Original-source browsing requires the matching files and hashes. The report itself remains useful without them. On macOS, the ordinary UI launcher returns your shell prompt while the session runs in the background; closing the browser tab does not stop it. Use the stop control or `code-analysis ui-stop` when you are finished.

## Let Basil Supply the Sample Code

There are nine Fawlty Towers-inspired tutorial investigations in the repository, covering beginner, intermediate, and advanced exercises in Python, JavaScript, and Ruby. They include working sample applications and saved source-bound evidence, followed by an investigation, optional hints, and separate solutions. Sybil wants answers before Basil improves the hotel software again, which strikes me as a fairly reasonable architecture-review policy.

The [Python reservation desk](https://github.com/unixwzrd/code-analytics/blob/main/tutorials/python/beginner/README.md) is the starting point. You can open its supplied evidence without running the application or rescanning it. The tutorials are in the source checkout, not bundled as an installed-wheel tutorial browser, and the language-specific capability limits still apply.

## Beta Means There Is Still Work to Do

The documented candidate is **0.2.0b1**, under the MIT license, and it requires Python **3.12 or newer**. Start with the [repository installation instructions](https://github.com/unixwzrd/code-analytics#installation), then run `code-analysis doctor` and `code-analysis providers` to check the capabilities available in your environment. Installation is from source; this announcement is not a claim that a package release has appeared on PyPI.

Static scans do not import or execute the target application, although they normally create their own `.code-analysis/` evidence workspace. Coverage execution and profiling are separate, explicit operations that run a supplied workload with your permissions. Reports can still contain source-derived names and details, so please do not attach a proprietary project's entire workspace to a public issue just because the paths are portable.

What I would find useful now is a small reproduction, the version and environment, what you expected, and what actually happened—especially where the WebUI makes a straightforward investigation unnecessarily difficult. The [beta scope](https://github.com/unixwzrd/code-analytics/blob/main/docs/beta.md) documents current limits, and [GitHub issues](https://github.com/unixwzrd/code-analytics/issues) are available for nonsensitive feedback. The [project page](/projects/code-analytics/) collects the overview and future updates. The aim is to make a better-informed change, not just a faster one.
