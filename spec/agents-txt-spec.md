# agents.txt — AI Agent Interface Declaration Standard
### Draft Specification v2.1 — March 2026

**Author:** Jasper van Veen  
**Status:** Draft  
**Repository:** https://github.com/jaspervanveen/agents-txt *(proposed)*  
**License:** CC BY 4.0

---

## Abstract

`agents.txt` is a proposed web standard that allows website owners to declare
how AI agents may discover, interact with, and act on their behalf within a
website or web application. It is a natural complement to `robots.txt` (RFC 9309),
which governs passive web crawlers, and extends the web's permission model into
the era of autonomous agentic systems.

Where `robots.txt` answers *"Can you look at this?"*, `agents.txt` answers
*"Here is what you can do here, how to do it, and under what terms."*

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

`agents.txt` solves these problems with a simple, human- and machine-readable
file, following the spirit and syntax of `robots.txt`.

### 1.1 Why Agents Comply

A natural question is: why would agents honour `agents.txt` at all? The answer
operates on two levels.

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
has grown larger than the ecosystem of bad actors ever since. `agents.txt`
follows the same logic, extended into an era where agents act rather than
merely read.

### 1.2 Relationship to Existing Standards

`agents.txt` is **complementary to, not competing with** existing web standards.
A well-configured site in the agentic era should maintain all three files below,
each serving a distinct and non-overlapping purpose.

| Concern | `robots.txt` | `llms.txt` | `agents.txt` |
|---|---|---|---|
| Crawl permissions | ✅ | — | — |
| Crawl rate limiting | ✅ | — | — |
| Sitemap location | ✅ | — | — |
| Content summary for LLMs | — | ✅ | — |
| Key pages / structure for AI | — | ✅ | — |
| Action permissions | — | — | ✅ |
| API / MCP discovery | — | — | ✅ |
| Training / RAG consent | — | partial | ✅ |
| Agent identity tiers | — | — | ✅ |
| Authentication methods | — | — | ✅ |

**`robots.txt`** governs passive crawling. It is a read/don't-read declaration
for search bots and web crawlers, standardised as RFC 9309.

**`llms.txt`** (proposed by Jeremy Howard of Answer.AI / fast.ai, 2024) is a
Markdown file that provides a clean, structured summary of a site's content
and key pages — essentially a README written for language models. It addresses
a *reading* problem: helping LLMs understand what a site contains.

**`agents.txt`** addresses a fundamentally different and more consequential
problem: the *doing* problem. It governs what AI agents are permitted to
*do* on a site — transacting, authenticating, calling APIs, submitting forms —
and how they should do it. No existing standard covers this.

The distinction matters in practice: no site has faced legal liability because
an LLM misread their content. Sites will face liability when an agent
purchases something it was not authorised to purchase, or exfiltrates data it
was not permitted to access. `agents.txt` is the declaration that makes those
boundaries machine-readable.

Sites SHOULD maintain all three files. They do not conflict.

---

## 2. File Location and Discovery

An `agents.txt` file MUST be placed at the root of the web origin:

```
https://example.com/agents.txt
```

Agents SHOULD retrieve the file via HTTP GET before interacting with a site.
The file MUST be served with `Content-Type: text/plain; charset=utf-8`.

Redirects (HTTP 301/302) MUST be followed, up to a maximum of 5 hops.

If no `agents.txt` file is present (HTTP 404), agents SHOULD assume default
permissive behaviour for read-only access and default restrictive behaviour
for actions.

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
# agents.txt for ExampleShop
# https://exampleshop.com/agents.txt

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

`agents.txt` is a *declaration*, not a technical enforcement mechanism.
Compliant agents SHOULD respect its contents. Sites MUST NOT rely solely on
`agents.txt` for security — access controls and authentication MUST be enforced
server-side.

However, `agents.txt` is not merely aspirational. A published, machine-readable
policy changes the legal posture around non-compliance:

- Violation of a declared `agents.txt` policy may constitute a breach of the
  site's Terms of Service, which can support Computer Fraud and Abuse Act
  (CFAA) claims in the US and equivalent Computer Misuse Act claims in the UK
  and EU jurisdictions.
- "The agent ignored your published access policy" is a substantially cleaner
  legal argument than relying on implicit expectations alone.

Sites that wish to preserve these claims SHOULD ensure their `agents.txt`
policy is referenced from or consistent with their Terms of Service.

### 7.2 Agent Identity

Agent identifiers in section headers are self-declared strings. There is
currently no cryptographic verification of agent identity in this v0.1 spec.
Future versions may incorporate signed agent certificates or W3C Verifiable
Credentials for verified agent identity.

### 7.3 Sensitive Paths

Sites SHOULD use `Disallow` to explicitly protect sensitive paths even if they
are protected by authentication. Defense in depth is recommended.

---

## 8. Comparison with Related Standards

### 8.1 Established and emerging standards

| Standard | Author / Origin | Purpose | Nature |
|---|---|---|---|
| `robots.txt` (RFC 9309) | Martijn Koster, 1994 | Crawl permissions for search bots | Policy (passive) |
| `llms.txt` | Jeremy Howard, Answer.AI / fast.ai, 2024 | LLM-readable site content summary | Content (passive) |
| `security.txt` (RFC 9116) | IETF, 2022 | Security vulnerability disclosure | Contact |
| aipref-vocab (draft-ietf-aipref-vocab) | Keller & Thomson, IETF AIPREF WG, 2025 | Vocabulary for AI training & search consent | Vocabulary (passive) |
| `agents.txt` (this spec) | Jasper van Veen, 2026 | AI agent action permissions & discovery | Policy (active) |

#### `llms.txt` and `agents.txt` — a closer comparison

`llms.txt`, proposed by Jeremy Howard (fast.ai / Answer.AI), addresses the
challenge of helping language models understand a website's content and
structure. A typical `llms.txt` file contains a site description, links to
key documentation pages, and optionally a full content dump (`llms-full.txt`).
It is Markdown-formatted and read-only in nature — its purpose is
comprehension, not action.

`agents.txt` addresses a complementary but distinct problem: not what a site
*contains*, but what an AI agent is *permitted to do* there. The two files
answer different questions:

- `llms.txt`: *"Here is what our site is about, in a format you can digest."*
- `agents.txt`: *"Here is what you are allowed to do here, and how to do it."*

Neither file makes the other redundant. A site could and should publish both.
A useful analogy: `llms.txt` is to `agents.txt` as a product catalogue is to
a terms-of-service agreement — one informs, the other governs.

#### IETF AIPREF Working Group and `agents.txt`

The IETF has established a dedicated working group for AI-related web
standards: the **AIPREF WG** (mailing list: `ai-control@ietf.org`). Its
current work item, `draft-ietf-aipref-vocab` (Keller & Thomson, 2025), defines
a standardised vocabulary for declaring how digital assets may be used by
automated systems — specifically covering AI training consent and search
indexing preferences. It is on the Standards Track at version 05.

This vocabulary overlaps with a subset of `agents.txt` directives:

| Concern | aipref-vocab | `agents.txt` |
|---|---|---|
| AI training consent | ✅ Core purpose | ✅ `Allow-Training` |
| Search / RAG consent | ✅ Core purpose | ✅ `Allow-RAG` |
| Scraping consent | ✅ | ✅ `Allow-Scraping` |
| Action permissions | ❌ | ✅ Core purpose |
| API / MCP discovery | ❌ | ✅ |
| Agent identity tiers | ❌ | ✅ |
| Authentication methods | ❌ | ✅ |
| Carrier format | Vocabulary only (robots.txt, HTTP headers, HTML) | Standalone file |

The relationship is complementary. `aipref-vocab` defines *what* terms mean
for content-use consent across multiple carriers; `agents.txt` defines a
dedicated file format that may carry those terms alongside the action-layer
directives that `aipref-vocab` deliberately does not address.

A future revision of this specification should consider aligning its
`Allow-Training`, `Allow-RAG`, and `Allow-Scraping` directive values with
the vocabulary defined in `draft-ietf-aipref-vocab` to ensure
interoperability. The action-permission, discovery, and authentication
directives of `agents.txt` remain outside the scope of any existing IETF
work item and represent its primary novel contribution.

### 8.2 Related prior art

Several independent efforts have explored the `agents.txt` namespace. This
section documents them and clarifies how this specification relates.

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
The two are complementary and could coexist in a combined file or separate
files (e.g. `agents.txt` for inbound permissions, `agent-services.txt` for
outbound discovery).

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

**Summary:** The `agents.txt` concept has been independently conceived by
multiple authors, which strongly suggests the need is real. No existing effort
has produced a complete, formally-reasoned specification or pursued a standards
track. This document aims to fill that gap.

---

## 9. Versioning

This document describes `agents.txt` version 2.0 (draft). The version may be
declared explicitly:

```
Agents-Txt-Version: 2.1
```

---

## 10. Open Questions (for community discussion)

1. **Agent identity verification** — How should agent identity be verified
   beyond self-declaration? (Signed certificates? OAuth client credentials?)
2. **Capability vocabulary** — Should capabilities be a defined controlled
   vocabulary, or free-form strings?
3. **Conflict resolution** — When `robots.txt` and `agents.txt` conflict on
   path access, which takes precedence?
4. **Monetary terms** — Should `agents.txt` support declaring pricing for
   automated access (pay-per-call APIs)?
5. **MCP vs. REST** — As MCP gains adoption, should this spec more tightly
   integrate with the MCP standard?

---

## 11. Acknowledgements

This specification was conceived by **Jasper van Veen** in March 2026 with support from Claude Sonnet 4.6 as part
of broader work on AI infrastructure.
The author recognises the foundational work of Martijn Koster (robots.txt, 1994) 
and the IETF working group that produced RFC 9309.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 0.1 | 2026-03-09 | Initial draft |
| 0.1.1 | 2026-03-10 | Added §1.1 agent incentives & compliance rationale; expanded §7.1 legal posture |
| 2.0 | 2026-03-14 | Expanded §1.2 to cover relationship with `llms.txt` and Jeremy Howard / Answer.AI; updated three-way comparison table (`robots.txt` / `llms.txt` / `agents.txt`); expanded §8.1 with detailed `llms.txt` comparison |
| 2.1 | 2026-03-14 | Added IETF AIPREF WG (draft-ietf-aipref-vocab) to §8.1; detailed overlap/complement analysis; noted alignment path for `Allow-Training` / `Allow-RAG` / `Allow-Scraping` with aipref vocabulary |

---

*This specification is published under the Creative Commons Attribution 4.0
International License (CC BY 4.0). You are free to share and adapt it with
attribution.*
