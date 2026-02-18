#!/usr/bin/env python3
"""
PRINTMAXX Self-Test Automation
Validates operational readiness across all money methods.
Scores each op on Infrastructure, Accounts, Revenue, and Freshness.

Usage:
    python3 scripts/self_test.py             # Full self-test
    python3 scripts/self_test.py --op MM007  # Test specific op
    python3 scripts/self_test.py --json      # JSON output for automation
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER = BASE_DIR / "LEDGER"
FINANCIALS = BASE_DIR / "FINANCIALS"
AUTOMATIONS = BASE_DIR / "AUTOMATIONS"
MONEY_METHODS = BASE_DIR / "MONEY_METHODS"
PRODUCTS = BASE_DIR / "PRODUCTS"
EMAIL_DIR = BASE_DIR / "EMAIL"
CONTENT = BASE_DIR / "CONTENT"
LANDING = BASE_DIR / "LANDING"
OPS = BASE_DIR / "OPS"

ACCOUNTS_CSV = LEDGER / "ACCOUNTS.csv"
REVENUE_CSV = FINANCIALS / "REVENUE_TRACKER.csv"
RESULTS_DIR = LEDGER / "SELF_TEST_RESULTS"

FRESHNESS_DAYS = 30  # Files modified within this window score full marks

# ---------------------------------------------------------------------------
# Op definitions: what each op needs to be ready
# ---------------------------------------------------------------------------

OP_DEFINITIONS = {
    "MM007_COLD_OUTBOUND": {
        "display": "MM007_COLD_OUTBOUND",
        "description": "Cold email outreach pipeline",
        "infra_files": [
            AUTOMATIONS / "local_biz_pipeline.py",
            LEDGER / "OUTREACH_PIPELINE.csv",
            MONEY_METHODS / "COLD_OUTBOUND" / "TIER1_COLD_EMAIL_SEQUENCES.md",
            MONEY_METHODS / "COLD_OUTBOUND" / "EMAIL_SEQUENCES_TIER1.md",
            EMAIL_DIR / "sequences",
        ],
        "infra_dirs": [
            MONEY_METHODS / "COLD_OUTBOUND",
            EMAIL_DIR,
        ],
        "required_accounts": {
            "platforms": ["Email"],
            "statuses_ok": ["ACTIVE", "WARMING_UP", "PENDING"],
        },
        "revenue_method_ids": ["MM007_COLD_OUTBOUND", "MM007"],
    },
    "MM_DIGITAL_PRODUCTS": {
        "display": "MM_DIGITAL_PRODUCTS",
        "description": "Gumroad / Whop digital products",
        "infra_files": [
            PRODUCTS / "listings",
            PRODUCTS / "descriptions",
        ],
        "infra_dirs": [
            PRODUCTS,
            MONEY_METHODS / "DIGITAL_PRODUCTS" if (MONEY_METHODS / "DIGITAL_PRODUCTS").exists() else PRODUCTS,
        ],
        "required_accounts": {
            "platforms": ["Gumroad", "Whop"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_DIGITAL_PRODUCTS", "MM002", "MM002_INFO_PRODUCTS"],
    },
    "MM_FREELANCE_ARB": {
        "display": "MM_FREELANCE_ARB",
        "description": "Fiverr/Upwork freelance arbitrage",
        "infra_files": [
            LEDGER / "FREELANCE_PIPELINE.csv",
        ],
        "infra_dirs": [],
        "required_accounts": {
            "platforms": ["Fiverr", "Upwork"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_FREELANCE_ARB", "MM029", "MM029_FREELANCE_ARBITRAGE"],
    },
    "MM_AI_FINDOM": {
        "display": "MM_AI_FINDOM",
        "description": "AI NSFW findom persona network",
        "infra_files": [
            MONEY_METHODS / "AI_INFLUENCER" / "AI_NSFW_FINDOM_EXECUTION_PLAN.md",
            MONEY_METHODS / "AI_INFLUENCER" / "FINDOM" / "EDGE_SYNTHESIS_AND_DISTRIBUTION_PLAYBOOK.md",
            MONEY_METHODS / "AI_INFLUENCER" / "FINDOM" / "DEEP_RESEARCH_DISTRIBUTION.md",
            MONEY_METHODS / "AI_INFLUENCER" / "FINDOM" / "DEEP_RESEARCH_PRICING_PSYCHOLOGY.md",
        ],
        "infra_dirs": [
            MONEY_METHODS / "AI_INFLUENCER" / "FINDOM",
        ],
        "required_accounts": {
            "platforms": ["Fanvue", "Fansly", "X"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_AI_FINDOM", "AI001", "AI001_AI_FINDOM"],
    },
    "MM_LOCAL_BIZ": {
        "display": "MM_LOCAL_BIZ",
        "description": "Local business website redesign service",
        "infra_files": [
            AUTOMATIONS / "local_biz_pipeline.py",
            MONEY_METHODS / "COLD_OUTBOUND" / "LOCAL_BIZ_WEBSITE_SERVICE.md",
        ],
        "infra_dirs": [
            MONEY_METHODS / "COLD_OUTBOUND",
        ],
        "required_accounts": {
            "platforms": ["Email"],
            "statuses_ok": ["ACTIVE", "WARMING_UP", "PENDING"],
        },
        "revenue_method_ids": ["MM_LOCAL_BIZ", "MM070", "MM070_LOCAL_BIZ"],
    },
    "MM_CONTENT_FARM": {
        "display": "MM_CONTENT_FARM",
        "description": "Multi-niche content farm accounts",
        "infra_files": [
            LEDGER / "CONTENT_CALENDAR_30DAY.csv",
            AUTOMATIONS / "content_posting" / "printmaxxer_tweets_50.csv",
        ],
        "infra_dirs": [
            MONEY_METHODS / "CONTENT_FARM",
            AUTOMATIONS / "content_posting",
        ],
        "required_accounts": {
            "platforms": ["X", "TikTok"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_CONTENT_FARM", "CF001", "CF001_CONTENT_FARM"],
    },
    "MM_AFFILIATE": {
        "display": "MM_AFFILIATE",
        "description": "Affiliate marketing sites and content",
        "infra_files": [
            LEDGER / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv",
        ],
        "infra_dirs": [],
        "required_accounts": {
            "platforms": ["Amazon Associates", "ShareASale", "Impact"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_AFFILIATE", "MM009", "MM009_AFFILIATE"],
    },
    "MM_SEO": {
        "display": "MM_SEO",
        "description": "SEO / programmatic landing pages",
        "infra_files": [
            LEDGER / "GEO_PROMPTS_200.csv",
            LEDGER / "GEO_LONGTAIL_SLUGS_300.csv",
        ],
        "infra_dirs": [
            CONTENT,
        ],
        "required_accounts": {
            "platforms": ["Vercel", "Google Search Console"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_SEO", "MM015", "MM015_SEO"],
    },
    "MM_APP_FACTORY": {
        "display": "MM_APP_FACTORY",
        "description": "iOS/web app builds and submissions",
        "infra_files": [
            MONEY_METHODS / "APP_FACTORY" / "builds" / "prayerlock-web",
            MONEY_METHODS / "APP_FACTORY" / "builds" / "biomaxx-sdk54",
        ],
        "infra_dirs": [
            MONEY_METHODS / "APP_FACTORY" / "builds",
            MONEY_METHODS / "APP_FACTORY",
        ],
        "required_accounts": {
            "platforms": ["Apple Developer", "Google Play"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_APP_FACTORY", "MM001", "MM001_APP_FACTORY"],
    },
    "MM_NEWSLETTER": {
        "display": "MM_NEWSLETTER",
        "description": "Beehiiv newsletters (faith, fitness, tech)",
        "infra_files": [
            MONEY_METHODS / "NEWSLETTER" / "WELCOME_SEQUENCE_FAITH.md",
            MONEY_METHODS / "NEWSLETTER" / "WELCOME_SEQUENCE_FITNESS.md",
            MONEY_METHODS / "NEWSLETTER" / "WELCOME_SEQUENCE_TECH.md",
        ],
        "infra_dirs": [
            MONEY_METHODS / "NEWSLETTER",
        ],
        "required_accounts": {
            "platforms": ["Beehiiv"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_NEWSLETTER", "MM006", "MM006_NEWSLETTER"],
    },
    "MM_POD": {
        "display": "MM_POD",
        "description": "Print-on-demand via TikTok/Etsy",
        "infra_files": [],
        "infra_dirs": [
            MONEY_METHODS / "POD",
        ],
        "required_accounts": {
            "platforms": ["Printful", "Printify", "Etsy"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_POD", "MM011", "MM011_POD"],
    },
    "MM_AI_UGC": {
        "display": "MM_AI_UGC",
        "description": "AI-generated UGC factory",
        "infra_files": [
            MONEY_METHODS / "AI_INFLUENCER" / "AI_NSFW_FINDOM_EXECUTION_PLAN.md",
        ],
        "infra_dirs": [
            MONEY_METHODS / "AI_INFLUENCER",
        ],
        "required_accounts": {
            "platforms": ["HeyGen", "Synthesia"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_AI_UGC", "AI005", "AI005_AI_UGC"],
    },
    "MM_PAID_ADS": {
        "display": "MM_PAID_ADS",
        "description": "Paid ads testing (Meta + TikTok)",
        "infra_files": [],
        "infra_dirs": [],
        "required_accounts": {
            "platforms": ["Meta Ads", "TikTok Ads"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_PAID_ADS", "MM013", "MM013_PAID_ADS"],
    },
    "MM_TIKTOK_SHOP": {
        "display": "MM_TIKTOK_SHOP",
        "description": "TikTok Shop affiliate / dropship",
        "infra_files": [],
        "infra_dirs": [
            MONEY_METHODS / "TIKTOK_SHOP",
        ],
        "required_accounts": {
            "platforms": ["TikTok Shop"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_TIKTOK_SHOP", "MM010"],
    },
    "MM_ROBLOX": {
        "display": "MM_ROBLOX",
        "description": "Roblox tycoon game monetization",
        "infra_files": [
            MONEY_METHODS / "APP_FACTORY" / "builds" / "roblox_tycoon",
        ],
        "infra_dirs": [
            MONEY_METHODS / "APP_FACTORY" / "builds" / "roblox_tycoon",
        ],
        "required_accounts": {
            "platforms": ["Roblox Developer"],
            "statuses_ok": ["ACTIVE"],
        },
        "revenue_method_ids": ["MM_ROBLOX", "MM050"],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def file_exists_and_nonempty(path: Path) -> bool:
    """Check if path exists (file or dir) and if file, is non-empty."""
    p = Path(path)
    if p.is_dir():
        return True
    if p.is_file():
        return p.stat().st_size > 0
    return False


def file_modified_within_days(path: Path, days: int) -> bool:
    """Check if path was modified within the given number of days."""
    p = Path(path)
    if not p.exists():
        return False
    mtime = datetime.fromtimestamp(p.stat().st_mtime)
    return (datetime.now() - mtime) < timedelta(days=days)


def get_newest_mtime(paths: list[Path]) -> datetime | None:
    """Return the most recent mtime across a list of paths."""
    newest = None
    for p in paths:
        pp = Path(p)
        if pp.exists():
            mtime = datetime.fromtimestamp(pp.stat().st_mtime)
            if newest is None or mtime > newest:
                newest = mtime
    return newest


def load_csv(path: Path) -> list[dict]:
    """Load a CSV file into a list of dicts. Returns [] if file missing."""
    if not path.is_file():
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []


def load_accounts() -> list[dict]:
    """Load LEDGER/ACCOUNTS.csv."""
    return load_csv(ACCOUNTS_CSV)


def load_revenue() -> list[dict]:
    """Load FINANCIALS/REVENUE_TRACKER.csv."""
    return load_csv(REVENUE_CSV)


# ---------------------------------------------------------------------------
# Scoring functions
# ---------------------------------------------------------------------------

def score_infrastructure(op_def: dict) -> tuple[int, list[str]]:
    """
    Score infrastructure readiness (0-25).
    Checks that required files/dirs exist and are non-empty.
    """
    all_paths = list(op_def.get("infra_files", [])) + list(op_def.get("infra_dirs", []))

    if not all_paths:
        # No infra requirements defined -- give partial credit
        return 15, ["No infra requirements defined (partial credit)"]

    found = 0
    missing = []
    for p in all_paths:
        if file_exists_and_nonempty(p):
            found += 1
        else:
            missing.append(str(p.relative_to(BASE_DIR)))

    ratio = found / len(all_paths)
    score = round(ratio * 25)

    notes = []
    if missing:
        notes = [f"MISSING: {m}" for m in missing]
    return score, notes


def score_accounts(op_def: dict, all_accounts: list[dict]) -> tuple[int, list[str]]:
    """
    Score account readiness (0-25).
    Checks that required platform accounts exist and are in acceptable status.
    """
    req = op_def.get("required_accounts", {})
    platforms = req.get("platforms", [])
    ok_statuses = [s.upper() for s in req.get("statuses_ok", ["ACTIVE"])]

    if not platforms:
        return 15, ["No account requirements defined (partial credit)"]

    found_active = 0
    found_any = 0
    missing_platforms = []

    for plat in platforms:
        plat_lower = plat.lower()
        matched = [
            a for a in all_accounts
            if plat_lower in a.get("Platform", "").lower()
            or plat_lower in a.get("Niche", "").lower()
            or plat_lower in a.get("Handle", "").lower()
            or plat_lower in a.get("Notes", "").lower()
        ]
        if matched:
            found_any += 1
            if any(a.get("Status", "").upper() in ok_statuses for a in matched):
                found_active += 1
        else:
            missing_platforms.append(plat)

    if not platforms:
        return 25, []

    # Weight: existing accounts = some credit, active accounts = full credit
    existence_ratio = found_any / len(platforms)
    active_ratio = found_active / len(platforms)

    # 60% weight on existence, 40% on active status
    combined = (existence_ratio * 0.6 + active_ratio * 0.4)
    score = round(combined * 25)

    notes = []
    if missing_platforms:
        notes.append(f"MISSING ACCOUNTS: {', '.join(missing_platforms)}")
    inactive = found_any - found_active
    if inactive > 0:
        notes.append(f"{inactive} account(s) found but not ACTIVE")
    return score, notes


def score_revenue(op_def: dict, all_revenue: list[dict]) -> tuple[int, list[str]]:
    """
    Score revenue tracking (0-25).
    Checks for entries in revenue tracker matching this op.
    """
    method_ids = [mid.lower() for mid in op_def.get("revenue_method_ids", [])]

    if not method_ids:
        return 10, ["No revenue method IDs defined"]

    matching = [
        r for r in all_revenue
        if r.get("method_id", "").lower() in method_ids
        or r.get("method_name", "").lower() in method_ids
    ]

    if not matching:
        # New op with no revenue yet: partial credit for being set up
        return 5, ["No revenue entries yet (new op)"]

    # Has revenue entries
    total_rev = 0.0
    for row in matching:
        try:
            total_rev += float(row.get("revenue", 0) or 0)
        except (ValueError, TypeError):
            pass

    notes = [f"{len(matching)} revenue entries, ${total_rev:,.2f} total"]

    if total_rev > 0:
        return 25, notes
    else:
        return 15, notes + ["Revenue entries exist but $0 total"]


def score_freshness(op_def: dict) -> tuple[int, list[str]]:
    """
    Score freshness (0-25).
    Checks if key files have been modified within FRESHNESS_DAYS.
    """
    all_paths = list(op_def.get("infra_files", [])) + list(op_def.get("infra_dirs", []))

    if not all_paths:
        return 10, ["No files to check freshness"]

    existing_paths = [p for p in all_paths if Path(p).exists()]
    if not existing_paths:
        return 0, ["No files exist to check freshness"]

    newest = get_newest_mtime(existing_paths)
    if newest is None:
        return 0, ["Could not determine file modification times"]

    age_days = (datetime.now() - newest).days

    if age_days <= 7:
        score = 25
    elif age_days <= 14:
        score = 20
    elif age_days <= FRESHNESS_DAYS:
        score = 15
    elif age_days <= 60:
        score = 8
    else:
        score = 3

    notes = [f"Newest file: {age_days} days old ({newest.strftime('%Y-%m-%d')})"]
    return score, notes


# ---------------------------------------------------------------------------
# Main test runner
# ---------------------------------------------------------------------------

def run_op_test(op_id: str, op_def: dict, accounts: list[dict], revenue: list[dict]) -> dict:
    """Run all validation checks for a single op. Returns result dict."""
    infra_score, infra_notes = score_infrastructure(op_def)
    acct_score, acct_notes = score_accounts(op_def, accounts)
    rev_score, rev_notes = score_revenue(op_def, revenue)
    fresh_score, fresh_notes = score_freshness(op_def)

    total = infra_score + acct_score + rev_score + fresh_score

    if total >= 80:
        status = "GREEN"
    elif total >= 50:
        status = "YELLOW"
    else:
        status = "RED"

    return {
        "op_id": op_id,
        "display": op_def.get("display", op_id),
        "description": op_def.get("description", ""),
        "scores": {
            "infrastructure": infra_score,
            "accounts": acct_score,
            "revenue": rev_score,
            "freshness": fresh_score,
            "total": total,
        },
        "status": status,
        "notes": {
            "infrastructure": infra_notes,
            "accounts": acct_notes,
            "revenue": rev_notes,
            "freshness": fresh_notes,
        },
    }


def extract_blockers(results: list[dict]) -> list[dict]:
    """Analyze results and extract common blockers."""
    blocker_map: dict[str, list[str]] = {}

    for r in results:
        for note in r["notes"].get("accounts", []):
            if note.startswith("MISSING ACCOUNTS:"):
                platforms = note.replace("MISSING ACCOUNTS: ", "").split(", ")
                for plat in platforms:
                    plat = plat.strip()
                    if plat not in blocker_map:
                        blocker_map[plat] = []
                    blocker_map[plat].append(r["display"])

        for note in r["notes"].get("infrastructure", []):
            if note.startswith("MISSING:"):
                filepath = note.replace("MISSING: ", "").strip()
                key = f"File: {filepath}"
                if key not in blocker_map:
                    blocker_map[key] = []
                blocker_map[key].append(r["display"])

    blockers = []
    for blocker, ops in sorted(blocker_map.items(), key=lambda x: -len(x[1])):
        blockers.append({
            "blocker": blocker,
            "blocked_ops": ops,
            "count": len(ops),
        })

    return blockers


def generate_recommendations(blockers: list[dict]) -> list[str]:
    """Generate prioritized recommendations from blockers."""
    recs = []
    # Sort by number of ops blocked (descending)
    sorted_blockers = sorted(blockers, key=lambda b: -b["count"])

    for i, b in enumerate(sorted_blockers[:10], 1):
        if b["blocker"].startswith("File:"):
            action = f"Create {b['blocker'].replace('File: ', '')}"
        else:
            action = f"Create {b['blocker']} account"
        recs.append(f"{i}. {action} (unblocks {b['count']} op{'s' if b['count'] != 1 else ''}: {', '.join(b['blocked_ops'])})")

    return recs


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_table(results: list[dict]) -> str:
    """Format results as aligned ASCII table."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append(f"=== PRINTMAXX SELF-TEST RESULTS ({today}) ===")
    lines.append("")

    header = f"{'OP':<25} {'INFRA':>5}  {'ACCTS':>5}  {'REV':>5}  {'FRESH':>5}  {'TOTAL':>5}  {'STATUS':<8}"
    lines.append(header)
    lines.append("-" * len(header))

    # Sort by total score descending
    sorted_results = sorted(results, key=lambda r: -r["scores"]["total"])

    for r in sorted_results:
        s = r["scores"]
        status_display = r["status"]
        line = (
            f"{r['display']:<25} "
            f"{s['infrastructure']:>2}/25  "
            f"{s['accounts']:>2}/25  "
            f"{s['revenue']:>2}/25  "
            f"{s['freshness']:>2}/25  "
            f"{s['total']:>3}/100 "
            f" {status_display:<8}"
        )
        lines.append(line)

    return "\n".join(lines)


def format_blockers(blockers: list[dict]) -> str:
    """Format blocker analysis."""
    if not blockers:
        return "\nBLOCKERS:\n  (none detected)"

    lines = ["\nBLOCKERS:"]
    # Account blockers first
    acct_blockers = [b for b in blockers if not b["blocker"].startswith("File:")]
    file_blockers = [b for b in blockers if b["blocker"].startswith("File:")]

    for b in sorted(acct_blockers, key=lambda x: -x["count"]):
        lines.append(f"  - {b['count']} op(s) blocked by missing {b['blocker']} account")

    if file_blockers:
        lines.append(f"  - {len(file_blockers)} missing infrastructure file(s)")

    return "\n".join(lines)


def format_recommendations(recs: list[str]) -> str:
    """Format recommendations."""
    if not recs:
        return "\nRECOMMENDATIONS:\n  (all ops are GREEN)"

    lines = ["\nRECOMMENDATIONS:"]
    for rec in recs:
        lines.append(f"  {rec}")
    return "\n".join(lines)


def format_summary(results: list[dict]) -> str:
    """Format summary stats."""
    total_ops = len(results)
    green = sum(1 for r in results if r["status"] == "GREEN")
    yellow = sum(1 for r in results if r["status"] == "YELLOW")
    red = sum(1 for r in results if r["status"] == "RED")
    avg_score = sum(r["scores"]["total"] for r in results) / total_ops if total_ops else 0

    lines = [
        "\nSUMMARY:",
        f"  Total ops tested: {total_ops}",
        f"  GREEN  (>=80): {green}",
        f"  YELLOW (50-79): {yellow}",
        f"  RED    (<50):   {red}",
        f"  Average score:  {avg_score:.0f}/100",
    ]
    return "\n".join(lines)


def format_detail(result: dict) -> str:
    """Format detailed output for a single op."""
    lines = []
    lines.append(f"\n--- {result['display']} ---")
    lines.append(f"  Description: {result['description']}")
    lines.append(f"  Status: {result['status']} ({result['scores']['total']}/100)")
    lines.append("")

    for dimension in ["infrastructure", "accounts", "revenue", "freshness"]:
        score = result["scores"][dimension]
        notes = result["notes"].get(dimension, [])
        lines.append(f"  {dimension.upper()} ({score}/25):")
        if notes:
            for note in notes:
                lines.append(f"    - {note}")
        else:
            lines.append(f"    - OK")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON output & persistence
# ---------------------------------------------------------------------------

def save_results_json(results: list[dict], blockers: list[dict], recs: list[str]):
    """Save results to LEDGER/SELF_TEST_RESULTS/self_test_YYYY-MM-DD.json."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_path = RESULTS_DIR / f"self_test_{today}.json"

    payload = {
        "timestamp": datetime.now().isoformat(),
        "date": today,
        "ops_tested": len(results),
        "summary": {
            "green": sum(1 for r in results if r["status"] == "GREEN"),
            "yellow": sum(1 for r in results if r["status"] == "YELLOW"),
            "red": sum(1 for r in results if r["status"] == "RED"),
            "average_score": round(sum(r["scores"]["total"] for r in results) / len(results), 1) if results else 0,
        },
        "results": results,
        "blockers": blockers,
        "recommendations": recs,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Self-Test: validate operational readiness"
    )
    parser.add_argument(
        "--op",
        type=str,
        default=None,
        help="Test a specific op only (e.g. MM007, MM_DIGITAL_PRODUCTS)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON for automation",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed notes per op",
    )
    args = parser.parse_args()

    # Load shared data
    accounts = load_accounts()
    revenue = load_revenue()

    # Determine which ops to test
    if args.op:
        # Match by prefix or exact
        op_key = args.op.upper()
        matched = {}
        for k, v in OP_DEFINITIONS.items():
            if k.upper() == op_key or k.upper().startswith(op_key):
                matched[k] = v
        if not matched:
            print(f"ERROR: No op matching '{args.op}' found.", file=sys.stderr)
            print(f"Available ops: {', '.join(sorted(OP_DEFINITIONS.keys()))}", file=sys.stderr)
            sys.exit(1)
        ops_to_test = matched
    else:
        ops_to_test = OP_DEFINITIONS

    # Run tests
    results = []
    for op_id, op_def in ops_to_test.items():
        result = run_op_test(op_id, op_def, accounts, revenue)
        results.append(result)

    # Analyze blockers and recommendations
    blockers = extract_blockers(results)
    recs = generate_recommendations(blockers)

    # Save JSON results
    output_path = save_results_json(results, blockers, recs)

    # Output
    if args.json:
        with open(output_path, "r") as f:
            print(f.read())
    else:
        print(format_table(results))

        if args.verbose or args.op:
            for r in sorted(results, key=lambda x: -x["scores"]["total"]):
                print(format_detail(r))

        print(format_blockers(blockers))
        print(format_recommendations(recs))
        print(format_summary(results))
        print(f"\nResults saved to: {output_path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
