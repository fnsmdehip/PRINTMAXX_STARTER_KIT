# ClawWork Minimal Sidecar Plan (PRINTMAXX)

Updated: 2026-02-16

## Objective

- Add ClawWork-style economic validation without replacing the existing Ship Captain stack.
- Keep total stack spend capped at $200/mo by hard-capping sidecar evaluation to $20/mo.
- Route recommendations back into existing execution lanes: freelance, Gumroad, cold outreach, RBI.

## What Is Integrated

1. Sidecar evaluator script:
   - `AUTOMATIONS/clawwork_sidecar.py`
2. Sidecar policy + budget caps:
   - `OPS/CLAWWORK_SIDECAR_POLICY.json`
3. Ship Captain lane wiring:
   - `AUTOMATIONS/ship_captain.py` step id `clawwork_sidecar`
4. Human brief visibility:
   - `AUTOMATIONS/human_brief.py` now includes sidecar budget/profit summary
5. Fleet observability:
   - `AUTOMATIONS/cron_fleet_report.py` includes sidecar artifacts + run ledger

## Budget Envelope

- Global stack cap: `$200/mo` (unchanged)
- Sidecar cap (sub-budget): `$20/mo`
- Sidecar soft cap: `$15/mo`
- Sidecar hard stop: `$18/mo`
- Per-run sidecar max: `$1.00`
- Estimated eval cost per sampled task: `$0.012`

If sidecar reaches hard stop, sampling automatically drops to zero and only reporting continues.

## Lane Mapping

1. `freelance_arbitrage`
   - Source: `output/freelance/manifest.json` (`draft_count`)
2. `gumroad_listings`
   - Source: `output/ecom_autolist/manifest.json` (`pending_count`)
3. `cold_outreach_warmup`
   - Source: `output/cold_emails/cold_emails_ready.csv` (row count)
4. `rbi_intent_sniping`
   - Source: `output/clawdbot/manifest.json` (`counts.intent_rows`)

Each lane is scored for expected revenue, eval cost, and expected profit.

## Operational Cadence

- Ship Captain already triggers sidecar once per run.
- Recommended direct cron cadence (if using standalone): every 2-4 hours.

Standalone command:

```bash
python3 AUTOMATIONS/clawwork_sidecar.py --tick
```

Dry-run command (no ledger write):

```bash
python3 AUTOMATIONS/clawwork_sidecar.py --tick --dry-run
```

## External ClawWork Runner (Optional)

Default is disabled. To enable:

1. Clone ClawWork outside this repo.
2. Set `external_runner.enabled=true` and `external_runner.clawwork_home` in:
   - `OPS/CLAWWORK_SIDECAR_POLICY.json`
3. Run:

```bash
python3 AUTOMATIONS/clawwork_sidecar.py --tick --invoke-external
```

Keep this optional path behind sidecar budget constraints and do not run in high frequency mode.

## First 3 Revenue Triggers (2-Hour Human Unblock)

1. Freelance arbitrage drafts:
   - `python3 AUTOMATIONS/freelance_demand_scanner.py --hourly`
   - `python3 AUTOMATIONS/auto_freelance_responder.py --dry-run`
2. Gumroad listing prep:
   - `python3 AUTOMATIONS/gumroad_autolist_packager.py --write`
3. Cold outreach warmup:
   - `python3 AUTOMATIONS/email_sender.py --preview --outreach AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv --max-sends 25`

## Guardrails

- Sidecar never performs live sends, auto-posting, form submission, or payment actions.
- Account and payment actions remain gated by `HUMAN_APPROVALS.csv`.
- Sidecar output is advisory and budget-governed.

## Output Artifacts

- `output/clawwork_sidecar/manifest.json`
- `output/clawwork_sidecar/latest.md`
- `LEDGER/CLAWWORK_SIDECAR_RUNS.csv`
