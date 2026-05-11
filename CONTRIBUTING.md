# Contributing to ArcMesh Registry

## Adding a new server

1. Create `servers/<name>/manifest.json` (name must match `"name"` inside the file).
2. Validate against the schema:
   ```bash
   npx ajv-cli validate -s schema/manifest.schema.json -d servers/<name>/manifest.json
   ```
3. Open a pull request. The CI check runs the same validation automatically.

### Naming rules

- Lowercase letters, digits, and hyphens only: `^[a-z][a-z0-9-]*$`
- Use the canonical upstream package name where one exists (e.g. `postgres`, not `postgresql` or `pg`).
- Scoped npm packages drop the scope: `@company/server-foo` → `foo`.

### Required fields checklist

- [ ] `name` matches the directory name
- [ ] `version` is valid semver
- [ ] `description` is 10–300 characters
- [ ] `publisher.verified` is `false` for community submissions (the team flips it after review)
- [ ] `install.type` is one of the allowed enum values
- [ ] `config.args` uses `${VAR_NAME}` for any value the user must supply
- [ ] `config.env` entries have `secret: true` for passwords and tokens
- [ ] `permissions` lists every capability the server actually uses
- [ ] `source_url` points to public, browsable source code
- [ ] `license` is a valid SPDX identifier

### install.type guidance

| Runtime | `type` | `command` | Example package |
|---|---|---|---|
| Node / npm | `npx` | `npx` | `@modelcontextprotocol/server-filesystem` |
| Python / PyPI | `pip` | `python` | `mcp-server-git` |
| Python / uv | `uvx` | `uvx` | `mcp-server-fetch` |
| Container | `docker` | `docker` | `ghcr.io/org/mcp-server:latest` |
| Standalone binary | `binary` | path or name | `mcp-server-sqlite` |

### permissions enum

Use only the values defined in the schema. If your server needs a capability not listed, open an issue to propose a new enum value before submitting the manifest.

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

## Updating an existing manifest

- Bump `version` in the manifest file.
- Do not change `name` (it is the stable identifier used by the CLI).

## Review criteria

PRs are merged when:
1. CI schema validation passes.
2. `source_url` points to publicly accessible, reviewable source.
3. `permissions` accurately reflects what the server does — over-claiming permissions is grounds for rejection.
4. No sensitive values (passwords, tokens) appear in any field other than as `${VAR}` placeholders.
