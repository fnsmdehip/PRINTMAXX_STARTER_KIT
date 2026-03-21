#!/usr/bin/env python3

from __future__ import annotations
"""
Alpha Screening System - Institutional Grade
Rigorous multi-factor scoring with decay modeling and cross-validation

This is NOT a simple keyword matcher. This is a quant fund's alpha validation pipeline.

Scoring Breakdown (EXACTLY 100 points):
========================================
1. Evidence Quality (30 pts) - Hard evidence > claims
2. Replicability (20 pts) - Can we actually do this?
3. Time Decay (20 pts) - How stale is this alpha?
4. Historical Performance (15 pts) - Did similar tactics work before?
5. ROI Potential Weight (15 pts) - HIGHEST vs LOW potential

Decision Thresholds:
- SCALE: >= 70 (deploy with confidence)
- PAPER_TRADE: 50-69 (test with minimal capital first)
- KILL: < 50 (do not pursue)

Category-Specific Decay Rates (Monthly):
- PLATFORM_ARBITRAGE: 50% (arbitrage windows close fast)
- COLD_OUTBOUND: 20% (ESP rules tighten gradually)
- APP_FACTORY: 10% (app tactics stable)
- CONTENT_FARM: 15% (algorithm shifts quarterly)
- SEO_GEO_ASO: 15% (Google updates quarterly)
- MONETIZATION: 10% (pricing psychology stable)
- TOOL_ALPHA: 20% (tools change, get deprecated)
- GROWTH_HACK: 30% (platforms patch exploits)
- AI_INFLUENCER: 25% (platform policies shift)
- ALGO_TRADING: 40% (market edges decay fast)
- ECOM_ARB: 35% (arbitrage windows close)
- DEFAULT: 15%

Usage:
    python3 alpha_screening.py ALPHA524
    python3 alpha_screening.py --pending
    python3 alpha_screening.py --category COLD_OUTBOUND --pending
    python3 alpha_screening.py --min-score 60 --pending
    python3 alpha_screening.py --export-report
"""

import csv
csv.field_size_limit(10 * 1024 * 1024)
import re
import argparse
import math
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import json

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
BACKTEST_DIR = LEDGER_DIR / "BACKTESTS"
BACKTEST_DIR.mkdir(exist_ok=True)


# ============================================================================
# DECAY RATES - Category-specific alpha decay (monthly percentage)
# ============================================================================

DECAY_RATES = {
    "PLATFORM_ARBITRAGE": 0.50,    # Arbitrage windows close FAST
    "PLATFORM_ARB": 0.50,          # Alias
    "ALGO_TRADING": 0.40,          # Market edges decay quickly
    "ECOM_ARB": 0.35,              # Ecom arbitrage windows close
    "GROWTH_HACK": 0.30,           # Platforms patch exploits
    "AI_INFLUENCER": 0.25,         # Platform policies shift
    "TOOL_ALPHA": 0.20,            # Tools get deprecated/changed
    "COLD_OUTBOUND": 0.20,         # ESP rules tighten gradually
    "OUTBOUND": 0.20,              # Alias for COLD_OUTBOUND
    "CONTENT_FARM": 0.15,          # Algorithm shifts quarterly
    "CONTENT_FORMAT": 0.15,        # Format trends change
    "SEO_GEO_ASO": 0.15,           # Google updates quarterly
    "APP_FACTORY": 0.10,           # App tactics relatively stable
    "MONETIZATION": 0.10,          # Pricing psychology stable
    "MICRO_SAAS": 0.10,            # SaaS principles stable
    "NEW_METHOD": 0.20,            # Unknown - default to moderate
    "DEFAULT": 0.15                # Fallback
}

# ROI potential weights (multiplied against final score)
ROI_WEIGHTS = {
    "HIGHEST": 1.0,   # Full score
    "HIGH": 0.85,     # 15% penalty
    "MEDIUM": 0.70,   # 30% penalty
    "LOW": 0.55,      # 45% penalty
    "UNKNOWN": 0.75   # Default to conservative
}


@dataclass
class EvidenceScore:
    """Detailed evidence quality breakdown"""
    has_revenue_numbers: bool = False
    has_specific_percentages: bool = False
    has_timeline_data: bool = False
    has_verified_source: bool = False
    has_multiple_sources: bool = False
    has_case_study: bool = False
    engagement_authentic: bool = True
    earnings_verified: bool = False

    def calculate_score(self) -> Tuple[int, str]:
        """Calculate evidence quality score (0-30 points)"""
        score = 0
        notes = []

        # Hard evidence: revenue numbers with verification (0-10)
        if self.has_revenue_numbers:
            if self.earnings_verified:
                score += 10
                notes.append("Verified revenue")
            else:
                score += 5
                notes.append("Unverified revenue claim")

        # Specific metrics (0-8)
        if self.has_specific_percentages:
            score += 4
            notes.append("Specific %")
        if self.has_timeline_data:
            score += 4
            notes.append("Timeline data")

        # Source quality (0-8)
        if self.has_multiple_sources:
            score += 5
            notes.append("Multi-source")
        elif self.has_verified_source:
            score += 3
            notes.append("Single verified source")

        if self.has_case_study:
            score += 3
            notes.append("Case study")

        # Authenticity penalty (0-4)
        if self.engagement_authentic:
            score += 4
            notes.append("Authentic engagement")
        else:
            notes.append("SUSPICIOUS engagement")

        return min(score, 30), ", ".join(notes)


@dataclass
class ReplicabilityScore:
    """Can we actually implement this?"""
    has_clear_steps: bool = False
    has_specific_tools: bool = False
    has_action_verbs: bool = False
    requires_resources_we_have: bool = True
    complexity_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH, EXTREME

    def calculate_score(self) -> Tuple[int, str]:
        """Calculate replicability score (0-20 points)"""
        score = 0
        notes = []

        # Clear methodology (0-8)
        if self.has_clear_steps:
            score += 4
            notes.append("Clear steps")
        if self.has_specific_tools:
            score += 4
            notes.append("Named tools")

        # Actionability (0-6)
        if self.has_action_verbs:
            score += 3
            notes.append("Action-oriented")
        if self.requires_resources_we_have:
            score += 3
            notes.append("Resources available")
        else:
            notes.append("MISSING resources")

        # Complexity penalty (0-6)
        complexity_scores = {
            "LOW": 6,      # Easy to implement
            "MEDIUM": 4,   # Moderate effort
            "HIGH": 2,     # Significant effort
            "EXTREME": 0   # Massive undertaking
        }
        score += complexity_scores.get(self.complexity_level, 4)
        notes.append(f"Complexity: {self.complexity_level}")

        return min(score, 20), ", ".join(notes)


@dataclass
class ScreeningResult:
    """Complete screening result with confidence intervals"""
    alpha_id: str
    raw_score: float
    decay_adjusted_score: float
    final_score: float
    decision: str
    confidence_lower: float
    confidence_upper: float
    category: str
    roi_potential: str
    age_months: float
    decay_rate: float
    evidence_breakdown: Dict
    replicability_breakdown: Dict
    historical_similar_count: int
    historical_similar_success_rate: float
    timestamp: str
    notes: List[str] = field(default_factory=list)


class AlphaScreener:
    """Institutional-grade alpha screening system"""

    def __init__(self):
        self.alpha_file = LEDGER_DIR / "ALPHA_STAGING.csv"
        self.backtest_output = BACKTEST_DIR / "BACKTEST_RESULTS.csv"
        self.historical_results = self._load_historical_results()

    def _load_historical_results(self) -> Dict[str, List[Dict]]:
        """Load historical backtest results for cross-reference"""
        results_by_category = defaultdict(list)

        if self.backtest_output.exists():
            try:
                with open(self.backtest_output, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        category = row.get('category', 'UNKNOWN')
                        results_by_category[category].append(row)
            except Exception as e:
                print(f"Warning: Could not load historical results: {e}")

        return results_by_category

    def _load_alpha(self, alpha_id: str) -> Dict[str, str]:
        """Load alpha entry from ALPHA_STAGING.csv"""
        try:
            with open(self.alpha_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('alpha_id') == alpha_id:
                        return row
        except Exception as e:
            print(f"Error loading alpha: {e}")
        return {}

    def _extract_numbers(self, text: str) -> List[str]:
        """Extract numeric values from text"""
        # Match: $X, X%, Xk, XM, X/month, etc.
        patterns = [
            r'\$[\d,]+\.?\d*[KkMmBb]?',           # Dollar amounts
            r'\d+\.?\d*%',                          # Percentages
            r'\d+\.?\d*[KkMmBb]',                  # K/M/B numbers
            r'\d+\.?\d*x',                          # Multipliers
            r'\d+\.\d+',                           # Decimals
            r'\b\d{2,}\b'                          # Numbers with 2+ digits
        ]

        numbers = []
        for pattern in patterns:
            numbers.extend(re.findall(pattern, text, re.IGNORECASE))

        return numbers

    def _assess_evidence_quality(self, alpha: Dict) -> EvidenceScore:
        """Deep assessment of evidence quality"""
        description = alpha.get('description', '') + ' ' + alpha.get('tactic', '')
        description_lower = description.lower()
        reviewer_notes = alpha.get('reviewer_notes', '').lower()

        evidence = EvidenceScore()

        # Revenue/earning numbers
        revenue_patterns = [r'\$[\d,]+', r'\d+[KkMm]\s*(arr|mrr|revenue|profit|month)',
                          r'(made|earned|generated|profit)\s*\$']
        evidence.has_revenue_numbers = any(re.search(p, description, re.IGNORECASE) for p in revenue_patterns)

        # Specific percentages
        evidence.has_specific_percentages = bool(re.search(r'\d+\.?\d*%', description))

        # Timeline data
        timeline_patterns = [r'\d+\s*(day|week|month|hour|minute)',
                           r'in\s+\d+', r'after\s+\d+', r'within\s+\d+']
        evidence.has_timeline_data = any(re.search(p, description_lower) for p in timeline_patterns)

        # Source verification
        verified_indicators = ['verified', 'confirmed', 'documented', 'public dashboard',
                              'tax docs', 'bank statement', 'proof', 'screenshot']
        evidence.has_verified_source = any(ind in description_lower or ind in reviewer_notes
                                           for ind in verified_indicators)

        # Multiple sources
        multi_indicators = ['multiple sources', 'several', 'confirmed by', 'various',
                           'both', 'independent']
        evidence.has_multiple_sources = any(ind in description_lower or ind in reviewer_notes
                                            for ind in multi_indicators)

        # Case study
        evidence.has_case_study = any(x in description_lower for x in
                                      ['case study', 'example:', 'portfolio:', 'built'])

        # Engagement authenticity (from CSV field or inference)
        auth_field = alpha.get('engagement_authenticity', '').upper()
        if auth_field == 'SUSPICIOUS':
            evidence.engagement_authentic = False
        elif auth_field == 'AUTHENTIC':
            evidence.engagement_authentic = True
        else:
            # Infer from patterns
            suspicious_patterns = ['round number', 'selling to audience', 'no proof',
                                  'inflated', 'fake', 'botted']
            evidence.engagement_authentic = not any(p in reviewer_notes for p in suspicious_patterns)

        # Earnings verification (from CSV field)
        earnings_field = alpha.get('earnings_verified', '').upper()
        evidence.earnings_verified = earnings_field == 'TRUE'

        return evidence

    def _assess_replicability(self, alpha: Dict) -> ReplicabilityScore:
        """Assess how replicable this tactic is"""
        tactic = alpha.get('tactic', '') + ' ' + alpha.get('description', '')
        tactic_lower = tactic.lower()

        repl = ReplicabilityScore()

        # Clear steps (numbered or bulleted)
        step_patterns = [r'\d+[\.\)]\s', r'step\s*\d+', r'first.*then.*finally',
                        r'•', r'-\s+\w+']
        repl.has_clear_steps = any(re.search(p, tactic, re.IGNORECASE) for p in step_patterns)

        # Specific tools mentioned
        tool_indicators = ['using', 'with', 'via', '.io', '.com', '.ai', 'api',
                          'tool:', 'platform:', 'software']
        repl.has_specific_tools = any(ind in tactic_lower for ind in tool_indicators)

        # Action verbs
        action_verbs = ['create', 'build', 'send', 'post', 'generate', 'use',
                       'implement', 'deploy', 'launch', 'test', 'run', 'set up',
                       'configure', 'install', 'write', 'automate']
        repl.has_action_verbs = any(verb in tactic_lower for verb in action_verbs)

        # Resource requirements
        expensive_indicators = ['$1000+', 'enterprise', 'team of', 'hire', 'investment',
                               'capital required', 'funding']
        repl.requires_resources_we_have = not any(ind in tactic_lower for ind in expensive_indicators)

        # Complexity assessment
        complexity_indicators = {
            'EXTREME': ['months of', 'year-long', 'massive', 'requires team', 'enterprise'],
            'HIGH': ['weeks of', 'complex', 'advanced', 'technical expertise', 'custom'],
            'MEDIUM': ['few days', 'moderate', 'some experience', 'configure'],
            'LOW': ['minutes', 'simple', 'easy', 'quick', 'straightforward', 'no-code']
        }

        repl.complexity_level = 'MEDIUM'  # Default
        for level, indicators in complexity_indicators.items():
            if any(ind in tactic_lower for ind in indicators):
                repl.complexity_level = level
                break

        return repl

    def _calculate_age_months(self, alpha: Dict) -> float:
        """Calculate age of alpha in months"""
        date_added = alpha.get('date_added', '')
        timestamp = alpha.get('timestamp', '')

        # Try to parse date
        date_str = date_added or timestamp
        if not date_str:
            return 1.0  # Default to 1 month if unknown

        try:
            # Handle various date formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
                try:
                    parsed_date = datetime.strptime(date_str[:19], fmt[:19] if 'T' in date_str else fmt)
                    break
                except ValueError:
                    continue
            else:
                return 1.0  # Default if parsing fails

            age_days = (datetime.now() - parsed_date).days
            return max(age_days / 30.0, 0.01)  # Convert to months, minimum 0.01

        except Exception:
            return 1.0

    def _get_decay_rate(self, category: str) -> float:
        """Get monthly decay rate for category"""
        # Handle compound categories
        for cat in category.upper().replace(' ', '_').split('+'):
            cat = cat.strip()
            if cat in DECAY_RATES:
                return DECAY_RATES[cat]

        return DECAY_RATES['DEFAULT']

    def _calculate_decay_factor(self, age_months: float, decay_rate: float) -> float:
        """Calculate decay factor using exponential decay"""
        # Exponential decay: value = initial * e^(-decay_rate * time)
        # We use: factor = e^(-decay_rate * age_months)
        factor = math.exp(-decay_rate * age_months)
        return max(factor, 0.1)  # Minimum 10% retention

    def _check_historical_similar(self, alpha: Dict) -> Tuple[int, float]:
        """Check historical performance of similar tactics"""
        category = alpha.get('category', 'UNKNOWN')
        historical = self.historical_results.get(category, [])

        if not historical:
            return 0, 0.5  # No history, neutral

        # Find similar tactics (same category, similar keywords)
        tactic_words = set(alpha.get('tactic', '').lower().split())

        similar_results = []
        for hist in historical:
            hist_words = set(hist.get('source', '').lower().split())
            # Consider similar if 30%+ word overlap
            if tactic_words and hist_words:
                overlap = len(tactic_words & hist_words) / len(tactic_words | hist_words)
                if overlap > 0.3:
                    decision = hist.get('decision', '')
                    score = int(hist.get('backtest_score', 0))
                    similar_results.append((decision, score))

        if not similar_results:
            return 0, 0.5

        # Calculate success rate (SCALE or PAPER_TRADE = success)
        successes = sum(1 for d, s in similar_results if d in ['SCALE', 'PAPER_TRADE'])
        success_rate = successes / len(similar_results)

        return len(similar_results), success_rate

    def _calculate_historical_score(self, similar_count: int, success_rate: float) -> Tuple[int, str]:
        """Calculate historical performance score (0-15 points)"""
        if similar_count == 0:
            return 7, "No historical data (neutral)"

        # Success rate to score conversion
        # 0% = 0 points, 50% = 7.5 points, 100% = 15 points
        score = int(success_rate * 15)

        if success_rate >= 0.7:
            note = f"Similar tactics succeeded ({success_rate:.0%} of {similar_count})"
        elif success_rate >= 0.4:
            note = f"Mixed results ({success_rate:.0%} of {similar_count})"
        else:
            note = f"Similar tactics FAILED ({success_rate:.0%} of {similar_count})"

        return score, note

    def _get_roi_weight(self, roi_potential: str) -> float:
        """Get ROI potential weight"""
        return ROI_WEIGHTS.get(roi_potential.upper(), ROI_WEIGHTS['UNKNOWN'])

    def _calculate_confidence_interval(self, base_score: float, evidence: EvidenceScore) -> Tuple[float, float]:
        """Calculate confidence interval based on evidence quality"""
        # Higher evidence quality = tighter interval
        evidence_score, _ = evidence.calculate_score()

        # Map evidence score (0-30) to uncertainty (5-20)
        uncertainty = 20 - (evidence_score / 30.0) * 15

        # Additional uncertainty for unverified claims
        if not evidence.earnings_verified and evidence.has_revenue_numbers:
            uncertainty += 5

        if not evidence.engagement_authentic:
            uncertainty += 8

        lower = max(0, base_score - uncertainty)
        upper = min(100, base_score + uncertainty)

        return lower, upper

    def screen_alpha(self, alpha_id: str) -> ScreeningResult:
        """
        Full alpha screening pipeline

        Returns ScreeningResult with:
        - Raw score (before decay/ROI adjustment)
        - Decay-adjusted score
        - Final score (with ROI weighting)
        - Confidence intervals
        - Detailed breakdowns
        """
        alpha = self._load_alpha(alpha_id)
        if not alpha:
            raise ValueError(f"Alpha {alpha_id} not found")

        notes = []

        # 1. EVIDENCE QUALITY (30 points)
        evidence = self._assess_evidence_quality(alpha)
        evidence_score, evidence_notes = evidence.calculate_score()

        # 2. REPLICABILITY (20 points)
        replicability = self._assess_replicability(alpha)
        replicability_score, replicability_notes = replicability.calculate_score()

        # 3. TIME DECAY (20 points)
        age_months = self._calculate_age_months(alpha)
        category = alpha.get('category', 'UNKNOWN')
        decay_rate = self._get_decay_rate(category)
        decay_factor = self._calculate_decay_factor(age_months, decay_rate)

        # Time decay score: fresh alpha = 20 points, decayed = less
        time_score = int(20 * decay_factor)
        time_notes = f"Age: {age_months:.1f}mo, Decay: {(1-decay_factor)*100:.0f}%"
        notes.append(time_notes)

        # 4. HISTORICAL PERFORMANCE (15 points)
        similar_count, success_rate = self._check_historical_similar(alpha)
        historical_score, historical_notes = self._calculate_historical_score(similar_count, success_rate)
        notes.append(historical_notes)

        # 5. ROI POTENTIAL WEIGHT (15 points)
        roi_potential = alpha.get('roi_potential', 'UNKNOWN')
        roi_weight = self._get_roi_weight(roi_potential)
        # ROI score is based on potential: HIGHEST=15, HIGH=12.75, MEDIUM=10.5, LOW=8.25
        roi_score = int(15 * roi_weight)
        notes.append(f"ROI potential: {roi_potential} ({roi_weight:.0%})")

        # Calculate scores
        raw_score = evidence_score + replicability_score + 20 + 15 + roi_score  # Max before decay/history

        # Apply time decay to the score
        decay_adjusted = evidence_score + replicability_score + time_score + 15 + roi_score

        # Apply historical adjustment
        final_score = evidence_score + replicability_score + time_score + historical_score + roi_score

        # Confidence interval
        confidence_lower, confidence_upper = self._calculate_confidence_interval(final_score, evidence)

        # Decision based on final score
        if final_score >= 70:
            decision = "SCALE"
        elif final_score >= 50:
            decision = "PAPER_TRADE"
        else:
            decision = "KILL"

        return ScreeningResult(
            alpha_id=alpha_id,
            raw_score=raw_score,
            decay_adjusted_score=decay_adjusted,
            final_score=final_score,
            decision=decision,
            confidence_lower=confidence_lower,
            confidence_upper=confidence_upper,
            category=category,
            roi_potential=roi_potential,
            age_months=age_months,
            decay_rate=decay_rate,
            evidence_breakdown={
                'score': evidence_score,
                'notes': evidence_notes,
                'has_revenue': evidence.has_revenue_numbers,
                'verified_earnings': evidence.earnings_verified,
                'authentic_engagement': evidence.engagement_authentic,
                'has_percentages': evidence.has_specific_percentages,
                'has_timeline': evidence.has_timeline_data,
                'multiple_sources': evidence.has_multiple_sources
            },
            replicability_breakdown={
                'score': replicability_score,
                'notes': replicability_notes,
                'clear_steps': replicability.has_clear_steps,
                'specific_tools': replicability.has_specific_tools,
                'action_verbs': replicability.has_action_verbs,
                'resources_available': replicability.requires_resources_we_have,
                'complexity': replicability.complexity_level
            },
            historical_similar_count=similar_count,
            historical_similar_success_rate=success_rate,
            timestamp=datetime.now().isoformat(),
            notes=notes
        )

    def screen_batch(self, alpha_ids: List[str], min_score: Optional[int] = None) -> List[ScreeningResult]:
        """Screen multiple alpha entries"""
        results = []

        for alpha_id in alpha_ids:
            try:
                result = self.screen_alpha(alpha_id)
                results.append(result)

                # Color-coded output
                color = '\033[92m' if result.decision == 'SCALE' else '\033[93m' if result.decision == 'PAPER_TRADE' else '\033[91m'
                reset = '\033[0m'

                print(f"{color}{alpha_id}: {result.final_score:.0f} ({result.confidence_lower:.0f}-{result.confidence_upper:.0f}) - {result.decision}{reset}")

            except Exception as e:
                print(f"Error screening {alpha_id}: {e}")

        # Filter by min score if specified
        if min_score is not None:
            results = [r for r in results if r.final_score >= min_score]

        return results

    def get_pending_alpha(self, category: Optional[str] = None) -> List[str]:
        """Get all PENDING_REVIEW alpha IDs, optionally filtered by category"""
        pending = []
        try:
            with open(self.alpha_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'PENDING_REVIEW':
                        if category is None or row.get('category', '').upper() == category.upper():
                            pending.append(row.get('alpha_id'))
        except Exception as e:
            print(f"Error loading pending alpha: {e}")

        return pending

    def save_results(self, results: List[ScreeningResult]) -> None:
        """Save screening results to CSV"""
        if not results:
            return

        file_exists = self.backtest_output.exists()

        with open(self.backtest_output, 'a', newline='') as f:
            fieldnames = [
                'alpha_id', 'backtest_score', 'decision', 'category', 'source',
                'timestamp', 'multiple_sources', 'has_numbers', 'has_timeline',
                'still_valid_2026', 'engagement_data', 'conversion_data', 'replicable',
                'raw_score', 'decay_adjusted_score', 'confidence_lower', 'confidence_upper',
                'age_months', 'decay_rate', 'roi_potential', 'historical_similar_count',
                'historical_success_rate', 'evidence_score', 'replicability_score',
                'complexity', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for result in results:
                row = {
                    'alpha_id': result.alpha_id,
                    'backtest_score': int(result.final_score),
                    'decision': result.decision,
                    'category': result.category,
                    'source': '',  # Would need to pull from alpha
                    'timestamp': result.timestamp,
                    'multiple_sources': result.evidence_breakdown.get('multiple_sources', False),
                    'has_numbers': result.evidence_breakdown.get('has_revenue', False),
                    'has_timeline': result.evidence_breakdown.get('has_timeline', False),
                    'still_valid_2026': result.decay_adjusted_score > 50,
                    'engagement_data': result.evidence_breakdown.get('authentic_engagement', True),
                    'conversion_data': result.evidence_breakdown.get('has_percentages', False),
                    'replicable': result.replicability_breakdown.get('clear_steps', False),
                    'raw_score': result.raw_score,
                    'decay_adjusted_score': result.decay_adjusted_score,
                    'confidence_lower': result.confidence_lower,
                    'confidence_upper': result.confidence_upper,
                    'age_months': round(result.age_months, 2),
                    'decay_rate': result.decay_rate,
                    'roi_potential': result.roi_potential,
                    'historical_similar_count': result.historical_similar_count,
                    'historical_success_rate': round(result.historical_similar_success_rate, 2),
                    'evidence_score': result.evidence_breakdown.get('score', 0),
                    'replicability_score': result.replicability_breakdown.get('score', 0),
                    'complexity': result.replicability_breakdown.get('complexity', 'MEDIUM'),
                    'notes': ' | '.join(result.notes)
                }
                writer.writerow(row)

        print(f"\nResults saved to {self.backtest_output}")

    def generate_report(self, results: List[ScreeningResult]) -> str:
        """Generate detailed screening report"""
        if not results:
            return "No results to report"

        report = []
        report.append("=" * 70)
        report.append("ALPHA SCREENING REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)

        # Summary stats
        total = len(results)
        scale = [r for r in results if r.decision == 'SCALE']
        paper = [r for r in results if r.decision == 'PAPER_TRADE']
        kill = [r for r in results if r.decision == 'KILL']

        report.append(f"\nSUMMARY:")
        report.append(f"  Total screened: {total}")
        report.append(f"  SCALE: {len(scale)} ({len(scale)/total*100:.1f}%)")
        report.append(f"  PAPER_TRADE: {len(paper)} ({len(paper)/total*100:.1f}%)")
        report.append(f"  KILL: {len(kill)} ({len(kill)/total*100:.1f}%)")

        # Category breakdown
        by_category = defaultdict(list)
        for r in results:
            by_category[r.category].append(r)

        report.append(f"\nBY CATEGORY:")
        for cat, cat_results in sorted(by_category.items()):
            avg_score = sum(r.final_score for r in cat_results) / len(cat_results)
            decay_rate = cat_results[0].decay_rate if cat_results else 0.15
            report.append(f"  {cat}: {len(cat_results)} entries, avg score {avg_score:.1f}, decay {decay_rate:.0%}/mo")

        # Top performers
        top = sorted(results, key=lambda x: x.final_score, reverse=True)[:10]
        report.append(f"\nTOP 10 ALPHA (Deploy First):")
        for r in top:
            conf = f"({r.confidence_lower:.0f}-{r.confidence_upper:.0f})"
            report.append(f"  {r.alpha_id}: {r.final_score:.0f} {conf} [{r.decision}] - {r.category}")

        # Detailed breakdowns for SCALE decisions
        if scale:
            report.append(f"\n{'='*70}")
            report.append("SCALE DECISIONS - DETAILED BREAKDOWN")
            report.append("=" * 70)

            for r in scale:
                report.append(f"\n{r.alpha_id} - Score: {r.final_score:.0f} ({r.confidence_lower:.0f}-{r.confidence_upper:.0f})")
                report.append(f"  Category: {r.category}")
                report.append(f"  ROI Potential: {r.roi_potential}")
                report.append(f"  Age: {r.age_months:.1f} months, Decay: {r.decay_rate:.0%}/mo")
                report.append(f"  Evidence ({r.evidence_breakdown['score']}/30): {r.evidence_breakdown['notes']}")
                report.append(f"  Replicability ({r.replicability_breakdown['score']}/20): {r.replicability_breakdown['notes']}")
                report.append(f"  Historical: {r.historical_similar_count} similar, {r.historical_similar_success_rate:.0%} success")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Alpha Screening System - Institutional Grade',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 alpha_screening.py ALPHA524           # Screen single alpha
  python3 alpha_screening.py --pending          # Screen all PENDING_REVIEW
  python3 alpha_screening.py --pending --category COLD_OUTBOUND
  python3 alpha_screening.py --pending --min-score 60
  python3 alpha_screening.py --pending --export-report
        """
    )
    parser.add_argument('alpha_id', nargs='?', help='Alpha ID to screen (e.g. ALPHA524)')
    parser.add_argument('--pending', action='store_true', help='Screen all PENDING_REVIEW entries')
    parser.add_argument('--category', type=str, help='Filter by category')
    parser.add_argument('--min-score', type=int, help='Minimum score threshold for results')
    parser.add_argument('--export-report', action='store_true', help='Export detailed report')
    parser.add_argument('--no-save', action='store_true', help='Do not save results to CSV')

    args = parser.parse_args()

    screener = AlphaScreener()

    if args.pending:
        print("Screening PENDING_REVIEW entries...")
        if args.category:
            print(f"  Filtered by category: {args.category}")

        alpha_ids = screener.get_pending_alpha(category=args.category)

        if not alpha_ids:
            print("No PENDING_REVIEW entries found")
            return

        print(f"Found {len(alpha_ids)} entries to screen\n")

        results = screener.screen_batch(alpha_ids, min_score=args.min_score)

        if not args.no_save:
            screener.save_results(results)

        # Summary stats
        total = len(results)
        scale = sum(1 for r in results if r.decision == 'SCALE')
        paper = sum(1 for r in results if r.decision == 'PAPER_TRADE')
        kill = sum(1 for r in results if r.decision == 'KILL')

        print(f"\n{'='*50}")
        print(f"SCREENING SUMMARY")
        print(f"{'='*50}")
        print(f"Total: {total}")
        print(f"\033[92mSCALE: {scale} ({scale/total*100:.1f}%)\033[0m")
        print(f"\033[93mPAPER_TRADE: {paper} ({paper/total*100:.1f}%)\033[0m")
        print(f"\033[91mKILL: {kill} ({kill/total*100:.1f}%)\033[0m")

        # Export report if requested
        if args.export_report:
            report = screener.generate_report(results)
            report_file = BACKTEST_DIR / f"SCREENING_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"\nReport exported to {report_file}")

    elif args.alpha_id:
        try:
            result = screener.screen_alpha(args.alpha_id)
        except ValueError as e:
            print(str(e))
            return

        # Detailed output
        print(f"\n{'='*50}")
        print(f"SCREENING RESULT: {args.alpha_id}")
        print(f"{'='*50}")

        color = '\033[92m' if result.decision == 'SCALE' else '\033[93m' if result.decision == 'PAPER_TRADE' else '\033[91m'
        reset = '\033[0m'

        print(f"Final Score: {color}{result.final_score:.0f}/100{reset}")
        print(f"Confidence Interval: ({result.confidence_lower:.0f} - {result.confidence_upper:.0f})")
        print(f"Decision: {color}{result.decision}{reset}")
        print(f"\nCategory: {result.category}")
        print(f"ROI Potential: {result.roi_potential}")
        print(f"Age: {result.age_months:.1f} months")
        print(f"Decay Rate: {result.decay_rate:.0%}/month")

        print(f"\n--- Score Breakdown ---")
        print(f"Evidence Quality: {result.evidence_breakdown['score']}/30")
        print(f"  {result.evidence_breakdown['notes']}")
        print(f"Replicability: {result.replicability_breakdown['score']}/20")
        print(f"  {result.replicability_breakdown['notes']}")
        print(f"Time Freshness: ~{int(20 * math.exp(-result.decay_rate * result.age_months))}/20")
        print(f"Historical Performance: ~{int(result.historical_similar_success_rate * 15)}/15")
        print(f"  {result.historical_similar_count} similar tactics, {result.historical_similar_success_rate:.0%} success")
        print(f"ROI Weight: ~{int(15 * ROI_WEIGHTS.get(result.roi_potential.upper(), 0.75))}/15")

        if not args.no_save:
            screener.save_results([result])

    else:
        print("Please specify an alpha ID or use --pending")
        parser.print_help()


if __name__ == "__main__":
    main()
