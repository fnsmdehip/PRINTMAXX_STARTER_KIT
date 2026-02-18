#!/usr/bin/env python3
"""
Trading Signal Scraper for ALGO_TRADING Money Method

Specialized scraper for FinTwit/Crypto Twitter signals.
Filters for: whale alerts, unusual activity, breaking news, on-chain signals.

Based on: AUTOMATIONS/scripts/daily_timeline_scraper.py

Usage:
    python3 trading_signal_scraper.py [--dry-run] [--tier HIGHEST|HIGH] [--visible]

Example:
    python3 trading_signal_scraper.py --tier HIGHEST --visible
"""

import asyncio
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
import argparse

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
HIGH_SIGNAL_SOURCES = LEDGER_DIR / 'HIGH_SIGNAL_SOURCES.csv'
ALGO_TRADING_DIR = BASE_DIR / 'MONEY_METHODS' / 'ALGO_TRADING'
SIGNAL_LOG = ALGO_TRADING_DIR / 'signals' / 'signal_log.csv'
LOGS_DIR = ALGO_TRADING_DIR / 'signals' / 'logs'

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'trading_signal_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('trading_signal_scraper')


@dataclass
class TradingSignal:
    """Represents a trading signal extracted from social media."""
    signal_id: str
    source: str
    source_url: str
    timestamp: str
    signal_type: str  # WHALE, OPTIONS_FLOW, MACRO, ON_CHAIN, LIQUIDATION, BREAKOUT, NEWS
    asset: str  # BTC, ETH, SPY, specific ticker
    direction: str  # BULLISH, BEARISH, NEUTRAL
    confidence: str  # HIGH, MEDIUM, LOW
    raw_content: str
    extracted_data: dict  # Specific numbers, levels, etc.
    status: str  # PENDING, EXECUTED, IGNORED


# Signal type keywords for classification
SIGNAL_PATTERNS = {
    'WHALE': [
        r'whale', r'large transfer', r'moved \d+', r'million', r'billion',
        r'smart money', r'institution', r'\$\d+[MBK]', r'whale alert'
    ],
    'OPTIONS_FLOW': [
        r'unusual options', r'options flow', r'call sweep', r'put sweep',
        r'volume spike', r'OI change', r'gamma', r'delta', r'IV crush'
    ],
    'MACRO': [
        r'FOMC', r'Fed', r'CPI', r'PPI', r'jobs report', r'rate cut',
        r'rate hike', r'inflation', r'GDP', r'Powell', r'Yellen'
    ],
    'ON_CHAIN': [
        r'on-chain', r'exchange inflow', r'exchange outflow', r'HODL',
        r'wallet activity', r'funding rate', r'OI liquidation', r'stablecoin'
    ],
    'LIQUIDATION': [
        r'liquidat', r'liq map', r'short squeeze', r'long squeeze',
        r'margin call', r'cascade', r'funding'
    ],
    'BREAKOUT': [
        r'breakout', r'breakdown', r'support', r'resistance', r'ATH',
        r'all-time high', r'new high', r'new low', r'trend break'
    ],
    'NEWS': [
        r'breaking', r'just in', r'announced', r'launch', r'partnership',
        r'SEC', r'lawsuit', r'ETF', r'approval', r'regulation'
    ]
}

# Direction detection
BULLISH_PATTERNS = [
    r'bullish', r'buy', r'long', r'pump', r'moon', r'breakout',
    r'accumulation', r'inflow', r'ATH', r'approval', r'launch'
]
BEARISH_PATTERNS = [
    r'bearish', r'sell', r'short', r'dump', r'crash', r'breakdown',
    r'distribution', r'outflow', r'lawsuit', r'ban', r'liquidat'
]

# Asset ticker extraction
ASSET_PATTERNS = [
    r'\$([A-Z]{2,5})',  # $BTC, $ETH, $SPY
    r'#([A-Z]{2,5})',   # #BTC, #ETH
    r'\b(BTC|ETH|SOL|AVAX|MATIC|DOGE|XRP|ADA|DOT|LINK)\b',  # Crypto tickers
    r'\b(SPY|QQQ|AAPL|TSLA|NVDA|AMD|META|GOOG|AMZN|MSFT)\b'  # Stock tickers
]

# Trading-focused sources from HIGH_SIGNAL_SOURCES.csv
TRADING_SOURCE_IDS = [
    'SRC097', 'SRC098', 'SRC099', 'SRC100', 'SRC101',  # zerohedge to lookonchain
    'SRC102', 'SRC103', 'SRC104', 'SRC105', 'SRC106',  # whale_alert to IntoTheBlock
    'SRC107', 'SRC108', 'SRC109', 'SRC110', 'SRC111',  # CryptoQuant to arkaborns
    'SRC112', 'SRC113', 'SRC114', 'SRC115', 'SRC116'   # tier10k to OptionsAction
]


def classify_signal_type(content: str) -> str:
    """Classify the signal type based on content patterns."""
    content_lower = content.lower()
    scores = {}

    for signal_type, patterns in SIGNAL_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, content_lower))
        if score > 0:
            scores[signal_type] = score

    if not scores:
        return 'NEWS'  # Default

    return max(scores, key=scores.get)


def detect_direction(content: str) -> str:
    """Detect bullish/bearish direction from content."""
    content_lower = content.lower()

    bullish_score = sum(1 for p in BULLISH_PATTERNS if re.search(p, content_lower))
    bearish_score = sum(1 for p in BEARISH_PATTERNS if re.search(p, content_lower))

    if bullish_score > bearish_score:
        return 'BULLISH'
    elif bearish_score > bullish_score:
        return 'BEARISH'
    else:
        return 'NEUTRAL'


def extract_assets(content: str) -> List[str]:
    """Extract asset tickers from content."""
    assets = set()

    for pattern in ASSET_PATTERNS:
        matches = re.findall(pattern, content)
        assets.update(matches)

    return list(assets) if assets else ['GENERAL']


def extract_numbers(content: str) -> Dict:
    """Extract specific numbers and levels from content."""
    data = {}

    # Price levels
    price_matches = re.findall(r'\$[\d,]+\.?\d*', content)
    if price_matches:
        data['price_levels'] = price_matches[:5]  # Limit to 5

    # Percentages
    pct_matches = re.findall(r'[\d.]+%', content)
    if pct_matches:
        data['percentages'] = pct_matches[:3]

    # Large numbers (millions, billions)
    large_matches = re.findall(r'\$?[\d.]+[MBK]', content)
    if large_matches:
        data['amounts'] = large_matches[:3]

    return data


def parse_tweet_to_signal(
    tweet_content: str,
    source: str,
    source_url: str,
    signal_counter: int
) -> TradingSignal:
    """Parse a tweet into a TradingSignal object."""

    signal_type = classify_signal_type(tweet_content)
    direction = detect_direction(tweet_content)
    assets = extract_assets(tweet_content)
    extracted_data = extract_numbers(tweet_content)

    # Assign confidence based on source tier and content specificity
    if len(extracted_data) >= 2:
        confidence = 'HIGH'
    elif len(extracted_data) >= 1:
        confidence = 'MEDIUM'
    else:
        confidence = 'LOW'

    return TradingSignal(
        signal_id=f"SIG{signal_counter:04d}",
        source=source,
        source_url=source_url,
        timestamp=datetime.now().isoformat(),
        signal_type=signal_type,
        asset=','.join(assets),
        direction=direction,
        confidence=confidence,
        raw_content=tweet_content[:500],  # Truncate long content
        extracted_data=extracted_data,
        status='PENDING'
    )


def get_trading_sources() -> List[Dict]:
    """Get trading-focused sources from HIGH_SIGNAL_SOURCES.csv."""
    sources = []

    if not HIGH_SIGNAL_SOURCES.exists():
        logger.error(f"HIGH_SIGNAL_SOURCES.csv not found at {HIGH_SIGNAL_SOURCES}")
        return sources

    with open(HIGH_SIGNAL_SOURCES, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['source_id'] in TRADING_SOURCE_IDS:
                sources.append(row)

    logger.info(f"Found {len(sources)} trading-focused sources")
    return sources


def get_next_signal_id() -> int:
    """Get the next signal ID from existing log."""
    if not SIGNAL_LOG.exists():
        return 1

    try:
        with open(SIGNAL_LOG, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                last_id = rows[-1]['signal_id']
                return int(last_id.replace('SIG', '')) + 1
    except Exception as e:
        logger.warning(f"Could not read signal log: {e}")

    return 1


def save_signals(signals: List[TradingSignal]):
    """Save signals to the signal log CSV."""
    if not signals:
        return

    file_exists = SIGNAL_LOG.exists()

    with open(SIGNAL_LOG, 'a', newline='') as f:
        fieldnames = [
            'signal_id', 'source', 'source_url', 'timestamp', 'signal_type',
            'asset', 'direction', 'confidence', 'raw_content', 'extracted_data',
            'status'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for signal in signals:
            row = asdict(signal)
            row['extracted_data'] = json.dumps(row['extracted_data'])
            writer.writerow(row)

    logger.info(f"Saved {len(signals)} signals to {SIGNAL_LOG}")


async def scrape_trading_signals(
    tier_filter: str = 'HIGHEST',
    headless: bool = True,
    max_tweets: int = 20,
    dry_run: bool = False
) -> List[TradingSignal]:
    """
    Scrape trading signals from configured sources.

    This is a template that needs to be connected to actual scraping.
    For now, it demonstrates the parsing logic.
    """
    signals = []
    sources = get_trading_sources()

    if not sources:
        logger.warning("No trading sources configured")
        return signals

    # Filter by tier if specified
    if tier_filter:
        sources = [s for s in sources if s.get('signal_quality') == tier_filter]

    logger.info(f"Processing {len(sources)} sources with tier={tier_filter}")

    # Get next signal ID
    signal_counter = get_next_signal_id()

    # NOTE: Actual scraping requires Playwright browser automation
    # This would integrate with the TwitterScraper class from
    # AUTOMATIONS/scripts/source_scrapers/twitter_scraper.py
    #
    # For now, demonstrating the parsing pipeline:

    sample_tweets = [
        "$BTC whale just moved 5,000 BTC ($320M) from Binance to unknown wallet",
        "BREAKING: Unusual options activity on $NVDA - massive call sweeps at $140 strike",
        "Exchange outflow hits 3-month high as institutions accumulate",
        "Fed Powell: 'Data dependent on rate cuts' - markets rally on dovish tone",
        "$ETH breaking above $4,000 resistance - potential breakout confirmed",
        "Liquidation cascade: $500M in longs liquidated in last hour"
    ]

    for i, tweet in enumerate(sample_tweets):
        source = sources[i % len(sources)]
        signal = parse_tweet_to_signal(
            tweet,
            source['source_name'],
            source['url'],
            signal_counter
        )
        signals.append(signal)
        signal_counter += 1

    if dry_run:
        logger.info("DRY RUN - Signals parsed but not saved:")
        for sig in signals:
            logger.info(f"  {sig.signal_id}: {sig.signal_type} | {sig.asset} | {sig.direction}")
    else:
        save_signals(signals)

    return signals


def main():
    parser = argparse.ArgumentParser(description='Trading Signal Scraper')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--tier', default='HIGHEST', help='Signal quality tier filter')
    parser.add_argument('--visible', action='store_true', help='Show browser (not headless)')
    parser.add_argument('--max-tweets', type=int, default=20, help='Max tweets per source')

    args = parser.parse_args()

    logger.info(f"Starting trading signal scraper (tier={args.tier}, dry_run={args.dry_run})")

    signals = asyncio.run(scrape_trading_signals(
        tier_filter=args.tier,
        headless=not args.visible,
        max_tweets=args.max_tweets,
        dry_run=args.dry_run
    ))

    logger.info(f"Completed. Extracted {len(signals)} signals.")

    # Summary
    if signals:
        type_counts = {}
        for sig in signals:
            type_counts[sig.signal_type] = type_counts.get(sig.signal_type, 0) + 1

        logger.info("Signal breakdown:")
        for sig_type, count in sorted(type_counts.items()):
            logger.info(f"  {sig_type}: {count}")


if __name__ == '__main__':
    main()
