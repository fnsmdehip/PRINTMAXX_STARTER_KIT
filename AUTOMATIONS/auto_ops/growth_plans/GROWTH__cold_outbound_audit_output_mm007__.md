# Growth Plan: # COLD OUTBOUND Audit Output (MM007)  **Date:** 2026-02-06 *

**Created:** 2026-03-20 23:12
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Personalize subject line with the prospect's actual site URL to increase open rates
2. Lead with a 1-line specific observation from their site (e.g. 'Your site loads in 8.2s on mobile') — proof of audit, not spam
3. Offer free 5-min Loom audit video as CTA — converts 3-5x better than 'book a call'
4. Follow up D+3 and D+7 with different angles (mobile stats, competitor comparison)
5. Cross-promote wins to Twitter @printmaxxer as social proof loop

## Budget Tier Strategies

### FREE
Claude -p for personalization, Playwright for scraping, custom SMTP via Gmail/Zoho free tier, 20 emails/day warmup, track replies manually in OUTREACH_PIPELINE.csv

### LOW
$20-30/mo for Mailgun SMTP relay (10K emails free then $0.80/1K), Hunter.io free tier (25 searches/mo) for email enrichment, boost top-performing email angle as Twitter thread

### MID
$100-150/mo for Instantly or Lemlist lookalike (n8n self-hosted + SMTP rotation as free alternative), add LinkedIn connection + view warmup sequence after email open

## Daily Actions

- [ ] Read existing MM007/MM070 files to find what 3 files already exist and what's built
- [ ] Run cold_outbound_executor.py DAG: scrape 50 prospects → qualify top 20 → generate emails → send
- [ ] Wire cron: weekdays 8 AM — scrape fresh batch + send previous day's approved emails
- [ ] Add OUTREACH_PIPELINE.csv tracking to KPI_DASHBOARD.md
- [ ] After 50 emails sent, analyze reply rate and double-down on winning angle

## Tooling

```json
{
  "browser": "Playwright MCP (scrape sites)",
  "email": "custom SMTP script (Zoho free tier) or Mailgun",
  "content": "claude -p for email personalization"
}
```
