# PRINTMAXX — COMPLETE SYSTEM MAP
# Canonical live architecture map. Update this file in the same session whenever the system changes.
# One solopreneur. Zero revenue. 33 autonomous agents. 394 Python scripts. 107 cron jobs (zero collisions). 27GB.
# Goal: $0 → hedge fund capital management via recursive automation.

---

## CANONICAL STATUS

This is the live system map for PRINTMAXX.

- Update this file immediately when agents, automations, schedules, queues, dashboards, memory layers, control surfaces, key directories, or data flow change.
- If the change also affects navigation or standing instructions, update `.claude/CLAUDE.md` in the same session.
- Latest verified control-surface update: 2026-03-18 EDT.

---

## WHAT IT IS

A fully autonomous solopreneur operations system that scrapes intelligence, generates content, manages ventures, deploys assets, and makes strategic decisions 24/7 without human input — running primarily on a $200/mo Claude Max plan via `claude -p` CLI calls through launchd and cron, with a Codex automation layer handling recurring meta-planning and task-queue generation.

The human does: account creation, payments, API keys, posting from personal accounts.
The system does: everything else.

---

## OPERATING ETHOS (Capital Genesis)

PRINTMAXX operates as a **hedge fund of revenue lanes**, not a single-bet startup.

**Portfolio theory:** 10+ revenue lanes simultaneously. Each lane has ~30% solo success rate. 10 lanes = 97% chance of at least one hit, 70% chance of 3+. By Phase 5, no single method exceeds 30% of total revenue. The portfolio survives any single-method extinction event.

**Cross-pollination:** Every method feeds at least one other. Content → personas → newsletters → flash sales → apps → community → outreach → back to content. Stacked Revenue = Sum(Individual) × Synergy Multiplier (1.3-2.5x) × Automation Factor (1.0-3.0x). Standalone methods are dead weight.

**Shared infrastructure:** Same $240-280/mo tooling drives ALL revenue. Claude Max ($200) generates content, code, research, automation for every lane. Marginal cost per new method → zero. A solopreneur running these independently would spend $1,500+/mo on separate tools.

**Kill ruthlessly, scale winners:**
- Kill: App <$100 MRR after 60 days. Content <500 followers after 90 days. Outbound <2% reply after 3 optimizations.
- Scale: App MRR growing 20%+ at $500+ → paid ads. Content >5% engagement sustained → double frequency. Newsletter >40% open rate at 500+ subs → launch paid tier.

**Reinvestment matrix:** $0-1k → 90% back to business. $1-5k → 80% business. $5-15k → 70% business, 10% index funds, 5% crypto. $15-50k → 50% business, 20% index, 10% crypto, 5% angel. Revenue per hour tracked per method — time flows to highest-ROI lanes.

**Phase-based activation:** Don't start everything at once. Phase 0 = account setup (3-4h human). Phase 1 = first revenue in 72h. Phase 3 unlocks at $1k/mo. Phase 4 at $5k/mo. Phase 5 (empire mode) at $16-57k/mo.

**Execute and log:** The system documents its own operations — but for machine consumption, not human reports. Every action, decision, result goes to structured files (CSVs, JSONL, state JSON) that agents read and act on. No vanity docs.

---

## STRUCTURE TREE

```
PRINTMAXX_STARTER_KITttttt/          # 27GB, 595K files
│
├── AUTOMATIONS/                      # THE BRAIN — 300 Python scripts, 5K files
│   ├── ceo_agent.py                  #   L0 orchestrator. 16 phases. Scores ops, decides PROMOTE/ENHANCE/CREATE/KILL.
│   ├── venture_autonomy.py           #   L1 engine. 8 venture types. Self-managing schedules. SelfManager auto-adjusts.
│   ├── agent_swarm.py                #   L1 engine. 25 operational agents. Generates launchd plists. Health monitoring.
│   ├── intelligence_router.py        #   L2 intelligence. 484 docs, 15K alpha, 16 CSVs → single brief per venture+task.
│   ├── decision_engine.py            #   L1 engine. Closed-loop: pending data → scored decisions → actions.
│   ├── daily_tactical_engine.py      #   L3 execution. Unified "do exactly this today" plan across all 8 ventures.
│   ├── daily_engagement_planner.py   #   L3 execution. Warmup-aware Twitter action plan (posts, replies, likes, timing).
│   ├── daily_digest.py               #   L2 intelligence. Human-readable summary of what system did overnight.
│   ├── alpha_query.py                #   L2 intelligence. Venture-based alpha search with ROI normalization.
│   ├── growth_strategist.py          #   L3 execution. Creates growth strategies per venture from intelligence.
│   ├── loop_closer.py                #   L6 maintenance. 3 loops: decision execution, feedback tracking, pipeline advancement.
│   ├── meta_planner.py               #   L2/L3 planning. Reads MASTER_OPS, maps automation gaps, writes META_PLAN.json + AUTONOMOUS_TASK_QUEUE.jsonl.
│   ├── twitter_warmup_poster.py      #   L3 execution. 21-day warmup (LURK/ENGAGE/SOFT_POST/RAMP/FULL_OPS).
│   ├── twitter_alpha_scraper.py      #   L4 collection. 133 Twitter accounts via Brave cookies + Playwright.
│   ├── background_reddit_scraper.py  #   L4 collection. Reddit JSON API, no auth.
│   ├── alpha_auto_processor.py       #   L3 execution. Routes ALPHA_STAGING.csv → ventures/OPS/cron/archive.
│   ├── daily_research_orchestrator.py#   L3 execution. Research pipeline: scrapers → alpha review → content gen.
│   ├── app_factory_autopilot.py      #   L3 execution. Bookmarks + app alpha scrape + auto-approve + auto-process + queue rebuild.
│   ├── app_factory_command_center.py #   L3 execution. Scores app alpha → ranked app queue + OPS app command center.
│   ├── eas_lead_pipeline.py           #   L3 execution. EAS venture: scores leads for automation fit, generates cold emails, exports CSV. Cron weekday 8AM.
│   ├── quality_gate.py               #   L5 quality. Hard gate — blocks slop, rewrites bad content.
│   ├── system_health_monitor.py      #   L5 quality. Health checks: agents, cron, disk, processes.
│   ├── compliance_scanner.py         #   L5 quality. FTC/platform compliance auditing.
│   ├── prompt_meta_review.py         #   L2 intelligence. Analyzes user prompts for lost threads, patterns, forgotten goals.
│   ├── session_briefing.py           #   L2 intelligence. Auto session-start briefing: agent reports, changes, queue.
│   ├── actionable_aggregator.py      #   L3 execution. Scans 6 sources → prioritized P0-P3 action queue.
│   ├── method_discovery_crawler.py   #   L4 collection. Daily crawls 18 subreddits + HN + Twitter for new revenue methods. Capital Genesis scoring. Cron 5 AM.
│   ├── capital_genesis_ranker.py     #   L2 intelligence. Scores ALL methods on 7 weighted dimensions, phase-aware. Daily priority stack. Cron 5:30 AM.
│   ├── memory_manager.py             #   L6 maintenance. Filesystem-based memory management.
│   ├── wire_missed_intelligence.py   #   L6 maintenance. Parses scan results → updates intelligence catalog.
│   ├── build_codebase_grammar.py     #   L6 maintenance. AST-based 118x compression for LLM context.
│   ├── _common.py                    #   Shared utilities: safe_path, ts, log, load_json, hours_since, run_script.
│   │
│   ├── agent/                        #   Agent state, communication, orchestration
│   │   ├── ceo_agent/                #     CEO state, decisions.jsonl, audit.jsonl
│   │   ├── autonomy/                 #     Venture state, schedules, launchd plists, results, app_factory_priority_queue.json, app_factory_autopilot_status.json
│   │   ├── swarm/                    #     Swarm state, reports/ (gap, health, alpha, SEO, competitor intel)
│   │   ├── missions.jsonl            #     Shared mission log (visible in Command Center)
│   │   └── message_bus.jsonl         #     Inter-agent communication bus
│   │
│   ├── hooks/                        #   8 active hooks: path validation, py_compile, secret detection,
│   │                                 #   safe_path discard check, file handle leak check, type hint check,
│   │                                 #   cron critical agents check
│   │
│   ├── subconscious/                 #   Memory injection/extraction at session start/end
│   │   └── memories/memories.jsonl   #     Categories: PREFERENCE, DECISION, STRATEGIC, BLOCKER, LEARNED
│   │
│   └── logs/                         #   All script execution logs (append-only, rotated)
│
├── LEDGER/                           # DATA WAREHOUSE — 2,023 CSVs, 2.2K files
│   ├── ALPHA_STAGING.csv             #   Raw alpha intake (PENDING_REVIEW → routed)
│   ├── MEGA_SHEET/                   #   10 consolidated CSVs, 2,512 rows
│   ├── APP_FACTORY_METHODS.csv       #   Method-specific alpha
│   ├── MARKETING_CHANNELS_MASTER.csv #   All marketing channels scored
│   ├── ECOM_ARB_OPPORTUNITIES.csv    #   3,519 arbitrage opportunities
│   ├── BRAIN_STATE.json              #   LLM decision state
│   └── DECISIONS.csv                 #   Decision audit trail
│
├── OPS/                              # OPERATIONS CENTER — 1.2K files
│   ├── DAILY_TACTICAL_PLAN.md        #   Today's "do exactly this" (auto 7:15 AM)
│   ├── DAILY_DIGEST.md               #   What system did overnight (auto 6:45 AM)
│   ├── INTELLIGENCE_CATALOG.json     #   487 docs crawled, 127 HIGH value, buried gold
│   ├── CODEBASE_GRAMMAR.md           #   118x compressed system grammar (auto 5:45 AM)
│   ├── PERSISTENT_TASK_TRACKER.md    #   Every task, status, blocker. Survives compaction.
│   ├── SESSION_BRIEFING.md           #   Auto session-start: agent reports, changes, queue, lost threads
│   ├── ACTIONABLE_QUEUE.md           #   Prioritized P0-P3 from 6 sources (auto 7:30 AM)
│   ├── AUTONOMOUS_TASK_QUEUE.jsonl   #   System-wide queued work generated from MASTER_OPS wiring
│   ├── PROMPT_META_REVIEW.md         #   48h prompt analysis: intent, lost threads, patterns (auto every 2 days)
│   ├── META_PLAN.json                #   MASTER_OPS-derived gap map and execution plan
│   ├── APP_FACTORY_ALPHA_COMMAND_CENTER.md # Ranked app build/upgrade queue + hard gates
│   ├── MULTI_ACCOUNT_INFRASTRUCTURE.md # Antidetect browser, proxy, account architecture
│   ├── GROWTH_ALPHA_SOURCES.md       #   Forums, growth sources, proxy/payment comparisons
│   ├── NAV_INDEX.md                  #   632-line "Where is..." navigation index
│   ├── HEARTBEAT.md                  #   System pulse
│   └── SESSION_LOG.md                #   Session-by-session changelog
│
├── MONEY_METHODS/EAS/                # EAS VENTURE — Enterprise Automation Solutions
│   ├── website/                      #   7 HTML pages (Private Bank design: black/gold/serif)
│   ├── legal/                        #   MSA, SOW, Risk Disclosure, Subcontractor Agreement
│   ├── playbooks/                    #   Signal Map, Phone Pilot, Ops Pilot, Managed Ops delivery manuals
│   ├── outreach/                     #   Cold email sequences + lead scoring config + eas_leads_ready.csv
│   └── EAS_VENTURE_README.md         #   Venture overview for agents
│
├── CONTENT/                          # CONTENT ENGINE — 957 files
│   ├── social/
│   │   ├── TWITTER_GROWTH_ENGINE.md  #   1,492-line complete Twitter playbook (warmup → growth → revenue)
│   │   ├── REPLY_ENGAGEMENT_STRATEGY.md # Tier 1-3 accounts, 12 reply templates
│   │   ├── TWITTER_PROFILE_SPEC.md   #   Bio, banner, PFP spec
│   │   ├── TIKTOK_LAUNCH_SCRIPTS.md  #   5 scripts ready
│   │   ├── posting_queue/            #   40 approved posts, 50 buffer, 588 total generated
│   │   └── printmaxxer/              #   @PRINTMAXXER specific content
│   ├── growth/                       #   Growth playbooks, multi-account warmup, A/B testing
│   └── email_sequences/             #   Cold email, welcome, nurture sequences
│
├── MONEY_METHODS/                    # REVENUE METHODS — 11.7K files
│   ├── APP_FACTORY/                  #   7 PWAs built, central index, ASO research
│   └── CONTENT_FARM/                 #   Niche account content, generated posts
│
├── DIGITAL_PRODUCTS/                 # 13 products built, $0 listed
│   └── GUMROAD_LAUNCH_EXECUTION_GUIDE.md # Ship-in-8-hours, 4 products for $451 week 1
│
├── MEDIA/                            # MEDIA ASSETS — 11.5K files
│   ├── generated_images/             #   twitter_banner.png, twitter_pfp.png, app icons
│   ├── image_templates/              #   Playwright HTML-to-image (zero cost)
│   └── remotion/                     #   React-based programmatic video
│
├── FINANCIALS/                       # MONEY TRACKING
│   ├── P_AND_L_MONTHLY.csv          #   Revenue: $0. Expenses tracked.
│   └── REVENUE_TRACKER.csv          #   Empty. Waiting for first dollar.
│
├── 01_STRATEGY/                      # Strategic planning docs
├── 02_TRACKING/                      # Tracking spreadsheets
├── 03_PLAYBOOKS/                     # 19K files — agency, AI wrapper, local lead gen, ecom arb
├── 04_CONTENT/                       # Content templates and libraries
├── 05_AUTOMATION/                    # Legacy automation scripts
├── 06_OPERATIONS/growth/             # 27 growth playbooks incl EDGE_GROWTH_TACTICS.md (25KB)
├── 07_LANDING/                       # Next.js landing pages, 20+ surge.sh sites
├── 08_PRODUCTS/                      # Product specs
├── 09_LEGAL/                         # Privacy policies, terms, FTC compliance
├── 10_RESEARCH/                      # Market research
├── SECRETS/CREDENTIALS.env           # API keys, tokens (gitignored)
├── .claude/CLAUDE.md                 # 490-line master rules file (14 rules + infrastructure docs)
└── pyrightconfig.json                # Type checking config (basic mode, AUTOMATIONS only)
```

---

## CONTROL SURFACES AND CANONICAL STATE

| Surface | File | Role |
|---------|------|------|
| Claude operating manual | `.claude/CLAUDE.md` | Session rules, navigation, standing instructions |
| Canonical live system map | `OPS/PRINTMAXX_SYSTEM_MAP.md` | Current topology, control surfaces, data flow. Update on change. |
| Architecture patterns | `OPS/AUTONOMOUS_SYSTEM_ARCHITECTURE.md` | Stable battle-tested patterns and memory model |
| App factory autopilot | `AUTOMATIONS/app_factory_autopilot.py`, `AUTOMATIONS/agent/autonomy/app_factory_autopilot_status.json` | End-to-end APP alpha ingest and queue refresh chain |
| App factory command center | `OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md`, `AUTOMATIONS/agent/autonomy/app_factory_priority_queue.json` | Ranked app build/upgrade queue and execution gates |
| Codex automation config | `$CODEX_HOME/automations/printmaxx/automation.toml` | Recurring Codex automation definition |
| Codex automation memory | `$CODEX_HOME/automations/printmaxx/memory.md` | Run log and prior automation decisions |
| Meta planning outputs | `OPS/META_PLAN.json`, `OPS/AUTONOMOUS_TASK_QUEUE.jsonl` | Latest MASTER_OPS-derived plan and queued work |
| CodeRelay local remote bridge | `~/.coderelay/config.json`, `~/.coderelay/bin/coderelay`, `~/Library/LaunchAgents/com.coderelay.plist`, `AUTOMATIONS/coderelay_lan_proxy.py` | Agent-native remote control surface for Codex via Orbit/Anchor. Canonical public origin now points to the tailnet URL; LAN relay on `:8791` remains the same-Wi-Fi fallback for first-run pairing and local rescue. |
| Tailscale userspace transport | `~/Library/LaunchAgents/com.tailscale.userspace.plist`, `AUTOMATIONS/coderelay_tailscale_sync.py`, `~/Library/LaunchAgents/com.coderelay.tailscale-sync.plist` | Private remote-access transport for anywhere access. Userspace daemon + sync loop keep SSH, Serve, and CodeRelay public origin aligned to the live MagicDNS URL. |
| Full GUI fallback | `~/Applications/RustDesk.app`, `~/Library/LaunchAgents/com.rustdesk.client.plist` | Full remote desktop/app control layer for “act like I am on the laptop” fallback |
| Remote access doctor | `AUTOMATIONS/remote_access_status.py`, `~/.printmaxx_remote_access.json` | On-demand snapshot of Tailscale, CodeRelay, and RustDesk status. Sync loop now refreshes the private state file automatically. |
| Sanitized carve-out note | `OPS/REMOTE_CONTROL_DAISY_CHAIN.md` | Open-source extraction boundary and operating pattern for the remote-control daisy chain |
| Sanitized open-source kit | `OPEN_SOURCE/remote-control-daisy-chain/` | Repo-ready carve-out with generic scripts, launchd templates, docs, and example state |

**Latest verified Codex layer (2026-03-13):**
- `meta_planner` ran against `PRINTMAXX_MASTER_OPS_ENHANCED_2026-03-03.xlsx`.
- It produced `OPS/META_PLAN.json` and queued 507 tasks into `OPS/AUTONOMOUS_TASK_QUEUE.jsonl`.
- Coverage snapshot: 518 actionable ops, with 101 scripted, 62 LLM tasks, and 355 remaining gaps.
- `twitter_alpha_scraper.py --accounts --limit 12 --days 30` completed live with Brave cookies + Playwright under elevated browser permissions and saved 38 new high-signal entries (`ALPHA22483-ALPHA22520`) to `LEDGER/ALPHA_STAGING.csv`.
- `app_factory_autopilot.py --run --skip-accounts --approval-max 120 --processor-batch 120 --queue-limit 60` completed live and refreshed approval, routing, specs, and the ranked app queue.
- CodeRelay is installed locally at `~/.coderelay`, with `http://127.0.0.1:8790/health` and `/admin/status` verified and Anchor connected to Orbit.
- CodeRelay `publicOrigin` now resolves to `https://printmaxx-control.tail16dddb.ts.net` via `python3 AUTOMATIONS/coderelay_tailscale_sync.py`, and the LAN relay at `AUTOMATIONS/coderelay_lan_proxy.py` remains available as the same-Wi-Fi fallback on `http://192.168.1.172:8791`.
- Latest verified same-Wi-Fi pairing path: `http://192.168.1.172:8791/pair?code=<short-lived-code>` generated successfully at 2026-03-12 03:47 local. Codes are one-time and expire quickly, so mint fresh ones from `/admin` when needed.
- Tailscale userspace transport is live under `com.tailscale.userspace`. Node authenticated as `printmaxx-control.tail16dddb.ts.net` with Tailscale IP `100.70.237.42`, and `tailscale serve status` now confirms `https://printmaxx-control.tail16dddb.ts.net (tailnet only) -> http://127.0.0.1:8790`.
- `AUTOMATIONS/coderelay_tailscale_sync.py` plus `com.coderelay.tailscale-sync` now auto-finish Serve/origin wiring after login and keep `~/.printmaxx_remote_access.json` fresh.
- `AUTOMATIONS/remote_access_status.py` was added as an on-demand doctor for the full remote-control stack.
- RustDesk `1.4.6` is installed in `~/Applications/RustDesk.app` and launched at login via `com.rustdesk.client`, but unattended password/service setup still needs admin-level or manual in-app completion and macOS screen recording/accessibility permissions.
- Sanitized extraction work now lives at `OPEN_SOURCE/remote-control-daisy-chain/` so the daisy-chain concept can be split out without leaking PRINTMAXX business state or private identifiers.

---

## MASTER OPS ENHANCED (182 ops across 19 sheets)

Source: `PRINTMAXX_MASTER_OPS_ENHANCED_*.xlsx` (latest dated version)
Bridge: `AUTOMATIONS/master_ops_bridge.py` → cache at `AUTOMATIONS/master_ops_cache.json`
Dashboard: `http://localhost:9999` → Ops Intel tab

### Sheets & Contents

| Sheet | Rows | Purpose |
|-------|------|---------|
| ALL OPS MASTER | 182 | Every op: ID, category, revenue range, automation level, status, platforms |
| AUTO_STATUS_LIVE | 180 | Real-time readiness (READY/BUILD/BLOCKED), automation scores 0-100, signal counts |
| PRIORITY LAUNCH | 18 | Ranked by urgency: op, effort, revenue potential, first step, time-to-first-$ |
| PRIORITY_AUTOMATION_EXEC | 18 | Automation-ready items with command templates |
| SYNERGY STACKS | 26 | Synergy combos: score 85-97, revenue multipliers 4.5x-8.7x |
| VENTURE_AUTOMATION_MAP | 55 | Venture→lane→blocker→command mappings |
| ALPHA_THESIS_INDEX | 38 | Alpha opportunities with edge durations (6-36 months) |
| DEEP_PLAYBOOK_INDEX | 1,470 | Step-by-step instructions for 37 ops |
| VIDEO & MEDIA STACK | 28 | Tools: Kling, Veo, Remotion, Nano Banana + quality ratings |
| HOSTING & DEPLOY | 14 | Netlify, Cloudflare, Vercel, GitHub Pages + commercial use |
| LEAD GEN STACK | 33 | Bland AI, Instantly, Clay, Apollo + automation levels |
| EXISTING INFRA | 60 | What's built: scrapers, pipelines, dashboards, agents |
| RBI SYSTEM | 19 | Audit types: daily/weekly/monthly health checks |
| ETC_EXPANSION_QUEUE | 32 | Expansion candidates ranked by automation score |
| BROWSER & PROXY STACK | 60 | Browser automation fallback chain + stealth levels |
| DEEP PLAYBOOK | 2,999 | Raw playbook text for 37 ops (unstructured) |
| LLM ALPHA THESIS | 79 | Raw alpha thesis text (unstructured) |
| NSFW COMPLIANCE | 13 | Platform requirements for adult content ops |
| SYSTEM_EVIDENCE | 11 | Build metadata and approval counts |

### Op Categories (from ALL OPS MASTER)

```
CONTENT (C01-C20)     — TikTok, YouTube, Instagram, X, Podcast, Newsletter
SERVICE (S01-S08)     — Freelance, Local Biz, Agency, Cold Email, AI Services
APP (A01-A04)         — Portfolio Apps, Vertical SaaS, Chrome Extensions
DIGITAL_PRODUCT (D01-D12) — Gumroad PDFs, Courses, Templates, Notion Packs
ECOM (E01-E07)        — Trending Product Arb, Print-on-Demand, Dropship
NICHE (N61-N68)       — Ramadan Tracker, Local Biz Redesign, specialty apps
PERSONA (P01-P12)     — AI Persona content ops (compliance-critical)
```

### Synergy Multiplier System

Ops don't exist in isolation. SYNERGY STACKS define which ops compound:

```
SYN351: Voice AI + Vertical SaaS              — 97 score, 4.5x multiplier
SYN352: Clipper + TikTok Double Monetization   — 96 score, 6.5x multiplier
SYN353: Content Farm + TikTok + FB Reels Arb   — 96 score, 6.2x multiplier
SYN354: Portfolio Apps + Paywall Optimization   — 95 score, 8.7x multiplier
```

Revenue formula: Stacked = Sum(Individual) × Synergy Multiplier × Automation Factor

### Blocker Keys (what's stopping ops)

```
X_MULTI_ACCOUNT_STACK     — Antidetect browser + proxy setup (blocks 15+ content ops)
STORE_ACCOUNT_AND_PAYMENT — App Store + payment processor (blocks app factory)
FIVERR_UPWORK_ACCOUNT     — Freelance platform accounts (blocks service ops)
EMAIL_INFRA               — Email sending infrastructure (blocks outbound)
GUMROAD_ACCOUNT           — Gumroad seller setup (blocks digital products)
STRIPE_ACCOUNT            — Payment processing (blocks direct sales)
```

### Integration Map (who consumes xlsx data)

```
master_ops_bridge.py ─── cache ──→ master_ops_cache.json
         │
         ├──→ intelligence_router.py    (enriches ALL agent briefs)
         ├──→ ceo_agent.py              (VentureScorer uses xlsx for PROMOTE/KILL)
         ├──→ decision_engine.py        (xlsx-weighted decision scoring)
         ├──→ daily_tactical_engine.py  (priority launches in daily plans)
         ├──→ venture_autonomy.py       (venture context + blocker awareness)
         ├──→ growth_strategist.py      (synergy strategies + tool recommendations)
         ├──→ loop_closer.py            (blocker tracking + pipeline advancement)
         └──→ control_panel.py          (Ops Intel tab at localhost:9999)
```

---

## EXECUTION HIERARCHY

```
L0 ORCHESTRATOR     ceo_agent.py ─────────────────── Every 2h. Scores all ops. PROMOTE/ENHANCE/CREATE/KILL.
                         │
L1 ENGINES          venture_autonomy.py ──────────── Every 4h. 8 venture pipelines. Self-managing.
                    agent_swarm.py ────────────────── 25 agents via launchd. swarm_brain every 4h.
                    decision_engine.py ────────────── Every 30min. Processes pending data → actions.
                         │
L2 INTELLIGENCE     intelligence_router.py ────────── On demand. 484 docs + 15K alpha → briefing.
                    alpha_query.py ────────────────── On demand. Search/filter/score alpha.
                    capital_genesis_ranker.py ─────── 5:30 AM. Ranks ALL methods on 7 dimensions → priority stack.
                    daily_digest.py ───────────────── 6:45 AM. What happened overnight.
                    master_ops_bridge.py ─────────── On demand. 182 ops + synergy + playbooks from xlsx.
                         │
L3 EXECUTION        daily_tactical_engine.py ──────── 7:15 AM. "Do exactly this today."
                    daily_engagement_planner.py ───── 7:00 AM. Twitter warmup-safe plan.
                    growth_strategist.py ──────────── 5:00 AM. Growth strategies per venture.
                    twitter_warmup_poster.py ──────── Midnight. Advance warmup day.
                    alpha_auto_processor.py ───────── 6:30 AM. Route new alpha.
                         │
L4 COLLECTION       method_discovery_crawler.py ──── 5:00 AM. 18 subreddits + HN + Twitter for new methods.
                    twitter_alpha_scraper.py ──────── 6:00 AM. 133 accounts.
                    background_reddit_scraper.py ──── 6:15 AM. Reddit JSON.
                         │
L5 QUALITY          quality_gate.py ───────────────── Every 2h. Blocks slop.
                    compliance_scanner.py ─────────── On demand. FTC/platform.
                    system_health_monitor.py ──────── Every 6h. Agents/cron/disk.
                         │
L6 MAINTENANCE      loop_closer.py ────────────────── Every 2h. Closes decision/feedback/pipeline loops.
                    memory_manager.py ─────────────── 5:00 AM. Filesystem memory.
                    build_codebase_grammar.py ─────── 5:45 AM. 118x compressed grammar.
                         │
SOVRUN LAYER        core/handoff.py ──────────────── Agent-to-agent handoff protocol. Guardrails + audit trail.
(OPEN_SOURCE/       core/procedural_memory.py ─────── FTS5 skill docs. Agents recall learned solutions.
 agent-soul/)       core/orchestration.py ─────────── DAG executor. Parallel phase execution for CEO cycle.
                    core/resilience.py ────────────── Circuit breaker, retry, file locking, sanitization.
```

---

## DATA FLOW

```
method_discovery_crawler ──→ ALPHA_STAGING.csv (status=NEW_METHOD) + METHOD_DISCOVERY_LOG.csv
         │
         └──→ auto_ops/discovered_methods/ (high-scoring method stubs)

capital_genesis_ranker ◄── ALPHA_STAGING + all method CSVs + MASTER_OPS
         │
         └──→ OPS/CAPITAL_GENESIS_PRIORITY_STACK.md + LEDGER/CAPITAL_GENESIS_RANKINGS.csv
                    │
                    └──→ CEO agent + daily_tactical_engine (priority-driven decisions)

SCRAPE ──→ ALPHA_STAGING.csv ──→ alpha_auto_processor ──→ Method CSVs + Venture routing
BOOKMARKS/HIGH-SIGNAL ──→ app_factory_autopilot.py ──→ alpha_auto_approver.py ──→ alpha_auto_processor.py ──→ alpha_to_ops.py
                                 │
                                 └──→ app_factory_command_center.py ──→ app_factory_priority_queue.json + OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md
                                                              │
INTELLIGENCE_CATALOG.json ◄── wire_missed_intelligence ◄── filesystem scan
         │
intelligence_router.py ◄── alpha_query + docs + CSVs + swarm reports
         │
         ├──→ ceo_agent (Phase 3.5 enrichment)
         ├──→ venture_autonomy (pre-execution briefing)
         ├──→ agent_swarm (AGENT_VENTURE_MAP injection)
         ├──→ daily_tactical_engine (unified plan)
         ├──→ daily_engagement_planner (Twitter plan)
         └──→ growth_strategist (venture strategies)

DECISIONS ──→ decision_engine ──→ DECISIONS.csv
                    │
         loop_closer ──→ executes decisions, tracks feedback, advances pipeline
                    │
         ceo_agent ──→ PROMOTE/ENHANCE/CREATE/KILL ──→ venture_autonomy adjusts

PRINTMAXX_MASTER_OPS_ENHANCED.xlsx ──→ master_ops_bridge.py ──→ master_ops_cache.json
         │
         ├──→ intelligence_router (enriches all briefs)
         ├──→ ceo_agent (VentureScorer)
         ├──→ decision_engine (weighted scoring)
         ├──→ daily_tactical_engine (priority launches)
         └──→ control_panel (Ops Intel tab)
```

---

## AGENT TOPOLOGY (33 total)

**8 Venture Agents** (venture_autonomy.py, every 4h):
CONTENT | OUTBOUND | APP_FACTORY | LOCAL_BIZ | MONETIZATION | PRODUCT | RESEARCH | SCRAPING

**25 Swarm Agents** (agent_swarm.py, launchd):
META: swarm_brain (4h, Opus), meta_executor (4h, Opus)
DISCOVERY: gap_hunter, opportunity_scanner, competitor_stalker
ACTION: asset_deployer, content_compounder, lead_machine
MEDIA: video_factory, image_factory
OPTIMIZE: seo_aso_optimizer, conversion_optimizer, quality_enforcer
QUALITY: quality_gate (2h, Opus), playwright_tester
INTELLIGENCE: trend_synthesizer, cross_pollinator, revenue_tracker
MAINTENANCE: system_healer, data_janitor
GROWTH: distribution_engine, inbound_maximizer, social_poster, growth_strategist (24h, Opus)
NOTIFICATION: alert_dispatcher

All agents run via `claude -p --dangerously-skip-permissions` on Claude Max plan. Zero API cost. ALL agents use Opus — no Sonnet, no Haiku.

---

## CRON SCHEDULE (111 entries)

```
MORNING CHAIN (sequential):
  5:00  method_discovery_crawler   5:30  capital_genesis_ranker
  5:00  growth_strategist          5:30  venture self-manager
  5:45  codebase grammar           6:00  twitter scraper + alpha review
  6:15  reddit scraper             6:30  alpha auto-processor
  6:45  daily digest               7:00  engagement planner
  7:15  tactical engine

CONTINUOUS CYCLES:
  */15min  guardian pulse + agent daemon keepalive
  */30min  decision engine
  */2h     CEO agent + loop closer + safety commit
  */3h     signal aggregator + ops manager
  */4h     venture autonomy + venture tracker
  */6h     swarm health + memecoin + SAM.gov

DAILY:
  1 AM   ship engine layer1        2 AM   overnight master runner
  3 AM   closed-loop pipeline      4 AM   lead enrichment + log rotation
  9 PM   autonomous factory        11 PM  guardian improve
  Midnight  warmup poster advance

WEEKLY:
  Sun 2 AM  performance report     Sun 3 AM  full backup
  Sun 4 AM  system clone           Mon various  ASO, RPM, ecom
```

---

## STATE FILES (source of truth)

```
ceo_state.json          CEO cycle count, decisions, timestamps
autonomy_state.json     Venture pipelines, stages, results
swarm_state.json        Agent health, cycles, effectiveness scores
twitter_warmup_state.json  Warmup day, phase, post history
ALPHA_STAGING.csv       Raw alpha intake (15,154 entries)
INTELLIGENCE_CATALOG.json  487 docs, value scores, buried gold
decisions.jsonl         CEO decision audit trail
missions.jsonl          Shared mission log
message_bus.jsonl       Inter-agent messages
feedback_recommendations.json  Loop closer → swarm adjustments
USER_PROMPTS.jsonl      Every user prompt timestamped (hook captures on submit)
master_ops_cache.json   Bridge JSON cache of xlsx (182 ops, 19 sheets, 12h TTL)
app_factory_priority_queue.json  Ranked app alpha queue for APP_FACTORY autonomy
app_factory_autopilot_status.json  Last autopilot chain result and queue snapshot
throttle_state.json     Current throttle mode and agent overrides
throttle_config.json    Agent tier config (efficient/high intervals)
printmaxx_gates.db      Blocking gate states + task graph (SQLite, survives restart)
MODEL_ROUTING_CONFIG.json  Cross-model routing (writer != reviewer)
INBOUND_LEADS.csv       Observer agent lead captures (score, platform, engagement)
OUTREACH_QUEUE.csv      Quinn agent warm outreach queue
DECISION_REVIEWS.jsonl  Challenger agent review logs
PENDING_HUMAN_APPROVAL.jsonl  Items needing human action
worktree_state.json     Active git worktrees for parallel agents
SOUL.md                 Behavioral identity for all agents
CAPITAL_GENESIS_PRIORITY_STACK.md  Daily ranked method priorities (capital_genesis_ranker, 5:30 AM)
CAPITAL_GENESIS_RANKINGS.csv       Machine-readable method rankings with scores
METHOD_DISCOVERY_LOG.csv           New methods discovered by crawler with CG scores
```

---

## REVENUE STATUS

$0. Day 35. The system builds, scrapes, scores, decides, and generates 24/7.
The bottleneck is human activation of payment/distribution channels.

**Unblocked in ~85 min:** Stripe (5min) + Gmail MCP (5min) + Twitter profile (10min) + Gumroad 13 products (30min) + TikTok (30min) + Cloudflare (5min).

**Pipeline ready:** 13 digital products built. 40 posts queued. 1,110 leads. 16 live sites. 20 ecom arb products (27-66% margins). 12 freelance opps. 182 ops mapped with automation scores.

---

## HOOKS (8 active)

PreToolUse Write|Edit: path validation (blocks writes outside project)
PostToolUse Write|Edit: py_compile (syntax), secret detector, safe_path discard check, file handle leak check, type hint check
SessionStart: cron check, subconscious injection, warm-start context

---

## CONTROL PANEL (localhost:9999)

Unified dashboard replacing 8 scattered UIs. Auto-launches on session start.

**Tabs:** Dashboard (real-time charts) | Agents (throttle controls) | System Tree (L0-L6 hierarchy) | Actions (quick triggers) | Blockers (P0 human items) | Ops Intel (full xlsx intelligence)

**Desktop app:** `AUTOMATIONS/PrintmaxxPanel.app` — neon green P icon, launches server + browser.

**Endpoints:** `/api/status`, `/api/agents`, `/api/system-tree`, `/api/realtime`, `/api/ventures`, `/api/pipeline`, `/api/master-ops`, `/api/actions`, `/api/blockers`

---

## RESTRUCTURE V2 — NEW COMPONENTS (2026-03-13)

Source: PRINTMAXX_RESTRUCTURE_V2.xlsx — gap analysis from metaswarm, Swan AI, OpenClaw, IH patterns, ccswarm, wshobson/agents

### SOUL.md (Behavioral Identity)
```
AUTOMATIONS/SOUL.md — behavioral directives for all agents
  Injected via: intelligence_router.py → get_intelligence() → result["soul_directives"]
  Also: _common.py → get_soul() for direct reads
  Core: "be resourceful before asking", "execute don't deliberate", "every output has a consumer"
```

### Blocking State Gates (T014 — BEADS pattern)
```
AUTOMATIONS/gates.py — deterministic state machine for pipeline quality control
  States: PENDING → IMPLEMENTING → VALIDATING → REVIEWING → APPROVED | REJECTED | HUMAN_REQUIRED
  DB: LEDGER/printmaxx_gates.db (SQLite, survives session restart)
  Rule: NO path from REJECTED → APPROVED without human_override=True
  Consumers: content pipeline, lead outreach, ecomm arb, CEO agent
```

### Cross-Model Adversarial Review (T013)
```
.claude/external-tools.yaml — model routing config (Codex/Gemini stubs)
AUTOMATIONS/MODEL_ROUTING_CONFIG.json — evaluator_writer=Sonnet, evaluator_reviewer=Opus
  Rule: agent that writes output NEVER reviews own output
  Budget: $2/task, $20/session caps
```

### Swan AI GTM Agents (T015)
```
AUTOMATIONS/shakespeare_agent.py — content gen (Sonnet, daily 8am)
  Arc: Attack Outdated Belief → Evidence → New Framework → Data → CTA
  Output: CONTENT/linkedin/ + CONTENT/social/posting_queue/

AUTOMATIONS/observer_agent.py — engagement monitoring (Haiku, every 2h)
  Scoring: agency founder (10) → agency employee (7) → consultant (5) → other (2)
  Output: LEDGER/INBOUND_LEADS.csv (score > 7 = lead, score > 9 = immediate alert)

AUTOMATIONS/quinn_agent.py — warm outreach gen (Sonnet, triggered by observer)
  Output: LEDGER/OUTREACH_QUEUE.csv (warm messages referencing specific engagement)
  A/B: 50% Quinn warm vs 50% standard cold
```

### Task Dependency Graph (T016)
```
AUTOMATIONS/task_graph.py — DAG-based dependency chains
  CHAIN_ALPHA_PIPELINE: scraper → alpha_processor → intel_router → ceo_agent
  CHAIN_CONTENT: shakespeare → evaluator → cross_model_reviewer → social_poster
  CHAIN_LEAD: observer → quinn → lead_machine → compliance_scanner → send
  CHAIN_ARB: ecomm_arb → evaluator → HUMAN_GATE → asset_deployer
  State: LEDGER/printmaxx_gates.db (task_graph table)
```

### Git Worktree Isolation (T017)
```
AUTOMATIONS/worktree_manager.py — parallel agent file isolation
  Creates: ../printmaxx-{name}/ worktrees
  Strategies: last-write-wins (content), human-review (revenue files)
  State: AUTOMATIONS/agent/worktree_state.json
```

### Parallel Challenger Review (T023)
```
AUTOMATIONS/challenger_agents.py — adversarial review of CEO decisions
  Devil's Advocate | Risk Assessor | Market Reality Checker
  Trigger: MAJOR decisions (PROMOTE > $100, KILL > 30d active, CREATE > 10h build)
  2+ OBJECTIONs → PENDING_HUMAN_APPROVAL.jsonl
  Log: LEDGER/DECISION_REVIEWS.jsonl
```

### Agent Skills Marketplace (T018)
```
skills/printmaxx-intelligence-router/SKILL.md
skills/printmaxx-ceo-orchestrator/SKILL.md
skills/printmaxx-compliance-scanner/SKILL.md
skills/printmaxx-alpha-processor/SKILL.md
skills/printmaxx-revenue-tracker/SKILL.md
  Monetization: free basic + $49 pro bundle on Gumroad
```

### Human Approval Queue
```
OPS/PENDING_HUMAN_APPROVAL.jsonl — items needing human action
  HAG001: Reddit r/entrepreneur post (15 min)
  HAG002: LinkedIn EAS company + founder page (20 min)
  HAG003: Discord PRINTMAXX community server (30 min)
  HAG004: Public GitHub repo printmaxx-architecture (10 min)
  HAG005: Public GitHub repo printmaxx-skills (10 min)
```

### Distribution Status
```
Twitter: FULL_OPS (Day 22, advanced from Day 2 per T019/T022)
  40 posts queued, 10/day limit, links OK, threads OK
  Next cron run will post from full ops queue
LinkedIn: CONTENT/linkedin/ created, pending human account setup
Build-in-Public: CONTENT/build_in_public/ created
```

---

## CHANGES — 2026-03-18

### Method Discovery + Capital Genesis Ranking
- `method_discovery_crawler.py` (L4): Daily crawls 18 subreddits + HN + Twitter for NEW revenue methods not yet in master ops. Capital Genesis scoring on 7 dimensions. High-scoring methods get auto-stubs in `auto_ops/discovered_methods/`. Cron 5 AM. CLI: --crawl, --score, --report, --new-only, --dry-run.
- `capital_genesis_ranker.py` (L2): Scores ALL methods on 7 weighted dimensions, phase-aware across 4 revenue phases. Outputs daily priority stack to `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` + `LEDGER/CAPITAL_GENESIS_RANKINGS.csv`. Cron 5:30 AM. CLI: --rank, --top N, --p0, --new, --report, --export csv, --phase N.
- `auto_ops/alpha_theses/BOOMER_MALE_55_70_AFFILIATE.md`: P0 alpha thesis — faceless Facebook/YouTube pages targeting men 55-70, affiliate products $30-80 (health, golf, fishing, tools). Wired into ALPHA_STAGING, MARKETING_CHANNELS_MASTER, WINNING_CONTENT_STRUCTURES, INTELLIGENCE_CATALOG, intelligence_router, alpha_query.
- New data flow: crawler → ALPHA_STAGING (NEW_METHOD) → ranker → PRIORITY_STACK → CEO agent
- New state files: CAPITAL_GENESIS_PRIORITY_STACK.md, CAPITAL_GENESIS_RANKINGS.csv, METHOD_DISCOVERY_LOG.csv

---

## CHANGES — 2026-03-17

### Resilience Fixes
- `perpetual_guardian.py`: Added `_clear_stale_lock()` (removes .git/index.lock if >120s old), `_push_to_remote()` standalone push, increased all git timeouts to 60s. Pushes even when commit fails.
- `system_health_monitor.py`: Now 16-point health check (was 14). Added `check_16_git_push_health()` — GREEN/AMBER/RED based on unpushed commit count.
- `daily_research_pipeline.py`: Added atexit handler for lock cleanup, age-based stale lock detection (>2h = force remove).
- CSV field_size_limit raised to 10MB across 11 scripts: daily_digest, sqlite_alpha_index, perpetual_guardian, daily_research_pipeline, alpha_validator, alpha_screening, alpha_query, actionable_aggregator, intelligence_router, ceo_agent, venture_autonomy.

### Cron Stagger (zero collisions)
- `crontab_printmaxx_v7.txt`: 105 entries, ALL staggered to unique time slots. Was 55+ jobs at :00 causing resource contention.
- perpetual_guardian keeps :00 (priority). ceo_agent moved to :20. system_health_monitor to :05. All others staggered by 5-10 min offsets.

### Open-Source Extraction (sovrun)
- `OPEN_SOURCE/agent-soul/`: Meta-cognition framework extracted. 13 core modules (voice_extractor, cognitive_engine, pattern_miner, user_sim_refiner, loop_closer, self_audit, decision_engine, resilience, conversation_logger, session_briefing, handoff, procedural_memory, orchestration) + templates + examples.
- GitHub: `github.com/fnsmdehip/dogwalk` (private). Name pending.
- **Wired into PRINTMAXX production** (Mar 18):
  - `_common.py`: sovrun path added to sys.path. Helper functions: `sovrun_available()`, `get_procedural_memory()`, `get_handoff_router()`, `recall_skills_for_task()`, `capture_skill_from_result()`.
  - `agent_swarm.py`: HandoffRouter registers all 25 swarm agents as handoff targets. `--handoff SOURCE TARGET "task"` CLI. `--skills QUERY` CLI. Procedural memory injected into agent prompts at deploy time.
  - `ceo_agent.py`: `--dag` flag runs independent phases 7-16 in parallel via DAGOrchestrator (4 workers). `--dag-status` shows last run. Falls back to sequential on import failure.
  - `venture_autonomy.py`: Procedural memory recall before each venture cycle. Skill capture after successful cycles.
  - `loop_closer.py`: Skill capture for successful loop closing actions.
  - Skills DB: `AUTOMATIONS/agent/sovrun/skills.db` (FTS5). Handoff log: `AUTOMATIONS/agent/swarm/sovrun/handoffs.jsonl`.

### System Map Auto-Update
- `.claude/rules/system-map-maintenance.md`: Dedicated auto-loading rule file. Ensures system map gets updated same-session on any architecture change.
- CLAUDE.md Rule 12 expanded: now ARCHITECTURE-FIRST (read map before analyzing, update on ANY change, not just new ventures).
- Session Start step 4 added: read system map for architecture context.
- Session End step 3 added: update system map if architecture changed.

---

## RULES (14 in CLAUDE.md)

1. SHIP NOW               8. COPY STYLE (human-first)
2. EXECUTE DON'T DOCUMENT  9. ZERO WASTE + MAX SQUEEZE
3. NO AI SLOP             10. PARALLEL BY DEFAULT + AGENT TEAMS
4. AUTONOMOUS EXECUTION   11. CEO SANITY CHECK
5. GO ABOVE AND BEYOND    12. INTELLIGENCE-FIRST
6. FACTORY MODE           13. EXTERNAL CODE SECURITY SCANNING
7. NEVER DROP THE BALL    14. AUTO-QUALITY PIPELINE (15+ skills auto-triggered)
