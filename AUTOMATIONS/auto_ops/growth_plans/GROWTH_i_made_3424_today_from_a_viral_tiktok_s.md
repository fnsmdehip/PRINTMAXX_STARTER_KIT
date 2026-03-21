# Growth Plan: I made $3424 Today from a viral tiktok slideshow
which i mad

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $300-1500/mo

---

## Tactics

1. Post 3x/day during peak hours (6-9AM, 12-2PM, 7-10PM EST)
2. First 3 seconds = hook with bold text overlay — completion rate is the algo signal
3. Use trending sounds within 48h of emergence (sound discovery scraper)
4. Engagement warming: comment on 20 related videos before each post
5. Cross-post to IG Reels and YT Shorts for 3x distribution at 0 marginal cost
6. Slideshow format specifically favored by TikTok algo in 2026 (image carousel gets higher save rate)
7. Stacked monetization: Creator Rewards + affiliate links in bio + digital product funnel

## Budget Tier Strategies

### FREE
Organic posting 3x/day, trending sound riding, engagement warming (comment 20/day), cross-platform repurposing to IG Reels + YT Shorts, bio link to existing PRINTMAXX products

### LOW
$20-50/mo TikTok Promote on top-performing slideshows (only boost ones with >5% completion rate organically), CapCut Pro if needed ($8/mo)

### MID
$100-200/mo for TikTok ads driving to product funnels, multi-account operation (3 accounts across niches using GoLogin)

## Daily Actions

- [ ] 1. Create tiktok_slideshow_factory.py — scrapes trending TikTok sounds/formats via Playwright, generates slideshow frames using claude -p for hooks/text + free stock images
- [ ] 2. Wire into existing Remotion video_factory for slideshow assembly (we already have this infra)
- [ ] 3. Add trending sound scraper module (TikTok Creative Center is public, no auth needed)
- [ ] 4. Configure content_repurposer.py to auto-convert each TikTok slideshow → IG Reel + YT Short
- [ ] 5. Add cron 0 7 * * * for daily batch generation (3 slideshows/day)
- [ ] 6. Track in KPI dashboard: daily views, completion rate, follower growth
- [ ] 7. HUMAN BLOCKER: Need TikTok account created and warmed up (7-day warmup protocol before posting)
- [ ] 8. Once 10K followers reached, apply for Creator Rewards Program to unlock revenue

## Tooling

```json
{
  "browser": "playwright for trend scraping",
  "email": "none",
  "content": "remotion + ffmpeg + claude -p for text generation"
}
```
