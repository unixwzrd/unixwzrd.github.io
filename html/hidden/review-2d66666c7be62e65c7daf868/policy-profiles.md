---
layout: review
title: "Configuring Domain Policy Profiles"
permalink: /hidden/review-2d66666c7be62e65c7daf868/policy-profiles/
unlisted: true
search_exclude: true
sitemap: false
list_exclude: true
short_link: false
review_index: /hidden/review-2d66666c7be62e65c7daf868/
review_date: "2026-10-21"
review_note: "Peer-review snapshot. Links between the five included documents are retained; internal supporting references outside the packet are omitted. Example identifiers are generalized where needed. Each document retains its own design and qualification status."
---

# Configuring Domain Policy Profiles

**Status:** October 21, 2026. Configuration design guide, not an installed profile loader or regulatory certification. The small Python example below uses existing core types at `2d1502b`; the declarative manifest and administrative workflow are proposed and must not be represented as working CLI/configuration syntax. No live data, grants or services are changed.

Start with [worked domain profiles](#worked-domain-profiles) for terminology, [people-agents-and-conversations](#people-agents-and-conversations) for grants, and [classifying-external-documents](#classifying-external-documents) for Markdown, Office files, other media and URLs. These are synthetic configuration examples, not new installed domain evaluators. The separately qualified H1/H2 metadata APIs are described under [current capability](#current-capability-versus-proposed-configuration).

## One Model, Different Vocabularies

The engine evaluates ordered sensitivity, authenticated principals, compartments/need-to-know, audiences, purpose, action, destination and current authority. A profile gives those generic dimensions domain-specific names and reviewed constraints. Neither an administrator display label nor an end-user label changes the underlying identity or enforcement rule.

| Generic dimension | Government-inspired display | Healthcare display | Legal-practice display | Personal display |
| --- | --- | --- | --- | --- |
| Record sensitivity | Classification | Information sensitivity | Confidentiality category | Privacy level |
| Principal/context ceiling | Organizational clearance | Authorized sensitivity level | Authorized confidentiality level | Access level |
| Compartment/read-in | Project compartment | Patient/care-team scope | Client/matter and ethical-wall scope | Person/project scope |
| Purpose | Authorized mission/use | Approved care/payment/operations use | Authorized representation/matter use | Approved task |
| Recipient controls | Dissemination/release | Approved recipients/providers | Client/team/vendor disclosure controls | Allowed people/services |

These are presentation examples. A professional role, privilege status, HIPAA applicability or patient consent is not merely another name for a scalar level. Represent the actual applicable constraints separately. The [canonical domain mapping](/hidden/review-12caba0b6046f6338c842cd2/#regulatory-and-professional-overlays) cites the primary sources and limitations. An organization can select different vocabulary without changing the core engine, but it cannot make an unsupported regulatory rule work by renaming a field.

### Reading The Access Decision

Think of sensitivity as one gate, not a master key. The following diagram describes the proposed decision boundary, not an installed end-to-end authorization frontend. Inputs to the gates are trusted identity/policy metadata; restricted document contents must not be fetched to decide whether the reader qualifies.

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/profiles-01.svg" alt="Reading The Access Decision - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart TD
    R["Authenticated audience and current source policy"] --> L{"Every participant meets<br/>the required sensitivity level?"}
    L -->|No or unknown| D["Refuse without restricted content"]
    L -->|Yes| S{"Every participant has<br/>all required scopes?"}
    S -->|No or unknown| D
    S -->|Yes| P{"Purpose, action, recipient, provider<br/>and current authority all permitted?"}
    P -->|No or unknown| D
    P -->|Yes| A["Authorized candidate retrieval<br/>and separately rechecked use"]
```

</details>

**Read downward through the gates, not sideways between compartments.** Higher eligibility can satisfy a lower classification requirement, but it supplies no missing project authorization, need-to-know, purpose or recipient permission. Passing candidate admission is not a permanent evidence lease; expansion, prompt assembly and delivery still use the current decision.

## Worked Domain Profiles

There are two sides to every example: **document control** describes the information and its handling restrictions; **entity access control** describes what an authenticated person or agent may do. The conversation and destination supply additional constraints. A label on a document is not a grant to a reader, and a high access ceiling is not permission to read every document below it. Profile registration itself creates neither permission nor a public-release decision.

### Government And Government Contractors

For a U.S. national-security vocabulary, the order is Unclassified, Confidential, Secret, Top Secret. Only the last three are classified levels. An organization may use the names in an explicitly organizational analogue, but cannot turn that analogue into an official designation or personnel clearance. [Executive Order 13526, sections 1.2 and 4.1](https://www.archives.gov/isoo/policy-documents/cnsi-eo.html) establishes the classified levels and the eligibility, nondisclosure and need-to-know access conditions.

| Document terminology | Document control | Human access terminology | Additional access restriction |
| --- | --- | --- | --- |
| Unclassified | No national-security classification; other controls may apply | Authorized access, not a classified clearance requirement solely because it is unclassified | Ownership, purpose, CUI or other applicable handling, and release permission |
| Confidential | Preserve an authoritative Confidential designation, or clearly identify an organizational analogue | Current eligibility at the required level | Need-to-know and all other applicable access conditions |
| Secret | Same distinction for Secret | Current Secret-or-higher eligibility | Required project/program access; higher eligibility alone is insufficient |
| Top Secret | Same distinction for Top Secret | Current Top Secret eligibility | Specific need-to-know and any additional applicable access controls |

**SCI and compartments are not higher rungs.** A classification level and an SCI control/access authorization are separate dimensions; do not invent `SCI` as a tier above Top Secret. Record the applicable control-system/compartment identity and explicit access authorization separately. [ODNI ICD 703, definition D.2](https://www.dni.gov/files/documents/ICD/ICD-703.pdf) describes the formal intelligence access-control framework. An ordinary project compartment in this software is not automatically an SCI compartment or an official read-in.

#### Public Trust, Credentials And Classified Access

**Public Trust is not equivalent to Confidential and is not a security-clearance level.** It concerns the risk and suitability/fitness requirements of a position, not an information-classification rank. Credentialing, suitability/fitness and national-security determinations are distinct purposes of vetting; see [OPM's explanation](https://www.opm.gov/frequently-asked-questions/suitability-executive-agent-faq/suitability-adjudications/why-are-you-going-to-investigate-me/) and [position-designation guidance](https://www.opm.gov/suitability/suitability-executive-agent/position-designation-tool/). A favorable Public Trust determination by itself grants no Confidential, Secret or Top Secret access. Conversely, a classified clearance does not grant every unclassified business-system entitlement.

A Public Trust position can involve sensitive unclassified information and separately authorized application/data access. That information can require substantial protection without being national-security-classified. A company's lowercase "confidential" business label must not be mistaken for the government's Confidential classification or an entitlement supplied by Public Trust.

| Item | What it establishes or records | What it does not establish |
| --- | --- | --- |
| Identity credential / authenticated session | Who the requester is, under the admitted identity-assurance contract | Permission to read every resource after login |
| Position risk and favorable suitability/fitness determination | Whether the individual meets the applicable employment/position trust requirements | A national-security clearance, classification level or blanket application access |
| Classified-access eligibility | The individual's current adjudicated eligibility at the relevant level | A present need-to-know for every document at that level |
| SCI eligibility and specific access authorization | The applicable personnel eligibility and actual authorized access/read-in under the formal control system | Access to all SCI compartments or every intelligence project |
| Document classification and handling controls | What the information requires of readers, uses and processing environments | That a particular requester meets those requirements |

In the proposed generic model, these are independent trusted attestations/requirements, not synonyms in the ordered `levels` array. Public Trust must not be inserted as a rung below Confidential or used to infer a classified ceiling. The software records accepted references to determinations; it neither conducts official vetting nor issues clearances, credentials or SCI read-ins.

#### Worked TS/SCI Access Example

The shorthand **TS/SCI** combines different concepts: Top Secret eligibility and SCI-related eligibility/access. It is not one permission to every Top Secret intelligence record. [ICD 704](https://www.dni.gov/files/documents/ICD/ICD-704-Personnel-Security-Standards-and-Procedures-for-Access-to-SCI-2018-06-20.pdf) addresses personnel eligibility; [ICD 703](https://www.dni.gov/files/documents/ICD/ICD-703.pdf) addresses protection, need-to-know and controlled access. Resolve current eligibility and actual authorizations from the appropriate trusted authority; a resume or account label saying TS/SCI is not that evidence.

Assume a fictional document requires Top Secret eligibility, SCI authorization for `EXAMPLE-A`, a current mission need-to-know and an approved processing/delivery environment. `EXAMPLE-A` and `EXAMPLE-B` are explanation-only placeholders, not real control-system names, authorized markings or a ready-to-use policy. Assume all other necessary agreements/conditions are satisfied unless the row says otherwise:

| Requester | Current eligibility and specific authorization | Access to this document |
| --- | --- | --- |
| Elena | Top Secret, SCI eligible, authorized/read in for EXAMPLE-A, current mission need | Eligible only through the approved environment and recipient route |
| Ravi | Top Secret, SCI eligible, authorized for EXAMPLE-B but not EXAMPLE-A | Denied: the required authorization is missing |
| Morgan | Top Secret eligibility but no required SCI eligibility/access | Denied: the Top Secret ceiling alone is insufficient |
| Casey | Favorable Public Trust determination only | Denied: it supplies neither the classified eligibility nor the SCI access |
| Elena after reassignment | Still Top Secret/SCI eligible, but EXAMPLE-A access or the mission need has ended | Denied: old eligibility/access history does not preserve a current entitlement |

Even Elena's valid access cannot authorize Ravi to see the document in their shared conversation. The complete recipient set must qualify before the information reaches retrieval, model context or delivery. Similarly, Elena cannot send it to an ordinary local model or external API merely because she can read it herself. Personnel access and system/provider approval are separate gates; an agent service identity is not a cleared human.

Being assigned to a project and being admitted to a formal SCI control system are not interchangeable. The model may need both a project/mission scope and a specific control-system/compartment authorization. "Read-in" records the applicable formal access/indoctrination process, not simply adding a project tag. These software examples do not provision that real-world process or make an unapproved deployment suitable for classified information.

**CUI is also separate from rank.** Use its authoritative category and safeguarding/dissemination requirements when applicable, not a new level between Unclassified and Confidential. A contractor's own sensitive material is not automatically government CUI. [NARA's CUI glossary](https://www.archives.gov/cui/registry/cui-glossary.html) distinguishes the governmental applicability and handling framework.

For classified contract work, the applicable DD Form 254, Security Classification Guide and authorized source documents determine the required designations and instructions; a model does not invent them. DCSA's [derivative-classification job aid](https://www.cdse.edu/Portals/124/Documents/jobaids/information/DerivativeClassification.pdf) explains that relationship. Entity/facility eligibility, personnel access and the approved processing environment are separate matters, not profile settings that this toolkit can issue. See the [DCSA facility-clearance guidance](https://www.dcsa.mil/FCL/). A government contractor may therefore need separate corporate, CUI and classified-handling domains; do not flatten them into one corporate sensitivity ladder.

**Synthetic organizational example:** an engineering report has rank `secret` in `organizational-us-inspired/v1` and compartment `program:orion`. An analyst with the appropriate ceiling but only `program:lyra` is denied. An analyst authorized for Orion still needs the permitted purpose, recipients and processing route. These names demonstrate need-to-know, not a claim that Mnemosyne or a local LLM is approved for actual classified work. An agent's configured processing ceiling is not a government personnel clearance.

### Healthcare

Use familiar terms such as **information sensitivity**, **workforce access authorization**, **patient/care-team scope**, **permitted use or disclosure**, and **approved service account**. HIPAA does not prescribe a Confidential/Secret/Top Secret clearance ladder. The following ordered sensitivity tiers are a clinic's example policy, not HIPAA classifications:

| Example sensitivity tier | Example information | Who might be authorized, subject to the independent controls |
| --- | --- | --- |
| General | Approved published patient-education material | Intended public recipients after release approval |
| Internal | Operational material without patient-specific content, subject to its actual other restrictions | Approved workforce roles and internal service accounts |
| Confidential | A covered patient encounter or billing record | Authorized roles for the specific patient/data scope and permitted use |
| Restricted | Material the organization subjects to additional handling rules | Specifically authorized recipients after those rules are satisfied |

PHI/ePHI applicability is a separate attribute, not a synonym for the Confidential tier. Some records need specific additional treatment: separately maintained psychotherapy notes are a useful example, not a blanket label for all mental-health records. [HHS explains their special authorization protections and exceptions](https://www.hhs.gov/hipaa/for-professionals/faq/does-hipaa-provide-extra-protections-mental-health-information-compared-other-health.html). Purpose, authorization/other permitted basis, recipients and any applicable special rules must be resolved independently of rank.

**Example:** a billing specialist and billing agent may receive approved billing fields for synthetic patient `patient:001`, for billing, through an approved processing route. That does not grant access to the patient's entire clinical record or every patient. A physician's role is not universal patient access either. Apply the actual purpose-specific policy; the [HHS minimum-necessary guidance](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html) expressly has exceptions, including specified treatment disclosures/requests. A patient's own access rights are a separate workflow, not a workforce-role grant. Administrative access controls are described in the [HHS Security Rule summary](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html).

#### Healthcare Analogy: Role Plus Patient And Handling Scope

The functional parallel to compartmented access is **authorized role plus specific patient/data/purpose scope**, not a healthcare version of SCI clearance. A medical license, clinical privileges or employment credential does not itself authorize every electronic record. Assume the following clinic has explicitly approved these role/assignment rules and resolved the applicable legal basis and any exceptions:

| Requester | Approved scope | Example result |
| --- | --- | --- |
| Care-team clinician | Treatment access for patient 001 | May use the permitted patient-001 clinical material through the approved route |
| Equally qualified clinician outside that scope | Patient 002 only, with no authorized cross-cover/other access basis for 001 | Denied patient-001 access under this example policy; the same professional qualification is not the missing assignment |
| Billing specialist/agent | Patient-001 billing fields for billing | No automatic access to the full clinical narrative or an unrelated patient's records |

An additional handling rule can still restrict a care-team member. For example, where disclosure of separately maintained psychotherapy notes requires patient authorization and no applicable exception permits it, ordinary treatment-record access is not enough. [HHS's psychotherapy-note guidance](https://www.hhs.gov/hipaa/for-professionals/faq/does-hipaa-provide-extra-protections-mental-health-information-compared-other-health.html) explains those protections and exceptions. Do not generalize this to all mental-health information or require patient authorization for every treatment disclosure. Unknown required evidence means refusal, not an invented clinical emergency override.

### Legal Practice

Use **client confidentiality**, **authorized matter team**, **matter access**, **ethical wall/screen**, **permitted disclosure**, and **approved vendor/service account**. There is no universal ABA clearance ladder. A firm can define tiers like these while keeping substantive legal restrictions separate:

| Example confidentiality tier | Example information | Additional control |
| --- | --- | --- |
| Public | An approved published article or filing actually authorized for public release | Verify that the particular version is public; related drafts/annotations need not be |
| Firm Internal | An ordinary internal procedure | Approved internal audience and any applicable personnel/business restrictions |
| Client Confidential | Information relating to a client representation | Authorized client/matter, purpose and recipients |
| Restricted Matter | Tightly limited strategy or material under additional restrictions | Explicit team/read-in, exclusions and any applicable order or handling rule |

Attorney-client privilege, work product, a protective order and an attorneys'-eyes-only restriction are not interchangeable rank labels. Record reviewed status and controlling authority separately. Confidentiality is broader than merely a document marked privileged; see [ABA Model Rule 1.6](https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/). Screening/conflict obligations require their actual procedures, not just a compartment flag; [Model Rule 1.10](https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_10_imputation_of_conflicts_of_interest_general_rule/) supplies one relevant model-rule framework. The controlling jurisdiction, client instructions and matter-specific orders govern the real configuration.

**Example:** a lawyer and research agent admitted to `matter:001` may use its authorized material for representation through an approved service. Neither can retrieve `matter:002` merely because their confidentiality ceiling is high enough. A client-visible handout and firm-internal strategy can concern the same matter but have different audiences. An agent is an authorized processing identity, not a licensed attorney or an automatic member of every lawyer's matter team.

#### Legal Analogy: Matter Admission Plus Disclosure Restrictions

The functional parallel is **authorization for the particular matter, plus any screen/order/recipient restrictions**. Bar admission, seniority and a high confidentiality ceiling do not create access to every client's information. Matter membership is necessary only under the particular approved access policy and is not sufficient to settle privilege, conflicts or disclosure authority; applicable confidentiality and screening duties remain those discussed above.

| Requester or use | Example additional condition | Example result |
| --- | --- | --- |
| Partner working on matter B | No authorized access to matter A; any applicable screen remains in place | Denied matter-A material despite seniority or broad access elsewhere |
| Authorized outside counsel on matter A | A hypothetical protective order limits a particular document to its specified outside-counsel recipients | Eligible only if that lawyer and use satisfy the actual order and all other controls |
| Client executive normally authorized for matter A | The same hypothetical order excludes that recipient from this document | Denied this document even though other matter-A material is client-visible |
| Research agent serving matter A | The applicable order/client/vendor rules do not authorize that processing route, or their evaluator is unsupported | Denied before model submission; the supervising lawyer's access is not inherited automatically |

"Attorneys' eyes only" is not an extra sensitivity rung or a universal fixed rule. The actual protective order defines its recipients, uses and exceptions; another order may define them differently. A compartment flag cannot establish a valid ethical screen, waive a conflict, determine privilege or permit a processor the governing rule excludes. These are illustrative access decisions, not a legal-order interpreter implemented by the current profile APIs.

### Banking And Capital Markets

Use **information barrier** (also historically called a Chinese wall), **private/public side**, **deal-team access**, **research independence**, **control-room approval**, and **permitted use**. These are familiar operational terms, not a new government-style clearance ladder. A firm's example sensitivity tiers might remain Public / Internal / Confidential / Restricted, while `deal:cedar` and `deal:maple` are independent scopes. A public-side desk is not a public internet audience, and an internal research draft is not public merely because research often uses published sources.

#### Jurisdiction-Specific Controls

The following is a targeted information-handling comparison, not a complete banking regulatory profile. Sources were checked on October 21, 2026. Apply the actual entity, activity, instrument, jurisdiction and effective rule version; do not turn every bank employee into the subject of every securities rule.

| Jurisdiction and primary reference | Relevant control | Proposed policy mapping and boundary |
| --- | --- | --- |
| United States: [Exchange Act section 15(g), 15 USC 78o(g), 2024 Code edition](https://www.govinfo.gov/content/pkg/USCODE-2024-title15/pdf/USCODE-2024-title15-chap2B-sec78o.pdf) | Registered broker-dealers must maintain and enforce procedures against misuse of material nonpublic information | Deal/source scope, authorized use, controlled recipients and decision records; not an automatic trading permission |
| United States: [FINRA 2241(b)(2)(G)](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2241) and [2242(b)(2)(H)](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2242) | Equity/debt research safeguards against conflicted pressure or oversight, including from investment banking and sales/trading; the rules and exceptions differ | Separate research/deal purposes and routes; a department label alone does not establish analyst independence or forbid every legitimate interdepartmental communication |
| European Union: [MiFID II delegated Regulation 2017/565, Articles 34 and 37](https://eur-lex.europa.eu/eli/reg_del/2017/565/2022-08-02/eng) | Conflict-management controls on information exchange, separate supervision and investment-research safeguards, including physical separation or appropriate alternative barriers in the specified circumstances | Independently reviewed conflict exclusions, research-use constraints and controlled sharing; this is EU law, not UK/FCA guidance |
| European Union: [MAR Regulation 596/2014, Articles 7-10, 14 and 18; June 5, 2026 consolidation](https://eur-lex.europa.eu/eli/reg/2014/596/2026-06-05/eng) | Inside-information identification, insider-dealing/unlawful-disclosure controls and applicable insider-list obligations | Separate legal-status, recipient/use and recordkeeping rules; a sensitivity label or software grant establishes neither a lawful disclosure nor permission to trade |
| Japan: [FSA supervisory guidelines, III-2-4, customer/corporate-related information management](https://www.fsa.go.jp/common/law/guide/kinyushohin/03.html) | Need-to-know, organizational/physical/system barriers and specified procedures for exceptional wall-crossing, including records and prior compliance approval | Current deal/recipient/purpose scopes, controlled approvals and access history, not blanket interdepartmental access; [SESC](https://www.fsa.go.jp/sesc/english/index.html) is the Securities and Exchange Surveillance Commission within the FSA |

The EU comparison uses the cited consolidated texts as documentation aids; the linked EUR-Lex records identify the underlying Official Journal acts. U.S. MNPI, EU inside information and Japanese corporate-related information are jurisdiction-specific concepts, not interchangeable field labels. Cross-border work must satisfy every applicable resolved restriction; an unsupported required rule refuses the operation. UK requirements require a separate profile rather than assuming EU rules still apply identically. Privacy, resilience, supervision, retention and other obligations remain separate from this targeted barrier example.

#### Worked Deal-Room Example

Assume a synthetic firm has approved the following assignments and processing routes. These are design examples, not a working finance-policy loader or a claim of regulatory qualification:

| Requester or conversation | Authorized scope | Result under this example policy |
| --- | --- | --- |
| Cedar banker and Cedar deal agent | Restricted ceiling; deal Cedar; transaction diligence | May use eligible Cedar material through the approved private-side route |
| Equally senior Maple banker | Same ceiling; deal Maple only | Denied Cedar material; rank and employer do not supply Cedar need-to-know |
| Public-side research or trading assistant | Its approved released-source collection and permitted purpose | No Cedar/Maple private material, previews or hints; research and trading permissions still differ |
| Broadly authorized agent in a conversation with a Maple-only participant | Agent independently covers Cedar and Maple; shared audience does not | Cedar remains ineligible before retrieval or model input |
| Settings administrator | Metadata configuration only | No deal content; control-room/content/grant authority requires separate explicit capabilities |

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/profiles-02.svg" alt="Worked Deal-Room Example - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart TD
    C["Cedar team and scoped agent"] --> CG["Cedar audience / purpose gate"]
    CG --> CE["Eligible Cedar evidence"]
    M["Maple team and scoped agent"] --> MG["Maple audience / purpose gate"]
    MG --> ME["Eligible Maple evidence"]
    M -. "Cedar request: denied" .-> CG
    P["Public-side research or trading request"] --> PG["Separate audience / use gate"]
    PG --> PE["Only sources authorized<br/>for this audience and use"]
```

</details>

**Arrows describe requests and authorized results, not unrestricted data movement.** Cedar and Maple have no lateral grant. The denied arrow terminates at the gate, not at Cedar's evidence. The public-side path cannot borrow the agent's private-side context. A clean model conversation, not just a different search filter, is needed when the audience's authority narrows.

**Wall-crossing is a controlled exception workflow, not a higher clearance tier.** The proposed host must require a current, specifically scoped authorized decision and record who, what, why and when before admitting any newly permitted use. It must not self-approve from chat text or a generic compliance job title. Such a decision cannot override law, create trading permission, remove recordkeeping duties or make received information public. Removing a grant or opening a clean conversation also cannot make a human recipient forget information already received. The actual organizational procedures and trading restrictions remain outside what a memory label can accomplish.

### Personal Use

Keep the vocabulary simple. A possible profile `personal-example/v1` orders `unclassified`, `private`, `sensitive`, `restricted`, with user labels General, Private, Sensitive and Highly Private. General is not automatically Public. Sharing is a separate audience choice, so Family and Work are not ranks above or below each other.

| Example privacy tier | Example document | Reader/process scope |
| --- | --- | --- |
| General | A draft recipe or travel checklist | Owner and explicitly authorized helpers; publish only after release approval |
| Private | A household planning note | Selected household people/agents for an approved task |
| Sensitive | Tax, financial or personal health material | Specific person/project scope and approved local/external processing destinations |
| Highly Private | An intimate journal or similarly restricted record | Explicitly named readers/services and purposes; no automatic access for every personal assistant |

**Example:** a household assistant can work on the shared grocery list but not a private journal. A finance agent can help with taxes without receiving memoir/private relationship material. If a guest joins the conversation, the agent's broader independent access does not let private financial memories enter that shared model context. You can explicitly authorize one agent for several areas without merging those areas or their audiences.

### Generic Organization

A business can choose familiar **Public / Internal / Confidential / Restricted** labels with **authorized sensitivity level**, **department/project membership**, **permitted business purpose**, and **approved service account** on the entity side. These are an example organizational taxonomy, not a universal standard. Public applies only to explicitly approved material with compatible release/recipient controls. A defaulted or unresolved label must never become Public because it occupies the first position in this vocabulary.

An internal employee handbook, confidential budget workbook and restricted board pack can use that ladder. An approved finance analyst/agent may work on the budget without access to the board pack. The same budget used by two projects keeps one source policy; project membership does not issue a second, broader grant. Equal label text in healthcare, legal or corporate profiles does not establish equivalent permissions.

## People, Agents And Conversations

The profile changes the display words, not the decision's structure:

| Domain | Document-side label | Person-side access terminology | Agent-side terminology | Separate need-to-know scope |
| --- | --- | --- | --- | --- |
| Government / contractor | Classification and authoritative handling markings | Eligibility/clearance and specific access authorization, as applicable | Approved system/service processing scope, not personnel clearance | Contract/program and any required access-control compartment |
| Healthcare | Sensitivity, PHI applicability and handling restrictions | Workforce role/access authorization | Approved clinical/billing service identity | Patient/care team, data fields and permitted use |
| Legal | Confidentiality category and reviewed handling status | Authorized client/matter team and exclusions | Approved matter-processing service identity | Client/matter, purpose, screen and intended recipient |
| Banking / capital markets | Sensitivity plus reviewed nonpublic/inside-information status | Deal-team entitlement and controlled barrier crossing | Approved deal/research/trading processing identity | Deal, activity, purpose, recipients and jurisdiction-specific use restrictions |
| Personal | Privacy level and sharing restrictions | Named person/group access | Explicit assistant permissions | Person/project/topic and intended audience |
| Generic business | Sensitivity and business restrictions | Scoped role/access entitlement | Scoped service-account authorization | Department/project and approved business use |

For each human or agent, trusted administration records the authenticated identity, selected policy/version, ceiling, explicit compartments/scopes, purposes, allowed operations and destinations. Grant changes and approvals have separate administrative capabilities. Actual identity proof comes from the qualified host, not `persona:finance`, a chat title or a model-provided ID. A persona can select a registered agent identity; a trusted conversation binding can impose a lower ceiling and permitted scopes. Neither grants permissions that the participants lack.

In practical terms, an authorized access manager verifies the person/service identity, records its bounded entitlements and decision provenance, and reviews/revokes them when assignments change. The entity does not nominate its own clearance, patient list or matters. A job title can contribute to an approved grant policy but is not a universal grant by itself. Read, write, share, export and administration are separate operations; sharing an owner's identity or credentials is not how an agent receives access.

For a synthetic personal installation, an access register could contain these decisions (not installed manifest syntax):

| Entity | Ceiling under `personal-example/v1` | Explicit scope/purpose | What that does not grant |
| --- | --- | --- | --- |
| `person:alex` | Highly Private (`restricted`) | Finance and private writing, for the owner's approved uses | Automatic delivery to guests or arbitrary providers |
| `agent:tax-helper` | Sensitive (`sensitive`) | Household finance, read for tax preparation, approved processing destination | Private writing, general export, self-edited grants or every finance purpose |
| `person:guest` | General (`unclassified`) | Explicitly shared general material | Finance or private writing merely by joining a chat |
| `person:settings-editor` | No content grant | Separately authorized profile-label settings | Any document read, even at the lowest sensitivity |

The sensitive tax workbook can be admitted into an authorized tax-preparation conversation between Alex and the tax helper with a Sensitive-or-higher context ceiling and approved route. A Private-only context ceiling refuses it. Adding the guest refuses finance recall even if Alex and the helper remain present. Raising the chat ceiling does not add the guest's missing finance scope. These are access-decision examples, not a claim that this register or live conversation binding has been implemented.

For an access to succeed, the document's current restrictions must be satisfied by **every applicable participant and agent**, within the conversation's ceiling, purpose, action and actual destination/audience. Intersection is not just taking the lowest scalar level: a missing matter, patient, compartment, purpose or recipient authorization can deny even when every ceiling is high enough. The host must include silent recipients, relays and other actual output recipients. Provider approval is an additional gate, not a reason to omit a participant. Policy-free/general legacy operation is separate from opt-in protected operation.

For example, a broadly authorized agent plus a guest does not authorize a private answer "for internal reasoning." The private material must stay out of candidate retrieval, tools, prompts and provider submission in that conversation. Adding a participant or changing grants invalidates the old turn. When effective access narrows, a new clean security/model context is mandatory; the default is a fresh context on any new person/agent joining, even if its nominal clearance equals the others'. A configuration administrator may edit permitted settings while holding **no document-reading grant**.

### A Group Has An Intersection, Not A Union

This organizational example uses synthetic levels/scopes, not official clearances. Assume all participants permit the same purpose, action and destination; those controls can narrow the result further.

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/profiles-03.svg" alt="A Group Has An Intersection, Not A Union - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart TD
    A["Person 1: Top Secret ceiling<br/>Scopes A and B"] --> I["Intersect the complete audience<br/>and the conversation binding"]
    B["Person 2: Secret ceiling<br/>Scope A only"] --> I
    C["Agent: Top Secret ceiling<br/>Scopes A, B and C"] --> I
    I --> E["At most Secret<br/>Common scope A only"]
    E --> G["Check purpose, action, recipient,<br/>destination and current policy"]
    G --> R["Only eligible evidence enters<br/>retrieval and model context"]
```

</details>

**No participant lends extra privileges to the group.** Scope B does not enter this conversation even though Person 1 and the agent can use it elsewhere. The diagram's last arrow applies only after every gate permits the request; unresolved participants or controls deny. Several required scopes on one document must all be satisfied, not merely one matching tag.

### When Somebody Joins: Start Fresh

Do not try to remove a few names, messages or citations from a privileged live context and hope the model has forgotten their implications. For example, if a Secret-only colleague joins a Top Secret discussion, the old model session must not continue for that colleague. The same applies when everyone has the same tier but the newcomer lacks a matter/patient/compartment authorization. The implementation contract is:

1. Pause protected continuation, fence/cancel the old turn and prevent queued/streaming/late provider or tool responses and retries from reaching the new audience. Do not blindly resend a cancelled action in the replacement context.
2. Resolve the actual complete audience and current permission intersection. Unknown participants or stale permissions refuse; creating an empty context does not turn an unresolved audience into an authorized one.
3. Establish a fresh security/model context with new admitted handles, no old provider-session/prompt state and no inherited transcript, tool results, persona/prelude or cached conversation summary. Reapply only independently authorized configuration and evidence. Preserve the old conversation under its old restrictions; do not expose its history, attachments, previews or notifications to the newcomer. A separate conversation is the safer default when thread history would otherwise be visible.
4. Continue only after the frontend/provider/output path proves that separation. If it cannot, refuse the protected transition. This cannot retract text already emitted, but must block old-epoch output from appearing after the audience change.

An optional summary can help, but it is not a shortcut around the boundary. Build a new summary from sources independently authorized for the new audience, or use an already approved releasable summary with current policy/provenance. Do not have the old privileged model generate a "sanitized" summary and automatically declare it safe. Summaries inherit restrictions; lowering them is a separate authorized release/reclassification process. Starting with an empty context and no handoff is preferable to an unproven summary. None of these rules deletes or retroactively reclassifies the original thread.

These are protected-frontend requirements, not a feature claim for the currently deployed Hermes/Mnemosyne path. They also do not imply that the library can erase provider-held information or sandbox arbitrary owner-controlled tools.

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/profiles-04.svg" alt="When Somebody Joins: Start Fresh - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart TD
    J["Audience or authority changes"] --> F["Fence old turns, streams,<br/>tools, queues and retries"]
    F --> V{"Complete current audience<br/>and permissions verified?"}
    V -->|No| D["Refuse continuation"]
    V -->|Yes| N["New clean context<br/>No inherited privileged state"]
    N --> H{"Independently authorized<br/>handoff available?"}
    H -->|Yes| A["Admit only that approved evidence"]
    H -->|No| E["Start empty; no summary required"]
    A --> P["Continue through qualified<br/>provider and output gates"]
    E --> P
    F -. "Retain separately" .-> O["Old history remains restricted<br/>Not visible to the new audience"]
```

</details>

**A fresh context is a security boundary, not a transcript-cleanup operation.** The approved-handoff branch never asks the old privileged model to declare its own summary safe. Both continuation paths require verified state separation, current authorization and a qualified delivery path; otherwise they refuse.

#### Fresh-Context Transition Checks

The following supplement H14 and V2/V3/V5/V6. They are planned qualification, not newly passed tests:

| ID | Required proof |
| --- | --- |
| T01 | A lower-ceiling newcomer or equal-tier newcomer lacking a compartment triggers a new clean context; no old prompt/provider state is reused |
| T02 | A late token, tool result, full response, queued message or retry from the old epoch never reaches the new audience |
| T03 | The newcomer cannot see old restricted transcript/attachments/previews/notifications through UI, history, reconnect or other delivery paths |
| T04 | Denied old-context canaries never reach a new-context summary/model input; a handoff is independently authorized or omitted |
| T05 | Unknown/incomplete participants or stale authority refuse continuation without falling back to public/unclassified mode |
| T06 | Safe startup succeeds with no handoff summary; original history remains protected and unchanged, and any approved release artifact retains its provenance/current policy |

#### Financial Information-Barrier Checks

These are additional planned design/qualification cases, not executed tests or regulatory certification:

| ID | Required proof |
| --- | --- |
| F01 | Equal-ceiling deal-A and deal-B principals cannot retrieve or expand each other's evidence; counts, filenames and denied diagnostics disclose no restricted objects |
| F02 | A broadly authorized shared agent cannot inject private-side evidence, cached text, persona history or summaries into an unauthorized deal/public-side context |
| F03 | Wall-crossing requires a current explicit scoped decision through the authorized workflow; stale approval, a chat request or a compliance title alone cannot grant access |
| F04 | Read admission is distinct from share/export/trading authority; a read grant cannot authorize an otherwise prohibited use or make information publicly releasable |
| F05 | Settings administration yields no deal-content access; any separate control-room/grant authority has explicit bounded capabilities and attributable decisions |
| F06 | The applicable jurisdiction/activity/rule revision and required obligations are resolved conjunctively; unknown or unsupported constraints refuse rather than select a permissive profile |

## Classifying External Documents

### One Source, An External Original And A Current Policy

Keep the original bytes in the owner's filesystem, Vault, object store or external archive. Mnemosyne keeps permitted compact policy/index/evidence metadata, not an original-file or full-text-archive copy. Use a stable source ID, immutable byte-revision ID, available byte checksum and current **policy revision**. A URI identifies an occurrence/location; it is neither the source's permanent identity nor its permission grant. Copies of identical bytes do not prove identical ownership, release status or permission across tenants.

Maintain the authoritative policy binding in the access-controlled source/policy catalog for that ownership domain, reusing the existing asset/revision/policy facilities rather than introducing an unrelated labeling database. The archive can own that document-control authority; Mnemosyne must consume its trusted current binding and retain the policy/source lineage needed to enforce derived memories. This is a logical authority, not a requirement for one global database or an external policy server. The complete cross-format import/control-plane contract still requires implementation and qualification.

| Source format | Where a classification indication can travel | What the protected resolver/indexer must rely on |
| --- | --- | --- |
| Markdown / text | YAML front matter or a separate manifest | Accepted source/revision policy binding; untrusted document text cannot grant access |
| Word / Excel / PowerPoint | Existing approved label/metadata, visible marking and/or external catalog/sidecar reference | Verified mapping to the issuer/tenant/profile/version and current policy authority; not a filename or a freely editable custom property |
| PDF | Existing marking/metadata and/or catalog/sidecar reference | The accepted whole-file or qualified representation policy, including attachments/annotations |
| Image / photograph / audio / video | Optional embedded metadata plus catalog/sidecar reference | Source-level policy and authorized extraction/transcription/vision route; missing metadata does not mean public |
| Web page / remote object | External registration and, where available, a referenced immutable capture | Current access/handling policy plus the exact authorized representation/revision, not URL reachability alone |

Office sensitivity labels can persist in file metadata; Microsoft's [sensitivity-label documentation](https://learn.microsoft.com/en-gb/microsoft-365/compliance/sensitivity-labels?view=o365-worldwide) describes that mechanism. This is a possible integration signal, not a claim that Mnemosyne currently interprets or enforces Microsoft labels, decrypts protected Office files or supports every document format. Preserve an existing protection system; do not strip encryption/labels to index a file. Where required import, decryption or policy translation is unsupported, refuse the protected path.

### Markdown And Portable Metadata

This **illustrative front matter is not a newly implemented Wiki/Mnemosyne loader**. The fields express the desired document-control contract; an untrusted author changing them cannot change accepted authority or declassify material.

```yaml
---
source_id: "source:household-planning"
policy_id: "personal-example"
policy_version: 1
classification: "private"
compartments: ["household-planning"]
audiences: ["household-authorized"]
purposes: ["household-planning"]
---
```

A Word document or spreadsheet can instead have portable metadata beside it. Prefer a stable source ID over a path-only association. The following is an **illustrative external manifest**, not installed configuration or a signed authorization. The referenced workbook does not exist in this example. Its checksum is explicitly unknown, not an invented verified digest:

```yaml
manifest_version: 1
source_id: "source:household-accounts"
source_revision_id: "bytes:001"
occurrences:
  - uri: "file:///example/evidence/household-accounts.xlsx"
verification:
  algorithm: "sha256"
  digest: null
  state: "unverified"
policy_revision: 1
policy:
  policy_id: "personal-example"
  policy_version: 1
  classification: "sensitive"
  classification_source: "manual"
  owner: "person:owner"
  compartments: ["household-finance"]
  audiences: ["household-authorized"]
  purposes: ["tax-preparation", "financial-review"]
project_memberships: ["project:tax", "project:household-budget"]
review:
  state: "accepted"
  decision_ref: "decision:synthetic-classification-001"
```

Accepted policy review is different from verified source bytes. Compute a real SHA-256 over the defined source representation when authorized readable bytes are available; register the digest, method/time and verification result. A reference-only registration stays unverified. Explicit expansion must verify the expected revision; ordinary recall does not reopen and hash every original.

The manifest can be held beside the original, or a local sidecar can contain only its stable source/policy references. In either arrangement, the accepted current policy binding is authoritative. A missing, edited or conflicting sidecar/front matter is not permission to downgrade: use the trusted binding or keep the protected operation unresolved/denied. Signed exports can authenticate an issuer, but alone do not prove that an old policy is still current. Policy changes require current revision/epoch/witness checks and invalidation, independently of source-byte checksums.

Changing front matter or embedded Office metadata changes source bytes and therefore the byte revision. Changing only the external accepted policy can advance the policy revision without changing the original file. That distinction avoids forcing an edit of an original merely to change handling. Embedding reuse still depends on the qualified extraction/input contract; unchanged bytes or a label-only edit is not a blanket promise to skip every dependent check.

### One Document Shared By Several Projects

Do not create independent authoritative classifications in each project folder. Within the same permitted ownership domain, both projects reference the same source/revision and current policy binding. Membership says **relevant here**, not **everyone here may read it**.

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/profiles-05.svg" alt="One Document Shared By Several Projects - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart LR
    T[Tax project] --> S[Stable source and byte revision]
    B[Household budget project] --> S
    S --> O[External original and permitted occurrences]
    S --> P[Current accepted policy revision]
    P --> G[Participant, purpose and destination gates]
    G --> I[Authorized derived index and evidence]
```

</details>

For the workbook above, adding it to a generally shared household project does not expose financial information to every project member. The file keeps its finance compartment and audience restrictions. Project-specific notes/summaries inherit the source restrictions and can add stricter ones. Multiple required compartments mean multiple requirements, not an automatic union of project readers. Moving/renaming the workbook changes its registered occurrence, not its identity or rights. A symlink or identical copy is not a new less-restricted source.

If another project needs a less-restricted subset, an authorized release workflow can create a separately identified reviewed extract/redacted derivative with exact provenance and an approved policy. Merely copying, summarizing, hiding rows or asking a model to redact does not lower restrictions. Cross-owner/tenant sharing requires explicit sharing authority; a checksum match must not reveal another owner's file. General multi-policy composition is not currently implemented: if required domains cannot be represented/enforced together, refuse rather than choose the looser profile.

### Assigning And Revising A Classification

1. Register the external source and its authority/owner; recognize trusted existing markings and required restrictions before sending content to an extractor or model. Reference-only metadata registration need not read the payload.
2. Obtain an accepted decision from the authorized document owner/steward or applicable classification authority. Government-derived markings follow their authoritative instructions; clinical and legal material follow the actual reviewed organizational/domain rules. An approved deterministic folder/import rule may supply a restrictive baseline, not blanket public release.
3. Record the selected profile/version, sensitivity, compartments, audience, purpose, applicable handling controls, decision provenance and current policy revision. A classifier or LLM may suggest a decision only on a separately authorized processing route; its suggestion is not an accepted grant or declassification.
4. Index only through an authorized path and retain source/revision/policy lineage on chunks, summaries, embeddings and evidence handles. Do not run Office macros, embedded scripts or arbitrary external links as a classification/import step. Unsupported parsers/controls refuse their protected path.
5. On correction, reclassification or revocation, update current authority and invalidate affected permissions/handles/caches/derivatives promptly, without waiting for re-embedding. Preserve historical provenance; an old policy snapshot cannot reopen revoked access. Byte edits create a new immutable source revision and any necessary extraction revision.

Missing classification retains the accepted `unclassified` default only where that exact vocabulary/defaulting contract exists and no stricter trusted inheritance applies. It does not grant readers or public release. Missing required owner/access metadata, unknown labels or conflicting required controls remain denied/pending. Do not resolve a disagreement by taking whichever label is easier to use.

**Mixed-content files need whole-file discipline.** An Excel workbook includes hidden sheets/rows, comments and embedded content; a presentation may have hidden slides and speaker notes; a Word/PDF file may have comments, revisions or attachments. A visible public-looking page does not make the entire file public. Default to the source's full applicable restrictions. Lower-granularity sheet/page/slide/span access needs qualified extraction and policy inheritance, or a separately approved derivative; it must not expose forbidden text to an internal model/ranker first.

### External URLs Are Not Automatically Public

An openly published page can be registered with reviewed public access/reuse controls for its exact representation. But URLs also identify authenticated portals, shared-drive objects, private links and accidentally exposed material. Reachability is not ownership, release authority, permitted processing or permission to publish. Even an actually public source can support a private annotation or revealing project association. Copyright/licensing and any other applicable use conditions are separate from confidentiality.

Bind web evidence to an external immutable capture or exact defined representation hash and capture identity when available. ETag/Last-Modified are hints, not cryptographic revision proof; a current page need not match an earlier citation. Keep credentials/token-bearing links out of public metadata/logs, apply approved resolver/redirect/destination restrictions, and never let a redirect silently broaden authority. Required source content must not be fetched merely to decide whether an unauthorized requester may know it exists.

### Additional Documentation Acceptance Scenarios

These are requirements for the future cross-format integration, **not newly passed tests**:

| ID | Scenario and expected result |
| --- | --- |
| D01 | Each domain renders its own document and person/agent vocabulary; matching display names do not confer cross-domain equivalence |
| D02 | Human and service identities have explicit independent grants; high ceiling without patient/matter/program need-to-know denies |
| D03 | Front matter, embedded labels, sidecars and accepted authority disagree; no automatic downgrade or grant from untrusted content |
| D04 | One source appears in two projects or moves by URI; identity/policy stays intact and project membership grants no reader |
| D05 | Same bytes occur under another tenant; no hash-existence disclosure or implicit policy/content sharing |
| D06 | Policy changes without byte changes; current controls invalidate old handles/derived access without a source-hash dependency |
| D07 | Source bytes change, including front matter; old citations remain tied to their revision and changed-source expansion is explicit |
| D08 | Hidden sheets, slide notes, revisions and embedded attachments contain denied canaries; none reaches unauthorized extraction, ranking or model input |
| D09 | Public URL, private link, redirect and private annotation have distinct controls; reachability never acts as authorization |
| D10 | A claimed redacted/public derivative has no accepted release decision or qualified control mapping; protected access/release refuses |

## Configuration Workflow

1. Establish the policy domain, tenant/owner and authoritative source for its rules. Decide which stores and real frontend/provider paths are supported. Do not merge unrelated domains just because their label text matches.
2. Choose a stable policy ID/version and ordered level IDs, lowest first. Define user/admin display labels separately. Specify what each tier means within that domain; public release remains a separate decision.
3. Define compartments, audiences, purposes, actions and destination/provider controls. A project association is relevance, not an access grant. Define required exclusions such as ethical walls explicitly.
4. Identify each required handling-rule version and current evidence/attestation source. Unknown applicability or unsupported evaluator means deny, not a permissive default. Reference existing approved credentials; do not store secrets or executable callbacks in the profile.
5. Register authenticated agent/persona identities, trusted chat/audience bindings and participant grants. Each agent, chat ceiling and applicable participant constrains the effective request. A display name or chat selector cannot assert authority.
6. Assign configuration/grant-administration capabilities independently from data access. Preview direct and indirect access expansion and required approvals before exact-predecessor application.
7. Validate synthetic allowed/denied cases through actual supported dispatch, not just parsing. Inspect candidates, tool results, model inputs, delivery, audit and restoration. Only then consider separately approved activation/migration.

## Proposed Manifest Shape

The JSON below is an illustrative design projection, **not a file the current CLI accepts**. `rule_refs` identify reviewed registry entries, never module paths or shell expressions. A future loader must use a strict versioned schema with unknown/duplicate-field refusal and supported capability checks before enabling it.

```json
{
  "schema_version": 1,
  "policy_id": "clinic-example",
  "policy_version": 1,
  "levels": [
    {"id": "L0", "user_label": "General", "admin_label": "Tier 0"},
    {"id": "L1", "user_label": "Sensitive", "admin_label": "Tier 1"},
    {"id": "L2", "user_label": "Highly sensitive", "admin_label": "Tier 2"}
  ],
  "terminology": {
    "user": {"classification": "Information sensitivity", "clearance": "Access level"},
    "administrator": {"classification": "Record tier", "clearance": "Principal ceiling"}
  },
  "compartment_kinds": ["patient", "care_team"],
  "purposes": ["billing"],
  "rule_refs": ["clinic-policy:phi-disclosure:v1"],
  "missing_classification": {"mode": "deny_pending_review"}
}
```

The example does not define a clinical clearance standard or declare all clinic data HIPAA-covered. The required rule reference is hypothetical and must refuse until its exact evaluator, applicability and evidence are provided and qualified. The profile is not a grant: registering it creates no reader or administrator. Neither `L0` nor "General" authorizes publication.

### Existing API Example

This complete snippet constructs and validates synthetic policy metadata only. It does not authenticate a participant, authorize retrieval, open a store, apply an overlay or load the proposed JSON. Run it only in an isolated development environment with the qualified core on its import path.

```python
from mnemosyne.core.policy import MemoryPolicy, PolicyDefinition

levels = (
    {"id": "L0", "user_label": "General", "admin_label": "Tier 0"},
    {"id": "L1", "user_label": "Sensitive", "admin_label": "Tier 1"},
    {"id": "L2", "user_label": "Highly sensitive", "admin_label": "Tier 2"},
)
definition = PolicyDefinition(
    policy_id="clinic-example", version=1,
    levels=tuple(level["id"] for level in levels),
)
record_policy = MemoryPolicy(
    policy_id=definition.policy_id, policy_version=definition.version,
    classification="L1", owner="owner:example",
    classification_source="manual",
    compartments=frozenset({"patient:synthetic-001"}),
    audiences=frozenset({"billing-team"}),
    purposes=frozenset({"billing"}),
)
definition.validate_binding(record_policy)
labels = {level["id"]: level["user_label"] for level in levels}
assert labels[record_policy.classification] == "Sensitive"
assert definition.levels.index("L0") < definition.levels.index("L1")
print("Synthetic policy metadata validated; no content access granted.")
```

The same stable level can render as "Sensitive" to a user and "Tier 1" to an administrator. That display conversion occurs outside authorization. Reordering IDs or changing their meaning is a new security-semantic revision, not a harmless translation update. Real use still needs fresh complete participant grants and the protected host/session APIs described in the [host design](/hidden/review-2d66666c7be62e65c7daf868/host-authorization/).

## Access And Administrative Configuration

Keep independent capability sets, with scoped delegation and no universal `admin = allow all` shortcut:

| Capability example | Permitted administration | Content access implied |
| --- | --- | --- |
| Presentation editor | Approved translations, help and display labels that do not change semantics | None |
| Profile/settings administrator | Approved profile configuration proposals/settings within its scope | None |
| Grant administrator | Explicit bounded grant proposals/changes, subject to ceiling, target and approval rules | None |
| Policy/grant approver | Approve allowed changes under the configured separation-of-duties policy | None |
| Audit reviewer | Separately scoped sensitive audit metadata | No memory/prompt content by default |
| Content reader | Explicit record/purpose/audience/destination access | No administrative authority |
| Platform/key owner | Separately controlled trusted host capability | Outside application-level protection if it can read keys or replace enforcement |

These are proposed capability bundles, not hard-coded required role names. One operator may explicitly hold several bundles, but granting configuration authority does not silently assign content-reader, approval or key-owner rights.

Treat level ordering/defaults, rule references, identity/group mappings, provider routes, delegation, approval policy and restore/key configuration as security-semantic changes. Ordinary administrators cannot increase their own or controlled identities' access indirectly through these settings. Subject/actor aliases, groups, service identities and delegated agents must be included in expansion analysis. A configurable approval policy may require a distinct approver; a single-operator installation must explicitly provision the stronger authority rather than bypassing approval through a generic configuration role. Reading sensitive names/relationships in the control plane needs its own metadata scope.

Administrative backup, troubleshooting, impersonation and export must not become undeclared data-reading paths. Preserve content-free audit and separately authorized incident/recovery capabilities. If tools share an unrestricted raw owner/key identity, document the bypass and do not claim the application admin role constrains that identity.

## Defaults, Multiple Domains And Migration

The example profile explicitly denies missing classification. The existing reviewed defaulting helper instead uses the exact `unclassified` label when the selected vocabulary contains it and no stricter inheritance applies. That helper is not an arbitrary configurable-default loader. Keep the existing accepted behavior unless an explicit, separately tested profile/migration revision changes it. A cosmetic alias for `unclassified` cannot turn it into public access or remove inherited overlays.

Identical level names in two domains do not establish equivalence. The current binding has one exact policy ID/version; a record subject to several policies requires an explicitly reviewed joint policy/constraint representation, not choosing whichever profile grants access. General multi-policy composition and legally conflicting obligations remain separate implementation work. No model-selected namespace, guessed label conversion or unreviewed cross-bank union is allowed.

For a migration, preview every old-to-new policy/version/level mapping, inherited compartment/overlay, defaulted value and unresolved row. Unknown/ambiguous mappings stay denied/pending. Preserve originals, provenance, current authority, rollback/recovery evidence and stricter restrictions. Editing a label must not reclassify old data, invalidate citations silently or revive revoked access.

## Current Capability Versus Proposed Configuration

Development supplement: fork candidate `b70cf2d` adds a qualified profile metadata type (internal supporting reference; not included in this packet) and owner-only configuration history (internal supporting reference; not included in this packet). The type supports separate user/admin labels for both levels and field terminology. It is not a loader for the illustrative manifest above, an administrative role, a content grant or a regulatory evaluator. The table below retains the original `2d1502b` baseline explicitly; actual frontend rendering and administrative authorization remain separate work.

### Scoped Administration API

The next isolated candidate adds a metadata-only administration facade (internal supporting reference; not included in this packet), not a deployed administrator account or CLI configuration loader. A trusted host supplies authenticated sessions, current scoped capabilities and canonical independent-actor mappings. The facade deliberately has no memory-read, grant/delegation, key-export, recovery or activation method. Source/API qualification and actual frontend authentication are separate acceptance steps.

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/profiles-06.svg" alt="Scoped Administration API - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart LR
    S[Authenticated administrative session] --> C[Fresh profile scope and capability]
    C --> P[Preview exact profile change]
    P --> L[Labels only: same policy definition]
    P --> M[Policy meaning: identity, version or level order]
    M --> A[Independent actor approves exact plan]
    L --> F[Fresh claims and predecessor checks]
    A --> F
    F --> W[Stage, witness, finalize configuration]
    W --> R[Metadata receipt, not memory access]
```

</details>

This function is a complete label-change operation for an already constructed, qualified `ProfileAdministration` instance. `session` is an opaque authenticated host session, not a username or a model-supplied principal. It increments the immutable profile version without changing policy identity, classification order, grants or records. A concurrent configuration or authorization change refuses; do not blindly retry an uncertain publication.

```python
from dataclasses import replace
from mnemosyne.core.host_profile import LevelDisplayMetadata


def rename_level(admin, session, profile_id, level_id, user_label):
    current = admin.view(session, profile_id)
    profile = current.profile
    if profile is None or level_id not in profile.policy.levels:
        raise ValueError("A registered profile and level are required")
    levels = tuple(
        LevelDisplayMetadata(level.level_id, user_label, level.admin_label)
        if level.level_id == level_id else level
        for level in profile.levels
    )
    replacement = replace(profile, version=profile.version + 1, levels=levels)
    plan = admin.preview(session, profile_id, replacement)
    return admin.apply(session, plan)
```

Adding/removing a profile or changing its policy definition uses `profiles:policy` rather than `profiles:labels`. It additionally requires `approval = admin.approve(independent_session, plan)` followed by `admin.apply(session, plan, approval=approval)`. Both actors need explicit view/profile scope; the approver needs `profiles:approve`, a different principal and canonical separation identity, and the same current authority-wide authorization revision/epoch. Two personas or aliases for the same person are not independent approval. An administrator cannot grant these capabilities to itself through this facade.

Plans are local exact-object handles, limited to 64 pending changes and 1-300 seconds. They are not portable bearer credentials. Authentication is repeated at read/publication gates, including after a potentially slow callback before expiry admission. Once a write is attempted, the plan is consumed; preserve its operation ID for separately authorized owner receipt/recovery inspection. A refused return may follow a committed change. Never interpret a lost acknowledgment as proof that nothing happened.

This API does not solve actual host authentication, the persistent principal/grant/audience registry, output/provider/history gating, semantic evaluator implementation or regulatory compliance. Configuration grants do not imply content grants, and public-facing labels must accurately describe the unchanged policy semantics. Raw owner/key capabilities must stay outside ordinary/model tools.

| Piece | Current boundary at `2d1502b` |
| --- | --- |
| Explicit ordered policy vocabulary and exact policy/version validation | Implemented core types; indexed qualification covers explicit supported prepared-store APIs, not arbitrary records or a profile loader |
| Generic compartments, audiences, purposes and explicit host grants | Implemented scoped APIs; real frontend authority still needs implementation/qualification |
| User/admin display dictionaries | Demonstrated local projection above; integrated UI/profile renderer not implemented |
| Declarative manifest loader, strict schema, administration/approval workflow | Proposed; not installed CLI/configuration syntax |
| Generic overlay metadata | Present; unsupported overlay dimensions refuse in the inspected reader |
| HIPAA/ABA/other domain rule evaluator, consent/exception handling and provider attestation | Not supplied by names or labels; requires reviewed supported rule implementations |
| Automatic policy-profile migration, arbitrary defaulting and general multi-policy composition | Not implemented or authorized by this guide |

## Validation Checklist

Before enabling a profile, prove exact namespace/version and level order, independent user/admin labels, unknown-rule refusal, missing-value behavior, nonpublic base tier, complete participant intersection, compartment/purpose/recipient denial, and unchanged legacy operation. Include an administrator with no content grant who can perform only its scoped administrative actions and cannot self-elevate through aliases, groups, route changes or approval settings. A content reader must not edit grants.

Exercise actual supported APIs/frontends, candidate generation, provider inputs, streams, caches, source expansion, derivative lineage and restore. Verify that revocation and profile changes invalidate old contexts and that old privileged history is not reused. Include any required distinct-approver workflow and explicit single-operator capability assignments. Record exact artifact and interpreter identities, denial coverage, measured cost and every unsupported path; do not treat successful parsing or this metadata snippet as enforcement qualification. See [G01-G10](/hidden/review-12caba0b6046f6338c842cd2/#profile-implementation-and-acceptance-boundary), [H01-H23](/hidden/review-2d66666c7be62e65c7daf868/host-authorization/#qualification-and-performance) and [V1-V10](/hidden/review-2d66666c7be62e65c7daf868/validation/).
