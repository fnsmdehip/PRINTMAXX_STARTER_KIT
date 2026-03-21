# Growth Plan: [r/SaaS] If you're trying to market your project on Reddit, 

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo indirect (engagement → followers → funnel)

---

## Tactics

1. Use 'learn from my mistake' framing as Twitter/LinkedIn hook — outperforms positive case studies by 30-40% CTR
2. Cross-post the anti-pattern insight as a Reddit comment in r/indiehackers, r/entrepreneur (not self-promo — add genuine insight)
3. Feed Reddit marketing lessons into our reddit_engagement_strategy to avoid the same mistakes in our own subreddit marketing

## Budget Tier Strategies

### FREE
Run python3 AUTOMATIONS/engagement_bait_converter.py with this entry to generate 3 contrarian posts for posting_queue. Tag chain_i_spent_4_hours_a_day_on_reddit_to_get_m for context augmentation.

### LOW
N/A — content-only entry, paid amplification not warranted at LOW ROI

### MID
N/A

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --input '[r/SaaS] Reddit marketing mistakes' --format contrarian --count 3
- [ ] Output lands in CONTENT/social/posting_queue/ — review and queue
- [ ] Augment chain_i_spent_4_hours_a_day_on_reddit_to_get_m with anti-pattern notes to improve future Reddit outreach scripts

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
