# Growth Plan: [GOV CONTRACT] THIS TIME AND MATERIALS (T&M) TASK ORDER IS I

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $5K-$50K/contract win as subcontractor. 1-2 wins/quarter realistic once pipeline running. Monthly avg: $2K-$8K.

---

## Tactics

1. Enhance existing chain__tendersinfo_comgovernment_contracts_be with editorial-specific NAICS codes
2. Monitor GSA Multiple Award Schedules (MAS) Schedule 36 — professional services for recurring subcontracting opportunities
3. Set up SAM.gov saved search + email alert as backup to the scraper
4. Target 8(a) set-aside primes — they actively seek subcontractors to fulfill T&M contracts
5. Use USASpending.gov to find agencies with historically high editorial/publication spend — proactive BD before solicitations drop
6. Build a one-page agency-specific capability statement factory: auto-customize for each agency's mission language

## Budget Tier Strategies

### FREE
SAM.gov API (free, no key needed for basic search). claude -p for proposal gen. Manual email outreach to prime contacts found via SAM entity search. Target 5 primes/week.

### LOW
$20-50/mo — GovWin IQ free trial for pipeline visibility. Targeted LinkedIn outreach to BD managers at prime contractors holding editorial/comms IDIQs.

### MID
$50-200/mo — GovWin IQ subscription ($99/mo) for pre-solicitation intel. Allows 2-3 week head start on competitors. ROI: one subcontract win pays 6 months of subscription.

## Daily Actions

- [ ] Enhance chain__tendersinfo_comgovernment_contracts_be with editorial NAICS codes (519130, 541830, 711510, 541922)
- [ ] Build sam_gov_editorial_contract_monitor.py: SAM.gov API query + USASpending prime lookup + qualification scoring
- [ ] Create gov_editorial_cap_statement.md template in AUTOMATIONS/gov_contracts/templates/
- [ ] Wire claude -p proposal generator: takes solicitation text → outputs cap statement + 1-page proposal outline in <90s
- [ ] Add cron entry: 0 7 * * * (daily 7 AM SAM.gov check)
- [ ] Append qualified opps to LEDGER/GOV_OPPORTUNITIES.csv with status tracking
- [ ] Log first run results, verify JSON output before declaring operational

## Tooling

```json
{
  "browser": "playwright (SAM.gov entity search, USASpending)",
  "email": "custom cold email script (existing AUTOMATIONS/cold_email_sender.py)",
  "content": "claude -p (capability statement + proposal outline generation)"
}
```
