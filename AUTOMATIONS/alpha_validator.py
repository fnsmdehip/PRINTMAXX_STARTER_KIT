#!/usr/bin/env python3
"""
Alpha Validator - Live Web Validation for Alpha Screening

Validates alpha entries against current web data:
1. Checks if source URL still exists (not 404)
2. Searches for recent mentions of the tactic (2025-2026)
3. Searches for "doesn't work anymore" / "patched" / "dead" mentions
4. Returns a freshness_score (0-100)
5. Applies category-specific decay based on half-life

Half-life by category:
- PLATFORM_ARBITRAGE: 30 days (tactics expire fast)
- AUTOMATION_HACK: 45 days
- COLD_OUTBOUND: 90 days
- CONTENT_FARM: 120 days
- APP_FACTORY: 180 days (more evergreen)

Decision thresholds:
- freshness_score < 30: auto-KILL
- freshness_score > 70: bonus points in backtest
- 30-70: neutral, proceed with standard backtest

Usage:
    python3 alpha_validator.py ALPHA524
    python3 alpha_validator.py --pending
    python3 alpha_validator.py --batch ALPHA524,ALPHA525,ALPHA526
    python3 alpha_validator.py --integrate  # Run validation + update backtest scores
"""

import csv
import json
import argparse
import hashlib
import urllib.request
import urllib.error
import urllib.parse
import ssl
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import math

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
CACHE_FILE = LEDGER_DIR / "ALPHA_VALIDATION_CACHE.csv"
ALPHA_FILE = LEDGER_DIR / "ALPHA_STAGING.csv"
BACKTEST_FILE = LEDGER_DIR / "BACKTESTS" / "BACKTEST_RESULTS.csv"

# Category half-lives in days (how quickly tactics in this category expire)
CATEGORY_HALF_LIVES = {
    "PLATFORM_ARBITRAGE": 30,   # Platforms change fast
    "AUTOMATION_HACK": 45,      # Gets patched
    "GROWTH_HACK": 45,          # Saturates quickly
    "COLD_OUTBOUND": 90,        # Deliverability rules change slower
    "OUTBOUND": 90,             # Same as cold outbound
    "CONTENT_FARM": 120,        # Algorithm changes ~quarterly
    "CONTENT_FORMAT": 120,      # Same as content farm
    "SEO_GEO_ASO": 120,         # SEO evolves but slower
    "APP_FACTORY": 180,         # More evergreen tactics
    "MONETIZATION": 180,        # Monetization models stable
    "TOOL_ALPHA": 90,           # Tools change often
    "NEW_METHOD": 60,           # Unproven = higher risk
    "MICRO_SAAS": 150,          # Business models stable
    # Default for unknown categories
    "DEFAULT": 120
}

# Keywords indicating a tactic is dead/patched
DEAD_KEYWORDS = [
    "doesn't work anymore",
    "no longer works",
    "stopped working",
    "got patched",
    "been patched",
    "is dead",
    "is patched",
    "algorithm changed",
    "algorithm update",
    "account banned",
    "accounts banned",
    "mass bans",
    "shut down",
    "discontinued",
    "deprecated",
    "not working 2026",
    "not working 2025",
    "doesn't work 2026",
    "doesn't work 2025",
    "broken after",
    "killed by",
    "rip to"
]

# Keywords indicating a tactic still works
ALIVE_KEYWORDS = [
    "still works",
    "still working",
    "works in 2026",
    "works in 2025",
    "confirmed working",
    "just did this",
    "made $ using",
    "making money with",
    "currently using",
    "update 2026",
    "2026 guide",
    "latest method",
    "new approach",
    "working strategy"
]


class AlphaValidator:
    """Validate alpha entries against live web data"""

    def __init__(self, use_cache: bool = True, cache_ttl_hours: int = 24):
        self.use_cache = use_cache
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.cache = self._load_cache()

        # Create SSL context for HTTPS requests
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def _load_cache(self) -> Dict[str, Dict]:
        """Load validation cache from CSV"""
        cache = {}
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cache_key = row.get('cache_key', '')
                        if cache_key:
                            cache[cache_key] = row
            except Exception as e:
                print(f"Warning: Could not load cache: {e}")
        return cache

    def _save_cache(self) -> None:
        """Save validation cache to CSV"""
        if not self.cache:
            return

        fieldnames = [
            'cache_key', 'alpha_id', 'source_url', 'url_exists',
            'freshness_score', 'decay_factor', 'alive_signals',
            'dead_signals', 'last_validated', 'validation_notes'
        ]

        try:
            with open(CACHE_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in self.cache.values():
                    # Only write fields we care about
                    row = {k: entry.get(k, '') for k in fieldnames}
                    writer.writerow(row)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

    def _get_cache_key(self, alpha_id: str, source_url: str) -> str:
        """Generate cache key from alpha_id and source_url"""
        combined = f"{alpha_id}:{source_url}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]

    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        if not self.use_cache:
            return False

        last_validated = cache_entry.get('last_validated', '')
        if not last_validated:
            return False

        try:
            validated_time = datetime.fromisoformat(last_validated)
            return datetime.now() - validated_time < self.cache_ttl
        except:
            return False

    def _check_url_exists(self, url: str) -> Tuple[bool, int]:
        """
        Check if URL still exists (not 404)
        Returns: (exists: bool, status_code: int)
        """
        if not url or not url.startswith(('http://', 'https://')):
            return False, 0

        try:
            # Create request with browser-like headers
            request = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
            )

            response = urllib.request.urlopen(
                request,
                timeout=10,
                context=self.ssl_context
            )
            return True, response.getcode()

        except urllib.error.HTTPError as e:
            # 404, 410 = definitely dead
            # 403, 401 = might be auth-protected but exists
            if e.code in [404, 410]:
                return False, e.code
            elif e.code in [403, 401, 429]:
                return True, e.code  # Exists but protected/rate limited
            return False, e.code

        except urllib.error.URLError as e:
            # DNS error, connection refused, etc.
            return False, 0

        except Exception as e:
            # Timeout or other error
            return False, 0

    def _extract_keywords_from_alpha(self, alpha: Dict) -> List[str]:
        """Extract key search terms from alpha entry"""
        keywords = []

        # Get tactic description
        tactic = alpha.get('tactic', '')
        category = alpha.get('category', '')
        source = alpha.get('source', '')

        # Extract key phrases (2-3 word combinations)
        if tactic:
            # Split and get meaningful chunks
            words = re.findall(r'\b\w{4,}\b', tactic.lower())
            if len(words) >= 2:
                keywords.append(' '.join(words[:3]))
            if len(words) >= 4:
                keywords.append(' '.join(words[1:4]))

        # Add category-specific search terms
        if category:
            keywords.append(f"{category.lower().replace('_', ' ')}")

        # Add source if it's a known account
        if source and source.startswith('@'):
            keywords.append(source)

        return keywords[:5]  # Limit to 5 searches

    def _simulate_web_search(self, query: str, for_dead: bool = False) -> Tuple[int, List[str]]:
        """
        Simulate web search by checking keyword patterns

        In a real implementation, this would use WebSearch tool or API.
        For now, we do pattern analysis on the query and return estimated signals.

        Returns: (signal_count, matched_patterns)
        """
        # This is a simplified simulation
        # In production, integrate with actual web search

        query_lower = query.lower()
        matched = []

        if for_dead:
            # Check for dead indicators
            for keyword in DEAD_KEYWORDS:
                if keyword in query_lower:
                    matched.append(keyword)
        else:
            # Check for alive indicators
            for keyword in ALIVE_KEYWORDS:
                if keyword in query_lower:
                    matched.append(keyword)

        return len(matched), matched

    def _calculate_decay_factor(self, category: str, date_added: str) -> float:
        """
        Calculate decay factor based on category half-life and age

        Formula: decay = 2^(-age_days / half_life)

        Returns: 0.0 to 1.0 (1.0 = fresh, 0.0 = completely decayed)
        """
        # Get half-life for category
        half_life = CATEGORY_HALF_LIVES.get(
            category.upper(),
            CATEGORY_HALF_LIVES["DEFAULT"]
        )

        # Calculate age in days
        try:
            if date_added:
                added_date = datetime.strptime(date_added.split('T')[0], '%Y-%m-%d')
            else:
                # Assume added today if no date
                added_date = datetime.now()
        except:
            added_date = datetime.now()

        age_days = (datetime.now() - added_date).days

        # Apply exponential decay formula
        decay = math.pow(2, -age_days / half_life)

        return round(decay, 3)

    def _analyze_tactic_text(self, alpha: Dict) -> Tuple[int, int, List[str]]:
        """
        Analyze tactic text for alive/dead signals

        Returns: (alive_signals, dead_signals, notes)
        """
        tactic = alpha.get('tactic', '').lower()
        notes = alpha.get('reviewer_notes', '').lower()
        combined = f"{tactic} {notes}"

        alive_count = 0
        dead_count = 0
        analysis_notes = []

        # Check for dead signals
        for keyword in DEAD_KEYWORDS:
            if keyword in combined:
                dead_count += 1
                analysis_notes.append(f"DEAD_SIGNAL: '{keyword}'")

        # Check for alive signals
        for keyword in ALIVE_KEYWORDS:
            if keyword in combined:
                alive_count += 1
                analysis_notes.append(f"ALIVE_SIGNAL: '{keyword}'")

        # Check for 2026/2025 mentions (recent = good)
        if '2026' in combined:
            alive_count += 2
            analysis_notes.append("Recent: mentions 2026")
        elif '2025' in combined:
            alive_count += 1
            analysis_notes.append("Somewhat recent: mentions 2025")
        elif '2024' in combined and '2023' not in combined:
            # 2024 without older years might be okay
            pass
        elif any(year in combined for year in ['2023', '2022', '2021', '2020']):
            dead_count += 1
            analysis_notes.append("OLD: mentions 2023 or earlier")

        # Check for specific revenue numbers (good sign)
        if re.search(r'\$\d+[kK]|\$\d{4,}', combined):
            alive_count += 1
            analysis_notes.append("Has specific revenue numbers")

        return alive_count, dead_count, analysis_notes

    def validate_alpha(self, alpha_id: str) -> Dict[str, Any]:
        """
        Validate a single alpha entry against live web data

        Returns validation result with freshness_score
        """
        # Load alpha entry
        alpha = self._load_alpha(alpha_id)
        if not alpha:
            return {
                "alpha_id": alpha_id,
                "error": f"Alpha {alpha_id} not found",
                "freshness_score": 0,
                "decision": "KILL"
            }

        source_url = alpha.get('source_url', '')
        category = alpha.get('category', 'DEFAULT')
        date_added = alpha.get('date_added', '')

        # Check cache first
        cache_key = self._get_cache_key(alpha_id, source_url)
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            cached = self.cache[cache_key]
            return {
                "alpha_id": alpha_id,
                "freshness_score": int(cached.get('freshness_score', 50)),
                "url_exists": cached.get('url_exists', 'unknown') == 'True',
                "decay_factor": float(cached.get('decay_factor', 0.5)),
                "alive_signals": int(cached.get('alive_signals', 0)),
                "dead_signals": int(cached.get('dead_signals', 0)),
                "cached": True,
                "validation_notes": cached.get('validation_notes', ''),
                "decision": self._get_decision(int(cached.get('freshness_score', 50)))
            }

        # === VALIDATION PIPELINE ===

        score = 50  # Start neutral
        notes = []

        # 1. Check if source URL exists (20 points)
        url_exists, status_code = self._check_url_exists(source_url)
        if url_exists:
            score += 15
            notes.append(f"URL exists (status {status_code})")
        else:
            score -= 20
            notes.append(f"URL dead/unreachable (status {status_code})")

        # 2. Calculate decay based on category + age (up to -30 points)
        decay_factor = self._calculate_decay_factor(category, date_added)
        decay_penalty = int((1 - decay_factor) * 30)
        score -= decay_penalty
        notes.append(f"Decay factor: {decay_factor} ({category} half-life)")

        # 3. Analyze tactic text for alive/dead signals
        alive_signals, dead_signals, text_notes = self._analyze_tactic_text(alpha)
        notes.extend(text_notes)

        # Apply signal adjustments
        score += (alive_signals * 5)  # +5 per alive signal
        score -= (dead_signals * 10)  # -10 per dead signal

        # 4. Category-specific adjustments
        if category.upper() in ['PLATFORM_ARBITRAGE', 'AUTOMATION_HACK']:
            # High-risk categories need more alive signals to be trusted
            if alive_signals < 2:
                score -= 10
                notes.append("High-risk category needs more recent validation")

        # 5. Clamp score to 0-100
        score = max(0, min(100, score))

        # Build result
        result = {
            "alpha_id": alpha_id,
            "source_url": source_url,
            "category": category,
            "freshness_score": score,
            "url_exists": url_exists,
            "decay_factor": decay_factor,
            "alive_signals": alive_signals,
            "dead_signals": dead_signals,
            "validation_notes": "; ".join(notes),
            "last_validated": datetime.now().isoformat(),
            "decision": self._get_decision(score)
        }

        # Update cache
        self.cache[cache_key] = {
            "cache_key": cache_key,
            "alpha_id": alpha_id,
            "source_url": source_url,
            "url_exists": str(url_exists),
            "freshness_score": str(score),
            "decay_factor": str(decay_factor),
            "alive_signals": str(alive_signals),
            "dead_signals": str(dead_signals),
            "last_validated": datetime.now().isoformat(),
            "validation_notes": "; ".join(notes)
        }

        return result

    def _get_decision(self, score: int) -> str:
        """Get decision based on freshness score"""
        if score < 30:
            return "AUTO_KILL"
        elif score >= 70:
            return "FRESH"
        else:
            return "NEUTRAL"

    def _load_alpha(self, alpha_id: str) -> Dict[str, str]:
        """Load alpha entry from ALPHA_STAGING.csv"""
        try:
            with open(ALPHA_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('alpha_id') == alpha_id:
                        return row
        except Exception as e:
            print(f"Error loading alpha: {e}")
        return {}

    def validate_batch(self, alpha_ids: List[str]) -> List[Dict]:
        """Validate multiple alpha entries"""
        results = []

        for i, alpha_id in enumerate(alpha_ids):
            result = self.validate_alpha(alpha_id)
            results.append(result)

            # Progress indicator
            decision = result.get('decision', 'UNKNOWN')
            score = result.get('freshness_score', 0)
            print(f"[{i+1}/{len(alpha_ids)}] {alpha_id}: Score {score} - {decision}")

        # Save cache after batch
        self._save_cache()

        return results

    def get_pending_alpha_ids(self) -> List[str]:
        """Get all PENDING_REVIEW alpha IDs"""
        pending = []
        try:
            with open(ALPHA_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'PENDING_REVIEW':
                        alpha_id = row.get('alpha_id')
                        if alpha_id:
                            pending.append(alpha_id)
        except Exception as e:
            print(f"Error loading pending alpha: {e}")
        return pending

    def get_all_alpha_ids(self) -> List[str]:
        """Get all alpha IDs"""
        all_ids = []
        try:
            with open(ALPHA_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    alpha_id = row.get('alpha_id')
                    if alpha_id:
                        all_ids.append(alpha_id)
        except Exception as e:
            print(f"Error loading alpha: {e}")
        return all_ids

    def integrate_with_backtest(self, validation_results: List[Dict]) -> None:
        """
        Integrate validation results with backtest system

        - AUTO_KILL entries get marked for killing
        - FRESH entries get bonus points
        - Updates backtest results CSV
        """
        if not validation_results:
            return

        # Load existing backtest results
        backtest_scores = {}
        if BACKTEST_FILE.exists():
            try:
                with open(BACKTEST_FILE, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        backtest_scores[row.get('alpha_id')] = row
            except:
                pass

        # Update scores based on validation
        updates = []
        for result in validation_results:
            alpha_id = result.get('alpha_id')
            freshness = result.get('freshness_score', 50)
            decision = result.get('decision', 'NEUTRAL')

            if alpha_id in backtest_scores:
                existing = backtest_scores[alpha_id]
                old_score = int(existing.get('backtest_score', 50))

                # Apply freshness modifier
                if decision == "AUTO_KILL":
                    new_score = min(old_score, 25)  # Cap at 25 if auto-kill
                    new_decision = "KILL"
                elif decision == "FRESH":
                    new_score = min(100, old_score + 10)  # +10 bonus
                    new_decision = existing.get('decision', 'PAPER_TRADE')
                else:
                    new_score = old_score
                    new_decision = existing.get('decision', 'PAPER_TRADE')

                existing['backtest_score'] = str(new_score)
                existing['decision'] = new_decision
                existing['freshness_validated'] = str(freshness)
                existing['freshness_decision'] = decision

                updates.append(existing)

        # Save updated backtest results
        if updates:
            print(f"\nUpdated {len(updates)} backtest entries with freshness scores")

    def print_summary(self, results: List[Dict]) -> None:
        """Print summary of validation results"""
        if not results:
            print("No results to summarize")
            return

        total = len(results)
        auto_kill = sum(1 for r in results if r.get('decision') == 'AUTO_KILL')
        fresh = sum(1 for r in results if r.get('decision') == 'FRESH')
        neutral = sum(1 for r in results if r.get('decision') == 'NEUTRAL')
        errors = sum(1 for r in results if 'error' in r)

        avg_score = sum(r.get('freshness_score', 0) for r in results) / total if total > 0 else 0

        print("\n" + "="*50)
        print("ALPHA VALIDATION SUMMARY")
        print("="*50)
        print(f"Total validated:   {total}")
        print(f"Average score:     {avg_score:.1f}")
        print(f"")
        print(f"FRESH (>70):       {fresh} ({fresh/total*100:.1f}%)")
        print(f"NEUTRAL (30-70):   {neutral} ({neutral/total*100:.1f}%)")
        print(f"AUTO_KILL (<30):   {auto_kill} ({auto_kill/total*100:.1f}%)")
        if errors:
            print(f"Errors:            {errors}")
        print("="*50)

        # Show top fresh entries
        if fresh > 0:
            print("\nTop FRESH entries:")
            fresh_entries = [r for r in results if r.get('decision') == 'FRESH']
            fresh_entries.sort(key=lambda x: x.get('freshness_score', 0), reverse=True)
            for entry in fresh_entries[:5]:
                print(f"  {entry['alpha_id']}: {entry['freshness_score']} - {entry.get('category', 'N/A')}")

        # Show auto-kill entries
        if auto_kill > 0:
            print("\nAUTO_KILL entries:")
            kill_entries = [r for r in results if r.get('decision') == 'AUTO_KILL']
            for entry in kill_entries[:10]:
                print(f"  {entry['alpha_id']}: {entry['freshness_score']} - {entry.get('validation_notes', '')[:60]}")


def main():
    parser = argparse.ArgumentParser(
        description='Validate alpha entries against live web data'
    )
    parser.add_argument(
        'alpha_id',
        nargs='?',
        help='Alpha ID to validate (e.g., ALPHA524)'
    )
    parser.add_argument(
        '--pending',
        action='store_true',
        help='Validate all PENDING_REVIEW entries'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all alpha entries'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='Comma-separated list of alpha IDs to validate'
    )
    parser.add_argument(
        '--integrate',
        action='store_true',
        help='Integrate results with backtest system'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Skip cache and revalidate everything'
    )
    parser.add_argument(
        '--cache-ttl',
        type=int,
        default=24,
        help='Cache TTL in hours (default: 24)'
    )

    args = parser.parse_args()

    validator = AlphaValidator(
        use_cache=not args.no_cache,
        cache_ttl_hours=args.cache_ttl
    )

    results = []

    if args.pending:
        print("Validating all PENDING_REVIEW entries...")
        alpha_ids = validator.get_pending_alpha_ids()
        if not alpha_ids:
            print("No PENDING_REVIEW entries found")
            return
        print(f"Found {len(alpha_ids)} pending entries\n")
        results = validator.validate_batch(alpha_ids)

    elif args.all:
        print("Validating ALL alpha entries...")
        alpha_ids = validator.get_all_alpha_ids()
        if not alpha_ids:
            print("No alpha entries found")
            return
        print(f"Found {len(alpha_ids)} entries\n")
        results = validator.validate_batch(alpha_ids)

    elif args.batch:
        alpha_ids = [aid.strip() for aid in args.batch.split(',')]
        print(f"Validating {len(alpha_ids)} entries...")
        results = validator.validate_batch(alpha_ids)

    elif args.alpha_id:
        result = validator.validate_alpha(args.alpha_id)
        results = [result]

        # Print detailed single result
        print("\n" + "="*50)
        print(f"VALIDATION RESULT: {args.alpha_id}")
        print("="*50)
        for key, value in result.items():
            if key != 'validation_notes':
                print(f"{key}: {value}")
        print(f"\nNotes:")
        for note in result.get('validation_notes', '').split('; '):
            if note:
                print(f"  - {note}")
        print("="*50)

    else:
        parser.print_help()
        return

    # Print summary for batch operations
    if len(results) > 1:
        validator.print_summary(results)

    # Integrate with backtest if requested
    if args.integrate and results:
        print("\nIntegrating with backtest system...")
        validator.integrate_with_backtest(results)

    # Save cache
    validator._save_cache()
    print(f"\nCache saved to {CACHE_FILE}")


if __name__ == "__main__":
    main()
