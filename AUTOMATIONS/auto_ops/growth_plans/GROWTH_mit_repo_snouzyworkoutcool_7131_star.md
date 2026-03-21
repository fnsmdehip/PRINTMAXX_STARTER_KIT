# Growth Plan: MIT repo: Snouzy/workout-cool (7131 stars, TypeScript)

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Submit each fitness variant to ProductHunt on Tuesdays (peak traffic day)
2. Post in r/fitness, r/bodyweightfitness, r/running, r/yoga with app link in bio — organic, no spam
3. SEO longtail: '[exercise]-streak tracker app', 'free workout-cool alternative', 'best [exercise] habit app'
4. Open a GitHub issue or PR on workout-cool repo to get backlink + contributor visibility from 7K+ star audience
5. Cross-link all fitness streak variants from each other (internal network effect, boosts all app SEO)

## Budget Tier Strategies

### FREE
ProductHunt launches, Reddit organic in fitness subs, cross-link network across all streak variants, GitHub engagement on workout-cool for organic exposure, SEO pages targeting 'workout-cool alternatives'

### LOW
$20-50/mo Apple Search Ads basic targeting '[exercise] tracker' keywords; small Reddit promoted posts in r/fitness

### MID
$50-200/mo micro-influencer seeding (fitness creators 10K-100K subs on YouTube/TikTok), Pinterest fitness board automation via content_factory, TikTok fitness niche short-form with app CTA

## Daily Actions

- [ ] Clone workout-cool repo locally and run component analysis to map reusable modules
- [ ] Extract: workout exercise database, streak tracking logic, progress visualization components
- [ ] Generate 6 white-label variant configs: cycling-streak, pushup-streak, yoga-streak, HIIT-streak, plank-streak, water-streak
- [ ] Swap branding, color palette, and exercise content per variant using base template pattern
- [ ] Wire RevenueCat IAP + AdMob to each variant from MONEY_METHODS/APP_FACTORY base template
- [ ] Deploy web versions to surge.sh and add all URLs to OPS/DEPLOYMENT_URLS.md
- [ ] Create Stripe payment links for premium tier of each variant; update OPS/STRIPE_PRODUCTS.md
- [ ] Generate SEO landing pages targeting '[exercise] streak tracker' and 'workout-cool alternative' longtails
- [ ] Add weekly Monday 7AM cron to check workout-cool for new features worth backporting

## Tooling

```json
{
  "browser": "playwright",
  "email": "none",
  "content": "content_factory"
}
```
