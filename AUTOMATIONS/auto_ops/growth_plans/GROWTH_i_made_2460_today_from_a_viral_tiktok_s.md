# Growth Plan: I made $2460 Today from a viral tiktok slideshow
which liter

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $300-1500/mo

---

## Tactics

1. Post slideshows at peak TikTok hours (7-9 AM, 12-2 PM, 7-10 PM EST) for completion rate boost
2. Use hook-in-first-slide pattern: controversial stat or question that forces swipe
3. Cross-post slideshows as IG carousels and Twitter image threads for 3x distribution from same asset
4. Engagement warming: like/comment on 20 related videos before posting to seed algorithm
5. Stitch trending videos with slideshow response format for discovery page placement

## Budget Tier Strategies

### FREE
Organic posting 3x/day across 3 niches, cross-post to IG/Twitter, engagement warming loops, trending audio matching, completion-rate-optimized slide count (5-7 slides sweet spot)

### LOW
$20-40/mo TikTok Promote on top-performing slideshows only (boost winners, not losers), micro-influencer reposts via DM barter

### MID
$100-150/mo systematic Promote campaigns on all 3 niche accounts + UGC-style slideshows via AI avatar tools

## Daily Actions

- [ ] Wire tiktok_slideshow_generator.py into existing content factory DAG
- [ ] Use image_factory templates to render text-on-image slides (zero cost, Playwright screenshot)
- [ ] Source hooks from ALPHA_STAGING content-tagged entries + trending TikTok sounds/formats
- [ ] Generate 3 slideshows/day (1 per niche: faith, fitness, tech) — 5-7 slides each
- [ ] Queue output to CONTENT/social/posting_queue/ with platform tags
- [ ] Link to existing faceless content chain for account management and posting SOP
- [ ] Track Creator Rewards payout + affiliate link clicks as KPI
- [ ] BLOCKER: TikTok account creation still requires human action (see ACCOUNT_CREATION_NOW.md)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "image_factory (Playwright HTML-to-image) + content_multiplier.py + existing posting queue"
}
```
