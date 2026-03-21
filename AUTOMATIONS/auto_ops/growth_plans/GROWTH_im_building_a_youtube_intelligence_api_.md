# Growth Plan: I'm building a YouTube Intelligence API because vidIQ and Tu

**Created:** 2026-03-20 18:35
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. Post in YouTube creator subreddits showing the API gap with working examples
2. Reply to vidIQ/TubeBuddy complaint threads with free tier link
3. Create dev.to and Medium tutorials showing API usage for common YouTube analytics tasks
4. Seed in indie hacker communities as a vibe-coded API product story

## Budget Tier Strategies

### FREE
Reddit posts in r/SideProject r/youtube r/webdev, dev.to tutorials, reply to vidIQ complaint threads, Product Hunt launch, Twitter threads about the API gap

### LOW
$20-40/mo RapidAPI promoted listing, targeted Reddit ads in creator subs

### MID
$100-150/mo sponsor a YouTube creator tools newsletter, dev influencer seed kits

## Daily Actions

- [ ] Validate demand: search RapidAPI for existing YouTube intelligence APIs, count subscribers on similar APIs
- [ ] Build FastAPI service with 4 core endpoints using YouTube Data API v3 free tier
- [ ] Add caching layer (SQLite) to stay within 10K daily quota
- [ ] Deploy to Railway free tier with custom domain
- [ ] List on RapidAPI with freemium tiers: Free (100 calls/day), Basic $9.99 (1K/day), Pro $29.99 (10K/day)
- [ ] Launch distribution: Reddit + Twitter + Product Hunt + dev.to
- [ ] Daily cron refreshes trending data cache at 4 AM

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for launch threads and tutorials"
}
```
