# Growth Plan: Is Social Media A Waste OF Time

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct — engagement/follower growth asset only

---

## Tactics

1. contrarian-hook engagement farming
2. quote-tweet bait on polarizing social media ROI takes
3. cross-post debate framing to r/sweatystartup and r/EntrepreneurRideAlong

## Budget Tier Strategies

### FREE
Post contrarian 'social media is a waste of time for X' takes across Twitter/Reddit/LinkedIn. Use debate framing to drive replies. Repurpose top comments as follow-up threads.

### LOW
$0-20/mo boost top-performing contrarian posts on Twitter/LinkedIn

### MID
N/A — content hook, not a revenue method

## Daily Actions

- [ ] Run entry through engagement_bait_converter.py with contrarian-hook template
- [ ] Generate 3 debate-framed posts: Twitter thread, Reddit comment-bait, LinkedIn hot take
- [ ] Add to CONTENT/social/posting_queue/ with contrarian tag
- [ ] Schedule via existing content cron — no new infrastructure needed

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
