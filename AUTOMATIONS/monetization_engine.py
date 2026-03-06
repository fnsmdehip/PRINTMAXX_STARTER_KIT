#!/usr/bin/env python3
"""
PRINTMAXX Monetization Engine
==============================
Automatically determines optimal monetization strategy for any app or digital product.
Analyzes niche, recommends pricing, projects revenue, and generates monetization configs.

Usage:
  python3 monetization_engine.py --analyze APP_NAME --niche NICHE
  python3 monetization_engine.py --pricing NICHE
  python3 monetization_engine.py --revenue NICHE --downloads N
  python3 monetization_engine.py --affiliates NICHE
  python3 monetization_engine.py --generate APP_NAME --niche NICHE
  python3 monetization_engine.py --all
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Safe path validation (guardrails)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def safe_path(target) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ---------------------------------------------------------------------------
# 1. MONETIZATION MODELS DATABASE
# ---------------------------------------------------------------------------

SUBSCRIPTION_TIERS = {
    "weekly": {"low": 1.99, "mid": 3.99, "high": 6.99},
    "monthly": {"low": 4.99, "mid": 9.99, "high": 19.99},
    "yearly": {"low": 29.99, "mid": 49.99, "high": 79.99},
}

IAP_TYPES = {
    "consumable": {
        "description": "Credits, tokens, single-use unlocks",
        "examples": ["50 AI credits - $4.99", "100 AI credits - $7.99", "premium analysis token - $2.99"],
        "avg_price": 4.99,
    },
    "non_consumable": {
        "description": "Permanent unlocks, lifetime features",
        "examples": ["Lifetime premium - $49.99", "Theme pack - $3.99", "Icon pack - $2.99"],
        "avg_price": 9.99,
    },
}

AD_TYPES = {
    "banner": {
        "description": "Bottom/top banner ads (320x50)",
        "cpm_range": {"low": 0.50, "mid": 2.00, "high": 5.00},
        "user_impact": "low",
        "best_for": ["memes", "aesthetic", "curation"],
    },
    "interstitial": {
        "description": "Full-screen ads between screens",
        "cpm_range": {"low": 4.00, "mid": 10.00, "high": 20.00},
        "user_impact": "medium",
        "best_for": ["memes", "games", "utilities"],
    },
    "rewarded_video": {
        "description": "User opts in to watch ad for reward",
        "cpm_range": {"low": 10.00, "mid": 25.00, "high": 50.00},
        "user_impact": "low (opt-in)",
        "best_for": ["fitness", "sleep", "productivity", "faith"],
    },
}

MONETIZATION_MODELS = {
    "subscription": {
        "description": "Recurring subscription (weekly/monthly/yearly)",
        "pros": ["predictable revenue", "high LTV", "App Store featured preference"],
        "cons": ["harder initial conversion", "churn management needed"],
        "avg_conversion": 0.03,
        "apple_cut": 0.30,  # 30% first year, 15% after
    },
    "iap": {
        "description": "In-app purchases (consumable and non-consumable)",
        "pros": ["impulse purchases", "no commitment barrier"],
        "cons": ["unpredictable revenue", "lower LTV"],
        "avg_conversion": 0.05,
        "apple_cut": 0.30,
    },
    "ads": {
        "description": "Ad revenue (banner, interstitial, rewarded)",
        "pros": ["monetizes free users", "passive revenue"],
        "cons": ["needs high DAU", "degrades UX"],
        "avg_conversion": 1.0,  # all free users see ads
        "apple_cut": 0.0,
    },
    "affiliate": {
        "description": "Affiliate links to relevant products",
        "pros": ["no upfront cost", "adds user value", "iOS allows external payment links"],
        "cons": ["variable commissions", "disclosure required (FTC)"],
        "avg_conversion": 0.02,
        "apple_cut": 0.0,
    },
    "one_time": {
        "description": "Single purchase to unlock full app",
        "pros": ["simple", "no churn"],
        "cons": ["limited LTV", "harder to iterate pricing"],
        "avg_conversion": 0.04,
        "apple_cut": 0.30,
    },
    "freemium": {
        "description": "Free core with premium features",
        "pros": ["large user base", "viral potential"],
        "cons": ["most users never pay"],
        "avg_conversion": 0.03,
        "apple_cut": 0.30,
    },
    "creator_rewards": {
        "description": "Platform creator fund, tips, brand deals",
        "pros": ["scales with audience", "no user payment friction"],
        "cons": ["needs large audience", "platform dependent"],
        "avg_conversion": None,
        "apple_cut": 0.0,
    },
}


# ---------------------------------------------------------------------------
# 2. NICHE-SPECIFIC STRATEGIES
# ---------------------------------------------------------------------------

NICHE_STRATEGIES = {
    "faith": {
        "primary": "subscription",
        "secondary": ["affiliate", "freemium"],
        "tertiary": ["ads"],
        "subscription_tier": "mid",
        "optimal_weekly": 2.99,
        "optimal_monthly": 9.99,
        "optimal_yearly": 49.99,
        "affiliate_categories": [
            {"category": "devotional books", "commission": "4-8%", "program": "Amazon Associates", "avg_order": 18.00},
            {"category": "faith journals", "commission": "10-20%", "program": "DaySpring Affiliate", "avg_order": 22.00},
            {"category": "prayer beads/rosaries", "commission": "8-15%", "program": "Etsy Affiliate", "avg_order": 25.00},
            {"category": "Bible study tools", "commission": "20-40%", "program": "Logos Bible Software", "avg_order": 49.99},
            {"category": "faith-based supplements", "commission": "15-30%", "program": "Garden of Life", "avg_order": 35.00},
        ],
        "ad_strategy": "rewarded video only (respect the spiritual experience)",
        "paywall_timing": "after 3-day free trial with daily devotional preview",
        "premium_features": [
            "unlimited prayer tracking",
            "audio devotionals",
            "community prayer wall",
            "custom prayer reminders",
            "offline mode",
        ],
        "donation_model": True,
        "notes": "faith users have high retention + willingness to pay for spiritual tools. never make the app feel transactional. lead with value, paywall after emotional connection.",
    },
    "fitness": {
        "primary": "subscription",
        "secondary": ["affiliate", "iap"],
        "tertiary": ["ads"],
        "subscription_tier": "mid",
        "optimal_weekly": 3.99,
        "optimal_monthly": 9.99,
        "optimal_yearly": 49.99,
        "affiliate_categories": [
            {"category": "protein/supplements", "commission": "10-25%", "program": "MyProtein / Transparent Labs", "avg_order": 55.00},
            {"category": "fitness equipment", "commission": "4-8%", "program": "Amazon Associates", "avg_order": 45.00},
            {"category": "workout apparel", "commission": "8-15%", "program": "Gymshark / Lululemon", "avg_order": 65.00},
            {"category": "fitness trackers", "commission": "3-6%", "program": "Amazon / Best Buy Affiliate", "avg_order": 120.00},
            {"category": "meal prep services", "commission": "15-30%", "program": "Factor / HelloFresh", "avg_order": 60.00},
        ],
        "ad_strategy": "rewarded video for extra workout content. no banner ads during workouts.",
        "paywall_timing": "after completing first workout or 3 workouts free",
        "premium_features": [
            "personalized workout plans",
            "advanced analytics / body metrics",
            "trainer-curated programs",
            "offline downloads",
            "Apple Health / Google Fit sync",
        ],
        "donation_model": False,
        "notes": "fitness users expect polish and results. subscription anchored to 'cost of 1 gym visit'. supplement affiliate is the money printer. integrate recommendations naturally after workouts.",
    },
    "sleep": {
        "primary": "subscription",
        "secondary": ["affiliate", "freemium"],
        "tertiary": ["ads"],
        "subscription_tier": "mid",
        "optimal_weekly": 2.99,
        "optimal_monthly": 7.99,
        "optimal_yearly": 39.99,
        "affiliate_categories": [
            {"category": "mattresses", "commission": "5-12%", "program": "Casper / Purple / Helix", "avg_order": 1200.00},
            {"category": "sleep supplements (melatonin, magnesium)", "commission": "15-30%", "program": "Moon Juice / Natural Vitality", "avg_order": 30.00},
            {"category": "weighted blankets", "commission": "8-15%", "program": "Bearaby / Amazon", "avg_order": 120.00},
            {"category": "blue light glasses", "commission": "10-20%", "program": "Felix Gray / Warby Parker", "avg_order": 95.00},
            {"category": "white noise machines", "commission": "4-8%", "program": "Hatch / Amazon", "avg_order": 60.00},
        ],
        "ad_strategy": "no ads during sleep sessions. rewarded video for premium sounds during daytime browsing only.",
        "paywall_timing": "after 7-night sleep score tracking preview",
        "premium_features": [
            "unlimited sleep sounds library",
            "smart alarm (wake during light sleep)",
            "sleep coaching / tips engine",
            "sleep environment analysis",
            "advanced sleep analytics",
        ],
        "donation_model": False,
        "notes": "mattress affiliate is the sleeper (pun intended) money maker. a single mattress sale = $60-$144 commission. sleep users are health-conscious spenders. never interrupt sleep experience with monetization.",
    },
    "productivity": {
        "primary": "subscription",
        "secondary": ["affiliate", "freemium"],
        "tertiary": ["iap"],
        "subscription_tier": "mid",
        "optimal_weekly": 1.99,
        "optimal_monthly": 6.99,
        "optimal_yearly": 39.99,
        "affiliate_categories": [
            {"category": "productivity tools (Notion, Todoist)", "commission": "20-40%", "program": "Notion / Todoist Affiliate", "avg_order": 96.00},
            {"category": "standing desks", "commission": "5-10%", "program": "FlexiSpot / Autonomous", "avg_order": 400.00},
            {"category": "focus supplements (nootropics)", "commission": "15-30%", "program": "Onnit / Alpha Brain", "avg_order": 45.00},
            {"category": "noise-canceling headphones", "commission": "3-6%", "program": "Amazon Associates", "avg_order": 250.00},
            {"category": "digital courses", "commission": "30-50%", "program": "Skillshare / Udemy", "avg_order": 30.00},
        ],
        "ad_strategy": "no ads during focus sessions. banner ads on home/dashboard only.",
        "paywall_timing": "after 5 completed tasks or sessions",
        "premium_features": [
            "unlimited focus sessions",
            "advanced time analytics",
            "integrations (calendar, Notion, Todoist)",
            "custom focus modes",
            "team/accountability features",
        ],
        "donation_model": False,
        "notes": "productivity users are tool-obsessed. affiliate for other tools converts well. position price as 'cost of 1 coffee per week for 10x output'. template packs work as IAP.",
    },
    "cooking": {
        "primary": "subscription",
        "secondary": ["affiliate", "iap"],
        "tertiary": ["ads"],
        "subscription_tier": "low",
        "optimal_weekly": 1.99,
        "optimal_monthly": 6.99,
        "optimal_yearly": 34.99,
        "affiliate_categories": [
            {"category": "kitchen tools / gadgets", "commission": "4-8%", "program": "Amazon Associates", "avg_order": 35.00},
            {"category": "meal kit delivery", "commission": "10-20%", "program": "HelloFresh / Blue Apron", "avg_order": 60.00},
            {"category": "specialty ingredients", "commission": "8-15%", "program": "Thrive Market", "avg_order": 50.00},
            {"category": "cookware sets", "commission": "5-10%", "program": "Our Place / Caraway", "avg_order": 150.00},
            {"category": "cooking classes", "commission": "20-40%", "program": "MasterClass / America's Test Kitchen", "avg_order": 120.00},
        ],
        "ad_strategy": "native recipe sponsorships. rewarded video for premium recipes.",
        "paywall_timing": "after 5 saved recipes or 1 week of meal planning",
        "premium_features": [
            "unlimited recipe saves",
            "AI meal planning",
            "grocery list generation",
            "nutritional analysis",
            "premium chef recipes",
        ],
        "donation_model": False,
        "notes": "recipe packs as IAP ($1.99-$4.99 per cuisine pack). kitchen tool affiliate integrates naturally into recipe ingredients. meal kit affiliate on the meal planning screen.",
    },
    "finance": {
        "primary": "subscription",
        "secondary": ["affiliate", "freemium"],
        "tertiary": [],
        "subscription_tier": "high",
        "optimal_weekly": 3.99,
        "optimal_monthly": 12.99,
        "optimal_yearly": 69.99,
        "affiliate_categories": [
            {"category": "investment platforms (Robinhood, Wealthfront)", "commission": "$5-$100 per signup", "program": "Robinhood / Wealthfront Referral", "avg_order": 0},
            {"category": "budgeting tools", "commission": "20-40%", "program": "YNAB / Copilot Affiliate", "avg_order": 99.00},
            {"category": "credit monitoring", "commission": "$20-$50 per signup", "program": "Credit Karma / Experian", "avg_order": 0},
            {"category": "financial books", "commission": "4-8%", "program": "Amazon Associates", "avg_order": 20.00},
            {"category": "tax software", "commission": "15-25%", "program": "TurboTax / H&R Block", "avg_order": 80.00},
        ],
        "ad_strategy": "no ads. finance users expect premium, ad-free experience.",
        "paywall_timing": "after connecting 1 account or 2-week trial",
        "premium_features": [
            "unlimited account connections",
            "AI spending analysis",
            "investment tracking",
            "bill reminders / negotiation",
            "custom financial reports",
            "net worth tracking",
        ],
        "donation_model": False,
        "notes": "finance is the highest-willingness-to-pay niche. per-signup referral commissions for investment platforms are massive ($5-$100 each). no ads, premium feel mandatory. compliance: never give financial advice, only tracking/tools.",
    },
    "aesthetic": {
        "primary": "ads",
        "secondary": ["creator_rewards", "affiliate"],
        "tertiary": ["freemium"],
        "subscription_tier": "low",
        "optimal_weekly": None,
        "optimal_monthly": 2.99,
        "optimal_yearly": 19.99,
        "affiliate_categories": [
            {"category": "print-on-demand merch", "commission": "20-40% margin", "program": "Printful / Printify (own store)", "avg_order": 30.00},
            {"category": "camera gear", "commission": "3-6%", "program": "Amazon / B&H Photo", "avg_order": 200.00},
            {"category": "editing software", "commission": "15-30%", "program": "Adobe / Canva Affiliate", "avg_order": 120.00},
            {"category": "home decor", "commission": "5-10%", "program": "Etsy / Society6", "avg_order": 45.00},
        ],
        "ad_strategy": "native brand deals > programmatic ads. integrate sponsored content aesthetically.",
        "paywall_timing": "optional ad-free tier",
        "premium_features": [
            "ad-free experience",
            "exclusive collections",
            "high-res downloads",
            "early access to new content",
        ],
        "donation_model": False,
        "notes": "aesthetic/curation pages monetize through volume (ads) and brand deals. print-on-demand is the real margin play. never compromise the aesthetic for monetization.",
    },
    "memes": {
        "primary": "ads",
        "secondary": ["creator_rewards", "affiliate"],
        "tertiary": [],
        "subscription_tier": None,
        "optimal_weekly": None,
        "optimal_monthly": None,
        "optimal_yearly": None,
        "affiliate_categories": [
            {"category": "merch / print-on-demand", "commission": "30-50% margin", "program": "Spring / Printful (own store)", "avg_order": 25.00},
            {"category": "gaming accessories", "commission": "4-8%", "program": "Amazon Associates", "avg_order": 40.00},
            {"category": "snacks / novelty food", "commission": "10-20%", "program": "Various DTC brands", "avg_order": 20.00},
        ],
        "ad_strategy": "interstitial between scrolls. banner on home. rewarded video for 'premium' memes.",
        "paywall_timing": "no paywall. monetize through volume.",
        "premium_features": [],
        "donation_model": False,
        "notes": "memes = volume play. 100K+ DAU needed for meaningful ad revenue. merch is the real money. creator fund on X/TikTok if eligible. never paywall memes.",
    },
    "ai_tools": {
        "primary": "subscription",
        "secondary": ["iap", "freemium"],
        "tertiary": ["affiliate"],
        "subscription_tier": "high",
        "optimal_weekly": 4.99,
        "optimal_monthly": 14.99,
        "optimal_yearly": 79.99,
        "affiliate_categories": [
            {"category": "AI API credits (OpenAI, Anthropic)", "commission": "varies", "program": "Usage-based resale", "avg_order": 20.00},
            {"category": "AI courses", "commission": "30-50%", "program": "Udemy / Coursera", "avg_order": 40.00},
            {"category": "developer tools", "commission": "15-30%", "program": "Vercel / Railway / Supabase", "avg_order": 25.00},
        ],
        "ad_strategy": "no ads. AI tool users expect clean, premium UX.",
        "paywall_timing": "after N free generations (5-10 free, then paywall)",
        "premium_features": [
            "unlimited AI generations",
            "premium AI models (GPT-4, Claude Opus)",
            "priority processing",
            "API access",
            "custom model fine-tuning",
            "export in all formats",
        ],
        "donation_model": False,
        "notes": "AI tools have real marginal cost (API calls). subscription must cover API costs + margin. consumable IAP (credit packs) works well. usage tiers: free (5/day) -> basic (50/day) -> pro (unlimited).",
    },
    "outbound": {
        "primary": "subscription",
        "secondary": ["affiliate", "freemium"],
        "tertiary": ["iap"],
        "subscription_tier": "high",
        "optimal_weekly": 4.99,
        "optimal_monthly": 19.99,
        "optimal_yearly": 99.99,
        "affiliate_categories": [
            {"category": "CRM tools", "commission": "20-40%", "program": "HubSpot / Pipedrive Affiliate", "avg_order": 500.00},
            {"category": "email tools", "commission": "20-30%", "program": "Instantly / Lemlist", "avg_order": 97.00},
            {"category": "lead databases", "commission": "15-25%", "program": "Apollo.io / ZoomInfo", "avg_order": 99.00},
            {"category": "sales books/courses", "commission": "4-8% / 30-50%", "program": "Amazon / Gumroad", "avg_order": 30.00},
        ],
        "ad_strategy": "no ads. B2B users expect professional, ad-free tools.",
        "paywall_timing": "after 10 free emails or 1-week trial",
        "premium_features": [
            "unlimited email sequences",
            "AI email writer",
            "CRM integrations",
            "analytics dashboard",
            "team collaboration",
            "premium templates",
        ],
        "donation_model": False,
        "notes": "outbound/sales tools command highest prices. users are paying to make money, so ROI framing works. CRM affiliate commissions are massive (recurring 20-40%). template packs as IAP.",
    },
    "habits": {
        "primary": "subscription",
        "secondary": ["affiliate", "freemium"],
        "tertiary": ["ads"],
        "subscription_tier": "low",
        "optimal_weekly": 1.99,
        "optimal_monthly": 4.99,
        "optimal_yearly": 29.99,
        "affiliate_categories": [
            {"category": "habit books (Atomic Habits, etc.)", "commission": "4-8%", "program": "Amazon Associates", "avg_order": 18.00},
            {"category": "journals / planners", "commission": "10-20%", "program": "Etsy / Amazon", "avg_order": 22.00},
            {"category": "wellness supplements", "commission": "15-30%", "program": "AG1 / Athletic Greens", "avg_order": 79.00},
            {"category": "mindfulness apps", "commission": "20-40%", "program": "Headspace / Calm referral", "avg_order": 70.00},
        ],
        "ad_strategy": "rewarded video for streak protection. no ads during habit logging.",
        "paywall_timing": "after tracking 3 habits for 7 days free",
        "premium_features": [
            "unlimited habits",
            "advanced analytics / streaks",
            "custom reminders",
            "habit stacking suggestions",
            "community / accountability partners",
            "widget support",
        ],
        "donation_model": False,
        "notes": "habit apps have the highest retention potential. streak mechanics create natural lock-in. AG1/supplement affiliate works because health-conscious habit trackers overlap. streak freeze as consumable IAP ($0.99).",
    },
}


# ---------------------------------------------------------------------------
# 3. COMPETITOR PRICING ANALYSIS (hardcoded from research)
# ---------------------------------------------------------------------------

COMPETITOR_PRICING = {
    "faith": {
        "competitors": [
            {"name": "Pray.com", "monthly": 9.99, "yearly": 49.99, "downloads": "10M+", "rating": 4.8},
            {"name": "Hallow", "monthly": 12.99, "yearly": 69.99, "downloads": "5M+", "rating": 4.9},
            {"name": "Glorify", "monthly": 11.99, "yearly": 59.99, "downloads": "1M+", "rating": 4.7},
            {"name": "Abide", "monthly": 9.99, "yearly": 59.99, "downloads": "5M+", "rating": 4.8},
            {"name": "Bible App (YouVersion)", "monthly": 0.00, "yearly": 0.00, "downloads": "500M+", "rating": 4.9},
        ],
        "avg_monthly": 11.24,
        "avg_yearly": 59.99,
        "recommended_monthly": 9.99,
        "recommended_yearly": 49.99,
        "strategy_note": "slightly undercut Pray.com and Hallow. YouVersion is free but lacks premium devotional content.",
    },
    "fitness": {
        "competitors": [
            {"name": "Strava", "monthly": 11.99, "yearly": 79.99, "downloads": "100M+", "rating": 4.5},
            {"name": "Nike Run Club", "monthly": 0.00, "yearly": 0.00, "downloads": "50M+", "rating": 4.7},
            {"name": "Fitbod", "monthly": 12.99, "yearly": 79.99, "downloads": "1M+", "rating": 4.6},
            {"name": "Strong", "monthly": 9.99, "yearly": 39.99, "downloads": "5M+", "rating": 4.7},
            {"name": "SWEAT", "monthly": 19.99, "yearly": 119.99, "downloads": "10M+", "rating": 4.6},
        ],
        "avg_monthly": 10.99,
        "avg_yearly": 63.99,
        "recommended_monthly": 9.99,
        "recommended_yearly": 49.99,
        "strategy_note": "match Strong's pricing. undercut Strava/Fitbod. niche down to specific workout type for differentiation.",
    },
    "sleep": {
        "competitors": [
            {"name": "Calm", "monthly": 14.99, "yearly": 69.99, "downloads": "100M+", "rating": 4.4},
            {"name": "Headspace", "monthly": 12.99, "yearly": 69.99, "downloads": "70M+", "rating": 4.5},
            {"name": "Sleep Cycle", "monthly": 9.99, "yearly": 39.99, "downloads": "50M+", "rating": 4.5},
            {"name": "Pillow", "monthly": 4.99, "yearly": 29.99, "downloads": "1M+", "rating": 4.3},
            {"name": "BetterSleep", "monthly": 9.99, "yearly": 49.99, "downloads": "10M+", "rating": 4.7},
        ],
        "avg_monthly": 10.59,
        "avg_yearly": 51.99,
        "recommended_monthly": 7.99,
        "recommended_yearly": 39.99,
        "strategy_note": "undercut Calm/Headspace significantly. match Sleep Cycle. sleep-specific positioning vs meditation-first competitors.",
    },
    "productivity": {
        "competitors": [
            {"name": "Forest", "monthly": 0.00, "yearly": 0.00, "downloads": "10M+", "rating": 4.7},
            {"name": "Focus Bear", "monthly": 6.99, "yearly": 39.99, "downloads": "100K+", "rating": 4.5},
            {"name": "Be Focused", "monthly": 0.00, "yearly": 0.00, "downloads": "1M+", "rating": 4.5},
            {"name": "Structured", "monthly": 4.99, "yearly": 29.99, "downloads": "500K+", "rating": 4.7},
            {"name": "Notion", "monthly": 10.00, "yearly": 96.00, "downloads": "50M+", "rating": 4.7},
        ],
        "avg_monthly": 4.40,
        "avg_yearly": 33.20,
        "recommended_monthly": 6.99,
        "recommended_yearly": 39.99,
        "strategy_note": "Forest is a one-time purchase ($3.99). Notion is a different category. focus on Structured/Focus Bear price range. gamification is the differentiator.",
    },
    "cooking": {
        "competitors": [
            {"name": "Mealime", "monthly": 5.99, "yearly": 29.99, "downloads": "5M+", "rating": 4.6},
            {"name": "Paprika", "monthly": 0.00, "yearly": 0.00, "downloads": "1M+", "rating": 4.5},
            {"name": "Yummly", "monthly": 4.99, "yearly": 29.99, "downloads": "10M+", "rating": 4.7},
            {"name": "Whisk", "monthly": 0.00, "yearly": 0.00, "downloads": "1M+", "rating": 4.4},
            {"name": "SideChef", "monthly": 9.99, "yearly": 59.99, "downloads": "1M+", "rating": 4.5},
        ],
        "avg_monthly": 4.19,
        "avg_yearly": 23.99,
        "recommended_monthly": 6.99,
        "recommended_yearly": 34.99,
        "strategy_note": "Paprika is one-time $4.99. cooking apps are price-sensitive. AI meal planning is the premium differentiator that justifies subscription.",
    },
    "finance": {
        "competitors": [
            {"name": "Mint (Credit Karma)", "monthly": 0.00, "yearly": 0.00, "downloads": "50M+", "rating": 4.6},
            {"name": "YNAB", "monthly": 14.99, "yearly": 99.00, "downloads": "5M+", "rating": 4.8},
            {"name": "Copilot", "monthly": 14.99, "yearly": 95.88, "downloads": "500K+", "rating": 4.8},
            {"name": "Rocket Money", "monthly": 12.00, "yearly": 48.00, "downloads": "10M+", "rating": 4.6},
            {"name": "PocketGuard", "monthly": 7.99, "yearly": 34.99, "downloads": "5M+", "rating": 4.5},
        ],
        "avg_monthly": 9.99,
        "avg_yearly": 55.57,
        "recommended_monthly": 12.99,
        "recommended_yearly": 69.99,
        "strategy_note": "match Copilot. finance users pay premium for quality. YNAB has strong brand loyalty. differentiate with AI analysis and simpler UX.",
    },
    "habits": {
        "competitors": [
            {"name": "Streaks", "monthly": 0.00, "yearly": 0.00, "downloads": "1M+", "rating": 4.7},
            {"name": "HabitNow", "monthly": 2.99, "yearly": 14.99, "downloads": "5M+", "rating": 4.5},
            {"name": "Habitica", "monthly": 4.99, "yearly": 47.99, "downloads": "5M+", "rating": 4.3},
            {"name": "Productive", "monthly": 6.99, "yearly": 39.99, "downloads": "1M+", "rating": 4.6},
            {"name": "Atoms", "monthly": 4.99, "yearly": 29.99, "downloads": "500K+", "rating": 4.7},
        ],
        "avg_monthly": 3.99,
        "avg_yearly": 26.59,
        "recommended_monthly": 4.99,
        "recommended_yearly": 29.99,
        "strategy_note": "Streaks is Apple Design Award winner, one-time $4.99. habit apps are price-sensitive. gamification (streaks, badges) drives retention better than features.",
    },
}


# ---------------------------------------------------------------------------
# Current PRINTMAXX Apps
# ---------------------------------------------------------------------------

CURRENT_APPS = {
    "prayerlock": {"niche": "faith", "description": "prayer tracking and devotional app"},
    "dusk": {"niche": "sleep", "description": "sleep tracking and sounds app"},
    "vault": {"niche": "finance", "description": "personal finance and budget tracking"},
    "streakr": {"niche": "habits", "description": "habit tracking with streak mechanics"},
    "mise": {"niche": "cooking", "description": "AI meal planning and recipe management"},
    "steplock": {"niche": "fitness", "description": "step-based fitness gamification"},
}


# ---------------------------------------------------------------------------
# 4. REVENUE PROJECTION
# ---------------------------------------------------------------------------

def project_revenue(niche: str, monthly_downloads: int) -> dict:
    """Project monthly revenue across pessimistic, realistic, optimistic scenarios."""
    strategy = NICHE_STRATEGIES.get(niche)
    pricing = COMPETITOR_PRICING.get(niche, {})
    if not strategy:
        return {"error": f"unknown niche: {niche}"}

    monthly_price = strategy.get("optimal_monthly") or pricing.get("recommended_monthly", 9.99)
    yearly_price = strategy.get("optimal_yearly") or pricing.get("recommended_yearly", 49.99)
    apple_cut = 0.30  # first year

    scenarios = {
        "pessimistic": {"conversion_rate": 0.01, "label": "1% conversion"},
        "realistic": {"conversion_rate": 0.03, "label": "3% conversion"},
        "optimistic": {"conversion_rate": 0.07, "label": "7% conversion"},
    }

    results = {}
    for scenario_name, scenario in scenarios.items():
        cr = scenario["conversion_rate"]
        subscribers = int(monthly_downloads * cr)
        # Assume 70% choose monthly, 30% choose yearly (paying yearly_price/12 per month)
        monthly_subs = int(subscribers * 0.70)
        yearly_subs = int(subscribers * 0.30)

        gross_monthly = (monthly_subs * monthly_price) + (yearly_subs * (yearly_price / 12))
        net_monthly = gross_monthly * (1 - apple_cut)

        # Estimate affiliate revenue (2% of free users click, 5% of those convert)
        free_users = monthly_downloads - subscribers
        affiliate_clicks = int(free_users * 0.02)
        affiliate_conversions = int(affiliate_clicks * 0.05)
        avg_commission = 8.00  # rough avg across categories
        affiliate_revenue = affiliate_conversions * avg_commission

        # Ad revenue estimate (for niches that use ads)
        ad_revenue = 0.0
        if "ads" in strategy.get("secondary", []) + strategy.get("tertiary", []):
            dau_estimate = int(free_users * 0.15)  # 15% DAU
            ad_impressions = dau_estimate * 3  # 3 ad views per session
            avg_cpm = 15.0  # rewarded video avg
            ad_revenue = (ad_impressions / 1000) * avg_cpm * 30  # monthly

        total_monthly = net_monthly + affiliate_revenue + ad_revenue

        results[scenario_name] = {
            "label": scenario["label"],
            "monthly_downloads": monthly_downloads,
            "conversion_rate": cr,
            "paying_users": subscribers,
            "monthly_subscribers": monthly_subs,
            "yearly_subscribers": yearly_subs,
            "subscription_gross": round(gross_monthly, 2),
            "subscription_net": round(net_monthly, 2),
            "affiliate_revenue": round(affiliate_revenue, 2),
            "ad_revenue": round(ad_revenue, 2),
            "total_monthly_revenue": round(total_monthly, 2),
            "total_yearly_revenue": round(total_monthly * 12, 2),
        }

    return results


# ---------------------------------------------------------------------------
# 5. AUTO-GENERATE: RevenueCat config, affiliate placements, ad placements, paywall copy
# ---------------------------------------------------------------------------

def generate_revenuecat_config(app_name: str, niche: str) -> dict:
    """Generate RevenueCat product IDs and subscription groups."""
    strategy = NICHE_STRATEGIES.get(niche, {})
    prefix = app_name.lower().replace(" ", "_").replace("-", "_")

    config = {
        "app_name": app_name,
        "revenuecat_project": f"rc_{prefix}",
        "entitlements": [
            {
                "id": f"{prefix}_premium",
                "display_name": f"{app_name} Premium",
                "description": "Full access to all premium features",
            }
        ],
        "offerings": [
            {
                "id": f"{prefix}_default",
                "display_name": "Default Offering",
                "packages": [],
            }
        ],
        "products": [],
        "subscription_group": f"{prefix}_subscriptions",
    }

    # Add subscription products based on niche pricing
    if strategy.get("optimal_weekly"):
        config["products"].append({
            "id": f"{prefix}_weekly",
            "type": "auto_renewable_subscription",
            "price": strategy["optimal_weekly"],
            "period": "P1W",
            "trial": "P3D",
            "store_product_id": f"{prefix}.weekly",
        })
        config["offerings"][0]["packages"].append({
            "id": "$rc_weekly",
            "product_id": f"{prefix}_weekly",
        })

    if strategy.get("optimal_monthly"):
        config["products"].append({
            "id": f"{prefix}_monthly",
            "type": "auto_renewable_subscription",
            "price": strategy["optimal_monthly"],
            "period": "P1M",
            "trial": "P7D",
            "store_product_id": f"{prefix}.monthly",
        })
        config["offerings"][0]["packages"].append({
            "id": "$rc_monthly",
            "product_id": f"{prefix}_monthly",
        })

    if strategy.get("optimal_yearly"):
        config["products"].append({
            "id": f"{prefix}_yearly",
            "type": "auto_renewable_subscription",
            "price": strategy["optimal_yearly"],
            "period": "P1Y",
            "trial": "P7D",
            "store_product_id": f"{prefix}.yearly",
            "introductory_offer": {
                "type": "pay_up_front",
                "price": round(strategy["optimal_yearly"] * 0.5, 2),
                "period": "P1Y",
                "cycles": 1,
            },
        })
        config["offerings"][0]["packages"].append({
            "id": "$rc_annual",
            "product_id": f"{prefix}_yearly",
        })

    # Add lifetime IAP
    config["products"].append({
        "id": f"{prefix}_lifetime",
        "type": "non_consumable",
        "price": round((strategy.get("optimal_yearly") or 49.99) * 3, 2),
        "store_product_id": f"{prefix}.lifetime",
    })

    return config


def generate_affiliate_placements(niche: str) -> list:
    """Generate recommended affiliate link integration points in the app flow."""
    strategy = NICHE_STRATEGIES.get(niche, {})
    affiliates = strategy.get("affiliate_categories", [])

    placements = []
    placement_templates = {
        "faith": [
            {"screen": "post_prayer_completion", "trigger": "after completing a prayer session", "type": "contextual_recommendation"},
            {"screen": "devotional_reading", "trigger": "after reading daily devotional", "type": "related_product"},
            {"screen": "settings_recommendations", "trigger": "user browses recommendations section", "type": "curated_list"},
            {"screen": "weekly_reflection", "trigger": "weekly prayer summary screen", "type": "suggested_resource"},
        ],
        "fitness": [
            {"screen": "post_workout_summary", "trigger": "after completing a workout", "type": "recovery_recommendation"},
            {"screen": "nutrition_tab", "trigger": "viewing nutrition/macro info", "type": "supplement_suggestion"},
            {"screen": "equipment_needed", "trigger": "workout requires equipment user doesn't have", "type": "equipment_link"},
            {"screen": "progress_milestone", "trigger": "hitting a fitness milestone", "type": "reward_recommendation"},
        ],
        "sleep": [
            {"screen": "sleep_report", "trigger": "viewing morning sleep report", "type": "improvement_suggestion"},
            {"screen": "sleep_environment", "trigger": "browsing sleep improvement tips", "type": "product_recommendation"},
            {"screen": "bedtime_routine", "trigger": "setting up bedtime routine", "type": "relaxation_product"},
            {"screen": "weekly_sleep_summary", "trigger": "weekly sleep score review", "type": "upgrade_suggestion"},
        ],
        "productivity": [
            {"screen": "focus_complete", "trigger": "after a focus session ends", "type": "tool_recommendation"},
            {"screen": "analytics_dashboard", "trigger": "reviewing productivity analytics", "type": "optimization_tool"},
            {"screen": "integration_settings", "trigger": "looking at app integrations", "type": "partner_tool"},
            {"screen": "tips_section", "trigger": "browsing productivity tips", "type": "resource_link"},
        ],
        "cooking": [
            {"screen": "recipe_detail", "trigger": "viewing a recipe's ingredients", "type": "ingredient_source"},
            {"screen": "grocery_list", "trigger": "generating a shopping list", "type": "delivery_service"},
            {"screen": "equipment_tag", "trigger": "recipe needs specific equipment", "type": "equipment_link"},
            {"screen": "meal_plan_complete", "trigger": "completing weekly meal plan", "type": "kit_recommendation"},
        ],
        "finance": [
            {"screen": "investment_overview", "trigger": "viewing investment summary", "type": "platform_referral"},
            {"screen": "budget_optimization", "trigger": "AI suggests savings opportunities", "type": "tool_suggestion"},
            {"screen": "credit_score", "trigger": "viewing credit-related info", "type": "monitoring_referral"},
            {"screen": "tax_season", "trigger": "Q1 tax prep reminder", "type": "software_recommendation"},
        ],
        "habits": [
            {"screen": "habit_complete", "trigger": "after completing daily habits", "type": "wellness_recommendation"},
            {"screen": "streak_milestone", "trigger": "hitting 7/30/100 day streaks", "type": "celebration_suggestion"},
            {"screen": "habit_suggestions", "trigger": "browsing suggested new habits", "type": "resource_link"},
            {"screen": "weekly_review", "trigger": "weekly habit summary", "type": "improvement_product"},
        ],
    }

    templates = placement_templates.get(niche, placement_templates.get("productivity", []))

    for i, template in enumerate(templates):
        affiliate = affiliates[i % len(affiliates)] if affiliates else {}
        placements.append({
            **template,
            "affiliate_category": affiliate.get("category", "general"),
            "program": affiliate.get("program", "Amazon Associates"),
            "commission": affiliate.get("commission", "4-8%"),
            "disclosure": "FTC disclosure required. use 'recommended for you (affiliate link)' or similar.",
            "ux_note": "must feel native, not spammy. contextual relevance is everything.",
        })

    return placements


def generate_ad_placements(niche: str) -> list:
    """Generate ad placement recommendations for the niche."""
    strategy = NICHE_STRATEGIES.get(niche, {})

    if strategy.get("primary") != "ads" and "ads" not in strategy.get("secondary", []) + strategy.get("tertiary", []):
        return [{"recommendation": f"ads not recommended for {niche}. focus on subscription + affiliate instead."}]

    placements = []

    if niche in ("memes", "aesthetic"):
        placements = [
            {
                "type": "banner",
                "location": "bottom of feed/home screen",
                "frequency": "always visible",
                "estimated_cpm": 2.00,
                "note": "use AdMob adaptive banner. must not obstruct content.",
            },
            {
                "type": "interstitial",
                "location": "between content pages (every 5th swipe)",
                "frequency": "max 1 per 2 minutes",
                "estimated_cpm": 12.00,
                "note": "frequency cap prevents user fatigue. skip button after 5s.",
            },
            {
                "type": "rewarded_video",
                "location": "unlock premium content / remove ads for 30 min",
                "frequency": "user-initiated, max 5 per day",
                "estimated_cpm": 30.00,
                "note": "highest CPM. user chooses to watch. reward must feel valuable.",
            },
        ]
    else:
        placements = [
            {
                "type": "rewarded_video",
                "location": "unlock premium feature for 24h / streak protection",
                "frequency": "user-initiated, max 3 per day",
                "estimated_cpm": 25.00,
                "note": "only ad type. keeps experience clean. user opts in.",
            },
        ]

    return placements


def generate_paywall_copy(app_name: str, niche: str) -> dict:
    """Generate paywall copy suggestions in PRINTMAXXER voice."""
    strategy = NICHE_STRATEGIES.get(niche, {})
    pricing = COMPETITOR_PRICING.get(niche, {})

    monthly_price = strategy.get("optimal_monthly") or 9.99
    yearly_price = strategy.get("optimal_yearly") or 49.99
    yearly_monthly_equiv = round(yearly_price / 12, 2)
    savings_pct = round((1 - (yearly_price / (monthly_price * 12))) * 100)

    # Niche-specific headline and features
    niche_copy = {
        "faith": {
            "headline": "your prayer life. upgraded.",
            "subhead": f"unlimited devotionals, prayer tracking, and community. less than a coffee per week.",
            "value_prop": "people spend $5 on coffee that lasts 20 minutes. this lasts all day, every day.",
            "social_proof": "join 10,000+ believers deepening their prayer practice",
            "features_headline": "everything you get with premium:",
        },
        "fitness": {
            "headline": "stop guessing. start growing.",
            "subhead": f"personalized workouts, real analytics, and recovery tracking. less than 1 gym visit per month.",
            "value_prop": f"${monthly_price}/mo. that's less than a single protein shake at the gym.",
            "social_proof": "athletes who track progress gain 2.4x more strength (Journal of Strength Research)",
            "features_headline": "unlock your full potential:",
        },
        "sleep": {
            "headline": "sleep better tonight.",
            "subhead": f"smart alarm, sleep sounds, and sleep coaching. {yearly_monthly_equiv}/mo with annual.",
            "value_prop": f"better sleep = better everything. ${yearly_monthly_equiv}/mo is less than one bad night costs your productivity.",
            "social_proof": "users report falling asleep 23 minutes faster on average",
            "features_headline": "wake up feeling different:",
        },
        "productivity": {
            "headline": "your focus. multiplied.",
            "subhead": f"deep focus sessions, smart analytics, and zero distractions. ${yearly_monthly_equiv}/mo.",
            "value_prop": f"${monthly_price}/mo to save 2+ hours per day. the ROI is borderline illegal.",
            "social_proof": "average user saves 14 hours per week with focused work sessions",
            "features_headline": "the tools your brain needs:",
        },
        "cooking": {
            "headline": "dinner. solved.",
            "subhead": f"AI meal plans, smart grocery lists, and premium recipes. less than one takeout order per month.",
            "value_prop": f"you spend $40+ on one takeout order. ${monthly_price}/mo saves you $200+ on groceries with better meals.",
            "social_proof": "users save an average of $127/month on food costs",
            "features_headline": "never ask 'what's for dinner' again:",
        },
        "finance": {
            "headline": "see where every dollar goes.",
            "subhead": f"AI analysis, investment tracking, bill negotiation. pays for itself in the first week.",
            "value_prop": f"${monthly_price}/mo. users find an average of $340/mo in savings they didn't know they had.",
            "social_proof": "85% of premium users save more than the subscription cost in their first month",
            "features_headline": "your money. your rules:",
        },
        "habits": {
            "headline": "don't break the chain.",
            "subhead": f"unlimited habits, streak protection, and smart insights. ${yearly_monthly_equiv}/mo.",
            "value_prop": f"${monthly_price}/mo to build the life you actually want. cheaper than the gym membership you never use.",
            "social_proof": "users with 30+ day streaks report 67% higher life satisfaction",
            "features_headline": "everything you need to stick with it:",
        },
    }

    copy = niche_copy.get(niche, {
        "headline": f"{app_name}. upgraded.",
        "subhead": f"unlock everything for ${yearly_monthly_equiv}/mo.",
        "value_prop": f"${monthly_price}/mo for something that actually improves your life.",
        "social_proof": "thousands of users already upgraded",
        "features_headline": "what you get:",
    })

    copy["pricing_display"] = {
        "monthly": {
            "label": "monthly",
            "price": f"${monthly_price}",
            "period": "/mo",
            "note": "cancel anytime",
        },
        "yearly": {
            "label": "yearly",
            "price": f"${yearly_monthly_equiv}",
            "period": "/mo",
            "note": f"billed ${yearly_price}/yr. save {savings_pct}%.",
            "badge": "most popular" if savings_pct >= 40 else f"save {savings_pct}%",
            "recommended": True,
        },
    }

    if strategy.get("optimal_weekly"):
        copy["pricing_display"]["weekly"] = {
            "label": "weekly",
            "price": f"${strategy['optimal_weekly']}",
            "period": "/wk",
            "note": "3-day free trial",
        }

    copy["cta_button"] = "start free trial"
    copy["cta_subtext"] = "7-day free trial. cancel anytime. no commitment."
    copy["premium_features"] = strategy.get("premium_features", [])
    copy["close_button_note"] = "always show X/close button. apple rejects hidden close buttons."

    return copy


# ---------------------------------------------------------------------------
# OUTPUT / DISPLAY
# ---------------------------------------------------------------------------

def print_separator(char: str = "=", width: int = 80):
    print(char * width)


def print_header(title: str):
    print()
    print_separator()
    print(f"  {title.upper()}")
    print_separator()
    print()


def display_full_analysis(app_name: str, niche: str):
    """Full monetization analysis for an app."""
    strategy = NICHE_STRATEGIES.get(niche)
    pricing = COMPETITOR_PRICING.get(niche)

    if not strategy:
        print(f"error: unknown niche '{niche}'. available: {', '.join(NICHE_STRATEGIES.keys())}")
        return

    print_header(f"monetization analysis: {app_name} ({niche})")

    # Strategy overview
    print("STRATEGY OVERVIEW")
    print(f"  primary model:   {strategy['primary']}")
    print(f"  secondary:       {', '.join(strategy['secondary'])}")
    if strategy.get("tertiary"):
        print(f"  tertiary:        {', '.join(strategy['tertiary'])}")
    print(f"  donation model:  {'yes' if strategy.get('donation_model') else 'no'}")
    print()
    print(f"  notes: {strategy.get('notes', '')}")
    print()

    # Pricing
    print_separator("-")
    print("RECOMMENDED PRICING")
    if strategy.get("optimal_weekly"):
        print(f"  weekly:   ${strategy['optimal_weekly']}")
    if strategy.get("optimal_monthly"):
        print(f"  monthly:  ${strategy['optimal_monthly']}")
    if strategy.get("optimal_yearly"):
        print(f"  yearly:   ${strategy['optimal_yearly']}")
    print()

    # Competitor analysis
    if pricing:
        print_separator("-")
        print("COMPETITOR PRICING")
        for comp in pricing.get("competitors", []):
            m = f"${comp['monthly']}" if comp["monthly"] > 0 else "free"
            y = f"${comp['yearly']}" if comp["yearly"] > 0 else "free"
            print(f"  {comp['name']:20s}  monthly: {m:>8s}  yearly: {y:>8s}  downloads: {comp['downloads']:>8s}  rating: {comp['rating']}")
        print()
        print(f"  avg monthly: ${pricing.get('avg_monthly', 'N/A')}")
        print(f"  avg yearly:  ${pricing.get('avg_yearly', 'N/A')}")
        print(f"  our monthly: ${pricing.get('recommended_monthly', 'N/A')}")
        print(f"  our yearly:  ${pricing.get('recommended_yearly', 'N/A')}")
        print(f"  strategy:    {pricing.get('strategy_note', '')}")
        print()

    # Affiliate programs
    print_separator("-")
    print("AFFILIATE PROGRAMS")
    for aff in strategy.get("affiliate_categories", []):
        print(f"  {aff['category']:40s}  commission: {aff['commission']:>10s}  via: {aff['program']}")
    print()

    # Premium features
    print_separator("-")
    print("PREMIUM FEATURES")
    for feat in strategy.get("premium_features", []):
        print(f"  - {feat}")
    print()

    # Ad strategy
    print_separator("-")
    print("AD STRATEGY")
    print(f"  {strategy.get('ad_strategy', 'N/A')}")
    print()

    # Paywall timing
    print_separator("-")
    print("PAYWALL TIMING")
    print(f"  {strategy.get('paywall_timing', 'N/A')}")
    print()

    # Revenue projection (estimate 5K downloads/month as baseline)
    print_separator("-")
    print("REVENUE PROJECTION (5,000 downloads/month)")
    projections = project_revenue(niche, 5000)
    for name, data in projections.items():
        print(f"  {name:12s} ({data['label']}): ${data['total_monthly_revenue']:>10,.2f}/mo  |  ${data['total_yearly_revenue']:>12,.2f}/yr  |  {data['paying_users']} paying users")
    print()


def display_pricing(niche: str):
    """Display pricing recommendations for a niche."""
    strategy = NICHE_STRATEGIES.get(niche)
    pricing = COMPETITOR_PRICING.get(niche)

    if not strategy:
        print(f"error: unknown niche '{niche}'. available: {', '.join(NICHE_STRATEGIES.keys())}")
        return

    print_header(f"pricing recommendations: {niche}")

    print("OUR RECOMMENDED PRICING")
    if strategy.get("optimal_weekly"):
        print(f"  weekly:   ${strategy['optimal_weekly']}")
    if strategy.get("optimal_monthly"):
        print(f"  monthly:  ${strategy['optimal_monthly']}")
    if strategy.get("optimal_yearly"):
        print(f"  yearly:   ${strategy['optimal_yearly']}")
    print()

    if pricing:
        print("COMPETITOR LANDSCAPE")
        for comp in pricing.get("competitors", []):
            m = f"${comp['monthly']}" if comp["monthly"] > 0 else "free"
            y = f"${comp['yearly']}" if comp["yearly"] > 0 else "free"
            print(f"  {comp['name']:20s}  {m:>8s}/mo  {y:>8s}/yr  {comp['downloads']:>8s} downloads")
        print()
        print(f"  market avg:  ${pricing.get('avg_monthly', 'N/A')}/mo  |  ${pricing.get('avg_yearly', 'N/A')}/yr")
        print(f"  strategy:    {pricing.get('strategy_note', '')}")
    print()


def display_revenue(niche: str, downloads: int):
    """Display revenue projections."""
    if niche not in NICHE_STRATEGIES:
        print(f"error: unknown niche '{niche}'. available: {', '.join(NICHE_STRATEGIES.keys())}")
        return

    print_header(f"revenue projection: {niche} ({downloads:,} downloads/month)")

    projections = project_revenue(niche, downloads)
    for name, data in projections.items():
        print(f"  {name.upper()} ({data['label']})")
        print(f"    paying users:        {data['paying_users']:>8,}")
        print(f"    subscription (net):   ${data['subscription_net']:>10,.2f}/mo")
        print(f"    affiliate revenue:    ${data['affiliate_revenue']:>10,.2f}/mo")
        print(f"    ad revenue:           ${data['ad_revenue']:>10,.2f}/mo")
        print(f"    TOTAL MONTHLY:        ${data['total_monthly_revenue']:>10,.2f}/mo")
        print(f"    TOTAL YEARLY:         ${data['total_yearly_revenue']:>10,.2f}/yr")
        print()


def display_affiliates(niche: str):
    """Display affiliate program recommendations."""
    strategy = NICHE_STRATEGIES.get(niche)
    if not strategy:
        print(f"error: unknown niche '{niche}'. available: {', '.join(NICHE_STRATEGIES.keys())}")
        return

    print_header(f"affiliate programs: {niche}")

    print("RECOMMENDED AFFILIATE PROGRAMS")
    print()
    for aff in strategy.get("affiliate_categories", []):
        print(f"  category:    {aff['category']}")
        print(f"  commission:  {aff['commission']}")
        print(f"  program:     {aff['program']}")
        if aff.get("avg_order"):
            print(f"  avg order:   ${aff['avg_order']:.2f}")
            # Estimate per-conversion revenue
            comm_str = aff["commission"]
            if "%" in comm_str:
                # Take mid-point of range
                nums = [float(x.replace("%", "").strip()) for x in comm_str.split("-") if x.replace("%", "").replace(".", "").strip().isdigit()]
                if nums:
                    mid_pct = sum(nums) / len(nums) / 100
                    est_commission = aff["avg_order"] * mid_pct
                    print(f"  est/sale:    ${est_commission:.2f}")
        print()

    print("INTEGRATION POINTS (where in the app)")
    placements = generate_affiliate_placements(niche)
    for p in placements:
        print(f"  screen:    {p['screen']}")
        print(f"  trigger:   {p['trigger']}")
        print(f"  type:      {p['type']}")
        print(f"  category:  {p['affiliate_category']}")
        print(f"  note:      {p['disclosure']}")
        print()


def generate_monetization_config(app_name: str, niche: str):
    """Generate full monetization configuration and save to file."""
    if niche not in NICHE_STRATEGIES:
        print(f"error: unknown niche '{niche}'. available: {', '.join(NICHE_STRATEGIES.keys())}")
        return

    print_header(f"generating monetization config: {app_name} ({niche})")

    config = {
        "app_name": app_name,
        "niche": niche,
        "generated_at": datetime.now().isoformat(),
        "strategy": NICHE_STRATEGIES[niche],
        "competitor_pricing": COMPETITOR_PRICING.get(niche, {}),
        "revenuecat_config": generate_revenuecat_config(app_name, niche),
        "affiliate_placements": generate_affiliate_placements(niche),
        "ad_placements": generate_ad_placements(niche),
        "paywall_copy": generate_paywall_copy(app_name, niche),
        "revenue_projections": {
            "at_1k_downloads": project_revenue(niche, 1000),
            "at_5k_downloads": project_revenue(niche, 5000),
            "at_10k_downloads": project_revenue(niche, 10000),
            "at_50k_downloads": project_revenue(niche, 50000),
        },
    }

    # Save config
    output_dir = safe_path(PROJECT_ROOT / "AUTOMATIONS" / "monetization_configs")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{app_name.lower().replace(' ', '_')}_monetization.json"
    output_path = safe_path(output_dir / filename)

    with open(output_path, "w") as f:
        json.dump(config, f, indent=2, default=str)

    print(f"config saved to: {output_path}")
    print()

    # Print summary
    rc = config["revenuecat_config"]
    print("REVENUECAT PRODUCT IDS")
    for product in rc["products"]:
        print(f"  {product['id']:30s}  ${product['price']:>8.2f}  ({product.get('period', 'one-time')})")
    print(f"  subscription group: {rc['subscription_group']}")
    print()

    print("AFFILIATE INTEGRATION POINTS")
    for p in config["affiliate_placements"]:
        print(f"  [{p['screen']}] {p['affiliate_category']} via {p['program']}")
    print()

    print("AD PLACEMENTS")
    for p in config["ad_placements"]:
        if "recommendation" in p:
            print(f"  {p['recommendation']}")
        else:
            print(f"  [{p['type']}] {p['location']} (est CPM: ${p['estimated_cpm']})")
    print()

    print("PAYWALL COPY")
    pw = config["paywall_copy"]
    print(f"  headline: {pw.get('headline', '')}")
    print(f"  subhead:  {pw.get('subhead', '')}")
    print(f"  value:    {pw.get('value_prop', '')}")
    print(f"  proof:    {pw.get('social_proof', '')}")
    print(f"  cta:      {pw.get('cta_button', '')}")
    print()

    # Print revenue projections table
    print("REVENUE PROJECTIONS")
    print(f"  {'downloads/mo':>14s}  {'pessimistic':>14s}  {'realistic':>14s}  {'optimistic':>14s}")
    for label, key in [("1,000", "at_1k_downloads"), ("5,000", "at_5k_downloads"),
                       ("10,000", "at_10k_downloads"), ("50,000", "at_50k_downloads")]:
        proj = config["revenue_projections"][key]
        p = proj["pessimistic"]["total_monthly_revenue"]
        r = proj["realistic"]["total_monthly_revenue"]
        o = proj["optimistic"]["total_monthly_revenue"]
        print(f"  {label:>14s}  ${p:>12,.2f}  ${r:>12,.2f}  ${o:>12,.2f}")
    print()

    return config


def analyze_all_apps():
    """Analyze all current PRINTMAXX apps."""
    print_header("PRINTMAXX APP PORTFOLIO MONETIZATION ANALYSIS")
    print(f"  analyzing {len(CURRENT_APPS)} apps: {', '.join(CURRENT_APPS.keys())}")
    print()

    total_realistic_monthly = 0.0

    for app_name, info in CURRENT_APPS.items():
        niche = info["niche"]
        strategy = NICHE_STRATEGIES.get(niche, {})
        pricing = COMPETITOR_PRICING.get(niche, {})

        print_separator("=")
        print(f"  {app_name.upper()} ({niche}) - {info['description']}")
        print_separator("-")

        print(f"  primary model:  {strategy.get('primary', 'N/A')}")
        print(f"  monthly price:  ${strategy.get('optimal_monthly', 'N/A')}")
        print(f"  yearly price:   ${strategy.get('optimal_yearly', 'N/A')}")

        # Revenue at 5K downloads
        proj = project_revenue(niche, 5000)
        realistic = proj.get("realistic", {})
        total_realistic_monthly += realistic.get("total_monthly_revenue", 0)
        print(f"  revenue @5K/mo: ${realistic.get('total_monthly_revenue', 0):,.2f}/mo (realistic)")

        # Top affiliate
        affiliates = strategy.get("affiliate_categories", [])
        if affiliates:
            print(f"  top affiliate:  {affiliates[0]['category']} ({affiliates[0]['commission']})")

        print(f"  paywall:        {strategy.get('paywall_timing', 'N/A')}")
        print()

    print_separator("=")
    print(f"  PORTFOLIO TOTAL (realistic, 5K downloads each): ${total_realistic_monthly:,.2f}/mo  |  ${total_realistic_monthly * 12:,.2f}/yr")
    print_separator("=")
    print()

    # Generate configs for all
    print("generating monetization configs for all apps...")
    for app_name, info in CURRENT_APPS.items():
        generate_monetization_config(app_name, info["niche"])
    print()
    print("done. all configs saved to AUTOMATIONS/monetization_configs/")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Monetization Engine - optimal monetization strategy for any app",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python3 monetization_engine.py --analyze prayerlock --niche faith
  python3 monetization_engine.py --pricing sleep
  python3 monetization_engine.py --revenue fitness --downloads 10000
  python3 monetization_engine.py --affiliates cooking
  python3 monetization_engine.py --generate dusk --niche sleep
  python3 monetization_engine.py --all

available niches: faith, fitness, sleep, productivity, cooking, finance,
                  aesthetic, memes, ai_tools, outbound, habits

current apps: prayerlock (faith), dusk (sleep), vault (finance),
              streakr (habits), mise (cooking), steplock (fitness)
        """,
    )

    parser.add_argument("--analyze", metavar="APP_NAME", help="full monetization analysis for an app")
    parser.add_argument("--niche", help="niche for the app (faith, fitness, sleep, etc.)")
    parser.add_argument("--pricing", metavar="NICHE", help="pricing recommendations for a niche")
    parser.add_argument("--revenue", metavar="NICHE", help="revenue projections for a niche")
    parser.add_argument("--downloads", type=int, default=5000, help="estimated monthly downloads (default: 5000)")
    parser.add_argument("--affiliates", metavar="NICHE", help="affiliate program recommendations")
    parser.add_argument("--generate", metavar="APP_NAME", help="generate full monetization config")
    parser.add_argument("--all", action="store_true", help="analyze all 6 current PRINTMAXX apps")
    parser.add_argument("--json", action="store_true", help="output in JSON format (for --analyze)")

    args = parser.parse_args()

    if args.all:
        analyze_all_apps()
    elif args.analyze:
        if not args.niche:
            # Try to auto-detect from current apps
            if args.analyze.lower() in CURRENT_APPS:
                args.niche = CURRENT_APPS[args.analyze.lower()]["niche"]
            else:
                print("error: --niche required when using --analyze (unless app is a known PRINTMAXX app)")
                sys.exit(1)
        if args.json:
            config = {
                "strategy": NICHE_STRATEGIES.get(args.niche, {}),
                "competitor_pricing": COMPETITOR_PRICING.get(args.niche, {}),
                "revenuecat_config": generate_revenuecat_config(args.analyze, args.niche),
                "affiliate_placements": generate_affiliate_placements(args.niche),
                "ad_placements": generate_ad_placements(args.niche),
                "paywall_copy": generate_paywall_copy(args.analyze, args.niche),
                "revenue_projections": project_revenue(args.niche, args.downloads),
            }
            print(json.dumps(config, indent=2, default=str))
        else:
            display_full_analysis(args.analyze, args.niche)
    elif args.pricing:
        display_pricing(args.pricing)
    elif args.revenue:
        display_revenue(args.revenue, args.downloads)
    elif args.affiliates:
        display_affiliates(args.affiliates)
    elif args.generate:
        if not args.niche:
            if args.generate.lower() in CURRENT_APPS:
                args.niche = CURRENT_APPS[args.generate.lower()]["niche"]
            else:
                print("error: --niche required when using --generate (unless app is a known PRINTMAXX app)")
                sys.exit(1)
        generate_monetization_config(args.generate, args.niche)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
