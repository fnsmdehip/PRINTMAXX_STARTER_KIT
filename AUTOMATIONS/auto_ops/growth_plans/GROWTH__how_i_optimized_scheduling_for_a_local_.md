# Growth Plan:  how i optimized scheduling for a local service gig. what's 

**Created:** 2026-03-20 18:09
**Venture:** LOCAL_BIZ
**Budget Tier:** FREE
**Revenue Est:** $500-1500/mo

---

## Tactics

1. Target businesses with 10-50 Google reviews (established enough to pay, small enough to lack tech)
2. Build one scheduling demo per vertical (landscaping, cleaning, pressure washing, HVAC) as social proof
3. Post before/after scheduling efficiency screenshots in r/sweatystartup and r/smallbusiness
4. Cross-pollinate with EAS venture: scheduling is an upsell to any local biz automation client
5. Repurpose the app factory template: one base scheduling PWA, skin per vertical

## Budget Tier Strategies

### FREE
Cold email with personalized demo links, Reddit/Facebook group posts showing scheduling optimization results, cross-promote from existing local biz content

### LOW
$0-50/mo — Boost 2-3 Facebook posts in local service business owner groups, Google Ads on 'scheduling software for [vertical]' longtail keywords

### MID
$50-200/mo — Targeted LinkedIn ads to small business owners, sponsor one local trades Facebook group

## Daily Actions

- [ ] 1. Build scheduling PWA template in app factory (route optimization + AI time slots) — extend existing streak app template with booking UI
- [ ] 2. Create 3 vertical skins: landscaping, cleaning, pressure washing
- [ ] 3. Deploy demo instances to surge.sh (landscaping-scheduler.surge.sh etc)
- [ ] 4. Write local_biz_scheduling_prospector.py — scrapes Google Maps API for service businesses in top 20 US metros
- [ ] 5. Qualifier scores businesses by pain signal (no website booking = HIGH, phone-only = HIGH, uses competitor tool = SKIP)
- [ ] 6. Wire into existing eas_lead_pipeline.py for email extraction and cold outreach
- [ ] 7. Cold email template: 'I noticed [Business Name] takes bookings by phone. Here is what your customers could see instead: [demo link]. 14-day free trial, $99/mo after.'
- [ ] 8. Add to cron: Mon+Thu 7:30 AM scrape cycle, daily 6 PM outreach batch
- [ ] 9. KPI tracking: businesses scraped, emails sent, demo visits (analytics pixel), replies, conversions
- [ ] 10. Content: 3 tweets about 'boring business scheduling optimization' + 1 thread on building AI scheduling tools for trades

## Tooling

```json
{
  "browser": "playwright for scraping Google Maps/Yelp",
  "email": "custom cold email script (eas_lead_pipeline.py pattern)",
  "content": "app_factory template + scheduling PWA base"
}
```
