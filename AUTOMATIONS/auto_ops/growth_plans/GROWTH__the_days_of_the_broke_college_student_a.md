# Growth Plan:  the days of the broke college student are going to be gone 

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. cross-post clips across TikTok/Reels/Shorts simultaneously
2. engagement warm accounts with college hashtags before posting
3. reply-bait on viral college finance content with value-add clips

## Budget Tier Strategies

### FREE
Organic cross-posting, hashtag optimization for college niches (#sidehustle #collegemoney #brokecollegestudent), engagement warming on trending college finance posts, link-in-bio affiliate rotation

### LOW
$10-30/mo boosting top-performing clips on TikTok/IG to college-age demo (18-24)

### MID
$50-150/mo micro-influencer seeding — send clips to college finance creators for duet/stitch

## Daily Actions

- [ ] Wire existing auto_clip_pipeline output to affiliate_link_matcher (match clip topic to best affiliate offer from LEDGER/ASO_KEYWORDS.csv and affiliate pages)
- [ ] Add affiliate link injection to clip description templates in CONTENT/social/posting_queue/
- [ ] Add college-age niche keywords to content_trend_pipeline.py topic scanner
- [ ] Schedule DAG at 7:30 AM daily via cron
- [ ] Track clip+affiliate conversion in LEDGER/CONTENT_TO_REVENUE_MAP.csv

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "auto_clip_pipeline + content_repurposer.py + affiliate pages"
}
```
