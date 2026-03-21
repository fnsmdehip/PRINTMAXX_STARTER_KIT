# Growth Plan: 48 SVG backgrounds. Copy/paste into landing pages and app UI

**Created:** 2026-03-20 13:50
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0 direct but +5-15% conversion uplift across 114 pages = accelerates all existing revenue lanes

---

## Tactics

1. Before/after screenshots as Twitter content (Rule 9: 3 tweets + 1 thread)
2. Open-source the SVG collection on GitHub for backlinks
3. Post SVG pack on Product Hunt as free resource for inbound
4. Use upgraded pages as portfolio proof for cold outbound web design gigs

## Budget Tier Strategies

### FREE
Before/after tweets, GitHub repo with SVG pack, Reddit posts in r/webdev and r/design, Product Hunt free launch

### LOW
$10-20 for promoted tweets showing the visual upgrade across 114 sites

### MID
$50-100 for design community sponsorships or newsletter placements featuring the free SVG pack

## Daily Actions

- [ ] Curate 48 SVG backgrounds from HN source into MEDIA/svg_backgrounds/ with category tags (geometric, gradient, wave, blob, pattern)
- [ ] Build svg_background_injector.py that reads OPS/DEPLOYMENT_URLS.md, classifies each page niche, selects matching SVG
- [ ] Inject SVGs as inline CSS background-image (no external requests, zero latency hit) into hero sections
- [ ] Batch redeploy all 114 pages via surge
- [ ] Playwright screenshot before/after for QA
- [ ] Hook: PostToolUse on any new landing page build auto-applies SVG background from registry
- [ ] Weekly cron catches new pages added since last run
- [ ] Generate 3 tweets + 1 thread from the before/after screenshots (Rule 9)

## Tooling

```json
{
  "browser": "playwright for screenshot verification",
  "email": "none",
  "content": "content_factory for before/after posts"
}
```
