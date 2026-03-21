#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Telegram bot bridge that pushes Claude Code session events (agent completions, cron failures, revenue alerts, heartbeat diffs) to Telegram — immediately useful for monitoring our 33 autonomous agents from mobile. Secondary: package the setup guide as a $9-19 Gumroad product targeting Claude Code power users who run autonomous pipelines.
# Created: 2026-03-21T12:40:57.240336
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_ph_launch_claude_code_channe.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
