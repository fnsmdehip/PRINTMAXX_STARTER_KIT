# Growth Plan: [ACQUISITION] 18, no funding, we shipped. Contral is live.

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-150/mo

---

## Tactics

1. Use PRINTMAXX's real story (Day 44, $0 revenue, 47 apps live, no funding) as authentic bait on r/indiehackers — authenticity beats polish in this community
2. Post weekly 'Day X' milestone updates in the '[no funding, we shipped]' format — these reliably hit front page on low-effort days
3. Scrape r/indiehackers [ACQUISITION] flair posts weekly to surface micro-SaaS flip targets under $50K that PRINTMAXX could acquire, improve, and re-list
4. Cross-post milestone content to HN 'Show HN' and Twitter simultaneously — indie hacker audience spans all three
5. Reply-bait: comment on other bootstrapped founder posts with specific PRINTMAXX stats (363 scripts, 47 apps) to build name recognition without posting

## Budget Tier Strategies

### FREE
Weekly authentic posts to r/indiehackers and HN using real PRINTMAXX milestones. Engage in comments on [ACQUISITION] threads to build credibility. Route inbound interest to cold email pipeline via existing chain_cold_outbound.

### LOW
$0-50/mo: Boost best-performing posts via Reddit promoted posts after organic validation. Use story as cold outreach opener to potential acquirers or agency clients.

### MID
$50-200/mo: Build email list from indie hacker audience. Sponsor a relevant newsletter (e.g., Indie Hackers digest) with PRINTMAXX's story as the hook.

## Daily Actions

- [ ] Pull current PRINTMAXX metrics from OPS/HEARTBEAT.md (apps live, scripts, days since start)
- [ ] Feed metrics into engagement_bait_converter.py with template: '[Day X] no funding, shipped Y apps, Z revenue — here is what actually worked'
- [ ] Queue output to CONTENT/social/posting_queue/ for r/indiehackers + Twitter
- [ ] Add weekly cron to auto-refresh metrics and regenerate post (data changes, post stays fresh)
- [ ] Add secondary scraper job: hit r/indiehackers/search?q=[ACQUISITION] weekly, extract micro-SaaS listings under $50K into LEDGER/ACQUISITION_TARGETS.csv

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
