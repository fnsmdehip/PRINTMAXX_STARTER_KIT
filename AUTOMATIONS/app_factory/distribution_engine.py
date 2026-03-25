#!/usr/bin/env python3
"""App Factory Distribution Engine.

Automates app distribution across channels:
  - App Store screenshots from HTML templates (Playwright)
  - ASO keywords from description + competitor analysis
  - Social media launch posts (Twitter, Reddit, Product Hunt)
  - Influencer outreach email drafts
  - Distribution tracking per app

Usage:
  python3 AUTOMATIONS/app_factory/distribution_engine.py --plan APP_DIR
  python3 AUTOMATIONS/app_factory/distribution_engine.py --generate-posts APP_DIR
  python3 AUTOMATIONS/app_factory/distribution_engine.py --generate-screenshots APP_DIR
  python3 AUTOMATIONS/app_factory/distribution_engine.py --generate-aso APP_DIR
  python3 AUTOMATIONS/app_factory/distribution_engine.py --full APP_DIR
  python3 AUTOMATIONS/app_factory/distribution_engine.py --help
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
BUILDS_DIR = PROJECT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
CONTENT_DIR = PROJECT / "CONTENT" / "social"
POSTING_QUEUE = CONTENT_DIR / "posting_queue"
LOG_DIR = AUTOMATIONS / "app_factory" / "logs"
DIST_DIR = AUTOMATIONS / "app_factory" / "distribution"
SCREENSHOTS_DIR = PROJECT / "MEDIA" / "generated_images" / "app_screenshots"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DIST_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

LOGFILE = LOG_DIR / "distribution_engine.log"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# App Info Loader
# ---------------------------------------------------------------------------
def load_app_info(app_dir: Path) -> dict[str, Any] | None:
    """Load app info from app.json and niche config."""
    app_json_path = app_dir / "app.json"
    if not app_json_path.exists():
        log(f"ERROR: No app.json in {app_dir}")
        return None

    with open(app_json_path) as f:
        app_json = json.load(f)

    expo = app_json.get("expo", {})
    name = expo.get("name", "")
    slug = expo.get("slug", "")

    # Try to detect niche from source files
    niche = _detect_niche(app_dir)

    return {
        "name": name,
        "slug": slug,
        "bundle_id": expo.get("ios", {}).get("bundleIdentifier", ""),
        "niche": niche,
        "app_dir": str(app_dir),
    }


def _detect_niche(app_dir: Path) -> str:
    """Detect app niche from source code and config."""
    # Check for niche keywords in source files
    niche_signals: dict[str, int] = {}
    keywords_map = {
        "Health & Fitness": ["workout", "exercise", "fitness", "gym", "pushup", "plank"],
        "Wellness": ["meditation", "mindfulness", "breathing", "calm", "sleep"],
        "Religious/Spiritual": ["prayer", "bible", "quran", "faith", "scripture"],
        "Productivity": ["habit", "focus", "productivity", "routine", "streak"],
        "Education": ["study", "learn", "reading", "language", "quiz"],
        "Food & Health": ["water", "fasting", "nutrition", "meal", "calorie"],
        "Mental Health": ["mood", "gratitude", "journal", "anxiety"],
        "Finance": ["budget", "saving", "expense", "money"],
    }

    tsx_files = list(app_dir.rglob("*.tsx"))
    tsx_files = [f for f in tsx_files if "node_modules" not in str(f)]

    for f in tsx_files[:10]:
        try:
            content = f.read_text(errors="replace").lower()
            for niche, kws in keywords_map.items():
                for kw in kws:
                    if kw in content:
                        niche_signals[niche] = niche_signals.get(niche, 0) + 1
        except Exception:
            continue

    if niche_signals:
        return max(niche_signals, key=niche_signals.get)  # type: ignore[arg-type]
    return "General"


# ---------------------------------------------------------------------------
# ASO Keywords Generator
# ---------------------------------------------------------------------------
def generate_aso_keywords(app_info: dict) -> dict[str, Any]:
    """Generate ASO keywords based on app name, niche, and competitive analysis."""
    name = app_info.get("name", "")
    niche = app_info.get("niche", "General")

    # Core keywords from app name
    name_words = [w.lower() for w in re.findall(r'[A-Za-z]+', name) if len(w) > 2]

    # Niche-specific high-volume keywords
    niche_keywords: dict[str, list[str]] = {
        "Health & Fitness": [
            "workout tracker", "fitness streak", "exercise log", "gym habit",
            "daily workout", "fitness goals", "health tracker", "exercise streak",
            "workout planner", "fitness motivation", "body tracker",
        ],
        "Wellness": [
            "meditation app", "mindfulness tracker", "calm app", "sleep tracker",
            "breathing exercises", "stress relief", "daily meditation",
            "wellness journal", "relaxation app", "mental wellness",
        ],
        "Religious/Spiritual": [
            "prayer tracker", "bible reading", "daily devotion", "faith app",
            "scripture daily", "prayer journal", "spiritual growth",
            "church app", "worship tracker", "bible study plan",
        ],
        "Productivity": [
            "habit tracker", "daily routine", "streak counter", "goal tracker",
            "productivity app", "habit builder", "daily goals", "routine planner",
            "task tracker", "self improvement", "discipline tracker",
        ],
        "Education": [
            "study tracker", "learning app", "study streak", "education planner",
            "study timer", "learning goals", "daily study", "student planner",
        ],
        "Food & Health": [
            "water tracker", "fasting app", "nutrition log", "diet tracker",
            "water reminder", "meal planner", "healthy eating", "calorie counter",
        ],
        "Mental Health": [
            "mood tracker", "gratitude journal", "mental health app",
            "daily journal", "anxiety relief", "mood diary", "self care app",
        ],
        "Finance": [
            "budget tracker", "savings app", "money habit", "expense tracker",
            "financial goals", "no spend tracker", "savings challenge",
        ],
    }

    # Combine and deduplicate
    keywords = list(set(
        name_words +
        niche_keywords.get(niche, ["habit tracker", "daily streak", "goal tracker"])
    ))

    # Generate subtitle suggestions (30 char max for App Store)
    subtitles = []
    if niche == "Health & Fitness":
        subtitles = ["Track Your Fitness Streak", "Daily Workout Habits", "Build Exercise Habits"]
    elif niche == "Wellness":
        subtitles = ["Daily Calm & Mindfulness", "Build Your Peace Habit", "Meditation Made Simple"]
    elif niche == "Religious/Spiritual":
        subtitles = ["Daily Faith Habits", "Grow Your Spiritual Life", "Prayer & Scripture Daily"]
    elif niche == "Productivity":
        subtitles = ["Build Better Habits Daily", "Track Your Streaks", "Achieve Your Goals"]
    else:
        subtitles = ["Build Better Habits", "Track Daily Streaks", "Reach Your Goals"]

    # Description template
    description = _generate_app_description(app_info, niche)

    return {
        "keywords": keywords[:100],  # App Store limit: 100 chars total
        "keyword_string": ", ".join(keywords[:15]),
        "subtitles": subtitles,
        "description": description,
        "promotional_text": f"Start building {niche.lower()} habits today. Track your streak and stay motivated.",
    }


def _generate_app_description(app_info: dict, niche: str) -> str:
    """Generate App Store description."""
    name = app_info.get("name", "This app")
    return f"""{name} helps you build consistent {niche.lower()} habits through daily streak tracking.

KEY FEATURES:
- Track multiple daily habits with streak counters
- Beautiful dark mode interface designed for focus
- Customizable reminders to stay on track
- Progress statistics and trend analysis
- Celebrate milestones and achievements

WHY STREAKS WORK:
Research shows that habit streaks create powerful motivation loops. Seeing your streak grow makes you want to keep going. {name} makes it easy to build and maintain the habits that matter most to you.

PREMIUM FEATURES:
- Unlimited habit tracking
- Advanced analytics and insights
- Custom categories and organization
- Data export
- Priority support

Start your free trial today and build the habits that change your life.

SUBSCRIPTION INFORMATION:
- Payment will be charged to your Apple ID account at confirmation of purchase
- Subscription automatically renews unless canceled at least 24 hours before the end of the current period
- You can manage and cancel subscriptions in your Account Settings
- Privacy Policy: https://printmaxx.io/privacy
- Terms of Use: https://printmaxx.io/terms"""


# ---------------------------------------------------------------------------
# Social Media Post Generator
# ---------------------------------------------------------------------------
def generate_launch_posts(app_info: dict) -> dict[str, list[dict]]:
    """Generate social media launch posts for all platforms."""
    name = app_info.get("name", "Our App")
    niche = app_info.get("niche", "productivity")

    posts: dict[str, list[dict]] = {"twitter": [], "reddit": [], "producthunt": []}

    # Twitter posts
    posts["twitter"] = [
        {
            "platform": "twitter",
            "type": "launch_announcement",
            "content": f"Just shipped {name} on the App Store.\n\nA simple streak tracker for {niche.lower()} habits.\n\nNo bloat. No social features you didn't ask for. Just track your habits and watch the streak grow.\n\nLink in bio.",
            "timing": "launch_day",
        },
        {
            "platform": "twitter",
            "type": "builder_story",
            "content": f"Built {name} in a weekend because every {niche.lower()} app I tried was either:\n\n- Bloated with features\n- Ugly UI\n- $15/month for a streak counter\n\nSo I built one that does exactly what you need.\n\nDark mode. Clean design. Actually affordable.\n\nFree to try.",
            "timing": "launch_day+1",
        },
        {
            "platform": "twitter",
            "type": "feature_highlight",
            "content": f"The psychology behind {name}:\n\n1. Start small (1 habit)\n2. See the streak grow\n3. Feel the momentum\n4. Add more habits\n5. Watch your life change\n\nSimple system. Real results.\n\nDownload free on the App Store.",
            "timing": "launch_day+3",
        },
    ]

    # Reddit posts
    subreddits = _get_target_subreddits(niche)
    for sub in subreddits[:3]:
        posts["reddit"].append({
            "platform": "reddit",
            "subreddit": sub,
            "type": "value_post",
            "title": f"I built a simple {niche.lower()} habit tracker because nothing else worked for me",
            "content": f"I kept trying different {niche.lower()} apps and they were all either too complicated or too expensive for what they do.\n\nSo I built {name} -- it does one thing well: tracks your daily habits with a streak counter.\n\nDark mode, clean UI, and it actually helps you stay consistent.\n\nWould love feedback from this community. What features would make your ideal habit tracker?",
            "timing": "launch_week",
        })

    # Product Hunt
    posts["producthunt"] = [
        {
            "platform": "producthunt",
            "type": "launch",
            "tagline": f"Simple streak tracking for {niche.lower()} habits",
            "description": f"{name} helps you build consistent daily habits through the power of streak tracking. Dark mode, clean design, and actually affordable.",
            "maker_comment": f"Hey PH! I built {name} because I was frustrated with how complicated habit trackers have gotten. This one does exactly what you need -- tracks your daily habits and shows you your streak. The psychology of not wanting to break a streak is powerful. Would love your feedback!",
            "timing": "tuesday_or_wednesday",
        },
    ]

    return posts


def _get_target_subreddits(niche: str) -> list[str]:
    """Get target subreddits for a niche."""
    subreddit_map: dict[str, list[str]] = {
        "Health & Fitness": ["Fitness", "loseit", "bodyweightfitness", "getdisciplined"],
        "Wellness": ["Meditation", "mindfulness", "selfimprovement", "getdisciplined"],
        "Religious/Spiritual": ["Christianity", "Islam", "Buddhism", "spirituality"],
        "Productivity": ["productivity", "getdisciplined", "selfimprovement", "DecidingToBeBetter"],
        "Education": ["GetStudying", "learnprogramming", "languagelearning"],
        "Food & Health": ["intermittentfasting", "MealPrepSunday", "EatCheapAndHealthy"],
        "Mental Health": ["mentalhealth", "anxiety", "selfimprovement", "DecidingToBeBetter"],
        "Finance": ["personalfinance", "FinancialPlanning", "Frugal"],
    }
    return subreddit_map.get(niche, ["SideProject", "indiehackers", "AppIdeas"])


# ---------------------------------------------------------------------------
# Screenshot Generator (HTML templates)
# ---------------------------------------------------------------------------
def generate_screenshot_html(app_info: dict, aso: dict) -> list[dict]:
    """Generate HTML templates for App Store screenshots."""
    name = app_info.get("name", "App")
    niche = app_info.get("niche", "General")

    # Standard iPhone screenshot dimensions: 1290x2796 (6.7"), 1242x2208 (5.5")
    screenshots = []

    # Screenshot 1: Hero / Value prop
    screenshots.append({
        "name": "01_hero",
        "title": f"Build Better {niche} Habits",
        "subtitle": "Track your daily streaks",
        "html": _screenshot_template(
            name, f"Build Better\\n{niche} Habits",
            "Track your daily streaks and stay motivated",
            "#1a1a2e", app_info,
        ),
    })

    # Screenshot 2: Streak counter
    screenshots.append({
        "name": "02_streak",
        "title": "Watch Your Streak Grow",
        "subtitle": "Every day counts",
        "html": _screenshot_template(
            name, "Watch Your\\nStreak Grow",
            "Stay consistent and build momentum",
            "#0d1117", app_info,
        ),
    })

    # Screenshot 3: Multiple habits
    screenshots.append({
        "name": "03_habits",
        "title": "Track Multiple Habits",
        "subtitle": "All in one place",
        "html": _screenshot_template(
            name, "Track Multiple\\nHabits at Once",
            "Customize your daily routine",
            "#1a0a1e", app_info,
        ),
    })

    # Screenshot 4: Analytics
    screenshots.append({
        "name": "04_analytics",
        "title": "See Your Progress",
        "subtitle": "Beautiful analytics",
        "html": _screenshot_template(
            name, "Beautiful\\nProgress Analytics",
            "Understand your habits over time",
            "#0a1628", app_info,
        ),
    })

    # Screenshot 5: Reminders
    screenshots.append({
        "name": "05_reminders",
        "title": "Never Miss a Day",
        "subtitle": "Smart reminders",
        "html": _screenshot_template(
            name, "Smart Reminders\\nKeep You on Track",
            "Gentle nudges when you need them",
            "#121212", app_info,
        ),
    })

    return screenshots


def _screenshot_template(name: str, headline: str, subheadline: str, bg: str, app_info: dict) -> str:
    """Generate a screenshot HTML template."""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1290px; height: 2796px;
    background: linear-gradient(180deg, {bg} 0%, #000 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    color: #fff;
  }}
  .headline {{
    font-size: 96px; font-weight: 800; text-align: center;
    line-height: 1.1; margin-bottom: 32px;
    white-space: pre-line;
  }}
  .subheadline {{
    font-size: 42px; font-weight: 400; text-align: center;
    opacity: 0.7; margin-bottom: 80px;
  }}
  .phone-frame {{
    width: 380px; height: 780px;
    background: #111; border-radius: 40px;
    border: 3px solid #333;
    display: flex; align-items: center; justify-content: center;
  }}
  .phone-content {{
    font-size: 36px; opacity: 0.5;
    text-align: center;
  }}
  .app-name {{
    font-size: 36px; font-weight: 600;
    margin-top: 60px; opacity: 0.5;
  }}
</style>
</head>
<body>
  <div class="headline">{headline}</div>
  <div class="subheadline">{subheadline}</div>
  <div class="phone-frame">
    <div class="phone-content">{name}<br>Screenshot Placeholder</div>
  </div>
  <div class="app-name">{name}</div>
</body>
</html>"""


def save_screenshots(app_info: dict, screenshots: list[dict], dry_run: bool = False) -> list[Path]:
    """Save screenshot HTML templates to disk."""
    slug = app_info.get("slug", "unknown")
    output_dir = safe_path(SCREENSHOTS_DIR / slug)

    if dry_run:
        log(f"DRY RUN: Would save {len(screenshots)} screenshots to {output_dir}")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []

    for ss in screenshots:
        html_path = output_dir / f"{ss['name']}.html"
        with open(html_path, "w") as f:
            f.write(ss["html"])
        saved.append(html_path)

    log(f"Saved {len(saved)} screenshot templates to {output_dir}")
    log(f"  To render: use Playwright to screenshot each HTML at 1290x2796")
    return saved


# ---------------------------------------------------------------------------
# Queue Posts for Distribution
# ---------------------------------------------------------------------------
def queue_posts(app_info: dict, posts: dict[str, list[dict]], dry_run: bool = False) -> int:
    """Queue social media posts for distribution."""
    if dry_run:
        total = sum(len(v) for v in posts.values())
        log(f"DRY RUN: Would queue {total} posts")
        return total

    POSTING_QUEUE.mkdir(parents=True, exist_ok=True)
    queued = 0
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for platform, platform_posts in posts.items():
        for i, post in enumerate(platform_posts):
            filename = f"{ts}_{platform}_{app_info.get('slug', 'app')}_{i}.json"
            post_data = {
                **post,
                "app_name": app_info.get("name", ""),
                "app_slug": app_info.get("slug", ""),
                "created_at": datetime.now().isoformat(),
                "status": "QUEUED",
            }
            with open(POSTING_QUEUE / filename, "w") as f:
                json.dump(post_data, f, indent=2)
            queued += 1

    log(f"Queued {queued} posts to {POSTING_QUEUE}")
    return queued


# ---------------------------------------------------------------------------
# Distribution Plan
# ---------------------------------------------------------------------------
def generate_distribution_plan(app_info: dict) -> str:
    """Generate a full distribution plan for an app."""
    name = app_info.get("name", "App")
    niche = app_info.get("niche", "General")
    slug = app_info.get("slug", "app")

    subreddits = _get_target_subreddits(niche)

    plan = f"""# Distribution Plan: {name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Launch Week Timeline

### Day 0 (Launch Day)
- [ ] App Store listing live with ASO keywords
- [ ] Post launch tweet (announcement thread)
- [ ] Post to r/{subreddits[0]} (value-first, ask for feedback)
- [ ] Submit to Product Hunt (schedule for Tuesday/Wednesday)
- [ ] Email 10 niche influencers with personalized pitch

### Day 1-3
- [ ] Post builder story tweet
- [ ] Post to r/{subreddits[1] if len(subreddits) > 1 else 'SideProject'} and r/{subreddits[2] if len(subreddits) > 2 else 'indiehackers'}
- [ ] Engage with every comment/reply within 1 hour
- [ ] Cross-post to Hacker News (Show HN)
- [ ] Share in relevant Discord communities

### Day 4-7
- [ ] Feature highlight tweets (3 posts)
- [ ] Record 30-second demo video for TikTok/Reels
- [ ] Reply to niche-relevant tweets with genuine advice (soft promote)
- [ ] Track initial install/revenue numbers

### Week 2-4 (Sustained)
- [ ] Weekly "user story" or "progress" tweet
- [ ] A/B test App Store screenshots
- [ ] Run first pricing experiment
- [ ] Analyze which channels drove installs

## Channel Priority (by expected ROI)

1. **Reddit** - {', '.join(f'r/{s}' for s in subreddits[:4])}
   - Value-first posts, ask for feedback
   - Comment in existing threads about {niche.lower()} apps

2. **Twitter/X** - @printmaxxer
   - Builder story thread
   - Feature highlights
   - Reply engagement in {niche.lower()} community

3. **Product Hunt**
   - Schedule for Tuesday 12:01 AM PT
   - Prepare 5 upvoters for launch hour
   - Respond to every comment

4. **Hacker News**
   - Show HN: {name} -- {niche} habit tracker
   - Technical angle: built with Expo/React Native

5. **TikTok/Instagram Reels**
   - 30s demo: "I built this app because..."
   - Before/after: messy habits vs organized streaks

## Influencer Outreach

Target: micro-influencers in {niche.lower()} (5K-50K followers)
Offer: Free premium access + affiliate link (30% revenue share)
Template:
  Subject: Free premium access to {name} for your audience
  Body: Short, personal, mention specific content of theirs you liked.

## ASO Optimization
- Primary keywords: {', '.join(_get_target_subreddits(niche)[:5])}
- Run keyword experiments every 2 weeks
- Monitor competitor keywords via AppFollow/Sensor Tower free tier

## Budget Tiers

### FREE ($0) -- Start here
- Organic Reddit, Twitter, HN, Discord
- Cross-promotion with other PRINTMAXX apps
- Reply engagement (30 min/day)

### LOW ($0-50/mo)
- Apple Search Ads basic ($20/mo)
- Boosted tweets ($10/mo)
- Small Reddit ads ($20/mo)

### MID ($50-200/mo) -- Once at $200+ MRR
- Micro-influencer payments
- Apple Search Ads expanded
- TikTok promoted posts
"""

    return plan


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Factory Distribution Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/app_factory/distribution_engine.py --plan builds/fitstreak
  python3 AUTOMATIONS/app_factory/distribution_engine.py --generate-posts builds/fitstreak
  python3 AUTOMATIONS/app_factory/distribution_engine.py --generate-aso builds/fitstreak
  python3 AUTOMATIONS/app_factory/distribution_engine.py --generate-screenshots builds/fitstreak
  python3 AUTOMATIONS/app_factory/distribution_engine.py --full builds/fitstreak
        """,
    )
    parser.add_argument("--plan", metavar="APP_DIR", help="Generate distribution plan")
    parser.add_argument("--generate-posts", metavar="APP_DIR", help="Generate social media posts")
    parser.add_argument("--generate-aso", metavar="APP_DIR", help="Generate ASO keywords")
    parser.add_argument("--generate-screenshots", metavar="APP_DIR", help="Generate screenshot templates")
    parser.add_argument("--full", metavar="APP_DIR", help="Run full distribution pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")

    args = parser.parse_args()

    target_dir = args.plan or args.generate_posts or args.generate_aso or args.generate_screenshots or args.full
    if not target_dir:
        parser.print_help()
        return

    app_dir = _resolve_dir(target_dir)
    app_info = load_app_info(app_dir)
    if not app_info:
        log(f"ERROR: Could not load app info from {app_dir}")
        return

    log(f"App: {app_info['name']} | Niche: {app_info['niche']}")

    if args.plan or args.full:
        plan = generate_distribution_plan(app_info)
        if args.dry_run:
            print(plan)
        else:
            plan_path = safe_path(DIST_DIR / f"plan_{app_info['slug']}.md")
            with open(plan_path, "w") as f:
                f.write(plan)
            log(f"Distribution plan saved: {plan_path}")
            print(plan)

    if args.generate_posts or args.full:
        posts = generate_launch_posts(app_info)
        total = queue_posts(app_info, posts, dry_run=args.dry_run)
        log(f"Generated {total} launch posts")

        if not args.dry_run:
            # Also save as single file for review
            posts_path = safe_path(DIST_DIR / f"posts_{app_info['slug']}.json")
            with open(posts_path, "w") as f:
                json.dump(posts, f, indent=2)

    if args.generate_aso or args.full:
        aso = generate_aso_keywords(app_info)
        if args.dry_run:
            print(json.dumps(aso, indent=2))
        else:
            aso_path = safe_path(DIST_DIR / f"aso_{app_info['slug']}.json")
            with open(aso_path, "w") as f:
                json.dump(aso, f, indent=2)
            log(f"ASO keywords saved: {aso_path}")
            print(f"Keywords: {aso['keyword_string']}")
            print(f"Subtitles: {aso['subtitles']}")

    if args.generate_screenshots or args.full:
        aso = generate_aso_keywords(app_info)
        screenshots = generate_screenshot_html(app_info, aso)
        saved = save_screenshots(app_info, screenshots, dry_run=args.dry_run)
        log(f"Generated {len(screenshots)} screenshot templates")


def _resolve_dir(path: str) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    if (BUILDS_DIR / path).exists():
        return BUILDS_DIR / path
    if (PROJECT / path).exists():
        return PROJECT / path
    return p


if __name__ == "__main__":
    main()
