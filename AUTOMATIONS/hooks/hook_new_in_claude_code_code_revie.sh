#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: DAG pipeline: (1) Generate content pieces for tech niche about Claude Code review feature (tweets, thread, newsletter), (2) Update existing Claude Code digital product listings with review workflow section, (3) Add PR review hook to PRINTMAXX dev pipeline for internal code quality, (4) Queue content for distribution
# Created: 2026-03-20T18:09:52.025473
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_new_in_claude_code_code_revie.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
