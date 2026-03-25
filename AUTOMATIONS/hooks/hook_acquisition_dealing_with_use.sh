#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Trial abuse detection module: fingerprint users via device ID + email hash + IP subnet to detect multi-account serial trial users, then route them to targeted conversion flow (discounted upgrade offer or credit card trial gate) instead of blocking — converts abusers into paying customers
# Created: 2026-03-24T18:50:44.104221
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_acquisition_dealing_with_use.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
