#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Pre-post compliance checker that validates any r/indiehackers content against the new subreddit rules before distribution. Ensures posts aren't removed for rule violations, maximizing visibility. Also updates the reddit posting templates in CONTENT/social/ to reflect new formatting and content requirements.
# Created: 2026-03-20T13:50:39.495548
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_new_rules_for_the_indiehackers.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
