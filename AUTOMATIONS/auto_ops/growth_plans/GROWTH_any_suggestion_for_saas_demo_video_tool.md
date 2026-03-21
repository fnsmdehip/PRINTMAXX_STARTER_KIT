# Growth Plan: any suggestion for saas demo video tool

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo indirect affiliate (Loom partner: $0, Synthesia: up to $150/ref, Descript: 15% recurring, Arcade: affiliate program exists)

---

## Tactics

1. Deploy comparison page to LANDING/affiliate-pages/saas-demo-video-tools/ via surge (matches existing pattern: best-ai-tools-2026, best-lead-generation-tools)
2. Answer the exact Reddit thread with comparison link (non-spammy: post genuine comparison, link in comments)
3. Target longtail: 'best saas demo video tool 2026', 'loom vs arcade vs descript', 'free saas demo screen recorder'
4. Cross-link from existing affiliate pages (best-ai-tools-2026 already live) for internal link juice
5. Repurpose into 3 tweets: 'I compared 7 SaaS demo tools so you don't have to [thread]'

## Budget Tier Strategies

### FREE
Surge deploy + Reddit answer post + internal cross-links from existing affiliate pages + 3 Twitter comparison posts

### LOW
$0-50/mo: Boost comparison tweet, submit to Hacker News 'Ask HN: best SaaS demo tools?' thread

### MID
$50-200/mo: Google Ads on 'saas demo video tool' exact match (buyer intent, $2-4 CPC, affiliate pays $30-150/conv = positive ROI at <5% CTR)

## Daily Actions

- [ ] Copy LANDING/affiliate-pages/best-ai-tools-2026/index.html as template
- [ ] Generate comparison content for 7 tools: Loom, Arcade, Tella, Descript, Synthesia, Camtasia, ScreenStudio
- [ ] Wire affiliate links (placeholder IDs if accounts not yet created — see OPS/AFFILIATE_LINK_SETUP.md)
- [ ] Deploy to surge: saas-demo-tools.surge.sh
- [ ] Generate sitemap.xml and add to OPS/DEPLOYMENT_URLS.md
- [ ] Post to Reddit r/SaaS as genuine answer to similar threads
- [ ] Generate 3 tweets via engagement_bait_converter.py

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory \u2014 use existing affiliate page template from LANDING/affiliate-pages/"
}
```
