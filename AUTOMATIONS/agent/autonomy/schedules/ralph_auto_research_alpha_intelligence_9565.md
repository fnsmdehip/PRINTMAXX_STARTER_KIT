# Ralph Loop: Alpha Intelligence (auto_research_alpha_intelligence_9565)

Read state from AUTOMATIONS/agent/autonomy/auto_research_alpha_intelligence_9565/
Execute the next step in the pipeline: scrape → analyze → score → route → compound

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/auto_research_alpha_intelligence_9565/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_auto_research_alpha_intelligence_9565.log
4. Exit cleanly so the next loop iteration gets fresh context


Type: RESEARCH
Interval: 24h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
