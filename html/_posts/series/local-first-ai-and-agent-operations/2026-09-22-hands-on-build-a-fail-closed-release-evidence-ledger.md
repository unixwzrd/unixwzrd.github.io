---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-22-hands-on-build-a-fail-closed-release-evidence-ledger.md"
short_url: "https://unixwzrd.ai/s/7afa6d66f9/"
layout: post
title: "Hands-On: Build a Fail-Closed Release Evidence Ledger"
date: 2026-09-22 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, llm-ops-kit, testing, python, devops]
image: /assets/images/blog/agent-optimization/post-14a-release-evidence-ledger-hero.png
excerpt: "Run a standard-library Python lab that binds release evidence to one artifact identity and rejects missing gates, stale observations, mixed identities, and unsupported claims."
series: "Local First AI and Agent Operations"
series_part: "14A"
series_order: 145
series_total: 17
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 14
series_previous_title: "What a Prerelease Still Has to Prove"
series_previous_url: /technology/2026/09/22/what-a-prerelease-still-has-to-prove/
series_next_title: "Secrets-Kit: From Local Secret Store to Governed Beta Service"
published: true
---

This is Hands-On 14A in the Local-First Agent Operations series. It accompanies [Part 14, What a Prerelease Still Has to Prove]({{ page.series_previous_url | relative_url }}), where I separated implemented capability, exact-artifact acceptance, and observable publication into three ledgers that do not necessarily move together.

A release conversation can go wrong before anyone runs a single test. One person is talking about what the source implements, another is looking at a green CI run, and a third is looking at a public download. All three may be stating true facts about different ledgers.

This lab gives those facts somewhere separate to live. It validates an invented release-evidence packet, binds every result to one artifact identity, and refuses to turn publication metadata into runtime acceptance. Its successful result is deliberately narrow: `EVIDENCE PACKET READY FOR REVIEW`.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-14a-evidence-packet-flow.svg" alt="An invented release evidence packet passes through closed-schema, identity, gate, time, and claim-support checks. Invalid packets stop with a bounded not-ready result, while a valid packet becomes ready for human review without any release, approval, or publication inference." caption="The validator checks whether the packet is coherent enough to review. It does not decide whether the artifact should be released." variant="wide" %}

Here we can break one of those ledgers safely and see exactly where it stops.

<!--more-->

## Download the Lab

Download the [complete Hands-On 14A package]({{ '/assets/code/agent-optimization/post-14a/release-evidence-ledger.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/agent-optimization/post-14a/release-evidence-ledger.zip.sha256' | relative_url }}). Every source file and fixture is also available through the site's collapsed source viewer:

{% include source_code.html source="/assets/code/agent-optimization/post-14a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/manifest.json" language="json" title="manifest.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/release_evidence.py" language="python" title="release_evidence.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/test_release_evidence.py" language="python" title="test_release_evidence.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/fixtures/review-ready.json" language="json" title="fixtures/review-ready.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/fixtures/missing-gate.json" language="json" title="fixtures/missing-gate.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/fixtures/identity-mismatch.json" language="json" title="fixtures/identity-mismatch.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/fixtures/manifest-mismatch.json" language="json" title="fixtures/manifest-mismatch.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/fixtures/stale-evidence.json" language="json" title="fixtures/stale-evidence.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-14a/fixtures/unsupported-approval.json" language="json" title="fixtures/unsupported-approval.json" %}

## 1. Start With the Boundary

The package reads one local JSON document and prints a deterministic result. It does not build software, install an archive, inspect Git, query CI, make a network request, sign anything, upload anything, approve anything, or publish anything.

That is not a missing feature. It is the point of the exercise. A packet validator should be able to say, "These records refer to the same artifact, every required gate has an entry, and the claims agree with the evidence." It should not be able to promote an artifact because somebody chose an optimistic filename.

The package contains eleven files:

```text
release-evidence-ledger/
|-- README.md
|-- manifest.json
|-- release_evidence.py
|-- run_lab.py
|-- test_release_evidence.py
`-- fixtures/
    |-- review-ready.json
    |-- missing-gate.json
    |-- identity-mismatch.json
    |-- manifest-mismatch.json
    |-- stale-evidence.json
    `-- unsupported-approval.json
```

It requires Python 3.10 or newer and uses only the standard library.

## 2. Verify and Extract the Package

Place the reviewed ZIP and checksum in one directory, then verify the archive before extracting it:

```bash
shasum -a 256 -c release-evidence-ledger.zip.sha256
mkdir release-evidence-lab
cd release-evidence-lab
unzip ../release-evidence-ledger.zip
cd release-evidence-ledger
python3 --version
```

Nothing needs to be installed with `pip`. The package manifest lists the files and their SHA-256 values, while the outer checksum binds the ZIP readers actually download.

## 3. Read the Review-Ready Fixture

Open `fixtures/review-ready.json`. The artifact is invented. Its version, commit, archive digest, manifest digest, evidence identifiers, and dates do not describe a real project or deployment.

The packet declares four required gates. Artifact identity and publication observation have passing evidence. Installation and lifecycle acceptance remain incomplete. The publication observation says that a prerelease was seen, but the approval claim remains `unobserved`.

That combination is intentional. A prerelease can be public while the larger acceptance record remains unfinished. The packet does not need to deny the publication event to preserve that distinction.

Each evidence item repeats the artifact version, source commit, archive digest, and manifest digest. The publication observation must also name the release tag declared by the artifact and point to passing `release-metadata` evidence. This is tedious in exactly the right way. It prevents a result from an older candidate or an unrelated publication record from drifting into the current packet just because the gate name looks familiar.

## 4. Validate the Clean Packet

Run the validator:

```bash
python3 -B release_evidence.py fixtures/review-ready.json
```

The report should begin like this:

```text
EVIDENCE PACKET READY FOR REVIEW
Packet: example-release-review
Artifact: example-control-kit 1.4.0b3
Publication observation: prerelease (supplied evidence)
Acceptance claim: incomplete
Approval claim: unobserved
Required gates: 4
Passed gates: 2
Incomplete gates: 2
Failed gates: 0
Release readiness inferred: no
Approval inferred: no
Next gate: human review of the identity-bound evidence packet.
```

The first line is not a synonym for release readiness. It says a human can now inspect a coherent packet. The two `no` lines make the stopping point hard to miss.

For structured output, add `--format json`:

```bash
python3 -B release_evidence.py fixtures/review-ready.json --format json
```

That form is useful in a review workflow because a later tool can display the counts and claims without scraping terminal prose. It still carries the same bounded decision.

## 5. Remove a Required Gate

The first broken fixture declares a required gate but supplies no corresponding evidence record:

```bash
python3 -B release_evidence.py fixtures/missing-gate.json
test $? -eq 1
```

The validator returns:

```text
EVIDENCE PACKET NOT READY
Error: E_MISSING_GATE
Field: evidence
```

An absent record remains absent. The validator does not reinterpret silence as not applicable, borrow a similarly named result, or reduce the gate count until the packet passes.

That last behavior matters. A release process becomes meaningless if the easiest way to satisfy it is to stop declaring the inconvenient checks.

## 6. Mix Two Artifact Identities

Now run the identity mismatch:

```bash
python3 -B release_evidence.py fixtures/identity-mismatch.json
test $? -eq 1
```

This fixture changes the version, source commit, archive digest, and manifest digest on one evidence record. The result is `E_IDENTITY`, even though the gate name and reported result still look plausible.

The supplied `manifest-mismatch.json` fixture narrows the same test to one field:

```bash
python3 -B release_evidence.py fixtures/manifest-mismatch.json
test $? -eq 1
```

It changes only the evidence record's manifest digest and receives the same `E_IDENTITY` result. In a real release packet, the matching tuple includes the version, source commit, archive digest, and manifest digest. Architecture and observation time then describe where and when that exact artifact was exercised. If any of those facts are unknown, the honest state is unknown. A nearby result from another build is useful history, but it is not exact-artifact acceptance.

## 7. Let Evidence Age Out

Evidence also has a time boundary. The clean packet supplies an evaluation time and a maximum evidence age. The stale fixture moves one observation outside that window:

```bash
python3 -B release_evidence.py fixtures/stale-evidence.json
test $? -eq 1
```

The validator returns `E_STALE`. It does not decide that every engineering result expires after the same number of days. The packet declares its own review window, and the validator enforces the full duration: evidence exactly thirty days old passes a thirty-day limit, while evidence thirty days and one second old does not.

This gives reviewers a visible place to argue about policy. If ninety days is appropriate for one gate and not another, the schema should evolve deliberately. Quietly accepting an old observation because rerunning it is inconvenient is not a policy.

## 8. Try to Invent Approval

The final supplied failure case claims approval without a matching approval record:

```bash
python3 -B release_evidence.py fixtures/unsupported-approval.json
test $? -eq 1
```

The result is `E_APPROVAL_CLAIM`. The validator permits an approval claim only when the packet contains a passing `release-approval` evidence item and the claim points to that exact evidence identifier.

The clean fixture takes the safer path. It records the public prerelease observation and leaves approval provenance unobserved. That does not imply the publication was unauthorized. It means this packet does not contain the decision record, so the program refuses to reconstruct one from the public result.

## 9. Keep Private Material Out of the Packet

The fixtures use symbolic identifiers rather than paths, hosts, addresses, URLs, credentials, or real evidence locations. The validator rejects common private-looking forms such as absolute home and runtime paths, IP addresses, URI authorities, credential assignments, and private-key markers.

Rejected values are not echoed in the bounded error output. This is defense in depth for a teaching package, not a complete secret scanner. A real collector still needs an explicit privacy review before its records are attached to a public issue, release, or article.

The right public evidence reference is often a neutral identifier such as `ci-run-tag` or `archive-checksum-record`, with the private storage location retained separately under normal access controls.

## 10. Run the Fixed Walkthrough

The runner exercises the clean packet and the four supplied failures:

```bash
python3 -B run_lab.py
```

It currently checks twenty-six conditions. Those checks include the observed prerelease state, incomplete acceptance, unobserved approval, gate counts, deterministic output, full artifact identity, five supplied failure fixtures, a contract with no required gate, a publication reference to the wrong gate, a mismatched release tag, both sides of the exact age boundary, and the explicit refusal to infer readiness or approval.

Then run the unit suite:

```bash
python3 -B -m unittest -v test_release_evidence.py
```

The forty-three tests cover closed fields, strict types, malformed timestamps and digests, duplicate gates and evidence, a contract with no required gate, missing records, full identity mismatch, exact-duration staleness, future evidence, publication gate and tag binding, unsupported acceptance and approval claims, privacy rejection, deterministic non-mutating validation, command-line behavior, source boundaries, and manifest integrity.

An abstract-syntax-tree test checks that the runtime does not import network, subprocess, SSH, HTTP, Git, or project-control surfaces. That is a bounded review of this package, not a claim that source scanning can prove every possible Python behavior.

## 11. Adapt the Ledger Without Turning It Into a Release Bot

The fixture is small enough to understand in one sitting, but its separation is useful in a larger workflow:

| Packet section | What supplies it | What the validator may conclude |
| --- | --- | --- |
| Artifact identity | Build or release metadata retained elsewhere | Evidence either matches the declared artifact or it does not |
| Publication observation | A retained observation supplied to the packet | The stated tag or release state was observed according to that evidence |
| Required gates | The reviewed release contract | Every required gate has one unambiguous record |
| Evidence | Test, inspection, and review procedures | Results are current enough and identity-bound |
| Claims | The packet author | Acceptance and approval claims have the required support |

I would keep evidence collection separate from this validator. Collectors may need network access, Git, CI credentials, build tools, target hosts, or privileged inspection. Mixing those powers into the decision layer makes the result harder to reproduce and much harder to audit.

I would also keep human authorization outside the automatic success path. A validator can establish that an approval record exists and matches the packet. It cannot decide that the approver had the right authority, understood the remaining risk, or intended to authorize this exact public action unless the surrounding process defines and reviews those facts.

## 12. Clean Up

Return to the directory above the disposable lab and remove it:

```bash
cd ../..
rm -rf release-evidence-lab
```

The walkthrough changes no service, repository, release, or remote state. The only files created are the extracted teaching package inside the directory you remove.

## Current State

The companion validates an invented release-evidence packet with one clean case and five focused failures. It binds results to an exact artifact identity, requires at least one required gate and one record for every required gate, enforces a declared evidence-age window without truncating partial days, binds publication observations to the expected tag and release-metadata evidence, keeps publication observation separate from acceptance, and rejects unsupported approval claims.

Its successful state is `EVIDENCE PACKET READY FOR REVIEW`. It never infers `RELEASE READY`, `APPROVED`, or `PUBLISHED`, and it performs no operation that could produce any of those states.

## Next Work

A production version would need a reviewed schema for the project's real gates, retention policy, architectures, evidence types, authority model, and privacy boundary. Separate collectors could then produce candidate records, while this layer remained deterministic and offline.

The next gate would still be human review. Only after the exact-artifact acceptance record and the authorization record are complete should a separate, explicitly authorized release procedure do anything public.
