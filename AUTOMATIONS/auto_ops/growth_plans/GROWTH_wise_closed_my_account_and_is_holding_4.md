# Growth Plan: Wise closed my account and is holding $45,000

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post 'Wise froze $45K' warning threads on Twitter — shares heavily in nomad community, triggers algo
2. Reply within first hour to new Reddit freeze posts with helpful alternatives + comparison page link
3. Build wise-alternatives.surge.sh comparison landing page with affiliate links (Mercury $30/referral, Revolut tiered)
4. Create 'Digital Nomad Payment Safety Checklist' Gumroad product ($9-19) from freeze incidents — pre-built digital product
5. Engage r/digitalnomad, r/solotravel finance threads — provide value, earn trust, soft-link to guide

## Budget Tier Strategies

### FREE
Post freeze warning content on Twitter, reply to Reddit incidents with alternatives, build comparison landing page on surge.sh with Mercury/Revolut/Airwallex affiliate links, queue all posts through content_repurposer.py for cross-platform spread

### LOW
$0-50/mo: Boost top-performing freeze warning posts, build niche Twitter following in digital nomad finance, place comparison page in nomad Facebook groups

### MID
$50-200/mo: Sponsored placement in nomad newsletters (Nomad List, Hacker Paradise), collab with nomad finance YouTubers for affiliate revenue share

## Daily Actions

- [ ] Write fintech_freeze_content_monitor.py — scrape r/digitalnomad, r/Wise, r/Revolut, r/expats via Reddit JSON API (no browser needed, per existing reddit_deep_scraper.py pattern) for freeze-signal keywords daily at 8 AM
- [ ] Pipe matched posts through engagement_bait_converter.py — output 3 posts per incident: (1) warning post, (2) alternatives comparison, (3) checklist hook
- [ ] Build wise-alternatives static comparison page (HTML to surge.sh) with affiliate links for Mercury, Revolut, Airwallex — target 'wise alternative digital nomad' keyword cluster
- [ ] Create 'Fintech Freeze Protection Checklist' digital product — pre-populate from scraped incidents, list on Gumroad when account exists ($9-19 price point)
- [ ] Queue all generated posts to CONTENT/social/posting_queue/ for warmup-aware posting via twitter_warmup_poster.py
- [ ] Add cron entry at 0 8 * * * + KPI row in KPI_DASHBOARD.md tracking: incidents_scraped, posts_queued, page_visits, affiliate_clicks

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py + content_multiplier.py"
}
```
