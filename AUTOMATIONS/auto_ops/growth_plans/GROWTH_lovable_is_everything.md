# Growth Plan: Lovable Is Everything

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $80-300/mo

---

## Tactics

1. Post build-in-public threads per app: 'Built X in 4 hours with Lovable' — affiliate link in reply
2. Inject Lovable affiliate link into every app factory landing page footer
3. Cross-post Lovable build showcases to r/vibecoding, r/SideProject, r/entrepreneur
4. Twitter bio + pinned tweet: Lovable affiliate link with social proof (apps built count)
5. Offer 'Lovable-built MVP in 48h' as EAS service at $500-1500 — Lovable cuts build time 80%

## Budget Tier Strategies

### FREE
Build next 3 app factory apps using Lovable free tier. Generate build-in-public thread per app via engagement_bait_converter.py. Inject affiliate link in all output. Zero cost, captures affiliate upside from existing build schedule.

### LOW
$20/mo Lovable Starter — 5x build velocity, unlimited apps. ROI-positive after 1 affiliate signup. Bundle Lovable into EAS service pitch as a differentiator.

### MID
$50-100/mo Lovable Pro + $30 boosted posts targeting 'vibe coding' audience on X. Affiliate funnel converts at 2-4% of click traffic.

## Daily Actions

- [ ] Sign up for Lovable affiliate program at lovable.dev — get referral link
- [ ] Run lovable_affiliate_injector.py: scans all 47 live landing pages and appends affiliate CTA to footer
- [ ] Build next 2 app factory apps using Lovable instead of raw code — benchmark time saved
- [ ] Run engagement_bait_converter.py on each build: output 1 thread + 3 tweets per app with affiliate link
- [ ] Add KPI entry: track affiliate clicks weekly via UTM params in KPI_DASHBOARD.md
- [ ] If EAS venture active: add 'Lovable MVP in 48h' as a service tier at $799

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
