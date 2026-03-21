# Growth Plan: [GOV CONTRACT] BJA PEER REVIEW SUPPORT SERVICES (deadline: 2

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $50K-500K/contract (1-3 contracts/yr realistic, discounted 60% = $20K-200K/yr)

---

## Tactics

1. Register on SAM.gov as small business (free) — unlocks set-aside contracts worth 23% of all federal spend
2. Pull USASpending.gov data for BJA historical awards to find realistic price-to-win for peer-review services
3. Target IDIQ vehicles and BPAs where one win = recurring task orders without rebidding
4. Use NAICS 541611, 541690, 541990 cross-search to catch all support services solicitations not just peer review
5. Monitor GSA Schedule 541 for faster award vehicles with less competition than open SAM solicitations
6. Mine SAM.gov for expiring contracts (recompetes) — incumbent rarely wins recompetes, best entry point
7. Build past-performance log from ANY completed project to satisfy PP requirements on future bids
8. Target solicitations explicitly waiving past-performance for new entrants or small businesses

## Budget Tier Strategies

### FREE
SAM.gov public API daily scrape + Claude proposal drafting + USASpending.gov historical price research + free SAM registration. Full pipeline costs $0. This entry alone (BJA deadline 2026-04-17) is actionable immediately.

### LOW
$0-50/mo — GovWin IQ basic tier or BidSync for pre-solicitation intel. Expands pipeline 3x with early warning on upcoming solicitations before SAM posting.

### MID
$50-200/mo — Deltek GovWin or Bloomberg Government for full procurement history, teaming partner matching, and incumbent identification. Use for contracts > $250K to justify research spend.

## Daily Actions

- [ ] IMMEDIATE (today): Manually review BJA solicitation at SAM.gov for 'Peer Review Support Services' deadline 2026-04-17 — confirm scope, set-aside status, page limit, submission format
- [ ] TODAY: Register on SAM.gov (free, 1h) — required to bid on any federal contract
- [ ] TODAY: Run `python3 AUTOMATIONS/gov_contract_monitor.py --init` to scaffold the script and do first SAM.gov API pull
- [ ] DAY 2: Pull USASpending.gov for past BJA peer-review awards to estimate price-to-win range
- [ ] DAY 2-3: claude -p generates capability statement and proposal outline for BJA solicitation
- [ ] DAY 4-7: Human reviews and decides go/no-go on submission (hard deadline 2026-04-17)
- [ ] ONGOING: cron 0 7 * * * runs gov_contract_monitor.py daily, feeds LEDGER/GOV_OPPORTUNITIES.csv, surfaces 7-day deadline alerts

## Tooling

```json
{
  "browser": "Playwright MCP (SAM.gov fallback scrape)",
  "email": "custom cold email scripts (target existing BJA awardees for teaming)",
  "content": "claude -p for proposal drafting",
  "data": "USASpending.gov API (free, no key) for price comps",
  "tracking": "LEDGER/GOV_OPPORTUNITIES.csv"
}
```
