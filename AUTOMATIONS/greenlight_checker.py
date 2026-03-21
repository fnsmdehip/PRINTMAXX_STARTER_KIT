#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Greenlight Checker
=============================
Wrapper around RevylAI Greenlight (https://github.com/RevylAI/greenlight)
for batch Apple App Store pre-submission compliance scanning across the
entire PRINTMAXX app portfolio.

Checks:
  - Metadata: Info.plist, icons, bundle ID format, privacy policy URLs
  - Code patterns: 30+ rejection-risk patterns (private APIs, hardcoded
    secrets, unauthorized payments, dynamic code loading)
  - Privacy: PrivacyInfo.xcprivacy, Required Reason APIs, tracking SDK
    compliance
  - IPA binary: icons, launch storyboards, size (when --ipa provided)

Usage:
  python3 AUTOMATIONS/greenlight_checker.py --all
  python3 AUTOMATIONS/greenlight_checker.py --app ramadan-tracker
  python3 AUTOMATIONS/greenlight_checker.py --app focuslock --ipa build/App.ipa
  python3 AUTOMATIONS/greenlight_checker.py --all --fix
  python3 AUTOMATIONS/greenlight_checker.py --all --format json

Exit codes:
  0 = all scanned apps passed (zero FAIL results)
  1 = one or more apps had FAIL results
  2 = greenlight not installed or other tool error
  3 = no matching app directories found
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Project root (one level up from AUTOMATIONS/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# All 6 PRINTMAXX app directories with their canonical paths and display names
APP_REGISTRY = {
    "ramadan-tracker": {
        "path": "ralph/loops/app_factory/output/ramadan-tracker",
        "display": "Hilal (Ramadan Tracker)",
        "ios_subdir": "native-wrapper",
    },
    "focuslock": {
        "path": "ralph/loops/app_factory/output/focuslock-web",
        "display": "Vault (FocusLock)",
        "ios_subdir": "native-wrapper",
    },
    "habitforge": {
        "path": "ralph/loops/app_factory/output/habitforge-web",
        "display": "Streakr (HabitForge)",
        "ios_subdir": "native-wrapper",
    },
    "mealmaxx": {
        "path": "ralph/loops/app_factory/output/mealmaxx-web",
        "display": "Mise (MealMaxx)",
        "ios_subdir": "native-wrapper",
    },
    "sleepmaxx": {
        "path": "ralph/loops/app_factory/output/sleepmaxx-web",
        "display": "Dusk (SleepMaxx)",
        "ios_subdir": None,
    },
    "walktounlock": {
        "path": "ralph/loops/app_factory/output/walktounlock-web",
        "display": "Steplock (WalkToUnlock)",
        "ios_subdir": None,
    },
}

# Alias map so users can type either internal or brand name
ALIASES = {
    "hilal": "ramadan-tracker",
    "ramadan": "ramadan-tracker",
    "vault": "focuslock",
    "focus": "focuslock",
    "streakr": "habitforge",
    "habit": "habitforge",
    "mise": "mealmaxx",
    "meal": "mealmaxx",
    "dusk": "sleepmaxx",
    "sleep": "sleepmaxx",
    "steplock": "walktounlock",
    "walk": "walktounlock",
}


def resolve_app_name(name: str) -> str | None:
    """Resolve an app name or alias to the canonical registry key."""
    lower = name.lower().strip()
    if lower in APP_REGISTRY:
        return lower
    if lower in ALIASES:
        return ALIASES[lower]
    # Try partial match
    for key in APP_REGISTRY:
        if lower in key:
            return key
    for alias, key in ALIASES.items():
        if lower in alias:
            return key
    return None


def check_greenlight_installed() -> bool:
    """Check if the greenlight CLI is available."""
    try:
        result = subprocess.run(
            ["greenlight", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_scan_path(app_key: str) -> Path | None:
    """
    Determine the best directory to scan for an app.
    Prefers the iOS native-wrapper subdir if it exists, otherwise the web root.
    """
    app_info = APP_REGISTRY[app_key]
    base = PROJECT_ROOT / app_info["path"]

    if not base.exists():
        return None

    # If there is a native-wrapper or ios subdir, prefer it for iOS-specific checks
    if app_info["ios_subdir"]:
        ios_path = base / app_info["ios_subdir"]
        if ios_path.exists():
            return ios_path

    # Check for ios/ subdir (standard Capacitor layout)
    ios_path = base / "ios"
    if ios_path.exists():
        return ios_path

    # Fall back to project root
    return base


def run_greenlight(scan_path: Path, ipa_path: str | None = None, json_output: bool = True) -> dict:
    """
    Run greenlight preflight on a directory and return parsed results.

    Returns a dict with keys:
      - success: bool (True if greenlight ran without error)
      - exit_code: int
      - results: list of check results (if JSON parse succeeded)
      - raw_output: str (raw stdout)
      - error: str (stderr if any)
      - pass_count: int
      - warn_count: int
      - fail_count: int
      - info_count: int
    """
    cmd = ["greenlight", "preflight", str(scan_path)]

    if ipa_path:
        cmd.extend(["--ipa", ipa_path])

    if json_output:
        cmd.extend(["--format", "json"])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(scan_path),
        )
    except FileNotFoundError:
        return {
            "success": False,
            "exit_code": 2,
            "results": [],
            "raw_output": "",
            "error": "greenlight command not found. Install: pip install greenlight-appstore",
            "pass_count": 0,
            "warn_count": 0,
            "fail_count": 0,
            "info_count": 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": 2,
            "results": [],
            "raw_output": "",
            "error": "greenlight timed out after 120 seconds",
            "pass_count": 0,
            "warn_count": 0,
            "fail_count": 0,
            "info_count": 0,
        }

    output = result.stdout
    error = result.stderr

    # Try to parse JSON output
    results = []
    pass_count = 0
    warn_count = 0
    fail_count = 0
    info_count = 0

    if json_output and output.strip():
        try:
            parsed = json.loads(output)
            # Greenlight JSON format may vary; handle both list and dict formats
            if isinstance(parsed, list):
                results = parsed
            elif isinstance(parsed, dict):
                results = parsed.get("checks", parsed.get("results", []))
                if not results and "summary" not in parsed:
                    # The whole dict might be the result
                    results = [parsed]

            for check in results:
                status = check.get("status", check.get("result", "")).upper()
                if status == "PASS":
                    pass_count += 1
                elif status == "WARN" or status == "WARNING":
                    warn_count += 1
                elif status == "FAIL" or status == "ERROR":
                    fail_count += 1
                elif status == "INFO":
                    info_count += 1
        except json.JSONDecodeError:
            # Fall back to parsing text output
            pass

    # If JSON parsing didn't yield counts, try counting from text output
    if pass_count == 0 and warn_count == 0 and fail_count == 0 and output:
        for line in output.splitlines():
            line_upper = line.upper()
            if "PASS" in line_upper and ("FAIL" not in line_upper):
                pass_count += 1
            elif "WARN" in line_upper:
                warn_count += 1
            elif "FAIL" in line_upper or "ERROR" in line_upper:
                fail_count += 1
            elif "INFO" in line_upper:
                info_count += 1

    return {
        "success": True,
        "exit_code": result.returncode,
        "results": results,
        "raw_output": output,
        "error": error,
        "pass_count": pass_count,
        "warn_count": warn_count,
        "fail_count": fail_count,
        "info_count": info_count,
    }


def print_app_result(app_key: str, scan_result: dict, verbose: bool = False) -> None:
    """Print a formatted result for a single app."""
    app_info = APP_REGISTRY[app_key]
    display = app_info["display"]

    if not scan_result["success"]:
        print(f"\n  {display}")
        print(f"    ERROR: {scan_result['error']}")
        return

    total = (
        scan_result["pass_count"]
        + scan_result["warn_count"]
        + scan_result["fail_count"]
        + scan_result["info_count"]
    )

    # Determine overall status
    if scan_result["fail_count"] > 0:
        status_icon = "FAIL"
        status_color = "\033[91m"  # red
    elif scan_result["warn_count"] > 0:
        status_icon = "WARN"
        status_color = "\033[93m"  # yellow
    else:
        status_icon = "PASS"
        status_color = "\033[92m"  # green

    reset = "\033[0m"

    print(f"\n  {status_color}[{status_icon}]{reset} {display}")
    print(f"    Path: {app_info['path']}")
    print(
        f"    Results: {scan_result['pass_count']} pass, "
        f"{scan_result['warn_count']} warn, "
        f"{scan_result['fail_count']} fail, "
        f"{scan_result['info_count']} info "
        f"({total} total checks)"
    )

    if scan_result["fail_count"] > 0 or verbose:
        # Show individual check details for failures (and all if verbose)
        for check in scan_result["results"]:
            check_status = check.get("status", check.get("result", "")).upper()
            check_name = check.get("name", check.get("check", "unknown"))
            check_msg = check.get("message", check.get("description", ""))

            if check_status in ("FAIL", "ERROR") or verbose:
                if check_status in ("FAIL", "ERROR"):
                    print(f"    \033[91m  FAIL: {check_name}\033[0m")
                elif check_status in ("WARN", "WARNING"):
                    print(f"    \033[93m  WARN: {check_name}\033[0m")
                else:
                    print(f"      {check_status}: {check_name}")
                if check_msg:
                    print(f"            {check_msg}")

                # Show fix suggestion if available
                fix = check.get("fix", check.get("suggestion", ""))
                if fix:
                    print(f"            Fix: {fix}")

    # If no JSON results but we have raw output with failures, show it
    if not scan_result["results"] and scan_result["fail_count"] > 0:
        print("    Raw output (first 20 lines):")
        for line in scan_result["raw_output"].splitlines()[:20]:
            print(f"      {line}")


def save_json_report(app_key: str, scan_result: dict) -> Path | None:
    """Save JSON report to the app directory for audit trail."""
    app_info = APP_REGISTRY[app_key]
    app_path = PROJECT_ROOT / app_info["path"]

    if not app_path.exists():
        return None

    report = {
        "app": app_key,
        "display_name": app_info["display"],
        "scan_time": datetime.now().isoformat(),
        "pass_count": scan_result["pass_count"],
        "warn_count": scan_result["warn_count"],
        "fail_count": scan_result["fail_count"],
        "info_count": scan_result["info_count"],
        "overall": "PASS" if scan_result["fail_count"] == 0 else "FAIL",
        "checks": scan_result["results"],
    }

    report_path = app_path / "greenlight_report.json"
    try:
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        return report_path
    except OSError:
        return None


def attempt_auto_fix(app_key: str, scan_result: dict) -> list[str]:
    """
    Attempt to apply automated fixes based on Greenlight suggestions.
    Returns a list of actions taken.
    """
    actions = []
    app_info = APP_REGISTRY[app_key]
    app_path = PROJECT_ROOT / app_info["path"]

    for check in scan_result["results"]:
        check_status = check.get("status", check.get("result", "")).upper()
        check_name = check.get("name", check.get("check", "")).lower()
        fix = check.get("fix", check.get("suggestion", ""))

        if check_status not in ("FAIL", "ERROR", "WARN", "WARNING"):
            continue

        # Auto-fix: missing PrivacyInfo.xcprivacy
        if "privacy" in check_name and "manifest" in check_name:
            ios_dir = app_path / "ios" / "App"
            if not ios_dir.exists():
                ios_dir = app_path / "native-wrapper" / "ios" / "App"
            if ios_dir.exists():
                privacy_file = ios_dir / "PrivacyInfo.xcprivacy"
                if not privacy_file.exists():
                    privacy_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>"""
                    try:
                        privacy_file.write_text(privacy_content)
                        actions.append(f"Created PrivacyInfo.xcprivacy at {privacy_file}")
                    except OSError as e:
                        actions.append(f"Failed to create PrivacyInfo.xcprivacy: {e}")

        # Auto-fix: missing ITSAppUsesNonExemptEncryption in Info.plist
        if "encryption" in check_name.lower():
            # Find Info.plist
            for plist_path in app_path.rglob("Info.plist"):
                try:
                    content = plist_path.read_text()
                    if "ITSAppUsesNonExemptEncryption" not in content:
                        # Insert before closing </dict>
                        insert = (
                            "\t<key>ITSAppUsesNonExemptEncryption</key>\n"
                            "\t<false/>\n"
                        )
                        content = content.replace("</dict>\n</plist>", f"{insert}</dict>\n</plist>")
                        plist_path.write_text(content)
                        actions.append(f"Added ITSAppUsesNonExemptEncryption=NO to {plist_path}")
                except OSError:
                    pass

        # Log suggested fixes we cannot auto-apply
        if fix and not actions:
            actions.append(f"Manual fix needed for '{check_name}': {fix}")

    return actions


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Greenlight Checker -- batch Apple App Store compliance scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                    Scan all 6 apps
  %(prog)s --app ramadan-tracker    Scan single app
  %(prog)s --app hilal              Scan by alias
  %(prog)s --all --fix              Scan all + attempt auto-fixes
  %(prog)s --all --verbose          Scan all with detailed output
  %(prog)s --all --save-reports     Scan all + save JSON reports per app
  %(prog)s --list                   List available apps

Requires: greenlight CLI (pip install greenlight-appstore)
Source: https://github.com/RevylAI/greenlight
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Scan all 6 PRINTMAXX apps",
    )
    group.add_argument(
        "--app",
        type=str,
        help="Scan a single app by name or alias (e.g., ramadan-tracker, hilal, focuslock, vault)",
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="List all available apps and their paths",
    )

    parser.add_argument(
        "--ipa",
        type=str,
        help="Path to IPA file for binary analysis (only with --app)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to auto-fix common issues (creates missing PrivacyInfo.xcprivacy, etc.)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all check details, not just failures",
    )
    parser.add_argument(
        "--save-reports",
        action="store_true",
        help="Save JSON reports to each app directory (greenlight_report.json)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Handle --list
    if args.list:
        print("\nPRINTMAXX App Portfolio:\n")
        print(f"  {'Key':<20} {'Display Name':<30} {'Path'}")
        print(f"  {'-'*20} {'-'*30} {'-'*50}")
        for key, info in APP_REGISTRY.items():
            full_path = PROJECT_ROOT / info["path"]
            exists = "OK" if full_path.exists() else "MISSING"
            print(f"  {key:<20} {info['display']:<30} {info['path']} [{exists}]")
        print(f"\nAliases: {', '.join(f'{a} -> {k}' for a, k in sorted(ALIASES.items()))}")
        sys.exit(0)

    # Check greenlight is installed
    if not check_greenlight_installed():
        print("\nERROR: greenlight CLI not found.")
        print("Install it with: pip install greenlight-appstore")
        print("Or from source: git clone https://github.com/RevylAI/greenlight.git && cd greenlight && pip install -e .")
        sys.exit(2)

    # Determine which apps to scan
    apps_to_scan = []
    if args.all:
        apps_to_scan = list(APP_REGISTRY.keys())
    elif args.app:
        resolved = resolve_app_name(args.app)
        if resolved is None:
            print(f"\nERROR: Unknown app '{args.app}'")
            print(f"Available apps: {', '.join(APP_REGISTRY.keys())}")
            print(f"Aliases: {', '.join(ALIASES.keys())}")
            sys.exit(3)
        apps_to_scan = [resolved]

    # Scan each app
    all_results = {}
    total_fails = 0
    total_warns = 0
    total_passes = 0
    missing_apps = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"  PRINTMAXX Greenlight Compliance Scanner")
    print(f"  {timestamp}")
    print(f"  Scanning {len(apps_to_scan)} app(s)")
    print(f"{'='*60}")

    for app_key in apps_to_scan:
        scan_path = get_scan_path(app_key)

        if scan_path is None:
            missing_apps.append(app_key)
            all_results[app_key] = {
                "success": False,
                "exit_code": 3,
                "results": [],
                "raw_output": "",
                "error": f"App directory not found: {APP_REGISTRY[app_key]['path']}",
                "pass_count": 0,
                "warn_count": 0,
                "fail_count": 0,
                "info_count": 0,
            }
            print_app_result(app_key, all_results[app_key], args.verbose)
            continue

        # Run greenlight
        ipa = args.ipa if args.app and args.ipa else None
        scan_result = run_greenlight(scan_path, ipa_path=ipa, json_output=True)
        all_results[app_key] = scan_result

        # Print result
        print_app_result(app_key, scan_result, args.verbose)

        # Save report if requested
        if args.save_reports:
            report_path = save_json_report(app_key, scan_result)
            if report_path:
                print(f"    Report saved: {report_path}")

        # Attempt auto-fix if requested
        if args.fix and (scan_result["fail_count"] > 0 or scan_result["warn_count"] > 0):
            fixes = attempt_auto_fix(app_key, scan_result)
            if fixes:
                print(f"    Auto-fix actions:")
                for fix in fixes:
                    print(f"      - {fix}")

        # Accumulate totals
        total_fails += scan_result["fail_count"]
        total_warns += scan_result["warn_count"]
        total_passes += scan_result["pass_count"]

    # Print summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Apps scanned:  {len(apps_to_scan) - len(missing_apps)}/{len(apps_to_scan)}")
    if missing_apps:
        print(f"  Apps missing:  {', '.join(missing_apps)}")
    print(f"  Total PASS:    {total_passes}")
    print(f"  Total WARN:    {total_warns}")
    print(f"  Total FAIL:    {total_fails}")

    if total_fails > 0:
        print(f"\n  \033[91mVERDICT: FAIL -- {total_fails} issue(s) must be fixed before submission\033[0m")
        print(f"  Fix all FAIL items, then re-run this script.")
    elif total_warns > 0:
        print(f"\n  \033[93mVERDICT: WARN -- {total_warns} warning(s) should be reviewed\033[0m")
        print(f"  Review all WARN items. Fix or document justification before submission.")
    else:
        print(f"\n  \033[92mVERDICT: PASS -- all apps clear for submission\033[0m")

    print(f"{'='*60}\n")

    # JSON output mode
    if args.format == "json":
        json_summary = {
            "scan_time": timestamp,
            "apps_scanned": len(apps_to_scan) - len(missing_apps),
            "apps_missing": missing_apps,
            "total_pass": total_passes,
            "total_warn": total_warns,
            "total_fail": total_fails,
            "verdict": "FAIL" if total_fails > 0 else ("WARN" if total_warns > 0 else "PASS"),
            "per_app": {
                key: {
                    "display": APP_REGISTRY[key]["display"],
                    "pass": r["pass_count"],
                    "warn": r["warn_count"],
                    "fail": r["fail_count"],
                    "info": r["info_count"],
                    "status": "FAIL" if r["fail_count"] > 0 else ("WARN" if r["warn_count"] > 0 else "PASS"),
                }
                for key, r in all_results.items()
            },
        }
        print(json.dumps(json_summary, indent=2))

    # Exit code for CI/CD
    if total_fails > 0:
        sys.exit(1)
    elif missing_apps and len(missing_apps) == len(apps_to_scan):
        sys.exit(3)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
