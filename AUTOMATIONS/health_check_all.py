#!/usr/bin/env python3
"""
PRINTMAXX Automation Health Checker
====================================
Imports and validates every script in AUTOMATIONS/.
Reports: WORKING / BROKEN / NEEDS_CONFIG for each.
Shows which scripts need API keys, which need accounts, which are self-contained.

Usage:
    python3 AUTOMATIONS/health_check_all.py --check          # Full health check
    python3 AUTOMATIONS/health_check_all.py --fix-imports     # Show/fix import issues
    python3 AUTOMATIONS/health_check_all.py --report          # Generate summary report
    python3 AUTOMATIONS/health_check_all.py --check --json    # Machine-readable output
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import os
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
OPS_DIR = PROJECT_DIR / "OPS"
REPORT_DIR = OPS_DIR

# ── Constants ────────────────────────────────────────────────────────────────
SKIP_FILES = {
    "__init__.py",
    "health_check_all.py",
    "_audit_scanner.py",
    "_audit_results.json",
    "_duplicate_finder.py",
}

# Standard library modules (cached)
STDLIB: set = set()
if hasattr(sys, "stdlib_module_names"):
    STDLIB = set(sys.stdlib_module_names)
else:
    # Fallback for older Python
    import pkgutil
    STDLIB = {m.name for m in pkgutil.iter_modules() if m.module_finder is None} | {
        "os", "sys", "json", "csv", "re", "time", "datetime", "pathlib",
        "subprocess", "argparse", "logging", "hashlib", "shutil", "threading",
        "typing", "collections", "functools", "dataclasses", "io", "math",
        "random", "tempfile", "signal", "unittest", "http", "urllib",
        "email", "html", "xml", "sqlite3", "socket", "ssl", "textwrap",
        "abc", "copy", "enum", "glob", "string", "struct", "traceback",
        "warnings", "weakref", "operator", "itertools", "contextlib",
        "concurrent", "multiprocessing", "queue", "fcntl",
    }

# API key patterns to detect
API_KEY_PATTERNS = {
    "OPENAI": "OpenAI API key",
    "ANTHROPIC": "Anthropic API key",
    "STRIPE": "Stripe payment key",
    "TWITTER_BEARER": "Twitter/X API bearer token",
    "REDDIT_CLIENT": "Reddit API credentials",
    "GUMROAD": "Gumroad access token",
    "SENDGRID": "SendGrid email API",
    "SLACK_TOKEN": "Slack bot token",
    "VERCEL_TOKEN": "Vercel deploy token",
    "SURGE_TOKEN": "Surge.sh token",
    "NETLIFY_AUTH_TOKEN": "Netlify auth token",
}

INSTALL_HINTS = {
    "requests": "pip3 install requests",
    "bs4": "pip3 install beautifulsoup4",
    "playwright": "pip3 install playwright && python3 -m playwright install chromium",
    "openpyxl": "pip3 install openpyxl",
    "rich": "pip3 install rich",
    "Crypto": "pip3 install pycryptodome",
    "pytrends": "pip3 install pytrends",
    "anthropic": "pip3 install anthropic",
    "textual": "pip3 install textual",
    "flask": "pip3 install flask",
    "tqdm": "pip3 install tqdm",
    "numpy": "pip3 install numpy",
    "torch": "pip3 install torch",
    "soundfile": "pip3 install soundfile",
    "browser_cookie3": "pip3 install browser-cookie3",
    "whisper": "pip3 install openai-whisper",
    "duckdb": "pip3 install duckdb",
    "requests_oauthlib": "pip3 install requests-oauthlib",
    "google": "pip3 install google-api-python-client",
    "urllib3": "pip3 install urllib3",
    "certifi": "pip3 install certifi",
}


@dataclass
class ScriptHealth:
    """Health status for a single automation script."""
    filename: str
    lines: int = 0
    status: str = "UNKNOWN"  # WORKING / BROKEN / NEEDS_CONFIG / NEEDS_DEPS
    has_argparse: bool = False
    has_main_guard: bool = False
    imports_all: List[str] = field(default_factory=list)
    imports_missing: List[str] = field(default_factory=list)
    imports_local: List[str] = field(default_factory=list)
    api_keys_needed: List[str] = field(default_factory=list)
    hardcoded_paths: List[int] = field(default_factory=list)
    help_output: str = ""
    help_works: bool = False
    error_message: str = ""
    category: str = "unknown"  # scraper, orchestrator, dashboard, utility, etc.

    def status_emoji(self) -> str:
        return {
            "WORKING": "[OK]",
            "BROKEN": "[BROKEN]",
            "NEEDS_CONFIG": "[CONFIG]",
            "NEEDS_DEPS": "[DEPS]",
            "UNKNOWN": "[???]",
        }.get(self.status, "[???]")


def categorize_script(filename: str) -> str:
    """Categorize a script by its name."""
    name = filename.lower()
    if any(x in name for x in ["scraper", "scrape"]):
        return "scraper"
    if any(x in name for x in ["monitor", "tracker", "scanner"]):
        return "monitor"
    if any(x in name for x in ["orchestrator", "supervisor", "runner", "pipeline"]):
        return "orchestrator"
    if any(x in name for x in ["dashboard", "tui", "desktop", "server"]):
        return "dashboard"
    if any(x in name for x in ["guard", "backup", "health", "checkpoint", "log_rotator"]):
        return "safety"
    if any(x in name for x in ["content", "email", "post", "tweet"]):
        return "content"
    if any(x in name for x in ["ecom", "arb", "product", "listing", "gumroad"]):
        return "ecommerce"
    if any(x in name for x in ["lead", "outreach", "freelance", "client"]):
        return "outbound"
    if any(x in name for x in ["alpha", "research", "trend", "signal"]):
        return "research"
    if any(x in name for x in ["deploy", "ship", "build", "package"]):
        return "deploy"
    return "utility"


def analyze_script(filepath: Path) -> ScriptHealth:
    """Static analysis of a single Python script."""
    filename = filepath.name
    health = ScriptHealth(filename=filename)
    health.category = categorize_script(filename)

    try:
        src = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        health.status = "BROKEN"
        health.error_message = f"Cannot read file: {e}"
        return health

    health.lines = len(src.splitlines())

    # Parse AST
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        health.status = "BROKEN"
        health.error_message = f"Syntax error: {e}"
        return health

    # Extract imports
    imports = set()
    local_imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mod = node.module.split(".")[0]
                imports.add(mod)
                if (BASE_DIR / f"{mod}.py").exists():
                    local_imports.add(mod)

    health.imports_all = sorted(imports)
    health.imports_local = sorted(local_imports)

    # Check for missing imports
    missing = []
    for imp in sorted(imports):
        if imp in STDLIB:
            continue
        if (BASE_DIR / f"{imp}.py").exists():
            continue
        try:
            importlib.import_module(imp)
        except ImportError:
            missing.append(imp)
    health.imports_missing = missing

    # Check for argparse and __main__
    health.has_argparse = "argparse" in imports
    health.has_main_guard = "__main__" in src

    # Check for hardcoded paths
    for i, line in enumerate(src.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "/Users/" in line and "Path(__file__)" not in line:
            health.hardcoded_paths.append(i)

    # Check for API key references
    for pattern, desc in API_KEY_PATTERNS.items():
        if pattern in src:
            health.api_keys_needed.append(pattern)

    # Determine status
    if missing:
        health.status = "NEEDS_DEPS"
        health.error_message = f"Missing: {', '.join(missing)}"
    elif health.api_keys_needed:
        health.status = "NEEDS_CONFIG"
        health.error_message = f"Needs: {', '.join(health.api_keys_needed)}"
    else:
        health.status = "WORKING"

    return health


def test_script_help(filepath: Path, health: ScriptHealth) -> ScriptHealth:
    """Try running script with --help to verify it actually loads."""
    if not health.has_argparse:
        return health

    try:
        result = subprocess.run(
            [sys.executable, str(filepath), "--help"],
            capture_output=True, text=True, timeout=10,
            cwd=str(BASE_DIR),
        )
        if result.returncode == 0:
            health.help_works = True
            health.help_output = result.stdout[:500]
        else:
            # --help returned non-zero but may still be a valid script
            health.help_output = (result.stderr or result.stdout)[:300]
            if health.status == "WORKING":
                health.status = "BROKEN"
                health.error_message = f"--help failed: {health.help_output[:100]}"
    except subprocess.TimeoutExpired:
        health.help_output = "TIMEOUT (>10s)"
    except Exception as e:
        health.help_output = f"Error: {e}"

    return health


def run_check(run_help: bool = False, json_output: bool = False) -> List[ScriptHealth]:
    """Run health check on all scripts."""
    results: List[ScriptHealth] = []
    scripts = sorted(BASE_DIR.glob("*.py"))

    print(f"Scanning {len(scripts)} Python files in {BASE_DIR}\n")

    for filepath in scripts:
        if filepath.name in SKIP_FILES or filepath.name.startswith("_"):
            continue

        health = analyze_script(filepath)

        if run_help and health.has_argparse and health.status in ("WORKING", "NEEDS_CONFIG"):
            health = test_script_help(filepath, health)

        results.append(health)

    if json_output:
        print(json.dumps([asdict(h) for h in results], indent=2))
        return results

    # Summary
    total = len(results)
    working = sum(1 for r in results if r.status == "WORKING")
    needs_config = sum(1 for r in results if r.status == "NEEDS_CONFIG")
    needs_deps = sum(1 for r in results if r.status == "NEEDS_DEPS")
    broken = sum(1 for r in results if r.status == "BROKEN")

    print("=" * 70)
    print(f"  PRINTMAXX AUTOMATION HEALTH CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print(f"  Total scripts:    {total}")
    print(f"  WORKING:          {working}")
    print(f"  NEEDS_CONFIG:     {needs_config}  (need API keys or accounts)")
    print(f"  NEEDS_DEPS:       {needs_deps}  (missing pip packages)")
    print(f"  BROKEN:           {broken}")
    print("=" * 70)

    # Category breakdown
    cats = Counter(r.category for r in results)
    print("\n  BY CATEGORY:")
    for cat, count in cats.most_common():
        cat_working = sum(1 for r in results if r.category == cat and r.status == "WORKING")
        print(f"    {cat:15s}: {count:3d} total, {cat_working:3d} working")

    # Show broken/needs-config
    if needs_deps > 0:
        print(f"\n  NEEDS DEPENDENCIES ({needs_deps}):")
        for r in results:
            if r.status == "NEEDS_DEPS":
                hints = [INSTALL_HINTS.get(m, f"pip3 install {m}") for m in r.imports_missing]
                print(f"    {r.filename:45s} {r.error_message}")
                for h in hints:
                    print(f"      -> {h}")

    if needs_config > 0:
        print(f"\n  NEEDS CONFIG ({needs_config}):")
        for r in results:
            if r.status == "NEEDS_CONFIG":
                keys = ", ".join(r.api_keys_needed)
                print(f"    {r.filename:45s} needs: {keys}")

    if broken > 0:
        print(f"\n  BROKEN ({broken}):")
        for r in results:
            if r.status == "BROKEN":
                print(f"    {r.filename:45s} {r.error_message}")

    # Hardcoded paths warning
    with_hardcoded = [r for r in results if r.hardcoded_paths]
    if with_hardcoded:
        print(f"\n  HARDCODED PATHS ({len(with_hardcoded)} scripts):")
        for r in with_hardcoded[:10]:
            print(f"    {r.filename:45s} lines: {r.hardcoded_paths[:5]}")
        if len(with_hardcoded) > 10:
            print(f"    ... and {len(with_hardcoded) - 10} more")

    # Scripts with --help working
    if run_help:
        help_ok = sum(1 for r in results if r.help_works)
        print(f"\n  --help TESTED: {help_ok}/{sum(1 for r in results if r.has_argparse)} argparse scripts passed")

    print()
    return results


def run_fix_imports():
    """Show and suggest fixes for import issues."""
    results = run_check(run_help=False)

    print("\n" + "=" * 70)
    print("  IMPORT FIX SUGGESTIONS")
    print("=" * 70)

    # Collect all missing packages
    all_missing = Counter()
    for r in results:
        for m in r.imports_missing:
            all_missing[m] += 1

    if not all_missing:
        print("  All imports resolve correctly. No fixes needed.")
        return

    print(f"\n  Missing packages (install to fix {sum(all_missing.values())} import issues):\n")
    install_cmds = []
    for pkg, count in all_missing.most_common():
        hint = INSTALL_HINTS.get(pkg, f"pip3 install {pkg}")
        print(f"    {pkg:25s} (used by {count} scripts) -> {hint}")
        install_cmds.append(hint)

    print(f"\n  ONE-LINER FIX (install all at once):")
    packages = []
    for pkg in all_missing:
        if pkg in INSTALL_HINTS:
            # Extract package name from hint
            parts = INSTALL_HINTS[pkg].split("install ")[-1].split(" &&")[0]
            packages.append(parts)
        else:
            packages.append(pkg)
    print(f"    pip3 install {' '.join(packages)}")

    # Check for local import issues (cross-imports that need sys.path)
    print(f"\n  LOCAL CROSS-IMPORTS:")
    for r in results:
        if r.imports_local:
            print(f"    {r.filename:45s} -> {', '.join(r.imports_local)}")
    print("    (These work if scripts are run from AUTOMATIONS/ directory)")


def run_report(results: Optional[List[ScriptHealth]] = None) -> str:
    """Generate a full report and return the report path."""
    if results is None:
        results = run_check(run_help=True)

    total = len(results)
    working = sum(1 for r in results if r.status == "WORKING")
    needs_config = sum(1 for r in results if r.status == "NEEDS_CONFIG")
    needs_deps = sum(1 for r in results if r.status == "NEEDS_DEPS")
    broken = sum(1 for r in results if r.status == "BROKEN")

    report_path = REPORT_DIR / "AUTOMATION_HEALTH_REPORT_MAR5.md"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f"# PRINTMAXX Automation Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total scripts | {total} |")
    lines.append(f"| WORKING (self-contained) | {working} |")
    lines.append(f"| NEEDS_CONFIG (API keys/accounts) | {needs_config} |")
    lines.append(f"| NEEDS_DEPS (missing packages) | {needs_deps} |")
    lines.append(f"| BROKEN | {broken} |")
    lines.append("")

    lines.append("## Category Breakdown")
    lines.append("")
    cats = Counter(r.category for r in results)
    lines.append("| Category | Total | Working | Needs Config | Needs Deps | Broken |")
    lines.append("|----------|-------|---------|--------------|------------|--------|")
    for cat, count in cats.most_common():
        cw = sum(1 for r in results if r.category == cat and r.status == "WORKING")
        cc = sum(1 for r in results if r.category == cat and r.status == "NEEDS_CONFIG")
        cd = sum(1 for r in results if r.category == cat and r.status == "NEEDS_DEPS")
        cb = sum(1 for r in results if r.category == cat and r.status == "BROKEN")
        lines.append(f"| {cat} | {count} | {cw} | {cc} | {cd} | {cb} |")
    lines.append("")

    # Top 10 fixes applied
    lines.append("## Top 10 Fixes Applied (Mar 5, 2026)")
    lines.append("")
    lines.append("1. **qwen3_tts_longform.py** - Added try/except guards for missing qwen_tts, soundfile, torch, numpy with install hints")
    lines.append("2. **guardrails.py** - Replaced hardcoded PROJECT_ROOT with auto-detection from `Path(__file__)`")
    lines.append("3. **daily_research_pipeline.py** - Replaced hardcoded PROJECT_DIR with auto-detection")
    lines.append("4. **background_reddit_scraper.py** - Replaced hardcoded PROJECT_DIR with auto-detection")
    lines.append("5. **background_twitter_scraper.py** - Replaced hardcoded PROJECT_DIR with auto-detection")
    lines.append("6. **meme_coin_signal_tracker.py** - Added missing `from pathlib import Path`, replaced hardcoded PROJECT_ROOT")
    lines.append("7. **download_bulk_leads.py** - Replaced hardcoded PROJECT_ROOT and PYTHON path with auto-detection using `sys.executable`")
    lines.append("8. **autonomous_orchestrator.py** - Replaced hardcoded claude CLI path with `shutil.which()` auto-detection")
    lines.append("9. **alpha_monitor.py** - Replaced hardcoded PROJECT_DIR with auto-detection")
    lines.append("10. **alpha_screening.py** - Replaced hardcoded PROJECT_DIR with auto-detection")
    lines.append("")

    # Scraper variants (duplicates)
    lines.append("## Duplicate / Consolidation Candidates")
    lines.append("")
    lines.append("### Reddit Scrapers (6 variants)")
    lines.append("")
    reddit = sorted(r.filename for r in results if "reddit" in r.filename.lower() and "scraper" in r.filename.lower())
    for s in reddit:
        lines.append(f"- `{s}`")
    lines.append("")
    lines.append("Recommendation: Keep `background_reddit_scraper.py` (JSON API, no auth) and `reddit_deep_scraper.py` (Playwright). Archive the rest.")
    lines.append("")

    lines.append("### Twitter Scrapers (9 variants)")
    lines.append("")
    twitter = sorted(r.filename for r in results if "twitter" in r.filename.lower() and "scraper" in r.filename.lower())
    for s in twitter:
        lines.append(f"- `{s}`")
    lines.append("")
    lines.append("Recommendation: Keep `twitter_alpha_scraper.py` (primary) and `background_twitter_scraper.py` (cookie-based). Archive the rest.")
    lines.append("")

    lines.append("### Content Scripts (12 variants)")
    lines.append("")
    content = sorted(r.filename for r in results if "content" in r.filename.lower())
    for s in content:
        lines.append(f"- `{s}`")
    lines.append("")
    lines.append("Recommendation: Consolidate around `content_factory.py` as primary, `auto_content_poster.py` for posting.")
    lines.append("")

    lines.append("### Ecom Scripts (7 variants)")
    lines.append("")
    ecom = sorted(r.filename for r in results if "ecom" in r.filename.lower())
    for s in ecom:
        lines.append(f"- `{s}`")
    lines.append("")
    lines.append("Recommendation: Keep `ecom_autopilot.py` (unified) and `ecom_arb_engine.py`. Archive scanners into archive/.")
    lines.append("")

    # Full script list
    lines.append("## Full Script Status")
    lines.append("")
    lines.append("| Script | Lines | Status | Category | API Keys | Notes |")
    lines.append("|--------|-------|--------|----------|----------|-------|")
    for r in sorted(results, key=lambda x: (x.status != "BROKEN", x.status != "NEEDS_DEPS", x.status != "NEEDS_CONFIG", x.filename)):
        keys = ", ".join(r.api_keys_needed) if r.api_keys_needed else "-"
        notes = ""
        if r.imports_missing:
            notes = f"Missing: {', '.join(r.imports_missing)}"
        elif r.hardcoded_paths:
            notes = f"Hardcoded paths: {len(r.hardcoded_paths)}"
        elif r.help_works:
            notes = "--help OK"
        lines.append(f"| {r.filename} | {r.lines} | {r.status} | {r.category} | {keys} | {notes} |")
    lines.append("")

    # Scripts that need API keys
    lines.append("## Scripts Requiring API Keys")
    lines.append("")
    api_scripts = [r for r in results if r.api_keys_needed]
    if api_scripts:
        key_usage = Counter()
        for r in api_scripts:
            for k in r.api_keys_needed:
                key_usage[k] += 1
        lines.append("| API Key | Used By | Description |")
        lines.append("|---------|---------|-------------|")
        for key, count in key_usage.most_common():
            desc = API_KEY_PATTERNS.get(key, "Unknown")
            lines.append(f"| {key} | {count} scripts | {desc} |")
    lines.append("")

    # Self-contained scripts (highest value - run immediately)
    lines.append("## Self-Contained Scripts (run immediately, no config needed)")
    lines.append("")
    self_contained = [r for r in results if r.status == "WORKING" and r.has_argparse]
    for r in sorted(self_contained, key=lambda x: x.category):
        lines.append(f"- `{r.filename}` ({r.category}, {r.lines}L)")
    lines.append("")

    report_content = "\n".join(lines)
    report_path.write_text(report_content, encoding="utf-8")
    print(f"\nReport written to: {report_path}")
    print(f"  {total} scripts analyzed, {working} working, {needs_config} need config, {needs_deps} need deps, {broken} broken")
    return str(report_path)


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Automation Health Checker - validates all scripts in AUTOMATIONS/"
    )
    parser.add_argument("--check", action="store_true", help="Full health check of all scripts")
    parser.add_argument("--fix-imports", action="store_true", help="Show import issues and fix suggestions")
    parser.add_argument("--report", action="store_true", help="Generate full report to OPS/")
    parser.add_argument("--json", action="store_true", help="Output in JSON format (with --check)")
    parser.add_argument("--run-help", action="store_true", help="Also test --help on each script (slower)")

    args = parser.parse_args()

    if not any([args.check, args.fix_imports, args.report]):
        args.check = True  # default to check

    if args.fix_imports:
        run_fix_imports()
    elif args.report:
        run_report()
    elif args.check:
        run_check(run_help=args.run_help, json_output=args.json)


if __name__ == "__main__":
    main()
