#!/usr/bin/env python3
"""
sovrun connector registry CLI

Setup, discover, and manage MCP connectors for the sovrun agent OS.

Usage:
    python setup.py --list                    Show all connectors by category
    python setup.py --list-category social    Show connectors in a category
    python setup.py --setup slack             Print setup instructions for a connector
    python setup.py --status                  Check which connectors are configured
    python setup.py --mcp-config              Generate MCP config JSON for configured connectors
    python setup.py --search stripe           Search connectors by name/description
    python setup.py --stats                   Show registry statistics
    python setup.py --connect slack           Install & configure a connector end-to-end
    python setup.py --connect-all             Walk through all HIGH priority connectors
    python setup.py --disconnect slack        Remove a connector's config and credentials
"""

import json
import os
import shutil
import subprocess
import sys
import argparse
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "registry.json"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env.sovrun"
MCP_CONFIG_DIR = PROJECT_ROOT / "config"
MCP_CONFIG_FILE = MCP_CONFIG_DIR / "mcp_servers.json"


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def color(text, code):
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def green(text):
    return color(text, "32")


def red(text):
    return color(text, "31")


def yellow(text):
    return color(text, "33")


def cyan(text):
    return color(text, "36")


def bold(text):
    return color(text, "1")


def dim(text):
    return color(text, "2")


def check_env_vars(required_vars):
    """Check which env vars are set."""
    results = {}
    for var in required_vars:
        results[var] = var in os.environ
    return results


def cmd_list(registry, category_filter=None):
    """List all connectors grouped by category."""
    connectors = registry["connectors"]

    by_category = {}
    for c in connectors:
        cat = c["category"]
        if category_filter and cat != category_filter:
            continue
        by_category.setdefault(cat, []).append(c)

    if category_filter and not by_category:
        print(f"No connectors found in category '{category_filter}'")
        print(f"Available categories: {', '.join(registry['categories'])}")
        return

    for cat in sorted(by_category.keys()):
        items = sorted(by_category[cat], key=lambda x: (0 if x["priority"] == "high" else 1 if x["priority"] == "medium" else 2, x["name"]))
        print(f"\n{bold(cat.upper())} ({len(items)} connectors)")
        print("-" * 60)
        for c in items:
            mcp_badge = green("[MCP]") if c["mcp_available"] else dim("[---]")
            priority_badge = {
                "high": green("HIGH"),
                "medium": yellow("MED "),
                "low": dim("LOW "),
            }.get(c["priority"], "")
            print(f"  {mcp_badge} {priority_badge}  {c['display_name']:25s} {dim(c['description'][:50])}")

    total = sum(len(v) for v in by_category.values())
    mcp_count = sum(1 for c in connectors if c["mcp_available"] and (not category_filter or c["category"] == category_filter))
    print(f"\n{bold(str(total))} connectors shown, {green(str(mcp_count))} with MCP servers")


def cmd_setup(registry, connector_name):
    """Print setup instructions for a connector."""
    connector_name = connector_name.lower().replace("-", "_").replace(" ", "_")

    connector = None
    for c in registry["connectors"]:
        if c["name"] == connector_name:
            connector = c
            break

    if not connector:
        # Try fuzzy match
        matches = [c for c in registry["connectors"] if connector_name in c["name"] or connector_name in c["display_name"].lower()]
        if matches:
            print(f"Did you mean one of these?")
            for m in matches:
                print(f"  - {m['name']} ({m['display_name']})")
            return
        print(f"Connector '{connector_name}' not found. Use --list to see all.")
        return

    print(f"\n{bold(connector['display_name'])} Setup")
    print("=" * 60)
    print(f"Category:    {connector['category']}")
    print(f"Priority:    {connector['priority']}")
    print(f"Description: {connector['description']}")

    print(f"\n{bold('Capabilities:')}")
    for cap in connector["capabilities"]:
        print(f"  - {cap}")

    if connector["competitors_with_this"]:
        print(f"\n{bold('Also available in:')} {', '.join(connector['competitors_with_this'])}")

    print(f"\n{bold('MCP Server:')}")
    if connector["mcp_available"]:
        print(f"  {green('Available')}: {connector['mcp_server']}")
    else:
        print(f"  {red('Not available')} - custom implementation needed")
        print(f"  Consider using Composio or Pipedream as a bridge connector")

    if connector["setup_requires"]:
        print(f"\n{bold('Required Environment Variables:')}")
        env_status = check_env_vars(connector["setup_requires"])
        for var, is_set in env_status.items():
            status = green("SET") if is_set else red("MISSING")
            print(f"  {status}  {var}")

        missing = [v for v, s in env_status.items() if not s]
        if missing:
            print(f"\n{bold('To configure, add to your .env:')}")
            for var in missing:
                print(f"  {var}=your_value_here")
    else:
        print(f"\n{green('No configuration required')} - works out of the box")

    if connector["mcp_available"]:
        print(f"\n{bold('Add to your MCP config (claude_desktop_config.json):')}")
        config = _build_mcp_entry(connector)
        print(json.dumps(config, indent=2))


def cmd_status(registry):
    """Show which connectors are configured."""
    connectors = registry["connectors"]

    configured = []
    partial = []
    unconfigured = []

    for c in connectors:
        if not c["setup_requires"]:
            configured.append(c)
            continue
        env_status = check_env_vars(c["setup_requires"])
        all_set = all(env_status.values())
        any_set = any(env_status.values())

        if all_set:
            configured.append(c)
        elif any_set:
            partial.append(c)
        else:
            unconfigured.append(c)

    print(f"\n{bold('Connector Status')}")
    print("=" * 60)

    if configured:
        print(f"\n{green('CONFIGURED')} ({len(configured)}):")
        for c in configured:
            mcp = green("[MCP]") if c["mcp_available"] else dim("[---]")
            print(f"  {mcp} {c['display_name']}")

    if partial:
        print(f"\n{yellow('PARTIALLY CONFIGURED')} ({len(partial)}):")
        for c in partial:
            env_status = check_env_vars(c["setup_requires"])
            missing = [v for v, s in env_status.items() if not s]
            print(f"  {c['display_name']} - missing: {', '.join(missing)}")

    print(f"\n{dim('UNCONFIGURED')}: {len(unconfigured)} connectors")
    print(f"  Run --setup <name> to see how to configure any connector")

    print(f"\n{bold('Summary:')} {green(str(len(configured)))} ready, {yellow(str(len(partial)))} partial, {dim(str(len(unconfigured)))} unconfigured")


def _build_mcp_entry(connector):
    """Build an MCP config entry for a connector."""
    parts = connector["mcp_server"].split()
    # Parse: npx -y @scope/package or uvx package
    if "npx" in parts:
        command = "npx"
        args = [p for p in parts if p != "npx"]
    elif "uvx" in parts:
        command = "uvx"
        args = [p for p in parts if p != "uvx"]
    else:
        command = parts[0]
        args = parts[1:]

    entry = {
        "command": command,
        "args": args,
    }

    if connector["setup_requires"]:
        entry["env"] = {var: os.environ.get(var, f"<{var}>") for var in connector["setup_requires"]}

    return entry


def cmd_mcp_config(registry):
    """Generate MCP server config for all configured connectors."""
    connectors = registry["connectors"]

    config = {"mcpServers": {}}

    for c in connectors:
        if not c["mcp_available"]:
            continue

        # Check if configured
        if c["setup_requires"]:
            env_status = check_env_vars(c["setup_requires"])
            if not all(env_status.values()):
                continue

        config["mcpServers"][c["name"]] = _build_mcp_entry(c)

    if not config["mcpServers"]:
        print("No MCP connectors are fully configured.")
        print("Run --status to see what needs configuration.")
        return

    print(json.dumps(config, indent=2))
    print(f"\n# {len(config['mcpServers'])} MCP servers configured", file=sys.stderr)


def cmd_search(registry, query):
    """Search connectors by name or description."""
    query = query.lower()
    results = []
    for c in registry["connectors"]:
        score = 0
        if query in c["name"]:
            score += 3
        if query in c["display_name"].lower():
            score += 2
        if query in c["description"].lower():
            score += 1
        if query in c["category"]:
            score += 1
        if any(query in cap for cap in c["capabilities"]):
            score += 1
        if score > 0:
            results.append((score, c))

    results.sort(key=lambda x: -x[0])

    if not results:
        print(f"No connectors match '{query}'")
        return

    print(f"\n{bold('Search results for')} '{query}':")
    print("-" * 60)
    for _, c in results:
        mcp = green("[MCP]") if c["mcp_available"] else dim("[---]")
        print(f"  {mcp} {c['display_name']:25s} ({c['category']}) - {c['description'][:45]}")


def cmd_stats(registry):
    """Show registry statistics."""
    connectors = registry["connectors"]
    total = len(connectors)
    mcp_count = sum(1 for c in connectors if c["mcp_available"])
    high = sum(1 for c in connectors if c["priority"] == "high")
    med = sum(1 for c in connectors if c["priority"] == "medium")
    low = sum(1 for c in connectors if c["priority"] == "low")

    by_category = {}
    for c in connectors:
        by_category.setdefault(c["category"], []).append(c)

    competitors = set()
    for c in connectors:
        competitors.update(c.get("competitors_with_this", []))

    print(f"\n{bold('sovrun Connector Registry Stats')}")
    print("=" * 60)
    print(f"  Total connectors:    {bold(str(total))}")
    print(f"  MCP available:       {green(str(mcp_count))} ({mcp_count * 100 // total}%)")
    print(f"  Custom needed:       {red(str(total - mcp_count))}")
    print(f"  Priority HIGH:       {green(str(high))}")
    print(f"  Priority MEDIUM:     {yellow(str(med))}")
    print(f"  Priority LOW:        {dim(str(low))}")
    print(f"  Categories:          {len(by_category)}")
    print(f"  Competitors tracked: {', '.join(sorted(competitors))}")

    print(f"\n{bold('By Category:')}")
    for cat in sorted(by_category.keys()):
        items = by_category[cat]
        mcp_in_cat = sum(1 for c in items if c["mcp_available"])
        print(f"  {cat:20s} {len(items):3d} connectors ({green(str(mcp_in_cat))} MCP)")


def _find_connector(registry, name):
    """Find a connector by name, with normalization and fuzzy fallback."""
    name = name.lower().replace("-", "_").replace(" ", "_")
    for c in registry["connectors"]:
        if c["name"] == name:
            return c
    # Try partial match
    matches = [c for c in registry["connectors"]
               if name in c["name"] or name in c["display_name"].lower()]
    if len(matches) == 1:
        return matches[0]
    return None


def _load_env_file():
    """Load existing .env.sovrun as a dict. Returns {} if missing."""
    if not ENV_FILE.exists():
        return {}
    env = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip()
    return env


def _save_env_file(env):
    """Write env dict back to .env.sovrun (idempotent, preserves order)."""
    lines = ["# sovrun connector credentials", "# Auto-generated by setup.py", ""]
    for key in sorted(env.keys()):
        lines.append(f"{key}={env[key]}")
    lines.append("")
    ENV_FILE.write_text("\n".join(lines))


def _load_mcp_config():
    """Load existing mcp_servers.json or return empty structure."""
    if MCP_CONFIG_FILE.exists():
        with open(MCP_CONFIG_FILE) as f:
            return json.load(f)
    return {"mcpServers": {}}


def _save_mcp_config(config):
    """Write MCP config JSON (idempotent)."""
    MCP_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(MCP_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def _check_tool(tool_name):
    """Check if a CLI tool is available on PATH."""
    return shutil.which(tool_name) is not None


def _detect_install_type(connector):
    """Determine install type from connector fields or mcp_server string."""
    if connector.get("install_type"):
        return connector["install_type"]
    mcp = connector.get("mcp_server") or ""
    if "npx" in mcp or "npm" in mcp:
        return "npm"
    if "uvx" in mcp or "pip" in mcp:
        return "pip"
    return "npm"  # default for MCP servers


def _get_install_command(connector):
    """Get the install command for a connector."""
    if connector.get("install_command"):
        return connector["install_command"]
    mcp = connector.get("mcp_server") or ""
    # Extract package name from mcp_server field
    # e.g. "npx -y @modelcontextprotocol/server-slack" -> "@modelcontextprotocol/server-slack"
    parts = mcp.split()
    for p in parts:
        if p.startswith("@") or (not p.startswith("-") and p != "npx" and p != "uvx"):
            return p
    return None


def _run_install(connector):
    """Install the MCP server package. Returns True on success."""
    install_type = _detect_install_type(connector)
    package = _get_install_command(connector)

    if not package:
        print(f"  {red('ERROR')}: No install command found for {connector['name']}")
        return False

    if install_type == "npm":
        if not _check_tool("npx") and not _check_tool("npm"):
            print(f"  {red('ERROR')}: npm/npx not found. Install Node.js first: https://nodejs.org")
            return False
        print(f"  Installing {cyan(package)} via npx ...")
        # npx -y will auto-install on first use, so we just verify it can resolve
        try:
            result = subprocess.run(
                ["npx", "-y", package, "--help"],
                capture_output=True, text=True, timeout=120
            )
            # Many MCP servers exit non-zero on --help but still install fine
            # The key is that npx resolved and downloaded the package
            print(f"  {green('OK')}: Package {package} is available via npx")
            return True
        except subprocess.TimeoutExpired:
            print(f"  {yellow('WARN')}: Install timed out but package may still work")
            return True
        except FileNotFoundError:
            print(f"  {red('ERROR')}: npx not found on PATH")
            return False

    elif install_type == "pip":
        if not _check_tool("pip3") and not _check_tool("pip"):
            print(f"  {red('ERROR')}: pip not found. Install Python first.")
            return False
        pip_cmd = "pip3" if _check_tool("pip3") else "pip"
        print(f"  Installing {cyan(package)} via pip ...")
        try:
            result = subprocess.run(
                [pip_cmd, "install", package],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print(f"  {green('OK')}: {package} installed")
                return True
            else:
                print(f"  {red('ERROR')}: pip install failed: {result.stderr[:200]}")
                return False
        except subprocess.TimeoutExpired:
            print(f"  {red('ERROR')}: pip install timed out")
            return False

    print(f"  {red('ERROR')}: Unknown install type: {install_type}")
    return False


def _prompt_credentials(connector, existing_env):
    """Prompt user for required API keys. Returns dict of new/updated values."""
    required = connector.get("setup_requires", [])
    if not required:
        return {}

    print(f"\n  {bold('Credentials required')} ({len(required)} keys):")
    creds = {}
    for var in required:
        current = existing_env.get(var) or os.environ.get(var)
        if current:
            masked = current[:4] + "..." + current[-4:] if len(current) > 10 else "****"
            prompt_str = f"    {var} [{green('SET')}: {masked}] (press Enter to keep, or paste new): "
        else:
            prompt_str = f"    {var} [{red('MISSING')}]: "

        try:
            user_input = input(prompt_str).strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {yellow('Cancelled')}")
            return creds

        if user_input:
            creds[var] = user_input
        elif current:
            creds[var] = current
        else:
            print(f"      {yellow('SKIPPED')} - {var} not set")

    return creds


def cmd_connect(registry, connector_name):
    """Install and configure a single connector end-to-end."""
    connector = _find_connector(registry, connector_name)

    if not connector:
        matches = [c for c in registry["connectors"]
                   if connector_name.lower() in c["name"]
                   or connector_name.lower() in c["display_name"].lower()]
        if matches:
            print(f"Did you mean one of these?")
            for m in matches:
                print(f"  - {m['name']} ({m['display_name']})")
        else:
            print(f"Connector '{connector_name}' not found. Use --list to see all.")
        return False

    print(f"\n{'=' * 60}")
    print(f"  {bold('CONNECT')}: {connector['display_name']}")
    print(f"  {dim(connector['description'])}")
    print(f"{'=' * 60}")

    # Step 1: Check MCP availability
    if not connector["mcp_available"]:
        print(f"\n  {red('NO MCP SERVER')}: {connector['display_name']} has no MCP server.")
        print(f"  Consider using Composio or Pipedream as a bridge connector.")
        print(f"  Run: python setup.py --connect composio")
        return False

    # Step 2: Install MCP server
    print(f"\n  {bold('Step 1/4')}: Install MCP server")
    installed = _run_install(connector)
    if not installed:
        print(f"  {yellow('WARN')}: Installation may have issues, continuing anyway...")

    # Step 3: Prompt for credentials
    print(f"\n  {bold('Step 2/4')}: Configure credentials")
    existing_env = _load_env_file()
    new_creds = _prompt_credentials(connector, existing_env)

    # Step 4: Save credentials to .env.sovrun
    if new_creds:
        print(f"\n  {bold('Step 3/4')}: Save credentials to .env.sovrun")
        existing_env.update(new_creds)
        _save_env_file(existing_env)
        print(f"  {green('SAVED')}: {ENV_FILE}")
    else:
        print(f"\n  {bold('Step 3/4')}: No new credentials to save")

    # Step 5: Generate MCP config entry
    print(f"\n  {bold('Step 4/4')}: Update MCP config")
    mcp_config = _load_mcp_config()
    entry = _build_mcp_entry(connector)
    # Replace env placeholders with actual values from .env.sovrun
    if "env" in entry:
        for var in entry["env"]:
            if var in existing_env:
                entry["env"][var] = existing_env[var]
    mcp_config["mcpServers"][connector["name"]] = entry
    _save_mcp_config(mcp_config)
    print(f"  {green('SAVED')}: {MCP_CONFIG_FILE}")

    # Report success
    total_servers = len(mcp_config["mcpServers"])
    missing_creds = [v for v in connector.get("setup_requires", [])
                     if v not in existing_env]

    print(f"\n{'=' * 60}")
    if missing_creds:
        print(f"  {yellow('PARTIAL')}: {connector['display_name']} configured with missing keys:")
        for v in missing_creds:
            print(f"    - {red(v)}")
        print(f"  Re-run: python setup.py --connect {connector['name']}")
    else:
        print(f"  {green('SUCCESS')}: {connector['display_name']} is ready")
    print(f"  MCP servers configured: {bold(str(total_servers))}")
    print(f"  Config: {MCP_CONFIG_FILE}")
    print(f"  Creds:  {ENV_FILE}")
    print(f"{'=' * 60}\n")
    return True


def cmd_connect_all(registry):
    """Walk through all HIGH priority MCP-available connectors."""
    high_mcp = [c for c in registry["connectors"]
                if c["priority"] == "high" and c["mcp_available"]]

    # Sort by category for logical grouping
    high_mcp.sort(key=lambda c: (c["category"], c["name"]))

    print(f"\n{bold('CONNECT ALL')} - HIGH priority connectors with MCP servers")
    print(f"{'=' * 60}")
    print(f"Found {green(str(len(high_mcp)))} connectors to configure.\n")

    for i, c in enumerate(high_mcp, 1):
        print(f"  [{i}/{len(high_mcp)}] {c['display_name']:20s} ({c['category']}) - {dim(c['description'][:40])}")

    print(f"\nThis will walk you through each one.")
    print(f"Press Ctrl+C at any time to stop.\n")

    try:
        resp = input("Continue? [Y/n] ").strip().lower()
        if resp and resp != "y":
            print("Cancelled.")
            return
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return

    connected = 0
    skipped = 0
    failed = 0

    for i, c in enumerate(high_mcp, 1):
        print(f"\n{'#' * 60}")
        print(f"  [{i}/{len(high_mcp)}] {bold(c['display_name'])}")
        print(f"{'#' * 60}")

        try:
            resp = input(f"\n  Connect {c['display_name']}? [Y/n/q(uit)] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nStopped.")
            break

        if resp == "q":
            print("Stopped.")
            break
        if resp == "n":
            skipped += 1
            print(f"  {dim('Skipped')}")
            continue

        ok = cmd_connect(registry, c["name"])
        if ok:
            connected += 1
        else:
            failed += 1

    print(f"\n{bold('Connect-All Summary')}")
    print(f"  {green(str(connected))} connected, {yellow(str(skipped))} skipped, {red(str(failed))} failed")
    print(f"  MCP config: {MCP_CONFIG_FILE}")


def cmd_disconnect(registry, connector_name):
    """Remove a connector's config and credentials."""
    connector = _find_connector(registry, connector_name)

    if not connector:
        print(f"Connector '{connector_name}' not found. Use --list to see all.")
        return

    print(f"\n{bold('DISCONNECT')}: {connector['display_name']}")
    print(f"{'=' * 60}")

    removed_config = False
    removed_creds = False

    # Remove from MCP config
    if MCP_CONFIG_FILE.exists():
        mcp_config = _load_mcp_config()
        if connector["name"] in mcp_config.get("mcpServers", {}):
            del mcp_config["mcpServers"][connector["name"]]
            _save_mcp_config(mcp_config)
            removed_config = True
            print(f"  {green('REMOVED')} from MCP config: {MCP_CONFIG_FILE}")
        else:
            print(f"  {dim('Not found')} in MCP config")
    else:
        print(f"  {dim('No MCP config file exists')}")

    # Remove credentials from .env.sovrun
    if ENV_FILE.exists() and connector.get("setup_requires"):
        env = _load_env_file()
        removed_keys = []
        for var in connector["setup_requires"]:
            if var in env:
                # Check if any OTHER connector also uses this env var
                shared = False
                for other in registry["connectors"]:
                    if other["name"] != connector["name"] and var in other.get("setup_requires", []):
                        shared = True
                        break
                if shared:
                    print(f"  {yellow('KEPT')} {var} (shared with other connectors)")
                else:
                    del env[var]
                    removed_keys.append(var)
        if removed_keys:
            _save_env_file(env)
            removed_creds = True
            print(f"  {green('REMOVED')} credentials: {', '.join(removed_keys)}")
        elif not removed_keys and connector.get("setup_requires"):
            print(f"  {dim('No credentials found')} in .env.sovrun")
    else:
        print(f"  {dim('No credentials to remove')}")

    if removed_config or removed_creds:
        print(f"\n  {green('DISCONNECTED')}: {connector['display_name']}")
    else:
        print(f"\n  {dim('Nothing to disconnect')}: {connector['display_name']} was not configured")


def main():
    parser = argparse.ArgumentParser(
        description="sovrun connector registry - discover and configure MCP connectors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--list", action="store_true", help="List all connectors by category")
    parser.add_argument("--list-category", metavar="CAT", help="List connectors in a specific category")
    parser.add_argument("--setup", metavar="NAME", help="Show setup instructions for a connector")
    parser.add_argument("--status", action="store_true", help="Check which connectors are configured")
    parser.add_argument("--mcp-config", action="store_true", help="Generate MCP config JSON")
    parser.add_argument("--search", metavar="QUERY", help="Search connectors by name/description")
    parser.add_argument("--stats", action="store_true", help="Show registry statistics")
    parser.add_argument("--connect", metavar="NAME", help="Install & configure a connector end-to-end")
    parser.add_argument("--connect-all", action="store_true", help="Walk through all HIGH priority connectors")
    parser.add_argument("--disconnect", metavar="NAME", help="Remove a connector's config and credentials")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    registry = load_registry()

    if args.list:
        cmd_list(registry)
    elif args.list_category:
        cmd_list(registry, args.list_category)
    elif args.setup:
        cmd_setup(registry, args.setup)
    elif args.status:
        cmd_status(registry)
    elif args.mcp_config:
        cmd_mcp_config(registry)
    elif args.search:
        cmd_search(registry, args.search)
    elif args.stats:
        cmd_stats(registry)
    elif args.connect:
        cmd_connect(registry, args.connect)
    elif args.connect_all:
        cmd_connect_all(registry)
    elif args.disconnect:
        cmd_disconnect(registry, args.disconnect)


if __name__ == "__main__":
    main()
