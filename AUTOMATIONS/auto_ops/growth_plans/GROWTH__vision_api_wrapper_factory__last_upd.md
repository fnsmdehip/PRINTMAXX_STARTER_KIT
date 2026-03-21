# Growth Plan: # Vision API Wrapper Factory  **Last updated:** 2026-02-27 *

**Created:** 2026-03-20 18:10
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo across 10 apps (discounted from stated $5-10K; realistic with organic-only distribution at Phase 0)

---

## Tactics

1. ASO keyword stuffing for '[thing] identifier app' longtails
2. Reddit seeding in niche subreddits (r/whatsthisplant, r/whatsthisbird, r/mycology)
3. TikTok demo videos showing instant identification (high viral potential)
4. Cross-promote between vision apps via in-app recommendations

## Budget Tier Strategies

### FREE
ASO optimization for 'identify [X]' keywords, Reddit organic posts in 20+ identification subreddits, TikTok/Reels demo clips from app, cross-app promotion banners

### LOW
$20-50/mo Apple Search Ads on highest-volume niche (likely plant ID), micro-influencer seeding with free premium codes

### MID
$50-200/mo scaled Apple Search Ads across top 5 niches, paid TikTok creator demos

## Daily Actions

- [ ] 1. Audit free vision API tiers: Google Cloud Vision (1K free), Hugging Face (rate-limited free), Plant.id (500 free/day), on-device CoreML as zero-cost fallback
- [ ] 2. Create vision-app-base-template extending existing scripture-streak Capacitor template: camera capture → API call → styled result card → paywall gate after 3 free IDs
- [ ] 3. Generate 10 niche variants by swapping: app name, icon, color scheme, API endpoint, result display template, ASO keywords
- [ ] 4. Wire RevenueCat for $4.99/mo subscription per app (existing payment integration pattern)
- [ ] 5. Deploy landing pages via existing surge pipeline, submit to App Store via existing Capacitor→Xcode pipeline
- [ ] 6. Create 3 TikTok/Reels demo scripts per app for content factory queue
- [ ] 7. Seed identification subreddits organically (r/whatsthisplant = 1.8M members, r/whatsthisbird = 500K)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for demo clips and ASO descriptions",
  "vision_api": "Google Cloud Vision free tier (1K/mo) + Hugging Face Inference API (free) + fallback to on-device CoreML models"
}
```
