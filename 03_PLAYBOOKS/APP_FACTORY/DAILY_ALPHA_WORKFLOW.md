# Daily Alpha Research Workflow for APP_FACTORY

How to run systematic daily research to discover app conversion tactics, monetization strategies, and growth hacks. All findings go through human approval before implementation.

---

## Quick reference

| File | Purpose |
|------|---------|
| `LEDGER/HIGH_SIGNAL_SOURCES.csv` | 56+ sources to monitor |
| `LEDGER/ALPHA_STAGING.csv` | New findings awaiting review |
| `LEDGER/ALPHA_WATCHLIST.csv` | Emerging platforms/tools to track |
| `LEDGER/APP_FACTORY_METHODS.csv` | Approved tactics for app building |
| `.claude/commands/daily-research.md` | Skill to run the scan |

---

## 1. Daily research process

### Running the scan

Use the `/daily-research` skill:

```
/daily-research
```

This scans HIGH_SIGNAL_SOURCES.csv and extracts actionable alpha. The skill:
1. Checks X accounts, Reddit, newsletters, tools
2. Filters for APP_FACTORY relevant content
3. Stages findings to ALPHA_STAGING.csv
4. Flags items for human review

### Manual source check (if skill unavailable)

Priority sources for app alpha (from HIGH_SIGNAL_SOURCES.csv):

**X accounts (app-focused)**
| Handle | Signal | Focus |
|--------|--------|-------|
| @knoxtwts | HIGHEST | App marketing, content formats, revenue math |
| @purpdevvv | HIGHEST | Mobile app formulas, niche adaptation |
| @xivy0k | HIGH | Mobile app marketing, solopreneur tactics |
| @simonecanciello | HIGH | Indie app development |
| @iamgdsa | HIGHEST | Creator marketing, app virality |
| @matteo_spada | HIGH | Tech entrepreneurship, trust stacks |

**Tools to check daily**
| Tool | URL | What to look for |
|------|-----|------------------|
| appkittie | appkittie.com | App store movers, trending apps |
| FB Ads Library | fb.com/ads/library | Active digital product ads |
| Product Hunt | producthunt.com | New app launches |
| algrow.online | algrow.online | Terminated channels (content gaps) |

**Reddit communities**
| Subreddit | Focus |
|-----------|-------|
| r/AppBusiness | Mobile app monetization tactics |
| r/SideProject | Launch feedback, what's working |
| r/indiehackers | Revenue numbers, growth tactics |

### What to capture

When scanning sources, extract:

1. **Specific numbers** - "$600k/mo", "23.8M views", "11 sales/day"
2. **Mechanics** - How something works step-by-step
3. **Proof** - Screenshots, links, verifiable claims
4. **Applicability** - Which niches (faith, fitness, AI, all)

Skip:
- Vague hype ("opportunities are insane")
- No specifics or steps
- Paid course pitches without free value

---

## 2. Alpha categories for apps

Tag each finding with the appropriate category:

### app_onboarding

Tactics for improving first-time user experience and activation.

**What to look for:**
- Onboarding flow structures that convert
- First-session hooks that drive retention
- Permission request timing
- Progress indicators and gamification
- "Aha moment" acceleration

**Related docs:**
- `onboarding/ONBOARDING_OPTIMIZATION_PLAYBOOK.md`
- `onboarding/ONBOARDING_METRICS.md`

**Example alpha:**
```
ALPHA: Google Sign-In Default
Source: @startup_lessons
Tactic: Make Google sign-in the primary button. 90%+ of users pick it.
Steps: 1. Make Google SSO primary 2. Other options secondary 3. Reduce friction
```

### paywall_conversion

Tactics for improving trial-to-paid conversion.

**What to look for:**
- Paywall designs that convert
- Pricing experiments and results
- Hard vs soft paywall performance
- Copy that drives action
- Urgency/scarcity mechanics (compliant)

**Related docs:**
- `monetization/PAYWALL_EXPERIMENTS.md`
- `monetization/PRICING_EXPERIMENTS.md`
- `monetization/REVENUE_OPTIMIZATION_PLAYBOOK.md`

**Example alpha:**
```
ALPHA: Authority Trust Stack
Source: @matteo_spada
Tactic: $350k MRR app uses Harvard citations + visual goal timelines + bright paywall colors
Steps: 1. Add legitimate citations 2. Show progress timeline 3. Bright CTA colors 4. "goals 4.2x faster" copy
```

### aso_optimization

App Store Optimization tactics for discoverability.

**What to look for:**
- Keyword strategies that rank
- Screenshot copy variations
- Icon A/B test results
- Review/rating optimization
- Seasonal ranking opportunities

**Related docs:**
- `aso/ASO_PLAYBOOK.md`
- `aso/ASO_TRACKING.csv`
- `aso/screenshot_copy_variations.md`
- `aso/seasonal_calendar.md`

**Example alpha:**
```
ALPHA: Seasonal ASO Push
Source: appkittie trending
Tactic: New Year's resolution apps spike Dec 26-Jan 7. Update keywords/screenshots 2 weeks before.
Steps: 1. Update metadata 2. New screenshots with resolution language 3. Submit Dec 20
```

### retention_tactics

Tactics for keeping users engaged long-term.

**What to look for:**
- Push notification strategies
- Habit formation triggers
- Gamification systems
- Streak mechanics
- Re-engagement campaigns

**Related docs:**
- `retention/RETENTION_PLAYBOOK.md`
- `retention/gamification_system.md`
- `retention/habit_formation_triggers/`
- `retention/lifecycle_campaigns/`

**Example alpha:**
```
ALPHA: Streak Mercy Day
Source: @purpdevvv
Tactic: Give users one "mercy day" per week where broken streak doesn't reset. Reduces churn 40%.
Steps: 1. Implement streak system 2. Add 1 mercy/week 3. Show mercy status in UI
```

### monetization_strategies

Broader monetization tactics beyond paywalls.

**What to look for:**
- Hybrid ad + subscription models
- Affiliate integration opportunities
- In-app purchase structures
- Pricing tiers that work
- Revenue math frameworks

**Related docs:**
- `APP_MONETIZATION_STRATEGY.md`
- `AFFILIATE_SOURCES_MASTER.md`
- `monetization/HYBRID_MONETIZATION.md`
- `monetization/AD_MONETIZATION_STRATEGY.md`

**Example alpha:**
```
ALPHA: Revenue Math Framework
Source: @knoxtwts
Tactic: Work backwards from target. $30k/mo = 309 sales @ $97 = 11/day. Cold 1% = 1100 visitors.
Steps: 1. Set revenue target 2. Calculate needed conversions 3. Choose traffic temp 4. Build to numbers
```

---

## 3. Approval workflow

All alpha goes through human review. No auto-implementation.

### Staging new findings

When you find actionable alpha:

1. **Add to ALPHA_STAGING.csv** with fields:
   - `alpha_id`: ALPHA[XXX] sequential
   - `source`: Handle or site
   - `source_url`: Direct link
   - `category`: One of the 5 categories above
   - `title`: Short descriptive name
   - `description`: What it is
   - `actionable_steps`: Numbered steps to implement
   - `effort_level`: LOW/MEDIUM/HIGH
   - `roi_potential`: LOW/MEDIUM/HIGH/HIGHEST
   - `risk_level`: LOW/MEDIUM/HIGH
   - `applies_to_niches`: AI,Faith,Fitness or ALL
   - `status`: PENDING_REVIEW

2. **Set status to PENDING_REVIEW**

### Human review process

Run `/review-alpha` or manually review ALPHA_STAGING.csv:

**For each PENDING_REVIEW item, decide:**

| Decision | Action |
|----------|--------|
| APPROVED | Move tactic to APP_FACTORY_METHODS.csv or relevant doc |
| APPROVED | If it's a tool/platform to track, add to ALPHA_WATCHLIST.csv |
| REPURPOSE_ONLY | Mark as engagement format, not actionable tactic |
| REJECTED | Remove from staging (vague, unreliable, or violates compliance) |

**Approval criteria:**
- Specific and actionable (not vague hype)
- Verifiable source or proof
- Legal and compliant (see section 5)
- Applies to our niches
- Reasonable effort-to-ROI ratio

### Post-approval integration

**If tactic goes to APP_FACTORY_METHODS.csv:**
```csv
AFM014,Streak Mercy Day,"Give users one mercy day per week...",etc
```

**If item goes to ALPHA_WATCHLIST.csv:**
```csv
5,iOS 18 Live Activities,developer.apple.com,watching,HIGH,"New engagement surface..."
```

**If tactic updates existing doc:**
- Add to relevant section in APP_FACTORY docs
- Note source and date
- Link back to original alpha_id

---

## 4. Integration with app builds

### Pre-build checklist

Before building any app, review alpha:

```
1. Check LEDGER/APP_FACTORY_METHODS.csv for relevant tactics
2. Review recent ALPHA_STAGING.csv approvals
3. Check category-specific docs:
   - onboarding/ONBOARDING_OPTIMIZATION_PLAYBOOK.md
   - monetization/PAYWALL_EXPERIMENTS.md
   - aso/ASO_PLAYBOOK.md
   - retention/RETENTION_PLAYBOOK.md
```

### Documenting tactics used

When building an app, track which alpha was applied:

In the app's build doc (e.g., `products/prayerlock/BUILD_LOG.md`):

```markdown
## Alpha Applied

| Tactic | Source | Implementation |
|--------|--------|----------------|
| AFM010: Community First | @purpdevvv | Built X audience before app |
| AFM012: Screen Blocker | @Jahjiren | Core mechanic |
| AFM013: Trust Stack | @matteo_spada | Added Harvard citations to paywall |
| ALPHA020: Google Sign-In Default | @startup_lessons | Made Google SSO primary button |
```

### Measuring alpha effectiveness

After launch, track which tactics worked:

```markdown
## Alpha Results

| Tactic | Expected | Actual | Keep/Drop |
|--------|----------|--------|-----------|
| Trust Stack citations | +20% conv | +15% conv | KEEP |
| Google SSO default | 90% usage | 87% usage | KEEP |
| Hard paywall | Higher LTV | -30% installs | TEST SOFT |
```

Report significant findings back to ALPHA_STAGING for community benefit.

---

## 5. Legal compliance

### Required

All alpha must comply with:

**FTC Guidelines**
- Clear disclosure of affiliate relationships
- Substantiated claims only
- No fake testimonials
- AI content disclosure where required (NY law effective June 2026)

**App Store Policies**
- No manipulation of rankings
- No fake reviews
- No incentivized ratings
- Accurate app descriptions

**Platform Terms**
- No automation that violates ToS
- No fake engagement
- No purchased followers/reviews

### Prohibited tactics

**Never implement alpha that involves:**

- Fake reviews or testimonials with specific names
- Buying app store rankings
- Bot-generated reviews
- Fake user counts or social proof numbers
- Manipulated screenshots showing fake data
- Claims without substantiation ("clinically proven" without proof)
- Undisclosed affiliate relationships
- Fake urgency ("only 3 left!" when unlimited)

### Compliance check

Before approving any alpha, verify:

```
[ ] Does not require fake reviews/testimonials
[ ] Does not manipulate app store rankings
[ ] Claims are substantiated or clearly opinion
[ ] Affiliate relationships will be disclosed
[ ] No platform ToS violations
[ ] No FTC violations
```

If any box is unchecked, REJECT the alpha.

### Edge cases

Some tactics ride the compliance line. Review:
- `GREY_HAT_COMPLIANCE_PLAYBOOK.md` - What's allowed, what's not
- `APP_STORE_REJECTION_GUIDE.md` - Avoid rejection triggers

When in doubt, ask: "Would this survive an FTC investigation?" If no, don't do it.

---

## 6. Daily workflow summary

### Morning (5-10 min)

```
1. Run /daily-research skill
2. Quick scan of appkittie for trending apps
3. Check X list for app-focused accounts
```

### Capture (as found)

```
1. Add promising finds to ALPHA_STAGING.csv
2. Tag with appropriate category
3. Include source URL and steps
```

### Review (weekly)

```
1. Run /review-alpha or manual review
2. Approve/reject pending items
3. Integrate approved tactics to docs
4. Update ALPHA_WATCHLIST for emerging tools
```

### Build integration (per project)

```
1. Pre-build: Review relevant alpha
2. During build: Apply proven tactics
3. Post-launch: Document what was used
4. Measure: Track which tactics worked
```

---

## 7. Files reference

### Input files (sources)

| File | Purpose |
|------|---------|
| `LEDGER/HIGH_SIGNAL_SOURCES.csv` | 56+ accounts, subreddits, tools to monitor |
| `LEDGER/APP_CLONE_OPPORTUNITIES.csv` | Apps worth adapting |

### Staging files (pending review)

| File | Purpose |
|------|---------|
| `LEDGER/ALPHA_STAGING.csv` | New findings awaiting approval |

### Output files (approved tactics)

| File | Purpose |
|------|---------|
| `LEDGER/APP_FACTORY_METHODS.csv` | Approved app building methods |
| `LEDGER/ALPHA_WATCHLIST.csv` | Platforms/tools to track |
| `APP_FACTORY/onboarding/` | Onboarding tactics |
| `APP_FACTORY/monetization/` | Monetization tactics |
| `APP_FACTORY/aso/` | ASO tactics |
| `APP_FACTORY/retention/` | Retention tactics |

### Skills

| Skill | Purpose |
|-------|---------|
| `/daily-research` | Run automated source scan |
| `/review-alpha` | Review and approve pending alpha |

---

## 8. Example: full workflow

### Day 1: Discovery

Scanning @knoxtwts, find a post about paywall psychology.

**Add to ALPHA_STAGING.csv:**
```csv
ALPHA032,@knoxtwts,https://x.com/knoxtwts/status/123,paywall_conversion,"Anchoring Price Display","Show crossed-out annual price next to monthly to make monthly feel cheaper. 22% lift in one test.","1. Add annual price crossed out 2. Show monthly as 'savings' 3. A/B test vs control",LOW,HIGH,LOW,"ALL",PENDING_REVIEW,,
```

### Day 3: Review

Human reviews ALPHA_STAGING.csv, sees ALPHA032.

**Decision: APPROVED**
- Specific (22% lift cited)
- Actionable (3 clear steps)
- Compliant (legitimate pricing display)
- Low effort, high potential

**Update status:**
```csv
ALPHA032,...,APPROVED,2026-01-21,"Added to PAYWALL_EXPERIMENTS.md"
```

**Add to monetization/PAYWALL_EXPERIMENTS.md:**
```markdown
## Anchoring Price Display

Source: @knoxtwts (ALPHA032)
Result: 22% lift in conversion

Implementation:
1. Show annual price crossed out above monthly
2. Frame monthly as "savings" relative to annual
3. A/B test vs control without anchoring

Status: TO TEST
```

### Day 7: Implementation

Building new app (FemFit). Check alpha before paywall design.

**Find in PAYWALL_EXPERIMENTS.md:** Anchoring Price Display

**Implement in app. Add to build log:**
```markdown
## Alpha Applied

| Tactic | Source | Implementation |
|--------|--------|----------------|
| Anchoring Price Display | ALPHA032/@knoxtwts | Paywall shows crossed annual, monthly highlighted |
```

### Day 30: Measurement

FemFit launched. Review paywall performance.

**Result:** 18% lift vs control (slightly below 22% cited, but still positive)

**Update build log:**
```markdown
## Alpha Results

| Tactic | Expected | Actual | Keep/Drop |
|--------|----------|--------|-----------|
| Anchoring Price Display | +22% | +18% | KEEP |
```

Tactic validated. Stays in playbook.

---

## Notes

- Run daily research consistently. Compound gains come from systematic scanning.
- Human approval is non-negotiable. No auto-implementation of external tactics.
- Document what you use. Future builds benefit from past learnings.
- Measure results. Not all alpha works. Track what does.
- Stay compliant. Short-term hacks aren't worth long-term account risk.
