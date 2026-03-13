# agents.txt

**A proposed web standard for AI agent interaction declarations.**

> `robots.txt` tells crawlers where they can go.  
> `agents.txt` tells AI agents what they can *do* — and how.

---

## The Problem

The web's permission model was built for passive crawlers. `robots.txt` (RFC 9309) answers one question: *can you look at this?*

AI agents don't just look. They book, buy, submit, authenticate, and act on behalf of users. None of that is addressed by any existing standard.

Sites have no machine-readable way to:
- Declare what actions agents are permitted to perform
- Advertise their API or MCP server to agents
- Express consent for AI training or RAG use
- Apply different rules to different types of agents

## The Proposal

Place an `agents.txt` file at `https://yourdomain.com/agents.txt`:

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

## Key Differences from robots.txt

| | robots.txt | agents.txt |
|---|---|---|
| Crawl permissions | ✅ | — |
| Action permissions | — | ✅ |
| API / MCP discovery | — | ✅ |
| Training / RAG consent | — | ✅ |
| Agent identity tiers | — | ✅ |
| Auth methods | — | ✅ |

They are **complementary** — both files can and should coexist.

## Status

🟡 **Draft v0.1** — open for community feedback

## Read the Spec

→ [spec/agents-txt-spec.md](spec/agents-txt-spec.md)

## Contribute

- **Open an issue** to discuss a directive, edge case, or design question
- **Open a PR** to propose changes

Questions or ideas? [Open an issue](https://github.com/jaspervanveen/agents-txt/issues) on GitHub.

## Author

**Jasper van Veen**  
With some love from Claude Sonnet 4.6.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)
