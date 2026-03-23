# Ralph Loop: Cold Outreach Engine (auto_outbound_cold_outreach_engine_9569)

Read state from AUTOMATIONS/agent/autonomy/auto_outbound_cold_outreach_engine_9569/
Execute the next step in the pipeline: prospect → qualify → build_asset → outreach → followup → track

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/auto_outbound_cold_outreach_engine_9569/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_auto_outbound_cold_outreach_engine_9569.log
4. Exit cleanly so the next loop iteration gets fresh context


Type: OUTBOUND
Interval: 12h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
