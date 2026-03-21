# Growth Plan: [ACQUISITION] Show HN: Added API key support to my AI writin

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Post Show HN on launch day — HN drives organic installs and VC eyeballs with zero ad spend
2. BYOK framing is a trust hook: 'your API key, your data, your bill' — use in all copy
3. Target r/productivity, r/ChatGPT, r/webdev, r/artificial on launch week
4. AlternativeTo + BetaList + ProductHunt same-day launch stack for install spike
5. Chrome Web Store keyword optimization: 'AI writing assistant', 'ChatGPT Chrome extension', 'Claude extension'
6. Pin a 'how to get your API key' YouTube short to reduce BYOK friction — repurpose as content

## Budget Tier Strategies

### FREE
Show HN post + 3 subreddit posts + Chrome Web Store organic + AlternativeTo listing + ProductHunt launch + 3 tweets via posting queue

### LOW
$20-50 Reddit ads targeting r/ChatGPT and r/productivity during launch week only

### MID
$50-150 outreach to 5-10 mid-tier productivity YouTube creators for honest reviews in exchange for lifetime access

## Daily Actions

- [ ] Run hn_extension_gap_scanner.py — maps existing AI writing extensions, flags BYOK gaps and underserved niches
- [ ] Pick top-scoring niche (likely legal writing or sales copy — both underserved vs productivity generalist)
- [ ] Build minimal Chrome extension: text selection → Claude API call via user-provided key → rewrite/improve in popup
- [ ] Submit to Chrome Web Store ($5 one-time dev fee) + Firefox Add-ons (free)
- [ ] Post Show HN + distribute to 3 subreddits via posting queue
- [ ] Run engagement_bait_converter.py on the launch to generate 3 tweets + 1 thread (Rule 9)
- [ ] Add cron entry for daily hn_extension_gap_scanner.py run to monitor competitor launches

## Tooling

```json
{
  "browser": "playwright",
  "email": "none",
  "content": "engagement_bait_converter.py + content_factory"
}
```
