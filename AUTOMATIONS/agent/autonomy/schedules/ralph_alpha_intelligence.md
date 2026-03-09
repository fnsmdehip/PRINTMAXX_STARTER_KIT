# Ralph Loop: Alpha Intelligence Research (alpha_intelligence)

Read state from AUTOMATIONS/agent/autonomy/alpha_intelligence/
Execute the next step in the pipeline: scrape → analyze → report

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/alpha_intelligence/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_alpha_intelligence.log
4. Exit cleanly so the next loop iteration gets fresh context

Type: RESEARCH
Interval: 4h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
