# ArcMesh Registry

The open registry of MCP servers — think **npm for MCP**.

Each entry is a single `manifest.json` file that describes how to install, configure, and run an MCP server in any supported client (Claude Desktop, Cursor, Windsurf, VS Code, and more).

---

## Structure

```
servers/
  <name>/
    manifest.json      ← one server, one file
schema/
  manifest.schema.json ← JSON Schema for validation
```

---

## Using a server

Install via the ArcMesh CLI (coming soon):

```bash
arcmesh install filesystem
arcmesh install postgres
```

Or copy the `config` block from `manifest.json` directly into your client's MCP settings.

**Claude Desktop example for `filesystem`:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/docs"]
    }
  }
}
```

---

## Manifest format

| Field | Required | Description |
|---|---|---|
| `name` | yes | Unique slug (`lowercase-hyphens`) |
| `version` | yes | Semver of the manifest entry |
| `description` | yes | One- or two-sentence summary |
| `publisher.name` | yes | Maintainer name |
| `publisher.verified` | yes | Verified by ArcMesh team |
| `install.type` | yes | `npx` \| `pip` \| `uvx` \| `docker` \| `binary` |
| `install.package` | yes | Package identifier |
| `config.command` | yes | Executable (e.g. `npx`, `python`) |
| `config.args` | yes | Args; use `${VAR}` for user values |
| `config.env` | no | Env vars with description + secret flag |
| `clients` | yes | Supported clients |
| `permissions` | yes | Coarse capabilities required |
| `source_url` | yes | Link to source code |
| `license` | yes | SPDX identifier |
| `homepage` | no | Project docs/website |
| `tags` | no | Search keywords |

Full spec: [`schema/manifest.schema.json`](schema/manifest.schema.json)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
