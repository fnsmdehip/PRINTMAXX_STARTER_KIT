# Onboarding Optimization Playbook

Diagnose and fix common onboarding drop-offs. Organized by symptom.

---

## Diagnosis Framework

### Step 1: Identify the problem screen

Look at screen-by-screen completion rates. The screen with the highest drop-off needs attention first.

### Step 2: Categorize the drop-off type

| Drop-off Pattern | Likely Cause | Section |
|------------------|--------------|---------|
| > 30% drop on welcome screen | App icon/store listing mismatch | Welcome Screen Fixes |
| High drop on permission screens | Poor permission priming | Permission Request Fixes |
| High drop on preference screens | Too many choices or unclear value | Preference Screen Fixes |
| High drop on paywall | Weak value prop or wrong timing | Paywall Fixes |
| High drop on final action | Friction or unclear next step | First Action Fixes |
| High drop everywhere | Slow load times or bugs | Technical Fixes |

### Step 3: Apply targeted fixes

Use the specific fixes below based on your diagnosis.

---

## Welcome Screen Fixes

**Symptom:** > 5% drop-off on the first screen

### Problem: App store expectation mismatch

**Diagnosis:** Users downloaded expecting something different.

**Fixes:**
1. Audit your app store screenshots and description
2. Make sure onboarding headline matches store promise
3. Show the core value in first 3 seconds

### Problem: Slow load time

**Diagnosis:** Screen takes > 2 seconds to appear.

**Fixes:**
1. Preload onboarding assets during splash screen
2. Use static images instead of videos on first screen
3. Compress images (< 100KB per screen)
4. Remove animations that delay content display

### Problem: Unclear value proposition

**Diagnosis:** Users don't understand what the app does.

**Fixes:**
1. Lead with the outcome, not the feature
   - Bad: "Track your habits"
   - Good: "Build habits that stick"
2. Add social proof immediately
   - "Join 10,000 users who..."
3. Use a single sentence that explains the core benefit

### A/B Tests to Run

| Test | Control | Variant |
|------|---------|---------|
| Headline focus | Feature-focused | Outcome-focused |
| Social proof | None | User count |
| Visual | Illustration | Screenshot of app |

---

## Permission Request Fixes

**Symptom:** > 35% drop-off on notification permission, > 25% on health/screen time

### Problem: Asking too early

**Diagnosis:** Permission requested before user sees value.

**Fixes:**
1. Move permission request after value demonstration
2. Show what the permission enables before asking
3. Use a "prime" screen before the system prompt

**Permission priming template:**
```
Screen before permission:
Headline: "Get reminded to [habit]"
Body: "82% of users who enable reminders complete their goal."
CTA: "Enable reminders" -> triggers system prompt
Skip: "Maybe later"
```

### Problem: No explanation of why

**Diagnosis:** User doesn't understand the benefit.

**Fixes:**
1. Explain the specific benefit of granting permission
2. Address privacy concerns proactively
3. Show what notifications look like

**Good notification priming:**
```
Headline: "Can we remind you to pray?"
Body: "A gentle nudge each morning. No spam."
[Preview of notification: "Your prayer time is waiting"]
CTA: "Enable reminders"
```

### Problem: Permission feels invasive

**Diagnosis:** Users concerned about privacy or control.

**Fixes:**
1. Add privacy assurance text
2. Emphasize user control
3. Make it clear what you won't do

**Privacy assurance example:**
```
"Your health data stays on your device. We only read step count. Nothing else is accessed or uploaded."
```

### Problem: Screen Time permission is confusing

**Diagnosis:** Users don't understand accessibility/screen time permissions.

**Fixes:**
1. Explain exactly what the permission does
2. Show before/after of app behavior
3. Acknowledge it looks scary

**Good screen time explanation:**
```
Headline: "One permission to make this work"
Body: "We need Screen Time access to block apps. This lets us show you a locked screen when you try to open [blocked app]. Without this, the app can't do its job."
Visual: Screenshot of a blocked app screen
CTA: "Grant access"
```

### A/B Tests to Run

| Test | Control | Variant |
|------|---------|---------|
| Timing | During onboarding | After first value moment |
| Priming | System prompt only | Prime screen + system prompt |
| Copy | Generic | Benefit-focused |

---

## Preference Screen Fixes

**Symptom:** > 15% drop-off on goal/preference selection

### Problem: Too many choices

**Diagnosis:** Decision paralysis from too many options.

**Fixes:**
1. Reduce options to 4-6 maximum
2. Add "most popular" badge to guide choice
3. Make one option the default/recommended
4. Allow "skip" with a sensible default

### Problem: Options are unclear

**Diagnosis:** Users don't understand what they're choosing.

**Fixes:**
1. Add descriptions to each option
2. Use concrete examples, not abstract labels
3. Show what the selection changes in the app

**Good option format:**
```
Option: "5,000 steps"
Subtext: "About 50 minutes of walking. Most popular choice."
```

### Problem: Forced choice feels premature

**Diagnosis:** Users don't know enough to choose yet.

**Fixes:**
1. Add "I'll decide later" option
2. Explain that choices can be changed
3. Use smart defaults based on common choices

### Problem: Selection doesn't feel personalized

**Diagnosis:** Generic options that don't resonate.

**Fixes:**
1. Use contextual options based on earlier selections
2. Add follow-up questions to narrow down
3. Show how selection affects their experience

### A/B Tests to Run

| Test | Control | Variant |
|------|---------|---------|
| Number of options | Many (6+) | Few (3-4) |
| Default selection | None | Recommended option |
| Skip option | Hidden | Visible |

---

## Paywall Fixes

**Symptom:** > 50% drop-off on hard paywall, > 25% on soft paywall

### Problem: Value not demonstrated yet

**Diagnosis:** Paywall appears before user experiences benefit.

**Fixes:**
1. Move paywall later in the flow
2. Show a "taste" of the product first
3. Use delayed paywall (after first session, not during onboarding)

### Problem: Price feels too high

**Diagnosis:** Sticker shock at pricing.

**Fixes:**
1. Show per-week/per-day pricing
   - "$49.99/year" -> "$0.96/week"
2. Compare to relatable purchases
   - "Less than one coffee per week"
3. Anchor with a higher decoy price
   - Show monthly prominently, then annual as "save 58%"

### Problem: Features don't matter to user

**Diagnosis:** Feature list doesn't resonate.

**Fixes:**
1. Lead with outcomes, not features
   - Bad: "Unlimited habits"
   - Good: "Build any habit you want"
2. Show before/after transformation
3. Use testimonials that describe results

### Problem: No urgency to act now

**Diagnosis:** User thinks "I'll come back later."

**Fixes:**
1. Add trial that expires
2. Show limited-time offer (careful with compliance)
3. Highlight what they'll miss without premium

### Problem: Paywall design feels aggressive

**Diagnosis:** "Salesy" design creates distrust.

**Fixes:**
1. Use softer colors and language
2. Make the free/trial option visible
3. Remove artificial urgency (countdown timers, etc.)

### Paywall Copy Framework

**Headline formula:** [Outcome they want] + [Timeframe or ease]

Examples:
- "Build lasting habits in 5 minutes a day"
- "Your prayer life, transformed"
- "Walk more. Scroll less."

**Price framing hierarchy:**
1. Annual price (best value, show savings)
2. Monthly price (easy to compare)
3. Per-week/day (minimize perceived cost)

### A/B Tests to Run

| Test | Control | Variant |
|------|---------|---------|
| Timing | During onboarding | After first session |
| Price framing | Annual | Per-week |
| Headline | Feature-focused | Outcome-focused |
| Social proof | None | Testimonial |
| Trial length | 3 days | 7 days |

---

## First Action Fixes

**Symptom:** > 20% drop-off on final onboarding screen or first action

### Problem: Unclear what to do next

**Diagnosis:** User doesn't know how to start.

**Fixes:**
1. Single, clear CTA
2. Remove secondary options
3. Make the first action trivially easy

### Problem: First action feels too big

**Diagnosis:** First task seems overwhelming.

**Fixes:**
1. Break into micro-steps
2. Provide a "quick start" option
3. Set extremely low bar for first win

**Examples:**
- PrayerLock: "Start with a 5-minute session"
- WalkToUnlock: "Your steps today already count"
- StudyLock: "Just 15 minutes to start"
- PromptVault: "Copy your first prompt"
- DailyAnchor: "Check off one habit"
- FemFit: "Try a 10-minute workout"
- DailyDevotion: "Read today's verse (30 seconds)"

### Problem: Friction in completing first action

**Diagnosis:** Technical barriers prevent completion.

**Fixes:**
1. Pre-fill information from earlier screens
2. Remove required fields
3. Provide sensible defaults

### Problem: User doesn't see immediate value

**Diagnosis:** First action doesn't deliver a reward.

**Fixes:**
1. Add celebration/feedback on completion
2. Show progress immediately
3. Connect first action to their stated goal

### A/B Tests to Run

| Test | Control | Variant |
|------|---------|---------|
| CTA text | "Get started" | "Do it now" |
| First action size | Full action | Micro-action |
| Celebration | None | Confetti/animation |

---

## Technical Fixes

**Symptom:** Drop-off is high everywhere, or users report bugs

### Problem: Slow load times

**Diagnosis:** Screens take > 1 second to load.

**Fixes:**
1. Measure and optimize image sizes
2. Preload next screen while on current
3. Use skeleton loaders instead of spinners
4. Defer non-critical operations

### Problem: Crashes during onboarding

**Diagnosis:** Crashlytics shows onboarding crashes.

**Fixes:**
1. Add error boundaries
2. Handle edge cases (no network, permissions denied)
3. Test on low-end devices
4. Add retry mechanisms

### Problem: State is lost on app kill

**Diagnosis:** Users restart from beginning if they close app.

**Fixes:**
1. Save progress after each screen
2. Resume from last completed screen
3. Don't require continuous session

### Problem: Deep link breaks onboarding

**Diagnosis:** Users from ads skip onboarding.

**Fixes:**
1. Force onboarding for new users regardless of deep link
2. Queue the deep link destination for after onboarding
3. Track deep link users separately

---

## Drop-off Triage Checklist

When drop-off is higher than benchmark, work through this checklist:

### Immediate checks (< 1 hour)
- [ ] Is the screen loading correctly? (No crashes, no blank screens)
- [ ] Is the CTA visible above the fold?
- [ ] Does the CTA work? (Test yourself)
- [ ] Are there any error states being triggered?

### Copy review (1-2 hours)
- [ ] Is the headline clear and benefit-focused?
- [ ] Is the body copy concise (< 30 words)?
- [ ] Does the CTA tell users what happens next?
- [ ] Is there unnecessary friction (too many fields, unclear options)?

### Design review (2-4 hours)
- [ ] Is the visual hierarchy correct (headline > body > CTA)?
- [ ] Is there visual clutter competing for attention?
- [ ] Does the screen feel consistent with previous screens?
- [ ] Are touch targets large enough (44x44pt minimum)?

### Analytics deep dive (4-8 hours)
- [ ] Are certain user segments dropping more than others?
- [ ] Is there a time-of-day pattern?
- [ ] Did the drop-off start after a specific release?
- [ ] What's the time spent on this screen vs others?

---

## Optimization Prioritization Matrix

Use this to prioritize which screens to fix first.

| Drop-off | Traffic | Priority | Action |
|----------|---------|----------|--------|
| High | High | P0 | Fix immediately |
| High | Low | P1 | Fix this week |
| Low | High | P2 | Optimize for gains |
| Low | Low | P3 | Monitor only |

**Traffic = percentage of all users who reach this screen**

Example:
- Welcome screen: 100% traffic, 8% drop-off = P0
- Permission screen: 92% traffic, 30% drop-off = P0
- Paywall: 64% traffic, 45% drop-off = P1
- Final action: 35% traffic, 15% drop-off = P2

---

## Quick Wins Checklist

These typically improve metrics without major effort:

### Copy quick wins
- [ ] Add social proof number to welcome screen
- [ ] Add "most popular" badge to default option
- [ ] Rewrite headline as outcome, not feature
- [ ] Add privacy assurance before permissions
- [ ] Show per-week price instead of annual

### Design quick wins
- [ ] Increase CTA button size
- [ ] Add progress indicator
- [ ] Reduce number of options
- [ ] Add default selection
- [ ] Add completion celebration

### Technical quick wins
- [ ] Preload next screen assets
- [ ] Save progress after each screen
- [ ] Add loading states
- [ ] Handle offline gracefully

---

## Quarterly Optimization Cadence

### Month 1: Audit and baseline
- Instrument all analytics events
- Establish baseline metrics
- Identify top 3 drop-off screens

### Month 2: Fix critical issues
- Address P0 and P1 screens
- Run A/B tests on paywall
- Optimize permission flows

### Month 3: Iterate and expand
- Ship winning A/B variants
- Start new tests on secondary screens
- Document learnings

### Ongoing
- Weekly metric review
- Monthly A/B test planning
- Quarterly deep audit
