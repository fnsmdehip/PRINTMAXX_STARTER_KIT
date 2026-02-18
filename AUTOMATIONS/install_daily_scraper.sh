#!/bin/bash
# Install daily Twitter scraper to run automatically every morning at 6 AM

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create cron job
CRON_COMMAND="0 6 * * * cd $PROJECT_DIR && /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 AUTOMATIONS/daily_twitter_scraper.py >> AUTOMATIONS/scraper_daily.log 2>&1"

# Check if cron job already exists
(crontab -l 2>/dev/null | grep -F "daily_twitter_scraper.py") && {
    echo "✓ Cron job already installed"
    exit 0
}

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

echo "✅ Daily scraper installed"
echo "Runs every day at 6 AM"
echo "Logs: AUTOMATIONS/scraper_daily.log"
echo ""
echo "To test now: python3 AUTOMATIONS/daily_twitter_scraper.py"
