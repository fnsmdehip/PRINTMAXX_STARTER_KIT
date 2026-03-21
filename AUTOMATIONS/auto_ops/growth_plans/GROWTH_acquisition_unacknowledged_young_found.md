# Growth Plan: [ACQUISITION] Unacknowledged young founder

**Created:** 2026-03-21 12:40
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo (brokerage fees on 1-2 deals/mo at 3-5% of $5-15K deal size) + indirect content audience growth

---

## Tactics

1. Post 'I scanned 100 abandoned side projects — here is what they were actually worth' thread on Twitter/X
2. Reply to r/SideProject 'show off your project' threads with valuation analysis (builds trust + drives DMs)
3. Create a free 'What is my side project worth?' Typeform linked from printmaxxer bio — captures founder leads
4. Cross-post acquisition finds to r/MicroSaaS and r/AcquireStartups as case studies
5. Wire found targets into existing chain_post_how_much_do_you_think_this_app_is for community valuation engagement

## Budget Tier Strategies

### FREE
Reddit scraping daily, Twitter thread content from each batch, reply engagement on r/SideProject posts, DM outreach to founders directly

### LOW
$0-50/mo — Acquire.com basic listing fee ($0) + 1 sponsored r/SideProject post ($20) to drive inbound acquisition inquiries

### MID
$50-200/mo — Microacquire premium listing ($150/mo) to connect buyers with sourced deals, take 3-5% broker fee per closed deal

## Daily Actions

- [ ] Create young_founder_acquisition_scanner.py — Reddit JSON API scraper with keyword filters (gave up, shutting down, taking over, no users, not worth continuing)
- [ ] Add undervaluation scorer: proxy signals = GitHub stars vs traffic vs MRR vs niche CPM
- [ ] Wire output to engagement_bait_converter.py for auto-content generation per batch
- [ ] Add cron at 0 7 * * * for daily scan
- [ ] Create LEDGER/BROKERING_PIPELINE.csv to track sourced targets and deal stage
- [ ] Handoff high-score targets to chain__post_how_much_do_you_think_this_app_is for community valuation posts
- [ ] Add KPI entry: weekly count of targets sourced + outreach sent

## Tooling

```json
{
  "browser": "playwright (Reddit scraping via JSON API fallback + r/SideProject HTML)",
  "email": "none \u2014 DM-first outreach via Reddit + Twitter",
  "content": "content_factory + engagement_bait_converter.py"
}
```
