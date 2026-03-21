#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Auto-append engagement CTA (like/RT/follow prompt) to all generated social posts via PostToolUse hook on content_multiplier, engagement_bait_converter, and content_repurposer outputs. Extracts the pattern: high-signal AI/LLM accounts systematically close every post with a soft CTA to amplify algorithmic reach.
# Created: 2026-03-21T12:40:48.645403
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook_if_you_found_this_useful_a_li.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
