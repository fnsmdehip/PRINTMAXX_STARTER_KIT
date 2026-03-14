# Ralph Loop: App Factory (auto_app_app_factory_9788)

Read state from AUTOMATIONS/agent/autonomy/auto_app_app_factory_9788/
Execute the next step in the pipeline: find_gap → spec → build → deploy → aso → track

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

Before choosing the next step:
1. Run `python3 AUTOMATIONS/app_factory_autopilot.py --run`
2. Read `OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md`
3. Use `AUTOMATIONS/agent/autonomy/app_factory_priority_queue.json` as the ranking source of truth
4. If the top item maps to an existing app, iterate that app before greenfield work
5. Enforce hard gates: real billing path, native-feeling UX, privacy URL, post-value review prompt timing

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/auto_app_app_factory_9788/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_auto_app_app_factory_9788.log
4. Exit cleanly so the next loop iteration gets fresh context

Type: APP
Interval: 12h
Working dir: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
