#!/usr/bin/env python3
"""
Alpha Processor for PRINTMAXX Daily Research

Processes findings from all scanners:
- Deduplicates against existing ALPHA_STAGING
- Scores by actionability
- Assigns priority
- Outputs to ALPHA_STAGING.csv

Usage:
    python alpha_processor.py [--dry-run]
"""

import csv
import json
import os
import sys
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import argparse
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('alpha_processor')

# Paths
BASE_DIR = Path(__file__).parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'


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

    def to_dict(self) -> dict:
        return asdict(self)


class AlphaProcessor:
    """Processes and scores alpha findings"""

    def __init__(self):
        self.existing_findings = self._load_existing()
        self.existing_urls = {f['source_url'] for f in self.existing_findings}
        self.existing_titles = {self._normalize_title(f['title']) for f in self.existing_findings}

        # Scoring weights
        self.category_weights = {
            'APP_FACTORY': 1.2,      # High priority - build and ship
            'MONETIZATION': 1.3,     # Highest - direct revenue
            'GROWTH_HACK': 1.1,
            'OUTBOUND': 1.0,
            'CONTENT_FORMAT': 1.0,
            'TOOL_ALPHA': 0.9,
            'ENGAGEMENT_FARM': 0.7,  # Lower priority
            'COMPLIANCE': 1.1        # Important but not exciting
        }

        self.effort_weights = {
            'LOW': 1.5,    # Prefer quick wins
            'MEDIUM': 1.0,
            'HIGH': 0.6    # Penalize high effort
        }

        self.roi_weights = {
            'HIGHEST': 2.0,
            'HIGH': 1.5,
            'MEDIUM': 1.0,
            'LOW': 0.5
        }

        self.risk_weights = {
            'LOW': 1.0,
            'MEDIUM': 0.8,
            'HIGH': 0.5
        }

    def _load_existing(self) -> List[dict]:
        """Load existing findings from ALPHA_STAGING.csv"""
        if not ALPHA_STAGING.exists():
            return []

        findings = []
        with open(ALPHA_STAGING, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                findings.append(row)

        return findings

    def _normalize_title(self, title: str) -> str:
        """Normalize title for comparison"""
        # Remove special chars, lowercase, remove extra spaces
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = ' '.join(normalized.split())
        return normalized

    def _generate_content_hash(self, finding: AlphaFinding) -> str:
        """Generate a hash of the finding content for deduplication"""
        content = f"{finding.source_url}|{self._normalize_title(finding.title)}"
        return hashlib.md5(content.encode()).hexdigest()

    def is_duplicate(self, finding: AlphaFinding) -> Tuple[bool, str]:
        """
        Check if finding is a duplicate.
        Returns (is_duplicate, reason)
        """
        # Check URL match
        if finding.source_url in self.existing_urls:
            return True, 'URL already exists'

        # Check similar title
        normalized = self._normalize_title(finding.title)
        for existing_title in self.existing_titles:
            # Use simple similarity check
            if self._title_similarity(normalized, existing_title) > 0.8:
                return True, f'Similar title exists: {existing_title[:50]}'

        return False, ''

    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate simple title similarity (Jaccard index on words)"""
        words1 = set(title1.split())
        words2 = set(title2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def score_finding(self, finding: AlphaFinding) -> float:
        """
        Calculate an actionability score for a finding.
        Higher score = more actionable and valuable.
        """
        base_score = 10.0

        # Apply weights
        category_mult = self.category_weights.get(finding.category, 1.0)
        effort_mult = self.effort_weights.get(finding.effort_level, 1.0)
        roi_mult = self.roi_weights.get(finding.roi_potential, 1.0)
        risk_mult = self.risk_weights.get(finding.risk_level, 1.0)

        score = base_score * category_mult * effort_mult * roi_mult * risk_mult

        # Bonus for specific numbers in description
        if re.search(r'\$\d+|\d+%|\d+k|\d+K|\d+m|\d+M', finding.description):
            score *= 1.2  # 20% bonus for concrete numbers

        # Bonus for actionable steps
        if finding.actionable_steps and len(finding.actionable_steps) > 50:
            score *= 1.1  # 10% bonus for detailed steps

        # Bonus for multi-niche applicability
        if 'ALL' in finding.applies_to_niches:
            score *= 1.1

        return round(score, 2)

    def categorize_finding(self, finding: AlphaFinding) -> str:
        """
        Attempt to better categorize a finding based on content.
        Returns improved category if found.
        """
        content = f"{finding.title} {finding.description}".lower()

        # Category detection rules
        rules = [
            ('APP_FACTORY', ['app ', 'mobile', 'ios', 'android', 'react native', 'flutter', 'download', 'install']),
            ('MONETIZATION', ['revenue', 'mrr', 'arr', '$', 'pricing', 'monetiz', 'subscription', 'paywall']),
            ('OUTBOUND', ['cold email', 'outreach', 'reply rate', 'deliverability', 'lead gen', 'prospect']),
            ('CONTENT_FORMAT', ['viral', 'views', 'hook', 'tiktok', 'youtube', 'content', 'video']),
            ('GROWTH_HACK', ['seo', 'traffic', 'growth', 'acquisition', 'conversion', 'marketing']),
            ('TOOL_ALPHA', ['tool', 'api', 'service', 'platform', 'software']),
            ('COMPLIANCE', ['ftc', 'compliance', 'legal', 'disclosure', 'gdpr', 'regulation'])
        ]

        for category, keywords in rules:
            if any(kw in content for kw in keywords):
                return category

        return finding.category  # Keep original

    def determine_niches(self, finding: AlphaFinding) -> str:
        """
        Determine which niches the finding applies to.
        Returns comma-separated niche list.
        """
        content = f"{finding.title} {finding.description}".lower()

        niches = []

        # Niche detection rules
        if any(kw in content for kw in ['faith', 'prayer', 'church', 'christian', 'bible', 'religious', 'spiritual']):
            niches.append('Faith')
        if any(kw in content for kw in ['fitness', 'workout', 'exercise', 'gym', 'health', 'wellness', 'diet']):
            niches.append('Fitness')
        if any(kw in content for kw in ['ai', 'automation', 'chatgpt', 'claude', 'llm', 'machine learning']):
            niches.append('AI')

        # If no specific niche found, it applies to all
        if not niches:
            return 'ALL'

        return ','.join(niches)

    def enrich_finding(self, finding: AlphaFinding) -> AlphaFinding:
        """
        Enrich a finding with better categorization and metadata.
        """
        # Improve categorization
        finding.category = self.categorize_finding(finding)

        # Determine applicable niches
        finding.applies_to_niches = self.determine_niches(finding)

        # Clean up description
        finding.description = finding.description.strip()[:500]

        # Ensure actionable steps
        if not finding.actionable_steps or finding.actionable_steps == 'Review and extract specific steps from source':
            finding.actionable_steps = self._generate_actionable_steps(finding)

        return finding

    def _generate_actionable_steps(self, finding: AlphaFinding) -> str:
        """Generate basic actionable steps based on category"""
        templates = {
            'APP_FACTORY': '1. Research target audience 2. Build MVP 3. Test with real users 4. Launch on relevant platforms',
            'MONETIZATION': '1. Analyze revenue model 2. Calculate unit economics 3. Test pricing 4. Implement and track',
            'OUTBOUND': '1. Build target list 2. Craft personalized outreach 3. Test different angles 4. Track and optimize',
            'CONTENT_FORMAT': '1. Study winning examples 2. Adapt for your niche 3. Create test content 4. Distribute and measure',
            'GROWTH_HACK': '1. Validate the tactic 2. Set up tracking 3. Run small test 4. Scale if works',
            'TOOL_ALPHA': '1. Sign up and test 2. Evaluate for your workflow 3. Calculate ROI 4. Integrate or build alternative',
            'COMPLIANCE': '1. Review requirements 2. Audit current state 3. Implement changes 4. Document compliance'
        }
        return templates.get(finding.category, 'Review source and extract specific implementation steps')

    def process_findings(self, findings: List[AlphaFinding], dry_run: bool = False) -> Dict:
        """
        Process a list of findings:
        - Deduplicate
        - Enrich
        - Score
        - Sort by priority

        Returns processing summary.
        """
        logger.info(f"Processing {len(findings)} findings...")

        processed = []
        duplicates = []
        errors = []

        for finding in findings:
            try:
                # Check for duplicates
                is_dup, reason = self.is_duplicate(finding)
                if is_dup:
                    duplicates.append({'finding': finding.title[:50], 'reason': reason})
                    continue

                # Enrich the finding
                enriched = self.enrich_finding(finding)

                # Score it
                score = self.score_finding(enriched)

                processed.append({
                    'finding': enriched,
                    'score': score
                })

                # Add to tracking sets
                self.existing_urls.add(enriched.source_url)
                self.existing_titles.add(self._normalize_title(enriched.title))

            except Exception as e:
                errors.append({'finding': finding.title[:50], 'error': str(e)})
                logger.error(f"Error processing {finding.title[:50]}: {e}")

        # Sort by score (highest first)
        processed.sort(key=lambda x: x['score'], reverse=True)

        # Build summary
        summary = {
            'total_input': len(findings),
            'processed': len(processed),
            'duplicates': len(duplicates),
            'errors': len(errors),
            'duplicate_details': duplicates[:10],  # First 10
            'error_details': errors[:10],
            'top_findings': [{
                'title': p['finding'].title[:60],
                'category': p['finding'].category,
                'score': p['score']
            } for p in processed[:10]],
            'category_breakdown': self._count_categories([p['finding'] for p in processed])
        }

        # Save if not dry run
        if not dry_run and processed:
            saved = self.save_findings([p['finding'] for p in processed])
            summary['saved'] = saved

        return summary

    def _count_categories(self, findings: List[AlphaFinding]) -> Dict[str, int]:
        """Count findings by category"""
        counts = {}
        for f in findings:
            counts[f.category] = counts.get(f.category, 0) + 1
        return counts

    def save_findings(self, findings: List[AlphaFinding]) -> int:
        """Save findings to ALPHA_STAGING.csv"""
        if not findings:
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

            for finding in findings:
                writer.writerow(finding.to_dict())

        logger.info(f"Saved {len(findings)} findings to ALPHA_STAGING.csv")
        return len(findings)


def load_findings_from_scanners() -> List[AlphaFinding]:
    """
    Load findings from scanner output files.
    This function can be called by the orchestrator.
    """
    # Import scanners
    sys.path.insert(0, str(BASE_DIR / 'AUTOMATIONS' / 'daily_research'))

    findings = []

    try:
        from twitter_scanner import TwitterScanner
        scanner = TwitterScanner()
        twitter_findings = scanner.scan_all_sources(dry_run=True)
        findings.extend(twitter_findings)
        logger.info(f"Loaded {len(twitter_findings)} from Twitter scanner")
    except Exception as e:
        logger.warning(f"Twitter scanner failed: {e}")

    try:
        from reddit_scanner import RedditScanner
        scanner = RedditScanner()
        reddit_findings = scanner.scan_all_sources(dry_run=True)
        findings.extend(reddit_findings)
        logger.info(f"Loaded {len(reddit_findings)} from Reddit scanner")
    except Exception as e:
        logger.warning(f"Reddit scanner failed: {e}")

    try:
        from hn_scanner import HNScanner
        scanner = HNScanner()
        hn_findings = scanner.scan_all(dry_run=True)
        findings.extend(hn_findings)
        logger.info(f"Loaded {len(hn_findings)} from HN scanner")
    except Exception as e:
        logger.warning(f"HN scanner failed: {e}")

    try:
        from producthunt_scanner import ProductHuntScanner
        scanner = ProductHuntScanner()
        ph_findings = scanner.scan_all(dry_run=True)
        findings.extend(ph_findings)
        logger.info(f"Loaded {len(ph_findings)} from Product Hunt scanner")
    except Exception as e:
        logger.warning(f"Product Hunt scanner failed: {e}")

    return findings


def main():
    parser = argparse.ArgumentParser(description='Process alpha findings')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--from-file', type=str, help='Load findings from JSON file instead of scanners')
    args = parser.parse_args()

    processor = AlphaProcessor()

    if args.from_file:
        # Load from file
        with open(args.from_file, 'r') as f:
            data = json.load(f)
            findings = [AlphaFinding(**d) for d in data]
    else:
        # Load from scanners
        findings = load_findings_from_scanners()

    if not findings:
        logger.info("No findings to process")
        return

    summary = processor.process_findings(findings, dry_run=args.dry_run)

    # Print summary
    print("\n" + "="*60)
    print("ALPHA PROCESSING SUMMARY")
    print("="*60)
    print(f"Total input: {summary['total_input']}")
    print(f"Processed: {summary['processed']}")
    print(f"Duplicates: {summary['duplicates']}")
    print(f"Errors: {summary['errors']}")

    if summary.get('saved'):
        print(f"Saved: {summary['saved']}")

    print("\nCategory Breakdown:")
    for cat, count in sorted(summary['category_breakdown'].items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    print("\nTop Findings (by score):")
    for i, f in enumerate(summary['top_findings'], 1):
        print(f"  {i}. [{f['category']}] {f['title']} (score: {f['score']})")

    if summary['duplicate_details']:
        print(f"\nDuplicates skipped ({len(summary['duplicate_details'])} shown):")
        for d in summary['duplicate_details'][:5]:
            print(f"  - {d['finding']}: {d['reason']}")


if __name__ == '__main__':
    main()
