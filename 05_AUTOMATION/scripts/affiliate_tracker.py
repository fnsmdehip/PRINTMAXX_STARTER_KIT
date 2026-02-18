#!/usr/bin/env python3
"""
Affiliate Tracker

Track affiliate signups, monitor conversions, calculate payouts, and generate reports.
Reads from and writes to LEDGER/AFFILIATES_MASTER.csv.

Usage:
    python affiliate_tracker.py --action list
    python affiliate_tracker.py --action add --name "John Doe" --email "john@example.com" --platform tiktok --handle "@johndoe" --followers 15000 --niche fitness
    python affiliate_tracker.py --action update --affiliate-id AFF001 --clicks 100 --signups 20 --sales 8
    python affiliate_tracker.py --action payout --affiliate-id AFF001 --amount 150.00
    python affiliate_tracker.py --action report --type summary
    python affiliate_tracker.py --action report --type top-performers
    python affiliate_tracker.py --action report --type payout-due
    python affiliate_tracker.py --action report --type inactive
"""

import argparse
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Configuration
LEDGER_DIR = Path(__file__).parent.parent / "LEDGER"
AFFILIATES_CSV = LEDGER_DIR / "AFFILIATES_MASTER.csv"
PAYOUT_THRESHOLD = 25.00  # Minimum payout amount
INACTIVE_DAYS = 30  # Days without activity to flag as inactive

# CSV field names
FIELDS = [
    "affiliate_id",
    "name",
    "email",
    "platform",
    "handle",
    "followers",
    "niche",
    "status",
    "commission_rate",
    "promo_code",
    "signup_date",
    "last_active",
    "total_clicks",
    "total_signups",
    "total_sales",
    "revenue_generated",
    "total_commission",
    "total_paid",
    "notes",
]


def read_affiliates() -> list[dict]:
    """Read all affiliates from CSV."""
    if not AFFILIATES_CSV.exists():
        return []

    with open(AFFILIATES_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_affiliates(affiliates: list[dict]) -> None:
    """Write affiliates to CSV."""
    with open(AFFILIATES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(affiliates)


def generate_affiliate_id(affiliates: list[dict]) -> str:
    """Generate next affiliate ID."""
    if not affiliates:
        return "AFF001"

    max_id = 0
    for aff in affiliates:
        try:
            num = int(aff["affiliate_id"].replace("AFF", ""))
            max_id = max(max_id, num)
        except (ValueError, KeyError):
            continue

    return f"AFF{max_id + 1:03d}"


def generate_promo_code(name: str) -> str:
    """Generate promo code from name."""
    # Take first name, uppercase, add random suffix
    first_name = name.split()[0].upper()
    return f"{first_name}20"


def list_affiliates(status_filter: Optional[str] = None) -> None:
    """List all affiliates."""
    affiliates = read_affiliates()

    if status_filter:
        affiliates = [a for a in affiliates if a["status"] == status_filter]

    if not affiliates:
        print("No affiliates found.")
        return

    print(f"\n{'ID':<8} {'Name':<20} {'Platform':<12} {'Status':<10} {'Sales':<8} {'Commission':<12}")
    print("-" * 80)

    for aff in affiliates:
        print(
            f"{aff['affiliate_id']:<8} "
            f"{aff['name'][:18]:<20} "
            f"{aff['platform']:<12} "
            f"{aff['status']:<10} "
            f"{aff['total_sales']:<8} "
            f"${float(aff['total_commission']):.2f}"
        )

    print(f"\nTotal: {len(affiliates)} affiliates")


def add_affiliate(
    name: str,
    email: str,
    platform: str,
    handle: str,
    followers: int,
    niche: str,
    commission_rate: float = 0.20,
    notes: str = "",
) -> None:
    """Add a new affiliate."""
    affiliates = read_affiliates()

    # Check for duplicate email
    for aff in affiliates:
        if aff["email"].lower() == email.lower():
            print(f"Error: Affiliate with email {email} already exists (ID: {aff['affiliate_id']})")
            return

    affiliate_id = generate_affiliate_id(affiliates)
    promo_code = generate_promo_code(name)
    today = datetime.now().strftime("%Y-%m-%d")

    new_affiliate = {
        "affiliate_id": affiliate_id,
        "name": name,
        "email": email,
        "platform": platform,
        "handle": handle,
        "followers": followers,
        "niche": niche,
        "status": "pending",
        "commission_rate": commission_rate,
        "promo_code": promo_code,
        "signup_date": today,
        "last_active": today,
        "total_clicks": 0,
        "total_signups": 0,
        "total_sales": 0,
        "revenue_generated": 0.00,
        "total_commission": 0.00,
        "total_paid": 0.00,
        "notes": notes,
    }

    affiliates.append(new_affiliate)
    write_affiliates(affiliates)

    print(f"\nAffiliate added successfully!")
    print(f"  ID: {affiliate_id}")
    print(f"  Name: {name}")
    print(f"  Promo Code: {promo_code}")
    print(f"  Commission Rate: {commission_rate * 100:.0f}%")


def update_affiliate(
    affiliate_id: str,
    clicks: Optional[int] = None,
    signups: Optional[int] = None,
    sales: Optional[int] = None,
    revenue: Optional[float] = None,
    status: Optional[str] = None,
    commission_rate: Optional[float] = None,
    notes: Optional[str] = None,
) -> None:
    """Update affiliate stats."""
    affiliates = read_affiliates()

    affiliate = None
    for aff in affiliates:
        if aff["affiliate_id"] == affiliate_id:
            affiliate = aff
            break

    if not affiliate:
        print(f"Error: Affiliate {affiliate_id} not found.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    updated_fields = []

    if clicks is not None:
        affiliate["total_clicks"] = int(affiliate.get("total_clicks", 0)) + clicks
        updated_fields.append(f"clicks +{clicks}")

    if signups is not None:
        affiliate["total_signups"] = int(affiliate.get("total_signups", 0)) + signups
        updated_fields.append(f"signups +{signups}")

    if sales is not None:
        affiliate["total_sales"] = int(affiliate.get("total_sales", 0)) + sales
        updated_fields.append(f"sales +{sales}")

    if revenue is not None:
        old_revenue = float(affiliate.get("revenue_generated", 0))
        affiliate["revenue_generated"] = old_revenue + revenue

        # Calculate commission
        rate = float(affiliate.get("commission_rate", 0.20))
        commission = revenue * rate
        old_commission = float(affiliate.get("total_commission", 0))
        affiliate["total_commission"] = old_commission + commission

        updated_fields.append(f"revenue +${revenue:.2f}, commission +${commission:.2f}")

    if status is not None:
        affiliate["status"] = status
        updated_fields.append(f"status -> {status}")

    if commission_rate is not None:
        affiliate["commission_rate"] = commission_rate
        updated_fields.append(f"rate -> {commission_rate * 100:.0f}%")

    if notes is not None:
        affiliate["notes"] = notes
        updated_fields.append(f"notes updated")

    # Update last active date if any activity
    if clicks or signups or sales or revenue:
        affiliate["last_active"] = today
        if affiliate["status"] == "pending":
            affiliate["status"] = "active"

    write_affiliates(affiliates)

    print(f"\nAffiliate {affiliate_id} ({affiliate['name']}) updated:")
    for field in updated_fields:
        print(f"  - {field}")


def process_payout(affiliate_id: str, amount: float) -> None:
    """Record a payout to an affiliate."""
    affiliates = read_affiliates()

    affiliate = None
    for aff in affiliates:
        if aff["affiliate_id"] == affiliate_id:
            affiliate = aff
            break

    if not affiliate:
        print(f"Error: Affiliate {affiliate_id} not found.")
        return

    owed = float(affiliate.get("total_commission", 0)) - float(affiliate.get("total_paid", 0))

    if amount > owed:
        print(f"Warning: Paying ${amount:.2f} but only ${owed:.2f} is owed.")
        confirm = input("Continue? (y/n): ")
        if confirm.lower() != "y":
            print("Payout cancelled.")
            return

    affiliate["total_paid"] = float(affiliate.get("total_paid", 0)) + amount
    write_affiliates(affiliates)

    new_owed = float(affiliate["total_commission"]) - float(affiliate["total_paid"])

    print(f"\nPayout recorded:")
    print(f"  Affiliate: {affiliate['name']} ({affiliate_id})")
    print(f"  Amount Paid: ${amount:.2f}")
    print(f"  Remaining Balance: ${new_owed:.2f}")


def generate_report(report_type: str) -> None:
    """Generate various reports."""
    affiliates = read_affiliates()

    if not affiliates:
        print("No affiliates to report on.")
        return

    if report_type == "summary":
        generate_summary_report(affiliates)
    elif report_type == "top-performers":
        generate_top_performers_report(affiliates)
    elif report_type == "payout-due":
        generate_payout_due_report(affiliates)
    elif report_type == "inactive":
        generate_inactive_report(affiliates)
    elif report_type == "niche":
        generate_niche_report(affiliates)
    elif report_type == "platform":
        generate_platform_report(affiliates)
    else:
        print(f"Unknown report type: {report_type}")
        print("Available types: summary, top-performers, payout-due, inactive, niche, platform")


def generate_summary_report(affiliates: list[dict]) -> None:
    """Generate overall summary report."""
    total_affiliates = len(affiliates)
    active = sum(1 for a in affiliates if a["status"] == "active")
    pending = sum(1 for a in affiliates if a["status"] == "pending")
    inactive = sum(1 for a in affiliates if a["status"] == "inactive")

    total_clicks = sum(int(a.get("total_clicks", 0)) for a in affiliates)
    total_signups = sum(int(a.get("total_signups", 0)) for a in affiliates)
    total_sales = sum(int(a.get("total_sales", 0)) for a in affiliates)
    total_revenue = sum(float(a.get("revenue_generated", 0)) for a in affiliates)
    total_commission = sum(float(a.get("total_commission", 0)) for a in affiliates)
    total_paid = sum(float(a.get("total_paid", 0)) for a in affiliates)
    total_owed = total_commission - total_paid

    print("\n" + "=" * 60)
    print("AFFILIATE PROGRAM SUMMARY")
    print("=" * 60)

    print(f"\nAffiliates:")
    print(f"  Total: {total_affiliates}")
    print(f"  Active: {active}")
    print(f"  Pending: {pending}")
    print(f"  Inactive: {inactive}")

    print(f"\nPerformance:")
    print(f"  Total Clicks: {total_clicks:,}")
    print(f"  Total Signups: {total_signups:,}")
    print(f"  Total Sales: {total_sales:,}")

    if total_clicks > 0:
        print(f"  Click-to-Signup Rate: {total_signups / total_clicks * 100:.1f}%")
    if total_signups > 0:
        print(f"  Signup-to-Sale Rate: {total_sales / total_signups * 100:.1f}%")

    print(f"\nFinancials:")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Total Commission: ${total_commission:,.2f}")
    print(f"  Already Paid: ${total_paid:,.2f}")
    print(f"  Outstanding: ${total_owed:,.2f}")

    if total_affiliates > 0:
        print(f"\nAverages per Affiliate:")
        print(f"  Avg Revenue: ${total_revenue / total_affiliates:,.2f}")
        print(f"  Avg Commission: ${total_commission / total_affiliates:,.2f}")
        print(f"  Avg Sales: {total_sales / total_affiliates:.1f}")


def generate_top_performers_report(affiliates: list[dict], limit: int = 10) -> None:
    """Generate top performers report."""
    # Sort by revenue generated
    sorted_affiliates = sorted(
        affiliates,
        key=lambda x: float(x.get("revenue_generated", 0)),
        reverse=True,
    )[:limit]

    print("\n" + "=" * 60)
    print(f"TOP {limit} PERFORMERS BY REVENUE")
    print("=" * 60)

    print(f"\n{'Rank':<6} {'Name':<20} {'Platform':<12} {'Sales':<8} {'Revenue':<12} {'Commission':<12}")
    print("-" * 80)

    for i, aff in enumerate(sorted_affiliates, 1):
        revenue = float(aff.get("revenue_generated", 0))
        commission = float(aff.get("total_commission", 0))

        if revenue == 0:
            continue

        print(
            f"{i:<6} "
            f"{aff['name'][:18]:<20} "
            f"{aff['platform']:<12} "
            f"{aff['total_sales']:<8} "
            f"${revenue:>10,.2f} "
            f"${commission:>10,.2f}"
        )


def generate_payout_due_report(affiliates: list[dict]) -> None:
    """Generate report of affiliates with payouts due."""
    payout_due = []

    for aff in affiliates:
        commission = float(aff.get("total_commission", 0))
        paid = float(aff.get("total_paid", 0))
        owed = commission - paid

        if owed >= PAYOUT_THRESHOLD:
            payout_due.append({**aff, "owed": owed})

    # Sort by amount owed
    payout_due.sort(key=lambda x: x["owed"], reverse=True)

    print("\n" + "=" * 60)
    print(f"PAYOUTS DUE (threshold: ${PAYOUT_THRESHOLD:.2f})")
    print("=" * 60)

    if not payout_due:
        print("\nNo payouts currently due.")
        return

    total_owed = sum(a["owed"] for a in payout_due)

    print(f"\n{'ID':<8} {'Name':<20} {'Email':<25} {'Amount Due':<12}")
    print("-" * 70)

    for aff in payout_due:
        print(
            f"{aff['affiliate_id']:<8} "
            f"{aff['name'][:18]:<20} "
            f"{aff['email'][:23]:<25} "
            f"${aff['owed']:>10,.2f}"
        )

    print("-" * 70)
    print(f"{'TOTAL':<8} {'':<20} {'':<25} ${total_owed:>10,.2f}")
    print(f"\n{len(payout_due)} affiliates with payouts due.")


def generate_inactive_report(affiliates: list[dict]) -> None:
    """Generate report of inactive affiliates."""
    today = datetime.now()
    inactive_threshold = today - timedelta(days=INACTIVE_DAYS)

    inactive_affiliates = []

    for aff in affiliates:
        if aff["status"] == "inactive":
            inactive_affiliates.append(aff)
            continue

        try:
            last_active = datetime.strptime(aff["last_active"], "%Y-%m-%d")
            if last_active < inactive_threshold:
                inactive_affiliates.append(aff)
        except (ValueError, KeyError):
            continue

    print("\n" + "=" * 60)
    print(f"INACTIVE AFFILIATES (no activity in {INACTIVE_DAYS} days)")
    print("=" * 60)

    if not inactive_affiliates:
        print("\nNo inactive affiliates found.")
        return

    print(f"\n{'ID':<8} {'Name':<20} {'Last Active':<15} {'Total Sales':<12}")
    print("-" * 60)

    for aff in inactive_affiliates:
        print(
            f"{aff['affiliate_id']:<8} "
            f"{aff['name'][:18]:<20} "
            f"{aff['last_active']:<15} "
            f"{aff['total_sales']:<12}"
        )

    print(f"\n{len(inactive_affiliates)} inactive affiliates.")
    print("Consider: re-engagement email or removal from program.")


def generate_niche_report(affiliates: list[dict]) -> None:
    """Generate performance report by niche."""
    niches = {}

    for aff in affiliates:
        niche = aff.get("niche", "unknown")
        if niche not in niches:
            niches[niche] = {
                "count": 0,
                "revenue": 0,
                "sales": 0,
                "active": 0,
            }

        niches[niche]["count"] += 1
        niches[niche]["revenue"] += float(aff.get("revenue_generated", 0))
        niches[niche]["sales"] += int(aff.get("total_sales", 0))
        if aff["status"] == "active":
            niches[niche]["active"] += 1

    print("\n" + "=" * 60)
    print("PERFORMANCE BY NICHE")
    print("=" * 60)

    print(f"\n{'Niche':<15} {'Affiliates':<12} {'Active':<10} {'Sales':<10} {'Revenue':<15}")
    print("-" * 65)

    for niche, data in sorted(niches.items(), key=lambda x: x[1]["revenue"], reverse=True):
        print(
            f"{niche:<15} "
            f"{data['count']:<12} "
            f"{data['active']:<10} "
            f"{data['sales']:<10} "
            f"${data['revenue']:>12,.2f}"
        )


def generate_platform_report(affiliates: list[dict]) -> None:
    """Generate performance report by platform."""
    platforms = {}

    for aff in affiliates:
        platform = aff.get("platform", "unknown")
        if platform not in platforms:
            platforms[platform] = {
                "count": 0,
                "revenue": 0,
                "sales": 0,
                "clicks": 0,
            }

        platforms[platform]["count"] += 1
        platforms[platform]["revenue"] += float(aff.get("revenue_generated", 0))
        platforms[platform]["sales"] += int(aff.get("total_sales", 0))
        platforms[platform]["clicks"] += int(aff.get("total_clicks", 0))

    print("\n" + "=" * 60)
    print("PERFORMANCE BY PLATFORM")
    print("=" * 60)

    print(f"\n{'Platform':<12} {'Affiliates':<12} {'Clicks':<12} {'Sales':<10} {'Revenue':<15}")
    print("-" * 65)

    for platform, data in sorted(platforms.items(), key=lambda x: x[1]["revenue"], reverse=True):
        print(
            f"{platform:<12} "
            f"{data['count']:<12} "
            f"{data['clicks']:<12} "
            f"{data['sales']:<10} "
            f"${data['revenue']:>12,.2f}"
        )


def flag_inactive_affiliates() -> None:
    """Flag affiliates as inactive if no activity in INACTIVE_DAYS."""
    affiliates = read_affiliates()
    today = datetime.now()
    inactive_threshold = today - timedelta(days=INACTIVE_DAYS)

    flagged = 0

    for aff in affiliates:
        if aff["status"] not in ["active", "pending"]:
            continue

        try:
            last_active = datetime.strptime(aff["last_active"], "%Y-%m-%d")
            if last_active < inactive_threshold:
                aff["status"] = "inactive"
                flagged += 1
        except (ValueError, KeyError):
            continue

    if flagged > 0:
        write_affiliates(affiliates)
        print(f"Flagged {flagged} affiliates as inactive.")
    else:
        print("No affiliates to flag.")


def main():
    parser = argparse.ArgumentParser(
        description="Affiliate tracking and management system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--action",
        "-a",
        required=True,
        choices=["list", "add", "update", "payout", "report", "flag-inactive"],
        help="Action to perform",
    )

    # Add affiliate args
    parser.add_argument("--name", help="Affiliate name")
    parser.add_argument("--email", help="Affiliate email")
    parser.add_argument("--platform", help="Platform (tiktok, instagram, youtube, blog)")
    parser.add_argument("--handle", help="Social media handle")
    parser.add_argument("--followers", type=int, help="Follower count")
    parser.add_argument("--niche", help="Content niche (faith, fitness, ai)")
    parser.add_argument("--commission-rate", type=float, help="Commission rate (0.20 = 20%)")
    parser.add_argument("--notes", help="Notes about affiliate")

    # Update args
    parser.add_argument("--affiliate-id", help="Affiliate ID (e.g., AFF001)")
    parser.add_argument("--clicks", type=int, help="Add clicks")
    parser.add_argument("--signups", type=int, help="Add signups")
    parser.add_argument("--sales", type=int, help="Add sales")
    parser.add_argument("--revenue", type=float, help="Add revenue")
    parser.add_argument("--status", help="Set status (active, inactive, pending)")

    # Payout args
    parser.add_argument("--amount", type=float, help="Payout amount")

    # Report args
    parser.add_argument(
        "--type",
        dest="report_type",
        help="Report type (summary, top-performers, payout-due, inactive, niche, platform)",
    )

    # List filter
    parser.add_argument("--filter", help="Filter list by status")

    args = parser.parse_args()

    if args.action == "list":
        list_affiliates(status_filter=args.filter)

    elif args.action == "add":
        if not all([args.name, args.email, args.platform, args.handle, args.followers, args.niche]):
            print("Error: --name, --email, --platform, --handle, --followers, and --niche are required for add")
            return

        add_affiliate(
            name=args.name,
            email=args.email,
            platform=args.platform,
            handle=args.handle,
            followers=args.followers,
            niche=args.niche,
            commission_rate=args.commission_rate or 0.20,
            notes=args.notes or "",
        )

    elif args.action == "update":
        if not args.affiliate_id:
            print("Error: --affiliate-id is required for update")
            return

        update_affiliate(
            affiliate_id=args.affiliate_id,
            clicks=args.clicks,
            signups=args.signups,
            sales=args.sales,
            revenue=args.revenue,
            status=args.status,
            commission_rate=args.commission_rate,
            notes=args.notes,
        )

    elif args.action == "payout":
        if not args.affiliate_id or args.amount is None:
            print("Error: --affiliate-id and --amount are required for payout")
            return

        process_payout(affiliate_id=args.affiliate_id, amount=args.amount)

    elif args.action == "report":
        if not args.report_type:
            print("Error: --type is required for report")
            print("Available: summary, top-performers, payout-due, inactive, niche, platform")
            return

        generate_report(args.report_type)

    elif args.action == "flag-inactive":
        flag_inactive_affiliates()


if __name__ == "__main__":
    main()
