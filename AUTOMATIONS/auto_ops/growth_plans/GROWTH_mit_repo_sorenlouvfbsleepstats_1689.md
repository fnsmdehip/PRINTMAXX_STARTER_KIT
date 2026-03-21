# Growth Plan: MIT repo: sorenlouv/fb-sleep-stats (1689 stars, JavaScript)

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $300-1200/mo

---

## Tactics

1. Post on HN: 'I analyzed when 10K leads were online — reply rates 3x higher in the 90-minute window after they go active'
2. Reddit r/sales + r/coldemail: data-backed post on timing effect on reply rates
3. GitHub: fork the original repo with PRINTMAXX branding, link to hosted SaaS version in README
4. Twitter thread: 'The dirty secret of cold email is not the copy — it is the timestamp' with real data
5. ProductHunt: launch as 'ReachRadar — know when your lead is at their desk'

## Budget Tier Strategies

### FREE
Post data-driven findings on Reddit r/sales, r/entrepreneur, HN Show HN. Fork and star-bait the original OSS repo with a README pointing to the SaaS. Cold email 50 sales-tool reviewers with a one-click demo link.

### LOW
$20-30/mo on Reddit promoted posts in r/sales and r/recruiting. Seed 3-5 micro-influencer sales coaches with free accounts in exchange for a mention.

### MID
$100-200/mo on LinkedIn ads targeting 'Sales Development Representative' + 'Account Executive' job titles with a '3x reply rate' hook ad.

## Daily Actions

- [ ] Write contact_activity_radar.py: accepts CSV of leads, polls LinkedIn/GitHub/email signals on 2h cron, outputs peak_windows.csv
- [ ] Build surge-deployed landing page: 'ReachRadar — cold email when they are actually at their desk' with $19/mo CTA
- [ ] Wire peak_windows.csv output into chain_cold_outbound so outreach scripts auto-schedule sends at computed optimal windows
- [ ] Run engagement_bait_converter.py on the timing findings data to generate 3 tweets + 1 thread
- [ ] Add KPI entry to OPS/KPI_DASHBOARD.md: weekly reply rate delta (timed vs baseline)

## Tooling

```json
{
  "browser": "playwright (activity polling via headless browser)",
  "email": "existing cold email scripts in AUTOMATIONS/",
  "content": "engagement_bait_converter.py \u2014 convert timing findings into data posts"
}
```
