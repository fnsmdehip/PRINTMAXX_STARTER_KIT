# Growth Plan:            A dormant address containing 2,100 #BTC (147,695,

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-20/mo

---

## Tactics

1. Quote-tweet actual whale-alert.io posts with commentary — rides their audience
2. Tag $BTC $ETH in posts for hashtag discovery
3. Post within 15min of whale movement for recency boost on crypto Twitter

## Budget Tier Strategies

### FREE
Auto-generate 1-2 posts per whale event via engagement_bait_converter.py, post to Twitter warmup queue — zero cost, rides real-time crypto news cycle

### LOW
$0-50/mo — boost top-performing whale posts ($5-10 each) to crypto audiences on Twitter Ads

### MID
$50-200/mo — sponsor crypto newsletter inclusion when whale events go viral

## Daily Actions

- [ ] Call engagement_bait_converter.py with this entry — generates 3 post variants (hook/question/stat format)
- [ ] Add generated posts to CONTENT/social/posting_queue/ with crypto tag
- [ ] Wire whale_alert_content_generator.py to poll whale-alert.io RSS every 4h for new dormancy reactivations
- [ ] Filter: dormancy >3yr AND value >$500K only — noise reduction
- [ ] Cron 0 */4 * * * — runs passively, zero maintenance

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
