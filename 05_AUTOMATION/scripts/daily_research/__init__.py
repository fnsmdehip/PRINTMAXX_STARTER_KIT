"""
PRINTMAXX Daily Research Scanners

This package contains automated scanners for daily alpha research:
- twitter_scanner.py - Scan X/Twitter accounts
- reddit_scanner.py - Scan subreddits
- hn_scanner.py - Scan Hacker News
- producthunt_scanner.py - Scan Product Hunt

Usage:
    Run individual scanners:
        python twitter_scanner.py [--dry-run] [--tier HIGHEST|HIGH|MEDIUM]
        python reddit_scanner.py [--dry-run] [--tier HIGHEST|HIGH|MEDIUM]
        python hn_scanner.py [--dry-run] [--count 30]
        python producthunt_scanner.py [--dry-run] [--days 1]

    Run the full pipeline:
        python ../research_orchestrator.py [--dry-run] [--parallel]
"""

from pathlib import Path

# Package info
__version__ = '1.0.0'
__author__ = 'PRINTMAXX'

# Paths
PACKAGE_DIR = Path(__file__).parent
BASE_DIR = PACKAGE_DIR.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
CACHE_DIR = PACKAGE_DIR / '.cache'

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)
