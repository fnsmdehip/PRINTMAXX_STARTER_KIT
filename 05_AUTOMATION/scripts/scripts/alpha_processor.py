#!/usr/bin/env python3
"""
Alpha Processor - Deduplication, Categorization, and Scoring
Takes raw findings from scrapers, processes them for human review.

Features:
- Deduplicates findings by URL and content similarity
- Categorizes into: tool, tactic, trend, competitor
- Calculates priority score based on engagement and relevance
- Formats output for ALPHA_STAGING.csv

Usage:
    processor = AlphaProcessor()
    processed = processor.process_findings(raw_findings)
    processor.save_to_staging(processed, output_path)
"""

import csv
import hashlib
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger('AlphaProcessor')

# Category keywords (from existing daily_alpha_extractor.py + expanded)
CATEGORY_KEYWORDS = {
    'APP_FACTORY': [
        'app', 'mobile', 'ios', 'android', 'flutter', 'react native',
        'install', 'download', 'mrr', 'arr', 'paywall', 'saas', 'subscription',
        'indie app', 'side project', 'ship', 'launched', 'build in public'
    ],
    'CONTENT_FORMAT': [
        'hook', 'format', 'template', 'thumbnail', 'views', 'viral',
        'algorithm', 'carousel', 'thread', 'reel', 'shorts', 'tiktok',
        'content structure', 'headline', 'caption', 'engagement'
    ],
    'OUTBOUND': [
        'cold email', 'outbound', 'deliverability', 'open rate', 'reply rate',
        'linkedin', 'apollo', 'instantly', 'email list', 'lead gen',
        'prospecting', 'b2b', 'sales', 'pipeline', 'booking rate'
    ],
    'GROWTH_HACK': [
        'growth', 'hack', 'organic', 'seo', 'traffic', 'distribution',
        'viral', 'ugc', 'clipper', 'influencer', 'affiliate', 'referral',
        'acquisition', 'cac', 'ltv', 'retention', 'churn'
    ],
    'TOOL_ALPHA': [
        'tool', 'software', 'api', 'automation', 'n8n', 'zapier', 'make',
        'workflow', 'cursor', 'lovable', 'ai tool', 'extension', 'plugin',
        'integration', 'no-code', 'low-code'
    ],
    'COMPLIANCE': [
        'ftc', 'disclosure', 'legal', 'compliance', 'terms', 'policy',
        'banned', 'terminated', 'copyright', 'trademark', 'gdpr', 'privacy'
    ],
    'NICHE_INSIGHT': [
        'niche', 'market', 'women', 'faith', 'fitness', 'opportunity',
        'underserved', 'demographic', 'target audience', 'persona', 'segment'
    ],
    'MONETIZATION': [
        'pricing', 'offer', 'upsell', 'funnel', 'conversion', 'revenue',
        'monetize', 'flash sale', 'paywall', 'subscription', 'ltv',
        'arpu', 'profit', 'margin', 'income'
    ],
    'COMPETITOR': [
        'competitor', 'alternative', 'vs', 'comparison', 'market share',
        'levelsio', 'tdinh', 'pieter levels', 'indie hacker'
    ],
    'TREND': [
        'trend', 'emerging', 'new', 'future', 'prediction', 'shift',
        '2026', 'next big', 'rising', 'growing'
    ]
}

# Signal quality keywords
HIGH_SIGNAL_INDICATORS = [
    # Specific numbers
    r'\$[\d,]+k?',      # Dollar amounts
    r'\d+%',            # Percentages
    r'\d+k followers',  # Follower counts
    r'\d+x',            # Multipliers
    r'\d+/mo',          # Monthly metrics
    r'\d+ sales',       # Sales counts
    r'mrr.*\$',         # MRR mentions
    r'arr.*\$',         # ARR mentions
]

LOW_SIGNAL_INDICATORS = [
    'believe in yourself',
    'mindset',
    'grateful',
    'blessed',
    'motivation',
    'inspire',
    'journey',
    'opportunities are insane',
    'passive income',
    'anyone can',
    'in just',
    'this one trick',
    'secret to',
    'you wont believe',
]

ACTIONABLE_WORDS = [
    'step', 'how to', "here's", 'do this', 'try this',
    'hack', 'strategy', 'tactic', 'playbook', 'framework',
    'guide', 'tutorial', 'breakdown', 'example', 'case study'
]


class AlphaProcessor:
    """Processes raw findings into structured alpha entries."""

    def __init__(self, dedup_threshold: float = 0.8):
        """
        Initialize processor.

        Args:
            dedup_threshold: Similarity threshold for deduplication (0-1)
        """
        self.dedup_threshold = dedup_threshold
        self._seen_urls = set()
        self._seen_hashes = set()

    def process_findings(self, findings: list[dict]) -> list[dict]:
        """
        Process raw findings from scrapers.

        Args:
            findings: List of raw finding dictionaries

        Returns:
            List of processed alpha entries ready for staging
        """
        processed = []

        for finding in findings:
            try:
                # Skip if duplicate
                if self._is_duplicate(finding):
                    logger.debug(f"Skipping duplicate: {finding.get('source_url', '')[:50]}")
                    continue

                # Categorize
                categories = self._categorize(finding.get('content', ''))

                # Score
                score_info = self._calculate_score(finding)

                # Skip low signal
                if score_info['signal'] == 'LOW':
                    logger.debug(f"Skipping low signal: {finding.get('content', '')[:50]}")
                    continue

                # Create alpha entry
                alpha_entry = self._create_alpha_entry(finding, categories, score_info)
                processed.append(alpha_entry)

                # Mark as seen
                self._mark_seen(finding)

            except Exception as e:
                logger.error(f"Error processing finding: {e}")
                continue

        logger.info(f"Processed {len(processed)} findings from {len(findings)} raw")
        return processed

    def _is_duplicate(self, finding: dict) -> bool:
        """Check if finding is a duplicate."""
        url = finding.get('source_url', '')
        if url and url in self._seen_urls:
            return True

        # Content hash check
        content = finding.get('content', '')
        if content:
            content_hash = self._hash_content(content)
            if content_hash in self._seen_hashes:
                return True

        return False

    def _mark_seen(self, finding: dict):
        """Mark finding as seen for deduplication."""
        url = finding.get('source_url', '')
        if url:
            self._seen_urls.add(url)

        content = finding.get('content', '')
        if content:
            self._seen_hashes.add(self._hash_content(content))

    @staticmethod
    def _hash_content(content: str) -> str:
        """Create hash of content for deduplication."""
        # Normalize content
        normalized = content.lower().strip()
        # Remove URLs
        normalized = re.sub(r'https?://\S+', '', normalized)
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        # Take first 500 chars for hash
        return hashlib.md5(normalized[:500].encode()).hexdigest()

    def _categorize(self, content: str) -> list[str]:
        """Categorize content into alpha categories."""
        content_lower = content.lower()
        categories = []

        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in content_lower for kw in keywords):
                categories.append(category)

        return categories if categories else ['GENERAL']

    def _calculate_score(self, finding: dict) -> dict:
        """
        Calculate signal quality and priority score.

        Returns:
            Dictionary with signal level, score, and reason
        """
        content = finding.get('content', '').lower()
        engagement = finding.get('engagement', {})

        # Check for high signal indicators
        has_numbers = any(
            re.search(pattern, content, re.IGNORECASE)
            for pattern in HIGH_SIGNAL_INDICATORS
        )

        # Check for actionable language
        has_actionable = any(word in content for word in ACTIONABLE_WORDS)

        # Check for noise
        is_noise = any(indicator in content for indicator in LOW_SIGNAL_INDICATORS)

        # Calculate engagement score
        engagement_score = self._engagement_score(engagement, finding.get('platform', ''))

        # Determine signal level
        if is_noise:
            return {
                'signal': 'LOW',
                'score': 0,
                'reason': 'Motivational/noise content'
            }

        if has_numbers and has_actionable:
            return {
                'signal': 'HIGHEST',
                'score': 100 + engagement_score,
                'reason': 'Specific numbers + actionable'
            }

        if has_numbers:
            return {
                'signal': 'HIGH',
                'score': 75 + engagement_score,
                'reason': 'Contains specific numbers'
            }

        if has_actionable:
            return {
                'signal': 'MEDIUM',
                'score': 50 + engagement_score,
                'reason': 'Actionable but no specifics'
            }

        # Default based on engagement
        if engagement_score > 50:
            return {
                'signal': 'MEDIUM',
                'score': engagement_score,
                'reason': 'High engagement'
            }

        return {
            'signal': 'LOW',
            'score': engagement_score,
            'reason': 'General content'
        }

    def _engagement_score(self, engagement: dict, platform: str) -> int:
        """Calculate engagement score based on platform metrics."""
        score = 0

        if platform == 'X':
            likes = engagement.get('likes', 0)
            retweets = engagement.get('retweets', 0)
            views = engagement.get('views', 0)

            # Weight engagement relative to typical ranges
            if likes > 100:
                score += 20
            if likes > 500:
                score += 20
            if retweets > 50:
                score += 15
            if views > 10000:
                score += 15

        elif platform == 'Reddit':
            upvotes = engagement.get('upvotes', 0)
            comments = engagement.get('comments', 0)

            if upvotes > 50:
                score += 20
            if upvotes > 200:
                score += 20
            if comments > 20:
                score += 15

        elif platform == 'HN':
            points = engagement.get('points', 0)
            comments = engagement.get('comments', 0)

            if points > 50:
                score += 25
            if points > 200:
                score += 25
            if comments > 50:
                score += 20

        return min(score, 70)  # Cap engagement contribution

    def _create_alpha_entry(
        self,
        finding: dict,
        categories: list[str],
        score_info: dict
    ) -> dict:
        """Create structured alpha entry for staging."""
        content = finding.get('content', '')

        # Generate alpha ID
        alpha_id = f"ALPHA_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(finding.get('source_url', '')) % 1000:03d}"

        # Create title from first 60 chars
        title = content[:60].replace('\n', ' ').strip()
        if len(content) > 60:
            title += "..."

        # Determine effort level based on actionability
        effort = 'MEDIUM'
        content_lower = content.lower()
        if 'step' in content_lower or 'how to' in content_lower:
            effort = 'LOW'  # Clear instructions
        elif 'build' in content_lower or 'create' in content_lower:
            effort = 'HIGH'  # Building required

        # Determine risk level
        risk = 'LOW'
        if any(word in content_lower for word in ['banned', 'terminated', 'risky', 'gray hat']):
            risk = 'MEDIUM'
        if any(word in content_lower for word in ['illegal', 'scam', 'fraud']):
            risk = 'HIGH'

        # Determine applicable niches
        niches = 'ALL'
        if 'fitness' in content_lower or 'workout' in content_lower or 'health' in content_lower:
            niches = 'Fitness'
        elif 'faith' in content_lower or 'pray' in content_lower or 'christian' in content_lower:
            niches = 'Faith'
        elif 'ai' in content_lower or 'automation' in content_lower or 'tech' in content_lower:
            niches = 'AI'

        return {
            'alpha_id': alpha_id,
            'source': finding.get('source', ''),
            'source_url': finding.get('source_url', ''),
            'category': '|'.join(categories),
            'title': title,
            'description': content[:500].replace('\n', ' '),
            'actionable_steps': '',  # Human fills this
            'effort_level': effort,
            'roi_potential': score_info['signal'],
            'risk_level': risk,
            'applies_to_niches': niches,
            'status': 'PENDING_REVIEW',
            'reviewed_date': '',
            'reviewer_notes': f"Auto-staged: {score_info['reason']}. Score: {score_info['score']}. Focus: {finding.get('focus_area', '')}"
        }

    def save_to_staging(self, entries: list[dict], output_path: Path):
        """
        Save processed entries to ALPHA_STAGING.csv.

        Args:
            entries: List of processed alpha entries
            output_path: Path to output CSV file
        """
        if not entries:
            logger.info("No entries to save")
            return

        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category', 'title',
            'description', 'actionable_steps', 'effort_level', 'roi_potential',
            'risk_level', 'applies_to_niches', 'status', 'reviewed_date', 'reviewer_notes'
        ]

        file_exists = output_path.exists()

        with open(output_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(entries)

        logger.info(f"Saved {len(entries)} entries to {output_path}")

    def load_existing_urls(self, staging_path: Path) -> set:
        """Load existing URLs from staging file for deduplication."""
        urls = set()

        if not staging_path.exists():
            return urls

        with open(staging_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('source_url', '')
                if url:
                    urls.add(url)

        self._seen_urls.update(urls)
        logger.info(f"Loaded {len(urls)} existing URLs for deduplication")
        return urls

    def get_category_stats(self, entries: list[dict]) -> dict:
        """Get category breakdown of processed entries."""
        stats = {}
        for entry in entries:
            categories = entry.get('category', '').split('|')
            for cat in categories:
                stats[cat] = stats.get(cat, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: -x[1]))

    def get_source_stats(self, entries: list[dict]) -> dict:
        """Get source breakdown of processed entries."""
        stats = {}
        for entry in entries:
            source = entry.get('source', 'Unknown')
            stats[source] = stats.get(source, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: -x[1]))


# Standalone test
def _test():
    """Test the alpha processor."""
    processor = AlphaProcessor()

    # Sample findings
    findings = [
        {
            'source': '@levelsio',
            'source_url': 'https://x.com/levelsio/status/123',
            'platform': 'X',
            'content': "Made $50k MRR with my side project. Here's exactly how to do it step by step: 1) Find a problem 2) Build MVP in a week 3) Launch on ProductHunt",
            'engagement': {'likes': 500, 'retweets': 100, 'views': 50000},
            'focus_area': 'Indie hacking'
        },
        {
            'source': 'r/SideProject',
            'source_url': 'https://reddit.com/r/SideProject/comments/abc123',
            'platform': 'Reddit',
            'content': "Launched my app yesterday, got 1000 downloads in 24 hours. The key was using TikTok for distribution.",
            'engagement': {'upvotes': 200, 'comments': 50},
            'focus_area': 'App launches'
        },
        {
            'source': '@motivationalGuru',
            'source_url': 'https://x.com/motivationalGuru/status/456',
            'platform': 'X',
            'content': "Believe in yourself! The opportunities are insane right now. Anyone can make passive income!",
            'engagement': {'likes': 1000, 'retweets': 200},
            'focus_area': 'Motivation'
        }
    ]

    processed = processor.process_findings(findings)

    print(f"\n=== Processed {len(processed)} findings ===")
    for entry in processed:
        print(f"\n[{entry['roi_potential']}] {entry['title']}")
        print(f"  Categories: {entry['category']}")
        print(f"  Source: {entry['source']}")

    print(f"\n=== Category Stats ===")
    print(processor.get_category_stats(processed))


if __name__ == '__main__':
    _test()
