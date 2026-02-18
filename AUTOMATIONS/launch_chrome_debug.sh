#!/bin/bash
# Launch Chrome with remote debugging enabled
# This allows Playwright to connect to your running Chrome instance

echo "🚀 Launching Chrome with remote debugging..."
echo "Port: 9222"
echo ""

# Close existing Chrome if running
osascript -e 'quit app "Google Chrome"' 2>/dev/null
sleep 2

# Launch Chrome with remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" \
  > /dev/null 2>&1 &

sleep 3

echo "✅ Chrome launched with remote debugging"
echo "✅ You can now run: python3 AUTOMATIONS/parallel_twitter_scraper.py"
echo ""
echo "Your Chrome will work normally. The scraper will connect in the background."
