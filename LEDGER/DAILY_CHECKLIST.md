# PRINTMAXX Daily Operator Checklist

Run through this checklist every day. Takes 15-30 minutes.

---

## Morning tasks (before 9am)

### Content queue
- [ ] Run `make queue` to see what needs posting
- [ ] Post content to each platform (or schedule)
- [ ] Run `make post ID=xxx` to mark as posted
- [ ] Check engagement on yesterday's posts

### Account health
- [ ] Check X account status (no restrictions)
- [ ] Check Instagram account (no shadowban)
- [ ] Check TikTok account (no violations)
- [ ] Verify proxies are working (if using automation)

### Email
- [ ] Check warmup tool status (Instantly, Smartlead)
- [ ] Review any bounces or complaints
- [ ] Check cold email campaign replies

---

## Content creation (midday)

### New content
- [ ] Write 3 posts per niche (9 total)
- [ ] Schedule for next 3 days
- [ ] Add to LEDGER/CONTENT_PIPELINE.csv

### Research
- [ ] Run `/daily-research` for new alpha
- [ ] Check HIGH_SIGNAL_SOURCES for new posts
- [ ] Save interesting finds to ALPHA_STAGING.csv

---

## Metrics check (evening)

### Social metrics
| Platform | Metric | Target | Today |
|----------|--------|--------|-------|
| X | Impressions | 5k+ | |
| X | Followers | +10 | |
| Instagram | Reach | 1k+ | |
| TikTok | Views | 500+ | |

### Revenue metrics
| Source | Metric | Target | Today |
|--------|--------|--------|-------|
| Affiliate | Clicks | 10+ | |
| Leads | New leads | 5+ | |
| App downloads | New installs | 5+ | |

### Update tracking
- [ ] Update LEDGER/FUNNEL_METRICS.csv with today's numbers
- [ ] Log wins/losses in notes

---

## Weekly tasks (pick one day)

### Monday: Content audit
- [ ] Review content performance from last week
- [ ] Identify top 3 performing posts
- [ ] Plan content themes for this week

### Tuesday: Technical health
- [ ] Run `make validate` to check all files
- [ ] Review any blocked tasks in OPS/logs/
- [ ] Update any stale CSVs

### Wednesday: Outreach
- [ ] Send 10 cold DMs to potential customers
- [ ] Follow up on any pending conversations
- [ ] Update LEDGER/OUTREACH_PIPELINE.csv

### Thursday: Alpha review
- [ ] Run `/review-alpha` to check staging
- [ ] Integrate approved findings to master files
- [ ] Update ALPHA_WATCHLIST with new platforms

### Friday: Planning
- [ ] Review week's metrics
- [ ] Plan next week's content calendar
- [ ] Update LEDGER/MASTER_TASKS.md if needed

---

## Quick commands reference

```bash
# Content
make queue              # Show items to post
make post ID=A001       # Mark as posted
make content N=10       # Generate content placeholders

# Validation
make validate           # Run all validators
make status             # Show current project status

# Apps
make apps               # Show app build status
make test-app APP=xxx   # Test specific app

# Development
make dev                # Start Next.js server
make build              # Production build
```

---

## Emergency protocols

### Account restricted
1. Stop all automation immediately
2. Log in manually and complete any verification
3. Wait 24-48 hours before resuming
4. Document in OPS/logs/BLOCKED_account_[platform].md

### Bounce rate spike
1. Pause all cold email campaigns
2. Review bounced addresses
3. Check domain reputation (MXToolbox)
4. Contact email provider if needed

### Traffic drop
1. Check Google Search Console for issues
2. Review any recent content changes
3. Check competitor activity
4. Document in OPS/logs/traffic_investigation.md

---

## Notes

Use this space for daily observations:

### $(date +%Y-%m-%d)
-

---

Last updated: 2026-01-21
