# iOS Paywall Best Practices: What Top-Grossing Apps Do and What We Should Copy

Research compiled March 2026. Sources: Adapty State of Subscriptions 2026, RevenueCat State of Subscription Apps 2025, Superwall blog, Airbridge benchmarks, ScreensDesign teardowns, Cal AI founder tweets, Business of Apps trial benchmarks.

---

## 1. WHAT CAL AI DOES (THE BENCHMARK)

Cal AI went from $0 to $50M ARR in 18 months. Their paywall is the single most studied indie app paywall in 2024-2025. Here is their exact flow:

### Onboarding (21 steps)
1. Personal goal setting (weight, target weight, activity level, fitness goals)
2. Goal validation screen ("Your goal is realistic") -- emotional investment hook
3. Progress projection graph showing projected weight loss timeline
4. Social proof / testimonial screen mid-onboarding
5. Feature showcase -- AI food scanning demo (the "magic moment" shown before paywall)
6. Extensive personalization quiz -- makes users feel the app is built for them

**Why 21 steps works:** By the time users hit the paywall, they have invested 2-3 minutes of personal data and emotional energy. Sunk cost psychology kicks in. Duolingo uses 52 steps. Long onboarding = higher conversion. 83% of users who start onboarding reach the paywall screen. 16% of those convert to trial.

### Hard Paywall (no free tier)
- Users CANNOT access any core features without starting a free trial
- Payment info required upfront
- 3-day free trial with visual timeline showing: sign up today > reminder before trial ends > billing starts after day 3

### Pricing Structure
- **Two plans only:** Monthly (~$10/mo) and Yearly (~$30/yr, shown as ~$2.50/mo)
- Monthly is the anchor (makes yearly look cheap)
- Yearly is visually emphasized (highlighted, "BEST VALUE" badge)
- If user declines, a "rescue offer" appears at ~$20/year
- Price varies by user segment (dynamic pricing)

### Key Cal AI Numbers
- ~500K monthly installs
- LTV estimated ~$100 per acquired customer
- $2M+/mo revenue at scale
- 150+ influencers on retainer, each posting 4x/month
- $7,000/day on paid ads (layered AFTER influencer saturation)
- Break-even math: at $100 LTV, need only 5 customers per 100K-view influencer video

### Tools Cal AI Uses
- **RevenueCat** for subscription management
- **Superwall** for paywall A/B testing (recommended by co-founder Blake Anderson)
- **Adapty** for paywall management and analytics
- **Amplitude/Mixpanel** for event tracking and onboarding A/B testing

---

## 2. THE STANDARD PLAYBOOK (TOP-GROSSING APPS)

### Duolingo (52-step onboarding, $700M+ ARR)
- Progressive disclosure: multiple screens, never overloads
- Shows value at $0.00 first, then feature comparison, then trial reminder, then price
- Bright gradients + mascot for brand consistency
- 7-day free trial with "Cancel anytime" stated plainly
- Two plan options with "Most Popular" tag
- CTA: "Start my free week" (user-centric, not "Subscribe")

### Calm (dynamic paywall, $100M+ ARR)
- Dynamic paywalls triggered when users tap locked content
- Copy and imagery change based on WHAT the user tapped
- Pulls through the image of tapped content in paywall header
- Segmented messaging for different user intents (sleep vs. anxiety vs. meditation)

### Headspace (segmented paywalls)
- Different paywall messages for different user segments
- Tailored to specific interests: stress relief, better sleep, focus
- Price testing every 6 months
- Treats paywall as a living sales funnel, not a static screen

### Noom (long onboarding + personalization)
- 15-20 minute onboarding quiz (even longer than Cal AI)
- Creates a "personalized plan" that makes the subscription feel necessary
- Hard paywall after extensive investment

### AllTrails (freemium with contextual upsell)
- Free tier exists with basic features
- Premium paywall shown at moments of high intent (mid-hike, trail download)
- Contextual paywalls convert better than one-size-fits-all

---

## 3. HARD PAYWALL VS SOFT PAYWALL VS FREEMIUM: THE DATA

### Conversion Rates (Airbridge/Adapty 2026 data)

| Model | Install-to-Paid | Notes |
|-------|-----------------|-------|
| Hard paywall | 10.7% median | Self-selects for high-intent users |
| Hard paywall top 10% | 38.7% | Elite apps with strong onboarding |
| Soft paywall | ~50% higher than hard | But lower quality users |
| Freemium | 2.1% | 5x lower than hard paywall |
| Onboarding with trial | 1.78% install-to-paid | Highest placement conversion |
| In-app paywall | 1.60% install-to-paid | Second best |
| Web paywall | 1.10% install-to-paid | Lowest, but avoids 30% Apple fee |

### Revenue Quality

| Metric | Hard Paywall | Freemium |
|--------|-------------|----------|
| 1-year LTV | 21% higher | Baseline |
| Revenue per install (Day 14) | 8x higher | Baseline |
| Retention after 1 year | 12.8% | Nearly identical |
| Refund rate | 5.8% | Lower |
| Day 0 conversion | 50% of paid conversions | 23% happen 6+ weeks later |

### Health & Fitness Category Specifically (our apps)

| Metric | Value |
|--------|-------|
| Trial-to-paid conversion | 35.0% (highest of all categories) |
| First-renewal retention | 30.3% (lowest of all categories -- churn risk) |
| Install LTV | $1.20 (highest of all categories) |
| Annual plan share of revenue | 68% |
| Annual subscriber retention (Day 380) | 19.9% |
| Monthly subscriber retention (Day 380) | 14.2% |
| Weekly subscriber retention (Day 380) | 5.5% |

### The Verdict
Hard paywall wins for health/fitness/productivity apps where the user has a specific problem and arrives with intent. Soft paywall/freemium wins for discovery-driven apps (social, games) where users need to experience value first. For our streak/devotional apps: **hard paywall with long onboarding is the play.**

---

## 4. APPLE IAP VS STRIPE VS BOTH: THE TRADEOFFS

### Post-Epic v. Apple Ruling (May 2025)

US iOS apps can now link to external payment systems. Apple cannot charge commission on off-app transactions. This changes the math.

| Payment Method | Fee | Conversion | Best For |
|----------------|-----|------------|----------|
| Apple IAP (via RevenueCat) | 30% (15% small biz) | Highest -- one-tap purchase | Primary flow, all users |
| Stripe web checkout | 2.9% + $0.30 | -11.9% vs IAP | High-LTV users, annual plans |
| Both (hybrid) | Mixed | Optimized | Best of both worlds |

### Superwall's Early Data on Web Checkout
- Conversion drop: -11.9% when sending users to web checkout vs IAP
- Net proceeds increase: +19.85% despite lower conversion (avoiding 30% fee)
- If trial conversion improves by 10%, net proceeds increase ~32%
- For Small Business Program (15% fee): web checkout may REDUCE proceeds by ~1.3% unless trial conversion improves 20%+

### Recommendation for Our Apps
1. **Primary:** RevenueCat for Apple IAP -- handles StoreKit complexity, subscription management, analytics, cross-platform
2. **Secondary:** Stripe web checkout for annual plans in US -- offer a "web discount" (pass some of the 27% savings to the user as lower price)
3. **RevenueCat + Stripe integration exists** -- RevenueCat syncs entitlements across IAP and Stripe purchases automatically
4. Start with IAP only. Add Stripe web flow after reaching $1K MRR when optimization matters.

---

## 5. THE ONBOARDING-TO-PAYWALL FLOW THAT CONVERTS BEST

### The Proven Sequence (based on top 10% performing apps)

```
INSTALL
  |
  v
STEP 1-3: Personal questions (goal, situation, preferences)
  - Build emotional investment
  - Collect data for personalization
  |
  v
STEP 4-5: Validation + projection
  - "Your goal is achievable"
  - Show projected outcome with timeline graph
  |
  v
STEP 6-7: Social proof
  - Testimonials mid-flow (not at paywall)
  - Before/after results from real users
  |
  v
STEP 8-10: Feature showcase / "magic moment"
  - Demo the core feature
  - Let them FEEL the value before asking for money
  |
  v
STEP 11-15: Deeper personalization
  - Makes the subscription feel CUSTOM
  - Sunk cost deepens with each step
  |
  v
PAYWALL
  - Visual trial timeline (Apple-endorsed pattern)
  - "No payment due now" prominently displayed
  - Two plans (monthly anchor + yearly highlight)
  - Benefit-driven CTA ("Start my plan" not "Subscribe")
  - "Cancel anytime" visible
  |
  v
DECLINE HANDLER
  - Rescue offer (lower price or extended trial)
  - Or exit to limited free experience (soft paywall variant)
```

### Key Timing Stats
- 82% of trial starts happen on Day 0 (same day as install)
- 78% of hard paywall users start trial in first week
- 50% of paid conversions in health/fitness happen on Day 0
- Conversion drops dramatically after Day 0 -- the onboarding paywall is your ONE shot

---

## 6. SPECIFIC UI PATTERNS THAT INCREASE CONVERSION

### Trial Language That Works
- "No payment due now" -- #1 friction reducer (Cal AI uses this)
- "Cancel anytime" -- reduces commitment anxiety
- "Start my free week" / "Start my plan" -- user-centric CTAs beat "Subscribe" or "Buy"
- "Try free for 3 days" -- specific timeframe beats vague "free trial"
- Visual timeline showing: Today (free) > Day 2 (reminder) > Day 3 (billing starts) -- Apple-endorsed, Blinkist pioneered

### Pricing Anchoring
- Show monthly price first as the anchor ($9.99/mo = $120/yr)
- Highlight yearly as the deal ($29.99/yr = $2.50/mo, "Save 75%")
- Use per-day framing for yearly: "Less than $0.10/day"
- **Two plans maximum.** 50% of top-grossing apps offer only 1 tier. 30% offer 2. Fewer choices = more conversions.
- "Most Popular" or "Best Value" badge on the plan you want them to pick

### Rescue Offers (decline handling)
- When user hits X or back: show a lower-priced offer
- Cal AI shows ~$20/year rescue after declining ~$30/year
- Some apps offer extended trial (7 days instead of 3)
- Some apps offer a one-time "lifetime" purchase as rescue
- Rescue offers can recover 10-20% of declining users

### Social Proof on Paywalls
- Star ratings ("4.8 stars, 100K+ reviews")
- User count ("Join 2M+ users")
- Testimonial quotes (keep short, 1 line)
- Before/after imagery (health/fitness)
- "As featured in" logos (press mentions)

### Visual Design
- Clean, uncluttered -- reduce cognitive load
- Feature benefits as icons + short text (3-5 max)
- Benefit-driven, not feature-driven ("Reach your goal 3x faster" not "Premium content")
- High contrast CTA button (stands out from background)
- Progress indicator showing how close they are to their personalized plan

### Dynamic/Contextual Paywalls
- Calm changes paywall copy based on what locked content the user tapped
- Show different paywalls to different user segments (new vs returning, source channel)
- Superwall/Adapty enable this without app store updates
- Apps using dynamic paywalls see 20%+ conversion lift vs static paywalls

---

## 7. SUBSCRIPTION PERIOD: WHAT TO OFFER

### Revenue Distribution (Adapty 2026)
- Weekly plans: 55.6% of all subscription revenue
- Monthly plans: 27.9%
- Annual plans: 6.2%
- One-time purchases: 10.3%

### But for Health & Fitness Specifically
- Annual plans generate 68% of category revenue
- Annual subscribers retain at 19.9% after Day 380 (3.6x better than weekly)
- Health/fitness is one of the few categories where annual wins over weekly

### Conversion vs Retention Tradeoff
- Weekly plans convert 2-7x better than annual
- But weekly retention is abysmal (5.5% at Day 380)
- Annual has highest LTV despite lower initial conversion
- **For our apps: lead with annual (highlighted), offer monthly as anchor. No weekly.**

### Trial Impact
- Trial users show 8-60% better retention at first renewal
- Weekly plans with trials: 636% LTV increase ($7.40 to $54.50)
- Of users who start a trial, 38% convert to paid (top quartile: 60%+)
- 3-day trial is standard for hard paywall apps
- 7-day trial is standard for soft paywall / freemium apps

---

## 8. TOOLS TO IMPLEMENT THIS

| Tool | Purpose | Cost | Priority |
|------|---------|------|----------|
| **RevenueCat** | Subscription management, Apple/Google IAP, analytics | Free to $99/mo | P0 -- required |
| **Superwall** | Remote paywall config, A/B testing, no app updates needed | Free tier available | P1 -- high leverage |
| **Adapty** | Alternative to Superwall (paywall testing + analytics) | Free tier available | P1 alternative |
| **Stripe** | Web checkout for US users (avoid 30% Apple fee) | 2.9% + $0.30 | P2 -- after $1K MRR |
| **Mixpanel/Amplitude** | Onboarding funnel analytics | Free tier | P1 -- measure everything |

### RevenueCat + Superwall is the standard stack for indie apps doing $10K-$1M ARR.

---

## 9. WHAT OUR 4 APPS SHOULD COPY -- EXACT IMPLEMENTATION

### For Each Streak App (Scripture Streak, Quran Streak, Gita Streak, etc.)

**Onboarding Flow (12-18 steps):**
1. Welcome screen with app value prop (1 screen)
2. "What's your goal?" (spiritual growth / daily habit / deeper understanding)
3. "How often do you want to read?" (daily / 5x week / 3x week)
4. "What time works best?" (morning / afternoon / evening)
5. "How long per session?" (5 min / 10 min / 15 min)
6. Validation: "Based on your answers, you'll complete [X chapters] in [Y days]"
7. Progress projection graph (visual timeline to completion)
8. Social proof: "[X,000] people are on a streak right now"
9. Feature showcase: show the daily reading experience, streak tracking, progress
10. Notification permission request (after showing value, not before)
11. Personalization summary: "Your personalized plan is ready"
12. **PAYWALL**

**Paywall Screen:**
- Header: "Start Your Journey" or "Your Plan Is Ready"
- Visual trial timeline: Today (free) > Day 2 (reminder) > Day 3 (billing starts)
- "No payment due now" prominently displayed
- Two plans:
  - Monthly: $6.99/mo (the anchor)
  - Yearly: $29.99/yr ($2.50/mo) -- highlighted with "BEST VALUE" badge and "Save 70%"
- Benefits list (3 items max, icons):
  - Unlimited daily readings with commentary
  - Streak tracking and progress insights
  - Offline access to all content
- CTA button: "Start My Free Trial" (large, high contrast)
- Below CTA: "Cancel anytime. No commitment."
- Social proof: "4.8 stars | Join 10,000+ readers"

**Decline Handler:**
- If user taps X: show rescue offer
- Rescue: $19.99/year or 7-day extended trial
- If user declines rescue: limited free tier (1 reading per day, no streak features)

**Payment Stack:**
- RevenueCat for Apple IAP (primary)
- 3-day free trial on both plans
- Annual plan preselected
- Stripe web checkout added later (post $1K MRR, US users only)

**A/B Test Plan (via Superwall, week 1):**
1. Test: 3-day trial vs 7-day trial
2. Test: $29.99/yr vs $24.99/yr vs $34.99/yr
3. Test: "Start My Free Trial" vs "Start My Plan" vs "Try Free for 3 Days"
4. Test: with rescue offer vs without

---

## 10. METRICS TO TRACK

| Metric | Target | Source |
|--------|--------|--------|
| Onboarding completion rate | >80% | Mixpanel/Amplitude |
| Install-to-trial rate | >10% | RevenueCat |
| Trial-to-paid conversion | >35% | RevenueCat |
| Day 0 trial starts | >80% of all trials | RevenueCat |
| Annual plan selection rate | >60% | RevenueCat |
| First renewal retention | >30% | RevenueCat |
| Day 380 retention (annual) | >15% | RevenueCat |
| Rescue offer recovery rate | >10% | Superwall |
| Paywall A/B test frequency | 1 test/2 weeks | Superwall |

---

## SOURCES

- Adapty State of In-App Subscriptions Report 2026
- RevenueCat State of Subscription Apps 2025
- Airbridge: Hard Paywall vs Soft Paywall vs Freemium
- Superwall: App-to-Web Conversion Rates After App Store Ruling
- Superwall: Proven Paywall and Pricing Experiments
- Business of Apps: App Subscription Trial Benchmarks 2026
- Cal AI founder tweets (@zach_yadegari, @blakeandersonw)
- ScreensDesign: Cal AI teardown
- RevenueCat: Hard Paywall vs Soft Paywall
- RevenueCat: How Top Apps Approach Paywalls
- RevenueCat: Can You Use Stripe for In-App Purchases
- Adapty: Can You Use Stripe for In-App Purchases in 2026
