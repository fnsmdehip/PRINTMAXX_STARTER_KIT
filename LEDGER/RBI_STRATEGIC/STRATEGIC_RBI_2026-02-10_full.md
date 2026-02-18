# PRINTMAXX STRATEGIC RBI ENGINE — 2026-02-10
# Mode: FULL
# ========================================================

============================================================
  LAYER 2: DEEP ANALYSIS
============================================================


--- PERFORMANCE vs CLAIMS ANALYSIS ---

Active methods: 6
Planning methods: 44
Total methods: 69
Methods with ANY revenue: 0
⚠️ CRITICAL: Methods marked ACTIVE but ZERO revenue tracked!
   → Either tracking is broken or methods arent actually active.
   → ACTION: Verify each "active" method is genuinely producing revenue.
  MM001 (APP_FACTORY): claimed=, actual=$0.00
  MM006 (CONTENT_FARM): claimed=, actual=$0.00
  MM009 (AI_INFLUENCER): claimed=, actual=$0.00
  MM019 (PORTFOLIO_APP_BUILDER): claimed=, actual=$0.00
  MM021 (PERSONAL_BRAND_SEO): claimed=, actual=$0.00
  MM070 (WEB_REDESIGN_COLD_OUTREACH): claimed=, actual=$0.00

--- BOTTLENECK ANALYSIS ---

[CRITICAL] Alpha Pipeline
  Issue: 85 alpha entries stuck in PENDING_REVIEW
  Impact: New tactics and opportunities not being implemented
  Fix: Schedule 30-min daily review. Process 10-20 entries per session. Ruthlessly reject low-quality.
  Automate: Build auto-scorer that pre-ranks alpha by: recency, ROI tag, category match to active ops

[CRITICAL] Experimentation
  Issue: 42 A/B tests DESIGNED but ZERO running
  Impact: No learning happening. Flying blind on what works. Optimizing nothing.
  Fix: Launch 3 tests THIS WEEK: 1 pricing test, 1 content format test, 1 CTA test.
  Automate: Build experiment runner that auto-tracks metrics and signals statistical significance

[CRITICAL] Revenue Tracking
  Issue: Only 0 revenue entries. Cannot optimize what you dont measure.
  Impact: No idea which ops actually make money. All decisions are guesses.
  Fix: Track EVERY dollar: source, method, amount, date, channel. Even $1 matters.
  Automate: Build revenue intake form or script that logs from multiple sources

[HIGH] Freelance Pipeline
  Issue: Freelance pipeline is EMPTY. Zero gigs tracked.
  Impact: Freelance arbitrage (S01) is listed as active but has zero activity.
  Fix: Create Fiverr + Upwork listings TODAY. Start with top 5 services from FREELANCE_ARB.xlsx.
  Automate: Set up listing templates and auto-response scripts for common gig types


--- OPS VIABILITY SCORING ---

OPS VIABILITY MATRIX (based on real market data, not projections):

OP TYPE                SUCCESS%   TIME→$1K       AUTO%    SATURATION   REAL RANGE              
------------------------------------------------------------------------------------------
nsfw_ai_persona           30%     1-2 months       50%   GROWING      $500-25K/mo
findom                    30%     2-4 weeks        40%   LOW          $500-30K/mo
local_biz_service         25%     2-4 weeks        60%   LOW          $2-15K/mo
ai_ugc                    20%     2-3 months       70%   MEDIUM       $1.2-10K/mo
cold_email                20%     1-2 months       50%   MEDIUM       $2-8K/mo
digital_products          15%     1-3 months       90%   MEDIUM       $100-10K/mo
faceless_youtube          10%     3-4 months       80%   HIGH         $500-20K/mo for top 10%
freelance_arbitrage       10%     4-6 weeks        40%   GROWING      $1-8K/mo
seo_affiliate             10%     3-6 months       70%   HIGH         $200-5K/mo
newsletter                 8%     6-12 months      50%   MEDIUM       $200-5K/mo
tiktok_content             5%     2-3 months       70%   HIGH         $0-5K/mo for most
micro_saas                 5%     2-3 months MRR   60%   LOW-MED      $0-5K/mo for 95%
app_factory                5%     3-6 months       60%   HIGH         $0-5K/mo for 95%

KEY INSIGHT: Success rate × automation level = true viability score.
  Top picks by viability:
  1. AI NSFW/Findom (30% × 0.4 = best risk-reward, lowest saturation)
  2. Local biz service (25% × 0.6 = fastest to revenue, low saturation)
  3. Cold email lead gen (20% × 0.5 = proven model, medium saturation)
  4. Digital products (15% × 0.9 = highest automation, medium saturation)
  5. AI UGC (20% × 0.7 = growing market but commoditizing)

AVOID (low viability): Generic micro-SaaS (5%), app factory (5%), TikTok creator fund (5%)
  These have high failure rates AND high saturation. Only pursue with strong differentiation.

--- DEAD ZONE DETECTION ---

  [DEAD] 03_PLAYBOOKS: 2/21915 files modified in last 7 days (0.0%)

--- METHOD SYNERGY ANALYSIS ---

  Total synergy pairs: 308
  High synergy (>2x): 0

  MOST SYNERGISTIC METHODS (appear in most high-synergy pairs):

  → These are your "hub" methods. Activating them multiplies everything else.

============================================================
  LAYER 4: VALIDATION
============================================================


--- INFRASTRUCTURE VALIDATION ---


  [S01 - Freelance Arbitrage]
    File PRINTMAXX_FREELANCE_ARB.xlsx: ✓ EXISTS
    Account on Fiverr: ✗ NOT CREATED
      → ACTION: Create Fiverr account. Add to ACCOUNTS.csv.
    Account on Upwork: ✗ NOT CREATED
      → ACTION: Create Upwork account. Add to ACCOUNTS.csv.
    → STATUS: ✗ BLOCKED - Missing prerequisites above

  [S02 - Local Biz Pipeline]
    File AUTOMATIONS/local_biz_pipeline.py: ✓ EXISTS
    File AUTOMATIONS/bulk_landing_page_generator.py: ✓ EXISTS
    → STATUS: ✓ INFRASTRUCTURE READY

  [P02 - AI NSFW Findom]
    File MONEY_METHODS/AI_INFLUENCER/AI_NSFW_FINDOM_EXECUTION_PLAN.md: ✓ EXISTS
    Account on Fanvue: ✗ NOT CREATED
      → ACTION: Create Fanvue account. Add to ACCOUNTS.csv.
    Account on Fansly: ✗ NOT CREATED
      → ACTION: Create Fansly account. Add to ACCOUNTS.csv.
    → STATUS: ✗ BLOCKED - Missing prerequisites above

  [D01 - Gumroad Products]
    File DIGITAL_PRODUCTS/: ✓ EXISTS
    Account on Gumroad: ✗ NOT CREATED
      → ACTION: Create Gumroad account. Add to ACCOUNTS.csv.
    → STATUS: ✗ BLOCKED - Missing prerequisites above

  [C01 - TikTok Content Farm]
    File MONEY_METHODS/CONTENT_FARM/: ✓ EXISTS
    Account on TikTok: ✗ NOT CREATED
      → ACTION: Create TikTok account. Add to ACCOUNTS.csv.
    → STATUS: ✗ BLOCKED - Missing prerequisites above

  [G02 - RBI System]
    File scripts/rbi_audit.py: ✓ EXISTS
    File scripts/strategic_rbi_engine.py: ✓ EXISTS
    → STATUS: ✓ INFRASTRUCTURE READY

--- AUTOMATION HEALTH CHECK ---

  Total automation scripts: 49
  ⚠️ DEPRECATED scripts still present: 1
    → backtest_alpha_DEPRECATED.py — DELETE or ARCHIVE

  Scripts requiring browser automation (11):
    background_twitter_scraper.py: needs playwright
    scrape_caiden_playwright.py: needs playwright
    scrape_twitter_selenium.py: needs selenium, selenium, selenium, selenium, selenium, selenium
    headless_twitter_scraper.py: needs playwright
    twitter_content_scraper.py: needs playwright
    twitter_scraper_live.py: needs playwright
    viral_content_scanner.py: needs playwright
    parallel_background_scraper.py: needs playwright
    scrape_caiden_cdp.py: needs playwright
    twitter_alpha_scraper.py: needs playwright
    enhanced_reddit_scraper.py: needs playwright
  → These need a browser environment (not available in all contexts)

  Automation runs today: 0
  Errors today: 0

--- REVENUE CLAIM VALIDATION ---

REVENUE REALITY CHECK (based on market research):

  tiktok_creator_fund:
    Realistic range: $0-$5000/mo
    Note: New Creator Rewards: $0.40-1/1K views. Need 500K+ views/mo for real money

  youtube_adsense:
    Realistic range: $500-$20000/mo
    Note: RPM $3-20. Need 100K+ views/mo. Top 10% only.

  fiverr_services:
    Realistic range: $100-$8000/mo
    Note: 20% platform fee. First sale takes 2-4 weeks avg.

  fanvue_ai:
    Realistic range: $500-$25000/mo
    Note: Top AI creator: $50K/mo. Most: $500-3K after 3-6mo. 15-20% platform fee.

  cold_email_agency:
    Realistic range: $1000-$10000/mo
    Note: 3.4% avg reply rate. Need 500+ sends for meaningful results.

  micro_saas:
    Realistic range: $0-$5000/mo
    Note: 92% fail within 3 years. Median profitable: $4.2K MRR.

  gumroad_products:
    Realistic range: $50-$5000/mo
    Note: 10% platform fee. Need existing audience for sales.

  local_biz_websites:
    Realistic range: $500-$15000/mo
    Note: $500-5K per site. Cold email: 3-5% reply rate.

KEY TAKEAWAY: Nobody makes real money in <3-4 weeks despite what sales pages say.
80% automation + 20% human judgment = best results for any op.

============================================================
  LAYER 5: IMPROVEMENT ENGINE
============================================================


--- HYPOTHESIS GENERATION ---

Generated 8 testable hypotheses:

  [H001] Animated paywalls convert 2.9x better than static paywalls
    Test: Deploy animated paywall on PrayerLock/Scripture Streak. Measure conversion vs current.
    Metric: paywall_conversion_rate | Target: 2.9x improvement
    Effort: LOW (2-3 hours) | Status: NOT STARTED
    Source: LEDGER/AB_TESTS_MASTER.csv + paywall optimization playbook

  [H002] Findom content on X/Twitter with #findom #paypig hashtags converts 5x better than general adult hashtags
    Test: Post 20 findom tweets with niche hashtags vs 20 with general hashtags. Track link clicks and conversions.
    Metric: clicks_per_impression | Target: 5x CTR improvement
    Effort: LOW (1-2 hours) | Status: NOT STARTED
    Source: findom_tweets_50.csv

  [H003] Cold emails with timeline-based hooks get 10% reply rate vs 4.4% for problem-statement hooks
    Test: Split test 200 cold emails: 100 with timeline hook, 100 with problem hook. Track replies.
    Metric: reply_rate | Target: 10%+ reply rate
    Effort: MEDIUM (4-6 hours setup + 1 week measurement) | Status: NOT STARTED
    Source: Instantly.ai benchmark report 2026

  [H004] Gumroad products with video demos convert 3x better than text-only listings
    Test: Add Kling-generated demo videos to top 3 Gumroad products. Measure conversion change.
    Metric: sales_conversion_rate | Target: 3x improvement
    Effort: MEDIUM (3-4 hours) | Status: NOT STARTED
    Source: First principles + UGC research

  [H005] Local biz cold emails with attached mockup landing page get 5x more responses than generic offers
    Test: Send 100 emails with mockup attached vs 100 generic. Track response + close rate.
    Metric: response_rate + close_rate | Target: 15%+ reply rate with mockup
    Effort: LOW (pipeline already built) | Status: NOT STARTED
    Source: local_biz_pipeline.py already generates mockups

  [H006] Bland AI cold calls to recently funded companies (Crunchbase) convert at 6-10% vs 2-3% for cold lists
    Test: Use Bland AI free tier (100 calls/day) to call 200 recently funded cos vs 200 cold list. Track bookings.
    Metric: call_to_meeting_rate | Target: 6-10% with warm signal
    Effort: MEDIUM (setup Bland AI + Crunchbase scraper) | Status: NOT STARTED
    Source: Research: funded companies have budget and urgency

  [H007] AI persona accounts that post 3x/day grow 5x faster than 1x/day
    Test: Run 2 identical persona accounts: one posts 1x/day, one posts 3x/day for 30 days. Track follower growth.
    Metric: follower_growth_rate | Target: 5x faster growth at 3x posting frequency
    Effort: MEDIUM (need 2 accounts, 30 days) | Status: NOT STARTED
    Source: Platform algorithm research

  [H008] Sending cold emails at 6-8 AM local time gets 42% higher open rate than afternoon sends
    Test: Split 200 identical cold emails: 100 sent at 7 AM, 100 sent at 2 PM. Track opens and replies.
    Metric: open_rate + reply_rate | Target: 42% improvement in opens
    Effort: LOW (just change send time in Instantly) | Status: NOT STARTED
    Source: Instantly.ai benchmark data

Saved hypotheses to /sessions/awesome-nice-brown/mnt/PRINTMAXX_STARTER_KITttttt/LEDGER/RBI_STRATEGIC/HYPOTHESES.json

--- GTM + EDGE TACTICS ---


  [Platform Algorithm Optimization (Legal)]
    1. TikTok: First 3 seconds = hook or die. Use pattern interrupts (zoom, cut, text flash). Post at 6-10 AM and 7-11 PM.
    2. TikTok: Reply to comments with new videos (algo boost). Stitch/duet trending content in your niche.
    3. YouTube Shorts: Cross-post TikTok content. YouTube rewards consistency. 1-3 Shorts/day. Use end screens.
    4. Instagram: Reels get 2-3x reach vs posts. Collab feature = instant audience share. Use trending audio.
    5. X/Twitter: Quote-tweet viral posts with your take. Thread game: 5-8 tweet threads perform best. Post 5-10x/day.
    6. Pinterest: SEO-optimize pin titles and descriptions. Rich pins. Group boards. 15-25 pins/day via scheduler.
    7. YouTube Long: First 30 seconds = retention or death. Open loops. Pattern interrupts every 60 seconds.

  [Cold Outreach Edge Tactics]
    1. Email warmup: Instantly.ai auto-warmup for 14 days before sending. Start 5 emails/day, ramp to 50.
    2. SPF/DKIM/DMARC: Set up ALL THREE or go to spam. Use Google Postmaster Tools to monitor reputation.
    3. Inbox rotation: Use 3-5 sending accounts. Rotate daily. Each account sends max 50/day.
    4. Timeline hooks: "I noticed [company] just raised [amount]..." → 10% reply rate vs 4.4% for generic.
    5. LinkedIn: Connect → engage with 3 posts → THEN pitch. Warm connection = 5x response rate.
    6. Follow-up sequence: 4-7 touches. Day 1, 3, 7, 14, 21. 42% of replies come from follow-ups.
    7. Personalization: Use Clay for enrichment. Reference specific company detail in line 1. Never generic openers.
    8. Subject lines: 3-5 words. Lowercase. No spam triggers. "quick question" = 46% open rate benchmark.

  [SEO Edge Tactics (Legal)]
    1. Programmatic SEO: 300+ pages targeting "[service] in [city]" patterns. Claude Code generates all pages.
    2. Parasite SEO: Post on Medium, LinkedIn, Quora (high DA). Link back to money site. Legal, just aggressive.
    3. Topical authority: 50+ pages on one topic cluster. Google rewards depth. Build pillar + cluster model.
    4. HARO/Connectively: Answer journalist queries. Get backlinks from Forbes, Business Insider etc. Free DR boost.
    5. Expired domains: Buy expired domains with existing backlinks. Redirect to your site. Legal but aggressive.
    6. Google Business Profile: Optimize for local SEO. Photos, posts, reviews, Q&A. Free local traffic.
    7. Schema markup: Add FAQ, HowTo, Review schema. Rich snippets = 2x CTR in search results.

  [Multi-Account Strategy (Platform-Dependent)]
    1. GoLogin: Separate browser profiles per account. Each profile = unique fingerprint, cookies, storage.
    2. Proxy rotation: 1 residential proxy per account. Decodo/Smartproxy. Never share IPs between accounts.
    3. Warmup schedule: Day 1-3: browse only. Day 4-7: like/follow. Day 8-14: post 1x/day. Day 15+: full activity.
    4. Content differentiation: Each account = different niche, voice, visual style. Never cross-post identical content.
    5. Phone verification: Use separate phone numbers per account. Services like TextNow or cheap SIMs.
    6. Device diversity: Mix mobile and desktop posting. Vary post times. Mimic human behavior patterns.
    7. CRITICAL: Stay within platform ToS where possible. Multi-account = risk. Lose accounts = lose revenue.

  [Findom/NSFW Growth Edge]
    1. X/Twitter discovery: #findom #paypig #humanATM #cashslave #finsub hashtags. Post 5-10x/day.
    2. Engagement farming: Reply to findom community posts. Build presence. Dont just broadcast.
    3. Teaser→paywall funnel: Free teaser content on Twitter → "Full content on Fanvue" → subscription.
    4. Telegram VIP: $99-499/mo for "personalized attention". Spin wheel games, flash sales, exclusive drops.
    5. Cross-platform stacking: Twitter (discovery) → Fanvue/Fansly (content) → Telegram (VIP) → CashApp (tributes).
    6. Flash sales: "Next 10 tributes get exclusive content". 25% conversion on warm audience. $200 avg.
    7. Consistency beats volume: 2-3 quality posts/day > 10 low-quality. Build character/narrative arc.
    8. Bio optimization: CashApp, Venmo, crypto address, Fanvue link, Linktree. Maximum payment options.

  [Conversion Edge Tactics]
    1. Anchoring: Show higher price crossed out next to sale price. "$197 $97". 2-3x conversion boost.
    2. Social proof: "1,247 people bought this" or "97% satisfaction rate". Numbers beat testimonials.
    3. Countdown timers: Real scarcity (not fake). "Price increases in 48 hours" with actual price change.
    4. Exit intent popups: Offer discount/bonus when user tries to leave. 10-15% save rate.
    5. Payment splitting: "3 payments of $33" vs "$97 one-time". Installments = 2x conversion.
    6. Guarantee: "30-day money-back, no questions" removes risk. Refund rate stays under 5% for quality.
    7. Bundle pricing: Individual items $30 each, bundle of 5 for $97. Perceived value = 50% off.
    8. First-time discount: 20% off first purchase via email popup. Builds list + converts visitors.

  [Payment and Revenue Optimization]
    1. Stripe: 2.9% + $0.30. For high volume: negotiate to 2.2%. Use Stripe Billing for subscriptions.
    2. Gumroad: 10% fee (down from old pricing). Good for digital products. No monthly fee.
    3. CashApp/Venmo: 0% fee for personal payments. Perfect for findom tributes. Instant settlement.
    4. Crypto: Bitcoin/ETH/SOL in bio. Zero fees. Anonymous for buyers (findom audience prefers this).
    5. Reduce chargebacks: Clear product descriptions, easy refund process, good customer service.
    6. Multi-currency: Accept international payments. Wise for low-fee international transfers.
    7. Tax optimization: Track all expenses (tools, hosting, subscriptions). Home office deduction. S-Corp for >$50K/yr.

  Saved to /sessions/awesome-nice-brown/mnt/PRINTMAXX_STARTER_KITttttt/LEDGER/RBI_STRATEGIC/GTM_EDGE_TACTICS.json

--- FIRST-PRINCIPLES OP DISCOVERY ---

Applying first principles: What can Claude Code + AI tools + zero capital actually produce?

  NEW OP: AI Agent-as-a-Service
    Thesis: Businesses need AI agents but cant build them. Sell pre-built agents for specific verticals (real estate, legal, medical intake).
    Edge: Claude Code builds agent in 2-4 hours. Charge $500-5K per agent + $50-200/mo maintenance.
    Viability: HIGH - $7.6B market growing 30% CAGR. Demand >> Supply in 2026.
    GTM: Cold email to businesses in target vertical. Offer free 7-day trial. Convert to monthly.
    Validation: Check if competitors exist. If yes = market validated. If few = opportunity.
    Status: NEW - NOT IN CURRENT OPS

  NEW OP: AI Data Analysis Service
    Thesis: Small businesses have data but no analysts. Offer automated data analysis reports via Claude Code.
    Edge: Claude Code analyzes CSVs/databases in minutes. Charge $200-1K per report.
    Viability: HIGH - Every business has data. Few have analysts. Clear pain point.
    GTM: Target Shopify stores, SaaS companies. Offer free sample report as lead magnet.
    Validation: Fiverr "data analysis" category growing. Check pricing and demand.
    Status: NEW - NOT IN CURRENT OPS

  NEW OP: AI-Powered Outreach Orchestrator
    Thesis: Combine Bland AI (voice) + Instantly (email) + LinkedIn automation into unified outreach system. Sell as service.
    Edge: Multi-channel outreach = 3-5x response rate vs single channel. Orchestrate all three.
    Viability: HIGH - B2B lead gen = massive market. Multi-channel is the future but complex to setup.
    GTM: Use the system to sell itself. Generate leads via the multi-channel system, then sell the system.
    Validation: Check Clay, Apollo pricing. If they charge $149+/mo, our orchestrated service has room.
    Status: NEW - COMBINES EXISTING TOOLS

  NEW OP: Programmatic Blog Network
    Thesis: 50+ niche blogs, each targeting 100+ long-tail keywords. AI generates all content. Monetize via affiliate + display ads.
    Edge: Claude Code generates entire blog (10-50 posts) in 1-2 hours. Deploy on Cloudflare Pages (free, unlimited bandwidth).
    Viability: MEDIUM - SEO is slow (3-6 months) but compounds. Programmatic = scale advantage.
    GTM: Target underserved niches with high affiliate commissions. Finance, health, legal.
    Validation: Check Ahrefs/SEMrush for keyword difficulty. Target KD <20 keywords.
    Status: NEW - LEVERAGES EXISTING INFRA (longtail_pages + Cloudflare)

  NEW OP: AI Translation Service
    Thesis: Translate existing content (courses, docs, websites) into 10+ languages via Claude. Sell as service.
    Edge: Claude translates at near-human quality. Charge $0.10/word. Automated = 99% margin.
    Viability: HIGH - Translation market $26B. AI disrupting but quality still varies.
    GTM: List on Fiverr/Upwork. Target course creators, SaaS companies, ecom stores.
    Validation: Check Fiverr translation prices. If $0.05-0.15/word = competitive.
    Status: NEW - PURE CLAUDE CODE ARBITRAGE

  NEW OP: AI Meeting Notes Service
    Thesis: Process meeting recordings into structured action items, decisions, and follow-ups.
    Edge: Upload recording → Claude transcribes + structures → deliver in 5 min. Charge $10-50/meeting.
    Viability: MEDIUM - Otter.ai exists but expensive. Niche: small teams who dont want subscription.
    GTM: Target small businesses, freelancers, consultants on LinkedIn.
    Validation: Check Otter.ai pricing ($16.67/mo). Our per-meeting model may appeal to occasional users.
    Status: NEW - EASY TO BUILD AND TEST

Saved to /sessions/awesome-nice-brown/mnt/PRINTMAXX_STARTER_KITttttt/LEDGER/RBI_STRATEGIC/NEW_OP_DISCOVERIES.json

--- SELF-TEST PROTOCOL (for Claude Code execution) ---


# PRINTMAXX SELF-TEST PROTOCOL
# =============================
# Run via Claude Code to validate ops are actually viable.
#
# For each op, Claude Code should:
# 1. CHECK if the infrastructure exists (files, accounts, scripts)
# 2. TEST if scripts actually run without errors
# 3. VALIDATE if output quality meets minimum standards
# 4. RESEARCH if the market opportunity still exists
# 5. SCORE the op on a 1-10 viability scale
# 6. RECOMMEND: ACTIVATE / IMPROVE / KILL / DEPRIORITIZE
#
# Self-test commands to run via printmaxx_cron.sh:
#   ./printmaxx_cron.sh self-test           # Run all self-tests
#   ./printmaxx_cron.sh self-test S02       # Test specific op
#
# Example self-test for S02 (Local Biz Pipeline):
#   1. python3 AUTOMATIONS/local_biz_pipeline.py --dry-run --category=plumbers --city=austin
#   2. Check: Did it generate a mockup landing page?
#   3. Check: Is the landing page valid HTML with no broken links?
#   4. Check: Did it generate a cold email draft?
#   5. Check: Is the email compliant with CAN-SPAM?
#   6. Check: Are there actual businesses in the scrape results?
#   7. Score: 1-10 based on above checks
#   8. Recommend: ACTIVATE if score >= 7, IMPROVE if 4-6, KILL if < 4
#
# This protocol should be run WEEKLY to validate all active ops.


SELF-TEST SUITE:

  [S02] Local Biz Pipeline
    Commands:
      $ python3 AUTOMATIONS/local_biz_pipeline.py --dry-run --category=plumbers --city=austin
      $ python3 AUTOMATIONS/bulk_landing_page_generator.py --dry-run --count=1
    Success criteria:
      ✓ Scraper returns 5+ businesses
      ✓ Landing page is valid HTML
      ✓ Cold email draft passes spam check
      ✓ Total runtime < 60 seconds

  [D01] Gumroad Products
    Commands:
      $ ls -la DIGITAL_PRODUCTS/
      $ wc -c DIGITAL_PRODUCTS/*
    Success criteria:
      ✓ 9+ product files exist
      ✓ Each file > 1KB (not empty)
      ✓ Product descriptions are coherent (manual review)

  [G04] Alpha Extraction
    Commands:
      $ python3 scripts/extract_source_csvs_from_mega_sheet.py
      $ wc -l LEDGER/ALPHA_STAGING.csv
    Success criteria:
      ✓ Extraction completes without errors
      ✓ Alpha staging has 50+ entries
      ✓ No duplicate URLs in staging