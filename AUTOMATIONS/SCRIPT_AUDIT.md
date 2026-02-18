# AUTOMATIONS Script Audit

**Date:** 2026-02-06
**Total scripts:** 46 Python files
**Total lines:** 22,850
**Total disk:** 968 KB
**Auditor:** Phase 4 Automation Audit

---

## Section A: Script Inventory

### Full Inventory Table

| # | Script | Lines | Status | Purpose | Dependencies | Last Modified |
|---|--------|-------|--------|---------|--------------|---------------|
| 1 | `twitter_alpha_scraper.py` | 825 | WORKING | Bookmarks + high-signal account scraping with deep reply/funnel analysis, media download | playwright, brave-cookies | Feb 5 23:01 |
| 2 | `twitter_content_scraper.py` | 564 | WORKING | Meme/viral content download for repurposing, image download, caption generation | playwright, brave-cookies | Feb 5 23:03 |
| 3 | `background_twitter_scraper.py` | 437 | WORKING | Lightweight daily account scraper, cookie injection, append mode | playwright, brave-cookies | Feb 5 22:43 |
| 4 | `reddit_deep_scraper.py` | 640 | WORKING | All 41 subreddits via JSON API, deep comment scraping, number extraction, funnel detection | requests (stdlib-only) | Feb 5 23:29 |
| 5 | `viral_content_scanner.py` | 859 | WORKING | Viral tweet detection (10K+ likes), media download, repurpose queue, breaking news detection | playwright, brave-cookies | Feb 6 00:48 |
| 6 | `printmaxx_quant_terminal.py` | 1895 | WORKING | Bloomberg-style 6-panel TUI dashboard | textual, rich | Feb 4 20:58 |
| 7 | `ops_dashboard.py` | 725 | WORKING | 53 daily/weekly/monthly ops pattern tracker, Jane Street style | rich | Feb 4 20:11 |
| 8 | `revenue_projector.py` | 912 | WORKING | Monte Carlo simulation + Kelly Criterion position sizing | numpy (has stdlib fallback) | Feb 5 19:15 |
| 9 | `alpha_screening.py` | 851 | WORKING | Institutional-grade multi-factor alpha scoring with decay modeling | stdlib only | Feb 4 20:55 |
| 10 | `paper_trade.py` | 1154 | WORKING | Test methods with $0-100, statistical rigor, Kelly Criterion | stdlib only | Feb 4 20:56 |
| 11 | `method_performance_analyzer.py` | 451 | WORKING | Weekly method performance reports, revenue/hour, ROI calc | stdlib only | Feb 5 19:15 |
| 12 | `agent_monitor.py` | 253 | WORKING | Live agent progress monitoring | rich | Feb 2 15:50 |
| 13 | `niche_meta_detector.py` | 464 | WORKING | Ghibli/Saratoga pattern matching across niches | stdlib only | Feb 2 16:44 |
| 14 | `platform_meta_monitor.py` | 293 | WORKING | TikTok/X/IG algorithm change monitoring (framework only, needs WebSearch integration) | stdlib only | Feb 2 16:03 |
| 15 | `meme_coin_signal_tracker.py` | 508 | WORKING | Reddit/Twitter meme coin signal scoring | stdlib only | Feb 2 16:46 |
| 16 | `quant_dashboard.py` | 482 | WORKING | Simplified 6-panel Bloomberg TUI | textual | Feb 4 20:58 |
| 17 | `portfolio_rebalancer.py` | 775 | WORKING | KILL/SCALE/REDUCE/ADD portfolio recommendations | stdlib only | Feb 4 20:57 |
| 18 | `alpha_validator.py` | 743 | WORKING | Live web validation for alpha entries, freshness scoring, decay by category | stdlib only | Feb 4 20:56 |
| 19 | `alpha_csv_parser.py` | 209 | WORKING | ALPHA_STAGING.csv parser handling multiline quoted fields, corruption detection | stdlib only | Feb 6 02:58 |
| 20 | `auto_clip_pipeline.py` | 594 | WORKING | Long-form to viral short clips: download, transcribe, detect viral moments, crop | subprocess (yt-dlp, ffmpeg, whisper) | Feb 6 02:24 |
| 21 | `bulk_landing_page_generator.py` | 894 | WORKING | Generate conversion-optimized landing pages for local businesses | stdlib only | Feb 6 01:56 |
| 22 | `clip_post_scheduler.py` | 333 | WORKING | Optimal posting schedule generator for clips across platforms | stdlib only | Feb 6 02:25 |
| 23 | `daily_ops_from_alpha.py` | 422 | WORKING | Convert alpha entries into automated daily monitoring tasks | stdlib only | Feb 4 18:14 |
| 24 | `local_biz_pipeline.py` | 836 | WORKING | Master pipeline: scrape, generate, host, outreach for local biz redesign service | requests, beautifulsoup4 | Feb 6 02:08 |
| 25 | `local_biz_website_scraper.py` | 658 | WORKING | Scrape and analyze local business websites for redesign prospects | requests, beautifulsoup4, tqdm | Feb 6 01:54 |
| 26 | `ecom_arb_scanner.py` | 431 | WORKING | E-commerce arbitrage scanner comparing source vs selling prices | requests, beautifulsoup4 | Feb 6 02:26 |
| 27 | `trending_products_scanner.py` | 407 | WORKING | Trending product scanner across Amazon categories | requests, beautifulsoup4 | Feb 6 02:27 |
| 28 | `process_console_scrape.py` | 164 | WORKING | Process console-scraped JSON and append to ALPHA_STAGING.csv | stdlib only | Feb 3 15:50 |
| 29 | `reddit_alpha_scraper.py` | 527 | PARTIAL | Reddit meta/alpha extraction framework. Has analysis logic but uses Playwright for scraping (should use requests JSON API like reddit_deep_scraper) | playwright | Feb 2 16:21 |
| 30 | `background_reddit_scraper.py` | 272 | WORKING | Background Reddit scraper using requests JSON API | requests | Feb 4 22:34 |
| 31 | `twitter_scraper_live.py` | 510 | LEGACY | Chrome cookie-based Twitter scraper. Superseded by twitter_alpha_scraper.py (Brave cookies) | playwright, chrome | Feb 3 15:55 |
| 32 | `daily_reddit_scraper.py` | 263 | LEGACY | Playwright-based Reddit scraper via Chrome profile. Superseded by reddit_deep_scraper.py | playwright, chrome | Feb 3 17:33 |
| 33 | `daily_twitter_scraper.py` | 261 | LEGACY | Playwright-based Twitter scraper via Chrome profile. Superseded by twitter_alpha_scraper.py | playwright, chrome | Feb 3 17:33 |
| 34 | `enhanced_reddit_scraper.py` | 229 | LEGACY | Playwright Reddit scraper with comments. Superseded by reddit_deep_scraper.py | playwright | Feb 4 18:46 |
| 35 | `enhanced_twitter_scraper.py` | 418 | LEGACY | Playwright Twitter scraper with reply funnel detection. Superseded by twitter_alpha_scraper.py | playwright, chrome | Feb 4 18:48 |
| 36 | `headless_reddit_scraper.py` | 210 | LEGACY | Headless Playwright Reddit scraper. Superseded by reddit_deep_scraper.py | playwright | Feb 4 18:26 |
| 37 | `headless_twitter_scraper.py` | 267 | LEGACY | Headless Playwright Twitter scraper. Superseded by background_twitter_scraper.py | playwright, chrome | Feb 4 18:25 |
| 38 | `parallel_background_scraper.py` | 283 | LEGACY | Parallel Playwright Twitter scraper copying Chrome profile. Superseded by twitter_alpha_scraper.py | playwright, chrome | Feb 3 16:32 |
| 39 | `parallel_twitter_scraper.py` | 217 | LEGACY | Parallel Playwright scraper via CDP. Superseded by twitter_alpha_scraper.py | playwright, chrome | Feb 4 17:59 |
| 40 | `scrape_caiden_cdp.py` | 201 | LEGACY | Single-account Caiden scraper via CDP. One-off, superseded by twitter_alpha_scraper.py | playwright, chrome | Feb 3 15:44 |
| 41 | `scrape_caiden_playwright.py` | 113 | LEGACY | Single-account Caiden scraper. One-off, superseded | playwright, chrome | Feb 3 15:14 |
| 42 | `scrape_parallel_fixed.py` | 255 | LEGACY | "Fixed" parallel scraper. Superseded by twitter_alpha_scraper.py | playwright, chrome | Feb 3 16:34 |
| 43 | `scrape_twitter_applescript.py` | 280 | LEGACY | AppleScript-based Twitter scraper controlling Chrome. Novel approach, fragile | applescript, chrome | Feb 3 16:00 |
| 44 | `scrape_twitter_selenium.py` | 293 | LEGACY | Selenium-based Twitter scraper. Superseded by Playwright-based scrapers | selenium, chrome | Feb 3 15:51 |
| 45 | `scrape_via_websearch.py` | 97 | STUB | Loads accounts but requires external WebSearch agent call to actually scrape. Not standalone | stdlib only | Feb 3 16:43 |
| 46 | `backtest_alpha_DEPRECATED.py` | 375 | DEPRECATED | Old alpha backtesting. Replaced by alpha_screening.py + alpha_validator.py | stdlib only | Feb 2 15:50 |

### Summary Statistics

| Category | Count | Lines | % of Total |
|----------|-------|-------|------------|
| **WORKING** | 30 | 16,739 | 73.2% |
| **PARTIAL** | 1 | 527 | 2.3% |
| **LEGACY** | 13 | 3,590 | 15.7% |
| **STUB** | 1 | 97 | 0.4% |
| **DEPRECATED** | 1 | 375 | 1.6% |
| **Total** | 46 | 22,850 | 100% |

---

## Section B: Working Scripts

### Tier 1: Production Scrapers (Tested, Confirmed Working per Project Memory)

**1. `twitter_alpha_scraper.py` (825 lines) - PRIMARY Twitter Scraper**
- Extracts cookies from Brave Browser, injects into headless Chromium
- Brave stays open and untouched during scraping
- Modes: `--bookmarks`, `--accounts`, `--all`, `--meme`, `--deep`, `--download-media`
- Deep mode: clicks into tweets, scrapes top replies, detects funnels
- Output: appends to `LEDGER/ALPHA_STAGING.csv`
- Usage: `python3 AUTOMATIONS/twitter_alpha_scraper.py --all --deep`

**2. `twitter_content_scraper.py` (564 lines) - Content Repurposing**
- Downloads viral/meme images and videos for repurposing
- Generates quote tweet drafts with reply-bait captions
- Uses same Brave cookie injection pattern
- Output: `AUTOMATIONS/content_library/` + `AUTOMATIONS/repurpose_queue.csv`
- Usage: `python3 AUTOMATIONS/twitter_content_scraper.py @daquan @pubity --captions`

**3. `background_twitter_scraper.py` (437 lines) - Lightweight Daily**
- Lightweight daily scraper, good for background cron jobs
- Cookie injection from Brave
- Output: appends to `LEDGER/ALPHA_STAGING.csv`
- Usage: `python3 AUTOMATIONS/background_twitter_scraper.py --full`

**4. `reddit_deep_scraper.py` (640 lines) - PRIMARY Reddit Scraper**
- Uses Reddit JSON API (no browser, no auth, no anti-bot)
- Scrapes all 41 subreddits from `RESEARCH_SUBREDDITS.csv`
- Deep comment scraping, number extraction ($revenue, %growth)
- Funnel detection in comments, engagement-weighted scoring
- Output: appends to `LEDGER/ALPHA_STAGING.csv` + JSON backups
- Usage: `python3 AUTOMATIONS/reddit_deep_scraper.py --daily --deep`

**5. `viral_content_scanner.py` (859 lines) - Viral Content Detection**
- Monitors meme/viral accounts for high-engagement content (10K+ likes, 2K+ RT)
- Breaking news detection (viral velocity in last 2 hours)
- Media download and repurpose queue generation
- Uses Brave cookie injection
- Output: `AUTOMATIONS/viral_queue.csv`
- Usage: `python3 AUTOMATIONS/viral_content_scanner.py --scan --download`

### Tier 2: Quant Infrastructure (All Tested, All Parse/Run)

**6. `printmaxx_quant_terminal.py` (1895 lines) - Main Dashboard**
- Bloomberg-style 6-panel TUI (requires `textual` package)
- Panels: Alpha Discovery, Method Performance, Agent Activity, Portfolio, Backtests, Alerts
- Quick summary: `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary`
- Full TUI: `python3 AUTOMATIONS/printmaxx_quant_terminal.py`

**7. `ops_dashboard.py` (725 lines) - Operations Tracker**
- Tracks 53 daily/weekly/monthly operations patterns
- Summary mode: `python3 AUTOMATIONS/ops_dashboard.py --summary`
- Run specific op: `python3 AUTOMATIONS/ops_dashboard.py --run DOP001`
- Run all daily: `python3 AUTOMATIONS/ops_dashboard.py --run-daily`

**8. `revenue_projector.py` (912 lines) - Revenue Modeling**
- Monte Carlo simulation with Kelly Criterion position sizing
- Has numpy fallback for stdlib-only environments
- Runs automatically on invocation (no --help, just outputs projections)
- Loads: backtests (670), paper trades (2), validated alpha (20), synergies (92)

**9. `alpha_screening.py` (851 lines) - Alpha Scoring**
- 100-point multi-factor scoring: Evidence (30), Replicability (20), Time Decay (20), Historical (15), ROI (15)
- Category-specific decay rates (PLATFORM_ARBITRAGE: 50%/mo, APP_FACTORY: 10%/mo)
- Usage: `python3 AUTOMATIONS/alpha_screening.py --pending`

**10. `paper_trade.py` (1154 lines) - Paper Trading**
- Statistical framework: min 10 data points, 80% confidence, Kelly Criterion
- Decision: SCALE (revenue/hr >= $20, 80% confidence, 10+ obs) or KILL
- Usage: `python3 AUTOMATIONS/paper_trade.py --list`

**11. `method_performance_analyzer.py` (451 lines) - Weekly Analysis**
- Reads revenue, expenses, funnel metrics
- Classifies methods as winners/losers
- Auto-runs on invocation, outputs to `OPS/reports/`
- Usage: `python3 AUTOMATIONS/method_performance_analyzer.py`

**12. `portfolio_rebalancer.py` (775 lines) - Portfolio Management**
- KILL/SCALE/REDUCE/ADD recommendations
- Risk limits: max 40% single method, max 50% single platform, min 3 active
- Usage: `python3 AUTOMATIONS/portfolio_rebalancer.py --simulate`

**13. `alpha_validator.py` (743 lines) - Alpha Freshness**
- Validates alpha against current web data (URL check, recency search, "patched" detection)
- Category-specific half-lives (30-180 days)
- Usage: `python3 AUTOMATIONS/alpha_validator.py --pending`

**14. `quant_dashboard.py` (482 lines) - Simplified TUI**
- Lighter 6-panel Textual dashboard (alternative to printmaxx_quant_terminal)
- Usage: `python3 AUTOMATIONS/quant_dashboard.py`

### Tier 3: Business Automation

**15. `local_biz_pipeline.py` (836 lines) - Full Local Biz Pipeline**
- End-to-end: SCRAPE websites, GENERATE landing pages, HOST, OUTREACH via cold email
- Usage: `python3 AUTOMATIONS/local_biz_pipeline.py --category dentist --city "Austin TX" --dry-run`

**16. `local_biz_website_scraper.py` (658 lines) - Website Analysis**
- Analyze business websites for redesign prospects (mobile, SEO, SSL scoring)
- Requires: requests, beautifulsoup4, tqdm
- Usage: `python3 AUTOMATIONS/local_biz_website_scraper.py --demo`

**17. `bulk_landing_page_generator.py` (894 lines) - Landing Page Generator**
- Category-specific templates (dentist, plumber, restaurant, etc.)
- Generates full HTML landing pages
- Usage: `python3 AUTOMATIONS/bulk_landing_page_generator.py --name "Joe's Plumbing" --category plumber --city "Austin TX" --preview`

**18. `ecom_arb_scanner.py` (431 lines) - Ecom Arbitrage**
- Compares source prices to selling prices across eBay, Amazon, Mercari, etc.
- Calculates net profit after platform fees
- Usage: `python3 AUTOMATIONS/ecom_arb_scanner.py electronics --min-profit 10`

**19. `trending_products_scanner.py` (407 lines) - Trending Products**
- Scans Amazon movers/bestsellers/wishlists for trending products
- Usage: `python3 AUTOMATIONS/trending_products_scanner.py --source movers --category electronics`

### Tier 4: Content Pipeline

**20. `auto_clip_pipeline.py` (594 lines) - Video Clip Pipeline**
- Download VODs with yt-dlp, transcribe with Whisper, detect viral moments, auto-crop 9:16
- Warning: Whisper not installed (`pip install openai-whisper`)
- Usage: `python3 AUTOMATIONS/auto_clip_pipeline.py --url "https://youtube.com/watch?v=xxx" --demo`

**21. `clip_post_scheduler.py` (333 lines) - Post Scheduling**
- Generates optimal posting times by platform (TikTok, Twitter, IG, YouTube)
- Usage: `python3 AUTOMATIONS/clip_post_scheduler.py --input clips/clips_metadata.csv --output schedule.csv`

### Tier 5: Analysis & Monitoring

**22. `niche_meta_detector.py` (464 lines) - Pattern Detection**
- Detects Ghibli-pattern (aesthetic virality), Saratoga-pattern (pump), Morning Routine, etc.
- Auto-runs and outputs to `LEDGER/META_TRACKER.csv` and `LEDGER/NICHE_META_OPPORTUNITIES.csv`

**23. `platform_meta_monitor.py` (293 lines) - Platform Monitoring**
- Framework for monitoring TikTok/X/IG algorithm changes
- Note: scanning phase is a placeholder that logs URLs, needs WebSearch integration to fetch data

**24. `meme_coin_signal_tracker.py` (508 lines) - Memecoin Signals**
- Scores coin entry potential (0-100) based on pattern matching
- Auto-runs with example data on invocation

**25. `agent_monitor.py` (253 lines) - Agent Progress**
- Live dashboard for running agents, ralph loops, ALPHA_STAGING growth
- Requires `rich` package

**26. `daily_ops_from_alpha.py` (422 lines) - Alpha to Ops**
- Converts alpha entries into automated daily monitoring tasks
- Found 178 of 1229 entries convertible to daily ops

**27. `alpha_csv_parser.py` (209 lines) - CSV Parser**
- Robust ALPHA_STAGING.csv parser handling multiline fields and corruption
- Multi-format support (11-col, 13-col, 14-col)
- Usage: `python3 AUTOMATIONS/alpha_csv_parser.py`

**28. `process_console_scrape.py` (164 lines) - Console Import**
- Processes console-scraped JSON and appends to ALPHA_STAGING.csv
- Usage: `python3 AUTOMATIONS/process_console_scrape.py <json_file>`

**29. `background_reddit_scraper.py` (272 lines) - Reddit via Requests**
- Background Reddit scraper using requests JSON API
- Simpler alternative to reddit_deep_scraper.py (less features)
- Usage: `python3 AUTOMATIONS/background_reddit_scraper.py --full`

### Tier 6: Partial

**30. `reddit_alpha_scraper.py` (527 lines) - Reddit Alpha (PARTIAL)**
- Has good analysis/categorization logic for Reddit data
- BUT uses Playwright for scraping (should use requests JSON API)
- The analysis logic could be merged into reddit_deep_scraper.py

---

## Section C: Legacy/Stub Scripts (Candidates for Deletion)

### 13 Legacy Playwright/Chrome Scrapers

These scripts all share the same problem: they use Playwright with Chrome profiles for scraping Twitter and Reddit. This approach was superseded when the team discovered:
1. User uses Brave Browser (not Chrome) for Twitter login
2. Chrome's `AutomationProfile` was empty with no logins
3. Profile copy approach failed (headless can't decrypt copied cookies)
4. Reddit blocks Playwright/Selenium entirely

All have been replaced by the Brave cookie injection approach in `twitter_alpha_scraper.py` and the requests JSON API in `reddit_deep_scraper.py`.

| # | Script | Lines | Problem | Replaced By |
|---|--------|-------|---------|-------------|
| 1 | `daily_reddit_scraper.py` | 263 | Uses Playwright + Chrome profile for Reddit | `reddit_deep_scraper.py` |
| 2 | `daily_twitter_scraper.py` | 261 | Uses Playwright + Chrome profile for Twitter | `twitter_alpha_scraper.py` |
| 3 | `enhanced_reddit_scraper.py` | 229 | Uses Playwright for Reddit (blocked) | `reddit_deep_scraper.py` |
| 4 | `enhanced_twitter_scraper.py` | 418 | Uses Playwright + Chrome profile | `twitter_alpha_scraper.py` |
| 5 | `headless_reddit_scraper.py` | 210 | Uses Playwright for Reddit (blocked) | `reddit_deep_scraper.py` |
| 6 | `headless_twitter_scraper.py` | 267 | Uses Playwright + `.printmaxx-chrome-profile` | `background_twitter_scraper.py` |
| 7 | `parallel_background_scraper.py` | 283 | Uses Playwright + Chrome profile copy | `twitter_alpha_scraper.py` |
| 8 | `parallel_twitter_scraper.py` | 217 | Uses Playwright CDP to connect to Chrome | `twitter_alpha_scraper.py` |
| 9 | `scrape_caiden_cdp.py` | 201 | One-off single-account scraper via CDP | `twitter_alpha_scraper.py` |
| 10 | `scrape_caiden_playwright.py` | 113 | One-off single-account scraper | `twitter_alpha_scraper.py` |
| 11 | `scrape_parallel_fixed.py` | 255 | "Fixed" parallel Chrome profile copy approach | `twitter_alpha_scraper.py` |
| 12 | `scrape_twitter_applescript.py` | 280 | AppleScript controlling Chrome (fragile) | `twitter_alpha_scraper.py` |
| 13 | `scrape_twitter_selenium.py` | 293 | Selenium + Chrome (older approach) | `twitter_alpha_scraper.py` |

**Recommendation: DELETE ALL 13.** Total: 3,290 lines. No unique logic not already in the working scrapers. They represent iterative attempts to solve the Chrome authentication problem that was ultimately solved by Brave cookie extraction.

### 1 Intermediate Scraper

| Script | Lines | Status | Notes |
|--------|-------|--------|-------|
| `twitter_scraper_live.py` | 510 | LEGACY | Uses Chrome cookies (not Brave). Intermediate version between legacy and current approach. Some cookie extraction logic was basis for current scrapers. |

**Recommendation: DELETE.** The cookie extraction logic has been improved and incorporated into `twitter_alpha_scraper.py`.

### 1 Stub

| Script | Lines | Status | Notes |
|--------|-------|--------|-------|
| `scrape_via_websearch.py` | 97 | STUB | Loads accounts list but prints "Need to call WebSearch via agent for actual scraping". Not standalone, requires external agent to do the actual work. |

**Recommendation: DELETE.** The WebSearch approach for Twitter scraping is inferior to the Brave cookie injection method.

### 1 Deprecated

| Script | Lines | Status | Notes |
|--------|-------|--------|-------|
| `backtest_alpha_DEPRECATED.py` | 375 | DEPRECATED | Filename explicitly marks it as deprecated. Replaced by `alpha_screening.py` (851 lines, better scoring) + `alpha_validator.py` (743 lines, web validation). |

**Recommendation: DELETE.** Already explicitly deprecated in its filename.

---

## Section D: Missing Automation

### High Priority (Would Directly Generate Revenue)

| # | Missing Automation | Purpose | Priority | Effort |
|---|-------------------|---------|----------|--------|
| 1 | **Content auto-poster** | Post scheduled content to Twitter/X, TikTok, Instagram from CSV queue | P0 | 2-3 days |
| 2 | **Fanvue/Fansly uploader** | Batch upload AI-generated content to Fanvue/Fansly with tiers/pricing | P0 | 2 days |
| 3 | **Whop/Gumroad product lister** | Create and list digital products from specs automatically | P1 | 1-2 days |
| 4 | **Cold email sender** | Integrate with DeliverOn/EmailBison/Instantly to send cold email sequences | P1 | 2 days |
| 5 | **ComfyUI batch generator** | Batch generate AI images/videos via ComfyUI API for AI personas | P1 | 3 days |

### Medium Priority (Would Improve Operational Efficiency)

| # | Missing Automation | Purpose | Priority | Effort |
|---|-------------------|---------|----------|--------|
| 6 | **Cron/scheduler orchestrator** | Unified scheduler to run daily/weekly scripts (currently manual) | P2 | 1 day |
| 7 | **Revenue auto-tracker** | Auto-detect Stripe/Gumroad/Fanvue transactions and update REVENUE_TRACKER.csv | P2 | 2 days |
| 8 | **Health check runner** | Run all scripts with `--help` or dry-run to detect breakage proactively | P2 | 0.5 day |
| 9 | **Alpha auto-reviewer** | Apply alpha-review.md rules automatically to PENDING_REVIEW entries using Claude API | P2 | 1 day |
| 10 | **Beehiiv newsletter sender** | Draft and schedule newsletters via Beehiiv API | P2 | 1 day |

### Low Priority (Nice to Have)

| # | Missing Automation | Purpose | Priority | Effort |
|---|-------------------|---------|----------|--------|
| 11 | **Competitor price monitor** | Monitor competitor pricing pages (currently described in alpha but not automated) | P3 | 1 day |
| 12 | **ASO keyword tracker** | Track App Store keyword rankings for launched apps | P3 | 1 day |
| 13 | **Twitter engagement bot** | Auto-like, reply, quote-tweet from managed accounts (grey-hat, platform risk) | P3 | 2 days |
| 14 | **Content A/B test runner** | Post variants, measure engagement, auto-pick winner | P3 | 2 days |

---

## Section E: Recommended Cleanup

### Scripts to Delete (16 scripts, 4,272 lines)

| Script | Lines | Rationale |
|--------|-------|-----------|
| `daily_reddit_scraper.py` | 263 | Playwright+Chrome for Reddit (blocked). Use `reddit_deep_scraper.py` |
| `daily_twitter_scraper.py` | 261 | Playwright+Chrome for Twitter. Use `twitter_alpha_scraper.py` |
| `enhanced_reddit_scraper.py` | 229 | Playwright for Reddit (blocked). Use `reddit_deep_scraper.py` |
| `enhanced_twitter_scraper.py` | 418 | Playwright+Chrome. Use `twitter_alpha_scraper.py` |
| `headless_reddit_scraper.py` | 210 | Playwright for Reddit (blocked). Use `reddit_deep_scraper.py` |
| `headless_twitter_scraper.py` | 267 | Playwright+fake profile. Use `background_twitter_scraper.py` |
| `parallel_background_scraper.py` | 283 | Chrome profile copy (broken). Use `twitter_alpha_scraper.py` |
| `parallel_twitter_scraper.py` | 217 | CDP approach. Use `twitter_alpha_scraper.py` |
| `scrape_caiden_cdp.py` | 201 | One-off single account. Use `twitter_alpha_scraper.py --accounts` |
| `scrape_caiden_playwright.py` | 113 | One-off single account. Use `twitter_alpha_scraper.py --accounts` |
| `scrape_parallel_fixed.py` | 255 | "Fixed" version still broken. Use `twitter_alpha_scraper.py` |
| `scrape_twitter_applescript.py` | 280 | AppleScript fragile approach. Use `twitter_alpha_scraper.py` |
| `scrape_twitter_selenium.py` | 293 | Selenium older approach. Use `twitter_alpha_scraper.py` |
| `scrape_via_websearch.py` | 97 | Stub, not standalone. Use real scrapers |
| `twitter_scraper_live.py` | 510 | Chrome cookies, superseded by Brave approach |
| `backtest_alpha_DEPRECATED.py` | 375 | Explicitly deprecated in filename |

**Total to delete: 16 scripts, 4,272 lines, ~180 KB**

### Scripts to Merge

| Merge From | Merge Into | Rationale |
|-----------|-----------|-----------|
| `reddit_alpha_scraper.py` (analysis logic) | `reddit_deep_scraper.py` | reddit_alpha_scraper has good meta-detection/categorization code but uses Playwright for scraping. Extract the analysis functions, merge into reddit_deep_scraper |
| `background_reddit_scraper.py` | `reddit_deep_scraper.py` | background_reddit_scraper is a simpler version of reddit_deep_scraper using same requests approach. Merge unique features (if any) and delete |

**Post-merge deletions: 2 more scripts, 799 lines**

### Scripts to Upgrade

| Script | Issue | Fix |
|--------|-------|-----|
| `platform_meta_monitor.py` | Scanning phase is placeholder (logs URLs, doesn't fetch) | Integrate WebSearch or requests to actually fetch platform announcement pages |
| `auto_clip_pipeline.py` | Whisper not installed | `pip install openai-whisper` (or switch to faster-whisper) |
| `meme_coin_signal_tracker.py` | Only runs with example data, no real signal sources connected | Connect to Reddit/Twitter scraper output for real signal detection |

### Estimated Savings After Cleanup

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Script count | 46 | 28 | 18 fewer (39% reduction) |
| Total lines | 22,850 | 17,779 | 5,071 fewer (22% reduction) |
| Disk size | 968 KB | ~750 KB | ~218 KB |
| Cognitive load | High (which scraper do I use?) | Low (1 per platform) | Significant |

---

## Section F: Automation Map

### Data Flow Diagram

```
                     INPUTS                          PROCESSING                         OUTPUTS
                     ======                          ==========                         =======

  Brave Browser                                                                   LEDGER/ALPHA_STAGING.csv
  (Twitter login) ─────┐                                                         (source of truth)
                        │                                                              │
                        ▼                                                              │
              ┌─────────────────────┐                                                  │
              │  TWITTER SCRAPERS   │                                                  │
              │                     │                                                  │
              │  twitter_alpha_     │──── bookmarks + accounts ────────────────────────►│
              │  scraper.py         │                                                  │
              │                     │                                                  │
              │  background_        │──── daily lightweight ───────────────────────────►│
              │  twitter_scraper.py │                                                  │
              │                     │                                                  │
              │  twitter_content_   │──── viral content ──────► content_library/        │
              │  scraper.py         │                           repurpose_queue.csv     │
              │                     │                                                  │
              │  viral_content_     │──── breaking viral ─────► viral_queue.csv         │
              │  scanner.py         │                                                  │
              └─────────────────────┘                                                  │
                                                                                       │
  Reddit JSON API ──────┐                                                              │
  (no auth needed)      │                                                              │
                        ▼                                                              │
              ┌─────────────────────┐                                                  │
              │  REDDIT SCRAPERS    │                                                  │
              │                     │                                                  │
              │  reddit_deep_       │──── 41 subreddits + comments ───────────────────►│
              │  scraper.py         │         + JSON backups                            │
              │                     │                                                  │
              │  background_reddit_ │──── simpler daily ──────────────────────────────►│
              │  scraper.py         │                                                  │
              └─────────────────────┘                                                  │
                                                                                       │
  Console scrape ───────┐                                                              │
                        ▼                                                              │
              ┌─────────────────────┐                                                  │
              │  process_console_   │──── JSON import ────────────────────────────────►│
              │  scrape.py          │                                                  │
              └─────────────────────┘                                                  │
                                                                                       │
                                                                                       ▼
                                                                          ┌────────────────────────┐
                                                                          │   SCREENING PIPELINE   │
                                                                          │                        │
                    ┌─────────────────────────────────────────────────────►│  alpha_csv_parser.py   │
                    │                                                      │  (parse + clean)       │
                    │                                                      │         │              │
                    │                                                      │         ▼              │
                    │                                                      │  alpha_screening.py    │
                    │                                                      │  (100-pt scoring)      │
                    │                                                      │         │              │
                    │                                                      │         ▼              │
                    │                                                      │  alpha_validator.py    │
                    │                                                      │  (web freshness)       │
                    │                                                      │         │              │
                    │                                                      │         ▼              │
                    │                                                      │  SCALE / PAPER_TRADE   │
                    │                                                      │  / KILL decision       │
                    │                                                      └────────────────────────┘
                    │                                                                 │
                    │                                                                 ▼
                    │                                                    ┌──────────────────────────┐
                    │                                                    │   PAPER TRADING          │
                    │                                                    │                          │
                    │                                                    │  paper_trade.py          │
                    │                                                    │  (test with $0-100)      │
                    │                                                    │         │                │
                    │                                                    │         ▼                │
                    │                                                    │  SCALE / ITERATE / KILL  │
                    │                                                    └──────────────────────────┘
                    │                                                                 │
                    │                                                                 ▼
                    │                                                    ┌──────────────────────────┐
                    │                                                    │  PORTFOLIO MANAGEMENT    │
                    │                                                    │                          │
                    │                                                    │  revenue_projector.py    │
                    │                                                    │  (Monte Carlo + Kelly)   │
                    │                                                    │         │                │
                    │                                                    │         ▼                │
                    │                                                    │  portfolio_rebalancer.py │
                    │                                                    │  (KILL/SCALE/REDUCE/ADD) │
                    │                                                    │         │                │
                    │                                                    │         ▼                │
                    │                                                    │  method_performance_     │
                    │                                                    │  analyzer.py             │
                    │                                                    │  (weekly reports)        │
                    │                                                    └──────────────────────────┘
                    │
                    │                                                    ┌──────────────────────────┐
                    │                                                    │  DASHBOARDS (TUI)        │
                    │                                                    │                          │
                    ├───────────────────────────────────────────────────►│  printmaxx_quant_        │
                    │                                                    │  terminal.py (main)      │
                    │                                                    │                          │
                    ├───────────────────────────────────────────────────►│  quant_dashboard.py      │
                    │                                                    │  (simplified)            │
                    │                                                    │                          │
                    ├───────────────────────────────────────────────────►│  ops_dashboard.py        │
                    │                                                    │  (53 ops tracker)        │
                    │                                                    │                          │
                    └───────────────────────────────────────────────────►│  agent_monitor.py        │
                                                                         │  (live agents)           │
                                                                         └──────────────────────────┘


  ┌────────────────────────────────────────────────────────────────────────────────┐
  │  STANDALONE BUSINESS AUTOMATION (not connected to main pipeline)              │
  │                                                                                │
  │  local_biz_website_scraper.py ──► local_biz_pipeline.py ──► bulk_landing_     │
  │  (analyze websites)               (orchestrate)              page_generator.py │
  │                                                              (generate HTML)   │
  │                                                                                │
  │  ecom_arb_scanner.py ──► OPS/ECOM_ARBITRAGE_OPPORTUNITIES.md                  │
  │  trending_products_scanner.py ──► trending product CSVs                        │
  │                                                                                │
  │  auto_clip_pipeline.py ──► clip_post_scheduler.py ──► posting_schedule.csv    │
  │  (extract clips)           (schedule posts)                                    │
  └────────────────────────────────────────────────────────────────────────────────┘


  ┌────────────────────────────────────────────────────────────────────────────────┐
  │  MONITORING / DETECTION (read-only, feed back into alpha)                     │
  │                                                                                │
  │  niche_meta_detector.py ──► LEDGER/META_TRACKER.csv                           │
  │                              LEDGER/NICHE_META_OPPORTUNITIES.csv               │
  │                                                                                │
  │  platform_meta_monitor.py ──► LEDGER/ALPHA_STAGING.csv (placeholder only)     │
  │                                                                                │
  │  meme_coin_signal_tracker.py ──► LEDGER/MEME_COIN_SIGNALS.csv                │
  │                                                                                │
  │  daily_ops_from_alpha.py ──► OPS/DAILY_AUTOMATED_TASKS.md                     │
  └────────────────────────────────────────────────────────────────────────────────┘
```

### What is Automated vs Manual

| Activity | Automated? | Tool | Notes |
|----------|-----------|------|-------|
| Twitter scraping | YES | twitter_alpha_scraper.py | Needs manual trigger (no cron) |
| Reddit scraping | YES | reddit_deep_scraper.py | Needs manual trigger (no cron) |
| Alpha scoring | YES | alpha_screening.py | Needs manual trigger |
| Alpha web validation | YES | alpha_validator.py | Needs manual trigger |
| Paper trading setup | YES | paper_trade.py | Manual data entry for observations |
| Revenue projection | YES | revenue_projector.py | Auto-runs, reads from CSVs |
| Performance analysis | YES | method_performance_analyzer.py | Needs manual trigger |
| Portfolio rebalancing | YES | portfolio_rebalancer.py | Needs manual trigger |
| Local biz pipeline | YES | local_biz_pipeline.py | Needs manual trigger + URLs |
| Ecom arbitrage scan | YES | ecom_arb_scanner.py | Needs manual trigger |
| Video clip extraction | YES | auto_clip_pipeline.py | Needs Whisper install |
| Dashboard viewing | YES | printmaxx_quant_terminal.py | Interactive TUI |
| **Scheduling/cron** | **NO** | Missing | All scripts require manual invocation |
| **Content posting** | **NO** | Missing | No auto-poster to Twitter/TikTok/IG |
| **Revenue tracking** | **NO** | Missing | Manual CSV updates |
| **Email sending** | **NO** | Missing | No ESP integration |
| **AI content generation** | **NO** | Missing | No ComfyUI/Flux automation |
| **Product listing** | **NO** | Missing | No Whop/Gumroad API integration |
| **Alpha review** | **PARTIAL** | alpha_screening.py | Scores but doesn't decide APPROVED/REJECTED per human criteria |

### Dependency Graph

```
Required Python packages:
  playwright ........... twitter_alpha_scraper, twitter_content_scraper, background_twitter_scraper, viral_content_scanner
  textual .............. printmaxx_quant_terminal, quant_dashboard
  rich ................. ops_dashboard, agent_monitor
  requests ............. reddit_deep_scraper, background_reddit_scraper, local_biz_*, ecom_arb_scanner, trending_products_scanner
  beautifulsoup4 ....... local_biz_*, ecom_arb_scanner
  tqdm ................. local_biz_website_scraper
  numpy ................ revenue_projector (has stdlib fallback)
  openai-whisper ....... auto_clip_pipeline (NOT INSTALLED)

External tools:
  Brave Browser ........ Twitter scrapers (cookie source)
  yt-dlp ............... auto_clip_pipeline (video download)
  ffmpeg ............... auto_clip_pipeline (video processing)
  Claude API ........... auto_clip_pipeline (viral moment detection)
```

---

## Appendix: Quick Command Reference

### Daily Operations
```bash
# Morning alpha scan
python3 AUTOMATIONS/reddit_deep_scraper.py --daily --deep
python3 AUTOMATIONS/twitter_alpha_scraper.py --all --deep

# Screen new alpha
python3 AUTOMATIONS/alpha_screening.py --pending

# Check system health
python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary

# Weekly analysis
python3 AUTOMATIONS/method_performance_analyzer.py
python3 AUTOMATIONS/portfolio_rebalancer.py --simulate
```

### One-Time Setup
```bash
pip install playwright textual rich requests beautifulsoup4 tqdm
playwright install chromium
# Optional: pip install openai-whisper numpy
```

### Deletion Command (When Approved)
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS
rm -f daily_reddit_scraper.py daily_twitter_scraper.py enhanced_reddit_scraper.py \
      enhanced_twitter_scraper.py headless_reddit_scraper.py headless_twitter_scraper.py \
      parallel_background_scraper.py parallel_twitter_scraper.py scrape_caiden_cdp.py \
      scrape_caiden_playwright.py scrape_parallel_fixed.py scrape_twitter_applescript.py \
      scrape_twitter_selenium.py scrape_via_websearch.py twitter_scraper_live.py \
      backtest_alpha_DEPRECATED.py
```
