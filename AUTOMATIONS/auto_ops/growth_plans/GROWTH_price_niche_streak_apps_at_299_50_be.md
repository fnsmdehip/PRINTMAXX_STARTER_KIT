# Growth Plan: Price niche streak apps at $2.99 (50% below Streaks $5.99). 

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo across portfolio (20-100 paid downloads/mo at $2.99 across 8+ apps, Apple takes 30%)

---

## Tactics

1. Price anchor in all ASO descriptions: 'Half the price of Streaks — same features'
2. Reddit posts in r/iosapps r/productivity showing price comparison screenshots
3. App Store keyword targeting: 'cheap habit tracker', 'affordable streak app', 'streaks alternative'
4. Cross-promote between streak apps: 'Like this? Try our other $2.99 streak apps'
5. Review request automation at day 7 streak milestone to boost ratings at launch price

## Budget Tier Strategies

### FREE
ASO price anchoring in descriptions, cross-app promotion banners, Reddit/HN comparison posts, review request automation at streak milestones

### LOW
$20-40/mo Apple Search Ads on 'streaks alternative' and 'cheap habit tracker' keywords — low CPA at $2.99 price point

### MID
$100/mo targeted Apple Search Ads on competitor brand terms (Streaks, Habitica, Productive) with price-undercut messaging

## Daily Actions

- [ ] 1. Scrape current competitor pricing: Streaks, Habitica, Productive, Done, Habit Minder on App Store
- [ ] 2. Create/update Stripe price objects to $2.99 for all streak apps with premium tiers
- [ ] 3. Bulk update all 47 deployed streak app landing pages: price display, CTA copy, comparison tables
- [ ] 4. Update ASO metadata in App Store Connect: inject price-anchored keywords and subtitle
- [ ] 5. Generate 5 Reddit/HN comparison posts: price vs feature matrix of paid habit trackers
- [ ] 6. Deploy updated landing pages via surge
- [ ] 7. Set weekly cron to re-scrape competitor prices and alert on changes
- [ ] 8. Add KPI row: track weekly install→paid conversion at $2.99 price point

## Tooling

```json
{
  "browser": "playwright for App Store price scraping",
  "email": "none",
  "content": "content_factory for comparison posts"
}
```
