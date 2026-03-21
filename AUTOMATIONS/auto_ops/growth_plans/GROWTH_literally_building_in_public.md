# Growth Plan: Literally building in public

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Use #buildinpublic + #indiehacker + #microsaas tags on every post
2. Reply to other #buildinpublic posts with our real numbers to piggyback their reach
3. Post revenue=$0 honestly — zero-revenue transparency outperforms fake wins in this niche
4. Milestone posts (Day 1, Day 30, Day 44, first dollar) get 3-5x normal engagement
5. Quote-tweet our own old posts with updates — 'Day 1 vs Day 44' format
6. Ask a question at end of every post — drives replies which push algo distribution

## Budget Tier Strategies

### FREE
Post daily metrics thread using real LEDGER data (leads, scripts, apps deployed, revenue). Engage with top 10 #buildinpublic accounts daily via thoughtful replies. Cross-post to r/MicroSaas, r/indiehackers with expanded writeup.

### LOW
$0-50/mo: Boost top-performing transparency post once/week ($5-10). Submit milestone posts to IndieHackers milestones section. Join 2-3 founder Slack communities and share updates.

### MID
$50-200/mo: Sponsor a #buildinpublic newsletter recap. Pay a ghostwriter to expand best tweets into full blog posts for SEO. Run targeted X ads to founder/solopreneur audience on milestone content.

## Daily Actions

- [ ] Read OPS/HEARTBEAT.md + LEDGER metrics (leads analyzed, scripts count, apps live, revenue)
- [ ] Read git log --oneline --since='24 hours ago' for commit activity
- [ ] Generate 3 post formats: (1) raw numbers thread, (2) today's win/loss, (3) question hook
- [ ] Run through engagement_bait_converter.py for hook optimization
- [ ] Append to CONTENT/social/posting_queue/ with platform tags
- [ ] Cron runs daily at 7 AM, pairs with existing content pipeline

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_multiplier.py"
}
```
