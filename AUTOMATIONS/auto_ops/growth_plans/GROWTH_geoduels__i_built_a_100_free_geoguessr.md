# Growth Plan: GeoDuels - I built a 100% free GeoGuessr clone in my mom's b

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $150-400/mo (10 variants × 5K-20K monthly visits × $1-2 RPM AdSense + 0.5% premium conversion at $2.99/mo)

---

## Tactics

1. Post dev story to r/SideProject exactly like original GeoDuels post — format: 'I built X in my [relatable location]', include demo link, self-deprecating hook
2. Submit all variants to free game directories: itch.io, Newgrounds, Coolmathgames directory, Game Jolt
3. Cross-link all 10 variants internally — boosts all pages' domain authority simultaneously
4. SEO target: 'free geoguessr alternative', 'geoguessr free 2026', 'geography games free online' — combined 50K+ monthly searches
5. Embed OpenGraph previews with game screenshot so Twitter/Discord auto-previews look clickable
6. Add 'Made with ❤️ in [city]' to appeal to local/regional communities on Reddit
7. Post each niche variant to its relevant subreddit (anime game → r/anime, movie locations → r/movies)
8. HN Show HN: 'Show HN: I cloned GeoGuessr but free and open source' — OSS framing wins HN

## Budget Tier Strategies

### FREE
r/SideProject post (proven: GeoDuels got high engagement), HN Show HN, game directories, subreddit targeting per niche, IndieHackers launch, cross-linking all variants for compound SEO, Google Search Console submission

### LOW
$20-30 Reddit promoted post on r/geography or r/travel targeting 'free games' interest, ProductHunt launch with 10-variant angle ('I launched 10 free geography games')

### MID
$50-100 micro-influencer seeding to geography/travel YouTubers for embed in 'free GeoGuessr alternatives' roundup videos — high search intent traffic

## Daily Actions

- [ ] Run geo_game_clone_factory.py --research to identify top 10 niche variants by search demand
- [ ] Build base Leaflet.js geo-game template with OpenStreetMap tiles (no API key), AdSense slot, freemium gate
- [ ] Run --generate to parameterize 10 niche configs into standalone HTML bundles
- [ ] Run --deploy to surge.sh all variants ([niche]-geo-game.surge.sh)
- [ ] Playwright smoke test: verify game loads, 5-round limit works, AdSense fires
- [ ] Route through engagement_bait_converter.py: generate r/SideProject post, 3 tweets, 1 IH post
- [ ] Submit all URLs to Google Search Console via GSC API
- [ ] Add KPI entry to OPS/KPI_DASHBOARD.md: track weekly AdSense impressions per variant
- [ ] Update OPS/DEPLOYMENT_URLS.md with all 10 new URLs
- [ ] Update OPS/PRINTMAXX_SYSTEM_MAP.md with new geo-game venture + cron entry

## Tooling

```json
{
  "browser": "none \u2014 OpenStreetMap is free, no Google Maps API key needed",
  "email": "none",
  "content": "engagement_bait_converter.py \u2192 content_repurposer.py",
  "deployment": "surge.sh (existing account, 18 free slots remain)",
  "maps": "OpenStreetMap + Leaflet.js (MIT licensed, zero cost)",
  "monetization": "AdSense (ca-app-pub-5277873663568466) + Stripe Payment Link for premium tier"
}
```
