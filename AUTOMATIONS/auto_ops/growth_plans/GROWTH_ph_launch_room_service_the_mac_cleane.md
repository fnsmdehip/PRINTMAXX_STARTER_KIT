# Growth Plan: [PH LAUNCH] Room Service: The Mac cleaner built for develope

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $300-1200/mo

---

## Tactics

1. Build a competing Mac dev utility (env cleaner, log manager, port killer, dev disk analyzer) via app factory in 1-2 days
2. Launch on PH with 'built for developers' hook — same positioning Room Service used, proven framing
3. Post Show HN on launch day with technical implementation details to capture dev audience
4. Submit to developer directories: DevHunt, AlternativeTo, MacUpdate, dev.to #showdev
5. X build thread: 'I built a Mac cleaner for developers in 48h — here's what I learned from Room Service's PH launch'

## Budget Tier Strategies

### FREE
Show HN post, r/macapps + r/devtools + r/programming Reddit posts, X build thread, free directory submissions (AlternativeTo, MacUpdate, DevHunt), comment on Room Service's PH page to drive awareness

### LOW
$20-40 Reddit targeted ads in r/programming and r/apple dev communities; PH supporter outreach via existing hunter network

### MID
$50-150/mo: sponsor Fireship or similar dev YouTube shorts; dev newsletter sponsorships (TLDR Tech, Bytes.dev CPM ~$2-5)

## Daily Actions

- [ ] 1. Check if existing ph_scraper.py or hn_ph_scraper already covers PH developer-tools category — if yes, add category filter and min_votes=100 param instead of new script
- [ ] 2. If no coverage: create ph_devtools_monitor.py — fetch PH /topics/developer-tools RSS or API, parse name+votes+pricing+website+tagline
- [ ] 3. Score each app: simplicity (<3d build) +3, priced $5-30 +2, Mac-specific +2, 100+ votes +2, has free tier competitor +1
- [ ] 4. Append entries with clone_score >= 6 to app_factory_priority_queue.json with source=PH_DEVTOOLS and category=mac_utility
- [ ] 5. Wire cron: 0 8 * * * ph_devtools_monitor.py — runs after PH daily digest resets
- [ ] 6. Route signal through existing chain_14_ph_launches_today for content generation (tweet about dev tool trends)

## Tooling

```json
{
  "browser": "playwright",
  "email": "none",
  "content": "content_factory"
}
```
