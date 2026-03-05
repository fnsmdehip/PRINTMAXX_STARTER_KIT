#!/usr/bin/env python3
"""
PRINTMAXX Ad Budget Tracker
=============================
$20 per marketing run. Kill losers. Scale winners.
Tracks spend, performance, and auto-recommends scale/kill decisions.

Usage:
  python3 ad_budget_tracker.py --add                    # Log a new ad run
  python3 ad_budget_tracker.py --status                 # View all runs + recommendations
  python3 ad_budget_tracker.py --log ID --impressions N --clicks N --conversions N  # Update metrics
  python3 ad_budget_tracker.py --winners                # Show winners to scale
  python3 ad_budget_tracker.py --kill                   # Show losers to kill
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
TRACKER = LEDGER / "AD_BUDGET_TRACKER.csv"
FIELDNAMES = [
    "run_id", "date", "platform", "content_type", "target_audience",
    "spend", "impressions", "clicks", "ctr", "conversions", "cpa",
    "revenue", "roas", "status", "action", "notes"
]


def ensure_tracker():
    if not TRACKER.exists():
        with open(TRACKER, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_runs():
    ensure_tracker()
    with open(TRACKER, "r") as f:
        return list(csv.DictReader(f))


def write_runs(runs):
    with open(TRACKER, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in runs:
            writer.writerow(r)


def safe_float(v, default=0.0):
    try:
        return float(str(v).replace("$", "").replace(",", ""))
    except (ValueError, TypeError):
        return default


def next_id(runs):
    max_id = 0
    for r in runs:
        try:
            num = int(r.get("run_id", "AD0").replace("AD", ""))
            if num > max_id:
                max_id = num
        except ValueError:
            pass
    return f"AD{max_id + 1:03d}"


def score_run(r):
    """Score a run 0-100 for rebalancer integration."""
    spend = safe_float(r.get("spend"))
    clicks = safe_float(r.get("clicks"))
    conversions = safe_float(r.get("conversions"))
    revenue = safe_float(r.get("revenue"))
    impressions = safe_float(r.get("impressions"))

    if spend <= 0:
        return 50  # No data

    score = 0

    # CTR component (0-30 points)
    if impressions > 0:
        ctr = clicks / impressions * 100
        if ctr >= 3.0:
            score += 30
        elif ctr >= 1.5:
            score += 20
        elif ctr >= 0.5:
            score += 10

    # Conversion rate (0-30 points)
    if clicks > 0:
        conv_rate = conversions / clicks * 100
        if conv_rate >= 5.0:
            score += 30
        elif conv_rate >= 2.0:
            score += 20
        elif conv_rate >= 0.5:
            score += 10

    # ROAS component (0-40 points)
    roas = revenue / spend if spend > 0 else 0
    if roas >= 3.0:
        score += 40
    elif roas >= 1.5:
        score += 30
    elif roas >= 1.0:
        score += 20
    elif roas >= 0.5:
        score += 10

    return min(100, score)


def recommend_action(score):
    if score >= 70:
        return "SCALE_5X"
    elif score >= 50:
        return "SCALE_2X"
    elif score >= 30:
        return "MAINTAIN"
    elif score >= 15:
        return "REDUCE"
    else:
        return "KILL"


def cmd_add():
    runs = read_runs()
    rid = next_id(runs)

    print(f"\nNew Ad Run: {rid}")
    platform = input("Platform (twitter/tiktok/meta/google/other): ").strip() or "twitter"
    content_type = input("Content type (tweet/reel/story/post/ad): ").strip() or "tweet"
    target = input("Target audience (brief description): ").strip() or "general"
    spend = input("Spend amount [$20]: ").strip() or "20"
    notes = input("Notes: ").strip()

    run = {
        "run_id": rid,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "platform": platform,
        "content_type": content_type,
        "target_audience": target,
        "spend": spend,
        "impressions": "0",
        "clicks": "0",
        "ctr": "0",
        "conversions": "0",
        "cpa": "0",
        "revenue": "0",
        "roas": "0",
        "status": "ACTIVE",
        "action": "PENDING",
        "notes": notes,
    }
    runs.append(run)
    write_runs(runs)
    print(f"\nLogged {rid}: ${spend} on {platform} ({content_type})")
    print(f"Update metrics later: python3 ad_budget_tracker.py --log {rid} --impressions N --clicks N --conversions N")


def cmd_log(run_id, impressions, clicks, conversions, revenue=0):
    runs = read_runs()
    found = False
    for r in runs:
        if r["run_id"] == run_id:
            r["impressions"] = str(impressions)
            r["clicks"] = str(clicks)
            r["conversions"] = str(conversions)
            r["revenue"] = str(revenue)

            imp = safe_float(impressions)
            clk = safe_float(clicks)
            spd = safe_float(r["spend"])

            r["ctr"] = f"{clk / imp * 100:.2f}" if imp > 0 else "0"
            r["cpa"] = f"{spd / safe_float(conversions):.2f}" if safe_float(conversions) > 0 else "N/A"
            r["roas"] = f"{safe_float(revenue) / spd:.2f}" if spd > 0 else "0"

            score = score_run(r)
            r["action"] = recommend_action(score)
            r["status"] = "MEASURED"
            found = True
            print(f"Updated {run_id}: {impressions} imp, {clicks} clicks, {conversions} conv")
            print(f"Score: {score}/100 -> Action: {r['action']}")
            break

    if not found:
        print(f"Run {run_id} not found")
        return

    write_runs(runs)


def cmd_status():
    runs = read_runs()
    if not runs:
        print("No ad runs yet. Use --add to log one.")
        return

    total_spend = sum(safe_float(r.get("spend")) for r in runs)
    total_revenue = sum(safe_float(r.get("revenue")) for r in runs)

    print("=" * 75)
    print(f"PRINTMAXX AD BUDGET TRACKER -- {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 75)
    print()
    print(f"{'ID':<8} {'DATE':<12} {'PLATFORM':<10} {'SPEND':>7} {'IMP':>8} {'CLICKS':>7} {'CTR':>6} {'CONV':>5} {'ROAS':>6} {'ACTION':<10}")
    print("-" * 75)

    for r in runs:
        score = score_run(r)
        action = recommend_action(score)
        tag = ""
        if action == "KILL":
            tag = " !!!"
        elif "SCALE" in action:
            tag = " +++"

        print(
            f"{r['run_id']:<8} {r['date']:<12} {r['platform']:<10} "
            f"${safe_float(r['spend']):>6.0f} {safe_float(r['impressions']):>8.0f} "
            f"{safe_float(r['clicks']):>7.0f} {r.get('ctr', '0'):>5}% "
            f"{safe_float(r['conversions']):>5.0f} {r.get('roas', '0'):>5}x "
            f"{action:<10}{tag}"
        )

    print("-" * 75)
    print(f"TOTAL: ${total_spend:.0f} spent | ${total_revenue:.0f} revenue | "
          f"ROAS: {total_revenue / total_spend:.2f}x" if total_spend > 0 else "TOTAL: $0 spent")
    print()


def cmd_winners():
    runs = read_runs()
    winners = [r for r in runs if score_run(r) >= 50]
    if not winners:
        print("No winners yet. Need more data or better ads.")
        return

    print("WINNERS (Scale these):")
    for r in winners:
        score = score_run(r)
        action = recommend_action(score)
        next_budget = safe_float(r["spend"]) * (5 if score >= 70 else 2)
        print(f"  {r['run_id']} | {r['platform']} | Score {score} | {action} | Next budget: ${next_budget:.0f}")


def cmd_kill():
    runs = read_runs()
    losers = [r for r in runs if score_run(r) < 30 and r.get("status") == "MEASURED"]
    if not losers:
        print("No losers to kill. Either too early or ads are performing.")
        return

    print("KILL THESE (Stop spending):")
    for r in losers:
        score = score_run(r)
        print(f"  {r['run_id']} | {r['platform']} | Score {score} | "
              f"Spent ${safe_float(r['spend']):.0f} | "
              f"CTR {r.get('ctr', '0')}% | ROAS {r.get('roas', '0')}x")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="PRINTMAXX Ad Budget Tracker")
    p.add_argument("--add", action="store_true", help="Log new ad run")
    p.add_argument("--status", action="store_true", help="View all runs")
    p.add_argument("--log", metavar="ID", help="Update metrics for a run")
    p.add_argument("--impressions", type=int, default=0)
    p.add_argument("--clicks", type=int, default=0)
    p.add_argument("--conversions", type=int, default=0)
    p.add_argument("--revenue", type=float, default=0)
    p.add_argument("--winners", action="store_true", help="Show winners to scale")
    p.add_argument("--kill", action="store_true", help="Show losers to kill")
    args = p.parse_args()

    if args.add:
        cmd_add()
    elif args.log:
        cmd_log(args.log, args.impressions, args.clicks, args.conversions, args.revenue)
    elif args.winners:
        cmd_winners()
    elif args.kill:
        cmd_kill()
    else:
        cmd_status()
