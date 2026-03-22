## CRITICAL: Master Navigation Map (READ THIS TO FIND ANYTHING)

**Philosophy:** PRINTMAXX = run ALL bootstrapped internet money methods in parallel until revenue scales to hedge fund level capital management. Legal + FTC compliant. Controversial/grey/ethically subjective = OK. Illegal = never. The endgame: reinvest into longevity, community building, organic food, education, family infrastructure.

**Central Nervous System:** `LEDGER/` is the source of truth. All data lives in CSVs. Agent works directly with files on disk (no Google Sheets needed).

**IMPORTANT:** Folder reorganization planned (see `FOLDER_REORGANIZATION_PLAN.md`) but NOT YET executed. Use current structure below for now.

---

## Master Navigation

### Quick rules
1. **START** with `OPS/SESSION_HANDOFF_FEB10_2026.md` every session
2. **TRACK** everything in `LEDGER/` (source of truth). Quick access: `LEDGER/MEGA_SHEET/` (10 CSVs, 2,512 rows)
3. **ALPHA** goes to `LEDGER/ALPHA_STAGING.csv` as PENDING_REVIEW. Format: `.claude/rules/alpha-review.md`. Approve: `/review-alpha`
4. **CONTENT** follows `.claude/rules/copy-style.md` (non-negotiable @pipelineabuser voice check)
5. **HUMAN APPROVALS** go to `ralph/loops/mega/checkpoints/` (PENDING_PURCHASES/PUBLISH/ACCOUNTS/HIGH_RISK). Flag and continue.

### "Where is...?" (complete reference)

| "Where is..." | Location |
|---------------|----------|
| **Latest handoff** | `OPS/SESSION_HANDOFF_FEB10_2026.md` |
| **Current status** | `OPS/SESSION_HANDOFF.md` |
| **Mega loop status** | `ralph/loops/mega/.ralph/progress.md` |
| **Latest alpha** | `LEDGER/ALPHA_STAGING.csv` |
| **All tracking data** | `LEDGER/MEGA_SHEET/` |
| **Revenue** | `FINANCIALS/REVENUE_TRACKER.csv` |
| **Expenses** | `FINANCIALS/EXPENSE_TRACKER.csv` |
| **Human tasks** | `01_STRATEGY/CAPITAL_GENESIS_HUMAN_TASKS.md` |
| **Human review items** | `ralph/loops/mega/checkpoints/` |
| **Growth tactics** | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` |
| **Copy style rules** | `.claude/rules/copy-style.md` |
| **Alpha review rules** | `.claude/rules/alpha-review.md` |
| **App builds** | `MONEY_METHODS/APP_FACTORY/builds/` |
| **Strategic plans** | `01_STRATEGY/CAPITAL_GENESIS_*.md` |
| **Lead gen methods** | `LEDGER/RESEARCH_METHODS_LEAD_GEN.csv` |
| **Launch directories** | `LEDGER/LAUNCH_DIRECTORIES.csv` |
| **Overnight deliverables** | `OPS/OVERNIGHT_DELIVERABLES_FEB_2026.md` |
| **Quant guides** | `OPS/QUANT_QUICK_START.md` / `OPS/QUANT_INFRASTRUCTURE_GUIDE.md` |
| **Deep alpha report** | `OPS/DEEP_ALPHA_REPORT_FEB_2026.md` |
| **Fastest revenue** | `06_OPERATIONS/gtm/FASTEST_REVENUE_PATHS_FEB_2026.md` |
| **First $1K plan** | `06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md` |
| **Content calendar** | `LEDGER/CONTENT_CALENDAR_30DAY.csv` |
| **Posting guide** | `OPS/CONTENT_POSTING_GUIDE.md` |
| **Gumroad products** | `06_OPERATIONS/gtm/GUMROAD_PRODUCT_SPECS.md` |
| **Strategic synthesis** | `OPS/PRINTMAXX_STRATEGIC_SYNTHESIS_FEB_2026.md` |
| **Service packages** | `OPS/SERVICE_OFFERING_PACKAGES.md` |
| **Research subreddits** | `LEDGER/RESEARCH_SUBREDDITS.csv` |
| **Platform arbitrage** | `OPS/PLATFORM_ARBITRAGE_UPDATE_FEB_2026.md` |
| **Ops audit** | `OPS/OPS_AUDIT_REPORT_FEB_2026.md` |
| **Cross-pollination** | `LEDGER/CROSS_POLLINATION_MATRIX.csv` |
| **GTM priorities** | `LEDGER/GTM_OPTIMIZATION_PRIORITIES.csv` |
| **Ralph logs** | `ralph/logs/` |
| **Affiliate launch** | `OPS/AFFILIATE_LAUNCH_CHECKLIST.md` |
| **Cold email launch** | `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` |
| **Upwork launch** | `OPS/UPWORK_LAUNCH_CHECKLIST.md` |
| **Revenue streams tracker** | `LEDGER/REVENUE_STREAMS_TRACKER.csv` |
| **Master Ops (150+ ops, v3)** | `PRINTMAXX_MASTER_OPS.xlsx` ★ |
| **Strategic RBI** | `PRINTMAXX_STRATEGIC_RBI.xlsx` ★ |
| **Viability matrix** | `PRINTMAXX_STRATEGIC_RBI.xlsx` → VIABILITY MATRIX sheet |
| **GTM edge tactics** | `LEDGER/RBI_STRATEGIC/GTM_EDGE_TACTICS.json` ★ |
| **Testable hypotheses** | `LEDGER/RBI_STRATEGIC/HYPOTHESES.json` ★ |
| **Self-test protocol** | `LEDGER/RBI_STRATEGIC/SELF_TEST_PROTOCOL.json` ★ |
| **New op discoveries** | `LEDGER/RBI_STRATEGIC/NEW_OP_DISCOVERIES.json` ★ |
| **Strategic RBI report** | `LEDGER/RBI_STRATEGIC/STRATEGIC_RBI_2026-02-10_full.md` ★ |
| **RBI audit outputs** | `LEDGER/RBI_AUDITS/` |
| **Daily briefings** | `LEDGER/DAILY_BRIEFINGS/` |
| **Learnings database** | `LEDGER/RBI_STRATEGIC/LEARNINGS.jsonl` ★ |
| **Freelance arbitrage** | `PRINTMAXX_FREELANCE_ARB.xlsx` ★ |
| **Freelance pipeline** | `LEDGER/FREELANCE_PIPELINE.csv` |
| **Ops playbook (deep)** | `PRINTMAXX_OPS_PLAYBOOK.xlsx` ★ |
| **Brand names (207)** | `PRINTMAXX_BRAND_NAMES.xlsx` ★ |
| **Infra stacks** | `PRINTMAXX_INFRA_STACKS.xlsx` ★ |
| **Infra assignments** | `PRINTMAXX_INFRA_ASSIGNMENTS.xlsx` ★ |
| **Zero cost deploy** | `PRINTMAXX_ZERO_COST_DEPLOYMENT.xlsx` ★ |
| **NSFW compliance** | `PRINTMAXX_MASTER_OPS.xlsx` → NSFW COMPLIANCE sheet |
| **Findom execution plan** | `MONEY_METHODS/AI_INFLUENCER/AI_NSFW_FINDOM_EXECUTION_PLAN.md` |
| **Findom personas** | `PRODUCTS/branding/FINDOM_PERSONAS.md` |
| **Findom tweets** | `AUTOMATIONS/content_posting/findom_tweets_50.csv` |
| **Builder scripts** | `scripts/builders/` (11 Python scripts) |
| **Cron orchestrator** | `printmaxx_cron.sh` |
| **Strategic RBI engine** | `scripts/strategic_rbi_engine.py` |
| **Daily briefing script** | `scripts/daily_briefing.py` |
| **RBI audit script** | `scripts/rbi_audit.py` |
| **Claude Code handoff** | `CLAUDE_CODE_HANDOFF.md` |
| **RBI Scanner (17 categories)** | `AUTOMATIONS/daily_nocost_rbi_scanner.py` |
| **Social setup outputs** | `ralph/loops/social_setup/output/` |
| **Account creation checklist** | `ralph/loops/social_setup/output/T7_HUMAN_ACCOUNT_CREATION_MASTER.md` |
| **Meme repurpose strategy** | `ralph/loops/social_setup/output/MEME_REPURPOSE_STRATEGY.md` |
| **Ecom launch plan** | `ralph/loops/social_setup/output/ECOM_LAUNCH_PLAN.md` |
| **Full codebase audit** | `ralph/loops/social_setup/output/FULL_AUDIT_MISSING_OPS.md` |
| **Zero-cost acceleration** | `OPS/ZERO_COST_REVENUE_ACCELERATION.md` |
| **Clipping service** | `MONEY_METHODS/CLIPPING_SERVICE/` |
| **Updated accounts (49 rows)** | `LEDGER/ACCOUNTS.csv` |
| **Local biz templates (6)** | `MONEY_METHODS/LOCAL_BIZ/templates/` (dental, restaurant, fitness, legal, plumber, realtor) |
| **Local biz cold email** | `MONEY_METHODS/LOCAL_BIZ/COLD_EMAIL_DEMO_TEMPLATE.md` |
| **Template personalizer** | `MONEY_METHODS/LOCAL_BIZ/personalize_template.py` |
| **Lead scraper (savvy scoring)** | `AUTOMATIONS/savvy_lead_scraper.py` (quant-level 0-100 scoring) |
| **Lead scoring criteria** | `AUTOMATIONS/lead_scoring_criteria.md` |
| **Lead gen runner** | `AUTOMATIONS/run_lead_gen.sh` (10 cities x 5 industries) |
| **Local biz pipeline** | `AUTOMATIONS/local_biz_pipeline.py` (scrape → analyze → generate) |
| **App clone/rebrand strategy** | `MONEY_METHODS/APP_FACTORY/APP_CLONE_REBRAND_STRATEGY.md` |
| **App factory output (6 apps)** | `ralph/loops/app_factory/output/` (dusk, vault, streakr, mise, steplock, prayerlock) |
| **App naming audit** | `MONEY_METHODS/APP_FACTORY/APP_NAMING_AUDIT.md` (794 lines) |
| **Top app audit (24 apps)** | `MONEY_METHODS/APP_FACTORY/TOP_APP_AUDIT.md` |
| **App UI/UX research** | `MONEY_METHODS/APP_FACTORY/APP_UIUX_RESEARCH.md` (20+ apps, benchmarks, design trends) |
| **Onboarding playbook** | `MONEY_METHODS/APP_FACTORY/ONBOARDING_PLAYBOOK.md` (screen-by-screen flows for all 7 apps) |
| **Competitor GTM tactics** | `MONEY_METHODS/APP_FACTORY/COMPETITOR_GTM_TACTICS.md` (how top apps got 10K users) |
| **App Factory GTM master** | `MONEY_METHODS/APP_FACTORY/APP_FACTORY_GTM_MASTER.md` (portfolio launch strategy) |
| **Aggregate design system** | `MONEY_METHODS/APP_FACTORY/AGGREGATE_DESIGN_SYSTEM.md` |
| **App arbitrage matrix** | `MONEY_METHODS/APP_FACTORY/APP_ARBITRAGE_MATRIX.md` |
| **App Store trends Feb 2026** | `MONEY_METHODS/APP_FACTORY/APP_STORE_TRENDS_FEB2026.md` |
| **Arb opportunities (10)** | `MONEY_METHODS/APP_FACTORY/ARB_OPPORTUNITIES_10.md` |
| **Rejection prevention** | `MONEY_METHODS/APP_FACTORY/REJECTION_PREVENTION.md` |
| **GTM by budget** | `MONEY_METHODS/APP_FACTORY/GTM_BY_BUDGET.md` |
| **App asset prompts** | `MONEY_METHODS/APP_FACTORY/APP_ASSET_GENERATION_PROMPTS.md` |
| **Gumroad launch** | `OPS/GUMROAD_LAUNCH_CHECKLIST.md` (731 lines) |
| **Whop launch** | `OPS/WHOP_LAUNCH_CHECKLIST.md` |
| **Fiverr launch** | `OPS/FIVERR_LAUNCH_PACKAGE.md` + `OPS/FIVERR_LAUNCH_CHECKLIST.md` |
| **Upwork launch** | `OPS/UPWORK_LAUNCH_CHECKLIST.md` |
| **Affiliate launch** | `OPS/AFFILIATE_LAUNCH_CHECKLIST.md` (42 programs) |
| **Cold email launch** | `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` |
| **Content syndication** | `OPS/CONTENT_SYNDICATION_LAUNCH.md` (Medium + Substack + 5 platforms) |
| **Revenue streams (100 rows)** | `LEDGER/REVENUE_STREAMS_TRACKER.csv` |
| **Execution dashboard** | `OPS/RETARDMAXX_EXECUTION_DASHBOARD.md` (1,037 lines) |
| **Etsy listings (20)** | `PRODUCTS/ETSY_LISTINGS_20.md` |
| **POD designs** | `PRODUCTS/POD_DESIGNS_20.md` |
| **KDP journals** | `PRODUCTS/KDP_JOURNALS_10.md` |
| **Medium articles (5 new)** | `CONTENT/medium_articles/MEDIUM_BATCH_NEW_5.md` |
| **Motion templates (3)** | `MONEY_METHODS/LOCAL_BIZ/motion_templates/` (dental, restaurant, realtor - animated scroll) |
| **Motion upsell pricing** | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL.md` (3 tiers: $500/$1,500/$3,000) + `MOTION_UPSELL_PRICING.md` (42KB, 10 industry prompts, AI tool comparison, competitive analysis) |
| **Nationwide lead scraper** | `AUTOMATIONS/nationwide_scraper.py` (880 lines, 203 cities, 0-100 scoring) |
| **Mass outreach system** | `AUTOMATIONS/mass_outreach.py` (732 lines, 4-email sequence, demo generator) |
| **Cities database (203)** | `AUTOMATIONS/cities_top200.csv` (44 states, 4 regions, population sorted) |
| **Nationwide lead gen playbook** | `MONEY_METHODS/LOCAL_BIZ/NATIONWIDE_LEAD_GEN_SYSTEM.md` (488 lines) |
| **AI call outreach** | `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` (Bland.ai, TCPA, 3 scripts) |
| **Agency website spec** | `MONEY_METHODS/LOCAL_BIZ/AGENCY_WEBSITE.md` (8 name options, wireframe) |
| **App asset gen prompts** | `MONEY_METHODS/APP_FACTORY/APP_ASSET_GENERATION_PROMPTS.md` (41KB, ImageFX/Nano Banana) |
| **Favicon SVG pack** | `MONEY_METHODS/APP_FACTORY/FAVICON_SVG_PACK.md` (inline SVGs for all 7 apps) |
| **Ramadan tracker PWA** | `ralph/loops/app_factory/output/ramadan-tracker/` (bilingual EN/AR, RTL, Ramadan 2026) |
| **PRINTMAXX app playbook** | `MONEY_METHODS/APP_FACTORY/PRINTMAXX_APP_PLAYBOOK.md` (11-phase assembly line) |
| **AI web design tools comparison** | `MONEY_METHODS/LOCAL_BIZ/AI_WEB_DESIGN_TOOLS.md` (7 tools: Lovable, Bolt, v0, Cursor, Framer, Webflow, Wix) |
| **Viral product arb playbook** | `MONEY_METHODS/ECOM/VIRAL_PRODUCT_ARB_PLAYBOOK.md` (FB Ads Library → Shopify → white label) |
| **Viral product scanner** | `AUTOMATIONS/viral_product_scanner.py` (scan FB Ads Library for validated products) |
| **Ecom arb content (30 posts)** | `AUTOMATIONS/content_posting/ecom_arb_content_30.csv` (build-in-public @PRINTMAXXER posts) |
| **Digital products (Gumroad)** | `DIGITAL_PRODUCTS/` (listings, micro products, PDFs) |
| **Gumroad launch execution** | `DIGITAL_PRODUCTS/GUMROAD_LAUNCH_EXECUTION_GUIDE.md` |
| **Gumroad listing 1** | `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md` |
| **Gumroad listings 2-4** | `DIGITAL_PRODUCTS/listings/` (PRODUCT2, PRODUCT3, PRODUCT4) |
| **Micro product specs** | `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md` |
| **Cold email subject lines (73)** | `DIGITAL_PRODUCTS/micro_products/PRODUCT_1_73_cold_email_subject_lines.md` |
| **Funnel teardown PDF** | `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md` |
| **Products quick prep (2-4)** | `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md` |
| **Nav scanner script** | `scripts/update_claude_md_nav.py` (scan for CLAUDE.md gaps) |
| **Prompt logger** | `AUTOMATIONS/prompt_logger.py` (log/search/audit all user prompts across sessions) |
| **Prompt log data** | `LEDGER/PROMPT_LOG.jsonl` (all user prompts, JSONL format) |
| **Prompt audit export** | `OPS/PROMPT_AUDIT_LOG.md` (markdown export of all prompts) |
| **Ramadan social content** | `CONTENT/social/ramadan/` |
| **Meme engagement tweets** | `AUTOMATIONS/content_posting/meme_engagement_tweets_30.csv` |
| **Mercari/eBay arb** | `PRODUCTS/MERCARI_EBAY_ARB.md` |
| **Redbubble listings** | `PRODUCTS/REDBUBBLE_LISTINGS.md` |
| **Ecom upload checklist** | `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md` |
| **Gumroad cover specs** | `PRODUCTS/GUMROAD_COVER_SPECS.md` |
| **POD designs (50)** | `PRODUCTS/POD_DESIGNS_50.md` |
| **Ramadan reels scripts** | `builds/ramadan_reels_scripts_10.md` |
| **Ramadan tweets (30)** | `builds/ramadan_tweets_30.csv` |
| **App quality standards** | `MONEY_METHODS/APP_FACTORY/APP_QUALITY_STANDARDS.md` |
| **iOS rejection prevention** | `MONEY_METHODS/APP_FACTORY/IOS_REJECTION_PREVENTION.md` |
| **App restructure plan** | `MONEY_METHODS/APP_FACTORY/APP_RESTRUCTURE_PLAN.md` |
| **GitHub repurpose strategy** | `MONEY_METHODS/GITHUB_REPURPOSE_STRATEGY.md` |
| **GitHub repurpose tracker** | `LEDGER/GITHUB_REPURPOSE_TRACKER.csv` |
| **Motion site templates** | `MONEY_METHODS/LOCAL_BIZ/motion_templates/` |
| **Motion upsell pricing** | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL.md` |
| **Agent best practices (OpenAI)** | `OPS/BEST_PRACTICES_AGENT_SKILLS_SHELL_COMPACTION.md` (skills, shell, compaction tips for long-running agents) |
| **First-principles opp matrix** | `OPS/FIRST_PRINCIPLES_OPPORTUNITY_MATRIX.md` |
| **Human execution dashboard** | `OPS/HUMAN_EXECUTION_DASHBOARD.md` |
| **Alpha execution tracker** | `LEDGER/ALPHA_EXECUTION_TRACKER.csv` |
| **Alpha execution report** | `OPS/ALPHA_EXECUTION_REPORT.md` |
| **Info product ops strategy** | `MONEY_METHODS/DIGITAL_PRODUCTS/INFO_PRODUCT_OPS_STRATEGY.md` |
| **Competitor real data** | `MONEY_METHODS/APP_FACTORY/COMPETITOR_REAL_DATA.md` |
| **Gov contract tweet alerts** | `AUTOMATIONS/gov_contract_tweet_alerts.py` |
| **Substack content batch** | `CONTENT/substack_posts/SUBSTACK_BATCH_10.md` |
| **Substack launch guide** | `CONTENT/substack_posts/SUBSTACK_LAUNCH_GUIDE.md` |
| **Deploy all apps script** | `AUTOMATIONS/deploy_all_apps.sh` |
| **Substack Notes (50)** | `CONTENT/substack_posts/SUBSTACK_NOTES_50.csv` |
| **Session squeeze content (Feb 12)** | `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB12.md` |
| **Account creation helper** | `AUTOMATIONS/account_creation_helper.py` |
| **Twitter account quick sheets** | `OPS/TWITTER_ACCOUNT_QUICK_SHEETS/` (directory) |
| **Grey hat edge growth master** | `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md` |
| **Pre-warmed account buying guide** | `OPS/PREWARMED_ACCOUNT_BUYING_GUIDE.md` |
| **Twitter account creation SOP** | `OPS/TWITTER_ACCOUNT_CREATION_SOP.md` |
| **Free tier setup guide** | `OPS/FREE_TIER_SETUP_GUIDE.md` |
| **Account creation master process** | `OPS/ACCOUNT_CREATION_MASTER_PROCESS.md` |
| **Community monetization playbook** | `MONEY_METHODS/COMMUNITY/COMMUNITY_MONETIZATION_PLAYBOOK.md` |
| **--- FEB 12 SESSION FILES ---** | |
| **Daily agent runner** | `AUTOMATIONS/daily_agent_runner.py` (auto-orient any new agent in 10 seconds) |
| **Agent daily playbook** | `OPS/AGENT_DAILY_PLAYBOOK.md` (THE guide for any new session) |
| **Venture performance tracker** | `AUTOMATIONS/venture_performance_tracker.py` (score methods 0-100, KILL/MAINTAIN/DOUBLE_DOWN) |
| **Account creation NOW** | `OPS/ACCOUNT_CREATION_NOW.md` (definitive step-by-step, priority order) |
| **Master ops gap analysis** | `OPS/MASTER_OPS_GAP_ANALYSIS.md` (missing ventures identified) |
| **AI NSFW full execution** | `MONEY_METHODS/AI_INFLUENCER/AI_NSFW_EXECUTION_FULL.md` (38KB, compliance + monetization + subreddits) |
| **Fiverr gigs (10)** | `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md` (copy-paste ready) |
| **Upwork profiles (5)** | `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md` (copy-paste ready) |
| **Etsy listings complete** | `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md` (90KB, full listings) |
| **System products package** | `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md` (53KB, PRINTMAXX as sellable products) |
| **NoFap/KarmaMaxx app spec** | `MONEY_METHODS/APP_FACTORY/NOFAP_KARMAMAXX_APP_SPEC.md` (30KB, full PWA spec) |
| **Cold email sequences ready** | `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv` (ready to send) |
| **Gov contract tweets (50)** | `AUTOMATIONS/content_posting/gov_contract_tweets_50.csv` (expanded) |
| **Browser auto-lister** | `AUTOMATIONS/auto_list_products.py` (Playwright automated product listing) |
| **AI agent services playbook** | `MONEY_METHODS/AI_AGENT_SERVICES/AI_AGENT_SERVICES_PLAYBOOK.md` (new method) |
| **Prediction market arb playbook** | `MONEY_METHODS/PREDICTION_MARKETS/PREDICTION_MARKET_ARB_PLAYBOOK.md` (new method) |
| **Prompt marketplace playbook** | `MONEY_METHODS/PROMPT_MARKETPLACE/PROMPT_MARKETPLACE_PLAYBOOK.md` (new method) |
| **Session handoff FEB12** | `OPS/SESSION_HANDOFF_FEB12_2026.md` (latest state) |
| **--- FEB 12 SESSION B FILES ---** | |
| **Cold email generator** | `AUTOMATIONS/generate_cold_emails.py` (610 lines, auto-match surge.sh demos, 3-email sequences) |
| **Website signal scorer** | `AUTOMATIONS/website_signal_scorer.py` (637 lines, score 0-100, 15 signals) |
| **Email sender** | `AUTOMATIONS/email_sender.py` (606 lines, smtplib, rate-limited, --dry-run) |
| **Auto account creator** | `AUTOMATIONS/auto_account_creator.py` (518 lines, Playwright, CAPTCHA detection) |
| **Perpetual improvement runner** | `AUTOMATIONS/perpetual_improvement_runner.py` (530 lines, 5-loop orchestrator) |
| **Full ship audit** | `OPS/FULL_SHIP_AUDIT.md` (730 lines, 182 ops audited) |
| **System wiring diagram** | `OPS/SYSTEM_WIRING_DIAGRAM.md` (5 perpetual loops mapped) |
| **Master launch dashboard** | `OPS/MASTER_LAUNCH_DASHBOARD.md` (470 lines, command center) |
| **Mobile app submission guide** | `OPS/MOBILE_APP_SUBMISSION_GUIDE.md` (350+ lines) |
| **Browser automation setup** | `OPS/BROWSER_AUTOMATION_SETUP.md` (proxy, anti-detect, warmed accounts) |
| **Deploy log (16 sites)** | `OPS/DEPLOY_LOG.md` (all live URLs + redeploy commands) |
| **Gumroad instant upload (13)** | `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` (13 products, copy-paste ready) |
| **Fiverr instant upload (11)** | `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_01-10.md` (11 gigs, 3-tier pricing) |
| **Digital product PDFs (5)** | `DIGITAL_PRODUCTS/ready_to_sell/pdfs/` (18-35KB each) |
| **Scored leads (952)** | `AUTOMATIONS/leads/SCORED_LEADS.csv` (website scores 0-100) |
| **Hot leads (170)** | `AUTOMATIONS/leads/HOT_LEADS.csv` (score <= 30, highest priority) |
| **Master leads (977)** | `AUTOMATIONS/leads/MASTER_LEADS.csv` (all consolidated) |
| **Cold email batch (2,987)** | `AUTOMATIONS/outreach/MASTER_LEADS_emails.csv` (Instantly-compatible) |
| **Pipeline tracker (87)** | `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` |
| **Crontab v2 (22 jobs)** | `AUTOMATIONS/crontab_printmaxx_v2.txt` (installed) |
| **Tweets session 2** | `CONTENT/social/ai/TWEETS_FEB12_SESSION2.md` (3 tweets + 1 thread) |
| **--- FEB 12 SESSION D (AUTONOMOUS SYSTEM + LEAD PIPELINE) ---** | |
| **Intelligent lead qualifier** | `AUTOMATIONS/intelligent_lead_qualifier.py` (1,052 lines, 2.87M leads, website analysis, 0-100 scoring) |
| **Closed-loop pipeline** | `AUTOMATIONS/closed_loop_pipeline.py` (qualify→email→track, crash recovery, cron-ready) |
| **Memory manager** | `AUTOMATIONS/memory_manager.py` (3-layer OpenClaw memory: heartbeat + active tasks + daily logs) |
| **HEARTBEAT** | `OPS/HEARTBEAT.md` (<20 lines, pure numbers, 3-second system pulse) |
| **Active tasks (crash recovery)** | `OPS/active-tasks.md` (what's running NOW, resume on crash) |
| **Daily logs** | `AUTOMATIONS/logs/daily/YYYY-MM-DD.md` (append-only daily execution log) |
| **Pipeline metrics** | `AUTOMATIONS/leads/qualified/pipeline_metrics.jsonl` (JSONL metrics per cycle) |
| **Pre-filtered leads (1.45M)** | `AUTOMATIONS/leads/qualified/PREFILTERED_LEADS.csv` (deduplicated, domain-normalized) |
| **Analyzed leads (30,200)** | `AUTOMATIONS/leads/qualified/ANALYZED_LEADS.csv` (website-scored, full breakdown) |
| **Hot leads qualified (2,618)** | `AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv` (score >= 65, ready for outreach) |
| **Warm leads qualified (15,739)** | `AUTOMATIONS/leads/qualified/WARM_LEADS_QUALIFIED.csv` (score 45-64) |
| **--- FEB 12 SESSION C (RIGOR AUDIT + APP QUALITY FIXES) ---** | |
| **App quality audit (REAL)** | `MONEY_METHODS/APP_FACTORY/APP_QUALITY_AUDIT_REAL.md` (27KB, portfolio avg 42.7/100, code-level audit) |
| **Rigor audit (all assets)** | `OPS/RIGOR_AUDIT_FEB12.md` (31KB, overall 6.8/10, websites 5.5, emails 7, products 7.5, scrapers 8.5) |
| **NSFW status audit** | `MONEY_METHODS/AI_INFLUENCER/NSFW_STATUS_AUDIT.md` (21KB, 5000 lines docs / 0 execution) |
| **iOS submission process (6-phase)** | `MONEY_METHODS/APP_FACTORY/IOS_SUBMISSION_PROCESS.md` (48KB, real Apple guidelines, pre-build→post-accept) |
| **AI video tools comparison** | `MONEY_METHODS/AI_INFLUENCER/AI_VIDEO_TOOLS_COMPARISON.md` (15KB, 8 tools, Seedance 2.0 deep dive) |
| **VIDEO PIPELINE (Mar 2026)** | |
| Video editor (FFmpeg) | `AUTOMATIONS/claude_video_editor.py` — captions, hooks, CTA, resize, music, Remotion |
| Video script generator | `AUTOMATIONS/ai_video_content_pipeline.py` — auto tool selection from tracker |
| Video posting queue | `LEDGER/VIDEO_POSTING_QUEUE.csv` — edited videos ready for posting |
| Post videos CLI | `AUTOMATIONS/auto_content_poster.py --post-video` — reads queue, uploads to Twitter |
| Viral template extractor | `AUTOMATIONS/viral_content_scanner.py --extract-templates` — mines viral patterns |
| Tool researcher | `AUTOMATIONS/perpetual_tool_researcher.py` — ALL tool categories, Capital Genesis feed |
| Tool tracker CSV | `10_RESEARCH/VIDEO_RESEARCH/tools_tracker/ALL_TOOLS_TRACKER.csv` — 25 tools, 6 categories |
| Video research hub | `10_RESEARCH/VIDEO_RESEARCH/README.md` — master comparison, pipeline spec, templates |
| Viral formats library | `10_RESEARCH/VIDEO_RESEARCH/templates/VIRAL_FORMATS.md` — 8 hook types, 7 formats |
| Master video comparison | `10_RESEARCH/VIDEO_RESEARCH/comparisons/MASTER_VIDEO_TOOLS_2026.md` — canonical Mar 2026 |
| Pipeline spec | `10_RESEARCH/VIDEO_RESEARCH/pipeline/VIDEO_AUTOPILOT_SPEC.md` — full autopilot design |
| n8n workflow spec | `10_RESEARCH/VIDEO_RESEARCH/pipeline/N8N_VIDEO_WORKFLOW.md` — subscription-only |
| **App discovery engine** | `MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_ENGINE.md` (41KB, CloneChart + Appkittie + 7-phase process) |
| **Real screenshot audit (15 apps)** | `MONEY_METHODS/APP_FACTORY/REAL_SCREENSHOT_AUDIT.md` (35KB, verified revenue, onboarding steps, color palettes) |
| **Aggregate design system v2** | `MONEY_METHODS/APP_FACTORY/AGGREGATE_DESIGN_SYSTEM_V2.md` (25KB, supersedes v1, real data from top apps) |
| **--- FEB 13 SESSION (PARALLEL SHIPPING SPRINT + AGENT TEAMS) ---** | |
| **Personalized demo generator** | `AUTOMATIONS/personalize_demos.py` (200 lines, maps 30+ categories to 6 templates, CLI: --top/--category/--deploy) |
| **Pipeline dashboard generator** | `AUTOMATIONS/refresh_dashboard.py` (200 lines, Bloomberg-style HTML with Chart.js, 6 panels) |
| **SEO competitor analyzer** | `AUTOMATIONS/seo_competitor_analyzer.py` (737 lines, competitive grouping, cold-email snippets, --summary/--export) |
| **Unified CLI (printmaxx.py)** | `AUTOMATIONS/printmaxx.py` (480 lines, 12 subcommands wrapping 28+ scripts) |
| **Session squeeze content (Feb 13)** | `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13.md` (5 tweets + 7-tweet thread + Reddit post) |
| **Pipeline dashboard (LIVE)** | `https://printmaxx-dashboard.surge.sh` (Bloomberg-style pipeline dashboard) |
| **Personalized demos (LIVE, 100)** | `https://printmaxx-demos.surge.sh` (100 personalized landing pages for hot leads) |
| **Site score analyzer (LIVE)** | `https://sitescore-analyzer.surge.sh` (web frontend for SEO competitor analysis) |
| **Dashboard HTML output** | `output/dashboard/index.html` (generated by refresh_dashboard.py) |
| **Personalized demo output (100)** | `output/personalized_demos/` (100 subdirectories with personalized index.html) |
| **Demo manifest** | `output/personalized_demos/MANIFEST.csv` (all generated demos with slugs, categories, scores) |
| **SEO analyzer web frontend** | `builds/seo-analyzer-web/index.html` (single-page web app for site scoring) |
| **Response tracker** | `AUTOMATIONS/response_tracker.py` (392 lines, campaign funnel: QUEUED→SENT→OPENED→REPLIED→BOOKED→CLOSED) |
| **Lead enrichment engine** | `AUTOMATIONS/lead_enrichment.py` (306 lines, Google rating, social, tech stack, competitors, hooks) |
| **Cold email A/B test** | `AUTOMATIONS/cold_email_ab_test.py` (396 lines, hash-based split, 2 variant templates, chi-square significance) |
| **Overnight orchestrator** | `AUTOMATIONS/overnight_orchestrator.py` (308 lines, 3-phase pipeline, lock file, retry logic) |
| **Email domain health** | `AUTOMATIONS/email_domain_health.py` (367 lines, SPF/DKIM/DMARC/MX/blacklist/age, 0-100 score) |
| **Client onboarding** | `AUTOMATIONS/client_onboarding.py` (346 lines, auto-generates welcome/brief/timeline/invoice/checklist) |
| **Portfolio site (LIVE)** | `https://printmaxx-portfolio.surge.sh` (agency credibility site with pricing + live demos) |
| **Website analyzer (LIVE)** | `https://printmaxx-analyzer.surge.sh` (lead-gen tool with animated scanning + score ring) |
| **Analyzed leads (33,200)** | `AUTOMATIONS/leads/qualified/ANALYZED_LEADS.csv` (website-scored, full breakdown) |
| **Hot leads qualified (2,908)** | `AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv` (score >= 65, ready for outreach) |
| **Warm leads qualified (17,408)** | `AUTOMATIONS/leads/qualified/WARM_LEADS_QUALIFIED.csv` (score 45-64) |
| **Personalized demos (600)** | `output/personalized_demos/` (600 personalized landing pages, deployed to surge.sh) |
| **Cold emails ready** | `output/cold_emails/cold_emails_ready.csv` + `instantly_step*.csv` (personalized 3-email sequences) |
| **Trend-to-listing pipeline** | `AUTOMATIONS/trend_to_listing.py` (775 lines, trend→POD/Gumroad/Etsy/social listings, winner tracking) |
| **System health monitor** | `AUTOMATIONS/system_health_monitor.py` (820 lines, 14-point health check, GREEN/AMBER/RED) |
| **Greenlight iOS checker** | `AUTOMATIONS/greenlight_checker.py` (wrapper for RevylAI Greenlight pre-submission scanner) |
| **Daily research pipeline** | `AUTOMATIONS/daily_research_pipeline.py` (~600 lines, scrape→extract→filter→repurpose master orchestrator, cron 6:30 AM) |
| **ImportYeti sourcing scanner** | `AUTOMATIONS/import_sourcing_scanner.py` (~700 lines, Playwright ImportYeti scraper, US customs data, factory intel, cron 4 AM) |
| **Import sourcing intel** | `LEDGER/IMPORT_SOURCING_INTEL.csv` (factory sourcing data from ImportYeti scans) |
| **Contact-ready factories** | `LEDGER/CONTACT_READY_FACTORIES.csv` (factories with Alibaba/Google contact URLs) |
| **Sourcing report** | `OPS/SOURCING_REPORT.md` (markdown sourcing intelligence report) |
| **Auto-generated content** | `CONTENT/social/auto_generated/` (daily auto-repurposed content from alpha pipeline) |
| **Daily research digest** | `OPS/DAILY_RESEARCH_DIGEST_*.md` (daily alpha extraction summary with top approved entries) |
| **Unified alpha digest** | `OPS/UNIFIED_ALPHA_DIGEST_*.md` (daily consolidated: Reddit niche + GitHub MIT + ASO + competitors + freshness) |
| **Unified alpha monitor** | `AUTOMATIONS/unified_alpha_monitor.py` (540 lines, 350+ sources, covers gaps in existing scrapers, cron 5:45 AM) |
| **--- FEB 13 SESSION B (LIVE DASHBOARD + COMPLIANCE + PIPELINE EXECUTION) ---** | |
| **Live monitoring dashboard** | `AUTOMATIONS/live_dashboard_server.py` (22KB Flask server, /api/status JSON, 14 real-time data panels) |
| **Live dashboard frontend** | `AUTOMATIONS/live_dashboard.html` (30KB Bloomberg-style, Chart.js, 30s auto-refresh) |
| **Content compliance scanner** | `AUTOMATIONS/compliance_scanner.py` (~400 lines, FTC/CAN-SPAM/income/PII/fake-proof/health/platform) |
| **Compliance scan report** | `OPS/COMPLIANCE_SCAN_2026_02_13.md` (4,828 lines, 285 CRITICAL, 1,796 WARNING, 5 INFO) |
| **Compliance scan JSON** | `LEDGER/compliance_scan_2026_02_13.json` (machine-readable compliance data) |
| **Freelance response templates (10)** | `AUTOMATIONS/freelance_response_templates/` (copy-paste Reddit replies, $3K one-time + $9.4K/mo) |
| **Freelance pipeline active** | `LEDGER/FREELANCE_PIPELINE_ACTIVE.csv` (10 active opportunities, scores, priorities) |
| **Hot leads rebuilt (21)** | `AUTOMATIONS/leads/HOT_LEADS.csv` (rebuilt, filtered junk, real emails + scores <= 60) |
| **Hot batch cold emails (359)** | `AUTOMATIONS/outreach/HOT_BATCH_FEB13.csv` (3-step sequences, Instantly-compatible) |
| **Local biz execution status** | `OPS/LOCAL_BIZ_EXECUTION_STATUS.md` (full pipeline status, 87 READY, single blocker: email infra) |
| **Signal account directory** | `OPS/SIGNAL_ACCOUNT_DIRECTORY.md` (304 lines, 13 categories, 116+ accounts, quick lookup table) |
| **--- CENTRAL INDEX FILES (navigate EVERYTHING from here) ---** | |
| **App Factory central index** | `MONEY_METHODS/APP_FACTORY/APP_FACTORY_CENTRAL_INDEX.md` (all 6 apps, all docs, status, next actions) |
| **Products central index** | `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md` (674 lines, all products by platform, duplicates flagged) |
| **Leads/Outreach central index** | `OPS/LEADS_OUTREACH_CENTRAL_INDEX.md` (all leads, emails, scrapers, pipeline status) |
| **Content central index** | `CONTENT/CONTENT_CENTRAL_INDEX.md` (506 lines, 3,300+ pieces, all tweets/posts/articles/scripts by platform) |
| **Social account acquisition** | `OPS/SOCIAL_ACCOUNT_ACQUISITION_GUIDE.md` (Fameswap/Swapd/AccsMarket + proxy + anti-detect browser setup) |
| **Niche account expansion strategy** | `OPS/NICHE_ACCOUNT_EXPANSION_STRATEGY.md` (833 lines, 19 accounts mapped, 6 expansion proposals, prioritization matrix, content repurposing playbook, rising niche detector) |
| **Master file audit** | `OPS/MASTER_FILE_AUDIT.md` (893 lines, full project audit, orphans, duplicates, cleanup priorities P0-P3) |
| **Ecom arb engine (LIVE)** | `AUTOMATIONS/ecom_arb_engine.py` (real Amazon/eBay prices, AliExpress sourcing, profit calc, cron every 2h) |
| **Freelance demand scanner (LIVE)** | `AUTOMATIONS/freelance_demand_scanner.py` (9 subreddits, 10 AI-deliverable services, scores 0-100) |
| **Trend aggregator (LIVE)** | `AUTOMATIONS/trend_aggregator.py` (Google Trends + Reddit + PH, trend→product matching, cron every 4h) |
| **Ecom arb opportunities** | `LEDGER/ECOM_ARB_OPPORTUNITIES.csv` (real scan data, profit margins, best platform per product) |
| **Freelance demand scan** | `LEDGER/FREELANCE_DEMAND_SCAN.csv` (active hiring posts matched to our services) |
| **Freelance pipeline CLI** | `AUTOMATIONS/freelance_pipeline.py` (460 lines, --scan/--pipeline/--portfolio/--revenue/--daily) |
| **Freelance arb execution playbook** | `OPS/FREELANCE_ARB_EXECUTION.md` (OP17 complete playbook, 95%+ margin model) |
| **Multi-platform listings (10 platforms)** | `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md` (1184 lines, copy-paste ready) |
| **SiteScore SaaS (LIVE)** | `https://sitescore-app.surge.sh/` + `builds/site-scorer/` (website analyzer demo) |
| **ShopMetrics Dashboard (LIVE)** | `https://shopmetrics-dashboard.surge.sh/` + `builds/portfolio/dashboard/` (analytics demo) |
| **Flowstack Landing Page (LIVE)** | `https://flowstack-demo.surge.sh/` + `builds/portfolio/landing-page/` (SaaS landing demo) |
| **Trend signals** | `LEDGER/TREND_SIGNALS.csv` (multi-source trend detection, category heat map) |
| **Programmatic SEO (LIVE)** | `https://printmaxx-seo.surge.sh/` (602 pages deployed, indexed) |
| **Arb listing generator** | `AUTOMATIONS/arb_listing_generator.py` (FB/eBay/Mercari listings from scan data) |
| **Arb listings (copy-paste)** | `PRODUCTS/ARB_LISTINGS/ARB_LISTINGS_2026_02_12.md` (7 products, 3 platforms) |
| **Arb sourcing guide** | `PRODUCTS/ARB_SOURCING/SOURCING_GUIDE_2026_02_12.md` (AliExpress/Alibaba/CJ links) |
| **Freelance responses (copy-paste)** | `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md` (3 real posts, template library) |
| **Demo sites (fixed, live)** | `https://printmaxx-local-demos.surge.sh/` (dental, restaurant, fitness, legal, plumber, realtor) |
| **--- FEB 13 SESSION C (12-ACCOUNT SOCIAL EMPIRE + ANTI-DETECT + CONTENT) ---** | |
| **12-account creation plan** | `OPS/10_ACCOUNTS_CREATION_PLAN.md` (12 accounts, bios, voice, monetization, platform distribution) |
| **Account setup matrix** | `OPS/ACCOUNT_SETUP_MATRIX.md` (~45 accounts, browser profiles, creation order, content status) |
| **Anti-detect browser profiles** | `OPS/ANTIDETECT_BROWSER_PROFILES.md` (5 groups, email/phone strategy, warmup schedule) |
| **Proxy + VPN wiring guide** | `OPS/PROXY_ANTIDETECT_VPN_WIRING_GUIDE.md` (Dolphin Anty + SOAX + VPN, Playwright automation, A/B test) |
| **Safe warmup automation guide** | `OPS/SAFE_WARMUP_AUTOMATION_GUIDE.md` (562 lines, per-platform warmup schedules, API vs browser risk matrix, anti-detect comparison, 35+ sources) |
| **Handle availability check** | `OPS/HANDLE_AVAILABILITY_CHECK.md` (12 handles checked, alternatives for taken ones) |
| **@toolstwts content (452 lines)** | `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md` (14 tweets, 2 threads, 7 YT Shorts) |
| **@growthpilled content (540 lines)** | `CONTENT/social/growthpilled/FIRST_WEEK_CONTENT.md` (14 tweets, 2 threads, 7 TikTok/Reels) |
| **@clipvault_ content (576 lines)** | `CONTENT/social/clipvault/FIRST_WEEK_CONTENT.md` (14 captions, sourcing playbook, hashtag sets) |
| **@shiplog_ content (598 lines)** | `CONTENT/social/shiplog/FIRST_WEEK_CONTENT.md` (14 tweets, 2 threads, 7 YT Shorts, 3 PH drafts) |
| **@drifthour content (596 lines)** | `CONTENT/social/drifthour/FIRST_WEEK_CONTENT.md` (14 posts, 3 YT Long, 3 Shorts, 5 Spotify) |
| **@outboundtwts content (777 lines)** | `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md` (14 tweets, 2 threads, 7 LinkedIn, 5 YT) |
| **@selahmoments content (943 lines)** | `CONTENT/social/selahmoments/FIRST_WEEK_CONTENT.md` (14 posts, 2 threads, 10 Ramadan, 7 Reels, 3 Substack) |
| **@repscheme content (734 lines)** | `CONTENT/social/repscheme/FIRST_WEEK_CONTENT.md` (14 tweets, 2 threads, 7 Reels, 7 IG carousels) |
| **@voidpilled content (306 lines)** | `CONTENT/social/esoteric/FIRST_WEEK_CONTENT.md` (14 tweets, 2 threads, sacred geometry guide) |
| **@silentframes content (417 lines)** | `CONTENT/social/aesthetic/FIRST_WEEK_CONTENT.md` (14 captions, sourcing guide, carousel concepts) |
| **@velvetframes beauty content** | `CONTENT/social/beauty_curated/FIRST_WEEK_CONTENT.md` (14 captions, legal compliance, sourcing playbook, monetization path) |
| **Curated beauty page playbook** | `OPS/CURATED_BEAUTY_PAGE_PLAYBOOK.md` (legal framework, DMCA, right of publicity, monetization) |
| **Account setup matrix (13 brands)** | `OPS/ACCOUNT_SETUP_MATRIX.md` (13 brands × platforms = ~49 accounts, browser profiles, proxy assignments, handle availability) |
| **--- FEB 15 SESSION (OPS AUDIT AUTOMATION — COMPLIANCE + TELEGRAM + ALPHA MONITOR) ---** | |
| **Compliance deadline tracker** | `AUTOMATIONS/compliance_deadline_tracker.py` (~450 lines, 21 regulations, RSS scanning, digest generation, cron 8:45 AM daily + 6:30 AM Mon) |
| **Compliance deadlines CSV** | `LEDGER/COMPLIANCE_DEADLINES.csv` (21 regulatory deadlines with days remaining, urgency, penalties) |
| **Compliance deadline digest** | `OPS/COMPLIANCE_DEADLINE_DIGEST_*.md` (markdown digest of all compliance deadlines, auto-generated) |
| **Telegram community monitor** | `AUTOMATIONS/telegram_community_monitor.py` (~450 lines, 26 channels, 8 niches, signal keyword scoring, cron 9:15 AM) |
| **Telegram signals CSV** | `LEDGER/TELEGRAM_SIGNALS.csv` (signal extraction from public Telegram channels, deduped) |
| **Reddit pain point miner** | `AUTOMATIONS/reddit_pain_point_miner.py` (~400 lines, 25 subreddits, buying intent extraction, cron 6:30 AM) |
| **Unified alpha monitor** | `AUTOMATIONS/unified_alpha_monitor.py` (540 lines, 350+ sources: Reddit niche + GitHub MIT + ASO + competitors + freshness, cron 5:45 AM) |
| **--- MAR 3 SESSION (CONTENT PIPELINE + APP CLONE + 35 AGENTS + UGCDROP) ---** | |
| **Content trend pipeline** | `AUTOMATIONS/content_trend_pipeline.py` (~350 lines, trend→content for 5 accounts, hook templates, PRINTMAXXER voice) |
| **App clone pipeline** | `AUTOMATIONS/app_clone_pipeline.py` (~540 lines, 61 clone opps, 6 apps × 9 langs × 6 demos, rebrand packages) |
| **App clone packages** | `MONEY_METHODS/APP_FACTORY/clone_packages/` (generated rebrand packages with asset prompts + checklists) |
| **Tweet auto drafter** | `AUTOMATIONS/tweet_auto_drafter.py` (auto-draft tweets from scraped high-signal content) |
| **Quote tweet scanner** | `AUTOMATIONS/quote_tweet_scanner.py` (find QT opportunities from monitored accounts) |
| **Scheduled tasks framework** | `OPS/SCHEDULED_TASKS_FRAMEWORK.md` (cron, LaunchD, overnight loops, all automation scheduling) |
| **Agent directory (39 agents)** | `.claude/agents/` (8 categories: eng 5, prod 4, mkt 6, design 3, pm 4, studio 7, test 4, research 2) |
| **UGCDrop ops** | Added to `PRINTMAXX_MASTER_OPS.xlsx` ($0.01 UGC clips, affiliate opportunity) |
| **--- MAR 4 SESSION (AUTONOMOUS AGENT LOOP SYSTEM) ---** | |
| **Autonomous orchestrator** | `AUTOMATIONS/autonomous_orchestrator.py` (~300 lines, generates Claude session prompts from system state, runs headless Claude sessions, routes outputs) |
| **Auto rebalancer** | `AUTOMATIONS/auto_rebalancer.py` (~300 lines, kill losers/reinvest winners, composite scoring, 7-day rolling health, checkpoints for kills) |
| **Checkpoint manager** | `AUTOMATIONS/checkpoint_manager.py` (~200 lines, human-in-the-loop: PURCHASE/PUBLISH/ACCOUNT/STRATEGY/KILL approvals) |
| **Schedule Claude** | `AUTOMATIONS/schedule_claude.sh` (~100 lines, cron-callable: disk guard, lock file, caffeinate, 30min timeout, 3 daily sessions) |
| **SaaS product scanner** | `AUTOMATIONS/saas_product_scanner.py` (~300 lines, scores 12 automations for SaaS potential, generates manifest) |
| **SaaS product manifest** | `OPS/SAAS_PRODUCT_MANIFEST.md` (12 SaaS candidates ranked, detailed breakdown, anti-abuse architecture) |
| **Semantic memory search** | `AUTOMATIONS/semantic_memory_search.py` (TF-IDF search across all JSONL logs + markdown, 1,175 docs, 14 categories) |
| **Search index** | `AUTOMATIONS/logs/.search_index/` (tfidf_index.json + documents.json, rebuilt daily 4:30 AM) |
| **Claude subconscious setup** | `AUTOMATIONS/setup_subconscious.sh` (letta-ai persistent memory plugin for interactive sessions, requires API key) |
| **PRINTMAXX Desktop App** | `AUTOMATIONS/printmaxx_desktop.py` (~650 lines, tkinter GUI, 5 tabs, hourly macOS notifications, 40 motivational quotes, alarm system, launch tracker, quick-launch buttons) |
| **Product Launch Automator** | `AUTOMATIONS/product_launch_automator.py` (~450 lines, 17 directory guides, 6 products, copy gen, tab opening, CSV tracking, submission checklists) |
| **Launch copy output** | `OPS/LAUNCH_COPY_{PRODUCT}.md` (auto-generated submission copy per product) |

### "I want to..." (task router)

| "I want to..." | Start Here |
|----------------|------------|
| Build an app | `MONEY_METHODS/APP_FACTORY/` + `APP_FACTORY_GTM_MASTER.md` + `ONBOARDING_PLAYBOOK.md` |
| Launch an app | `MONEY_METHODS/APP_FACTORY/APP_FACTORY_GTM_MASTER.md` + `COMPETITOR_GTM_TACTICS.md` |
| Design app onboarding | `MONEY_METHODS/APP_FACTORY/ONBOARDING_PLAYBOOK.md` + `APP_UIUX_RESEARCH.md` |
| Create content | `06_OPERATIONS/growth/NICHE_POSTING_STRATEGY.md` + `LEDGER/WINNING_CONTENT_STRUCTURES.csv` |
| Do cold outbound | `MONEY_METHODS/COLD_OUTBOUND/` + `LEDGER/OUTREACH_PIPELINE.csv` |
| Run daily research | `/daily-research` skill + `LEDGER/ALPHA_STAGING.csv` |
| Check revenue | `FINANCIALS/REVENUE_TRACKER.csv` + `FINANCIALS/FINANCIAL_DASHBOARD.md` |
| Find alpha | `LEDGER/ALPHA_STAGING.csv` (filter by category) |
| Stack methods | `LEDGER/CROSS_POLLINATION_MATRIX.csv` (synergy_score 90+) |
| Launch a product | `06_OPERATIONS/growth/GTM_OPTIMIZATION_CHECKLIST.md` + `LEDGER/GTM_OPTIMIZATION_PRIORITIES.csv` |
| Run overnight loops | `ralph/run_all_loops.sh` |
| Check human blockers | `01_STRATEGY/CAPITAL_GENESIS_HUMAN_TASKS.md` |
| Make first dollar | `06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md` + `06_OPERATIONS/gtm/GUMROAD_PRODUCT_SPECS.md` |
| Screen alpha | `python3 AUTOMATIONS/alpha_screening.py --pending` |
| Paper trade a method | `python3 AUTOMATIONS/paper_trade.py` + `LEDGER/PAPER_TRADES/` |
| Post content now | `OPS/CONTENT_POSTING_GUIDE.md` + `AUTOMATIONS/content_posting/` |
| Launch quant dashboard | `python3 AUTOMATIONS/quant_dashboard.py` |
| Sell services | `OPS/SERVICE_OFFERING_PACKAGES.md` |
| Sell local biz websites | `MONEY_METHODS/LOCAL_BIZ/` (6 templates + personalizer + cold email + lead scraper) |
| Find local biz leads | `python3 AUTOMATIONS/savvy_lead_scraper.py --city "Austin TX" --industry dental --count 50` |
| Scrape leads nationwide | `python3 AUTOMATIONS/nationwide_scraper.py --cities AUTOMATIONS/cities_top200.csv --industries "dentist,plumber,lawyer" --max-cities 10` |
| Send mass outreach | `python3 AUTOMATIONS/mass_outreach.py --leads output/leads.csv --min-score 60 --template-dir MONEY_METHODS/LOCAL_BIZ/templates/` |
| Pitch motion website upsell | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL.md` + `MOTION_UPSELL_PRICING.md` (42KB: 10 prompts, AI tools, competitive pricing, objection handling) |
| Setup AI call outreach | `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` (Bland.ai setup + 3 scripts + TCPA) |
| Build agency credibility site | `MONEY_METHODS/LOCAL_BIZ/AGENCY_WEBSITE.md` (full spec + wireframe) |
| Build Ramadan tracker | `ralph/loops/app_factory/output/ramadan-tracker/` (18 days to Ramadan 2026!) |
| Polish/rebrand apps | `MONEY_METHODS/APP_FACTORY/APP_NAMING_AUDIT.md` + `AGGREGATE_DESIGN_SYSTEM.md` |
| Generate app icons | `MONEY_METHODS/APP_FACTORY/APP_ASSET_GENERATION_PROMPTS.md` (ImageFX/Nano Banana prompts) |
| List on Gumroad | `OPS/GUMROAD_LAUNCH_CHECKLIST.md` (click-by-click, 13 products) |
| List on Fiverr | `OPS/FIVERR_LAUNCH_PACKAGE.md` + `OPS/FIVERR_LAUNCH_CHECKLIST.md` |
| List on Upwork | `OPS/UPWORK_LAUNCH_CHECKLIST.md` (5 profiles) |
| List on Etsy | `PRODUCTS/ETSY_LISTINGS_20.md` (20 listings ready) |
| Setup affiliates | `OPS/AFFILIATE_LAUNCH_CHECKLIST.md` (42 programs, tiered) |
| Setup cold email | `OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md` (domains + warmup + sequences) |
| Publish on Medium | `OPS/CONTENT_SYNDICATION_LAUNCH.md` + `CONTENT/medium_articles/` |
| Track all revenue | `LEDGER/REVENUE_STREAMS_TRACKER.csv` (100 streams pre-populated) |
| Run viral product arb | `MONEY_METHODS/ECOM/VIRAL_PRODUCT_ARB_PLAYBOOK.md` + `python3 AUTOMATIONS/viral_product_scanner.py --keywords "product"` |
| Scan ecom arb opportunities | `python3 AUTOMATIONS/ecom_arb_engine.py --scan --top 8 --category beauty` (real prices, auto cron every 2h) |
| Scan freelance demand | `python3 AUTOMATIONS/freelance_demand_scanner.py --scan` (9 subreddits, match to AI-deliverable services) |
| Run freelance pipeline daily | `python3 AUTOMATIONS/freelance_pipeline.py --daily` (scan + pipeline + portfolio + platforms) |
| See freelance portfolio | `python3 AUTOMATIONS/freelance_pipeline.py --portfolio` (16+ live URLs mapped to services) |
| Add freelance deal to pipeline | `python3 AUTOMATIONS/freelance_pipeline.py --add-deal` (interactive deal logging) |
| Execute OP17 freelance arb | `OPS/FREELANCE_ARB_EXECUTION.md` (complete playbook) + `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md` (all 10 platforms) |
| Detect trending products | `python3 AUTOMATIONS/trend_aggregator.py --scan` (Google Trends + Reddit + PH, trend→product matching) |
| Compare AI web design tools | `MONEY_METHODS/LOCAL_BIZ/AI_WEB_DESIGN_TOOLS.md` (Lovable vs Bolt vs v0 vs Cursor vs Framer) |
| Clone/rebrand an app for new region | `MONEY_METHODS/APP_FACTORY/APP_CLONE_REBRAND_STRATEGY.md` |
| Analyze a funnel | `OPS/TREND_INTEL/templates/FUNNEL_ANALYSIS_TEMPLATE.md` + `LEDGER/TREND_INTEL_TRACKER.csv` |
| Run RBI audit | `./printmaxx_cron.sh rbi daily` or `./printmaxx_cron.sh strategic full` |
| Test ops viability | `PRINTMAXX_STRATEGIC_RBI.xlsx` → VIABILITY MATRIX + `scripts/strategic_rbi_engine.py analyze` |
| Find edge/grey hat tactics | `LEDGER/RBI_STRATEGIC/GTM_EDGE_TACTICS.json` + `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` |
| Start findom ops | `MONEY_METHODS/AI_INFLUENCER/AI_NSFW_FINDOM_EXECUTION_PLAN.md` → create Fanvue account |
| Launch freelance arbitrage | `PRINTMAXX_FREELANCE_ARB.xlsx` → list top 10 on Fiverr + Upwork |
| Rebuild any xlsx | `scripts/builders/build_*.py` → `python3 scripts/recalc.py <output.xlsx>` |
| Run daily briefing | `./printmaxx_cron.sh briefing` → output in `LEDGER/DAILY_BRIEFINGS/` |
| Check bottlenecks | `PRINTMAXX_STRATEGIC_RBI.xlsx` → BOTTLENECKS sheet |
| Run A/B experiments | `PRINTMAXX_STRATEGIC_RBI.xlsx` → HYPOTHESES sheet (H001-H008) |
| Validate ops actually work | `./printmaxx_cron.sh self-test` or `scripts/strategic_rbi_engine.py self-test` |
| Get deep ops playbook | `PRINTMAXX_OPS_PLAYBOOK.xlsx` → step-by-step for 22 ops |
| Pick brand names | `PRINTMAXX_BRAND_NAMES.xlsx` → 207 names with availability |
| Compare infra options | `PRINTMAXX_INFRA_STACKS.xlsx` → side-by-side comparison |
| Deploy for free | `PRINTMAXX_ZERO_COST_DEPLOYMENT.xlsx` → free hosting/tools guide |
| List no-cost products | `python3 AUTOMATIONS/daily_nocost_rbi_scanner.py --ready-to-list` |
| Create social accounts | `ralph/loops/social_setup/output/T7_HUMAN_ACCOUNT_CREATION_MASTER.md` |
| Create 12 social accounts (NEW) | `OPS/ACCOUNT_SETUP_MATRIX.md` (full matrix, browser profiles, creation order) |
| Set up anti-detect + proxy + VPN | `OPS/PROXY_ANTIDETECT_VPN_WIRING_GUIDE.md` (Dolphin Anty + SOAX + automation) |
| Get first-week content for any account | `CONTENT/social/{handle}/FIRST_WEEK_CONTENT.md` (all 10 packages ready) |
| Set up Dolphin Anty browser profiles | `OPS/ANTIDETECT_BROWSER_PROFILES.md` (5 groups, 10 profiles) |
| Warm up new social accounts safely | `OPS/SAFE_WARMUP_AUTOMATION_GUIDE.md` (per-platform schedules, API vs browser risk, anti-detect comparison) |
| Buy pre-warmed accounts | `OPS/PREWARMED_ACCOUNT_BUYING_GUIDE.md` + `OPS/PROXY_ANTIDETECT_VPN_WIRING_GUIDE.md` (A/B test plan) |
| Launch curated beauty page (@velvetframes) | `CONTENT/social/beauty_curated/FIRST_WEEK_CONTENT.md` + `OPS/CURATED_BEAUTY_PAGE_PLAYBOOK.md` (legal compliance, sourcing, monetization) |
| Check handle availability | `OPS/HANDLE_AVAILABILITY_CHECK.md` + `OPS/ACCOUNT_SETUP_MATRIX.md` (handle status section) |
| Repurpose memes | `ralph/loops/social_setup/output/MEME_REPURPOSE_STRATEGY.md` |
| Launch ecom (no social) | `ralph/loops/social_setup/output/ECOM_LAUNCH_PLAN.md` |
| Clip for others (service) | `AUTOMATIONS/auto_clip_pipeline.py` + list on Fiverr |
| Run daily RBI scan | `python3 AUTOMATIONS/daily_nocost_rbi_scanner.py` |
| Make money with $0 | `OPS/ZERO_COST_REVENUE_ACCELERATION.md` + RBI scanner |
| Clip content for money | `MONEY_METHODS/CLIPPING_SERVICE/` |
| Find zero-cost ops | `python3 AUTOMATIONS/daily_nocost_rbi_scanner.py --opportunities` |
| Set up social profiles | `ralph/loops/social_setup/output/` (bios, photos, warmup) |
| List digital products | `DIGITAL_PRODUCTS/` + `DIGITAL_PRODUCTS/GUMROAD_LAUNCH_EXECUTION_GUIDE.md` |
| Sell micro products | `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md` |
| Sell PDF products | `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md` |
| Scan for CLAUDE.md gaps | `python3 scripts/update_claude_md_nav.py --scan` |
| Auto-update CLAUDE.md nav | `python3 scripts/update_claude_md_nav.py --update` |
| Log a user prompt | `python3 AUTOMATIONS/prompt_logger.py --log "prompt text"` |
| Audit incomplete prompts | `python3 AUTOMATIONS/prompt_logger.py --audit` |
| Search old prompts | `python3 AUTOMATIONS/prompt_logger.py --search "keyword"` |
| Export prompt audit log | `python3 AUTOMATIONS/prompt_logger.py --export` |
| Post Ramadan content | `CONTENT/social/ramadan/` + `builds/ramadan_tweets_30.csv` + `builds/ramadan_reels_scripts_10.md` |
| List on Redbubble | `PRODUCTS/REDBUBBLE_LISTINGS.md` |
| Sell on Mercari/eBay | `PRODUCTS/MERCARI_EBAY_ARB.md` |
| Build a high-quality app | `MONEY_METHODS/APP_FACTORY/APP_QUALITY_STANDARDS.md` + `IOS_REJECTION_PREVENTION.md` |
| Repurpose GitHub repos | `MONEY_METHODS/GITHUB_REPURPOSE_STRATEGY.md` + `LEDGER/GITHUB_REPURPOSE_TRACKER.csv` |
| Sell motion websites to local biz | `MONEY_METHODS/LOCAL_BIZ/MOTION_UPSELL.md` + `motion_templates/` |
| Squeeze content from build session | See "Max Squeeze Protocol" in CLAUDE.md + `.claude/rules/copy-style.md` |
| Learn agent best practices | `OPS/BEST_PRACTICES_AGENT_SKILLS_SHELL_COMPACTION.md` (OpenAI tips for skills, shell, compaction) |
| See all human blockers at once | `OPS/HUMAN_EXECUTION_DASHBOARD.md` (single-page priority-ordered view) |
| Find first-principles opportunities | `OPS/FIRST_PRINCIPLES_OPPORTUNITY_MATRIX.md` (scored 0-100, constraint-based) |
| Track alpha execution | `LEDGER/ALPHA_EXECUTION_TRACKER.csv` + `OPS/ALPHA_EXECUTION_REPORT.md` |
| Buy pre-warmed accounts | `OPS/PREWARMED_ACCOUNT_BUYING_GUIDE.md` (platforms, pricing, vetting) |
| Create Twitter/X accounts | `OPS/TWITTER_ACCOUNT_CREATION_SOP.md` + `OPS/TWITTER_ACCOUNT_QUICK_SHEETS/` |
| Set up free tier tools | `OPS/FREE_TIER_SETUP_GUIDE.md` (all free tiers in one place) |
| Master account creation flow | `OPS/ACCOUNT_CREATION_MASTER_PROCESS.md` + `AUTOMATIONS/account_creation_helper.py` |
| Find grey hat growth edges | `OPS/GREY_HAT_EDGE_GROWTH_MASTER.md` + `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` |
| Post Substack Notes | `CONTENT/substack_posts/SUBSTACK_NOTES_50.csv` (50 ready-to-post notes) |
| Launch paid community | `MONEY_METHODS/COMMUNITY/COMMUNITY_MONETIZATION_PLAYBOOK.md` (5 niches, platform comparison, pricing tiers, launch sequence) |
| Auto-orient as new agent | `python3 AUTOMATIONS/daily_agent_runner.py --status` (10-second orientation) |
| Check what's printing | `python3 AUTOMATIONS/venture_performance_tracker.py --recommend` (KILL/MAINTAIN/DOUBLE_DOWN) |
| Read the agent playbook | `OPS/AGENT_DAILY_PLAYBOOK.md` (THE guide for any new session) |
| Log a learning | `python3 AUTOMATIONS/daily_agent_runner.py --learning "text"` |
| Start NSFW/findom ops | `MONEY_METHODS/AI_INFLUENCER/AI_NSFW_EXECUTION_FULL.md` (compliance + monetization + subreddits) |
| List on Fiverr (10 gigs ready) | `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md` (copy-paste) |
| List on Upwork (5 profiles ready) | `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md` (copy-paste) |
| List on Etsy (complete listings) | `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md` (90KB) |
| Sell PRINTMAXX systems as products | `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md` (53KB) |
| Auto-list products via browser | `python3 AUTOMATIONS/auto_list_products.py` (Playwright) |
| Create accounts (step by step) | `OPS/ACCOUNT_CREATION_NOW.md` (definitive, priority order) |
| Find missing money methods | `OPS/MASTER_OPS_GAP_ANALYSIS.md` |
| Sell AI agent services | `MONEY_METHODS/AI_AGENT_SERVICES/AI_AGENT_SERVICES_PLAYBOOK.md` |
| Trade prediction markets | `MONEY_METHODS/PREDICTION_MARKETS/PREDICTION_MARKET_ARB_PLAYBOOK.md` |
| Sell prompts on marketplaces | `MONEY_METHODS/PROMPT_MARKETPLACE/PROMPT_MARKETPLACE_PLAYBOOK.md` |
| Build NoFap/discipline app | `MONEY_METHODS/APP_FACTORY/NOFAP_KARMAMAXX_APP_SPEC.md` |
| Send cold email sequences | `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv` |
| Run full cold outreach pipeline | `python3 AUTOMATIONS/website_signal_scorer.py -i AUTOMATIONS/leads/MASTER_LEADS.csv` → `python3 AUTOMATIONS/generate_cold_emails.py --industry dental` → `python3 AUTOMATIONS/email_sender.py --preview` |
| Score local biz websites | `python3 AUTOMATIONS/website_signal_scorer.py --url "https://example.com"` or `--input AUTOMATIONS/leads/HOT_LEADS.csv` |
| Generate cold emails with demos | `python3 AUTOMATIONS/generate_cold_emails.py --industry dental --min-score 40 --dry-run` |
| Send cold emails | `python3 AUTOMATIONS/email_sender.py --leads AUTOMATIONS/leads/HOT_LEADS.csv --preview` |
| See master launch dashboard | `OPS/MASTER_LAUNCH_DASHBOARD.md` (all 16 live sites, products, pipeline) |
| List 11 Fiverr gigs (NEW) | `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_01-10.md` (3-tier pricing, copy-paste) |
| Upload Gumroad PDFs | `DIGITAL_PRODUCTS/ready_to_sell/pdfs/` (5 PDFs ready) + `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` (13 listings) |
| Wrap apps for iOS | `scripts/wrap_and_submit_all.sh` (Capacitor 8.x, 6 apps ready, 4+ native plugins each) |
| Check system health | `python3 AUTOMATIONS/perpetual_improvement_runner.py --status` (5-loop orchestrator) |
| Discover new apps to build | `MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_ENGINE.md` (CloneChart + Appkittie + revenue intel + weekly cadence) |
| Submit app to iOS | `MONEY_METHODS/APP_FACTORY/IOS_SUBMISSION_PROCESS.md` (6-phase, real Apple guidelines, checklists) |
| Audit app quality (code-level) | `MONEY_METHODS/APP_FACTORY/APP_QUALITY_AUDIT_REAL.md` (portfolio benchmarks, deficiency list) |
| Research AI video tools | `10_RESEARCH/VIDEO_RESEARCH/comparisons/MASTER_VIDEO_TOOLS_2026.md` (canonical Mar 2026, supersedes Feb) |
| Edit AI videos (FFmpeg) | `python3 AUTOMATIONS/claude_video_editor.py --edit INPUT.mp4 --platform tiktok` |
| Post edited videos | `python3 AUTOMATIONS/auto_content_poster.py --post-video` (reads VIDEO_POSTING_QUEUE.csv) |
| Extract viral templates | `python3 AUTOMATIONS/viral_content_scanner.py --extract-templates` → VIRAL_FORMATS.md |
| Check video queue | `python3 AUTOMATIONS/claude_video_editor.py --queue` or `auto_content_poster.py --video-queue` |
| Rank all AI tools | `python3 AUTOMATIONS/perpetual_tool_researcher.py --rank` |
| Audit rigor of built assets | `OPS/RIGOR_AUDIT_FEB12.md` (scoring rubric for websites, emails, products, scrapers) |
| Find ANY app factory file | `MONEY_METHODS/APP_FACTORY/APP_FACTORY_CENTRAL_INDEX.md` (single source for all app docs) |
| Find ANY product listing | `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md` (all platforms, duplicates flagged, priority order) |
| Find ANY lead/outreach file | `OPS/LEADS_OUTREACH_CENTRAL_INDEX.md` (leads, emails, scrapers, pipeline) |
| Buy warmed social accounts | `OPS/PREWARMED_ACCOUNT_BUYING_GUIDE.md` (Fameswap, Swapd, AccsMarket) |
| Set up anti-detect browser | `OPS/BROWSER_AUTOMATION_SETUP.md` (AdsPower free, GoLogin, proxy config) |
| Find ANY content file | `CONTENT/CONTENT_CENTRAL_INDEX.md` (3,300+ pieces, platform-sorted, posting instructions) |
| Audit/clean up project files | `OPS/MASTER_FILE_AUDIT.md` (893 lines, orphans, duplicates, P0-P3 cleanup priorities) |
| Buy Fameswap account + proxy setup | `OPS/SOCIAL_ACCOUNT_ACQUISITION_GUIDE.md` (full acquisition → proxy → warmup pipeline) |
| Expand niche account portfolio | `OPS/NICHE_ACCOUNT_EXPANSION_STRATEGY.md` (6 new accounts proposed, prioritization matrix, content routing, rising niche detector) |
| Route alpha to niche accounts | `OPS/NICHE_ACCOUNT_EXPANSION_STRATEGY.md` section 5 (auto-categorize scraped alpha to correct account queue) |
| Detect rising niches for new accounts | `OPS/NICHE_ACCOUNT_EXPANSION_STRATEGY.md` section 7 (Google Trends + X engagement + monetization scoring) |
| Repurpose content legally | `OPS/NICHE_ACCOUNT_EXPANSION_STRATEGY.md` section 4 (6 safe methods, X enforcement patterns, legal analysis) |
| Run live monitoring dashboard | `python3 AUTOMATIONS/live_dashboard_server.py` (localhost:8888, 14 panels, real data) |
| Scan content for compliance | `python3 AUTOMATIONS/compliance_scanner.py --audit-all --save` (FTC/CAN-SPAM/income/PII) |
| Scan single file for compliance | `python3 AUTOMATIONS/compliance_scanner.py --scan-file path/to/file.md` |
| View compliance report | `OPS/COMPLIANCE_SCAN_2026_02_13.md` (285 CRITICAL, 1,796 WARNING) |
| Respond to freelance Reddit posts | `AUTOMATIONS/freelance_response_templates/` (10 copy-paste replies) |
| Track freelance pipeline | `LEDGER/FREELANCE_PIPELINE_ACTIVE.csv` (10 active, $3K + $9.4K/mo) |
| See hot leads for cold email | `AUTOMATIONS/leads/HOT_LEADS.csv` (21 filtered, real emails) |
| Get hot batch cold emails | `AUTOMATIONS/outreach/HOT_BATCH_FEB13.csv` (359 emails, 3-step sequence) |
| Check local biz pipeline status | `OPS/LOCAL_BIZ_EXECUTION_STATUS.md` (87 READY, blocker: email infra) |
| Look up signal accounts | `OPS/SIGNAL_ACCOUNT_DIRECTORY.md` (116+ accounts by specialty) |
| Check system heartbeat | `cat OPS/HEARTBEAT.md` (<20 lines, 3-second pulse check) |
| Recover from crash | `cat OPS/active-tasks.md` (what was running, where it stopped) |
| Run closed-loop pipeline | `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000 --workers 30` |
| Update all memory layers | `python3 AUTOMATIONS/memory_manager.py --full` (heartbeat + active tasks + daily log + health) |
| Log something to daily log | `python3 AUTOMATIONS/memory_manager.py --log "message"` |
| Check venture health | `python3 AUTOMATIONS/memory_manager.py --health` |
| Qualify 2.87M leads | `python3 AUTOMATIONS/intelligent_lead_qualifier.py --analyze --batch 5000 --workers 30` |
| Run full lead→email loop | `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 10 --batch 2000 --workers 30` (unattended) |
| Generate personalized demos | `python3 AUTOMATIONS/personalize_demos.py --top 100` (or `--all`, `--category dentist`, `--deploy`) |
| Refresh pipeline dashboard | `python3 AUTOMATIONS/refresh_dashboard.py` (generates Bloomberg-style HTML + opens in browser) |
| Run SEO competitor analysis | `python3 AUTOMATIONS/seo_competitor_analyzer.py --top 50 --summary` (or `--industry dental --city Austin`) |
| Use unified CLI | `python3 AUTOMATIONS/printmaxx.py status` (or `leads`, `emails`, `dashboard`, `deploy`, `content`, `memory`) |
| View pipeline dashboard | `open https://printmaxx-dashboard.surge.sh` (live Bloomberg-style dashboard) |
| View personalized demos | `open https://printmaxx-demos.surge.sh` (100 personalized landing pages) |
| View site score analyzer | `open https://sitescore-analyzer.surge.sh` (web frontend for website scoring) |
| View portfolio/agency site | `open https://printmaxx-portfolio.surge.sh` (credibility site for cold outreach) |
| View website analyzer tool | `open https://printmaxx-analyzer.surge.sh` (lead-gen: enter URL, get score) |
| Track cold email campaigns | `python3 AUTOMATIONS/response_tracker.py dashboard` (funnel metrics: open/reply/book/close rates) |
| Log email response | `python3 AUTOMATIONS/response_tracker.py log --id L00001 --status REPLIED` |
| Enrich hot leads | `python3 AUTOMATIONS/lead_enrichment.py --enrich --top 50` (Google rating, social, tech stack) |
| A/B test cold emails | `python3 AUTOMATIONS/cold_email_ab_test.py --split --limit 100` then `--generate` |
| Run overnight automation | `python3 AUTOMATIONS/overnight_orchestrator.py --run` (3-phase: analyze→emails→dashboard) |
| Check email domain health | `python3 AUTOMATIONS/email_domain_health.py --check yourdomain.com` (SPF/DKIM/DMARC/MX/blacklist) |
| Onboard a new client | `python3 AUTOMATIONS/client_onboarding.py --search "business" --tier professional` |
| Get follow-up reminders | `python3 AUTOMATIONS/response_tracker.py followups` (overdue follow-ups) |
| Auto-list trending products | `python3 AUTOMATIONS/trend_to_listing.py --scan` (trend→listings, `--hourly` for cron, `--check-winners`) |
| Check system health | `python3 AUTOMATIONS/system_health_monitor.py --check` (14-point health, `--quick` for one-line) |
| Pre-check app for App Store | `python3 AUTOMATIONS/greenlight_checker.py --all` (or `--app ramadan-tracker`, Apple compliance scan) |
| Run daily research pipeline | `python3 AUTOMATIONS/daily_research_pipeline.py --extract-only` (or `--full`, `--scrape-only`, `--repurpose`, `--status`) |
| Source products from factories | `python3 AUTOMATIONS/import_sourcing_scanner.py --product "product name"` (or `--daily`, `--status`, `--report`) |
| View today's alpha digest | `cat OPS/DAILY_RESEARCH_DIGEST_$(date +%Y_%m_%d).md` |
| View auto-generated content | `ls CONTENT/social/auto_generated/` (daily repurposed tweets from alpha pipeline) |
| Run unified alpha monitor | `python3 AUTOMATIONS/unified_alpha_monitor.py --full` (Reddit niche + GitHub MIT + ASO + competitors + freshness, cron 5:45 AM) |
| Check unified alpha status | `python3 AUTOMATIONS/unified_alpha_monitor.py --status` (monitoring scope, related scripts) |
| View unified alpha digest | `cat OPS/UNIFIED_ALPHA_DIGEST_$(date +%Y_%m_%d).md` (daily consolidated findings) |
| Check compliance deadlines | `python3 AUTOMATIONS/compliance_deadline_tracker.py --check` (21 regulations, days remaining, urgency alerts) |
| View upcoming compliance deadlines | `python3 AUTOMATIONS/compliance_deadline_tracker.py --upcoming 30` (next 30 days) |
| Scan for new regulations | `python3 AUTOMATIONS/compliance_deadline_tracker.py --scan` (RSS feeds: FTC, NetInfluencer, National Law Review) |
| View compliance digest | `cat OPS/COMPLIANCE_DEADLINE_DIGEST_$(date +%Y_%m_%d).md` (markdown regulatory overview) |
| Monitor Telegram channels | `python3 AUTOMATIONS/telegram_community_monitor.py --scan` (26 channels, 8 niches, signal scoring) |
| Scan specific Telegram niche | `python3 AUTOMATIONS/telegram_community_monitor.py --niche ai_tools` (single niche scan) |
| View Telegram signal digest | `python3 AUTOMATIONS/telegram_community_monitor.py --digest` (generate signal digest) |
| Mine Reddit pain points | `python3 AUTOMATIONS/reddit_pain_point_miner.py --scan` (25 subreddits, buying intent extraction) |
| Generate content from trends | `python3 AUTOMATIONS/content_trend_pipeline.py --scan --generate` (trend→content for 5 accounts) |
| Check content trend status | `python3 AUTOMATIONS/content_trend_pipeline.py --status` (pipeline health + stats) |
| Scan app clone opportunities | `python3 AUTOMATIONS/app_clone_pipeline.py --scan` (61 opps: language/demo/niche variants) |
| View app clone matrix | `python3 AUTOMATIONS/app_clone_pipeline.py --matrix` (full opportunity matrix sorted by score) |
| Generate rebrand package | `python3 AUTOMATIONS/app_clone_pipeline.py --generate APPNAME` (asset prompts + checklist) |
| Generate app asset prompts | `python3 AUTOMATIONS/app_clone_pipeline.py --assets APPNAME` (Nano Banana/ImageFX prompts) |
| Auto-draft tweets from scraped content | `python3 AUTOMATIONS/tweet_auto_drafter.py` (drafts from high-signal accounts) |
| Find quote tweet opportunities | `python3 AUTOMATIONS/quote_tweet_scanner.py` (scan monitored accounts for QT opps) |
| View Claude scheduled tasks guide | `OPS/SCHEDULED_TASKS_FRAMEWORK.md` (cron, LaunchD, overnight loops, all automation scheduling) |
| Browse 39 specialized agents | `.claude/agents/` (8 categories: eng, prod, mkt, design, pm, studio, test, research) |
| Find UGCDrop pricing/details | `MONEY_METHODS/UGCDROP/` (UGC clips from $0.01, affiliate opp) |
| Search operational memory | `python3 AUTOMATIONS/semantic_memory_search.py "query"` (or `--category learnings --recent 7 "query"`, `--live`, `--stats`, `--index`) |
| Search memory via web dashboard | `python3 AUTOMATIONS/ops_web_dashboard.py` then use search bar (or `GET /api/search?q=query&category=X`) |
| Run autonomous orchestrator | `python3 AUTOMATIONS/autonomous_orchestrator.py --status` (system state) or `--prep morning\|midday\|evening` (generate prompt) or `--auto morning` (full headless session) |
| Score all methods (rebalancer) | `python3 AUTOMATIONS/auto_rebalancer.py --check` (score + report) or `--rebalance` (auto-adjust + checkpoints) or `--history` (trend) |
| Manage human checkpoints | `python3 AUTOMATIONS/checkpoint_manager.py --status` (pending items) or `--approve FILE` or `--reject FILE` or `--summary` |
| Scan SaaS potential | `python3 AUTOMATIONS/saas_product_scanner.py --scan` (rank all) or `--top 5` (details) or `--manifest` (generate full manifest) |
| View SaaS manifest | `OPS/SAAS_PRODUCT_MANIFEST.md` (12 products ranked with pricing, competitors, moats, anti-abuse architecture) |
| Open PRINTMAXX desktop app | `python3 AUTOMATIONS/printmaxx_desktop.py` (5-tab command center, hourly reminders, macOS notifications, alarms, motivation, launch tracker) |
| Run desktop reminders only (no GUI) | `python3 AUTOMATIONS/printmaxx_desktop.py --minimized` (hourly task notifications + motivational quotes every 30 min) |
| Check product launch status | `python3 AUTOMATIONS/product_launch_automator.py --status` (progress bars per product, priority breakdown) |
| Launch product on directories | `python3 AUTOMATIONS/product_launch_automator.py --launch --product focuslock-web` (generates copy + opens tabs) |
| Generate submission copy | `python3 AUTOMATIONS/product_launch_automator.py --generate-copy --product focuslock-web` (saves to OPS/LAUNCH_COPY_{PRODUCT}.md) |
| Get submission checklist | `python3 AUTOMATIONS/product_launch_automator.py --checklist --product focuslock-web` (step-by-step per directory) |
| Mark directories submitted | `python3 AUTOMATIONS/product_launch_automator.py --mark-submitted --product focuslock-web --directories ProductHunt,HackerNews` |
| Set a quick alarm | Desktop app → Alarms tab → Quick alarms (15min/30min/1hr/2hr) or custom HH:MM |

### Cross-reference checklist (before building ANY method)

| Working on... | Must check... |
|---------------|---------------|
| New app | `LEDGER/APP_FACTORY_METHODS.csv` + `CROSS_POLLINATION_MATRIX.csv` + `GTM_OPTIMIZATION_PRIORITIES.csv` |
| Content campaign | `LEDGER/MARKETING_CHANNELS_MASTER.csv` + `WINNING_CONTENT_STRUCTURES.csv` + `EDGE_GROWTH_TACTICS.md` |
| Cold outbound | `LEDGER/MARKETING_CHANNELS_MASTER.csv` + `ALPHA_STAGING.csv` (outbound category) |
| New niche | `LEDGER/CROSS_POLLINATION_MATRIX.csv` + all related method CSVs |
| Monetization | `LEDGER/APP_FACTORY_METHODS.csv` + `ALPHA_STAGING.csv` (monetization) |
| Any app build | `APP_QUALITY_STANDARDS.md` + `IOS_REJECTION_PREVENTION.md` + `APP_RESTRUCTURE_PLAN.md` |
| Using GitHub repos | `GITHUB_REPURPOSE_STRATEGY.md` security protocol + `GITHUB_REPURPOSE_TRACKER.csv` |
| Building clone/rebrand app | `APP_CLONE_REBRAND_STRATEGY.md` + `APP_QUALITY_STANDARDS.md` + `IOS_REJECTION_PREVENTION.md` |

---

