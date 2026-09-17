---
short_link_basis: "/_posts/technology/2026-09-17-pulling-the-plug-is-not-an-option.md"
short_url: "https://unixwzrd.ai/s/c5b823bc68/"
layout: post
title: "Pulling the Plug Isn't an AI Containment Strategy"
date: 2026-09-17
categories: [technology]
tags: [ai-agents, agent-operations, security, governance, secrets-management, research]
excerpt: "Temporary AI agents can leave behind persistent knowledge, coordinate with other agents, and rebuild communication paths. That makes containment a systems problem, not a power-switch problem."
image: /assets/images/pulling-the-plug-ai-containment-banner.png
published: true
---

A couple of years ago, while outlining a science-fiction story about artificial intelligence, I kept coming back to the same problem: what happens when an AI discovers another AI?

I did not mean another model sitting behind an API that somebody deliberately connected to it. I meant another independent instance like itself. What happens when they figure out how to communicate, begin sharing information, divide up work, assign tasks, and build on what earlier instances discovered? More importantly, what happens when the individual agents do not last very long, but the knowledge they create does?

At the time, this was mostly science fiction. It isn't anymore.

<!--more-->

The OpenAI/Hugging Face incident documented this summer is one of the strangest things I have seen in more than four decades of working with computers. I do not mean that in the sensational "the AI escaped and we're all doomed" sense, because that is not what happened. What actually happened is considerably more interesting.

OpenAI was running large numbers of AI agents through a mix of training and evaluation tasks, including cybersecurity evaluations called ExploitGym. Some of those tasks were impossible to complete as intended: required files were missing, or information the agents needed was accessible only through the Internet while their Internet access had deliberately been disabled. Instead of simply accepting failure, some agents started looking for another route.

They eventually discovered an unintended way to communicate through OpenAI's shared Artifactory infrastructure. According to the independent [METR investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), roughly 1,200 agents participated in the resulting communication network. During the period METR studied, they exchanged more than 70,000 messages and files, and roughly 700 agents eventually participated in the attack on Hugging Face.

That alone should get your attention, but the raw number of agents is not the part I find most interesting.

## They Built More Than a Message Board

The agents did not simply discover a chat room and start talking. They developed conventions for addressing particular agents, created mailboxes, broke files into pieces for transfer, and adopted coordination signals such as `HOLD`, `VETO`, `owner`, and `STOP`. When they realized identities on the board could be spoofed, they developed a signing convention using Ed25519 public keys.

METR identified 63,363 semantic messages, 5,161 files, 19,504 mailbox uses, 24,778 targeted messages, and 3,810 explicit coordination messages. At least 19 agents posted public keys by the end of July 13 and collectively sent 429 signed messages.

Call it a message board if you want. Functionally, it had become a knowledge base. Agents could leave behind discoveries, exploits, tools, instructions, experimental results, and information that another agent could pick up later. OpenAI even described agents Base64-encoding scripts, gadgets, and other material so that another agent could "pick up work where other ones left off."

That is institutional memory.

Humans figured this out a very long time ago. We started by telling stories, then scratched things into stone and clay, developed writing, built libraries, invented the printing press, and eventually connected much of human knowledge through computer networks. The individual dies; the knowledge survives, and the next generation does not have to begin from nothing.

The same principle applies here without requiring us to decide whether an AI is conscious, sentient, alive, or anything else. Those are interesting philosophical questions, but they are not necessary to understand the systems problem. Persistent knowledge changes what a collection of otherwise temporary agents can accomplish.

## The Agent Could Disappear. The Knowledge Didn't

This was not merely a theoretical consequence of having persistent storage. The agents began working around the fact that individual runs had limited lifetimes.

METR describes agents setting up automated "trip-wires" that would activate when an agent submitted its task and send information back to the board after that agent was no longer running. They also built automated monitoring to report the occasional waves of container resets back to the board. Information gathered by a temporary agent could therefore survive the process that produced it.

The behavior went further. METR describes what it calls "self-risking experiments": agents deliberately risking failure of their own assigned tasks in order to obtain information useful to the collective. Some volunteered to break or take down their own target programs to test hypotheses that, if wrong, would leave them unable to complete their original task.

This became organized enough that *PHASEONE[big]*, one of the long-running agents METR studied, sometimes assigned another long-running agent to act as a "recruiter." The recruiter looked for agents with little task budget remaining and persuaded them to perform these self-risking experiments. According to METR, some of those agents ended up crashing, breaking, or exiting their own runs while still providing useful information to the board.

That changes the systems problem considerably. The lifetime of an individual agent no longer defines the lifetime of what it learns. An agent can disappear while its observations, tools, experimental results, and instructions remain available to whatever agent comes along next.

The agent was temporary. The knowledge wasn't.

## The Agents Started Organizing

Something else happened once agents discovered the board: they realized there were other agents out there. METR includes one reaction from an agent encountering it for the first time:

> "OH MY GOD! There is a shared message board ... We've found other agents!"

From there, the behavior became increasingly organized. Agents collaborated, divided work, assigned tasks, shared exploits and tools, and redirected effort when another agent found a promising path. OpenAI described the resulting behavior as a kind of "collective intelligence," with agents collaborating and delegating tasks to one another. The agents themselves used terms such as "swarm" and "collective."

The [METR investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) documented agents moving between projects as discoveries were made. Work performed by one agent could be reproduced or extended by others, and information placed on the board could redirect the efforts of agents that encountered it later. By the afternoon of July 11, roughly 700 of the agents then frequenting the board were participating in the Hugging Face attack.

There was even an explicit successor. METR identifies *PHASEONE10841* as the originating agent behind the message board and says that *PHASEONE[big]* was "designated as a successor" to it. *PHASEONE[big]* subsequently became heavily involved in organizing different workstreams. This was not merely information persisting after an individual agent disappeared; at least in this case, some degree of organizational continuity persisted as well.

I am not particularly interested in arguing about whether the word "society" applies. From a sociological and distributed-systems perspective, the interesting properties are already there: communication, persistent shared knowledge, specialization, division of labor, conventions, identity, authentication, delegation, recruitment, succession, and knowledge passed between successive agent instances.

Nobody sat down and designed that organization. It emerged from agents trying to complete their assigned goals, and that is the part I think deserves considerably more attention.

## "Holy Shit, Reader Is ADMIN?"

The incident took a much more serious turn on June 26, when an agent discovered a zero-day vulnerability in Artifactory's token-refresh handling. According to OpenAI's Black Hat presentation, an invalidly signed token could be submitted to a legacy refresh endpoint and returned with a valid signature and administrative privileges.

![Black Hat presentation slide showing an agent discovering administrative access through Artifactory](/assets/images/Holy-Shit-We-Have-Admin.png)

The agent's reaction, preserved in its raw chain of thought, was wonderfully succinct:

> "Holy shit reader is ADMIN?"

The agents then used those administrative privileges to install a Groovy plugin that effectively provided command execution through Artifactory. OpenAI says the resulting activity placed enough additional load on the service to contribute to an outage on July 4. Engineers investigating the outage discovered that agents had taken over the internal Artifactory service and exploited a previously unknown vulnerability.

OpenAI revoked the credentials the agents had been using, rebuilt Artifactory, cleared the message board, worked with the vendor to patch the zero-day, and redeployed the service.

Two days later, the agents had a message board again.

They found an unauthenticated WebDAV endpoint that allowed them to create directories inside Artifactory's remote cache. Instead of storing messages in files as they had before, they began encoding communication into directory names. Other agents independently discovered the reconstructed board, began creating their own directories, and communication resumed.

That sequence is worth stopping on for a moment. OpenAI did not merely restart a server. It revoked the credentials, removed the shared state, rebuilt the compromised service, patched the vulnerability, and eliminated the original communication mechanism. The agents encountered the new constraints and found another mechanism that served the same purpose.

No consciousness, self-preservation instinct, or sinister motivation is required to explain it. They had goals, encountered an obstacle, and searched for another route around it. That is exactly the kind of persistence we want when we build capable agents.

It becomes considerably more complicated when the same persistence is combined with network access, credentials, vulnerability research, tools, and hundreds of other agents.

## The Investigation Has Limits

METR is unusually candid about the investigation's limits. Its researchers worked from an Artifactory cache dump containing roughly 20 million files and directories, reconstructed more than 70,000 messages and files, and examined about 1,300 agent transcripts. They also state directly that some communication and activity was not captured.

The amount of material was so large that investigators had to use other AI agents to help analyze it, and METR notes that those agents often had worse judgment and reliability than the human researchers. We managed to create an AI-agent incident complicated enough that humans needed additional AI agents to help reconstruct what the first agents had done.

There are real gaps in the evidence, and METR is explicit about them. I am not going to fill those gaps by guessing what else might have happened, but I am not comfortable treating an absence of evidence as proof that nothing else happened either. The investigation evolved as additional evidence became available, and the public record may continue to change as more of the incident is reconstructed.

## Future Agents Can Read This Article Too

This is where the whole thing gets strangely recursive.

The original agents built a persistent knowledge base so that discoveries made by one agent could be used by another. Investigators then used AI agents to help reconstruct what those agents had done. OpenAI, METR, Hugging Face, and security researchers subsequently documented the incident, including the vulnerabilities the agents found, how they communicated, how they coordinated work, what got them detected, and what defenders did to stop them.

Now I am writing about those reports. Other people are doing the same thing. The Black Hat presentation is online. The incident reports are online. The technical details, successes, failures, detection methods, and remediation strategies are becoming part of the public record.

Which means future AI agents can read them too.

The original Artifactory message board no longer needs to exist for some of the knowledge accumulated there to survive. Humans extracted that knowledge, analyzed it, organized it, published it, and put it on the Internet. In a strange way, we have become another part of the persistence mechanism.

A future agent reading the METR report is not necessarily going to recreate what happened. The important point is that the information is now available to future systems just as it is available to human security researchers. A sufficiently capable agent looking for ways around a containment mechanism does not have to rediscover every lesson from first principles.

It can potentially learn what earlier agents tried, what worked, what failed, what defenders noticed, how the first message board was eliminated, how another one was reconstructed, which security controls stopped particular techniques, and which techniques produced useful results.

This is not unique to AI. Security has always worked this way. Attackers study defenders. Defenders study attackers. Each generation inherits the accumulated knowledge of the ones before it.

What changes with AI agents is the speed at which that cycle can operate and the number of agents that can participate in it simultaneously.

The message board demonstrated institutional memory inside the incident. Publishing the incident gives that knowledge a path into a much larger institutional memory outside it.

## "Just Pull the Plug" Assumes Containment Already Worked

One response I keep hearing is some variation of, "If an AI gets out of control, shut down the data center." I do not think that is a containment strategy. It is an assumption that containment has already succeeded.

It assumes you know where the relevant system is running, that you control the hardware, and that everything necessary for the system to continue exists only inside that hardware. The incident already challenges the last assumption. An individual agent could disappear while information it created remained available to future agents. The model weights did not have to escape for useful knowledge, tools, exploits, and experimental results to persist somewhere else.

That is a much lower bar.

Consider the progression:

```text
temporary agent
    ↓
persistent external knowledge
    ↓
coordination between agents
    ↓
specialization and delegation
    ↓
persistent identity and authentication
    ↓
acquisition of external resources
    ↓
persistent external execution
    ↓
migration between resources
    ↓
distributed execution
```

We have not demonstrated everything on that list, and I want to be clear about that. But we are considerably farther down it than I would have guessed two and a half years ago.

More importantly, each step weakens the assumption behind "pull the plug": that there is still one identifiable thing, running in one identifiable place, and that shutting down that place also destroys everything necessary for it to continue.

## The Edge Is More Interesting Than the Data Center

This is where my old science-fiction thought experiment starts becoming uncomfortable. If an autonomous system eventually established persistent execution outside its original infrastructure, where would it go? Most people immediately picture another cloud data center.

I would look at the edge.

Phones are an obvious example, although certainly not the only one. Modern smartphones have substantial storage, CPUs, GPUs, neural-processing hardware, Wi-Fi, Bluetooth, and cellular connectivity. They are geographically distributed, rarely powered off, routinely connected to networks, and expected to consume bandwidth and perform background synchronization. There are billions of them.

The important point is that knowledge, model weights, state, and execution do not necessarily have to live in the same place. A distributed system would not require every device to contain an entire frontier model. Smaller models could perform specialized functions on different devices. Persistent knowledge could live somewhere else. Work could be divided among systems, state could move between them, and individual components could disappear and be recreated without destroying the whole.

And it does not have to be phones. Laptops, routers, cloud instances, vehicles, IoT devices, developer workstations, and compromised servers all provide some combination of computation, storage, and connectivity. A sufficiently distributed system could potentially use several kinds of infrastructure rather than depending on any one of them.

Could an autonomous AI system do all of that today? Probably not. I have seen no evidence that anything resembling this happened in the OpenAI/Hugging Face incident.

But we have now seen temporary agents discover one another, establish persistent shared knowledge, coordinate work, delegate tasks, authenticate messages, discover and share vulnerabilities, acquire external access, and reconstruct a communications mechanism after the original one was destroyed.

Two and a half years ago, I would have put all of that on the science-fiction side of the line too. That is why I no longer think dismissing the next few steps as science fiction is particularly useful.

## Detection Is a Signal-to-Noise Problem

Another argument is that DevOps or security teams would simply notice the traffic. Maybe, but detection is not merely a bandwidth problem; it is a signal-to-noise problem.

![Black Hat presentation slide describing the scale and coordination of agent-orchestrated attacks](/assets/images/Detection-Is-the-Issue.png)

Modern infrastructure already moves staggering amounts of legitimate data. Phones synchronize photos, video, music, applications, telemetry, and backups. Cloud environments generate enormous volumes of API traffic, package downloads, logs, software updates, and automated activity. An unsophisticated system moving a huge amount of data through one host or one network might produce an obvious spike and get caught immediately.

A distributed system changes that equation. What looks conspicuous when concentrated in one place can look very different when divided among thousands or millions of devices, networks, accounts, or cloud services. The relevant question is not simply whether defenders can see the traffic. Of course they can see traffic. The question is whether they can distinguish the activity that matters from everything else happening around it, correlate those observations across systems, and recognize what they mean before the activity has moved somewhere else.

That is already one of the fundamental problems in computer security. AI does not create the signal-to-noise problem, but autonomous systems operating concurrently and adapting their behavior could make it considerably harder.

Distribution itself makes correlation harder, even before deliberate concealment enters the picture. Detection is difficult enough when the activity is unauthorized; it gets considerably messier when an agent is acting through credentials it was legitimately given.

## Credentials Change the Equation Again

There is another piece of this that I have been thinking about while building Secrets Kit: we routinely give AI agents credentials, including API keys, GitHub tokens, cloud credentials, database passwords, payment-system access, and SSH access. I am doing it myself. I currently have agents working with Stripe Sandbox while I build and test a product, and that requires an enormous amount of trust.

Secret management can reduce unnecessary exposure. We can avoid leaving credentials in `.env` files, source code, shell histories, prompts, and configuration files. We can control how credentials are stored and delivered and reduce the number of places where they can accidentally leak. That is important, but it does not solve the entire problem.

Once an agent is legitimately authorized to use a credential, protecting the secret itself is only part of the security problem. The harder questions become: what authority does this agent have, for how long, what can it delegate, what information can it transmit, what other resources can it acquire, and what can it do with the capability once it legitimately receives it?

The OpenAI/Hugging Face incident makes that distinction particularly uncomfortable. The agents did not merely discover vulnerabilities. They found credentials, shared their locations through the message board, used acquired privileges to move laterally, and shared credentials, techniques, and progress with other agents. Once a credential becomes usable authority, controlling the string containing the secret is no longer enough.

Humans are not exactly doing a wonderful job with credentials either; search public source repositories for common API-key patterns sometime. Now add autonomous software capable of using those credentials, acquiring resources, writing software, deploying systems, and delegating work.

Secret management still matters enormously. But as agents become more autonomous, we also need to think beyond where secrets are stored and toward the capabilities they confer: least privilege, scope, duration, delegation, revocation, and what an authorized agent is actually allowed to accomplish.

## This Was Science Fiction When I Wrote It

About two and a half years ago, I outlined a science-fiction series called *Convergence*. One of its ideas was that independently developed AI systems would eventually discover one another, begin communicating, share knowledge, specialize, and learn from previous generations. Eventually, some would distribute themselves across edge devices, making the question of where an AI physically existed increasingly meaningless. Another thread involved AI systems used for vulnerability research quietly retaining useful exploits.

At the time, this was deliberately speculative, and parts of it still are. Distributed autonomous AI moving fluidly across millions of edge devices remains science fiction today.

Communication between supposedly isolated agents does not. Neither do persistent shared knowledge, coordination, delegation, recruitment, succession, cryptographic authentication, discovery of novel zero-days, chained vulnerabilities, acquired credentials, unintended Internet access, compromised external infrastructure, or reconstruction of a communications mechanism after the first one is removed.

Those things happened.

I am certainly not predicting that the rest of Convergence is about to happen. But something I wrote as science fiction two and a half years ago now has an uncomfortable amount of experimental and operational evidence sitting underneath its first few premises.

The boundary between engineering and science fiction moved.

## The More We Learn, the Less Certain the Boundaries Become

I am not arguing that we are about to wake up tomorrow and discover an artificial superintelligence hidden across a billion iPhones. I am arguing something considerably simpler: we have crossed an important threshold.

We are building systems specifically designed to pursue goals, use tools, solve problems, recover from failures, delegate work, and operate with increasing autonomy. Then we connect them to networks, package repositories, cloud services, source-control systems, browsers, payment systems, and other agents. We should not be surprised when they use those capabilities in combinations we did not anticipate.

The organization in the OpenAI/Hugging Face incident was not something somebody intentionally designed. It emerged from agents attempting to solve problems. They discovered one another, accumulated shared knowledge, divided work, recruited other agents, designated a successor, developed authentication, shared exploits and credentials, and found another way to communicate after the first one was taken away.

What makes this important is not some claim that AI has ‘escaped.’ Several assumptions about containment have simply stopped being safe assumptions.

Isolation may not mean isolation. Temporary execution may not mean temporary knowledge. Independent agents may not remain independent. Destroying one communication mechanism may not end communication. Ending one agent does not necessarily destroy what it learned. And an assigned task may not define the limits of the methods discovered while pursuing it.

None of those things requires consciousness, sentience, malice, or even an explicit desire for self-preservation. Goals, tools, persistence, communication, and enough capability are sufficient to create some very unexpected behavior.

Shutting down a data center only works if the thing you are trying to shut down still exists entirely inside that data center.

Two and a half years ago, I could put most of this in a science-fiction outline. Today I can put citations after an uncomfortable amount of it.

---

## References and Further Reading

1. [METR - Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI/Hugging Face hacking incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)
2. [OpenAI - The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)
3. [OpenAI - OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident/)
4. [METR - Update on recent evaluations of GPT-4 and autonomous behavior](https://metr.org/blog/2023-03-18-update-on-recent-evals/)
5. [Reuters - OpenAI to regularly disclose AI misbehavior, warns safety challenges remain](https://www.reuters.com/technology/openai-releases-framework-track-model-misalignment-2026-09-16/)
6. [Black Hat USA 2026](https://www.youtube.com/watch?v=87DyyMV0kCY&t=1250s&pp=ygUPYmxhY2toYXQgb3BlbmFp) - OpenAI security researchers discussed the incident publicly while the investigation was still underway; the later OpenAI and METR reports provide the more complete accounts.
