# agents-brief.txt

**A proposed web standard for AI agent interaction declarations.**

> `robots.txt` tells crawlers where they can go.  
> `agents-brief.txt` tells AI agents what they can *do* — and how.

---

## What is it?

`agents-brief.txt` is the briefing document for AI agents visiting your site.
Like a mission brief or creative brief, it answers everything an agent needs
to know before acting: what it may do, how to authenticate, which API or MCP
endpoint to use, and what data it may use — in a single plain-text file at
your domain root.

Place it at `https://yourdomain.com/agents-brief.txt`.

---

## The Problem

The web's permission model was built for passive crawlers. `robots.txt`
(RFC 9309) answers one question: *can you look at this?*

AI agents don't just look. They book, buy, submit, authenticate, and act on
behalf of users. None of that is addressed by any existing standard.

Sites have no machine-readable way to:
- Declare what actions agents are permitted to perform
- Advertise their API or MCP server to agents
- Express consent for AI training or RAG use
- Apply different rules to different types of agents

**eBay, Shopify, and Amazon are already trying to solve this by embedding
agent policies inside `robots.txt` — a file not designed for it.** This
proposal provides the dedicated standard they actually need.

## The Proposal

Place an `agents-brief.txt` file at `https://yourdomain.com/agents-brief.txt`:

```
# agents-brief.txt for ExampleShop

Site-Name: ExampleShop
Site-Description: Online marketplace for sustainable home goods.
Contact: agents@exampleshop.com

Allow-Training: no
Allow-RAG: yes
Allow-Actions: no
Preferred-Interface: rest
API-Docs: https://api.exampleshop.com/openapi.json
MCP-Server: https://mcp.exampleshop.com

[Agent: *]
Allow: /products/*
Allow: /search
Disallow: /checkout
Rate-Limit: 30/minute

[Agent: verified-purchasing-agent]
Allow: /checkout
Auth-Required: yes
Auth-Method: oauth2
Allow-Actions: yes
```

## How it fits with existing standards

`agents-brief.txt` complements — not replaces — the standards already in use:

| | `robots.txt` | `llms.txt` | `agents-brief.txt` |
|---|---|---|---|
| Crawl permissions | ✅ | — | — |
| Content summary for LLMs | — | ✅ | — |
| Action permissions | — | — | ✅ |
| API / MCP discovery | — | — | ✅ |
| Training / RAG consent | — | partial | ✅ |
| Agent identity tiers | — | — | ✅ |
| Auth methods | — | — | ✅ |

**`llms.txt`** (Jeremy Howard / Answer.AI) tells LLMs what your site *contains*.  
**`agents-brief.txt`** tells agents what they *can do* — and how.  
A well-configured site should have all three.

## Status

🟡 **Draft v0.4.0** — open for community feedback

## Read the Spec

→ [spec/agents-brief-spec.md](spec/agents-brief-spec.md)

## Naming History

This project has had three names: `agents.txt` → `agent-manifest.txt` →
`agents-brief.txt`. Each change was research-driven. The full rationale,
including prior art analysis across IETF, IANA, GitHub, Wikipedia, and
trademark databases, is documented in:

→ [naming-research.md](naming-research.md)  
→ [CHANGELOG.md](CHANGELOG.md)

The short version:
- `agents.txt` — dropped because an IETF I-D claimed the filename
- `agent-manifest.txt` — dropped because "agent manifest" is already the
  established term for a config file *describing an agent* (used by Microsoft
  Copilot, ACP protocol, and others) — the exact opposite of what this file does
- `agents-brief.txt` — selected for full spec coverage and zero prior art

## Contribute

- **Open an issue** to discuss a directive, edge case, or design question
- **Open a PR** to propose changes

Questions or ideas? [Open an issue](https://github.com/jaspervanveen/agents-brief.txt/issues) on GitHub.

## Author

**Jasper van Veen**  
With some love from Claude Sonnet 4.6.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)
