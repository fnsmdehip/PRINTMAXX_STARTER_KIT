# Growth Plan: https://reddit.com/r/AppBusiness/comments/1rva997/built_5_ap

**Created:** 2026-03-20 23:12
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $2-3K/mo

---

## Tactics

1. Post our own case study on r/AppBusiness at first $1K MRR milestone — drives credibility + backlinks + recruits beta users
2. Monitor r/AppBusiness weekly for founders disclosing $5K+ MRR — reverse-engineer their App Store ASO keywords via store scraper
3. Apply portfolio kill rule to our app factory NOW: any app at $0 revenue 30 days post-launch gets axed or pivoted, not maintained
4. Use engagement_bait_converter.py on extracted lessons — frame as contrarian take ('4 of my 5 apps failed and I still made $7K/mo')

## Budget Tier Strategies

### FREE
Weekly automated scrape of r/AppBusiness, r/SideProject, r/indiehackers. Extract niche/ASO/pricing signals. Feed into app factory priority queue. Generate Twitter threads from each case study using engagement_bait_converter.py.

### LOW
$0-50/mo: App Store API scraping to validate niches surfaced by case studies before committing build cycles. Priority-sort our existing 50-app queue using extracted win-rate patterns.

### MID
$50-200/mo: Once at $1K MRR, promote our own case study post via Reddit ads targeting r/AppBusiness and r/EntrepreneurRideAlong for backlinks + product launch traffic.

## Daily Actions

- [ ] Fetch full post via playwright Brave-cookie session, extract raw text
- [ ] LLM parse: what made app 5 succeed where 1-4 failed — niche specificity, pricing, ASO, distribution channel
- [ ] Cross-reference extracted niche with LEDGER/APP_CLONE_OPPORTUNITIES.csv and APP_FACTORY_METHODS.csv
- [ ] Update APP_FACTORY_METHODS.csv with new kill-criteria row: 0 revenue at 30d = kill flag
- [ ] Re-rank app_factory_command_center.py top-8 queue using updated signals
- [ ] Schedule weekly r/AppBusiness scrape for posts matching revenue-disclosure regex
- [ ] Run engagement_bait_converter.py on extracted lessons — output 3 tweets + 1 thread to CONTENT/social/posting_queue/

## Tooling

```json
{
  "browser": "playwright (Brave cookie injection for authenticated Reddit)",
  "email": "none",
  "content": "engagement_bait_converter.py \u2014 convert case study lessons into 3 tweets + 1 thread per scrape cycle"
}
```
