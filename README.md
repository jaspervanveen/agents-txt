# agent-manifest.txt

**A proposed web standard for AI agent interaction declarations.**

> `robots.txt` tells crawlers where they can go.  
> `agent-manifest.txt` tells AI agents what they can *do* — and how.

> **Historical note:** This project was originally named `agents.txt`, derived
> from `robots.txt` by direct analogy. In March 2026, it was renamed to
> `agent-manifest.txt` after the `agents.txt` namespace became crowded: an
> independent IETF Internet-Draft (`draft-srijal-agents-policy-00`) had claimed
> that filename, and multiple community projects were using it for different
> purposes. The new name more accurately reflects the document's purpose — a
> rich capability *manifest* — while preserving a clean path toward formal
> standardisation.

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

## The Proposal

Place an `agent-manifest.txt` file at `https://yourdomain.com/agent-manifest.txt`:

```
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

`agent-manifest.txt` complements — not replaces — the standards already in use:

| | `robots.txt` | `llms.txt` | `agent-manifest.txt` |
|---|---|---|---|
| Crawl permissions | ✅ | — | — |
| Content summary for LLMs | — | ✅ | — |
| Action permissions | — | — | ✅ |
| API / MCP discovery | — | — | ✅ |
| Training / RAG consent | — | partial | ✅ |
| Agent identity tiers | — | — | ✅ |
| Auth methods | — | — | ✅ |

**`llms.txt`** (Jeremy Howard / Answer.AI) tells LLMs what your site *contains*.  
**`agent-manifest.txt`** tells agents what they *can do* — and how.  
A well-configured site should have all three.

## Status

🟡 **Draft v0.3.0** — open for community feedback

## Read the Spec

→ [spec/agent-manifest-spec.md](spec/agent-manifest-spec.md)

## Contribute

- **Open an issue** to discuss a directive, edge case, or design question
- **Open a PR** to propose changes

Questions or ideas? [Open an issue](https://github.com/jaspervanveen/agents-txt/issues) on GitHub.

## Author

**Jasper van Veen**  
With some love from Claude Sonnet 4.6.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)
