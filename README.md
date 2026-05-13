# ArcMesh Registry

The open registry of MCP servers — install any MCP server with one command.

[MCP (Model Context Protocol)](https://modelcontextprotocol.io) lets AI assistants like Claude connect to external tools — GitHub, Notion, Stripe, databases, and more. Setting up MCP servers manually means finding the package, reading docs, editing JSON config files by hand, and figuring out where each client stores its config. ArcMesh eliminates all of that.

```bash
apm install github
apm install notion
apm install stripe
```

Each entry in this registry is a single `manifest.json` file that describes how to install, configure, and run an MCP server. The [arcmesh-pm](https://github.com/arcmesh-labs/arcmesh-pm) CLI reads these manifests, prompts you for any required tokens, and writes the correct config block automatically.

---

## Supported clients

| Client | Status |
|---|---|
| Claude Desktop | ✅ Supported |
| Cursor | 🔜 Coming soon |
| Windsurf | 🔜 Coming soon |
| VS Code | 🔜 Coming soon |

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

## Quick start

### Install arcmesh-pm

```bash
pip install arcmesh-pm
```

### Install a server

```bash
apm install github
```

`apm` will prompt you for any required tokens, then write the config block to your Claude Desktop config file automatically.

### Other commands

```bash
apm list                                          # browse all available servers
apm search notion                                 # search by name or description
apm uninstall github                              # remove a server
apm set-env github GITHUB_PERSONAL_ACCESS_TOKEN   # update a token after install
apm doctor                                        # check your config for issues
apm status                                        # list installed servers and token status
```

### Manual install (without apm)

Copy the `config` block from any `manifest.json` directly into your Claude Desktop config file.

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

---

## Repository structure

```
servers/
  <name>/
    manifest.json        ← one server, one file
schema/
  manifest.schema.json   ← JSON Schema (draft-07) for validation
validate_manifests.py    ← local validation script
CONTRIBUTING.md          ← how to add a new server
```

---

## Contributing

Want to add a server? See [CONTRIBUTING.md](CONTRIBUTING.md).

Community contributions are what make this registry useful. If you maintain an MCP server or know of one that's missing, a pull request is the fastest way to get it in.

---

## License

MIT