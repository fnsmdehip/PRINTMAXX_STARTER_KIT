#!/usr/bin/env python3
"""
PRINTMAXX Auto-Content from Metrics
=====================================
Max Squeeze Protocol: every pipeline run auto-generates building-in-public content.

Reads pipeline_metrics.jsonl and generates @PRINTMAXXER tweets from real numbers.
No AI slop. Real numbers. @pipelineabuser energy.

Usage:
    python3 AUTOMATIONS/auto_content_from_metrics.py                # Generate tweets from latest metrics
    python3 AUTOMATIONS/auto_content_from_metrics.py --preview      # Show what would be generated
    python3 AUTOMATIONS/auto_content_from_metrics.py --output FILE  # Write to specific file
"""

import json
import random
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
METRICS_FILE = BASE / "AUTOMATIONS" / "leads" / "qualified" / "pipeline_metrics.jsonl"
OUTPUT_DIR = BASE / "CONTENT" / "social" / "printmaxxer"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")


def load_latest_metrics() -> dict:
    """Load the most recent metrics entry."""
    if not METRICS_FILE.exists():
        return {}
    lines = METRICS_FILE.read_text().strip().split("\n")
    # Find the most recent 'metrics' entry
    for line in reversed(lines):
        try:
            m = json.loads(line)
            if m.get("step") == "metrics":
                return m
        except:
            continue
    return {}


def generate_tweets(metrics: dict) -> list:
    """Generate building-in-public tweets from real pipeline data."""
    if not metrics:
        return ["No metrics available yet. Run the pipeline first."]

    analyzed = metrics.get("analyzed", 0)
    total_pool = metrics.get("total_pool", 0)
    hot = metrics.get("hot_leads", 0)
    warm = metrics.get("warm_leads", 0)
    hot_rate = metrics.get("hot_rate_pct", 0)
    pipeline = metrics.get("pipeline_entries", 0)
    emails = metrics.get("emails_generated", 0)
    pct = metrics.get("pct_complete", 0)

    templates = [
        # Consequence-first hooks with real numbers
        f"analyzed {analyzed:,} business websites last night while sleeping. "
        f"{hot:,} have garbage sites that need rebuilding. "
        f"cold emails already drafted. this is what automation looks like.",

        f"{hot:,} local businesses with outdated websites identified. "
        f"personalized cold emails with live demo links generated automatically. "
        f"the pipeline runs at 3am. I wake up to qualified leads.",

        f"built a system that scores websites 0-100 on design, SEO, and AI readiness. "
        f"ran it against {analyzed:,} local businesses. {hot_rate}% scored as hot prospects. "
        f"cold outreach pipeline generates emails while I sleep.",

        f"1.45 million business domains in the queue. "
        f"{analyzed:,} analyzed so far ({pct}%). "
        f"{hot:,} hot leads. {emails:,} cold emails drafted. "
        f"the machine runs 24/7 via cron. I just check the dashboard.",

        f"most people manually find leads one at a time. "
        f"I downloaded 2.87 million from Overture Maps, "
        f"deduped to 1.45M unique domains, "
        f"and built a closed-loop pipeline that qualifies → emails → tracks automatically. "
        f"{hot:,} hot leads so far.",

        f"pipeline update:\n\n"
        f"• {analyzed:,} websites analyzed\n"
        f"• {hot:,} hot leads (bad site + high budget industry)\n"
        f"• {warm:,} warm leads\n"
        f"• {emails:,} cold emails generated\n"
        f"• {pipeline:,} in outreach pipeline\n\n"
        f"runs autonomously. cron job at 3am. "
        f"crash recovery built in. this is the way.",
    ]

    # Pick 3 random tweets (different styles)
    selected = random.sample(templates, min(3, len(templates)))
    return selected


def generate_thread(metrics: dict) -> list:
    """Generate a tweet thread from pipeline data."""
    if not metrics:
        return []

    analyzed = metrics.get("analyzed", 0)
    total_pool = metrics.get("total_pool", 0)
    hot = metrics.get("hot_leads", 0)
    emails = metrics.get("emails_generated", 0)

    thread = [
        f"I built a system that finds local businesses with garbage websites "
        f"and cold emails them with live demos of what their site COULD look like. "
        f"here's exactly how it works (and the numbers so far). 🧵",

        f"step 1: data.\n\n"
        f"downloaded 2.87 million US business locations from Overture Maps (free, open data). "
        f"dentists, lawyers, realtors, gyms, salons, restaurants, chiropractors, vets, plumbers.\n\n"
        f"filtered to 1.45 million unique domains after dedup.",

        f"step 2: website analysis.\n\n"
        f"each site gets scored 0-100 across 5 dimensions:\n"
        f"• design modernity (CSS Grid vs table layouts)\n"
        f"• SEO quality (meta tags, schema, sitemap)\n"
        f"• AI/GIO readiness (structured data, FAQ content)\n"
        f"• mobile responsiveness\n"
        f"• business activity signals\n\n"
        f"runs at ~12 sites/second with 30 parallel workers.",

        f"step 3: automatic cold email generation.\n\n"
        f"hot leads (score >= 65) get personalized 3-email sequences. "
        f"each email includes a live demo URL matching their industry. "
        f"dental practice → dental-demo.surge.sh. "
        f"law firm → legal-demo.surge.sh.\n\n"
        f"the demo sites are already live. 16 of them.",

        f"step 4: closed loop.\n\n"
        f"entire pipeline runs via cron at 3am. "
        f"crash recovery built in (active-tasks.md pattern from OpenClaw). "
        f"if it dies mid-batch, next run picks up exactly where it left off.\n\n"
        f"qualify → email → track → repeat. no human in the loop.",

        f"current numbers:\n\n"
        f"• {analyzed:,} websites analyzed (of 1.45M)\n"
        f"• {hot:,} hot leads identified\n"
        f"• {emails:,} cold emails generated\n"
        f"• 16 live demo sites\n"
        f"• 6 industry templates\n\n"
        f"total cost: $0 (Overture Maps is free, surge.sh is free, email via smtplib).",

        f"the playbook:\n\n"
        f"1. find businesses with bad websites (automated)\n"
        f"2. show them what a good one looks like (live demos)\n"
        f"3. offer to build it for $500-$3,000\n"
        f"4. use AI tools to actually build it in 2 hours\n\n"
        f"margin is insane because the build cost is near zero.\n\n"
        f"shipping > planning.",
    ]
    return thread


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--output', type=str, default='')
    args = parser.parse_args()

    metrics = load_latest_metrics()
    if not metrics:
        print("No pipeline metrics found. Run closed_loop_pipeline.py first.")
        return

    tweets = generate_tweets(metrics)
    thread = generate_thread(metrics)

    output_file = args.output or str(OUTPUT_DIR / f"PIPELINE_TWEETS_{TODAY}.md")

    content = [
        f"# Pipeline Building-in-Public Content — {TODAY}",
        f"",
        f"Generated from real pipeline metrics. @PRINTMAXXER voice.",
        f"Status: PENDING_REVIEW",
        f"",
        f"## Tweets (pick 1-2 per day)",
        f"",
    ]
    for i, tweet in enumerate(tweets, 1):
        content.append(f"### Tweet {i}")
        content.append(f"```")
        content.append(tweet)
        content.append(f"```")
        content.append(f"")

    content.append(f"## Thread (7 tweets)")
    content.append(f"")
    for i, t in enumerate(thread, 1):
        content.append(f"### {i}/7")
        content.append(f"```")
        content.append(t)
        content.append(f"```")
        content.append(f"")

    full_content = "\n".join(content)

    if args.preview:
        print(full_content)
    else:
        Path(output_file).write_text(full_content)
        print(f"Content written to: {output_file}")
        print(f"  {len(tweets)} tweets + 1 thread ({len(thread)} tweets)")
        print(f"  Status: PENDING_REVIEW")


if __name__ == "__main__":
    main()
