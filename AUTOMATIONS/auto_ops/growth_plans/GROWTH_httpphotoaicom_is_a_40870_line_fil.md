# Growth Plan: http://
photoai.com is a 40,870 line file called index.php



**Created:** 2026-03-20 18:35
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-2000/mo

---

## Tactics

1. Ship ugly single-file MVP, iterate on revenue not architecture
2. Cross-post build log to IndieHackers + Twitter for organic distribution
3. Reply to Levels' tweets with our version to draft off his audience
4. Target subreddits where users complain about PhotoAI pricing ($29/mo)

## Budget Tier Strategies

### FREE
Build in public tweets, IndieHackers show posts, reply to competitor threads on Reddit, HN Show posts

### LOW
$0-50/mo for API costs (Claude API for AI processing), rest is organic distribution

### MID
$50-200/mo for targeted Reddit/Twitter ads to competitor keyword searches

## Daily Actions

- [ ] Research PhotoAI feature set and pricing funnel via Playwright scrape
- [ ] Identify 5 underserved AI wrapper niches (AI headshots for specific verticals, AI product photos, AI pet portraits, etc.)
- [ ] Score niches by App Store/Google demand vs existing competition
- [ ] Build single-file MVP using existing app factory template — HTML+JS+Stripe checkout
- [ ] Wire Claude API as backend AI processor (or use free Stable Diffusion API for image gen)
- [ ] Deploy to surge, add to DEPLOYMENT_URLS
- [ ] Generate build-in-public content for distribution
- [ ] Track signups and conversion weekly

## Tooling

```json
{
  "browser": "playwright",
  "email": "none",
  "content": "content_factory"
}
```
