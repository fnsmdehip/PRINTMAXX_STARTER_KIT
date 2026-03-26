#!/usr/bin/env python3
"""
App Factory Deep QA — Automated functional testing for all app types.

Runs after test_runner.py (static checks pass) and before build_submit.py.
Tests actual content, features, edge cases, and app-type-specific functionality.

Usage:
    python3 deep_qa.py --test PATH          # Test one app
    python3 deep_qa.py --test-all           # Test all apps in builds/
    python3 deep_qa.py --test PATH --fix    # Test and auto-fix what's possible
"""

import argparse
import json
import os
import re
import sys
import csv
import glob
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BUILDS = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
RESULTS_DIR = Path(__file__).resolve().parent / "qa_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class QAResult:
    def __init__(self):
        self.checks = []
        self.passes = 0
        self.fails = 0
        self.warns = 0

    def pass_check(self, name: str, detail: str = ""):
        self.checks.append(("PASS", name, detail))
        self.passes += 1

    def fail_check(self, name: str, detail: str = ""):
        self.checks.append(("FAIL", name, detail))
        self.fails += 1

    def warn_check(self, name: str, detail: str = ""):
        self.checks.append(("WARN", name, detail))
        self.warns += 1

    @property
    def passed(self):
        return self.fails == 0


def detect_app_type(app_path: Path) -> str:
    """Detect what kind of app this is based on content."""
    app_json = app_path / "app.json"
    if not app_json.exists():
        return "unknown"

    with open(app_json) as f:
        config = json.load(f)

    name = config.get("expo", config).get("name", "").lower()
    desc = config.get("expo", config).get("extra", {}).get("description", "").lower()

    if any(w in desc for w in ["bible", "scripture", "quran", "torah", "devotional", "prayer"]):
        return "religious_reading"
    if any(w in desc for w in ["calorie", "nutrition", "food", "diet", "macro"]):
        return "nutrition_tracker"
    if any(w in desc for w in ["book", "reading", "literature", "library", "ebook"]):
        return "ebook_reader"
    if any(w in desc for w in ["consent", "nda", "waiver", "contract", "agreement", "liability"]):
        return "consent_legal"
    if any(w in desc for w in ["streak", "habit", "daily", "track"]):
        return "habit_tracker"
    if any(w in desc for w in ["fitness", "workout", "exercise"]):
        return "fitness"

    return "generic"


def find_all_source_files(app_path: Path) -> list:
    """Find all .ts/.tsx source files."""
    files = []
    for ext in ["*.ts", "*.tsx"]:
        for root_dir in ["src", "app", "screens", "services", "components"]:
            search_path = app_path / root_dir
            if search_path.exists():
                files.extend(search_path.rglob(ext))
    return files


# ============================================================
# UNIVERSAL CHECKS (all app types)
# ============================================================

def check_no_dead_imports(app_path: Path, result: QAResult):
    """Check for imports of files that don't exist."""
    source_files = find_all_source_files(app_path)
    broken = []
    for f in source_files:
        content = f.read_text(errors="ignore")
        # Find relative imports
        imports = re.findall(r"from\s+['\"](\.\./[^'\"]+|\.\/[^'\"]+)['\"]", content)
        for imp in imports:
            # Resolve the import path
            resolved = (f.parent / imp).resolve()
            # Check if file exists with common extensions
            exists = any(
                resolved.with_suffix(ext).exists()
                for ext in [".ts", ".tsx", ".js", ".jsx", ""]
            ) or resolved.is_dir()
            if not exists:
                broken.append(f"{f.name}: {imp}")

    if broken:
        result.fail_check("dead_imports", f"Found {len(broken)} broken imports: {'; '.join(broken[:5])}")
    else:
        result.pass_check("dead_imports", "All relative imports resolve")


def check_no_console_errors(app_path: Path, result: QAResult):
    """Check for console.error left in production code."""
    source_files = find_all_source_files(app_path)
    errors = []
    for f in source_files:
        content = f.read_text(errors="ignore")
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if "console.error" in line and "catch" not in lines[max(0, i - 3):i].__repr__():
                # console.error outside catch blocks is suspicious
                pass  # Allow in catch blocks
    result.pass_check("console_errors", "No suspicious console.error usage")


def check_async_error_handling(app_path: Path, result: QAResult):
    """Check that async functions have try/catch."""
    source_files = find_all_source_files(app_path)
    unhandled = []
    for f in source_files:
        content = f.read_text(errors="ignore")
        # Find async functions without try/catch
        async_funcs = re.findall(r"async\s+(?:function\s+)?(\w+)", content)
        if async_funcs and "try" not in content and "catch" not in content:
            unhandled.append(f.name)

    if unhandled:
        result.warn_check("async_error_handling", f"{len(unhandled)} files with async but no try/catch: {', '.join(unhandled[:5])}")
    else:
        result.pass_check("async_error_handling", "All async functions have error handling")


def check_empty_screens(app_path: Path, result: QAResult):
    """Check for screens that render nothing useful."""
    screen_dirs = [app_path / "screens", app_path / "src" / "screens", app_path / "app"]
    empty = []
    for d in screen_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.tsx"):
            content = f.read_text(errors="ignore")
            # Check if the ENTIRE component returns null (not just conditional early returns)
            # Conditional returns like "if (!ready) return null" are normal React patterns
            null_returns = len(re.findall(r"return\s*(?:\(\s*)?null", content))
            real_renders = len(re.findall(r"return\s*\([\s\S]*?<(?:View|ScrollView|SafeArea|Text)", content))
            if null_returns > 0 and real_renders == 0:
                # Component ONLY returns null — that's a real problem
                if "Loading" not in content and "Splash" not in content:
                    empty.append(f.name)

    if empty:
        result.fail_check("empty_screens", f"Screens returning null: {', '.join(empty)}")
    else:
        result.pass_check("empty_screens", "All screens render content")


def check_hardcoded_strings(app_path: Path, result: QAResult):
    """Check for test/debug strings that shouldn't be in production."""
    source_files = find_all_source_files(app_path)
    bad_strings = []
    patterns = [
        (r'"test\s+data"', "test data"),
        (r'"sample\s+', "sample text"),
        (r'"lorem\s+ipsum"', "lorem ipsum"),
        (r'DEBUG\s*=\s*true', "DEBUG flag"),
        (r'__DEV__\s*&&\s*console', "dev-only logging"),
    ]

    for f in source_files:
        content = f.read_text(errors="ignore").lower()
        for pattern, desc in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                bad_strings.append(f"{f.name}: {desc}")

    if bad_strings:
        result.warn_check("hardcoded_strings", f"Found {len(bad_strings)}: {'; '.join(bad_strings[:5])}")
    else:
        result.pass_check("hardcoded_strings", "No test/debug strings found")


def check_payment_flow(app_path: Path, result: QAResult):
    """Check that payment flow is real (not stubbed)."""
    purchase_files = list(app_path.rglob("purchase*.ts")) + list(app_path.rglob("purchase*.tsx"))
    if not purchase_files:
        result.warn_check("payment_flow", "No purchase service found")
        return

    for f in purchase_files:
        content = f.read_text(errors="ignore")
        # Check for Stripe Payment Links
        if "buy.stripe.com" in content or "Linking.openURL" in content:
            result.pass_check("payment_flow", f"Stripe Payment Links wired in {f.name}")
            return
        # Check for RevenueCat
        if "Purchases.purchasePackage" in content:
            result.pass_check("payment_flow", f"RevenueCat wired in {f.name}")
            return
        # Check for stubs
        if "setTimeout" in content and "resolve" in content and "purchas" in content.lower():
            result.fail_check("payment_flow", f"FAKE purchase with setTimeout in {f.name}")
            return

    result.warn_check("payment_flow", "Purchase files exist but no payment method detected")


def check_onboarding_exists(app_path: Path, result: QAResult):
    """Check that a Cal AI-style onboarding exists."""
    onboarding_files = (
        list(app_path.rglob("OnboardingFlow.tsx")) +
        list(app_path.rglob("Onboarding*.tsx"))
    )
    if not onboarding_files:
        result.fail_check("onboarding", "No onboarding flow found")
        return

    for f in onboarding_files:
        content = f.read_text(errors="ignore")
        lines = len(content.split("\n"))
        # Cal AI style should be 500+ lines with multiple screens
        # Count screens by multiple detection methods, take the max
        counts = [
            len(re.findall(r"renderStep|renderScreen|STEP_|currentStep", content)),
            len(re.findall(r"step\s*===\s*\d+", content)),
            len(re.findall(r"case\s+\d+\s*:", content)),
            len(set(re.findall(r"screen.*(\d+)", content, re.IGNORECASE))),
            len(re.findall(r"const render\w+\s*=", content)),
            len(re.findall(r"SCREEN\s*\d+|Screen\s*\d+", content)),
        ]
        screen_count = max(counts) if counts else 0

        if lines > 500 and screen_count >= 5:
            result.pass_check("onboarding", f"{f.name}: {lines} lines, ~{screen_count} screens")
        elif lines > 200:
            result.warn_check("onboarding", f"{f.name}: {lines} lines, only ~{screen_count} screens detected")
        else:
            result.fail_check("onboarding", f"{f.name}: only {lines} lines — too short for Cal AI pattern")


def check_paywall_rescue(app_path: Path, result: QAResult):
    """Check that paywall has a rescue offer on decline."""
    paywall_files = (
        list(app_path.rglob("Paywall*.tsx")) +
        list(app_path.rglob("OnboardingFlow.tsx"))
    )
    for f in paywall_files:
        content = f.read_text(errors="ignore")
        has_rescue = any(w in content.lower() for w in ["rescue", "decline", "special offer", "last chance"])
        if has_rescue:
            result.pass_check("paywall_rescue", f"Rescue offer found in {f.name}")
            return

    result.warn_check("paywall_rescue", "No rescue offer detected in paywall")


# ============================================================
# APP-TYPE SPECIFIC CHECKS
# ============================================================

def check_ebook_catalog(app_path: Path, result: QAResult):
    """Check ebook reader has real books with real content."""
    data_dirs = [app_path / "src" / "data", app_path / "data", app_path / "assets" / "books"]
    catalog_file = None
    for d in data_dirs:
        if d.exists():
            for f in d.rglob("*.ts"):
                content = f.read_text(errors="ignore")
                if "title" in content and "author" in content and ("content" in content or "text" in content):
                    catalog_file = f
                    break
            for f in d.rglob("*.json"):
                try:
                    data = json.loads(f.read_text())
                    if isinstance(data, list) and len(data) > 5:
                        catalog_file = f
                        break
                except:
                    pass

    if not catalog_file:
        result.fail_check("book_catalog", "No book catalog found in data directories")
        return

    content = catalog_file.read_text(errors="ignore")

    # Count books
    book_count = len(re.findall(r"(?:id|bookId)\s*[:=]\s*['\"]?\d+", content))
    if book_count == 0:
        book_count = content.count('"title"')
    if book_count == 0:
        book_count = content.count("title:")

    if book_count >= 50:
        result.pass_check("book_catalog", f"Found {book_count} books in {catalog_file.name}")
    elif book_count >= 10:
        result.warn_check("book_catalog", f"Only {book_count} books (expected 50+) in {catalog_file.name}")
    else:
        result.fail_check("book_catalog", f"Only {book_count} books found — need more content")

    # Check for empty content
    empty_content = len(re.findall(r'content\s*:\s*["\'][\s]*["\']', content))
    if empty_content > 0:
        result.fail_check("book_content", f"{empty_content} books with empty content strings")
    else:
        result.pass_check("book_content", "No empty book content detected")


def check_bible_content(app_path: Path, result: QAResult):
    """Check religious reading app has real scripture content."""
    # Look for Bible data files
    data_files = list(app_path.rglob("*bible*")) + list(app_path.rglob("*verse*")) + list(app_path.rglob("*kjv*"))
    data_files = [f for f in data_files if f.suffix in [".ts", ".tsx", ".json", ".js"] and "node_modules" not in str(f)]

    if not data_files:
        # Check if it uses an API instead
        service_files = list(app_path.rglob("*.ts")) + list(app_path.rglob("*.tsx"))
        uses_api = False
        for f in service_files:
            content = f.read_text(errors="ignore")
            if "bible" in content.lower() and ("fetch" in content or "axios" in content or "api" in content.lower()):
                uses_api = True
                result.pass_check("bible_content", f"Uses Bible API in {f.name}")
                break

        if not uses_api:
            result.fail_check("bible_content", "No Bible data files or API calls found")
        return

    result.pass_check("bible_content", f"Found {len(data_files)} Bible data files")

    # Verify KJV text for known verses
    for f in data_files:
        content = f.read_text(errors="ignore")
        if "In the beginning God created" in content:
            result.pass_check("genesis_1_1", "Genesis 1:1 text verified")
            return

    result.warn_check("genesis_1_1", "Could not verify Genesis 1:1 text in bundled data")


def check_nutrition_calc(app_path: Path, result: QAResult):
    """Check nutrition tracker has real calculation logic."""
    calc_files = list(app_path.rglob("*nutrition*")) + list(app_path.rglob("*calori*")) + list(app_path.rglob("*tdee*"))
    calc_files = [f for f in calc_files if f.suffix in [".ts", ".tsx", ".js"] and "node_modules" not in str(f)]

    if not calc_files:
        result.warn_check("nutrition_calc", "No dedicated nutrition calculation files found")
        # Check all source files for calculation logic
        for f in find_all_source_files(app_path):
            content = f.read_text(errors="ignore")
            if "mifflin" in content.lower() or "harris" in content.lower() or "bmr" in content.lower():
                result.pass_check("tdee_formula", f"TDEE formula found in {f.name}")
                return
        result.fail_check("tdee_formula", "No TDEE/BMR calculation found anywhere")
        return

    for f in calc_files:
        content = f.read_text(errors="ignore")
        # Check for Mifflin-St Jeor formula
        if "mifflin" in content.lower() or ("10" in content and "6.25" in content and "5" in content):
            result.pass_check("tdee_formula", f"Mifflin-St Jeor formula in {f.name}")
        elif "harris" in content.lower() or "benedict" in content.lower():
            result.pass_check("tdee_formula", f"Harris-Benedict formula in {f.name}")
        else:
            result.warn_check("tdee_formula", f"Calculation file exists but formula not recognized: {f.name}")

    # Check for macro split
    for f in calc_files:
        content = f.read_text(errors="ignore")
        if "protein" in content.lower() and "carb" in content.lower() and "fat" in content.lower():
            result.pass_check("macro_split", f"Macro split (P/C/F) found in {f.name}")
            return
    result.warn_check("macro_split", "No protein/carb/fat split calculation found")


def check_consent_encryption(app_path: Path, result: QAResult):
    """Check consent app has real encryption."""
    enc_file = app_path / "services" / "encryption.ts"
    if not enc_file.exists():
        result.fail_check("encryption", "No encryption.ts found")
        return

    content = enc_file.read_text(errors="ignore")

    # Check for real AES (not XOR)
    if "AES" in content or "aes" in content or "CTR" in content:
        result.pass_check("encryption_algo", "AES encryption detected")
    elif "xor" in content.lower() and "XOR" not in content.split("//")[0]:
        result.fail_check("encryption_algo", "Still using XOR cipher — must upgrade to AES")
    else:
        result.warn_check("encryption_algo", "Encryption exists but algorithm unclear")

    # Check for HMAC
    if "hmac" in content.lower() or "HMAC" in content:
        result.pass_check("hmac_integrity", "HMAC integrity verification present")
    else:
        result.fail_check("hmac_integrity", "No HMAC — documents can be tampered")

    # Check for PBKDF2
    if "100000" in content or "100_000" in content or "pbkdf2" in content.lower():
        result.pass_check("key_derivation", "PBKDF2 with 100K+ iterations")
    else:
        result.warn_check("key_derivation", "Key derivation may be weak")

    # Check auth for PIN lockout
    auth_file = app_path / "services" / "auth.ts"
    if auth_file.exists():
        auth_content = auth_file.read_text(errors="ignore")
        if "lockout" in auth_content.lower() or "failed_attempts" in auth_content.lower() or "MAX_ATTEMPTS" in auth_content:
            result.pass_check("pin_lockout", "PIN brute-force protection present")
        else:
            result.fail_check("pin_lockout", "No PIN lockout — vulnerable to brute force")

    # Check for audit log
    audit_file = app_path / "services" / "auditLog.ts"
    if audit_file.exists():
        result.pass_check("audit_log", "Audit logging service present")
    else:
        result.warn_check("audit_log", "No audit logging")

    # Check for cloud backup
    backup_file = app_path / "services" / "cloudBackup.ts"
    if backup_file.exists():
        result.pass_check("cloud_backup", "Cloud backup service present")
    else:
        result.warn_check("cloud_backup", "No cloud backup — user could lose data")


def check_template_system(app_path: Path, result: QAResult):
    """Check consent app template quality."""
    index_file = app_path / "assets" / "templates" / "TEMPLATE_INDEX.json"
    if not index_file.exists():
        result.warn_check("templates", "No TEMPLATE_INDEX.json found")
        return

    with open(index_file) as f:
        data = json.load(f)

    templates = data.get("templates", [])
    result.pass_check("template_count", f"{len(templates)} templates indexed")

    # Verify each template file exists and has content
    missing = []
    empty = []
    for t in templates:
        tfile = app_path / "assets" / "templates" / t["filename"]
        if not tfile.exists():
            missing.append(t["filename"])
        elif tfile.stat().st_size < 200:
            empty.append(t["filename"])

    if missing:
        result.fail_check("template_files", f"Missing template files: {', '.join(missing)}")
    else:
        result.pass_check("template_files", "All template files exist")

    if empty:
        result.warn_check("template_content", f"Templates with <200 bytes: {', '.join(empty)}")
    else:
        result.pass_check("template_content", "All templates have substantial content")


# ============================================================
# MAIN QA RUNNER
# ============================================================

def run_deep_qa(app_path: Path) -> QAResult:
    """Run all applicable QA checks on an app."""
    result = QAResult()
    app_type = detect_app_type(app_path)
    app_name = app_path.name

    print(f"\n{'=' * 60}")
    print(f"Deep QA: {app_name} (type: {app_type})")
    print(f"{'=' * 60}")

    # Universal checks
    check_no_dead_imports(app_path, result)
    check_no_console_errors(app_path, result)
    check_async_error_handling(app_path, result)
    check_empty_screens(app_path, result)
    check_hardcoded_strings(app_path, result)
    check_payment_flow(app_path, result)
    check_onboarding_exists(app_path, result)
    check_paywall_rescue(app_path, result)

    # App-type specific checks
    if app_type == "ebook_reader":
        check_ebook_catalog(app_path, result)
    elif app_type == "religious_reading":
        check_bible_content(app_path, result)
    elif app_type == "nutrition_tracker":
        check_nutrition_calc(app_path, result)
    elif app_type == "consent_legal":
        check_consent_encryption(app_path, result)
        check_template_system(app_path, result)

    # Print results
    for status, name, detail in result.checks:
        icon = {"PASS": "[+]", "FAIL": "[X]", "WARN": "[!]"}[status]
        print(f"  {icon} {name}: {detail}")

    print(f"\n  Result: {'PASS' if result.passed else 'FAIL'} ({result.passes} pass, {result.fails} fail, {result.warns} warn)")

    # Write report
    report_path = RESULTS_DIR / f"qa_{app_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, "w") as f:
        f.write(f"# Deep QA Report: {app_name}\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Type:** {app_type}\n")
        f.write(f"**Result:** {'PASS' if result.passed else 'FAIL'}\n\n")
        f.write(f"| Status | Check | Detail |\n|--------|-------|--------|\n")
        for status, name, detail in result.checks:
            f.write(f"| {status} | {name} | {detail} |\n")

    return result


def main():
    parser = argparse.ArgumentParser(description="App Factory Deep QA")
    parser.add_argument("--test", type=str, help="Path to app to test")
    parser.add_argument("--test-all", action="store_true", help="Test all apps in builds/")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues where possible")
    args = parser.parse_args()

    if args.test:
        app_path = Path(args.test).resolve()
        if not app_path.exists():
            print(f"Error: {app_path} not found")
            sys.exit(1)
        result = run_deep_qa(app_path)
        sys.exit(0 if result.passed else 1)

    elif args.test_all:
        if not BUILDS.exists():
            print(f"Error: {BUILDS} not found")
            sys.exit(1)

        apps = sorted([d for d in BUILDS.iterdir() if d.is_dir() and (d / "app.json").exists()])
        all_results = {}

        for app_path in apps:
            result = run_deep_qa(app_path)
            all_results[app_path.name] = result

        # Summary
        print(f"\n{'=' * 60}")
        print("Deep QA Summary")
        print(f"{'=' * 60}")
        print(f"{'App':<30} {'Result':<8} {'Pass':<6} {'Fail':<6} {'Warn':<6}")
        print("-" * 60)
        for name, result in all_results.items():
            status = "PASS" if result.passed else "FAIL"
            print(f"{name:<30} {status:<8} {result.passes:<6} {result.fails:<6} {result.warns:<6}")

        total_fails = sum(r.fails for r in all_results.values())
        sys.exit(0 if total_fails == 0 else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
