#!/usr/bin/env python3
"""Cold email response tracker. Reads cold_emails_ready.csv, tracks campaign status,
shows dashboard metrics, flags overdue follow-ups, exports for CRM."""

import argparse
import csv
import io
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COLD_EMAILS_CSV = BASE_DIR / "output" / "cold_emails" / "cold_emails_ready.csv"
TRACKER_DIR = BASE_DIR / "AUTOMATIONS" / "leads" / "qualified"
TRACKER_CSV = TRACKER_DIR / "campaign_tracker.csv"

STATUSES = ["QUEUED", "SENT", "OPENED", "REPLIED", "BOOKED", "CLOSED", "BOUNCED", "UNSUBSCRIBED"]
TRACKER_FIELDS = [
    "email_id", "to_email", "business_name", "city", "industry", "website",
    "demo_url", "lead_score", "status", "deal_value", "sent_at", "opened_at",
    "replied_at", "booked_at", "closed_at", "followup_1_due", "followup_2_due",
    "followup_1_sent", "followup_2_sent", "notes",
]


def parse_multiline_csv(filepath: Path) -> list[dict]:
    """Parse CSV with multiline quoted fields."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        if row.get("to_email") and "@" in row["to_email"]:
            rows.append(row)
    return rows


def load_tracker() -> list[dict]:
    if not TRACKER_CSV.exists():
        return []
    with open(TRACKER_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_tracker(rows: list[dict]):
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def cmd_init(args):
    """Import cold emails into the tracker."""
    if TRACKER_CSV.exists() and not args.force:
        existing = load_tracker()
        print(f"Tracker already exists with {len(existing)} records.")
        print("Use --force to overwrite.")
        return

    if not COLD_EMAILS_CSV.exists():
        print(f"ERROR: cold emails file not found at {COLD_EMAILS_CSV}")
        sys.exit(1)

    emails = parse_multiline_csv(COLD_EMAILS_CSV)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    seen, rows = set(), []
    copy_fields = ["to_email", "business_name", "city", "industry", "website", "demo_url", "lead_score"]
    for i, e in enumerate(emails, 1):
        addr = e.get("to_email", "").strip()
        if not addr or addr in seen:
            continue
        seen.add(addr)
        row = {f: "" for f in TRACKER_FIELDS}
        row.update({f: e.get(f, "") for f in copy_fields})
        row.update({"email_id": f"CE-{i:05d}", "status": "QUEUED", "notes": f"imported {now_str}"})
        rows.append(row)

    save_tracker(rows)
    print(f"Initialized tracker: {len(rows)} unique emails imported from {len(emails)} records.")
    print(f"Saved to: {TRACKER_CSV}")
    _print_status_summary(rows)


def cmd_log(args):
    """Log a status change for an email."""
    rows = load_tracker()
    if not rows:
        print("ERROR: tracker is empty. Run --init first.")
        sys.exit(1)

    target = args.email.lower()
    matches = [r for r in rows if r["to_email"].lower() == target or r["email_id"].lower() == target]
    if not matches:
        print(f"ERROR: no match for '{args.email}'. Use email address or email_id (CE-XXXXX).")
        sys.exit(1)

    new_status = args.status.upper()
    if new_status not in STATUSES:
        print(f"ERROR: invalid status '{new_status}'. Must be one of: {', '.join(STATUSES)}")
        sys.exit(1)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    ts_map = {"SENT": "sent_at", "OPENED": "opened_at", "REPLIED": "replied_at",
              "BOOKED": "booked_at", "CLOSED": "closed_at"}

    for row in matches:
        row["status"] = new_status
        if new_status in ts_map:
            row[ts_map[new_status]] = now_str
        if new_status == "SENT" and not row["followup_1_due"]:
            fu1 = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            fu2 = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            row["followup_1_due"] = fu1
            row["followup_2_due"] = fu2
        if args.value:
            row["deal_value"] = str(args.value)
        if args.notes:
            row["notes"] = args.notes
        print(f"  {row['email_id']} ({row['to_email']}) -> {new_status}")

    save_tracker(rows)
    print(f"Updated {len(matches)} record(s).")


def cmd_dashboard(args):
    """Show campaign metrics dashboard."""
    rows = load_tracker()
    if not rows:
        print("ERROR: tracker is empty. Run --init first.")
        return

    total = len(rows)
    counts = {}
    for s in STATUSES:
        counts[s] = sum(1 for r in rows if r["status"] == s)

    sent_plus = total - counts.get("QUEUED", 0)
    opened = counts.get("OPENED", 0) + counts.get("REPLIED", 0) + counts.get("BOOKED", 0) + counts.get("CLOSED", 0)
    replied = counts.get("REPLIED", 0) + counts.get("BOOKED", 0) + counts.get("CLOSED", 0)
    booked = counts.get("BOOKED", 0) + counts.get("CLOSED", 0)
    closed = counts.get("CLOSED", 0)

    def pct(num, denom):
        return f"{(num / denom * 100):.1f}%" if denom > 0 else "0.0%"

    total_revenue = sum(float(r["deal_value"] or 0) for r in rows if r["status"] == "CLOSED")
    pipeline_val = sum(float(r["deal_value"] or 0) for r in rows if r["status"] in ("REPLIED", "BOOKED"))
    rev_per_email = total_revenue / sent_plus if sent_plus > 0 else 0

    w = 52
    print("\n" + "=" * w)
    print("  COLD EMAIL CAMPAIGN DASHBOARD")
    print("=" * w)
    print(f"  Total emails:        {total:>6}")
    print(f"  Queued:              {counts.get('QUEUED', 0):>6}")
    print(f"  Sent:                {sent_plus:>6}")
    print(f"  Bounced:             {counts.get('BOUNCED', 0):>6}")
    print(f"  Unsubscribed:        {counts.get('UNSUBSCRIBED', 0):>6}")
    print("-" * w)
    print("  FUNNEL METRICS")
    print("-" * w)
    print(f"  Open rate:           {pct(opened, sent_plus):>6}  ({opened}/{sent_plus})")
    print(f"  Reply rate:          {pct(replied, sent_plus):>6}  ({replied}/{sent_plus})")
    print(f"  Book rate:           {pct(booked, sent_plus):>6}  ({booked}/{sent_plus})")
    print(f"  Close rate:          {pct(closed, sent_plus):>6}  ({closed}/{sent_plus})")
    print("-" * w)
    print("  REVENUE")
    print("-" * w)
    print(f"  Closed revenue:      ${total_revenue:>10,.2f}")
    print(f"  Pipeline value:      ${pipeline_val:>10,.2f}")
    print(f"  Revenue per email:   ${rev_per_email:>10,.2f}")
    print("-" * w)
    print("  STATUS BREAKDOWN")
    print("-" * w)
    bar_max = 30
    for s in STATUSES:
        c = counts.get(s, 0)
        bar_len = int(c / total * bar_max) if total > 0 else 0
        bar = "#" * bar_len
        print(f"  {s:<14} {c:>5}  {bar}")
    print("=" * w)

    for flag, key, label in [(args.by_city, "city", "BY CITY"), (args.by_industry, "industry", "BY INDUSTRY")]:
        if not flag:
            continue
        groups = {}
        for r in rows:
            g = r.get(key, "unknown") or "unknown"
            groups.setdefault(g, {"total": 0, "replied": 0, "closed": 0, "revenue": 0})
            groups[g]["total"] += 1
            if r["status"] in ("REPLIED", "BOOKED", "CLOSED"):
                groups[g]["replied"] += 1
            if r["status"] == "CLOSED":
                groups[g]["closed"] += 1
                groups[g]["revenue"] += float(r["deal_value"] or 0)
        print(f"\n  {label}:")
        print(f"  {'Name':<22} {'Total':>6} {'Replied':>8} {'Closed':>7} {'Revenue':>10}")
        for name in sorted(groups, key=lambda x: groups[x]["replied"], reverse=True):
            d = groups[name]
            print(f"  {name:<22} {d['total']:>6} {d['replied']:>8} {d['closed']:>7} ${d['revenue']:>9,.0f}")


def cmd_followups(args):
    """Show overdue follow-ups."""
    rows = load_tracker()
    if not rows:
        print("ERROR: tracker is empty. Run --init first.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    overdue_1, overdue_2 = [], []

    for r in rows:
        if r["status"] in ("BOUNCED", "UNSUBSCRIBED", "CLOSED", "QUEUED"):
            continue
        if r["followup_1_due"] and r["followup_1_due"] <= today and r["followup_1_sent"] != "true":
            overdue_1.append(r)
        if r["followup_2_due"] and r["followup_2_due"] <= today and r["followup_2_sent"] != "true":
            if r["followup_1_sent"] == "true":
                overdue_2.append(r)

    print(f"\nOverdue follow-ups as of {today}:")
    print(f"  Follow-up 1 overdue: {len(overdue_1)}")
    print(f"  Follow-up 2 overdue: {len(overdue_2)}")

    for label, items, due_key in [("FOLLOW-UP 1", overdue_1, "followup_1_due"),
                                    ("FOLLOW-UP 2", overdue_2, "followup_2_due")]:
        if not items:
            continue
        print(f"\n  {label} OVERDUE ({len(items)}):")
        print(f"  {'ID':<10} {'Email':<35} {'Business':<25} {'Due':<12}")
        for r in items[:20]:
            print(f"  {r['email_id']:<10} {r['to_email']:<35} {r['business_name'][:24]:<25} {r[due_key]:<12}")
        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more")
    if not overdue_1 and not overdue_2:
        print("  No overdue follow-ups. All caught up.")


def cmd_export(args):
    """Export tracker data for CRM import."""
    rows = load_tracker()
    if not rows:
        print("ERROR: tracker is empty. Run --init first.")
        return

    fmt = args.format
    if args.status_filter:
        filt = args.status_filter.upper()
        rows = [r for r in rows if r["status"] == filt]
        print(f"Filtered to {len(rows)} records with status={filt}")

    out_dir = BASE_DIR / "output" / "crm_exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    if fmt == "csv":
        out_path = out_dir / f"crm_export_{ts}.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    elif fmt == "json":
        out_path = out_dir / f"crm_export_{ts}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
    else:
        print(f"ERROR: unknown format '{fmt}'. Use csv or json.")
        return

    print(f"Exported {len(rows)} records to {out_path}")


def cmd_simulate(args):
    """Generate fake data across statuses for testing."""
    rows = load_tracker()
    if not rows:
        print("ERROR: tracker is empty. Run --init first.")
        return

    n = min(args.count, len(rows))
    sample = random.sample(rows, n)
    now = datetime.now()
    deal_values = [500, 750, 1000, 1500, 2000, 2500, 3000]

    buckets = {"SENT": 0.30, "OPENED": 0.20, "REPLIED": 0.15, "BOOKED": 0.10,
               "CLOSED": 0.05, "BOUNCED": 0.10, "UNSUBSCRIBED": 0.10}
    buckets = {k: int(n * v) for k, v in buckets.items()}
    idx = 0

    for status, count in buckets.items():
        for _ in range(count):
            if idx >= len(sample):
                break
            r = sample[idx]
            days_ago = random.randint(1, 14)
            sent_dt = now - timedelta(days=days_ago)
            r["status"] = status
            r["sent_at"] = sent_dt.strftime("%Y-%m-%d %H:%M")
            r["followup_1_due"] = (sent_dt + timedelta(days=3)).strftime("%Y-%m-%d")
            r["followup_2_due"] = (sent_dt + timedelta(days=7)).strftime("%Y-%m-%d")

            if status in ("OPENED", "REPLIED", "BOOKED", "CLOSED"):
                r["opened_at"] = (sent_dt + timedelta(hours=random.randint(1, 48))).strftime("%Y-%m-%d %H:%M")
            if status in ("REPLIED", "BOOKED", "CLOSED"):
                r["replied_at"] = (sent_dt + timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d %H:%M")
            if status in ("BOOKED", "CLOSED"):
                r["booked_at"] = (sent_dt + timedelta(days=random.randint(2, 5))).strftime("%Y-%m-%d %H:%M")
                r["deal_value"] = str(random.choice(deal_values))
            if status == "CLOSED":
                r["closed_at"] = (sent_dt + timedelta(days=random.randint(5, 10))).strftime("%Y-%m-%d %H:%M")
            if days_ago > 3:
                r["followup_1_sent"] = "true"
            if days_ago > 7:
                r["followup_2_sent"] = "true"
            r["notes"] = f"simulated {now.strftime('%Y-%m-%d %H:%M')}"
            idx += 1

    save_tracker(rows)
    print(f"Simulated {n} records across funnel stages.")
    _print_status_summary(rows)


def _print_status_summary(rows):
    counts = {}
    for r in rows:
        s = r.get("status", "UNKNOWN")
        counts[s] = counts.get(s, 0) + 1
    print("\n  Status breakdown:")
    for s in STATUSES:
        if counts.get(s, 0) > 0:
            print(f"    {s:<16} {counts[s]:>5}")


def main():
    parser = argparse.ArgumentParser(description="Cold email response tracker")
    sub = parser.add_subparsers(dest="command")

    # --init
    p_init = sub.add_parser("init", help="Import cold_emails_ready.csv into tracker")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing tracker")

    # --log
    p_log = sub.add_parser("log", help="Log a response/status change")
    p_log.add_argument("email", help="Email address or email_id (CE-XXXXX)")
    p_log.add_argument("status", help=f"New status: {', '.join(STATUSES)}")
    p_log.add_argument("--value", type=float, help="Deal value in dollars")
    p_log.add_argument("--notes", help="Optional notes")

    # --dashboard
    p_dash = sub.add_parser("dashboard", help="Show campaign metrics")
    p_dash.add_argument("--by-city", action="store_true", help="Break down by city")
    p_dash.add_argument("--by-industry", action="store_true", help="Break down by industry")

    # --followups
    sub.add_parser("followups", help="Show overdue follow-ups")

    # --export
    p_export = sub.add_parser("export", help="Export for CRM import")
    p_export.add_argument("--format", default="csv", choices=["csv", "json"], help="Output format")
    p_export.add_argument("--status-filter", help="Filter by status before export")

    # --simulate
    p_sim = sub.add_parser("simulate", help="Generate fake funnel data for testing")
    p_sim.add_argument("--count", type=int, default=100, help="Number of records to simulate (default 100)")

    args = parser.parse_args()

    commands = {
        "init": cmd_init, "log": cmd_log, "dashboard": cmd_dashboard,
        "followups": cmd_followups, "export": cmd_export, "simulate": cmd_simulate,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 response_tracker.py init                     # Import emails")
        print("  python3 response_tracker.py log user@co.com SENT     # Log status")
        print("  python3 response_tracker.py log CE-00012 REPLIED --value 2500")
        print("  python3 response_tracker.py dashboard --by-industry  # Show metrics")
        print("  python3 response_tracker.py followups                # Overdue follow-ups")
        print("  python3 response_tracker.py export --format json     # CRM export")
        print("  python3 response_tracker.py simulate --count 150     # Test data")


if __name__ == "__main__":
    main()
