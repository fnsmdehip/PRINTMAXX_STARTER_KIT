# Growth Plan: ALPHA804,r/SideProject + IndieHackers,https://www.indiehacke

**Created:** 2026-03-20 18:10
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Cross-promote between apps in portfolio (each app promotes 2-3 others via footer/settings)
2. ASO keyword rotation: test 5 keyword sets per app per month using existing ASO_KEYWORDS.csv
3. Portfolio landing page showing all apps as social proof (builds brand, not just individual apps)
4. Reddit/IH case study post: 'I built 100+ micro-apps, here is what I learned' — engagement bait that drives traffic to portfolio

## Budget Tier Strategies

### FREE
Cross-app promotion, ASO optimization, Reddit/IH/Twitter case study posts about portfolio approach, engagement bait converter for content

### LOW
$0-50/mo: Apple Search Ads basic campaigns on top 5 apps, targeted Reddit ads on niche subreddits

### MID
$50-200/mo: Micro-influencer reviews of top apps, paid Product Hunt launches for best performers

## Daily Actions

- [ ] Run payment_integrator.py --status to see which apps have Stripe wired
- [ ] Crawl all 114 deployed URLs (DEPLOYMENT_URLS.md) to verify live + check for payment CTAs
- [ ] Score each app: has_payment_link + niche_demand + aso_keyword_volume + deployment_health
- [ ] Top 20 apps: create Stripe payment links via MCP, inject into landing pages
- [ ] Bottom 20 apps: flag for kill review (Capital Genesis kill criteria: <$100 MRR after 60d)
- [ ] Generate portfolio case study content for Reddit/Twitter/IH distribution
- [ ] Add weekly cron to re-run portfolio audit and track MRR per app

## Tooling

```json
{
  "browser": "playwright for URL audit",
  "email": "none",
  "content": "engagement_bait_converter.py for portfolio case study content"
}
```
