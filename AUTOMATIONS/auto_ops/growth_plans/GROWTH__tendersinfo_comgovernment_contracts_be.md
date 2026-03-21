# Growth Plan:  tendersinfo .comgovernment contracts before they close.filt

**Created:** 2026-03-20 18:09
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. LinkedIn outreach to government contractors and small biz owners with SAM.gov registrations
2. Reddit r/govcontracting r/smallbusiness content seeding with real tender examples
3. Content series: 'Government contracts most small businesses miss' — builds authority + captures leads
4. Partner with SBA-adjacent consultants who help businesses get SAM.gov registered
5. Cross-pollinate with EAS venture — local businesses often qualify for set-aside contracts

## Budget Tier Strategies

### FREE
Cold email to SAM.gov registered businesses, Reddit/LinkedIn organic posts about underserved government contracts, content repurposing via existing content_factory pipeline

### LOW
$20-50/mo for email warmup tool or additional scraping proxies for state portals that rate-limit

### MID
$100-200/mo for LinkedIn Sales Navigator to find government contractor decision-makers + targeted ads to small biz owners

## Daily Actions

- [ ] 1. Build gov_tender_scraper.py using SAM.gov Opportunities API (api.sam.gov, free, no key needed for public data)
- [ ] 2. Add state procurement portal scrapers (top 10 states by spending: CA, TX, NY, FL, PA, IL, OH, GA, NC, MI)
- [ ] 3. Build qualifier that scores tenders by budget, deadline, competition, set-aside status
- [ ] 4. Build business matcher using SAM.gov Entity API to find registered businesses by NAICS code
- [ ] 5. Wire into existing cold outreach pipeline (chain_recruit_new_affiliates) for email sending
- [ ] 6. Create LEDGER/GOV_TENDERS_PIPELINE.csv to track scrape→qualify→match→outreach→revenue
- [ ] 7. Add to cron: daily 6:30 AM scrape, 7:00 AM qualify+match, 8:00 AM outreach batch
- [ ] 8. Generate content: '5 government contracts closing this week that nobody is bidding on' — weekly thread

## Tooling

```json
{
  "browser": "playwright for state portals without APIs",
  "email": "custom cold email scripts (existing outbound infra)",
  "content": "content_factory for gov contracting tips content"
}
```
