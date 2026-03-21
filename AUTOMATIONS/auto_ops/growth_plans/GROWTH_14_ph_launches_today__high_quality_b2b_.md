# Growth Plan: 14 PH launches today - HIGH quality B2B leads. 48h outreach 

**Created:** 2026-03-21 11:41
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo

---

## Tactics

1. Personalize email body with the product's specific tagline and one concrete use case for our offer — generic congrats get ignored on launch day
2. Send within first 6 hours of launch detection (highest founder energy window)
3. Follow-up sequence: day 3 (light check-in), day 7 (different angle — user research ask, not sales)
4. Cross-reference PH maker profile with Twitter/LinkedIn for multi-channel touch
5. For top-voted launches (500+ votes), manually craft email — worth 10 minutes
6. Track which B2B categories convert best and tighten filter over 30 days

## Budget Tier Strategies

### FREE
PH public API scrape daily, claude -p personalization, self-hosted cold email via cold_email_2026.py, manual follow-up for top 5 leads/day

### LOW
$0-50/mo — Hunter.io free tier for email enrichment (25/mo free), Instantly warm-up pool to improve deliverability

### MID
$50-200/mo — Instantly paid ($37/mo) for full send queue management + analytics, add LinkedIn DM via PhantomBuster for dual-channel outreach on top 3 leads/day

## Daily Actions

- [ ] Verify producthunt_scraper.py exists and PH API endpoint is functional — curl test
- [ ] Add B2B category filter + founder email extraction to producthunt_scraper.py
- [ ] Wire output CSV to cold_email_2026.py --input flag with 48h timestamp guard
- [ ] Add LEDGER/PH_OUTREACH_LOG.csv dedup check before send
- [ ] Install cron: 30 6 * * * python3 AUTOMATIONS/producthunt_b2b_outreach.py
- [ ] Add KPI row to OPS/KPI_DASHBOARD.md: PH outreach sent/replied/converted daily
- [ ] Run once manually, verify 5+ emails generated with personalized content before scheduling

## Tooling

```json
{
  "browser": "playwright (email enrichment fallback only)",
  "email": "cold_email_2026.py (self-hosted)",
  "content": "claude -p for personalization"
}
```
