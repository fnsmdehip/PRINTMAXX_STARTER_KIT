# Growth Plan:  heres an actual way to make $10k a month from tiktok + orga

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Slideshow format specifically bypasses TT AI label — key competitive edge over video AI content
2. Completion rate optimization: front-load curiosity gap in slide 1, payoff on slide 5-7 to maximize watch-through
3. Comment seeding: post first comment with engagement bait question related to product
4. Cross-post slides to IG carousels (same assets, different captions) for 2x distribution at 0 marginal cost
5. Batch create 30 days of content in one session, drip-schedule to maintain consistency
6. Use trending sounds/hashtags from TT discovery page to piggyback algorithm boost
7. Multi-account strategy: 3 niche accounts (tech gadgets, beauty, fitness) to diversify risk

## Budget Tier Strategies

### FREE
Organic posting 3x/day, trending hashtags, comment engagement farming, cross-post IG carousels, AI image gen via Claude prompts + free Playground v2/SDXL, warmup 2 weeks before monetizing

### LOW
$10-30/mo for higher-quality image gen API (Midjourney alt) + scheduling tool if needed, boost 1 top-performer/week at $5 spend

### MID
$50-150/mo for GoLogin multi-account management + residential proxies for 3-5 TT accounts, paid sound library, micro-influencer duets/stitches at $20-50 each

## Daily Actions

- [ ] 1. Research: Identify 3 affiliate niches with high TT slideshow virality (tech gadgets, beauty hacks, fitness gear) — use existing LEDGER/ASO_KEYWORDS.csv + trending TT hashtags
- [ ] 2. Sign up for affiliate programs: Amazon Associates, ClickBank, Impact (human action — add to P0 queue)
- [ ] 3. Build tiktok_slide_affiliate_pipeline.py with DAG phases: product scout → image gen → slide assembly → publish
- [ ] 4. Image generation: Use free SDXL/Playground V2 API for lifestyle product images that pass as real photos — avoid obvious AI tells (hands, text, symmetry)
- [ ] 5. Slide format: 5-7 images per carousel, hook on slide 1, product reveal slide 3, CTA slide final, text overlays via PIL/Pillow
- [ ] 6. Posting automation via Playwright MCP — login with Brave cookie injection, post slides with captions + hashtags + trending audio tag
- [ ] 7. Affiliate link strategy: TT bio link (Linktree/Beacons free tier) rotating per niche, CTA 'link in bio' on final slide
- [ ] 8. Wire into existing content_repurposer.py to auto-cross-post slides as IG carousels
- [ ] 9. Cron 3x/day (7AM, 12PM, 6PM) for posting, daily analytics pull at 10PM
- [ ] 10. Performance tracking: completion rate >60% = winner (remix/repost), <30% = kill, feed winners into engagement_bait_converter.py for thread repurposing

## Tooling

```json
{
  "browser": "playwright for TT posting automation",
  "email": "none",
  "content": "claude -p for captions + SDXL/PlaygroundV2 for images (free)",
  "affiliate": "Amazon Associates + ClickBank (free signup)"
}
```
