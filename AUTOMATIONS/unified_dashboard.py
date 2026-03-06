#!/usr/bin/env python3
"""
PRINTMAXX Unified Status Dashboard
Single command: python3 AUTOMATIONS/unified_dashboard.py
Reads all operational CSVs and shows a clean terminal dashboard.
Zero external dependencies.
"""

import csv
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def read_csv(filepath):
    """Read a CSV file and return list of dicts. Returns empty list on error."""
    fp = safe_path(filepath)
    if not fp.exists():
        return []
    try:
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []


def get_revenue_data():
    """Parse REVENUE_TRACKER.csv for this month's revenue."""
    rows = read_csv(PROJECT_ROOT / "FINANCIALS" / "REVENUE_TRACKER.csv")
    now = datetime.now()
    month_prefix = now.strftime("%Y-%m")
    total_revenue = 0.0
    total_expenses = 0.0
    total_profit = 0.0
    method_revenue = Counter()
    for row in rows:
        date_str = row.get("date", "")
        if date_str.startswith(month_prefix):
            try:
                rev = float(row.get("revenue", 0) or 0)
                exp = float(row.get("expenses", 0) or 0)
                prof = float(row.get("profit", 0) or 0)
                total_revenue += rev
                total_expenses += exp
                total_profit += prof
                method_revenue[row.get("method_name", "unknown")] += rev
            except (ValueError, TypeError):
                pass
    # Also scan all-time if no current month data
    all_time_revenue = 0.0
    for row in rows:
        try:
            all_time_revenue += float(row.get("revenue", 0) or 0)
        except (ValueError, TypeError):
            pass
    return {
        "month_revenue": total_revenue,
        "month_expenses": total_expenses,
        "month_profit": total_profit,
        "all_time_revenue": all_time_revenue,
        "top_methods": method_revenue.most_common(5),
    }


def get_venture_health():
    """Parse VENTURE_MAP_HEALTH.csv for venture status."""
    rows = read_csv(PROJECT_ROOT / "LEDGER" / "VENTURE_MAP_HEALTH.csv")
    if not rows:
        return {"total_checks": 0, "ok_count": 0, "warn_count": 0, "latest_status": "NO DATA", "latest_time": "N/A"}

    ok_count = sum(1 for r in rows if r.get("status") == "OK")
    warn_count = sum(1 for r in rows if r.get("status") in ("WARN", "WARNING", "STALE"))
    latest = rows[-1] if rows else {}
    return {
        "total_checks": len(rows),
        "ok_count": ok_count,
        "warn_count": warn_count,
        "latest_status": latest.get("status", "UNKNOWN"),
        "latest_time": latest.get("timestamp", "N/A"),
        "latest_reason": latest.get("reason", ""),
    }


def get_alpha_stats():
    """Parse ALPHA_STAGING.csv for alpha intel status."""
    rows = read_csv(PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv")
    status_counts = Counter()
    category_counts = Counter()
    for row in rows:
        status_counts[row.get("status", "UNKNOWN")] += 1
        category_counts[row.get("category", "UNKNOWN")] += 1
    return {
        "total": len(rows),
        "by_status": dict(status_counts.most_common(10)),
        "by_category": dict(category_counts.most_common(10)),
        "pending": status_counts.get("PENDING_REVIEW", 0),
        "approved": status_counts.get("APPROVED", 0),
    }


def get_content_queue():
    """Parse content queue for pending posts."""
    rows = read_csv(PROJECT_ROOT / "CONTENT" / "social" / "CONTENT_QUEUE.csv")
    status_counts = Counter()
    account_counts = Counter()
    for row in rows:
        st = row.get("status", "UNKNOWN")
        status_counts[st] += 1
        if "PENDING" in st:
            account_counts[row.get("account", "unknown")] += 1
    return {
        "total": len(rows),
        "by_status": dict(status_counts.most_common(10)),
        "pending": sum(v for k, v in status_counts.items() if "PENDING" in k),
        "posted": status_counts.get("POSTED", 0),
        "by_account": dict(account_counts.most_common(10)),
    }


def get_script_health():
    """Check how many Python scripts exist in AUTOMATIONS/."""
    automations_dir = safe_path(PROJECT_ROOT / "AUTOMATIONS")
    py_files = list(automations_dir.glob("*.py"))
    total = len(py_files)
    # Quick syntax check on each
    valid = 0
    broken = []
    for f in py_files:
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                source = fh.read()
            compile(source, str(f), "exec")
            valid += 1
        except SyntaxError:
            broken.append(f.name)
    return {"total": total, "valid": valid, "broken": broken}


def get_log_health():
    """Check log freshness."""
    logs_dir = safe_path(PROJECT_ROOT / "AUTOMATIONS" / "logs")
    if not logs_dir.exists():
        return {"total": 0, "fresh": 0, "stale": [], "recent": []}
    now = datetime.now()
    cutoff = now - timedelta(hours=24)
    log_files = list(logs_dir.glob("*.log"))
    fresh = 0
    stale = []
    recent = []
    for lf in log_files:
        try:
            mtime = datetime.fromtimestamp(lf.stat().st_mtime)
            if mtime > cutoff:
                fresh += 1
                recent.append((lf.name, mtime.strftime("%Y-%m-%d %H:%M")))
            else:
                stale.append((lf.name, mtime.strftime("%Y-%m-%d %H:%M")))
        except Exception:
            stale.append((lf.name, "ERROR"))
    recent.sort(key=lambda x: x[1], reverse=True)
    return {"total": len(log_files), "fresh": fresh, "stale": stale[:10], "recent": recent[:10]}


def get_blockers():
    """Read task tracker for active blockers."""
    tracker_path = safe_path(PROJECT_ROOT / "OPS" / "PERSISTENT_TASK_TRACKER.md")
    blockers = []
    if not tracker_path.exists():
        return blockers
    try:
        with open(tracker_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        current_task = ""
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("### T"):
                current_task = stripped.replace("### ", "")
            if "**Status:** BLOCKED" in stripped and current_task:
                blockers.append(current_task)
    except Exception:
        pass
    return blockers[:10]


def get_accounts_status():
    """Count content account directories."""
    social_dir = safe_path(PROJECT_ROOT / "CONTENT" / "social")
    if not social_dir.exists():
        return {"total": 0, "dirs": []}
    dirs = [d.name for d in social_dir.iterdir() if d.is_dir()]
    return {"total": len(dirs), "dirs": sorted(dirs)}


def priority_matrix(revenue, content, ventures, alpha, blockers):
    """Generate WHAT TO DO RIGHT NOW section."""
    actions = []

    # P0: Revenue is zero
    if revenue["month_revenue"] == 0 and revenue["all_time_revenue"] < 500:
        actions.append(("P0 CRITICAL", "Revenue is $0. Deploy something that makes money TODAY.", "Run freelance responder, post on Reddit hiring threads, activate cold outbound"))

    # P0: Blockers exist
    if blockers:
        for b in blockers[:3]:
            actions.append(("P0 BLOCKER", f"Blocked task: {b[:80]}", "Resolve blocker or find workaround"))

    # P1: Content sitting unposted
    if content["pending"] > 20:
        actions.append(("P1 HIGH", f"{content['pending']} posts sitting in PENDING_REVIEW", "Run auto_scheduler.py to generate Buffer CSV, then bulk upload"))

    # P1: Alpha unprocessed
    if alpha["pending"] > 10:
        actions.append(("P1 HIGH", f"{alpha['pending']} alpha entries need review", "Run alpha_auto_processor.py --process-new"))

    # P2: Stale logs
    if ventures["latest_status"] not in ("OK",):
        actions.append(("P2 MEDIUM", f"Venture health: {ventures['latest_status']}", "Check venture map, run health_check_all.py"))

    # P2: Build content
    if content["pending"] < 10:
        actions.append(("P2 MEDIUM", "Content queue is low (< 10 pending)", "Generate new content batch from alpha + session work"))

    # P3: Routine
    actions.append(("P3 ROUTINE", "Run daily scrapers (Twitter + Reddit)", "python3 AUTOMATIONS/daily_twitter_scraper.py --all"))
    actions.append(("P3 ROUTINE", "Check cron health", "python3 AUTOMATIONS/cron_health_checker.py"))

    return actions


def render_dashboard():
    """Render the full ASCII dashboard."""
    now = datetime.now()
    width = 78

    # Gather all data
    revenue = get_revenue_data()
    ventures = get_venture_health()
    alpha = get_alpha_stats()
    content = get_content_queue()
    scripts = get_script_health()
    logs = get_log_health()
    blockers = get_blockers()
    accounts = get_accounts_status()
    actions = priority_matrix(revenue, content, ventures, alpha, blockers)

    def box_top(title=""):
        if title:
            padding = width - 4 - len(title)
            return f"+{'=' * 2} {title} {'=' * max(padding, 1)}+"
        return f"+{'=' * (width - 2)}+"

    def box_bottom():
        return f"+{'=' * (width - 2)}+"

    def box_line(text=""):
        text = str(text)[:width - 4]
        return f"| {text}{' ' * (width - 4 - len(text))} |"

    def box_sep():
        return f"+{'-' * (width - 2)}+"

    lines = []

    # Header
    lines.append(box_top("PRINTMAXX UNIFIED STATUS DASHBOARD"))
    lines.append(box_line(f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}"))
    lines.append(box_line(f"Project: PRINTMAXX_STARTER_KIT"))
    lines.append(box_bottom())
    lines.append("")

    # Revenue
    lines.append(box_top("REVENUE"))
    month_name = now.strftime("%B %Y")
    lines.append(box_line(f"  {month_name}:"))
    lines.append(box_line(f"    Revenue:  ${revenue['month_revenue']:,.2f}"))
    lines.append(box_line(f"    Expenses: ${revenue['month_expenses']:,.2f}"))
    lines.append(box_line(f"    Profit:   ${revenue['month_profit']:,.2f}"))
    lines.append(box_line(f"  All-Time Revenue: ${revenue['all_time_revenue']:,.2f}"))
    if revenue["top_methods"]:
        lines.append(box_sep())
        lines.append(box_line("  Top Methods:"))
        for method, rev in revenue["top_methods"]:
            lines.append(box_line(f"    {method[:40]}: ${rev:,.2f}"))
    lines.append(box_bottom())
    lines.append("")

    # Ventures + Scripts + Content (3-column-ish)
    lines.append(box_top("OPERATIONS SNAPSHOT"))
    lines.append(box_line(f"  Ventures Health:  {ventures['latest_status']} (last: {ventures['latest_time'][:19] if ventures['latest_time'] != 'N/A' else 'N/A'})"))
    lines.append(box_line(f"    OK checks: {ventures['ok_count']}  |  Warnings: {ventures['warn_count']}  |  Total: {ventures['total_checks']}"))
    lines.append(box_sep())
    lines.append(box_line(f"  Scripts:    {scripts['total']} total  |  {scripts['valid']} valid  |  {len(scripts['broken'])} broken"))
    if scripts["broken"]:
        for b in scripts["broken"][:5]:
            lines.append(box_line(f"    BROKEN: {b}"))
    lines.append(box_sep())
    lines.append(box_line(f"  Content Accounts: {accounts['total']} directories"))
    lines.append(box_line(f"  Content Queue:    {content['total']} total  |  {content['pending']} pending  |  {content.get('posted', 0)} posted"))
    if content["by_account"]:
        top3 = list(content["by_account"].items())[:5]
        acct_str = "  ".join(f"{a}({c})" for a, c in top3)
        lines.append(box_line(f"    Pending by acct: {acct_str[:60]}"))
    lines.append(box_sep())
    lines.append(box_line(f"  Alpha Intel:  {alpha['total']} total  |  {alpha['approved']} approved  |  {alpha['pending']} pending review"))
    lines.append(box_sep())
    lines.append(box_line(f"  Logs: {logs['total']} files  |  {logs['fresh']} fresh (24h)  |  {logs['total'] - logs['fresh']} stale"))
    if logs["recent"][:3]:
        lines.append(box_line("    Most recent:"))
        for name, ts in logs["recent"][:3]:
            lines.append(box_line(f"      {name}: {ts}"))
    lines.append(box_bottom())
    lines.append("")

    # Blockers
    if blockers:
        lines.append(box_top("ACTIVE BLOCKERS"))
        for b in blockers:
            lines.append(box_line(f"  [!] {b[:70]}"))
        lines.append(box_bottom())
        lines.append("")

    # WHAT TO DO RIGHT NOW
    lines.append(box_top("WHAT TO DO RIGHT NOW"))
    if not actions:
        lines.append(box_line("  All systems nominal. Keep building."))
    for priority, desc, action in actions:
        marker = "!!!" if "P0" in priority else ">>>" if "P1" in priority else "   "
        lines.append(box_line(f"  {marker} [{priority}]"))
        lines.append(box_line(f"      {desc[:66]}"))
        lines.append(box_line(f"      -> {action[:64]}"))
        lines.append(box_line(""))
    lines.append(box_bottom())

    return "\n".join(lines)


def main():
    try:
        output = render_dashboard()
        print(output)
    except Exception as e:
        print(f"[ERROR] Dashboard generation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
