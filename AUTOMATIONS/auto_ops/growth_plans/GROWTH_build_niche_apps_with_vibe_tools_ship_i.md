# Growth Plan: build niche apps with vibe tools. ship in hours. $456k-$144k

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo

---

## Tactics

1. Product Hunt launch per app (free, high-signal traffic)
2. Build-in-public Twitter threads with real revenue screenshots
3. Reddit r/SideProject r/indiehackers show posts
4. Cross-pollinate: each app links to other apps in footer (portfolio flywheel)
5. ASO keyword optimization via existing ASO_KEYWORDS.csv pipeline

## Budget Tier Strategies

### FREE
Product Hunt launches, Reddit show posts, Twitter build-in-public threads, cross-linking between apps, ASO optimization, HN Show posts

### LOW
$20-50/mo on targeted Reddit/Twitter ads for highest-MRR app, micro-influencer seeding in niche communities

### MID
$50-200/mo on Google Ads for high-intent keywords (e.g. 'flight simulator app', 'prayer tracker app'), retargeting pixels on all landing pages

## Daily Actions

- [ ] Wire vibe_app_niche_scanner.py into existing app_factory_autopilot.py pipeline — adds niche scoring weighted by monetization proof
- [ ] Add speed constraint to app factory: 4hr max build time per app, skip anything requiring >4hrs
- [ ] Enhance APP_FACTORY_METHODS.csv with new niche candidates from this alpha (flight sim, chat widget, trend aggregator, link-in-bio tool)
- [ ] Wire Stripe payment links into ALL existing 47 deployed apps that lack them (biggest gap — apps exist but no payment path)
- [ ] Add weekly cron (Monday 7AM) to scan for new niche opportunities and queue top 3 for build
- [ ] Generate 3 tweets + 1 thread from this build cycle per Rule 9

## Tooling

```json
{
  "browser": "playwright for PH/Reddit posting",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
