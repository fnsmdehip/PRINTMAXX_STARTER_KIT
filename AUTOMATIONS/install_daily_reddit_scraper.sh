#!/bin/bash
# Install daily Reddit scraper to run automatically every morning at 6:15 AM

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create cron job (15 minutes after Twitter scraper)
CRON_COMMAND="15 6 * * * cd $PROJECT_DIR && /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 AUTOMATIONS/daily_reddit_scraper.py >> AUTOMATIONS/scraper_daily_reddit.log 2>&1"

# Check if cron job already exists
(crontab -l 2>/dev/null | grep -F "daily_reddit_scraper.py") && {
    echo "✓ Cron job already installed"
    exit 0
}

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

echo "✅ Daily Reddit scraper installed"
echo "Runs every day at 6:15 AM"
echo "Logs: AUTOMATIONS/scraper_daily_reddit.log"
echo ""
echo "To test now: python3 AUTOMATIONS/daily_reddit_scraper.py"
