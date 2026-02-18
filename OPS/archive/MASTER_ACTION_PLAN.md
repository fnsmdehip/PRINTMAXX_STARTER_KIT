# PRINTMAXX Master Action Plan

Single source of truth for execution. Prioritized by ROI and dependency order.

Last updated: 2026-01-21

---

## Executive Summary

**Budget:** $200-$1500 bootstrap
**Timeline:** 90 days to $10k MRR target
**Strategy:** Apps + Content + Outreach running in parallel

**Highest ROI actions (do first):**
1. Link RevenueCat to Stripe (unblocks all app revenue)
2. Buy Soax proxy (unblocks social automation)
3. Create social accounts (unblocks content distribution)
4. Submit first app (unblocks revenue)

---

## Phase 1: Immediate (Today)

### Critical path blockers - DO THESE NOW

| Task | Owner | Time | Cost | Blocks |
|------|-------|------|------|--------|
| Link RevenueCat to Stripe | Human | 15 min | $0 | All app revenue |
| Buy Soax mobile proxy | Human | 5 min | $99/mo | Social automation |
| Buy domains (prayerlock.app, walktounlock.app) | Human | 10 min | ~$20 | Landing pages, email |
| Create support@prayerlock.app email | Human | 10 min | $6/mo | App Store submission |

### Ralph can do in parallel

| Task | Agent | Output |
|------|-------|--------|
| Build PrayerLock MVP | Ralph | /MONEY_METHODS/APP_FACTORY/products/prayerlock/ |
| Generate app store screenshots | Ralph | /MONEY_METHODS/APP_FACTORY/assets/ |
| Draft privacy policy | Ralph | /LANDING/printmaxx-site/public/privacy/ |
| Write app descriptions | Ralph | /MONEY_METHODS/APP_FACTORY/marketing/ |

### Success criteria for Day 1

- [ ] RevenueCat shows Stripe connected
- [ ] Soax proxy credentials in .env
- [ ] 2 domains purchased
- [ ] Support emails configured

---

## Phase 2: This Week (Days 1-7)

### Human tasks (cannot automate)

#### Social account creation (Day 1-2)

| Platform | Handle | Email | Notes |
|----------|--------|-------|-------|
| TikTok | @prayerlock | support@prayerlock.app | Phone required |
| Instagram | @prayerlock | support@prayerlock.app | Phone required |
| X/Twitter | @prayerlock | support@prayerlock.app | No phone needed |
| TikTok | @walktounlock | support@walktounlock.app | Phone required |
| Instagram | @walktounlock | support@walktounlock.app | Phone required |
| X/Twitter | @walktounlock | support@walktounlock.app | No phone needed |

**Rules:**
- Use different phone numbers if possible
- Complete profile fully before ANY posting
- Post 5-10 manual posts before automation
- Wait 7-14 days before automating

#### Manual posts for warming (Days 2-7)

Post 2x/day per account. Content types:
- Faith: Bible verses, prayer prompts, devotional thoughts
- Fitness: Workout tips, step challenges, motivation

Goal: 10+ posts per account before week end.

### Ralph tasks

| Task | Priority | Output |
|------|----------|--------|
| Complete PrayerLock build | HIGH | Testable app |
| Start WalkToUnlock build | HIGH | /products/walktounlock/ |
| Generate 30 TikTok scripts (faith) | HIGH | /CONTENT/video_scripts/faith/ |
| Generate 30 TikTok scripts (fitness) | HIGH | /CONTENT/video_scripts/fitness/ |
| Build landing pages | MEDIUM | /LANDING/printmaxx-site/app/prayerlock/ |
| Write email welcome sequence | MEDIUM | /MONEY_METHODS/COLD_OUTBOUND/sequences/ |

### Content queue targets

| Platform | App | Posts needed | Type |
|----------|-----|--------------|------|
| TikTok | PrayerLock | 30 | Problem/solution, demos, testimonials |
| TikTok | WalkToUnlock | 30 | Problem/solution, demos, testimonials |
| Instagram | Both | 20 carousels | Tips, how-tos |
| X/Twitter | Both | 50 posts | Tips, engagement hooks |

### Budget allocation (Week 1)

| Item | Cost | Cumulative |
|------|------|------------|
| Soax proxy | $99 | $99 |
| Domains (2) | $20 | $119 |
| Google Workspace (1 user) | $6 | $125 |
| **Week 1 total** | | $125 |

### Success criteria for Week 1

- [ ] Both app MVPs testable (TestFlight)
- [ ] 6 social accounts created and warming
- [ ] Landing pages live
- [ ] 60+ content pieces ready
- [ ] RevenueCat products configured

---

## Phase 3: Week 2 (Days 8-14)

### App submission (HIGH PRIORITY)

#### PrayerLock submission checklist

| Task | Owner | Notes |
|------|-------|-------|
| Create App Store Connect entry | Human | Manual |
| Upload build to TestFlight | Ralph | Via Xcode |
| Create App Store products ($9.99/mo, $49.99/yr) | Human | Manual |
| Link products in RevenueCat | Human | Manual |
| Test purchase flow (sandbox) | Human | Manual |
| Upload screenshots | Human | Ralph generates |
| Submit for review | Human | Manual |

Expected: 2-5 day review time

#### WalkToUnlock submission

Start 2-3 days after PrayerLock submission. Same process.

### Launch social content

Once accounts have 14 days age:
- Enable posting automation (with proxy)
- Start with 1 post/day, ramp to 3/day
- Use winning hooks from ALPHA_STAGING.csv

**Winning hook formats (from alpha research):**

1. **Relationship bait:** "I haven't heard from my BOYFRIEND in FOUR days..." (23.8M views)
2. **AI girl slideshow:** Selfie hook + listicle + brand promo
3. **Problem/solution:** Direct pain point + app demo

### Affiliate recruitment (start this week)

**Target:** 20 affiliates by end of Week 2

**Where to find:**
- Faith micro-influencers (1k-50k followers)
- Fitness nano-influencers
- Productivity creators

**Outreach template:**
```
Hey [Name],

Love your content about [topic]. Your [specific post] was great.

We have an affiliate program for PrayerLock - 25% recurring commission.

Interested? I can send details and some content ideas.

[Name]
```

**Commission structure:**
| Tier | Monthly sales | Commission |
|------|---------------|------------|
| Bronze | 1-10 | 20% |
| Silver | 11-50 | 25% |
| Gold | 51+ | 30% |

**Incentives:**
- $100 bonus for first 10 sales
- $500 bonus for hitting 100 sales

### Ralph tasks (Week 2)

| Task | Priority |
|------|----------|
| Build StudyLock MVP | MEDIUM |
| Generate affiliate landing page | HIGH |
| Create affiliate creative kit | HIGH |
| Write 50 more social posts | MEDIUM |
| Set up email capture on landing pages | HIGH |

### Budget allocation (Week 2)

| Item | Cost | Cumulative |
|------|------|------------|
| Week 1 carry | $125 | $125 |
| No new costs | $0 | $125 |

### Success criteria for Week 2

- [ ] PrayerLock submitted to App Store
- [ ] WalkToUnlock in final testing
- [ ] 10+ affiliates signed up
- [ ] Social posting automated (1-3x/day)
- [ ] First organic content getting traction

---

## Phase 4: Month 1 (Days 15-30)

### App targets

| App | Status target | Revenue target |
|-----|---------------|----------------|
| PrayerLock | Live + 50 downloads | $200 MRR |
| WalkToUnlock | Live + 30 downloads | $100 MRR |
| StudyLock | Submitted | - |
| DailyDevotion (habit tracker) | Building | - |
| FemFit (women's gym) | Building | - |

### Church outreach campaign (HIGH ROI)

**The opportunity:** 380,000+ churches in US. Built-in distribution.

**The offer:**
- Free app for congregation
- Church gets 20% of subscription revenue
- Custom branding option (premium)

**Math:**
- Church has 500 members
- 10% download = 50 users
- 20% convert = 10 paying users
- 10 x $50/yr = $500/yr
- Church gets $100/yr, you get $400/yr

Scale to 100 churches = $40k/yr recurring

**Execution:**

Week 3: VA hiring
- Hire 1-2 VAs on OnlineJobs.ph ($5-6/hr)
- Train on outreach process
- Target: 50 churches/week

Week 4: Scale outreach
- Target: 200 churches contacted
- Expected: 12 positive responses (6% rate)
- Expected: 3 partnerships signed (25% close)

**VA job posting:**
```
Title: Church Outreach Specialist

Tasks:
- Research churches with active social media
- Find pastor/admin contact info
- Send personalized emails (template provided)
- Track responses in spreadsheet
- Follow up with interested leads

Pay: $5/hr + $10 bonus per positive response
Hours: 10-20/week
```

### Gym partnership campaign (WalkToUnlock)

**Target:** 10 local gyms for pilot

**The offer:**
- Branded version for members
- 15% of subscription revenue
- Engagement dashboard

**Execution:**
- Week 3: Research and outreach
- Week 4: Pilot setup with first 3 gyms

### Affiliate army scaling

**Target:** 100 affiliates by end of Month 1

**Tactics:**
1. Mass DM to creators in niche
2. Creator seeding (free lifetime access to 100 creators)
3. Affiliate network listings (FirstPromoter, Rewardful)

### A/B tests to run

| Test | Variants | Success metric |
|------|----------|----------------|
| Paywall copy | "Unlock premium" vs "Start free trial" | Trial conversion |
| Pricing | $9.99/mo vs $7.99/mo | Revenue per user |
| Trial length | 3 days vs 7 days | Conversion rate |
| App icon | 3 variants | App Store conversion |
| Social hooks | 5 hook formats | Engagement rate |

### Ralph tasks (Month 1)

| Task | Week |
|------|------|
| Build apps 3-5 | 3-4 |
| Generate 100 UGC-style videos | 3-4 |
| Build church partnership landing page | 3 |
| Create gym partnership deck | 3 |
| Set up A/B testing infrastructure | 3 |
| Analyze first content performance | 4 |
| Generate case studies from early users | 4 |

### Budget allocation (Month 1)

| Item | Cost | Cumulative |
|------|------|------------|
| Week 1-2 carry | $125 | $125 |
| VA (20 hrs x $5) | $100 | $225 |
| Small ad test budget | $100 | $325 |
| **Month 1 total** | | $325 |

### Success criteria for Month 1

- [ ] All 5 apps submitted
- [ ] 100 affiliates recruited
- [ ] 50 churches contacted, 3+ partnerships
- [ ] 10 gyms contacted, 1+ pilot
- [ ] A/B tests showing clear winners
- [ ] $500+ MRR from apps

---

## Phase 5: Month 2-3 (Days 31-90)

### Scale what works

By now you should have data on:
- Which app converts best
- Which content hooks perform
- Which outreach channels work
- Which price points optimize revenue

**Decision framework:**

| Signal | Action |
|--------|--------|
| App at >5% trial-to-paid | Double down, add features |
| App at <2% trial-to-paid | Fix onboarding or kill |
| Content hook at >10% engagement | Produce 10 more variants |
| Content hook at <2% engagement | Stop using |
| Outreach at >10% reply rate | Scale volume 5x |
| Outreach at <3% reply rate | Rewrite or change channel |

### Kill what doesn't work

**Red flags to watch:**
- App with <100 downloads after 30 days
- Social account with 0 organic growth
- Outreach channel with <1% reply rate
- Content format with consistent low engagement

**Kill protocol:**
1. Document in OPS/logs/KILLED_[thing].md
2. Extract learnings
3. Reallocate budget/time to winners

### Launch paid ads (only after organic works)

**Prerequisites:**
- At least 1 app at >3% conversion
- Content that gets organic traction
- Email list of 500+

**Ad budget (Month 2):**
| Channel | Daily budget | Target CPI |
|---------|--------------|------------|
| TikTok Ads | $20-50 | $1-2 |
| Apple Search Ads | $20-30 | $2-4 |
| Meta Ads | $20-50 | $1-3 |

**Scaling rule:** Only scale ads where LTV > 3x CAC

### Cold outbound launch (if B2B angle emerges)

**If you discover B2B demand (corporate wellness, etc.):**

Infrastructure needed:
- 3-5 secondary domains
- Google Workspace ($180/mo for 25 inboxes)
- Instantly.ai ($97/mo)
- Apollo Pro ($79/mo)

**Target:** 500 emails/day after 30-day warmup

**Benchmark targets:**
| Metric | Target |
|--------|--------|
| Open rate | 50%+ |
| Reply rate | 5%+ |
| Meeting rate | 1.5%+ |

### Month 2-3 targets

| Metric | Month 2 | Month 3 |
|--------|---------|---------|
| MRR | $2,000 | $5,000 |
| Total downloads | 500 | 2,000 |
| Affiliates | 150 | 300 |
| Church partners | 10 | 25 |
| Social followers (total) | 5,000 | 20,000 |

### Budget allocation (Month 2-3)

| Item | Monthly cost |
|------|--------------|
| Soax proxy | $99 |
| Google Workspace | $6 |
| VAs (40 hrs) | $200 |
| Ad budget | $500-1000 |
| Tools (as needed) | $100 |
| **Monthly total** | $905-1405 |

---

## Automation vs Human Matrix

### Ralph can automate

| Task | Tool/Method |
|------|-------------|
| Content generation | Claude + templates |
| Social posting | Playwright + proxy |
| App builds | Xcode CLI |
| Screenshot generation | Playwright |
| Email sequence writing | Claude |
| Landing page builds | Next.js |
| Analytics reports | Python scripts |
| A/B test analysis | Python scripts |
| Competitor monitoring | Playwright |

### Human must do

| Task | Why |
|------|-----|
| Create social accounts | Phone verification |
| App Store Connect entry | Apple ID required |
| RevenueCat product setup | Dashboard-only |
| Submit app for review | Manual button |
| Respond to app rejections | Judgment required |
| Sign affiliate agreements | Legal |
| Pay affiliates | Financial |
| VA hiring/training | Relationship |
| Strategic pivots | Judgment |

---

## Decision Points

### Week 2 checkpoint

**Go/No-go for scaling:**
- Are apps building successfully? If no, diagnose blockers
- Are social accounts warming without bans? If no, adjust strategy
- Is content generating engagement? If no, try different hooks

### Month 1 checkpoint

**Scale vs pivot decision:**

| Signal | Action |
|--------|--------|
| 1+ app at $200+ MRR | Scale that app |
| All apps at <$50 MRR | Diagnose: traffic or conversion? |
| Organic social growing | Keep posting, delay ads |
| Zero organic growth | Test paid ads earlier |
| Church outreach >5% reply | Scale VA team |
| Church outreach <2% reply | Try different angle or kill |

### Month 2 checkpoint

**Double down vs diversify:**

| Signal | Action |
|--------|--------|
| Clear winner emerging | Focus 80% resources there |
| Multiple moderate performers | Keep all, optimize each |
| Nothing working | Major pivot or new niche |

---

## Risk Mitigation

### App rejection

**Prevention:**
- Follow Apple guidelines exactly
- No screenshots with fake content
- Clear privacy policy
- No undisclosed tracking

**If rejected:**
1. Read rejection reason carefully
2. Fix exactly what they mention
3. Resubmit within 24 hours
4. If rejected 2x for same reason, create OPS/logs/BLOCKED_[app].md

### Social account ban

**Prevention:**
- 14+ day warmup before automation
- Mobile proxy for all automation
- Human-like posting patterns (vary times, not exactly consistent)
- Never exceed 50 actions/hour

**If banned:**
1. Do NOT create new account immediately
2. Wait 7 days
3. Use different email/phone
4. Start warming from scratch

### Revenue plateau

**Signs:**
- Growth stops for 2+ weeks
- Conversion rate declining
- Churn increasing

**Actions:**
1. Run user interviews (5-10 calls)
2. Analyze drop-off points in funnel
3. Test new acquisition channels
4. Test new price points

---

## Quick Reference: Daily/Weekly Routines

### Daily (15 min)

- [ ] Check crash reports (RevenueCat, App Store Connect)
- [ ] Respond to app reviews (all of them)
- [ ] Check social metrics (any posts going viral?)
- [ ] Check email replies (outreach responses)

### Weekly (1 hour)

- [ ] Review full metrics dashboard
- [ ] Approve/reject content queue
- [ ] Check ALPHA_STAGING.csv for new tactics
- [ ] Update MASTER_TASKS.md with completed items
- [ ] Plan next week's priorities

### Monthly (2 hours)

- [ ] Full revenue review
- [ ] Affiliate payouts
- [ ] User interviews (schedule 5)
- [ ] Competitive analysis
- [ ] Strategic planning for next month

---

## File Outputs

This plan references and produces:

**Inputs (source files):**
- LEDGER/APP_CLONE_OPPORTUNITIES.csv
- LEDGER/ALPHA_STAGING.csv
- LEDGER/HIGH_SIGNAL_SOURCES.csv
- MONEY_METHODS/APP_FACTORY/*
- OPS/TECH_STACK_FOUNDATION.md
- OPS/MANUAL_SETUP_TASKS.md

**Outputs (track progress):**
- LEDGER/MASTER_TASKS.md (update statuses)
- LEDGER/FUNNEL_METRICS.csv (track conversions)
- LEDGER/GTM_EXPERIMENTS.csv (track outreach)
- LEDGER/leads.csv (track leads)
- OPS/logs/* (document blockers)

---

## Next action

**Right now, open a new tab and:**

1. Log into RevenueCat
2. Go to Project Settings > Integrations
3. Add Stripe integration
4. Complete the webhook setup

This takes 15 minutes and unblocks all app revenue.

---

Created: 2026-01-21
