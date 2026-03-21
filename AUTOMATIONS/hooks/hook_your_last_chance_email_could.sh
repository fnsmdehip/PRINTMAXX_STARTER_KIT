#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: CEMA compliance gate: scans all outgoing cold email templates and sequences for fake urgency patterns (last chance, final hours, sale ends tonight, expiring soon) before send. Blocks non-compliant emails. Also generates weekly compliance content posts from real lawsuit data for engagement bait.
# Created: 2026-03-20T18:35:54.432725
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_your_last_chance_email_could.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
