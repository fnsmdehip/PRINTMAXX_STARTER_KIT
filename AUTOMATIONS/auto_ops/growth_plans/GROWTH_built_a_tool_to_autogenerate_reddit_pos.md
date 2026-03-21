# Growth Plan: Built a tool to auto-generate Reddit posts from our blog con

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Reddit karma warming: comment value-add in target subs before posting (existing warmup protocol)
2. Subreddit-specific tone matching: r/MicroSaas wants technical builds, r/Entrepreneur wants revenue numbers
3. Cross-post timing: stagger same content across 3-4 subs over 48h to avoid spam detection
4. Engagement seeding: ask a genuine question at end of each post to drive comments (Reddit algo rewards comment velocity)

## Budget Tier Strategies

### FREE
Repurpose existing content via claude -p, post manually from warmed account, engage in comments for 10min post-publish, use content_repurposer.py for format adaptation

### LOW
$0-20/mo for Reddit premium (removes ads, subtle credibility signal) + potential boost via awarded posts in niche subs

### MID
$50-100/mo for multiple warmed Reddit accounts via GoLogin + residential proxies for higher volume posting across sub-niches

## Daily Actions

- [ ] Wire blog_to_reddit_repurposer.py to scan CONTENT/ and DIGITAL_PRODUCTS/ for recent content pieces
- [ ] Use claude -p to rewrite each piece into Reddit-native format (strip self-promo, add discussion hooks, match sub tone)
- [ ] Output to CONTENT/social/posting_queue/ with subreddit tags and optimal posting times
- [ ] Add cron entry: 0 7 * * 1,3,5 (MWF mornings, peak Reddit engagement)
- [ ] Human pastes queued posts when Reddit account is warmed (ACCOUNT BLOCKER still active)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_repurposer.py + engagement_bait_converter.py + claude -p"
}
```
