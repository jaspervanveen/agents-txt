# Changelog

All notable changes to this project are documented here.

---

## [0.4.0] — 2026-03-27

### Changed — **Renamed `agent-manifest.txt` → `agents-brief.txt`**

The filename has been changed for the final time following extensive research
across four rounds (documented in `naming-research.md`).

**Why `agent-manifest.txt` was dropped:**

Research confirmed that "agent manifest" is already the established industry
term for a config file *describing an agent's own identity and capabilities* —
used by Microsoft Security Copilot, Microsoft 365 Copilot, the Agent
Communication Protocol (ACP), `agent-manifest.org`, `agent-manifest.com`,
and others. This is the exact conceptual opposite of what this file does: a
*website* declaring policy *for* agents visiting it. Keeping the name would
have actively misled the target audience.

**Why `agents-brief.txt` was selected:**

A brief — in professional use (creative brief, mission brief, operational brief)
— is the document you read before you begin a task: permissions, boundaries,
available tools, contacts, and terms in one structured document. This maps
perfectly to all four functional dimensions of this spec:
- Permissions (Allow/Disallow, Allow-Actions)
- Boundaries (Rate-Limit, Auth-Required)
- Available tools (MCP-Server, API-Docs, Capabilities)
- Terms (Allow-Training, Allow-RAG, Contact)

The plural form (`agents-brief`, not `agent-brief`) follows the `robots.txt`
/ `llms.txt` / `humans.txt` naming convention: when the filename names the
audience, it is plural.

Prior art check confirmed clean across IETF, IANA, GitHub, Wikipedia, academic
sources, and brand names. Trademark databases require manual verification
(USPTO, EUIPO, WIPO).

### Added
- New spec file: `spec/agents-brief-spec.md` (replaces `agent-manifest-spec.md`)
- `CHANGELOG.md` — this file
- `§10` in spec fully rewritten: three-chapter naming history with rationale
- `§10.4` — complete alternatives table with reasons for each rejection

### Updated
- `README.md` — new name throughout; naming history section added
- Version directive: `Agents-Brief-Version: 0.4.0`
- All file path references updated: `https://example.com/agents-brief.txt`
- §1.2 comparison table updated
- §6 complete example updated
- §7, §8.1, §9, §11 — all `agent-manifest.txt` references replaced
- §8.2 summary updated

### Removed
- `spec/agent-manifest-spec.md` (superseded by `spec/agents-brief-spec.md`)

---

## [0.3.0] — 2026-03-27

### Changed — **Renamed `agents.txt` → `agent-manifest.txt`**

The `agents.txt` namespace had become crowded:
- IETF Internet-Draft `draft-srijal-agents-policy-00` had claimed the filename
- Multiple community projects used the same name for different purposes

### Added
- `naming-research.md` — full naming research documentation
- `§1.3` — Industry Validation: eBay, Shopify, Amazon robots.txt workaround
- `§1.4` — Scope: formal definition of "web agent" for this spec
- `§8.2` — AMP (`agent-manifest.com`) added as prior art
- `§8.2` — eBay/Shopify/Amazon industry practice added as prior art

---

## [0.2.0] — 2026-03-22

### Added
- `globalchatads/agents-txt` added to §8.2 prior art
- Community input on open questions 1–3 from dev.to comments
- GitHub Issues #1–#4 linked from §11

---

## [0.1.5] — 2026-03-20

### Added
- §10: naming rationale, alternatives considered, author's position

---

## [0.1.4] — 2026-03-14

### Added
- IETF WEBBOTAUTH WG reference and full IETF landscape summary table

---

## [0.1.3] — 2026-03-14

### Added
- IETF AIPREF WG reference and overlap analysis with `Allow-Training` /
  `Allow-RAG` / `Allow-Scraping`

---

## [0.1.2] — 2026-03-14

### Added
- Expanded §1.2 with `llms.txt` comparison
- Three-way comparison table (`robots.txt` / `llms.txt` / `agents.txt`)
- IETF AIPREF WG and WEBBOTAUTH WG landscape

---

## [0.1.1] — 2026-03-10

### Added
- §1.1: agent incentives and compliance rationale
- §7.1: legal posture expanded (CFAA, Computer Misuse Act)
- §8.2: prior art (dennj, kaylacar, muzz-yasir)

---

## [0.1.0] — 2026-03-09

Initial draft published as `agents.txt`. Core structure: global directives,
agent sections, Allow/Disallow, Rate-Limit, Auth-*, MCP-Server, API-Docs,
Capabilities, training/RAG consent, complete example.
