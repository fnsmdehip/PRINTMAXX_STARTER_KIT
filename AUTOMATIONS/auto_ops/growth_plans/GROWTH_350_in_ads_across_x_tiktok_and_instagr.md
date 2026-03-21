# Growth Plan: $350 in ads across X, TikTok and Instagram. Only one platfor

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct (intelligence entry — prevents $200+/mo wasted spend on X/TikTok when Phase 1 ad budget unlocks)

---

## Tactics

1. Instagram-only paid SaaS ads when budget unlocks — skip X and TikTok entirely until CPA evidence improves
2. Run Instagram burst campaigns then let organic tail convert — do NOT turn off immediately after budget runs out
3. Target Instagram Story ads over feed: lower CPC, higher intent signal for SaaS signups
4. Retarget Instagram site visitors at 3x cheaper CPL than cold traffic once pixel has 100+ events
5. Use engagement_bait_converter.py to generate IG-native organic posts that mirror paid ad hooks — zero-cost version of the same funnel

## Budget Tier Strategies

### FREE
Organic Instagram content mimicking paid ad hooks via engagement_bait_converter.py; 2 posts/day at peak hours (7-9pm EST); CTA to app signup on every post; track which hooks drive profile visits to reverse-engineer paid creative before spending

### LOW
$50-150/mo Instagram Story ads only; target founder/solopreneur/SaaS audiences; hard cap CPA at $21 (baseline to beat); pause X and TikTok entirely

### MID
$150-300/mo Instagram retargeting + lookalike from signup list; add Reels ads (lower CPM than feed); A/B test direct app link vs landing page; leverage organic tail data to time campaign bursts

## Daily Actions

- [ ] Check if LEDGER/AD_PLATFORM_BENCHMARKS.csv exists; if not, create with columns: platform, spend, clicks, signups, cpa, organic_tail_days, notes, date
- [ ] Append row: instagram,$150,258,7,$21.43,ongoing,organic tail continues post-campaign,2026-03-21
- [ ] Append row: x_twitter,$100,300,1,$100.00,none,misclick traffic dominant,2026-03-21
- [ ] Append row: tiktok,$150,34,0,null,none,misclick traffic dominant,2026-03-21
- [ ] Add ad spend recommendation rule to decision_engine.py: if budget > $0 and platform IN [x_twitter, tiktok] and CPA_benchmark > $50, route to instagram_only flag
- [ ] Run engagement_bait_converter.py with context: 'Instagram ads work for SaaS; X and TikTok are misclick traps; IG organic tail persists post-campaign' to generate 3 posts

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
