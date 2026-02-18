#!/usr/bin/env python3
"""
PRINTMAXX Account Tracker & Warmup System

CLI for tracking account status, warmup progress, and identifying
which revenue ops are blocked by missing/inactive accounts.

Usage:
    python3 scripts/account_tracker.py status
    python3 scripts/account_tracker.py add --platform Gumroad --username printmaxxer --email x@y.com --status CREATED
    python3 scripts/account_tracker.py warmup --platform Gumroad
    python3 scripts/account_tracker.py blockers
    python3 scripts/account_tracker.py update --platform Gumroad --status ACTIVE
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ACCOUNTS_CSV = BASE_DIR / "LEDGER" / "ACCOUNTS.csv"

# Platform name aliases: CSV may use "X" but warmup schedule uses "Twitter/X"
PLATFORM_ALIASES = {
    "X": "Twitter/X",
    "x": "Twitter/X",
    "twitter": "Twitter/X",
    "Twitter": "Twitter/X",
}

HEADERS = [
    "Niche", "Platform", "Handle", "Email", "ProxyUsed",
    "GoLoginProfile", "Status", "CreatedDate", "LastActive", "Notes"
]

# ---------------------------------------------------------------------------
# Warmup schedules: day_number -> task description
# ---------------------------------------------------------------------------
WARMUP_SCHEDULES = {
    "Gumroad": {
        1: "Create account + connect Stripe. Upload profile pic, write bio.",
        2: "Upload first product (use best Notion template or digital product).",
        3: "Share product link on Twitter/X and relevant subreddit.",
        4: "Share on second platform (LinkedIn, Facebook group, or Discord).",
        5: "Share on third platform. Ask 1-2 friends to leave reviews.",
        6: "ACTIVE - Monitor sales, iterate on listings.",
    },
    "Fiverr": {
        1: "Create account. Complete profile: photo, bio, skills, portfolio.",
        2: "Create first 3 gigs with optimized titles, tags, and pricing.",
        3: "Create remaining gigs (up to 7). Add FAQ and gig extras.",
        4: "Share gig links on social. Join Fiverr buyer requests.",
        5: "Apply to 5+ buyer requests. Share on Reddit (r/forhire).",
        6: "Apply to 5+ buyer requests. Optimize gig descriptions.",
        7: "Apply to 5+ buyer requests. Get first review (offer discount if needed).",
        8: "ACTIVE - Daily buyer request applications, gig optimization.",
    },
    "Upwork": {
        1: "Create account. Complete profile: photo, title, overview, skills, portfolio.",
        2: "Apply to 5 jobs. Use personalized proposals, not templates.",
        3: "Apply to 5 more jobs. Refine proposal based on responses.",
        4: "Apply to 5 jobs. Start bidding more aggressively on smaller jobs.",
        5: "Apply to 5 jobs. Consider lower rate for first 1-2 to build reviews.",
        6: "Apply to 5 jobs. Check for invitations.",
        7: "Apply to 5 jobs. Optimize profile based on what gets responses.",
        8: "ACTIVE - Daily applications, raise rates after first 3 reviews.",
    },
    "Fanvue": {
        1: "Create account. Set tiers: $9.99 (Peek), $24.99 (VIP), $49.99 (Elite). Upload profile pic + banner.",
        2: "Upload 10 teaser posts (mix of free + locked). Write compelling captions.",
        3: "Cross-promote on Twitter/X with teaser images. Pin best post.",
        4: "Post 3-5 new pieces. Engage with subscribers. Set up tip menu.",
        5: "Cross-promote on Reddit (relevant NSFW subs). Run promo pricing.",
        6: "ACTIVE - Daily posts, DM engagement, weekly PPV drops.",
    },
    "Fansly": {
        1: "Create account. Set tiers: $9.99 (Peek), $24.99 (VIP), $49.99 (Elite). Upload profile pic + banner.",
        2: "Upload 10 teaser posts (mix of free + locked). Write compelling captions.",
        3: "Cross-promote on Twitter/X with teaser images. Pin best post.",
        4: "Post 3-5 new pieces. Engage with subscribers. Set up tip menu.",
        5: "Cross-promote on Reddit (relevant subs). Run promo pricing.",
        6: "ACTIVE - Daily posts, DM engagement, weekly PPV drops.",
    },
    "TikTok": {
        1: "Create account. Profile pic, bio with link, switch to business account.",
        2: "Watch and like 50+ videos in your niche. Follow 20 creators.",
        3: "Watch, like, comment on 30+ videos. Follow 20 more. Study trends.",
        4: "Post first video (trending sound + niche topic). Keep watching/engaging.",
        5: "Post 1-2 videos. Engage with comments on other posts.",
        6: "Post 1-2 videos. Reply to all comments on your posts.",
        7: "Post 1-2 videos. Duet or stitch a trending video.",
        8: "Post 2-3 videos daily. Engage 30 min/day.",
        9: "Post 2-3 videos daily. Test different hooks.",
        10: "Post 2-3 videos daily. Analyze which topics perform.",
        11: "Post 2-3 videos daily. Double down on best format.",
        12: "Post 2-3 videos daily.",
        13: "Post 2-3 videos daily.",
        14: "Post 3x/day. Analyze performance, refine strategy.",
        15: "ACTIVE - 3x/day posting, consistent engagement, trend-jacking.",
    },
    "Twitter/X": {
        1: "Create account. Profile pic, banner, bio with CTA, pinned tweet.",
        2: "Follow 50 relevant accounts. Like and RT 20+ tweets. Post 2 tweets.",
        3: "Follow 30 more. Like/RT 20+. Post 3 tweets. Reply to 10 accounts.",
        4: "Post 3-5 tweets. Reply to 15 accounts in niche. Quote tweet 2.",
        5: "Post 3-5 tweets. Run first thread. Reply to 15 accounts.",
        6: "Post 3-5 tweets. Reply to 15 accounts. Engage with quote tweets.",
        7: "Post 5 tweets. Full engagement routine. First thread with CTA.",
        8: "ACTIVE - 5+ tweets/day, daily engagement, weekly threads.",
    },
}

# ---------------------------------------------------------------------------
# Account -> Ops blocking mapping
# ---------------------------------------------------------------------------
OPS_BLOCKED_BY = {
    "Gumroad": [
        "Digital products (9 products ready to list)",
        "Info products (playbooks, guides)",
        "Notion templates (5+ ready)",
        "Gumroad affiliate program",
    ],
    "Fiverr": [
        "Freelance arbitrage (30 services spec'd)",
        "AI UGC service offerings",
        "Vibe-coded app dev services",
    ],
    "Upwork": [
        "Freelance arbitrage (higher ticket)",
        "Agency service packages",
        "Cold outbound lead gen services",
    ],
    "Fanvue": [
        "AI findom personas (10 personas ready)",
        "AI influencer monetization (primary platform)",
        "PPV content drops",
        "Tip menu / custom content",
    ],
    "Fansly": [
        "AI findom personas (backup platform)",
        "AI influencer monetization (secondary)",
        "Cross-platform content distribution",
    ],
    "TikTok": [
        "Content farm (3 niches: faith, fitness, AI)",
        "Short-form video ops",
        "TikTok Shop affiliate",
        "Creator fund revenue",
    ],
    "Twitter/X": [
        "Findom discovery + subscriber acquisition",
        "@PRINTMAXXER brand building",
        "Content distribution (primary)",
        "Niche account engagement farming",
        "Newsletter subscriber acquisition",
    ],
    "Beehiiv": [
        "Newsletter monetization (3 newsletters planned)",
        "Subscriber list building",
        "Beehiiv Ad Network revenue",
    ],
    "Stripe": [
        "ALL payment processing",
        "Gumroad payouts",
        "Direct sales",
    ],
}


def normalize_platform(name):
    """Normalize platform name to match warmup schedule keys."""
    return PLATFORM_ALIASES.get(name, name)


def load_accounts():
    """Load accounts from CSV. Returns list of dicts."""
    if not ACCOUNTS_CSV.exists():
        return []
    rows = []
    with open(ACCOUNTS_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def save_accounts(rows):
    """Write accounts back to CSV."""
    ACCOUNTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(ACCOUNTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def days_since_created(created_str):
    """Return number of days since account was created, or None."""
    if not created_str:
        return None
    try:
        created = datetime.strptime(created_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None
    return (datetime.now() - created).days


def warmup_day(platform, created_str):
    """Return the current warmup day number (1-indexed) or 'N/A'."""
    d = days_since_created(created_str)
    if d is None:
        return "N/A"
    return d + 1  # day 1 = creation day


def get_warmup_task(platform, day_num):
    """Return today's warmup task for a platform, or None."""
    schedule = WARMUP_SCHEDULES.get(normalize_platform(platform))
    if not schedule:
        return None
    if day_num in schedule:
        return schedule[day_num]
    max_day = max(schedule.keys())
    if day_num >= max_day:
        return schedule[max_day]
    # Find the most recent milestone day
    for d in sorted(schedule.keys(), reverse=True):
        if day_num >= d:
            return schedule[d]
    return schedule[min(schedule.keys())]


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(args):
    """Show all accounts with status, warmup day, and blocked ops."""
    accounts = load_accounts()
    if not accounts:
        print("No accounts found in LEDGER/ACCOUNTS.csv")
        return

    # Group by platform
    by_platform = {}
    for acc in accounts:
        plat = acc.get("Platform", "Unknown")
        by_platform.setdefault(plat, []).append(acc)

    print("=" * 80)
    print("PRINTMAXX ACCOUNT TRACKER")
    print(f"  {len(accounts)} accounts across {len(by_platform)} platforms")
    print(f"  Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    status_counts = {"ACTIVE": 0, "WARMUP": 0, "CREATED": 0, "PENDING": 0, "SUSPENDED": 0}

    for platform in sorted(by_platform.keys()):
        accs = by_platform[platform]
        print(f"\n--- {platform} ({len(accs)} accounts) ---")
        for acc in accs:
            status = acc.get("Status", "UNKNOWN")
            handle = acc.get("Handle", "N/A")
            niche = acc.get("Niche", "")
            created = acc.get("CreatedDate", "")
            day = warmup_day(platform, created)
            notes = acc.get("Notes", "")

            status_icon = {
                "ACTIVE": "[OK]",
                "WARMUP": "[~~]",
                "CREATED": "[..] ",
                "PENDING": "[!!]",
                "SUSPENDED": "[XX]",
            }.get(status, "[??]")

            status_counts[status] = status_counts.get(status, 0) + 1

            day_str = f"Day {day}" if isinstance(day, int) else day
            print(f"  {status_icon} {handle:<30} {status:<12} {day_str:<8} {niche:<10} {notes}")

        # Show blocked ops for this platform
        blocked = OPS_BLOCKED_BY.get(normalize_platform(platform), [])
        if blocked:
            has_active = any(a.get("Status") == "ACTIVE" for a in accs)
            if not has_active:
                print(f"  BLOCKED OPS:")
                for op in blocked:
                    print(f"    - {op}")

    print("\n" + "=" * 80)
    print("SUMMARY:")
    for s, c in sorted(status_counts.items()):
        if c > 0:
            print(f"  {s}: {c}")
    print("=" * 80)


def cmd_add(args):
    """Add a new account."""
    accounts = load_accounts()

    # Check for duplicate
    for acc in accounts:
        if acc.get("Platform") == args.platform and acc.get("Handle") == args.username:
            print(f"Account already exists: {args.platform} / {args.username}")
            print(f"  Status: {acc.get('Status')} | Created: {acc.get('CreatedDate')}")
            return

    new_row = {
        "Niche": args.niche or "",
        "Platform": args.platform,
        "Handle": args.username,
        "Email": args.email or "",
        "ProxyUsed": args.proxy or "",
        "GoLoginProfile": args.profile or "",
        "Status": args.status or "CREATED",
        "CreatedDate": args.date or datetime.now().strftime("%Y-%m-%d"),
        "LastActive": "",
        "Notes": args.notes or "",
    }

    accounts.append(new_row)
    save_accounts(accounts)
    print(f"Added: {args.platform} / {args.username} (Status: {new_row['Status']})")

    # Show warmup schedule
    schedule = WARMUP_SCHEDULES.get(args.platform)
    if schedule:
        print(f"\nWarmup schedule for {args.platform}:")
        for day, task in sorted(schedule.items()):
            marker = " <-- TODAY" if day == 1 else ""
            print(f"  Day {day}: {task}{marker}")


def cmd_warmup(args):
    """Show today's warmup tasks for a platform (or all platforms)."""
    accounts = load_accounts()

    if args.platform:
        platforms = [args.platform]
    else:
        platforms = sorted(set(WARMUP_SCHEDULES.keys()))

    print("=" * 80)
    print(f"WARMUP TASKS FOR TODAY ({datetime.now().strftime('%Y-%m-%d')})")
    print("=" * 80)

    found_any = False
    for platform in platforms:
        norm = normalize_platform(platform)
        # Match accounts by either raw platform name or normalized name
        platform_accounts = [a for a in accounts
                             if a.get("Platform") == platform
                             or normalize_platform(a.get("Platform", "")) == norm]
        if not platform_accounts:
            if args.platform:
                print(f"\nNo accounts found for {platform}")
                print(f"Add one: python3 scripts/account_tracker.py add --platform {platform} --username <handle> --email <email>")
            continue

        schedule = WARMUP_SCHEDULES.get(norm)
        if not schedule:
            continue

        for acc in platform_accounts:
            status = acc.get("Status", "")
            if status == "ACTIVE":
                continue  # Skip already active accounts

            handle = acc.get("Handle", "N/A")
            created = acc.get("CreatedDate", "")
            day = warmup_day(platform, created)

            if not isinstance(day, int):
                continue

            task = get_warmup_task(platform, day)
            if not task:
                continue

            found_any = True
            print(f"\n{platform} - {handle} (Day {day}):")
            print(f"  TODAY: {task}")

            # Show what's next
            next_day = day + 1
            next_task = get_warmup_task(platform, next_day)
            if next_task and next_task != task:
                print(f"  TOMORROW: {next_task}")

    if not found_any:
        print("\nNo accounts currently in warmup. All accounts are either ACTIVE or not yet created.")
        print("\nPlatforms with warmup schedules:")
        for p in sorted(WARMUP_SCHEDULES.keys()):
            max_day = max(WARMUP_SCHEDULES[p].keys())
            print(f"  {p}: {max_day}-day warmup")


def cmd_blockers(args):
    """Show which revenue ops are blocked by missing/inactive accounts."""
    accounts = load_accounts()

    print("=" * 80)
    print("REVENUE OPS BLOCKERS")
    print(f"  Checked: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    total_blocked = 0
    total_unblocked = 0

    for platform in sorted(OPS_BLOCKED_BY.keys()):
        ops = OPS_BLOCKED_BY[platform]
        # Match accounts by normalized platform name
        platform_accounts = [a for a in accounts
                             if a.get("Platform") == platform
                             or normalize_platform(a.get("Platform", "")) == platform]
        has_active = any(a.get("Status") == "ACTIVE" for a in platform_accounts)
        has_any = len(platform_accounts) > 0

        if has_active:
            status_label = "UNBLOCKED"
            icon = "[OK]"
            total_unblocked += len(ops)
        elif has_any:
            warmup_accs = [a for a in platform_accounts if a.get("Status") in ("CREATED", "WARMUP", "PENDING")]
            if warmup_accs:
                acc = warmup_accs[0]
                day = warmup_day(platform, acc.get("CreatedDate", ""))
                sched = WARMUP_SCHEDULES.get(platform) or WARMUP_SCHEDULES.get(normalize_platform(platform))
                max_day = max(sched.keys()) if sched else "?"
                status_label = f"IN WARMUP (Day {day}/{max_day})"
                icon = "[~~]"
            else:
                status_label = "ACCOUNT EXISTS BUT NOT ACTIVE"
                icon = "[..]"
            total_blocked += len(ops)
        else:
            status_label = "NO ACCOUNT - CREATE NOW"
            icon = "[XX]"
            total_blocked += len(ops)

        print(f"\n{icon} {platform} - {status_label}")
        for op in ops:
            if has_active:
                print(f"    [OK] {op}")
            else:
                print(f"    [BLOCKED] {op}")

    print("\n" + "=" * 80)
    print(f"SUMMARY: {total_unblocked} ops unblocked, {total_blocked} ops BLOCKED")
    if total_blocked > 0:
        print(f"\nACTION: Create/warm up accounts to unblock {total_blocked} revenue ops.")
        missing = []
        for platform in OPS_BLOCKED_BY:
            platform_accounts = [a for a in accounts
                                 if a.get("Platform") == platform
                                 or normalize_platform(a.get("Platform", "")) == platform]
            if not platform_accounts:
                missing.append(platform)
        if missing:
            print(f"MISSING ACCOUNTS: {', '.join(missing)}")
    print("=" * 80)


def cmd_update(args):
    """Update account status."""
    accounts = load_accounts()
    updated = False

    for acc in accounts:
        match = acc.get("Platform") == args.platform
        if args.username:
            match = match and acc.get("Handle") == args.username

        if match:
            old_status = acc.get("Status")
            acc["Status"] = args.status
            if args.status == "ACTIVE":
                acc["LastActive"] = datetime.now().strftime("%Y-%m-%d")
            if args.notes:
                existing = acc.get("Notes", "")
                acc["Notes"] = f"{existing}; {args.notes}" if existing else args.notes
            print(f"Updated: {acc.get('Platform')} / {acc.get('Handle')}: {old_status} -> {args.status}")
            updated = True

    if not updated:
        print(f"No account found for platform={args.platform}" +
              (f", username={args.username}" if args.username else ""))
        return

    save_accounts(accounts)
    print("Saved.")


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Account Tracker & Warmup System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/account_tracker.py status
  python3 scripts/account_tracker.py add --platform Gumroad --username printmaxxer --email x@y.com
  python3 scripts/account_tracker.py warmup --platform Twitter/X
  python3 scripts/account_tracker.py blockers
  python3 scripts/account_tracker.py update --platform Gumroad --status ACTIVE
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # status
    sub.add_parser("status", help="Show all accounts with status and warmup day")

    # add
    add_p = sub.add_parser("add", help="Add a new account")
    add_p.add_argument("--platform", required=True, help="Platform name (Gumroad, Fiverr, etc.)")
    add_p.add_argument("--username", required=True, help="Handle or username")
    add_p.add_argument("--email", help="Email used for the account")
    add_p.add_argument("--status", default="CREATED", help="Initial status (default: CREATED)")
    add_p.add_argument("--niche", help="Niche (Meta, AI, Faith, Fitness, etc.)")
    add_p.add_argument("--proxy", help="Proxy used")
    add_p.add_argument("--profile", help="GoLogin profile name")
    add_p.add_argument("--date", help="Created date (YYYY-MM-DD, default: today)")
    add_p.add_argument("--notes", help="Notes")

    # warmup
    warmup_p = sub.add_parser("warmup", help="Show today's warmup tasks")
    warmup_p.add_argument("--platform", help="Platform name (or omit for all)")

    # blockers
    sub.add_parser("blockers", help="Show which revenue ops are blocked")

    # update
    update_p = sub.add_parser("update", help="Update account status")
    update_p.add_argument("--platform", required=True, help="Platform name")
    update_p.add_argument("--username", help="Handle (updates all platform accounts if omitted)")
    update_p.add_argument("--status", required=True,
                          help="New status (CREATED, WARMUP, ACTIVE, SUSPENDED, PENDING)")
    update_p.add_argument("--notes", help="Add notes")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "status": cmd_status,
        "add": cmd_add,
        "warmup": cmd_warmup,
        "blockers": cmd_blockers,
        "update": cmd_update,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
