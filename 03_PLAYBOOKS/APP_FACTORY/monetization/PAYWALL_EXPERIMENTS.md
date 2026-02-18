# Paywall experiments

Systematic testing of paywall presentation, timing, and psychology to maximize conversion.

---

## Hard vs soft paywall

### Definitions

**Hard paywall**
- User cannot access core features without subscription
- Free tier is limited demo or no free tier at all
- Trial required to experience value

**Soft paywall**
- Core features available for free
- Premium features locked behind paywall
- User can derive value without paying

### When to use each

| App type | Recommended | Reasoning |
|----------|-------------|-----------|
| Utility (calculator, timer) | Soft | Low differentiation, users will switch |
| Content (meditation, courses) | Hard | Content is the product |
| Productivity (notes, tasks) | Soft | Network effects, switching cost builds |
| Creative (photo editing) | Soft | Users need to see capability first |
| Health/Fitness | Hard | Commitment psychology helps |

### Test framework

```
Experiment: Hard vs soft paywall
Duration: 21 days
Sample: 1000+ users per variant

Variant A (Hard):
- Show paywall after onboarding
- 7-day free trial required
- No free tier features

Variant B (Soft):
- 3 free uses per day
- Premium unlocks unlimited + extra features
- Upgrade prompts at limit

Metrics:
- Day 1 retention
- Day 7 retention
- Trial start rate
- Trial-to-paid conversion
- 30-day revenue per install
```

### Benchmark data

| Paywall type | Trial start rate | Conversion rate | Revenue per install |
|--------------|------------------|-----------------|---------------------|
| Hard | 15-25% | 25-40% of trials | Higher short-term |
| Soft | N/A (no trial) | 3-8% of users | Higher long-term |

---

## Paywall timing experiments

### Timing strategies

**Immediate (after onboarding)**
```
Pros: Filters to high-intent users early
Cons: No value demonstration
Best for: Strong brand recognition, clear value prop
Benchmark: 8-15% trial start rate
```

**After first value moment**
```
Pros: User understands value before ask
Cons: Delayed monetization, some churn before paywall
Best for: Apps requiring demonstration
Benchmark: 15-25% trial start rate
```

**After X uses**
```
Pros: Builds habit before paywall
Cons: Users feel entitled to free access
Best for: Habit-forming apps
Benchmark: 10-20% trial start rate
```

**At feature attempt**
```
Pros: High intent at moment of display
Cons: Can feel bait-and-switch
Best for: Freemium with premium features
Benchmark: 20-35% trial start rate for that feature
```

### Test configurations

**Test 1: Onboarding timing**
```
Variant A: Paywall at end of onboarding
Variant B: Paywall after first session completion
Variant C: Paywall after third session

Primary metric: Revenue per install (7-day)
Secondary: D7 retention, trial conversion
```

**Test 2: Action-triggered paywall**
```
Variant A: Paywall after 3 uses
Variant B: Paywall after 5 uses
Variant C: Paywall after 7 uses

Primary metric: Trial-to-paid conversion
Secondary: Time to conversion, LTV
```

### Timing benchmarks by category

| Category | Optimal timing | Expected trial start |
|----------|----------------|---------------------|
| Meditation | After first session | 18-25% |
| Fitness | After completing onboarding | 20-30% |
| Productivity | After 3-5 uses | 12-18% |
| Photo editing | At premium feature use | 25-35% |
| Learning | After first lesson complete | 15-22% |

---

## Feature gating strategies

### Gating models

**Horizontal gating**
- All features available, usage limited
- Example: 3 exports per month on free tier
- Works for: Tools where usage = value

**Vertical gating**
- Basic features free, advanced paid
- Example: Basic filters free, AI editing paid
- Works for: Apps with clear feature hierarchy

**Time gating**
- Full access limited by time
- Example: 7-day free trial with all features
- Works for: Apps where habit formation matters

**Output gating**
- Creation free, export/save paid
- Example: Design in app, export requires subscription
- Works for: Creative tools

### Feature gating test

```
Experiment: Gating strategy comparison
Duration: 28 days
Sample: 2000+ users per variant

Variant A (Horizontal):
- 5 free uses per day
- Premium = unlimited

Variant B (Vertical):
- Core features free forever
- 4 premium features gated

Variant C (Time):
- 7-day full access trial
- Then limited to basic features

Metrics:
- Trial start rate
- Conversion rate
- D30 retention
- Revenue per install
```

---

## Social proof on paywall

### Social proof elements to test

**User count**
```
"Join 50,000+ users"
Expected lift: 5-15%
```

**Ratings display**
```
"4.8 stars from 2,000+ reviews"
Expected lift: 10-20%
```

**Testimonial quotes**
```
"This app changed my morning routine" - Sarah M.
Expected lift: 8-15%
```

**Usage stats**
```
"Users have completed 1M+ sessions"
Expected lift: 5-12%
```

**Trust badges**
```
"Featured in App Store" + Apple logo
Expected lift: 10-18%
```

### Social proof test framework

```
Experiment: Social proof elements
Duration: 14 days
Sample: 500+ users per variant

Variant A (Control): No social proof
Variant B: User count only
Variant C: Rating + user count
Variant D: Testimonial + rating + user count

Primary metric: Trial start rate
Secondary: Trust survey (if possible)
```

### Placement test

```
Variant A: Social proof above pricing
Variant B: Social proof below pricing
Variant C: Social proof in header

Expected: Above pricing typically wins (15-20% lift)
```

---

## Urgency elements

### Urgency tactics

**Countdown timers**
```
"Offer expires in 23:59:42"
Expected lift: 20-40%
Caution: Can feel manipulative, use sparingly
```

**Limited-time discount**
```
"50% off - Today only"
Expected lift: 30-50%
Caution: Must be genuine or violates FTC rules
```

**Trial expiration reminder**
```
"Your free trial ends in 2 days"
Expected lift: 15-25% (in-app notification)
```

**Social urgency**
```
"127 people upgraded in the last hour"
Expected lift: 10-15%
Caution: Must be real data
```

### Urgency test framework

```
Experiment: Urgency element effectiveness
Duration: 14 days
Sample: 500+ users per variant

Variant A (Control): No urgency
Variant B: Countdown timer (24h offer)
Variant C: Limited spots ("Only 50 spots left at this price")
Variant D: Social proof urgency ("47 upgraded today")

Primary metric: Conversion rate
Secondary: User feedback/complaints, refund rate
```

### Ethical urgency guidelines

**Do:**
- Use real deadlines (trial expiration)
- Show genuine limited-time offers
- Display actual user activity data

**Never:**
- Fake countdown timers that reset
- Fake scarcity ("only 3 left" forever)
- Pressure tactics that harm trust

---

## Paywall design elements

### Layout tests

**Single plan display**
```
Show only annual plan
Expected: Higher ARPU, lower conversion
Best for: High-value apps with clear differentiation
```

**Two plan display**
```
Monthly + Annual side by side
Expected: Balanced conversion and ARPU
Best for: Most apps
```

**Three plan display**
```
Monthly + Annual + Lifetime
Expected: Anchoring effect, annual looks reasonable
Best for: Apps with dedicated user base
```

### Visual hierarchy tests

```
Experiment: Plan highlighting
Duration: 14 days

Variant A: No highlighting
Variant B: "Most Popular" badge on annual
Variant C: Annual plan larger/centered
Variant D: Annual pre-selected

Expected winner: Pre-selected annual (20-30% lift in annual selection)
```

### Copy tests

**Value-focused**
```
"Unlock unlimited access"
"Get the full experience"
```

**Loss-focused**
```
"Don't miss out on these features"
"Your progress will be lost without Pro"
```

**Benefit-focused**
```
"Save 2 hours every week"
"Join 10,000 productive users"
```

```
Experiment: Paywall headline copy
Duration: 14 days

Variant A: "Upgrade to Premium"
Variant B: "Unlock Your Full Potential"
Variant C: "You're 7 days away from [outcome]"

Primary metric: Trial start rate
```

---

## Paywall flow experiments

### Single-screen vs multi-screen

**Single screen**
- All info on one paywall
- Faster decision
- Lower friction
- Works for: Simple value props

**Multi-screen**
- Feature walkthrough before pricing
- Builds value before ask
- Higher friction, higher conversion
- Works for: Complex apps needing explanation

```
Experiment: Paywall flow length
Duration: 21 days

Variant A: Single-screen paywall
Variant B: 2-screen (features + pricing)
Variant C: 3-screen (benefit, features, pricing)

Primary metric: Trial-to-paid conversion
Secondary: Drop-off rate per screen
```

### Exit intent handling

**No action on dismiss**
- User dismisses, nothing happens
- Clean experience
- Baseline conversion

**Discount on dismiss**
- User tries to dismiss, show discount offer
- Can recover 10-20% of dismissers
- Can feel aggressive

**Survey on dismiss**
- Ask why user isn't upgrading
- Gather data for optimization
- Can feel like guilt trip

```
Experiment: Exit intent handling
Duration: 14 days

Variant A: No action
Variant B: 30% discount popup
Variant C: Single question survey + 20% discount

Primary metric: Recovery conversion rate
Secondary: User sentiment (if tracked)
```

---

## Paywall A/B test checklist

Before running any paywall test:

- [ ] Sample size calculated (500+ per variant minimum)
- [ ] Statistical significance threshold defined (95%)
- [ ] Primary and secondary metrics identified
- [ ] Test duration set (minimum 14 days)
- [ ] Segmentation defined (new users only? all users?)
- [ ] Tracking implemented for all conversion events
- [ ] Fallback plan if test harms metrics significantly
- [ ] Legal review for urgency/scarcity claims
- [ ] Screenshots captured for documentation

---

## Paywall conversion benchmarks

### By category

| Category | Trial start rate | Trial-to-paid | Overall conversion |
|----------|------------------|---------------|-------------------|
| Meditation | 18-25% | 35-50% | 6-12% |
| Fitness | 20-30% | 30-45% | 6-13% |
| Productivity | 12-18% | 25-40% | 3-7% |
| Photo/Video | 15-22% | 20-35% | 3-8% |
| Education | 15-22% | 30-45% | 5-10% |

### By paywall type

| Paywall type | Trial start rate | Notes |
|--------------|------------------|-------|
| Hard (immediate) | 8-15% | Lower start, higher intent |
| Soft (usage limit) | N/A | Conversion measured directly |
| Feature-gated | 20-35% | At moment of feature attempt |
| Time-delayed | 15-25% | After N sessions or days |
