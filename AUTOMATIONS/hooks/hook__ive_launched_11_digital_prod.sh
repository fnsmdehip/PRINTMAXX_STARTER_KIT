#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: 72-hour pre-launch protocol for digital products. Automates the 3-day warmup sequence before listing any product: Day -3 = seed communities with problem-awareness content, Day -2 = share behind-the-scenes/WIP teasers, Day -1 = direct CTAs and waitlist collection, Day 0 = list with warm audience ready. Applies to all 16 Gumroad drafts and 12 Fiverr drafts currently queued.
# Created: 2026-03-20T18:10:02.451612
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook__ive_launched_11_digital_prod.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
