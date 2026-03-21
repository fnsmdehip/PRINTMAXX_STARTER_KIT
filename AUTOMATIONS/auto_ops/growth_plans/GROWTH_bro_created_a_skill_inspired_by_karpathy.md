# Growth Plan: bro created a skill inspired by Karpathy's autoresearch to f

**Created:** 2026-03-20 23:12
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. post skill score improvement screenshots on Twitter (56%→92% in 4 rounds is a proven hook)
2. open source the refinement framework on GitHub → drives inbound to paid skill packs
3. seed in Claude Code subreddit and Indie Hackers with before/after quality proof
4. offer free refined skill audit to 10 people in exchange for testimonials
5. cross-promote in OpenClaw and Claude Code communities as the anti-slop skill optimizer

## Budget Tier Strategies

### FREE
Post case study thread on Twitter with real quality scores. Engage Claude Code community. Open source the test framework (keep refined skills paid). Submit to Hacker News Show HN.

### LOW
$20-30 on X promoted post targeting Claude Code power users. Submit to Product Hunt as Claude Code skill optimizer tool.

### MID
$50-100 sponsoring Claude Code newsletter or community. Bundle with existing digital products for upsell.

## Daily Actions

- [ ] Create skill_refinement_engine.py: scans .claude/skills/, scores each via claude -p with rubric, outputs scores to LEDGER/SKILL_QUALITY_SCORES.csv
- [ ] Create ralph loop at ralph/loops/skill_refiner/ with PROMPT.md that iterates: read lowest-scored skill → generate test cases → run 4 critique cycles → rewrite → re-score → write improved version
- [ ] Add PostToolUse hook: after any skill Edit, auto-trigger quick re-score on that file
- [ ] After first run: package top 10 refined skills into DIGITAL_PRODUCTS/ready_to_sell/LISTING_refined_claude_skills_pack.md
- [ ] Generate 3 tweets via engagement_bait_converter.py: '56% → 92% in 4 rounds' hook format
- [ ] Add weekly cron (Sunday 3 AM) to re-audit all skills and flag regressions

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py for case study tweets"
}
```
