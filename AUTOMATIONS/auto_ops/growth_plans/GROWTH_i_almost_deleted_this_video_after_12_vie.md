# Growth Plan: I almost deleted this video after 12 views… it ended up bein

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. Repost underperformers to alternate platforms (Reddit→Twitter, Twitter→LinkedIn)
2. Reframe hooks on recycled content using engagement_bait_converter.py
3. A/B test different posting times for recycled content

## Budget Tier Strategies

### FREE
Recycle content across owned accounts with rewritten hooks. Use content_repurposer.py to adapt format per platform. Post recycled content during peak engagement windows (6-9 AM, 12-1 PM, 7-9 PM).

### LOW
$0-20/mo: Use Buffer free tier or scheduling scripts to auto-post recycled content at optimal times across 3+ platforms.

### MID
$50-100/mo: Boost best-performing recycled posts with $2-5 micro-spends on platforms where they show traction signals.

## Daily Actions

- [ ] 1. Add tracking column to posting_queue CSV for post_date and initial_engagement_score
- [ ] 2. Build content_recycler.py that scans posts older than 7 days with below-median engagement
- [ ] 3. Run recycled posts through engagement_bait_converter.py to rewrite hooks
- [ ] 4. Re-queue to posting_queue for different platform or time slot
- [ ] 5. Cron weekly Monday 9 AM to process recycling queue

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + content_repurposer.py + engagement_bait_converter.py"
}
```
