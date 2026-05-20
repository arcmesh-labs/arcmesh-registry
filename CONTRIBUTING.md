# Contributing to ArcMesh Registry

Thanks for helping grow the registry. Every new manifest makes ArcMesh more useful for everyone.

---

## What is a manifest?

A manifest is a single `servers/<name>/manifest.json` file that describes an MCP server — its package name, how to run it, which environment variables it needs, and which clients it supports. The [arcmesh-pm](https://github.com/arcmesh-labs/arcmesh-pm) CLI reads manifests to install servers automatically.

See the full spec: [`schema/manifest.schema.json`](schema/manifest.schema.json)

---

## Before you start

**Research the package first.** Before writing a manifest, find the official or best-maintained npm/pip package for the server. Do not invent package names. Check:

- The server's official GitHub repo
- npmjs.com or pypi.org for the package name and latest version
- The server's own documentation for correct env var names and auth details

**Check if it already exists.** Search [`servers/`](servers/) and [`servers/index.json`](servers/index.json) before opening a PR.

---

## Adding a new server

### 1. Create the manifest file

```
servers/<name>/manifest.json
```

The directory name must match the `"name"` field inside the file.

Use an existing manifest as a reference — [github](servers/github/manifest.json) is a good starting point for single-token npx servers, [slack](servers/slack/manifest.json) for servers with multiple env vars.

### 2. Validate locally

Install the dependency and run the validation script from the repo root:

```bash
pip install jsonschema
python3 validate_manifests.py
```

All checks must pass before opening a PR:
- Schema validation against `manifest.schema.json`
- Cross-check that your server appears in `servers/index.json`
- Content checks (name matches directory, env vars have `required` and `secret` set, etc.)

### 3. Add an entry to servers/index.json

Append your server to the `"servers"` array in [`servers/index.json`](servers/index.json):

```json
{
  "name": "your-server",
  "description": "One sentence from your manifest description.",
  "version": "1.0.0",
  "publisher": "your name or org",
  "verified": false,
  "tags": ["tag1", "tag2"],
  "path": "servers/your-server/manifest.json"
}
```

`verified` is always `false` for community submissions. The ArcMesh team flips it after reviewing the publisher.

### 4. Open a pull request

Include in the PR description:
- Link to the package on npm or PyPI
- Link to the server's source code
- Brief note on what the server does and why it belongs in the registry

---

## Manifest field reference

### Required fields checklist

- [ ] `name` matches the directory name exactly
- [ ] `version` is valid semver (e.g. `1.0.0`)
- [ ] `description` is 10–300 characters, plain English
- [ ] `publisher.verified` is `false` for community submissions
- [ ] `install.type` is one of the allowed enum values
- [ ] `install.package` is a real, published package name
- [ ] `config.args` uses `${VAR_NAME}` placeholders for any user-supplied values
- [ ] `config.env` entries have both `required` and `secret` explicitly set
- [ ] `permissions` lists every capability the server actually uses
- [ ] `source_url` points to public, browsable source code
- [ ] `license` is a valid SPDX identifier (e.g. `MIT`, `Apache-2.0`)

### install.type guidance

| Runtime | `type` | `command` | Example |
|---|---|---|---|
| Node / npm | `npx` | `npx` | `@modelcontextprotocol/server-github` |
| Python / pip | `pip` | `python` | `mcp-server-git` |
| Python / uv | `uvx` | `uvx` | `mcp-server-fetch` |
| Docker | `docker` | `docker` | `ghcr.io/org/mcp-server:latest` |
| Binary | `binary` | path or name | `mcp-server-sqlite` |

### permissions enum

Only use values defined in the schema. If your server needs a capability not listed, open an issue before submitting.

| Value | When to use |
|---|---|
| `filesystem` | Reads or writes local files |
| `network` | Makes outbound HTTP/TCP calls |
| `database` | Connects to a database server |
| `process` | Spawns or manages OS processes |
| `browser` | Controls a browser via automation |
| `memory` | Persists state between sessions |
| `secrets` | Handles API keys, passwords, or tokens |
| `git` | Reads or writes git repositories |

### clients field

List only clients the server is known to work with. Current valid values:

```
claude-desktop  cursor  windsurf  vscode  zed  continue
```

`apm` supports Claude Desktop, VS Code, Cursor, and Windsurf. List all clients the server is compatible with so the registry is accurate across all of them.

### Naming rules

- Lowercase letters, digits, and hyphens only: `^[a-z][a-z0-9-]*$`
- Use the canonical upstream name where one exists (`postgres`, not `postgresql`)
- Scoped npm packages drop the scope: `@company/server-foo` → `foo`

---

## Updating an existing manifest

- Bump `version` in the manifest file
- Update the `version` field in `servers/index.json` to match
- Do not change `name` — it is the stable identifier used by the CLI

---

## Review criteria

PRs are merged when:

1. `validate_manifests.py` passes with zero errors
2. `source_url` points to publicly accessible, reviewable source code
3. `install.package` is a real published package (verifiable on npmjs.com or pypi.org)
4. `permissions` accurately reflects what the server does — over-claiming is grounds for rejection
5. No sensitive values appear anywhere except as `${VAR}` placeholders in `config.args`
6. `servers/index.json` has been updated with the new entry

---

## Questions?

Open an issue or start a discussion on GitHub.