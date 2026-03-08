# PRINTMAXX — COMPLETE SYSTEM MAP
# One solopreneur. Zero revenue. 33 autonomous agents. 298 Python scripts. 109 cron jobs. 27GB.
# Goal: $0 → hedge fund capital management via recursive automation.

---

## WHAT IT IS

A fully autonomous solopreneur operations system that scrapes intelligence, generates content, manages ventures, deploys assets, and makes strategic decisions 24/7 without human input — all running on a $200/mo Claude Max plan via `claude -p` CLI calls through launchd and cron.

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
├── AUTOMATIONS/                      # THE BRAIN — 298 Python scripts, 5K files
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
│   ├── twitter_warmup_poster.py      #   L3 execution. 21-day warmup (LURK/ENGAGE/SOFT_POST/RAMP/FULL_OPS).
│   ├── twitter_alpha_scraper.py      #   L4 collection. 133 Twitter accounts via Brave cookies + Playwright.
│   ├── background_reddit_scraper.py  #   L4 collection. Reddit JSON API, no auth.
│   ├── alpha_auto_processor.py       #   L3 execution. Routes ALPHA_STAGING.csv → ventures/OPS/cron/archive.
│   ├── daily_research_orchestrator.py#   L3 execution. Research pipeline: scrapers → alpha review → content gen.
│   ├── quality_gate.py               #   L5 quality. Hard gate — blocks slop, rewrites bad content.
│   ├── system_health_monitor.py      #   L5 quality. Health checks: agents, cron, disk, processes.
│   ├── compliance_scanner.py         #   L5 quality. FTC/platform compliance auditing.
│   ├── prompt_meta_review.py         #   L2 intelligence. Analyzes user prompts for lost threads, patterns, forgotten goals.
│   ├── session_briefing.py           #   L2 intelligence. Auto session-start briefing: agent reports, changes, queue.
│   ├── actionable_aggregator.py      #   L3 execution. Scans 6 sources → prioritized P0-P3 action queue.
│   ├── memory_manager.py             #   L6 maintenance. Filesystem-based memory management.
│   ├── wire_missed_intelligence.py   #   L6 maintenance. Parses scan results → updates intelligence catalog.
│   ├── build_codebase_grammar.py     #   L6 maintenance. AST-based 118x compression for LLM context.
│   ├── _common.py                    #   Shared utilities: safe_path, ts, log, load_json, hours_since, run_script.
│   │
│   ├── agent/                        #   Agent state, communication, orchestration
│   │   ├── ceo_agent/                #     CEO state, decisions.jsonl, audit.jsonl
│   │   ├── autonomy/                 #     Venture state, schedules, launchd plists, results
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
│   ├── PROMPT_META_REVIEW.md         #   48h prompt analysis: intent, lost threads, patterns (auto every 2 days)
│   ├── MULTI_ACCOUNT_INFRASTRUCTURE.md # Antidetect browser, proxy, account architecture
│   ├── GROWTH_ALPHA_SOURCES.md       #   Forums, growth sources, proxy/payment comparisons
│   ├── NAV_INDEX.md                  #   632-line "Where is..." navigation index
│   ├── HEARTBEAT.md                  #   System pulse
│   └── SESSION_LOG.md                #   Session-by-session changelog
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
                    daily_digest.py ───────────────── 6:45 AM. What happened overnight.
                         │
L3 EXECUTION        daily_tactical_engine.py ──────── 7:15 AM. "Do exactly this today."
                    daily_engagement_planner.py ───── 7:00 AM. Twitter warmup-safe plan.
                    growth_strategist.py ──────────── 5:00 AM. Growth strategies per venture.
                    twitter_warmup_poster.py ──────── Midnight. Advance warmup day.
                    alpha_auto_processor.py ───────── 6:30 AM. Route new alpha.
                         │
L4 COLLECTION       twitter_alpha_scraper.py ──────── 6:00 AM. 133 accounts.
                    background_reddit_scraper.py ──── 6:15 AM. Reddit JSON.
                         │
L5 QUALITY          quality_gate.py ───────────────── Every 2h. Blocks slop.
                    compliance_scanner.py ─────────── On demand. FTC/platform.
                    system_health_monitor.py ──────── Every 6h. Agents/cron/disk.
                         │
L6 MAINTENANCE      loop_closer.py ────────────────── Every 2h. Closes decision/feedback/pipeline loops.
                    memory_manager.py ─────────────── 5:00 AM. Filesystem memory.
                    build_codebase_grammar.py ─────── 5:45 AM. 118x compressed grammar.
```

---

## DATA FLOW

```
SCRAPE ──→ ALPHA_STAGING.csv ──→ alpha_auto_processor ──→ Method CSVs + Venture routing
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

## CRON SCHEDULE (109 entries)

```
MORNING CHAIN (sequential):
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
```

---

## REVENUE STATUS

$0. Day 35. The system builds, scrapes, scores, decides, and generates 24/7.
The bottleneck is human activation of payment/distribution channels.

**Unblocked in ~85 min:** Stripe (5min) + Gmail MCP (5min) + Twitter profile (10min) + Gumroad 13 products (30min) + TikTok (30min) + Cloudflare (5min).

**Pipeline ready:** 13 digital products built. 40 posts queued. 1,110 leads. 16 live sites. 20 ecom arb products (27-66% margins). 12 freelance opps.

---

## HOOKS (8 active)

PreToolUse Write|Edit: path validation (blocks writes outside project)
PostToolUse Write|Edit: py_compile (syntax), secret detector, safe_path discard check, file handle leak check, type hint check
SessionStart: cron check, subconscious injection, warm-start context

---

## RULES (14 in CLAUDE.md)

1. SHIP NOW               8. COPY STYLE (human-first)
2. EXECUTE DON'T DOCUMENT  9. ZERO WASTE + MAX SQUEEZE
3. NO AI SLOP             10. PARALLEL BY DEFAULT + AGENT TEAMS
4. AUTONOMOUS EXECUTION   11. CEO SANITY CHECK
5. GO ABOVE AND BEYOND    12. INTELLIGENCE-FIRST
6. FACTORY MODE           13. EXTERNAL CODE SECURITY SCANNING
7. NEVER DROP THE BALL    14. AUTO-QUALITY PIPELINE (15+ skills auto-triggered)
