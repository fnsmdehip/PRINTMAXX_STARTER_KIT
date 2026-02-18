#!/usr/bin/env python3
"""
Analyze X DMs for real funnel strategies
SAFE MODE: Only reads DMs, never clicks unknown links
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime
import re

OUTPUT_DIR = Path("deep_scrape_output")

async def analyze_dm_funnels(page):
    """
    Analyze DMs for funnel patterns
    SAFETY: Only reads text, never clicks links
    """

    print("🔍 Analyzing X DMs for funnel strategies...")
    print("⚠️  SAFE MODE: Only reading DMs, not clicking any links\n")

    results = {
        'dm_funnels': [],
        'gumroad_funnels': [],
        'product_types': {},
        'funnel_patterns': []
    }

    try:
        # Navigate to DMs
        print("📬 Opening DM inbox...")
        await page.goto("https://x.com/messages", wait_until="load", timeout=20000)
        await asyncio.sleep(4)

        # Get conversation list (skip message requests)
        print("📋 Loading conversations (skipping message requests)...\n")

        # Click on "Primary" tab to avoid message requests
        try:
            primary_tab = page.locator('a[href="/messages"]').first
            if await primary_tab.count() > 0:
                await primary_tab.click()
                await asyncio.sleep(2)
        except:
            pass

        # Get all visible conversations
        conversations = await page.locator('div[data-testid="conversation"]').all()
        print(f"Found {len(conversations)} conversations\n")

        for i, conv in enumerate(conversations[:20], 1):  # Analyze first 20
            try:
                print(f"[{i}/20] Analyzing conversation...")

                # Click conversation to open
                await conv.click()
                await asyncio.sleep(2)

                # Get sender name
                sender = "Unknown"
                try:
                    sender_elem = page.locator('div[data-testid="conversation"] h2').first
                    if await sender_elem.count() > 0:
                        sender = await sender_elem.inner_text()
                except:
                    pass

                print(f"   From: {sender}")

                # Get all messages in conversation
                messages = await page.locator('div[data-testid="messageEntry"]').all()
                print(f"   Messages: {len(messages)}")

                conversation_data = {
                    'sender': sender,
                    'message_count': len(messages),
                    'has_links': False,
                    'funnel_type': 'unknown',
                    'messages': []
                }

                # Read each message
                for msg in messages[-10:]:  # Last 10 messages
                    try:
                        msg_text_elem = msg.locator('div[dir="auto"]').first
                        if await msg_text_elem.count() > 0:
                            msg_text = await msg_text_elem.inner_text()

                            # Check for funnel indicators
                            has_link = 'http' in msg_text or 'link' in msg_text.lower()
                            is_gumroad = 'gumroad' in msg_text.lower()
                            has_free_offer = any(word in msg_text.lower() for word in ['free', 'download', 'get it here', 'grab it'])

                            if has_link or len(msg_text) > 50:
                                conversation_data['messages'].append({
                                    'text': msg_text[:500],
                                    'has_link': has_link,
                                    'is_gumroad': is_gumroad,
                                    'has_free_offer': has_free_offer
                                })

                                if has_link:
                                    conversation_data['has_links'] = True

                                # Extract URLs (but don't visit them)
                                urls = re.findall(r'https?://\S+', msg_text)
                                if urls:
                                    conversation_data['extracted_urls'] = urls[:3]

                                    # Categorize funnel type
                                    for url in urls:
                                        if 'gumroad' in url:
                                            conversation_data['funnel_type'] = 'gumroad'
                                        elif 'lemonsqueezy' in url or 'lemon.squeezy' in url:
                                            conversation_data['funnel_type'] = 'lemonsqueezy'
                                        elif 'notion' in url:
                                            conversation_data['funnel_type'] = 'notion'
                                        elif 'beehiiv' in url or 'substack' in url:
                                            conversation_data['funnel_type'] = 'newsletter'
                                        elif 'calendly' in url or 'cal.com' in url:
                                            conversation_data['funnel_type'] = 'booking'
                    except:
                        continue

                # Only save if it has funnel content
                if conversation_data['has_links'] and conversation_data['messages']:
                    results['dm_funnels'].append(conversation_data)

                    print(f"   ✅ Funnel type: {conversation_data['funnel_type']}")
                    print(f"   📎 Links found: {len(conversation_data.get('extracted_urls', []))}")

                    if conversation_data['funnel_type'] == 'gumroad':
                        results['gumroad_funnels'].append(conversation_data)

                    # Count funnel types
                    funnel_type = conversation_data['funnel_type']
                    results['product_types'][funnel_type] = results['product_types'].get(funnel_type, 0) + 1

                print()

            except Exception as e:
                print(f"   ❌ Error: {e}\n")
                continue

            # Rate limit
            await asyncio.sleep(1)

        # Analyze patterns
        print("\n" + "="*80)
        print("📊 FUNNEL ANALYSIS SUMMARY")
        print("="*80)

        print(f"\n💬 Total DM funnels found: {len(results['dm_funnels'])}")
        print(f"🛒 Gumroad funnels: {len(results['gumroad_funnels'])}")

        print(f"\n📈 Funnel types:")
        for funnel_type, count in sorted(results['product_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"   • {funnel_type}: {count}")

        # Show examples
        if results['gumroad_funnels']:
            print(f"\n🎯 GUMROAD FUNNEL EXAMPLES:")
            for i, funnel in enumerate(results['gumroad_funnels'][:3], 1):
                print(f"\n{i}. From: {funnel['sender']}")
                print(f"   Messages: {funnel['message_count']}")
                if funnel.get('extracted_urls'):
                    print(f"   URLs: {funnel['extracted_urls'][0]}")
                if funnel['messages']:
                    print(f"   Sample: {funnel['messages'][0]['text'][:150]}...")

        # Save results
        output_file = OUTPUT_DIR / f"dm_funnel_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Analysis saved to: {output_file}")

        return results

    except Exception as e:
        print(f"\n❌ Error analyzing DMs: {e}")
        return results

async def main():
    print("🚀 X DM Funnel Analyzer")
    print("=" * 80)
    print("Analyzing your DMs for working funnel strategies")
    print("SAFE MODE: Only reading, never clicking links\n")

    async with async_playwright() as p:
        print("🔌 Connecting to Brave...")
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected!\n")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("Start Brave with: /Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --remote-debugging-port=9222")
            return

        contexts = browser.contexts
        if not contexts:
            print("❌ No browser contexts")
            return

        context = contexts[0]
        pages = context.pages
        page = pages[0] if pages else await context.new_page()

        # Analyze DMs
        results = await analyze_dm_funnels(page)

        print(f"\n\n{'='*80}")
        print("✅ ANALYSIS COMPLETE")
        print("="*80)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
