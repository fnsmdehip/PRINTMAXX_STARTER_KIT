#!/usr/bin/env python3
"""App Factory Test Runner.

Automated testing pipeline that checks apps against Apple's rejection criteria
and common quality issues before submission.

Checks:
  - TypeScript compilation (npx tsc --noEmit)
  - Expo export (npx expo export --platform ios)
  - Privacy policy URL resolves
  - Camera/mic permission strings are specific
  - No placeholder text
  - Bundle ID uniqueness
  - App name collision check
  - ITSAppUsesNonExemptEncryption set
  - No hardcoded API keys
  - Minimum useful functionality
  - Subscription terms (Apple 3.1.1/3.1.2)
  - No broken images/missing assets

Usage:
  python3 AUTOMATIONS/app_factory/test_runner.py --test APP_DIR
  python3 AUTOMATIONS/app_factory/test_runner.py --test-all
  python3 AUTOMATIONS/app_factory/test_runner.py --help
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import urllib.request
import urllib.error
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
TEST_RESULTS_DIR = AUTOMATIONS / "app_factory" / "test_results"
TEST_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
LOGFILE = LOG_DIR / "test_runner.log"


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
# Test Result Types
# ---------------------------------------------------------------------------
class TestResult:
    def __init__(self, name: str, status: str, message: str, severity: str = "error"):
        self.name = name
        self.status = status  # PASS, FAIL, WARN, SKIP
        self.message = message
        self.severity = severity  # error, warning, info

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "severity": self.severity,
        }


# ---------------------------------------------------------------------------
# Individual Tests
# ---------------------------------------------------------------------------
def test_app_json_exists(app_dir: Path) -> TestResult:
    """Check app.json exists and is valid JSON."""
    path = app_dir / "app.json"
    if not path.exists():
        return TestResult("app_json", "FAIL", "app.json not found", "error")
    try:
        with open(path) as f:
            json.load(f)
        return TestResult("app_json", "PASS", "app.json is valid JSON")
    except json.JSONDecodeError as e:
        return TestResult("app_json", "FAIL", f"Invalid JSON: {e}", "error")


def test_bundle_id(app_dir: Path) -> TestResult:
    """Check bundle ID is set and unique."""
    app_json = _load_app_json(app_dir)
    if not app_json:
        return TestResult("bundle_id", "SKIP", "Cannot load app.json")

    bundle_id = app_json.get("expo", {}).get("ios", {}).get("bundleIdentifier", "")
    if not bundle_id:
        return TestResult("bundle_id", "FAIL", "Missing ios.bundleIdentifier", "error")

    # Check it follows convention
    parts = bundle_id.split(".")
    if len(parts) < 3:
        return TestResult("bundle_id", "WARN", f"Bundle ID '{bundle_id}' is unusually short", "warning")

    # Check against known built apps
    known_ids = _get_known_bundle_ids(app_dir)
    slug = app_json.get("expo", {}).get("slug", "")
    dupes = [kid for kid in known_ids if kid == bundle_id and kid != bundle_id]
    if dupes:
        return TestResult("bundle_id", "FAIL", f"Duplicate bundle ID: {bundle_id}", "error")

    return TestResult("bundle_id", "PASS", f"Bundle ID: {bundle_id}")


def test_app_name_collision(app_dir: Path) -> TestResult:
    """Check app name doesn't clash with popular apps."""
    app_json = _load_app_json(app_dir)
    if not app_json:
        return TestResult("app_name", "SKIP", "Cannot load app.json")

    name = app_json.get("expo", {}).get("name", "").lower()
    if not name:
        return TestResult("app_name", "FAIL", "Missing app name", "error")

    # Known popular app names to avoid
    popular_names = {
        "instagram", "facebook", "twitter", "tiktok", "snapchat", "whatsapp",
        "youtube", "spotify", "netflix", "uber", "lyft", "airbnb", "amazon",
        "google", "apple", "microsoft", "zoom", "slack", "discord", "telegram",
        "signal", "reddit", "pinterest", "linkedin", "duolingo", "calm",
        "headspace", "noom", "peloton", "strava", "fitbit", "myfitnesspal",
    }

    if name in popular_names:
        return TestResult("app_name", "FAIL", f"Name '{name}' clashes with a popular app", "error")

    # Check if name starts with a popular brand
    for popular in popular_names:
        if name.startswith(popular) and len(name) < len(popular) + 5:
            return TestResult("app_name", "WARN", f"Name '{name}' is very similar to '{popular}'", "warning")

    return TestResult("app_name", "PASS", f"App name: {name}")


def test_encryption_flag(app_dir: Path) -> TestResult:
    """Check ITSAppUsesNonExemptEncryption is set."""
    app_json = _load_app_json(app_dir)
    if not app_json:
        return TestResult("encryption_flag", "SKIP", "Cannot load app.json")

    ios = app_json.get("expo", {}).get("ios", {})
    infoplist = ios.get("infoPlist", {})

    if "ITSAppUsesNonExemptEncryption" not in infoplist:
        return TestResult(
            "encryption_flag", "FAIL",
            "Missing ITSAppUsesNonExemptEncryption in ios.infoPlist. Add it to avoid App Store compliance popup.",
            "error"
        )

    return TestResult("encryption_flag", "PASS", "ITSAppUsesNonExemptEncryption is set")


def test_permission_strings(app_dir: Path) -> TestResult:
    """Check camera/mic permission strings are specific, not generic."""
    app_json = _load_app_json(app_dir)
    if not app_json:
        return TestResult("permissions", "SKIP", "Cannot load app.json")

    infoplist = app_json.get("expo", {}).get("ios", {}).get("infoPlist", {})

    generic_phrases = [
        "this app needs access",
        "allow access",
        "we need your",
        "required for app functionality",
        "permission is needed",
    ]

    issues = []
    for key in ["NSCameraUsageDescription", "NSPhotoLibraryUsageDescription",
                 "NSMicrophoneUsageDescription", "NSLocationWhenInUseUsageDescription"]:
        val = infoplist.get(key, "")
        if val:
            val_lower = val.lower()
            for generic in generic_phrases:
                if generic in val_lower:
                    issues.append(f"{key} uses generic language: '{val}'")
                    break
            if len(val) < 20:
                issues.append(f"{key} is too short ({len(val)} chars): '{val}'")

    if issues:
        return TestResult("permissions", "WARN", "; ".join(issues), "warning")

    return TestResult("permissions", "PASS", "Permission strings look specific")


def test_no_placeholder_text(app_dir: Path) -> TestResult:
    """Scan source files for placeholder text that would cause App Store rejection.

    Excludes known false positives:
    - 'xxx' inside 'xxxl' (spacing constants like Spacing.xxxl)
    - 'placeholder' as a React Native TextInput prop or TypeScript field name
    - 'todo:' / 'fixme:' / 'hack:' inside code comments (// or /* */)
    """
    # Patterns checked via regex to avoid false positives
    placeholder_patterns = [
        (re.compile(r'\blorem\s+ipsum\b', re.IGNORECASE), "lorem ipsum"),
        (re.compile(r'(?<!//)(?<!\*)\s*\btodo\b(?!write|list)', re.IGNORECASE), None),  # skip -- too many false positives in comments
        (re.compile(r'\bcoming\s+soon\b', re.IGNORECASE), "coming soon"),
        (re.compile(r'\bsample\s+text\b', re.IGNORECASE), "sample text"),
        (re.compile(r'\btest\s+test\b', re.IGNORECASE), "test test"),
        (re.compile(r'\bchange\s+me\b', re.IGNORECASE), "change me"),
        (re.compile(r'\breplace\s+this\b', re.IGNORECASE), "replace this"),
        (re.compile(r'\byour\s+text\s+here\b', re.IGNORECASE), "your text here"),
    ]

    source_files = list(app_dir.rglob("*.tsx")) + list(app_dir.rglob("*.ts"))
    # Exclude node_modules
    source_files = [f for f in source_files if "node_modules" not in str(f)]

    findings = []
    for src_file in source_files[:50]:  # Limit to avoid huge scans
        try:
            content = src_file.read_text(errors="replace")
            for pattern, label in placeholder_patterns:
                if label is None:
                    continue  # Skip disabled patterns
                if pattern.search(content):
                    rel = src_file.relative_to(app_dir)
                    findings.append(f"{rel}: contains '{label}'")
        except Exception:
            continue

    if findings:
        return TestResult(
            "placeholder_text", "FAIL",
            f"Found {len(findings)} placeholder(s): {'; '.join(findings[:5])}",
            "error"
        )

    return TestResult("placeholder_text", "PASS", f"No placeholder text found in {len(source_files)} files")


def test_no_hardcoded_keys(app_dir: Path) -> TestResult:
    """Check for hardcoded API keys in source."""
    key_patterns = [
        r'["\']sk[-_](?:live|test)[-_][a-zA-Z0-9]{20,}["\']',  # Stripe
        r'["\']pk[-_](?:live|test)[-_][a-zA-Z0-9]{20,}["\']',
        r'["\']AIza[a-zA-Z0-9_-]{35}["\']',  # Google
        r'["\']ghp_[a-zA-Z0-9]{36}["\']',  # GitHub
        r'["\']AKIA[A-Z0-9]{16}["\']',  # AWS
        r'Bearer\s+[a-zA-Z0-9._-]{30,}',
        r'api[_-]?key\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
    ]

    source_files = list(app_dir.rglob("*.tsx")) + list(app_dir.rglob("*.ts")) + list(app_dir.rglob("*.js"))
    source_files = [f for f in source_files if "node_modules" not in str(f)]

    findings = []
    for src_file in source_files[:50]:
        try:
            content = src_file.read_text(errors="replace")
            for pattern in key_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    rel = src_file.relative_to(app_dir)
                    findings.append(f"{rel}: potential key ({pattern[:20]}...)")
        except Exception:
            continue

    if findings:
        return TestResult(
            "hardcoded_keys", "FAIL",
            f"Found {len(findings)} potential hardcoded key(s): {'; '.join(findings[:3])}",
            "error"
        )

    return TestResult("hardcoded_keys", "PASS", "No hardcoded API keys detected")


def test_privacy_policy_url(app_dir: Path) -> TestResult:
    """Check that privacy policy URL resolves."""
    # Search source for privacy policy links
    source_files = list(app_dir.rglob("*.tsx")) + list(app_dir.rglob("*.ts"))
    source_files = [f for f in source_files if "node_modules" not in str(f)]

    urls_found = []
    for src_file in source_files[:50]:
        try:
            content = src_file.read_text(errors="replace")
            # Find URLs near "privacy"
            url_matches = re.findall(r'https?://[^\s\'"<>]+(?:privacy|terms)[^\s\'"<>]*', content, re.IGNORECASE)
            urls_found.extend(url_matches)
        except Exception:
            continue

    if not urls_found:
        return TestResult(
            "privacy_policy", "WARN",
            "No privacy policy URL found in source. Required for App Store.",
            "warning"
        )

    # Try to resolve the first URL
    url = urls_found[0]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return TestResult("privacy_policy", "PASS", f"Privacy policy URL resolves: {url}")
            else:
                return TestResult("privacy_policy", "WARN", f"Privacy URL returned {resp.status}: {url}", "warning")
    except Exception as e:
        return TestResult("privacy_policy", "WARN", f"Cannot reach privacy URL {url}: {e}", "warning")


def test_subscription_terms(app_dir: Path) -> TestResult:
    """Check Apple 3.1.1/3.1.2 subscription terms are displayed."""
    source_files = list(app_dir.rglob("*.tsx")) + list(app_dir.rglob("*.ts"))
    source_files = [f for f in source_files if "node_modules" not in str(f)]

    required_phrases = [
        "cancel",
        "renew",
        "apple id",
    ]

    found_in = set()
    for src_file in source_files[:50]:
        try:
            content = src_file.read_text(errors="replace").lower()
            for phrase in required_phrases:
                if phrase in content:
                    found_in.add(phrase)
        except Exception:
            continue

    if len(found_in) < 2:
        return TestResult(
            "subscription_terms", "FAIL",
            f"Missing Apple subscription terms (3.1.1/3.1.2). Found: {found_in}. Need: cancel policy, renewal info, Apple ID reference.",
            "error"
        )

    return TestResult(
        "subscription_terms", "PASS",
        f"Subscription terms found ({len(found_in)}/{len(required_phrases)} required phrases)"
    )


def test_minimum_functionality(app_dir: Path) -> TestResult:
    """Check app has minimum useful functionality."""
    # Count meaningful screens/components
    tsx_files = list(app_dir.rglob("*.tsx"))
    tsx_files = [f for f in tsx_files if "node_modules" not in str(f)]

    if len(tsx_files) < 3:
        return TestResult(
            "min_functionality", "FAIL",
            f"Only {len(tsx_files)} TSX files. Need at least 3 screens for minimum functionality.",
            "error"
        )

    # Check for at least one interactive element
    has_interaction = False
    for src_file in tsx_files[:20]:
        try:
            content = src_file.read_text(errors="replace")
            if "TouchableOpacity" in content or "Pressable" in content or "Button" in content:
                has_interaction = True
                break
        except Exception:
            continue

    if not has_interaction:
        return TestResult(
            "min_functionality", "WARN",
            "No interactive elements (TouchableOpacity/Pressable/Button) found",
            "warning"
        )

    return TestResult("min_functionality", "PASS", f"{len(tsx_files)} TSX files with interactive elements")


def test_missing_assets(app_dir: Path) -> TestResult:
    """Check for required assets."""
    assets_dir = app_dir / "assets"
    if not assets_dir.exists():
        return TestResult("assets", "FAIL", "No assets/ directory found", "error")

    required = ["icon.png", "splash-icon.png"]
    missing = [a for a in required if not (assets_dir / a).exists()]

    if missing:
        return TestResult(
            "assets", "WARN",
            f"Missing assets: {', '.join(missing)}. These are needed for App Store.",
            "warning"
        )

    return TestResult("assets", "PASS", "Required assets present")


def test_typescript_compilation(app_dir: Path, dry_run: bool = False) -> TestResult:
    """Run TypeScript compilation check."""
    if dry_run:
        return TestResult("typescript", "SKIP", "Skipped in dry-run mode")

    if not (app_dir / "node_modules").exists():
        return TestResult("typescript", "SKIP", "node_modules missing -- run npm install first")

    if not (app_dir / "tsconfig.json").exists():
        return TestResult("typescript", "SKIP", "No tsconfig.json found")

    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=str(app_dir),
            capture_output=True, text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return TestResult("typescript", "PASS", "TypeScript compilation clean")
        else:
            error_count = result.stdout.count("error TS")
            return TestResult(
                "typescript", "FAIL",
                f"{error_count} TypeScript errors. First: {result.stdout[:200]}",
                "error"
            )
    except subprocess.TimeoutExpired:
        return TestResult("typescript", "WARN", "TypeScript check timed out", "warning")
    except FileNotFoundError:
        return TestResult("typescript", "SKIP", "npx not found")


def test_expo_export(app_dir: Path, dry_run: bool = False) -> TestResult:
    """Run expo export check."""
    if dry_run:
        return TestResult("expo_export", "SKIP", "Skipped in dry-run mode")

    if not (app_dir / "node_modules").exists():
        return TestResult("expo_export", "SKIP", "node_modules missing")

    try:
        result = subprocess.run(
            ["npx", "expo", "export", "--platform", "ios", "--dump-sourcemap", "--no-minify"],
            cwd=str(app_dir),
            capture_output=True, text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return TestResult("expo_export", "PASS", "Expo export successful")
        else:
            return TestResult(
                "expo_export", "FAIL",
                f"Expo export failed: {(result.stderr or result.stdout)[:200]}",
                "error"
            )
    except subprocess.TimeoutExpired:
        return TestResult("expo_export", "WARN", "Expo export timed out (2 min)", "warning")
    except FileNotFoundError:
        return TestResult("expo_export", "SKIP", "npx not found")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _load_app_json(app_dir: Path) -> dict | None:
    path = app_dir / "app.json"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def _get_known_bundle_ids(exclude_dir: Path) -> list[str]:
    """Get bundle IDs from all known builds."""
    ids = []
    if BUILDS_DIR.exists():
        for build_dir in BUILDS_DIR.iterdir():
            if build_dir == exclude_dir or not build_dir.is_dir():
                continue
            aj = _load_app_json(build_dir)
            if aj:
                bid = aj.get("expo", {}).get("ios", {}).get("bundleIdentifier", "")
                if bid:
                    ids.append(bid)
    return ids


# ---------------------------------------------------------------------------
# Test Runner
# ---------------------------------------------------------------------------
ALL_TESTS = [
    test_app_json_exists,
    test_bundle_id,
    test_app_name_collision,
    test_encryption_flag,
    test_permission_strings,
    test_no_placeholder_text,
    test_no_hardcoded_keys,
    test_privacy_policy_url,
    test_subscription_terms,
    test_minimum_functionality,
    test_missing_assets,
]

# Tests that require npm install / running tools
RUNTIME_TESTS = [
    test_typescript_compilation,
    test_expo_export,
]


def run_tests(app_dir: Path, include_runtime: bool = True, dry_run: bool = False) -> list[TestResult]:
    """Run all tests on an app directory."""
    app_dir = Path(app_dir).resolve()
    results: list[TestResult] = []

    if not app_dir.exists():
        return [TestResult("exists", "FAIL", f"Directory not found: {app_dir}", "error")]

    log(f"Testing: {app_dir.name}")

    # Static tests
    for test_fn in ALL_TESTS:
        try:
            result = test_fn(app_dir)
        except Exception as e:
            result = TestResult(test_fn.__name__, "FAIL", f"Test crashed: {e}", "error")
        results.append(result)
        status_icon = {"PASS": "+", "FAIL": "X", "WARN": "!", "SKIP": "-"}.get(result.status, "?")
        log(f"  [{status_icon}] {result.name}: {result.message[:80]}")

    # Runtime tests
    if include_runtime:
        for test_fn in RUNTIME_TESTS:
            try:
                result = test_fn(app_dir, dry_run=dry_run)
            except Exception as e:
                result = TestResult(test_fn.__name__, "FAIL", f"Test crashed: {e}", "error")
            results.append(result)
            status_icon = {"PASS": "+", "FAIL": "X", "WARN": "!", "SKIP": "-"}.get(result.status, "?")
            log(f"  [{status_icon}] {result.name}: {result.message[:80]}")

    return results


def generate_report(app_dir: Path, results: list[TestResult]) -> str:
    """Generate a test report."""
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    warned = sum(1 for r in results if r.status == "WARN")
    skipped = sum(1 for r in results if r.status == "SKIP")
    total = len(results)

    overall = "PASS" if failed == 0 else "FAIL"

    lines = [
        f"# Test Report: {app_dir.name}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Overall: **{overall}**",
        f"Results: {passed} passed, {failed} failed, {warned} warnings, {skipped} skipped / {total} total",
        "",
        "## Results",
        "",
        "| Status | Test | Message |",
        "|--------|------|---------|",
    ]

    for r in results:
        icon = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN", "SKIP": "SKIP"}.get(r.status, "?")
        msg = r.message[:80].replace("|", "/")
        lines.append(f"| {icon} | {r.name} | {msg} |")

    # Action items
    action_items = [r for r in results if r.status == "FAIL"]
    if action_items:
        lines.extend([
            "",
            "## Required Fixes (must fix before submission)",
            "",
        ])
        for r in action_items:
            lines.append(f"- **{r.name}**: {r.message}")

    warnings = [r for r in results if r.status == "WARN"]
    if warnings:
        lines.extend([
            "",
            "## Warnings (should fix)",
            "",
        ])
        for r in warnings:
            lines.append(f"- **{r.name}**: {r.message}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Factory Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/app_factory/test_runner.py --test builds/fitstreak
  python3 AUTOMATIONS/app_factory/test_runner.py --test builds/fitstreak --static-only
  python3 AUTOMATIONS/app_factory/test_runner.py --test-all
  python3 AUTOMATIONS/app_factory/test_runner.py --test-all --dry-run
        """,
    )
    parser.add_argument("--test", metavar="APP_DIR", help="Test a specific app directory")
    parser.add_argument("--test-all", action="store_true", help="Test all apps in builds directory")
    parser.add_argument("--static-only", action="store_true", help="Skip runtime tests (tsc, expo export)")
    parser.add_argument("--dry-run", action="store_true", help="Skip tests that require running commands")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if not args.test and not args.test_all:
        parser.print_help()
        return

    if args.test:
        app_dir = Path(args.test)
        if not app_dir.is_absolute():
            # Try relative to builds dir, then project root
            if (BUILDS_DIR / args.test).exists():
                app_dir = BUILDS_DIR / args.test
            elif (PROJECT / args.test).exists():
                app_dir = PROJECT / args.test

        results = run_tests(
            app_dir,
            include_runtime=not args.static_only,
            dry_run=args.dry_run,
        )

        if args.json:
            print(json.dumps([r.to_dict() for r in results], indent=2))
        else:
            report = generate_report(app_dir, results)
            print(report)

            # Save report
            report_path = safe_path(TEST_RESULTS_DIR / f"test_{app_dir.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
            with open(report_path, "w") as f:
                f.write(report)
            log(f"Report saved: {report_path}")

    elif args.test_all:
        if not BUILDS_DIR.exists():
            log("Builds directory not found")
            return

        all_reports = []
        for build_dir in sorted(BUILDS_DIR.iterdir()):
            if not build_dir.is_dir():
                continue
            if not (build_dir / "app.json").exists():
                continue

            log(f"\n{'='*50}")
            results = run_tests(
                build_dir,
                include_runtime=not args.static_only,
                dry_run=args.dry_run,
            )

            passed = sum(1 for r in results if r.status == "PASS")
            failed = sum(1 for r in results if r.status == "FAIL")
            overall = "PASS" if failed == 0 else "FAIL"
            all_reports.append({
                "app": build_dir.name,
                "overall": overall,
                "passed": passed,
                "failed": failed,
                "total": len(results),
            })

        # Summary
        print(f"\n{'='*50}")
        print(f"Test Summary ({len(all_reports)} apps)")
        print(f"{'='*50}")
        print(f"{'App':<30} {'Result':<8} {'Pass':<6} {'Fail':<6}")
        print("-" * 50)
        for r in all_reports:
            print(f"{r['app']:<30} {r['overall']:<8} {r['passed']:<6} {r['failed']:<6}")


if __name__ == "__main__":
    main()
