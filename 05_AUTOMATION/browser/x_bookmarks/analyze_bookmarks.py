#!/usr/bin/env python3
"""
Analyze X bookmarks for tech stacks, money methods, and solopreneur insights
"""

import json
import re
from collections import Counter

# Load bookmarks
with open('x_bookmarks_2026-01-19.json', 'r') as f:
    bookmarks = json.load(f)

print(f"📊 Analyzing {len(bookmarks)} bookmarks...\n")

# === MONEY-MAKING METHODS ===
print("=" * 80)
print("💰 MONEY-MAKING METHODS & BUSINESS MODELS")
print("=" * 80)

money_keywords = {
    'Digital Products': ['digital product', 'ebook', 'course', 'template', 'notion', 'gumroad', 'teachable'],
    'SaaS/Apps': ['saas', 'app', 'subscription', 'mrr', 'arr', 'software'],
    'Content/Creator': ['youtube', 'tiktok', 'newsletter', 'content creator', 'influencer', 'subscribers'],
    'Ads/Marketing': ['meta ads', 'facebook ads', 'google ads', 'paid ads', 'cpa', 'cpc', 'roas'],
    'Affiliate': ['affiliate', 'commission', 'referral'],
    'Services': ['consulting', 'coaching', 'agency', 'freelance', 'service'],
    'AI Products': ['ai tool', 'ai agent', 'chatbot', 'automation', 'ai app'],
    'Ecommerce': ['shopify', 'dropshipping', 'ecommerce', 'online store', 'physical product']
}

money_findings = {category: [] for category in money_keywords}
revenue_mentions = []

for bm in bookmarks:
    text_lower = bm['text'].lower()
    
    # Revenue mentions
    revenue_patterns = [
        r'\$[\d,]+k?[\/\s]*(month|mo|year|yr|day)',
        r'[\d,]+k[\/\s]*(month|mo|per month)',
        r'(made|making|earned|revenue|profit).*?\$[\d,]+',
    ]
    
    for pattern in revenue_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            revenue_mentions.append({
                'text': bm['text'][:200],
                'author': bm['author'],
                'url': bm['url']
            })
            break
    
    # Categorize money methods
    for category, keywords in money_keywords.items():
        if any(kw in text_lower for kw in keywords):
            money_findings[category].append({
                'text': bm['text'][:150],
                'author': bm['author'],
                'url': bm['url']
            })

for category, items in money_findings.items():
    if items:
        print(f"\n{category}: {len(items)} mentions")
        for item in items[:3]:
            print(f"  • {item['author']}: {item['text'][:100]}...")

print(f"\n\n💵 REVENUE MENTIONS: {len(revenue_mentions)} bookmarks")
for item in revenue_mentions[:10]:
    print(f"  • {item['author']}: {item['text'][:120]}...")

# === TECH STACKS ===
print("\n" + "=" * 80)
print("🛠️  TECH STACKS & TOOLS")
print("=" * 80)

tech_keywords = {
    'AI/ML': ['gpt', 'claude', 'openai', 'anthropic', 'llm', 'ai agent', 'langchain', 'vector'],
    'Frontend': ['react', 'next.js', 'nextjs', 'vue', 'tailwind', 'typescript', 'vercel'],
    'Backend': ['node', 'python', 'django', 'flask', 'fastapi', 'express', 'supabase', 'firebase'],
    'Mobile': ['react native', 'flutter', 'swift', 'ios', 'android'],
    'NoCode': ['bubble', 'webflow', 'airtable', 'zapier', 'make.com', 'n8n'],
    'Marketing': ['convertkit', 'beehiiv', 'meta ads', 'google ads', 'stripe', 'lemonsqueezy'],
    'Design': ['figma', 'canva', 'midjourney', 'stable diffusion'],
    'Video/Content': ['capcut', 'descript', 'runway', 'elevenlabs', 'video ai']
}

tech_findings = {category: Counter() for category in tech_keywords}

for bm in bookmarks:
    text_lower = bm['text'].lower()
    for category, keywords in tech_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                tech_findings[category][kw] += 1

for category, counter in tech_findings.items():
    if counter:
        print(f"\n{category}:")
        for tool, count in counter.most_common(5):
            print(f"  • {tool}: {count} mentions")

# === SOLOPRENEUR INSIGHTS ===
print("\n" + "=" * 80)
print("💡 SOLOPRENEUR INSIGHTS & STRATEGIES")
print("=" * 80)

insight_keywords = [
    'distribution', 'organic', 'viral', 'seo', 'traffic',
    'validate', 'mvp', 'launch', 'build in public',
    'email list', 'audience', 'community', 'twitter',
    'passive income', 'automation', 'scale', 'leverage',
    'niche', 'micro-saas', 'indie hacker', 'bootstrap'
]

insights = []
for bm in bookmarks:
    text_lower = bm['text'].lower()
    if any(kw in text_lower for kw in insight_keywords):
        if bm['word_count'] > 50:
            insights.append({
                'text': bm['text'],
                'author': bm['author'],
                'url': bm['url'],
                'word_count': bm['word_count']
            })

insights.sort(key=lambda x: x['word_count'], reverse=True)

print(f"\nFound {len(insights)} detailed strategy posts. Top 15:\n")
for i, item in enumerate(insights[:15], 1):
    print(f"{i}. {item['author']} ({item['word_count']} words)")
    print(f"   {item['text'][:200]}...")
    print(f"   {item['url']}\n")

print(f"\n\n✅ Analysis complete!")
