# Growth Plan: I tracked which marketing channels actually make money vs ju

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Shift digital product promotion heavily to Reddit (r/Entrepreneur, r/SideProject, r/IMadeThis) — 6.25% conversion vs 0% on Twitter
2. Use IndieHackers Show/launches for every new product — 4.5% conversion rate
3. Twitter stays for brand/audience building but NOT direct product links — use it for funnel top only
4. Add UTM params to every link across all 47 deployed sites to track channel attribution
5. Create channel-specific landing page variants (Reddit users respond to technical proof, IH users to build logs)
6. Cross-post product launches to Dev.to, HN Show, and niche subreddits simultaneously

## Budget Tier Strategies

### FREE
UTM-tagged links on all organic posts, Reddit/IH/Dev.to launches, channel performance tracking via access logs, shift posting ratio to 3:1 Reddit:Twitter for sales content

### LOW
$0-50/mo: Boost top Reddit posts via awards, ProductHunt ship page, targeted subreddit cross-posts with A/B tested titles

### MID
$50-200/mo: Reddit ads targeting competitor subreddits, IH sponsorship slots, retargeting pixels on high-converting channel landing pages

## Daily Actions

- [ ] Build channel_roi_tracker.py: reads all deployed product URLs from DEPLOYMENT_URLS.md, generates UTM-tagged variants per channel (reddit, indiehackers, twitter, devto, hn, linkedin, medium)
- [ ] Create lightweight redirect tracker (Python script serving 302 redirects that logs channel + timestamp to CSV) OR parse Surge access logs if available
- [ ] Update all posting_queue templates to use UTM-tagged links by default
- [ ] Add conversion tracking: match UTM source to any payment event (Stripe webhook or manual log)
- [ ] Weekly cron (Monday 7 AM): aggregate clicks and conversions by channel, output LEDGER/CHANNEL_ROI_WEEKLY.csv
- [ ] Auto-adjust CONTENT/social/distribution weights: channels with >3% conversion get 2x posting frequency, channels with 0% conversion over 100+ clicks get flagged for review
- [ ] Immediate action: for all 16 Gumroad draft products, prepare Reddit and IndieHackers launch posts FIRST (not Twitter)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + posting_queue channel weighting"
}
```
