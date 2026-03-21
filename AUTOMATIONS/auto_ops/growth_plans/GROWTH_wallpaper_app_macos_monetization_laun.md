# Growth Plan: Wallpaper app (macOS) monetization: launch v0.1 with 2-3 use

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo

---

## Tactics

1. Post free sample wallpapers on r/macsetups and r/unixporn with watermarked previews linking to paid packs
2. Cross-post to r/wallpapers r/WidescreenWallpaper r/ultrawidescreens for maximum organic reach
3. X posts showing desktop setups using the wallpapers (setup porn content style)
4. Bundle wallpapers into existing app factory streak apps as premium unlock content (cross-sell)
5. Seasonal drops (spring colors, dark mode autumn, holiday themes) for repeat engagement

## Budget Tier Strategies

### FREE
Reddit organic posts (3-5 subreddits per pack), X preview posts, cross-promote in existing 47 deployed sites via banner, Discord community for feedback and requests

### LOW
$0-50/mo: Boost top-performing Reddit posts, micro-influencer seeding to macOS setup YouTubers

### MID
$50-200/mo: Paid Reddit ads targeting r/macsetups, ProductHunt launch, Setapp marketplace listing

## Daily Actions

- [ ] 1. Create wallpaper_pack_generator.py using existing image_factory HTML-to-image pipeline to render 5K resolution wallpapers from styled HTML/CSS templates
- [ ] 2. Generate 5 themed packs (8-12 wallpapers each) at macOS native resolutions (5120x2880 for 5K, 3456x2234 for 16-inch, 2560x1600 for 13-inch)
- [ ] 3. Create Stripe products via MCP ($5.99 per pack, $14.99 bundle) and generate payment links
- [ ] 4. Build landing page with masonry gallery grid, deploy to surge.sh
- [ ] 5. Queue Reddit posts with free sample wallpapers + watermarked previews to r/macsetups, r/wallpapers, r/unixporn
- [ ] 6. Queue X posts showing full desktop setups using the wallpapers
- [ ] 7. Add weekly cron (Monday 4 AM) to generate new seasonal/trending wallpaper batch
- [ ] 8. Wire download tracking to KPI dashboard

## Tooling

```json
{
  "browser": "playwright for HTML-to-image rendering",
  "email": "none",
  "content": "image_factory (existing HTML-to-PNG pipeline)"
}
```
