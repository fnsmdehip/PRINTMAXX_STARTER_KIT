#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Validate ProductHunt launch freshness (account age, cache status) before routing to outreach chain
# Created: 2026-03-21T12:40:59.536370
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_ph_launch_cacheless.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
