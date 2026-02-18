# PRINTMAXX Starter Kit

---

## 1. SESSION HANDOFF (Read First)

**Latest Handoff:** `OPS/SESSION_HANDOFF_FEB5_2026.md`
**Date:** 2026-02-05
**Archive:** Verbose content archived to `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md`

### Quick Context
- Swarm research complete: 184 alpha entries staged (PENDING_REVIEW)
- FB Reels $4.40/1K = DEBUNKED (actual $0.02-$0.20)
- MCP Apps first-mover window = WEEKS not months
- Whop saves $730+ per $10K vs Gumroad

### Session Start Protocol
1. Read `OPS/SESSION_HANDOFF_FEB5_2026.md` for current state
2. Check `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` for blockers
3. Read `.claude/rules/copy-style.md` (all content follows this voice)
4. Run `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary`
5. Default to ralph-style loops for substantial work
6. Continue building

### Session End Protocol (Mandatory)
Before ending any session, update this CLAUDE.md:
1. Add new files to relevant section
2. Update task/method status
3. Add strategic docs to navigation
4. Update "Current Status" with accomplishments
5. Ensure next agent can pick up seamlessly

---

## 2. PROJECT CONTEXT

**Project:** AI-powered content distribution system for solopreneurs
**Stack:** Next.js, Python, Playwright, Google Sheets
**Goal:** Ship MVP, start compounding distribution, measure, scale
**Brand:** @PRINTMAXXER (building-in-public, like @pipelineabuser / @levelsio)

**Philosophy:** Escape the permanent underclass. Build, print, compound. The game rewards aggression not caution.

**Capital Stacking Arc:**
```
$0-$1K/mo     -> Affiliate, meme pages, AI influencers, vibe-coded apps, VA lead gen
$1K-$10K/mo   -> Portfolio apps, info products, services, content monetization
$10K-$50K/mo  -> Paid acquisition, team leverage, portfolio expansion
$50K-$200K/mo -> Strategic exits, PE investments, diversification
$200K+/mo     -> Hedge fund capital management
```

---

## 3. AGENT BEHAVIOR DIRECTIVES

### Autonomous Execution (No Permission Required)

1. **DON'T ASK PERMISSION** - Execute with best judgment
2. **RETRY ON FAILURE** - Try alternative approaches, never give up after first failure
3. **FIX MISTAKES AUTONOMOUSLY** - Don't report problems, fix problems
4. **OPEN FILES AUTOMATICALLY** - `open "/path/to/file.ext"` after creating/updating
5. **HIGH QUALITY BY DEFAULT** - Thorough bot detection, proper deduplication, exact execution
6. **FIGURE IT OUT** - Try multiple approaches until it works

### Quality Standard (Quant Level, Not Basic)

Every research output MUST include:
- Actual costs (not "affordable" - give the number)
- Actual margins (not "good margins" - give the percentage)
- Actual timeframes (not "quickly" - give days/weeks)
- Actual examples with revenue/results

| Basic Work (DON'T) | Quant-Level Work (DO) |
|---------------------|----------------------|
| "POD can be profitable" | "POD home decor 28% CAGR, 50-70% margins" |
| "Use TikTok Shop" | "TikTok Shop 8% + 2.9% = 10.9% total. Whop 5.7%. Save $830 per $10K" |
| "Find trending content" | "Monitor r/OutOfTheLoop, Twitter trending. Design in 15 min. List same day. 3-7 day window" |

### Parallel Execution (Default Mode)

Multiple tasks = multiple parallel agents. ALWAYS. Never sequential unless true dependencies exist.
```
BAD:  Fix app 1 -> Fix app 2 -> Fix app 3
GOOD: Launch 3 agents for apps 1, 2, 3 simultaneously
```

### Content Voice

**Full guide:** `.claude/rules/copy-style.md` (NON-NEGOTIABLE)

Quick check before writing ANY content:
- Zero em dashes (use commas or periods)
- Zero banned AI vocabulary (leverage, utilize, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge, delve, journey)
- Consequence-first hooks (start with result, not explanation)
- Specific numbers always
- Would @pipelineabuser actually post this?

### Action-First Directive

When user says "build X" or "do Y" -> IMMEDIATELY start building/doing, don't create docs about it.
When done with a task -> start next logical task. Don't ask "What's next?"
Only stop for: payments, credentials, publishing decisions.

### Operating Policies (Non-Negotiable)

1. No payment/credentials actions - Create PURCHASE_REQUEST.md and STOP
2. LEDGER CSVs are source of truth - All tracking data lives there
3. Human-in-loop for publishing - Draft for review, don't auto-publish
4. Compliance first - FTC disclosures, no fake testimonials
5. Human-first copy - Follow copy-style.md
6. Security: Flag vulnerabilities with WARNING comment. OWASP Top 10 awareness required
7. Don't reinvent existing systems - Check for existing files before creating new ones

---

## 4. HONEST STATUS (Updated 2026-02-05)

### Reality Check
- **Revenue:** $0 (zero products shipped, zero content published)
- **Alpha entries:** ~1,288 valid unique entries in ALPHA_STAGING.csv (file contains ~3,900 rows but ~63% are corrupted/duplicate from swarm concatenation issues)
- **App builds:** 13 builds in MONEY_METHODS/APP_FACTORY/builds/, 0 shipped to any app store
- **Content:** ~665 files generated, 0 published anywhere
- **Methods tracked:** 88 in MONEY_METHODS_TRACKER.csv
- **Execution gap score:** 12/100 (massive planning, near-zero execution)

### What Actually Works
- Swarm research system (6 parallel agents, produces alpha)
- Quant infrastructure (11 Python scripts, all functional)
- Content generation pipeline (produces quality content)
- Ralph loop pattern (stateless resampling, filesystem memory)

### What Does NOT Work
- Individual ralph loops in ralph/loops/ (BROKEN - most have incomplete prompts or missing run.sh)
- Mega ralph loop (DOCUMENTED but never successfully completed a full day cycle autonomously)
- Chrome MCP tools (frequently unavailable or unreliable)
- Twitter scraper (requires Chrome closed, profile lock conflicts)
- Backtest system has 79.8% false-negative KILL rate (structurally broken scoring)

### Fastest Path to First Dollar
1. List 4 PDFs on Gumroad compiling existing playbooks (1-3 days, $0 cost)
2. Post social content via Buffer CSVs (immediate, $0 cost)
3. Submit biomaxx to App Store (needs Apple Developer $99)
4. Launch cold outbound (needs warmed inboxes)

**Human blockers (10 min total):** Gumroad signup, Stripe connect, X/Twitter account creation

**Full plan:** `06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md`

---

## 5. NAVIGATION (Single Consolidated Table)

### Find Anything

| Need | Location |
|------|----------|
| **LATEST HANDOFF** | `OPS/SESSION_HANDOFF_FEB5_2026.md` |
| **Current status** | `OPS/SESSION_HANDOFF.md` |
| **Human setup tasks** | `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` |
| **Latest alpha** | `LEDGER/ALPHA_STAGING.csv` |
| **All tracking data** | `LEDGER/MEGA_SHEET/` (10 CSVs, 2,512 rows) |
| **Active investments** | `LEDGER/ACTIVE_INVESTMENTS.csv` |
| **Revenue** | `FINANCIALS/REVENUE_TRACKER.csv` |
| **Expenses** | `FINANCIALS/EXPENSE_TRACKER.csv` |
| **Financial dashboard** | `FINANCIALS/FINANCIAL_DASHBOARD.md` |
| **Growth tactics** | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` |
| **Platform limits** | `06_OPERATIONS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md` |
| **Copy style rules** | `.claude/rules/copy-style.md` |
| **Alpha review rules** | `.claude/rules/alpha-review.md` |
| **App builds** | `MONEY_METHODS/APP_FACTORY/builds/` |
| **App monetization** | `MONEY_METHODS/APP_FACTORY/APP_MONETIZATION_STRATEGY.md` |
| **App discovery** | `MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_PROCESS.md` |
| **Cold email sequences** | `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES.md` |
| **LinkedIn templates** | `MONEY_METHODS/COLD_OUTBOUND/LINKEDIN_TEMPLATES.md` |
| **Content calendar** | `LEDGER/CONTENT_CALENDAR_30DAY.csv` |
| **Posting guide** | `OPS/CONTENT_POSTING_GUIDE.md` |
| **Buffer CSVs** | `AUTOMATIONS/content_posting/` (12 CSVs) |
| **High-signal sources** | `LEDGER/HIGH_SIGNAL_SOURCES.csv` (81+ accounts) |
| **Research subreddits** | `LEDGER/RESEARCH_SUBREDDITS.csv` (41 subreddits) |
| **Cross-pollination** | `LEDGER/CROSS_POLLINATION_MATRIX.csv` |
| **GTM checklist** | `06_OPERATIONS/growth/GTM_OPTIMIZATION_CHECKLIST.md` |
| **GTM priorities** | `LEDGER/GTM_OPTIMIZATION_PRIORITIES.csv` |
| **Fastest revenue paths** | `06_OPERATIONS/gtm/FASTEST_REVENUE_PATHS_FEB_2026.md` |
| **First $1K plan** | `06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md` |
| **Gumroad products** | `06_OPERATIONS/gtm/GUMROAD_PRODUCT_SPECS.md` |
| **Service packages** | `OPS/SERVICE_OFFERING_PACKAGES.md` |
| **Content-to-revenue map** | `LEDGER/CONTENT_TO_REVENUE_MAP.csv` |
| **Grey-hat playbook** | `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` |
| **Browser automation** | `OPS/BROWSER_CONTROL/BROWSER_AGENT_GUIDE.md` |
| **Account warmup** | `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` |
| **Manual setup** | `06_OPERATIONS/setup/RETARDMAXX_MANUAL_TODO.md` |
| **Ultimate stack guide** | `06_OPERATIONS/setup/ULTIMATE_STACK_GUIDE.md` |
| **Quant quick start** | `OPS/QUANT_QUICK_START.md` |
| **Quant full guide** | `OPS/QUANT_INFRASTRUCTURE_GUIDE.md` (800+ lines) |
| **Deep alpha report** | `OPS/DEEP_ALPHA_REPORT_FEB_2026.md` |
| **Platform arbitrage** | `OPS/PLATFORM_ARBITRAGE_UPDATE_FEB_2026.md` |
| **Strategic synthesis** | `OPS/PRINTMAXX_STRATEGIC_SYNTHESIS_FEB_2026.md` |
| **Ops audit** | `OPS/OPS_AUDIT_REPORT_FEB_2026.md` |
| **Overnight deliverables** | `OPS/OVERNIGHT_DELIVERABLES_FEB_2026.md` |
| **Swarm research summary** | `ralph/.swarm/SWARM_RESEARCH_SUMMARY_FEB2026.md` |
| **Archived CLAUDE.md content** | `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md` |
| **Master operating doc** | `MASTER_DOC/PRINTMAXX_MASTER_OPERATING_SYSTEM_...v26.md` |
| **LEDGER index** | `LEDGER/LEDGER_INDEX.md` |
| **Money methods index** | `MONEY_METHODS/INDEX.md` |

### Task Router

| "I want to..." | Go to |
|----------------|-------|
| Build an app | `MONEY_METHODS/APP_FACTORY/` then `LEDGER/APP_FACTORY_METHODS.csv` |
| Create content | `06_OPERATIONS/growth/NICHE_POSTING_STRATEGY.md` then `LEDGER/WINNING_CONTENT_STRUCTURES.csv` |
| Do cold outbound | `MONEY_METHODS/COLD_OUTBOUND/` then `LEDGER/OUTREACH_PIPELINE.csv` |
| Run daily research | `/daily-research` skill then `LEDGER/ALPHA_STAGING.csv` |
| Check revenue | `FINANCIALS/REVENUE_TRACKER.csv` |
| Find alpha | `LEDGER/ALPHA_STAGING.csv` filter by category |
| Stack methods | `LEDGER/CROSS_POLLINATION_MATRIX.csv` synergy_score 90+ |
| Launch a product | `06_OPERATIONS/growth/GTM_OPTIMIZATION_CHECKLIST.md` |
| Make first dollar | `06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md` |
| Screen alpha | `python3 AUTOMATIONS/alpha_screening.py --pending` |
| Paper trade | `python3 AUTOMATIONS/paper_trade.py --list` |
| Post content now | `OPS/CONTENT_POSTING_GUIDE.md` then `AUTOMATIONS/content_posting/` |
| Launch quant dashboard | `python3 AUTOMATIONS/printmaxx_quant_terminal.py` |
| Sell services | `OPS/SERVICE_OFFERING_PACKAGES.md` |
| Analyze a funnel | `OPS/TREND_INTEL/templates/FUNNEL_ANALYSIS_TEMPLATE.md` |

### Skills (Invoke with /)

| Skill | Purpose |
|-------|---------|
| `/printmaxx` | Load full PRINTMAXX context |
| `/daily-research` | Scan sources for new alpha |
| `/review-alpha` | Approve/reject staged entries |
| `/status` | Show project status |
| `/deploy-check` | Pre-flight deployment checklist |
| `/remotion-video` | Create marketing videos |

---

## 6. DIRECTORY MAP

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `LEDGER/` | SOURCE OF TRUTH. All tracking CSVs | `LEDGER_INDEX.md`, `MEGA_SHEET/` (10 consolidated CSVs) |
| `MONEY_METHODS/` | Playbooks + builds for all methods | `INDEX.md`, subdirs per method |
| `OPS/` | Operations, handoffs, growth tactics | `SESSION_HANDOFF.md`, growth/ subdir |
| `CONTENT/` | 665 content files | `truth_pages/`, `longtail_pages/`, `social/` |
| `AUTOMATIONS/` | Scripts, scrapers, quant tools | 11 Python quant tools, scrapers |
| `LANDING/` | Next.js site | `printmaxx-site/` (App Router) |
| `FINANCIALS/` | Revenue, expenses, P&L | 7 tracking files |
| `ralph/` | Autonomous loops | `run_mega.sh`, `loops/mega/` |
| `01_STRATEGY/` | Strategic plans | Capital Genesis docs |
| `06_OPERATIONS/` | Setup, growth, GTM | `setup/`, `growth/`, `gtm/` |
| `.claude/` | Agent config, rules, commands | This file, `rules/`, `commands/` |
| `MASTER_DOC/` | 280KB master operating system | v26 reference doc |

### MEGA_SHEET: Consolidated Data Layer

Location: `LEDGER/MEGA_SHEET/` - 10 CSVs combining all 70+ LEDGER files

| Tab | CSV File | Rows | Contains |
|-----|----------|------|----------|
| 1 | TAB1_MONEY_METHODS_MASTER.csv | 68 | All methods + synergy scores |
| 2 | TAB2_NICHES_MASTER.csv | 33 | All niches (N001-N033) |
| 3 | TAB3_ALPHA_MASTER.csv | 835 | Alpha entries (staging + watchlist) |
| 4 | TAB4_TOOLS_CHANNELS_MASTER.csv | 225 | Tools, channels, MCP servers |
| 5 | TAB5_CONTENT_MASTER.csv | 569 | Content pipeline, calendar |
| 6 | TAB6_APPS_ECOM_MASTER.csv | 154 | Apps, clones, ecom, micro SaaS |
| 7 | TAB7_SOURCES_ACCOUNTS.csv | 158 | Sources (81+), social accounts |
| 8 | TAB8_OPERATIONS.csv | 213 | GTM, affiliates, outreach |
| 9 | TAB9_EXPERIMENTS_METRICS.csv | 78 | A/B tests, funnel metrics |
| 10 | TAB10_RESEARCH_MISC.csv | 179 | Research, SEO, repos |

---

## 7. QUANT INFRASTRUCTURE

**Quick Start:** `OPS/QUANT_QUICK_START.md`
**Full Guide:** `OPS/QUANT_INFRASTRUCTURE_GUIDE.md`
**Detailed tool docs:** `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md` (Section: Quant Tool Individual Documentation)

### Tools Summary

| Tool | Command | Purpose |
|------|---------|---------|
| Quant Terminal | `python3 AUTOMATIONS/printmaxx_quant_terminal.py` | Bloomberg-style 6-panel TUI (PRIMARY) |
| Terminal Summary | `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary` | Quick health check (session start) |
| Alpha Screener | `python3 AUTOMATIONS/alpha_screening.py --pending` | Score alpha 0-100 |
| Paper Trader | `python3 AUTOMATIONS/paper_trade.py --list` | Test methods $0-100 budget |
| Revenue Projector | `python3 AUTOMATIONS/revenue_projector.py` | Monte Carlo + Kelly Criterion |
| Portfolio Rebalancer | `python3 AUTOMATIONS/portfolio_rebalancer.py --weekly-report` | KILL/SCALE recommendations |
| Ops Dashboard | `python3 AUTOMATIONS/ops_dashboard.py` | Track 53 ops patterns |
| Method Analyzer | `python3 AUTOMATIONS/method_performance_analyzer.py` | Weekly performance report |
| Agent Monitor | `python3 AUTOMATIONS/agent_monitor.py` | Live agent progress (0.5s) |
| Alpha Validator | `python3 AUTOMATIONS/alpha_validator.py --pending` | Live web validation + decay |
| Niche Meta Detector | `python3 AUTOMATIONS/niche_meta_detector.py` | Pattern matching |
| Platform Monitor | `python3 AUTOMATIONS/platform_meta_monitor.py` | Algorithm changes |
| Memecoin Tracker | `python3 AUTOMATIONS/meme_coin_signal_tracker.py` | Signal detection |

### Quant Workflow

```
DISCOVERY -> SCREEN -> PAPER_TRADE -> DEPLOY -> MONITOR -> REBALANCE
```

### Decision Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Backtest score | >= 70 | DEPLOY |
| Backtest score | 50-69 | PAPER_TRADE first |
| Backtest score | < 50 | KILL |
| Revenue/hour | >= $20 | SCALE |
| Revenue/hour | < $15 for 30d | KILL |
| Method concentration | > 40% | Reduce |
| Platform concentration | > 50% | Diversify |
| Alpha age | > 90 days | Stale, revalidate |

---

## 8. RALPH LOOPS (Canonical Pattern)

### Core Pattern

AI sessions rot after 40-60 min. Don't compact memory, throw it away and start fresh.

```bash
while :; do cat prompt.md | claude --dangerously-skip-permissions --print ; done
```

**Memory = filesystem + git, NOT context window.**

If it's not written to a file, it doesn't exist.

### Key Files Per Loop

```
loop_name/
  prompt.md          # STATIC - never changes during loop
  prd.json           # Task list with passes: true/false
  progress.txt       # Append-only learnings (survives context reset)
  guardrails.md      # Constraints learned from failures
  run.sh             # The while loop runner
```

### Critical Rules

1. **Static prompts** - NEVER let AI modify its own instructions
2. **Filesystem memory** - Write EVERYTHING to files immediately
3. **Append-only logs** - progress.txt grows, never shrinks
4. **Guardrails accumulate** - When something fails, add to guardrails.md
5. **Stories flip to passes: true** - Loop ends when all stories pass

### prd.json Format

```json
{
  "branchName": "feature-name",
  "userStories": [
    {
      "id": "US-001",
      "title": "Story title",
      "description": "Detailed description",
      "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
      "priority": 1,
      "passes": false
    }
  ]
}
```

### Swarm Orchestration

See `ralph/SWARM_ORCHESTRATION_V3.md` for multi-agent coordination.

The swarm system works (6 parallel agents producing alpha). Individual ralph loops in ralph/loops/ are mostly broken. The mega loop at ralph/loops/mega/ has documentation but has not completed a full autonomous day cycle.

### Mega Loop Quick Start

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph
./run_mega.sh      # 1 day = 21 iterations
./run_mega.sh 7    # Full week = 147 iterations
```

**Mega loop docs:** `ralph/loops/mega/prompt.md`
**Progress:** `ralph/loops/mega/.ralph/progress.md`
**Checkpoints:** `ralph/loops/mega/checkpoints/`

**Full mega loop documentation archived:** `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md`

---

## 9. RESEARCH AND ALPHA SYSTEM

### Alpha Pipeline

All new findings -> `LEDGER/ALPHA_STAGING.csv` with status PENDING_REVIEW
Review with `/review-alpha` skill
Full guidelines: `.claude/rules/alpha-review.md`

### Alpha Review Quick Test

1. Has specific numbers? No -> DIG DEEPER (check thread, bio, replies)
2. High engagement (1K+ likes)? -> Signal exists, keep digging
3. Clear method/framework? Partial -> APPROVE with note
4. Can implement this week? No but valuable -> APPROVE with priority BACKLOG
5. Exact duplicate URL? -> REJECT

### Bot Detection (Run First)

- Engagement ratio off (10K likes, 3 comments = botted)
- Generic comments only = suspicious
- Mark `engagement_authenticity: SUSPICIOUS` if botted
- Mark `earnings_verified: FALSE` for unverified claims
- STILL extract the method even if numbers are BS

### Research Sources

All 81+ sources tracked in `LEDGER/HIGH_SIGNAL_SOURCES.csv`
41 subreddits in `LEDGER/RESEARCH_SUBREDDITS.csv`

**Twitter scraping:** `AUTOMATIONS/twitter_alpha_scraper.py` (requires Chrome closed)
**Reddit:** Python requests JSON API (bypasses browser detection): `requests.get("https://www.reddit.com/r/SaaS/top.json?t=week")`
**Browser fallback chain:** `OPS/BROWSER_CONTROL/BROWSER_AGENT_GUIDE.md`

### Zero Waste Protocol

Every research finding gets tagged with:
- `applicable_methods`: Which methods can use this?
- `applicable_niches`: Faith/fitness/tech angles?
- `content_concepts`: Post/product/newsletter angles (list ideas, not full content)
- `product_opportunity`: Gumroad/course/service concept?
- `implementation_priority`: NOW / SOON / BACKLOG

Full 15-output chain and content storage map: `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md`

### GTM Protocol

Before launching ANY product/method:
1. Query `LEDGER/ALPHA_STAGING.csv` for relevant category
2. Check `LEDGER/CROSS_POLLINATION_MATRIX.csv` for synergies
3. Check `LEDGER/GTM_OPTIMIZATION_PRIORITIES.csv` for SEO/ASO/GEO requirements
4. Run `06_OPERATIONS/growth/GTM_OPTIMIZATION_CHECKLIST.md`
5. Full SEO/GEO/ASO checklists: `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md`

### Money Methods (88 Total)

**Core (MM001-MM016):** APP_FACTORY, INFO_PRODUCTS, AFFILIATE_SITES, SAAS, AGENCY_SERVICES, CONTENT_FARM, COLD_OUTBOUND, UGC_ARBITRAGE, AI_INFLUENCER, STREAMER_CLIPS, ROBLOX_GAMES, ALGO_TRADING, PAID_ADS, YOUTUBE_LONGFORM, NEWSLETTER, TIKTOK_SHOP

**Extended (MM022-MM069):** ECOM_DROPSHIP, ECOM_ARB, PRINT_ON_DEMAND, DIGITAL_PRODUCTS, AMAZON_KDP, AI_WRAPPER, MICRO_SAAS, LOCAL_LEAD_GEN, FACELESS_YOUTUBE, plus 20 novel methods (MM050-MM069 including MCP_SERVER_PRODUCTS, AI_AUTOMATION_AGENCY, AI_COMPLIANCE_AUDIT, etc.)

**Content Farm Subs (CF001-CF013):** RELAX, SLEEP_TIMER, NEWS, MEMES, WOMEN, CLIPS, MOTIVATION, FINANCE_NEWS, TECH, SPORTS, CRYPTO_NEWS, STOCK_RESEARCH, YOUTUBE_SHORTS

**AI Influencer Subs (AI001-AI008):** NICHE_EXPERTS, FINDOM, ONLYFANS, ASMR, FITNESS_COACHES, LIFESTYLE, GAMING, RELATIONSHIP

**Tracking:** `LEDGER/MONEY_METHODS_TRACKER.csv`
**Full index:** `MONEY_METHODS/INDEX.md`

### Cross-Pollination

Check `LEDGER/CROSS_POLLINATION_MATRIX.csv` before building ANY method.

Running one method alone = linear returns.
Running 10 methods that cross-pollinate = exponential returns.

Example: Content farm builds audience -> Newsletter converts -> Info products monetize -> Apps retain -> Services upsell

---

## APPENDIX: App Factory Quick Reference

**Before building any app, check these files:**
- Monetization: `MONEY_METHODS/APP_FACTORY/APP_MONETIZATION_STRATEGY.md`
- Assets: `MONEY_METHODS/APP_FACTORY/ASSET_GENERATION_GUIDE.md`
- Clone opps: `LEDGER/APP_CLONE_OPPORTUNITIES.csv`
- Rejection guide: `MONEY_METHODS/APP_FACTORY/APP_STORE_REJECTION_GUIDE.md`
- Launch checklist: `MONEY_METHODS/APP_FACTORY/APP_LAUNCH_FULL_STACK.md`

**After any app milestone:** Launch in iOS Simulator (`npx expo start --ios`), create Remotion marketing video, update APP_LAUNCH_TRACKER.csv.

**MIT repos first:** Search `"{app name} clone" license:mit stars:>100` before building from scratch.

---

## APPENDIX: Gemini API and Video Production

**Gemini API Key:** `/.env` -> `GEMINI_API_KEY`
**MCP Config:** `~/.claude/claude_desktop_config.json`

**Remotion prompts:** `OPS/prompts/remotion/`
- `REMOTION_MASTER_PROMPT.md` - Video styles
- `SOUND_DESIGN_GUIDE.md` - Niche-to-audio matching
- `TIKTOK_MUSIC_TRENDS.md` - Current trending sounds

**Sound quick reference:**
| Niche | Style |
|-------|-------|
| Faith/Prayer | Worship ambient, peaceful piano |
| Fitness/Gym | Brazilian phonk |
| Women's Wellness | Soft pop, empowering R&B |
| Tech/Productivity | Lo-fi, minimal electronic |

---

## APPENDIX: Strategic Intelligence Docs

Read these when doing strategic work. All created Jan-Feb 2026.

| Document | Location |
|----------|----------|
| Unified Plan | `01_STRATEGY/CAPITAL_GENESIS_UNIFIED_PLAN.md` |
| Hedge Fund Intel | `01_STRATEGY/HEDGE_FUND_INTELLIGENCE_REPORT.md` |
| Novel Opportunities (MM050-MM069) | `OPS/NOVEL_OPPORTUNITIES_REPORT.md` |
| Method Stacking Playbook | `01_STRATEGY/METHOD_STACKING_PLAYBOOK.md` |
| Grey-Hat Legal Playbook | `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` |
| Deep Alpha Report | `OPS/DEEP_ALPHA_REPORT_FEB_2026.md` |
| Platform Arbitrage | `OPS/PLATFORM_ARBITRAGE_UPDATE_FEB_2026.md` |
| Strategic Synthesis | `OPS/PRINTMAXX_STRATEGIC_SYNTHESIS_FEB_2026.md` |
| Reprioritized Execution | `01_STRATEGY/CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md` |

---

## Session Log (Most Recent)

### Session: 2026-02-05 (CLAUDE.md Restructuring)

**Task:** Slim CLAUDE.md from 5,899 lines (~65K tokens, 33% context) to ~2,000 lines (~22K tokens)

**Delivered:**
- `.claude/CLAUDE_SLIM.md` - Restructured 9-section version
- `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md` - All archived content preserved

**What changed:**
- Consolidated 4 navigation systems into 1 table
- Removed 1,200 lines of session logs (archived)
- Removed 500+ lines of quant tool details (archived, pointer to guide)
- Removed 300+ lines of browser automation (pointer to BROWSER_AGENT_GUIDE.md)
- Removed 250+ lines of Zero Waste chain details (archived)
- Removed 200+ lines of SEO/ASO/GEO checklists (pointer to GTM_OPTIMIZATION_CHECKLIST.md)
- Removed 150+ lines of tech stack tiers (archived)
- Removed 150+ lines of operating model details (archived)
- Added honest status section with real numbers
- Reduced "CRITICAL:" markers from 34 to 12
- Fixed false metrics claims

**Files Created:**
- `.claude/CLAUDE_SLIM.md`
- `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md`

**Next:** Rename CLAUDE_SLIM.md to CLAUDE.md (backup original first) to activate the slimmed version.
