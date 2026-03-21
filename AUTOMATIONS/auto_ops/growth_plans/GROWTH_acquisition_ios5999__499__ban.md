# Growth Plan: [ACQUISITION] [iOS][$59.99 → $4.99 ] Ban It - Quit Bad Habit

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** LOW
**Revenue Est:** $150-600/mo per acquisition (existing user base + RevenueCat reactivation at $2.99/mo)

---

## Tactics

1. Post acquisition journey on Twitter: 'I bought a $60 iOS habit app. Here is what I found inside.' — builds credibility + deal flow inbound
2. List PRINTMAXX as a buyer on Acquire.com with niche criteria — passive inbound deal flow
3. After acquiring: update App Store metadata with ASO keywords from existing streak app research
4. Wire RevenueCat into acquired app source code within 48h of acquisition — turn free users into $2.99/mo subscribers
5. Cross-promote acquired app in existing streak app portfolio (interstitial screen: 'Also try Ban It')
6. Reframe app description around social accountability (compete with friends) — differentiation from solo streak apps

## Budget Tier Strategies

### FREE
Twitter thread about app acquisition process + AppFollow free tier for review monitoring on acquired apps + ASO keyword refresh using existing research

### LOW
$59-200 acquisition cost for qualifying app + Acquire.com buyer profile listing (free) + RevenueCat free tier (up to $2.5K MRR)

### MID
$200-500 acquisition budget for higher-revenue apps + Sensor Tower lite for competitive ASO ($49/mo) + AppFollow growth plan for review management

## Daily Actions

- [ ] Create ios_app_acquisition_scanner.py — Playwright scrapes Acquire.com and Flippa weekly, filters by iOS + habit/streak niche + price <= $500
- [ ] Score listings: ROI ratio = (monthly_revenue * 24) / asking_price, require >= 0.8x, source code included, App Store listing live
- [ ] Output acquisition_leads.csv ranked by ROI ratio, append to LEDGER/APP_CLONE_OPPORTUNITIES.csv
- [ ] Auto-generate cold inquiry email for top-3 listings using existing template (reference existing cold_outbound scripts)
- [ ] Add cron: 0 7 * * 1 (Monday 7am weekly scan)
- [ ] Post-acquisition protocol: wire RevenueCat + AdMob from base template, update App Store metadata, cross-promote in streak portfolio
- [ ] Generate Twitter thread content about acquisition process → route to engagement_bait_converter.py

## Tooling

```json
{
  "browser": "playwright MCP (Acquire.com + Flippa scraping)",
  "email": "existing cold_email scripts",
  "content": "engagement_bait_converter.py (acquisition story content)"
}
```
