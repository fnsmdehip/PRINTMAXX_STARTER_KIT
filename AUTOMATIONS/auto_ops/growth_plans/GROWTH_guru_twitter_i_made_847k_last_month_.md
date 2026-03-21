# Growth Plan: Guru Twitter: "I made $847K last month, here's my morning ro

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo direct (engagement/followers → funnel to paid products), $500-2K/mo indirect (audience building accelerant for all other ventures)

---

## Tactics

1. QT guru tweets with the debunk — rides their viral wave for free impressions
2. Reply-bait format: post the guru claim, then reply with the real reason — algo treats as conversation
3. Screenshot format posts (guru tweet + red circle/annotation) get 3x shares over text-only
4. Cross-post debunks to r/Entrepreneur and r/juststart where guru hate = upvotes
5. Tag/mention the original guru sparingly — controversy drives engagement but avoid harassment flags
6. Bundle 5-10 debunks into a weekly thread: 'This week in guru BS' — becomes a recurring series people follow for

## Budget Tier Strategies

### FREE
QT viral guru tweets with contrarian take, reply-bait under trending guru threads, cross-post to Reddit/HN where anti-guru sentiment is high, use engagement_bait_converter for multi-platform repurposing

### LOW
$10-30/mo boost top-performing debunk threads on X, A/B test hook formats (question vs statement vs screenshot)

### MID
$50-100/mo run promoted contrarian content as ads targeting entrepreneur audiences, collab with other debunker accounts

## Daily Actions

- [ ] 1. Build guru_debunker_content_gen.py: scrape revenue-claim tweets, extract real method vs stated attribution using Claude
- [ ] 2. Create 5 content templates: 'What they say vs reality', 'The actual reason', 'Guru morning routine vs P&L', 'I reverse-engineered their Stripe', 'Nobody made money from cold plunges'
- [ ] 3. Wire into existing content_factory chain and posting_queue
- [ ] 4. Use procedural memory contrarian hook pattern: 'Contrarian hook: challenge conventional wisdom'
- [ ] 5. Generate 3 posts/day minimum, queue in CONTENT/social/posting_queue/
- [ ] 6. Track engagement vs baseline content — expect 2-3x on contrarian posts
- [ ] 7. Feed high-performing formats back into engagement_bait_converter as templates
- [ ] 8. Cross-pollinate: when debunking reveals a REAL method, route that method back to alpha_staging as new alpha

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter + content_repurposer"
}
```
