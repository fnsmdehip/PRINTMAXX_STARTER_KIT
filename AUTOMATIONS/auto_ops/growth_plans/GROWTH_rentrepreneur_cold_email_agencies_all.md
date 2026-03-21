# Growth Plan: [r/entrepreneur] Cold email agencies all claim personalizati

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo (reply rate improvement on existing OUTBOUND venture, not standalone)

---

## Tactics

1. Screenshot reply rate improvement from personalized vs generic batch — post as content proof
2. Offer 'real personalization audit' as lead magnet: scan a prospect's current cold emails and show them they're fake-personalizing
3. Build public tool at /cold-email-personalizer that does 3 free personalized lines — captures emails, upsells to full sequence

## Budget Tier Strategies

### FREE
Enhance existing outbound scripts with Playwright scraping of prospect homepage + LinkedIn headline. Claude generates opener. Zero additional cost. Wire into chain_cold_outbound as preprocessing step.

### LOW
$0-30/mo: Apollo.io free tier for enrichment signals (job change, company funding). Feeds richer context to Claude personalization prompt.

### MID
$50-100/mo: Hunter.io or Clearbit for company tech stack signals — 'I see you're using HubSpot, most cold email tools won't integrate with it without manual work, ours does' angle.

## Daily Actions

- [ ] Extend existing lead enrichment in eas_lead_pipeline.py to scrape: homepage headline, most recent blog post title, LinkedIn About snippet, recent job posting titles
- [ ] Add personalization_prompt function: pass 4 signals to Claude claude-haiku-4-5 with instruction to generate one 15-word hyper-specific opener referencing exactly one signal
- [ ] Inject generated opener as {{personalized_line}} variable in cold email template — first sentence only
- [ ] A/B test: 50% personalized first-line vs 50% generic. Log reply rates to LEDGER/COLD_EMAIL_AB.csv
- [ ] Wire cron at 7AM daily to pre-generate personalized openers for that day's batch before send window

## Tooling

```json
{
  "browser": "Playwright MCP for LinkedIn/website scraping",
  "email": "existing cold email scripts in AUTOMATIONS/",
  "content": "claude -p for personalized opener generation"
}
```
