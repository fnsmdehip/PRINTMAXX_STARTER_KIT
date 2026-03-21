# Growth Plan: Residents exiting Massachusetts took a net of $4.2 Billion i

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo organic content engagement; $100-400/mo if SEO calculator page built with CPA affiliate links

---

## Tactics

1. Post tax migration content immediately after major tax policy news drops — engagement window is 2-6 hours
2. Quote-tweet Bloomberg/IRS reports with founder-angle commentary: 'Here is what this means for your business location'
3. Reply to high-engagement tax policy tweets with specific state-level data to drive profile visits
4. Post in r/financialindependence and r/entrepreneur when IRS SOI annual data releases — these threads go viral
5. Build state-tax-comparison SEO calculator page targeting 'best states to move to avoid income tax' (3K+ monthly searches) with SmartAsset/Harness Tax affiliate links

## Budget Tier Strategies

### FREE
Pipe Bloomberg/IRS wealth-flight data through engagement_bait_converter.py weekly. Post during market hours Mon-Fri for finance audience. Reply-bait on high-traffic tax policy discussions. Cross-post to r/financialindependence when IRS SOI data drops annually.

### LOW
$0-50/mo: Boost top-performing tax migration post ($10-20). Sponsor placement in one indie finance newsletter per month ($20-40/issue). SmartAsset affiliate signup (free, $50-200 per qualified lead referral).

### MID
$50-200/mo: Build and rank a 'State Tax Migration Calculator' landing page targeting 'should I move from [state] for taxes' long-tail keywords. Add CPA affiliate program links (SmartAsset, Harness Tax, 1-800Accountant) at 30-50% commission per referral. Estimated $100-400/mo at modest traffic.

## Daily Actions

- [ ] Run python3 AUTOMATIONS/engagement_bait_converter.py with this entry now to generate 3 Twitter posts + 1 thread: angle = 'Massachusetts lost $4.2B in taxpayer income in one year — here is what that means for founders choosing where to incorporate'
- [ ] Queue generated posts in CONTENT/social/posting_queue/ for warmup-aware scheduling
- [ ] Add weekly Monday cron: scrape IRS SOI migration page + Google News 'state tax migration billion' → pipe any new data points into engagement_bait_converter
- [ ] P1 (no accounts needed): stub out state-tax-comparison landing page in MONEY_METHODS/APP_FACTORY/builds/ with affiliate CPA links for when Stripe/affiliate accounts are live

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
