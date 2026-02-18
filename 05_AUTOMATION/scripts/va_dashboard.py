#!/usr/bin/env python3
"""
VA Performance Dashboard

Track VA performance, calculate ROI, and generate weekly reports.

Usage:
    python va_dashboard.py                    # Show current dashboard
    python va_dashboard.py --update VA001    # Update VA stats interactively
    python va_dashboard.py --report          # Generate weekly report
    python va_dashboard.py --export          # Export report to markdown
"""

import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import argparse

# Configuration
BASE_DIR = Path(__file__).parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
VA_TRACKING_FILE = LEDGER_DIR / "VA_TRACKING.csv"
REPORTS_DIR = BASE_DIR / "OPS" / "logs" / "va_reports"

# Bonus structures by task type
BONUS_STRUCTURE = {
    "church_outreach": {
        "positive_response": 10.00,
        "call_booked": 25.00,
        "conversion": 50.00,
    },
    "gym_outreach": {
        "positive_response": 15.00,
        "call_booked": 30.00,
        "conversion": 75.00,
    },
    "school_outreach": {
        "positive_response": 20.00,
        "call_booked": 40.00,
        "conversion": 100.00,
    },
    "affiliate_recruitment": {
        "positive_response": 5.00,
        "call_booked": 10.00,
        "conversion": 25.00,
    },
}

# Conversion values (what a conversion is worth to us)
CONVERSION_VALUES = {
    "church_outreach": 400.00,  # Annual value of church partnership
    "gym_outreach": 300.00,     # Annual value of gym partnership
    "school_outreach": 500.00,  # Annual value of school partnership
    "affiliate_recruitment": 150.00,  # Annual value of active affiliate
}


class VATracker:
    """Track and analyze VA performance."""

    def __init__(self, csv_path: Path = VA_TRACKING_FILE):
        self.csv_path = csv_path
        self.vas = self._load_vas()

    def _load_vas(self) -> list[dict]:
        """Load VA data from CSV."""
        if not self.csv_path.exists():
            print(f"Warning: VA tracking file not found at {self.csv_path}")
            return []

        vas = []
        with open(self.csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for field in ["hourly_rate", "leads_contacted", "responses",
                              "positive_responses", "calls_booked", "conversions",
                              "hours_logged", "bonuses_earned", "total_paid"]:
                    try:
                        row[field] = float(row[field]) if "." in str(row[field]) else int(row[field])
                    except (ValueError, KeyError):
                        row[field] = 0
                vas.append(row)
        return vas

    def _save_vas(self):
        """Save VA data back to CSV."""
        if not self.vas:
            return

        fieldnames = list(self.vas[0].keys())
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.vas)

    def get_va(self, va_id: str) -> Optional[dict]:
        """Get a specific VA by ID."""
        for va in self.vas:
            if va["va_id"] == va_id:
                return va
        return None

    def get_active_vas(self) -> list[dict]:
        """Get all active VAs."""
        return [va for va in self.vas if va.get("status") == "active"]

    def calculate_response_rate(self, va: dict) -> float:
        """Calculate response rate for a VA."""
        if va["leads_contacted"] == 0:
            return 0.0
        return (va["responses"] / va["leads_contacted"]) * 100

    def calculate_positive_rate(self, va: dict) -> float:
        """Calculate positive response rate."""
        if va["leads_contacted"] == 0:
            return 0.0
        return (va["positive_responses"] / va["leads_contacted"]) * 100

    def calculate_conversion_rate(self, va: dict) -> float:
        """Calculate conversion rate from positive responses."""
        if va["positive_responses"] == 0:
            return 0.0
        return (va["conversions"] / va["positive_responses"]) * 100

    def calculate_bonuses_earned(self, va: dict) -> float:
        """Calculate total bonuses based on activity."""
        task_type = va.get("task_type", "church_outreach")
        bonuses = BONUS_STRUCTURE.get(task_type, BONUS_STRUCTURE["church_outreach"])

        total = 0.0
        total += va["positive_responses"] * bonuses["positive_response"]
        total += va["calls_booked"] * bonuses["call_booked"]
        total += va["conversions"] * bonuses["conversion"]

        return total

    def calculate_total_cost(self, va: dict) -> float:
        """Calculate total cost for a VA."""
        base_pay = va["hours_logged"] * va["hourly_rate"]
        bonuses = self.calculate_bonuses_earned(va)
        return base_pay + bonuses

    def calculate_revenue_generated(self, va: dict) -> float:
        """Calculate revenue generated by VA conversions."""
        task_type = va.get("task_type", "church_outreach")
        conversion_value = CONVERSION_VALUES.get(task_type, 300.00)
        return va["conversions"] * conversion_value

    def calculate_roi(self, va: dict) -> float:
        """Calculate ROI for a VA."""
        cost = self.calculate_total_cost(va)
        if cost == 0:
            return 0.0
        revenue = self.calculate_revenue_generated(va)
        return ((revenue - cost) / cost) * 100

    def calculate_cost_per_lead(self, va: dict) -> float:
        """Calculate cost per lead contacted."""
        cost = self.calculate_total_cost(va)
        if va["leads_contacted"] == 0:
            return 0.0
        return cost / va["leads_contacted"]

    def calculate_cost_per_conversion(self, va: dict) -> float:
        """Calculate cost per conversion."""
        cost = self.calculate_total_cost(va)
        if va["conversions"] == 0:
            return float("inf")
        return cost / va["conversions"]

    def update_va_stats(self, va_id: str, **kwargs):
        """Update stats for a VA."""
        va = self.get_va(va_id)
        if not va:
            print(f"VA {va_id} not found")
            return

        for key, value in kwargs.items():
            if key in va:
                va[key] = value

        # Recalculate bonuses and total paid
        va["bonuses_earned"] = self.calculate_bonuses_earned(va)
        va["total_paid"] = self.calculate_total_cost(va)

        self._save_vas()
        print(f"Updated {va_id}")

    def add_weekly_stats(self, va_id: str, leads: int, responses: int,
                         positive: int, calls: int, conversions: int, hours: float):
        """Add weekly stats to a VA's running totals."""
        va = self.get_va(va_id)
        if not va:
            print(f"VA {va_id} not found")
            return

        va["leads_contacted"] += leads
        va["responses"] += responses
        va["positive_responses"] += positive
        va["calls_booked"] += calls
        va["conversions"] += conversions
        va["hours_logged"] += hours

        va["bonuses_earned"] = self.calculate_bonuses_earned(va)
        va["total_paid"] = self.calculate_total_cost(va)

        self._save_vas()
        print(f"Added weekly stats for {va_id}")


def print_dashboard(tracker: VATracker):
    """Print the VA dashboard to console."""
    active_vas = tracker.get_active_vas()

    if not active_vas:
        print("No active VAs found.")
        return

    print("\n" + "=" * 80)
    print("VA PERFORMANCE DASHBOARD")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    # Summary stats
    total_leads = sum(va["leads_contacted"] for va in active_vas)
    total_responses = sum(va["responses"] for va in active_vas)
    total_conversions = sum(va["conversions"] for va in active_vas)
    total_cost = sum(tracker.calculate_total_cost(va) for va in active_vas)
    total_revenue = sum(tracker.calculate_revenue_generated(va) for va in active_vas)

    print("\nOVERALL SUMMARY")
    print("-" * 40)
    print(f"Active VAs:           {len(active_vas)}")
    print(f"Total leads contacted:{total_leads:>10}")
    print(f"Total responses:      {total_responses:>10}")
    print(f"Total conversions:    {total_conversions:>10}")
    print(f"Total cost:           ${total_cost:>9,.2f}")
    print(f"Total revenue:        ${total_revenue:>9,.2f}")
    if total_cost > 0:
        overall_roi = ((total_revenue - total_cost) / total_cost) * 100
        print(f"Overall ROI:          {overall_roi:>9.1f}%")

    # Individual VA stats
    print("\n" + "=" * 80)
    print("INDIVIDUAL VA PERFORMANCE")
    print("=" * 80)

    for va in active_vas:
        response_rate = tracker.calculate_response_rate(va)
        positive_rate = tracker.calculate_positive_rate(va)
        conversion_rate = tracker.calculate_conversion_rate(va)
        total_cost = tracker.calculate_total_cost(va)
        revenue = tracker.calculate_revenue_generated(va)
        roi = tracker.calculate_roi(va)
        cost_per_lead = tracker.calculate_cost_per_lead(va)
        cost_per_conversion = tracker.calculate_cost_per_conversion(va)

        print(f"\n{va['va_id']} - {va['name']}")
        print(f"Task: {va['task_type']} | Rate: ${va['hourly_rate']}/hr | Platform: {va['platform']}")
        print("-" * 60)
        print(f"  Leads contacted:     {va['leads_contacted']:>6}")
        print(f"  Responses:           {va['responses']:>6} ({response_rate:.1f}%)")
        print(f"  Positive responses:  {va['positive_responses']:>6} ({positive_rate:.1f}%)")
        print(f"  Calls booked:        {va['calls_booked']:>6}")
        print(f"  Conversions:         {va['conversions']:>6} ({conversion_rate:.1f}% from positive)")
        print(f"  Hours logged:        {va['hours_logged']:>6}")
        print("-" * 60)
        print(f"  Base pay:            ${va['hours_logged'] * va['hourly_rate']:>9,.2f}")
        print(f"  Bonuses earned:      ${va['bonuses_earned']:>9,.2f}")
        print(f"  Total cost:          ${total_cost:>9,.2f}")
        print(f"  Revenue generated:   ${revenue:>9,.2f}")
        print(f"  ROI:                 {roi:>9.1f}%")
        print(f"  Cost per lead:       ${cost_per_lead:>9,.2f}")
        if cost_per_conversion != float("inf"):
            print(f"  Cost per conversion: ${cost_per_conversion:>9,.2f}")
        else:
            print(f"  Cost per conversion: N/A (no conversions)")

    # Performance rankings
    print("\n" + "=" * 80)
    print("PERFORMANCE RANKINGS")
    print("=" * 80)

    # By response rate
    by_response = sorted(active_vas, key=lambda x: tracker.calculate_response_rate(x), reverse=True)
    print("\nBy Response Rate:")
    for i, va in enumerate(by_response[:5], 1):
        rate = tracker.calculate_response_rate(va)
        print(f"  {i}. {va['name']}: {rate:.1f}%")

    # By ROI
    by_roi = sorted(active_vas, key=lambda x: tracker.calculate_roi(x), reverse=True)
    print("\nBy ROI:")
    for i, va in enumerate(by_roi[:5], 1):
        roi = tracker.calculate_roi(va)
        print(f"  {i}. {va['name']}: {roi:.1f}%")

    # By conversions
    by_conversions = sorted(active_vas, key=lambda x: x["conversions"], reverse=True)
    print("\nBy Conversions:")
    for i, va in enumerate(by_conversions[:5], 1):
        print(f"  {i}. {va['name']}: {va['conversions']} conversions")

    print("\n" + "=" * 80)


def generate_weekly_report(tracker: VATracker) -> str:
    """Generate a weekly report in markdown format."""
    active_vas = tracker.get_active_vas()
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())

    report = []
    report.append(f"# VA Performance Report")
    report.append(f"**Week of {week_start.strftime('%Y-%m-%d')}**")
    report.append(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')}")
    report.append("")

    # Summary section
    report.append("## Summary")
    report.append("")

    total_leads = sum(va["leads_contacted"] for va in active_vas)
    total_responses = sum(va["responses"] for va in active_vas)
    total_positive = sum(va["positive_responses"] for va in active_vas)
    total_conversions = sum(va["conversions"] for va in active_vas)
    total_cost = sum(tracker.calculate_total_cost(va) for va in active_vas)
    total_revenue = sum(tracker.calculate_revenue_generated(va) for va in active_vas)

    report.append(f"| Metric | Value |")
    report.append(f"|--------|-------|")
    report.append(f"| Active VAs | {len(active_vas)} |")
    report.append(f"| Total leads | {total_leads} |")
    report.append(f"| Total responses | {total_responses} ({(total_responses/total_leads*100):.1f}%) |" if total_leads > 0 else f"| Total responses | 0 |")
    report.append(f"| Positive responses | {total_positive} |")
    report.append(f"| Conversions | {total_conversions} |")
    report.append(f"| Total cost | ${total_cost:,.2f} |")
    report.append(f"| Revenue generated | ${total_revenue:,.2f} |")
    if total_cost > 0:
        roi = ((total_revenue - total_cost) / total_cost) * 100
        report.append(f"| Overall ROI | {roi:.1f}% |")
    report.append("")

    # Individual VA performance
    report.append("## Individual Performance")
    report.append("")

    for va in active_vas:
        response_rate = tracker.calculate_response_rate(va)
        positive_rate = tracker.calculate_positive_rate(va)
        roi = tracker.calculate_roi(va)
        total_cost = tracker.calculate_total_cost(va)

        report.append(f"### {va['name']} ({va['va_id']})")
        report.append(f"**Task:** {va['task_type']} | **Rate:** ${va['hourly_rate']}/hr")
        report.append("")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Leads contacted | {va['leads_contacted']} |")
        report.append(f"| Response rate | {response_rate:.1f}% |")
        report.append(f"| Positive rate | {positive_rate:.1f}% |")
        report.append(f"| Calls booked | {va['calls_booked']} |")
        report.append(f"| Conversions | {va['conversions']} |")
        report.append(f"| Hours logged | {va['hours_logged']} |")
        report.append(f"| Total cost | ${total_cost:,.2f} |")
        report.append(f"| ROI | {roi:.1f}% |")
        report.append("")

        # Performance assessment
        if response_rate >= 10:
            report.append("**Status:** Performing well")
        elif response_rate >= 5:
            report.append("**Status:** Acceptable, monitor closely")
        else:
            report.append("**Status:** Below target, intervention needed")
        report.append("")

    # Recommendations section
    report.append("## Recommendations")
    report.append("")

    # Find top performer
    if active_vas:
        top_by_roi = max(active_vas, key=lambda x: tracker.calculate_roi(x))
        report.append(f"- **Top performer:** {top_by_roi['name']} (consider rate increase)")

        # Find underperformers
        underperformers = [va for va in active_vas if tracker.calculate_response_rate(va) < 5 and va["leads_contacted"] > 50]
        if underperformers:
            report.append(f"- **Needs attention:** {', '.join(va['name'] for va in underperformers)}")

        # Scaling recommendation
        avg_roi = sum(tracker.calculate_roi(va) for va in active_vas) / len(active_vas)
        if avg_roi > 100:
            report.append("- **Scaling:** Strong ROI across team. Consider hiring additional VAs.")
        elif avg_roi > 50:
            report.append("- **Scaling:** Moderate ROI. Optimize current team before hiring.")
        else:
            report.append("- **Scaling:** ROI needs improvement before scaling.")

    report.append("")
    report.append("---")
    report.append(f"*Report generated by va_dashboard.py*")

    return "\n".join(report)


def export_report(tracker: VATracker):
    """Export weekly report to markdown file."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    filename = f"va_report_{now.strftime('%Y-%m-%d')}.md"
    filepath = REPORTS_DIR / filename

    report = generate_weekly_report(tracker)

    with open(filepath, "w") as f:
        f.write(report)

    print(f"Report exported to: {filepath}")


def interactive_update(tracker: VATracker, va_id: str):
    """Interactively update a VA's weekly stats."""
    va = tracker.get_va(va_id)
    if not va:
        print(f"VA {va_id} not found")
        return

    print(f"\nUpdating weekly stats for {va['name']} ({va_id})")
    print(f"Current totals: {va['leads_contacted']} leads, {va['conversions']} conversions")
    print("-" * 40)

    try:
        leads = int(input("Leads contacted this week: "))
        responses = int(input("Responses received: "))
        positive = int(input("Positive responses: "))
        calls = int(input("Calls booked: "))
        conversions = int(input("Conversions: "))
        hours = float(input("Hours logged: "))

        tracker.add_weekly_stats(va_id, leads, responses, positive, calls, conversions, hours)
        print("\nStats updated successfully!")

        # Show updated metrics
        va = tracker.get_va(va_id)
        print(f"\nNew totals:")
        print(f"  Leads: {va['leads_contacted']}")
        print(f"  Conversions: {va['conversions']}")
        print(f"  Total paid: ${tracker.calculate_total_cost(va):,.2f}")

    except ValueError:
        print("Invalid input. Please enter numbers only.")


def main():
    parser = argparse.ArgumentParser(description="VA Performance Dashboard")
    parser.add_argument("--update", type=str, help="Update stats for a VA (e.g., VA001)")
    parser.add_argument("--report", action="store_true", help="Generate weekly report")
    parser.add_argument("--export", action="store_true", help="Export report to markdown file")
    parser.add_argument("--list", action="store_true", help="List all VAs")

    args = parser.parse_args()

    tracker = VATracker()

    if args.list:
        print("\nAll VAs:")
        for va in tracker.vas:
            print(f"  {va['va_id']}: {va['name']} ({va['status']}) - {va['task_type']}")

    elif args.update:
        interactive_update(tracker, args.update)

    elif args.report:
        print(generate_weekly_report(tracker))

    elif args.export:
        export_report(tracker)

    else:
        print_dashboard(tracker)


if __name__ == "__main__":
    main()
