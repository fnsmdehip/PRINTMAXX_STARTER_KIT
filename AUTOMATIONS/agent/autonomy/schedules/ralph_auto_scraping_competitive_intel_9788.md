# Ralph Loop: Competitive Intel (auto_scraping_competitive_intel_9788)

Read state from AUTOMATIONS/agent/autonomy/auto_scraping_competitive_intel_9788/
Execute the next step in the pipeline: configure → scrape → clean → analyze → store → alert

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/auto_scraping_competitive_intel_9788/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_auto_scraping_competitive_intel_9788.log
4. Exit cleanly so the next loop iteration gets fresh context


Type: SCRAPING
Interval: 2h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
