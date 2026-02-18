#!/usr/bin/env python3
"""
E-commerce Arbitrage Scanner
Finds profitable arbitrage opportunities by comparing source prices to selling prices.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import argparse
from datetime import datetime
from urllib.parse import quote_plus
import json

# Platform fees
PLATFORM_FEES = {
    'ebay': 0.1325,  # 13.25% final value fee
    'facebook': 0.05,  # 5% (0% for local pickup)
    'amazon_fba': 0.15,  # 15% + fulfillment (estimated $3-5)
    'mercari': 0.10,  # 10%
    'poshmark': 0.20,  # 20%
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
]

def get_random_headers():
    """Return randomized headers to avoid detection."""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def search_walmart_clearance(category):
    """
    Search Walmart clearance section.
    Note: Actual API access requires API key. This is a simplified version.
    """
    print(f"[*] Searching Walmart clearance for {category}...")

    # Simulated results - in production, would use Walmart API or BrickSeek
    # For real implementation: https://developer.walmart.com/
    opportunities = [
        {
            'product_name': 'Example Wireless Earbuds',
            'source': 'Walmart',
            'source_price': 15.00,
            'source_url': 'https://walmart.com/clearance/electronics',
            'category': 'electronics',
            'note': 'API integration required for live data'
        }
    ]

    return opportunities

def search_amazon_price_drops(category):
    """
    Find Amazon products with recent price drops.
    Uses publicly available data (no API key needed).
    """
    print(f"[*] Searching Amazon price drops for {category}...")

    opportunities = []

    # Amazon Best Sellers by category
    category_urls = {
        'electronics': 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics',
        'home': 'https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden',
        'toys': 'https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games',
        'beauty': 'https://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty',
        'books': 'https://www.amazon.com/Best-Sellers-Books/zgbs/books',
    }

    url = category_urls.get(category, category_urls['electronics'])

    try:
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # This is simplified - actual scraping would need more robust selectors
            print(f"    [✓] Successfully fetched Amazon {category} page")
            opportunities.append({
                'product_name': f'Amazon {category.title()} Product',
                'source': 'Amazon',
                'source_price': 0.0,
                'source_url': url,
                'category': category,
                'note': 'Scraping Amazon requires rotating proxies and CAPTCHA handling'
            })
        else:
            print(f"    [!] Amazon returned status {response.status_code}")
    except Exception as e:
        print(f"    [!] Error fetching Amazon: {e}")

    time.sleep(random.uniform(2, 4))  # Rate limiting
    return opportunities

def search_aliexpress_trending(category):
    """
    Find trending products on AliExpress.
    These typically have 3-6 week shipping but very low prices.
    """
    print(f"[*] Searching AliExpress trending for {category}...")

    opportunities = []

    # AliExpress search URL
    search_term = quote_plus(category)
    url = f"https://www.aliexpress.com/wholesale?SearchText={search_term}&SortType=total_tranpro_desc"

    try:
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        if response.status_code == 200:
            print(f"    [✓] Successfully fetched AliExpress {category} page")

            # Simplified - actual implementation would parse JSON from page
            opportunities.append({
                'product_name': f'AliExpress {category.title()} Product',
                'source': 'AliExpress',
                'source_price': 0.0,
                'source_url': url,
                'category': category,
                'note': 'Long shipping times (3-6 weeks) - factor into strategy'
            })
        else:
            print(f"    [!] AliExpress returned status {response.status_code}")
    except Exception as e:
        print(f"    [!] Error fetching AliExpress: {e}")

    time.sleep(random.uniform(2, 4))
    return opportunities

def search_target_clearance(category):
    """
    Search Target clearance section.
    """
    print(f"[*] Searching Target clearance for {category}...")

    opportunities = []

    # Target clearance URL
    url = "https://www.target.com/c/clearance/-/N-5q0f4"

    try:
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        if response.status_code == 200:
            print(f"    [✓] Successfully fetched Target clearance page")

            opportunities.append({
                'product_name': f'Target {category.title()} Clearance',
                'source': 'Target',
                'source_price': 0.0,
                'source_url': url,
                'category': category,
                'note': 'Use BrickSeek.com for local inventory checking'
            })
        else:
            print(f"    [!] Target returned status {response.status_code}")
    except Exception as e:
        print(f"    [!] Error fetching Target: {e}")

    time.sleep(random.uniform(2, 4))
    return opportunities

def estimate_selling_price(product_name, source_price, category):
    """
    Estimate what a product could sell for based on markup patterns.

    Real implementation would:
    - Search completed eBay listings
    - Check Facebook Marketplace recent sales
    - Look at Amazon current prices
    - Use Keepa historical data
    """

    # Typical markup multipliers by category
    markup_multipliers = {
        'electronics': 2.0,  # 2x markup typical
        'home': 1.8,
        'toys': 2.2,
        'beauty': 2.5,
        'books': 1.5,
        'clothing': 2.0,
        'default': 2.0
    }

    multiplier = markup_multipliers.get(category, markup_multipliers['default'])

    # Estimate selling price
    estimated_price = source_price * multiplier

    return estimated_price

def calculate_profit(source_price, selling_price, platform, category):
    """
    Calculate net profit after platform fees and shipping.
    """

    # Platform fee
    fee_rate = PLATFORM_FEES.get(platform, 0.13)
    platform_fee = selling_price * fee_rate

    # Estimated shipping cost (varies by size/weight)
    shipping_costs = {
        'electronics': 5.00,
        'home': 8.00,
        'toys': 6.00,
        'beauty': 4.00,
        'books': 3.50,
        'clothing': 4.00,
        'default': 5.00
    }
    shipping = shipping_costs.get(category, shipping_costs['default'])

    # Additional FBA fulfillment fee if Amazon
    fba_fee = 3.50 if platform == 'amazon_fba' else 0.0

    # Net profit calculation
    total_cost = source_price + platform_fee + shipping + fba_fee
    net_profit = selling_price - total_cost

    # Margin percentage
    margin_pct = (net_profit / selling_price * 100) if selling_price > 0 else 0

    return {
        'net_profit': round(net_profit, 2),
        'margin_pct': round(margin_pct, 2),
        'fees': round(platform_fee + fba_fee, 2),
        'shipping': shipping,
        'total_cost': round(total_cost, 2)
    }

def analyze_opportunities(opportunities, min_profit=5.0, min_margin=20.0):
    """
    Analyze all opportunities and calculate profitability.
    """

    results = []

    print(f"\n[*] Analyzing {len(opportunities)} opportunities...")
    print(f"    Minimum profit: ${min_profit}")
    print(f"    Minimum margin: {min_margin}%\n")

    for opp in opportunities:
        # Skip if no price data
        if opp['source_price'] == 0.0:
            continue

        product_name = opp['product_name']
        source_price = opp['source_price']
        category = opp['category']

        # Estimate selling price
        estimated_sell_price = estimate_selling_price(product_name, source_price, category)

        # Calculate profit for each platform
        for platform in PLATFORM_FEES.keys():
            profit_data = calculate_profit(source_price, estimated_sell_price, platform, category)

            # Only include if meets minimum thresholds
            if profit_data['net_profit'] >= min_profit and profit_data['margin_pct'] >= min_margin:
                results.append({
                    'product_name': product_name,
                    'source': opp['source'],
                    'source_price': source_price,
                    'selling_platform': platform,
                    'estimated_sell_price': estimated_sell_price,
                    'fees': profit_data['fees'],
                    'shipping': profit_data['shipping'],
                    'net_profit': profit_data['net_profit'],
                    'margin_pct': profit_data['margin_pct'],
                    'product_url': opp.get('source_url', ''),
                    'category': category,
                    'note': opp.get('note', '')
                })

    # Sort by net profit descending
    results.sort(key=lambda x: x['net_profit'], reverse=True)

    return results

def get_trending_products():
    """
    Find currently trending/viral products.
    Sources: TikTok trends, Amazon Most Wished For, etc.
    """

    print("[*] Searching for trending products...\n")

    trending = []

    # Amazon Most Wished For
    print("[*] Checking Amazon Most Wished For...")
    try:
        url = "https://www.amazon.com/gcx/most-wished-for/gfhz/"
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        if response.status_code == 200:
            print("    [✓] Successfully fetched Most Wished For")
            trending.append({
                'product_name': 'Trending Amazon Product',
                'source': 'Amazon Most Wished For',
                'source_price': 0.0,
                'source_url': url,
                'category': 'trending',
                'note': 'Check for TikTok viral products - high demand items'
            })
    except Exception as e:
        print(f"    [!] Error: {e}")

    time.sleep(random.uniform(2, 4))

    # Amazon Movers & Shakers
    print("[*] Checking Amazon Movers & Shakers...")
    try:
        url = "https://www.amazon.com/gp/movers-and-shakers/"
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        if response.status_code == 200:
            print("    [✓] Successfully fetched Movers & Shakers")
            trending.append({
                'product_name': 'Fast-Rising Amazon Product',
                'source': 'Amazon Movers & Shakers',
                'source_price': 0.0,
                'source_url': url,
                'category': 'trending',
                'note': 'Products with biggest sales rank gains - catch the wave early'
            })
    except Exception as e:
        print(f"    [!] Error: {e}")

    return trending

def save_to_csv(results, filename):
    """Save results to CSV file."""

    if not results:
        print("\n[!] No opportunities found meeting criteria")
        return

    fieldnames = [
        'product_name', 'source', 'source_price', 'selling_platform',
        'estimated_sell_price', 'fees', 'shipping', 'net_profit',
        'margin_pct', 'product_url', 'category', 'note'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n[✓] Saved {len(results)} opportunities to {filename}")

    # Print top 5
    print(f"\n{'='*80}")
    print("TOP 5 OPPORTUNITIES")
    print(f"{'='*80}\n")

    for i, result in enumerate(results[:5], 1):
        print(f"{i}. {result['product_name']}")
        print(f"   Source: {result['source']} @ ${result['source_price']:.2f}")
        print(f"   Sell on: {result['selling_platform']} @ ${result['estimated_sell_price']:.2f}")
        print(f"   Net Profit: ${result['net_profit']:.2f} ({result['margin_pct']:.1f}% margin)")
        print(f"   Category: {result['category']}")
        if result['note']:
            print(f"   Note: {result['note']}")
        print()

def main():
    parser = argparse.ArgumentParser(description='E-commerce Arbitrage Scanner')
    parser.add_argument('category', nargs='?', default='electronics',
                        choices=['electronics', 'home', 'toys', 'beauty', 'books', 'clothing'],
                        help='Product category to search')
    parser.add_argument('--trending', action='store_true',
                        help='Focus on trending/viral products')
    parser.add_argument('--min-profit', type=float, default=5.0,
                        help='Minimum net profit in dollars (default: 5.0)')
    parser.add_argument('--min-margin', type=float, default=20.0,
                        help='Minimum profit margin percentage (default: 20.0)')
    parser.add_argument('--output', default='ecom_arb_opportunities.csv',
                        help='Output CSV filename')

    args = parser.parse_args()

    print("="*80)
    print("E-COMMERCE ARBITRAGE SCANNER")
    print("="*80)
    print(f"Category: {args.category}")
    print(f"Trending mode: {'ON' if args.trending else 'OFF'}")
    print(f"Min profit: ${args.min_profit}")
    print(f"Min margin: {args.min_margin}%")
    print("="*80 + "\n")

    all_opportunities = []

    if args.trending:
        # Search trending products
        trending = get_trending_products()
        all_opportunities.extend(trending)
    else:
        # Search all sources
        all_opportunities.extend(search_walmart_clearance(args.category))
        all_opportunities.extend(search_amazon_price_drops(args.category))
        all_opportunities.extend(search_aliexpress_trending(args.category))
        all_opportunities.extend(search_target_clearance(args.category))

    # Analyze and filter opportunities
    results = analyze_opportunities(all_opportunities, args.min_profit, args.min_margin)

    # Save to CSV
    save_to_csv(results, args.output)

    print("\n[*] IMPORTANT NOTES:")
    print("    - This is a research tool. Always verify prices manually before purchasing.")
    print("    - Consider shipping times (especially AliExpress: 3-6 weeks)")
    print("    - Check sell-through rates on target platforms")
    print("    - Use tools like Keepa (Amazon), BrickSeek (Walmart) for live data")
    print("    - Start small: test with $100-200 before scaling")
    print("    - Factor in storage, returns, and customer service time")

if __name__ == "__main__":
    main()
