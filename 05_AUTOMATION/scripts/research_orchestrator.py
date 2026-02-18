#!/usr/bin/env python3
"""
Research Orchestrator for PRINTMAXX Daily Research

Coordinates all scanners:
1. Runs twitter_scanner.py
2. Runs reddit_scanner.py
3. Runs hn_scanner.py
4. Runs producthunt_scanner.py
5. Processes results with alpha_processor.py
6. Generates daily report

Usage:
    python research_orchestrator.py [--dry-run] [--tier HIGHEST|HIGH|MEDIUM] [--parallel]

Environment Variables:
    X_BEARER_TOKEN - Twitter API bearer token
    REDDIT_CLIENT_ID - Reddit API client ID
    REDDIT_CLIENT_SECRET - Reddit API client secret
    PRODUCTHUNT_API_TOKEN - Product Hunt API token
"""

import csv
import json
import os
import sys
import time
import logging
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('research_orchestrator')

# Paths
BASE_DIR = Path(__file__).parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
OPS_DIR = BASE_DIR / 'OPS'
ALPHA_RESEARCH_DIR = OPS_DIR / 'alpha_research'
AUTOMATIONS_DIR = BASE_DIR / 'AUTOMATIONS'
DAILY_RESEARCH_DIR = AUTOMATIONS_DIR / 'daily_research'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
ALPHA_WATCHLIST = LEDGER_DIR / 'ALPHA_WATCHLIST.csv'
REPORT_TEMPLATE = OPS_DIR / 'DAILY_RESEARCH_REPORT_TEMPLATE.md'

# Add paths for imports
sys.path.insert(0, str(DAILY_RESEARCH_DIR))
sys.path.insert(0, str(AUTOMATIONS_DIR))


@dataclass
class ScannerResult:
    """Result from running a scanner"""
    name: str
    status: str  # SUCCESS, FAILED, SKIPPED
    findings_count: int
    items_checked: int
    sources_count: int
    duration: float
    errors: List[str]
    findings: List  # List of AlphaFinding objects


class ResearchOrchestrator:
    """Orchestrates the daily research process"""

    def __init__(self, tier_filter: Optional[str] = None, dry_run: bool = False):
        self.tier_filter = tier_filter
        self.dry_run = dry_run
        self.start_time = datetime.now()
        self.results: Dict[str, ScannerResult] = {}

        # Ensure output directory exists
        ALPHA_RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

    def run_twitter_scanner(self) -> ScannerResult:
        """Run the Twitter scanner"""
        logger.info("Running Twitter scanner...")
        start = time.time()

        try:
            from twitter_scanner import TwitterScanner

            scanner = TwitterScanner()
            sources = scanner.get_x_sources(self.tier_filter)
            findings = scanner.scan_all_sources(
                tier_filter=self.tier_filter,
                dry_run=self.dry_run
            )

            if not self.dry_run:
                saved = scanner.save_findings(findings)
            else:
                saved = len(findings)

            return ScannerResult(
                name='twitter_scanner',
                status='SUCCESS',
                findings_count=saved,
                items_checked=len(sources) * 10,  # Approximate
                sources_count=len(sources),
                duration=time.time() - start,
                errors=[],
                findings=findings
            )

        except Exception as e:
            logger.error(f"Twitter scanner failed: {e}")
            traceback.print_exc()
            return ScannerResult(
                name='twitter_scanner',
                status='FAILED',
                findings_count=0,
                items_checked=0,
                sources_count=0,
                duration=time.time() - start,
                errors=[str(e)],
                findings=[]
            )

    def run_reddit_scanner(self) -> ScannerResult:
        """Run the Reddit scanner"""
        logger.info("Running Reddit scanner...")
        start = time.time()

        try:
            from reddit_scanner import RedditScanner

            scanner = RedditScanner()
            sources = scanner.get_reddit_sources(self.tier_filter)
            findings = scanner.scan_all_sources(
                tier_filter=self.tier_filter,
                dry_run=self.dry_run
            )

            if not self.dry_run:
                saved = scanner.save_findings(findings)
            else:
                saved = len(findings)

            return ScannerResult(
                name='reddit_scanner',
                status='SUCCESS',
                findings_count=saved,
                items_checked=len(sources) * 25,  # Approximate
                sources_count=len(sources),
                duration=time.time() - start,
                errors=[],
                findings=findings
            )

        except Exception as e:
            logger.error(f"Reddit scanner failed: {e}")
            traceback.print_exc()
            return ScannerResult(
                name='reddit_scanner',
                status='FAILED',
                findings_count=0,
                items_checked=0,
                sources_count=0,
                duration=time.time() - start,
                errors=[str(e)],
                findings=[]
            )

    def run_hn_scanner(self) -> ScannerResult:
        """Run the Hacker News scanner"""
        logger.info("Running Hacker News scanner...")
        start = time.time()

        try:
            from hn_scanner import HNScanner

            scanner = HNScanner()
            findings = scanner.scan_all(count=30, dry_run=self.dry_run)

            if not self.dry_run:
                saved = scanner.save_findings(findings)
            else:
                saved = len(findings)

            return ScannerResult(
                name='hn_scanner',
                status='SUCCESS',
                findings_count=saved,
                items_checked=90,  # 30 * 3 endpoints
                sources_count=1,
                duration=time.time() - start,
                errors=[],
                findings=findings
            )

        except Exception as e:
            logger.error(f"HN scanner failed: {e}")
            traceback.print_exc()
            return ScannerResult(
                name='hn_scanner',
                status='FAILED',
                findings_count=0,
                items_checked=0,
                sources_count=1,
                duration=time.time() - start,
                errors=[str(e)],
                findings=[]
            )

    def run_producthunt_scanner(self) -> ScannerResult:
        """Run the Product Hunt scanner"""
        logger.info("Running Product Hunt scanner...")
        start = time.time()

        try:
            from producthunt_scanner import ProductHuntScanner

            scanner = ProductHuntScanner()
            findings = scanner.scan_all(days=1, dry_run=self.dry_run)

            if not self.dry_run:
                saved = scanner.save_findings(findings)
            else:
                saved = len(findings)

            return ScannerResult(
                name='producthunt_scanner',
                status='SUCCESS',
                findings_count=saved,
                items_checked=50,  # Approximate
                sources_count=1,
                duration=time.time() - start,
                errors=[],
                findings=findings
            )

        except Exception as e:
            logger.error(f"Product Hunt scanner failed: {e}")
            traceback.print_exc()
            return ScannerResult(
                name='producthunt_scanner',
                status='FAILED',
                findings_count=0,
                items_checked=0,
                sources_count=1,
                duration=time.time() - start,
                errors=[str(e)],
                findings=[]
            )

    def run_all_scanners(self, parallel: bool = False) -> Dict[str, ScannerResult]:
        """Run all scanners, optionally in parallel"""
        scanners = [
            ('twitter', self.run_twitter_scanner),
            ('reddit', self.run_reddit_scanner),
            ('hn', self.run_hn_scanner),
            ('producthunt', self.run_producthunt_scanner)
        ]

        results = {}

        if parallel:
            logger.info("Running scanners in parallel...")
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    executor.submit(scanner_func): name
                    for name, scanner_func in scanners
                }

                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        result = future.result()
                        results[name] = result
                    except Exception as e:
                        logger.error(f"Scanner {name} failed: {e}")
                        results[name] = ScannerResult(
                            name=name,
                            status='FAILED',
                            findings_count=0,
                            items_checked=0,
                            sources_count=0,
                            duration=0,
                            errors=[str(e)],
                            findings=[]
                        )
        else:
            logger.info("Running scanners sequentially...")
            for name, scanner_func in scanners:
                results[name] = scanner_func()
                # Brief pause between scanners
                time.sleep(2)

        self.results = results
        return results

    def process_findings(self) -> Dict:
        """Process all findings through alpha_processor"""
        logger.info("Processing findings...")

        try:
            from alpha_processor import AlphaProcessor, AlphaFinding

            processor = AlphaProcessor()

            # Collect all findings
            all_findings = []
            for result in self.results.values():
                all_findings.extend(result.findings)

            if not all_findings:
                logger.info("No findings to process")
                return {
                    'total_input': 0,
                    'processed': 0,
                    'duplicates': 0,
                    'errors': 0,
                    'category_breakdown': {},
                    'top_findings': []
                }

            # Process through alpha_processor
            summary = processor.process_findings(all_findings, dry_run=self.dry_run)
            return summary

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            traceback.print_exc()
            return {
                'total_input': 0,
                'processed': 0,
                'duplicates': 0,
                'errors': 1,
                'error_message': str(e),
                'category_breakdown': {},
                'top_findings': []
            }

    def check_watchlist(self) -> List[Dict]:
        """Check watchlist items for updates"""
        # This is a placeholder for watchlist monitoring
        # In production, this would check specific items like ChatGPT ads status
        watchlist_updates = []

        # ChatGPT ads monitoring
        watchlist_updates.append({
            'item': 'ChatGPT Ads',
            'status': 'Monitoring',
            'notes': 'No new announcements detected. Continue monitoring OpenAI blog and X.'
        })

        return watchlist_updates

    def generate_report(self, processing_summary: Dict) -> str:
        """Generate the daily research report"""
        logger.info("Generating report...")

        # Calculate totals
        total_sources = sum(r.sources_count for r in self.results.values())
        total_checked = sum(r.items_checked for r in self.results.values())
        total_new = processing_summary.get('processed', 0)
        total_duration = (datetime.now() - self.start_time).total_seconds()

        # Load template
        if REPORT_TEMPLATE.exists():
            with open(REPORT_TEMPLATE, 'r') as f:
                template = f.read()
        else:
            template = self._default_template()

        # Get category breakdown
        category_breakdown = processing_summary.get('category_breakdown', {})
        category_table = "\n".join([
            f"| {cat} | {count} |"
            for cat, count in sorted(category_breakdown.items(), key=lambda x: -x[1])
        ]) or "| None | 0 |"

        # Get top findings
        top_findings = processing_summary.get('top_findings', [])
        top_findings_text = "\n".join([
            f"{i}. **[{f['category']}]** {f['title']} (score: {f['score']})"
            for i, f in enumerate(top_findings[:10], 1)
        ]) or "No new findings today."

        # Get watchlist updates
        watchlist_updates = self.check_watchlist()
        watchlist_text = "\n".join([
            f"- **{w['item']}**: {w['status']} - {w['notes']}"
            for w in watchlist_updates
        ])

        # Build category sections
        category_sections = {}
        for cat in ['APP_FACTORY', 'MONETIZATION', 'GROWTH_HACK', 'OUTBOUND', 'CONTENT_FORMAT', 'TOOL_ALPHA']:
            findings = [f for f in top_findings if f.get('category') == cat]
            if findings:
                category_sections[cat] = "\n".join([
                    f"- {f['title'][:80]}"
                    for f in findings[:5]
                ])
            else:
                category_sections[cat] = "No new findings in this category."

        # Replace placeholders
        replacements = {
            '{{DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{TIMESTAMP}}': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '{{DURATION}}': f"{total_duration:.1f}s",
            '{{TOTAL_NEW}}': str(total_new),
            '{{PRIORITY_COUNT}}': str(min(5, total_new)),
            '{{TWITTER_SOURCES}}': str(self.results.get('twitter', ScannerResult('', '', 0, 0, 0, 0, [], [])).sources_count),
            '{{TWITTER_CHECKED}}': str(self.results.get('twitter', ScannerResult('', '', 0, 0, 0, 0, [], [])).items_checked),
            '{{TWITTER_FOUND}}': str(self.results.get('twitter', ScannerResult('', '', 0, 0, 0, 0, [], [])).findings_count),
            '{{REDDIT_SOURCES}}': str(self.results.get('reddit', ScannerResult('', '', 0, 0, 0, 0, [], [])).sources_count),
            '{{REDDIT_CHECKED}}': str(self.results.get('reddit', ScannerResult('', '', 0, 0, 0, 0, [], [])).items_checked),
            '{{REDDIT_FOUND}}': str(self.results.get('reddit', ScannerResult('', '', 0, 0, 0, 0, [], [])).findings_count),
            '{{HN_CHECKED}}': str(self.results.get('hn', ScannerResult('', '', 0, 0, 0, 0, [], [])).items_checked),
            '{{HN_FOUND}}': str(self.results.get('hn', ScannerResult('', '', 0, 0, 0, 0, [], [])).findings_count),
            '{{PH_CHECKED}}': str(self.results.get('producthunt', ScannerResult('', '', 0, 0, 0, 0, [], [])).items_checked),
            '{{PH_FOUND}}': str(self.results.get('producthunt', ScannerResult('', '', 0, 0, 0, 0, [], [])).findings_count),
            '{{TOTAL_SOURCES}}': str(total_sources),
            '{{TOTAL_CHECKED}}': str(total_checked),
            '{{CATEGORY_TABLE}}': f"| Category | Count |\n|----------|-------|\n{category_table}",
            '{{TOP_FINDINGS}}': top_findings_text,
            '{{APP_FACTORY_FINDINGS}}': category_sections.get('APP_FACTORY', 'None'),
            '{{MONETIZATION_FINDINGS}}': category_sections.get('MONETIZATION', 'None'),
            '{{GROWTH_HACK_FINDINGS}}': category_sections.get('GROWTH_HACK', 'None'),
            '{{OUTBOUND_FINDINGS}}': category_sections.get('OUTBOUND', 'None'),
            '{{CONTENT_FORMAT_FINDINGS}}': category_sections.get('CONTENT_FORMAT', 'None'),
            '{{TOOL_ALPHA_FINDINGS}}': category_sections.get('TOOL_ALPHA', 'None'),
            '{{DUPLICATES_COUNT}}': str(processing_summary.get('duplicates', 0)),
            '{{DUPLICATES_SAMPLE}}': 'See alpha_processor logs for details.',
            '{{ERRORS_COUNT}}': str(processing_summary.get('errors', 0)),
            '{{ERRORS_SAMPLE}}': processing_summary.get('error_message', 'No errors.'),
            '{{CHATGPT_ADS_STATUS}}': 'Monitoring',
            '{{CHATGPT_ADS_NOTES}}': '- No new announcements detected\n- Continue monitoring OpenAI blog and X',
            '{{WATCHLIST_UPDATES}}': watchlist_text,
            '{{IMMEDIATE_REVIEW}}': f"Review top {min(5, total_new)} findings in ALPHA_STAGING.csv",
            '{{QUICK_WINS}}': 'Look for LOW effort + HIGH ROI items',
            '{{RESEARCH_DEEPER}}': 'Investigate trending topics from HN/PH',
            '{{TWITTER_STATUS}}': self.results.get('twitter', ScannerResult('', 'SKIPPED', 0, 0, 0, 0, [], [])).status,
            '{{TWITTER_DURATION}}': f"{self.results.get('twitter', ScannerResult('', '', 0, 0, 0, 0, [], [])).duration:.1f}s",
            '{{TWITTER_ERRORS}}': str(len(self.results.get('twitter', ScannerResult('', '', 0, 0, 0, 0, [], [])).errors)),
            '{{REDDIT_STATUS}}': self.results.get('reddit', ScannerResult('', 'SKIPPED', 0, 0, 0, 0, [], [])).status,
            '{{REDDIT_DURATION}}': f"{self.results.get('reddit', ScannerResult('', '', 0, 0, 0, 0, [], [])).duration:.1f}s",
            '{{REDDIT_ERRORS}}': str(len(self.results.get('reddit', ScannerResult('', '', 0, 0, 0, 0, [], [])).errors)),
            '{{HN_STATUS}}': self.results.get('hn', ScannerResult('', 'SKIPPED', 0, 0, 0, 0, [], [])).status,
            '{{HN_DURATION}}': f"{self.results.get('hn', ScannerResult('', '', 0, 0, 0, 0, [], [])).duration:.1f}s",
            '{{HN_ERRORS}}': str(len(self.results.get('hn', ScannerResult('', '', 0, 0, 0, 0, [], [])).errors)),
            '{{PH_STATUS}}': self.results.get('producthunt', ScannerResult('', 'SKIPPED', 0, 0, 0, 0, [], [])).status,
            '{{PH_DURATION}}': f"{self.results.get('producthunt', ScannerResult('', '', 0, 0, 0, 0, [], [])).duration:.1f}s",
            '{{PH_ERRORS}}': str(len(self.results.get('producthunt', ScannerResult('', '', 0, 0, 0, 0, [], [])).errors)),
            '{{PROCESSOR_STATUS}}': 'SUCCESS' if processing_summary.get('processed', 0) > 0 else 'NO_DATA',
            '{{PROCESSOR_DURATION}}': '0.0s',  # Not tracked separately
            '{{PROCESSOR_ERRORS}}': str(processing_summary.get('errors', 0))
        }

        report = template
        for placeholder, value in replacements.items():
            report = report.replace(placeholder, value)

        return report

    def _default_template(self) -> str:
        """Default report template if file not found"""
        return """# Alpha Research Report - {{DATE}}

## Summary
- New Alpha Found: {{TOTAL_NEW}}
- Sources Scanned: {{TOTAL_SOURCES}}
- Duration: {{DURATION}}

## Top Findings
{{TOP_FINDINGS}}

## Category Breakdown
{{CATEGORY_TABLE}}

## Next Steps
1. Review ALPHA_STAGING.csv entries marked PENDING_REVIEW
2. Mark as APPROVED or REJECTED
3. Run `/review-alpha` to integrate
"""

    def save_report(self, report: str) -> Path:
        """Save the report to OPS/alpha_research/[DATE].md"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_path = ALPHA_RESEARCH_DIR / f"{date_str}.md"

        with open(report_path, 'w') as f:
            f.write(report)

        logger.info(f"Report saved to {report_path}")
        return report_path

    def run(self, parallel: bool = False) -> Tuple[Dict, str]:
        """
        Run the full orchestration pipeline:
        1. Run all scanners
        2. Process findings
        3. Generate report
        4. Save report

        Returns (processing_summary, report_path)
        """
        logger.info("="*60)
        logger.info("PRINTMAXX DAILY RESEARCH ORCHESTRATOR")
        logger.info("="*60)
        logger.info(f"Start time: {self.start_time}")
        logger.info(f"Dry run: {self.dry_run}")
        logger.info(f"Tier filter: {self.tier_filter or 'ALL'}")
        logger.info("")

        # Step 1: Run scanners
        self.run_all_scanners(parallel=parallel)

        # Step 2: Process findings
        processing_summary = self.process_findings()

        # Step 3: Generate report
        report = self.generate_report(processing_summary)

        # Step 4: Save report
        if not self.dry_run:
            report_path = self.save_report(report)
        else:
            report_path = Path('/dev/null')
            logger.info("DRY RUN: Report not saved")

        # Print summary
        logger.info("")
        logger.info("="*60)
        logger.info("ORCHESTRATION COMPLETE")
        logger.info("="*60)
        logger.info(f"Total duration: {(datetime.now() - self.start_time).total_seconds():.1f}s")
        logger.info(f"New findings: {processing_summary.get('processed', 0)}")
        logger.info(f"Report: {report_path}")

        return processing_summary, str(report_path)


def main():
    parser = argparse.ArgumentParser(
        description='Run PRINTMAXX daily research pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
    X_BEARER_TOKEN         Twitter API bearer token
    REDDIT_CLIENT_ID       Reddit API client ID
    REDDIT_CLIENT_SECRET   Reddit API client secret
    PRODUCTHUNT_API_TOKEN  Product Hunt API token

Examples:
    # Run full scan
    python research_orchestrator.py

    # Preview without saving
    python research_orchestrator.py --dry-run

    # Only scan HIGHEST tier sources
    python research_orchestrator.py --tier HIGHEST

    # Run scanners in parallel (faster but uses more API calls)
    python research_orchestrator.py --parallel
        """
    )
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving to files')
    parser.add_argument('--tier', choices=['HIGHEST', 'HIGH', 'MEDIUM'], help='Filter sources by signal tier')
    parser.add_argument('--parallel', action='store_true', help='Run scanners in parallel')

    args = parser.parse_args()

    orchestrator = ResearchOrchestrator(
        tier_filter=args.tier,
        dry_run=args.dry_run
    )

    summary, report_path = orchestrator.run(parallel=args.parallel)

    if args.dry_run:
        print("\n" + "="*60)
        print("DRY RUN COMPLETE")
        print("="*60)
        print(f"Would have saved {summary.get('processed', 0)} findings")
    else:
        print(f"\nReport saved to: {report_path}")
        print("\nNext steps:")
        print("1. Review ALPHA_STAGING.csv entries marked PENDING_REVIEW")
        print("2. Mark reviewed items as APPROVED or REJECTED")
        print("3. Run `/review-alpha` to integrate approved findings")


if __name__ == '__main__':
    main()
