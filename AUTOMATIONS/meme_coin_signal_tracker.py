#!/usr/bin/env python3
"""
Meme Coin Signal Tracker
Monitors Reddit + Twitter for coin launch signals based on historical patterns
Scores entry potential (0-100) based on backtest data
"""

import csv
import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Configuration
PROJECT_ROOT = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
BACKTEST_DATA = f"{PROJECT_ROOT}/LEDGER/MEME_COIN_BACKTEST_DATA.csv"
PATTERNS_DATA = f"{PROJECT_ROOT}/LEDGER/MEME_COIN_PATTERNS.csv"
WATCHLIST_FILE = f"{PROJECT_ROOT}/LEDGER/MEME_COIN_WATCHLIST.csv"
SIGNALS_OUTPUT = f"{PROJECT_ROOT}/LEDGER/MEME_COIN_SIGNALS.csv"

# Detection thresholds
TWITTER_MENTION_THRESHOLD = 1000  # Mentions in 6h
REDDIT_SCORE_THRESHOLD = 300  # Upvotes
HIGH_PROFILE_FOLLOWER_THRESHOLD = 1000000  # 1M+ followers = high profile
HOLDER_THRESHOLD = 200  # Minimum holders for legitimacy

@dataclass
class Signal:
    """Meme coin detection signal"""
    timestamp: str
    coin_name: str
    pattern_match: str
    score: int  # 0-100
    confidence: str  # LOW, MEDIUM, HIGH
    twitter_mentions: int
    reddit_score: int
    high_profile_mentions: List[str]
    time_since_catalyst: int  # hours
    entry_window: str  # IMMEDIATE, CLOSING, MISSED
    recommended_action: str
    risk_level: str
    exit_targets: str
    notes: str


class PatternMatcher:
    """Matches current signals against historical patterns"""

    def __init__(self):
        self.patterns = self._load_patterns()
        self.historical_data = self._load_historical_data()

    def _load_patterns(self) -> List[Dict]:
        """Load pattern definitions from CSV"""
        patterns = []
        with open(PATTERNS_DATA, 'r') as f:
            reader = csv.DictReader(f)
            patterns = list(reader)
        return patterns

    def _load_historical_data(self) -> List[Dict]:
        """Load historical backtest data"""
        data = []
        with open(BACKTEST_DATA, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data

    def detect_ai_trend_viral(self, context: Dict) -> Optional[int]:
        """
        PAT001: AI platform releases feature → viral trend → coins launch
        Returns: Score 0-100 or None
        """
        score = 0

        # Check for AI platform release (OpenAI, Anthropic, Google)
        if context.get('ai_platform_release', False):
            score += 25

        # Check viral art trend on Twitter
        if context.get('twitter_mentions', 0) > 2000:
            score += 20
        elif context.get('twitter_mentions', 0) > 1000:
            score += 10

        # High-profile posters (Musk, Altman, a16z, etc.)
        high_profile = context.get('high_profile_mentions', [])
        if len(high_profile) >= 2:
            score += 30
        elif len(high_profile) == 1:
            score += 15

        # Time since trend started
        hours_since = context.get('hours_since_catalyst', 999)
        if hours_since < 24:
            score += 15
        elif hours_since < 48:
            score += 5

        # Reddit spike
        if context.get('reddit_score', 0) > 500:
            score += 10

        return score if score >= 40 else None

    def detect_viral_moment_fitness(self, context: Dict) -> Optional[int]:
        """
        PAT002: Fitness influencer viral video → branded items become coins
        Returns: Score 0-100 or None
        """
        score = 0

        # Viral video detected
        if context.get('viral_video_views', 0) > 1000000:
            score += 30
        elif context.get('viral_video_views', 0) > 500000:
            score += 15

        # Branded product identifiable
        if context.get('branded_product_identified', False):
            score += 20

        # Reddit discussion threads
        if context.get('reddit_threads', 0) >= 3:
            score += 15
        elif context.get('reddit_threads', 0) >= 1:
            score += 8

        # Time since video
        hours_since = context.get('hours_since_video', 999)
        if hours_since < 48:
            score += 20
        elif hours_since < 72:
            score += 10

        # Multiple competing coins (good signal)
        if context.get('competing_coins', 0) >= 2:
            score += 15

        return score if score >= 40 else None

    def detect_ai_agent_platform(self, context: Dict) -> Optional[int]:
        """
        PAT003: AI bot platform + VC endorsement → token surge
        Returns: Score 0-100 or None
        """
        score = 0

        # AI bot has following
        if context.get('bot_followers', 0) > 10000:
            score += 20
        elif context.get('bot_followers', 0) > 5000:
            score += 10

        # Platform launched
        if context.get('platform_launched', False):
            score += 25

        # VC/influencer endorsement (Marc Andreessen, Naval, etc.)
        endorsers = context.get('vc_endorsements', [])
        if 'a16z' in endorsers or 'Naval' in endorsers:
            score += 30
        elif len(endorsers) > 0:
            score += 15

        # Social mentions spike
        if context.get('social_mentions_increase', 0) > 300:
            score += 15
        elif context.get('social_mentions_increase', 0) > 200:
            score += 8

        # Exchange listing
        if context.get('exchange_listing', False):
            score += 10

        return score if score >= 40 else None

    def detect_ai_agent_original(self, context: Dict) -> Optional[int]:
        """
        PAT004: First-mover AI agent coin → category creation
        Returns: Score 0-100 or None
        """
        score = 0

        # Novel concept (hardest to detect)
        if context.get('novel_concept', False):
            score += 30

        # Working AI bot with history
        if context.get('bot_content_history_days', 0) > 7:
            score += 20
        elif context.get('bot_content_history_days', 0) > 3:
            score += 10

        # Organic community building
        if context.get('holders', 0) > 500:
            score += 20
        elif context.get('holders', 0) > 200:
            score += 10

        # Twitter following growth
        if context.get('follower_growth_pct', 0) > 500:
            score += 20
        elif context.get('follower_growth_pct', 0) > 200:
            score += 10

        # Liquidity locked
        if context.get('liquidity_locked', False):
            score += 10

        return score if score >= 40 else None

    def match_all_patterns(self, context: Dict) -> List[tuple]:
        """
        Match context against all patterns
        Returns: List of (pattern_id, score) tuples
        """
        matches = []

        # Run all pattern detectors
        detectors = [
            ('PAT001', self.detect_ai_trend_viral),
            ('PAT002', self.detect_viral_moment_fitness),
            ('PAT003', self.detect_ai_agent_platform),
            ('PAT004', self.detect_ai_agent_original),
        ]

        for pattern_id, detector in detectors:
            score = detector(context)
            if score is not None:
                matches.append((pattern_id, score))

        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches


class SignalTracker:
    """Main signal tracking and scoring system"""

    def __init__(self):
        self.matcher = PatternMatcher()
        self.watchlist = self._load_watchlist()

    def _load_watchlist(self) -> List[Dict]:
        """Load current watchlist"""
        if not os.path.exists(WATCHLIST_FILE):
            return []

        with open(WATCHLIST_FILE, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _save_signal(self, signal: Signal):
        """Append signal to output CSV"""
        file_exists = os.path.exists(SIGNALS_OUTPUT)

        with open(SIGNALS_OUTPUT, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'coin_name', 'pattern_match', 'score', 'confidence',
                'twitter_mentions', 'reddit_score', 'high_profile_mentions',
                'time_since_catalyst', 'entry_window', 'recommended_action',
                'risk_level', 'exit_targets', 'notes'
            ])

            if not file_exists:
                writer.writeheader()

            writer.writerow(asdict(signal))

    def calculate_entry_window(self, pattern_id: str, hours_since_catalyst: int) -> str:
        """
        Determine if entry window is still open
        Based on historical time_to_peak data
        """
        # Pattern-specific entry windows (based on backtest median time to peak)
        windows = {
            'PAT001': 12,  # AI Trend Viral: 19h peak, enter in first 12h
            'PAT002': 36,  # Viral Fitness: 61h peak, enter in first 36h
            'PAT003': 18,  # AI Agent Platform: 32h peak, enter in first 18h
            'PAT004': 48,  # AI Agent Original: 132h peak, enter in first 48h
            'PAT005': 72,  # AI Agent Creative: 145h peak, enter in first 72h
            'PAT006': 36,  # AI Agent Absurdist: 66h peak, enter in first 36h
            'PAT007': 48,  # AI Agent Social: 92h peak, enter in first 48h
        }

        max_window = windows.get(pattern_id, 24)

        if hours_since_catalyst < max_window * 0.5:
            return "IMMEDIATE"
        elif hours_since_catalyst < max_window:
            return "CLOSING"
        else:
            return "MISSED"

    def get_exit_targets(self, pattern_id: str) -> str:
        """Get exit targets from pattern data"""
        pattern = next((p for p in self.matcher.patterns if p['pattern_id'] == pattern_id), None)
        if pattern:
            return pattern.get('exit_criteria', 'Unknown')
        return "Unknown"

    def score_signal(self, context: Dict) -> Optional[Signal]:
        """
        Score a potential meme coin signal

        Args:
            context: Dict with keys:
                - coin_name: str
                - ai_platform_release: bool
                - twitter_mentions: int
                - reddit_score: int
                - high_profile_mentions: List[str]
                - hours_since_catalyst: int
                - viral_video_views: int (optional)
                - bot_followers: int (optional)
                - holders: int (optional)
                - etc.

        Returns:
            Signal object or None if no pattern match
        """
        # Match against patterns
        matches = self.matcher.match_all_patterns(context)

        if not matches:
            return None

        # Best pattern match
        best_pattern_id, best_score = matches[0]

        # Get pattern details
        pattern = next((p for p in self.matcher.patterns if p['pattern_id'] == best_pattern_id), None)
        if not pattern:
            return None

        # Determine confidence
        if best_score >= 80:
            confidence = "HIGH"
        elif best_score >= 60:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        # Calculate entry window
        hours_since = context.get('hours_since_catalyst', 0)
        entry_window = self.calculate_entry_window(best_pattern_id, hours_since)

        # Recommended action
        if entry_window == "IMMEDIATE" and confidence in ["HIGH", "MEDIUM"]:
            action = "STRONG BUY - Enter now with defined stops"
        elif entry_window == "CLOSING" and confidence == "HIGH":
            action = "BUY - Enter quickly, window closing"
        elif entry_window == "IMMEDIATE" and confidence == "LOW":
            action = "WATCH - Monitor for more signals"
        elif entry_window == "CLOSING":
            action = "CAUTION - Window closing, high risk"
        else:
            action = "PASS - Missed entry window"

        # Create signal
        signal = Signal(
            timestamp=datetime.now(timezone.utc).isoformat(),
            coin_name=context.get('coin_name', 'Unknown'),
            pattern_match=f"{best_pattern_id}: {pattern['pattern_name']}",
            score=best_score,
            confidence=confidence,
            twitter_mentions=context.get('twitter_mentions', 0),
            reddit_score=context.get('reddit_score', 0),
            high_profile_mentions=context.get('high_profile_mentions', []),
            time_since_catalyst=hours_since,
            entry_window=entry_window,
            recommended_action=action,
            risk_level=pattern.get('risk_level', 'UNKNOWN'),
            exit_targets=self.get_exit_targets(best_pattern_id),
            notes=f"Pattern win rate: {pattern.get('win_rate', 'N/A')}. Avg ROI: {pattern.get('avg_roi', 'N/A')}. Sample size: {pattern.get('sample_size', 'N/A')}."
        )

        return signal

    def monitor_watchlist(self):
        """Monitor current watchlist and score signals"""
        print(f"Monitoring {len(self.watchlist)} coins on watchlist...")

        for item in self.watchlist:
            # Build context from watchlist data
            context = {
                'coin_name': item.get('coin_name', 'Unknown'),
                'twitter_mentions': int(item.get('twitter_mentions', 0)),
                'reddit_score': int(item.get('reddit_score', 0)),
                'high_profile_mentions': item.get('high_profile_mentions', '').split(',') if item.get('high_profile_mentions') else [],
                'hours_since_catalyst': int(item.get('hours_since_catalyst', 0)),
            }

            # Score signal
            signal = self.score_signal(context)

            if signal:
                print(f"\n{'='*60}")
                print(f"SIGNAL DETECTED: {signal.coin_name}")
                print(f"Pattern: {signal.pattern_match}")
                print(f"Score: {signal.score}/100 (Confidence: {signal.confidence})")
                print(f"Entry Window: {signal.entry_window}")
                print(f"Action: {signal.recommended_action}")
                print(f"Risk: {signal.risk_level}")
                print(f"Exit Targets: {signal.exit_targets}")
                print(f"{'='*60}\n")

                # Save signal
                self._save_signal(signal)


def example_usage():
    """Example: Detect signals for hypothetical coins"""
    tracker = SignalTracker()

    # Example 1: AI platform release with viral trend (PAT001 scenario)
    print("\n" + "="*60)
    print("EXAMPLE 1: AI Platform Viral Trend")
    print("="*60)

    context1 = {
        'coin_name': 'ANTHROPIC_ART',
        'ai_platform_release': True,
        'twitter_mentions': 3500,
        'reddit_score': 850,
        'high_profile_mentions': ['Elon Musk', 'Sam Altman'],
        'hours_since_catalyst': 8,
    }

    signal1 = tracker.score_signal(context1)
    if signal1:
        print(f"\nCoin: {signal1.coin_name}")
        print(f"Pattern: {signal1.pattern_match}")
        print(f"Score: {signal1.score}/100")
        print(f"Confidence: {signal1.confidence}")
        print(f"Entry Window: {signal1.entry_window}")
        print(f"Action: {signal1.recommended_action}")
        print(f"Risk: {signal1.risk_level}")
        tracker._save_signal(signal1)

    # Example 2: Fitness viral video (PAT002 scenario)
    print("\n" + "="*60)
    print("EXAMPLE 2: Fitness Viral Video")
    print("="*60)

    context2 = {
        'coin_name': 'PROTEIN_SHAKE_COIN',
        'viral_video_views': 2500000,
        'branded_product_identified': True,
        'reddit_threads': 5,
        'reddit_score': 620,
        'twitter_mentions': 1800,
        'hours_since_video': 28,
        'competing_coins': 2,
    }

    signal2 = tracker.score_signal(context2)
    if signal2:
        print(f"\nCoin: {signal2.coin_name}")
        print(f"Pattern: {signal2.pattern_match}")
        print(f"Score: {signal2.score}/100")
        print(f"Confidence: {signal2.confidence}")
        print(f"Entry Window: {signal2.entry_window}")
        print(f"Action: {signal2.recommended_action}")
        print(f"Risk: {signal2.risk_level}")
        tracker._save_signal(signal2)

    # Example 3: AI Agent with VC endorsement (PAT003 scenario)
    print("\n" + "="*60)
    print("EXAMPLE 3: AI Agent Platform with VC Endorsement")
    print("="*60)

    context3 = {
        'coin_name': 'AGENT_FORUM',
        'bot_followers': 15000,
        'platform_launched': True,
        'vc_endorsements': ['a16z'],
        'social_mentions_increase': 450,
        'exchange_listing': True,
        'twitter_mentions': 4200,
        'reddit_score': 720,
        'hours_since_catalyst': 6,
    }

    signal3 = tracker.score_signal(context3)
    if signal3:
        print(f"\nCoin: {signal3.coin_name}")
        print(f"Pattern: {signal3.pattern_match}")
        print(f"Score: {signal3.score}/100")
        print(f"Confidence: {signal3.confidence}")
        print(f"Entry Window: {signal3.entry_window}")
        print(f"Action: {signal3.recommended_action}")
        print(f"Risk: {signal3.risk_level}")
        tracker._save_signal(signal3)

    print(f"\n\nSignals saved to: {SIGNALS_OUTPUT}")


if __name__ == "__main__":
    # Run example
    example_usage()

    # To monitor watchlist:
    # tracker = SignalTracker()
    # tracker.monitor_watchlist()
