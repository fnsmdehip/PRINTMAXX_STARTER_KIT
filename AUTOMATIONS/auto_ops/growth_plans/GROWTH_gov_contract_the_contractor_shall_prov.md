# Growth Plan: [GOV CONTRACT] THE CONTRACTOR SHALL PROVIDE ON-SITE AND OFF-

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $5K-50K/contract (broker/subcontract margin 15-35%); realistic first 90 days $0-5K

---

## Tactics

1. Target small-biz set-aside contracts where large primes are excluded — direct bid path
2. Use USASpending.gov to find primes who won printing contracts and cold-pitch as subcontractor
3. Register in SAM.gov as vendor (free) to get notified of solicitations automatically
4. Monitor FPDS for awarded printing contracts — winners need ongoing capacity, pitch as overflow vendor
5. Stack: position as broker between government contract and offshore/budget print fulfillment at 20-40% margin

## Budget Tier Strategies

### FREE
SAM.gov registration (free), daily scraper via Playwright MCP, cold email via existing scripts, capability statement via claude -p template gen

### LOW
$0-50/mo — GovWin IQ free trial for opportunity intel, targeted LinkedIn outreach to contracting officers at agencies with active print solicitations

### MID
$50-200/mo — paid SAM.gov data feed or Deltek for full opportunity pipeline, GSA Schedule application if volume warrants

## Daily Actions

- [ ] Register on beta.sam.gov as vendor (free, 30 min human action)
- [ ] Run sam_gov_print_contract_monitor.py to baseline current active solicitations
- [ ] Scrape USASpending.gov for past printing contract awardees (prime targets)
- [ ] Generate capability statement template via claude -p from this solicitation's SOW
- [ ] Route 5 identified primes into cold_outbound pipeline with subcontract pitch
- [ ] Add to daily cron: scan + append new opps to GOV_OPPORTUNITIES.csv
- [ ] Wire into existing chain__tendersinfo_comgovernment_contracts_be handoff

## Tooling

```json
{
  "browser": "Playwright MCP for SAM.gov scraping",
  "email": "existing cold_email scripts",
  "content": "claude -p capability statement generator"
}
```
