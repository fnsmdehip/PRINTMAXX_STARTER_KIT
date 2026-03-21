# Growth Plan: Series D Unicorn Startup Offer Review (I will not promote)

**Created:** 2026-03-20 23:12
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo (content → equity calculator digital product $29-49 on Gumroad; lead gen → outbound consulting upsell)

---

## Tactics

1. Reply to top offer review threads with equity literacy value (builds authority, drives profile visits)
2. Post anonymized equity breakdowns as Twitter threads — high shareability among startup employees
3. Target 'just got Series D offer' + 'equity cliff question' Reddit commenters with DM outbound to free equity calculator
4. Cross-post equity analysis threads to r/cscareerquestions, r/financialindependence, r/Fire

## Budget Tier Strategies

### FREE
Daily Reddit JSON scrape + comment-reply engagement + Twitter thread repurposing via content_repurposer.py. No tools needed — Reddit JSON API requires no auth.

### LOW
$0-50/mo: Boost top equity thread with $10 Twitter ad to startup employee demographic. Buy 1 relevant newsletter sponsorship slot.

### MID
$50-200/mo: Sponsor r/startups weekly digest if available. Target LinkedIn promoted post to Series B-D employees at 1K+ headcount companies.

## Daily Actions

- [ ] Create startup_offer_monitor.py: hit Reddit JSON API for r/startups filtered by flair/keywords, parse top posts
- [ ] Wire equity_analyzer step: use claude -p to extract comp structure fields from post text
- [ ] Wire to engagement_bait_converter.py for thread generation
- [ ] Append output to CONTENT/social/posting_queue/
- [ ] Add cron 0 7 * * * for daily run
- [ ] Create DIGITAL_PRODUCTS draft: 'Startup Equity Offer Analyzer' — 1-page PDF template ($29 Gumroad)
- [ ] Update LEDGER/INBOUND_LEADS.csv schema to include 'equity_intent' flag

## Tooling

```json
{
  "browser": "none \u2014 Reddit JSON API (requests, no Playwright needed)",
  "email": "none at Phase 0",
  "content": "content_repurposer.py + engagement_bait_converter.py"
}
```
