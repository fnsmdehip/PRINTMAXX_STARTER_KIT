# Growth Plan: [GOV CONTRACT] CONTACT CENTER TIER 1 (CCT1)- THE PURPOSE OF 

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $2-6K/mo staffing placement fees at 15-25% margin on VA sub arrangements with prime contractors

---

## Tactics

1. Query USASpending.gov API (free, no auth) for recent contract awards on NAICS 561422 to surface prime contractor names already winning these deals
2. Cold pitch prime BD teams as staffing sub: bilingual VA agents at 40% below market, ready to onboard in 2 weeks
3. Monitor SAM.gov for subcontracting plan requirements on large awards (contracts >$750K require small business sub plans — prime is motivated to find you)
4. Target DHS/USCIS/SSA/VA specifically — their contact center contracts recur annually with known primes (Maximus, SAIC, Leidos)
5. Register free on SAM.gov as vendor to appear in prime contractor subcontractor searches

## Budget Tier Strategies

### FREE
SAM.gov API (api.sam.gov/prod/opportunities/v2/search, free key) daily scrape for keywords: contact center, tier 1, help desk, USCIS, call center; USASpending.gov API for prime award history; LinkedIn outreach to prime contractor BD directors; cold email scripts to contracting officers on active solicitations

### LOW
$0-50/mo: Hunter.io or Apollo for prime contractor BD team emails; submit capability statement via SAM.gov dynamic small business search listing

### MID
$50-200/mo: GovWin IQ basic tier for pre-solicitation intelligence; LinkedIn InMail to Program Managers at Maximus/Leidos/SAIC contact center divisions

## Daily Actions

- [ ] Build samgov_contract_monitor.py using SAM.gov Opportunities API v2 (free API key at sam.gov/data-services) — search NAICS 561422, 561421, 541519 with keywords 'contact center OR tier 1 OR help desk OR customer support'
- [ ] Filter results: deadline > 45 days, set-aside codes for small business (SBA, 8(a), HUBZone), dollar threshold $50K-$10M, agencies DHS/USCIS/SSA/VA/DoL
- [ ] Query USASpending.gov /api/v2/search/spending_by_award/ on same NAICS codes to extract prime contractor names winning these awards in last 24 months
- [ ] Deduplicate against existing chain__tendersinfo_comgovernment_contracts_be output to avoid reprocessing known primes
- [ ] Route prime contractor company names + BD contact titles to eas_lead_pipeline.py for cold outreach: capability statement + VA staffing offer
- [ ] Wire Monday 7 AM cron to catch weekly SAM.gov posting cycles (most solicitations drop Mon-Wed)

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "none"
}
```
