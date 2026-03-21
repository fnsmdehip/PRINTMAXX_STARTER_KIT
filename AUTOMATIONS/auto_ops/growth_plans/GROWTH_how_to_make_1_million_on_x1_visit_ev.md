# Growth Plan: How to make $1 million on X

1) Visit every large creator (>

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Reply to large creators in same niche within 3 min of their posts (algo boost from proximity)
2. Rotate posting times across 3 peak windows (7-9AM, 12-1PM, 6-8PM EST)
3. Use engagement warming protocol: 30 min genuine engagement before each post
4. Cross-post adapted versions to Threads and LinkedIn for compound reach
5. Quote-tweet own post 4-6 hours later with added context to double impressions
6. Build creator list from multiple niches to avoid detection of single-source copying

## Budget Tier Strategies

### FREE
Organic viral replication pipeline — scrape, rewrite, post, engage. Zero cost with Claude Max + existing scrapers. Warm account with genuine replies before posting.

### LOW
$8-16/mo X Premium subscription for Creator Payouts eligibility + longer posts + edit button. Required to monetize impressions directly.

### MID
$50-100/mo for GoLogin multi-account + residential proxies to run 3-5 themed accounts in parallel, each targeting different niches for diversified reach.

## Daily Actions

- [ ] Build creator watchlist: 50 accounts >100K in money/tech/hustle niches
- [ ] Extend twitter_alpha_scraper.py with --top-posts mode (filter by Most Liked, last 7 days)
- [ ] Create viral_content_curator.py: daily scrape → rank → top 10 → Claude rewrite → posting_queue
- [ ] Wire into existing content_factory chain for scheduling and warmup compliance
- [ ] Add engagement phase: auto-generate 3 reply variants per post for first-commenter engagement
- [ ] Cron at 6:30 AM daily, posts queued for 3 optimal windows
- [ ] HUMAN BLOCKER: X Premium subscription needed for Creator Payouts ($8/mo)
- [ ] HUMAN BLOCKER: X account must be active 3+ months with 500+ followers for payout eligibility
- [ ] Track KPIs: impressions per post, engagement rate, follower growth, payout threshold progress

## Tooling

```json
{
  "browser": "playwright_mcp_brave_cookies",
  "email": "none",
  "content": "engagement_bait_converter + content_repurposer + claude_rewrite"
}
```
