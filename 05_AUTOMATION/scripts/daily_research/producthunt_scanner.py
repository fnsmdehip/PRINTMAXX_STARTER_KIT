#!/usr/bin/env python3
"""
Product Hunt Scanner for PRINTMAXX Daily Research

Scans Product Hunt for new tools and launches relevant to solopreneurs.
Uses PH's public API/web scraping.

Usage:
    python producthunt_scanner.py [--dry-run] [--days 1]
"""

import csv
import json
import os
import sys
import time
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, asdict
import argparse
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('producthunt_scanner')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
CACHE_DIR = BASE_DIR / 'AUTOMATIONS' / 'daily_research' / '.cache'


@dataclass
class PHProduct:
    """Represents a Product Hunt product"""
    id: str
    name: str
    tagline: str
    description: str
    url: str
    ph_url: str
    topics: List[str]
    votes_count: int
    comments_count: int
    maker_names: List[str]
    featured: bool
    launched_at: str


@dataclass
class AlphaFinding:
    """Represents a potential alpha finding"""
    alpha_id: str
    source: str
    source_url: str
    category: str
    title: str
    description: str
    actionable_steps: str
    effort_level: str
    roi_potential: str
    risk_level: str
    applies_to_niches: str
    status: str = 'PENDING_REVIEW'
    reviewed_date: str = ''
    reviewer_notes: str = ''


class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_minute: int = 20):
        self.calls_per_minute = calls_per_minute
        self.call_times = []

    def wait_if_needed(self):
        now = time.time()
        self.call_times = [t for t in self.call_times if now - t < 60]

        if len(self.call_times) >= self.calls_per_minute:
            wait_time = 60 - (now - self.call_times[0])
            if wait_time > 0:
                logger.debug(f"Rate limit reached. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time + random.uniform(0.5, 1.5))

        self.call_times.append(time.time())


class ProductHuntScanner:
    """Scans Product Hunt for alpha"""

    def __init__(self):
        self.api_token = os.getenv('PRODUCTHUNT_API_TOKEN')
        self.rate_limiter = RateLimiter(calls_per_minute=20)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.seen_ids = self._load_seen_ids()

        # Relevant topics for PRINTMAXX
        self.relevant_topics = [
            'artificial-intelligence', 'ai', 'productivity', 'developer-tools',
            'marketing', 'seo', 'email', 'automation', 'no-code', 'saas',
            'social-media', 'content-creation', 'writing', 'design',
            'mobile-apps', 'chrome-extensions', 'side-project',
            'fitness', 'health', 'wellness'
        ]

        # Keywords that indicate high relevance
        self.high_signal_keywords = [
            'solopreneur', 'indie', 'bootstrap', 'side project', 'ai',
            'automation', 'no-code', 'api', 'saas', 'mrr', 'revenue',
            'growth', 'seo', 'marketing', 'email', 'outreach',
            'content', 'creator', 'newsletter', 'social media'
        ]

    def _load_seen_ids(self) -> set:
        cache_file = CACHE_DIR / 'seen_ph.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                    return {k for k, v in data.items() if v > cutoff}
            except Exception as e:
                logger.warning(f"Failed to load seen IDs: {e}")
        return set()

    def _save_seen_ids(self):
        cache_file = CACHE_DIR / 'seen_ph.json'
        try:
            existing = {}
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    existing = json.load(f)

            now = datetime.now().isoformat()
            for product_id in self.seen_ids:
                if str(product_id) not in existing:
                    existing[str(product_id)] = now

            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            existing = {k: v for k, v in existing.items() if v > cutoff}

            with open(cache_file, 'w') as f:
                json.dump(existing, f)
        except Exception as e:
            logger.warning(f"Failed to save seen IDs: {e}")

    def fetch_products_api(self, days: int = 1) -> List[PHProduct]:
        """
        Fetch products using Product Hunt GraphQL API.
        Requires PRODUCTHUNT_API_TOKEN environment variable.
        """
        if not self.api_token:
            logger.info("No PRODUCTHUNT_API_TOKEN. Falling back to web scraping.")
            return []

        try:
            import requests

            self.rate_limiter.wait_if_needed()

            url = "https://api.producthunt.com/v2/api/graphql"
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }

            # GraphQL query for posts
            query = """
            query {
                posts(first: 50, order: VOTES) {
                    edges {
                        node {
                            id
                            name
                            tagline
                            description
                            url
                            slug
                            votesCount
                            commentsCount
                            featuredAt
                            topics {
                                edges {
                                    node {
                                        slug
                                    }
                                }
                            }
                            makers {
                                name
                            }
                        }
                    }
                }
            }
            """

            response = requests.post(url, json={"query": query}, headers=headers, timeout=15)

            if response.status_code != 200:
                logger.error(f"PH API failed: {response.status_code}")
                return []

            data = response.json()
            products = []

            for edge in data.get('data', {}).get('posts', {}).get('edges', []):
                node = edge.get('node', {})
                product_id = node.get('id', '')

                if product_id in self.seen_ids:
                    continue

                self.seen_ids.add(product_id)

                topics = [t['node']['slug'] for t in node.get('topics', {}).get('edges', [])]
                makers = [m['name'] for m in node.get('makers', [])]

                products.append(PHProduct(
                    id=product_id,
                    name=node.get('name', ''),
                    tagline=node.get('tagline', ''),
                    description=node.get('description', ''),
                    url=node.get('url', ''),
                    ph_url=f"https://www.producthunt.com/posts/{node.get('slug', '')}",
                    topics=topics,
                    votes_count=node.get('votesCount', 0),
                    comments_count=node.get('commentsCount', 0),
                    maker_names=makers,
                    featured=bool(node.get('featuredAt')),
                    launched_at=node.get('featuredAt', '')
                ))

            return products

        except ImportError:
            logger.error("requests library not installed")
            return []
        except Exception as e:
            logger.error(f"Error fetching from PH API: {e}")
            return []

    def fetch_products_web(self, days: int = 1) -> List[PHProduct]:
        """
        Fetch products by scraping Product Hunt homepage.
        Fallback when API is not available.
        """
        try:
            import requests
            from bs4 import BeautifulSoup

            self.rate_limiter.wait_if_needed()

            url = "https://www.producthunt.com/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                logger.error(f"Failed to fetch PH: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            products = []

            # PH uses dynamic rendering, but some data is in initial HTML
            # Look for product cards in the page
            for item in soup.select('[data-test="post-item"]')[:30]:
                try:
                    # Extract product info from HTML structure
                    name_elem = item.select_one('h3')
                    tagline_elem = item.select_one('p')
                    link_elem = item.select_one('a[href^="/posts/"]')

                    if not name_elem or not link_elem:
                        continue

                    product_id = link_elem.get('href', '').split('/')[-1]

                    if product_id in self.seen_ids:
                        continue

                    self.seen_ids.add(product_id)

                    # Get vote count if available
                    votes = 0
                    vote_elem = item.select_one('[data-test="vote-button"]')
                    if vote_elem:
                        try:
                            votes = int(vote_elem.text.strip().replace(',', ''))
                        except:
                            pass

                    products.append(PHProduct(
                        id=product_id,
                        name=name_elem.text.strip(),
                        tagline=tagline_elem.text.strip() if tagline_elem else '',
                        description='',
                        url='',
                        ph_url=f"https://www.producthunt.com{link_elem.get('href', '')}",
                        topics=[],
                        votes_count=votes,
                        comments_count=0,
                        maker_names=[],
                        featured=True,
                        launched_at=datetime.now().isoformat()
                    ))
                except Exception as e:
                    logger.debug(f"Failed to parse product: {e}")
                    continue

            return products

        except ImportError:
            logger.error("requests or bs4 not installed")
            return []
        except Exception as e:
            logger.error(f"Error scraping PH: {e}")
            return []

    def is_relevant(self, product: PHProduct) -> bool:
        """Check if a product is relevant to PRINTMAXX"""
        # Check topics
        if any(topic in self.relevant_topics for topic in product.topics):
            return True

        # Check keywords in name/tagline/description
        content = f"{product.name} {product.tagline} {product.description}".lower()
        if any(keyword in content for keyword in self.high_signal_keywords):
            return True

        # High vote products are always interesting
        if product.votes_count >= 200:
            return True

        return False

    def analyze_product_for_alpha(self, product: PHProduct) -> Optional[AlphaFinding]:
        """Analyze a Product Hunt product for alpha"""
        content = f"{product.name} {product.tagline} {product.description}".lower()

        # Categorize
        category = 'TOOL_ALPHA'  # Default for PH

        if any(kw in content for kw in ['app', 'mobile', 'ios', 'android']):
            category = 'APP_FACTORY'
        elif any(kw in content for kw in ['content', 'writing', 'social', 'creator']):
            category = 'CONTENT_FORMAT'
        elif any(kw in content for kw in ['email', 'outreach', 'sales', 'crm']):
            category = 'OUTBOUND'
        elif any(kw in content for kw in ['seo', 'marketing', 'growth', 'analytics']):
            category = 'GROWTH_HACK'
        elif any(kw in content for kw in ['revenue', 'monetize', 'pricing', 'subscription']):
            category = 'MONETIZATION'

        # Determine effort level (using the tool)
        effort_level = 'LOW'  # Most PH tools are easy to try

        # ROI potential based on votes and relevance
        roi_potential = 'MEDIUM'
        if product.votes_count >= 500:
            roi_potential = 'HIGHEST'
        elif product.votes_count >= 200:
            roi_potential = 'HIGH'

        alpha_id = f"ALPHPH{hashlib.md5(product.id.encode()).hexdigest()[:5].upper()}"

        description = f"{product.name}: {product.tagline}"
        if product.description:
            description += f" - {product.description[:300]}"
        if product.url:
            description += f" (Website: {product.url})"

        return AlphaFinding(
            alpha_id=alpha_id,
            source='Product Hunt',
            source_url=product.ph_url,
            category=category,
            title=f"{product.name}: {product.tagline[:80]}",
            description=description[:500],
            actionable_steps=f'1. Try {product.name} 2. Evaluate for workflow 3. Consider building competitor/niche version',
            effort_level=effort_level,
            roi_potential=roi_potential,
            risk_level='LOW',
            applies_to_niches='ALL',
            status='PENDING_REVIEW'
        )

    def scan_all(self, days: int = 1, dry_run: bool = False) -> List[AlphaFinding]:
        """Scan Product Hunt for alpha"""
        logger.info("Scanning Product Hunt...")

        # Try API first, then web scraping
        products = self.fetch_products_api(days)
        if not products:
            products = self.fetch_products_web(days)

        logger.info(f"  Found {len(products)} products to analyze")

        all_findings = []

        for product in products:
            if not self.is_relevant(product):
                continue

            finding = self.analyze_product_for_alpha(product)
            if finding:
                all_findings.append(finding)
                logger.info(f"  Found alpha: {product.name} ({product.votes_count} votes)")

        if not dry_run:
            self._save_seen_ids()

        logger.info(f"  Found {len(all_findings)} relevant products")
        return all_findings

    def save_findings(self, findings: List[AlphaFinding]) -> int:
        """Save findings to ALPHA_STAGING.csv"""
        if not findings:
            return 0

        existing_ids = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row['alpha_id'])

        new_findings = [f for f in findings if f.alpha_id not in existing_ids]

        if not new_findings:
            logger.info("No new findings to save")
            return 0

        file_exists = ALPHA_STAGING.exists()
        with open(ALPHA_STAGING, 'a', newline='') as f:
            fieldnames = [
                'alpha_id', 'source', 'source_url', 'category', 'title',
                'description', 'actionable_steps', 'effort_level', 'roi_potential',
                'risk_level', 'applies_to_niches', 'status', 'reviewed_date', 'reviewer_notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for finding in new_findings:
                writer.writerow(asdict(finding))

        logger.info(f"Saved {len(new_findings)} new findings")
        return len(new_findings)


def main():
    parser = argparse.ArgumentParser(description='Scan Product Hunt for alpha')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--days', type=int, default=1, help='Days of products to check')
    args = parser.parse_args()

    scanner = ProductHuntScanner()
    findings = scanner.scan_all(days=args.days, dry_run=args.dry_run)

    if args.dry_run:
        logger.info(f"DRY RUN: Would save {len(findings)} findings")
        for f in findings:
            print(f"  - [{f.category}] {f.title[:60]}...")
    else:
        saved = scanner.save_findings(findings)
        logger.info(f"Scan complete. Saved {saved} new findings.")

    return findings


if __name__ == '__main__':
    main()
