# Growth Plan: How I built $15-20k vibecoding agency as non-technical histo

**Created:** 2026-03-20 13:50
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Post vibecoding case studies to r/SideHustle r/webdev r/Entrepreneur showing before/after with build timelines
2. Cross-post app factory builds as portfolio proof on Upwork/Fiverr profiles
3. Reply to 'looking for developer' posts within 15min using auto-detection scraper
4. Build public portfolio page from existing 47+ deployed PRINTMAXX apps as social proof

## Budget Tier Strategies

### FREE
Organic Reddit/IndieHackers/Twitter replies to build-request posts, portfolio page from existing apps, case study threads from real builds

### LOW
$20-50/mo for Upwork Connects or Fiverr promoted gig placement to boost visibility on marketplace searches

### MID
$50-150/mo for targeted LinkedIn/Twitter ads showing AI-speed build demos, retarget portfolio page visitors

## Daily Actions

- [ ] Wire into existing chain_how_i_built_1520k_vibecoding_agency_as with updated prospect sources
- [ ] Create vibecoding_agency_lead_feeder.py that scrapes Upwork/Reddit/IH for app-build requests daily
- [ ] Auto-qualify leads by budget/urgency/scope using Claude scoring
- [ ] Generate proposals referencing PRINTMAXX portfolio (47 live apps) as proof of rapid delivery
- [ ] Route qualified leads to EAS outreach pipeline (eas_lead_pipeline.py)
- [ ] Add cron 6:30 AM daily scrape, feed new prospects into handoff chain
- [ ] Track close rate and average deal size in KPI dashboard

## Tooling

```json
{
  "browser": "playwright",
  "email": "custom cold email scripts via eas_lead_pipeline.py",
  "content": "content_factory for case study generation"
}
```
