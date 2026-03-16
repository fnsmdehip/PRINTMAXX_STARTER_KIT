#!/usr/bin/env python3
"""
Batch Surge Deployer — deploys all undeployed apps to surge.sh
Scans builds/ for apps with index.html, checks DEPLOYMENT_URLS.md, deploys missing ones.

Usage:
    python3 batch_surge_deployer.py --scan       # Show what would be deployed
    python3 batch_surge_deployer.py --deploy      # Deploy all undeployed apps
    python3 batch_surge_deployer.py --deploy APP  # Deploy specific app
"""

import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILDS_DIR = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
DEPLOYMENT_FILE = PROJECT_ROOT / "OPS" / "DEPLOYMENT_URLS.md"


def get_deployed_apps():
    """Read DEPLOYMENT_URLS.md and return set of deployed app names."""
    deployed = set()
    if DEPLOYMENT_FILE.exists():
        content = DEPLOYMENT_FILE.read_text()
        for line in content.split("\n"):
            match = re.search(r"\|\s*(\S+)\s*\|.*surge\.sh", line)
            if match:
                deployed.add(match.group(1).strip())
    return deployed


def get_deployable_apps():
    """Find all apps with index.html in builds/."""
    apps = []
    if not BUILDS_DIR.exists():
        return apps
    for app_dir in sorted(BUILDS_DIR.iterdir()):
        if app_dir.is_dir():
            index = app_dir / "index.html"
            if index.exists():
                size = index.stat().st_size
                apps.append({
                    "name": app_dir.name,
                    "path": str(app_dir),
                    "size_kb": round(size / 1024, 1),
                })
    return apps


def scan():
    """Show deployment status of all apps."""
    deployed = get_deployed_apps()
    deployable = get_deployable_apps()

    print(f"\n=== Batch Surge Deployer ===")
    print(f"Deployed apps: {len(deployed)}")
    print(f"Apps with index.html: {len(deployable)}")

    undeployed = []
    for app in deployable:
        status = "LIVE" if app["name"] in deployed else "NOT DEPLOYED"
        marker = "  " if status == "LIVE" else ">>"
        print(f"  {marker} {app['name']:30s} {app['size_kb']:>8.1f} KB  [{status}]")
        if status == "NOT DEPLOYED":
            undeployed.append(app)

    if undeployed:
        print(f"\n{len(undeployed)} apps ready to deploy:")
        for app in undeployed:
            print(f"  surge {app['path']} {app['name']}.surge.sh")
    else:
        print("\nAll apps deployed.")

    return undeployed


def deploy(app_name=None):
    """Deploy apps to surge.sh."""
    deployed = get_deployed_apps()
    deployable = get_deployable_apps()

    if app_name:
        targets = [a for a in deployable if a["name"] == app_name]
        if not targets:
            print(f"App '{app_name}' not found or has no index.html")
            return
    else:
        targets = [a for a in deployable if a["name"] not in deployed]

    if not targets:
        print("Nothing to deploy.")
        return

    results = []
    for app in targets:
        domain = f"{app['name']}.surge.sh"
        print(f"\nDeploying {app['name']} → {domain}...")

        try:
            result = subprocess.run(
                ["surge", app["path"], domain],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                print(f"  SUCCESS: https://{domain}")
                results.append({"name": app["name"], "url": f"https://{domain}", "status": "LIVE"})
            else:
                print(f"  FAILED: {result.stderr[:200]}")
                results.append({"name": app["name"], "url": domain, "status": "FAILED"})
        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT after 120s")
            results.append({"name": app["name"], "url": domain, "status": "TIMEOUT"})
        except FileNotFoundError:
            print("  ERROR: surge CLI not found. Install with: npm install -g surge")
            return

    # Update DEPLOYMENT_URLS.md
    successes = [r for r in results if r["status"] == "LIVE"]
    if successes and DEPLOYMENT_FILE.exists():
        content = DEPLOYMENT_FILE.read_text()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_entries = []
        for r in successes:
            entry = f"| {r['name']} | {r['url']} | LIVE |"
            if entry not in content and r["name"] not in content:
                new_entries.append(entry)

        if new_entries:
            # Find the last table row and append after it
            lines = content.split("\n")
            insert_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith("|") and "surge.sh" in line:
                    insert_idx = i + 1

            if insert_idx:
                for entry in new_entries:
                    lines.insert(insert_idx, entry)
                    insert_idx += 1

                # Update timestamp
                for i, line in enumerate(lines):
                    if "Last updated:" in line:
                        lines[i] = f"**Last updated:** {timestamp}"
                        break

                DEPLOYMENT_FILE.write_text("\n".join(lines))
                print(f"\nUpdated DEPLOYMENT_URLS.md with {len(new_entries)} new entries")

    print(f"\nDeployment complete: {len(successes)} succeeded, {len(results) - len(successes)} failed")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--scan" in args:
        scan()
    elif "--deploy" in args:
        idx = args.index("--deploy")
        app_name = args[idx + 1] if idx + 1 < len(args) else None
        deploy(app_name)
    else:
        print("Usage:")
        print("  batch_surge_deployer.py --scan        # Show deployment status")
        print("  batch_surge_deployer.py --deploy       # Deploy all undeployed")
        print("  batch_surge_deployer.py --deploy APP   # Deploy specific app")
