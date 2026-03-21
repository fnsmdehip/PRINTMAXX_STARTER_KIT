# Growth Plan: $350 in ads across X, TikTok and Instagram. Only one platfor

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct (intelligence entry — prevents $200+/mo ad waste when budget unlocks, routes future spend to 4.7x better platform)

---

## Tactics

1. Use this data as content: 'We analyzed $350 in ads — here's why Instagram crushed X and TikTok' thread
2. Instagram organic residual: even $50 test campaign seeds the algorithm for continued free reach
3. Anti-pattern: avoid X/TikTok paid ads for SaaS at low budget — misclick rates too high
4. When budget unlocks: Instagram retargeting on signup page visitors (cheapest warm audience)

## Budget Tier Strategies

### FREE
Use this intel to inform organic content strategy — double down on Instagram Reels over X/TikTok. Create 3 posts breaking down these real ad numbers (engagement bait: real data posts outperform advice posts). Post the breakdown on r/buildinpublic and r/SaaS for organic reach.

### LOW
$50-100 Instagram-only test campaigns targeting exact niche audience. Track organic residual traffic 7-14 days post-campaign. Never split budget across X/TikTok until Instagram CPA is proven at scale.

### MID
$150-200/mo Instagram-only with retargeting pixel. A/B test carousel vs Reels ads. Use organic residual as free multiplier — each campaign seeds 1-2 weeks of continued traffic.

## Daily Actions

- [ ] Log platform performance data: Instagram CPA=$21.43/signup, X CPA=$100/signup, TikTok=infinite (0 signups)
- [ ] Update MARKETING_CHANNELS_MASTER.csv with ad platform routing rules: Instagram priority 1, X deprioritize, TikTok avoid for SaaS
- [ ] Record organic residual insight: Instagram continues driving traffic after campaign ends — factor into true ROI calc
- [ ] Generate 3 content pieces from this data (real numbers = high engagement): thread, contrarian take on TikTok ads, Instagram hack post
- [ ] Route to engagement_bait_converter.py for posting queue
- [ ] Add weekly cron to check if ad budget has been allocated — auto-route to Instagram when it does

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
