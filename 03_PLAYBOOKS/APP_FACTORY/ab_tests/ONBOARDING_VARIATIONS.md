# Onboarding A/B Test Variations

Ready-to-test onboarding flows for improved activation and retention.

---

## Onboarding Length Tests

### Test 1: Short vs Long Flow

**Hypothesis:** Shorter onboarding reduces drop-off but may reduce personalization benefits.

**Variant A: 3-Screen Flow**
```
Screen 1: Welcome + value prop
Screen 2: Key permission (notifications)
Screen 3: Start using app
```

**Variant B: 5-Screen Flow**
```
Screen 1: Welcome + value prop
Screen 2: Goal selection
Screen 3: Personalization question 1
Screen 4: Personalization question 2
Screen 5: Notification permission + start
```

**Variant C: 7-Screen Flow**
```
Screen 1: Welcome + value prop
Screen 2: How it works (3-step explainer)
Screen 3: Goal selection
Screen 4: Personalization 1
Screen 5: Personalization 2
Screen 6: Personalization 3
Screen 7: Notifications + start
```

**Metrics:**
- Completion rate
- Day 7 retention
- Feature adoption

---

### Test 2: Skip Option

**Hypothesis:** Skip option reduces frustration without hurting personalization.

**Variant A: No Skip**
```
Must complete all screens
Progress indicator (1/5, 2/5...)
```

**Variant B: Skip Available**
```
"Skip" text button top right
Still shows progress
```

**Variant C: Skip with Warning**
```
"Skip" available
Tapping shows: "Personalization helps us serve you better. Skip anyway?"
```

---

## First Action Tests

### Test 3: What Comes First

**Hypothesis:** Quick win before account creation increases completion.

**Variant A: Account First**
```
1. Sign up / Create account
2. Verify email
3. Set preferences
4. Use app
```

**Variant B: Value First**
```
1. Complete one action (generate content, log workout, etc.)
2. See result
3. "Save your progress - create account"
4. Sign up
```

**Variant C: Tour First**
```
1. Interactive feature tour
2. Guided first action
3. "Keep your data - create account"
4. Sign up
```

---

### Test 4: Guided vs Self-Directed

**Hypothesis:** Guided experience improves activation for complex apps.

**Variant A: Self-Directed**
```
After onboarding: Drop user into main app
No tooltips or guidance
```

**Variant B: Tooltip Guidance**
```
After onboarding: Main app with contextual tooltips
"Tap here to create your first post"
Dismiss individually
```

**Variant C: Step-by-Step Guide**
```
After onboarding: Mandatory first task
"Let's create your first post together"
Hand-hold through complete flow
```

---

## Personalization Tests

### Test 5: Personalization Depth

**Hypothesis:** More personalization improves retention despite longer onboarding.

**Variant A: No Personalization**
```
Generic experience for all users
Skip straight to app
```

**Variant B: Light Personalization (2 questions)**
```
1. What's your main goal?
2. How experienced are you?
```

**Variant C: Deep Personalization (5 questions)**
```
1. What's your main goal?
2. How experienced are you?
3. How much time do you have?
4. What's your biggest challenge?
5. What have you tried before?
```

---

### Test 6: Personalization Type

**Hypothesis:** Visual selection converts better than text input.

**Variant A: Multiple Choice**
```
What's your goal?
○ Lose weight
○ Build muscle
○ Get healthier
○ Train for event
```

**Variant B: Visual Cards**
```
What's your goal?
[Image Card: Weight Loss]
[Image Card: Muscle]
[Image Card: Health]
[Image Card: Athletics]
```

**Variant C: Slider/Scale**
```
What's your experience level?
[Beginner] ----○---- [Expert]
```

---

## Permission Request Tests

### Test 7: Notification Permission Timing

**Hypothesis:** Asking after value moment increases opt-in rate.

**Variant A: During Onboarding**
```
Screen 4 of 5: "Turn on notifications"
Explain benefits
System prompt
```

**Variant B: After First Value**
```
User completes first action
"Get notified when [relevant trigger]"
Contextual ask
```

**Variant C: After 3 Uses**
```
Wait until 3rd session
"You've used the app 3 times!"
"Want reminders to keep your streak?"
```

---

### Test 8: Permission Explanation

**Hypothesis:** Specific benefits increase opt-in rate.

**Variant A: Generic**
```
"Enable notifications"
[Allow] [Not Now]
```

**Variant B: Benefit-Focused**
```
"Get reminded to [core action]"
"Members with notifications are 3x more likely to reach their goals"
[Enable Reminders] [Skip]
```

**Variant C: Control-Focused**
```
"Choose your notifications:"
☐ Daily reminders (10am)
☐ Weekly progress reports
☐ Tips and motivation
[Save Preferences] [Skip All]
```

---

## Progress Indicator Tests

### Test 9: Progress Display Type

**Hypothesis:** Progress indicators reduce abandonment.

**Variant A: No Indicator**
```
No visual progress
Users don't know how many screens remain
```

**Variant B: Step Counter**
```
"Step 2 of 5"
Text-based progress
```

**Variant C: Progress Bar**
```
[████████░░░░░░░░░░░░] 40%
Visual progress bar
```

**Variant D: Dots**
```
● ● ○ ○ ○
Dot indicator
```

---

### Test 10: Progress Psychology

**Hypothesis:** Starting with progress increases completion.

**Variant A: Start at 0%**
```
[░░░░░░░░░░░░░░░░░░░░] 0%
"Let's get started!"
```

**Variant B: Start at 20%**
```
[████░░░░░░░░░░░░░░░░] 20%
"You're already on your way!"
(First screen counts as 20%)
```

**Variant C: Reverse Count**
```
"Only 4 steps to go!"
Countdown instead of progress
```

---

## App-Specific Onboarding Flows

### Dating App (HeartSync)

**Flow A: Photo-First**
```
1. Welcome to HeartSync
2. Add your best photo (required)
3. Write a short bio
4. Set your preferences (age, distance)
5. Start matching!
```

**Flow B: Preferences-First**
```
1. Welcome to HeartSync
2. Who are you looking for? (preferences)
3. What are you looking for? (relationship type)
4. Now let's set up your profile
5. Add photos + bio
```

**Flow C: Quick Start**
```
1. Welcome to HeartSync
2. Add one photo
3. Start swiping immediately
4. "Complete your profile to get more matches" (prompt later)
```

---

### Fitness App (FitTracker)

**Flow A: Goal-Focused**
```
1. What's your fitness goal?
   - Lose weight
   - Build muscle
   - Get fit
   - Train for event
2. Current fitness level (beginner/intermediate/advanced)
3. How many days/week can you work out?
4. Any equipment available?
5. Here's your personalized plan!
```

**Flow B: Quick Win**
```
1. Let's do a quick workout together (5 min guided)
2. "Great job! Want to see your personalized plan?"
3. Set your goal
4. Create account to save progress
```

**Flow C: Assessment**
```
1. Let's see where you're starting
2. Quick fitness test (push-ups, squats)
3. Enter your results
4. "Based on your assessment, here's your plan"
5. Set reminders
```

---

### AI/Productivity App (AIWriter)

**Flow A: Template Showcase**
```
1. Welcome to AIWriter
2. What will you create most?
   - Blog posts
   - Social media
   - Emails
   - Code docs
3. Show relevant templates
4. "Try generating your first [selected type]"
5. Account creation (to save)
```

**Flow B: Instant Demo**
```
1. Welcome - watch this magic
2. [Pre-filled example generates automatically]
3. "Impressed? Now try your own"
4. User generates first content
5. Account creation (to access more)
```

**Flow C: Use Case Deep Dive**
```
1. What's your role?
   - Marketer
   - Writer
   - Developer
   - Business owner
2. Show role-specific features
3. Guided first generation
4. "Unlock all templates with Pro"
```

---

## Implementation Checklist

### For Each Flow Variant:
- [ ] Screen designs completed
- [ ] Copy written and reviewed
- [ ] Animations/transitions defined
- [ ] Analytics events mapped
- [ ] A/B test configured
- [ ] QA on all device sizes
- [ ] Accessibility checked
- [ ] Loading states handled
- [ ] Error states handled

### Analytics Events to Track:
```
onboarding_started
onboarding_screen_viewed (screen_number, screen_name)
onboarding_screen_completed
onboarding_skipped (screen_number)
onboarding_completed
onboarding_abandoned (last_screen)
permission_prompted (type)
permission_granted (type)
permission_denied (type)
first_action_completed
```

---

## Measurement Framework

### Primary Metrics
- **Completion rate:** % who finish onboarding
- **Day 1 retention:** % who return next day
- **Day 7 retention:** % who return after 7 days
- **Activation rate:** % who complete core action

### Secondary Metrics
- Time to complete onboarding
- Screens where users drop off
- Permission opt-in rates
- Feature adoption rate (day 7)

### Segment Analysis
- New installs vs reinstalls
- Organic vs paid users
- iOS vs Android
- Age/demographic groups

---

## Quick Wins to Test First

### Highest Impact Tests:
1. **Onboarding length** (3 vs 5 vs 7 screens)
2. **Value-first vs account-first**
3. **Notification permission timing**

### Quick Implementations:
1. Add skip button (if not present)
2. Add progress indicator (if not present)
3. Move account creation after first value

### Common Mistakes to Avoid:
- Asking for too much info upfront
- Forcing account creation before value
- No progress indication
- Permission asks without context
- Generic welcome screens

---

*Remember: Onboarding sets the tone for the entire user journey. Test aggressively here.*
