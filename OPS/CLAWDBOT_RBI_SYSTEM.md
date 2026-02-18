# CLAWDBOT-STYLE RBI SYSTEM (PRINTMAXX)

Updated: 2026-02-16

## Objective
- Run a clawdbot-style growth surface across all major online monetization lanes.
- Keep execution bootstrapped by default.
- Enforce draft-first plus human approval for high-risk or payment actions.

## Live Engine
- `AUTOMATIONS/clawdbot_rbi_engine.py`
- Runs inside Ship Captain as `clawdbot_rbi`.
- Generates queue artifacts, not direct posting/submission.

## Use-Case Coverage
1. Buying-intent sniping:
- Output: `output/clawdbot/intents/reply_queue.csv`
- Sources: `LEDGER/ALPHA_STAGING.csv`, Reddit scan JSON.
- Mode: compliant draft replies with disclosure line.

2. Multi-platform content syndication:
- Output: `output/clawdbot/syndication/syndication_wave.csv`
- Scope: multi-platform wave schedule and style mapping.
- Mode: draft-only, no autopublish.

3. Directory swarm submissions:
- Output: `output/clawdbot/directories/submission_wave.csv`
- Source: `LEDGER/LAUNCH_DIRECTORIES_MASTER.csv` + discovered products.
- Mode: staged wave with day offsets; human submit.

4. Job-posting sniper:
- Output: `output/clawdbot/jobs/job_sniper_queue.csv`
- Sources: `LEDGER/TRIGGERING_EVENTS.csv` + hiring signals from alpha.
- Mode: pitch drafts only.

5. SEO keyword-gap exploitation:
- Output: `output/clawdbot/seo/keyword_gap_queue.csv`
- Source: SEO/ASO-related alpha plus generated seed expansions.
- Mode: content queue, no auto publish.

6. Community signal extraction:
- Output: `output/clawdbot/community/community_signal_queue.csv`
- Sources: `LEDGER/TELEGRAM_SIGNALS.csv` + Reddit scan JSON.
- Mode: value-first response drafts with disclosure.

7. Compounding skill memory:
- Output: `OPS/skills/CLAWDBOT_RBI_SKILL.md`
- Captures handles, formulas, and run-level signal patterns.

## Ship Captain Integration
- `AUTOMATIONS/ship_captain.py` now includes:
- `triggering_events` lane step (network-guarded)
- `clawdbot_rbi` lane step (local queue generation)
- `growth` parallel lane in swarm mode.

## Dashboard + Brief Integration
- Dashboard panel: `Clawdbot RBI`
- Source: `output/clawdbot/manifest.json`
- Human brief section: `Clawdbot RBI Pack (Draft Queues)`

## Guardrails
- No auto-posting from this engine.
- No auto-form submission from this engine.
- No payment, deploy, or outbound live-send changes in this engine.
- High-risk content patterns are auto-filtered from draft queues.
- Existing Ship Captain approval gates remain source of truth.
