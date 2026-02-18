#!/usr/bin/env python3
"""
hashtag_optimizer.py - Generate optimal hashtags per platform and niche

Analyzes content and generates platform-specific hashtag sets based on
niche, content type, and platform best practices.

Usage:
    python3 hashtag_optimizer.py --content "Your post about cold email" --platform X --niche ai
    python3 hashtag_optimizer.py --niche fitness --platform Instagram --count 30
    python3 hashtag_optimizer.py --content "App launch" --platform all

Example:
    python3 hashtag_optimizer.py --content "I built a prayer app" --platform X --niche faith
    python3 hashtag_optimizer.py --niche tech --platform Instagram --count 25
"""

import argparse
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
CONFIG_PATH = AUTOMATIONS_DIR / "config.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "hashtag_optimizer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Hashtag databases per niche
NICHE_HASHTAGS = {
    "faith": {
        "primary": ["#faith", "#prayer", "#christian", "#Jesus", "#God", "#Bible", "#blessed",
                     "#worship", "#church", "#spirituality"],
        "secondary": ["#dailydevotional", "#prayerlife", "#faithjourney", "#Godisgood",
                       "#christianlife", "#scriptureoftheday", "#churchlife", "#grace",
                       "#motivation", "#hope"],
        "trending": ["#faithoverfear", "#prayerwarrior", "#dailyprayer", "#morningprayer",
                      "#Godisfaithful", "#trustGod", "#bibleverse"],
        "long_tail": ["#christianentrepreneur", "#faithbasedapp", "#prayerapp",
                       "#christiancommunity", "#faithandwork"],
    },
    "fitness": {
        "primary": ["#fitness", "#gym", "#workout", "#health", "#fit", "#bodybuilding",
                     "#training", "#muscle", "#gains", "#exercise"],
        "secondary": ["#fitlife", "#gymlife", "#fitnessmotivation", "#personaltrainer",
                       "#nutrition", "#healthylifestyle", "#strengthtraining", "#cardio",
                       "#protein", "#gymrat"],
        "trending": ["#gymmotivation", "#fitcheck", "#legday", "#chestday",
                      "#progresspic", "#transformationtuesday", "#mealprep"],
        "long_tail": ["#fitnessapp", "#homeworkout", "#fitnesstech",
                       "#workouttracker", "#fitnessjourney2026"],
    },
    "ai": {
        "primary": ["#AI", "#artificialintelligence", "#machinelearning", "#tech",
                     "#automation", "#ChatGPT", "#Claude", "#coding", "#startup", "#SaaS"],
        "secondary": ["#indiehacker", "#buildinpublic", "#solopreneur", "#nocode",
                       "#productiviy", "#techstartup", "#webapp", "#devtools",
                       "#openai", "#anthropic"],
        "trending": ["#vibecoding", "#aitools", "#aistartup", "#buildwithAI",
                      "#aiagents", "#MCPserver", "#claudeCode"],
        "long_tail": ["#aitoolslist", "#aiforsolopreneurs", "#aiautomation",
                       "#aicontent", "#aibusiness2026"],
    },
    "tech": {
        "primary": ["#tech", "#programming", "#developer", "#code", "#software",
                     "#webdev", "#reactjs", "#javascript", "#python", "#startup"],
        "secondary": ["#techstartup", "#fullstack", "#frontend", "#backend",
                       "#devlife", "#opensources", "#github", "#nextjs",
                       "#typescript", "#nodejs"],
        "trending": ["#vibecoding", "#techtwitter", "#shipfast", "#indiehacker",
                      "#buildinpublic", "#devtools"],
        "long_tail": ["#techsolopreneur", "#codingtips", "#sideproject",
                       "#microSaaS", "#techproductivity"],
    },
    "business": {
        "primary": ["#business", "#entrepreneur", "#startup", "#money", "#marketing",
                     "#sales", "#revenue", "#growth", "#hustle", "#income"],
        "secondary": ["#onlinebusiness", "#digitalmarketing", "#sidehustle",
                       "#passiveincome", "#ecommerce", "#branding", "#coldemail",
                       "#contentmarketing", "#socialmediamarketing", "#leads"],
        "trending": ["#buildinpublic", "#solopreneur", "#indiehacker",
                      "#makemoneyonline", "#businesstips"],
        "long_tail": ["#solopreneurlife", "#bootstrapped", "#revenuefirst",
                       "#profitablestartup", "#businessautomation"],
    },
}

# Platform-specific limits and best practices
PLATFORM_RULES = {
    "X": {"max": 3, "style": "minimal", "placement": "end"},
    "Twitter": {"max": 3, "style": "minimal", "placement": "end"},
    "Instagram": {"max": 30, "style": "heavy", "placement": "first_comment"},
    "LinkedIn": {"max": 5, "style": "moderate", "placement": "end"},
    "TikTok": {"max": 5, "style": "trending", "placement": "inline"},
    "YouTube": {"max": 15, "style": "seo", "placement": "description"},
    "Pinterest": {"max": 20, "style": "seo", "placement": "description"},
    "Facebook": {"max": 3, "style": "minimal", "placement": "end"},
    "Threads": {"max": 5, "style": "moderate", "placement": "end"},
    "Medium": {"max": 5, "style": "seo", "placement": "end"},
    "Substack": {"max": 0, "style": "none", "placement": "none"},
}


def extract_keywords(content):
    """Extract likely keywords from content text."""
    if not content:
        return []

    # Remove common words
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "out", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "both", "each", "few", "more", "most",
        "other", "some", "such", "no", "not", "only", "own", "same", "so",
        "than", "too", "very", "just", "and", "but", "or", "if", "it", "its",
        "i", "my", "me", "you", "your", "we", "our", "they", "this", "that",
    }

    words = re.findall(r"\b[a-zA-Z]{3,}\b", content.lower())
    filtered = [w for w in words if w not in stop_words]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(10)]


def generate_hashtags(niche, platform, content=None, count=None):
    """Generate optimized hashtag set."""
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES.get("X"))
    max_tags = count if count else rules["max"]

    if max_tags == 0:
        return []

    niche_tags = NICHE_HASHTAGS.get(niche, NICHE_HASHTAGS.get("business"))

    # Build tag pool based on platform style
    pool = []

    if rules["style"] == "minimal":
        pool = niche_tags["primary"][:2] + niche_tags["trending"][:2]

    elif rules["style"] == "heavy":
        pool = (niche_tags["primary"] + niche_tags["secondary"] +
                niche_tags["trending"] + niche_tags["long_tail"])

    elif rules["style"] == "moderate":
        pool = niche_tags["primary"][:5] + niche_tags["trending"][:3]

    elif rules["style"] == "trending":
        pool = niche_tags["trending"] + niche_tags["primary"][:3]

    elif rules["style"] == "seo":
        pool = (niche_tags["long_tail"] + niche_tags["primary"][:5] +
                niche_tags["secondary"][:5])

    # Add content-derived hashtags
    if content:
        keywords = extract_keywords(content)
        for kw in keywords[:5]:
            tag = f"#{kw}"
            if tag not in pool:
                pool.append(tag)

    # Deduplicate and limit
    seen = set()
    unique = []
    for tag in pool:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            seen.add(tag_lower)
            unique.append(tag)

    return unique[:max_tags]


def format_output(hashtags, platform):
    """Format hashtags for the specific platform."""
    rules = PLATFORM_RULES.get(platform, {})

    if rules.get("placement") == "first_comment":
        return {
            "post_tags": "",
            "comment_tags": " ".join(hashtags),
            "note": "Add hashtags as first comment, not in caption",
        }

    return {
        "post_tags": " ".join(hashtags),
        "comment_tags": "",
        "note": f"Place at {rules.get('placement', 'end')} of post",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate optimized hashtags per platform and niche"
    )
    parser.add_argument("--content", type=str, default="", help="Content text to analyze")
    parser.add_argument("--niche", type=str, default="business", help="Content niche")
    parser.add_argument(
        "--platform",
        type=str,
        default="X",
        help="Platform or 'all' (default: X)",
    )
    parser.add_argument("--count", type=int, default=None, help="Override hashtag count")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    if args.platform.lower() == "all":
        platforms = list(PLATFORM_RULES.keys())
    else:
        platforms = [args.platform]

    results = {}
    for platform in platforms:
        tags = generate_hashtags(args.niche, platform, args.content, args.count)
        formatted = format_output(tags, platform)
        results[platform] = {
            "hashtags": tags,
            "count": len(tags),
            **formatted,
        }

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        for platform, data in results.items():
            print(f"\n--- {platform} ({data['count']} tags) ---")
            print(f"Tags: {data['post_tags']}")
            if data["comment_tags"]:
                print(f"Comment: {data['comment_tags']}")
            print(f"Note: {data['note']}")

    logger.info(f"Generated hashtags for {len(platforms)} platform(s)")


if __name__ == "__main__":
    main()
