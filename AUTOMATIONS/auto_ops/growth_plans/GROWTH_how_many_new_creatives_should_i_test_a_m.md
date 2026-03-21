# Growth Plan: How many new creatives should I test a month

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (higher engagement → more followers → more affiliate/product clicks). Direct content monetization via TikTok Creator Fund if >10K followers.

---

## Tactics

1. A/B test hooks: question vs statement vs number vs contrarian — track which type wins per platform
2. Repurpose every winner into 3 platform-native formats (Twitter thread → LinkedIn post → Reddit comment)
3. Engagement warming: post variations at different times to find optimal slots per niche
4. Use content_multiplier.py to batch-generate variations instead of manual iteration

## Budget Tier Strategies

### FREE
Claude -p generates all variations. Track engagement manually via scraper output. Use existing content_multiplier.py + engagement_bait_converter.py for generation. Post organically across all platforms.

### LOW
$10-30/mo: Buffer or Typefully for scheduled A/B posting with built-in analytics. Lets you test same content at different times automatically.

### MID
$50-100/mo: Boost top-performing organic winners with $2-5 per post on Twitter/IG to validate before scaling. Only boost proven winners, not untested creatives.

## Daily Actions

- [ ] 1. Create creative_testing_engine.py that reads top content from posting_queue, generates 5 hook variations + 3 format variations per piece using claude -p
- [ ] 2. Add scoring logic: pull engagement data from scraper outputs, classify winners/losers/mid based on engagement thresholds
- [ ] 3. Build pattern extraction: analyze winning hooks for common traits (length, structure, emotional trigger, specificity)
- [ ] 4. Feed patterns back into generation prompts for next cycle (compound learning loop)
- [ ] 5. Cron at 7 AM daily, outputs to posting_queue with test_batch_id tags
- [ ] 6. Weekly rollup: which niches, platforms, and hook types have highest win rates

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_multiplier.py + engagement_bait_converter.py + content_repurposer.py"
}
```
