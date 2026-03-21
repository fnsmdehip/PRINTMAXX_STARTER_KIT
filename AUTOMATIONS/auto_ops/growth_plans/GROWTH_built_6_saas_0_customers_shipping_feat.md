# Growth Plan: Built 6 SaaS, 0 customers: shipping features is safe, talkin

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct (process improvement) but redirects effort toward apps with $200-2000/mo potential by killing zero-demand builds early

---

## Tactics

1. Run validation on ALL 47 existing deployed apps to rank by demand signals — focus monetization effort on top 5 instead of building more
2. Use Reddit pain point data already in LEDGER to score existing apps against real user complaints
3. Post 'would you use X?' polls on relevant subreddits before any new app build — free demand validation
4. Check App Store reviews of competitors for feature gaps — validates demand without talking to anyone

## Budget Tier Strategies

### FREE
Mine existing REDDIT_PAIN_POINTS.csv + ASO_KEYWORDS.csv + COMPETITIVE_INTEL.csv for demand signals on current apps. Post validation polls on Reddit. Use App Store review scraping for competitor pain points.

### LOW
$0-50/mo: Run Google Ads keyword planner for search volume validation. Small Reddit ad tests ($5/app) to measure click-through as demand proxy.

### MID
$50-200/mo: Smoke test landing pages with $10-20 ad spend per app concept. Measure email signups as pre-sale validation before building.

## Daily Actions

- [ ] Create app_factory_validation_gate.py that scores app ideas on 5 demand signals: Reddit mentions, ASO search volume, competitor revenue, existing leads, trending signals
- [ ] Wire as pre-build hook in app_factory_autopilot.py — blocks builds scoring below 6/10
- [ ] Run validation retroactively on all 47 deployed apps to create priority ranking for monetization focus
- [ ] Update app_factory_priority_queue.json to weight demand validation score heavily
- [ ] Add daily cron to re-score app pipeline against fresh Reddit/ASO data
- [ ] Feed top-5 validated apps into payment integration pipeline (Stripe product creation) instead of building app #48

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
