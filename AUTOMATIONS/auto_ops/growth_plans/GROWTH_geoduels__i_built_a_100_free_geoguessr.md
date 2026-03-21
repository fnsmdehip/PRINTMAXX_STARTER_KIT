# Growth Plan: GeoDuels - I built a 100% free GeoGuessr clone in my mom's b

**Created:** 2026-03-20 23:36
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $150-600/mo per clone (AdSense at 50K-200K monthly visits + 0.5% premium conversion at $1.99/mo)

---

## Tactics

1. Post 'I built a free alternative to X' on r/SideProject, r/webdev, and the paid app's own subreddit — this exact format consistently pulls 500-2K upvotes with zero ad spend
2. Target zero-competition SEO keywords: 'free [app name]', '[app name] free alternative', 'play [game] online free' — paid app brand terms have high intent and low CPC
3. Submit to alternativeto.net on day 1 — free alternative directories drive compounding long-tail traffic
4. Show HN launch — 'I built a free GeoGuessr clone' style posts regularly hit front page
5. Wire AdSense or AdMob day 1 — free tier monetizes immediately, no account needed beyond existing AdMob ID
6. Add thin premium tier at $1.99/mo matching paid app price (no ads + extra features) via Stripe Payment Link — 0.5-1% conversion on traffic still meaningful
7. Cross-promote in existing streak apps: interstitial banner to related free clone apps

## Budget Tier Strategies

### FREE
Reddit posts in paid app subreddits and r/SideProject, HN Show HN, alternativeto.net listing, ProductHunt launch, SEO on branded free-alternative keywords, Twitter thread about build process

### LOW
$20-40/mo Reddit ads targeting exact subreddits of the paid app (r/geoguessr etc), Google Ads on 'free [app name]' exact match — niche game keywords often under $0.10 CPC

### MID
$50-150/mo micro-influencer seeding in gaming or productivity communities depending on app type, sponsored newsletter placement in relevant niche

## Daily Actions

- [ ] Create paid_app_clone_opportunity_scanner.py: pulls App Store top 100 paid apps + top 50 paid games, checks Google search volume for 'free [app name]', scores by demand/complexity ratio
- [ ] Add to app_factory_priority_queue.json: top 3 clone opportunities each Monday
- [ ] For each clone: use existing app factory base template (PWA-first), wire AdMob (existing ID: ca-app-pub-5277873663568466~6431629011) day 1
- [ ] Wire Stripe Payment Link for premium tier using payment_integrator.py --route WEB_APP
- [ ] On launch: run engagement_bait_converter.py with 'I built free X clone' prompt, queue Reddit + HN + Twitter posts
- [ ] Submit to alternativeto.net within 24h of each launch
- [ ] Cron 0 7 * * 1 — weekly rescan for new opportunities as paid apps raise prices

## Tooling

```json
{
  "browser": "playwright (App Store scraping, alternativeto.net gap analysis)",
  "email": "none",
  "content": "engagement_bait_converter.py (I built free X format) + content_repurposer.py (Reddit post \u2192 Twitter thread \u2192 HN)"
}
```
