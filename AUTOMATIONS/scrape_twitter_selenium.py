#!/usr/bin/env python3
"""
Scrape Twitter/X using Selenium with Chrome profile
Requires: pip install selenium webdriver-manager
Usage: python3 scrape_twitter_selenium.py
"""

import time
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
ALPHA_STAGING = PROJECT_DIR / "LEDGER" / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = PROJECT_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"

# Chrome profile path (macOS default)
CHROME_USER_DATA = str(Path.home() / "Library/Application Support/Google/Chrome")


class TwitterSeleniumScraper:
    def __init__(self):
        self.existing_urls = self.load_existing_urls()
        self.next_alpha_id = self.get_next_alpha_id()

    def load_existing_urls(self):
        """Load existing source URLs to avoid duplicates"""
        urls = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('source_url'):
                        urls.add(row['source_url'])
        return urls

    def get_next_alpha_id(self):
        """Get next available ALPHA ID"""
        max_id = 0
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    match = re.match(r'ALPHA(\\d+)', row.get('alpha_id', ''))
                    if match:
                        max_id = max(max_id, int(match.group(1)))
        return max_id + 1

    def load_high_signal_accounts(self):
        """Load Twitter accounts marked auto_monitor=TRUE"""
        accounts = []
        with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                platform = row.get('platform', '').strip()
                if platform in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                    handle = row.get('source_name', '').replace('@', '')
                    if handle:
                        accounts.append({
                            'handle': handle,
                            'signal_quality': row.get('signal_quality', 'MEDIUM')
                        })

        # Sort by signal quality
        priority = {'HIGHEST': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        accounts.sort(key=lambda x: priority.get(x['signal_quality'], 4))
        return accounts

    def is_business_content(self, text):
        """Filter for business/tech content only"""
        if len(text) < 50:
            return False

        business_keywords = [
            'revenue', 'mrr', 'arr', 'users', 'growth', 'launch', 'build',
            'app', 'saas', 'startup', 'indie', 'maker', 'founder',
            'email', 'seo', 'marketing', 'conversion', 'funnel',
            'automation', 'ai', 'tool', 'product', 'api', 'code', '$'
        ]

        text_lower = text.lower()
        return any(keyword in text_lower for keyword in business_keywords)

    def scrape_account(self, driver, handle):
        """Scrape recent posts from a Twitter account"""
        print(f"🔍 Scraping @{handle}...")

        try:
            # Navigate to profile
            driver.get(f"https://x.com/{handle}")
            time.sleep(3)

            posts = []
            seen_urls = set()

            # Scroll and collect tweets
            for scroll in range(5):
                try:
                    # Wait for tweets to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
                    )

                    articles = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')

                    for article in articles:
                        try:
                            link = article.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
                            url = link.get_attribute('href')

                            if url in seen_urls or url in self.existing_urls:
                                continue
                            seen_urls.add(url)

                            text_elem = article.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                            text = text_elem.text

                            if self.is_business_content(text):
                                posts.append({
                                    'url': url,
                                    'text': text,
                                    'handle': handle,
                                    'scraped_at': datetime.now().isoformat()
                                })

                        except Exception:
                            continue

                    # Scroll down
                    driver.execute_script("window.scrollBy(0, 800)")
                    time.sleep(1.5)

                except Exception as e:
                    print(f"  ⚠️  Scroll {scroll + 1} error: {e}")
                    break

            print(f"  ✓ Found {len(posts)} new posts from @{handle}")
            return posts

        except Exception as e:
            print(f"  ❌ Error scraping @{handle}: {e}")
            return []

    def categorize_content(self, text):
        """Auto-categorize based on content"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['app', 'mobile', 'ios', 'android']):
            return 'APP_FACTORY'
        elif any(word in text_lower for word in ['email', 'cold', 'outbound']):
            return 'COLD_OUTBOUND'
        elif any(word in text_lower for word in ['seo', 'search', 'google']):
            return 'SEO_GEO_ASO'
        elif any(word in text_lower for word in ['content', 'tiktok', 'youtube']):
            return 'CONTENT_FARM'
        elif any(word in text_lower for word in ['ai', 'automation', 'tool']):
            return 'TOOL_ALPHA'
        elif any(word in text_lower for word in ['revenue', 'pricing', 'monetization']):
            return 'MONETIZATION'
        elif any(word in text_lower for word in ['growth', 'traffic', 'viral']):
            return 'GROWTH_HACK'
        else:
            return 'GENERAL'

    def save_to_csv(self, data):
        """Save extracted data to ALPHA_STAGING.csv"""
        if not data:
            print("⚠️  No new posts to save")
            return

        print(f"💾 Saving {len(data)} posts to ALPHA_STAGING.csv...")

        # Read existing file
        rows = []
        fieldnames = []
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)
        else:
            fieldnames = [
                'alpha_id', 'source', 'source_url', 'category', 'tactic',
                'full_description', 'actionable_steps', 'roi_potential',
                'implementation_complexity', 'legal_risk', 'applicable_methods',
                'status', 'priority', 'reviewer_notes', 'engagement_authenticity',
                'earnings_verified'
            ]

        # Add new entries
        for item in data:
            alpha_id = f"ALPHA{self.next_alpha_id}"
            self.next_alpha_id += 1

            category = self.categorize_content(item['text'])

            row = {k: '' for k in fieldnames}
            row.update({
                'alpha_id': alpha_id,
                'source': f"@{item['handle']} (high-signal Selenium scrape)",
                'source_url': item['url'],
                'category': category,
                'tactic': item['text'][:200] + '...' if len(item['text']) > 200 else item['text'],
                'full_description': item['text'],
                'actionable_steps': '',
                'roi_potential': 'MEDIUM',
                'implementation_complexity': 'MEDIUM',
                'legal_risk': 'LOW',
                'applicable_methods': category,
                'status': 'PENDING_REVIEW',
                'priority': '',
                'reviewer_notes': f"Auto-scraped via Selenium. Scraped {item.get('scraped_at', 'unknown')}",
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'FALSE'
            })
            rows.append(row)

        # Write back
        with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ Saved {len(data)} new entries (ALPHA{self.next_alpha_id - len(data)}-ALPHA{self.next_alpha_id - 1})")


def main():
    print("🚀 Twitter Selenium Scraper")
    print("=" * 60)

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={CHROME_USER_DATA}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    print("🌐 Launching Chrome with your profile...")
    print("⚠️  Make sure Chrome is CLOSED before running this script")
    print()

    try:
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        scraper = TwitterSeleniumScraper()
        accounts = scraper.load_high_signal_accounts()

        print(f"📋 Found {len(accounts)} high-signal accounts to scrape")
        print()

        all_posts = []
        for i, account in enumerate(accounts, 1):
            print(f"[{i}/{len(accounts)}]", end=' ')
            posts = scraper.scrape_account(driver, account['handle'])
            all_posts.extend(posts)
            time.sleep(2)  # Delay between accounts

        scraper.save_to_csv(all_posts)

        print()
        print("✅ SCRAPING COMPLETE")
        print(f"📊 Total new entries: {len(all_posts)}")
        print(f"📁 Check: {ALPHA_STAGING}")
        print()
        print("🔍 Run: /review-alpha to approve entries")

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Make sure:")
        print("  1. Chrome is COMPLETELY CLOSED")
        print("  2. You have selenium installed: pip install selenium webdriver-manager")
        print("  3. Your Chrome profile is at the default location")

    finally:
        if 'driver' in locals():
            driver.quit()


if __name__ == "__main__":
    main()
