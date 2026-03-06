## Daily Research & Organization (NON-NEGOTIABLE — RUN ALL SCRAPERS EVERY SESSION)

**Commands:** `/daily-research` (scan sources) | `/review-alpha` (approve findings) | `./ralph/run_mega.sh` (overnight)

**All findings go to:** `LEDGER/ALPHA_STAGING.csv` with status PENDING_REVIEW.

### Full Daily Research Pipeline (RUN ALL OF THESE)

Every session and every daily cron cycle MUST run the full scraper pipeline. This is not optional. Use both existing (battle-tested) scrapers AND new value-add scrapers together.

**PHASE 1: Existing Scrapers (Brave cookies + headless browser, PROVEN WORKING)**

| Script | Command | What It Does | Auth |
|--------|---------|-------------|------|
| **Twitter Alpha Scraper** | `python3 AUTOMATIONS/twitter_alpha_scraper.py --all` | Scrapes 89+ high-signal Twitter accounts + bookmarks via Playwright + Brave cookies | Brave cookies |
| **Background Twitter Scraper** | `python3 AUTOMATIONS/background_twitter_scraper.py --scrape` | Background headless Twitter scraping with Brave cookie injection | Brave cookies |
| **Background Reddit Scraper** | `python3 AUTOMATIONS/background_reddit_scraper.py --scrape` | Reddit JSON API scraping, no auth needed | None |
| **Reddit Deep Scraper** | `python3 AUTOMATIONS/reddit_deep_scraper.py` | Deep Reddit thread analysis with comment extraction | None |
| **Reddit Alpha Scraper** | `python3 AUTOMATIONS/reddit_alpha_scraper.py` | Reddit alpha extraction for solopreneur signals | None |

**PHASE 2: New Value-Add Scrapers (API-based + specialized)**

| Script | Command | What It Does | Cron |
|--------|---------|-------------|------|
| **Daily Research Orchestrator** | `python3 AUTOMATIONS/daily_research_orchestrator.py --full` | Master orchestrator: runs 5 scrapers + HN + 41 subs + PH, deduplicates, scores 0-100 | 5 AM |
| **Twitter Bookmarks Scraper** | `python3 AUTOMATIONS/twitter_bookmarks_scraper.py --scrape` | GraphQL API bookmarks extraction (Brave cookies, auto-alpha) | 6 AM |
| **Daily Research Pipeline** | `python3 AUTOMATIONS/daily_research_pipeline.py --full` | Scrape-extract-filter-repurpose master pipeline | 6:30 AM |
| **Unified Alpha Monitor** | `python3 AUTOMATIONS/unified_alpha_monitor.py --full` | 350+ sources: Reddit niche + GitHub MIT + ASO + competitors + freshness | 5:45 AM |
| **Reddit Pain Point Miner** | `python3 AUTOMATIONS/reddit_pain_point_miner.py --scan` | Buying intent extraction from 25 subreddits | 6:30 AM |
| **Telegram Community Monitor** | `python3 AUTOMATIONS/telegram_community_monitor.py --scan` | 26 public channels, 8 niches, signal keyword scoring | 9:15 AM |

**PHASE 3: Competitive Intelligence Scrapers**

| Script | Command | What It Does | Cron |
|--------|---------|-------------|------|
| **Competitor Monitor** | `python3 AUTOMATIONS/competitor_monitor.py --scan` | 19 apps, 6 niches, iTunes API price/rating tracking | 7 AM |
| **App Store Tracker** | `python3 AUTOMATIONS/app_store_competitor_tracker.py` | 36 apps, price/rating/version change detection | 7 AM |
| **Trend Scanner** | `python3 AUTOMATIONS/trend_scanner.py --full` | Gumroad + Reddit pulse, niche trend detection | Mon 6 AM |
| **Gumroad Niche Scanner** | `python3 AUTOMATIONS/gumroad_niche_scanner.py` | 9 niches, scored product signals | 8:30 AM |

**PHASE 4: Alpha Processing (RUN AFTER ALL SCRAPERS COMPLETE)**

| Script | Command | What It Does | Cron |
|--------|---------|-------------|------|
| **Alpha Review Bot** | `python3 AUTOMATIONS/alpha_review_bot.py` | Clears PENDING_REVIEW backlog, classifies alpha | 6 AM |
| **Alpha Auto-Processor** | `python3 AUTOMATIONS/alpha_auto_processor.py --process-new` | Routes approved alpha to ventures/OPS/cron/archive | 6:30 AM |

### Quick Daily Research Command (Run This Every Session)

```bash
# Run all scrapers in parallel, then process alpha
python3 AUTOMATIONS/twitter_alpha_scraper.py --all &
python3 AUTOMATIONS/background_twitter_scraper.py --scrape &
python3 AUTOMATIONS/background_reddit_scraper.py --scrape &
python3 AUTOMATIONS/daily_research_orchestrator.py --full &
python3 AUTOMATIONS/competitor_monitor.py --scan &
python3 AUTOMATIONS/trend_scanner.py --full &
wait
python3 AUTOMATIONS/alpha_auto_processor.py --process-new
```

### Important Notes
- **Twitter scrapers use Brave browser cookies** — Brave must have an active Twitter/X login. Cookies are extracted from Brave's SQLite cookie DB automatically.
- **Twitter bookmarks scraper uses GraphQL API** — Query IDs rotate. If you get 404 "persisted query not found", update BOOKMARKS_QUERY_ID from `https://github.com/fa0311/TwitterInternalAPIDocument/blob/master/docs/json/API.json`
- **Reddit scrapers use JSON API** — No auth needed, reliable, works great.
- **All output goes to ALPHA_STAGING.csv** — Never create separate research files.

**Discovery engine** (`ralph/loops/mega/DISCOVERY_ENGINE.md`): 7 dimensions (geographic arb, demographic arb, new niches, new methods, sub-ops, social meta, emergent). Overnight outputs: 10-20 niches, 5-10 methods, 40+ arb opportunities.

**Account-niche pairing:** @PRINTMAXXER=tech, Faith=PrayerLock, Fitness=WalkToUnlock, Memes=engagement farming, AI adult=findom (separate brand). Tracked in `LEDGER/ACCOUNT_PORTFOLIO.csv`.

**Memecoin:** <5% allocation, $5-20/bet, track in `LEDGER/MEMECOIN_PORTFOLIO.csv`. Not core strategy.

---

