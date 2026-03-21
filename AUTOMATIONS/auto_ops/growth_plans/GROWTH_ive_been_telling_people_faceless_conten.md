# Growth Plan: i've been telling people faceless content accounts are a rea

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo at 5 accounts (10K+ followers each), $2K-5K/mo at 20+ accounts

---

## Tactics

1. Post 3-5x/day per account using content_multiplier.py — TikTok algo rewards volume
2. Hub-and-spoke repurposing: one piece of content → TikTok + IG Reels + YouTube Shorts + Pinterest
3. Target niches with high brand CPM: finance ($15-50 CPM), health ($10-30 CPM), tech ($12-40 CPM) — not entertainment ($3-8 CPM)
4. Use completion-rate optimization: hook in first 2 seconds, loop structure, no dead air
5. Cross-promote accounts to compound follower growth across the network
6. Once 10K reached: DM brands directly (no agency cut) — pitch CPM at 20-30% below market rate to win first deal fast
7. Track competitor faceless accounts in same niche — scrape their posting frequency and formats

## Budget Tier Strategies

### FREE
AI-generated content via claude -p + content_factory.py. Post 3-5x/day per account. Hub-and-spoke repurposing to 4 platforms. Engagement warming via strategic comments on trending posts in niche. Zero creator payments — we generate content ourselves.

### LOW
$0-50/mo: Stock footage licenses (Pexels/Pixabay free tier first). Scheduled posting tool (Buffer free tier or twitter_warmup_poster.py). Basic niche research tools.

### MID
$50-200/mo: ElevenLabs voiceover for narrated content ($22/mo). Stock footage premium access. Boost top-performing posts at $5-10 each to accelerate follower velocity past algorithm thresholds.

## Daily Actions

- [ ] Wire into existing chain_made_3200_last_month_with_faceless_af — enhance rather than duplicate
- [ ] Run engagement_bait_converter.py on this entry to generate 3 posts about faceless account model for @printmaxxer
- [ ] Add cron entry: 0 7 * * * python3 AUTOMATIONS/faceless_account_cpm_tracker.py — tracks follower delta + CPM benchmarks
- [ ] Add KPI row to OPS/KPI_DASHBOARD.md: faceless account follower count + niche CPM rate per week
- [ ] Identify 3 high-CPM niches to launch accounts in (finance, health, AI tools) — create content calendar per niche

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + content_multiplier.py + engagement_bait_converter.py + twitter_warmup_poster.py"
}
```
