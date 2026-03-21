# Growth Plan: Built something that turns websites, portfolio into macOS/Wi

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post before/after demo video: website URL → running desktop app in 60 seconds
2. Target r/webdev, r/design, r/MacApps, r/SideProject with free demo offer
3. Fiverr gig: 'I will convert your website or portfolio into a Mac/Windows desktop app'
4. Gumroad one-time tool listing with demo GIF — no subscription friction
5. Tweet thread: 'Your portfolio as a .app file — here is how I built the converter'

## Budget Tier Strategies

### FREE
Post demo videos to r/SideProject + r/webdev. Create Twitter/X thread showing the transformation. List on Gumroad free tier. Post Fiverr gig at base price $29.

### LOW
$0-50/mo — boost best-performing demo tweet. Submit to BetaList + Indie Hackers. Reach out to portfolio template creators (Framer, Webflow) as integration partners.

### MID
$50-200/mo — micro-influencer dev content creators to demo the tool. ProductHunt launch with demo video.

## Daily Actions

- [ ] Build web_to_desktop_packager.py: accepts URL → downloads assets via Playwright → scaffolds Electron project → runs electron-builder → outputs installer for all 3 platforms
- [ ] Generate demo: record terminal + output .app opening on macOS — 30-second screen capture
- [ ] Create Gumroad listing: 'Web to Desktop Packager' at $29 one-time — includes CLI tool + README
- [ ] Create Fiverr gig: 'I will package your website or portfolio as a Mac/Windows/Linux desktop app' — $50 basic, $150 premium with custom icon + auto-updater
- [ ] Run engagement_bait_converter.py on this method → 3 posts for posting queue
- [ ] Post demo to r/SideProject and schedule Twitter thread

## Tooling

```json
{
  "browser": "playwright (screenshot capture for demos)",
  "email": "none",
  "content": "engagement_bait_converter.py (demo \u2192 3 social posts)"
}
```
