# Growth Plan: [GOV CONTRACT] VA GENERAL MENTAL HEALTH AND SUICIDE PREVENTI

**Created:** 2026-03-21 12:40
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo (proposal writing fees + referral fees on wins; 6-18 month sales cycle — realistic Phase 1-2 revenue, not Phase 0)

---

## Tactics

1. Teaming arrangement: partner with SDVOSB-certified small biz (automatic preference on VA contracts) — they win, you get 10% for sourcing + proposal support
2. USASpending.gov reverse-lookup: find contractors who won similar VA mental health contracts in last 3 years — warm outreach vs cold
3. SAM.gov saved search + email alerts (free) to never miss a posting — automate forwarding into pipeline
4. Content play: publish 'VA Mental Health Contract Landscape 2026' report — positions as authority, attracts inbound from contractors needing intel
5. Proposal writing as a service: many small contractors lack BD staff — offer white-label proposal writing at $2-5K flat fee regardless of outcome

## Budget Tier Strategies

### FREE
SAM.gov API (free tier, 10 req/s). USASpending.gov public data. LinkedIn manual outreach to 10 prime contractors/week. Email templates via existing cold_email_scripts. Publish contract intel as Twitter threads to attract inbound.

### LOW
$0-50/mo — Apollo.io free tier for contractor contact enrichment. 1 Instantly mailbox for outbound to contractors. Publish monthly VA contract digest on Substack ($0) to build subscriber list of contractor BD teams.

### MID
$50-200/mo — Full Instantly sequence for 500 contractors/month. LinkedIn Sales Nav for past-performance targeting. Build simple web tool (SAM.gov alert bot) and charge $49/mo to contractors who want real-time VA health solicitation alerts.

## Daily Actions

- [ ] Register free SAM.gov API key at open.gsa.gov/api/opportunities-api (5 min)
- [ ] Wire gov_contract_scanner_va_health.py to query NAICS 624190 + 621330 weekly, output to AUTOMATIONS/agent/autonomy/gov_contracts/
- [ ] Wire into existing chain__tendersinfo_comgovernment_contracts_be handoff — skip re-creating, parameterize with VA+mental health filters
- [ ] Build contractor contact list from USASpending.gov (free download) — filter: VA awards, NAICS 624190, 2022-2025, <$10M (small business range)
- [ ] Cold outreach pitch: 'I monitor VA mental health solicitations — found this one with a 2027-03-03 deadline and no incumbent. Want the full details + teaming intro?'
- [ ] Parallel play: offer proposal writing service at $2-5K flat — mental health outreach proposals are templatable
- [ ] Add cron entry: weekly scan Monday 7 AM, results to Slack/email

## Tooling

```json
{
  "browser": "none \u2014 SAM.gov has public REST API",
  "email": "existing cold_email_scripts + Instantly at LOW tier",
  "content": "contract_intel_digest \u2192 content_repurposer.py for Twitter/LinkedIn"
}
```
