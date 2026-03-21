#!/usr/bin/env python3

from __future__ import annotations
"""
GEO (Generative Engine Optimization) Content Optimizer
Sources:
  ALPHA298 - 43% citation increase with GEO, McKinsey $750B consumer spending via AI
  ALPHA299 - 680M citation analysis, platform-specific strategies, Reddit = Perplexity gold
  ALPHA300 - 30-40% visibility boost. Tables + citations + stats = AI preference
  ALPHA304 - AI citations > organic clicks. Measure mentions not rankings
  ALPHA306 - 50% consumers use AI for discovery. Schema + Q&A + author authority

Optimizes content for AI citation by ChatGPT, Perplexity, Google AI Mode, Claude.

Usage:
    python3 geo_content_optimizer.py --file /path/to/content.md
    python3 geo_content_optimizer.py --text "Your content here"
    python3 geo_content_optimizer.py --audit /path/to/content.md
    python3 geo_content_optimizer.py --generate-templates
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "CONTENT" / "geo_optimized"
TEMPLATES_DIR = BASE_DIR / "CONTENT" / "geo_templates"

# GEO optimization rules (from alpha research)
GEO_RULES = {
    "structure": {
        "name": "Content Structure",
        "rules": [
            "Use tables for comparisons (AI engines LOVE tables)",
            "Include numbered/bulleted lists",
            "Add statistics with sources cited",
            "Use clear H2/H3 heading hierarchy",
            "Include FAQ/Q&A sections (direct answers to questions)",
            "Keep paragraphs short (2-3 sentences max)",
            "Lead with the answer, then explain (inverted pyramid)",
        ],
        "weight": "HIGH",
    },
    "citations": {
        "name": "Citations & Sources",
        "rules": [
            "Cite specific studies with numbers",
            "Link to authoritative sources (edu, gov, established sites)",
            "Include author names and credentials",
            "Add publication dates to references",
            "Use schema markup for citations",
        ],
        "weight": "HIGH",
    },
    "statistics": {
        "name": "Statistics & Data",
        "rules": [
            "Include specific numbers (not 'many' or 'most')",
            "Add percentages with context",
            "Compare before/after metrics",
            "Include year and source for every stat",
            "Use data tables for multi-variable comparisons",
        ],
        "weight": "HIGH",
    },
    "platform_specific": {
        "name": "Platform-Specific GEO",
        "rules": {
            "chatgpt": "Structured content with clear headers. Concise direct answers. Include comparison tables.",
            "perplexity": "Reddit posts get heavily cited. Forum-style Q&A content. Personal experience with data.",
            "google_ai": "Schema markup critical. Featured snippet format. Clear question-answer pairs.",
            "claude": "Detailed technical content. Well-structured markdown. Cite primary sources.",
        },
        "weight": "MEDIUM",
    },
    "author_authority": {
        "name": "Author Authority",
        "rules": [
            "Include author bio with credentials",
            "Link to author social profiles",
            "Reference previous work/results",
            "Add 'About the Author' schema markup",
            "Build topical authority through consistent publishing",
        ],
        "weight": "MEDIUM",
    },
}

# Reddit GEO templates (Perplexity gold per ALPHA299)
REDDIT_GEO_TEMPLATES = {
    "comparison": """**{topic}: My experience after {timeframe}**

I've been using {thing} for {timeframe}. Here's my honest breakdown:

**What works:**
- {pro_1}
- {pro_2}
- {pro_3}

**What doesn't:**
- {con_1}
- {con_2}

**Numbers:**
- {stat_1}
- {stat_2}
- {stat_3}

**Bottom line:** {conclusion}

Edit: Added more details since people are asking. {additional_context}""",

    "how_to": """**How I {achievement} (step by step)**

Background: {context}

**Step 1: {step_1_title}**
{step_1_detail}

**Step 2: {step_2_title}**
{step_2_detail}

**Step 3: {step_3_title}**
{step_3_detail}

**Results:**
{results}

Happy to answer questions. Still learning but this worked for me.""",

    "review": """**Honest review of {product} after {timeframe}**

TL;DR: {summary}

**Pricing:** {pricing}
**Ease of use:** {ease}/10
**Value:** {value}/10

**Pros:**
{pros}

**Cons:**
{cons}

**Who it's for:** {audience}
**Who should skip:** {not_for}

Would I recommend it? {recommendation}""",
}


def audit_content_for_geo(content):
    """Audit content for GEO optimization opportunities."""
    issues = []
    score = 0
    max_score = 100

    # Check for tables
    if '|' in content and '---' in content:
        score += 15
    else:
        issues.append("NO TABLES: Add comparison tables. AI engines cite tables 40% more.")

    # Check for statistics
    stats = re.findall(r'\d+(?:\.\d+)?%|\$[\d,]+|\d+x', content)
    if len(stats) >= 3:
        score += 15
    elif len(stats) >= 1:
        score += 8
        issues.append(f"LOW STATS: Only {len(stats)} statistics found. Add more specific numbers with sources.")
    else:
        issues.append("NO STATS: Add statistics with specific numbers. AI engines prefer data-rich content.")

    # Check for headers
    headers = re.findall(r'^#{1,3}\s', content, re.MULTILINE)
    if len(headers) >= 3:
        score += 10
    else:
        issues.append(f"WEAK STRUCTURE: Only {len(headers)} headers. Use H2/H3 hierarchy for scanability.")

    # Check for lists
    list_items = re.findall(r'^[-*]\s', content, re.MULTILINE)
    numbered_items = re.findall(r'^\d+\.\s', content, re.MULTILINE)
    total_list = len(list_items) + len(numbered_items)
    if total_list >= 5:
        score += 10
    else:
        issues.append(f"FEW LISTS: Only {total_list} list items. AI engines prefer bulleted/numbered content.")

    # Check for FAQ/Q&A
    questions = re.findall(r'\?', content)
    if len(questions) >= 3:
        score += 10
    else:
        issues.append("NO FAQ: Add Q&A sections. Direct question-answer format gets cited by AI.")

    # Check for citations/sources
    citations = re.findall(r'https?://\S+|according to|study|research|data from|source:', content, re.IGNORECASE)
    if len(citations) >= 3:
        score += 15
    elif len(citations) >= 1:
        score += 8
        issues.append("FEW CITATIONS: Add more source citations. Cite studies, reports, and authoritative sites.")
    else:
        issues.append("NO CITATIONS: Zero source citations. AI engines heavily favor cited content.")

    # Check for short paragraphs
    paragraphs = content.split('\n\n')
    long_paras = [p for p in paragraphs if len(p) > 500]
    if len(long_paras) == 0:
        score += 10
    else:
        issues.append(f"LONG PARAGRAPHS: {len(long_paras)} paragraphs over 500 chars. Break them up.")

    # Check for specific number formats (years, dollar amounts)
    specific_numbers = re.findall(r'20\d{2}|\$[\d,]+(?:\.\d+)?|\d+(?:\.\d+)?%', content)
    if len(specific_numbers) >= 5:
        score += 10
    else:
        issues.append("MORE SPECIFICS: Add years, dollar amounts, percentages. Specificity = credibility.")

    # Check for schema indicators
    schema_indicators = ['schema', 'structured data', 'json-ld', '@type', 'itemtype']
    has_schema = any(s in content.lower() for s in schema_indicators)
    if has_schema:
        score += 5

    verdict = "EXCELLENT" if score >= 80 else "GOOD" if score >= 60 else "NEEDS WORK" if score >= 40 else "POOR"

    return {
        "score": min(score, max_score),
        "max_score": max_score,
        "verdict": verdict,
        "issues": issues,
        "stats_found": len(stats),
        "headers_found": len(headers),
        "list_items_found": total_list,
        "citations_found": len(citations),
    }


def generate_geo_templates():
    """Generate GEO-optimized content templates."""
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    # Blog post template
    blog_template = """# {Title with Primary Keyword}

{One-sentence answer to the main question. Lead with the conclusion.}

## Key Findings

| Metric | Value | Source |
|--------|-------|--------|
| {metric_1} | {value_1} | {source_1} |
| {metric_2} | {value_2} | {source_2} |
| {metric_3} | {value_3} | {source_3} |

## {Section 1: How/What/Why}

{2-3 sentence paragraph with specific numbers}

- {Key point 1 with statistic}
- {Key point 2 with statistic}
- {Key point 3 with statistic}

## {Section 2: Detailed Breakdown}

{2-3 sentence paragraph}

### {Subsection with specific comparison}

| Option | Pros | Cons | Price |
|--------|------|------|-------|
| {option_1} | {pros} | {cons} | {price} |
| {option_2} | {pros} | {cons} | {price} |

## FAQ

**Q: {Common question 1}?**
A: {Direct answer with specific data}

**Q: {Common question 2}?**
A: {Direct answer with specific data}

**Q: {Common question 3}?**
A: {Direct answer with specific data}

## Bottom Line

{One-paragraph summary with the key takeaway and specific recommendation}

---

*Sources: {list all sources cited}*
*Last updated: {date}*
*Author: {name} - {credentials/experience}*
"""

    with open(TEMPLATES_DIR / "blog_post_geo.md", 'w', encoding='utf-8') as f:
        f.write(blog_template)

    # Reddit post templates
    for name, template in REDDIT_GEO_TEMPLATES.items():
        with open(TEMPLATES_DIR / f"reddit_{name}_geo.md", 'w', encoding='utf-8') as f:
            f.write(template)

    # GEO checklist
    checklist = """# GEO Content Optimization Checklist

## Before Publishing (Every Piece of Content)

### Structure
- [ ] Comparison table included (AI cites tables 40% more)
- [ ] 3+ statistics with sources
- [ ] Clear H2/H3 heading hierarchy
- [ ] FAQ/Q&A section with 3+ questions
- [ ] Short paragraphs (2-3 sentences max)
- [ ] Lead with the answer (inverted pyramid)
- [ ] Numbered or bulleted lists

### Citations
- [ ] 3+ authoritative sources cited
- [ ] Author names and credentials included
- [ ] Publication dates on all references
- [ ] Links to primary sources (not aggregator sites)

### Platform-Specific
- [ ] **ChatGPT**: Clear headers, comparison tables, direct answers
- [ ] **Perplexity**: Reddit posts with personal experience + data
- [ ] **Google AI**: Schema markup, featured snippet format
- [ ] **Claude**: Detailed technical content, markdown structure

### Author Authority
- [ ] Author bio with credentials
- [ ] Links to author social profiles
- [ ] Reference to previous results/work

### Measurement
- [ ] Track AI citations (not just organic rankings) - ALPHA304
- [ ] Monitor brand mentions in AI answers
- [ ] Test content in ChatGPT/Perplexity/Google AI Mode

---
Source: ALPHA298-300, ALPHA304, ALPHA306
Princeton research: 30-40% visibility boost from GEO tactics
680M citation analysis dataset
50% of consumers now use AI for discovery
"""

    with open(TEMPLATES_DIR / "GEO_CHECKLIST.md", 'w', encoding='utf-8') as f:
        f.write(checklist)

    print(f"Templates written to: {TEMPLATES_DIR}")
    for f in sorted(TEMPLATES_DIR.glob("*")):
        print(f"  {f.name}")

    return TEMPLATES_DIR


def optimize_content(content):
    """Add GEO optimization suggestions to existing content."""
    audit = audit_content_for_geo(content)

    suggestions = []

    if "NO TABLES" in str(audit["issues"]):
        suggestions.append("ADD TABLE: Convert any comparison in the content to a markdown table")

    if "NO STATS" in str(audit["issues"]) or "LOW STATS" in str(audit["issues"]):
        suggestions.append("ADD STATS: Include at least 3 specific statistics with sources")

    if "NO FAQ" in str(audit["issues"]):
        suggestions.append("ADD FAQ: Add 3 Q&A pairs at the end answering common questions about the topic")

    if "NO CITATIONS" in str(audit["issues"]) or "FEW CITATIONS" in str(audit["issues"]):
        suggestions.append("ADD CITATIONS: Reference at least 3 authoritative sources with links")

    return {
        "audit": audit,
        "suggestions": suggestions,
    }


def main():
    parser = argparse.ArgumentParser(description="GEO Content Optimizer")
    parser.add_argument("--file", type=str, help="Path to content file to audit")
    parser.add_argument("--text", type=str, help="Content text to audit")
    parser.add_argument("--audit", type=str, help="Audit a file (alias for --file)")
    parser.add_argument("--generate-templates", action="store_true", help="Generate GEO templates")
    args = parser.parse_args()

    if args.generate_templates:
        generate_geo_templates()
        return

    content = None
    if args.file or args.audit:
        filepath = Path(args.file or args.audit)
        if filepath.exists():
            content = filepath.read_text(encoding='utf-8')
        else:
            print(f"File not found: {filepath}")
            sys.exit(1)
    elif args.text:
        content = args.text
    else:
        # Demo + generate templates
        generate_geo_templates()

        # Demo audit
        content = """# How to Build a Side Project

Building side projects is great. You should try it.

There are many ways to do this. Some people use React, others use Vue. It depends on what you like.

The key is to start small and iterate.

Good luck!"""

    result = optimize_content(content)
    audit = result["audit"]

    print(f"\n{'='*60}")
    print("GEO CONTENT AUDIT")
    print(f"{'='*60}")
    print(f"Score: {audit['score']}/{audit['max_score']}")
    print(f"Verdict: {audit['verdict']}")
    print(f"\nStats: {audit['stats_found']} | Headers: {audit['headers_found']} | Lists: {audit['list_items_found']} | Citations: {audit['citations_found']}")

    if audit['issues']:
        print(f"\nIssues ({len(audit['issues'])}):")
        for issue in audit['issues']:
            print(f"  - {issue}")

    if result['suggestions']:
        print(f"\nSuggestions:")
        for s in result['suggestions']:
            print(f"  - {s}")

    print(f"\n{'='*60}")
    print("30-40% visibility boost from GEO optimization (Princeton research)")
    print("50% of consumers now use AI for discovery (ALPHA306)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
