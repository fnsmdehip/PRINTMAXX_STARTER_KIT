## QUICK REFERENCE: QUANT TOOLS (11 Python Scripts)

**All quant infrastructure for institutional-grade solopreneurship.**

| Tool | Command | Purpose |
|------|---------|---------|
| **QUANT TERMINAL** | `python3 AUTOMATIONS/printmaxx_quant_terminal.py` | Bloomberg-style 6-panel TUI (44KB) |
| **Quant Terminal Summary** | `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary` | Quick system health (use at session start) |
| **Ops Dashboard** | `python3 AUTOMATIONS/ops_dashboard.py` | Track 53 ops patterns (32KB) |
| **Revenue Projector** | `python3 AUTOMATIONS/revenue_projector.py` | Monte Carlo + Kelly Criterion (32KB) |
| **Alpha Screener** | `python3 AUTOMATIONS/alpha_screening.py --pending` | Institutional-grade scoring (35KB) |
| **Paper Trader** | `python3 AUTOMATIONS/paper_trade.py --list` | Test methods with $0-100 (19KB) |
| **Method Analyzer** | `python3 AUTOMATIONS/method_performance_analyzer.py` | Weekly performance reports (13KB) |
| **Agent Monitor** | `python3 AUTOMATIONS/agent_monitor.py` | Live agent progress (8KB) |
| **Niche Meta Detector** | `python3 AUTOMATIONS/niche_meta_detector.py` | Ghibli/Saratoga pattern matching (20KB) |
| **Platform Monitor** | `python3 AUTOMATIONS/platform_meta_monitor.py` | TikTok/X/IG algorithm changes (9KB) |
| **Memecoin Tracker** | `python3 AUTOMATIONS/meme_coin_signal_tracker.py` | Reddit/Twitter signals (17KB) |
| **Simple Dashboard** | `python3 AUTOMATIONS/quant_dashboard.py` | Simplified 6-panel TUI (13KB) |
| **Strategic RBI Engine** | `python3 scripts/strategic_rbi_engine.py full` | 5-layer analysis + validation + improvement ★ |
| **RBI Audit** | `python3 scripts/rbi_audit.py full` | Ops health audit (alpha, revenue, experiments) ★ |
| **Daily Briefing** | `python3 scripts/daily_briefing.py` | 10-system daily scan + human action report ★ |
| **Cron Orchestrator** | `./printmaxx_cron.sh [command]` | Master orchestrator for all automation ★ |
| **Nav Scanner** | `python3 scripts/update_claude_md_nav.py --scan` | Find files missing from CLAUDE.md navigation ★ |
| **Prompt Logger** | `python3 AUTOMATIONS/prompt_logger.py --audit` | Log/search/audit user prompts across sessions ★ |
| **Trend-to-Listing** | `python3 AUTOMATIONS/trend_to_listing.py --scan` | Trend→auto-list pipeline (POD/Gumroad/Etsy) |
| **System Health** | `python3 AUTOMATIONS/system_health_monitor.py --check` | 14-point system health check |
| **Greenlight iOS** | `python3 AUTOMATIONS/greenlight_checker.py --all` | Apple App Store compliance scan |
| **Research Pipeline** | `python3 AUTOMATIONS/daily_research_pipeline.py --status` | Daily scrape→extract→filter→repurpose (cron 6:30 AM) |
| **ImportYeti Sourcing** | `python3 AUTOMATIONS/import_sourcing_scanner.py --product "X"` | US customs factory intel (cron 4 AM) |
| **Unified Alpha Monitor** | `python3 AUTOMATIONS/unified_alpha_monitor.py --full` | Reddit niche + GitHub MIT + ASO + competitors + freshness (cron 5:45 AM) |
| **Pain Point Miner** | `python3 AUTOMATIONS/reddit_pain_point_miner.py --scan` | Extract buying intent from 25 subreddits (cron 6:30 AM) |
| **Compliance Deadlines** | `python3 AUTOMATIONS/compliance_deadline_tracker.py --check` | 21 regulations (6 CRITICAL), alerts on approach (cron 8:45 AM daily + 6:30 AM Mon scan) |
| **Telegram Monitor** | `python3 AUTOMATIONS/telegram_community_monitor.py --scan` | 26 channels, 8 niches, signal keyword scoring (cron 9:15 AM) |
| **Content Trend Pipeline** | `python3 AUTOMATIONS/content_trend_pipeline.py --scan --generate` | Trend→content for 5 accounts, PRINTMAXXER voice, hook templates |
| **App Clone Pipeline** | `python3 AUTOMATIONS/app_clone_pipeline.py --scan` | 61 clone opps: 6 apps × 9 langs × 6 demos, rebrand packages |
| **Tweet Auto Drafter** | `python3 AUTOMATIONS/tweet_auto_drafter.py` | Auto-draft tweets from scraped high-signal content |
| **Quote Tweet Scanner** | `python3 AUTOMATIONS/quote_tweet_scanner.py` | Find QT opportunities from monitored accounts |
| **Semantic Memory Search** | `python3 AUTOMATIONS/semantic_memory_search.py "query"` | TF-IDF search across all 1,175+ operational docs (14 categories, `--live`, `--stats`, `--index`) |
| **Autonomous Orchestrator** | `python3 AUTOMATIONS/autonomous_orchestrator.py --status` | Planner: system state → focused Claude session prompts (morning/midday/evening) |
| **Auto Rebalancer** | `python3 AUTOMATIONS/auto_rebalancer.py --check` | Judge: score all methods 0-100, KILL/REDUCE/MAINTAIN/DOUBLE_DOWN |
| **Checkpoint Manager** | `python3 AUTOMATIONS/checkpoint_manager.py --status` | Human-in-loop: PURCHASE/PUBLISH/ACCOUNT/STRATEGY/KILL approvals |
| **SaaS Product Scanner** | `python3 AUTOMATIONS/saas_product_scanner.py --scan` | Score 12+ automations for SaaS potential (price, moat, abuse risk) |
| **Schedule Claude** | `bash AUTOMATIONS/schedule_claude.sh morning\|midday\|evening` | Cron-callable: disk guard + caffeinate + Claude headless + 30min timeout |
| **PRINTMAXX Desktop** | `python3 AUTOMATIONS/printmaxx_desktop.py` | Desktop command center: 5-tab GUI, hourly reminders, macOS notifications, alarms, task list, launch tracker, quick-launch buttons. `--minimized` for background reminders only |
| **Product Launch Automator** | `python3 AUTOMATIONS/product_launch_automator.py --status` | 17 directory guides, 6 products, copy generation, browser tab opening, submission tracking. `--launch --product X`, `--generate-copy`, `--checklist`, `--open-tabs`, `--mark-submitted` |

**Full documentation:** `OPS/QUANT_INFRASTRUCTURE_GUIDE.md` | `OPS/QUANT_QUICK_START.md`
**Cron commands:** `./printmaxx_cron.sh` with no args for help. See Document Version Tracker above for full command list.

---

## ZERO-COST OPS SCANNER (Daily RBI System)

**Scanner:** `python3 AUTOMATIONS/daily_nocost_rbi_scanner.py`
**Acceleration Plan:** `OPS/ZERO_COST_REVENUE_ACCELERATION.md`
**Clipping Service:** `MONEY_METHODS/CLIPPING_SERVICE/`

| Command | What It Does |
|---------|-------------|
| `--scan` | Full daily scan across 17 zero-cost categories |
| `--category X` | Scan single category (affiliate, freelance, clipping, etc) |
| `--audit` | Audit existing ops status vs what's ready |
| `--opportunities` | List all actionable zero-cost ops |
| `--revenue-map` | Show revenue projections (30/60/90 day) |
| `--next-actions` | Top 10 things to do RIGHT NOW |
| `--integrate` | JSON output for quant terminal |
| `--summary` | Quick 20-line summary |
| `--ready-to-list` | Show items ready to list NOW |

**17 Categories Scanned:** Marketplace listings, affiliate networks, freelance platforms, content clipping (both directions), dropship/arbitrage, domain flipping, AI music, directory sites, free tool arbitrage, PLR/MRR, template marketplaces, community monetization, cold email free tier, content syndication, referral programs, repo monetization, data/lead lists

**Output:** `LEDGER/RBI_AUDITS/NOCOST_DAILY_{date}.md`

**Run daily at session start** alongside quant terminal summary.

**Key ready-to-list items:**
- 10 Gumroad products at `PRODUCTS/GUMROAD_READY_LISTINGS.md`
- 100 POD designs in `MONEY_METHODS/POD_TIKTOK_ARBITRAGE_AUDIT.md`
- Auto-clip pipeline built at `AUTOMATIONS/auto_clip_pipeline.py` (list as Fiverr gig)
- Clipping service dual-direction at `MONEY_METHODS/CLIPPING_SERVICE/`
- Bland AI 100 free calls/day (pair with `AUTOMATIONS/local_biz_pipeline.py`)
- Meme scraper at `ralph/loops/social_setup/output/meme_scraper_skeleton.py`

---

## FOLDER HIERARCHY (Current - Pre-Reorganization)

**DO NOT navigate blindly. Use this map:**

### Directory Map (19 Directories)

| Directory | Purpose | Key Files | When to Access |
|-----------|---------|-----------|----------------|
| `LEDGER/` | **SOURCE OF TRUTH.** All tracking data, alpha, methods, niches, metrics | `LEDGER_INDEX.md` (read first), `MEGA_SHEET/` (10 consolidated CSVs, 2,512 rows) | EVERY task. Query LEDGER_INDEX.md before doing anything |
| `MONEY_METHODS/` | Playbooks + builds for ALL 46+ money methods | `INDEX.md`, subdirs per method (APP_FACTORY/, AI_INFLUENCER/, COLD_OUTBOUND/, etc) | Building any revenue lane |
| `OPS/` | Operations, growth tactics, session handoffs, checklists | `SESSION_HANDOFF.md`, `CAPITAL_GENESIS_DASHBOARD.md`, `CAPITAL_GENESIS_HUMAN_TASKS.md`, `growth/` subdir | Session start, growth tactics, human tasks |
| `CONTENT/` | 612 content files: truth pages, longtail pages | `truth_pages/` (10 pillar), `longtail_pages/` (103 generated) | Content creation, SEO/GEO |
| `AUTOMATIONS/` | Playwright scripts, browser automation, proxy config | `x_bookmarks/`, `SOAX_MOBILE_PROXIES.md`, `BROWSER_CONTROL/` | Automation, scraping, browser tasks |
| `LANDING/` | Next.js site (printmaxx-site/) | `printmaxx-site/` (App Router, Turbopack) | Web development, landing pages |
| `FINANCIALS/` | Revenue, expenses, P&L, investments, tax tracking | `REVENUE_TRACKER.csv`, `EXPENSE_TRACKER.csv`, `P_AND_L_MONTHLY.csv`, `INVESTMENT_PORTFOLIO.csv`, `TAX_DEDUCTIONS_2026.csv` | Financial tracking, capital genesis |
| `ralph/` | Overnight autonomous loops (13 loops) | `run_all_loops.sh`, `loops/` (each has prompt.md + .ralph/) | Overnight builds, batch research |
| `ralph_tasks/` | Task definitions for ralph loops | `prd.json`, numbered task files | Ralph loop configuration |
| `MASTER_DOC/` | 280KB master operating system doc (v26) | `PRINTMAXX_MASTER_OPERATING_SYSTEM_...v26.md` | Deep reference, institutional memory |
| `EMAIL/` | Email templates and sequences | Cold email drafts | Cold outbound work |
| `LEGAL/` | Legal docs, compliance, terms | FTC compliance, disclosures | Compliance checks |
| `PRODUCTS/` | Product specs and assets | Product definitions | Product launches |
| `RESEARCH/` | Research outputs and findings | Analysis files | Deep research |
| `scripts/` | Python utility scripts | Generation, processing scripts | Automation |
| `.claude/` | Agent config, rules, commands, skills | `CLAUDE.md` (this file), `rules/`, `commands/` | Agent behavior |
| `.ralph/` | Ralph loop state (progress, guardrails, errors) | `progress.md`, `guardrails.md` | Ralph loop monitoring |
| `app factory/` | **LEGACY - use MONEY_METHODS/APP_FACTORY/ instead** | Old app builds (has node_modules bloat) | Avoid - use MONEY_METHODS/ |
| `cal ai/` | Calendar AI project files | Separate project | Only if specifically requested |
| `new money method ideas/` | Empty idea dump folder | Empty | Skip |
| `tasks/` | Task output files | Agent outputs | Checking agent results |
| `OPS/TREND_INTEL/` | Funnel reverse-engineering, influencer analysis, trend tracking | `analyses/`, `templates/` | Analyzing creator funnels, finding rising trends |
| `DIGITAL_PRODUCTS/` | Gumroad listings, micro products, PDF products | `listings/`, `micro_products/`, `pdfs/` | Listing digital products for sale |
| `builds/` | Programmatic SEO pages, app builds, content assets | `programmatic_seo/`, ramadan content | Deploying built assets |

### MEGA_SHEET: The Consolidated Data Layer

**Location:** `LEDGER/MEGA_SHEET/` - 10 CSVs combining all 70+ LEDGER files

| Tab | CSV File | Rows | Contains |
|-----|----------|------|----------|
| 1 | TAB1_MONEY_METHODS_MASTER.csv | 68 | All 46+ methods + cross-pollination synergy scores |
| 2 | TAB2_NICHES_MASTER.csv | 33 | All niches (N001-N033) with demos, themes, stacks |
| 3 | TAB3_ALPHA_MASTER.csv | 835 | ALL alpha entries (staging + watchlist + research) |
| 4 | TAB4_TOOLS_CHANNELS_MASTER.csv | 225 | Tools, marketing channels, MCP servers |
| 5 | TAB5_CONTENT_MASTER.csv | 569 | Content pipeline, calendar, structures, hashtags |
| 6 | TAB6_APPS_ECOM_MASTER.csv | 154 | App factory, clone opps, ecom arb, micro SaaS |
| 7 | TAB7_SOURCES_ACCOUNTS.csv | 158 | High signal sources (81+), social accounts |
| 8 | TAB8_OPERATIONS.csv | 213 | GTM priorities, affiliates, outreach, warmup |
| 9 | TAB9_EXPERIMENTS_METRICS.csv | 78 | A/B tests, experiments, funnel metrics |
| 10 | TAB10_RESEARCH_MISC.csv | 179 | Research findings, SEO, repos |

**Agent workflow:** Query MEGA_SHEET for broad lookups. Update individual LEDGER CSVs for writes (MEGA_SHEET is a consolidated view).

### Capital Genesis Revenue Lanes (ALL LAUNCH IN PARALLEL)

**AGGRESSIVE TIMELINE: Everything launches simultaneously. Buy warmed accounts. Buy initial engagement to trigger algorithms. Hire VA for cold outreach. Anti-detect browser + proxies + warmed inboxes from Day 1. No waiting months for anything.**

| Lane | Method | Assets Location | Status | Day 1 Action |
|------|--------|-----------------|--------|-------------|
| 1 | AI Findom Persona | `MONEY_METHODS/AI_INFLUENCER/FINDOM/` | Content ready | Buy warmed X account + launch |
| 2 | Notion Templates | `MONEY_METHODS/DIGITAL_PRODUCTS/NOTION_TEMPLATES/` | Listings ready | Gumroad signup + list 5 templates |
| 3 | Content Farm (3 niches) | `MONEY_METHODS/CONTENT_FARM/NICHE_ACCOUNTS/` | Templates ready | Buy 3 warmed accounts + post |
| 4 | Newsletters (3 Beehiiv) | `MONEY_METHODS/NEWSLETTER/LAUNCH_ASSETS/` | Full sequences ready | Beehiiv setup + welcome sequences |
| 5 | SFW AI Personas | `MONEY_METHODS/AI_INFLUENCER/SFW_PERSONAS/` | Building | Generate visuals + launch |
| 6 | Apps | `MONEY_METHODS/APP_FACTORY/builds/` | biomaxx READY | Submit biomaxx Day 1 |
| 7 | AI UGC Factory | `MONEY_METHODS/AI_INFLUENCER/` | FTC-compliant | HeyGen signup + first 10 videos |
| 8 | Cold Outbound | `MONEY_METHODS/COLD_OUTBOUND/` | Sequences ready | DeliverOn/EmailBison + warmed inboxes |
| 9 | AI Music/Streaming | `MONEY_METHODS/AI_INFLUENCER/` | New | AI musicians on Spotify/TikTok + AI Twitch |
| 10 | Paid Ads | `MONEY_METHODS/PAID_ADS/` | Playbooks ready | $100 Meta + $100 TikTok test Day 1 |
| 11 | VA Cold Calling | `MONEY_METHODS/COLD_OUTBOUND/` | Templates ready | Hire VA on Fiverr/OnlineJobs.ph |

**Infrastructure setup (4-6 hours):** Anti-detect browser + SOAX proxies + warmed accounts + warmed inboxes + AI tools + dev accounts + Stripe/Gumroad/Beehiiv + VA.

**Setup docs:** `06_OPERATIONS/setup/RETARDMAXX_MANUAL_TODO.md` (simplest) | `06_OPERATIONS/setup/ULTIMATE_STACK_GUIDE.md` (comprehensive) | `01_STRATEGY/CAPITAL_GENESIS_HUMAN_TASKS.md` (per-lane actions)

**Grey-hat growth:** `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` + `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` + `06_OPERATIONS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md`

### Tech Stack Tiers (Bootstrap → Scale)

**Full details:** `OPS/TECH_STACK_TIERS.md`
**Rule:** Never spend more than 60% of revenue on tools/team. Start Tier 0, upgrade as revenue grows.

### Financial Tracking

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `FINANCIALS/REVENUE_TRACKER.csv` | All revenue by method | Every transaction |
| `FINANCIALS/EXPENSE_TRACKER.csv` | All expenses (pre-populated with known costs) | Every purchase |
| `FINANCIALS/P_AND_L_MONTHLY.csv` | Monthly profit/loss summary | Monthly |
| `FINANCIALS/INVESTMENT_PORTFOLIO.csv` | Capital genesis investments (stocks, crypto, RE, PE) | Per trade |
| `FINANCIALS/TAX_DEDUCTIONS_2026.csv` | Tax-deductible expenses | Per expense |
| `FINANCIALS/FINANCIAL_DASHBOARD.md` | Human-readable financial summary | Weekly |

### Distribution Channels (Including Medium/Substack)

All channels tracked in `LEDGER/MARKETING_CHANNELS_MASTER.csv`. Key platforms:
- **X/Twitter** - Primary for all personas and content
- **TikTok** - Content farm, short-form video
- **YouTube** - Long-form, Shorts, faceless channels
- **Instagram** - Visual content, Reels
- **LoyalFans/Fanvue** - AI influencer monetization (18+ disclosed)
- **Gumroad** - Digital products, Notion templates
- **Beehiiv** - Newsletters (3 planned)
- **Medium** - Cross-post blog content, Partner Program revenue
- **Substack** - Newsletter + Notes, paid subscriptions, discovery network
- **Pinterest** - Affiliate, visual content
- **LinkedIn** - Cold outbound, B2B content
- **Telegram** - VIP channels, community
---

