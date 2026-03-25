#!/usr/bin/env python3
"""App Factory Build & Submit Automation.

Automates the EAS build and submission pipeline for Expo apps.

Flow:
  1. Verify project structure and config
  2. Run eas build --platform ios --profile production
  3. Monitor build status
  4. Run eas submit --platform ios when build completes
  5. Log results to LEDGER/APP_FACTORY_BUILDS.csv

Usage:
  python3 AUTOMATIONS/app_factory/build_submit.py --build APP_DIR
  python3 AUTOMATIONS/app_factory/build_submit.py --submit APP_DIR
  python3 AUTOMATIONS/app_factory/build_submit.py --build-and-submit APP_DIR
  python3 AUTOMATIONS/app_factory/build_submit.py --status APP_DIR
  python3 AUTOMATIONS/app_factory/build_submit.py --batch --top 3
  python3 AUTOMATIONS/app_factory/build_submit.py --help
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
BUILDS_DIR = PROJECT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
LOG_DIR = AUTOMATIONS / "app_factory" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

BUILDS_CSV = LEDGER / "APP_FACTORY_BUILDS.csv"
LOGFILE = LOG_DIR / "build_submit.log"

BUILD_CSV_FIELDS = [
    "timestamp", "name", "slug", "bundle_id", "niche", "pricing_tier",
    "monthly_price", "yearly_price", "output_dir", "status",
    "build_id", "build_url", "submit_id", "error",
]


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Pre-flight Checks
# ---------------------------------------------------------------------------
def check_eas_cli() -> bool:
    """Check if EAS CLI is installed and authenticated."""
    try:
        result = subprocess.run(
            ["eas", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            log(f"EAS CLI version: {result.stdout.strip()}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    log("ERROR: EAS CLI not found. Install with: npm install -g eas-cli")
    return False


def check_expo_login() -> bool:
    """Check if logged into Expo."""
    try:
        result = subprocess.run(
            ["eas", "whoami"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            log(f"Logged in as: {result.stdout.strip()}")
            return True
        else:
            log("WARNING: Not logged into Expo. Run: eas login")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        log("WARNING: Could not check Expo login status")
        return False


def validate_project(app_dir: Path) -> dict[str, Any]:
    """Validate the app project is ready for build."""
    issues: list[str] = []
    warnings: list[str] = []
    info: dict[str, Any] = {"valid": False, "issues": issues, "warnings": warnings}

    app_dir = Path(app_dir).resolve()
    if not app_dir.exists():
        issues.append(f"Directory not found: {app_dir}")
        return info

    # Check app.json
    app_json_path = app_dir / "app.json"
    if not app_json_path.exists():
        issues.append("Missing app.json")
    else:
        try:
            with open(app_json_path) as f:
                app_json = json.load(f)
            expo = app_json.get("expo", {})
            info["name"] = expo.get("name", "")
            info["slug"] = expo.get("slug", "")
            info["bundle_id"] = expo.get("ios", {}).get("bundleIdentifier", "")

            if not info["bundle_id"]:
                issues.append("Missing ios.bundleIdentifier in app.json")
            if not info["slug"]:
                issues.append("Missing slug in app.json")

            # Check EAS project ID
            eas_project = expo.get("extra", {}).get("eas", {}).get("projectId", "")
            if not eas_project:
                warnings.append("Missing eas.projectId -- will be created on first build")

            # Check encryption flag
            infoplist = expo.get("ios", {}).get("infoPlist", {})
            if "ITSAppUsesNonExemptEncryption" not in infoplist:
                warnings.append("Missing ITSAppUsesNonExemptEncryption in infoPlist")

        except json.JSONDecodeError:
            issues.append("Invalid app.json (bad JSON)")

    # Check package.json
    if not (app_dir / "package.json").exists():
        issues.append("Missing package.json")

    # Check node_modules
    if not (app_dir / "node_modules").exists():
        warnings.append("node_modules missing -- run npm install first")

    # Check eas.json
    if not (app_dir / "eas.json").exists():
        warnings.append("Missing eas.json -- will create default")

    # Check for required assets
    assets_dir = app_dir / "assets"
    if not assets_dir.exists():
        warnings.append("Missing assets/ directory")
    else:
        for asset in ["icon.png", "splash-icon.png"]:
            if not (assets_dir / asset).exists():
                warnings.append(f"Missing assets/{asset}")

    info["valid"] = len(issues) == 0
    return info


def ensure_eas_json(app_dir: Path) -> None:
    """Create eas.json if it doesn't exist."""
    eas_json = app_dir / "eas.json"
    if eas_json.exists():
        return

    config = {
        "cli": {
            "version": ">= 12.0.0"
        },
        "build": {
            "development": {
                "developmentClient": True,
                "distribution": "internal"
            },
            "preview": {
                "distribution": "internal"
            },
            "production": {
                "ios": {
                    "autoIncrement": True
                }
            }
        },
        "submit": {
            "production": {
                "ios": {
                    "appleId": os.environ.get("APPLE_ID", ""),
                    "ascAppId": "",
                    "appleTeamId": os.environ.get("APPLE_TEAM_ID", "")
                }
            }
        }
    }

    with open(eas_json, "w") as f:
        json.dump(config, f, indent=2)
    log(f"Created eas.json at {eas_json}")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def run_build(
    app_dir: Path,
    platform: str = "ios",
    profile: str = "production",
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run EAS build and return build info."""
    result_info: dict[str, Any] = {
        "success": False,
        "build_id": "",
        "build_url": "",
        "error": "",
    }

    app_dir = Path(app_dir).resolve()

    # Validate
    validation = validate_project(app_dir)
    if not validation["valid"]:
        result_info["error"] = "; ".join(validation["issues"])
        log(f"Build validation failed: {result_info['error']}")
        return result_info

    for w in validation.get("warnings", []):
        log(f"  WARNING: {w}")

    # Ensure eas.json exists
    ensure_eas_json(app_dir)

    if dry_run:
        log(f"DRY RUN: Would build {validation.get('name', '?')} ({platform}/{profile})")
        result_info["success"] = True
        result_info["build_id"] = "dry-run-build-id"
        return result_info

    # Install deps if needed
    if not (app_dir / "node_modules").exists():
        log("Installing dependencies...")
        npm_result = subprocess.run(
            ["npm", "install"],
            cwd=str(app_dir),
            capture_output=True, text=True, timeout=300,
        )
        if npm_result.returncode != 0:
            result_info["error"] = f"npm install failed: {npm_result.stderr[:200]}"
            log(f"ERROR: {result_info['error']}")
            return result_info

    # Run build
    cmd = [
        "eas", "build",
        "--platform", platform,
        "--profile", profile,
        "--non-interactive",
    ]

    log(f"Running: {' '.join(cmd)} in {app_dir}")

    try:
        build_result = subprocess.run(
            cmd,
            cwd=str(app_dir),
            capture_output=True,
            text=True,
            timeout=1800,  # 30 min timeout
        )

        output = build_result.stdout + "\n" + build_result.stderr

        # Extract build ID and URL from output
        build_id_match = re.search(r'Build ID:\s*(\S+)', output)
        if build_id_match:
            result_info["build_id"] = build_id_match.group(1)

        url_match = re.search(r'(https://expo\.dev/accounts/[^\s]+/builds/[^\s]+)', output)
        if url_match:
            result_info["build_url"] = url_match.group(1)

        if build_result.returncode == 0:
            result_info["success"] = True
            log(f"Build started successfully. ID: {result_info['build_id']}")
        else:
            result_info["error"] = _parse_build_error(output)
            log(f"Build failed: {result_info['error'][:200]}")

        # Save full output to log
        build_log = LOG_DIR / f"build_{validation.get('slug', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(build_log, "w") as f:
            f.write(output)

    except subprocess.TimeoutExpired:
        result_info["error"] = "Build timed out after 30 minutes"
        log("ERROR: Build timed out")
    except Exception as e:
        result_info["error"] = str(e)
        log(f"ERROR: Build exception: {e}")

    # Update builds CSV
    _update_builds_csv(validation, result_info, "BUILD")

    return result_info


def _parse_build_error(output: str) -> str:
    """Parse common EAS build errors into actionable messages."""
    if "credentials" in output.lower() or "provisioning" in output.lower():
        return "Missing iOS credentials/provisioning profile. Run: eas credentials"
    if "not found" in output.lower() and "project" in output.lower():
        return "EAS project not configured. Run: eas init"
    if "unauthorized" in output.lower() or "login" in output.lower():
        return "Not logged into Expo. Run: eas login"
    if "billing" in output.lower():
        return "Expo account billing issue. Check expo.dev account"
    if "apple developer" in output.lower():
        return "Apple Developer account issue. Check App Store Connect"

    # Return last meaningful error line
    lines = output.strip().split("\n")
    error_lines = [l for l in lines if "error" in l.lower() or "failed" in l.lower()]
    if error_lines:
        return error_lines[-1][:200]
    return "Unknown build error. Check build log."


# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------
def run_submit(
    app_dir: Path,
    platform: str = "ios",
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run EAS submit to App Store / Play Store."""
    result_info: dict[str, Any] = {
        "success": False,
        "submit_id": "",
        "error": "",
    }

    app_dir = Path(app_dir).resolve()
    validation = validate_project(app_dir)
    if not validation["valid"]:
        result_info["error"] = "; ".join(validation["issues"])
        return result_info

    if dry_run:
        log(f"DRY RUN: Would submit {validation.get('name', '?')} to {platform}")
        result_info["success"] = True
        return result_info

    cmd = [
        "eas", "submit",
        "--platform", platform,
        "--non-interactive",
        "--latest",
    ]

    log(f"Running: {' '.join(cmd)} in {app_dir}")

    try:
        submit_result = subprocess.run(
            cmd,
            cwd=str(app_dir),
            capture_output=True,
            text=True,
            timeout=600,  # 10 min timeout
        )

        output = submit_result.stdout + "\n" + submit_result.stderr

        if submit_result.returncode == 0:
            result_info["success"] = True
            # Try to extract submission ID
            id_match = re.search(r'Submission ID:\s*(\S+)', output)
            if id_match:
                result_info["submit_id"] = id_match.group(1)
            log(f"Submission successful for {validation.get('name', '?')}")
        else:
            result_info["error"] = output[-200:] if output else "Submit failed"
            log(f"Submit failed: {result_info['error'][:200]}")

        # Save log
        submit_log = LOG_DIR / f"submit_{validation.get('slug', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(submit_log, "w") as f:
            f.write(output)

    except subprocess.TimeoutExpired:
        result_info["error"] = "Submit timed out after 10 minutes"
    except Exception as e:
        result_info["error"] = str(e)

    _update_builds_csv(validation, result_info, "SUBMIT")

    return result_info


# ---------------------------------------------------------------------------
# Status Check
# ---------------------------------------------------------------------------
def check_build_status(app_dir: Path) -> dict[str, Any]:
    """Check the latest build status for an app."""
    app_dir = Path(app_dir).resolve()

    try:
        result = subprocess.run(
            ["eas", "build:list", "--platform", "ios", "--limit", "1", "--json"],
            cwd=str(app_dir),
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            builds = json.loads(result.stdout)
            if builds and isinstance(builds, list):
                latest = builds[0]
                return {
                    "status": latest.get("status", "UNKNOWN"),
                    "build_id": latest.get("id", ""),
                    "platform": latest.get("platform", ""),
                    "created_at": latest.get("createdAt", ""),
                    "completed_at": latest.get("completedAt", ""),
                    "artifacts_url": latest.get("artifacts", {}).get("buildUrl", ""),
                }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

    return {"status": "NO_BUILDS"}


# ---------------------------------------------------------------------------
# CSV Tracking
# ---------------------------------------------------------------------------
def _update_builds_csv(validation: dict, result: dict, action: str) -> None:
    """Update the builds CSV with build/submit results."""
    builds_path = safe_path(BUILDS_CSV)

    # Read existing rows
    rows: list[dict] = []
    if builds_path.exists():
        try:
            with open(builds_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception:
            pass

    slug = validation.get("slug", "")

    # Find existing row for this app
    found = False
    for row in rows:
        if row.get("slug") == slug:
            if action == "BUILD":
                row["build_id"] = result.get("build_id", "")
                row["build_url"] = result.get("build_url", "")
                row["status"] = "BUILDING" if result.get("success") else "BUILD_FAILED"
                row["error"] = result.get("error", "")
            elif action == "SUBMIT":
                row["submit_id"] = result.get("submit_id", "")
                row["status"] = "SUBMITTED" if result.get("success") else "SUBMIT_FAILED"
                row["error"] = result.get("error", "")
            row["timestamp"] = datetime.now().isoformat()
            found = True
            break

    if not found:
        new_row = {field: "" for field in BUILD_CSV_FIELDS}
        new_row["timestamp"] = datetime.now().isoformat()
        new_row["name"] = validation.get("name", "")
        new_row["slug"] = slug
        new_row["bundle_id"] = validation.get("bundle_id", "")
        if action == "BUILD":
            new_row["build_id"] = result.get("build_id", "")
            new_row["build_url"] = result.get("build_url", "")
            new_row["status"] = "BUILDING" if result.get("success") else "BUILD_FAILED"
        elif action == "SUBMIT":
            new_row["submit_id"] = result.get("submit_id", "")
            new_row["status"] = "SUBMITTED" if result.get("success") else "SUBMIT_FAILED"
        new_row["error"] = result.get("error", "")
        rows.append(new_row)

    # Write back
    with open(builds_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=BUILD_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Factory Build & Submit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/app_factory/build_submit.py --build builds/fitstreak
  python3 AUTOMATIONS/app_factory/build_submit.py --submit builds/fitstreak
  python3 AUTOMATIONS/app_factory/build_submit.py --build-and-submit builds/fitstreak
  python3 AUTOMATIONS/app_factory/build_submit.py --status builds/fitstreak
  python3 AUTOMATIONS/app_factory/build_submit.py --validate builds/fitstreak
        """,
    )
    parser.add_argument("--build", metavar="APP_DIR", help="Run EAS build for app directory")
    parser.add_argument("--submit", metavar="APP_DIR", help="Run EAS submit for app directory")
    parser.add_argument("--build-and-submit", metavar="APP_DIR", help="Build then submit")
    parser.add_argument("--status", metavar="APP_DIR", help="Check build status")
    parser.add_argument("--validate", metavar="APP_DIR", help="Validate project without building")
    parser.add_argument("--batch", action="store_true", help="Build all GENERATED apps from CSV")
    parser.add_argument("--top", type=int, default=3, help="Max apps to build in batch mode")
    parser.add_argument("--platform", default="ios", choices=["ios", "android", "all"])
    parser.add_argument("--dry-run", action="store_true", help="Don't actually build/submit")

    args = parser.parse_args()

    if not any([args.build, args.submit, args.build_and_submit, args.status, args.validate, args.batch]):
        parser.print_help()
        return

    # Pre-flight
    if not args.dry_run and not args.validate:
        if not check_eas_cli():
            return
        check_expo_login()

    if args.validate:
        app_dir = _resolve_app_dir(args.validate)
        info = validate_project(app_dir)
        print(json.dumps(info, indent=2))
        return

    if args.status:
        app_dir = _resolve_app_dir(args.status)
        status = check_build_status(app_dir)
        print(json.dumps(status, indent=2))
        return

    if args.build:
        app_dir = _resolve_app_dir(args.build)
        result = run_build(app_dir, args.platform, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))

    elif args.submit:
        app_dir = _resolve_app_dir(args.submit)
        result = run_submit(app_dir, args.platform, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))

    elif args.build_and_submit:
        app_dir = _resolve_app_dir(args.build_and_submit)
        log(f"Build & Submit pipeline for {app_dir}")

        build_result = run_build(app_dir, args.platform, dry_run=args.dry_run)
        if not build_result["success"]:
            log("Build failed, skipping submit")
            print(json.dumps(build_result, indent=2))
            return

        if not args.dry_run:
            log("Waiting for build to complete before submitting...")
            log("NOTE: EAS builds are async. Monitor with --status and submit when done.")
            # In real usage, you'd poll build status then submit.
            # For now, submit immediately (EAS submit --latest waits for latest build)

        submit_result = run_submit(app_dir, args.platform, dry_run=args.dry_run)
        print(json.dumps({"build": build_result, "submit": submit_result}, indent=2))

    elif args.batch:
        if not BUILDS_CSV.exists():
            log("No builds CSV found. Generate apps first.")
            return

        with open(BUILDS_CSV, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r.get("status") == "GENERATED"]

        if not rows:
            log("No GENERATED apps found in builds CSV")
            return

        log(f"Batch building {min(len(rows), args.top)} apps")
        for row in rows[:args.top]:
            app_dir = Path(row.get("output_dir", ""))
            if app_dir.exists():
                log(f"\n{'='*40}")
                log(f"Building: {row.get('name', '?')}")
                result = run_build(app_dir, args.platform, dry_run=args.dry_run)
                if result["success"]:
                    log(f"Build started for {row.get('name', '?')}")
                else:
                    log(f"Build failed for {row.get('name', '?')}: {result.get('error', '')}")


def _resolve_app_dir(path: str) -> Path:
    """Resolve app directory path (relative to builds dir or absolute)."""
    p = Path(path)
    if p.is_absolute():
        return p
    # Try relative to builds dir
    candidate = BUILDS_DIR / path
    if candidate.exists():
        return candidate
    # Try relative to project root
    candidate = PROJECT / path
    if candidate.exists():
        return candidate
    return p


if __name__ == "__main__":
    main()
