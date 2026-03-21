# Growth Plan:  my latest saas-app: iso weather. built and launched in 3 we

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo per utility app, $200-1000/mo portfolio of 5+

---

## Tactics

1. Cross-promote utility apps from existing 47 deployed streak apps via in-app banners
2. ProductHunt launch with maker profile (blocked on human account creation)
3. Reddit posts in r/SideProject r/webdev r/InternetIsBeautiful for each launch
4. SEO longtail pages: 'best [niche] app 2026' programmatic pages

## Budget Tier Strategies

### FREE
Cross-promote from existing 47 apps, Reddit/HN organic posts, ProductHunt launch, Twitter build-in-public threads, app directory submissions

### LOW
$10-30/mo on targeted Reddit/Twitter ads for highest-performing utility app

### MID
$50-100/mo on micro-influencer reviews in niche communities (e.g. photography forums for a photographer weather app)

## Daily Actions

- [ ] 1. Add utility-app template to APP_FACTORY (fork streak-app base, swap streak logic for API-driven data display)
- [ ] 2. Create niche scanner: scrape App Store utility category for apps with bad ratings but high downloads (opportunity signal)
- [ ] 3. Pick first niche that is NOT weather (too competitive) — target: unit converters, tide trackers, air quality, UV index, pollen count
- [ ] 4. Generate PWA + landing page from template, wire Stripe payment link for premium tier
- [ ] 5. Deploy to surge, run ASO keyword optimization, submit to 10 launch directories
- [ ] 6. Generate content: 3 tweets + 1 build-in-public thread + 1 Reddit post
- [ ] 7. Add weekly cron (Monday 7 AM) to scan for next utility niche and queue build sprint

## Tooling

```json
{
  "browser": "playwright_mcp",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
