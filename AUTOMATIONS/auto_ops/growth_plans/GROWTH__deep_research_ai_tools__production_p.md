# Growth Plan: # DEEP RESEARCH: AI Tools & Production Pipeline for NSFW Con

**Created:** 2026-03-20 23:12
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. Post free teaser content on Reddit adult subs to drive Fanvue traffic
2. Cross-promote across 3+ adult platforms simultaneously
3. Use engagement bait captions: question hooks + partial reveals
4. Batch-produce 30-day content calendar in one session to avoid daily effort
5. Repurpose single image set into 5 platform variants (crop ratios, caption styles)

## Budget Tier Strategies

### FREE
Stable Diffusion local, Claude captions, Reddit organic posting, playwright account warmup, batch content pre-production

### LOW
$10-30/mo Fanvue boosted posts, Reddit targeted ads on adult-allowed subs, recycled high-performer content

### MID
$50-150/mo ElevenLabs voice for video content, premium AI video tool free tier stacking, micro-influencer shoutout trades

## Daily Actions

- [ ] Verify Stable Diffusion API running locally (localhost:7860) or flag as blocker
- [ ] Create nsfw_content_production_pipeline.py implementing the 3-phase DAG
- [ ] Wire into existing chain_500_to_35kmonth_ai_influencer_fanvue handoff
- [ ] Add cron entry: 0 7 * * * python3 AUTOMATIONS/nsfw_content_production_pipeline.py --cycle
- [ ] Add KPI row to KPI_DASHBOARD.md: Fanvue subs + daily asset count
- [ ] BLOCKER: Fanvue/OnlyFans account creation is human-only — surface in task tracker

## Tooling

```json
{
  "browser": "playwright (Fanvue posting, Reddit warmup)",
  "email": "none",
  "content": "Stable Diffusion local API + claude -p captions + content_factory"
}
```
