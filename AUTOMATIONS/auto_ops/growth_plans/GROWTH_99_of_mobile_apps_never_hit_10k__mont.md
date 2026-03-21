# Growth Plan: 99% of mobile apps never hit $10k / month.

My last app hit 

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo (47 live apps at avg $10-65/mo each after optimization — Phase 1 target: 5 apps x $200/mo = $1000/mo)

---

## Tactics

1. ASO keyword refresh: scrape top 5 competitors per app category, extract keywords not in our metadata, inject into app description
2. Review velocity: add in-app review prompt after 3rd session or first streak milestone — automate via app build templates
3. Cross-promo: wire banner between all apps in same niche (faith apps cross-promote each other, streak apps cross-promote each other)
4. Paywall audit: check if each app has a paywall — 12 of 47 apps likely have none — wire Stripe payment link or RevenueCat IAP
5. Push notification cadence: apps without push notifications miss 40-60% re-engagement — add via service worker for PWAs
6. App Store featured screenshot A/B: generate 3 screenshot variants per app using image_factory, submit to TestFlight users first

## Budget Tier Strategies

### FREE
ASO metadata rewrites using claude -p + competitor keyword scraper. Cross-promo banners between existing apps. Review prompt injection into app builds. Push notification drip via Firebase (free tier, 10K/mo). Engagement bait thread on exact framework.

### LOW
$10-30/mo Apple Search Ads on 2-3 highest-potential apps using exact-match keywords from ASO audit. $0-20/mo Firebase Blaze for push beyond free tier.

### MID
$50-100/mo targeted UA on top-performing app creative. $20-50/mo Sensor Tower or AppFollow for live ASO rank tracking. Micro-influencer seeding ($30-50 per creator) in faith/fitness niches.

## Daily Actions

- [ ] Playwright MCP: fetch https://x.com/StevenCravotta/status/1955705493285990851 — extract full numbered tactic list
- [ ] Parse tactics into structured checklist: ASO, paywall, push notifications, review prompt, cross-promo, pricing test, retention hook
- [ ] Load all 47 apps from OPS/DEPLOYMENT_URLS.md + MONEY_METHODS/APP_FACTORY/builds/
- [ ] For each app: score against checklist, flag top 3 missing tactics, estimate revenue lift per gap
- [ ] Write OPS/APP_OPTIMIZATION_QUEUE.md sorted by estimated_lift desc — top 10 apps get immediate action
- [ ] Wire top 3 quick wins automatically: inject review prompt template, add cross-promo banner, add Stripe payment link if missing
- [ ] Generate 3 tweets + 1 thread via engagement_bait_converter.py on the $0-to-$10k app framework
- [ ] Add weekly cron: 0 7 * * 1 — re-audit portfolio as apps improve
- [ ] Update KPI_DASHBOARD.md with per-app MRR tracking row

## Tooling

```json
{
  "browser": "Playwright MCP for thread fetch",
  "analytics": "firebase (existing MCP)",
  "monetization": "RevenueCat (existing REVENUECAT_API_KEY) + Stripe",
  "aso": "custom scraper against App Store search API",
  "content": "engagement_bait_converter.py"
}
```
