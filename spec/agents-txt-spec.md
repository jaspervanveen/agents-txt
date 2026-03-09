# agents.txt — AI Agent Interface Declaration Standard
### Draft Specification v0.1 — March 2026

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

### 1.1 Relationship to robots.txt

`robots.txt` and `agents.txt` are **complementary, not competing** standards.

| Concern | robots.txt | agents.txt |
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

Sites SHOULD maintain both files. `robots.txt` governs crawling; `agents.txt`
governs interaction.

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

### 7.1 Trust

`agents.txt` is a *declaration*, not an enforcement mechanism. Compliant agents
SHOULD respect its contents. Sites MUST NOT rely solely on `agents.txt` for
security — access controls and authentication MUST be enforced server-side.

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

### 8.1 Established standards

| Standard | Purpose | Scope |
|---|---|---|
| `robots.txt` (RFC 9309) | Crawl permissions for search bots | Read-only crawling |
| `llms.txt` (Answer.AI, 2024) | LLM-readable site summary | Content discovery |
| `security.txt` (RFC 9116) | Security disclosure contacts | Security reporting |
| `agents.txt` (this spec) | AI agent capabilities & permissions | Agentic interaction |

`llms.txt` is a content-oriented standard that helps LLMs understand what a
site contains. `agents.txt` is an *interaction-oriented* standard that tells
agents what they may do and how. They are complementary.

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

This document describes `agents.txt` version 0.1 (draft). The version may be
declared explicitly:

```
Agents-Txt-Version: 0.1
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

This specification was conceived by **Jasper van Veen** in March 2026 as part
of broader work on AI-native talent and infrastructure discovery. The author
recognises the foundational work of Martijn Koster (robots.txt, 1994) and the
IETF working group that produced RFC 9309.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 0.1 | 2026-03-09 | Initial draft |

---

*This specification is published under the Creative Commons Attribution 4.0
International License (CC BY 4.0). You are free to share and adapt it with
attribution.*
