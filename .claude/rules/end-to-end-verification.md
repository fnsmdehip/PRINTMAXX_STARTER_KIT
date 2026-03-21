# End-to-End Verification Rule (ALWAYS active)

## The Claim Rule: NEVER claim something "worked" or "is done" without verifying the ACTUAL output.

### Before claiming ANY pipeline/automation worked:
1. **Check the OUTPUT, not the log.** "Pipeline complete" in a log means the code ran. It does NOT mean it produced the expected files/results.
2. **Count the actual artifacts.** If the pipeline should create 100 scripts, `ls | wc -l` the scripts. If it says 0, it failed.
3. **Test one artifact.** Pick one output file and verify it's not a stub/boilerplate.
4. **Check error counts.** `grep -c ERROR log` BEFORE reporting success. 553 errors is not success.
5. **Verify the FULL chain.** analysis → integration → script gen → cron wiring → execution. If script gen failed, the chain broke and nothing downstream works.

### Specific anti-patterns to NEVER repeat:
- Saying "1,295 entries integrated" when 0 executable scripts were generated
- Saying "DAG pipelines created" when the runners are boilerplate stubs
- Saying "handoff chains created" when no executor runs them
- Reporting plan/config file counts as "assets created" without noting they're inert
- Marking entries as INTEGRATED when only analysis + plan creation succeeded

### The Three-Level Verification:
1. **PLANNED** — a plan/config/JSON exists describing what should happen
2. **BUILT** — actual executable code exists (Python script, n8n workflow, cron entry)
3. **VERIFIED** — the code was run at least once and produced expected output

Only level 3 counts as "done." Level 1 and 2 must be explicitly labeled as such.

### When reporting pipeline results:
```
VERIFIED (actually works):
  - 4 new cron entries installed and tested
  - 2 scanners (EDGAR, Crunchbase) ran successfully

BUILT (code exists, not yet verified):
  - autonomous_integrator.py V2 rewrite
  - KPI rollover logic

PLANNED (configs/plans only, no executable code):
  - 292 DAG pipelines (JSON + stub runners)
  - 89 handoff chains (JSON configs)
  - 576 growth plans (markdown)
```

### For concurrent/parallel systems:
- Set timeouts to 3x the expected single-call duration
- Test with 1 worker first, verify output, THEN scale to N workers
- If ANY call fails, check if it's a systemic issue before continuing
- Don't burn 50 concurrent calls if the first 5 show a pattern of failure

### For `claude -p` specifically:
- Single call latency: ~20-30s for code gen, ~45-90s for analysis
- Max practical concurrency: ~5-8 before queue delays cause timeouts
- Use Sonnet for code generation (faster, equivalent quality for structured code)
- Use Haiku for classification/routing (cheapest)
- Use Opus only for complex analysis requiring deep reasoning
- Timeout = 300s minimum for code generation

## This rule exists because:
We claimed 1,295 entries were "fully integrated" with "2,582 assets created" when the reality was 0 executable scripts, 0 deployed workflows, and hundreds of inert plan files. The user lost hours of their work window because we burned through API limits processing entries that produced no executable output. Never again.
