#!/bin/bash

echo "🚀 Starting Brave with debugging..."
pkill -9 "Brave Browser" 2>/dev/null
sleep 2

# Start Brave with debugging
/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222 &

echo "✅ Brave started with debugging on port 9222"
echo ""
echo "📋 Next steps:"
echo "1. Log into X in the new Brave window"
echo "2. Open bookmarks in one tab: https://x.com/i/bookmarks"
echo "3. Open DMs in another tab: https://x.com/messages"
echo "4. Run: python3 master_funnel_analyzer.py"
