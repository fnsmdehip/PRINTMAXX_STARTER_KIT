# Growth Plan: Monetize existing skills portfolio. No new builds needed. Pr

**Created:** 2026-03-20 18:09
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Cross-post skill launches to r/claudeAI r/SideProject r/IndieHackers with genuine build story
2. Tweet each skill listing individually for 5x content from one launch
3. Reply to AI agent threads on X with link to specific relevant skill
4. Bundle discount urgency ($49 launch week, $79 after) on Gumroad
5. List on Product Hunt as collection when 5+ skills live

## Budget Tier Strategies

### FREE
Cross-post to Reddit/X/IndieHackers, engage in AI agent community threads, reply-market under relevant tweets, leverage existing PRINTMAXX content pipeline for launch posts

### LOW
$0-50/mo: Boost top-performing skill tweet, small Reddit ad targeting r/claudeAI subscribers

### MID
$50-200/mo: Micro-influencer review (send free bundle to 3 AI YouTubers), featured listing on marketplaces if available

## Daily Actions

- [ ] Scan AUTOMATIONS/ for top 5 most complete, documented, standalone scripts (quality_gate scoring)
- [ ] Verify AgentPowers.ai, SkillsMP, SkillHub actually exist and accept submissions (playwright check)
- [ ] For each skill: auto-generate README.md from docstrings + usage examples
- [ ] Use Playwright to capture demo screenshot of each skill running in terminal
- [ ] Create DIGITAL_PRODUCTS/skill_marketplace_bundle/ with all 5 packaged skills
- [ ] Write Gumroad listing markdown for Operator Pack at $49 (BLOCKER: Gumroad account needed)
- [ ] Submit to each verified marketplace via their submission process
- [ ] Generate 3 tweets + 1 thread per Rule 9 about the skill marketplace launch
- [ ] Add weekly cron to re-scan for new listable skills and auto-package

## Tooling

```json
{
  "browser": "playwright for demo screenshots",
  "email": "none",
  "content": "content_factory for launch posts"
}
```
