# Growth Plan:  i tracked which marketing channels actually make money vs j

**Created:** 2026-03-20 18:09
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo indirect (optimization savings — stops wasting time on dead channels, reallocates to converting ones)

---

## Tactics

1. UTM-tag every outbound link across all 47 deployed sites
2. Add Plausible/Umami self-hosted analytics to track source→conversion
3. A/B test landing pages per top-converting channel
4. Kill channels with >100 visits and 0 sales after 30 days

## Budget Tier Strategies

### FREE
UTM tagging on all existing links, Plausible self-hosted analytics, Stripe webhook→CSV logger, weekly cron report

### LOW
$0-50/mo: Plausible cloud ($9/mo) for real-time dashboards, or Simple Analytics free tier

### MID
$50-200/mo: Paid attribution tool (Hyros-lite or SegMetrics) for multi-touch attribution across email+social+organic

## Daily Actions

- [ ] 1. Create channel_attribution_tracker.py that reads MARKETING_CHANNELS_MASTER.csv and CONTENT_PERFORMANCE_LOG.csv
- [ ] 2. Add UTM parameter generator for all deployed site links
- [ ] 3. Wire Stripe webhook listener to log conversions with source attribution
- [ ] 4. Weekly cron produces LEDGER/CHANNEL_ROI_REPORT.csv with visits, conversions, revenue, ROI per channel
- [ ] 5. Auto-flag kill/double-down recommendations based on 30-day conversion data
- [ ] 6. Feed results back into capital_genesis_ranker.py to adjust channel priority scores

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
