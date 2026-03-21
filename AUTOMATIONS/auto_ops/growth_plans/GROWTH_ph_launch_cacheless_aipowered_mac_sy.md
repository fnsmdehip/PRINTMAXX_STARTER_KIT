# Growth Plan: [PH LAUNCH] Cacheless: AI-Powered Mac System Data Cleaner

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo

---

## Tactics

1. 48h launch window is critical — contact founders while post-launch dopamine is at peak
2. Comment on PH page with genuine utility tip — builds credibility with founder and other watchers
3. Cross-reference PH launches against LEDGER/COMPETITIVE_INTEL_MASTER.csv to identify repeat launchers (higher close rate)
4. Use upvote count as ambition proxy — 100+ upvotes = founder has growth mindset, warmer lead
5. Route all Mac utility launches to APP_FACTORY competitive intel regardless of outreach outcome

## Budget Tier Strategies

### FREE
Daily PH scrape via requests JSON API (no browser needed), founder email extraction via website crawl, cold outreach via existing scripts, track in LEDGER/ph_outreach_queue.csv

### LOW
$20-30/mo Hunter.io API for founder email enrichment + Instantly warmup on 1 dedicated outreach domain

### MID
$50-100/mo Clay alternative for PH founder enrichment + multi-domain outreach rotation + LinkedIn cross-referencing

## Daily Actions

- [ ] Wire into existing chain_14_ph_launches_today__high_quality_b2b_ — add Mac/utility category filter parameter
- [ ] Enhance existing ph_scraper in AUTOMATIONS/ to extract founder social + contact links from PH maker profiles
- [ ] Add Mac utility app signal branch: flag to APP_FACTORY competitive intel CSV alongside outreach
- [ ] Set cron 9 AM daily — scrape previous day PH launches, qualify, queue outreach within 24h window
- [ ] Track ph_outreach_sent / replies / conversions in LEDGER/ph_outreach_queue.csv

## Tooling

```json
{
  "browser": "playwright MCP for PH profile pages when JSON API insufficient",
  "email": "existing cold email scripts (AUTOMATIONS/)",
  "content": "none"
}
```
