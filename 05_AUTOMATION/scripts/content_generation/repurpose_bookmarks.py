#!/usr/bin/env python3
"""
PRINTMAXX Content Repurposing Engine
Takes scraped X bookmarks and generates reworded variants for niche accounts

Master doc source: v26 Content Farm Multi-Account strategy (lines 2120-2173)
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
BOOKMARKS_FILE = PROJECT_ROOT / "AUTOMATIONS/x_bookmarks/x_bookmarks_2026-01-19.json"
OUTPUT_DIR = PROJECT_ROOT / "AUTOMATIONS/content_generation/repurposed_content"
LEDGER_FILE = PROJECT_ROOT / "LEDGER/CONTENT_PIPELINE.csv"

# Create output dir if needed
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_bookmarks():
    """Load scraped X bookmarks"""
    with open(BOOKMARKS_FILE, 'r') as f:
        return json.load(f)

def analyze_bookmark_value(bookmark):
    """
    Score bookmark for repurposing value
    High value = playbooks, strategies, metrics, tools
    """
    text = bookmark['text'].lower()
    score = 0

    # Playbook indicators (+3 points each)
    playbook_words = ['how i', 'step-by-step', 'framework', 'strategy', 'playbook', 'guide']
    score += sum(3 for word in playbook_words if word in text)

    # Metrics/proof (+2 points each)
    metric_words = ['$', 'k/mo', 'views', 'revenue', '%', 'conversions']
    score += sum(2 for word in metric_words if word in text)

    # Tools/tactics (+2 points each)
    tool_words = ['tool', 'platform', 'automation', 'ai', 'script', 'prompt']
    score += sum(2 for word in tool_words if word in text)

    # Length bonus (longer = more substance)
    if bookmark['word_count'] > 100:
        score += 3
    elif bookmark['word_count'] > 50:
        score += 1

    # Media bonus
    if bookmark['has_images']:
        score += 2
    if bookmark['has_video']:
        score += 1

    return score

def categorize_niche(bookmark):
    """
    Categorize bookmark into niche buckets
    Niches from v26: AI utilities, Faith streak, Fitness
    """
    text = bookmark['text'].lower()

    # AI utilities
    if any(word in text for word in ['ai', 'automation', 'prompt', 'agent', 'cursor', 'claude']):
        return 'AI'

    # Faith (less common in tech bookmarks, but check)
    if any(word in text for word in ['faith', 'prayer', 'scripture', 'god', 'spiritual']):
        return 'Faith'

    # Fitness
    if any(word in text for word in ['fitness', 'gym', 'workout', 'protein', 'training']):
        return 'Fitness'

    # Default to AI if can't categorize (most tech content fits)
    return 'AI'

def generate_repurpose_prompts(bookmark, niche):
    """
    Generate Claude prompts to repurpose content
    Returns list of variant prompts (for A/B testing)
    """
    original = bookmark['text']
    author = bookmark['handle']

    # Base prompt template with STRICT anti-AI-cringe rules
    base = f'''Original post by {author}:
"{original}"

Rewrite this for a {niche} niche account with these requirements:

CONTENT RULES:
- Keep the core insight/strategy intact
- Add 20% original perspective or example specific to {niche}
- Change structure and wording completely
- Keep it under {bookmark['word_count'] + 30} words
- Add a CTA at the end (e.g., "Reply STACK for the setup", "Comment GUIDE for details")

ANTI-AI-CRINGE RULES (CRITICAL):
- NO em dashes (—) whatsoever
- NO "It's not just X. It's Y!" format
- NO "Here's the thing:" or "Let me tell you:"
- NO "game-changer", "unlock", "leverage", "dive deep"
- NO rhetorical questions back-to-back
- NO numbered lists unless the original had them
- Preserve the original author's sentence structure style (short/punchy vs long/flowing)
- Use the same punctuation style as original (periods vs. line breaks)
- Keep the same tone (casual vs. formal, hype vs. matter-of-fact)
- If original uses lowercase, match it. If caps, match it.
- Sound like a human who tweets, not a copywriter

Variant style: {{variant_style}}
'''

    # Different variant styles for A/B testing
    variants = [
        {
            'name': 'Thread_Hook',
            'style': 'Make it a thread hook (numbered list preview)',
            'prompt': base.replace('{variant_style}', 'Make it a thread hook (numbered list preview)')
        },
        {
            'name': 'Story_Format',
            'style': 'Turn it into a brief story/case study',
            'prompt': base.replace('{variant_style}', 'Turn it into a brief story/case study')
        },
        {
            'name': 'Question_Hook',
            'style': 'Start with a provocative question',
            'prompt': base.replace('{variant_style}', 'Start with a provocative question')
        }
    ]

    return variants

def main():
    """Main execution"""
    print("🔄 PRINTMAXX Content Repurposing Engine")
    print("=" * 50)

    # Load bookmarks
    print(f"📖 Loading bookmarks from {BOOKMARKS_FILE}")
    bookmarks = load_bookmarks()
    print(f"✅ Loaded {len(bookmarks)} bookmarks")

    # Analyze and sort by value
    print("\\n📊 Analyzing bookmark value...")
    scored_bookmarks = []
    for bm in bookmarks:
        score = analyze_bookmark_value(bm)
        niche = categorize_niche(bm)
        scored_bookmarks.append({
            **bm,
            'repurpose_score': score,
            'niche': niche
        })

    # Sort by score (highest first)
    scored_bookmarks.sort(key=lambda x: x['repurpose_score'], reverse=True)

    # Show top 10
    print(f"\\n🏆 Top 10 Bookmarks for Repurposing:")
    print("-" * 50)
    for i, bm in enumerate(scored_bookmarks[:10], 1):
        print(f"{i}. Score: {bm['repurpose_score']} | Niche: {bm['niche']} | @{bm['handle']}")
        print(f"   Preview: {bm['text'][:100]}...")
        print()

    # Generate repurpose plan for top 30
    top_30 = scored_bookmarks[:30]

    print(f"\\n📝 Generating repurpose prompts for top 30 bookmarks...")
    repurpose_plan = []

    for bm in top_30:
        variants = generate_repurpose_prompts(bm, bm['niche'])
        for variant in variants:
            repurpose_plan.append({
                'original_url': bm['url'],
                'original_author': bm['handle'],
                'niche': bm['niche'],
                'variant_name': variant['name'],
                'variant_style': variant['style'],
                'claude_prompt': variant['prompt'],
                'status': 'TODO',
                'generated_content': '',
                'performance_notes': ''
            })

    # Save to CSV
    output_csv = OUTPUT_DIR / f"repurpose_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(output_csv, 'w', newline='') as f:
        if repurpose_plan:
            writer = csv.DictWriter(f, fieldnames=repurpose_plan[0].keys())
            writer.writeheader()
            writer.writerows(repurpose_plan)

    print(f"✅ Saved {len(repurpose_plan)} repurpose prompts to:")
    print(f"   {output_csv}")

    # Summary by niche
    niche_counts = {}
    for item in repurpose_plan:
        niche = item['niche']
        niche_counts[niche] = niche_counts.get(niche, 0) + 1

    print(f"\\n📊 Content variants by niche:")
    for niche, count in sorted(niche_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {niche}: {count} variants")

    print(f"\\n✅ DONE! Next step: Run Claude to generate actual content from prompts")
    print(f"💡 Tip: Use Tier A model (Haiku) for bulk generation, Tier B (Sonnet) for quality check")

if __name__ == "__main__":
    main()
