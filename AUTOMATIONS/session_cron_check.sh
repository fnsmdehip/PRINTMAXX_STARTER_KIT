#!/bin/bash
# Quick cron check at session start - reinstalls if empty
CRON_LINES=$(crontab -l 2>/dev/null | wc -l | tr -d ' ')
BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

if [ "$CRON_LINES" -lt 10 ]; then
    # Crontab is empty or nearly empty - reinstall
    crontab "$BASE/AUTOMATIONS/crontab_printmaxx_v2.txt" 2>/dev/null
    NEW_COUNT=$(crontab -l 2>/dev/null | wc -l | tr -d ' ')
    echo "CRON WAS EMPTY. Reinstalled: $NEW_COUNT lines."
else
    echo "Cron OK: $CRON_LINES lines installed."
fi

# Check launchd
for label in com.printmaxx.scrapers com.printmaxx.claude-sessions; do
    if ! launchctl print "gui/$(id -u)/$label" >/dev/null 2>&1; then
        PLIST="$HOME/Library/LaunchAgents/$label.plist"
        if [ -f "$PLIST" ]; then
            launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null
            echo "Reloaded launchd: $label"
        fi
    fi
done
