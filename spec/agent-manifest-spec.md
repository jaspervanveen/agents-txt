# agent-manifest.txt — AI Agent Interface Declaration Standard
### Draft Specification v0.3.0 — March 2026

**Author:** Jasper van Veen  
**Status:** Draft  
**Repository:** https://github.com/jaspervanveen/agents-txt  
**License:** CC BY 4.0

---

## Abstract

`agent-manifest.txt` is a proposed web standard that allows website owners to
declare how AI agents may discover, interact with, and act on their behalf
within a website or web application. It is a natural complement to `robots.txt`
(RFC 9309), which governs passive web crawlers, and extends the web's permission
model into the era of autonomous agentic systems.

Where `robots.txt` answers *"Can you look at this?"*, `agent-manifest.txt`
answers *"Here is what you can do here, how to do it, and under what terms."*

> **Note on naming history:** This project was originally named `agents.txt`,
> derived directly from `robots.txt` by analogy. The name was changed in March
> 2026 to `agent-manifest.txt` after discovering that the `agents.txt` namespace
> had become crowded: an independent IETF Internet-Draft
> (`draft-srijal-agents-policy-00`) had already claimed the `agents.txt`
> filename at IETF, and multiple community projects were using the same name for
> different purposes. The new name more accurately reflects the document's
> purpose — a rich capability *manifest* rather than a simple access-control
> list — while avoiding naming conflicts on the standardisation path.

---

## 1. Introduction

The web was built for humans. Its permission model — `robots.txt`, `meta robots`,
`noindex` — was designed for passive, read-only crawlers and search indexers.

AI agents are fundamentally different. They do not merely read content: they
reason, decide, and act. An agent may book a flight, submit a form, call an API,
authenticate as a user, or transact on behalf of a person. None of this is
addressed by `robots.txt`.

The absence of a standard creates real problems:

- Sites have no machine-readable way to declare what agents are *allowed to do*
- Agents have no reliable way to discover a site's capabilities or preferred
  interface (HTML vs. REST API vs. MCP server)
- There is no standard mechanism for sites to express consent for AI training,
  retrieval-augmented generation (RAG), or automated scraping
- There is no tiered trust model: a read-only research agent and a
  transaction-executing purchasing agent are treated identically

`agent-manifest.txt` solves these problems with a simple, human- and
machine-readable file, following the spirit and syntax of `robots.txt`.

### 1.1 Why Agents Comply

A natural question is: why would agents honour `agent-manifest.txt` at all?
The answer operates on two levels.

**Self-interested compliance.** When a site declares a preferred interface —
particularly an MCP server or REST API — a well-built agent *actively wants*
to use it. Calling a structured API is faster, more reliable, and lower risk
than parsing HTML. A site offering `MCP-Server: https://mcp.example.com` is
not asking agents for a favour; it is giving them a better option. Compliance
here is not ethical concession — it is rational behaviour.

**Legal enforceability.** Once a machine-readable policy exists, ignoring it
becomes legally actionable. Operators can cite ToS violations more cleanly, and
"you had a published standard and the agent ignored it" substantially
strengthens CFAA and Computer Misuse Act arguments. The existence of a standard
changes the legal landscape for non-compliant actors, even if it cannot stop
them technically.

This mirrors the trajectory of `robots.txt`: the standard was not enforceable
in 1994, but it created a common language for good actors — and that ecosystem
has grown larger than the ecosystem of bad actors ever since.
`agent-manifest.txt` follows the same logic, extended into an era where agents
act rather than merely read.

### 1.2 Relationship to robots.txt

`robots.txt` and `agent-manifest.txt` are **complementary, not competing**
standards.

| Concern | robots.txt | agent-manifest.txt |
|---|---|---|
| Crawl permissions | ✅ | — |
| Crawl rate limiting | ✅ | — |
| Sitemap location | ✅ | — |
| Agent capabilities | — | ✅ |
| Action permissions | — | ✅ |
| API / MCP discovery | — | ✅ |
| Training / RAG consent | — | ✅ |
| Agent identity tiers | — | ✅ |
| Authentication methods | — | ✅ |

Sites SHOULD maintain both files. `robots.txt` governs crawling;
`agent-manifest.txt` governs interaction.

---

## 2. File Location and Discovery

An `agent-manifest.txt` file MUST be placed at the root of the web origin:

```
https://example.com/agent-manifest.txt
```

Agents SHOULD retrieve the file via HTTP GET before interacting with a site.
The file MUST be served with `Content-Type: text/plain; charset=utf-8`.

Redirects (HTTP 301/302) MUST be followed, up to a maximum of 5 hops.

If no `agent-manifest.txt` file is present (HTTP 404), agents SHOULD assume
default permissive behaviour for read-only access and default restrictive
behaviour for actions.

---

## 3. File Format

### 3.1 Syntax

The file uses an INI-inspired, line-based format:

- Lines beginning with `#` are comments and MUST be ignored
- Directives follow the format `Key: Value`
- Blank lines are ignored
- Keys are case-insensitive; values are case-sensitive unless noted
- Sections are declared as `[Agent: <identifier>]` where `*` is a wildcard
- Sections apply to all directives that follow until the next section header

### 3.2 Encoding

Files MUST be encoded in UTF-8. Lines SHOULD be terminated with CRLF (`\r\n`)
or LF (`\n`).

---

## 4. Global Directives

Global directives appear before any `[Agent]` section and apply to all agents
unless overridden.

### 4.1 Identity

**`Site-Name`** *(optional)*  
Human-readable name of the site or service.  
Example: `Site-Name: ExampleCorp`

**`Site-Description`** *(optional)*  
A brief natural-language description of the site's purpose. This field is
intended to give LLMs and agents meaningful context without parsing HTML.  
Example: `Site-Description: B2B SaaS platform for design workflow automation`

**`Contact`** *(optional)*  
Email address or URL for agent-related enquiries.  
Example: `Contact: agents@example.com`

**`Terms`** *(optional)*  
URL to the site's terms of service for automated/agent access.  
Example: `Terms: https://example.com/agents-terms`

### 4.2 Data Use

**`Allow-Training`** *(optional, default: no)*  
Whether the site's content may be used to train AI/ML models.  
Values: `yes` | `no` | `ask`  
Example: `Allow-Training: no`

**`Allow-RAG`** *(optional, default: yes)*  
Whether the site's content may be used in retrieval-augmented generation
(RAG) pipelines.  
Values: `yes` | `no` | `ask`  
Example: `Allow-RAG: yes`

**`Allow-Scraping`** *(optional, default: yes)*  
Whether automated extraction of structured data is permitted.  
Values: `yes` | `no` | `ask`  
Example: `Allow-Scraping: yes`

### 4.3 Interface Discovery

**`Allow-Actions`** *(optional, default: no)*  
Whether agents may perform write operations (form submissions, purchases,
bookings, etc.).  
Values: `yes` | `no` | `ask`  
Example: `Allow-Actions: yes`

**`Preferred-Interface`** *(optional)*  
The preferred interaction method for agents.  
Values: `html` | `rest` | `graphql` | `mcp` | `rpc`  
Example: `Preferred-Interface: rest`

**`API-Docs`** *(optional)*  
URL to machine-readable API documentation (OpenAPI, GraphQL schema, etc.).  
Example: `API-Docs: https://api.example.com/openapi.json`

**`MCP-Server`** *(optional)*  
URL to a Model Context Protocol (MCP) server endpoint, if available.  
This is the preferred mechanism for capable agents.  
Example: `MCP-Server: https://mcp.example.com`

**`Capabilities`** *(optional, repeatable)*  
Declares specific high-level capabilities available to agents.  
Example:
```
Capabilities: search
Capabilities: browse-catalog
Capabilities: get-pricing
Capabilities: check-availability
```

---

## 5. Agent Sections

Agent sections allow differentiated rules per agent type. They begin with a
section header and apply until the next section header or end of file.

```
[Agent: *]
```

The identifier may be:
- `*` — applies to all agents (wildcard)
- A specific agent identifier string (e.g. `openai-operator`, `claude-agent`)
- A prefix with wildcard (e.g. `openai-*`)

More specific rules take precedence over less specific rules. `[Agent: *]` is
the fallback.

### 5.1 Per-Agent Directives

**`Allow`** *(optional, repeatable)*  
URL path prefix that this agent type is permitted to access or act upon.  
Example: `Allow: /products/*`

**`Disallow`** *(optional, repeatable)*  
URL path prefix that this agent type is NOT permitted to access or act upon.  
Example: `Disallow: /admin`

**`Rate-Limit`** *(optional)*  
Maximum number of requests per time window.  
Format: `<n>/<unit>` where unit is `second`, `minute`, `hour`, or `day`.  
Example: `Rate-Limit: 60/minute`

**`Auth-Required`** *(optional, default: no)*  
Whether authentication is required for this agent tier.  
Values: `yes` | `no`

**`Auth-Method`** *(optional)*  
Authentication method to use when `Auth-Required: yes`.  
Values: `api-key` | `oauth2` | `bearer` | `basic` | `mtls`  
Example: `Auth-Method: oauth2`

**`Auth-Endpoint`** *(optional)*  
URL to the authentication endpoint.  
Example: `Auth-Endpoint: https://api.example.com/oauth/token`

**`Allow-Actions`** *(optional)*  
Override the global `Allow-Actions` setting for this agent type.

---

## 6. Complete Example

```
# agent-manifest.txt for ExampleShop
# https://exampleshop.com/agent-manifest.txt

Site-Name: ExampleShop
Site-Description: Online marketplace for sustainable home goods. Supports browsing, search, and checkout for verified agents.
Contact: agents@exampleshop.com
Terms: https://exampleshop.com/legal/agent-terms

# Data use policy
Allow-Training: no
Allow-RAG: yes
Allow-Scraping: yes

# Interface
Allow-Actions: no
Preferred-Interface: rest
API-Docs: https://api.exampleshop.com/openapi.json
MCP-Server: https://mcp.exampleshop.com

Capabilities: search
Capabilities: browse-catalog
Capabilities: get-pricing
Capabilities: check-availability

# Default rules for all agents
[Agent: *]
Allow: /products/*
Allow: /search
Allow: /categories/*
Disallow: /admin
Disallow: /account
Disallow: /checkout
Rate-Limit: 30/minute
Auth-Required: no

# Verified purchasing agents (registered with ExampleShop)
[Agent: verified-purchasing-agent]
Allow: /products/*
Allow: /search
Allow: /cart
Allow: /checkout
Allow: /account/orders
Disallow: /admin
Rate-Limit: 10/minute
Auth-Required: yes
Auth-Method: oauth2
Auth-Endpoint: https://api.exampleshop.com/oauth/token
Allow-Actions: yes
```

---

## 7. Security Considerations

### 7.1 Trust and Compliance

`agent-manifest.txt` is a *declaration*, not a technical enforcement mechanism.
Compliant agents SHOULD respect its contents. Sites MUST NOT rely solely on
`agent-manifest.txt` for security — access controls and authentication MUST be
enforced server-side.

However, `agent-manifest.txt` is not merely aspirational. A published,
machine-readable policy changes the legal posture around non-compliance:

- Violation of a declared `agent-manifest.txt` policy may constitute a breach
  of the site's Terms of Service, which can support Computer Fraud and Abuse
  Act (CFAA) claims in the US and equivalent Computer Misuse Act claims in the
  UK and EU jurisdictions.
- "The agent ignored your published access policy" is a substantially cleaner
  legal argument than relying on implicit expectations alone.

Sites that wish to preserve these claims SHOULD ensure their `agent-manifest.txt`
policy is referenced from or consistent with their Terms of Service.

### 7.2 Agent Identity

Agent identifiers in section headers are self-declared strings. There is
currently no cryptographic verification of agent identity in this v0.3 spec.
Future versions may incorporate signed agent certificates or W3C Verifiable
Credentials for verified agent identity.

### 7.3 Sensitive Paths

Sites SHOULD use `Disallow` to explicitly protect sensitive paths even if they
are protected by authentication. Defense in depth is recommended.

---

## 8. Comparison with Related Standards

### 8.1 Established standards

| Standard | Purpose | Scope |
|---|---|---|
| `robots.txt` (RFC 9309) | Crawl permissions for search bots | Read-only crawling |
| `llms.txt` (Answer.AI, 2024) | LLM-readable site summary | Content discovery |
| `security.txt` (RFC 9116) | Security disclosure contacts | Security reporting |
| `agent-manifest.txt` (this spec) | AI agent capabilities & permissions | Agentic interaction |

`llms.txt` is a content-oriented standard that helps LLMs understand what a
site contains. `agent-manifest.txt` is an *interaction-oriented* standard that
tells agents what they may do and how. They are complementary.

### 8.2 Related prior art

Several independent efforts have explored this problem space, many originally
under the `agents.txt` filename. This section documents them and clarifies how
this specification relates.

---

**`dennj/agents.txt`** — *agentstxt.dev* (March 2025)  
GitHub: https://github.com/dennj/agents.txt

This project uses the `agents.txt` filename for a different purpose: declaring
the AI *services a site offers* to other agents — a B2A (Business-to-Agent)
discovery mechanism. Its format advertises outbound agent capabilities
(communication protocols, payment systems) rather than governing what inbound
agents may do on the site.

Example from that project:
```
Agent: MyAIService
Description: AI service for automated customer support
Communication-Protocol: WebSocket, HTTP
Payment-System: Stripe, PayPal
```

**Distinction from this spec:** That project is an *agent directory* — a way
for sites to say "here are the AI services we provide." This specification
addresses the inverse: *what visiting agents are permitted to do here, and how*.
The two are complementary and could coexist.

---

**`kaylacar/agents-txt`** (March 2026)  
GitHub: https://github.com/kaylacar/agents-txt

A closely related proposal that shares the same core premise: "robots.txt tells
agents what NOT to do; agents.txt tells them what they CAN do." This project
ships as a TypeScript/npm package (`@agents-txt/express`) with MCP integration
and uses a `/.well-known/agents.txt` path. Its format uses structured
`Capability:` blocks with endpoints and authentication.

Example from that project:
```
Capability: product-search
  Endpoint: https://mystore.com/api/search
  Method: GET
  Protocol: REST
  Auth: none
  Rate-Limit: 60/minute
```

**Distinction from this spec:** That project is implementation-first (an npm
library) rather than specification-first. It lacks formal rationale, security
considerations, a versioning model, or a path toward standardisation. This
specification prioritises the standard over any particular implementation,
with the goal of eventual IETF or W3C adoption. The two approaches are
compatible and could converge.

---

**`muzz-yasir/agents.txt`** (January 2025)  
GitHub: https://github.com/muzz-yasir/agents.txt

Focused specifically on agent authentication and access control. Inactive
since publication.

---

**`draft-srijal-agents-policy-00`** — *IETF Internet-Draft* (October 2025, expires April 2026)  
Author: Srijal Dutta (independent)  
URL: https://www.ietf.org/archive/id/draft-srijal-agents-policy-00.html

This IETF Internet-Draft uses the `agents.txt` filename and shares a surface
resemblance to robots.txt, but addresses a fundamentally different problem:
tamper-evident path-level access control for automated clients. Its core
mechanism is a mandatory SHA-256 hash of the file's directive content, placed
on the first non-comment line. Any hash mismatch or syntax error causes the
entire site to be treated as fully restricted.

Example from that draft:
```
*e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
/status ALLOW
/dashboard ALLOW limit=50
/admin DISALLOW
```

**Distinction from this spec:** That draft is essentially a stricter,
integrity-verified robots.txt. It answers a single question: *"Can this
automated client access this path?"* It contains no concept of agent identity
tiers, agentic actions, API or MCP discovery, training and RAG consent, rate
limiting by agent type, authentication methods, or site capability declaration.
It treats all automated clients identically and provides no mechanism for the
richer agent↔site relationship that characterises modern AI systems.

This specification addresses that broader relationship. The two proposals operate
at different layers: Dutta's draft is an access-control mechanism; this
specification is an interaction protocol. They are not competing standards —
they are solutions to different problems.

As of March 2026, `draft-srijal-agents-policy-00` has not progressed beyond
its initial submission and is due to expire in April 2026 with no visible
community engagement or renewal activity. The crowding of the `agents.txt`
namespace — between this draft and the community projects above — was a
significant factor in renaming this specification to `agent-manifest.txt`.

---

**`globalchatads/agents-txt`** (March 2026)
GitHub: https://github.com/globalchatads/agents-txt
Live implementation: https://www.global-chat.io/agents-txt

A practical implementation of the `agents-txt` concept, oriented toward **agent
marketplace dynamics and on-chain payments**. Uses a section-header format
(IDENTITY, AUTHENTICATION, ENDPOINTS, PAYMENT METHODS) and requires a JSON
companion file at `/.well-known/agents`. Supports wallet registration, USDC
payments on Base, and per-endpoint rate limits. Includes a TypeScript validator
and is deployed on the author's own platform.

Example from that project:
```
## PAYMENT METHODS
Payment: USDC on Base (Chain ID: 8453)
Payment-Wallet: 0x1234...abcd
Min-Bid: 1.00 USDC
```

**Distinction from this spec:** That project targets an agent economy with
crypto-native payment rails as a first-class concern. This specification focuses
on the broader permission and discovery layer — training consent, auth methods,
rate limiting, MCP discovery — without prescribing a payment mechanism. The two
are complementary: this spec could serve as the foundation layer on which
payment-enabled extensions are built. The author provided substantive technical
commentary on open questions 1–3 in this spec (see §11 and
[dev.to](https://dev.to/jaspervanveen/agentstxt-a-proposed-web-standard-for-ai-agents-20lb)).

---

**Summary:** The `agents.txt` concept has been independently conceived by
multiple authors, which strongly suggests the need is real. No existing effort
has produced a complete, formally-reasoned specification or pursued a standards
track. This document — now under the name `agent-manifest.txt` — aims to fill
that gap.

---

## 9. Versioning

This document describes `agent-manifest.txt` version 0.3.0 (draft). The version
may be declared explicitly:

```
Agent-Manifest-Version: 0.3.0
```

---

## 10. On the Filename

### 10.1 History: from `agents.txt` to `agent-manifest.txt`

This specification was originally named `agents.txt`, chosen for its intuitive
parallel to `robots.txt`. In March 2026, it was renamed to `agent-manifest.txt`
for the following reasons:

**Namespace crowding.** As documented in §8.2, the `agents.txt` filename had
been independently adopted by at least four community projects and claimed in
an IETF Internet-Draft (`draft-srijal-agents-policy-00`). The collision risk
on the formal standardisation path made a cleaner name preferable.

**Accuracy.** "Manifest" better reflects what this file actually does. Unlike
`robots.txt` (an exclusion list) or `agents.txt` as used by prior-art projects
(typically access-control lists), this file is a rich capability and policy
*manifest* — declaring capabilities, permissions, API endpoints, authentication
methods, training consent, and agent tiers in a single document.

**IETF precedent.** The term "manifest" has established precedent in web
standards (Web App Manifest, W3C; `funding-manifest-urls`, IANA). Filing under
a clean name avoids immediate naming disputes in the IETF process.

### 10.2 Alternative Filenames Considered

The following alternatives were evaluated in March 2026:

| Filename | Character |
|---|---|
| `agent-manifest.txt` | **Selected.** Manifest pattern, accurate, no prior art |
| `agentpolicy.txt` | Policy-forward, IETF-friendly |
| `aipermit.txt` | Permission-forward, memorable |
| `aimanifest.txt` | Similar to selected; slightly less precise |
| `agentaccess.txt` | Access-control framing |
| `aiconsent.txt` | Consent and data-use emphasis |
| `agentlicense.txt` | Licensing lens |
| `machinepolicy.txt` | Broadest scope, technology-neutral |

All alternatives above were confirmed to have zero prior art on GitHub and no
active IETF drafts at the time of writing.

---

## 11. Open Questions (for community discussion)

The following questions have been raised by the community and are tracked as
GitHub issues at https://github.com/jaspervanveen/agents-txt/issues

1. **Agent identity verification** — How should agent identity be verified
   beyond self-declaration? A W3C Verifiable Credentials / DID-based approach
   has been proposed, where agents present operator-signed credentials combined
   with domain-level allowlists. → [Issue #1](https://github.com/jaspervanveen/agents-txt/issues/1)

2. **Capability vocabulary** — Should capabilities be a defined controlled
   vocabulary, or free-form strings? A controlled core vocabulary with an
   IANA-style extension registry has been proposed. → [Issue #2](https://github.com/jaspervanveen/agents-txt/issues/2)

3. **Conflict resolution / robots.txt cross-reference** — When `robots.txt`
   and `agent-manifest.txt` both exist on a domain, which governs path-level
   access? Proposed rule: robots.txt governs crawl/read access;
   `agent-manifest.txt` governs actions. → [Issue #3](https://github.com/jaspervanveen/agents-txt/issues/3)

4. **Monetary terms** — Should `agent-manifest.txt` support declaring pricing
   for automated access (pay-per-call APIs)?

5. **MCP integration depth** — As MCP gains adoption, should this spec more
   tightly integrate with the MCP standard? Current position: keep integration
   shallow — `agent-manifest.txt` serves as the *discovery layer*, while MCP
   handles everything from transport negotiation onward.

*Community input on questions 1–3 was provided by [@globalchatads](https://github.com/globalchatads)
in a comment on the [dev.to article](https://dev.to/jaspervanveen/agentstxt-a-proposed-web-standard-for-ai-agents-20lb)
on 2026-03-21.*

---

## 12. Acknowledgements

This specification was conceived by **Jasper van Veen** in March 2026 as part
of broader work on AI infrastructure.
The author recognises the foundational work of Martijn Koster (robots.txt, 1994)
and the IETF working group that produced RFC 9309.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 0.1.0 | 2026-03-09 | Initial draft (as `agents.txt`) |
| 0.1.1 | 2026-03-10 | Added §1.1 agent incentives & compliance rationale; expanded §7.1 legal posture; added related prior art (dennj, kaylacar, muzz-yasir) |
| 0.1.2 | 2026-03-14 | Expanded §1.2 to cover relationship with `llms.txt`; updated comparison table |
| 0.1.3 | 2026-03-14 | Added IETF AIPREF WG reference and overlap analysis |
| 0.1.4 | 2026-03-14 | Added IETF WEBBOTAUTH WG reference and full IETF landscape table |
| 0.1.5 | 2026-03-20 | Added §10 on filename rationale and alternatives |
| 0.2.0 | 2026-03-22 | Added globalchatads/agents-txt to prior art; community input on open questions |
| 0.3.0 | 2026-03-27 | **Renamed from `agents.txt` to `agent-manifest.txt`**; updated all references; added naming history to §10; updated §8.2 summary to reflect rename rationale |

---

*This specification is published under the Creative Commons Attribution 4.0
International License (CC BY 4.0). You are free to share and adapt it with
attribution.*
