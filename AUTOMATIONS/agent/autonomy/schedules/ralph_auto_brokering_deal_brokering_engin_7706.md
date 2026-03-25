# Ralph Loop: Deal Brokering Engine (auto_brokering_deal_brokering_engin_7706)

Read state from AUTOMATIONS/agent/autonomy/auto_brokering_deal_brokering_engin_7706/
Execute the next step in the pipeline: scrape_targets → qualify_leads → connect_parties → earn_fee → track_revenue

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/auto_brokering_deal_brokering_engin_7706/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_auto_brokering_deal_brokering_engin_7706.log
4. Exit cleanly so the next loop iteration gets fresh context


Type: BROKERING
Interval: 6h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
