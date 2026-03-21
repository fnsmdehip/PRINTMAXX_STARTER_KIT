# Growth Plan: P2

**Created:** 2026-03-20 18:10
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. ASO: target 'swimming streak' 'lap counter' 'swim tracker' — zero competition confirmed
2. Cross-promote from existing fitness-streak, hiit-streak, cycling-streak apps via in-app banners
3. Reddit seeding: r/Swimming (318K), r/triathlon (95K), r/openwater, r/masterssswimming — value posts not spam
4. Swimming forum/Facebook group infiltration with genuine streak challenge posts
5. Strava integration angle — swimmers use Strava, mention compatibility in copy

## Budget Tier Strategies

### FREE
ASO keyword optimization for zero-competition swimming terms, Reddit value posts in r/Swimming + r/triathlon, cross-promote from existing streak app family, swimming YouTube comment engagement

### LOW
$10-30/mo Reddit promoted posts in r/Swimming, micro-influencer swim coaches on IG/TikTok for free app review

### MID
$50-150/mo SwimSwam banner ad or newsletter sponsorship, swimming podcast ad reads, TikTok swim content creator collab

## Daily Actions

- [ ] 1. Clone fitness-streak or scripture-streak PWA template from APP_FACTORY/builds/
- [ ] 2. Rebrand: swimming-streak, stroke types (freestyle/backstroke/butterfly/breaststroke), lap counting, pool vs open water modes
- [ ] 3. Add swimming-specific streak metrics: laps per session, total distance, stroke variety
- [ ] 4. Generate landing page with swimming-specific copy targeting 318K community keywords
- [ ] 5. Deploy to swimming-streak.surge.sh
- [ ] 6. Wire Stripe payment link for premium tier ($2.99/mo or $19.99/yr)
- [ ] 7. Submit ASO keywords to LEDGER/ASO_KEYWORDS.csv
- [ ] 8. Generate 3 launch tweets + 1 Reddit value post for r/Swimming
- [ ] 9. Cross-link from all fitness-category streak apps
- [ ] 10. Add to APP_FACTORY priority queue and DEPLOYMENT_URLS.md

## Tooling

```json
{
  "browser": "playwright_for_deployment_testing",
  "email": "none",
  "content": "content_factory_for_launch_tweets_and_reddit_posts"
}
```
