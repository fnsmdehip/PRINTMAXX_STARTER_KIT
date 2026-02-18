# PRINTMAXX System Wiring Diagram

Master interconnection map of all 5 perpetual loops. Every script, every CSV, every connection.
Updated: 2026-02-12

---

## System Overview

```
                    +========================+
                    |   PERPETUAL ENGINE     |
                    |  perpetual_ship_engine |
                    |  .sh (Layer 1/2/3)    |
                    +========================+
                              |
          +-------------------+-------------------+
          |         |         |         |         |
     LOOP 1    LOOP 2    LOOP 3    LOOP 4    LOOP 5
    RESEARCH   CONTENT   PRODUCT    LEADS      APPS
     ALPHA      POST      LIST     OUTREACH    BUILD
    INTEGRATE  MEASURE     SELL     CLOSE      DEPLOY
```

---

## LOOP 1: RESEARCH --> ALPHA --> INTEGRATION

The intelligence pipeline. Scrapes the internet, scores findings, routes actionable alpha into the right systems.

```
 +------------------+     +------------------+     +-------------------+
 | SCRAPER LAYER    |     | STAGING LAYER    |     | INTEGRATION       |
 |                  |     |                  |     |                   |
 | twitter_alpha_   | --> | LEDGER/          | --> | APP_CLONE_OPPS    |
 |   scraper.py     |     |  ALPHA_STAGING   |     | MARKETING_CHAN    |
 |                  |     |  .csv            |     | WINNING_CONTENT   |
 | background_      | --> | (PENDING_REVIEW) |     | MONEY_METHODS_    |
 |   reddit_        |     |                  |     |   TRACKER         |
 |   scraper.py     |     +--------+---------+     +-------------------+
 |                  |              |                        |
 | browser_scraper_ |     +--------v---------+     +-------v-----------+
 |   daily.py       |     | SCREENING LAYER  |     | EXECUTION         |
 |                  |     |                  |     |                   |
 | producthunt_     |     | alpha_screening  |     | paper_trade.py    |
 |   scraper.py     |     |   .py            |     | self_test.py      |
 |                  |     | (score 0-100)    |     | experiment_       |
 | platform_meta_   |     |                  |     |   runner.py       |
 |   monitor.py     |     | SCALE >=70       |     |                   |
 |                  |     | PAPER_TRADE 50-69|     | revenue_          |
 | niche_meta_      |     | KILL <50         |     |   projector.py    |
 |   detector.py    |     +------------------+     +-------------------+
 |                  |
 | competitor_      |
 |   price_monitor  |
 |   .py            |
 |                  |
 | viral_product_   |
 |   scanner.py     |
 |                  |
 | run_all_research |
 |   _ops.py        |
 +------------------+
```

### Scripts (Status)

| Script | Input | Output | Status | Cron |
|--------|-------|--------|--------|------|
| `twitter_alpha_scraper.py` | Brave cookies + HIGH_SIGNAL_SOURCES.csv | ALPHA_STAGING.csv, SCRAPED_TWEETS_ALPHA.csv | WORKS (needs Brave) | 6:00 AM daily |
| `background_reddit_scraper.py` | RESEARCH_SUBREDDITS.csv (41 subs) | reddit_scraper_output/*.json, ALPHA_STAGING.csv | WORKS | 6:15 AM daily |
| `browser_scraper_daily.py` | Chrome/Brave cookies | output/scraper/*.csv | WORKS | Part of overnight |
| `producthunt_scraper.py` | None | ALPHA_STAGING.csv | WORKS | Part of overnight |
| `platform_meta_monitor.py` | Platform APIs | PLATFORM_ALGO_CHANGES.csv, ALPHA_STAGING.csv | WORKS | 7:00 AM daily |
| `platform_algo_detection.py` | Platform signals | PLATFORM_ALGO_CHANGES.csv | WORKS | 7:00 AM daily |
| `niche_meta_detector.py` | ALPHA_STAGING.csv, trend data | NICHE_META_OPPORTUNITIES.csv | WORKS | Part of overnight |
| `competitor_price_monitor.py` | URL watchlist | Price change alerts | WORKS | Manual |
| `viral_product_scanner.py` | FB Ads Library | VIRAL_PRODUCTS_SCAN.csv | WORKS (needs requests+bs4) | 5:00 AM Monday |
| `alpha_screening.py` | ALPHA_STAGING.csv | Scored alpha (SCALE/PAPER_TRADE/KILL) | WORKS | Every 6 hours |
| `run_all_research_ops.py` | All research scripts | Consolidated log | WORKS | On-demand |
| `daily_nocost_rbi_scanner.py` | Project state on disk | RBI_AUDITS/NOCOST_DAILY_*.md | WORKS | 8:00 AM daily |

### Data Flow (Exact Files)

```
SCRAPERS
  twitter_alpha_scraper.py -----> LEDGER/ALPHA_STAGING.csv
  background_reddit_scraper.py -> LEDGER/ALPHA_STAGING.csv + reddit_scraper_output/
  browser_scraper_daily.py -----> output/scraper/reddit_hot_*.csv
  viral_product_scanner.py -----> LEDGER/VIRAL_PRODUCTS_SCAN.csv
  platform_meta_monitor.py -----> LEDGER/PLATFORM_ALGO_CHANGES.csv
  niche_meta_detector.py -------> LEDGER/NICHE_META_OPPORTUNITIES.csv
  competitor_price_monitor.py --> AUTOMATIONS/logs/ (alerts)

SCREENING
  alpha_screening.py -----------> Reads ALPHA_STAGING.csv, updates status column

INTEGRATION (after APPROVED)
  alpha -> APP_CLONE_OPPORTUNITIES.csv    (if APP_FACTORY)
  alpha -> MARKETING_CHANNELS_MASTER.csv  (if GROWTH_HACK/OUTBOUND)
  alpha -> WINNING_CONTENT_STRUCTURES.csv (if CONTENT_FORMAT)
  alpha -> CROSS_POLLINATION_MATRIX.csv   (synergy scoring)

EXECUTION
  paper_trade.py -----> LEDGER/PAPER_TRADES/, FINANCIALS/REVENUE_TRACKER.csv
  self_test.py -------> stdout (0-100 readiness scores)
  experiment_runner.py -> LEDGER/EXPERIMENTS_AB.csv
```

### Run Manually

```bash
# Full research sweep
python3 AUTOMATIONS/run_all_research_ops.py

# Twitter only (needs Brave open)
python3 AUTOMATIONS/twitter_alpha_scraper.py --all

# Reddit only
python3 AUTOMATIONS/background_reddit_scraper.py --full

# Screen pending alpha
python3 AUTOMATIONS/alpha_screening.py --pending

# RBI scanner
python3 AUTOMATIONS/daily_nocost_rbi_scanner.py --scan
```

### GAPS in Loop 1

| Gap | Impact | Fix |
|-----|--------|-----|
| No auto-integration after screening | Approved alpha sits in CSV, never routes to target files | **perpetual_improvement_runner.py** will fix |
| No dedup across scraper outputs | Same alpha could be added from reddit + twitter | Need dedup step before staging |
| platform_meta_monitor.py output not fed to content | Algorithm changes should trigger content updates | Wire to Loop 2 |

---

## LOOP 2: CONTENT --> POST --> MEASURE

The distribution pipeline. Generates content, formats for each platform, posts, measures results.

```
 +------------------+     +------------------+     +-------------------+
 | GENERATION       |     | FORMATTING       |     | POSTING           |
 |                  |     |                  |     |                   |
 | content_         | --> | generate_        | --> | content_posting/  |
 |   multiplier.py  |     |   buffer_csvs.py |     |  *.csv            |
 |                  |     |                  |     |  (Buffer/Publer)  |
 | engagement_      | --> | generate_30day_  |     |                   |
 |   bait_          |     |   calendar.py    |     | auto_list_        |
 |   converter.py   |     |                  |     |   products.py     |
 |                  |     | content_queue.py |     |   (Playwright)    |
 | self_reply_      |     |                  |     |                   |
 |   funnel.py      |     +--------+---------+     +-------+-----------+
 |                  |              |                        |
 | geo_content_     |     +--------v---------+     +-------v-----------+
 |   optimizer.py   |     | CALENDAR LAYER   |     | MEASUREMENT       |
 |                  |     |                  |     |                   |
 | micro_info_      |     | CONTENT_CALENDAR |     | CONTENT_          |
 |   product_       |     |   _30DAY.csv     |     |  PERFORMANCE_     |
 |   builder.py     |     |                  |     |  TRACKER.csv      |
 |                  |     | CONTENT_         |     |                   |
 | clip_automation_ |     |   PIPELINE.csv   |     | ENGAGEMENT_       |
 |   pipeline.py    |     |                  |     |  METRICS_DAILY    |
 |                  |     | buffer_import_   |     |  .csv             |
 | platform_posting |     |   *.csv (12)     |     |                   |
 |   _optimizer.py  |     +------------------+     +-------------------+
 +------------------+
```

### Scripts (Status)

| Script | Input | Output | Status | Cron |
|--------|-------|--------|--------|------|
| `content_multiplier.py` | Any content (text/file) | 20+ variants across 9 formats | WORKS | On-demand |
| `generate_buffer_csvs.py` | CONTENT_CALENDAR_30DAY.csv | 12 buffer_import_*.csv files | WORKS | On-demand |
| `generate_30day_calendar.py` | Content templates + niche data | CONTENT_CALENDAR_30DAY.csv | WORKS | Monthly |
| `content_queue.py` | Content files in CONTENT/ | CONTENT_PIPELINE.csv updates | WORKS | On-demand |
| `engagement_bait_converter.py` | ALPHA_STAGING (ENGAGEMENT_BAIT) | Niche-adapted posts | WORKS | On-demand |
| `self_reply_funnel.py` | Tweet content | Thread with CTA funnel | WORKS | On-demand |
| `geo_content_optimizer.py` | Content + location data | GEO-optimized variants | WORKS | On-demand |
| `clip_automation_pipeline.py` | Video URL | Clips ready for posting | WORKS (needs yt-dlp, ffmpeg) | On-demand |
| `platform_posting_optimizer.py` | Content + platform rules | Optimized per-platform content | WORKS | On-demand |

### Data Flow (Exact Files)

```
GENERATION
  content_multiplier.py -------> AUTOMATIONS/content_posting/multiplied/
  engagement_bait_converter.py -> AUTOMATIONS/content_posting/
  self_reply_funnel.py ---------> AUTOMATIONS/content_posting/
  clip_automation_pipeline.py --> output/clips/

FORMATTING
  generate_buffer_csvs.py ------> LEDGER/buffer_import_*.csv (12 files)
  generate_30day_calendar.py ---> LEDGER/CONTENT_CALENDAR_30DAY.csv
  content_queue.py -------------> LEDGER/CONTENT_PIPELINE.csv

READY TO POST (already exists)
  content_posting/printmaxxer_tweets_50.csv
  content_posting/findom_tweets_50.csv
  content_posting/meme_engagement_tweets_30.csv
  content_posting/ecom_arb_content_30.csv
  content_posting/gov_contract_tweets_50.csv
  content_posting/cold_email_sequences_ready.csv
  content_posting/MASTER_CONTENT_BATCH_FEB12.csv

MEASUREMENT
  (reads) CONTENT_PERFORMANCE_TRACKER.csv -> method_performance_analyzer.py
  (reads) ENGAGEMENT_METRICS_DAILY.csv -> revenue_projector.py
```

### Run Manually

```bash
# Multiply one piece of content to 20+ variants
python3 AUTOMATIONS/content_multiplier.py --file /path/to/content.md

# Generate 30-day calendar
python3 scripts/generate_30day_calendar.py

# Generate Buffer-ready CSVs
python3 scripts/generate_buffer_csvs.py

# Convert engagement bait alpha to real posts
python3 AUTOMATIONS/engagement_bait_converter.py
```

### GAPS in Loop 2

| Gap | Impact | Fix |
|-----|--------|-----|
| No auto-posting to platforms | CSVs exist but manual upload to Buffer needed | Need account creation (human) then auto-upload |
| CONTENT_PERFORMANCE_TRACKER empty | No measurement happening, no feedback to optimize | Wire analytics API after accounts created |
| content_multiplier output not auto-staged | Generated content sits in multiplied/ folder | Auto-route to content_posting/ CSVs |
| No feedback from performance to generation | Good/bad content not informing next batch | Wire performance -> content_multiplier preferences |

---

## LOOP 3: PRODUCT --> LIST --> SELL --> TRACK

The commerce pipeline. Takes product specs, distributes to marketplaces, tracks revenue.

```
 +------------------+     +------------------+     +-------------------+
 | PRODUCT SPECS    |     | DISTRIBUTION     |     | TRACKING          |
 |                  |     |                  |     |                   |
 | PRODUCTS/        | --> | ecom_            | --> | FINANCIALS/       |
 |  GUMROAD_READY   |     |   distributor.py |     |  REVENUE_TRACKER  |
 |  _LISTINGS.md    |     |                  |     |  .csv             |
 |                  |     | auto_list_       |     |                   |
 | PRODUCTS/        | --> |   products.py    |     | LEDGER/           |
 |  ETSY_LISTINGS   |     |  (Playwright)    |     |  REVENUE_STREAMS  |
 |  _20.md          |     |                  |     |  _TRACKER.csv     |
 |                  |     +--------+---------+     |                   |
 | PRODUCTS/        |              |               | LEDGER/           |
 |  REDBUBBLE_      |     +--------v---------+     |  PRODUCTS.csv     |
 |  LISTINGS.md     |     | MARKETPLACES     |     |                   |
 |                  |     |                  |     | scripts/          |
 | DIGITAL_         |     | Gumroad          |     |  revenue_intake   |
 |  PRODUCTS/       |     | Etsy             |     |  .py              |
 |  listings/       |     | Redbubble        |     |                   |
 |  micro_products/ |     | Fiverr           |     | FINANCIALS/       |
 |  pdfs/           |     | Whop             |     |  P_AND_L_MONTHLY  |
 |                  |     | Creative Market  |     |  .csv             |
 | MONEY_METHODS/   |     | KDP              |     +-------------------+
 |  POD_TIKTOK_*    |     | Lemon Squeezy    |
 +------------------+     +------------------+
```

### Scripts (Status)

| Script | Input | Output | Status |
|--------|-------|--------|--------|
| `ecom_distributor.py` | Product specs (PRODUCTS/, DIGITAL_PRODUCTS/) | Platform-ready listing data, upload CSVs | WORKS |
| `auto_list_products.py` | Ready listings markdown | Playwright-driven marketplace listing | WORKS (needs Playwright + accounts) |
| `micro_info_product_builder.py` | Niche + topic | Complete micro product specs | WORKS |
| `scripts/revenue_intake.py` | Manual input | FINANCIALS/REVENUE_TRACKER.csv | WORKS |

### Data Flow (Exact Files)

```
PRODUCTS READY TO LIST
  PRODUCTS/GUMROAD_READY_LISTINGS.md ----> 10 products, copy-paste ready
  PRODUCTS/ETSY_LISTINGS_20.md ----------> 20 Etsy listings
  PRODUCTS/REDBUBBLE_LISTINGS.md --------> Redbubble designs
  PRODUCTS/POD_DESIGNS_50.md ------------> 50 POD designs
  PRODUCTS/KDP_JOURNALS_10.md -----------> 10 KDP journals
  DIGITAL_PRODUCTS/listings/ ------------> Gumroad products 2-4
  DIGITAL_PRODUCTS/micro_products/ ------> Micro info products
  DIGITAL_PRODUCTS/pdfs/ ----------------> PDF products

DISTRIBUTION
  ecom_distributor.py --distribute-all --> output/ecom_distribution/
  auto_list_products.py --platform X ----> Live marketplace listings

REVENUE TRACKING
  scripts/revenue_intake.py log ---------> FINANCIALS/REVENUE_TRACKER.csv
  (auto) --------------------------------> LEDGER/REVENUE_STREAMS_TRACKER.csv
  (auto) --------------------------------> FINANCIALS/P_AND_L_MONTHLY.csv
```

### Run Manually

```bash
# List ready products
python3 AUTOMATIONS/ecom_distributor.py --list

# Distribute all products to all platforms
python3 AUTOMATIONS/ecom_distributor.py --distribute-all

# Auto-list on Gumroad (needs Playwright + login)
python3 AUTOMATIONS/auto_list_products.py --platform gumroad

# Log revenue
python3 scripts/revenue_intake.py log --method MM002 --amount 47 --source gumroad
```

### GAPS in Loop 3

| Gap | Impact | Fix |
|-----|--------|-----|
| No marketplace accounts created | Cannot list anything | HUMAN: Create Gumroad, Etsy, Redbubble, Fiverr, Whop accounts |
| auto_list_products needs Playwright login | Can generate CSVs but not auto-post | Needs account cookies or manual first login |
| No auto-revenue detection | Revenue only logged when human runs revenue_intake.py | Wire platform APIs (Gumroad webhooks, Stripe) after accounts |
| ecom_distributor output not auto-uploaded | Distribution CSVs generated but not pushed to platforms | Chain with auto_list_products.py |

---

## LOOP 4: LEAD --> SCORE --> OUTREACH --> CLOSE

The B2B pipeline. Scrapes business leads, scores them, sends cold emails, tracks pipeline.

```
 +------------------+     +------------------+     +-------------------+
 | LEAD SCRAPING    |     | SCORING          |     | OUTREACH          |
 |                  |     |                  |     |                   |
 | savvy_lead_      | --> | 0-100 website    | --> | mass_outreach.py  |
 |   scraper.py     |     |   quality score  |     | (10 templates,    |
 |  (per city)      |     |   (LOW = HOT)    |     |  3-email sequence)|
 |                  |     |                  |     |                   |
 | nationwide_      | --> | AUTOMATIONS/     |     | AUTOMATIONS/      |
 |   scraper.py     |     |   leads/*.csv    |     |   outreach/*.csv  |
 |  (200+ cities)   |     |                  |     |  (Instantly fmt)  |
 |                  |     +--------+---------+     +-------+-----------+
 | local_biz_       |              |                       |
 |   pipeline.py    |     +--------v---------+     +-------v-----------+
 |  (full chain)    |     | LEAD DATABASE    |     | PIPELINE TRACKING |
 |                  |     |                  |     |                   |
 | hexomatic_       |     | leads/MASTER_    |     | LEDGER/           |
 |   lead_gen.py    |     |   LEADS.csv      |     |  OUTREACH_        |
 |                  |     |                  |     |  PIPELINE.csv     |
 | g2_reviewer_     |     | leads/dental_    |     |                   |
 |   scraper.py     |     |   *_leads.csv    |     | outreach/         |
 |                  |     |                  |     |  PIPELINE_TRACKER  |
 | indeed_hiring_   |     | leads/lawyer_    |     |  .csv             |
 |   monitor.py     |     |   *_leads.csv    |     |                   |
 |                  |     | LEDGER/          |     | FINANCIALS/       |
 | linkedin_events_ |     |  ECOM_LEADS.csv  |     |  REVENUE_TRACKER  |
 |   scraper.py     |     +------------------+     +-------------------+
 +------------------+
```

### Scripts (Status)

| Script | Input | Output | Status |
|--------|-------|--------|--------|
| `savvy_lead_scraper.py` | City + industry | leads/[industry]_[city]_leads.csv (scored 0-100) | WORKS (needs requests+bs4) |
| `nationwide_scraper.py` | cities_top200.csv + industries | leads/MASTER_LEADS.csv | WORKS |
| `mass_outreach.py` | leads CSV + template | outreach/*_emails.csv (Instantly format) | WORKS |
| `local_biz_pipeline.py` | City + category or URL file | Full pipeline: scrape -> score -> generate -> outreach | WORKS (needs requests+bs4) |
| `hexomatic_lead_gen.py` | Keywords | ECOM_LEADS.csv | WORKS |
| `g2_reviewer_scraper.py` | G2 product URLs | g2_reviewer_leads.csv | WORKS |
| `indeed_hiring_monitor.py` | Job keywords | indeed_hiring_leads.csv | WORKS |
| `linkedin_events_scraper.py` | LinkedIn event URLs | Attendee data | WORKS (needs login) |
| `run_lead_gen.sh` | None (runs savvy scraper across 10 cities x 5 industries) | 50 CSV files | WORKS |

### Data Flow (Exact Files)

```
SCRAPING
  savvy_lead_scraper.py ------> AUTOMATIONS/leads/[industry]_[city]_leads.csv
  nationwide_scraper.py -------> AUTOMATIONS/leads/MASTER_LEADS.csv
  local_biz_pipeline.py -------> AUTOMATIONS/leads/ + outreach emails
  g2_reviewer_scraper.py ------> AUTOMATIONS/leads/g2_reviewer_leads.csv
  indeed_hiring_monitor.py ----> AUTOMATIONS/leads/indeed_hiring_leads.csv

OUTREACH
  mass_outreach.py ------------> AUTOMATIONS/outreach/*_emails.csv
  (format: Instantly-compatible CSV with 3-email sequences)

PIPELINE TRACKING
  outreach/PIPELINE_TRACKER.csv
  LEDGER/OUTREACH_PIPELINE.csv
  LEDGER/FREELANCE_PIPELINE.csv

EXISTING LEADS (already scraped)
  leads/dental_austin_tx_leads.csv
  leads/dentist_[10 cities]_leads.csv
  leads/lawyer_[5 cities]_leads.csv
  leads/gov_tenders_active.csv
  leads/indeed_hiring_leads.csv
  leads/g2_reviewer_leads.csv
```

### Run Manually

```bash
# Scrape leads for one city
python3 AUTOMATIONS/savvy_lead_scraper.py --category dental --city "Austin TX" --limit 50

# Scrape nationwide (10 cities)
python3 AUTOMATIONS/nationwide_scraper.py --categories "dental,plumber,lawyer" --max-cities 10

# Generate outreach emails from leads
python3 AUTOMATIONS/mass_outreach.py --input AUTOMATIONS/leads/dental_austin_tx_leads.csv --template dental

# Full pipeline (scrape + score + generate pages + outreach)
python3 AUTOMATIONS/local_biz_pipeline.py --category dentist --city "Austin TX"

# Run 10 cities x 5 industries
bash AUTOMATIONS/run_lead_gen.sh
```

### GAPS in Loop 4

| Gap | Impact | Fix |
|-----|--------|-----|
| No email sending infrastructure | Outreach CSVs exist but no way to send | HUMAN: Set up Instantly.ai or cold email tool |
| No response tracking automation | Replies tracked manually | Wire Instantly API for auto-tracking |
| No auto-follow-up | 3-email sequences written but not auto-triggered | Needs email tool with drip capability |
| Pipeline tracker not auto-updated | PIPELINE_TRACKER.csv needs manual updates | Wire email tool responses to tracker |
| lead_gen.sh not on cron | Leads scraped manually only | Add to weekly cron (Monday) |

---

## LOOP 5: APP --> BUILD --> DEPLOY --> ASO --> MEASURE

The app factory pipeline. Build apps, deploy to web/stores, optimize discovery, measure results.

```
 +------------------+     +------------------+     +-------------------+
 | APP SPECS        |     | BUILD/DEPLOY     |     | OPTIMIZATION      |
 |                  |     |                  |     |                   |
 | APP_FACTORY/     | --> | ralph/loops/     | --> | aso_keyword_      |
 |   builds/        |     |   app_factory/   |     |   research.py     |
 |                  |     |   output/        |     |                   |
 | APP_CLONE_       |     | (6 PWAs ready)   |     | LEDGER/           |
 |   OPPORTUNITIES  |     |                  |     |   ASO_KEYWORDS    |
 |   .csv           |     | deploy_all_      |     |   .csv            |
 |                  |     |   apps.sh        |     |                   |
 | app_clone_       |     |                  |     | app_security_     |
 |   finder.py      |     | builds/          |     |   audit.py        |
 |                  |     |   programmatic_  |     |                   |
 | APP_QUALITY_     |     |   seo/           |     | APP_FACTORY_      |
 |   STANDARDS.md   |     |   (600 pages)    |     |   METHODS.csv     |
 +------------------+     +--------+---------+     +-------------------+
                                   |
                          +--------v---------+
                          | LIVE APPS        |
                          |                  |
                          | ramadan-tracker  |
                          | focuslock-web    |
                          | habitforge-web   |
                          | mealmaxx-web     |
                          | sleepmaxx-web    |
                          | walktounlock-web |
                          | programmatic_seo |
                          |   (600 pages)    |
                          +------------------+
```

### Scripts (Status)

| Script | Input | Output | Status |
|--------|-------|--------|--------|
| `app_clone_finder.py` | App Store categories | APP_CLONE_OPPORTUNITIES.csv | WORKS |
| `aso_keyword_research.py` | App category + niche | ASO_KEYWORDS.csv | WORKS |
| `app_security_audit.py` | App source code | Security findings | WORKS |
| `deploy_all_apps.sh` | App builds in output/ | Live deployments | NEEDS vercel login |
| `scripts/programmatic_seo.py` | City + service data | 600 HTML pages + sitemap | WORKS |

### Data Flow (Exact Files)

```
APP SPECS
  MONEY_METHODS/APP_FACTORY/ (quality standards, naming, design system)
  LEDGER/APP_CLONE_OPPORTUNITIES.csv (66+ clone targets)
  APP_FACTORY_GTM_MASTER.md (launch strategy)

BUILT APPS (ready to deploy)
  ralph/loops/app_factory/output/ramadan-tracker/
  ralph/loops/app_factory/output/focuslock-web/
  ralph/loops/app_factory/output/habitforge-web/
  ralph/loops/app_factory/output/mealmaxx-web/
  ralph/loops/app_factory/output/sleepmaxx-web/
  ralph/loops/app_factory/output/walktounlock-web/
  builds/programmatic_seo/ (600 HTML pages)

ASO/OPTIMIZATION
  aso_keyword_research.py -> LEDGER/ASO_KEYWORDS.csv
  app_security_audit.py -> stdout (audit results)

DEPLOYMENT
  deploy_all_apps.sh (Vercel/Surge/Cloudflare Pages)
```

### Run Manually

```bash
# Deploy all 6 apps
bash AUTOMATIONS/deploy_all_apps.sh

# Deploy programmatic SEO
cd builds/programmatic_seo && npx wrangler pages deploy .

# Run ASO keyword research
python3 AUTOMATIONS/aso_keyword_research.py

# Find clone opportunities
python3 AUTOMATIONS/app_clone_finder.py
```

### GAPS in Loop 5

| Gap | Impact | Fix |
|-----|--------|-----|
| No vercel/deployment login | 6 apps + 600 SEO pages cannot go live | HUMAN: `vercel login` or deploy to Surge/Cloudflare |
| No App Store submission pipeline | PWAs deployed but no iOS/Android native | Need Apple Dev account + Xcode build |
| No analytics wired | Deployed apps have no tracking | Add Plausible/PostHog after deployment |
| No revenue tracking from apps | App monetization (ads, subs) not tracked | Wire RevenueCat + ad network dashboards |
| ASO not feeding back to app updates | Keyword research not informing metadata | Auto-update app descriptions from ASO data |

---

## CROSS-LOOP CONNECTIONS (The Multiplier Effect)

These connections create compound growth across loops.

```
LOOP 1 (Research) ---> LOOP 2 (Content)
  ENGAGEMENT_BAIT alpha -> engagement_bait_converter.py -> content_posting/
  Trend detection -> content_multiplier.py -> topical content

LOOP 1 (Research) ---> LOOP 3 (Product)
  VIRAL_PRODUCTS_SCAN.csv -> ecom product selection
  NEW_OP_DISCOVERIES -> micro_info_product_builder.py -> new products

LOOP 1 (Research) ---> LOOP 4 (Leads)
  Industry trend alpha -> cold email hooks for outreach templates
  Competitor intel -> local_biz_pipeline.py landing page customization

LOOP 1 (Research) ---> LOOP 5 (Apps)
  APP_CLONE_OPPORTUNITIES.csv -> next app to build
  ASO_KEYWORDS.csv -> app metadata optimization

LOOP 2 (Content) ---> LOOP 3 (Product)
  Content performance -> product ideas (what resonates)
  CONTENT_TO_REVENUE_MAP.csv connects content to conversions

LOOP 2 (Content) ---> LOOP 4 (Leads)
  Social proof content -> cold email attachment / links
  Authority posts -> warm leads from DMs

LOOP 3 (Product) ---> LOOP 2 (Content)
  New product launch -> content_multiplier.py -> launch posts
  Product sales data -> case study content

LOOP 4 (Leads) ---> LOOP 3 (Product)
  Client feedback -> new product ideas
  Service delivery -> productized service -> info product

LOOP 5 (Apps) ---> LOOP 2 (Content)
  App launches -> "How I built" content threads
  App metrics -> build-in-public content

LOOP 5 (Apps) ---> LOOP 3 (Product)
  App users -> product upsells (affiliate, info products)
  App data -> content and product insights
```

---

## ORCHESTRATION LAYER

### Existing Cron (16 entries in crontab_printmaxx.txt)

| Time | Script | Loop |
|------|--------|------|
| 2:00 AM daily | overnight_master_runner.sh | L1 (Research) |
| 6:00 AM daily | daily_twitter_scraper.py | L1 (Research) |
| 6:15 AM daily | daily_reddit_scraper.py | L1 (Research) |
| 7:00 AM daily | platform_algo_detection.py | L1 (Research) |
| 7:15 AM daily | hashtag_audio_tracking.py | L1 (Research) |
| 8:00 AM daily | daily_nocost_rbi_scanner.py | ALL (Audit) |
| Every 30 min 0-8 AM | auto_resume_monitor.sh | ALL (Safety) |
| 3:00 AM Monday | platform_rpm_tracking.py | L1 (Research) |
| 3:30 AM Monday | creator_program_monitoring.py | L1 (Research) |
| 4:00 AM Monday | aso_keyword_research.py | L5 (Apps) |
| 4:30 AM Monday | gov_tenders_scraper.py | L4 (Leads) |
| 5:00 AM Monday | ecom_arb_scanner.py | L3 (Product) |
| 5:15 AM Monday | trending_products_scanner.py | L3 (Product) |
| Every 6 hours | sam_gov_monitor.py | L4 (Leads) |
| Every 6 hours | alpha_screening.py --pending | L1 (Research) |

### MISSING Cron Entries (Should Be Added)

| Time | Script | Loop | Why |
|------|--------|------|-----|
| 8:30 AM daily | daily_todo_generator.py | ALL | Prioritized daily task list |
| 9:00 AM daily | method_performance_analyzer.py | ALL | Track what's working |
| Monday 6:00 AM | run_lead_gen.sh | L4 | Weekly lead refresh |
| Monthly 1st | revenue_projector.py --report | ALL | Monthly revenue projection |
| 6:00 PM daily | perpetual_improvement_runner.py | ALL | Cross-loop integration |

---

## MASTER STATUS: What Works vs What's Blocked

### FULLY AUTONOMOUS (no human needed)

| System | Scripts | Cron | Notes |
|--------|---------|------|-------|
| Reddit scraping | background_reddit_scraper.py | 6:15 AM | Runs via public JSON API |
| Alpha screening | alpha_screening.py | Every 6h | Pure Python scoring |
| RBI scanning | daily_nocost_rbi_scanner.py | 8:00 AM | Reads project state |
| Platform monitoring | platform_algo_detection.py | 7:00 AM | Public API checks |
| Lead scraping | savvy_lead_scraper.py | Manual | DuckDuckGo + website analysis |
| Outreach generation | mass_outreach.py | Manual | Template-based, no AI |
| Content multiplication | content_multiplier.py | Manual | Format conversion |
| Product distribution | ecom_distributor.py | Manual | Generates listing data |
| TODO generation | daily_todo_generator.py | 8:30 AM | Scans all systems |

### BLOCKED BY HUMAN ACTION

| System | Blocker | Impact | Action Required |
|--------|---------|--------|-----------------|
| App deployment | No vercel login | 6 apps + 600 pages offline | `vercel login` |
| Product listing | No marketplace accounts | 100+ products can't list | Create Gumroad/Etsy/Redbubble |
| Email outreach | No email tool setup | 1,661 leads no outreach | Set up Instantly.ai |
| Content posting | No social accounts | 1,278+ posts queued | Create accounts per checklist |
| Twitter scraping | Needs Brave open | No Twitter alpha | Open Brave, stay logged in |
| Revenue tracking | No platform webhooks | No auto-revenue detection | After accounts: wire APIs |
| Analytics | No tracking installed | No performance data | Add Plausible after deploy |

---

## RECOMMENDED CRON SCHEDULE (Complete)

```bash
# === PRINTMAXX PERPETUAL CRON ===
# Layer 1: Research (2-8 AM)
0 2 * * *   cd $BASE && bash AUTOMATIONS/overnight_master_runner.sh
0 6 * * *   cd $BASE && $PYTHON AUTOMATIONS/daily_twitter_scraper.py
15 6 * * *  cd $BASE && $PYTHON AUTOMATIONS/background_reddit_scraper.py --full
0 7 * * *   cd $BASE && $PYTHON AUTOMATIONS/platform_algo_detection.py
15 7 * * *  cd $BASE && $PYTHON AUTOMATIONS/hashtag_audio_tracking.py
0 8 * * *   cd $BASE && $PYTHON AUTOMATIONS/daily_nocost_rbi_scanner.py --scan
30 8 * * *  cd $BASE && $PYTHON AUTOMATIONS/daily_todo_generator.py

# Layer 2: Screening + Integration (every 6h)
0 */6 * * * cd $BASE && $PYTHON AUTOMATIONS/alpha_screening.py --pending
30 */6 * * * cd $BASE && $PYTHON AUTOMATIONS/sam_gov_monitor.py

# Layer 3: Performance + Integration (daily PM)
0 18 * * *  cd $BASE && $PYTHON AUTOMATIONS/perpetual_improvement_runner.py
0 21 * * *  cd $BASE && $PYTHON AUTOMATIONS/method_performance_analyzer.py

# Layer 4: Weekly deep work (Monday)
0 3 * * 1   cd $BASE && $PYTHON AUTOMATIONS/platform_rpm_tracking.py
30 3 * * 1  cd $BASE && $PYTHON AUTOMATIONS/creator_program_monitoring.py
0 4 * * 1   cd $BASE && $PYTHON AUTOMATIONS/aso_keyword_research.py
30 4 * * 1  cd $BASE && $PYTHON AUTOMATIONS/gov_tenders_scraper.py --all-sources
0 5 * * 1   cd $BASE && bash AUTOMATIONS/run_lead_gen.sh
15 5 * * 1  cd $BASE && $PYTHON AUTOMATIONS/trending_products_scanner.py

# Layer 5: Monthly
0 3 1 * *   cd $BASE && $PYTHON AUTOMATIONS/revenue_projector.py --report
0 4 1 * *   cd $BASE && $PYTHON scripts/self_test.py --json

# Safety
*/30 0-8 * * * cd $BASE && bash AUTOMATIONS/auto_resume_monitor.sh
```
