#!/usr/bin/env python3
"""
Analyze funnel patterns from extracted data
"""

import json
import re

with open('deep_scrape_output/extracted_alpha.json', 'r') as f:
    alpha = json.load(f)

print("🎯 FUNNEL & MONETIZATION PATTERN ANALYSIS")
print("=" * 80)

# Analyze bio/funnel patterns from text
funnel_patterns = {
    'dm_triggers': [],
    'gumroad_mentions': [],
    'link_in_bio': [],
    'reply_for_access': [],
    'like_repost_triggers': []
}

all_posts = alpha['revenue_playbooks'] + alpha['technical_playbooks']

print(f"\nAnalyzing {len(all_posts)} high-value posts...\n")

# Pattern detection
for post in all_posts:
    text = post.get('text', '').lower()
    author = post.get('author', '')
    url = post.get('url', '')

    # DM triggers
    dm_patterns = [
        ('dm me', 'Direct DM request'),
        ('send me a dm', 'Direct DM request'),
        ('i\'ll dm you', 'Outbound DM promise'),
        ('reply and i\'ll send', 'Reply-for-DM'),
        ('comment and i\'ll dm', 'Comment-for-DM')
    ]

    for pattern, trigger_type in dm_patterns:
        if pattern in text:
            funnel_patterns['dm_triggers'].append({
                'author': author,
                'trigger': pattern,
                'type': trigger_type,
                'url': url,
                'preview': text[:200]
            })

    # Gumroad/product mentions
    product_patterns = ['gumroad', 'lemonsqueezy', 'stripe', 'checkout', 'buy now']
    if any(p in text for p in product_patterns):
        funnel_patterns['gumroad_mentions'].append({
            'author': author,
            'url': url,
            'preview': text[:200]
        })

    # Link in bio
    if 'link in bio' in text or 'link below' in text:
        funnel_patterns['link_in_bio'].append({
            'author': author,
            'url': url,
            'preview': text[:200]
        })

    # Reply triggers
    reply_patterns = ['reply with', 'comment below', 'drop a', 'tag someone']
    if any(p in text for p in reply_patterns):
        funnel_patterns['reply_for_access'].append({
            'author': author,
            'url': url,
            'preview': text[:200]
        })

    # Like/repost triggers
    engagement_patterns = ['like and repost', 'like + repost', 'retweet this', 'bookmark this']
    if any(p in text for p in engagement_patterns):
        funnel_patterns['like_repost_triggers'].append({
            'author': author,
            'url': url,
            'preview': text[:200]
        })

# Report findings
print("💬 DM TRIGGER STRATEGIES")
print(f"Found {len(funnel_patterns['dm_triggers'])} posts with DM triggers\n")
dm_types = {}
for item in funnel_patterns['dm_triggers']:
    trigger_type = item['type']
    dm_types[trigger_type] = dm_types.get(trigger_type, 0) + 1

for trigger_type, count in sorted(dm_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {trigger_type}: {count} uses")

if funnel_patterns['dm_triggers']:
    print(f"\n  Top examples:")
    for i, item in enumerate(funnel_patterns['dm_triggers'][:3], 1):
        print(f"\n  {i}. {item['author']}")
        print(f"     Trigger: '{item['trigger']}'")
        print(f"     {item['url']}")

# Gumroad/Product links
print(f"\n\n💰 PRODUCT/GUMROAD MENTIONS")
print(f"Found {len(funnel_patterns['gumroad_mentions'])} posts with product links\n")
for i, item in enumerate(funnel_patterns['gumroad_mentions'][:5], 1):
    print(f"  {i}. {item['author']}")
    print(f"     {item['url']}")
    print(f"     Preview: {item['preview'][:150]}...\n")

# Link in bio strategy
print(f"\n🔗 LINK IN BIO STRATEGY")
print(f"Found {len(funnel_patterns['link_in_bio'])} posts driving to bio link\n")
for i, item in enumerate(funnel_patterns['link_in_bio'][:5], 1):
    print(f"  {i}. {item['author']}")
    print(f"     {item['url']}\n")

# Reply triggers
print(f"\n💬 REPLY/COMMENT TRIGGERS")
print(f"Found {len(funnel_patterns['reply_for_access'])} posts with reply triggers\n")
for i, item in enumerate(funnel_patterns['reply_for_access'][:5], 1):
    print(f"  {i}. {item['author']}")
    print(f"     {item['url']}")
    print(f"     Preview: {item['preview'][:150]}...\n")

# Like/repost triggers
print(f"\n👍 LIKE + REPOST TRIGGERS")
print(f"Found {len(funnel_patterns['like_repost_triggers'])} posts with engagement triggers\n")
for i, item in enumerate(funnel_patterns['like_repost_triggers'][:5], 1):
    print(f"  {i}. {item['author']}")
    print(f"     {item['url']}")
    print(f"     Preview: {item['preview'][:150]}...\n")

# Save patterns
output = {
    'dm_triggers': funnel_patterns['dm_triggers'],
    'product_links': funnel_patterns['gumroad_mentions'],
    'link_in_bio': funnel_patterns['link_in_bio'],
    'reply_triggers': funnel_patterns['reply_for_access'],
    'engagement_triggers': funnel_patterns['like_repost_triggers']
}

with open('deep_scrape_output/funnel_patterns.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Patterns saved to: deep_scrape_output/funnel_patterns.json")
