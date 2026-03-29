# Naming Research — Full History

**Maintained by:** Pandora  
**Project:** jaspervanveen/agents-brief.txt  

---

## Name History

| Version | Date | Name | Reason for change |
|---|---|---|---|
| v0.1–v0.2 | 2026-03-09 | `agents.txt` | Original — direct robots.txt analogy |
| v0.3.0 | 2026-03-27 | `agent-manifest.txt` | IETF I-D `draft-srijal-agents-policy-00` claimed `agents.txt`; namespace crowded |
| TBD | TBD | ? | `agent-manifest.txt` found to mean the *opposite thing* — see Research Round 2 |

---

## Research Round 1 — March 2026-03-16

Original investigation into alternatives to `agents.txt`.

### Methodology
- GitHub: searched `github.com/search?q=<name>&type=repositories` — 0 results required
- IETF Datatracker API: `name__contains=<term>`
- Web (DDG): exact-match quoted search

### Candidates — all confirmed clean at time of research

| # | Filename | GitHub | IETF | Web | Notes |
|---|---|---|---|---|---|
| 1 | `agentpolicy.txt` | ✅ 0 | ✅ None | ✅ 0 | Policy-oriented. Strong IETF framing. |
| 2 | `aipermit.txt` | ✅ 0 | ✅ None | ✅ 0 | "Permit" evokes access control well. |
| 3 | `agentaccess.txt` | ✅ 0 | ✅ None | ✅ 0 | Parallel to robots.txt access-control framing. |
| 4 | `aimanifest.txt` | ✅ 0 | ✅ None | ✅ 0 | "Manifest" well understood in web/app contexts. |
| 5 | `agentcap.txt` | ✅ 0 | ✅ None | ✅ 0 | Short for "agent capabilities". Terse. |
| 6 | `machinepolicy.txt` | ✅ 0 | ✅ None | ✅ 0 | Broader than AI — covers any automation. |
| 7 | `aiconsent.txt` | ✅ 0 | ✅ None | ✅ 0 | Strong GDPR/regulatory resonance. |
| 8 | `agentdirective.txt` | ✅ 0 | ✅ None | ✅ 0 | EU regulatory weight — intentional? |
| 9 | `agentlicense.txt` | ✅ 0 | ✅ None | ✅ 0 | Licensing + training consent angle. |

---

## Research Round 2 — 2026-03-27 (post-rename to agent-manifest.txt)

### Finding: "agent manifest" means the *opposite* of what Jasper's proposal does

In the AI/software industry 2025–2026, "agent manifest" has solidified as the standard term for a file that describes an *agent's own identity and capabilities* — metadata **by** an agent, **about** an agent. Jasper's file is a *website* declaring policy **for** agents visiting it. Opposite perspectives.

**Confirmed usages (all verified by direct URL fetch):**

| Source | Usage | URL |
|---|---|---|
| Microsoft Security Copilot | YAML/JSON that defines an agent's identity and skills | `learn.microsoft.com/…/agent-manifest` |
| Microsoft M365 Copilot | "Declarative agent manifest" — spec v1.2, defines agent instructions | `github.com/MicrosoftDocs/m365copilot-docs` |
| Agent Communication Protocol (ACP) | Agent identity, capabilities, content types for ACP server advertising | `agentcommunicationprotocol.dev/core-concepts/agent-manifest` |
| agent-manifest.org (ADS project) | "Agent Definition Schema — Standardizing the Way Agents Describe Themselves" | `agent-manifest.org` |
| agent-manifest.com (AMP project) | `/.well-known/agent-manifest.json` — site declares its API for agents | `agent-manifest.com` |
| agent-manifest-spec.org | "Agent Manifest v1.0" — agent identity, authority, scope, constraints | `agent-manifest-spec.org` |
| AgentSpec (agents-oss) | `agent.yaml` = "The Universal Agent Manifest" | `agents-oss.github.io/agentspec` |
| Infobip | Agent config files called "agent manifests" | `infobip.com/docs/ai-agents/advanced-topics/agent-manifests` |

**Note on agent-manifest.com (AMP):** This is the closest to Jasper's proposal — a site-side declaration for agents. But it's JSON-only, API/auth-focused, and lacks training consent, tiered access, MCP discovery. Should be added to §8.2 prior art.

**IANA `agent-card.json`:** Linux Foundation registered Aug 2025 for A2A protocol agent identity. More "about an agent" territory.

**Verdict:** Rename away from `agent-manifest.txt` immediately.

---

## Research Round 3 — 2026-03-27 (evaluating "agent policy" and "webagent-policy")

### Finding: "agent policy" — three distinct collision layers

**Layer 1 — Reinforcement Learning (foundational ML term)**
"Agent policy" is one of the most established terms in machine learning. In RL, an agent's *policy* is its core decision function — the mapping from states to actions. Every RL textbook uses this. Audience: ML researchers, AI engineers.

*Severity for this proposal:* Moderate. Web standards developers don't think in RL terms day-to-day. But anyone from an ML background will get a momentary wrong association.

**Layer 2 — Industry practice: eBay, Shopify, Amazon (VALIDATING)**
"Robot & Agent Policy" / "Robots & Agent Policy" have emerged as the informal industry term for websites' AI access rules — currently embedded *inside* robots.txt. 

- **eBay:** Added "Robot & Agent Policy" to robots.txt late 2025. Prohibits "automated scraping, buy-for-me agents, LLM-driven bots, or any end-to-end flow that attempts to place orders without human review." (Source: Modern Retail, Jan 2026; Ars Technica)
- **Shopify:** Added "Robots & Agent Policy" block to robots.txt. States "checkouts are for humans." Uses `bots@shopify.com` contact.
- **Amazon:** Updated robots.txt to explicitly block specific AI agent user agents.
- **DataDome research** (Sep 2025): Published "Beyond robots.txt: Exposing the Cracks in AI Agent Policy Enforcement" — documents how AI agents inconsistently respect robots.txt and argues for a dedicated mechanism.

**This is the key insight:** Major platforms are trying to do exactly what Jasper's proposal enables, but they're doing it inside robots.txt — a format not designed for it. `agent-policy.txt` (or whatever this standard is named) is the dedicated file they actually need.

**Layer 3 — IETF network infrastructure draft**
`draft-zhang-rtgwg-agent-policy-aware-network` (March 2026) — about AI Agent Policy-Aware Networks for routing. Unrelated subject matter. No practical confusion.

**Layer 4 — MetaMirror blog: "Unified Agent Policy for Delegated Authority"**
A blog post (Medium, April 2025) proposing an "Agent Policy" spec for inter-agent trust using WS-Policy + OAuth. Not a formal draft. Not a competing standard.

### Finding: "webagent" — two established meanings

**"Web agent" in enterprise IAM (Broadcom SiteMinder, Oracle OpenSSO):**
A "web agent" is a server-side software component that intercepts HTTP requests and enforces authentication/authorization. It sits on the web server, checks resources against a policy server. This usage is 20+ years old and deeply embedded in enterprise IT vocabulary.

*Collision risk:* Enterprise IT teams managing SiteMinder deployments would read "web-agent-policy.txt" as a configuration file for their SiteMinder web agents. Not a blocking collision but a real one in the enterprise IAM audience.

**"WebAgent" in AI research:**
Google DeepMind coined "WebAgent" (one word) as the name of their ICLR 2024 (Oral) paper: "A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis" — an LLM-driven agent that completes tasks on real websites. This is the most prominent academic use of the term. It's now a named research project, not a generic term.

*Collision risk:* Low. This is a proper noun (a specific research system), not a category name.

**"webagent-policy.txt" availability:**
- IETF Datatracker: ✅ zero matches for `webagent` or `web-agent` as draft names
- GitHub: ✅ zero repositories for "webagent-policy"
- Web: ✅ zero results for "webagent-policy.txt"
- IANA well-known URIs: ✅ not registered

**Net assessment of `webagent-policy.txt`:**
Cleaner than `agent-policy.txt` on the RL collision. But introduces the SiteMinder "web agent" enterprise confusion. The SiteMinder usage is significant in corporate IT contexts — which is exactly where site operators configuring this file would work. Rating: better than agent-manifest.txt, but `agent-policy.txt` may ultimately be stronger because it's already the vocabulary eBay and Shopify are using organically.

---

## Current Recommendation (as of 2026-03-27)

**Primary: `agent-policy.txt`**
- The industry is converging on "agent policy" as the vocabulary for this problem space (eBay, Shopify, DataDome)
- RL collision exists but operates in a separate audience context
- `dnt-policy.txt` IANA precedent: identical `<subject>-policy.txt` structure
- Zero prior art as a filename
- Most likely to be intuitive to site operators who've read about eBay/Shopify's approach

**Alternative: `webagent-policy.txt`**  
- Also zero prior art as a filename
- Avoids RL collision
- Introduces SiteMinder enterprise IAM ambiguity
- Slightly longer, slightly less natural English

**Still under consideration by Jasper.**

---

## What to Add to the Spec (regardless of final name)

### New content needed

1. **§1 Introduction — strengthen with industry validation:**
   - eBay and Shopify are already trying to declare agent policy inside robots.txt
   - This validates the problem; also shows why robots.txt is insufficient
   - DataDome article validates the enforcement gap

2. **New §X — Definitions: "Web Agent"**
   - Define the scope of what "agent" means in this spec
   - Distinguish from: RL agents, SiteMinder web agents, simple crawlers, web browsers

3. **§8.2 Prior Art — add agent-manifest.com (AMP)**
   - Closest competing proposal on the site-side declaration angle

4. **§10 Naming History — update to document three iterations**
   - agents.txt → agent-manifest.txt → [current name]

---

## Research Round 4 — 2026-03-27: Synonym matrix + `agents-brief.txt` deep validation

### Synonym analysis

Full combinatorial exercise conducted across two synonym dimensions:

**"Webagent" synonyms evaluated:** `agent`, `webagent`, `bot`, `ai`, `actor`, `operator`, `robot`, `crawler`, `automaton`, `llm`

**"Policy" synonyms evaluated:** `policy`, `rules`, `terms`, `access`, `permit`, `licence`, `charter`, `directive`, `declaration`, `consent`, `accord`, `contract`, `conduct`, `brief`, `guide`, `manual`, `primer`, `prospectus`, `codex`, `spec`, `dossier`, `carte`

**All combinations confirmed zero prior art as filenames** (SearXNG + IETF Datatracker queries).

**Key findings:**
- `agent-rules.txt` — **occupied conceptually**: the `agent-rules/agent-rules` GitHub organisation runs an active community standard for AI coding agent rules (AGENTS.md ecosystem, supported by Cursor, Claude Code, GitHub Copilot, Google Gemini). Not a filename conflict, but a strong conceptual collision.
- `agent-terms.txt` — clean as a filename; "agent terms" in natural language refers to insurance/real estate agent commission terms. No technical conflict.
- `agents-brief.txt` — **winner**: see deep check below.

**Coverage analysis (how well each word covers the full spec):**

| Spec dimension | "rules" | "terms" | "brief" |
|---|---|---|---|
| Allow/Disallow paths | ✅ | ✅ | ✅ |
| Rate limiting | ✅ | ✅ | ✅ |
| Auth methods/endpoints | ✅ | ✅ | ✅ |
| Training/RAG consent | ⚠️ | ✅ | ✅ |
| MCP/API discovery | ❌ | ⚠️ | ✅ |
| Capability declaration | ❌ | ⚠️ | ✅ |
| Site metadata | ⚠️ | ✅ | ✅ |
| Tiered agent access | ✅ | ✅ | ✅ |

"Brief" is the only word that covers all dimensions, including the discovery/capability half of the spec. A brief (creative brief, mission brief, legal brief, operational brief) is precisely: permissions + boundaries + available tools + contacts + terms — in one document before you begin. This maps to all four functional areas of the spec simultaneously.

**Plural question resolved:** Following `robots.txt`, `llms.txt`, `humans.txt` precedent — when the filename names the *audience*, it's plural. `agents-brief.txt` (plural audience, singular document type) is correct. Mirrors the robots.txt family directly.

---

### `agents-brief.txt` — Deep Validation (2026-03-27)

**Methodology:** IETF Datatracker API, IANA Well-Known URI registry (full scan), GitHub repository search, GitHub code/filename search, Wikipedia, Google Scholar, trademark databases (WIPO/USPTO/EUIPO — partially blocked), npm, brand/product name search, SearXNG multi-engine search.

#### Results by source

| Source | Result | Detail |
|---|---|---|
| **IETF Datatracker** | ✅ Zero | `agents-brief` and `agent-brief` — 0 matches |
| **IANA Well-Known URIs** | ✅ Zero | Full registry scanned; neither form registered |
| **GitHub (filename)** | ✅ Zero | `filename:agents-brief.txt` — 0 code results |
| **GitHub (repos named)** | ✅ Zero | 0 repos named "agents-brief" |
| **GitHub (concept, broad)** | ⚠️ Context | 213 repos use "agents brief" as natural language (AI agents generating briefs as output). None use it as a web standard filename. |
| **Wikipedia** | ✅ Zero | No article, no disambiguation, 404 for "Agents brief" |
| **Google Scholar** | ✅ Clean | One incidental natural-language use (2003 military multi-agent paper). Not a named concept. |
| **Trademarks (USPTO)** | ⚠️ Unverified | JavaScript-heavy interface; automated check blocked. **Manual verification required.** |
| **Trademarks (EUIPO)** | ⚠️ Unverified | CAPTCHA-blocked. **Manual verification required.** |
| **Trademarks (WIPO BrandDB)** | ⚠️ Unverified | CAPTCHA-blocked. **Manual verification required.** |
| **Brand names** | ⚠️ Minor | `agentbrief.com` — real estate SaaS tracking agent activity. Different domain, different meaning, no hyphen, no `.txt`. Not a conflict. |
| **npm / package registries** | ✅ Clean | No conflicting packages. |
| **W3C / OASIS / ISO / ETSI** | ✅ Clean | No specifications found. |

#### Context: the 213 GitHub repos

All repos in the "agents brief" search use the phrase as English — AI agents that *produce* briefs (creative briefs, project briefs, investment briefs). This confirms the phrase is alive in AI discourse, but in the opposite direction: agents generating briefs *for humans*. Jasper's proposal is a brief *for agents* from a website. No filename, format, or standard uses the combination the way this proposal would.

#### Action required before final commit

**Jasper should manually verify trademarks** at:
- USPTO: `tmsearch.uspto.gov` → search "agents brief" and "agent brief"
- EUIPO: `euipo.europa.eu/eSearch` → search "agents brief"
- WIPO: `branddb.wipo.int` → search "agents brief"

This takes ~5 minutes. All three were CAPTCHA-blocked during automated research.

#### Verdict

`agents-brief.txt` is **effectively clean** across all verifiable sources. The only outstanding item is trademark confirmation, which requires a manual browser check. Subject to that passing, this is the strongest candidate name found across all four rounds of research.

---

*All research conducted by direct URL fetch, SearXNG (bing/qwant/mojeek engines used when primary engines rate-limited), and IETF Datatracker API.*
