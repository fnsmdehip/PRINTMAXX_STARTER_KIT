# Growth Plan: $22k/mo service business built with just cold emails and DMs

**Created:** 2026-03-20 23:12
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $3,000-7,000/mo

---

## Tactics

1. Post service case studies on r/coldemail and r/entrepreneurs with method breakdown — drives inbound DMs
2. Use engagement_bait_converter.py to turn each booked call into a Twitter thread about the niche pain point
3. Cross-pollinate: feed reply signals into alpha_auto_processor.py as new ICP refinement data
4. Retarget non-openers with DM on LinkedIn/Twitter 3 days after email (multi-touch > single touch)
5. Use chain_package_existing_stack_as_client_service to productize the first successful service delivery

## Budget Tier Strategies

### FREE
Playwright scrapes LinkedIn/Reddit for ICP prospects. Claude Max writes all emails. SMTP via existing warmed domains. Twitter DMs via cookie-injected Brave scraper. 50 emails/day, 5 DMs/day.

### LOW
$20-40/mo: Buy one Apollo.io starter list (1000 verified emails in target niche). Route through existing cold_outbound.py. Domain warm-up via Mailwarm OSS alternative.

### MID
$50-150/mo: Upgrade to Clay-lite enrichment (webhook into n8n at localhost:5678 → enrich with Clearbit free tier → score → send). Add 2nd warmed domain for A/B subject line testing.

## Daily Actions

- [ ] Extend cold_outbound.py with ICP trigger-event scoring (hire/launch/bad review signals)
- [ ] Wire handoff chain: scraper → qualifier → personalizer → sender → logger
- [ ] Add cron: 0 7 * * 1-5 (weekday mornings, 50 emails/day)
- [ ] Update LEDGER/FREELANCE_PIPELINE_ACTIVE.csv schema to track reply rate + meetings
- [ ] Add KPI entry to OPS/KPI_DASHBOARD.md: daily emails sent, reply %, meetings/week
- [ ] Capture refined ICP signal back into alpha_auto_processor.py for continuous improvement
- [ ] Route first case study win to engagement_bait_converter.py for content flywheel

## Tooling

```json
{
  "browser": "playwright MCP for LinkedIn/Twitter DMs",
  "email": "cold_outbound.py (custom SMTP, existing warmed domains)",
  "content": "engagement_bait_converter.py for case study \u2192 content pipeline"
}
```
