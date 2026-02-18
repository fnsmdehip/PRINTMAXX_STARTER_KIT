#!/usr/bin/env python3
"""
Email Sequence Manager - Track and manage cold email campaigns.

Manages email sequence execution, tracks sends/replies, calculates
deliverability metrics, and integrates with the content pipeline.

Usage:
    python3 email_sequence_manager.py list                  # List all sequences
    python3 email_sequence_manager.py stats                 # Campaign statistics
    python3 email_sequence_manager.py create --icp legal    # Create new campaign
    python3 email_sequence_manager.py track --campaign C001 --event reply --count 5
    python3 email_sequence_manager.py health                # Deliverability health check
    python3 email_sequence_manager.py schedule              # Show send schedule
    python3 email_sequence_manager.py export C001 --format json  # Export campaign data
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Optional

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
CONTENT_DIR = PROJECT_DIR / "CONTENT" / "email_sequences" / "cold"
OUTBOUND_DIR = PROJECT_DIR / "MONEY_METHODS" / "COLD_OUTBOUND"
CAMPAIGN_FILE = LEDGER_DIR / "EMAIL_CAMPAIGNS.csv"
SEQUENCE_DIR = CONTENT_DIR

CAMPAIGN_FIELDS = [
    'campaign_id', 'icp', 'sequence_name', 'sequence_file',
    'total_prospects', 'emails_sent', 'opens', 'replies',
    'positive_replies', 'bounces', 'complaints', 'unsubscribes',
    'meetings_booked', 'deals_closed', 'revenue',
    'open_rate', 'reply_rate', 'bounce_rate', 'complaint_rate',
    'status', 'created_date', 'last_updated', 'notes'
]

# ICP definitions with vertical-specific data
ICP_DEFINITIONS = {
    'legal': {
        'name': 'Legal Services',
        'expected_reply_rate': 0.10,
        'avg_deal_value': 3000,
        'sequence_file': 'legal_services.md',
        'pain_points': ['Google reviews gap', 'missed inbound calls', 'patient/client acquisition'],
        'personalization_vars': ['review_count', 'competitor_reviews', 'review_gap', 'city', 'practice_area'],
    },
    'healthcare': {
        'name': 'Healthcare/Dental',
        'expected_reply_rate': 0.08,
        'avg_deal_value': 3000,
        'sequence_file': 'healthcare_dental.md',
        'pain_points': ['missed calls', 'review gap', 'patient communication'],
        'personalization_vars': ['review_count', 'competitor_reviews', 'review_gap', 'city', 'specialty'],
    },
    'saas': {
        'name': 'SaaS Founders ($10K-$100K MRR)',
        'expected_reply_rate': 0.05,
        'avg_deal_value': 5000,
        'sequence_file': 'saas_founders.md',
        'pain_points': ['growth plateau', 'churn', 'acquisition cost'],
        'personalization_vars': ['company_name', 'mrr_estimate', 'product_category', 'recent_launch'],
    },
    'ecom': {
        'name': 'E-commerce Brands ($50K-$500K/mo)',
        'expected_reply_rate': 0.06,
        'avg_deal_value': 2500,
        'sequence_file': 'ecom_brands.md',
        'pain_points': ['ad fatigue', 'rising CAC', 'content production'],
        'personalization_vars': ['brand_name', 'product_category', 'monthly_revenue_estimate', 'ad_spend'],
    },
    'agency': {
        'name': 'Marketing Agencies (5-20 employees)',
        'expected_reply_rate': 0.07,
        'avg_deal_value': 2000,
        'sequence_file': 'marketing_agencies.md',
        'pain_points': ['white-label needs', 'client churn', 'scaling content'],
        'personalization_vars': ['agency_name', 'team_size', 'client_types', 'services'],
    },
    'coaches': {
        'name': 'Business/Life Coaches with Audience',
        'expected_reply_rate': 0.08,
        'avg_deal_value': 1500,
        'sequence_file': 'coaches.md',
        'pain_points': ['funnel optimization', 'community management', 'content repurposing'],
        'personalization_vars': ['coach_name', 'audience_size', 'niche', 'current_product'],
    },
}

# Deliverability thresholds (per Gmail 2026 requirements)
HEALTH_THRESHOLDS = {
    'complaint_rate_max': 0.001,   # 0.1% per Gmail RETVec
    'bounce_rate_max': 0.05,       # 5% max
    'reply_rate_min': 0.03,        # 3% minimum healthy
    'open_rate_min': 0.20,         # 20% minimum healthy
    'unsubscribe_max': 0.005,      # 0.5% max
}


def load_campaigns() -> list:
    """Load all campaigns from CSV."""
    if not CAMPAIGN_FILE.exists():
        return []
    with open(CAMPAIGN_FILE, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_campaign(campaign: dict):
    """Save or update a campaign row."""
    campaigns = load_campaigns()
    found = False

    for i, c in enumerate(campaigns):
        if c.get('campaign_id') == campaign.get('campaign_id'):
            campaigns[i] = campaign
            found = True
            break

    if not found:
        campaigns.append(campaign)

    with open(CAMPAIGN_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPAIGN_FIELDS)
        writer.writeheader()
        for c in campaigns:
            # Ensure all fields exist
            row = {k: c.get(k, '') for k in CAMPAIGN_FIELDS}
            writer.writerow(row)


def next_campaign_id() -> str:
    """Generate next campaign ID."""
    campaigns = load_campaigns()
    if not campaigns:
        return 'C001'
    ids = [c.get('campaign_id', '') for c in campaigns]
    nums = [int(i[1:]) for i in ids if i.startswith('C') and i[1:].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    return f'C{next_num:03d}'


def calculate_rates(campaign: dict) -> dict:
    """Calculate campaign rates from raw numbers."""
    sent = int(campaign.get('emails_sent', 0) or 0)
    if sent == 0:
        return campaign

    opens = int(campaign.get('opens', 0) or 0)
    replies = int(campaign.get('replies', 0) or 0)
    bounces = int(campaign.get('bounces', 0) or 0)
    complaints = int(campaign.get('complaints', 0) or 0)

    campaign['open_rate'] = f"{(opens / sent * 100):.1f}%"
    campaign['reply_rate'] = f"{(replies / sent * 100):.1f}%"
    campaign['bounce_rate'] = f"{(bounces / sent * 100):.1f}%"
    campaign['complaint_rate'] = f"{(complaints / sent * 100):.2f}%"
    campaign['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    return campaign


def cmd_list(args):
    """List all email sequences and campaigns."""
    # List available sequences
    print("\n=== Available Email Sequences ===\n")

    if CONTENT_DIR.exists():
        seq_files = sorted(CONTENT_DIR.glob("*.md"))
        for f in seq_files:
            icp_match = [k for k, v in ICP_DEFINITIONS.items() if v['sequence_file'] == f.name]
            icp_label = f" ({ICP_DEFINITIONS[icp_match[0]]['name']})" if icp_match else ""
            size_kb = f.stat().st_size / 1024
            print(f"  {f.name:<40} {size_kb:>6.1f}KB{icp_label}")
    else:
        print("  No sequences found in CONTENT/email_sequences/cold/")

    # List active campaigns
    campaigns = load_campaigns()
    if campaigns:
        print(f"\n=== Active Campaigns ({len(campaigns)}) ===\n")
        print(f"{'ID':<8} {'ICP':<25} {'Sent':>6} {'Replies':>8} {'Rate':>6} {'Status':<12}")
        print("-" * 75)
        for c in campaigns:
            cid = c.get('campaign_id', 'N/A')
            icp = c.get('icp', 'N/A')[:24]
            sent = c.get('emails_sent', '0')
            replies = c.get('replies', '0')
            rate = c.get('reply_rate', 'N/A')
            status = c.get('status', 'N/A')
            print(f"{cid:<8} {icp:<25} {sent:>6} {replies:>8} {rate:>6} {status:<12}")
    else:
        print("\n  No campaigns created yet. Use 'create --icp legal' to start.")

    # List ICPs
    print(f"\n=== ICP Definitions ({len(ICP_DEFINITIONS)}) ===\n")
    for key, icp in ICP_DEFINITIONS.items():
        print(f"  {key:<12} {icp['name']:<35} Expected reply: {icp['expected_reply_rate']*100:.0f}%  Avg deal: ${icp['avg_deal_value']}")


def cmd_create(args):
    """Create a new campaign."""
    icp_key = args.icp.lower()
    if icp_key not in ICP_DEFINITIONS:
        print(f"Error: Unknown ICP '{icp_key}'. Available: {', '.join(ICP_DEFINITIONS.keys())}")
        sys.exit(1)

    icp = ICP_DEFINITIONS[icp_key]
    campaign_id = next_campaign_id()

    # Check if sequence file exists
    seq_file = CONTENT_DIR / icp['sequence_file']
    seq_exists = seq_file.exists()

    campaign = {
        'campaign_id': campaign_id,
        'icp': icp['name'],
        'sequence_name': f"{icp_key}_cold_{datetime.now().strftime('%Y%m%d')}",
        'sequence_file': str(seq_file) if seq_exists else f"TODO: Create {icp['sequence_file']}",
        'total_prospects': args.prospects if hasattr(args, 'prospects') and args.prospects else 0,
        'emails_sent': 0,
        'opens': 0,
        'replies': 0,
        'positive_replies': 0,
        'bounces': 0,
        'complaints': 0,
        'unsubscribes': 0,
        'meetings_booked': 0,
        'deals_closed': 0,
        'revenue': 0,
        'open_rate': '0%',
        'reply_rate': '0%',
        'bounce_rate': '0%',
        'complaint_rate': '0%',
        'status': 'CREATED',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'notes': f"ICP: {icp['name']}. Pain points: {', '.join(icp['pain_points'])}",
    }

    save_campaign(campaign)

    print(f"\nCampaign created: {campaign_id}")
    print(f"  ICP: {icp['name']}")
    print(f"  Expected reply rate: {icp['expected_reply_rate']*100:.0f}%")
    print(f"  Avg deal value: ${icp['avg_deal_value']}")
    print(f"  Sequence file: {'EXISTS' if seq_exists else 'NEEDS CREATION'} ({icp['sequence_file']})")
    print(f"  Personalization vars: {', '.join(icp['personalization_vars'])}")
    print(f"\nNext: Track events with 'track --campaign {campaign_id} --event send --count 100'")


def cmd_track(args):
    """Track campaign events (sends, opens, replies, etc)."""
    campaigns = load_campaigns()
    campaign = None
    for c in campaigns:
        if c.get('campaign_id') == args.campaign:
            campaign = c
            break

    if not campaign:
        print(f"Error: Campaign '{args.campaign}' not found.")
        sys.exit(1)

    event = args.event.lower()
    count = args.count

    event_map = {
        'send': 'emails_sent',
        'open': 'opens',
        'reply': 'replies',
        'positive': 'positive_replies',
        'bounce': 'bounces',
        'complaint': 'complaints',
        'unsubscribe': 'unsubscribes',
        'meeting': 'meetings_booked',
        'deal': 'deals_closed',
    }

    if event not in event_map:
        print(f"Error: Unknown event '{event}'. Available: {', '.join(event_map.keys())}")
        sys.exit(1)

    field = event_map[event]
    current = int(campaign.get(field, 0) or 0)
    campaign[field] = str(current + count)

    # Update status based on sends
    if int(campaign.get('emails_sent', 0)) > 0:
        campaign['status'] = 'ACTIVE'

    # Recalculate rates
    campaign = calculate_rates(campaign)
    save_campaign(campaign)

    print(f"Updated {args.campaign}: {event} +{count} (total: {campaign[field]})")
    print(f"  Open rate: {campaign.get('open_rate', 'N/A')}")
    print(f"  Reply rate: {campaign.get('reply_rate', 'N/A')}")
    print(f"  Bounce rate: {campaign.get('bounce_rate', 'N/A')}")
    print(f"  Complaint rate: {campaign.get('complaint_rate', 'N/A')}")


def cmd_health(args):
    """Deliverability health check across all campaigns."""
    campaigns = load_campaigns()
    active = [c for c in campaigns if c.get('status', '').upper() == 'ACTIVE']

    if not active:
        print("No active campaigns to check.")
        return

    print(f"\n=== Deliverability Health Check ===\n")
    print(f"Gmail 2026 thresholds: Complaint <0.1%, Bounce <5%, Reply >3%\n")

    issues = []
    for c in active:
        cid = c.get('campaign_id', 'N/A')
        sent = int(c.get('emails_sent', 0) or 0)
        if sent == 0:
            continue

        complaints = int(c.get('complaints', 0) or 0)
        bounces = int(c.get('bounces', 0) or 0)
        replies = int(c.get('replies', 0) or 0)
        opens = int(c.get('opens', 0) or 0)

        complaint_rate = complaints / sent
        bounce_rate = bounces / sent
        reply_rate = replies / sent
        open_rate = opens / sent

        status_parts = []

        # Check thresholds
        if complaint_rate > HEALTH_THRESHOLDS['complaint_rate_max']:
            status_parts.append(f"CRITICAL: Complaint rate {complaint_rate*100:.2f}% (max 0.1%)")
            issues.append(f"{cid}: complaint rate critical")
        elif complaint_rate > HEALTH_THRESHOLDS['complaint_rate_max'] * 0.8:
            status_parts.append(f"WARNING: Complaint rate {complaint_rate*100:.2f}% (approaching 0.1%)")

        if bounce_rate > HEALTH_THRESHOLDS['bounce_rate_max']:
            status_parts.append(f"CRITICAL: Bounce rate {bounce_rate*100:.1f}% (max 5%)")
            issues.append(f"{cid}: bounce rate critical")

        if reply_rate < HEALTH_THRESHOLDS['reply_rate_min']:
            status_parts.append(f"LOW: Reply rate {reply_rate*100:.1f}% (target >3%)")

        if open_rate < HEALTH_THRESHOLDS['open_rate_min']:
            status_parts.append(f"LOW: Open rate {open_rate*100:.1f}% (target >20%)")

        if not status_parts:
            status_parts.append("HEALTHY")

        print(f"  {cid} ({c.get('icp', 'N/A')[:20]}):")
        for s in status_parts:
            print(f"    {s}")

    if issues:
        print(f"\n{len(issues)} CRITICAL issues found:")
        for issue in issues:
            print(f"  {issue}")
        print("\nAction: Pause affected campaigns, check domain reputation, review copy.")
    else:
        print("\nAll campaigns within healthy thresholds.")


def cmd_stats(args):
    """Campaign statistics summary."""
    campaigns = load_campaigns()

    if not campaigns:
        print("No campaigns. Use 'create --icp legal' to start.")
        return

    total_sent = sum(int(c.get('emails_sent', 0) or 0) for c in campaigns)
    total_replies = sum(int(c.get('replies', 0) or 0) for c in campaigns)
    total_meetings = sum(int(c.get('meetings_booked', 0) or 0) for c in campaigns)
    total_deals = sum(int(c.get('deals_closed', 0) or 0) for c in campaigns)
    total_revenue = sum(float(c.get('revenue', 0) or 0) for c in campaigns)

    print(f"\n{'=' * 50}")
    print(f"EMAIL CAMPAIGN STATISTICS")
    print(f"{'=' * 50}")
    print(f"\nCampaigns: {len(campaigns)}")
    print(f"Total emails sent: {total_sent}")
    print(f"Total replies: {total_replies} ({total_replies/total_sent*100:.1f}%)" if total_sent else "")
    print(f"Meetings booked: {total_meetings}")
    print(f"Deals closed: {total_deals}")
    print(f"Revenue: ${total_revenue:,.2f}")
    if total_deals > 0:
        print(f"Avg deal size: ${total_revenue/total_deals:,.2f}")
    if total_sent > 0:
        print(f"Revenue per email: ${total_revenue/total_sent:.2f}")

    # Per-campaign breakdown
    print(f"\nPer-Campaign Breakdown:")
    print(f"{'ID':<8} {'ICP':<20} {'Sent':>6} {'Reply%':>7} {'Meetings':>9} {'Revenue':>10}")
    print("-" * 65)
    for c in campaigns:
        print(f"{c.get('campaign_id', ''):<8} "
              f"{c.get('icp', '')[:19]:<20} "
              f"{c.get('emails_sent', '0'):>6} "
              f"{c.get('reply_rate', '0%'):>7} "
              f"{c.get('meetings_booked', '0'):>9} "
              f"${float(c.get('revenue', 0) or 0):>9,.0f}")

    # Vertical performance
    print(f"\nVertical Performance:")
    vertical_stats = defaultdict(lambda: {'sent': 0, 'replies': 0, 'revenue': 0})
    for c in campaigns:
        icp = c.get('icp', 'Unknown')
        vertical_stats[icp]['sent'] += int(c.get('emails_sent', 0) or 0)
        vertical_stats[icp]['replies'] += int(c.get('replies', 0) or 0)
        vertical_stats[icp]['revenue'] += float(c.get('revenue', 0) or 0)

    for icp, stats in sorted(vertical_stats.items(), key=lambda x: -x[1]['revenue']):
        rate = f"{stats['replies']/stats['sent']*100:.1f}%" if stats['sent'] > 0 else "N/A"
        print(f"  {icp:<30} Sent: {stats['sent']:>5}  Reply: {rate:>6}  Rev: ${stats['revenue']:>8,.0f}")


def cmd_schedule(args):
    """Show recommended send schedule."""
    print(f"\n=== Cold Email Send Schedule ===\n")

    print("Recommended daily limits (per 2026 deliverability best practices):")
    print(f"  Per domain: 50-100 emails/day (warm)")
    print(f"  Per inbox: 20-30 emails/day")
    print(f"  Total across all domains: 200-500/day")
    print(f"  Warmup period: 2-4 weeks before full volume")
    print()

    # Show active campaign schedule
    campaigns = load_campaigns()
    active = [c for c in campaigns if c.get('status', '').upper() in ('ACTIVE', 'CREATED')]

    if active:
        print("Active Campaign Schedule:")
        for c in active:
            cid = c.get('campaign_id', '')
            icp = c.get('icp', '')
            prospects = int(c.get('total_prospects', 0) or 0)
            sent = int(c.get('emails_sent', 0) or 0)
            remaining = prospects - sent

            if remaining > 0:
                days_at_50 = remaining / 50
                days_at_100 = remaining / 100
                print(f"  {cid} ({icp}):")
                print(f"    Remaining: {remaining} prospects")
                print(f"    At 50/day: {days_at_50:.0f} days")
                print(f"    At 100/day: {days_at_100:.0f} days")
            else:
                print(f"  {cid} ({icp}): All prospects contacted")

    print(f"\nOptimal send times (by vertical):")
    print(f"  Legal: Tue-Thu 8:00-10:00 AM local")
    print(f"  Healthcare: Mon-Wed 7:00-9:00 AM local")
    print(f"  SaaS: Tue-Thu 9:00-11:00 AM local")
    print(f"  E-commerce: Mon-Fri 10:00 AM-12:00 PM local")
    print(f"  Agency: Tue-Thu 8:00-10:00 AM local")


def cmd_export(args):
    """Export campaign data."""
    campaigns = load_campaigns()
    campaign = None
    for c in campaigns:
        if c.get('campaign_id') == args.campaign_id:
            campaign = c
            break

    if not campaign:
        print(f"Error: Campaign '{args.campaign_id}' not found.")
        sys.exit(1)

    if args.format == 'json':
        output = json.dumps(campaign, indent=2)
    else:
        output = json.dumps(campaign, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Exported to {args.output}")
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        description='Email Sequence Manager - Track cold email campaigns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                                    List sequences and campaigns
  %(prog)s create --icp legal --prospects 500      Create legal campaign
  %(prog)s track --campaign C001 --event send --count 100
  %(prog)s track --campaign C001 --event reply --count 5
  %(prog)s health                                  Deliverability check
  %(prog)s stats                                   Campaign statistics
  %(prog)s schedule                                Send schedule
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    sub_list = subparsers.add_parser('list', help='List sequences and campaigns')
    sub_list.set_defaults(func=cmd_list)

    sub_create = subparsers.add_parser('create', help='Create new campaign')
    sub_create.add_argument('--icp', required=True, help='ICP key (legal, healthcare, saas, ecom, agency, coaches)')
    sub_create.add_argument('--prospects', type=int, default=0, help='Number of prospects')
    sub_create.set_defaults(func=cmd_create)

    sub_track = subparsers.add_parser('track', help='Track campaign events')
    sub_track.add_argument('--campaign', required=True, help='Campaign ID')
    sub_track.add_argument('--event', required=True, help='Event type (send, open, reply, positive, bounce, complaint, unsubscribe, meeting, deal)')
    sub_track.add_argument('--count', type=int, default=1, help='Event count')
    sub_track.set_defaults(func=cmd_track)

    sub_health = subparsers.add_parser('health', help='Deliverability health check')
    sub_health.set_defaults(func=cmd_health)

    sub_stats = subparsers.add_parser('stats', help='Campaign statistics')
    sub_stats.set_defaults(func=cmd_stats)

    sub_schedule = subparsers.add_parser('schedule', help='Send schedule')
    sub_schedule.set_defaults(func=cmd_schedule)

    sub_export = subparsers.add_parser('export', help='Export campaign data')
    sub_export.add_argument('campaign_id', help='Campaign ID to export')
    sub_export.add_argument('--format', choices=['json'], default='json')
    sub_export.add_argument('--output', '-o', help='Output file path')
    sub_export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
