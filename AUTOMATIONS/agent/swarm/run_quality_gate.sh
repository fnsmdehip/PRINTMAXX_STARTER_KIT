#!/bin/bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
PROMPT_FILE="AUTOMATIONS/agent/swarm/quality_gate_prompt.md"
if [ -f "$PROMPT_FILE" ]; then
  claude -p "$(cat "$PROMPT_FILE")" >> AUTOMATIONS/logs/swarm_quality_gate.log 2>&1
else
  echo "ERROR: Quality gate prompt file not found at $PROMPT_FILE" >> AUTOMATIONS/logs/swarm_quality_gate.log
fi
