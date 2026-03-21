# Growth Plan: How I Added 16 New Customers in 30 Days (+31% MRR) Hey every

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $500-1500/mo

---

## Tactics

1. LinkedIn AI Agent sequences targeting SaaS founders at 35-50/day (stay under 100/day limit)
2. Cold email at 490/day via existing infrastructure — use as volume funnel to LinkedIn precision layer
3. Reddit r/SaaS + r/indiehackers: 3 posts/week minimum — entry admits Reddit was lazy at 20K impressions, extractable upside
4. Demo call conversion: 34 demos → 16 customers = 47% close rate. Document the demo script and replicate for client services
5. Repurpose this exact case study as content — '16 customers in 30 days' hook + real numbers drives engagement

## Budget Tier Strategies

### FREE
LinkedIn manual AI-assisted sequences via claude -p message gen + existing cold_email_pipeline.py. Reddit organic posting. n8n self-hosted for workflow automation.

### LOW
$0-50/mo: Phantombuster free tier for LinkedIn scraping (500 leads/mo). Apollo.io free (50 credits/mo) for email enrichment.

### MID
$50-200/mo: Instantly.ai at $37/mo for warmed sending infra. LinkedIn Sales Navigator at $99/mo for precise ICP targeting.

## Daily Actions

- [ ] Route to existing chain chain__cold_outbound_audit_output_mm007__ — do NOT create new chain
- [ ] Enhance eas_lead_pipeline.py: add LinkedIn AI agent message generation via claude -p with ICP persona targeting
- [ ] Wire Playwright MCP to scrape LinkedIn leads matching ICP (founder + SaaS + <50 employees)
- [ ] Set cron 8 AM weekdays: generate 40 LinkedIn messages + 490 cold emails, log to LEDGER/OUTREACH_PIPELINE.csv
- [ ] Add demo call booking link to all outreach (Calendly embed or plain URL)
- [ ] Run engagement_bait_converter.py on this case study → post 3 tweets + 1 thread to posting_queue

## Tooling

```json
{
  "browser": "Playwright MCP for LinkedIn profile scraping",
  "email": "Existing cold_email_pipeline.py (MM007)",
  "content": "engagement_bait_converter.py \u2014 convert this case study into 3 posts"
}
```
