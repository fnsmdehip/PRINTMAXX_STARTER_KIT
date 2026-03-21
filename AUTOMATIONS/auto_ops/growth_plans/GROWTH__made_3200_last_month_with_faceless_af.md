# Growth Plan:  made $3,200 last month with faceless affiliate content (6 m

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $500-1600/mo

---

## Tactics

1. 1-to-20 repurposing: one faceless video becomes TikTok + IG Reel + YouTube Short + Pinterest pin + Twitter clip + LinkedIn post
2. Completion rate optimization: hook in first 1.5 seconds, keep videos under 30s for TikTok algo boost
3. Pinterest SEO: faceless content + affiliate links thrive on Pinterest with 6-month evergreen traffic tail
4. Comment seeding: post affiliate link in pinned comment rather than caption to avoid platform suppression
5. Niche stacking: same product reviewed from faith angle + fitness angle + tech angle = 3x content from 1 product
6. Trending audio riding: use trending sounds on faceless content for algorithmic boost at zero cost

## Budget Tier Strategies

### FREE
Organic posting 3x/day across 12 accounts, Pinterest SEO pins (evergreen traffic), YouTube Shorts (no subscriber minimum for monetization), engagement warming on competitor comment sections, Reddit value posts with subtle affiliate mentions in profile

### LOW
$0-50/mo: Canva Pro for premium templates ($13/mo), link-in-bio tool upgrade, boost top-performing faceless posts on IG ($5-10 each)

### MID
$50-200/mo: Micro-influencer seeding — pay 5 small creators $20-40 to recreate our faceless format with their affiliate links (builds social proof), targeted TikTok Promote on best performers

## Daily Actions

- [ ] 1. Run subagent to research top 20 affiliate programs across faith/fitness/tech niches (free signup, >15% commission)
- [ ] 2. Create affiliate_content_generator.py that takes product + niche + hook style and outputs faceless video script + carousel copy + Pinterest pin
- [ ] 3. Wire into existing content_multiplier.py for 1-to-20 repurposing across all 12 buffer accounts
- [ ] 4. Generate initial batch: 30 faceless pieces (10 per niche) with affiliate CTAs
- [ ] 5. Create link-in-bio landing pages per niche (static HTML, deploy to surge.sh) aggregating top affiliate products
- [ ] 6. Add to cron: daily 7 AM generate 3 new faceless affiliate posts, queue to posting_queue
- [ ] 7. Wire tracking: UTM params on all affiliate links, weekly performance log to LEDGER/REVENUE_STREAMS_TRACKER.csv
- [ ] 8. Feed top performers back to content_trend_pipeline.py for format replication

## Tooling

```json
{
  "browser": "playwright for affiliate program signup verification",
  "email": "none",
  "content": "content_factory + image_factory + video_factory(Remotion) + content_repurposer + content_multiplier"
}
```
