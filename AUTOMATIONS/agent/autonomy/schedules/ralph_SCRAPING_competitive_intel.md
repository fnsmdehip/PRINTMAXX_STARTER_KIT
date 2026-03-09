# Ralph Loop: SCRAPING_competitive_intel (SCRAPING_competitive_intel)

Read state from AUTOMATIONS/agent/autonomy/SCRAPING_competitive_intel/
Execute the next step in the pipeline: 

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/SCRAPING_competitive_intel/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_SCRAPING_competitive_intel.log
4. Exit cleanly so the next loop iteration gets fresh context

Type: SCRAPING
Interval: 4h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
