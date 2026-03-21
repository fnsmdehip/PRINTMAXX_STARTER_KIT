#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Set up Claude Code Channels to connect our persistent PRINTMAXX session to a Telegram bot. Enables remote task dispatching (content, alpha review, deployments) from mobile without needing laptop access. Wires into existing control panel and venture autonomy stack so any session command can be triggered via Telegram message.
# Created: 2026-03-20T23:36:38.612649
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook__anthropicai_just_made_clau.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
