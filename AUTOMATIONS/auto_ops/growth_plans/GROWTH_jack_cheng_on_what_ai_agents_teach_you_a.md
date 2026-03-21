# Growth Plan: Jack Cheng on what AI agents teach you about the systems you

**Created:** 2026-03-20 23:36
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0 direct / follower growth asset

---

## Tactics

1. Use 'what X taught me about systems you ignore' hook structure for 3 threads — high engagement format in builder/founder communities
2. Anchor posts to PRINTMAXX real numbers (33 agents, 651 scripts, 191K leads) — specificity converts skimmers to followers
3. Cross-post to indie hacker communities where systems/ops content outperforms revenue flexing

## Budget Tier Strategies

### FREE
Run engagement_bait_converter.py on this hook pattern. Generate 3 posts: (1) what building 33 agents revealed about our broken manual ops, (2) specific system we were ignoring that agents exposed, (3) the invisible debt every solopreneur ignores. Queue to CONTENT/social/posting_queue/.

### LOW
$0-50: boost top-performing post if engagement exceeds 5% in first 2h

### MID
N/A — content-only play, no paid distribution warranted at this quality tier

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --hook 'what AI agents teach you about systems you ignore' --use-real-data --venture CONTENT
- [ ] Pull real data points from AUTOMATIONS/agent/swarm/swarm_state.json and OPS/HEARTBEAT.md for proof anchors
- [ ] Generate 3 posts + 1 thread using PRINTMAXX's actual agent discoveries as the narrative
- [ ] Append to CONTENT/social/posting_queue/ for warmup-aware posting

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
