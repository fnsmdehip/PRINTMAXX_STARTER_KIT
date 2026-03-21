# Growth Plan: extracted signal: 95% of affiliates are broke because they d

**Created:** 2026-03-20 18:09
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Comparison landing pages: '[SaaS tool] affiliate program review' targeting affiliates searching for programs — recruit sub-affiliates
2. Content repurpose the CPA-vs-MRR framing as engagement bait threads on X/Reddit to drive traffic to our affiliate review pages
3. Cold email SaaS founders offering to promote their tool in exchange for custom recurring commission tier

## Budget Tier Strategies

### FREE
Audit all 5 current affiliate selections (SEMrush, ConvertKit, Beehiiv, Instantly, Smartlead) — all already recurring, good. Add 3-5 more from PartnerStack/Impact free browse. Create 'best recurring affiliate programs' SEO page to attract sub-affiliates.

### LOW
$0-50/mo: Boost top-performing affiliate comparison page with $20 Reddit/Twitter ads targeting 'affiliate marketing' keywords. A/B test CPA-vs-MRR angle in cold outreach.

### MID
$50-200/mo: Build affiliate program directory site (programmatic SEO, 500+ SaaS program pages) as lead magnet for our own affiliate links embedded in reviews.

## Daily Actions

- [ ] Audit current PRINTMAXX affiliate selections in OPS/AFFILIATE_LINK_SETUP.md — confirm all are recurring commission (they are: SEMrush 40% recurring, ConvertKit 30% recurring, Beehiiv 50% yr1, Instantly tiered, Smartlead lifetime recurring)
- [ ] Build affiliate_mrr_scorer.py that scrapes PartnerStack/Impact/ShareASale public directories for SaaS programs with recurring commissions >20%, ranks by (commission_rate * avg_retention * search_volume)
- [ ] Output top 10 new recurring programs to LEDGER/CREATOR_PROGRAMS.csv with commission_model column
- [ ] Update affiliate landing pages (LANDING/affiliate-pages/) to prioritize highest-LTV recurring programs over any one-time CPA offers
- [ ] Feed CPA-vs-MRR framing to engagement_bait_converter.py for 3 threads + route to posting_queue
- [ ] Add weekly cron (Monday 7 AM) to re-scan and re-rank
- [ ] Wire into existing cold email chain to pitch SaaS founders for custom affiliate deals with higher recurring rates

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "content_factory + engagement_bait_converter"
}
```
