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
"""

import json
import os
import sys
import argparse
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "registry.json"


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


if __name__ == "__main__":
    main()
