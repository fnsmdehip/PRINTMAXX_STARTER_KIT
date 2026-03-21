# Growth Plan: Rented out my dormant LinkedIn account for B2B outreach ($40

**Created:** 2026-03-21 12:40
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $80-400/mo

---

## Tactics

1. Post 'anyone have a dormant LinkedIn with 500+ connections? I can monetize it for you' in r/SideHustle weekly
2. Cross-sell to existing OUTBOUND venture: offer EAS clients LinkedIn account access as premium tier
3. Use $40/mo pricing signal to price LinkedIn outreach-as-a-service at $150-300/mo (includes account + outreach labor)
4. Build aged account inventory now — even if not renting, having 3-5 warm LinkedIn profiles is infrastructure for cold outbound

## Budget Tier Strategies

### FREE
Reddit/Discord scraping to find account owners. Manual broker intro emails via existing cold email scripts. Zero cost matchmaking.

### LOW
$20-30/mo: Post paid 'WTB LinkedIn accounts' ads in relevant Facebook groups/forums to build supply faster

### MID
$50-150/mo: Buy 2-3 aged accounts outright ($30-80 each) instead of brokering. Rent directly to agencies at $80-120/mo. Net $50-90/mo per account after amortization.

## Daily Actions

- [ ] Wire linkedin_account_broker.py as weekly cron (Monday 8AM) using existing background_reddit_scraper.py pattern
- [ ] Add LinkedIn account rental as supply signal to ALPHA_STAGING auto-approve filter
- [ ] Update EAS venture pricing deck: add 'LinkedIn account access' as $150/mo upsell (validated by $40 rental market)
- [ ] Route qualified supply matches through chain_cold_outbound with broker-specific email template
- [ ] Log brokerage revenue in FINANCIALS/ with Stripe Payment Link for the 25% cut

## Tooling

```json
{
  "browser": "none \u2014 Reddit JSON API + requests",
  "email": "existing cold email scripts in AUTOMATIONS/",
  "content": "none"
}
```
