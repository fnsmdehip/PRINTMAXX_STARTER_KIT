# Growth Plan: Everyone says AI is unbundling Google Search.

ChatGPT proce

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0 direct — supports SEO/content pipeline worth $50-200/mo via organic traffic + positions for GEO consulting angle at $500-2K/project

---

## Tactics

1. Post contrarian thread: 'AI isn't killing Google SEO — here's the data' with 190x referral stat as hook
2. Repurpose into LinkedIn carousel showing ChatGPT query volume vs referral traffic gap
3. Write GEO explainer blog post targeting 'generative engine optimization' keyword (low competition, rising)
4. Quote-tweet Hiten Shah's thread with our own data point or tool angle
5. Publish comparison page: AI search traffic vs Google referral traffic by niche — organic SEO bait

## Budget Tier Strategies

### FREE
Publish 3-part Twitter thread using 190x stat as hook. Cross-post to LinkedIn. Submit GEO explainer to HN Show HN. Route through engagement_bait_converter.py for 5+ post variants.

### LOW
$10-20 boost on best-performing thread variant. Seed to 2-3 indie hacker subreddits (r/SEO, r/juststart, r/digital_marketing).

### MID
Commission data visualization of AI query vs referral traffic trend. Use as lead magnet for email list. Pitch to SEO newsletters (Detailed, SE Roundtable) as guest data piece.

## Daily Actions

- [ ] Run engagement_bait_converter.py on this entry: extract '190x less referral traffic' stat as primary hook
- [ ] Generate 3 Twitter variants (contrarian take, data thread, hot take) + 1 LinkedIn carousel outline
- [ ] Write 800-word SEO blog post: 'Why AI Search Won't Kill Google Referral Traffic (Yet)' targeting 'GEO optimization' + 'AI vs Google SEO' keywords
- [ ] Add to CONTENT/social/posting_queue/ for next batch posting
- [ ] Add 'geo_content_generator.py' to weekly Monday cron — refreshes AI query volume stats from public sources for evergreen data angle

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
