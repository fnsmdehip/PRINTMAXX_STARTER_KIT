# Growth Plan: Landscaping might be the most obvious roll-up in home servic

**Created:** 2026-03-20 23:12
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo per client retainer (fractional digital ops); realistic 1-2 clients in 60 days = $500-4K/mo

---

## Tactics

1. Position as 'acquisition-ready ops consultant' not generic agency — roll-up narrative is the hook
2. Post landscaping roll-up analysis threads on Twitter (use actual Axial/BizBuySell data for credibility)
3. Reddit play: r/Entrepreneur, r/smallbusiness — post case study framing not pitch
4. Repurpose scraped data into 'State of Landscaping Businesses in [City]' lead magnet

## Budget Tier Strategies

### FREE
Organic: Google Maps scrape via Playwright, SMTP cold email, Reddit/Twitter content about home services roll-ups, post in r/lawncare r/landscaping as value content

### LOW
$0-50/mo: Hunter.io email finder free tier (100/mo), basic LinkedIn outreach, boost 1-2 Twitter threads about landscaping biz valuations

### MID
$50-200/mo: Apollo.io for enriched landscaping contacts, targeted LinkedIn InMail to landscaping business owners 45-60 age bracket (pre-exit sweet spot)

## Daily Actions

- [ ] Wire Playwright scraper to extract top 200 landscaping businesses across 5 test metros (Atlanta, Phoenix, Tampa, Dallas, Denver — sunbelt = most landscaping activity)
- [ ] Build qualification scorer: web_gap_score + review_volume_score + business_age_score → composite
- [ ] Draft cold email template: roll-up exit narrative hook, not generic agency pitch
- [ ] Add to LEDGER/FREELANCE_PIPELINE_ACTIVE.csv with status tracking
- [ ] Wire to chain__how_i_optimized_scheduling_for_a_local_ for ops delivery playbook
- [ ] Schedule weekly cron: Monday 7 AM scrape + qualify + email batch
- [ ] Generate 3 Twitter posts from roll-up data angle via engagement_bait_converter.py

## Tooling

```json
{
  "browser": "Playwright (scrape Google Maps + Yelp)",
  "email": "SMTP custom script (no paid tool)",
  "content": "engagement_bait_converter.py \u2192 roll-up angle posts"
}
```
