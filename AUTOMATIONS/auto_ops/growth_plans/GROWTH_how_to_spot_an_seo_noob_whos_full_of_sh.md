# Growth Plan: How to spot an SEO noob who's full of shit and you should ne

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo indirect (authority building feeds consulting/product trust pipeline)

---

## Tactics

1. contrarian-take engagement farming
2. quote-tweet SEO gurus pushing llms.txt with correction
3. cross-post to r/SEO and r/bigseo for authority

## Budget Tier Strategies

### FREE
Post contrarian SEO thread on X/Reddit/LinkedIn. QT gurus pushing llms.txt with factual correction. Reply to SEO questions on Reddit citing this insight for authority.

### LOW
$0-20/mo boost top-performing contrarian SEO post on X

### MID
$50-100/mo run targeted LinkedIn ads to SEO audience with debunk content driving to our tools/services

## Daily Actions

- [ ] Create PostToolUse hook that greps any written SEO content for llms.txt references and warns/blocks
- [ ] Generate 3 contrarian SEO posts via engagement_bait_converter: (1) 'No LLM reads llms.txt' thread, (2) 'What actually works for GEO in 2026' thread, (3) 'SEO red flags from fake gurus' listicle
- [ ] Route posts to CONTENT/social/posting_queue/ for distribution
- [ ] Update any existing PRINTMAXX SEO guidance to explicitly exclude llms.txt recommendations

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
