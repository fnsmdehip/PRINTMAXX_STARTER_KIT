#!/bin/bash
# PRINTMAXX BACKGROUND RESEARCH RUNNER
# =====================================
# Runs ALL research scrapers in background - NO interference with your work
#
# Usage:
#   ./run_all_research_background.sh        # Run all scrapers
#   ./run_all_research_background.sh quick  # Quick scrape (top 20 accounts only)
#
# Check progress:
#   tail -f /tmp/printmaxx_research.log
#
# Stop all:
#   pkill -f "background_twitter_scraper\|background_reddit_scraper"

cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

LOG_FILE="/tmp/printmaxx_research.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "========================================" >> $LOG_FILE
echo "PRINTMAXX BACKGROUND RESEARCH - $TIMESTAMP" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# Check if Twitter scraper profile exists
if [ ! -d "$HOME/.printmaxx-scraper-profile" ]; then
    echo "⚠️  Twitter scraper not set up yet!"
    echo "Run: python3 AUTOMATIONS/background_twitter_scraper.py --setup"
    echo ""
    echo "This opens a browser ONE TIME for you to log in."
    echo "After that, all scraping runs in the background."
    exit 1
fi

MODE=${1:-full}

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PRINTMAXX BACKGROUND RESEARCH RUNNER                      ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  Mode: $MODE                                               "
echo "║  All scrapers run HEADLESS in background                   ║"
echo "║  Your computer is FREE to use normally                     ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  Check progress: tail -f /tmp/printmaxx_research.log       ║"
echo "║  Stop all: pkill -f background_twitter                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Run Twitter scraper in background
if [ "$MODE" == "quick" ]; then
    echo "Starting Twitter scraper (top 20 accounts)..."
    nohup python3 AUTOMATIONS/background_twitter_scraper.py --scrape >> $LOG_FILE 2>&1 &
else
    echo "Starting Twitter scraper (ALL 190 accounts)..."
    nohup python3 AUTOMATIONS/background_twitter_scraper.py --full >> $LOG_FILE 2>&1 &
fi
TWITTER_PID=$!
echo "  → Twitter PID: $TWITTER_PID"

# Run Reddit scraper if it exists and is set up
if [ -f "AUTOMATIONS/background_reddit_scraper.py" ]; then
    echo "Starting Reddit scraper..."
    nohup python3 AUTOMATIONS/background_reddit_scraper.py --scrape >> $LOG_FILE 2>&1 &
    REDDIT_PID=$!
    echo "  → Reddit PID: $REDDIT_PID"
fi

echo ""
echo "✅ All scrapers running in background!"
echo ""
echo "Monitor: tail -f $LOG_FILE"
echo "Results: Check LEDGER/ALPHA_STAGING.csv"
echo ""
