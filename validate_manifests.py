#!/usr/bin/env python3
"""
Validate all ArcMesh server manifests against manifest.schema.json.

Usage:
    cd ~/arcmesh-registry
    python3 validate_manifests.py

Requires:
    pip install jsonschema
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("Missing dependency. Run: pip install jsonschema")
    sys.exit(1)

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent
SCHEMA_PATH = REPO_ROOT / "schema" / "manifest.schema.json"
SERVERS_DIR = REPO_ROOT / "servers"
INDEX_PATH  = SERVERS_DIR / "index.json"

# ── Colours ──────────────────────────────────────────────────────────────────
GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):  print(f"  {GREEN}✓{RESET} {msg}")
def err(msg): print(f"  {RED}✗{RESET} {msg}")
def warn(msg):print(f"  {YELLOW}⚠{RESET} {msg}")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# ── 1. Schema validation ──────────────────────────────────────────────────────
def validate_manifests(schema: dict) -> tuple[list[str], list[str]]:
    passed, failed = [], []

    manifest_dirs = sorted(
        d for d in SERVERS_DIR.iterdir()
        if d.is_dir()
    )

    print(f"\n{BOLD}── Schema validation ({len(manifest_dirs)} servers) ──{RESET}")

    for server_dir in manifest_dirs:
        manifest_path = server_dir / "manifest.json"
        name = server_dir.name

        if not manifest_path.exists():
            warn(f"{name}: manifest.json missing — skipped")
            continue

        try:
            manifest = load_json(manifest_path)
        except json.JSONDecodeError as e:
            err(f"{name}: invalid JSON — {e}")
            failed.append(name)
            continue

        try:
            validate(instance=manifest, schema=schema,
                     format_checker=jsonschema.FormatChecker())
            ok(f"{name}")
            passed.append(name)
        except ValidationError as e:
            err(f"{name}: {e.message}  (path: {' → '.join(str(p) for p in e.absolute_path)})")
            failed.append(name)

    return passed, failed


# ── 2. Cross-checks ───────────────────────────────────────────────────────────
def cross_check_index(passed: list[str]) -> list[str]:
    """Verify every manifest dir has a matching entry in index.json."""
    issues = []

    print(f"\n{BOLD}── index.json cross-check ──{RESET}")

    if not INDEX_PATH.exists():
        err("index.json not found")
        return ["index.json missing"]

    try:
        index = load_json(INDEX_PATH)
    except json.JSONDecodeError as e:
        err(f"index.json invalid JSON — {e}")
        return ["index.json invalid"]

    indexed_names = {s["name"] for s in index.get("servers", [])}

    for name in passed:
        if name in indexed_names:
            ok(f"{name} in index.json")
        else:
            err(f"{name} missing from index.json")
            issues.append(name)

    # Reverse: index entries with no manifest dir
    for entry in index.get("servers", []):
        n = entry["name"]
        if not (SERVERS_DIR / n / "manifest.json").exists():
            warn(f"index.json references '{n}' but servers/{n}/manifest.json not found")
            issues.append(n)

    return issues


def content_checks(passed: list[str]) -> list[str]:
    """Spot-check field values that schema can't catch."""
    issues = []

    print(f"\n{BOLD}── Content checks ──{RESET}")

    for name in passed:
        manifest = load_json(SERVERS_DIR / name / "manifest.json")
        server_issues = []

        # name field must match directory name
        if manifest.get("name") != name:
            server_issues.append(f"name field '{manifest.get('name')}' ≠ directory '{name}'")

        # all env vars should have required + secret explicitly set
        env = manifest.get("config", {}).get("env", {})
        for var, meta in env.items():
            if "required" not in meta:
                server_issues.append(f"env.{var} missing 'required' field")
            if "secret" not in meta:
                server_issues.append(f"env.{var} missing 'secret' field")

        # install.type and config.command should be consistent
        install_type = manifest.get("install", {}).get("type")
        config_cmd   = manifest.get("config", {}).get("command")
        if install_type == "npx" and config_cmd != "npx":
            server_issues.append(f"install.type=npx but config.command='{config_cmd}'")
        if install_type == "pip" and config_cmd not in ("python", "python3", "uvx"):
            server_issues.append(f"install.type=pip but config.command='{config_cmd}'")

        if server_issues:
            for issue in server_issues:
                err(f"{name}: {issue}")
            issues.extend(server_issues)
        else:
            ok(f"{name}")

    return issues


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"\n{BOLD}{CYAN}ArcMesh manifest validator{RESET}")
    print(f"Registry: {REPO_ROOT}")

    if not SCHEMA_PATH.exists():
        print(f"{RED}schema/manifest.schema.json not found. Run from repo root.{RESET}")
        sys.exit(1)

    schema = load_json(SCHEMA_PATH)

    passed, failed = validate_manifests(schema)
    index_issues   = cross_check_index(passed)
    content_issues = content_checks(passed)

    # ── Summary ───────────────────────────────────────────────────────────────
    total  = len(passed) + len(failed)
    errors = len(failed) + len(index_issues) + len(content_issues)

    print(f"\n{BOLD}── Summary ──{RESET}")
    print(f"  Manifests validated : {total}")
    print(f"  Schema passed       : {GREEN}{len(passed)}{RESET}")
    print(f"  Schema failed       : {RED}{len(failed)}{RESET}" if failed else f"  Schema failed       : {len(failed)}")
    print(f"  Index issues        : {RED}{len(index_issues)}{RESET}" if index_issues else f"  Index issues        : {len(index_issues)}")
    print(f"  Content issues      : {RED}{len(content_issues)}{RESET}" if content_issues else f"  Content issues      : {len(content_issues)}")

    if errors == 0:
        print(f"\n{GREEN}{BOLD}All checks passed.{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{RED}{BOLD}{errors} issue(s) found — see above.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()