# agents-brief.txt — AI Agent Interaction Brief
### Draft Specification v0.4.0 — March 2026

**Author:** Jasper van Veen  
**Status:** Draft  
**Repository:** https://github.com/jaspervanveen/agents-txt  
**License:** CC BY 4.0

---

## Abstract

`agents-brief.txt` is a proposed web standard that allows website owners to
declare how AI agents may discover, interact with, and act within a website or
web application. It is a natural complement to `robots.txt` (RFC 9309), which
governs passive web crawlers, and extends the web's permission model into the
era of autonomous agentic systems.

Where `robots.txt` answers *"Can you look at this?"*, `agents-brief.txt`
answers *"Here is what you can do here, how to do it, and under what terms."*

> **Note on naming history:** This project has had three names. It began as
> `agents.txt` (March 2026), renamed to `agent-manifest.txt` when an IETF
> Internet-Draft (`draft-srijal-agents-policy-00`) claimed the `agents.txt`
> filename, and finally renamed to `agents-brief.txt` after research revealed
> that "agent manifest" is already an established industry term meaning the
> *opposite* — a config file describing an agent's own identity (used by
> Microsoft Copilot, ACP, and others), not a site's declaration *for* agents.
> The full naming history and rationale is documented in §10 and in
> `naming-research.md`.

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

`agents-brief.txt` solves these problems with a simple, human- and
machine-readable file, following the spirit and syntax of `robots.txt`.

### 1.1 Why Agents Comply

A natural question is: why would agents honour `agents-brief.txt` at all?
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
`agents-brief.txt` follows the same logic, extended into an era where agents
act rather than merely read.

### 1.2 Relationship to robots.txt

`robots.txt` and `agents-brief.txt` are **complementary, not competing**
standards.

| Concern | robots.txt | agents-brief.txt |
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
`agents-brief.txt` governs interaction.

### 1.3 Industry Validation: The robots.txt Workaround Problem

This standard does not emerge from theory. Major web platforms are already
attempting to solve exactly this problem — but without a dedicated file, they
are kludging agent policy into `robots.txt`, a format not designed for it.

**eBay** added a "Robot & Agent Policy" section to its `robots.txt` in late
2025, prohibiting *"automated scraping, buy-for-me agents, LLM-driven bots, or
any end-to-end flow that attempts to place orders without human review."* The
file was updated again in early 2026 to add explicit user-agent blocks for
specific AI crawlers.

**Shopify** added a "Robots & Agent Policy" comment block to the `robots.txt`
files of all stores on its platform, stating that *"checkouts are for humans"*
and prohibiting any automated payment flow without human review.

**Amazon** updated its `robots.txt` to block specific AI agent user agents by
name.

These are three of the world's largest e-commerce platforms independently
reaching for the same workaround within months of each other. This validates
the problem; it also illustrates why a purpose-built standard is necessary.
`robots.txt` was designed for passive crawlers. It has no semantics for:

- Declaring *which* agent types are permitted for *which* actions
- Advertising API or MCP endpoints to agents that want to integrate properly
- Expressing training and RAG consent with granularity
- Providing authentication pathways for trusted agents

The current situation — critical agent policy embedded as comments inside a
30-year-old crawler exclusion file — is a gap, not a solution. This
specification provides the dedicated file these platforms need.

*Source: Modern Retail (Jan 2026), Ars Technica (Jan 2026), Praella/Shopify
analysis. See also: DataDome, "Beyond robots.txt: Exposing the Cracks in AI
Agent Policy Enforcement" (Sep 2025).*

### 1.4 Scope: What Is a "Web Agent"?

This specification uses the term **web agent** (or simply *agent*) to mean:

> Any software system that autonomously navigates, queries, or acts upon web
> resources — including HTTP endpoints, HTML pages, and APIs — typically under
> instruction from a human principal or another automated system, using an
> LLM or rule-based planner to interpret intent and generate actions.

This definition deliberately includes:

- **Agentic AI assistants** (e.g. OpenAI Operator, Anthropic Claude computer-
  use, Google Gemini with tool use) that browse the web on a user's behalf
- **Autonomous purchasing or booking agents** that complete end-to-end
  transactions
- **Research and RAG agents** that retrieve and synthesise web content
- **AI-powered scraping pipelines** that extract structured data at scale
- **MCP-connected agents** that interact with sites via Model Context Protocol
  server endpoints

This definition **excludes**:

- Traditional search engine crawlers and indexers (governed by `robots.txt`,
  RFC 9309)
- Human users interacting via web browsers
- Enterprise IAM "web agents" (e.g. Broadcom SiteMinder, Oracle OpenSSO) —
  server-side authentication proxies unrelated to this standard
- Reinforcement learning agents operating in simulated or game environments —
  "agent policy" in that domain refers to an RL decision function, not a web
  access declaration

The distinction matters: `robots.txt` governs *access by crawlers*. This
specification governs *interaction by agents*. A crawler reads. An agent acts.

---

## 2. File Location and Discovery

An `agents-brief.txt` file MUST be placed at the root of the web origin:

```
https://example.com/agents-brief.txt
```

Agents SHOULD retrieve the file via HTTP GET before interacting with a site.
The file MUST be served with `Content-Type: text/plain; charset=utf-8`.

Redirects (HTTP 301/302) MUST be followed, up to a maximum of 5 hops.

If no `agents-brief.txt` file is present (HTTP 404), agents SHOULD assume
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
# agents-brief.txt for ExampleShop
# https://exampleshop.com/agents-brief.txt

Site-Name: ExampleShop
Site-Description: Online marketplace for sustainable home goods. Supports browsing, search, and checkout for verified agents.
Contact: agents@exampleshop.com
Terms: https://exampleshop.com/legal/agent-terms

# Data use
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

`agents-brief.txt` is a *declaration*, not a technical enforcement mechanism.
Compliant agents SHOULD respect its contents. Sites MUST NOT rely solely on
`agents-brief.txt` for security — access controls and authentication MUST be
enforced server-side.

However, `agents-brief.txt` is not merely aspirational. A published,
machine-readable policy changes the legal posture around non-compliance:

- Violation of a declared `agents-brief.txt` policy may constitute a breach
  of the site's Terms of Service, which can support Computer Fraud and Abuse
  Act (CFAA) claims in the US and equivalent Computer Misuse Act claims in the
  UK and EU jurisdictions.
- "The agent ignored your published access policy" is a substantially cleaner
  legal argument than relying on implicit expectations alone.

Sites that wish to preserve these claims SHOULD ensure their `agents-brief.txt`
policy is referenced from or consistent with their Terms of Service.

### 7.2 Agent Identity

Agent identifiers in section headers are self-declared strings. There is
currently no cryptographic verification of agent identity in this v0.4 spec.
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
| `agents-brief.txt` (this spec) | AI agent interaction brief | Agentic interaction |

`llms.txt` is a content-oriented standard that helps LLMs understand what a
site contains. `agents-brief.txt` is an *interaction-oriented* standard that
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

A closely related proposal using the same core premise: "robots.txt tells
agents what NOT to do; agents.txt tells them what they CAN do." Ships as a
TypeScript/npm package with MCP integration and a `/.well-known/agents.txt`
path.

Example from that project:
```
Capability: product-search
  Endpoint: https://mystore.com/api/search
  Method: GET
  Protocol: REST
  Auth: none
  Rate-Limit: 60/minute
```

**Distinction from this spec:** Implementation-first rather than
specification-first. Lacks formal rationale, security considerations, a
versioning model, or a standardisation path. Compatible and could converge.

---

**`muzz-yasir/agents.txt`** (January 2025)  
GitHub: https://github.com/muzz-yasir/agents.txt

Focused on agent authentication and access control. Inactive since publication.

---

**`draft-srijal-agents-policy-00`** — *IETF Internet-Draft* (October 2025, expires April 2026)  
Author: Srijal Dutta (independent)  
URL: https://www.ietf.org/archive/id/draft-srijal-agents-policy-00.html

An IETF Internet-Draft using the `agents.txt` filename. It addresses tamper-
evident path-level access control for automated clients via mandatory SHA-256
hash verification. Any hash mismatch causes the site to be treated as fully
restricted.

Example from that draft:
```
*e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
/status ALLOW
/dashboard ALLOW limit=50
/admin DISALLOW
```

**Distinction from this spec:** Essentially a stricter, integrity-verified
robots.txt. Answers only: *"Can this automated client access this path?"* No
agent identity tiers, agentic actions, API/MCP discovery, training consent,
tiered rate limits, or authentication methods. The crowding of the `agents.txt`
namespace by this draft was a factor in renaming this specification.

As of March 2026, this draft has not progressed beyond initial submission and
expires April 2026 with no visible community engagement.

---

**`globalchatads/agents-txt`** (March 2026)  
GitHub: https://github.com/globalchatads/agents-txt  
Live implementation: https://www.global-chat.io/agents-txt

Oriented toward agent marketplace dynamics and on-chain payments. Uses a
section-header format with USDC wallet registration and per-endpoint rate
limits.

Example from that project:
```
## PAYMENT METHODS
Payment: USDC on Base (Chain ID: 8453)
Payment-Wallet: 0x1234...abcd
Min-Bid: 1.00 USDC
```

**Distinction from this spec:** Crypto-native payment rails as a first-class
concern. This specification focuses on the broader permission and discovery
layer without prescribing a payment mechanism — the two are complementary.
The author provided substantive commentary on open questions 1–3 in this spec
(see §11 and [dev.to](https://dev.to/jaspervanveen/agentstxt-a-proposed-web-standard-for-ai-agents-20lb)).

---

**Agent Manifest Protocol (AMP)** — `agent-manifest.com` (2025)  
URL: https://agent-manifest.com  
Spec: `/.well-known/agent-manifest.json`

A live protocol for autonomous API onboarding. A site publishes a JSON manifest
declaring authentication flows, capabilities, and pricing; an agent fetches it
and integrates the API without human configuration.

Example structure:
```json
{
  "auth": { "type": "oauth2", "flow": "client_credentials" },
  "capabilities": ["search", "pricing"],
  "pricing": { "model": "per-call", "currency": "USD" }
}
```

**Distinction from this spec:** JSON-only, API/auth-focused. No training/RAG
consent, tiered agent permissions, plain-text readability, or rate limiting by
agent type. The two are complementary: AMP handles API-level integration; this
spec handles site-level policy declaration.

---

**Industry practice: eBay, Shopify, Amazon** (2025–2026)

The most significant validation of this proposal's thesis is commercial. Three
of the world's largest e-commerce platforms have independently moved to declare
agent access policy within the same six-month window — all using `robots.txt`
because no dedicated standard exists.

- **eBay**: Added "Robot & Agent Policy" to `robots.txt`, prohibiting buy-for-me
  agents and automated order placement without human review.
- **Shopify**: Added "Robots & Agent Policy" across all store `robots.txt` files.
  States "checkouts are for humans."
- **Amazon**: Updated `robots.txt` to explicitly block named AI agent user agents.

**This is the core pitch:** `agents-brief.txt` is the dedicated file these
platforms need but are approximating inside `robots.txt`. The problem is
proven. The solution is not yet standardised.

---

**Summary:** The concept behind this specification has been independently
conceived by multiple authors across community projects, industry platforms, and
formal standards bodies — strongly validating the underlying need. No existing
effort has produced a complete, formally-reasoned specification with a clear
standardisation path. This document aims to fill that gap.

---

## 9. Versioning

This document describes `agents-brief.txt` version 0.4.0 (draft). The version
may be declared explicitly in the file:

```
Agents-Brief-Version: 0.4.0
```

---

## 10. On the Filename: Naming History

This specification has had three names, each change documented with full
research. The complete naming research is in `naming-research.md`.

### 10.1 Chapter 1: `agents.txt` (v0.1–v0.2, March 2026)

The original name, chosen as a direct analogy to `robots.txt`. Dropped in
March 2026 because the `agents.txt` namespace had become crowded:

- **IETF clash**: `draft-srijal-agents-policy-00` claimed the `agents.txt`
  filename at IETF (October 2025, expires April 2026)
- **Community projects**: at least four independent projects used the same
  filename for different purposes (dennj, kaylacar, muzz-yasir, globalchatads)

### 10.2 Chapter 2: `agent-manifest.txt` (v0.3.0, March 2026)

Intended to be more precise. Abandoned after research revealed a deeper problem:
**"agent manifest" is already an established industry term meaning the exact
opposite of what this file does.**

In 2025–2026, "agent manifest" solidified as the standard term for a config
file describing *an agent's own identity and capabilities* — metadata **by**
an agent, **about** an agent:

- **Microsoft Security Copilot** and **Microsoft 365 Copilot**: official "agent
  manifest" format (YAML/JSON defining agent instructions and skills)
- **Agent Communication Protocol (ACP)**: "Agent Manifest" = agent identity,
  capabilities, and metadata declaration
- **agent-manifest.org**: "Agent Definition Schema — Standardizing the Way
  Agents Describe Themselves"
- **agent-manifest.com** (AMP): `/.well-known/agent-manifest.json` for
  autonomous API onboarding
- **agent-manifest-spec.org**: "Agent Manifest v1.0 — agent identity, authority,
  scope, constraints"

This specification is the *opposite*: a website declaring policy *for* agents
visiting it. Keeping `agent-manifest.txt` would actively mislead the target
audience.

### 10.3 Chapter 3: `agents-brief.txt` (v0.4.0, March 2026 — current)

Selected after extensive synonym analysis across two dimensions (agent-word
variants × document-type variants) and a deep prior-art check across IETF,
IANA, GitHub, Wikipedia, academic sources, trademark databases, and brand names.

**Why "brief":**

A brief — in professional use — is the document you read before you begin: it
covers permissions, boundaries, available tools, contacts, and terms, all in
one structured document. This is precisely what `agents-brief.txt` contains:

- Permissions (Allow/Disallow, Allow-Actions)
- Boundaries (Rate-Limit, Auth-Required)
- Available tools (MCP-Server, API-Docs, Capabilities)
- Contacts (Contact, Terms)
- Data use terms (Allow-Training, Allow-RAG, Allow-Scraping)

No other single word in the research covered all four functional dimensions of
the spec. "Rules" covers access control but not discovery. "Terms" covers
consent but not capability advertisement. "Brief" covers both — and everything
else.

**Why plural (`agents-brief.txt`, not `agent-brief.txt`):**

Following the precedent of `robots.txt`, `llms.txt`, and `humans.txt`: when
the filename names the *audience* (the class of entities the file addresses),
it is plural. `agents-brief.txt` — brief for agents — mirrors `robots.txt`
(rules for robots) directly.

**Prior art check (March 2026):**
- IETF Datatracker: ✅ zero matches
- IANA Well-Known URIs: ✅ not registered
- GitHub filename search: ✅ zero files named `agents-brief.txt`
- Wikipedia: ✅ no article
- Academic: ✅ no named standard or format
- Brand names: ⚠️ `agentbrief.com` exists (real estate SaaS, unrelated)
- Trademark databases: ⚠️ manual verification recommended (USPTO/EUIPO/WIPO)

### 10.4 Alternatives Considered (Final Round)

| Filename | Ruled out because |
|---|---|
| `agents.txt` | IETF I-D clash; namespace crowded |
| `agent-manifest.txt` | "Agent manifest" means config-file-about-an-agent |
| `agent-policy.txt` | "Agent policy" = RL decision function; eBay/Shopify already use the phrase informally inside robots.txt |
| `agent-rules.txt` | Active AGENTS.md coding-agent ecosystem uses "agent rules" |
| `agent-terms.txt` | Partially clean, but undersells discovery half of spec |
| `webagent-policy.txt` | SiteMinder enterprise IAM collision ("web agent") |
| `agents-brief.txt` | **Selected** — see above |

---

## 11. Open Questions (for community discussion)

Tracked as GitHub issues at https://github.com/jaspervanveen/agents-txt/issues

1. **Agent identity verification** — How should agent identity be verified
   beyond self-declaration? A W3C Verifiable Credentials / DID-based approach
   has been proposed. → [Issue #1](https://github.com/jaspervanveen/agents-txt/issues/1)

2. **Capability vocabulary** — Controlled vocabulary or free-form strings?
   A controlled core vocabulary with an IANA-style extension registry has been
   proposed. → [Issue #2](https://github.com/jaspervanveen/agents-txt/issues/2)

3. **Conflict resolution / robots.txt cross-reference** — When `robots.txt`
   and `agents-brief.txt` both exist on a domain, which governs path-level
   access? Proposed rule: `robots.txt` governs crawl/read; `agents-brief.txt`
   governs actions. → [Issue #3](https://github.com/jaspervanveen/agents-txt/issues/3)

4. **Monetary terms** — Should `agents-brief.txt` support declaring pricing
   for automated access (pay-per-call APIs)?

5. **MCP integration depth** — Current position: shallow integration —
   `agents-brief.txt` serves as the *discovery layer* (where is the MCP
   endpoint?), while MCP handles everything from transport negotiation onward.

*Community input on questions 1–3 was provided by [@globalchatads](https://github.com/globalchatads)
in a comment on the [dev.to article](https://dev.to/jaspervanveen/agentstxt-a-proposed-web-standard-for-ai-agents-20lb)
on 2026-03-21.*

---

## 12. Acknowledgements

This specification was conceived by **Jasper van Veen** in March 2026 as part
of broader work on AI infrastructure. The author recognises the foundational
work of Martijn Koster (robots.txt, 1994) and the IETF working group that
produced RFC 9309.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 0.1.0 | 2026-03-09 | Initial draft (as `agents.txt`) |
| 0.1.1 | 2026-03-10 | Agent compliance rationale; legal posture; prior art (dennj, kaylacar, muzz-yasir) |
| 0.1.2 | 2026-03-14 | `llms.txt` comparison and table |
| 0.1.3 | 2026-03-14 | IETF AIPREF WG reference |
| 0.1.4 | 2026-03-14 | IETF WEBBOTAUTH WG reference |
| 0.1.5 | 2026-03-20 | §10 naming rationale and alternatives |
| 0.2.0 | 2026-03-22 | globalchatads prior art; community input on open questions |
| 0.3.0 | 2026-03-27 | **Renamed `agents.txt` → `agent-manifest.txt`**; §1.3 industry validation (eBay/Shopify/Amazon); §1.4 web agent definition; AMP and industry practice added to §8.2 |
| 0.4.0 | 2026-03-27 | **Renamed `agent-manifest.txt` → `agents-brief.txt`** — "agent manifest" found to mean the opposite (config file about an agent, not for agents). Full naming history documented in §10. All references updated. Version directive updated to `Agents-Brief-Version`. |

---

*This specification is published under the Creative Commons Attribution 4.0
International License (CC BY 4.0). You are free to share and adapt it with
attribution.*
