# Growth Plan: [PH LAUNCH] Visdiff: Stop bridging the design-to-code gap, c

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-800/mo

---

## Tactics

1. 48h outreach window is critical — founders are dopamine-flooded post-launch and most receptive
2. Personalize with specific PH comment reference ('saw you mentioned X in comments') — 3x reply rate
3. Offer audit or teardown as lead magnet, not a pitch — 'I noticed your design-to-code pipeline does X, here is what I would change'
4. Target tools in design/dev/no-code niche specifically — they have technical founders who pay for technical services
5. Cross-reference PH launches against COMPETITIVE_INTEL.csv — if competitor launched, outreach to their disgruntled commenters

## Budget Tier Strategies

### FREE
Playwright scrapes PH daily top 20. Manual review of top 5. Claude -p generates personalized opener from product description. Cold email via existing smtp scripts. Zero cost.

### LOW
$0-50/mo: Apollo.io free tier (50 credits/mo) for email enrichment. Scale to top 20 launches/day. Add LinkedIn connection request sequence via existing outreach scripts.

### MID
$50-200/mo: Hunter.io API for bulk email finding ($49/mo, 500 finds). Instantly warm accounts for higher deliverability. Target 100+ PH launches/week across all categories.

## Daily Actions

- [ ] Wire ph_launch_lead_extractor.py to scrape PH /today page via playwright at 6:30 AM daily
- [ ] Filter for design/dev/no-code tools with >50 upvotes in first 12h
- [ ] Extract maker Twitter handles from PH maker profiles
- [ ] Enrich with email via existing email finder scripts (free tier)
- [ ] Route to chain_14_ph_launches_today__high_quality_b2b_ handoff chain
- [ ] Generate personalized cold email opener using product description + top PH comment via claude -p
- [ ] Log to LEDGER/OUTREACH_PIPELINE.csv with launch_date, product, founder, outreach_sent, reply_status
- [ ] Add cron entry: 30 6 * * * python3 AUTOMATIONS/ph_launch_lead_extractor.py --run

## Tooling

```json
{
  "browser": "playwright MCP for PH scraping",
  "email": "existing cold_email_pipeline.py scripts",
  "content": "claude -p for personalized opener generation"
}
```
