# Growth Plan: I stalked a dead URL for a decade, waiting for Lunchtimers t

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. SEO capture on '[dead service name] alternative' longtail keywords
2. Reddit posts in r/InternetIsBeautiful and r/SideProject announcing the revival
3. Wayback Machine nostalgia angle for social content

## Budget Tier Strategies

### FREE
Post revival stories to r/InternetIsBeautiful, r/SideProject, HN Show HN. Target '[original name] alternative' SEO keywords with landing pages. Cross-post build story as content.

### LOW
$0-20/mo for domain registration of exact-match or close-match domains of dead services

### MID
$50-100/mo for Google Ads on '[dead service] alternative' keywords with proven search volume

## Daily Actions

- [ ] Build dead_service_scanner.py using Wayback CDX API (free, no auth) to check HTTP status of curated list of once-popular tools
- [ ] Seed initial list from Product Hunt graveyard posts, HN dead links, and r/InternetIsBeautiful archives
- [ ] Cross-reference dead URLs against Google Keyword Planner or free keyword tools for residual search volume
- [ ] Qualifying threshold: >500 monthly searches + no active modern replacement = candidate
- [ ] Route qualified candidates to LEDGER/APP_CLONE_OPPORTUNITIES.csv for app factory pipeline
- [ ] Schedule weekly cron (Sunday 4 AM) — low frequency matches low expected volume

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for revival story posts"
}
```
