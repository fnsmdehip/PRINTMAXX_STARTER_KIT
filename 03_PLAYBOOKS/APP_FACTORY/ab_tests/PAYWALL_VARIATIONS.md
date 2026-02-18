# Paywall A/B Test Variations

Ready-to-test paywall copy and design variations for each app template.

---

## Universal Paywall Framework

Every paywall test should include:
1. Clear value proposition
2. Price anchor (crossed out higher price or comparison)
3. Social proof element
4. Risk reversal (trial, guarantee)
5. Single prominent CTA

---

## Dating App (HeartSync)

### Version A: Emotional Connection

```
[HERO IMAGE: Couple silhouette or heart visual]

"Stop swiping. Start connecting."

What you get with Premium:
- See everyone who liked you
- Unlimited daily likes
- No ads interrupting your search
- Advanced filters to find your type

[50,000+ matches made this month]

$9.99/week
[Start Free Trial]

7-day free trial. Cancel anytime.
```

### Version B: Feature-Focused

```
[HERO IMAGE: App interface preview]

"Unlock HeartSync Premium"

PREMIUM FEATURES:
✓ Unlimited likes (vs 50/day free)
✓ See who liked you first
✓ Advanced matching filters
✓ Rewind accidental swipes
✓ 5 Super Likes per day
✓ Boost your profile weekly

[Pricing table]
Weekly: $9.99
Monthly: $29.99 (save 25%)
Annual: $79.99 (save 84%)

[Get Premium]
```

### Version C: Social Proof Heavy

```
[HERO IMAGE: Real couple photo with quote]

"We met on HeartSync 6 months ago.
Now we're engaged." - Sarah & Mike

Join 2.3M members finding real love.

Premium members are 3x more likely to match.

Why? Because you can:
- See who likes you (no more guessing)
- Like without limits
- Get seen first with Profile Boost

$9.99/week
[Join Premium]

★★★★★ 4.8 rating (127K reviews)
```

### RevenueCat Configuration

```json
{
  "experiment_name": "paywall_copy_test_heartsync",
  "variants": [
    {"name": "emotional", "paywall_id": "heartsync_paywall_emotional"},
    {"name": "features", "paywall_id": "heartsync_paywall_features"},
    {"name": "social_proof", "paywall_id": "heartsync_paywall_social"}
  ],
  "traffic_split": [34, 33, 33],
  "primary_metric": "conversion_rate",
  "secondary_metrics": ["revenue_per_user", "trial_start_rate"]
}
```

---

## Fitness App (FitTracker)

### Version A: Transformation Focus

```
[HERO IMAGE: Before/after transformation]

"Your 30-day transformation starts now."

Sarah lost 15 lbs in her first month.
Join 500K+ who transformed with FitTracker Pro.

PRO FEATURES:
- 200+ workout programs
- AI personal trainer
- Custom meal plans
- Progress tracking
- Offline workouts

$9.99/month
(That's $0.33/day for a personal trainer)

[Start My Transformation]

30-day money-back guarantee
```

### Version B: Problem/Solution

```
[HERO IMAGE: Person struggling then succeeding]

"Tired of workouts that don't work?"

Most apps give you generic plans.
FitTracker Pro adapts to YOUR body.

HOW IT WORKS:
1. AI analyzes your goals & fitness level
2. Creates your personalized plan
3. Adjusts as you progress

WHAT YOU GET:
- Custom workout plans
- Meal planning with macros
- 24/7 AI coaching
- Community challenges

$9.99/month
[Try Free for 7 Days]

No commitment. Cancel anytime.
```

### Version C: Value Comparison

```
[HERO IMAGE: Price comparison visual]

"Personal trainer: $200/session
FitTracker Pro: $9.99/month"

Same results. 95% less cost.

INCLUDED IN PRO:
✓ 200+ expert workout programs
✓ AI coaching that adapts to you
✓ Meal plans + shopping lists
✓ Progress photos & measurements
✓ Community accountability

[COMPARISON TABLE]
              Free    Pro
Workouts      10     200+
AI Coaching   ✗      ✓
Meal Plans    ✗      ✓
Offline Mode  ✗      ✓

[Upgrade to Pro - $9.99/mo]

Join 500,000+ members
```

### RevenueCat Configuration

```json
{
  "experiment_name": "paywall_copy_test_fittracker",
  "variants": [
    {"name": "transformation", "paywall_id": "fittracker_paywall_transform"},
    {"name": "problem_solution", "paywall_id": "fittracker_paywall_problem"},
    {"name": "value_comparison", "paywall_id": "fittracker_paywall_value"}
  ],
  "traffic_split": [34, 33, 33],
  "primary_metric": "conversion_rate"
}
```

---

## AI/Productivity App (AIWriter)

### Version A: Productivity Angle

```
[HERO IMAGE: Time saved visualization]

"Write 10x faster. Sound 10x smarter."

AIWriter Pro handles the heavy lifting:
- Blog posts in 30 seconds
- Emails that get responses
- Social posts that engage
- Code documentation done right

FREE: 10 generations/day
PRO: Unlimited everything

"Saved me 5 hours this week alone" - @marketer_joe

$9.99/month
[Unlock Unlimited]

3-day free trial included
```

### Version B: FOMO/Scarcity

```
[HERO IMAGE: Counter or limited badge]

"You've hit your daily limit."

10/10 generations used today.

Don't let ideas wait until tomorrow.

PRO WRITERS GET:
- Unlimited generations
- Priority processing (2x faster)
- Advanced models (GPT-4 level)
- Custom brand voice
- API access

[SPECIAL OFFER: 50% OFF]
~~$19.99~~ $9.99/month

[Upgrade Now - Limited Time]

2,847 upgraded this week
```

### Version C: Use Case Specific

```
[HERO IMAGE: Content examples]

"What will you create today?"

[TAB: Blog Posts]
Write SEO-optimized articles in seconds.

[TAB: Social Media]
Generate a week of content in 10 minutes.

[TAB: Emails]
Cold emails that get 40% reply rates.

[TAB: Code Docs]
Auto-document your entire codebase.

PRO UNLOCKS ALL:
- Unlimited content
- All 50+ templates
- Custom training
- Team collaboration

$9.99/month or $79/year (save 34%)

[Start Free Trial]

Used by writers at Netflix, Airbnb, Stripe
```

### RevenueCat Configuration

```json
{
  "experiment_name": "paywall_copy_test_aiwriter",
  "variants": [
    {"name": "productivity", "paywall_id": "aiwriter_paywall_productivity"},
    {"name": "fomo_scarcity", "paywall_id": "aiwriter_paywall_fomo"},
    {"name": "use_cases", "paywall_id": "aiwriter_paywall_usecases"}
  ],
  "traffic_split": [34, 33, 33],
  "primary_metric": "conversion_rate"
}
```

---

## Paywall Design Variations (Cross-App)

### Design A: Minimalist

```
[Single color background]
[One headline]
[3 bullet points max]
[Price]
[Single CTA button]

No images, no testimonials, no comparison tables.
Let the copy do the work.
```

### Design B: Rich Media

```
[Video background or hero image]
[Animated elements]
[Scrolling testimonials]
[Interactive pricing toggle]
[Multiple CTA touchpoints]

Full experience, potentially overwhelming.
```

### Design C: Social Proof Wall

```
[Grid of user testimonials/photos]
[Star ratings prominent]
[Usage statistics]
[Press mentions]
[Minimal feature list]

Trust signals over features.
```

---

## Paywall Trigger Points to Test

### Trigger A: Immediate
- Show paywall on first app open
- Before any value delivered
- High impression volume, lower conversion

### Trigger B: After Value
- Show after first successful action
- User has experienced core value
- Lower impression volume, higher conversion

### Trigger C: Usage Limit
- Show when free limit reached
- Maximum pain point
- Converts motivated users, may lose casual users

### Trigger D: Feature Gate
- Show when premium feature tapped
- Intent signal strong
- May never see paywall if feature undiscovered

---

## Implementation Checklist

For each paywall variant:

- [ ] Copy written and reviewed
- [ ] Design mockup approved
- [ ] Implemented in app
- [ ] RevenueCat experiment configured
- [ ] Analytics events tracking
- [ ] QA on all devices
- [ ] Baseline metrics documented
- [ ] Test duration calculated
- [ ] Added to LEDGER/AB_TESTS_MASTER.csv

---

## Measurement Framework

### Primary Metric
- **Conversion rate**: Paywall views to purchase

### Secondary Metrics
- Trial start rate
- Trial to paid conversion
- Revenue per user (RPU)
- Churn within 7 days

### Segment Analysis
- New vs returning users
- iOS vs Android
- Organic vs paid acquisition
- Geographic region

---

*Use these templates as starting points. Customize for your specific app's voice and value proposition.*
