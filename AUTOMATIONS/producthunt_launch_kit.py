#!/usr/bin/env python3
"""
Product Hunt Launch Kit — fills N53 gap
Generates complete PH launch packages for PRINTMAXX apps.
Top 5 daily = 3K-10K visitors in 24 hours. FREE.

Usage:
    python3 producthunt_launch_kit.py --generate APP_NAME    # Generate launch kit for app
    python3 producthunt_launch_kit.py --list                 # List all apps ready for PH
    python3 producthunt_launch_kit.py --schedule             # Show optimal launch schedule
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAUNCH_DIR = PROJECT_ROOT / "CONTENT" / "producthunt_launches"
LAUNCH_DIR.mkdir(parents=True, exist_ok=True)

# Apps ready for Product Hunt launch, ranked by PH-fit
LAUNCHABLE_APPS = {
    "invoiceforge": {
        "name": "InvoiceForge",
        "tagline": "Free invoice generator for tradespeople. No signup, no subscription.",
        "url": "https://invoiceforge.surge.sh",
        "category": "Productivity",
        "topics": ["Free", "Invoice", "Small Business", "No Code", "PWA"],
        "ph_fit_score": 95,
        "reason": "Free tools crush on PH. Trade-specific angle is unique. Privacy-first (no data leaves device) is a strong hook.",
        "first_comment": """hey PH! built this because most invoice tools charge $15-30/mo for what is fundamentally a PDF generator with math.

InvoiceForge is:
- completely free, forever
- no signup, no account
- runs 100% in your browser
- your data never leaves your device
- trade-specific templates (plumber, electrician, HVAC, contractor, landscaper)
- PDF export + Stripe payment links
- works offline (PWA)

built it with Claude Code in a weekend. the entire app is a single HTML file under 100KB.

would love feedback on what templates/features tradespeople actually need.""",
    },
    "pdfmaxx": {
        "name": "PDFMaxx",
        "tagline": "Free PDF toolkit. Merge, split, compress. Everything stays in your browser.",
        "url": "https://pdfmaxx.surge.sh",
        "category": "Productivity",
        "topics": ["Free", "PDF", "Privacy", "No Code", "Tools"],
        "ph_fit_score": 90,
        "reason": "PDF tools always do well on PH. Privacy angle (no upload) differentiates from iLovePDF etc.",
        "first_comment": """built PDFMaxx because every PDF tool either:
1. uploads your files to their servers (privacy nightmare)
2. charges a subscription for basic operations
3. shows 47 ads before you can merge 2 files

PDFMaxx runs entirely in your browser. your files never leave your device. zero cost, zero tracking, zero BS.

merge, split, compress, extract pages, rearrange. single HTML file, works offline.

the bar was genuinely on the ground for PDF tools.""",
    },
    "pagescorer": {
        "name": "PageScorer",
        "tagline": "Audit any website in 30 seconds. Free, instant, no signup.",
        "url": "https://pagescorer.surge.sh",
        "category": "SEO",
        "topics": ["SEO", "Website Audit", "Free", "Developer Tools", "Marketing"],
        "ph_fit_score": 88,
        "reason": "Dev tools + SEO tools both perform well on PH. Instant results = great demo.",
        "first_comment": """PageScorer gives you a full website audit in 30 seconds.

checks: mobile responsiveness, load speed, SSL, meta tags, SEO basics, accessibility, performance score.

paste any URL, get a report. no account, no limit, no cost.

built this for the local biz website redesign service i run — i needed a quick way to show business owners what's wrong with their current site. then realized the tool itself was useful enough to share.

feedback welcome, especially from SEO folks.""",
    },
    "stackmaxx": {
        "name": "StackMaxx",
        "tagline": "Find your perfect tech stack. Compare tools, calculate costs, export.",
        "url": "https://stackmaxx.surge.sh",
        "category": "Developer Tools",
        "topics": ["Developer Tools", "SaaS", "Tech Stack", "Comparison", "Free"],
        "ph_fit_score": 85,
        "reason": "Tech stack tools resonate with PH audience (devs, founders). Comparison angle is engaging.",
        "first_comment": """every solopreneur and startup spends hours researching their tech stack. StackMaxx puts it all in one place.

compare hosting, auth, payments, email, analytics — see pricing tiers side by side. calculate your total monthly cost. export your stack as a shareable card.

free, no signup, runs in your browser.

built it because i was tired of opening 30 tabs to compare Supabase vs Firebase vs PocketBase for the 5th time.""",
    },
    "focuslock-web": {
        "name": "FocusLock",
        "tagline": "Glassmorphism Pomodoro timer with ambient sounds. Free PWA.",
        "url": "https://focuslock-web.surge.sh",
        "category": "Productivity",
        "topics": ["Pomodoro", "Productivity", "Focus", "PWA", "Free"],
        "ph_fit_score": 82,
        "reason": "Pomodoro tools always get attention. Glassmorphism design is visually appealing for screenshots.",
        "first_comment": """another pomodoro timer? yeah but this one doesn't suck.

FocusLock has:
- glassmorphism UI (actually looks good)
- ambient sounds via Web Audio API (rain, cafe, white noise — no audio files)
- drag-and-drop task management
- session analytics with charts
- works offline as a PWA
- zero subscriptions, zero accounts

the entire app is a single 66KB HTML file. installs on your phone like a native app.

built with vanilla JS. no React, no frameworks, no build step. view source to see everything.""",
    },
    "prospectmaxx": {
        "name": "ProspectMaxx",
        "tagline": "Free lead scoring tool. Score any business website in seconds.",
        "url": "https://prospectmaxx.surge.sh",
        "category": "Sales",
        "topics": ["Sales", "Lead Generation", "B2B", "Free", "Small Business"],
        "ph_fit_score": 80,
        "reason": "Sales tools do well on PH. Lead scoring is a pain point for SMBs.",
        "first_comment": """ProspectMaxx scores any business website on 12 criteria:
mobile responsiveness, load speed, SSL cert, design freshness, SEO basics, social presence, review count, business hours listed, and more.

the score tells you how likely they are to need your services.

built this for my web design outreach — instead of cold emailing randomly, i score 100 websites and only reach out to the bottom 20. close rate went from 2% to 12%.

free, no signup, no limits.""",
    },
}

# PH launch timing optimization
LAUNCH_SCHEDULE = {
    "best_days": ["Tuesday", "Wednesday", "Thursday"],
    "best_time": "12:01 AM PT (launch goes live at midnight PT)",
    "avoid": ["Monday (too crowded)", "Friday-Sunday (lower traffic)"],
    "spacing": "2-3 weeks between launches (avoid fatigue)",
    "optimal_cadence": "2 launches per month",
}


def generate_launch_kit(app_key):
    """Generate complete PH launch package for an app."""
    if app_key not in LAUNCHABLE_APPS:
        print(f"App '{app_key}' not found. Available: {', '.join(LAUNCHABLE_APPS.keys())}")
        return

    app = LAUNCHABLE_APPS[app_key]
    kit_dir = LAUNCH_DIR / app_key
    kit_dir.mkdir(exist_ok=True)

    # Generate launch kit
    kit = {
        "app": app_key,
        "name": app["name"],
        "tagline": app["tagline"],
        "url": app["url"],
        "category": app["category"],
        "topics": app["topics"],
        "ph_fit_score": app["ph_fit_score"],
        "generated": datetime.now().isoformat(),
    }

    # Write launch brief
    brief = f"""# {app['name']} — Product Hunt Launch Kit

## Quick Facts
- **Tagline:** {app['tagline']}
- **URL:** {app['url']}
- **Category:** {app['category']}
- **Topics:** {', '.join(app['topics'])}
- **PH Fit Score:** {app['ph_fit_score']}/100
- **Why it works on PH:** {app['reason']}

## Launch Checklist

### Pre-Launch (1 week before)
- [ ] Create PH maker profile (if not exists)
- [ ] Prepare 4 screenshots (1200x900 each)
  - Screenshot 1: Hero view (main feature)
  - Screenshot 2: Key feature closeup
  - Screenshot 3: Mobile responsive view
  - Screenshot 4: Unique differentiator
- [ ] Record 30-second demo GIF or video
- [ ] Prepare first comment (below)
- [ ] Line up 10 supporters for launch day upvotes
- [ ] Schedule tweets for launch day (3 minimum)
- [ ] Write Reddit posts for relevant subreddits

### Launch Day
- [ ] Submit at 12:01 AM PT (goes live immediately)
- [ ] Post first comment immediately after submission
- [ ] Tweet announcement with PH link
- [ ] Post in relevant subreddits
- [ ] Reply to every PH comment within 1 hour
- [ ] Share in Discord/Slack communities
- [ ] Update Twitter bio with PH link for 24hrs

### Post-Launch (24-48hrs after)
- [ ] Screenshot final ranking
- [ ] Write "lessons learned" thread for Twitter
- [ ] Update app landing page with "Featured on Product Hunt" badge
- [ ] Follow up with everyone who commented
- [ ] If top 5: add PH badge to all marketing materials

## First Comment (Post Immediately After Submission)

{app['first_comment']}

## Twitter Announcement Templates

### Tweet 1 (Launch Announcement)
just launched {app['name']} on Product Hunt.

{app['tagline'].lower()}

would appreciate your support: [PH LINK]

### Tweet 2 (Why I Built This)
built {app['name']} because the existing tools either cost $30/mo or upload your data to their servers.

this one is free, runs in your browser, and your data never leaves your device.

live on Product Hunt today: [PH LINK]

### Tweet 3 (Social Proof — Post After Getting Upvotes)
{app['name']} just hit top [X] on Product Hunt.

[specific stat, e.g., "200 upvotes in 4 hours"]

if you haven't checked it out: {app['url']}

## Reddit Posts

### r/SideProject
Title: I built {app['name']} — {app['tagline'].lower()}

[Include 3-4 sentences about what it does, why you built it, tech stack (single HTML file, vanilla JS, PWA). End with link.]

### r/webdev
Title: Built a full PWA as a single HTML file — {app['name']}

[Focus on the technical angle: single-file architecture, no frameworks, offline-capable, Web APIs used. Devs love this angle.]

## Optimal Launch Window
- **Best day:** {', '.join(LAUNCH_SCHEDULE['best_days'])}
- **Time:** {LAUNCH_SCHEDULE['best_time']}
- **Avoid:** {', '.join(LAUNCH_SCHEDULE['avoid'])}
"""

    with open(kit_dir / "LAUNCH_KIT.md", "w") as f:
        f.write(brief)

    with open(kit_dir / "launch_data.json", "w") as f:
        json.dump(kit, f, indent=2)

    print(f"Launch kit generated for {app['name']} at {kit_dir}/")
    print(f"  PH Fit Score: {app['ph_fit_score']}/100")
    print(f"  Tagline: {app['tagline']}")
    print(f"  Files: LAUNCH_KIT.md, launch_data.json")


def list_apps():
    """List all apps ready for PH launch, ranked by fit score."""
    print("\n=== Product Hunt Launchable Apps ===\n")
    sorted_apps = sorted(LAUNCHABLE_APPS.items(), key=lambda x: -x[1]["ph_fit_score"])
    for i, (key, app) in enumerate(sorted_apps, 1):
        existing = (LAUNCH_DIR / key / "LAUNCH_KIT.md").exists()
        status = "KIT READY" if existing else "NEEDS KIT"
        print(f"  {i}. [{app['ph_fit_score']}] {app['name']} — {app['tagline'][:50]}... [{status}]")

    print(f"\nTotal: {len(LAUNCHABLE_APPS)} apps ready for PH launch")
    print(f"Optimal cadence: {LAUNCH_SCHEDULE['optimal_cadence']}")
    print(f"Best days: {', '.join(LAUNCH_SCHEDULE['best_days'])}")


def show_schedule():
    """Generate optimal launch schedule for next 3 months."""
    print("\n=== Suggested PH Launch Schedule ===\n")
    sorted_apps = sorted(LAUNCHABLE_APPS.items(), key=lambda x: -x[1]["ph_fit_score"])

    launch_date = datetime.now()
    # Find next Tuesday
    while launch_date.strftime("%A") != "Tuesday":
        launch_date += timedelta(days=1)

    for i, (key, app) in enumerate(sorted_apps):
        print(f"  {launch_date.strftime('%b %d (%A)')}: {app['name']} [Score: {app['ph_fit_score']}]")
        launch_date += timedelta(weeks=2)  # 2 weeks between launches

    print(f"\n6 launches over 12 weeks = ~30K-60K total visitors (conservative)")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--generate" in args:
        idx = args.index("--generate")
        if idx + 1 < len(args):
            generate_launch_kit(args[idx + 1])
        else:
            # Generate all
            for app_key in LAUNCHABLE_APPS:
                generate_launch_kit(app_key)
    elif "--list" in args:
        list_apps()
    elif "--schedule" in args:
        show_schedule()
    else:
        print("Usage:")
        print("  producthunt_launch_kit.py --generate APP_NAME  # Generate launch kit")
        print("  producthunt_launch_kit.py --generate           # Generate ALL kits")
        print("  producthunt_launch_kit.py --list               # List launchable apps")
        print("  producthunt_launch_kit.py --schedule           # Show optimal schedule")
