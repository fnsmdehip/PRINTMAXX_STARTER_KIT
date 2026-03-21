# Growth Plan: Went from $0 to $1k MRR. If I started my SaaS over, here's e

**Created:** 2026-03-20 18:35
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0 direct (selection filter improves app factory hit rate by ~15-20%, compounding across all future app launches)

---

## Tactics

1. Validate recurring painpoint via Reddit/Twitter complaint frequency before building
2. Use app store review mining to confirm users mention the problem recurring weekly/monthly

## Budget Tier Strategies

### FREE
Mine Reddit threads and app store reviews for recurring complaint patterns. Cross-reference with existing REDDIT_PAIN_POINTS.csv to flag apps solving recurring problems.

### LOW
$0-20/mo on targeted Reddit ads testing painpoint messaging before building

### MID
$50-100/mo on Google Ads keyword tests measuring search volume for recurring problem queries

## Daily Actions

- [ ] Add recurring_painpoint_score field to APP_FACTORY_METHODS.csv scoring rubric
- [ ] Update app_factory_command_center.py --refresh to weight recurring problems +1.5 in composite score
- [ ] Tag existing 8 built apps as recurring vs one-time to validate the filter retroactively
- [ ] Add to alpha_auto_processor routing: any method mentioning 'recurring revenue' or 'subscription' auto-routes to APP venture

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
