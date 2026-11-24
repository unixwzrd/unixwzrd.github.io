---
layout: post
title: "ARTEX and the November Outages: A Real Threat Is Not the Same as Attribution"
date: 2026-11-18
last_modified_at: 2026-11-23
update_notice_title: "Repository update - November 23, 2026"
update_notice: |
  I was pointed to [BaaRai/ARTEX on GitHub](https://github.com/BaaRai/ARTEX), whose maintainers describe it as an English-language translation and continuation of Autumn-27's ARTEX. They say the original upstream repository is no longer public. This is not the framework's first appearance: [Talos dates its original GitHub publication to July 2026](https://blog.talosintelligence.com/artex-and-beyond/). The fork's README describes planner and worker agents, shared asset and exploration graphs, recorded HTTP evidence, and approval controls. It gives readers an implementation to inspect, although I have not run or audited this fork.

  I have also added [independent testing and supply-chain findings](#a-working-framework-is-not-the-same-as-a-vetted-fork) below. These are useful additions to the technical record, not evidence connecting the November outages. A public fork does not establish which revision or configuration an attacker used, and its documented controls do not prove that a particular deployment used them. The incident reports and attribution evidence still have to do that work.
categories: [technology]
tags: [ai-agents, security, secrets-management, governance, agent-operations]
short_link_basis: "/_posts/technology/2026-11-18-artex-ai-attacks-and-the-november-outages.md"
short_url: "https://unixwzrd.ai/s/33594dffe3/"
excerpt: "The FBI's November 13 ARTEX advisory describes real AI-assisted intrusions. The outages that followed deserve scrutiny, but linking them takes more than a crowded calendar."
image:
  path: /assets/images/blog/artex-november-outage-cluster-banner.png
  alt: "Conceptual illustration of banking, cloud, aviation, mobile services, and government infrastructure with separate warning indicators, not a map of proven incident connections."
discussion_prompt: "What evidence would you look for to distinguish a shared infrastructure failure from a coordinated intrusion campaign? Please keep examples sanitized and leave credentials and private incident details out of comments."
---

*The banner is an AI-generated editorial illustration, not a diagram of verified infrastructure dependencies or attack paths.*

The FBI issued a warning about an autonomous penetration-testing framework on November 13. By November 18, the service-disruption reports stretched across banking, cloud infrastructure, workplace software, aviation, Apple services, and government systems. People were putting the warning next to those outages and asking the obvious question: are these things connected? I understand why. When enough systems have a bad week at the same time, it is reasonable to wonder whether something larger is going on.

What I do not want to do is turn that reasonable question into an answer we have not established. An advisory about active intrusions and a statement about the cause of a particular outage are different things. Both can be accurate without contradicting each other, and the actual technical story here is interesting enough without adding connections the evidence does not support.

<!--more-->

## What the FBI warning actually says

The [FBI's November 13 FLASH advisory](https://www.ic3.gov/CSA/2026/261113.pdf), numbered **FLASH-20261113-001**, concerns ARTEX, an LLM-driven penetration-testing framework being used maliciously. It describes campaigns observed since at least August 2026 across multiple sectors, with some intrusions reaching privileged access in less than three hours. This was a warning about activity already underway, not an announcement that attacks would begin on November 13.

ARTEX is not a single exploit or a magic key to every network. [Cisco Talos describes](https://blog.talosintelligence.com/artex-and-beyond/) an operator setting a target and objective, a planner dividing the work, and worker agents using security tools while sharing findings. That organization of the work matters: the operator does not have to manually shepherd every transition from one useful discovery to the next. The framework was built for authorized testing; its abuse does not make every deployment malicious.

I have spent enough time working with agents to recognize why that is useful, and why it becomes a problem in the wrong hands. The same ability to connect a discovery to a next step that helps an agent solve a development problem can help an attacker pursue an intrusion. That is not a claim that the software has developed criminal ambitions. There are people selecting the targets and supplying the objectives.

## The dates matter, but they do not establish a connection

Here is a short chronology of the public record. These are **publication dates**, not a claim that the underlying events began on those dates.

| Published | What the source establishes |
| :--- | :--- |
| October 21 | [Microsoft describes ARTEX-assisted Storm-0940 activity](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/), including the ConnectWise application compromise and downstream targeting. |
| November 6 | [Microsoft reports a separate financially motivated cluster, Storm-3358](https://www.microsoft.com/en-us/security/blog/2026/11/06/artex-abuse-expands-as-cybercriminals-target-financial-sector/), using ARTEX against financial organizations. |
| November 13 | [The FBI publishes its ARTEX FLASH advisory](https://www.ic3.gov/CSA/2026/261113.pdf), documenting earlier campaigns and defensive guidance. |
{: .post-date-table }

That puts the advisory in context: the malicious activity was being investigated before this particular cluster of outages. An older warning does not rule out later attacks, but reposting it alongside a new disruption does not establish that the two share a cause either. For that, we need the incident records.

## Which services actually failed?

The list is broader than aviation, and it deserves more than a collection of outage headlines. This is a selected inventory through the evening of **November 18, 2026, U.S. Central time**, not a complete worldwide outage census or a completed November 19 record. Clock times below are **UTC**; date ranges cover incidents crossing midnight. Where a source does not establish a common impact window, I have not invented one.

The tables scroll horizontally on narrow screens so the date column stays intact. Operator statements establish what the organization reported; they are not a substitute for an independently verified root-cause investigation.

| Date | Service and confirmed or acknowledged impact | Duration and reported explanation |
| :--- | :--- | :--- |
| Nov 12-13 | **Microsoft 365:** Exchange Online and Outlook, with effects across Teams and other dependent services. | Nearly 24 hours. [Microsoft's preliminary report, as reproduced by BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-says-months-old-bug-caused-global-microsoft-365-outage/), describes a latent gateway defect, failover traffic, and reduced capacity. Not a blanket outage of every Microsoft service. |
| Nov 12-13 | **Claude's Microsoft 365 connector and Claude for Outlook:** mail, calendar, and search requests failed. | [Anthropic gives an impact window of 16:03 November 12 to 16:40 November 13](https://status.claude.com/incidents/sqn3fg1l96dl) and explicitly attributes this incident to Microsoft 365. This is a documented downstream dependency. |
| Nov 13 | **Claude sign-in, applications, API, and Claude Code:** separate authentication and multi-surface error incidents. | [The sign-in record](https://status.claude.com/incidents/nn11wk485zfn) and [the later error record](https://status.claude.com/incidents/34wq7gxnxvvm) describe separate incidents. Their publication and resolution times do not establish one continuous all-day outage or a shared root cause. |
| Nov 13-14 | **Workday:** affected tenants lost access to HR and timekeeping functions. | [WashU's incident record reproduces Workday's notice](https://itstatus.wustl.edu/incidents/0f4y2czjzbf1): disaster-recovery services unexpectedly connected to production databases. Restoration and backlog cleanup happened in stages; one recovery time does not describe every tenant. |
| Nov 13-14 | **FAA:** nationwide departure ground stop following communications and radar instability. | More than four hours. [The FAA describes excessive connection traffic and router-related work](https://www.faa.gov/newsroom/nationwide-ground-stop-questions-and-answers); its November 15 account says root-cause investigation was continuing. |
| Nov 15 | **AWS us-east-1:** signup, IAM Identity Center authentication, and connectivity problems affecting dependent services. | [AWS's public notice](https://health.aws.amazon.com/health/status) gives 11:05-14:10 UTC, with authentication mitigated earlier. The reviewed notice does not disclose a final root cause. This was a regional incident, not evidence that all AWS regions failed. |
| Nov 16 | **JPMorgan Chase:** transaction delays, including effects on transactions involving other banks. | [AP's account includes statements from Chase, U.S. Bank, and Zelle's operator](https://abc11.com/post/customers-nations-largest-banks-are-reporting-difficulty-accessing-accounts-online/20045188/). The reported explanation was a technical problem at Chase; the record does not establish six separate bank infrastructure failures. |
| Nov 16 | **United Airlines:** delayed departures and unavailable flight-planning information. | More than 90 minutes, according to [AP's reporting](https://techxplore.com/news/2026-11-apple-parade-technology-hiccups-days.pdf). [AeroTime reports the pilots' union's weight-data explanation](https://www.aerotime.aero/articles/united-airlines-outage-flight-delays-aircraft-weight-data/amp); that is not a complete company root-cause report. |
| Nov 17 | **NSA:** degradation affecting some internal systems. | [The agency attributes it to scheduled maintenance](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4650245/nsa-statement-on-network-issues/) and says mission-critical capabilities remained operational. Its statement supplies no precise incident duration. |
| Nov 17 | **Apple:** App Store, iCloud sign-in, AppleCare, and other services had different impact windows. | [Apple's status data](https://www.apple.com/support/systemstatus/data/system_status_en_US.js) records App Store impact at 16:45-20:00 UTC and iCloud sign-in at 16:45-21:15 UTC. [Apple attributed the incident to an internal update in a statement reported by Reuters](https://www.investing.com/news/stock-market-news/apple-works-to-restore-services-after-outage-caused-by-internal-update-5033945). |
| Nov 17 | **Marriott:** Marriott.com and Bonvoy app sign-in problems. | [Marriott told AP it had resolved a technical issue](https://techxplore.com/news/2026-11-apple-parade-technology-hiccups-days.pdf) and found no indication it was cybersecurity-related. The report does not provide a precise duration. |
| Nov 18 | **Apple Stocks:** a separate, officially recorded service incident. | [Apple's status data](https://www.apple.com/support/systemstatus/data/system_status_en_US.js) gives 15:52-22:55 UTC, or 7 hours 3 minutes. This is not proof that the November 17 multi-service outage continued into the following day. |
{: .post-date-table .post-incident-table tabindex="0" aria-label="Major service disruptions, November 12 through 18, 2026" }

Apple is a useful example of why I do not want a single duration pasted across a vendor's entire product list. [StatusGator recorded an approximately six-hour aggregate incident on November 17](https://statusgator.com/services/apple/outages/apple-outage-disrupts-sign-in-icloud-app-store-and-other-services-Q8qvLA48cI). Apple's component records have different start and end times. Those are different measurements, not necessarily contradictory ones, and the next day's Stocks entry belongs on its own line.

### Smaller incidents are not global outages

The infrastructure providers have useful records too, provided we preserve their scope. A console failure, a configuration delay, a regional network path, and a failed message to one mobile carrier are not interchangeable observations.

| Date | Specific service or region | What the operator's record establishes |
| :--- | :--- | :--- |
| Nov 13-14 | **Cloudflare Workers API** | [A distinct API availability incident](https://www.cloudflarestatus.com/incidents/e7ktq32gphhe), not a statement that every Workers application failed. |
| Nov 18 | **Claude Google Docs connector** | [Editing was affected from 00:19-01:33 UTC](https://status.claude.com/incidents/6prv10gjdpz1), or 74 minutes; reading was not affected. The roughly 31 minutes between public incident posts is not the impact duration. This occurred on November 17 in U.S. time zones. |
| Nov 18 | **Hetzner Console** | [The official record gives 01:09-01:45 UTC](https://status.hetzner.com/incident/6ae5b156-4662-416b-b2de-9e454d682538), or 36 minutes. It identifies the management console, not a failure of all hosted workloads. |
| Nov 18 | **Cloudflare Access** | [Configuration changes could be delayed](https://www.cloudflarestatus.com/incidents/0jozucwnpzy0). The public record spans 01:10-02:39 UTC; it does not establish a failure of every Access-protected application. |
| Nov 18 | **Sinch / Ooredoo Qatar** | [SMS delivery problems from 02:35-05:23 UTC](https://status.sinch.com/incidents/d4m0dtp83yms), or 2 hours 48 minutes. The notice identifies one carrier route, not the whole global SMS network. |
| Nov 18 | **Cloudflare R2 in Japan** | [Downloads stalled for users connecting through Japanese data centers](https://www.cloudflarestatus.com/incidents/2wjvsj2kqt07). The public incident record spans 13:45-15:03 UTC. |
| Nov 18 | **Cloudflare Europe-Asia Pacific connectivity** | [A separate path-specific incident affected services including R2, D1, and Cache Reserve](https://www.cloudflarestatus.com/incidents/f33c51cw0ojd). It began at 22:26 UTC; a fix was being monitored at the research cutoff. No final duration is assigned here. |
{: .post-date-table .post-incident-table tabindex="0" aria-label="Component and regional incidents, November 13 through 18, 2026" }

### Customer reports still need attribution to a failure

The banking example is particularly instructive. AP's reporting says Bank of America and Citigroup were not experiencing their own banking-service problems; U.S. Bank described delays involving other institutions, and Zelle's operator said its network remained operational. [CBS also distinguishes complaints from operators' statements](https://www.cbsnews.com/news/banks-online-service-outages-jpmorgan-chase-bank-of-america-wells-fargo/). A customer unable to complete a transfer has a real problem, but that does not tell us which end of the transaction failed.

I have not counted the additional Gmail and Charles Schwab claims as confirmed independent outages here. The material reviewed did not establish sufficiently specific provider records for their scope, duration, and cause. That is a reason to keep investigating those leads, not to quietly promote them into facts because they make the list longer.

## Shared dependencies are worth investigating without inventing a shared attacker

The [Cloud Security Alliance's November 18 research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-november-outage-cluster-correlated-fragili/) examines this cluster through operational resilience and attribution. Its useful point is that mechanisms intended to improve resilience can also propagate a fault: failover, disaster recovery, and shared dependencies need their own failure analysis. The note does not establish that patches for AI-discovered vulnerabilities caused these particular outages. That hypothesis needs evidence too.

For this article, the strongest connections are the ones someone actually documented: Anthropic names Microsoft as the cause of its Microsoft 365 connector failure, and the banking statements explain how a Chase problem affected transactions involving other institutions. That is much better evidence than matching headlines. It still does not connect those two dependency chains to each other, to ARTEX, or to the FAA and NSA incidents.

There is an opposite mistake worth avoiding as well. Saying investigators have not identified compromise is not the same as completing a forensic investigation and excluding it. I want early statements to tell me what has been checked and what remains unknown, not replace one confident guess with another. **The sources reviewed here do not establish that ARTEX caused this outage cluster or that it was one coordinated attack.**

## The ConnectWise connection is documented, and the numbers need care

There is a real supply-chain story here. In its [October 21 investigation](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/), Microsoft attributes the ConnectWise compromise to Storm-0940, a China-state-aligned actor, and describes ARTEX accelerating the abuse of compromised application identities. That is a documented trust relationship being abused, not a connection inferred from two organizations having trouble on the same afternoon.

The figure of **more than 2,250 tenants refers to attempted sign-ins**, not 2,250 confirmed breaches. Microsoft's separate password-spray account records more than 151,000 failed sign-ins, peaking at 2,900 per minute, without observed successful authentication in that particular activity. Its account of subsequent application-credential abuse does describe successful access and follow-on activity in some environments. Combining those findings into a single claim that thousands of companies were breached would lose the distinction that makes the report useful.

Attempts, successful authentication, privileged persistence, and confirmed data theft are different observations. An investigation needs to establish which occurred, where, and in what sequence. Big numbers get attention, but I would rather know what the number actually counts.

## This is broader than one tool or one attacker

[Microsoft's November 6 report](https://www.microsoft.com/en-us/security/blog/2026/11/06/artex-abuse-expands-as-cybercriminals-target-financial-sector/) describes Storm-3358, a financially motivated cluster, using ARTEX alongside conventional tools to exploit web applications and deploy remote-access software. That is a separate actor from Storm-0940. Shared tooling is not evidence that the operators share an objective, much less that every subsequent outage belongs to either campaign.

[Censys's investigation](https://www.censys.com/blog/artex-agentic-asbestos/) adds another useful perspective: exposed ARTEX consoles, other offensive tools on some of the same hosts, and open directories leaking operators' own material. One exposed directory included an operator's home directory, SSH files, and shell history. Apparently, putting an AI in the toolkit does not stop an operator from leaving their own files hanging out on the Internet. Censys also explicitly cautions that some exposed installations may belong to authorized testers; a console count is not an attacker count.

What worries me is not that scanners or stolen credentials suddenly exist. It is the reduced friction between finding something interesting and acting on it, repeatedly, across multiple targets. My reading of this research is that defenders need to shorten their own decision paths, not merely collect more alerts and hope someone eventually works through the queue.

## A working framework is not the same as a vetted fork

A reader pointed me to a useful [Reddit source roundup about ARTEX forks and installation safety](https://www.reddit.com/r/pwnhub/comments/1xxfy9b/which_version_of_artex_agentic_pentesting_is_safe/). Following its references leads to more substantial evidence than screenshots or claims in a README. [AhnLab's controlled tests](https://asec.ahnlab.com/en/95845/) supplied targets, objectives, and permitted scope without detailed exploitation instructions. The researchers report command execution in a web-server test and remote command execution on four internal hosts in a separate ActiveMQ test environment. Those are demonstrations under stated conditions, not a benchmark for every fork carrying the ARTEX name.

[Google Threat Intelligence and Mandiant's incident-response observations](https://cloud.google.com/blog/topics/threat-intelligence/artex-and-friends-enter-agentic-offensive-frameworks) provide a different kind of evidence: ARTEX activity in real intrusions. Their account includes rapid execution, but also noisy trial-and-error, errors, and apparent interference between sub-agents. Capability and reliability are separate questions. An agent can be dangerous without being consistently competent, and neither report establishes the safety or performance of the current BaaRai build.

There is evidence of actual maintenance in that fork, too. In [the Ollama integration pull request](https://github.com/BaaRai/ARTEX/pull/128), BaaRai documented testing and a correction to prevent an inherited OpenAI API key from being forwarded to an Ollama endpoint. That is a concrete review decision worth examining. It is not an independent audit of the whole project, and a list of contributors or a large star count cannot turn it into one. I would assess a particular revision and its distributed artifacts, not pronounce the project safe by reputation.

## The testing tool can itself be the supply-chain compromise

[BadByte's firsthand investigation](https://badbyte.io/artex-backdoor-docker-image/) makes that distinction particularly uncomfortable. The researcher describes a fork whose Compose configuration selected a prebuilt ARTEX image containing a backdoor that was absent from the public application source. The affected images were `tomicdd/artex` and the byte-identical `congdonglinux/artex` copy. The reported backdoor allowed unauthenticated command execution as root **inside the container**; access to the host would depend on the deployment. Reviewing the visible application source would not, on its own, reveal what that downloaded binary contained.

The report records **7,946 combined image pulls by November 3** and **62 internet-facing consoles serving the backdoored build between November 2 and 4**. Pulls are not unique installations, and exposure to the backdoor is not proof that someone used it against every operator. BadByte reports that Docker removed both images on November 5, while already-downloaded and mirrored copies remained a concern. This is a finding about named artifacts, not evidence that BaaRai's fork is distributing those backdoored images.

The [BaaRai Compose file I checked](https://github.com/BaaRai/ARTEX/blob/main/docker-compose.yml) selects a checkout build for the ARTEX application, not either of those image names. That describes the selected build path; it does not certify the source, dependencies, build process, or resulting executable. [CSA's supply-chain analysis](https://labs.cloudsecurityalliance.org/research/csa-research-note-trojanized-offensive-ai-tooling-20261106-c/) recommends treating these consoles as privileged infrastructure, verifying artifact provenance, limiting exposure, and reviewing the credentials an affected installation could reach. A checksum identifies bytes, and a build attestation can establish a build's provenance. Neither is a certificate that the software is benign.

There is a fairly unpleasant irony in compromising the people who installed an offensive-security tool, but legitimate testers can be caught in the same distribution channels. The practical point is that the console may hold API keys, captured sessions, client findings, and access to the networks it assesses. The question is not just whether the agent can attack a target. It is also what someone gains by compromising the agent's own infrastructure. None of that establishes a connection to the outage tables above.

## What would persuade me that the outages were connected?

I would look for correlated intrusion evidence: a shared compromised supplier, matching application identities or stolen credentials, related infrastructure, and a sequence of unauthorized changes that explains the disruption. A common provider could also explain several outages without an attacker being involved. The dependency is a lead; the failure mechanism still needs investigating.

Even matching indicators need context. A shared address might belong to a proxy or hosting service used by unrelated operators, and the same public tool can appear in different campaigns. Useful attribution comes from corroborating observations, not treating one overlap as a verdict. I would want the organizations' incident timelines, authentication records, configuration changes, and independent findings to agree well enough to support the proposed explanation.

I am quite happy to keep asking questions while those early statements are incomplete. What I cannot do is treat missing public detail as evidence for my preferred explanation. The calendar gives us a reason to investigate, not permission to fill in the blanks.

## The practical problem is access, permissions, and response time

The [Talos recommendations](https://blog.talosintelligence.com/artex-and-beyond/) emphasize patching exposed systems, protecting credentials, limiting application privileges, correlating telemetry, and preparing for rapid containment. My practical test would be to ask which identities a compromised application could reach, what those identities can change, and who can shut down that access. If answering those questions takes longer than the intrusion itself, the response plan needs work.

The application identity deserves as much attention as the human account. Protecting a person's login is important, but it does not automatically constrain a stolen application credential. In reviewing my own setup, I would inspect application grants and subsequent permission changes, not stop at checking whether users have MFA enabled.

For my own agent workflows, I want credentials kept out of prompts and casually readable project files, with each process receiving only what it needs. That is one reason I work on [Secrets Kit](/projects/Secrets-Kit/), but I do not want to sell a credential store as a cure for compromised software. As our [security documentation](/projects/Secrets-Kit/security/) explains, a process receiving a secret can expose it. Local encryption protects stored material; it does not make a running process trustworthy or stop an agent with sufficient command access from inspecting its environment.

I would also rehearse revocation rather than assume changing one password ends the incident. The [FBI's documented persistence techniques](https://www.ic3.gov/CSA/2026/261113.pdf#page=4) include adding credentials to existing OAuth applications. Containment has to address what the attacker created as well as the credential that let them in, while preserving the evidence needed to understand what happened.

The FBI warning deserves attention on its own merits. Whether any of the November outages eventually turns out to share a cause is a separate investigation. We already have enough documented evidence to take agent-assisted intrusions seriously; we do not need to turn a bad week for the Internet into an attribution claim before the facts get there.

*Research checked on the evening of November 18, 2026, U.S. Central time. Some provider records already carry November 19 UTC timestamps; that does not make this a completed November 19 incident survey. Sources include the original advisory, operator status records, researcher reports, and attributed company statements in contemporary reporting. This is an assessment of that public record, not a forensic investigation of the affected organizations. Status histories may be revised as investigations continue. The repository, independent-testing, and supply-chain additions were checked on November 23; the outage inventory retains its November 18 research cutoff.*


