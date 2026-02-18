#!/usr/bin/env python3
"""
Longtail Content Generator - Generate SEO-optimized pages from GEO_LONGTAIL_SLUGS_300.csv
Uses Claude API (Haiku for bulk, Sonnet for quality)

Usage:
    python generate_longtails.py                     # Generate next 10 unpublished pages
    python generate_longtails.py --count 25          # Generate 25 pages
    python generate_longtails.py --model sonnet      # Use Sonnet for higher quality
    python generate_longtails.py --niche "AI workflows"  # Filter by niche
    python generate_longtails.py --template best     # Filter by template type
    python generate_longtails.py --dry-run           # Preview without generating

Environment Variables:
    ANTHROPIC_API_KEY: Required for Claude API
    LEDGER_DIR: Path to LEDGER directory (default: ../LEDGER)
    CONTENT_DIR: Path to CONTENT directory (default: ../CONTENT)

Output:
    Markdown files in CONTENT/longtail_pages/
    Updates GEO_LONGTAIL_SLUGS_300.csv with published status
"""

import argparse
import csv
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic not installed. Run: pip install anthropic")
    exit(1)


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = Path(os.getenv("LEDGER_DIR", BASE_DIR / "LEDGER"))
CONTENT_DIR = Path(os.getenv("CONTENT_DIR", BASE_DIR / "CONTENT"))
LONGTAIL_CSV = LEDGER_DIR / "GEO_LONGTAIL_SLUGS_300.csv"
OUTPUT_DIR = CONTENT_DIR / "longtail_pages"

# Model configuration
MODELS = {
    "haiku": "claude-3-haiku-20240307",
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-20250514"
}

# Cost per 1K tokens (approximate)
COSTS = {
    "haiku": {"input": 0.00025, "output": 0.00125},
    "sonnet": {"input": 0.003, "output": 0.015},
    "opus": {"input": 0.015, "output": 0.075}
}

# System prompt for content generation
SYSTEM_PROMPT = """You are a content writer for PRINTMAXX, a resource for solopreneurs building AI-powered workflows.

Writing style rules (STRICT - follow exactly):
- NEVER use em dashes (use commas or periods instead)
- NEVER use these words: leverage, utilize, delve, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge
- NEVER use "It's not just X, it's Y" constructions
- NEVER use vague attributions like "experts say" or "studies show"
- Use specific numbers and examples
- Write like texting a smart friend
- Start with the answer/conclusion
- Use sentence case for headings
- One hedge per sentence maximum
- Short sentences. One idea per sentence.

Content structure for longtail pages:
1. Quick answer (2-3 sentences answering the query directly)
2. Key points (bulleted, specific)
3. Detailed explanation (if needed)
4. Comparison table (if relevant)
5. FAQ section (3-5 questions)

Target audience: Solopreneurs, indie hackers, small team founders who want to automate their business with AI."""


def load_unpublished_slugs(
    niche_filter: Optional[str] = None,
    template_filter: Optional[str] = None,
    count: int = 10
) -> list[dict]:
    """Load unpublished slugs from GEO_LONGTAIL_SLUGS_300.csv"""
    slugs = []

    if not LONGTAIL_CSV.exists():
        print(f"ERROR: {LONGTAIL_CSV} not found")
        return slugs

    with open(LONGTAIL_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip already published
            if row.get("published", "").upper() == "TRUE":
                continue

            # Apply niche filter
            if niche_filter and niche_filter.lower() not in row.get("niche", "").lower():
                continue

            # Apply template filter
            if template_filter and template_filter.lower() != row.get("template_type", "").lower():
                continue

            slugs.append({
                "niche": row.get("niche", ""),
                "template_type": row.get("template_type", ""),
                "keyword": row.get("keyword", ""),
                "url_slug": row.get("url_slug", ""),
                "geo_scope": row.get("geo_scope", "global"),
            })

            if len(slugs) >= count:
                break

    return slugs


def generate_content(client: anthropic.Anthropic, slug: dict, model: str) -> dict:
    """Generate content for a single longtail page"""
    keyword = slug["keyword"]
    niche = slug["niche"]
    template_type = slug["template_type"]

    # Build prompt based on template type
    if template_type == "best":
        user_prompt = f"""Write a longtail page for: "{keyword}"

Niche: {niche}
Type: Best/recommendation list

Include:
1. Quick answer (what's the best option and why, 2-3 sentences)
2. Comparison table with 4-5 options (columns: Tool, Best For, Price, Key Feature)
3. Detailed breakdown of top 3 options (150 words each)
4. Decision guide (when to use each)
5. FAQ section (4 questions)

Remember: No em dashes. No banned words. Specific numbers. Direct answers."""

    elif template_type == "compare":
        user_prompt = f"""Write a longtail page for: "{keyword}"

Niche: {niche}
Type: Comparison/versus

Include:
1. Quick verdict (which is better for what use case, 2-3 sentences)
2. Side-by-side comparison table (features, pricing, pros/cons)
3. Detailed analysis (when to choose Option A, when to choose Option B)
4. Real-world use case examples
5. FAQ section (4 questions)

Remember: No em dashes. No banned words. Specific numbers. Direct answers."""

    elif template_type == "cost":
        user_prompt = f"""Write a longtail page for: "{keyword}"

Niche: {niche}
Type: Cost/pricing guide

Include:
1. Quick answer with specific numbers (2-3 sentences)
2. Cost breakdown table (different tiers/scenarios)
3. Hidden costs to watch for
4. Money-saving tips
5. Budget recommendations by use case
6. FAQ section (4 questions)

Remember: No em dashes. No banned words. Specific numbers. Direct answers."""

    elif template_type == "how-to":
        user_prompt = f"""Write a longtail page for: "{keyword}"

Niche: {niche}
Type: How-to guide

Include:
1. Quick answer (summary of the process, 2-3 sentences)
2. Prerequisites (what you need before starting)
3. Step-by-step guide (numbered, specific actions)
4. Common mistakes to avoid
5. Expected results/timeline
6. FAQ section (4 questions)

Remember: No em dashes. No banned words. Specific numbers. Direct answers."""

    else:  # template or general
        user_prompt = f"""Write a longtail page for: "{keyword}"

Niche: {niche}
Type: Template/framework

Include:
1. Quick answer (what this is and who it's for, 2-3 sentences)
2. Key components/sections
3. Step-by-step implementation
4. Customization tips
5. Example use cases
6. FAQ section (4 questions)

Remember: No em dashes. No banned words. Specific numbers. Direct answers."""

    # Call Claude API
    response = client.messages.create(
        model=MODELS[model],
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    content = response.content[0].text

    # Calculate cost
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    cost = (input_tokens / 1000 * COSTS[model]["input"]) + (output_tokens / 1000 * COSTS[model]["output"])

    return {
        "content": content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost
    }


def create_markdown_file(slug: dict, content: str, output_dir: Path) -> Path:
    """Create markdown file with frontmatter"""
    url_slug = slug["url_slug"]
    filename = f"{url_slug}.md"
    filepath = output_dir / filename

    # Create frontmatter
    frontmatter = f"""---
title: "{slug['keyword']}"
slug: "{url_slug}"
niche: "{slug['niche']}"
template_type: "{slug['template_type']}"
geo_scope: "{slug['geo_scope']}"
created_at: "{datetime.now().isoformat()}"
published: false
seo_meta:
  title: "{slug['keyword']} | PRINTMAXX"
  description: ""
---

"""

    # Write file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)
        f.write(content)

    return filepath


def update_csv_status(url_slug: str, csv_path: Path):
    """Mark slug as published in CSV"""
    rows = []
    updated = False

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row.get("url_slug") == url_slug:
                row["published"] = "TRUE"
                row["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                updated = True
            rows.append(row)

    if updated:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Generate longtail content from GEO_LONGTAIL_SLUGS_300.csv"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of pages to generate (default: 10)"
    )
    parser.add_argument(
        "--model",
        choices=["haiku", "sonnet", "opus"],
        default="haiku",
        help="Claude model to use (default: haiku)"
    )
    parser.add_argument(
        "--niche",
        type=str,
        help="Filter by niche (partial match)"
    )
    parser.add_argument(
        "--template",
        type=str,
        choices=["best", "compare", "cost", "how-to", "template"],
        help="Filter by template type"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview slugs without generating"
    )
    parser.add_argument(
        "--no-update-csv",
        action="store_true",
        help="Don't update CSV published status"
    )

    args = parser.parse_args()

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        exit(1)

    print("=" * 60)
    print("LONGTAIL CONTENT GENERATOR")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load slugs
    slugs = load_unpublished_slugs(
        niche_filter=args.niche,
        template_filter=args.template,
        count=args.count
    )

    if not slugs:
        print("No unpublished slugs found matching criteria")
        return

    print(f"\nSlugs to generate: {len(slugs)}")
    print(f"Model: {args.model} ({MODELS[args.model]})")
    print(f"Output: {args.output_dir}")
    print()

    for i, slug in enumerate(slugs[:10]):
        print(f"  {i+1}. [{slug['template_type']}] {slug['keyword'][:60]}...")
    if len(slugs) > 10:
        print(f"  ... and {len(slugs) - 10} more")

    if args.dry_run:
        print("\n[DRY RUN] Would generate the above pages")
        # Estimate cost
        est_tokens = len(slugs) * 3000  # ~3K tokens per page
        est_cost = est_tokens / 1000 * COSTS[args.model]["output"]
        print(f"Estimated cost: ${est_cost:.4f} ({args.model})")
        return

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)

    # Generate content
    total_cost = 0
    total_tokens = 0
    generated = 0

    for i, slug in enumerate(slugs):
        print(f"\n[{i+1}/{len(slugs)}] Generating: {slug['keyword'][:50]}...")

        try:
            result = generate_content(client, slug, args.model)

            # Create markdown file
            filepath = create_markdown_file(slug, result["content"], args.output_dir)

            # Update CSV
            if not args.no_update_csv:
                update_csv_status(slug["url_slug"], LONGTAIL_CSV)

            total_cost += result["cost"]
            total_tokens += result["output_tokens"]
            generated += 1

            print(f"  Created: {filepath.name}")
            print(f"  Tokens: {result['output_tokens']} | Cost: ${result['cost']:.4f}")

            # Rate limiting
            if i < len(slugs) - 1:
                time.sleep(1)

        except anthropic.RateLimitError:
            print("  Rate limited. Waiting 60 seconds...")
            time.sleep(60)
            # Retry
            try:
                result = generate_content(client, slug, args.model)
                filepath = create_markdown_file(slug, result["content"], args.output_dir)
                if not args.no_update_csv:
                    update_csv_status(slug["url_slug"], LONGTAIL_CSV)
                total_cost += result["cost"]
                generated += 1
                print(f"  Created: {filepath.name}")
            except Exception as e:
                print(f"  Failed after retry: {e}")

        except Exception as e:
            print(f"  Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Pages generated: {generated}/{len(slugs)}")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
