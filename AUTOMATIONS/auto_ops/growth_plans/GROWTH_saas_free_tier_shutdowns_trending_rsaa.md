# Growth Plan: SaaS free tier shutdowns trending (r/SaaS trending post). Us

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. SEO longtail: '[SaaS name] free alternative 2026' pages auto-generated per shutdown event
2. Reddit reply drops: helpful replies in shutdown threads linking our $1.99 alternative
3. Twitter thread: 'X just killed their free tier. Here are $2 alternatives that do the same thing'
4. Cross-post comparison content to r/selfhosted, r/degoogle, r/privacy
5. HN Show posts: 'I built a $2 alternative to [SaaS] after they killed their free tier'

## Budget Tier Strategies

### FREE
SEO comparison pages auto-deployed, Reddit reply templates in shutdown threads, Twitter threads on each shutdown event, cross-posting to r/selfhosted and r/degoogle

### LOW
$10-30/mo boosting best-performing comparison posts on Reddit/Twitter, micro-influencer seeding with free app codes

### MID
$50-100/mo targeted Google Ads on '[SaaS name] alternative' keywords during peak shutdown traffic windows

## Daily Actions

- [ ] Create free_tier_killer_scanner.py that monitors r/SaaS, r/selfhosted, HN for shutdown/pricing-change keywords
- [ ] Build matching engine: map detected SaaS categories to our existing app factory catalog (streak apps, productivity, faith, fitness)
- [ ] Create comparison landing page template: '[SaaS] just killed free tier → try [our app] for $1.99'
- [ ] Wire into content pipeline: each detected event → 3 tweets + 1 Reddit reply template + 1 landing page
- [ ] Add to existing reddit_deep_scraper.py keyword list: 'free tier', 'shutting down', 'price increase', 'removing free plan'
- [ ] Deploy comparison pages to surge.sh under /vs/ path pattern for SEO
- [ ] Schedule cron 2x daily (7AM scan for overnight announcements, 7PM for day announcements)
- [ ] Log all events to LEDGER/FREE_TIER_KILLER_EVENTS.csv for trend tracking

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
