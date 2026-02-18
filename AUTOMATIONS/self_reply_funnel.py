#!/usr/bin/env python3
"""
Self-Reply Funnel Generator for Twitter/X
Source: ALPHA334 - "Self-reply > bio link. 3-5x CTR. Algorithm shows OP reply first."

Generates tweet + self-reply pairs for maximum link CTR.
The algorithm prioritizes showing the original poster's first reply,
making self-replies 3-5x more effective than bio links.

Usage:
    python3 self_reply_funnel.py --topic "cold email system"
    python3 self_reply_funnel.py --product "PrayerLock" --url "https://prayerlock.app"
    python3 self_reply_funnel.py --batch /path/to/topics.csv
    python3 self_reply_funnel.py --generate-all    # Generate for all products
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "AUTOMATIONS" / "content_posting"
OUTPUT_CSV = OUTPUT_DIR / "self_reply_funnels.csv"

# Products to promote
PRODUCTS = {
    "prayerlock": {
        "name": "PrayerLock",
        "url": "https://prayerlock.app",
        "description": "Lock your phone until you pray. Faith-based screen time blocker.",
        "price": "Free trial, $4.99/mo",
        "niche": "faith",
    },
    "walktounlock": {
        "name": "WalkToUnlock",
        "url": "https://walktounlock.app",
        "description": "Lock your phone until you walk. Fitness-based screen time blocker.",
        "price": "Free trial, $4.99/mo",
        "niche": "fitness",
    },
    "cold_email_playbook": {
        "name": "Cold Email Playbook 2026",
        "url": "https://printmaxxer.gumroad.com/cold-email",
        "description": "73 proven cold email templates that actually get replies in 2026.",
        "price": "$29",
        "niche": "business",
    },
    "twitter_growth_kit": {
        "name": "Twitter Growth Kit",
        "url": "https://printmaxxer.gumroad.com/twitter-kit",
        "description": "147 tweet templates + posting schedule + growth playbook.",
        "price": "$19",
        "niche": "content",
    },
    "vibe_coding_playbook": {
        "name": "Vibe Coding Playbook",
        "url": "https://printmaxxer.gumroad.com/vibe-coding",
        "description": "Ship apps in days not months. Claude + Cursor + ship.",
        "price": "$34",
        "niche": "tech",
    },
    "printmaxxer": {
        "name": "@PRINTMAXXER",
        "url": "https://twitter.com/PRINTMAXXER",
        "description": "Follow for daily breakdowns on building internet businesses.",
        "price": "Free",
        "niche": "all",
    },
}

# Hook templates (main tweet)
HOOK_TEMPLATES = [
    "i spent {time} building {thing}.\n\nhere's exactly what i learned.\n\n(bookmark this)",
    "{thing} changed everything.\n\n{result}.\n\nhere's the full breakdown.",
    "stop {bad_thing}.\n\n{insight}.\n\nfull system in the reply.",
    "I tested {number} {things}.\n\nonly {winning_number} actually worked.\n\nbreaking down the winners below.",
    "{number} {metric} in {time}.\n\nhere's the exact system.\n\nreplying with everything.",
    "nobody talks about {topic}.\n\nbut it's the reason {result}.\n\nfull breakdown below.",
    "the {topic} playbook everyone's asking about.\n\n{teaser}.\n\nreplying with the full thing.",
    "i made every mistake with {topic}.\n\nso you don't have to.\n\nfull breakdown in the reply.",
    "this one trick {result}.\n\nsounds like BS but here's the proof.\n\n(thread in reply)",
    "if you're trying to {goal}:\n\nstop doing {bad_approach}.\n\ndo this instead.\n\n(reply has the full system)",
]

# Self-reply templates (the actual funnel)
REPLY_TEMPLATES = {
    "product_cta": [
        "full system/tool here: {url}\n\nbuilt this to solve exactly this problem.\n\n{price}. no bs.",
        "i packaged everything into {product_name}:\n\n{url}\n\n{description}\n\n{price}.",
        "here's the thing i built for this: {url}\n\n{description}\n\nfree trial to test it yourself.",
    ],
    "follow_cta": [
        "i break down stuff like this every day.\n\nfollow @PRINTMAXXER if you want the sauce.\n\n{url}",
        "more breakdowns like this on my profile.\n\nfollow for the next one.\n\nbuilding in public, sharing everything.",
        "this is what i do.\n\nbreak down what actually works.\n\nfollow for daily drops.",
    ],
    "lead_magnet": [
        "i put the full system in a doc.\n\n{url}\n\n{description}\n\nfree for the next 48 hours.",
        "full breakdown with templates:\n\n{url}\n\nnormally {price} but free this week.",
        "grab the full playbook:\n\n{url}\n\n{description}",
    ],
    "value_then_cta": [
        "here's the quick version:\n\n1. {step1}\n2. {step2}\n3. {step3}\n\nfull version with templates: {url}",
        "the tldr:\n\n- {point1}\n- {point2}\n- {point3}\n\ndetailed breakdown: {url}",
    ],
}


def generate_funnel_pair(topic, product_key=None, custom_url=None):
    """Generate a tweet + self-reply funnel pair."""
    pairs = []

    product = PRODUCTS.get(product_key, PRODUCTS["printmaxxer"])
    url = custom_url or product["url"]

    for hook_template in HOOK_TEMPLATES:
        # Fill hook
        hook = hook_template
        replacements = {
            "{time}": "2 weeks",
            "{thing}": topic,
            "{result}": "3x more results",
            "{bad_thing}": f"overthinking {topic}",
            "{insight}": f"the key to {topic} is simpler than you think",
            "{number}": "47",
            "{things}": "approaches",
            "{winning_number}": "3",
            "{metric}": "conversions",
            "{topic}": topic,
            "{teaser}": "it's simpler than you'd expect",
            "{goal}": f"get better at {topic}",
            "{bad_approach}": "following generic advice",
        }
        for k, v in replacements.items():
            hook = hook.replace(k, v)

        # Select reply type
        for reply_type, templates in REPLY_TEMPLATES.items():
            for reply_template in templates[:1]:  # One per type
                reply = reply_template
                reply_replacements = {
                    "{url}": url,
                    "{product_name}": product["name"],
                    "{description}": product["description"],
                    "{price}": product["price"],
                    "{step1}": f"identify your {topic} gaps",
                    "{step2}": f"apply the framework",
                    "{step3}": f"measure and iterate",
                    "{point1}": f"{topic} basics matter most",
                    "{point2}": "consistency beats intensity",
                    "{point3}": "measure everything",
                }
                for k, v in reply_replacements.items():
                    reply = reply.replace(k, v)

                if len(hook) <= 280 and len(reply) <= 280:
                    pairs.append({
                        "hook": hook,
                        "self_reply": reply,
                        "reply_type": reply_type,
                        "topic": topic,
                        "product": product["name"],
                        "url": url,
                    })

    return pairs


def generate_all_products():
    """Generate self-reply funnels for all products."""
    all_pairs = []

    topics_per_product = {
        "prayerlock": ["screen time", "phone addiction", "prayer habits", "digital wellness", "faith and technology"],
        "walktounlock": ["fitness habits", "walking", "phone addiction", "morning routine", "step count"],
        "cold_email_playbook": ["cold email", "outbound sales", "lead gen", "email marketing", "b2b sales"],
        "twitter_growth_kit": ["twitter growth", "content creation", "social media", "audience building", "viral tweets"],
        "vibe_coding_playbook": ["app building", "no-code", "shipping fast", "solopreneur tools", "AI coding"],
        "printmaxxer": ["building in public", "solopreneurship", "internet money", "side projects", "automation"],
    }

    for product_key, topics in topics_per_product.items():
        for topic in topics:
            pairs = generate_funnel_pair(topic, product_key)
            all_pairs.extend(pairs[:3])  # Top 3 per topic

    return all_pairs


def write_output(pairs):
    """Write funnel pairs to CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["hook", "self_reply", "reply_type", "topic", "product", "url"])
        writer.writeheader()
        writer.writerows(pairs)

    print(f"\nOutput written to: {OUTPUT_CSV}")
    print(f"Total funnel pairs: {len(pairs)}")

    # Stats
    by_product = {}
    for p in pairs:
        prod = p["product"]
        by_product[prod] = by_product.get(prod, 0) + 1

    print(f"\nBy product:")
    for prod, count in sorted(by_product.items()):
        print(f"  {prod}: {count} pairs")


def main():
    parser = argparse.ArgumentParser(description="Self-Reply Funnel Generator")
    parser.add_argument("--topic", type=str, help="Topic for the funnel")
    parser.add_argument("--product", type=str, help="Product key (prayerlock, cold_email_playbook, etc)")
    parser.add_argument("--url", type=str, help="Custom URL for CTA")
    parser.add_argument("--generate-all", action="store_true", help="Generate for all products")
    parser.add_argument("--batch", type=str, help="CSV of topics to generate for")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("SELF-REPLY FUNNEL GENERATOR")
    print(f"{'='*60}")
    print(f"Source: ALPHA334 - Self-reply > bio link. 3-5x CTR.")
    print(f"Algorithm shows OP reply first.\n")

    if args.generate_all:
        pairs = generate_all_products()
        write_output(pairs)
    elif args.topic:
        pairs = generate_funnel_pair(args.topic, args.product, args.url)
        write_output(pairs)
        # Show sample
        if pairs:
            print(f"\nSample funnel pair:")
            print(f"\n  TWEET: {pairs[0]['hook']}")
            print(f"\n  SELF-REPLY: {pairs[0]['self_reply']}")
    elif args.batch:
        all_pairs = []
        with open(args.batch, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                topic = row.get('topic', '')
                product = row.get('product', None)
                pairs = generate_funnel_pair(topic, product)
                all_pairs.extend(pairs[:3])
        write_output(all_pairs)
    else:
        # Demo mode
        pairs = generate_all_products()
        write_output(pairs)

        # Show samples
        print(f"\nSample pairs:")
        for p in pairs[:5]:
            print(f"\n  TWEET: {p['hook'][:100]}...")
            print(f"  REPLY: {p['self_reply'][:100]}...")
            print(f"  Product: {p['product']}")


if __name__ == "__main__":
    main()
