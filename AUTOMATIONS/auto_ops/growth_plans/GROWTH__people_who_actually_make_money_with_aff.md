# Growth Plan:  people who actually make money with affiliate marketing, ca

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Question-format posts get 3-5x reply rate vs statements — algorithm rewards reply depth
2. Cross-post the SAME question across Twitter, Reddit r/juststart r/affiliatemarketing r/Entrepreneur, and Indie Hackers
3. Use replies as UGC social proof — screenshot best answers for follow-up threads
4. Tag 2-3 known affiliate marketers in the post to seed initial engagement

## Budget Tier Strategies

### FREE
Organic question posts across 3 platforms, scrape replies, repurpose best answers into threads and listicles. Use engagement_bait_converter.py for format variations.

### LOW
$0-20/mo — boost top-performing question posts on Twitter to reach more practitioners

### MID
$50-100/mo — run targeted ads with question-format hooks to affiliate marketing audiences, harvest landing page email signups from the discussion

## Daily Actions

- [ ] Route hook template to engagement_bait_converter.py to generate 5 niche variations
- [ ] Add variations to CONTENT/social/posting_queue/ with 2x/week schedule (Mon+Thu)
- [ ] Configure twitter_alpha_scraper.py and background_reddit_scraper.py to monitor reply threads
- [ ] Run reply extraction through alpha_auto_processor.py to catch real methods in responses
- [ ] Best replies become new alpha entries — self-feeding loop
- [ ] Repurpose top answer threads into listicle content via content_repurposer.py

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
