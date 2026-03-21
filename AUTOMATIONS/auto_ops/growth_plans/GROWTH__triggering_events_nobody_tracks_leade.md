# Growth Plan:  triggering events nobody tracks:- leadership change (theorg

**Created:** 2026-03-20 18:09
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Use trigger events as engagement bait content: 'Most people cold email from a list. I email companies the week their VP of Sales quits.' — thread format for Twitter/LinkedIn
2. Cross-pollinate: trigger events feed APP_FACTORY (build a SaaS trigger monitor as a product) and CONTENT (weekly trigger event roundup newsletter)
3. Multi-signal stacking: company with 3+ triggers in 30 days = hot lead, prioritize above all other outreach
4. Glassdoor review spike detection doubles as content: '5 companies quietly imploding right now (Glassdoor data)' engagement bait

## Budget Tier Strategies

### FREE
Scrape TheOrg, Glassdoor, SEC EDGAR (existing scanner), Google Alerts RSS, LinkedIn public profiles. Use existing Brave cookie injection for authenticated scraping. Cold email from existing infrastructure.

### LOW
$0-50/mo — Add proxy rotation for Glassdoor/LinkedIn to avoid rate limits. Upgrade Google Alerts to Talkwalker for better coverage.

### MID
$50-200/mo — Add Clay.com or similar enrichment API for contact discovery. Scale to monitoring 500+ target companies.

## Daily Actions

- [ ] 1. Create triggering_event_scanner.py with 6 scraper modules (TheOrg, Glassdoor, LinkedIn, job boards, SEC EDGAR via existing sec_edgar_scanner.py, Google Alerts RSS)
- [ ] 2. Wire Playwright MCP for TheOrg and Glassdoor scraping, requests for SEC/RSS/job boards
- [ ] 3. Build signal scoring: each trigger type = 1-3 points, companies with 5+ points in 30 days = priority outreach
- [ ] 4. Connect to LEDGER/TRIGGERING_EVENTS.csv (already exists) as output sink
- [ ] 5. Wire handoff to eas_lead_pipeline.py: scored leads auto-generate personalized cold emails using trigger event as the hook line
- [ ] 6. Add cron 6:30 AM daily, append to TRIGGERING_EVENTS.csv, feed qualified leads to outreach queue
- [ ] 7. Generate 3 content pieces from weekly trigger findings (engagement_bait_converter.py)
- [ ] 8. Track reply rate on trigger-event emails vs baseline cold emails in KPI dashboard

## Tooling

```json
{
  "browser": "playwright_mcp + brave_cookie_injection",
  "email": "eas_lead_pipeline.py + custom cold email scripts",
  "content": "engagement_bait_converter.py for trigger-event threads"
}
```
