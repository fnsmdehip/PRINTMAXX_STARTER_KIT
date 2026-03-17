# Technical Quick Reference

Stack: Python | LLM: Claude Code (subscription, model-agnostic in theory) | Browser: 8-level fallback (Playwriter MCP, Brave cookies, Vercel Agent-Browser, Chrome CDP, Playwright, Selenium, Browserbase, requests) | Revenue: $0 | Apps: 114 deployed | Scripts: 392

## Essential Commands
- Decision engine: `python3 AUTOMATIONS/decision_engine.py --cycle`
- Heartbeat: `cat OPS/HEARTBEAT.md`
- Health: `python3 AUTOMATIONS/system_health_monitor.py --quick`
- Ventures: `python3 AUTOMATIONS/venture_autonomy.py --status`
- Swarm: `python3 AUTOMATIONS/agent_swarm.py --status`
- Control panel: `python3 AUTOMATIONS/control_panel.py` (localhost:9999)
- Unified CLI: `python3 AUTOMATIONS/printmaxx.py status`

## Intelligence
- Router: `python3 AUTOMATIONS/intelligence_router.py --venture TYPE --task TASK --brief`
- Alpha: `python3 AUTOMATIONS/alpha_query.py --venture APP_FACTORY --json`
- Master Ops: `python3 AUTOMATIONS/master_ops_bridge.py --brief VENTURE_TYPE`
- App factory: `python3 AUTOMATIONS/app_factory_command_center.py --refresh --top 8`

## Scrapers (run every session)
- Twitter: `python3 AUTOMATIONS/twitter_alpha_scraper.py --all`
- Reddit: `python3 AUTOMATIONS/background_reddit_scraper.py --scrape`
- Alpha process: `python3 AUTOMATIONS/alpha_auto_processor.py --process-new`

## V2 Components
- Gates: `python3 AUTOMATIONS/gates.py --stats`
- Task graph: `python3 AUTOMATIONS/task_graph.py --ready`
- Shakespeare/Observer/Quinn: `--status` on each
- Challengers: `python3 AUTOMATIONS/challenger_agents.py --stats`

## Master Ops Bridge
- Rebuild: `--rebuild` | Stats: `--stats` | Query: `--query CONTENT`
- Ready ops: `--ready` | Synergies: `--synergy` | Blockers: `--blockers`
- Playbook: `--playbook C01` | Brief: `--brief VENTURE_TYPE`
- 19 sheets, 182 ops, 26 synergies, 12h TTL cache, cron 5:15 AM

## Model Routing
Opus: swarm_brain, quality_gate, gap_hunter, growth_strategist
Sonnet: competitor_stalker, lead_machine, cross_pollinator, revenue_tracker, inbound_maximizer
Haiku: system_healer, data_janitor, playwright_tester

Browser fallback (priority order):
1. Playwriter MCP (your running Chrome, existing logins, anti-bot inherent) — github.com/remorses/playwriter
2. Brave cookie + Playwright persistent context (AES decrypted cookies from daily browser)
3. Vercel Agent-Browser CLI (headless, 82% less tokens than Playwright MCP) — github.com/vercel-labs/agent-browser
4. Chrome CDP (connect to running debug instance, localhost:9222)
5. Playwright (general headless automation)
6. Selenium (legacy fallback)
7. Browserbase (cloud anti-detection, proxy rotation, $20/mo) — browserbase.com
8. Python requests/urllib (API-only, no browser needed)
