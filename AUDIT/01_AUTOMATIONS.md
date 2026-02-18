# AUTOMATIONS AUDIT

**Date:** 2026-02-14
**Auditor:** Claude Opus 4.6 (automated code review)
**Scope:** AUTOMATIONS/, scripts/, 05_AUTOMATION/, deployment scripts, Makefile, cron

## Summary Stats
- Total Python scripts (AUTOMATIONS/): 128 files (incl. portfolio/ subpackage)
- Total Python scripts (scripts/): 24 files (incl. builders/)
- Total scripts (05_AUTOMATION/scripts/): ~97 files (older copy, mostly overlapping with AUTOMATIONS/)
- Deployment scripts (root): 4 (deploy_all_apps.sh, deploy_apps.py, deploy_surge_quick.sh, Makefile)
- Cron orchestrator: 1 (printmaxx_cron.sh, 741 lines)
- **Working end-to-end (stdlib only, no credentials needed): ~35**
- **Working with installed deps (requests/bs4/playwright): ~25**
- **Needs credentials to function: ~20**
- **Broken/incomplete/placeholder: ~15**
- **Duplicates/deprecated: ~15**
- **Total meaningful, potentially functional scripts: ~80**

## Cron Status

**printmaxx_cron.sh** is a well-built 741-line bash orchestrator. It has 12 commands (morning, briefing, content, outreach, digest, backup, overnight, weekly, monthly, rbi, strategic, self-test, status). It tracks yield metrics to LEDGER/AUTOMATION_RESULTS.csv and does CSV snapshots before mutations.

**Problem:** The cron is NOT actually installed. Git is not initialized (confirmed: `Is directory a git repo: No`). The `nightly_backup` function tries git operations that fail. The `overnight_sprint` calls `ralph/run_overnight_sprint.sh` which may not exist.

**What actually runs if cron were installed:**
| Schedule | Command | Would it work? |
|----------|---------|---------------|
| 5 AM | briefing | YES - reads CSVs, generates markdown |
| 6 AM | morning | PARTIAL - extract/organize scripts exist but depend on LEDGER CSVs existing |
| 6:30 AM | content | PARTIAL - generate_30day_calendar.py and generate_buffer_csvs.py exist |
| 9 AM | outreach | PARTIAL - content_to_qa_router.py exists |
| 6 PM | digest | YES - pure reporting from AUTOMATION_RESULTS.csv |
| 9 PM | backup | BROKEN - no git repo initialized |
| 10 PM | overnight | BROKEN - ralph/run_overnight_sprint.sh likely missing |
| Monday | weekly | PARTIAL - depends on multiple scripts, some may error |
| 1st | monthly | PARTIAL - same as weekly |

**Verdict:** Cron orchestrator is well-designed but untested. Maybe 60% of scheduled tasks would succeed if installed. The backup system is dead (no git).

## Script-by-Script Assessment

### Tier 1: Core Infrastructure (WORKS with stdlib)

| File | Purpose | Status | Deps | Notes |
|------|---------|--------|------|-------|
| daily_agent_runner.py | Auto-orient new agent, show priorities | WORKS | stdlib | Reads CSVs, generates priorities |
| venture_performance_tracker.py | Score methods 0-100, KILL/MAINTAIN/DOUBLE | WORKS | stdlib | Pure CSV analysis |
| memory_manager.py | 3-layer memory (heartbeat, tasks, logs) | WORKS | stdlib | OpenClaw pattern, solid design |
| alpha_screening.py | Multi-factor alpha scoring | WORKS | stdlib | Quant-grade scoring system |
| method_performance_analyzer.py | Weekly method performance reports | WORKS | stdlib | Pure CSV analysis |
| revenue_projector.py | Monte Carlo revenue simulation | WORKS | stdlib (numpy optional) | Has numpy fallback |
| paper_trade.py | Paper trade methods with $0-100 | WORKS | stdlib | File-based state |
| ops_dashboard.py | Track 53 ops patterns | WORKS | stdlib (rich optional) | TUI dashboard |
| prompt_logger.py | Log/search/audit user prompts | WORKS | stdlib | Append-only JSONL |
| guardrails.py | File-system safety module | WORKS | stdlib | Path validation, checkpoints |
| backup_system.py | Full/incremental backups | WORKS | stdlib | Writes to ~/PRINTMAXX_BACKUPS/ |
| compliance_scanner.py | FTC/CAN-SPAM content audit | WORKS | stdlib | Regex-based, 285 criticals found |
| daily_todo_generator.py | Auto-prioritized daily TODO | WORKS | stdlib | Generates OPS/DAILY_TODO_*.md |
| signal_aggregator.py | Aggregate signals from multiple sources | WORKS | stdlib | CSV aggregation |
| response_tracker.py | Campaign funnel tracking | WORKS | stdlib | QUEUED->SENT->OPENED->REPLIED |
| generate_cold_emails.py | Cold email generator from leads | WORKS | stdlib | 610 lines, matches demos to leads |
| printmaxx.py | Unified CLI wrapping 28+ scripts | WORKS | stdlib | 480 lines, 12 subcommands |
| overnight_orchestrator.py | 3-phase dependency-aware pipeline | WORKS | stdlib | Lock file, retry, timeouts |
| personalize_demos.py | Generate personalized landing pages | WORKS | stdlib | Maps categories to templates |
| refresh_dashboard.py | Bloomberg-style HTML dashboard | WORKS | stdlib | Chart.js output |
| daily_nocost_rbi_scanner.py | 17-category zero-cost scanner | WORKS | stdlib | Revenue projections |
| alpha_csv_parser.py | Parse alpha CSV entries | WORKS | stdlib | Utility |
| alpha_to_ops.py | Route alpha to operations | WORKS | stdlib | Pipeline routing |
| alpha_validator.py | Validate alpha entries | WORKS | stdlib | Data validation |
| greenlight_checker.py | Apple App Store compliance wrapper | WORKS | stdlib | Wraps RevylAI |
| agent_monitor.py | Live agent progress tracking | NEEDS rich | pip install rich | TUI |
| quant_dashboard.py | Simplified 6-panel TUI | NEEDS textual/rich | pip install | Bloomberg-style |
| printmaxx_quant_terminal.py | Full 7-panel institutional TUI | NEEDS textual/rich | pip install | 44KB, v4.0 |
| printmaxx_tui.py | TUI interface | NEEDS textual/rich | pip install | Alternate TUI |
| printmaxx_brain.py | AI-driven decision engine | WORKS | stdlib | Decision routing |

### Tier 2: Scrapers/Web (WORKS with requests/bs4/playwright)

| File | Purpose | Status | Deps | Notes |
|------|---------|--------|------|-------|
| background_reddit_scraper.py | Reddit JSON API scraper | WORKS | requests | No auth needed, best scraper |
| reddit_deep_scraper.py | Deep Reddit thread scraper | WORKS | requests | JSON API |
| reddit_alpha_scraper.py | Reddit alpha extraction | WORKS | requests | Targets solopreneur subs |
| ecom_arb_engine.py | Amazon/eBay price scraping + arb | WORKS | requests, pytrends(opt) | Has fallback if no pytrends |
| freelance_demand_scanner.py | Reddit hiring post scanner | WORKS | requests | Scans 9 subreddits |
| trend_aggregator.py | Google Trends + Reddit + PH | WORKS | requests, pytrends(opt) | Multi-source |
| website_signal_scorer.py | Score websites 0-100 | WORKS | requests, bs4 | 15 signals, 637 lines |
| intelligent_lead_qualifier.py | Bulk lead qualification | WORKS | requests, bs4 | 1,052 lines, 2.87M leads |
| savvy_lead_scraper.py | Local biz lead scraper | WORKS | requests, bs4 | Quant-level scoring |
| nationwide_scraper.py | 203-city lead scraper | WORKS | requests, bs4 | 880 lines |
| local_biz_pipeline.py | Scrape -> analyze -> generate | WORKS | requests, bs4 | End-to-end |
| local_biz_website_scraper.py | Business website analysis | WORKS | requests, bs4 | |
| producthunt_scraper.py | Product Hunt scraper | WORKS | requests, bs4 | Public API |
| viral_product_scanner.py | FB Ads Library scanner | WORKS | requests, bs4 | |
| app_clone_finder.py | App clone research | PARTIAL | requests, bs4 | Needs BRAVE_SEARCH_API_KEY for best results |
| aso_keyword_research.py | App Store keyword research | WORKS | requests, bs4 | |
| trending_products_scanner.py | Trending product scanner | WORKS | requests, bs4 | |
| twitter_alpha_scraper.py | Twitter via Brave cookies | NEEDS playwright + Brave | Requires Brave login | Core scraper |
| twitter_content_scraper.py | Twitter content extraction | NEEDS playwright + Brave | Requires Brave login | |
| viral_content_scanner.py | Viral content detection | NEEDS playwright + Brave | Requires Brave login | |
| headless_twitter_scraper.py | Headless Twitter scraping | NEEDS playwright | No cookie extraction | |
| headless_reddit_scraper.py | Headless Reddit scraping | NEEDS playwright | Overkill, use JSON API instead |
| scrape_twitter_selenium.py | Selenium Twitter scraper | NEEDS selenium + chromedriver | Deprecated approach |
| import_sourcing_scanner.py | ImportYeti US customs data | NEEDS playwright, requests | Factory sourcing intel |
| auto_list_products.py | Playwright automated listing | NEEDS playwright | Browser automation for platforms |
| auto_account_creator.py | Platform signup automation | NEEDS playwright | CAPTCHA detection |

### Tier 3: Needs Credentials/APIs

| File | Purpose | Status | Credentials Needed |
|------|---------|--------|--------------------|
| email_sender.py | Send cold emails | NEEDS CREDS | GMAIL_APP_PASSWORD or RESEND_API_KEY |
| auto_content_poster.py | Post to X/Twitter API | NEEDS CREDS | Twitter OAuth (CREDENTIALS.env) |
| auto_freelance_responder.py | Auto-respond on Reddit | NEEDS CREDS | REDDIT_CLIENT_ID/SECRET |
| sam_gov_monitor.py | SAM.gov contract monitor | PARTIAL | SAM_GOV_API_KEY (free, optional) |
| gov_tenders_scraper.py | Government tenders | PARTIAL | SAM_GOV_API_KEY (free, optional) |
| hexomatic_lead_gen.py | Yelp-based lead gen | NEEDS CREDS | YELP_API_KEY |
| auto_clip_pipeline.py | Video clipping pipeline | NEEDS CREDS | ANTHROPIC_API_KEY |
| live_dashboard_server.py | Flask dashboard on :8888 | NEEDS flask | pip install flask |
| email_domain_health.py | SPF/DKIM/DMARC checker | WORKS | stdlib (dns queries) |
| cold_email_ab_test.py | A/B test cold emails | WORKS | stdlib, needs email_sender for actual sends |
| lead_enrichment.py | Enrich leads with Google data | WORKS | requests |
| client_onboarding.py | Auto-generate client docs | WORKS | stdlib |

### Tier 4: Duplicate/Deprecated/Overlapping

| File | Purpose | Status | Notes |
|------|---------|--------|-------|
| backtest_alpha_DEPRECATED.py | Old backtester | DEPRECATED | Name says it all |
| daily_reddit_scraper.py | Playwright Reddit | SUPERSEDED | Use background_reddit_scraper.py instead |
| daily_twitter_scraper.py | Playwright Twitter | SUPERSEDED | Use twitter_alpha_scraper.py instead |
| enhanced_reddit_scraper.py | Another Reddit scraper | DUPLICATE | 6+ Reddit scrapers exist |
| enhanced_twitter_scraper.py | Another Twitter scraper | DUPLICATE | 7+ Twitter scrapers exist |
| parallel_twitter_scraper.py | Parallel Twitter | DUPLICATE | Yet another Twitter scraper |
| parallel_background_scraper.py | Parallel combined | DUPLICATE | |
| background_twitter_scraper.py | Background Twitter | DUPLICATE | |
| scrape_parallel_fixed.py | Fixed parallel scraper | DUPLICATE | |
| scrape_twitter_applescript.py | AppleScript Twitter | DEPRECATED | Mac-specific hack |
| scrape_via_websearch.py | WebSearch-based scraper | LIMITED | Not real browser scraping |
| ecom_arb_scanner.py | Simpler arb scanner | SUPERSEDED | Use ecom_arb_engine.py |
| scrape_caiden_cdp.py | CDP-based scraper | NICHE | Specific to Caiden platform |
| scrape_caiden_playwright.py | Playwright Caiden | NICHE | Specific to Caiden |
| twitter_scraper_live.py | Live Twitter scraper | DUPLICATE | |

### Tier 5: Pipeline/Orchestration Scripts

| File | Purpose | Status | Notes |
|------|---------|--------|-------|
| closed_loop_pipeline.py | Lead qualify -> email -> track | WORKS | Crash-recoverable, cron-ready |
| perpetual_improvement_runner.py | 5-loop orchestrator | WORKS | 530 lines |
| daily_research_pipeline.py | Scrape->extract->filter->repurpose | WORKS | Master orchestrator |
| run_all_research_ops.py | Run all research operations | WORKS | Batch runner |
| daily_ops_from_alpha.py | Convert alpha to daily ops | WORKS | Pipeline routing |
| ops_orchestrator.py | Orchestrate operations | WORKS | |
| ralph_loop_factory.py | Generate ralph loop configs | WORKS | |

### Tier 6: Content/Revenue/Misc

| File | Purpose | Status | Notes |
|------|---------|--------|-------|
| content_multiplier.py | One piece -> 20+ variants | WORKS | Template-based |
| engagement_bait_converter.py | Convert alpha to engagement posts | WORKS | |
| self_reply_funnel.py | Self-reply Twitter funnel | WORKS | Content generation |
| geo_content_optimizer.py | GEO-optimized content | WORKS | |
| bulk_landing_page_generator.py | Bulk landing pages | WORKS | HTML generation |
| arb_listing_generator.py | Generate marketplace listings | WORKS | |
| trend_to_listing.py | Trend -> product listing | WORKS | 775 lines |
| revenue_math_calculator.py | Revenue calculations | WORKS | |
| mass_outreach.py | Mass email outreach system | WORKS | 732 lines |
| system_health_monitor.py | 14-point health check | WORKS | 820 lines |
| micro_info_product_builder.py | Build info products | WORKS | Template-based |
| download_bulk_leads.py | Download lead files | WORKS | |
| portfolio_rebalancer.py | Rebalance method portfolio | WORKS | |

### scripts/ Directory (Utility Scripts)

| File | Purpose | Status | Notes |
|------|---------|--------|-------|
| strategic_rbi_engine.py | 5-layer Jane Street RBI | WORKS | 45K+ lines |
| rbi_audit.py | Ops health audit | WORKS | |
| daily_briefing.py | 10-system daily scan | WORKS | |
| validate.py | CSV/markdown/copy validation | WORKS | |
| self_test.py | Ops validation 0-100 scoring | WORKS | |
| experiment_runner.py | A/B test lifecycle | WORKS | Chi-square + t-test |
| account_tracker.py | Account lifecycle tracking | WORKS | |
| revenue_intake.py | Revenue logging CLI | WORKS | |
| programmatic_seo.py | Generate 600 SEO pages | WORKS | |
| content_queue.py | Content pipeline management | WORKS | |
| generate_30day_calendar.py | 30-day content calendar | WORKS | 66K file |
| generate_buffer_csvs.py | Buffer import CSVs | WORKS | |
| extract_source_csvs_from_mega_sheet.py | Extract from mega sheet | WORKS | |
| update_claude_md_nav.py | Scan for CLAUDE.md gaps | WORKS | |
| builders/ (11 scripts) | Rebuild XLSX files | WORKS | build_master_ops_v2.py etc. |

### 05_AUTOMATION/ Directory

Contains ~97 scripts in 05_AUTOMATION/scripts/ plus ralph task definitions and documentation. These appear to be an OLDER copy of the same scripts now in AUTOMATIONS/. The ralph/ subdirectory has 55+ task definitions and shell runners. The ralph_tasks/ directory has 21 task definition files.

**Verdict:** 05_AUTOMATION/scripts/ is largely a stale mirror. AUTOMATIONS/ is the active directory.

## External Dependencies

### Python Packages Required
| Package | Used By | Install | Status |
|---------|---------|---------|--------|
| requests | ~20 scrapers | pip install requests | Likely installed |
| beautifulsoup4 | ~15 scrapers | pip install beautifulsoup4 | Likely installed |
| playwright | ~12 scrapers | pip install playwright && playwright install | Needs browser install |
| pycryptodome | Twitter scrapers (4) | pip install pycryptodome | For Brave cookie decryption |
| pytrends | ecom_arb_engine, trend_aggregator | pip install pytrends | Optional, has fallback |
| flask | live_dashboard_server | pip install flask | For local dashboard |
| rich | agent_monitor, quant dashboards | pip install rich | TUI rendering |
| textual | quant_dashboard, TUIs | pip install textual | Bloomberg TUI |
| numpy | revenue_projector | pip install numpy | Has pure-Python fallback |
| requests_oauthlib | auto_content_poster | pip install requests-oauthlib | For Twitter OAuth |
| anthropic | auto_clip_pipeline | pip install anthropic | AI clipping |

### External Services/APIs
| Service | Script(s) | Auth Type | Cost |
|---------|-----------|-----------|------|
| Reddit JSON API | background_reddit_scraper | None needed | Free |
| Twitter/X | twitter_alpha_scraper + 6 others | Brave browser cookies | Free (needs login) |
| Gmail SMTP | email_sender | App password | Free |
| Resend API | email_sender | API key | Free tier exists |
| SAM.gov API | sam_gov_monitor, gov_tenders_scraper | API key | Free |
| Yelp API | hexomatic_lead_gen | API key | Free 500/day |
| Brave Search API | app_clone_finder | API key | Free tier |
| Anthropic API | auto_clip_pipeline | API key | Paid |
| Surge.sh | deploy scripts | Email login | Free |
| Vercel | deploy scripts | Token or login | Free tier |
| Netlify | deploy scripts | Token or login | Free tier |

### Credentials/Accounts Needed (Not Yet Created)
1. **Gmail App Password** - for cold email sending
2. **Twitter/X OAuth** - for auto_content_poster (API posting)
3. **Reddit OAuth** - for auto_freelance_responder
4. **Stripe** - for Gumroad/payment processing
5. **Gumroad account** - for digital product sales
6. **Fiverr account** - for freelance listings
7. **Upwork account** - for freelance proposals
8. **Surge.sh login** - for deployment (partially created)
9. **Vercel token** - for app deployment
10. **Anthropic API key** - for AI clipping pipeline

## Deployment Status

### What is Actually Live
- 20+ sites on surge.sh (printmaxx-seo, ramadan-tracker, focuslock-app, etc.)
- These were manually deployed via `npx surge` commands
- No automated deployment pipeline is actively running

### What Would Deploy (Scripts Exist)
- deploy_all_apps.sh: 6 PWA apps -> Vercel/Surge
- deploy_apps.py: Same with Python, multi-method fallback
- deploy_surge_quick.sh: Quick Surge.sh deploy for 6 apps

### Deployment Blockers
- No git repo initialized (backup/push fails)
- Vercel token not configured for automated deploys
- deploy_all_apps.sh has hardcoded path to app_factory/output (correct for this machine)

## Critical Gaps

1. **Scraper Duplication Epidemic:** There are 7+ Twitter scrapers and 6+ Reddit scrapers. Only 1 of each actually works well (twitter_alpha_scraper.py via Brave cookies, background_reddit_scraper.py via JSON API). The rest are failed experiments never cleaned up.

2. **Zero Revenue Pipeline is Active:** 128 scripts exist, 20+ sites are deployed, but $0 revenue. The blocker is account creation (Stripe, Gumroad, Fiverr, Upwork) -- none of these are automated. auto_account_creator.py exists but needs Playwright + CAPTCHA solving.

3. **Cron Not Installed / Git Not Initialized:** The 741-line cron orchestrator (printmaxx_cron.sh) is sophisticated but has never been installed in crontab. The nightly backup function is broken because there is no git repo. Run `git init && git add -A && git commit -m "initial"` to fix.

4. **Credential Gap:** At least 10 API keys/accounts are needed that do not exist. The email_sender.py, auto_content_poster.py, and auto_freelance_responder.py are all well-built but dead without credentials.

5. **05_AUTOMATION/ is a Stale Mirror:** ~97 scripts in 05_AUTOMATION/scripts/ duplicate what is in AUTOMATIONS/. This wastes disk and causes confusion about which version is authoritative. The AUTOMATIONS/ directory is the active one.

## Strengths

1. **Defensive Coding:** guardrails.py enforces project-root path restrictions on all file operations. Most scripts use `Path(__file__).resolve().parent.parent` for project root instead of hardcoded paths. Error handling with try/except and graceful fallbacks is widespread.

2. **Stdlib-First Design:** ~35 scripts work with zero external dependencies (pure Python stdlib). The revenue_projector.py even has a numpy fallback class. This means the core analysis/reporting pipeline runs without pip installs.

3. **Lead Pipeline is Production-Grade:** intelligent_lead_qualifier.py (1,052 lines), closed_loop_pipeline.py, generate_cold_emails.py, and website_signal_scorer.py form a genuine end-to-end lead qualification and outreach system. The closed-loop pipeline has crash recovery via active-tasks.md, parallel HTTP workers, and cron-friendly operation.

4. **Well-Structured Cron Orchestrator:** printmaxx_cron.sh tracks yield metrics, does pre-mutation CSV snapshots, has colored logging, and structured results tracking. It just needs to be installed.

5. **Memory Architecture is Sound:** The 3-layer memory system (HEARTBEAT.md for pulse, active-tasks.md for crash recovery, daily logs for history) is a legitimate autonomous agent pattern borrowed from OpenClaw. memory_manager.py keeps all three layers in sync.

6. **Reddit Scraper Actually Works:** background_reddit_scraper.py uses Reddit's JSON API (append `.json` to any subreddit URL), needs zero auth, and reliably extracts posts from 40+ subreddits. This is the one scraper that works out of the box.

7. **Quant Infrastructure is Serious:** alpha_screening.py uses category-specific decay rates, multi-factor scoring (evidence, replicability, time decay, historical performance, ROI potential). The venture_performance_tracker.py scores methods 0-100 with KILL/MAINTAIN/DOUBLE_DOWN recommendations. This is not toy code.
