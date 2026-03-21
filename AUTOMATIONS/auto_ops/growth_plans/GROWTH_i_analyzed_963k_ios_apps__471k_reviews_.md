# Growth Plan: I analyzed 963k iOS apps + 471k reviews I've built too many 

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo indirect — better-targeted app factory builds with validated trapped-demand signal = higher conversion and faster traction per app

---

## Tactics

1. Target competitor frustrated review keywords verbatim in our ASO — users searching fixes land on us
2. Use negative review quotes from trapped apps as social proof hooks: 'Tired of [competitor] crashing? We fixed that.'
3. Post teardown thread on X/Reddit r/SaaS showing gap-finding methodology — attracts indie dev audience
4. Cross-pollinate: package the scanner output as a $29 Gumroad report (iOS App Gaps 2026) when Gumroad account exists

## Budget Tier Strategies

### FREE
Organic ASO targeting competitor frustrated keywords. Teardown threads in r/SaaS, r/indiedev, r/iOSProgramming. Build 1 trapped-demand competitor app per week from scanner output. Apple Search Ads basic keyword targeting on gap categories.

### LOW
$0-50/mo — AppFollow free tier for delta tracking (catch when competitor score drops). $5/day Apple Search Ads on validated trapped-demand categories.

### MID
$50-200/mo — Sensor Tower standard plan for real revenue data validation. Scale Apple Search Ads on winners. Micro-influencer app review seeding in niche communities.

## Daily Actions

- [ ] Create AUTOMATIONS/ios_trapped_demand_scanner.py using iTunes Search API (free, no API key) across 25 hardcoded categories
- [ ] Implement trapped-demand composite score: frustrated_ratio from keyword matching in review text + revenue_proxy from rating_count/avg_rating heuristic
- [ ] Write top-25 to LEDGER/APP_FACTORY_OPPORTUNITIES.csv: app_name, category, score, frustrated_sample_quotes, revenue_proxy, build_recommendation
- [ ] Wire output into app_factory_command_center.py via --inject flag so scanner output becomes live build queue
- [ ] Add weekly Monday 5AM cron entry: 0 5 * * 1 python3 AUTOMATIONS/ios_trapped_demand_scanner.py
- [ ] Run engagement_bait_converter.py on top-5 findings to generate teardown content for posting queue

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
