#!/usr/bin/env python3
"""
Analyze deep scrape results and extract actionable alpha
"""

import json
import glob
from pathlib import Path

# Find latest results
result_files = sorted(glob.glob('deep_scrape_output/x_bookmarks_deep_*.json'), reverse=True)
if not result_files:
    # Try progress files
    result_files = sorted(glob.glob('deep_scrape_output/progress_*.json'), reverse=True)

if not result_files:
    print("❌ No results found!")
    exit(1)

latest_file = result_files[0]
print(f"📊 Analyzing: {latest_file}\n")

with open(latest_file, 'r') as f:
    results = json.load(f)

print(f"Total bookmarks scraped: {len(results)}\n")

# === ALPHA EXTRACTION ===
print("=" * 80)
print("💎 HIGH-VALUE ALPHA EXTRACTION")
print("=" * 80)

# 1. REVENUE PLAYBOOKS (text + proof)
revenue_playbooks = []
for r in results:
    orig = r['original']
    text = r.get('full_text', orig.get('text', ''))
    text_lower = text.lower()
    
    has_revenue = any(word in text_lower for word in ['$', 'revenue', 'made', 'earned', 'profit', 'k/mo', '/month'])
    has_images = r.get('image_urls') or r.get('screenshot_path')
    is_long = len(text) > 300
    
    if has_revenue and (has_images or is_long):
        revenue_playbooks.append({
            'author': orig['author'],
            'text': text,
            'url': orig['url'],
            'images': r.get('image_urls', []),
            'screenshot': r.get('screenshot_path'),
            'thread_length': r.get('thread_length', 0)
        })

print(f"\n1. REVENUE PLAYBOOKS ({len(revenue_playbooks)} found)")
print("   Posts with revenue mentions + proof/details\n")
for i, rb in enumerate(revenue_playbooks[:10], 1):
    print(f"{i}. {rb['author']}")
    print(f"   Text length: {len(rb['text'])} chars")
    print(f"   Images: {len(rb['images'])}")
    print(f"   Screenshot: {'✅' if rb['screenshot'] else '❌'}")
    print(f"   {rb['url']}")
    print(f"   Preview: {rb['text'][:200]}...")
    print()

# 2. TECHNICAL PLAYBOOKS (step-by-step guides)
playbook_keywords = ['step', 'how to', 'here\'s how', 'setup', 'guide', 'workflow', 'process', 'blueprint', 'framework']
technical_playbooks = []

for r in results:
    orig = r['original']
    text = r.get('full_text', orig.get('text', ''))
    text_lower = text.lower()
    
    has_playbook_words = any(kw in text_lower for kw in playbook_keywords)
    is_long = len(text) > 400
    
    if has_playbook_words and is_long:
        technical_playbooks.append({
            'author': orig['author'],
            'text': text,
            'url': orig['url'],
            'screenshot': r.get('screenshot_path'),
            'word_count': len(text.split())
        })

print(f"\n2. TECHNICAL PLAYBOOKS ({len(technical_playbooks)} found)")
print("   Step-by-step guides and workflows\n")
for i, tp in enumerate(technical_playbooks[:10], 1):
    print(f"{i}. {tp['author']} ({tp['word_count']} words)")
    print(f"   Screenshot: {'✅' if tp['screenshot'] else '❌'}")
    print(f"   {tp['url']}")
    print(f"   Preview: {tp['text'][:200]}...")
    print()

# 3. INFOGRAPHIC/VISUAL ALPHA (images with tactical info)
visual_alpha = []
for r in results:
    orig = r['original']
    has_images = len(r.get('image_urls', [])) >= 2 or r.get('screenshot_path')
    
    text_lower = r.get('full_text', orig.get('text', '')).lower()
    is_tactical = any(word in text_lower for word in [
        'stack', 'tools', 'framework', 'funnel', 'breakdown', 
        'metrics', 'stats', 'results', 'data', 'numbers'
    ])
    
    if has_images and is_tactical:
        visual_alpha.append({
            'author': orig['author'],
            'text': r.get('full_text', orig.get('text', '')),
            'url': orig['url'],
            'screenshot': r.get('screenshot_path'),
            'image_count': len(r.get('image_urls', []))
        })

print(f"\n3. VISUAL/INFOGRAPHIC ALPHA ({len(visual_alpha)} found)")
print("   Posts with images showing tactical info\n")
for i, va in enumerate(visual_alpha[:10], 1):
    print(f"{i}. {va['author']}")
    print(f"   Images: {va['image_count']}")
    print(f"   Screenshot: {Path(va['screenshot']).name if va['screenshot'] else '❌'}")
    print(f"   {va['url']}")
    print(f"   Preview: {va['text'][:150]}...")
    print()

# 4. COPYWRITING/HOOKS (repurpose for niche accounts)
hook_patterns = ['if you', 'the secret', 'nobody talks about', 'stop doing', 'you can', 'i made']
copywriting_gold = []

for r in results:
    orig = r['original']
    text = r.get('full_text', orig.get('text', ''))
    
    first_line = text.split('\n')[0] if text else ''
    has_hook = any(pattern in first_line.lower() for pattern in hook_patterns)
    
    if has_hook and len(text) > 100:
        copywriting_gold.append({
            'author': orig['author'],
            'hook': first_line,
            'full_text': text,
            'url': orig['url']
        })

print(f"\n4. COPYWRITING HOOKS ({len(copywriting_gold)} found)")
print("   Strong opening lines to repurpose\n")
for i, cg in enumerate(copywriting_gold[:15], 1):
    print(f"{i}. {cg['author']}")
    print(f"   Hook: {cg['hook'][:120]}...")
    print(f"   {cg['url']}")
    print()

# === SAVE EXTRACTED ALPHA ===
output = {
    'revenue_playbooks': revenue_playbooks,
    'technical_playbooks': technical_playbooks,
    'visual_alpha': visual_alpha,
    'copywriting_hooks': copywriting_gold
}

output_file = 'deep_scrape_output/extracted_alpha.json'
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Alpha extracted and saved to: {output_file}")
print(f"\n📊 SUMMARY:")
print(f"   • Revenue playbooks: {len(revenue_playbooks)}")
print(f"   • Technical playbooks: {len(technical_playbooks)}")
print(f"   • Visual alpha: {len(visual_alpha)}")
print(f"   • Copywriting hooks: {len(copywriting_gold)}")
