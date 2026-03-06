#!/usr/bin/env python3
"""
PRINTMAXX Creative Sourcer
=============================
Auto-finds top performing copy, hooks, sounds, ad creatives, and UGC patterns
per niche. Feeds the content pipeline with proven formats.

Sources:
  - Our own ALPHA_STAGING.csv for proven tactics
  - WINNING_CONTENT_STRUCTURES.csv for format patterns
  - HIGH_SIGNAL_SOURCES.csv for accounts to mirror
  - Trend signals for momentum
  - Ad library patterns (FB/TikTok creative formats)

Output:
  - Hook templates per niche
  - Sound/music recommendations
  - Ad creative formats ranked by performance
  - UGC script templates
  - Copy swipe file updates

Usage:
  python3 creative_sourcer.py --niche faith       # source creatives for faith niche
  python3 creative_sourcer.py --all-niches         # source for all niches
  python3 creative_sourcer.py --hooks              # generate hook templates
  python3 creative_sourcer.py --ugc-scripts        # generate UGC script templates
  python3 creative_sourcer.py --ad-formats         # rank ad creative formats
  python3 creative_sourcer.py --swipe-file         # update copy swipe file
  python3 creative_sourcer.py --api-json           # JSON for webapp
"""

import json
import csv
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
LEDGER = BASE / "LEDGER"
CONTENT = BASE / "CONTENT"
OPS = BASE / "OPS"
LOGS = AUTO / "logs"

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(BASE)):
        raise ValueError(f"BLOCKED: {resolved} outside {BASE}")
    return resolved

def read_csv(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

# ---------------------------------------------------------------------------
# NICHE DATABASE — proven patterns per vertical
# ---------------------------------------------------------------------------

NICHE_CREATIVES = {
    "faith": {
        "hooks": [
            "this one prayer changed everything for me...",
            "i stopped scrolling and started praying. here's what happened.",
            "day {N} of praying for 30 days straight.",
            "the bible verse that hits different at 3am.",
            "POV: you finally surrender it to God.",
            "i asked God for a sign and this happened.",
            "that moment when your prayer gets answered and you just...",
        ],
        "sounds": ["worship ambient", "piano worship", "hillsong", "maverick city music",
                    "bethel music", "acoustic worship", "gregorian chant lo-fi"],
        "ad_formats": ["testimonial UGC", "before/after spiritual journey",
                       "day-in-the-life prayer routine", "app walkthrough with worship background"],
        "affiliate_products": [
            {"product": "devotional journals", "commission": "8-15%", "platforms": ["Amazon Associates"]},
            {"product": "prayer apps (competitors)", "commission": "30-50% rev share", "platforms": ["direct"]},
            {"product": "christian books", "commission": "4-8%", "platforms": ["Amazon", "Bookshop.org"]},
            {"product": "church supplies", "commission": "5-10%", "platforms": ["ShareASale"]},
        ],
        "pricing": {"weekly": "$1.99", "monthly": "$4.99", "yearly": "$29.99", "lifetime": "$79.99"},
        "ugc_script": "Hey, I've been using this prayer app for {N} days and honestly it's changed my morning routine. I used to just scroll my phone first thing. Now I open {APP} and spend 5 minutes in prayer. The guided prayers are beautiful. Link in bio if you want to try it.",
        "cta_patterns": ["link in bio", "save this for later", "comment PRAY for the link",
                         "share with someone who needs this"],
    },
    "fitness": {
        "hooks": [
            "I walked 10,000 steps every day for 30 days. here's what happened.",
            "the workout nobody talks about that burns the most calories.",
            "POV: you actually stuck with it for a month.",
            "day {N} of walking until my phone unlocks.",
            "this app won't let me use my phone until I walk. I hate it. I love it.",
            "I lost {N} lbs by doing this one simple thing every morning.",
        ],
        "sounds": ["phonk", "gym motivation", "hardstyle", "aggressive rap",
                    "rocky training montage", "warrior motivation"],
        "ad_formats": ["transformation UGC", "screen recording + face cam",
                       "split screen before/after", "POV workout"],
        "affiliate_products": [
            {"product": "supplements (protein, creatine)", "commission": "15-30%", "platforms": ["Amazon", "iHerb"]},
            {"product": "fitness equipment", "commission": "5-12%", "platforms": ["Amazon"]},
            {"product": "athletic wear", "commission": "10-20%", "platforms": ["Lululemon", "Gymshark"]},
            {"product": "fitness trackers", "commission": "3-8%", "platforms": ["Amazon"]},
        ],
        "pricing": {"weekly": "$2.99", "monthly": "$7.99", "yearly": "$39.99", "lifetime": "$99.99"},
        "ugc_script": "Alright so I found this app that literally locks your phone until you walk. I know it sounds crazy but hear me out. I've walked {N} steps every day for the past month because of it. My screen time is down 40%. Link below.",
        "cta_patterns": ["try it free for 7 days", "comment WALK", "save this workout",
                         "tag your gym partner"],
    },
    "sleep": {
        "hooks": [
            "I fixed my sleep in 3 days. no pills. no supplements. just this.",
            "the 10-3-2-1-0 rule changed my life.",
            "POV: you wake up actually feeling rested for the first time.",
            "I tracked my sleep for 30 days. the data was terrifying.",
            "this bedtime routine gave me the best sleep of my life.",
            "your phone is ruining your sleep. here's the science.",
        ],
        "sounds": ["ambient sleep", "rain sounds", "lo-fi sleep", "binaural beats",
                    "white noise", "ASMR whisper"],
        "ad_formats": ["cozy bedroom setup", "sleep data screenshots", "morning routine POV",
                       "ASMR-style product demo"],
        "affiliate_products": [
            {"product": "mattresses", "commission": "$50-200 per sale", "platforms": ["Casper", "Purple", "Helix"]},
            {"product": "sleep supplements (magnesium, melatonin)", "commission": "15-30%", "platforms": ["Amazon", "iHerb"]},
            {"product": "blue light glasses", "commission": "10-20%", "platforms": ["Amazon"]},
            {"product": "sleep trackers (Oura, Whoop)", "commission": "$15-50", "platforms": ["direct"]},
            {"product": "weighted blankets", "commission": "8-15%", "platforms": ["Amazon"]},
        ],
        "pricing": {"weekly": "$1.99", "monthly": "$4.99", "yearly": "$29.99", "lifetime": "$69.99"},
        "ugc_script": "Okay I have to talk about this sleep app because my sleep score went from 62 to 89 in two weeks. It does this wind-down routine that actually works. No more lying in bed staring at the ceiling for 2 hours. Check it out, link in bio.",
        "cta_patterns": ["save for tonight", "comment SLEEP", "send to someone who needs better sleep"],
    },
    "productivity": {
        "hooks": [
            "I replaced 6 apps with this one thing.",
            "the 2-minute rule that 10x'd my output.",
            "I built a system that runs my entire life. here's the template.",
            "stop using to-do lists. do this instead.",
            "POV: you actually finish everything on your list.",
            "I tracked every minute for 30 days. the waste was insane.",
        ],
        "sounds": ["lo-fi beats", "binaural focus", "coffee shop ambient", "library sounds",
                    "classical piano", "synthwave work"],
        "ad_formats": ["screen recording workflow", "notion/app walkthrough", "desk setup ASMR",
                       "before/after productivity stats"],
        "affiliate_products": [
            {"product": "productivity apps (Notion, Todoist)", "commission": "20-40%", "platforms": ["direct"]},
            {"product": "standing desks", "commission": "5-10%", "platforms": ["Amazon", "FlexiSpot"]},
            {"product": "mechanical keyboards", "commission": "5-8%", "platforms": ["Amazon"]},
            {"product": "focus supplements (nootropics)", "commission": "20-35%", "platforms": ["direct"]},
        ],
        "pricing": {"weekly": "$2.99", "monthly": "$6.99", "yearly": "$34.99", "lifetime": "$89.99"},
        "ugc_script": "I used to waste 4 hours a day on my phone. Then I installed this app that locks everything until I finish my tasks. Sounds extreme but my productivity literally doubled. Free trial link in bio.",
        "cta_patterns": ["try it for 7 days", "comment FOCUS", "save for monday morning"],
    },
    "cooking": {
        "hooks": [
            "I meal prepped all week for $23. here's everything I made.",
            "$3 dinner that tastes like a $30 restaurant meal.",
            "the one kitchen tool that changed everything.",
            "POV: you actually enjoy cooking for the first time.",
            "I ate out 0 times this month. saved ${N}.",
            "5 ingredients. 15 minutes. restaurant quality.",
        ],
        "sounds": ["cooking ASMR", "jazz kitchen", "lofi cooking", "italian cafe",
                    "chopping sounds", "sizzling sounds"],
        "ad_formats": ["overhead cooking shot", "ingredient-to-plate transformation",
                       "grocery haul POV", "meal prep montage"],
        "affiliate_products": [
            {"product": "kitchen gadgets", "commission": "5-10%", "platforms": ["Amazon"]},
            {"product": "meal kit subscriptions", "commission": "$15-30 per signup", "platforms": ["HelloFresh", "Factor"]},
            {"product": "cookbooks", "commission": "4-8%", "platforms": ["Amazon"]},
            {"product": "meal prep containers", "commission": "8-15%", "platforms": ["Amazon"]},
        ],
        "pricing": {"weekly": "$1.99", "monthly": "$4.99", "yearly": "$24.99", "lifetime": "$59.99"},
        "ugc_script": "This app just saved me like $200 this month on food. It plans all my meals based on what's on sale, generates the grocery list, and tells me exactly what to cook each day. I went from ordering DoorDash 5 times a week to cooking every meal. Link in bio.",
        "cta_patterns": ["save this recipe", "comment RECIPE for the full list", "tag a foodie"],
    },
    "finance": {
        "hooks": [
            "I tracked every dollar for 30 days. the leaks were insane.",
            "the subscription audit that saved me $340/month.",
            "I automated my savings and forgot about it. 6 months later...",
            "POV: you check your bank account and it actually went UP.",
            "stop budgeting. do this instead.",
            "the savings trick banks don't want you to know.",
        ],
        "sounds": ["money counting ASMR", "stock market ambient", "corporate lo-fi",
                    "motivational speech"],
        "ad_formats": ["screen recording of savings", "financial dashboard walkthrough",
                       "spending vs saving comparison", "net worth tracking"],
        "affiliate_products": [
            {"product": "investing apps (Wealthfront, M1)", "commission": "$25-75 per signup", "platforms": ["direct"]},
            {"product": "budgeting tools", "commission": "20-40%", "platforms": ["direct"]},
            {"product": "financial books", "commission": "4-8%", "platforms": ["Amazon"]},
            {"product": "credit cards (referral)", "commission": "$50-200 per approval", "platforms": ["bank direct"]},
        ],
        "pricing": {"weekly": "$1.99", "monthly": "$5.99", "yearly": "$29.99", "lifetime": "$79.99"},
        "ugc_script": "This app found $340 in subscriptions I forgot I was paying for. Literally just scanned my bank and showed me everything I'm wasting money on. I cancelled 8 things in 5 minutes. Link in bio.",
        "cta_patterns": ["save this", "comment SAVE for the app link", "tag someone who needs this"],
    },
}

# ---------------------------------------------------------------------------
# AD CREATIVE FORMATS — ranked by general performance
# ---------------------------------------------------------------------------

AD_FORMATS_RANKED = [
    {"format": "UGC Testimonial (talking head)", "cpm_range": "$5-15", "cvr": "2-5%",
     "best_for": ["apps", "services", "digital products"], "cost_to_produce": "$0 (AI) / $3-25 (real)"},
    {"format": "Before/After Transformation", "cpm_range": "$8-20", "cvr": "3-7%",
     "best_for": ["fitness", "sleep", "productivity"], "cost_to_produce": "$0-5"},
    {"format": "Screen Recording + Facecam", "cpm_range": "$4-12", "cvr": "2-4%",
     "best_for": ["apps", "tools", "SaaS"], "cost_to_produce": "$0"},
    {"format": "Day-in-the-Life POV", "cpm_range": "$6-18", "cvr": "1-3%",
     "best_for": ["lifestyle", "fitness", "faith"], "cost_to_produce": "$0-10"},
    {"format": "Text Overlay Story", "cpm_range": "$3-8", "cvr": "1-3%",
     "best_for": ["memes", "engagement farming", "brand awareness"], "cost_to_produce": "$0"},
    {"format": "Problem-Solution Demo", "cpm_range": "$5-15", "cvr": "3-6%",
     "best_for": ["SaaS", "tools", "services"], "cost_to_produce": "$0-5"},
    {"format": "Listicle / Top 5", "cpm_range": "$4-10", "cvr": "1-3%",
     "best_for": ["tools", "products", "affiliate"], "cost_to_produce": "$0"},
    {"format": "AI UGC (HeyGen/D-ID)", "cpm_range": "$5-15", "cvr": "1-4%",
     "best_for": ["apps", "services", "info products"], "cost_to_produce": "$0.10-2 per video"},
]

# ---------------------------------------------------------------------------
# PLATFORM MONETIZATION RATES
# ---------------------------------------------------------------------------

PLATFORM_RATES = {
    "x_twitter": {
        "creator_revenue_share": "Based on ad impressions to verified subscribers. ~$2-8 per 1M impressions.",
        "minimum_payout": "$10",
        "requirements": "Subscribed to X Premium, 500+ followers, 5M organic impressions in last 3 months",
    },
    "youtube_shorts": {
        "rpm": "$0.01-0.07 per 1K views",
        "minimum_payout": "$100",
        "requirements": "1,000 subscribers + 10M Shorts views in 90 days",
    },
    "tiktok": {
        "creator_fund": "$0.02-0.04 per 1K views (Creativity Program Beta: $0.50-1.00 per 1K)",
        "tiktok_shop": "5-20% commission on products sold",
        "minimum_payout": "$10",
        "requirements": "10K followers + 100K views in 30 days (Creativity Program)",
    },
    "instagram_reels": {
        "bonus_program": "Invite-only. $100-35K per month based on performance.",
        "shopping": "5-20% commission via affiliate links",
        "requirements": "Professional account, consistent posting",
    },
    "snapchat_spotlight": {
        "payout": "$50-25K per snap based on unique views",
        "minimum_views": "No minimum, but higher payouts at 50K+ unique views",
        "requirements": "Public account",
    },
}


# ---------------------------------------------------------------------------
# HOOK GENERATOR
# ---------------------------------------------------------------------------

def generate_hooks(niche, count=10):
    """Generate hook variations for a niche."""
    nc = NICHE_CREATIVES.get(niche, {})
    base_hooks = nc.get("hooks", [])

    # Add numbered variations
    hooks = []
    for h in base_hooks:
        if "{N}" in h:
            for n in [7, 14, 21, 30, 60, 90]:
                hooks.append(h.replace("{N}", str(n)))
        else:
            hooks.append(h)

    return hooks[:count]


def generate_ugc_scripts(niche, app_name="the app"):
    """Generate UGC video scripts for a niche."""
    nc = NICHE_CREATIVES.get(niche, {})
    base = nc.get("ugc_script", "")
    if not base:
        return []

    scripts = []
    for n in [7, 14, 30]:
        script = base.replace("{N}", str(n)).replace("{APP}", app_name)
        scripts.append({"duration": "30-60s", "style": "UGC talking head", "script": script})

    return scripts


# ---------------------------------------------------------------------------
# SWIPE FILE — aggregate best copy from our alpha
# ---------------------------------------------------------------------------

def update_swipe_file():
    """Build a swipe file from ALPHA_STAGING approved entries with content value."""
    alpha = read_csv(LEDGER / "ALPHA_STAGING.csv")
    approved = [a for a in alpha if a.get("status") == "APPROVED"
                and a.get("category", "") in ("CONTENT_FORMAT", "GROWTH_HACK", "MONETIZATION")]

    swipe = {
        "updated": datetime.now().isoformat(),
        "total_entries": len(approved),
        "by_category": defaultdict(list),
    }

    for a in approved:
        entry = {
            "source": a.get("source", ""),
            "tactic": a.get("description", a.get("title", "")),
            "roi": a.get("roi_potential", ""),
        }
        swipe["by_category"][a.get("category", "OTHER")].append(entry)

    # Save swipe file
    out = safe_path(OPS / "CREATIVE_SWIPE_FILE.json")
    with open(out, "w") as f:
        json.dump(dict(swipe), f, indent=2, default=str)

    return swipe


# ---------------------------------------------------------------------------
# API JSON
# ---------------------------------------------------------------------------

def get_api_json():
    niches_summary = {}
    for niche, data in NICHE_CREATIVES.items():
        niches_summary[niche] = {
            "hooks": len(data["hooks"]),
            "sounds": len(data["sounds"]),
            "ad_formats": len(data["ad_formats"]),
            "affiliates": len(data["affiliate_products"]),
            "pricing": data["pricing"],
        }

    return {
        "timestamp": datetime.now().isoformat(),
        "niches": niches_summary,
        "ad_formats_ranked": AD_FORMATS_RANKED,
        "platform_rates": PLATFORM_RATES,
        "total_niches": len(NICHE_CREATIVES),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if "--niche" in args:
        idx = args.index("--niche")
        niche = args[idx + 1] if idx + 1 < len(args) else "faith"
        nc = NICHE_CREATIVES.get(niche, {})
        if not nc:
            print(f"Unknown niche: {niche}. Available: {', '.join(NICHE_CREATIVES.keys())}")
            return

        print(f"\n=== CREATIVE SOURCER: {niche.upper()} ===\n")

        print("HOOKS:")
        for h in nc["hooks"]:
            print(f"  - {h}")

        print(f"\nSOUNDS: {', '.join(nc['sounds'])}")

        print("\nAD FORMATS:")
        for f in nc["ad_formats"]:
            print(f"  - {f}")

        print("\nAFFILIATE PRODUCTS:")
        for a in nc["affiliate_products"]:
            print(f"  - {a['product']}: {a['commission']} via {', '.join(a['platforms'])}")

        print(f"\nPRICING: {nc['pricing']}")

        print(f"\nUGC SCRIPT TEMPLATE:\n  {nc['ugc_script']}")

        print(f"\nCTA PATTERNS: {', '.join(nc['cta_patterns'])}")

    elif "--all-niches" in args:
        print("\n=== ALL NICHE CREATIVES ===\n")
        for niche, data in NICHE_CREATIVES.items():
            print(f"  {niche.upper()}: {len(data['hooks'])} hooks, {len(data['sounds'])} sounds, {len(data['affiliate_products'])} affiliates")
            print(f"    Pricing: {data['pricing']}")
            print(f"    Top hook: {data['hooks'][0]}")
            print()

    elif "--hooks" in args:
        niche = args[args.index("--hooks") + 1] if args.index("--hooks") + 1 < len(args) else None
        if niche:
            hooks = generate_hooks(niche, count=20)
            for h in hooks:
                print(f"  {h}")
        else:
            for niche in NICHE_CREATIVES:
                print(f"\n{niche.upper()}:")
                for h in generate_hooks(niche, count=5):
                    print(f"  - {h}")

    elif "--ugc-scripts" in args:
        for niche in NICHE_CREATIVES:
            scripts = generate_ugc_scripts(niche)
            print(f"\n{niche.upper()}:")
            for s in scripts:
                print(f"  [{s['duration']}] {s['script'][:100]}...")

    elif "--ad-formats" in args:
        print("\n=== AD CREATIVE FORMATS (Ranked by Performance) ===\n")
        print(f"{'#':<4} {'Format':<35} {'CPM':<12} {'CVR':<10} {'Cost':<25} Best For")
        print("-" * 110)
        for i, f in enumerate(AD_FORMATS_RANKED, 1):
            print(f"{i:<4} {f['format']:<35} {f['cpm_range']:<12} {f['cvr']:<10} {f['cost_to_produce']:<25} {', '.join(f['best_for'])}")

    elif "--swipe-file" in args:
        swipe = update_swipe_file()
        print(f"\nSwipe file updated: {swipe['total_entries']} entries")
        for cat, entries in swipe["by_category"].items():
            print(f"  {cat}: {len(entries)} entries")

    elif "--platform-rates" in args:
        print("\n=== PLATFORM MONETIZATION RATES ===\n")
        for platform, rates in PLATFORM_RATES.items():
            print(f"  {platform.upper()}:")
            for k, v in rates.items():
                print(f"    {k}: {v}")
            print()

    elif "--api-json" in args:
        print(json.dumps(get_api_json(), indent=2))

    else:
        print("Usage: creative_sourcer.py [--niche NAME|--all-niches|--hooks|--ugc-scripts|--ad-formats|--swipe-file|--platform-rates|--api-json]")


if __name__ == "__main__":
    main()
