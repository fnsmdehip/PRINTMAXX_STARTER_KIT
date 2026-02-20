# PRINTMAXX NAV CONTEXT (compact agent reference)
# Generated: 2026-02-19 18:47
# Project: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

## Directory Map

| Directory | Contents |
|-----------|----------|
| `AUTOMATIONS/` | 195 Python scripts — scrapers, pipelines, monitors, tools |
| `OPS/` | Operational state — HEARTBEAT, active-tasks, task tracker, playbooks |
| `LEDGER/` | Source of truth — all CSVs: alpha, methods, niches, metrics |
| `LEDGER/MEGA_SHEET/` | 10 consolidated CSVs (2,512 rows) — query for broad lookups |
| `LEDGER/RBI_STRATEGIC/` | Strategic outputs — GTM tactics, hypotheses, learnings |
| `CONTENT/` | 612+ content files — truth pages, social, longtail, email |
| `CONTENT/social/` | Per-niche content packages — 13 accounts with first-week content |
| `PRODUCTS/` | Product listings — Gumroad, Fiverr, Etsy, Redbubble, KDP |
| `PRODUCTS/FREELANCE_LISTINGS_READY/` | Copy-paste freelance listings for 10 platforms |
| `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` | 13 Gumroad products ready to upload |
| `MONEY_METHODS/` | Playbooks per revenue method — APP_FACTORY, LOCAL_BIZ, etc. |
| `MONEY_METHODS/APP_FACTORY/` | 6 PWA apps + design system + GTM + submission guides |
| `MONEY_METHODS/LOCAL_BIZ/` | 6 templates + personalizer + lead scraper + pricing |
| `DIGITAL_PRODUCTS/` | Gumroad listings, micro products, PDFs ready to sell |
| `FINANCIALS/` | Revenue, expenses, P&L, investments, tax tracking |
| `LANDING/printmaxx-site/` | Next.js landing site — App Router, Turbopack |
| `ralph/` | Autonomous overnight loops — 13 loop configs |
| `scripts/` | Utility scripts — builders, audit, RBI engine, SEO generator |
| `scripts/builders/` | 11 Python scripts that regenerate any .xlsx from scratch |
| `SECRETS/` | Credentials (gitignored) — CREDENTIALS.env, PAYMENT_INFO.md |
| `AUDIT/` | Deep scan reports — alpha gaps, automation inventory |
| `builds/` | Programmatic SEO (602 pages), app builds, content assets |

## Memory System (read in this order)

1. `OPS/HEARTBEAT.md` — <20 lines, pure numbers, 3-second system pulse
2. `OPS/active-tasks.md` — crash recovery: what was running, what's left
3. `OPS/PERSISTENT_TASK_TRACKER.md` — all tasks, statuses, blockers
4. `LEDGER/ALPHA_STAGING.csv` — unprocessed alpha count
5. `OPS/AUTONOMOUS_TASK_QUEUE.jsonl` — current task queue
6. `AUTOMATIONS/logs/daily/YYYY-MM-DD.md` — today's execution log

## Key Scripts (most-used)

| Command | Purpose |
|---------|---------|
| `python3 AUTOMATIONS/daily_agent_runner.py --status` | Auto-orient in 10 seconds |
| `python3 AUTOMATIONS/memory_manager.py --full` | Refresh all 3 memory layers |
| `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000` | Lead qualification pipeline |
| `python3 AUTOMATIONS/system_health_monitor.py --quick` | 3-second health pulse |
| `python3 AUTOMATIONS/venture_performance_tracker.py --recommend` | Score methods, KILL/MAINTAIN/DOUBLE_DOWN |
| `python3 AUTOMATIONS/twitter_alpha_scraper.py --all` | Scrape 116+ Twitter accounts via Brave |
| `python3 AUTOMATIONS/background_reddit_scraper.py --scrape` | Reddit JSON API (no auth needed) |
| `python3 AUTOMATIONS/daily_research_orchestrator.py --full` | 5 scrapers + HN + 41 subs + PH |
| `python3 AUTOMATIONS/alpha_auto_processor.py --process-new` | Route alpha to ventures/OPS/cron/archive |
| `python3 AUTOMATIONS/competitor_monitor.py --scan` | 19 apps, 6 niches, iTunes API |
| `python3 AUTOMATIONS/ecom_arb_engine.py --scan --top 10` | Amazon/eBay pricing, margin calc |
| `python3 AUTOMATIONS/freelance_demand_scanner.py --scan` | 9 subreddits, hiring posts |
| `python3 AUTOMATIONS/trend_aggregator.py --scan` | Google Trends + Reddit + PH |
| `python3 AUTOMATIONS/compliance_deadline_tracker.py --check` | 21 regulatory deadlines |
| `python3 AUTOMATIONS/telegram_community_monitor.py --scan` | 26 channels, 8 niches |
| `python3 AUTOMATIONS/workflow_wirer.py --wire` | Wire all pipelines into task queue |
| `python3 AUTOMATIONS/meta_planner.py --meta-plan` | Full meta plan from MASTER_OPS |
| `python3 AUTOMATIONS/printmaxx.py status` | Unified CLI (12 subcommands wrapping 28+ scripts) |

## Key Data Files

| File | Contents |
|------|----------|
| `LEDGER/ALPHA_STAGING.csv` | All alpha entries with status and score |
| `LEDGER/MEGA_SHEET/*.csv` | 10 consolidated tabs (2,512 rows total) |
| `LEDGER/REVENUE_STREAMS_TRACKER.csv` | 100 revenue streams pre-populated |
| `LEDGER/FREELANCE_PIPELINE_ACTIVE.csv` | Active freelance opportunities |
| `LEDGER/ECOM_ARB_OPPORTUNITIES.csv` | Ecom arb scan results |
| `LEDGER/TREND_SIGNALS.csv` | Multi-source trend detection |
| `LEDGER/COMPLIANCE_DEADLINES.csv` | 21 regulatory deadlines |
| `LEDGER/TELEGRAM_SIGNALS.csv` | Telegram channel signals |
| `LEDGER/RBI_STRATEGIC/LEARNINGS.jsonl` | Append-only learnings database |
| `FINANCIALS/REVENUE_TRACKER.csv` | All revenue by method |
| `FINANCIALS/EXPENSE_TRACKER.csv` | All expenses |
| `AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv` | Score >= 65 leads |
| `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` | Cold email pipeline |

## XLSX Spreadsheets (project root)

- `PRINTMAXX_MASTER_OPS.xlsx` — 150+ ops across 12 sheets — THE master plan
- `PRINTMAXX_STRATEGIC_RBI.xlsx` — Viability matrix, bottlenecks, hypotheses
- `PRINTMAXX_FREELANCE_ARB.xlsx` — 30 services, 10 platforms
- `PRINTMAXX_OPS_PLAYBOOK.xlsx` — 22 ops, 1813 deep playbook rows
- `PRINTMAXX_BRAND_NAMES.xlsx` — 207 brand names

## Quick Lookup (Where is...?)

| What | Where |
|------|-------|
| Latest handoff | `OPS/SESSION_HANDOFF_FEB12_2026.md` |
| System pulse | `OPS/HEARTBEAT.md` |
| All alpha | `LEDGER/ALPHA_STAGING.csv` |
| Revenue | `FINANCIALS/REVENUE_TRACKER.csv` |
| Human tasks | `OPS/ACCOUNT_CREATION_NOW.md` |
| Copy style | `.claude/rules/copy-style.md` |
| Agent playbook | `OPS/AGENT_DAILY_PLAYBOOK.md` |
| Task tracker | `OPS/PERSISTENT_TASK_TRACKER.md` |
| Deploy log (16 sites) | `OPS/DEPLOY_LOG.md` |
| App Factory index | `MONEY_METHODS/APP_FACTORY/APP_FACTORY_CENTRAL_INDEX.md` |
| Product index | `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md` |
| Content index | `CONTENT/CONTENT_CENTRAL_INDEX.md` |
| Leads index | `OPS/LEADS_OUTREACH_CENTRAL_INDEX.md` |
| Cron orchestrator | `printmaxx_cron.sh` |
| Quant terminal | `python3 AUTOMATIONS/printmaxx_quant_terminal.py` |
| Fiverr gigs (10) | `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md` |
| Gumroad products (13) | `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` |
| Etsy listings | `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md` |
| Live dashboard | `python3 AUTOMATIONS/live_dashboard_server.py (localhost:8888)` |

## Current State (from HEARTBEAT)

- Leads: 96,200/1,454,245 analyzed | 9,123 hot | 52,491 warm | 230,506 pipeline
- Revenue: $0 total | 2 entries
- Content: 5 CSVs ready | 287 pending QA
- Apps: 6 built | 6/6 live (OPS/DEPLOYMENT_URLS.md)
- Products: gumroad_drafts=16 | fiverr_drafts=12 | etsy_copy=1
- Alpha: 417 pending review
- Accounts: 0/48 active (BLOCKER: need platform signups)
- Scripts: 195 automation scripts
- Blocker: Account creation → `OPS/ACCOUNT_CREATION_NOW.md`
- Next: `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000 --workers 30`

## Priority Framework

1. **P1 Revenue-blocking:** Unprocessed alpha, failed scrapers, system health
2. **P2 Compounding:** Alpha sources, content gen, lead qualification, trends
3. **P3 Building:** Apps, landing pages, tools, scripts
4. **P4 Analysis:** Competitors, optimization, A/B tests
5. **P5 Maintenance:** Compliance, backups, health checks
6. **P6 Learning:** Retrospectives, prompt effectiveness, learnings

## Guardrails

- All file ops MUST stay within: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt`
- Never propose tasks with risk_level CRITICAL
- Never propose tasks involving payments, account creation, or publishing
- Every task must have clear success_criteria
- Never delete CLAUDE.md, LEDGER/, FINANCIALS/, SECRETS/, XLSX files
