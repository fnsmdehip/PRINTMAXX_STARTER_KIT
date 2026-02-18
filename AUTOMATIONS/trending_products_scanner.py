#!/usr/bin/env python3
"""
Trending Products Scanner
Finds trending products across Amazon for arbitrage opportunities.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import argparse
from datetime import datetime
from urllib.parse import quote_plus

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

def get_random_headers():
    """Return randomized headers."""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def fetch_page(url, max_retries=3):
    """Fetch page with retry logic."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=get_random_headers(), timeout=15)
            if response.status_code == 200:
                return response
            elif response.status_code == 503:
                print(f"    [!] Got 503 (rate limited), waiting...")
                time.sleep(random.uniform(10, 20))
            else:
                print(f"    [!] Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"    [!] Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(5, 10))
    return None

def scrape_amazon_movers_shakers(category=''):
    """
    Scrape Amazon Movers & Shakers page.
    Products with biggest sales rank gains in last 24 hours.
    """
    print("[*] Scraping Amazon Movers & Shakers...")

    products = []

    # Category URLs
    category_urls = {
        '': 'https://www.amazon.com/gp/movers-and-shakers/',
        'electronics': 'https://www.amazon.com/gp/movers-and-shakers/electronics/',
        'home': 'https://www.amazon.com/gp/movers-and-shakers/home-garden/',
        'toys': 'https://www.amazon.com/gp/movers-and-shakers/toys-and-games/',
        'beauty': 'https://www.amazon.com/gp/movers-and-shakers/beauty/',
        'sports': 'https://www.amazon.com/gp/movers-and-shakers/sporting-goods/',
    }

    url = category_urls.get(category, category_urls[''])

    response = fetch_page(url)
    if not response:
        print("    [!] Failed to fetch Movers & Shakers")
        return products

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find product listings
    # Note: Amazon's HTML structure changes frequently - these selectors may need updates
    product_items = soup.find_all('div', {'class': 'zg-grid-general-faceout'})

    print(f"    Found {len(product_items)} potential product items")

    for item in product_items[:50]:  # Limit to top 50
        try:
            # Extract product title
            title_elem = item.find('div', {'class': 'p13n-sc-truncate'})
            if not title_elem:
                title_elem = item.find('a', {'class': 'a-link-normal'})

            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Product'

            # Extract price
            price_elem = item.find('span', {'class': 'p13n-sc-price'})
            if not price_elem:
                price_elem = item.find('span', {'class': 'a-price-whole'})

            price_text = price_elem.get_text(strip=True) if price_elem else '$0.00'
            price = float(price_text.replace('$', '').replace(',', '').split('.')[0])

            # Extract ASIN/product URL
            link_elem = item.find('a', href=True)
            product_url = f"https://www.amazon.com{link_elem['href']}" if link_elem else ''

            # Extract ASIN from URL
            asin = ''
            if '/dp/' in product_url:
                asin = product_url.split('/dp/')[1].split('/')[0].split('?')[0]

            # Extract rank
            rank_elem = item.find('span', {'class': 'zg-badge-text'})
            rank = rank_elem.get_text(strip=True).replace('#', '') if rank_elem else '0'

            products.append({
                'product_name': title[:100],  # Truncate long titles
                'price': price,
                'asin': asin,
                'url': product_url,
                'rank': rank,
                'source': 'Movers & Shakers',
                'category': category if category else 'All',
                'trend_type': 'Rising Fast'
            })

        except Exception as e:
            print(f"    [!] Error parsing product: {e}")
            continue

    print(f"    [✓] Extracted {len(products)} products from Movers & Shakers")
    return products

def scrape_amazon_best_sellers(category=''):
    """
    Scrape Amazon Best Sellers page.
    Current top-selling products.
    """
    print("[*] Scraping Amazon Best Sellers...")

    products = []

    category_urls = {
        '': 'https://www.amazon.com/gp/bestsellers/',
        'electronics': 'https://www.amazon.com/gp/bestsellers/electronics/',
        'home': 'https://www.amazon.com/gp/bestsellers/home-garden/',
        'toys': 'https://www.amazon.com/gp/bestsellers/toys-and-games/',
        'beauty': 'https://www.amazon.com/gp/bestsellers/beauty/',
        'sports': 'https://www.amazon.com/gp/bestsellers/sporting-goods/',
    }

    url = category_urls.get(category, category_urls[''])

    response = fetch_page(url)
    if not response:
        print("    [!] Failed to fetch Best Sellers")
        return products

    soup = BeautifulSoup(response.content, 'html.parser')

    product_items = soup.find_all('div', {'class': 'zg-grid-general-faceout'})

    print(f"    Found {len(product_items)} potential product items")

    for item in product_items[:50]:
        try:
            title_elem = item.find('div', {'class': 'p13n-sc-truncate'})
            if not title_elem:
                title_elem = item.find('a', {'class': 'a-link-normal'})

            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Product'

            price_elem = item.find('span', {'class': 'p13n-sc-price'})
            if not price_elem:
                price_elem = item.find('span', {'class': 'a-price-whole'})

            price_text = price_elem.get_text(strip=True) if price_elem else '$0.00'
            price = float(price_text.replace('$', '').replace(',', '').split('.')[0])

            link_elem = item.find('a', href=True)
            product_url = f"https://www.amazon.com{link_elem['href']}" if link_elem else ''

            asin = ''
            if '/dp/' in product_url:
                asin = product_url.split('/dp/')[1].split('/')[0].split('?')[0]

            rank_elem = item.find('span', {'class': 'zg-badge-text'})
            rank = rank_elem.get_text(strip=True).replace('#', '') if rank_elem else '0'

            products.append({
                'product_name': title[:100],
                'price': price,
                'asin': asin,
                'url': product_url,
                'rank': rank,
                'source': 'Best Sellers',
                'category': category if category else 'All',
                'trend_type': 'Top Seller'
            })

        except Exception as e:
            continue

    print(f"    [✓] Extracted {len(products)} products from Best Sellers")
    return products

def scrape_amazon_most_wished_for(category=''):
    """
    Scrape Amazon Most Wished For page.
    Products people are adding to wish lists.
    """
    print("[*] Scraping Amazon Most Wished For...")

    products = []

    category_urls = {
        '': 'https://www.amazon.com/gcx/most-wished-for/gfhz/',
        'electronics': 'https://www.amazon.com/gcx/most-wished-for/electronics/gfhz/',
        'home': 'https://www.amazon.com/gcx/most-wished-for/home-garden/gfhz/',
        'toys': 'https://www.amazon.com/gcx/most-wished-for/toys-and-games/gfhz/',
        'beauty': 'https://www.amazon.com/gcx/most-wished-for/beauty/gfhz/',
        'sports': 'https://www.amazon.com/gcx/most-wished-for/sporting-goods/gfhz/',
    }

    url = category_urls.get(category, category_urls[''])

    response = fetch_page(url)
    if not response:
        print("    [!] Failed to fetch Most Wished For")
        return products

    soup = BeautifulSoup(response.content, 'html.parser')

    product_items = soup.find_all('div', {'class': 'zg-grid-general-faceout'})

    print(f"    Found {len(product_items)} potential product items")

    for item in product_items[:50]:
        try:
            title_elem = item.find('div', {'class': 'p13n-sc-truncate'})
            if not title_elem:
                title_elem = item.find('a', {'class': 'a-link-normal'})

            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Product'

            price_elem = item.find('span', {'class': 'p13n-sc-price'})
            if not price_elem:
                price_elem = item.find('span', {'class': 'a-price-whole'})

            price_text = price_elem.get_text(strip=True) if price_elem else '$0.00'
            price = float(price_text.replace('$', '').replace(',', '').split('.')[0])

            link_elem = item.find('a', href=True)
            product_url = f"https://www.amazon.com{link_elem['href']}" if link_elem else ''

            asin = ''
            if '/dp/' in product_url:
                asin = product_url.split('/dp/')[1].split('/')[0].split('?')[0]

            rank_elem = item.find('span', {'class': 'zg-badge-text'})
            rank = rank_elem.get_text(strip=True).replace('#', '') if rank_elem else '0'

            products.append({
                'product_name': title[:100],
                'price': price,
                'asin': asin,
                'url': product_url,
                'rank': rank,
                'source': 'Most Wished For',
                'category': category if category else 'All',
                'trend_type': 'High Demand'
            })

        except Exception as e:
            continue

    print(f"    [✓] Extracted {len(products)} products from Most Wished For")
    return products

def identify_price_drops(products):
    """
    Identify products with recent price drops.
    In production, would integrate with Keepa API for historical price data.
    """
    print("\n[*] Analyzing for price drops...")
    print("    [!] Note: Full price history requires Keepa API integration")

    # Add placeholder for price drop analysis
    for product in products:
        product['price_drop'] = 'Unknown'
        product['historic_high'] = 0
        product['potential_margin'] = 0

    return products

def save_to_csv(products, filename):
    """Save products to CSV."""

    if not products:
        print("\n[!] No products found")
        return

    fieldnames = [
        'product_name', 'price', 'asin', 'url', 'rank',
        'source', 'category', 'trend_type', 'price_drop',
        'historic_high', 'potential_margin'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"\n[✓] Saved {len(products)} products to {filename}")

    # Print summary
    print(f"\n{'='*80}")
    print("TRENDING PRODUCTS SUMMARY")
    print(f"{'='*80}\n")

    # Group by source
    by_source = {}
    for product in products:
        source = product['source']
        by_source[source] = by_source.get(source, 0) + 1

    for source, count in by_source.items():
        print(f"  {source}: {count} products")

    # Show top 10
    print(f"\n{'='*80}")
    print("TOP 10 TRENDING PRODUCTS")
    print(f"{'='*80}\n")

    for i, product in enumerate(products[:10], 1):
        print(f"{i}. {product['product_name']}")
        print(f"   Price: ${product['price']:.2f} | Rank: #{product['rank']}")
        print(f"   Source: {product['source']} | Type: {product['trend_type']}")
        print(f"   ASIN: {product['asin']}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Trending Products Scanner')
    parser.add_argument('--category', default='',
                        choices=['', 'electronics', 'home', 'toys', 'beauty', 'sports'],
                        help='Product category (blank for all categories)')
    parser.add_argument('--source', default='all',
                        choices=['all', 'movers', 'bestsellers', 'wished'],
                        help='Which trending list to scrape')
    parser.add_argument('--output', default='trending_products.csv',
                        help='Output CSV filename')

    args = parser.parse_args()

    print("="*80)
    print("TRENDING PRODUCTS SCANNER")
    print("="*80)
    print(f"Category: {args.category if args.category else 'All'}")
    print(f"Source: {args.source}")
    print("="*80 + "\n")

    all_products = []

    # Scrape based on source parameter
    if args.source in ['all', 'movers']:
        products = scrape_amazon_movers_shakers(args.category)
        all_products.extend(products)
        time.sleep(random.uniform(3, 6))

    if args.source in ['all', 'bestsellers']:
        products = scrape_amazon_best_sellers(args.category)
        all_products.extend(products)
        time.sleep(random.uniform(3, 6))

    if args.source in ['all', 'wished']:
        products = scrape_amazon_most_wished_for(args.category)
        all_products.extend(products)
        time.sleep(random.uniform(3, 6))

    # Analyze for price drops
    all_products = identify_price_drops(all_products)

    # Remove duplicates by ASIN
    unique_products = {}
    for product in all_products:
        asin = product['asin']
        if asin and asin not in unique_products:
            unique_products[asin] = product

    final_products = list(unique_products.values())

    # Sort by rank
    final_products.sort(key=lambda x: int(x['rank']) if x['rank'].isdigit() else 999)

    # Save to CSV
    save_to_csv(final_products, args.output)

    print("\n[*] NEXT STEPS:")
    print("    1. Review trending_products.csv for high-demand items")
    print("    2. Check sourcing costs (Walmart, Target clearance, AliExpress)")
    print("    3. Use Keepa.com to verify price history and sales rank trends")
    print("    4. Calculate profit margins with ecom_arb_scanner.py")
    print("    5. Start with small test orders (1-5 units)")
    print("    6. Track sell-through rates before scaling")

if __name__ == "__main__":
    main()
