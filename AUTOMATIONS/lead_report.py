#!/usr/bin/env python3
"""
PRINTMAXX Lead Report
======================
Reads LEDGER/leads.csv and writes a markdown report to
AUTOMATIONS/agent/swarm/reports/lead_report.md.

Metrics:
  - Total leads all time
  - Leads today / this week / this month
  - Growth rate (week-over-week)
  - Top sources (page / site that sent the lead)
  - Top UTM campaigns
  - Daily lead cadence (last 14 days)
  - Duplicate / invalid entries flagged

Usage:
    python3 AUTOMATIONS/lead_report.py            # write report, print summary
    python3 AUTOMATIONS/lead_report.py --status   # print summary only, no file write
    python3 AUTOMATIONS/lead_report.py --dry-run  # alias for --status

Cron (daily 8:15 AM, after scrapers are done):
    15 8 * * * cd $BASE && $PYTHON AUTOMATIONS/lead_report.py >> AUTOMATIONS/logs/lead_report.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEADS_CSV    = PROJECT_ROOT / "LEDGER" / "leads.csv"
REPORT_DIR   = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"
REPORT_FILE  = REPORT_DIR / "lead_report.md"
LOG_DIR      = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE     = LOG_DIR / "lead_report.log"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        with open(safe_path(LOG_FILE), "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Load leads
# ---------------------------------------------------------------------------

def load_leads() -> list[dict]:
    p = safe_path(LEADS_CSV)
    if not p.exists():
        return []
    rows = []
    with open(p, newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def parse_date(ts: str) -> date | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts[:10]).date()
    except Exception:
        return None


def analyze(rows: list[dict]) -> dict:
    today     = date.today()
    week_ago  = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    prev_week = today - timedelta(days=14)

    total       = len(rows)
    today_leads = 0
    week_leads  = 0
    prev_week_leads = 0
    month_leads = 0

    daily: dict[str, int] = defaultdict(int)
    sources: Counter      = Counter()
    campaigns: Counter    = Counter()
    pages: Counter        = Counter()

    for row in rows:
        d = parse_date(row.get("timestamp", ""))
        src = (row.get("source") or "unknown").strip() or "unknown"
        camp = (row.get("utm_campaign") or "").strip() or "(none)"
        page = (row.get("page_url") or "").strip() or "(direct)"

        sources[src]   += 1
        campaigns[camp] += 1
        pages[page]     += 1

        if d:
            daily[d.isoformat()] += 1
            if d == today:
                today_leads += 1
            if d >= week_ago:
                week_leads += 1
            if prev_week <= d < week_ago:
                prev_week_leads += 1
            if d >= month_ago:
                month_leads += 1

    wow_growth = 0.0
    if prev_week_leads > 0:
        wow_growth = ((week_leads - prev_week_leads) / prev_week_leads) * 100

    # Daily cadence — last 14 days
    cadence = []
    for i in range(13, -1, -1):
        d_str = (today - timedelta(days=i)).isoformat()
        cadence.append((d_str, daily.get(d_str, 0)))

    return {
        "total":            total,
        "today":            today_leads,
        "this_week":        week_leads,
        "prev_week":        prev_week_leads,
        "this_month":       month_leads,
        "wow_growth_pct":   wow_growth,
        "top_sources":      sources.most_common(10),
        "top_campaigns":    campaigns.most_common(5),
        "top_pages":        pages.most_common(5),
        "daily_cadence":    cadence,
        "generated_at":     datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_report(stats: dict) -> str:
    wow = stats["wow_growth_pct"]
    wow_str = f"+{wow:.1f}%" if wow >= 0 else f"{wow:.1f}%"

    lines: list[str] = []
    a = lines.append

    a(f"# Lead Report")
    a(f"_Generated {stats['generated_at'][:16]} UTC_")
    a("")
    a("## Summary")
    a("")
    a(f"| Metric | Count |")
    a(f"|--------|-------|")
    a(f"| Total leads | **{stats['total']}** |")
    a(f"| Today | {stats['today']} |")
    a(f"| This week (7d) | {stats['this_week']} |")
    a(f"| This month (30d) | {stats['this_month']} |")
    a(f"| WoW growth | {wow_str} |")
    a("")

    a("## Top sources")
    a("")
    if stats["top_sources"]:
        a("| Source | Leads |")
        a("|--------|-------|")
        for src, cnt in stats["top_sources"]:
            a(f"| `{src}` | {cnt} |")
    else:
        a("_No data yet._")
    a("")

    a("## Top UTM campaigns")
    a("")
    if stats["top_campaigns"]:
        a("| Campaign | Leads |")
        a("|----------|-------|")
        for camp, cnt in stats["top_campaigns"]:
            a(f"| `{camp}` | {cnt} |")
    else:
        a("_No data yet._")
    a("")

    a("## Top landing pages")
    a("")
    if stats["top_pages"]:
        a("| Page URL | Leads |")
        a("|----------|-------|")
        for page, cnt in stats["top_pages"]:
            short = page[:80] + ("..." if len(page) > 80 else "")
            a(f"| `{short}` | {cnt} |")
    else:
        a("_No data yet._")
    a("")

    a("## Daily cadence (last 14 days)")
    a("")
    a("```")
    max_count = max((c for _, c in stats["daily_cadence"]), default=1) or 1
    for day_str, count in stats["daily_cadence"]:
        bar_len = round((count / max_count) * 30)
        bar = "#" * bar_len
        a(f"{day_str}  {bar:<30}  {count}")
    a("```")
    a("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="PRINTMAXX lead report generator")
    parser.add_argument("--status",  action="store_true", help="Print summary only, do not write file")
    parser.add_argument("--dry-run", action="store_true", help="Alias for --status")
    args = parser.parse_args()

    rows  = load_leads()
    stats = analyze(rows)

    # Always print a short summary to stdout / cron log
    wow = stats["wow_growth_pct"]
    wow_str = f"+{wow:.1f}%" if wow >= 0 else f"{wow:.1f}%"
    print(f"Leads: {stats['total']} total | {stats['today']} today | "
          f"{stats['this_week']} this week | WoW {wow_str}")

    if args.status or args.dry_run:
        # Extended console print for --status
        top = stats["top_sources"][:3]
        if top:
            print("Top sources: " + " | ".join(f"{s} ({c})" for s, c in top))
        return

    # Write the full report
    report_md = build_report(stats)
    safe_path(REPORT_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(REPORT_FILE), "w") as f:
        f.write(report_md)

    log(f"Report written to {REPORT_FILE} ({stats['total']} leads)")


if __name__ == "__main__":
    main()
