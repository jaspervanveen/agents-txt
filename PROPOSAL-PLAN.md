# agents.txt — Proposal & Standardisation Plan

**Author:** Jasper van Veen  
**Created:** March 2026

---

## Goal

Get `agents.txt` adopted as a recognised web standard — ideally an IETF RFC,
following the same path as `robots.txt` (RFC 9309, published 2022).

---

## Phase 1 — Establish the Idea (Now)

**Actions:**
- [x] Write draft spec v0.1
- [ ] Publish on GitHub (`jaspervanveen/agents-txt`)
- [ ] Write a short, accessible blog post explaining the idea
- [ ] Post to Hacker News ("Show HN: agents.txt — a proposed standard...")
- [ ] Post to relevant communities: r/MachineLearning, Lobsters, AI Twitter/X

**Goal:** Get the idea into the public record with a clear timestamp and author.  
Even if the spec evolves, the origin story matters.

**Timeline:** This week.

---

## Phase 2 — Community Validation (Weeks 2–6)

**Actions:**
- [ ] Engage AI/web developer communities for feedback on the spec
- [ ] Reach out to key stakeholders:
  - Browser vendors (Google, Mozilla, Apple) — they care about agent UX
  - AI labs (Anthropic, OpenAI, Google DeepMind) — they build the agents
  - MCP maintainers (Anthropic) — tight overlap with agents.txt
  - Major websites (GitHub, Shopify, Cloudflare) — early implementers
- [ ] Invite co-authors / contributors to strengthen credibility
- [ ] Publish a reference implementation (Python validator / parser)

**Goal:** Show the idea has traction and addresses a real need.

---

## Phase 3 — Formal Standardisation (Months 2–6)

### Primary path: IETF Internet-Draft

This is how `robots.txt` became RFC 9309. The IETF process:

1. **Submit an Internet-Draft** at datatracker.ietf.org
   - Format: RFC XML or Markdown via `mmark`
   - Title: "The agents.txt File for AI Agent Declarations"
   - Target working group: `httpapi` or a new `agentweb` WG

2. **Find a working group home**
   - `httpapi` WG — handles HTTP API conventions
   - `secdispatch` — for security/trust aspects
   - Or propose a new WG: "Agentic Web" (requires a charter and BOF session)

3. **IETF BOF (Birds of a Feather) session**
   - Propose a BOF at an IETF meeting to gauge interest
   - IETF meets 3×/year (typically March, July, November)
   - Next opportunity: IETF 122 (likely July 2026)

4. **Iterate through Last Call and publication**
   - Typical RFC timeline: 1–3 years from Internet-Draft to RFC
   - `robots.txt` took ~3 years through IETF

### Secondary path: W3C Community Group

If IETF traction is slow, a W3C Community Group is faster to establish:

1. **Propose a W3C Community Group**: "AI Agent Web Standards CG"
   - Free to create at w3.org/community
   - Low barrier — just needs 5 supporters to launch
   - Can publish CG Reports (not full W3C standards, but credible)

2. **Relevant W3C groups to engage:**
   - **W3C Technical Architecture Group (TAG)** — reviews emerging web architecture
   - **W3C Privacy Interest Group (PING)** — agent data use has privacy implications
   - **W3C Web of Things (WoT) WG** — autonomous agents in IoT/web context
   - **W3C AI & Web CG** — if it exists or can be created

3. **Submit for TAG review**
   - TAG reviews emerging web platform features
   - A TAG Findings document on "agentic web permissions" would be influential

### Tertiary path: Industry consortium

If formal standardisation is slow, an industry consortium can drive de-facto
adoption while the formal process catches up:

- **Partnership on AI** — AI safety/governance, relevant for agent trust
- **Open Web Foundation** — has hosted emerging web standards
- **Linux Foundation** — hosts many open tech standards
- **WHATWG** — for browser-level integration (if agents.txt gets browser support)

---

## Phase 4 — Reference Implementations (Parallel)

To drive adoption alongside standardisation:

- [ ] Python library: `agents-txt` (parse & validate agents.txt files)
- [ ] JavaScript/Node library
- [ ] CLI validator: `agents-txt validate https://example.com`
- [ ] WordPress plugin
- [ ] nginx / Apache config generator

---

## Key Messages for Outreach

1. **This is urgent** — agents are acting on the web *right now*, with no standard to guide them
2. **It's complementary, not competing** — sits alongside robots.txt, not replacing it
3. **Simple for sites to adopt** — a text file, zero infrastructure required
4. **Benefits both sides** — sites get control; agents get reliable capability discovery

---

## Contacts to Approach

| Person / Org | Why | How |
|---|---|---|
| Martijn Koster | Invented robots.txt — credibility/blessing | Email/LinkedIn |
| Anthropic (MCP team) | agents.txt + MCP is a natural pairing | GitHub / direct |
| OpenAI (Operator team) | They're building web-acting agents | GitHub / media |
| Cloudflare | They added AI bots to robots.txt support | Blog engagement |
| Google Search team | They maintain robots.txt tooling | IETF / public comment |
| W3C TAG | Architecture review | w3.org formal submission |

---

## Success Metrics

- 100+ GitHub stars within first month → real interest
- First "we're implementing this" comment from a major site → adoption signal
- IETF Internet-Draft accepted for discussion → on the standardisation track
- W3C TAG acknowledges the proposal → web architecture credibility

---

*This is a realistic plan. robots.txt spent 25 years as an informal standard
before becoming an RFC. agents.txt has the advantage of arriving at exactly the
right moment — when the need is obvious and urgent. Move fast.*
