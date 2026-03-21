# Growth Plan: Show HN: Clearview Cam Lite: Real-time Cam Engine to see thr

**Created:** 2026-03-21 12:41
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Comment on the HN thread with value-add (link to article organically after 48h cooldown)
2. Post demo clips of open-source defogging on dashcam footage — TikTok / YouTube Shorts
3. Target r/Dashcam, r/homeautomation, r/securitycameras with 'we tested 5 defogging tools' post
4. Programmatic SEO: auto-generate pages for '<city> foggy road dashcam' + defogging solution angle
5. Build free web demo (pyimagej or ONNX AOD-Net in browser via Transformers.js) — free tool = backlinks + traffic

## Budget Tier Strategies

### FREE
HN comment engagement, Reddit posts, Twitter threads from posting queue, surge-hosted demo page, programmatic longtail SEO pages, Amazon Associates affiliate links in article

### LOW
$20-30 Reddit promoted post in r/Dashcam targeting 'best dashcam 2026' searchers; $10 on a single sponsored LinkedIn post hitting fleet/logistics managers

### MID
$80-150/mo Google Ads on 'fog camera enhancement software' — low competition B2B query, CPCs likely $0.40-1.20; target security integrators + fleet managers

## Daily Actions

- [ ] Run Playwright scraper on HN thread — extract top comments, pain points, competitor mentions
- [ ] Keyword subagent: find 10 longtail defogging/adverse-weather queries with KD < 20
- [ ] Generate SEO article + 3 Twitter threads via claude -p with copy-style.md voice
- [ ] Build or fork open-source AOD-Net ONNX demo page (MIT license, zero cost)
- [ ] Deploy article + demo to surge (or Netlify once account created)
- [ ] Wire Amazon Associates / B&H camera affiliate links into article
- [ ] Push Twitter threads to posting_queue
- [ ] Add cron entry: weekly monitor for new HN 'Show HN' computer-vision launches to feed same pipeline

## Tooling

```json
{
  "browser": "playwright (scrape HN thread + screenshot demo outputs)",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
