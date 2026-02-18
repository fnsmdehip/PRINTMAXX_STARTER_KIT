# Growth Experiments Framework

Systematic approach to testing growth hypotheses. ICE scoring, experiment templates, tracking systems.

---

## ICE Scoring System

Rate each experiment 1-10 on three dimensions:

| Dimension | Question | Score Guide |
|-----------|----------|-------------|
| **Impact** | If this works, how big is the effect? | 10 = 2x growth, 5 = 20% lift, 1 = marginal |
| **Confidence** | How sure are we this will work? | 10 = proven elsewhere, 5 = logical hypothesis, 1 = wild guess |
| **Ease** | How easy is this to implement? | 10 = 1 hour, 5 = 1 week, 1 = 1 month+ |

**ICE Score = (Impact + Confidence + Ease) / 3**

Priority thresholds:
- 8.0+ = Run immediately
- 6.0-7.9 = Queue for next sprint
- 4.0-5.9 = Backlog
- <4.0 = Deprioritize

---

## Experiment Categories

### 1. Acquisition Experiments

| Experiment | Hypothesis | ICE | Metrics |
|------------|------------|-----|---------|
| TikTok hook variations | First 3 seconds determine watch time | 8.5 | Watch %, follows |
| App Store screenshot A/B | First 2 screenshots drive CVR | 8.0 | Install CVR |
| Landing page headline test | Direct benefit > clever copy | 7.5 | Signup CVR |
| Cold email subject lines | Curiosity > value proposition | 7.0 | Open rate |
| Reddit post timing | 8-9am EST = peak engagement | 6.5 | Upvotes, CTR |
| Instagram Reels hashtags | Niche hashtags > broad ones | 6.5 | Reach, follows |
| YouTube Shorts thumbnail | Text overlay > clean image | 7.0 | CTR |
| Twitter thread hooks | Numbers in hook > questions | 7.5 | Impressions |
| Pinterest pin formats | Tall pins > square | 6.0 | Saves, clicks |
| LinkedIn post format | Carousel > text-only | 7.0 | Engagement |

### 2. Activation Experiments

| Experiment | Hypothesis | ICE | Metrics |
|------------|------------|-----|---------|
| Onboarding length | 3 screens max = higher completion | 8.0 | Completion % |
| First session goal | Guided first action = retention | 8.5 | Day 1 retention |
| Permission timing | After value shown > upfront | 7.5 | Permission grant % |
| Default settings | Optimal defaults > choice overload | 7.0 | Feature adoption |
| Progress indicators | Visual progress = completion | 6.5 | Onboarding CVR |
| Personalization Q's | 2-3 questions max | 7.0 | Drop-off rate |
| Tutorial format | Interactive > video > text | 7.5 | Completion % |
| Value preview | Show outcome before asking input | 8.0 | Signup CVR |
| Social proof timing | Show before paywall | 7.5 | Trial starts |
| Friction removal | Each field removed = 10% lift | 8.5 | Form CVR |

### 3. Retention Experiments

| Experiment | Hypothesis | ICE | Metrics |
|------------|------------|-----|---------|
| Push notification timing | User-specific timing > fixed | 7.5 | Open rate, D7 |
| Streak mechanics | Visible streaks = habit formation | 8.0 | D7, D30 retention |
| Re-engagement emails | Day 3 + Day 7 = optimal | 7.0 | Reactivation % |
| Feature discovery | Progressive disclosure > all at once | 6.5 | Feature adoption |
| Community features | Social = stickiness | 6.0 | DAU/MAU |
| Content freshness | New content = return visits | 7.0 | Session frequency |
| Personalized recommendations | Relevance = engagement | 7.5 | CTR, time in app |
| Achievement system | Unlocks = motivation | 6.5 | D30 retention |
| Reminder customization | User-set reminders > default | 7.0 | Open rate |
| Win-back campaigns | Discount vs feature vs FOMO | 7.5 | Reactivation % |

### 4. Revenue Experiments

| Experiment | Hypothesis | ICE | Metrics |
|------------|------------|-----|---------|
| Paywall timing | After value > upfront | 8.5 | Conversion % |
| Price anchoring | Show annual first = annual CVR | 8.0 | Annual % |
| Trial length | 7 days > 3 days for complex apps | 7.0 | Trial CVR |
| Feature gating | Gate power features > basic | 7.5 | Upgrade % |
| Social proof on paywall | Testimonials = trust | 7.5 | Conversion % |
| Urgency tactics | Limited offer = action | 6.5 | Conversion % |
| Payment options | More options = higher CVR | 6.0 | Checkout CVR |
| Upsell timing | In-app at peak engagement | 7.5 | Upsell % |
| Pricing display | Per day < per month perception | 7.0 | Conversion % |
| Free tier limits | Strategic limits = upgrade pressure | 8.0 | Upgrade % |

### 5. Referral Experiments

| Experiment | Hypothesis | ICE | Metrics |
|------------|------------|-----|---------|
| Referral incentive type | Both-sided > one-sided | 7.5 | Referral rate |
| Referral timing | After first win > at signup | 8.0 | Referral CVR |
| Share mechanics | One-tap share > copy link | 7.0 | Share rate |
| Referral messaging | Benefit to friend > to self | 6.5 | Accept rate |
| Viral loops | Built-in sharing = organic growth | 7.0 | K-factor |
| Leaderboards | Competition = sharing | 6.0 | Referrals/user |
| Milestone rewards | Tiered rewards = more referrals | 6.5 | Referrals/user |

---

## Experiment Template

```markdown
# Experiment: [Name]

## Hypothesis
If we [change], then [outcome] because [reasoning].

## ICE Score
- Impact: X/10
- Confidence: X/10
- Ease: X/10
- **Total: X.X**

## Setup
- Control: [Current state]
- Variant: [Changed state]
- Traffic split: 50/50
- Duration: [X days/weeks]
- Sample size needed: [N users]

## Success Metrics
- Primary: [Metric] (target: +X%)
- Secondary: [Metric]
- Guardrail: [Metric that shouldn't decrease]

## Implementation
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Results
- Start date:
- End date:
- Control: [Result]
- Variant: [Result]
- Lift: [+/- X%]
- Statistical significance: [p-value]

## Decision
[ ] Ship variant
[ ] Keep control
[ ] Iterate and retest

## Learnings
[What we learned, even if experiment failed]
```

---

## Experiment Velocity Targets

| Stage | Experiments/Week | Focus |
|-------|------------------|-------|
| Pre-launch | 3-5 | Landing page, messaging |
| Launch (0-30 days) | 5-7 | Activation, onboarding |
| Growth (30-90 days) | 3-5 | Retention, revenue |
| Scale (90+ days) | 2-3 | Optimization, referral |

---

## Quick Win Experiments (High ICE, Low Effort)

### App Store Optimization
1. **Screenshot order test** - Move best-performing screenshot to position 1
2. **Subtitle keyword swap** - Test different benefit keywords
3. **Icon color test** - Bright vs dark background
4. **Preview video A/B** - With vs without

### Landing Page
1. **Headline clarity** - Specific benefit vs clever tagline
2. **CTA copy** - Action verb variations
3. **Hero image** - Product screenshot vs lifestyle
4. **Social proof placement** - Above fold vs below

### Email
1. **Subject line length** - Short (<30 chars) vs medium
2. **Send time** - Morning vs evening
3. **From name** - Personal vs brand
4. **Preview text** - Curiosity vs value

### Social Content
1. **Hook format** - Question vs statement vs number
2. **Post length** - Short (<100 words) vs long
3. **CTA placement** - End vs middle
4. **Hashtag count** - 3-5 vs 10+

---

## Statistical Significance

### Sample Size Calculator

For 95% confidence, 80% power:
- 5% baseline CVR, 10% lift needed: ~31,000 per variant
- 10% baseline CVR, 10% lift needed: ~14,000 per variant
- 20% baseline CVR, 10% lift needed: ~6,000 per variant

### Minimum Detectable Effect

| Weekly Traffic | Min Detectable Lift (2 weeks) |
|----------------|-------------------------------|
| 1,000 | 30%+ |
| 5,000 | 15%+ |
| 10,000 | 10%+ |
| 50,000 | 5%+ |

**Rule:** Don't run experiments you can't measure. If traffic is low, test bigger changes.

---

## Experiment Tracking

### LEDGER Integration

Log all experiments to `LEDGER/EXPERIMENTS.csv`:

```csv
experiment_id,name,hypothesis,ice_score,start_date,end_date,status,result,lift,winner,learnings
EXP001,Paywall timing,After value > upfront,8.5,2026-01-15,2026-01-29,completed,success,+23%,variant,"Users need to see value before paying"
```

### Status Values
- `planned` - In backlog
- `running` - Currently active
- `completed` - Finished with results
- `killed` - Stopped early (clear winner/loser or issue)

---

## Experiment Prioritization Matrix

Run weekly prioritization:

1. **Pull all planned experiments from backlog**
2. **Score/re-score ICE based on current context**
3. **Rank by ICE score**
4. **Check capacity** - How many can we run simultaneously?
5. **Avoid conflicts** - Don't test same page/feature twice
6. **Launch top N experiments**

### Capacity Guidelines

- 1 engineer: 2-3 experiments/week
- Small team: 5-7 experiments/week
- Never more than 3 experiments on same user flow

---

## Post-Experiment Playbook

### If Winner
1. Ship to 100% immediately
2. Document in experiment log
3. Update baseline metrics
4. Look for expansion opportunities (same principle, different area)

### If Loser
1. Analyze why (user feedback, heatmaps, session recordings)
2. Document learnings
3. Consider opposite hypothesis
4. Move to next experiment

### If Inconclusive
1. Check sample size - did we have enough traffic?
2. Check implementation - was test running correctly?
3. Consider extending duration
4. If still flat, move on - not worth more time

---

## 60 Experiment Ideas by Category

### Acquisition (20)
1. TikTok hook A/B (first 3 seconds)
2. App icon color test
3. Screenshot messaging (features vs benefits)
4. Landing page hero (product vs lifestyle)
5. Cold email subject line test
6. Reddit post title format
7. YouTube Shorts thumbnail style
8. Twitter thread hook format
9. Pinterest pin aspect ratio
10. LinkedIn carousel vs single image
11. SEO title tag variations
12. Meta description CTAs
13. Google Ads headline tests
14. Facebook ad creative (video vs static)
15. Influencer content style
16. Guest post headline format
17. Podcast mention CTA
18. Newsletter ad placement
19. Community post timing
20. Cross-promotion messaging

### Activation (15)
1. Onboarding screen count
2. First action prompt
3. Permission request timing
4. Default settings optimization
5. Progress bar visibility
6. Personalization depth
7. Tutorial format (video/interactive/text)
8. Sign-up form fields
9. Social login options
10. Welcome email timing
11. First session goal setting
12. Feature introduction order
13. Empty state messaging
14. Sample content provision
15. Quick win facilitation

### Retention (15)
1. Push notification copy
2. Push timing (fixed vs personalized)
3. Email cadence
4. Re-engagement triggers
5. Streak visibility
6. Achievement system depth
7. Content refresh frequency
8. Recommendation algorithm
9. Community feature adoption
10. Reminder customization
11. Usage milestone celebrations
12. Win-back email offer type
13. Inactive user segmentation
14. Feature discovery prompts
15. Habit loop optimization

### Revenue (10)
1. Paywall design
2. Pricing display format
3. Annual vs monthly prominence
4. Trial length
5. Trial reminder cadence
6. Upgrade prompt timing
7. Feature gating strategy
8. Discount vs feature messaging
9. Payment method options
10. Cancellation flow optimization

---

## Experiment Culture

### Principles
1. **Ship fast, learn fast** - Velocity > perfection
2. **Celebrate learnings, not just wins** - Failed experiments teach
3. **Data over opinions** - Let the numbers decide
4. **Small bets** - Many small experiments > few big ones
5. **Document everything** - Institutional memory

### Red Flags
- "We already know this won't work" - Test it anyway
- "Users will hate this" - Let them tell you
- "It's too small to matter" - Small lifts compound
- "We don't have enough traffic" - Test bigger changes

---

Last updated: 2026-01-23
