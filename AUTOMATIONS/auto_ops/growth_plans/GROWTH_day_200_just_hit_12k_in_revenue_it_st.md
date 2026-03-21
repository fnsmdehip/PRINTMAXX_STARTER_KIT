# Growth Plan: Day 200. Just hit $12k in revenue. It still feels unreal. Ab

**Created:** 2026-03-20 18:35
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Monitor competitor mentions (tydal.co, somiibo, phantombuster) to intercept their leads
2. Track pain-point keywords across r/SaaS, r/microsaas, r/Entrepreneur, r/smallbusiness, r/startups
3. Build karma on 2-3 Reddit accounts via genuine helpful replies before any product mentions
4. Cross-post Reddit insights as Twitter threads (Rule 9 content generation)
5. Use Reddit thread topics as SEO longtail keyword signals for landing pages

## Budget Tier Strategies

### FREE
Organic Reddit monitoring via existing scraper, manual posting from personal account, karma building through genuine value-first replies, cross-pollinate Reddit insights into Twitter content

### LOW
$0-50/mo: Reddit Ads targeting high-intent subreddits with $2-5/day budget, boost top-performing reply threads

### MID
$50-200/mo: Multiple Reddit accounts with aged history, proxy rotation for monitoring at scale, Reddit Ads retargeting site visitors

## Daily Actions

- [ ] Extend reddit_deep_scraper.py with intent-keyword filter layer (20 buying-signal phrases)
- [ ] Add intent scoring function: weight by subreddit size, post recency, comment count, keyword density
- [ ] Create reply template library per product type (streak apps, digital products, services)
- [ ] Wire output to CONTENT/social/posting_queue/reddit_replies.txt for human posting
- [ ] Add dedup tracking in LEDGER/REDDIT_REPLY_LOG.csv to prevent double-posting
- [ ] Schedule 3x daily cron (7am, 1pm, 7pm) to catch fresh threads within golden reply window
- [ ] Track clicks via UTM params on all posted links, feed back to qualifier for model improvement

## Tooling

```json
{
  "browser": "none \u2014 reddit_deep_scraper uses requests JSON API",
  "email": "none",
  "content": "claude -p for reply drafting"
}
```
