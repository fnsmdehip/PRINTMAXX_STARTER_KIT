# Growth Plan: [ACQUISITION] NEW PARTY GAME MOBILE APP : WHO PICKED WHO

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $150-600/mo per variant (AdMob + $2.99 premium pack IAP). 3 variants = $450-1800/mo portfolio.

---

## Tactics

1. Launch 3 audience variants simultaneously: bachelorette, office party, college dorm — each with own ASO keywords and landing page
2. Viral loop: app mechanics require 3+ players = each install generates 2-4 additional organic installs
3. TikTok UGC: film real gameplay reactions with embarrassing/funny moments — party game content performs exceptionally well
4. Reddit seeding: r/bacheloretteparty, r/weddingplanning, r/CollegeLife, r/partygames, r/boardgames
5. Cross-promote within existing app portfolio (PrayerLock, SoberStreak install base = faith variant audience)

## Budget Tier Strategies

### FREE
3 audience variants with ASO targeting occasion keywords (bachelorette party games, office party games, college drinking games alternatives). Seed gameplay clips to TikTok + Reddit. Cross-link with existing 47 live apps.

### LOW
$10-30/mo Apple Search Ads Basic on 'party game' + 'bachelorette game' keywords. Boost 1-2 TikTok gameplay clips per variant.

### MID
$50-150/mo micro-influencer seeding via bachelorette and college lifestyle TikTokers, Facebook interest targeting for party/event planners

## Daily Actions

- [ ] Scrape App Store top 50 party games: extract mechanics, pricing tiers, review sentiment, audience signals via Playwright
- [ ] Identify 3 underserved segments with weak existing apps: bachelorette (strong intent, weak supply), office party (corporate budgets), faith-based (zero competition)
- [ ] Fork base app template, inject audience-specific question bank (200+ questions per variant generated via claude -p)
- [ ] Wire RevenueCat: free tier (20 questions) + premium pack unlock at $2.99 (200 questions + categories)
- [ ] Wire AdMob interstitial between game rounds (natural break = high completion)
- [ ] Build landing page per variant (surge.sh), each with audience-specific copy and App Store link
- [ ] Generate 5 TikTok gameplay hooks per variant via engagement_bait_converter.py, route to posting queue

## Tooling

```json
{
  "browser": "playwright (App Store competitive scraping)",
  "email": "none",
  "content": "engagement_bait_converter.py for gameplay reaction hooks"
}
```
