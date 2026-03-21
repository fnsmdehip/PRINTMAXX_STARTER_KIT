# Growth Plan: Real examples of what sweaty startups have sold for (pulled 

**Created:** 2026-03-21 12:40
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Post 'real deal' breakdowns on Twitter/X as data-backed content (not hype) — verifiable numbers beat opinion content 3x on engagement
2. Build SEO pages: 'what does a pressure washing business sell for', 'lawn care business valuation multiple 2026' — high intent, near-zero competition
3. Compile top 50 deals into a Gumroad report: 'Sweaty Startup Acquisition Database 2026' at $19-29
4. Cross-post deal summaries to r/sweatystartup, r/Entrepreneur, r/smallbusiness as value posts with no promo
5. Build email capture: 'get notified when new sweaty startup deals are posted' — builds list of acquisition-minded buyers and sellers

## Budget Tier Strategies

### FREE
Reddit scraping via JSON API (no browser needed), Twitter content from deal data via engagement_bait_converter.py, SEO longtail pages deployed to surge.sh, Gumroad PDF product from compiled deals

### LOW
$0-50/mo — boost top-performing deal posts on Twitter, submit to acquisition-focused newsletters (Acquiring.com, MicroAcquisitions), Pinterest pins of deal infographics

### MID
$50-200/mo — sponsor r/sweatystartup adjacent newsletters, run retargeting to deal database page visitors, LinkedIn outreach to business brokers offering data partnership

## Daily Actions

- [ ] 1. Add r/sweatystartup to background_reddit_scraper.py subreddit list with sale-specific keywords filter
- [ ] 2. Write sweaty_startup_deal_scraper.py: hits Reddit JSON API, filters for deal posts, uses claude -p to extract structured fields into LEDGER/sweaty_deals.csv
- [ ] 3. Wire DAG: scrape → extract → parallel(content_factory, product_updater)
- [ ] 4. Route 3 best deals/week through engagement_bait_converter.py → posting_queue
- [ ] 5. Generate Gumroad PDF report from top 50 deals (digital product, $19-29, no account needed to build)
- [ ] 6. Deploy 5 SEO longtail pages: '[business type] business valuation multiple', 'how much does X sell for'
- [ ] 7. Add cron: 0 7 * * 1 (Monday 7 AM weekly sweep)
- [ ] 8. Add KPI entry to KPI_DASHBOARD.md: deals_scraped_weekly, content_pieces_from_deals, product_page_views

## Tooling

```json
{
  "browser": "none \u2014 Reddit JSON API (requests only, no Playwright needed)",
  "email": "none",
  "content": "engagement_bait_converter.py + content_multiplier.py"
}
```
