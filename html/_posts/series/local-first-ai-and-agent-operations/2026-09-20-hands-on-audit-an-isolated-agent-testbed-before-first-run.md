---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-20-hands-on-audit-an-isolated-agent-testbed-before-first-run.md"
short_url: "https://unixwzrd.ai/s/b042c7cef2/"
layout: post
title: "Hands-On: Audit an Isolated Agent Testbed Before First Run"
date: 2026-09-20 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, local-first-ai, testing, python, macos]
image: /assets/images/blog/agent-optimization/post-13a-agent-isolation-preflight-hero.png
excerpt: "Run a model-free Python preflight that rejects shared roots, port collisions, contradictory knowledge ownership, duplicate declarations, and reused inference canaries before provisioning begins."
series: "Local First AI and Agent Operations"
series_part: "13A"
series_order: 135
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 13
series_previous_title: "Running Multiple Agents Safely on One LAN"
series_previous_url: /technology/2026/09/20/running-multiple-agents-safely-on-one-lan/
series_next_title: "What Remains Before a Public Release"
published: true
---

This is Hands-On 13A in the Local-First Agent Operations series. It accompanies [Part 13, Running Multiple Agents Safely on One LAN]({{ page.series_previous_url | relative_url }}), where I separated a useful second-agent testbed from the much stronger claim that two environments are actually isolated.

It is much cheaper to find a shared state directory in a JSON file than after two agents have written into it. The same is true for a port collision, a reused credential identity, or a synchronized Vault with two writers. This lab is a small preflight for those mistakes.

The wording of its successful result is deliberate: `MANIFEST READY FOR ISOLATED TEST`. That means the declaration is internally consistent enough to begin live testing. It does not mean the machine was inspected, the agents are isolated, or the design is secure.

<!--more-->

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-13-acceptance-gates.svg" alt="An invented manifest passes through declaration checks before live acceptance may begin. Declaration conflicts are not ready, live failures remain incomplete, and only retained live evidence can support a bounded isolation claim." caption="This lab ends at declaration readiness. Everything below that line belongs to a separately reviewed live acceptance procedure." variant="wide" %}

## 1. Start With What This Lab Refuses to Do {#start-with-the-boundary}

The package reads local JSON fixtures, validates a closed set of fields, and prints a deterministic report. It does not create an account, change a permission, inspect launchd, open a socket, connect over SSH, query a keychain, start an agent, invoke LLM-Ops-Kit, or write into a knowledge store.

That limitation is useful. A declaration preflight can run during design and code review without needing access to the target machine. It catches contradictions before they become an installation problem, then stops before the work requires privilege or private evidence.

The package is deliberately small:

```text
agent-isolation-preflight/
|-- README.md
|-- manifest.json
|-- isolation_preflight.py
|-- run_lab.py
|-- test_isolation_preflight.py
`-- fixtures/
    |-- ready.json
    |-- shared-root.json
    |-- shared-port.json
    `-- shared-vault-writers.json
```

It requires Python 3.10 or newer and uses only the standard library.

Download the [complete Hands-On 13A package]({{ '/assets/code/agent-optimization/post-13a/agent-isolation-preflight.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/agent-optimization/post-13a/agent-isolation-preflight.zip.sha256' | relative_url }}). Every source file is also available here through the site's collapsed source viewer:

{% include source_code.html source="/assets/code/agent-optimization/post-13a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/manifest.json" language="json" title="manifest.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/isolation_preflight.py" language="python" title="isolation_preflight.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/test_isolation_preflight.py" language="python" title="test_isolation_preflight.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/fixtures/ready.json" language="json" title="fixtures/ready.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/fixtures/shared-root.json" language="json" title="fixtures/shared-root.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/fixtures/shared-port.json" language="json" title="fixtures/shared-port.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-13a/fixtures/shared-vault-writers.json" language="json" title="fixtures/shared-vault-writers.json" %}

## 2. Verify and Extract the Package

Download the reviewed archive and checksum into one directory, then verify the archive before opening it:

```bash
shasum -a 256 -c agent-isolation-preflight.zip.sha256
mkdir isolation-lab
cd isolation-lab
unzip ../agent-isolation-preflight.zip
cd agent-isolation-preflight
python3 --version
```

Nothing needs to be installed with `pip`. The package manifest declares only three capabilities: reading a supplied manifest, validating the declaration, and rendering a report. Provisioning, live inspection, networking, process startup, secret access, authoritative writes, and security certification are explicitly outside the package.

## 3. Read the Clean Declaration

Open `fixtures/ready.json`. It describes two invented agents sharing one modest host and one remote inference dependency. The examples use symbolic roots such as `agent-a:state`; they are labels for ownership comparison, not filesystem paths to paste into a real configuration.

The two agents declare different execution users, process-manager domains, configuration roots, state roots, log roots, caches, workspaces, memory stores, credential canaries, channel canaries, and listener ports. One uses a per-user LaunchAgent plan. Because that mode depends on a usable bootstrap domain, the manifest requires planned checks for login, logout, reboot, and headless operation. The other uses a symbolic standalone service domain and therefore does not claim those LaunchAgent checks.

The knowledge section demonstrates two different valid authorities. A writable shared test Vault has one declared owner and one writer. Both agents may read it, but only the owner may write. An immutable shared corpus has readers and no writer, which is correct for read-only input.

The remote inference section lists both clients, requires per-client request identity, and names separate contention and endpoint-failure canaries. Those names do not prove that the tests ran. They make the missing live work visible in the declaration.

## 4. Run the Ready Case {#run-the-ready-case}

```bash
python3 -B isolation_preflight.py fixtures/ready.json
```

The report should begin with:

```text
MANIFEST READY FOR ISOLATED TEST
Testbed: lan-agent-lab
Declared agents: 2
Shared inference dependency: model-node
Declaration conflicts: none
Runtime observed: no
Security certified: no
Next gate: inspect the declared environment with separately reviewed tools.
```

The last three lines are not boilerplate. They keep a clean design review from being mistaken for runtime evidence. JSON cannot tell us who owns a live process, whether a socket is already occupied, whether a credential canary is truly unavailable to the other account, or whether synchronization presented a complete file set to a reader.

For machine-readable output, add `--format json`:

```bash
python3 -B isolation_preflight.py fixtures/ready.json --format json
```

The JSON carries the same decision, agent count, shared dependency, findings, and two explicit false claims: `runtime_observed` and `security_certified`.

## 5. Give Both Agents the Same Root

The first broken fixture declares the same configuration root for both agents:

```bash
python3 -B isolation_preflight.py fixtures/shared-root.json
test $? -eq 1
```

It returns `NOT READY` and reports `shared_owned_root`. The preflight does not try to decide whether that sharing was convenient or intentional. These roots were declared as agent-owned, so sharing one contradicts the isolation plan.

This check covers configuration, state, logs, cache, workspace, and memory roots. It also rejects two categories inside one agent pointing to the same symbolic root. A real collector would later resolve symbolic ownership to actual paths and inspect permissions, links, mounts, and process behavior. This lab does none of that.

## 6. Make the Socket Collision Obvious

The next fixture gives both gateway declarations the same port on the same host:

```bash
python3 -B isolation_preflight.py fixtures/shared-port.json
test $? -eq 1
```

The finding is `same_host_port_collision`. The same port on different hosts could be valid, which is why the comparison uses the host and port together. The fixture does not include real addresses or private ports.

A live test still has more work. It must verify the bind address, process owner, transport direction, and teardown behavior. A stale tunnel or undeclared debug listener will not appear in a declaration no matter how carefully the JSON is validated.

## 7. Try Two Writers on One Shared Vault

Now run the knowledge-ownership failure:

```bash
python3 -B isolation_preflight.py fixtures/shared-vault-writers.json
test $? -eq 1
```

The fixture declares Agent A as owner but lists both agents as writers. The report identifies both the owner mismatch and multiple writers on a shared authority.

The rule is narrower than saying every store needs one writer. A read-only replica or immutable corpus may have none. Every writable authority does need one declared owner, and a shared authority may have at most one writer in this initial design. That does not turn synchronized storage into a transaction system. It simply prevents the test from beginning with an ownership contradiction.

## 8. Look at the LaunchAgent Gate

In the clean fixture, Agent A uses `launchagent` mode and carries this test plan:

```json
["login", "logout", "reboot", "headless"]
```

Remove `headless` and run the preflight again. The manifest is rejected with `E_BOOTSTRAP_PLAN` because it no longer describes the complete acceptance shape required for that mode.

The program does not claim that any of those tests passed. A future live procedure has to observe the applicable bootstrap domain and the agent's behavior under each condition. If the account cannot provide the required persistent context, the design can move to a separately reviewed standalone manager or another native service domain instead of pretending that a property list is enough.

## 9. Keep Credential Tests Harmless

The example uses `credential-canary-a` and `credential-canary-b`, not secret values and not production identities. The same pattern is used for communication channels. If the two agents declare the same reference, the preflight returns `shared_credential_reference` or `shared_channel_reference`.

In a live acceptance run, each canary should be least privilege and disposable. Agent A should be able to use its own canary, Agent B should be denied that canary, and the reverse should be tested separately. There is no reason to prove separation by attempting to read a real token or send a message through another agent's production channel.

The validator also rejects recognizable private forms such as absolute paths, network addresses, URI authorities, credential assignments, and private-key markers. Rejection errors use bounded codes and do not echo the input. These checks are defense in depth for the teaching artifact, not a complete secret scanner.

## 10. Run the Fixed Walkthrough {#run-the-fixed-walkthrough}

The runner exercises the ready manifest and all three collision fixtures:

```bash
python3 -B run_lab.py
```

It currently checks sixteen conditions. Every case must return the expected decision and findings, and every result must say that runtime was not observed and security was not certified.

Then run the unit suite:

```bash
python3 -B -m unittest -v test_isolation_preflight.py
```

The thirty-three tests cover deterministic output, root and port collisions, writable and read-only knowledge rules, shared and non-shared participant cardinality, LaunchAgent bootstrap plans, duplicate collection entries, shared identity references, inference attribution, distinct contention and failure canaries, teardown conflicts, closed fields, strict JSON types, bounded privacy rejection, the command-line error contract, lack of execution or network imports, non-mutating validation, and manifest-file integrity.

An abstract-syntax-tree check verifies that the runtime source does not import subprocess, socket, HTTP, SSH, or LLM-Ops-Kit surfaces. That is a bounded claim about this reviewed package. It is not a general proof that Python programs cannot have side effects.

## 11. Turn the Declaration Into a Live Test Plan

Once the manifest is clean, the real work begins. A separately reviewed collector and procedure would need to compare each declared item with the machine:

| Declaration | Live evidence still required |
| --- | --- |
| Execution user and process domain | Observed process ownership and bootstrap behavior across the required conditions |
| Symbolic roots | Resolved paths, permissions, links, mounts, write tests, and negative cross-account tests |
| Listener ports | Owning process, bind address, transport direction, collision behavior, and verified removal |
| Credential and channel canaries | Positive use by the owner and denial to the other agent without exposing values |
| Knowledge ownership | One observed writer, read-only consumers, synchronization caveats, and no concurrent merge path |
| Shared inference | Per-client attribution plus controlled solo, contention, endpoint-failure, and recovery runs |
| Teardown declaration | Removed jobs, processes, sockets, canaries, and owned roots, with preserved data verified separately |

That live phase should bind its report to the exact artifact version and digest tested. It should also retain failures and unknown observations rather than quietly turning them into a pass.

## 12. Clean Up

Return to the directory above the disposable lab and remove it:

```bash
cd ../..
rm -rf isolation-lab
```

No service or operating-system state was changed by the package. The only files created during this walkthrough came from extracting the archive into the directory you just removed.

## Current State

The companion is a model-free declaration preflight over four invented fixtures. The ready case has separate roots, identities, references, ports, writable ownership, read-only authority, shared-inference test declarations, and teardown responsibilities. Three negative cases expose the collisions most likely to make an early two-agent experiment misleading.

The package does not inspect or certify a live environment. Its successful result is permission to begin an isolated test, not evidence that the test passed.

## Next Work

The next artifact would be a privacy-bounded live collector that resolves the symbolic declaration into process, filesystem, launchd, listener, canary, synchronization, and inference observations. It would require explicit privileges, sanitization, versioned evidence, cancellation and timeout behavior, and its own negative tests.

Only after that procedure and teardown have been exercised against the exact release artifact should the result graduate from `MANIFEST READY FOR ISOLATED TEST` to a bounded isolation acceptance claim.
