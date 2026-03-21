#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Wire Claude Code Channels into PRINTMAXX Telegram bot for remote agent control on the go; simultaneously generate high-engagement content riding Anthropic's announcement wave and create a Gumroad setup guide
# Created: 2026-03-21T12:40:48.729430
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook__anthropicai_just_made_clau.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
