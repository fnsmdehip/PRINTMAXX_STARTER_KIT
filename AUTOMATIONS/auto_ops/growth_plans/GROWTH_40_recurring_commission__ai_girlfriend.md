# Growth Plan: 40% recurring commission — AI Girlfriend SaaS affiliate prog

**Created:** 2026-03-21 12:40
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo recurring by day 90 (50-200 converted users at 40% of $10-20/mo avg subscription)

---

## Tactics

1. Longtail SEO: 'best AI girlfriend app 2026', 'replika alternative free', 'ai companion app review', 'candy ai vs eva ai' — buyer intent, low competition
2. Comparison pages rank fast: 'Top 5 AI Girlfriend Apps (Honest Review)' — affiliate links embedded naturally
3. Reddit organic: r/replika, r/AICompanion, r/singularity — genuine value posts, affiliate link in bio/comment
4. TikTok faceless: 'I tried 5 AI companion apps so you don't have to' — link in bio to comparison page
5. Twitter thread: comparison breakdown with affiliate CTAs — existing printmaxxer account
6. Pinterest: comparison infographics (AI app feature tables) — evergreen traffic, underserved niche
7. Content repurpose via content_repurposer.py: one comparison page → 10 platform variants

## Budget Tier Strategies

### FREE
Surge-hosted comparison pages targeting longtail keywords + Reddit organic posts in 5 relevant subreddits + Twitter threads via engagement_bait_converter.py + Pinterest static comparison graphics via image_factory + content_multiplier.py bulk page generation

### LOW
$20-40/mo: 3-5 branded redirect domains for comparison URLs (aff.domain/best-ai-companion) + Reddit promoted posts in r/Affiliatemarketing + basic TikTok content boosting on top-performing video

### MID
$50-150/mo: TikTok/IG paid promotion targeting 'AI tools' + 'loneliness app' interest clusters, retarget visitors to comparison page, optimize to affiliate signup conversion

## Daily Actions

- [ ] 1. Run subagent: research top 10 AI companion SaaS affiliate programs, extract rates + signup URLs
- [ ] 2. Sign up for top 5 programs — store affiliate IDs in LEDGER/AFFILIATE_IDS.csv and .env
- [ ] 3. Run ai_companion_affiliate_engine.py --generate-pages → 10 comparison/review pages with injected links + FTC disclosure
- [ ] 4. Deploy all pages to surge.sh under dedicated subdomain or existing MONEY_METHODS build
- [ ] 5. Add pages to sitemap.xml + ping Google Search Console
- [ ] 6. Run engagement_bait_converter.py on top 3 pages → generate 3 Twitter threads + 2 Reddit posts → push to posting_queue/
- [ ] 7. Add weekly KPI row to KPI_DASHBOARD.md: clicks, conversions, active subs, commission total
- [ ] 8. Wire cron 0 7 * * 1: weekly content refresh (update rankings, add new programs, refresh comparisons)

## Tooling

```json
{
  "browser": "playwright (affiliate program research + signup flow mapping)",
  "email": "none initially \u2014 SEO/content primary traffic source",
  "content": "content_factory + engagement_bait_converter.py + content_multiplier.py"
}
```
