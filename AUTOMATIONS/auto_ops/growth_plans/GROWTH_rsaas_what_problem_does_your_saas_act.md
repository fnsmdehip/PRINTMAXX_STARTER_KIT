# Growth Plan: [r/SaaS] What problem does your SaaS actually solve? I’ll tr

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Extend existing background_reddit_scraper.py with r/SaaS subreddit + keyword filter (problem, solve, users, beta, traction, validate)
2. Extract post author username + flair (founder signals) + SaaS description from thread body
3. Score lead quality: upvotes + comment count + specific problem statement = higher intent
4. Append qualified leads to EAS pipeline CSV with source=reddit_saas and pain_point extracted from post title
5. Trigger chain_cold_outbound with SaaS-specific angle: 'saw your r/SaaS post about X — we help founders get first 100 users'

## Budget Tier Strategies

### FREE
Daily reddit scrape of r/SaaS + r/indiehackers + r/startups for founder posts. Filter by keywords: 'users', 'problem', 'validate', 'traction', 'beta'. Route to existing EAS cold email scripts. Zero cost, pure pipeline extension.

### LOW
$0-50/mo — Add Reddit API key for higher rate limits. Use Instantly free tier for 50 emails/day to SaaS founders.

### MID
$50-200/mo — Upgrade Instantly for volume. Add LinkedIn scrape cross-reference (founder on Reddit = likely has LinkedIn with direct email).

## Daily Actions

- [ ] Extend background_reddit_scraper.py: add r/SaaS to subreddit list with keywords ['problem', 'solve', 'users', 'validate', 'traction', 'beta testers', 'real users']
- [ ] Parse post: extract title, body snippet, author, post URL, upvotes, comment count
- [ ] Score: upvotes > 10 + specific problem statement + low comment count (less competition) = HIGH intent lead
- [ ] Append to LEDGER/INBOUND_LEADS.csv with source=reddit_saas, pain_point=extracted_text, contact=reddit_username
- [ ] Wire into chain_cold_outbound with template: SaaS-specific cold outreach referencing their exact problem statement
- [ ] Run daily at 7 AM via existing cron

## Tooling

```json
{
  "browser": "none \u2014 Reddit JSON API works without browser",
  "email": "existing cold email scripts",
  "content": "none"
}
```
