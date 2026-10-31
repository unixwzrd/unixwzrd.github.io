---
short_link_basis: "/_posts/technology/2026-10-19-tuning-codex-subagents-for-the-work-they-actually-do.md"
short_url: "https://unixwzrd.ai/s/9d7fe8140e/"
layout: post
title: "Tuning Codex Subagents for the Work They Actually Do"
date: 2026-10-19 07:00:00 -0500
categories: [technology]
tags: [codex, ai-agents, developer-workflow]
excerpt: "My Codex subagents have different jobs, models, and reasoning settings. That helps me route work sensibly, but spawning more agents is not a magic token discount."
image: /assets/images/blog/codex-subagent-routing-hero.png
discussion_prompt: "Which tasks have actually been worth handing to a subagent in your setup?"
---

I keep seeing complaints about how quickly Codex burns through usage. I understand the frustration. A subagent is another model doing another piece of work, with its own context and tool calls. Start four of them to answer a question you could have settled with one search, and you have probably made the bill worse.

There is another easy mistake, though: letting every subagent inherit the same model and high reasoning setting as the main thread. Finding the file that owns a menu and untangling a stubborn concurrency bug are different jobs. I configure them that way.

Before I delegate anything, I write down the objective, constraints, and acceptance checks. A clear plan usually saves more wasted work than clever agent routing.

This is the setup I use, trimmed to the parts that matter for routing work. It is an example to adapt, not a promise of a particular percentage saved. [OpenAI's current subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) is quite direct that subagent workflows generally use more total tokens than comparable single-agent runs. The useful question is whether the extra work bought you a better result, a faster independent investigation, or less expensive reasoning on a task that did not need the lead model.

<!--more-->

## Give the Main Thread a Different Job

My main Codex thread uses a stronger model at high reasoning effort. It keeps the problem, constraints, architecture, and final decision together. I do not need that same setting copied into every bit of file discovery.

The relevant part of my `~/.codex/config.toml` looks like this:

~~~toml
# Agent/sub-agent configuration.
[agents]
enabled = true

# Fallback for spawn_agent calls that don't explicitly select model/effort.
default_subagent_model = "gpt-6-luna"
default_subagent_reasoning_effort = "low"

# Primary thread is not counted here: allow up to five child agents.
max_concurrent_threads_per_session = 5

[agents.explorer]
description = "Fast, read-only codebase exploration, dependency tracing, file mapping, and bounded upstream research."
config_file = "agents/explorer.toml"

[agents.implementer]
description = "Implement bounded code changes and tests from an approved plan."
config_file = "agents/implementer.toml"

[agents.reviewer]
description = "Independent review for correctness, regressions, security vulnerabilities, and edge cases."
config_file = "agents/reviewer.toml"

[agents.diagnostician]
description = "Investigate complex failures, reproduce defects, correlate evidence, and identify root causes before recommending changes."
config_file = "agents/diagnostician.toml"

[agents.documenter]
description = "Maintain README files, API documentation, changelogs, and release notes. Document verified behavior without modifying implementation."
config_file = "agents/documenter.toml"

[agents.tester]
description = "Develop focused regression tests, reproduce failures, identify coverage gaps, and report test results. Avoid unrelated production changes."
config_file = "agents/tester.toml"

~~~

The [downloadable config example]({{ '/assets/code/codex-subagent-routing/config.toml' | relative_url }}) contains just those agent settings. Merge the sections you want into your existing file; do not replace your whole configuration with somebody else's. In particular, my local approval policy, sandbox access, notification command, and feature switches are machine policy, not token-tuning advice.

The two default-subagent values are the fallback when a spawned agent does not get a more specific model and effort. An explicit spawn can override those defaults. A role's own config file can set its model and effort as well. The current [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents those keys and says the relative `config_file` paths are resolved from the config file that declares the role.

The concurrency number is a ceiling on open child-agent threads, excluding the main thread. It does not tell Codex to start five agents, and it does not make five agents cheaper.

## Give Each Role the Amount of Thought It Needs

The separate files under `~/.codex/agents/` are small on purpose. My explorer uses Luna at low effort:

~~~toml
# ~/.codex/agents/explorer.toml
model = "gpt-6-luna"
model_reasoning_effort = "low"
model_verbosity = "low"
~~~

The other three follow the same pattern. Here are the [explorer]({{ '/assets/code/codex-subagent-routing/agents/explorer.toml' | relative_url }}), [implementer]({{ '/assets/code/codex-subagent-routing/agents/implementer.toml' | relative_url }}), [reviewer]({{ '/assets/code/codex-subagent-routing/agents/reviewer.toml' | relative_url }}), [diagnostician]({{ '/assets/code/codex-subagent-routing/agents/diagnostician.toml' | relative_url }}), [documenter]({{ '/assets/code/codex-subagent-routing/agents/documenter.toml' | relative_url }}), and [tester]({{ '/assets/code/codex-subagent-routing/agents/tester.toml' | relative_url }}) files to inspect or download.

| Role          | My setting          | What I give it                                                                                          |
| ------------- | ------------------- | ------------------------------------------------------------------------------------------------------- |
| Explorer      | GPT-6 Luna, low     | Read-only file mapping, dependency tracing, and a concise evidence report                               |
| Implementer   | GPT-6.1 Sol, medium | A bounded change with named files and relevant tests                                                    |
| Reviewer      | GPT-6.1 Sol, high   | An independent look for correctness, regressions, and edge cases                                        |
| Diagnostician | GPT-6.1 Sol, high   | A difficult failure to reproduce and explain before anyone changes code                                 |
| Documenter    | GPT-6.1 Sol, medium | A README, API documentation, changelog, and release note for verified behavior                          |
| Tester        | GPT-6.1 Sol, medium | A focused regression test, failure reproduction, coverage gap identification, and test result reporting |

Those are my choices for my work, not universal model recommendations. Use models and effort levels your Codex client and account actually support. Higher effort can use more reasoning tokens and time; sometimes that buys a better answer on a hard problem. A lighter model is no bargain if it needs three attempts to finish work a stronger model gets right the first time. [OpenAI's subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents) covers the inheritance and precedence rules, including that model and effort in a custom agent file take precedence for that role.

There is one configuration wrinkle worth calling out. My example declares each role in `config.toml` and points it at a TOML **config layer**. The current docs also describe standalone, automatically discovered custom-agent files. Those standalone files require `name`, `description`, and `developer_instructions`. Do not lift one of my three-line role layers and assume it is a complete standalone-agent definition. Both approaches exist; know which one you are setting up.

`explorer` is also the name of a built-in Codex role. [The current docs](https://learn.chatgpt.com/docs/agent-configuration/subagents) say a custom agent with the same name takes precedence, so check your own role declarations if an explorer behaves differently than you expected.

## The Configuration Does Not Decide When to Delegate

I also have instructions in `AGENTS.md`. The relevant part is short:

~~~markdown
- Use subagents selectively, not automatically.
- Delegate only work that is independent, bounded, or would add substantial noise to the primary context.
- Keep architecture, ambiguous debugging, security-sensitive decisions, cross-cutting changes, and final review with the primary agent.
- Do not delegate trivial sequential work.
- When delegating implementation, give the subagent a narrow scope and explicit acceptance criteria.
- Require subagents to report what they inspected or changed, commands/tests run, failures encountered, and unresolved questions.
- The primary agent owns synthesis and final decisions.
~~~

That is a *workflow* rule. The TOML files set model behavior for the roles; they do not judge whether spawning one is a good idea. [Codex documents AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) separately from its subagent settings.

There is also an external-agent preference in the same file. This is the part I actually use for coding handoffs:

~~~markdown
- Prefer Cursor Agent CLI for suitable delegated development tasks when available and authenticated.
- Use Cursor's automatic model selection unless a specific model is required.
- Prefer available Cursor premium usage before consuming Codex subagent capacity for equivalent tasks.
- If Cursor reports premium usage exhausted or unavailable, fall back to an appropriate available agent or model.
- Do not enable paid overages or purchase additional credits automatically.
- Verify externally generated changes and test results before accepting them.
~~~

The full instructions also keep architecture, security-sensitive decisions, and final review with the primary agent, and prohibit concurrent edits to the same files by independent runtimes. In practice, Codex runs the Cursor Agent command in the shell, gives it a bounded coding task, waits for the result, then inspects the diff and runs the relevant tests. There is no special bridge hiding in the middle. The `AGENTS.md` rule tells Codex when to make that handoff; a skill could spell out the command for a different tool, but a skill is not required when Codex already knows how to invoke it.

This is not a Cursor-only trick. I use Cursor because I already have a subscription and prefer its Agent CLI for suitable coding tasks. A reader with a different command-line coding agent could use the same pattern. [Claude Code](https://code.claude.com/docs/en/cli-usage) has `claude -p`, and [GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference) has `copilot -p` for non-interactive prompts. I could not confirm an official headless command for Windsurf's Cascade, so I would check that interface before promising the same handoff there. [VS Code's `code chat`](https://code.visualstudio.com/docs/configure/command-line) opens an editor chat; for a shell-driven handoff, GitHub Copilot CLI is the clearer example.

The external agent is not one of the Codex `[agents.*]` roles above, and its usage belongs to its own account. My Cursor subscription can preserve my Codex allocation, but it does not make the work free or prove I used fewer resources overall. Whichever CLI you choose, give it a clear task, avoid simultaneous edits to the same files, and check what it changed. My Cursor rule is a personal preference and an allocation choice, not an endorsement of a universal winner.

Suppose the new “On this page” index on my Jekyll posts stops showing up. An explorer could map the Ruby filter, post layout, and focused tests, then return the few files that matter. If the cause is obvious and the fix is tiny, the main thread can handle it. If a bounded implementation is worth delegating, the implementer gets the affected files and acceptance checks. If the behavior remains strange after a failed fix, that is when the diagnostician earns its keep. I am not going to launch all four roles because a dropdown failed to open.

The role description is guidance, not a separate security boundary. Codex subagents inherit the parent session's sandbox and approval settings. My “read-only explorer” instruction tells it what job to do; it does not create a read-only filesystem on its own. The [official subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents) makes that inheritance explicit.

## Count the Whole Job

I would be suspicious of a post claiming that this setup “saves 40% of your tokens” without showing the workload, the models, the retries, and the final quality. I have not measured that claim, so I am not making it. A low-effort explorer can spare the main thread a noisy search and avoid using high-effort reasoning for a mechanical task. An extra review can also catch a costly mistake. It can just as easily add work that nobody needed.

There *is* a way to get past opinion here, even if I do not have a controlled result to publish yet. [Codex's `/status` command](https://learn.chatgpt.com/docs/developer-commands) shows usage for the current chat, while `/usage daily`, `/usage weekly`, and `/usage cumulative` show account token activity where that command is available. For a repeatable CLI run, `codex exec --json` emits newline-delimited events; the completed turn has a `usage` record. I can extract that record without saving the full event stream, which may contain prompts, file contents, and tool output.

First, check what `codex` actually runs with `type -a codex`. On my Mac, a custom desktop launcher with that name came first on `PATH`; it opened the app and printed shell-startup messages instead of running the CLI. The example below uses the bundled CLI's explicit path to avoid that collision and `-C` to select the website's Git checkout, even if I run it from another directory such as `~/.codex`. Both paths are specific to my Mac; replace them with your actual CLI and repository paths.

~~~sh
set -o pipefail

codex_cli="/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex"
repo_dir="/Users/mps/projects/AI-PROJECTS/DTS-WebSite/unixwzrd.github.io"

"$codex_cli" exec --json --sandbox read-only \
  -C "$repo_dir" \
  "Map the files that build the post contents index; make no edits." |
  jq -c 'select(.type == "turn.completed") | .usage'
~~~

The filter discards intermediate events and prints only the usage object when the turn completes, not the file map itself. The terminal can therefore stay quiet for quite a while as Codex works; silence alone does not mean it has hung. `pipefail` makes the pipeline report a Codex failure rather than letting a successful `jq` exit hide it. To inspect the live event stream, temporarily omit the pipe to `jq`, keeping in mind that those events can contain sensitive content.

That command is a **single-run measurement**, not a magic whole-workflow meter. A failed run may not have a completed-turn usage event. I would not assume the parent event covers every child agent without checking the accounting for that run. OpenAI's [Agents API traces](https://developers.openai.com/api/docs/guides/agents-api/observability) can break out root and subagent usage, but that is a different integration from my ordinary Codex desktop and CLI subscription workflow; its usage is best-effort and can arrive late. I would not mix those numbers with a desktop allowance as though they were the same billing record.

Cursor belongs in the ledger too. Its CLI can emit structured output with `agent -p --output-format json`; I would record the session and request IDs and any usage fields my installed version reports, then check the [account's usage view](https://prod.cursor.com/help/models-and-usage/usage-limits) over the same interval. If I later run through the [Cursor SDK](https://cursor.com/docs/sdk/typescript), it exposes per-run token counts and a separate billed-usage lookup, although local billed-usage access is still account-gated. A Codex token and a Cursor token are not interchangeable units of subscription value, and a move from one allowance to another is not a reduction in the work performed.

Here is the comparison I want to run before claiming an effect: take several small, real repository tasks at fixed commits, write the acceptance checks down first, and use the same prompt for a fresh single-agent run and a fresh tuned-delegation run. Give the external-agent route its own arm when the task qualifies; Cursor is the one I would measure in my setup. For each run, record the client version, requested model and effort, elapsed time, token counts where reported, cache activity, retries, and test results. Review the finished work blind to the route if possible. Repeat enough tasks that one lucky answer or warm cache does not decide the story. If a provider does not expose a number, mark it missing; do not fill it in with a guess.

That gives me three separate answers: Did the task pass? Did it finish faster? And what did it consume across **all** the agents and services used? More parallel threads may finish sooner while consuming more total tokens. Those are different numbers.

My practical rule is simple. Start with the main thread. Delegate a clear piece of work when the separation will help. Give that agent a model and reasoning level that fit the job. Keep the final decision with someone who can see the whole problem.

If I need to find a filename, I want a fast scout. If I need to understand why the third fix still fails, I want a diagnostician. Paying for the deepest reasoning on both is silly. Spawning an entire committee for either is silly too.
