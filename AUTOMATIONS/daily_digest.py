#!/usr/bin/env python3
"""
DAILY DIGEST — What did the autonomous system do today?

Generates a human-readable summary of:
1. Alpha scraped + best finds
2. Content generated + ready to post
3. Agent decisions + actions taken
4. What changed (assets, deployments, fixes)
5. What ONLY the human can do next

Usage:
    python3 AUTOMATIONS/daily_digest.py              # Today's digest
    python3 AUTOMATIONS/daily_digest.py --days 3     # Last 3 days
    python3 AUTOMATIONS/daily_digest.py --save       # Save to OPS/DAILY_DIGEST.md
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT / "LEDGER" / "ALPHA_STAGING.csv"
CONTENT_DIR = PROJECT / "CONTENT" / "social"
REPORTS_DIR = PROJECT / "AUTOMATIONS" / "agent" / "swarm" / "reports"
DECISIONS_LOG = PROJECT / "AUTOMATIONS" / "agent" / "ceo_agent" / "decisions.jsonl"
ASSET_TRACKER = PROJECT / "LEDGER" / "ASSET_TRACKER.csv"
DIGEST_OUTPUT = PROJECT / "OPS" / "DAILY_DIGEST.md"

ROI_ORDER = {"HIGHEST": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


def get_date_range(days):
    dates = []
    for i in range(days):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(d)
    return dates


def alpha_summary(dates):
    if not ALPHA_CSV.exists():
        return "Alpha CSV not found."

    total = 0
    by_status = Counter()
    by_category = Counter()
    by_roi = Counter()
    best = []

    with open(ALPHA_CSV, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            da = row.get("date_added", "") or row.get("created_at", "") or ""
            if not any(d in da for d in dates):
                continue
            total += 1
            status = (row.get("status") or "").upper()
            by_status[status] += 1
            by_category[(row.get("category") or "UNKNOWN").upper()] += 1

            roi_raw = (row.get("roi_potential") or "").strip().upper()
            roi = roi_raw if roi_raw in ROI_ORDER else "UNKNOWN"
            by_roi[roi] += 1

            if status in ("APPROVED", "AUTO_APPROVED", "INTEGRATED", "ROUTED_TO_VENTURE"):
                score = ROI_ORDER.get(roi, 0)
                best.append((score, row))

    best.sort(key=lambda x: x[0], reverse=True)

    lines = []
    lines.append(f"### Alpha Intelligence")
    lines.append(f"- **{total} new entries** scraped")
    lines.append(f"- Actionable: {by_status.get('APPROVED',0) + by_status.get('AUTO_APPROVED',0) + by_status.get('INTEGRATED',0) + by_status.get('ROUTED_TO_VENTURE',0)}")
    lines.append(f"- Archived/low-value: {by_status.get('ARCHIVED',0)}")
    lines.append(f"- Flagged for human review: {by_status.get('FLAGGED_FOR_HUMAN',0)}")
    lines.append("")
    lines.append("**Top categories:** " + ", ".join(f"{c} ({n})" for c, n in by_category.most_common(5)))
    lines.append("")

    if best:
        lines.append("**Best finds:**")
        for _, row in best[:8]:
            aid = row.get("alpha_id", "?")
            cat = row.get("category", "?")
            roi = row.get("roi_potential", "?")
            tactic = (row.get("tactic") or "")[:150]
            source = (row.get("source") or "")[:30]
            lines.append(f"- [{aid}] {cat} | ROI:{roi} | {source}")
            lines.append(f"  {tactic}")
        lines.append("")

    return "\n".join(lines)


def content_summary(dates):
    lines = []
    lines.append("### Content Pipeline")

    # Check for approved posts CSVs
    for date_str in dates:
        month_day = date_str[5:]  # MM-DD
        # Try various naming patterns
        for pattern in [f"APPROVED_POSTS_MAR{date_str[-1]}.csv",
                       f"APPROVED_POSTS_MAR{date_str[-2:]}.csv",
                       f"BUFFER_UPLOAD_MAR{date_str[-1]}.csv",
                       f"BUFFER_UPLOAD_MAR{date_str[-2:]}.csv"]:
            fpath = CONTENT_DIR / pattern
            if fpath.exists():
                with open(fpath, encoding="utf-8", errors="replace") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                lines.append(f"- **{pattern}**: {len(rows)-1} posts ready")

    # Count total content files
    total_files = sum(1 for _ in CONTENT_DIR.rglob("*") if _.is_file() and not _.name.startswith("."))
    lines.append(f"- Total content files: {total_files}")

    # Check auto_generated
    auto_gen = CONTENT_DIR / "auto_generated"
    if auto_gen.exists():
        recent = [f for f in auto_gen.iterdir() if f.is_file()]
        recent_today = [f for f in recent if any(d in str(f.stat().st_mtime) for d in dates)]
        lines.append(f"- Auto-generated folder: {len(recent)} files total")

    lines.append("")
    return "\n".join(lines)


def agent_summary(dates):
    lines = []
    lines.append("### Agent Activity")

    # Check swarm reports
    if REPORTS_DIR.exists():
        date_strs = [d.replace("-", "") for d in dates]
        recent_reports = []
        for f in sorted(REPORTS_DIR.iterdir()):
            if f.is_file() and any(ds in f.name for ds in date_strs):
                recent_reports.append(f.name)

        lines.append(f"- **{len(recent_reports)} reports** generated")
        # Categorize reports
        report_types = Counter()
        for r in recent_reports:
            rtype = r.split("_20")[0] if "_20" in r else r
            report_types[rtype] += 1
        for rtype, count in report_types.most_common(10):
            lines.append(f"  - {rtype}: {count}")

    # Check CEO decisions
    if DECISIONS_LOG.exists():
        recent_decisions = []
        with open(DECISIONS_LOG, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    ts = d.get("ts", "")
                    if any(date in ts for date in dates):
                        recent_decisions.append(d)
                except json.JSONDecodeError:
                    continue

        if recent_decisions:
            lines.append(f"- **{len(recent_decisions)} CEO decisions** made")
            decision_types = Counter(d.get("type", "?") for d in recent_decisions)
            for dtype, count in decision_types.most_common(5):
                lines.append(f"  - {dtype}: {count}")

    lines.append("")
    return "\n".join(lines)


def blocker_summary():
    lines = []
    lines.append("### HUMAN REQUIRED (only you can do these)")
    lines.append("")
    lines.append("| Action | Time | Impact |")
    lines.append("|--------|------|--------|")
    lines.append("| Authenticate Stripe MCP (already installed) | 5 min | Accept payments |")
    lines.append("| Authenticate Gmail MCP (already installed) | 5 min | Send cold emails |")
    lines.append("| Create Gumroad account + list 13 products | 30 min | Digital product revenue |")
    lines.append("| Create Twitter/X account + post queued content | 15 min | Distribution channel |")
    lines.append("| Create Fiverr account + list 2 gigs | 15 min | Service revenue |")
    lines.append("| Sign up for Cloudflare (free) | 5 min | Replace surge.sh hosting |")
    lines.append("")
    lines.append("**Estimated total: ~75 minutes to unblock all revenue channels.**")
    lines.append("")
    return "\n".join(lines)


def improvements_summary(dates):
    lines = []
    lines.append("### What Changed / Improved")

    # Check asset tracker for recent updates
    if ASSET_TRACKER.exists():
        recent_assets = []
        with open(ASSET_TRACKER, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                updated = row.get("last_updated", "")
                if any(d in updated for d in dates):
                    recent_assets.append(row)

        if recent_assets:
            lines.append(f"- **{len(recent_assets)} assets** updated")
            for a in recent_assets[:5]:
                lines.append(f"  - {a.get('name','?')} ({a.get('status','?')}): {(a.get('notes','') or '')[:80]}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Daily digest of autonomous system activity")
    parser.add_argument("--days", type=int, default=1, help="Number of days to cover (default 1)")
    parser.add_argument("--save", action="store_true", help="Save to OPS/DAILY_DIGEST.md")
    args = parser.parse_args()

    dates = get_date_range(args.days)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    output = []
    output.append(f"# DAILY DIGEST — {now}")
    output.append(f"Covering: {dates[-1]} to {dates[0]}")
    output.append(f"Revenue: $0 | Day {(datetime.now() - datetime(2026, 2, 1)).days} at zero")
    output.append("")
    output.append("---")
    output.append("")
    output.append(alpha_summary(dates))
    output.append(content_summary(dates))
    output.append(agent_summary(dates))
    output.append(improvements_summary(dates))
    output.append(blocker_summary())

    digest = "\n".join(output)
    print(digest)

    if args.save:
        DIGEST_OUTPUT.write_text(digest, encoding="utf-8")
        print(f"\nSaved to {DIGEST_OUTPUT}")


if __name__ == "__main__":
    main()
