#!/bin/bash
# Auto-generated hook by autonomous_integrator V2
# Purpose: Auto-append newsletter CTA to every outgoing post — 'if you liked this, you'll love [newsletter name]' — using PostToolUse hook on content generation. Hook fires after any content write to CONTENT/social/posting_queue/, appends CTA line with Beehiiv signup URL. Tracks which posts drive signups via UTM params per post.
# Created: 2026-03-20T23:12:24.838465
# Hook type: PreToolUse
#
# To wire into settings.json, add to hooks.PreToolUse:
#   {"matcher": "Write", "command": "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/hooks/hook__if_you_liked_this_post_youl.sh"}

# Read tool input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

# Exit 0 = allow, exit 2 = block with message
exit 0
