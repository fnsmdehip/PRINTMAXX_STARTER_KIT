#!/usr/bin/env python3
"""
PRINTMAXX Product Launch Automator
Automates product submission to 86+ launch directories.
Generates submission copy, opens browser tabs, tracks status.

Usage:
  python3 AUTOMATIONS/product_launch_automator.py --status
  python3 AUTOMATIONS/product_launch_automator.py --launch --product focuslock-web
  python3 AUTOMATIONS/product_launch_automator.py --launch --product ALL --priority HIGHEST
  python3 AUTOMATIONS/product_launch_automator.py --generate-copy --product focuslock-web
  python3 AUTOMATIONS/product_launch_automator.py --open-tabs --product focuslock-web --priority HIGH
  python3 AUTOMATIONS/product_launch_automator.py --mark-submitted DIR001 DIR002 --product focuslock-web
  python3 AUTOMATIONS/product_launch_automator.py --checklist --product focuslock-web
"""

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
TRACKER_CSV = LEDGER / "LAUNCH_DIRECTORY_TRACKER.csv"
BUILDS_DIR = BASE / "MONEY_METHODS" / "APP_FACTORY" / "builds"

# ── product metadata (what we're launching) ────────────────────────────────

PRODUCTS = {
    "focuslock-web": {
        "name": "FocusLock",
        "tagline": "lock your phone. unlock your focus. productivity app that actually works.",
        "description": "FocusLock blocks distracting apps during focus sessions. set a timer, lock it in, get work done. no willpower needed. the app physically prevents you from opening TikTok/Instagram/Twitter until your session ends. 12,000+ focus sessions completed.",
        "url": "https://focuslock-app.surge.sh",
        "category": "Productivity",
        "pricing": "Free / $4.99/mo Pro",
        "tags": ["productivity", "focus", "app blocker", "screen time", "deep work"],
        "maker": "@PRINTMAXXER",
    },
    "habitforge-web": {
        "name": "HabitForge",
        "tagline": "build habits that stick. streak tracking meets accountability.",
        "description": "HabitForge helps you build and maintain habits with streak tracking, reminders, and visual progress. not another generic habit tracker. this one uses psychology-backed commitment devices. miss a streak? you lose your deposit. skin in the game.",
        "url": "https://habitforge-app.surge.sh",
        "category": "Productivity",
        "pricing": "Free / $3.99/mo Pro",
        "tags": ["habits", "streak tracking", "accountability", "self improvement"],
        "maker": "@PRINTMAXXER",
    },
    "mealmaxx-web": {
        "name": "MealMaxx",
        "tagline": "meal prep in 10 minutes. no thinking. just scan, plan, eat.",
        "description": "MealMaxx generates personalized meal plans based on your goals, preferences, and what's in your fridge. scan a barcode, get a recipe. track macros automatically. built for people who want to eat well without spending 2 hours planning.",
        "url": "https://mealmaxx-app.surge.sh",
        "category": "Health & Fitness",
        "pricing": "Free / $4.99/mo Pro",
        "tags": ["meal planning", "nutrition", "macro tracking", "recipes", "health"],
        "maker": "@PRINTMAXXER",
    },
    "sleepmaxx-web": {
        "name": "SleepMaxx",
        "tagline": "optimize your sleep. track what actually matters.",
        "description": "SleepMaxx tracks sleep quality, not just duration. monitors your sleep environment (light, noise, temperature), rates your sleep hygiene habits, and gives you a nightly score. the data tells you exactly what to fix. built by someone who went from 4hrs to 8hrs of quality sleep.",
        "url": "https://sleepmaxx-app.surge.sh",
        "category": "Health & Fitness",
        "pricing": "Free / $3.99/mo Pro",
        "tags": ["sleep", "health", "sleep tracking", "wellness", "optimization"],
        "maker": "@PRINTMAXXER",
    },
    "prayerlock-web": {
        "name": "PrayerLock",
        "tagline": "your daily prayer companion. structured devotion, zero distractions.",
        "description": "PrayerLock provides structured daily prayer sessions with guided devotions, scripture readings, and journaling. locks your phone during prayer time so you're fully present. supports multiple faith traditions. built for people who want deeper spiritual practice without phone interruptions.",
        "url": "https://prayerlock-web.surge.sh",
        "category": "Lifestyle",
        "pricing": "Free / $2.99/mo Premium",
        "tags": ["prayer", "faith", "devotion", "spiritual", "mindfulness"],
        "maker": "@PRINTMAXXER",
    },
    "walktounlock-web": {
        "name": "WalkToUnlock",
        "tagline": "your phone stays locked until you walk. no cheating.",
        "description": "WalkToUnlock requires you to hit a step count before unlocking your phone in the morning. set your target (500, 1000, 2000 steps). phone stays locked until you move. forces the morning walk habit. gamified with streaks, challenges, and leaderboards.",
        "url": "https://walktounlock-app.surge.sh",
        "category": "Health & Fitness",
        "pricing": "Free / $3.99/mo Pro",
        "tags": ["fitness", "walking", "morning routine", "gamification", "health"],
        "maker": "@PRINTMAXXER",
    },
}

# ── directory-specific submission guides ───────────────────────────────────

DIRECTORY_GUIDES = {
    "ProductHunt": {
        "submit_url": "https://www.producthunt.com/posts/new",
        "requires_account": True,
        "notes": "Schedule launch for Tuesday-Thursday. Need 5+ upvotes in first hour. Prepare hunter (can self-hunt). Add 3-5 images/GIFs. Write maker comment immediately after launch.",
        "fields": ["name", "tagline", "description", "url", "topics", "images"],
    },
    "HackerNews": {
        "submit_url": "https://news.ycombinator.com/submit",
        "requires_account": True,
        "notes": "Title format: 'Show HN: [Product Name] - [Short Description]'. Post between 8-10 AM ET. Don't ask for upvotes. Engage in comments honestly. HN hates marketing speak.",
        "fields": ["title", "url"],
        "title_format": "Show HN: {name} - {tagline}",
    },
    "Reddit": {
        "submit_url": "https://www.reddit.com/submit",
        "requires_account": True,
        "notes": "Post to r/SideProject, r/webdev, r/indiehackers, r/InternetIsBeautiful. Different subreddits need different angles. Be genuine, share the story. Reddit hates self-promo.",
        "fields": ["title", "url", "selftext"],
        "subreddits": ["r/SideProject", "r/webdev", "r/indiehackers", "r/InternetIsBeautiful", "r/androidapps"],
    },
    "BetaList": {
        "submit_url": "https://betalist.com/submit",
        "requires_account": True,
        "notes": "Free submission takes 2-4 weeks. Paid ($129) gets listed in 48 hours. Need logo, screenshots, description.",
        "fields": ["name", "tagline", "url", "description", "category"],
    },
    "MicroLaunch": {
        "submit_url": "https://microlaunch.net/submit",
        "requires_account": True,
        "notes": "Free to submit. Smaller community but engaged. Good for indie products.",
        "fields": ["name", "tagline", "url", "description"],
    },
    "Uneed": {
        "submit_url": "https://uneed.best/submit",
        "requires_account": True,
        "notes": "Free startup directory. Quick approval. Good for backlinks.",
        "fields": ["name", "url", "description", "category"],
    },
    "Fazier": {
        "submit_url": "https://fazier.com/submit",
        "requires_account": True,
        "notes": "Free to launch. Good for early-stage products. Community voting.",
        "fields": ["name", "tagline", "url", "description"],
    },
    "PeerList": {
        "submit_url": "https://peerlist.io/launch",
        "requires_account": True,
        "notes": "Professional community. Good for B2B/developer tools. Free to submit.",
        "fields": ["name", "url", "description", "category"],
    },
    "TinyLaunch": {
        "submit_url": "https://tinylaunch.com",
        "requires_account": True,
        "notes": "Small but active community. Free submission. Quick listing.",
        "fields": ["name", "tagline", "url"],
    },
    "IndieHackers": {
        "submit_url": "https://www.indiehackers.com/products/new",
        "requires_account": True,
        "notes": "Create a product page. Share revenue numbers (even $0). Community values transparency. Post milestones.",
        "fields": ["name", "url", "description", "revenue"],
    },
    "TinyStartups": {
        "submit_url": "https://tinystartups.com",
        "requires_account": False,
        "notes": "Directory for small startups. Free listing.",
        "fields": ["name", "url", "description"],
    },
    "SideProjectors": {
        "submit_url": "https://sideprojectors.com/submit",
        "requires_account": True,
        "notes": "Marketplace for side projects. Can list for sale or just showcase.",
        "fields": ["name", "url", "description", "category"],
    },
    "LaunchIgniter": {
        "submit_url": "https://launchigniter.com",
        "requires_account": True,
        "notes": "Free launch directory. Submit and get listed.",
        "fields": ["name", "tagline", "url"],
    },
    "Peerpush": {
        "submit_url": "https://peerpush.com",
        "requires_account": True,
        "notes": "Community-driven product launch platform.",
        "fields": ["name", "tagline", "url", "description"],
    },
    "DevHunt": {
        "submit_url": "https://devhunt.org",
        "requires_account": True,
        "notes": "GitHub-connected. Good for developer tools. Links to repo.",
        "fields": ["name", "url", "github_url", "description"],
    },
    "AILaunch": {
        "submit_url": "https://ailaunch.net",
        "requires_account": True,
        "notes": "AI-focused directory. Good for AI-powered products. Free submission.",
        "fields": ["name", "url", "description", "ai_features"],
    },
    "TheresAnAIForThat": {
        "submit_url": "https://theresanaiforthat.com/submit",
        "requires_account": True,
        "notes": "One of the largest AI directories. High traffic. Worth the effort.",
        "fields": ["name", "url", "description", "pricing", "category"],
    },
}


# ── core functions ─────────────────────────────────────────────────────────


def load_tracker() -> list:
    """Load the launch directory tracker CSV."""
    entries = []
    if not TRACKER_CSV.exists():
        print(f"ERROR: {TRACKER_CSV} not found")
        return entries
    with open(TRACKER_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries


def save_tracker(entries: list):
    """Save updated entries back to tracker CSV."""
    if not entries:
        return
    fieldnames = list(entries[0].keys())
    with open(TRACKER_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)


def generate_copy(product_id: str) -> dict:
    """Generate submission copy for a product."""
    product = PRODUCTS.get(product_id)
    if not product:
        return {"error": f"Unknown product: {product_id}"}

    return {
        "product_id": product_id,
        "name": product["name"],
        "tagline": product["tagline"],
        "description": product["description"],
        "url": product["url"],
        "category": product["category"],
        "pricing": product["pricing"],
        "tags": ", ".join(product["tags"]),
        "maker": product["maker"],
        "show_hn_title": f"Show HN: {product['name']} - {product['tagline']}",
        "reddit_title": f"{product['name']} - {product['tagline']}",
        "ph_tagline": product["tagline"][:60],  # PH tagline limit
    }


def show_status():
    """Show overall launch status."""
    entries = load_tracker()
    if not entries:
        print("No entries in launch tracker.")
        return

    products = sorted(set(e.get("product_id", "") for e in entries))
    priorities = ["HIGHEST", "HIGH", "MEDIUM", "LOW"]

    print("=" * 70)
    print("  PRINTMAXX PRODUCT LAUNCH STATUS")
    print("=" * 70)
    print(f"  Total entries: {len(entries)}")
    print(f"  Products: {len(products)}")
    print()

    # per-product breakdown
    for product in products:
        p_entries = [e for e in entries if e.get("product_id") == product]
        pending = sum(1 for e in p_entries if e.get("status") == "PENDING")
        submitted = sum(1 for e in p_entries if e.get("status") in ("SUBMITTED", "APPROVED"))
        total = len(p_entries)
        pct = ((total - pending) / total * 100) if total > 0 else 0

        display_name = PRODUCTS.get(product, {}).get("name", product)
        bar_len = 20
        filled = int(bar_len * (total - pending) / total) if total > 0 else 0
        bar = "#" * filled + "-" * (bar_len - filled)

        print(f"  {display_name:20s} [{bar}] {total - pending}/{total} ({pct:.0f}%)")

        for pri in priorities:
            pri_entries = [e for e in p_entries if e.get("priority") == pri]
            if pri_entries:
                pri_pending = sum(1 for e in pri_entries if e.get("status") == "PENDING")
                print(f"    {pri:10s}: {len(pri_entries) - pri_pending}/{len(pri_entries)} submitted")
        print()

    # action items
    print("-" * 70)
    print("  NEXT ACTIONS:")
    highest_pending = [
        e for e in entries
        if e.get("priority") == "HIGHEST" and e.get("status") == "PENDING"
    ]
    if highest_pending:
        products_with_highest = sorted(set(e.get("product_id", "") for e in highest_pending))
        print(f"  {len(highest_pending)} HIGHEST priority submissions pending across {len(products_with_highest)} products")
        for pid in products_with_highest[:3]:
            count = sum(1 for e in highest_pending if e.get("product_id") == pid)
            name = PRODUCTS.get(pid, {}).get("name", pid)
            print(f"    > {name}: {count} HIGHEST directories waiting")
    print(f"\n  Run: python3 {__file__} --launch --product <name> --priority HIGHEST")
    print("=" * 70)


def generate_checklist(product_id: str):
    """Generate a step-by-step submission checklist for a product."""
    product = PRODUCTS.get(product_id)
    if not product:
        print(f"Unknown product: {product_id}")
        return

    entries = load_tracker()
    p_entries = [e for e in entries if e.get("product_id") == product_id and e.get("status") == "PENDING"]

    print("=" * 70)
    print(f"  LAUNCH CHECKLIST: {product['name']}")
    print("=" * 70)
    print(f"  URL: {product['url']}")
    print(f"  Tagline: {product['tagline']}")
    print(f"  {len(p_entries)} directories pending")
    print()

    for priority in ["HIGHEST", "HIGH", "MEDIUM", "LOW"]:
        group = [e for e in p_entries if e.get("priority") == priority]
        if not group:
            continue

        print(f"  --- {priority} PRIORITY ({len(group)} directories) ---")
        print()
        for i, e in enumerate(group, 1):
            dir_name = e.get("directory_name", "")
            dir_url = e.get("directory_url", "")
            guide = DIRECTORY_GUIDES.get(dir_name, {})

            submit_url = guide.get("submit_url", dir_url)
            notes = guide.get("notes", "Submit product details on the website.")
            needs_account = guide.get("requires_account", True)

            print(f"  [{i}] {dir_name}")
            print(f"      URL: {submit_url}")
            if needs_account:
                print(f"      [!] Requires account signup first")
            print(f"      Steps:")
            print(f"        1. Open {submit_url}")
            if needs_account:
                print(f"        2. Create account / sign in")
                print(f"        3. Fill in product details:")
            else:
                print(f"        2. Fill in product details:")
            print(f"           Name: {product['name']}")
            print(f"           Tagline: {product['tagline']}")
            print(f"           URL: {product['url']}")
            print(f"           Category: {product['category']}")
            if guide.get("title_format"):
                print(f"           Title: {guide['title_format'].format(**product)}")
            print(f"      Notes: {notes}")
            print()


def open_tabs(product_id: str, priority: str = None):
    """Open browser tabs for all pending directories."""
    entries = load_tracker()
    p_entries = [
        e for e in entries
        if e.get("product_id") == product_id and e.get("status") == "PENDING"
    ]
    if priority:
        p_entries = [e for e in p_entries if e.get("priority") == priority]

    if not p_entries:
        print(f"No pending directories for {product_id}" + (f" at {priority} priority" if priority else ""))
        return

    print(f"Opening {len(p_entries)} tabs for {product_id}...")
    for e in p_entries:
        dir_name = e.get("directory_name", "")
        guide = DIRECTORY_GUIDES.get(dir_name, {})
        url = guide.get("submit_url", e.get("directory_url", ""))
        if url:
            print(f"  > {dir_name}: {url}")
            subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.5)

    print(f"\nOpened {len(p_entries)} tabs. Submit products, then run:")
    dir_ids = " ".join(e.get("directory_id", "") for e in p_entries)
    print(f"  python3 {__file__} --mark-submitted {dir_ids} --product {product_id}")


def mark_submitted(product_id: str, dir_ids: list):
    """Mark directories as submitted."""
    entries = load_tracker()
    now = datetime.now().strftime("%Y-%m-%d")
    updated = 0

    for entry in entries:
        if entry.get("product_id") == product_id and entry.get("directory_id") in dir_ids:
            entry["status"] = "SUBMITTED"
            entry["submitted_date"] = now
            updated += 1

    save_tracker(entries)
    print(f"Marked {updated} directories as SUBMITTED for {product_id}")


def launch_product(product_id: str, priority: str = None):
    """Full launch sequence: generate copy, show checklist, open tabs."""
    if product_id == "ALL":
        products = list(PRODUCTS.keys())
    else:
        products = [product_id]

    for pid in products:
        product = PRODUCTS.get(pid)
        if not product:
            print(f"Unknown product: {pid}. Available: {', '.join(PRODUCTS.keys())}")
            continue

        copy = generate_copy(pid)

        print("=" * 70)
        print(f"  LAUNCHING: {product['name']}")
        print("=" * 70)
        print()
        print(f"  Copy to clipboard:")
        print(f"  Name:      {copy['name']}")
        print(f"  Tagline:   {copy['tagline']}")
        print(f"  URL:       {copy['url']}")
        print(f"  Category:  {copy['category']}")
        print(f"  Pricing:   {copy['pricing']}")
        print(f"  Tags:      {copy['tags']}")
        print(f"  Maker:     {copy['maker']}")
        print()
        print(f"  Description (copy this):")
        print(f"  {copy['description']}")
        print()
        print(f"  Show HN title: {copy['show_hn_title']}")
        print(f"  PH tagline:    {copy['ph_tagline']}")
        print()

        # copy main description to clipboard
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(input=copy["description"].encode())
            print("  [Description copied to clipboard]")
        except Exception:
            pass

        # open tabs
        open_tabs(pid, priority)
        print()


def generate_copy_file(product_id: str):
    """Generate a submission copy markdown file."""
    copy = generate_copy(product_id)
    if "error" in copy:
        print(copy["error"])
        return

    output_path = OPS / f"LAUNCH_COPY_{product_id.upper()}.md"
    product = PRODUCTS[product_id]

    lines = [
        f"# Launch Copy: {product['name']}",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## Core Details",
        f"- **Name:** {product['name']}",
        f"- **Tagline:** {product['tagline']}",
        f"- **URL:** {product['url']}",
        f"- **Category:** {product['category']}",
        f"- **Pricing:** {product['pricing']}",
        f"- **Tags:** {', '.join(product['tags'])}",
        f"- **Maker:** {product['maker']}",
        f"",
        f"## Description (copy-paste)",
        f"",
        f"{product['description']}",
        f"",
        f"## Platform-Specific Titles",
        f"",
        f"**Product Hunt tagline (60 char):** {product['tagline'][:60]}",
        f"**Hacker News:** Show HN: {product['name']} - {product['tagline']}",
        f"**Reddit:** {product['name']} - {product['tagline']}",
        f"",
        f"## Submission URLs (in priority order)",
        f"",
    ]

    entries = load_tracker()
    p_entries = [e for e in entries if e.get("product_id") == product_id]
    for priority in ["HIGHEST", "HIGH", "MEDIUM", "LOW"]:
        group = [e for e in p_entries if e.get("priority") == priority]
        if group:
            lines.append(f"### {priority}")
            for e in group:
                status = e.get("status", "PENDING")
                icon = "[x]" if status != "PENDING" else "[ ]"
                name = e.get("directory_name", "")
                url = e.get("directory_url", "")
                guide = DIRECTORY_GUIDES.get(name, {})
                submit = guide.get("submit_url", url)
                lines.append(f"- {icon} **{name}**: {submit}")
                if guide.get("notes"):
                    lines.append(f"  - Notes: {guide['notes']}")
            lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"Generated: {output_path}")
    subprocess.Popen(["open", str(output_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ── CLI ────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Product Launch Automator")
    parser.add_argument("--status", action="store_true", help="Show launch status")
    parser.add_argument("--launch", action="store_true", help="Launch product (generate copy + open tabs)")
    parser.add_argument("--product", type=str, help="Product ID (e.g., focuslock-web) or ALL")
    parser.add_argument("--priority", type=str, help="Filter by priority (HIGHEST/HIGH/MEDIUM/LOW)")
    parser.add_argument("--generate-copy", action="store_true", help="Generate submission copy markdown")
    parser.add_argument("--open-tabs", action="store_true", help="Open browser tabs for pending directories")
    parser.add_argument("--mark-submitted", nargs="+", help="Mark directory IDs as submitted")
    parser.add_argument("--checklist", action="store_true", help="Generate step-by-step checklist")
    parser.add_argument("--list-products", action="store_true", help="List all products")

    args = parser.parse_args()

    if args.list_products:
        print("Available products:")
        for pid, p in PRODUCTS.items():
            print(f"  {pid:25s} {p['name']:15s} {p['url']}")
        return

    if args.status:
        show_status()
        return

    if args.launch:
        if not args.product:
            print("ERROR: --product required. Use --list-products to see options.")
            return
        launch_product(args.product, args.priority)
        return

    if args.generate_copy:
        if not args.product:
            print("ERROR: --product required")
            return
        generate_copy_file(args.product)
        return

    if args.open_tabs:
        if not args.product:
            print("ERROR: --product required")
            return
        open_tabs(args.product, args.priority)
        return

    if args.mark_submitted:
        if not args.product:
            print("ERROR: --product required")
            return
        mark_submitted(args.product, args.mark_submitted)
        return

    if args.checklist:
        if not args.product:
            print("ERROR: --product required")
            return
        generate_checklist(args.product)
        return

    # default: show status
    show_status()


if __name__ == "__main__":
    main()
