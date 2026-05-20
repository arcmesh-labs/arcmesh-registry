# ArcMesh Registry

The open registry of MCP servers for [arcmesh-pm](https://github.com/arcmesh-labs/arcmesh-pm).

[MCP (Model Context Protocol)](https://modelcontextprotocol.io) lets AI assistants like Claude connect to external tools — GitHub, Notion, Stripe, databases, and more. Each entry in this registry is a single `manifest.json` file that describes how to install, configure, and run an MCP server. The `apm` CLI reads these manifests and does the rest.

```bash
apm install github
apm install notion
apm install stripe
```

---

## How it works

The registry is a flat collection of manifest files — one directory per server:

```
servers/
  <name>/
    manifest.json        ← one server, one file
schema/
  manifest.schema.json   ← JSON Schema (draft-07) for validation
validate_manifests.py    ← local validation script
CONTRIBUTING.md          ← how to add a new server
```

`apm` fetches `servers/index.json` to search and list servers, then fetches the individual `manifest.json` to install. No database, no API — just files on GitHub.

---

## Manifest structure

A manifest describes everything `apm` needs to install a server:

```json
{
  "name": "github",
  "version": "2024.1.0",
  "description": "Interact with GitHub repositories, issues, pull requests, and code.",
  "publisher": {
    "name": "Anthropic / MCP",
    "url": "https://modelcontextprotocol.io",
    "verified": true
  },
  "install": {
    "type": "npx",
    "package": "@modelcontextprotocol/server-github",
    "version": "latest"
  },
  "config": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": {
        "description": "GitHub personal access token with repo scope.",
        "required": true,
        "secret": true
      }
    }
  },
  "clients": ["claude-desktop", "cursor", "windsurf", "vscode"],
  "permissions": ["network"],
  "source_url": "https://github.com/modelcontextprotocol/servers/tree/master/src/github",
  "license": "MIT",
  "tags": ["github", "git", "api"]
}
```

Full schema: [`schema/manifest.schema.json`](schema/manifest.schema.json)

---

## Available servers

| Name | Description | Publisher | Verified |
|---|---|---|---|
| [airtable](servers/airtable/manifest.json) | Read and write Airtable bases, tables, and records | community | — |
| [brave-search](servers/brave-search/manifest.json) | Web and local search via the Brave Search API | Anthropic / MCP | ✓ |
| [fetch](servers/fetch/manifest.json) | Retrieve content from URLs and web pages | Anthropic / MCP | ✓ |
| [filesystem](servers/filesystem/manifest.json) | Secure file operations with configurable access controls | Anthropic / MCP | ✓ |
| [github](servers/github/manifest.json) | Repos, issues, PRs, and code search via the GitHub API | Anthropic / MCP | ✓ |
| [gitlab](servers/gitlab/manifest.json) | Repos, issues, MRs, and file operations via the GitLab API | Anthropic / MCP | ✓ |
| [hubspot](servers/hubspot/manifest.json) | Contacts, companies, deals, and tasks via HubSpot CRM | HubSpot | ✓ |
| [linear](servers/linear/manifest.json) | Issues, projects, and teams via the Linear GraphQL API | tacticlaunch | — |
| [notion](servers/notion/manifest.json) | Pages, databases, and search via the Notion API | Notion / makenotion | ✓ |
| [postgres](servers/postgres/manifest.json) | Read-only PostgreSQL access with schema inspection | Anthropic / MCP | ✓ |
| [puppeteer](servers/puppeteer/manifest.json) | Browser automation and web scraping via Puppeteer | Anthropic / MCP | ✓ |
| [sentry](servers/sentry/manifest.json) | Issues, errors, and projects via the Sentry API | Sentry / getsentry | ✓ |
| [shopify](servers/shopify/manifest.json) | Products, orders, and customers via the Shopify Admin API | community | — |
| [slack](servers/slack/manifest.json) | Messages, channels, and users via the Slack API | Anthropic / MCP | ✓ |
| [sqlite](servers/sqlite/manifest.json) | Read and write a local SQLite database | Anthropic / MCP | ✓ |
| [stripe](servers/stripe/manifest.json) | Payments, customers, and subscriptions via the Stripe API | Stripe | ✓ |

---

## Contributing

Want to add a server? See [CONTRIBUTING.md](CONTRIBUTING.md).

Community contributions are what make this registry useful. If you maintain an MCP server or know of one that's missing, a pull request is the fastest way to get it in.

---

## License

MIT