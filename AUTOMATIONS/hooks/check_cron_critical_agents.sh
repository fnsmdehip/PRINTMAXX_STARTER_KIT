#!/bin/bash
# SessionStart hook: Verify critical agents are in cron/launchd
# Issue: CEO agent and venture autonomy were missing from cron and nobody noticed.
# This hook checks for the CRITICAL agents that must always be scheduled.

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
MISSING=""

# Critical scripts that MUST be in cron
CRITICAL_SCRIPTS=(
    "ceo_agent.py"
    "venture_autonomy.py"
    "daily_digest.py"
    "loop_closer.py"
    "system_health_monitor.py"
)

CRON=$(crontab -l 2>/dev/null)

for script in "${CRITICAL_SCRIPTS[@]}"; do
    if ! echo "$CRON" | grep -q "$script"; then
        # Check launchd as fallback
        PLIST_MATCH=$(ls ~/Library/LaunchAgents/ 2>/dev/null | grep -i "${script%.py}" 2>/dev/null)
        if [ -z "$PLIST_MATCH" ]; then
            MISSING="$MISSING  - $script (not in cron OR launchd)\n"
        fi
    fi
done

if [ -n "$MISSING" ]; then
    echo "CRITICAL AGENTS MISSING FROM SCHEDULER:"
    echo -e "$MISSING"
    echo "These agents should run 24/7. Add them to cron or launchd."
    echo "Check: $BASE/AUTOMATIONS/crontab_printmaxx_v2.txt"
fi
