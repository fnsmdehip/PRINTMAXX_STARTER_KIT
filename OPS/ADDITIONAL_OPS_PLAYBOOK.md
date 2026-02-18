# Additional Ops Playbook

High-value operations beyond the core money method lifecycle.

---

## 1. Alpha Extraction Ops

### Twitter Alpha Mining (Daily)

**What:** Systematically extract tactics from high-signal accounts.

```markdown
## Process
1. Scan HIGH_SIGNAL_SOURCES.csv (67 accounts)
2. Identify posts with: numbers, tactics, frameworks
3. Deep-dive: click into tweet, check self-reply, profile bio, funnel
4. Log to ALPHA_STAGING.csv with category
5. Weekly: approve and integrate via /review-alpha

## Output
- LEDGER/ALPHA_STAGING.csv (new entries)
- Method-specific tactic integration
```

### Reddit Signal Mining (Weekly)

**What:** Scrape proven tactics from solopreneur subreddits.

```markdown
## Target Subs
- r/SaaS (revenue posts, launch retrospectives)
- r/EntrepreneurRideAlong (service business tactics)
- r/juststart (affiliate site case studies)
- r/coldemail (deliverability updates)
- r/indiehackers (launch tactics)

## Filter For
- Posts with specific revenue numbers
- "Here's what worked" retrospectives
- Tool recommendations with results
- Failure post-mortems with lessons
```

### Bookmark Intelligence Ops

**What:** Process X bookmarks for accumulated alpha.

See: `AUTOMATIONS/x_bookmarks/MANUAL_EXTRACTION_WORKFLOW.md`

---

## 2. Competitive Intelligence Ops

### Competitor Shadow Ops (Weekly)

**What:** Track competitor moves in real-time.

```markdown
## Per Competitor
1. Sign up for their email list
2. Follow their social accounts
3. Set Google Alerts for brand name
4. Track pricing page changes (Visualping)
5. Monitor App Store updates
6. Track their job postings (signals scaling)

## Output
- MONEY_METHODS/{METHOD}/competitive/COMPETITOR_INTEL.md
- Weekly update log
```

### Pricing Intelligence Ops

**What:** Track market pricing to optimize your positioning.

```markdown
## Process
1. Screenshot competitor pricing pages monthly
2. Note any changes, new tiers, removed features
3. Cross-reference with reviews (value perception)
4. Adjust own pricing based on positioning

## Output
- MONEY_METHODS/{METHOD}/research/PRICING_TRACKER.md
```

### Feature Gap Analysis Ops

**What:** Find unserved needs in competitor products.

```markdown
## Process
1. Aggregate 1-star reviews of competitors
2. Categorize complaints (UX, features, pricing, support)
3. Identify patterns (>5 similar complaints = opportunity)
4. Prioritize by build effort vs. value

## Output
- MONEY_METHODS/{METHOD}/research/FEATURE_GAPS.md
```

---

## 3. Content Multiplication Ops

### Atomic Content Ops

**What:** Break one piece into 20+ pieces.

```markdown
## From One Long-Form Piece
- 10 tweet threads (different angles)
- 5 LinkedIn posts
- 3 email sequences
- 1 YouTube script
- 10 TikTok hooks
- 5 carousel slides
- 1 podcast episode outline
- Newsletter issue
- Quora answers (3-5)
- Reddit posts (2-3)

## Ralph Task
"Take CONTENT/{piece}.md and generate all atomic variants.
Output to CONTENT/atomic/{piece}/"
```

### Content Repurposing Pipeline

```
Blog Post → Twitter Thread → LinkedIn Post → Email → Video Script → Podcast Notes
    ↓
Carousel → Infographic → Quote Graphics → Meme → Shorts
```

### Evergreen Refresh Ops

**What:** Update old content for fresh traffic.

```markdown
## Quarterly Refresh
1. Identify top 20 performing pieces
2. Update stats, screenshots, tools mentioned
3. Add new sections for new developments
4. Republish with updated date
5. Re-promote on social

## Output
- Updated content files
- LEDGER/CONTENT_REFRESH_LOG.csv
```

---

## 4. Distribution Multiplication Ops

### Platform Expansion Ops

**What:** Systematically expand to new platforms.

```markdown
## Platform Priority Matrix

| Platform | Effort | Potential | Priority |
|----------|--------|-----------|----------|
| X | Low | High | Phase 1 |
| LinkedIn | Low | High | Phase 1 |
| TikTok | Medium | High | Phase 2 |
| YouTube | High | Very High | Phase 2 |
| Instagram | Medium | Medium | Phase 3 |
| Threads | Low | Medium | Phase 3 |
| Pinterest | Medium | Niche | Phase 4 |
| Reddit | Low | High (risky) | Ongoing |
| Quora | Low | Medium | Ongoing |
```

### Cross-Posting Automation Ops

**What:** Automate multi-platform distribution.

```markdown
## Flow
1. Create canonical content
2. Platform-adapt (format, length, hashtags)
3. Queue via Buffer/Hypefury
4. Schedule optimal times per platform
5. Track engagement back to canonical

## Tools
- Buffer for X, LinkedIn, TikTok
- Hypefury for X-specific
- Later for Instagram
- Metricool for all-in-one
```

### Community Seeding Ops

**What:** Strategic presence in relevant communities.

```markdown
## Target Communities
- Indie Hackers (profile + posts)
- Hacker News (for launches)
- Dev.to (technical content)
- Product Hunt (product launches)
- Slack communities (niche-specific)
- Discord servers (niche-specific)
- Facebook groups (older demographics)

## Process
1. Join, lurk, understand culture
2. Provide value (answer questions)
3. Build reputation over weeks
4. Then occasionally promote
5. Never spam (instant ban)
```

---

## 5. Relationship Building Ops

### Strategic Outreach Ops

**What:** Build relationships that compound.

```markdown
## Target Categories
1. Potential partners (complementary products)
2. Influencers in niche (micro: 5-50k followers)
3. Podcast hosts (guest opportunities)
4. Newsletter writers (cross-promo)
5. Community leaders (co-marketing)

## Process
1. Identify 50 targets per category
2. Follow, engage authentically (2 weeks)
3. Warm outreach with specific value offer
4. Track responses in CRM
5. Nurture relationships over time
```

### Podcast Guesting Ops

**What:** Systematic podcast outreach for authority + traffic.

```markdown
## Process
1. Find 100 podcasts in niche (ListenNotes, Podchaser)
2. Filter: active, relevant audience, accepts guests
3. Listen to 1 episode per show (understand format)
4. Craft personalized pitch per show
5. Send via cold email sequence
6. Prepare talking points once booked

## Output
- MONEY_METHODS/*/outreach/PODCAST_TARGETS.csv
- MONEY_METHODS/*/outreach/PODCAST_PITCHES/
```

### Affiliate/Partner Recruitment Ops

**What:** Build distribution through others.

```markdown
## Process
1. Identify potential affiliates (content creators, agencies)
2. Create affiliate program (RevenueCat, Rewardful)
3. Prepare affiliate kit (copy, graphics, tracking)
4. Outreach sequence (3-5 touches)
5. Onboard and support active affiliates
6. Monthly payout and relationship check-in

## Output
- MONEY_METHODS/APP_FACTORY/affiliate_program/
- MONEY_METHODS/*/affiliates/AFFILIATE_KIT.md
```

---

## 6. Conversion Optimization Ops

### Landing Page Ops

**What:** Systematic landing page improvement.

```markdown
## Monthly Audit
1. Check load speed (Lighthouse)
2. Review heatmaps (Hotjar)
3. Analyze form drop-offs
4. Test new headlines (A/B)
5. Test new CTAs (A/B)
6. Review mobile experience
7. Update social proof

## Output
- OPS/logs/LP_OPTIMIZATION_LOG.md
```

### Email Sequence Ops

**What:** Continuous email improvement.

```markdown
## Metrics to Track
- Open rate (benchmark: 20%+)
- Click rate (benchmark: 2%+)
- Reply rate (for cold email: 5%+)
- Conversion rate
- Unsubscribe rate

## Monthly Optimization
1. Identify worst-performing emails
2. A/B test subject lines
3. A/B test CTAs
4. Test send times
5. Prune non-engagers

## Output
- MONEY_METHODS/*/email_sequences/PERFORMANCE_LOG.md
```

### Pricing Ops

**What:** Optimize pricing for revenue.

```markdown
## Experiments
1. Price point testing (low/mid/high)
2. Tier structure testing (features per tier)
3. Annual vs monthly discount
4. Trial length testing
5. Decoy pricing (value tier)

## Process
1. Set up tracking for each variant
2. Run 2 weeks minimum per test
3. Measure conversion AND LTV
4. Implement winner
5. Document learnings
```

---

## 7. Financial Ops

### Revenue Tracking Ops

**What:** Know your numbers.

```markdown
## Daily
- Check Stripe/RevenueCat dashboard
- Note any anomalies

## Weekly
- Update LEDGER/FUNNEL_METRICS.csv
- Calculate CAC by channel
- Calculate LTV by cohort

## Monthly
- Full P&L review
- Unit economics calculation
- Runway calculation
- Cash flow projection
```

### Cost Optimization Ops

**What:** Reduce spend without reducing output.

```markdown
## Quarterly Review
1. Audit all subscriptions
2. Check usage vs. tier (downgrade unused)
3. Negotiate annual pricing
4. Find cheaper alternatives
5. Cancel unused tools

## Common Wins
- Downgrade unused SaaS tiers
- Use Haiku over Sonnet where possible
- Batch API calls to reduce costs
- Use free tiers strategically
- Negotiate startup discounts
```

### Tax Optimization Ops

**What:** Legal tax efficiency.

```markdown
## Quarterly
1. Track deductible expenses
2. Separate personal/business
3. Plan estimated payments
4. Review entity structure
5. Consult accountant as needed

## Common Deductions
- Software subscriptions
- Home office
- Equipment
- Travel for business
- Contractor payments
- Advertising spend
```

---

## 8. System Maintenance Ops

### Tech Debt Ops

**What:** Keep systems healthy.

```markdown
## Monthly
1. Update dependencies
2. Review error logs
3. Clean up unused code
4. Optimize slow queries
5. Archive old data
6. Test backup/restore

## Output
- OPS/logs/TECH_MAINTENANCE_LOG.md
```

### Documentation Ops

**What:** Keep docs current.

```markdown
## Quarterly
1. Review all SOPs for accuracy
2. Update screenshots/examples
3. Archive obsolete docs
4. Fill documentation gaps
5. Cross-link related docs
```

### Security Ops

**What:** Protect your assets.

```markdown
## Monthly
1. Review account access (revoke unused)
2. Update passwords (rotate critical)
3. Check 2FA on all accounts
4. Review API key usage
5. Backup critical data
6. Test recovery procedures
```

---

## 9. Learning/Growth Ops

### Skill Building Ops

**What:** Continuous capability improvement.

```markdown
## Quarterly Skill Audit
1. Identify skill gaps blocking growth
2. Find best resources for each gap
3. Schedule learning time
4. Apply immediately (learn by doing)
5. Document learnings for future reference

## Priority Skills
- Copywriting (always)
- Paid ads (for scaling)
- Video editing (for content)
- Data analysis (for optimization)
- Sales (for high-ticket)
```

### Network Building Ops

**What:** Strategic relationship development.

```markdown
## Monthly
1. Attend 1-2 virtual events
2. Send 5 "just checking in" messages
3. Make 3 introductions (give first)
4. Respond to all inbound requests
5. Share others' content publicly
```

---

## 10. Exit/Transition Ops

### Asset Documentation Ops

**What:** Prepare for sale or handoff.

```markdown
## Ongoing
1. Document all processes
2. Record all account access
3. Track all revenue sources
4. Maintain clean financials
5. Keep code documented
6. Archive important decisions

## Output
- Ready for due diligence at any time
- Clean handoff if selling or hiring
```

### Optionality Ops

**What:** Keep doors open.

```markdown
## Build for Multiple Exits
1. Can run as passive income
2. Can sell to acquirer
3. Can hire team to run
4. Can merge with complementary business
5. Can spin off components

## Maintain Flexibility
- Don't over-depend on one channel
- Document everything
- Build systems over personal reliance
- Keep relationships warm
```

---

## Ops Prioritization Framework

### Weekly Ops Priority

```
1. Revenue-generating ops (sales, outreach, launches)
2. Amplification ops (content, distribution)
3. Optimization ops (A/B tests, improvements)
4. Infrastructure ops (systems, maintenance)
5. Learning ops (skills, network)
```

### Time Allocation

```
60% - Direct revenue activities
25% - System building/optimization
15% - Learning/relationship building
```

---

## Ralph Integration

All ops can be Ralph-ified with clear success criteria.

**Template:**
```markdown
# Task: [OP NAME]

## Context
- Read [relevant docs]
- Output to [specific location]

## Success Criteria
1. [ ] [Specific, verifiable output 1]
2. [ ] [Specific, verifiable output 2]
3. [ ] [Quality check]
4. [ ] Saved to correct location
```

---

## Related Documents

- `OPS/MONEY_METHOD_OPS_FRAMEWORK.md` - Core lifecycle ops
- `OPS/RALPH_LOOP_GUIDE.md` - Overnight automation
- `OPS/AUTONOMOUS_TASKS.md` - What can run unattended
- `LEDGER/` - All tracking files

---

Last updated: 2026-01-22
