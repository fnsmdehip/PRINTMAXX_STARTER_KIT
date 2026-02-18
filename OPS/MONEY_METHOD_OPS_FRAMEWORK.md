# Money Method Ops Framework

Systematic operations to extract maximum value from each money method.

**Principle:** Every money method has a lifecycle. Each phase has specific ops that compound.

---

## Money Method Lifecycle

```
Discovery → Validation → Setup → Launch → Scale → Optimize → Automate → Exit/Sell
```

Each phase has documented ops. Run them systematically.

---

## Phase 1: Discovery Ops

### Per Money Method

| Op | Output | Frequency |
|----|--------|-----------|
| Competitor Scrape | `research/COMPETITORS.md` | Weekly |
| Revenue Research | `research/REVENUE_SIGNALS.md` | Monthly |
| Tool Discovery | `research/TOOL_STACK.md` | Monthly |
| Pricing Analysis | `research/PRICING_MATRIX.md` | Monthly |
| Gap Analysis | `research/GAPS_AND_OPPORTUNITIES.md` | Weekly |

### Discovery Scripts (Ralph-able)

```bash
# Run for each money method
claude "Scrape top 10 competitors for {MONEY_METHOD}.
       Output: pricing, features, positioning, revenue estimates.
       Save to MONEY_METHODS/{METHOD}/research/COMPETITORS.md"
```

### Alpha Integration

All discovery feeds into:
- `LEDGER/ALPHA_STAGING.csv` (new tactics)
- `LEDGER/APP_CLONE_OPPORTUNITIES.csv` (cloneable products)
- `LEDGER/APP_FACTORY_METHODS.csv` (proven playbooks)

---

## Phase 2: Validation Ops

### Minimum Viable Validation (MVV)

| Op | Time | Cost | Output |
|----|------|------|--------|
| Landing Page Test | 2h | $50 ads | Conversion rate |
| Cold Email Test | 1h | $0 | Response rate |
| Social Signal Test | 4h | $0 | Engagement metrics |
| Waitlist Build | 4h | $20 | Email count |

### Validation Scorecard

Create per money method: `research/VALIDATION_SCORECARD.md`

```markdown
## Validation Metrics

| Signal | Target | Actual | Pass? |
|--------|--------|--------|-------|
| Landing page CVR | >3% | ___% | Y/N |
| Cold email reply rate | >5% | ___% | Y/N |
| Social engagement | >2% | ___% | Y/N |
| Waitlist signups (7d) | >100 | ___ | Y/N |
| Manual sales (before code) | >$500 | $___ | Y/N |

**Decision:** Proceed / Pivot / Kill
```

---

## Phase 3: Setup Ops (Per Money Method)

### APP_FACTORY Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| App Store Account | Human | `MANUAL_SETUP_CHECKLIST.md` |
| RevenueCat Config | Human | `REVENUECAT_INTEGRATION.md` |
| Affiliate Program Setup | Human | `AFFILIATE_SOURCES_MASTER.md` |
| CI/CD Pipeline | Ralph | `ci_cd/` |
| Asset Generation | Ralph | `ASSET_GENERATION_GUIDE.md` |

### COLD_OUTBOUND Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Domain Purchase (10x) | Human | `infrastructure/DOMAIN_SETUP.md` |
| Email Warmup | Semi-auto | `infrastructure/WARMUP_PROTOCOLS.md` |
| Lead List Build | Ralph | `lead_gen/` |
| Sequence Writing | Ralph | `sequences/` |
| Instantly Config | Human | `infrastructure/INSTANTLY_SETUP.md` |

### UGC_ARBITRAGE Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Creator Roster Build | Ralph | `sourcing/` |
| Pricing Structure | Human | `financials/PRICING.md` |
| Client Templates | Ralph | `sales/` |
| Fulfillment SOP | Ralph | `operations/FULFILLMENT_SOP.md` |

### AFFILIATE_SITES Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Domain + Hosting | Human | setup required |
| Content Calendar | Ralph | `editorial/CALENDAR.md` |
| Affiliate Program Apps | Human | per program |
| SEO Foundation | Ralph | `seo/` |

### INFO_PRODUCTS Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Course Platform | Human | Teachable/Gumroad |
| Content Outline | Human + Ralph | `products/*/OUTLINE.md` |
| Sales Page | Ralph | `funnels/` |
| Email Sequences | Ralph | `email_sequences/` |

### AGENCY_SERVICES Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Service Packages | Human | `packages/` |
| Proposal Templates | Ralph | `proposals/` |
| Client Portal | Human | `systems/` |
| Fulfillment Process | Human + Ralph | `operations/` |

### CONTENT_FARM Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Account Network | Human | `accounts/` |
| Content Pipeline | Ralph | `automation/` |
| Proxy Setup | Human | `AUTOMATIONS/PROXY_COMPARISON.md` |
| Scheduling Tools | Human | Buffer/Hypefury |

### AI_INFLUENCER Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Persona Development | Human + Ralph | `personas/` |
| Content Voice Guide | Ralph | `voice/` |
| Compliance Review | Human | `compliance/` |
| Monetization Strategy | Human | `monetization/` |

### SAAS Setup Ops

| Op | Owner | Docs |
|----|-------|------|
| Tech Stack Decision | Human | `tech/` |
| MVP Scope | Human | `products/*/PRD.md` |
| Stripe Setup | Human | required |
| Landing Page | Ralph | `landing/` |

---

## Phase 4: Launch Ops

### Universal Launch Checklist

```markdown
## Pre-Launch (T-7 days)
- [ ] Product/service complete and tested
- [ ] Landing page live with tracking
- [ ] Email sequence loaded
- [ ] Social content queued
- [ ] Affiliate/partner outreach done
- [ ] PR/media list ready

## Launch Day (T-0)
- [ ] ProductHunt/Hacker News post (if applicable)
- [ ] Email blast to waitlist
- [ ] Social announcement posts
- [ ] Cold outreach blast
- [ ] Community posts (relevant subreddits)
- [ ] Influencer DMs

## Post-Launch (T+7 days)
- [ ] Follow-up sequences running
- [ ] Metrics dashboard reviewed daily
- [ ] Customer feedback collected
- [ ] Quick wins implemented
- [ ] Retargeting ads running
```

### Method-Specific Launch Ops

See: `MONEY_METHODS/{METHOD}/launch/LAUNCH_CHECKLIST.md`

---

## Phase 5: Scale Ops

### Scaling Triggers

| Signal | Action |
|--------|--------|
| CAC < LTV/3 | Increase ad spend 2x |
| Reply rate > 10% | Add more sequences/ICPs |
| App rating > 4.5 | Push for features, not retention |
| Content CVR > 5% | Expand topic clusters |
| UGC margin > 50% | Recruit more creators |

### Scale Ops by Method

**APP_FACTORY:** More apps, more niches, localization
**COLD_OUTBOUND:** More domains, more ICPs, more sequences
**UGC_ARBITRAGE:** More creators, white-label, agency model
**AFFILIATE_SITES:** More sites, more keywords, programmatic SEO
**INFO_PRODUCTS:** Cohorts, community upsell, certification
**AGENCY_SERVICES:** Productize, white-label, hire juniors
**CONTENT_FARM:** More accounts, more platforms, more automation
**AI_INFLUENCER:** More personas, brand deals, product launches
**SAAS:** Features, integrations, enterprise tier

---

## Phase 6: Optimize Ops

### Weekly Optimization Loop

```markdown
## Monday: Review metrics
- Pull all dashboards
- Identify top/bottom performers
- Note anomalies

## Tuesday: A/B test planning
- Pick 2-3 tests to run
- Define success criteria
- Set up variants

## Wednesday-Thursday: Execute tests
- Launch variants
- Monitor for errors
- Collect data

## Friday: Analyze and iterate
- Review test results
- Implement winners
- Document learnings
```

### Optimization Docs Per Method

Create: `MONEY_METHODS/{METHOD}/metrics/OPTIMIZATION_LOG.md`

```markdown
## Week of [DATE]

### Test 1: [Name]
- Hypothesis: [X] will improve [metric] by [%]
- Control: [description]
- Variant: [description]
- Result: [winner] (+X%)
- Action: [implemented/rolled back]

### Test 2: [Name]
...
```

---

## Phase 7: Automate Ops

### Automation Priority Matrix

| Task | Time Saved | Automation Cost | Priority |
|------|------------|-----------------|----------|
| Content generation | 10h/wk | 2h setup | HIGH |
| Email sequences | 5h/wk | 1h setup | HIGH |
| Social posting | 8h/wk | 4h setup | HIGH |
| Lead enrichment | 3h/wk | 2h setup | MEDIUM |
| Reporting | 2h/wk | 4h setup | MEDIUM |
| Customer support | varies | complex | LOW (initially) |

### Automation Playbooks

See: `OPS/AUTONOMOUS_TASKS.md` for full list.

Key automations per method:
- **APP_FACTORY:** ASO monitoring, review responses, crash alerts
- **COLD_OUTBOUND:** Sequence triggers, bounce handling, reply sorting
- **UGC_ARBITRAGE:** Creator outreach, delivery tracking, invoice generation
- **AFFILIATE_SITES:** Rank tracking, link checking, content scheduling
- **INFO_PRODUCTS:** Drip sequences, certificate delivery, community moderation
- **AGENCY_SERVICES:** Client reporting, task tracking, invoice reminders
- **CONTENT_FARM:** Multi-platform posting, engagement tracking, content recycling
- **AI_INFLUENCER:** Content scheduling, engagement automation, DM templates
- **SAAS:** Onboarding sequences, usage alerts, churn prediction

---

## Phase 8: Exit/Sell Ops

### Exit Preparation Checklist

```markdown
## Financial Documentation
- [ ] P&L statements (12+ months)
- [ ] Revenue by channel
- [ ] Customer cohort analysis
- [ ] Churn rates documented
- [ ] Unit economics clear

## Operational Documentation
- [ ] All SOPs written
- [ ] Tech stack documented
- [ ] Automation flows mapped
- [ ] Team structure clear
- [ ] Vendor contracts listed

## Growth Documentation
- [ ] Traffic sources analyzed
- [ ] SEO position documented
- [ ] Email list quality verified
- [ ] Social following audited
- [ ] Backlink profile clean

## Transfer Preparation
- [ ] All accounts listed
- [ ] Credentials organized
- [ ] Code repositories ready
- [ ] Training materials prepared
- [ ] Transition plan written
```

### Exit Channels by Method

| Method | Best Exit Channel | Typical Multiple |
|--------|-------------------|------------------|
| APP_FACTORY | Acquire.com, direct | 2-4x annual |
| AFFILIATE_SITES | Empire Flippers, Flippa | 30-40x monthly |
| SAAS | Acquire.com, FE International | 3-5x ARR |
| INFO_PRODUCTS | Direct to audience | 2-3x annual |
| AGENCY_SERVICES | Competitor acquisition | 1-2x annual + earnout |
| CONTENT_FARM | Direct, social brokers | Account-dependent |

---

## Cross-Method Synergies

### Flywheel Effects

```
APP_FACTORY → CONTENT_FARM (app promo content)
CONTENT_FARM → AFFILIATE_SITES (traffic arbitrage)
AFFILIATE_SITES → INFO_PRODUCTS (audience monetization)
INFO_PRODUCTS → AGENCY_SERVICES (done-for-you upsell)
AGENCY_SERVICES → SAAS (productized service)
SAAS → APP_FACTORY (mobile companion)
COLD_OUTBOUND → ALL (lead gen for any method)
UGC_ARBITRAGE → AI_INFLUENCER (content supply)
AI_INFLUENCER → INFO_PRODUCTS (audience building)
```

### Shared Operations

| Op | Methods Served | Location |
|----|----------------|----------|
| Content generation | All | Ralph loops |
| Email sequences | All | `sequences/` per method |
| Landing pages | All | `landing/` per method |
| Competitor research | All | `research/` per method |
| SEO/ASO | Apps, Sites | `seo/` and `aso/` |
| Social posting | All | `AUTOMATIONS/` |

---

## Daily/Weekly/Monthly Ops Cadence

### Daily (15 min)

```
- Check dashboards for anomalies
- Review email/social metrics
- Handle urgent items only
- Update LEDGER tracking
```

### Weekly (2 hours)

```
Monday: Metrics review, planning
Tuesday-Thursday: Execution
Friday: Optimization, documentation
```

### Monthly (4 hours)

```
Week 1: Full method audit
Week 2: Competitor research refresh
Week 3: Content/sequence refresh
Week 4: Strategy review, next month planning
```

---

## Ralph Task Integration

All ops in this doc can be converted to Ralph tasks.

### Example Ralph Task Template

```markdown
# Task: [OP NAME] for [MONEY_METHOD]

## Context
- Read MONEY_METHODS/{METHOD}/research/ for context
- Output to MONEY_METHODS/{METHOD}/{PHASE}/
- Follow copy-style.md for content

## Success Criteria
1. [ ] [Specific deliverable 1]
2. [ ] [Specific deliverable 2]
3. [ ] [Machine-verifiable check]
4. [ ] No banned AI vocabulary
5. [ ] Saved to correct location
```

---

## Getting Started

1. Pick your Phase 1 money methods (recommend: APP_FACTORY + COLD_OUTBOUND)
2. Run Discovery Ops for each
3. Complete Validation Ops before heavy investment
4. Run Setup Ops (mix of human + Ralph)
5. Execute Launch Ops
6. Enter weekly optimization loop
7. Automate when patterns stabilize
8. Prep for exit when growth plateaus

---

## Related Documents

- `OPS/AUTONOMOUS_TASKS.md` - What can run unattended
- `OPS/RALPH_LOOP_GUIDE.md` - Overnight build pattern
- `OPS/MANUAL_SETUP_CHECKLIST.md` - Human-required tasks
- `LEDGER/ALPHA_STAGING.csv` - New tactics discovery
- `.claude/CLAUDE.md` - Master project context

---

Last updated: 2026-01-22
