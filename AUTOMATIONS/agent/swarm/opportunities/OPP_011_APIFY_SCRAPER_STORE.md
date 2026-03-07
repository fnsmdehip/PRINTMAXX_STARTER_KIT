# OPP_011: Apify Actor Store — Sell Scrapers as Products

**Score: 9.0/10** | Fit: 10 | Effort: 2 | ROI: 8
**Created:** 2026-03-07 | **Source:** swarm_opportunity_scanner
**Status:** PENDING_REVIEW

---

## What

Package our existing Playwright/Python web scrapers as Apify Actors and sell them on the Apify Store. Zero listing cost. Apify handles billing, infrastructure, and user acquisition. Customers pay for compute — we get a cut of every run.

We already have 4+ working scrapers (Twitter bookmarks, Twitter accounts, Reddit deep scraper, background scraper). Adapt these + build new high-demand scrapers for the store.

## Why

- **Zero startup cost.** Apify Store listing is free.
- **Users come to you.** Apify has thousands of active users browsing the store daily.
- **We already have the scrapers.** 4 tested, working Playwright scrapers sitting in AUTOMATIONS/.
- **Passive income.** Once listed, scrapers run on Apify cloud. Revenue per run.
- **Popular actors earn $500-$5K+/mo.** Top actors (Google Maps, LinkedIn, TikTok) earn significantly more.
- **No customer support burden.** Apify handles infrastructure, scaling, proxy rotation.
- **Compounds with our stack.** Building more scrapers = more products = more revenue.

## How

### Apify Actor Architecture
- Apify Actors are Docker containers with a standard input/output schema
- Can be built in Python (Playwright) or Node.js (Puppeteer/Playwright)
- Input: JSON schema defining what users configure
- Output: Dataset (structured JSON/CSV)
- Apify provides proxy rotation, scheduling, webhooks, API access

### First 3 Steps (This Week)

1. **Register Apify developer account** (free, 5 min)
   - Go to apify.com → Sign up → Developer settings → Enable Actor publishing

2. **Adapt Reddit Deep Scraper as first Actor** (2-4 hours)
   - Our `reddit_deep_scraper.py` uses requests (JSON API) — perfect for Apify
   - Add Apify SDK wrapper: `from apify import Actor`
   - Define input schema: subreddits, keywords, time_filter, max_results
   - Output: structured dataset with post title, score, comments, URLs, extracted numbers
   - Test locally with `apify run`
   - Publish to store with description, README, example outputs

3. **Build 2 high-demand scrapers** (1-2 days each)
   - **Google Business Profile scraper** — local businesses need competitor reviews, ratings, hours. High demand on Apify.
   - **App Store reviews scraper** — developers need bulk review extraction for sentiment analysis. Gaps in existing actors.

### Revenue Model
- Apify takes 20% platform fee
- Users pay per compute unit (CU)
- Average scraper earns $0.05-0.50 per run
- Popular scrapers get 1,000-10,000+ runs/month
- Target: 3-5 actors earning $200-1,000/mo each = $600-5,000/mo

## Expected ROI

| Metric | Value |
|--------|-------|
| Startup cost | $0 |
| Time to first revenue | 1-2 weeks |
| Monthly potential (3mo) | $500-2,000/mo |
| Monthly potential (6mo) | $2,000-5,000/mo |
| Competition | Medium (but niche scrapers have gaps) |
| Stack fit | Perfect (Python + Playwright) |
| Recurring | Yes (passive per-run revenue) |

## Risk Assessment
- Low risk: zero upfront cost, existing code
- Apify could change revenue share (unlikely, stable for years)
- Some scrapers may violate site TOS — stick to public data APIs (Reddit JSON, App Store RSS)
- Need to maintain actors when target sites change HTML structure

## Adjacencies
- Each scraper = content for Twitter ("I built a scraper that...")
- Scraper data feeds other PRINTMAXX ventures (lead gen, competitor intel)
- Upsell: custom scraper development service ($500-2K per project)
