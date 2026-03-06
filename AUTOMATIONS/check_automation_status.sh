#!/bin/bash
# Quick check: are automations actually installed and running?
echo "=== AUTOMATION STATUS ==="
echo ""

# Crontab
CRON_LINES=$(crontab -l 2>/dev/null | wc -l | tr -d ' ')
if [ "$CRON_LINES" -gt 10 ]; then
    echo "CRONTAB: INSTALLED ($CRON_LINES lines)"
else
    echo "CRONTAB: EMPTY OR MISSING ($CRON_LINES lines)"
    echo "  FIX: bash AUTOMATIONS/install_automation.sh"
fi

# LaunchAgents
echo ""
for label in com.printmaxx.scrapers com.printmaxx.claude-sessions; do
    if launchctl print "gui/$(id -u)/$label" >/dev/null 2>&1; then
        echo "LAUNCHD $label: RUNNING"
    else
        echo "LAUNCHD $label: NOT RUNNING"
        echo "  FIX: bash AUTOMATIONS/install_automation.sh"
    fi
done

# Last log activity
echo ""
echo "LAST LOG ACTIVITY:"
BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
for log in "$BASE/AUTOMATIONS/logs/"*.log; do
    if [ -f "$log" ]; then
        MOD=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$log" 2>/dev/null)
        NAME=$(basename "$log")
        echo "  $MOD  $NAME"
    fi
done | sort -r | head -10

echo ""
echo "=== END ==="
