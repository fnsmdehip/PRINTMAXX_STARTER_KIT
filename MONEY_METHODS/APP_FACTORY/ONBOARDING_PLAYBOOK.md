# Onboarding Playbook: Best-Practice Flows for Every PRINTMAXX App

**Date:** 2026-02-10
**Purpose:** Exact screen-by-screen onboarding flows for each app in our portfolio. Based on patterns from 24 top apps audited, RevenueCat benchmarks, and ScreensDesign teardowns.
**How to use:** When building any app, follow its section below screen-by-screen. Every screen described with purpose, copy, and conversion intent.

---

## Universal Onboarding Principles (Apply to ALL Apps)

### The 4 Rules

1. **3-5 screens max before value.** RevenueCat data: 82% of trials start on Day 0. Get users to value fast, then paywall.
2. **Every screen must earn the next tap.** If a screen doesn't collect essential data or deliver value, cut it.
3. **Show value BEFORE paywall.** The highest-converting apps (ShutEye, Forest, Rise) give users a taste before asking for money.
4. **Personalize the paywall.** Echo the user's onboarding answers on the paywall screen. "Based on your goal to..." converts 65% better than generic paywalls.

### The Universal Screen Framework

```
Screen 1: Welcome + Permission/Context
Screen 2: Goal Selection (personalization)
Screen 3: Value Moment (let user DO something)
Screen 4: Paywall (personalized, with trial)
Screen 5: Dashboard (if paywall dismissed/accepted)
```

### Permission Request Timing

| Permission | When to Ask | Why |
|-----------|-------------|-----|
| Location | Screen 1 (faith apps) or never | Prayer times need it |
| Notifications | After value moment, before paywall | User understands what they'll get notified about |
| Health/Motion | During relevant feature setup | Context makes it feel natural |
| Camera | Only when user triggers a camera feature | Never preemptively |

### Paywall Design Spec (All Apps)

Every app paywall should include:
- Personalization echo ("Based on your goal to...")
- 7-day free trial (or 3-day for hard paywalls)
- Two options: Annual (pre-selected, show monthly equivalent) + Monthly
- Visual timeline showing trial period and billing date
- "Cancel anytime" text
- Subtle animation on feature list
- Skip/close button (soft paywall) or "Restore purchases" link

**Pricing structure for all apps:**
- Monthly: $3.99-4.99
- Annual: $24.99-29.99 (show "Save 50%")
- Lifetime: $49.99 (optional, reduces subscription anxiety)

---

## Dusk (Sleep Tracker)

**Category:** Health & Fitness > Sleep
**Competitors studied:** Sleep Cycle, Rise, ShutEye, Pillow, SleepScore
**Onboarding model:** Quiz-to-Diagnosis (like Rise)
**Target conversion:** 12%+ download-to-trial

### Screen 1: Welcome
**Purpose:** Set context, request essential permission
**Visual:** Dark background with sunset-to-night gradient. Moon/stars subtle animation.
**Copy:**
- Headline: "Better sleep starts with understanding"
- Subtext: "Track your sleep patterns and build a bedtime routine that works"
- CTA: "Get Started"
**Data collected:** None
**Permission:** None yet

### Screen 2: Sleep Challenge
**Purpose:** Identify user's primary pain point, personalize experience
**Visual:** Dark background. Large tappable cards with icons.
**Copy:**
- Headline: "What's your biggest sleep challenge?"
- Options (single select):
  - "Falling asleep" (moon icon)
  - "Staying asleep" (broken circle icon)
  - "Waking up tired" (low battery icon)
  - "Inconsistent schedule" (clock icon)
  - "Just curious about my sleep" (chart icon)
**Data collected:** `sleepChallenge` (stored locally)

### Screen 3: Sleep Schedule
**Purpose:** Collect baseline data for personalization
**Visual:** Two time pickers on dark background
**Copy:**
- Headline: "Your current sleep schedule"
- "What time do you usually go to bed?" [Time picker, default 11:00 PM]
- "What time do you wake up?" [Time picker, default 7:00 AM]
- Auto-calculated: "That's about 8 hours of sleep"
**Data collected:** `bedtime`, `wakeTime`, `sleepDuration`

### Screen 4: Value Moment (Sleep Score Preview)
**Purpose:** Show immediate value. Demonstrate the product.
**Visual:** Large sleep quality score (calculated from inputs) with circular progress ring. Gradient fill.
**Copy:**
- Headline: "Your estimated sleep quality"
- Large number: "72" (or calculated from inputs)
- Subtext: "Based on your schedule and challenges, there's room to improve"
- Below: 3 quick tips based on their challenge selection
  - If "falling asleep": "Try dimming screens 1 hour before bed"
  - If "waking tired": "Your wake time may not align with your sleep cycles"
**Data collected:** None (display only)
**Key moment:** This is the "aha" -- user sees their sleep analyzed before paying anything

### Screen 5: Notification Permission
**Purpose:** Get notification permission with context
**Visual:** Phone mockup showing a notification: "Time to start your bedtime routine"
**Copy:**
- Headline: "Never miss your sleep window"
- Subtext: "We'll remind you when it's time to wind down based on your schedule"
- CTA: "Enable Reminders" (triggers system permission)
- Skip: "Not now" (small text)

### Screen 6: Paywall
**Purpose:** Convert to trial
**Visual:** Dark gradient. Feature list with subtle check-mark animations.
**Copy:**
- Headline: "Your sleep improvement plan is ready" (personalized)
- Subtext: "Based on your goal to [fix falling asleep / stop waking tired / etc.]"
- Features:
  - Detailed sleep stage tracking
  - Bedtime routine builder
  - Smart alarm (wake in lightest sleep phase)
  - Sleep environment tips
  - Weekly sleep insights
- Trial timeline: "Try free for 7 days > Billed $29.99/year on [date]"
- Options: Annual $29.99/year (pre-selected, "Just $2.49/month") | Monthly $3.99/month
- CTA: "Start Free Trial"
- Skip: "Maybe later" (small, bottom)

---

## Vault (Focus/Pomodoro Timer)

**Category:** Productivity > Focus
**Competitors studied:** Forest, Session, Opal, Be Focused, Focus Bear
**Onboarding model:** Value-First (like Forest)
**Target conversion:** 10%+ download-to-trial

### Screen 1: Welcome
**Purpose:** Communicate core concept instantly
**Visual:** Clean dark background. Minimalist timer "25:00" centered. Subtle pulsing glow.
**Copy:**
- Headline: "Focus. Build. Ship."
- Subtext: "Block distractions and get deep work done"
- CTA: "Start Focusing"

### Screen 2: First Focus Session (Value Moment)
**Purpose:** Get user to DO the core action immediately. Speed to first value = seconds.
**Visual:** Full-screen timer. Tree/progress animation starts growing. Background ambient sound plays softly.
**Copy:**
- Headline: "Try a quick 5-minute focus session"
- Timer: "5:00" countdown, large and centered
- Subtext: "Put your phone down. We'll let you know when time's up."
- CTA: "Start" (large, centered button)
**Key moment:** User experiences the product. A growing animation (tree, crystal, orb) provides visual feedback. Ambient sound creates atmosphere. This is the hook.

### Screen 3: Session Complete Celebration
**Purpose:** Reward completion, create positive association
**Visual:** Completion animation (confetti, or the grown tree/crystal). Satisfying haptic feedback.
**Copy:**
- Headline: "5 minutes of deep focus. Done."
- Stats: "You stayed focused for 5:00"
- Subtext: "Imagine doing this for 25 minutes, 4 times a day"
- CTA: "Set Up Your Focus Sessions"

### Screen 4: Preferences
**Purpose:** Customize the experience
**Visual:** Large tappable options
**Copy:**
- "Default focus duration?" [15 min / 25 min / 45 min / Custom]
- "Block distracting apps during focus?" [Yes / No]
- "Play ambient sounds?" [Yes / No]
**Data collected:** `focusDuration`, `blockApps`, `ambientSounds`

### Screen 5: Notification + Paywall
**Purpose:** Permission request + conversion
**Visual:** Split screen. Top: notification mockup. Bottom: feature comparison.
**Copy:**
- "Enable focus reminders?" [Enable / Skip]
- Then transitions to paywall:
- Headline: "Unlock your full focus toolkit"
- Free: Timer, basic sounds, 2 sessions/day tracked
- Premium: App blocking, all ambient sounds, unlimited sessions, insights, widget
- Trial: "7 days free, then $24.99/year"
- CTA: "Start Free Trial"
- Skip: "Continue with free"

---

## Streakr (Habit Tracker)

**Category:** Productivity > Habits
**Competitors studied:** Streaks, Habitify, Productive, Done, Finch, Habitica
**Onboarding model:** Emotional Investment (like Finch/Habitica hybrid)
**Target conversion:** 10%+ download-to-trial

### Screen 1: Welcome
**Purpose:** Hook with the core promise
**Visual:** Light background with colorful habit ring visualizations. Confetti particles.
**Copy:**
- Headline: "Don't break the streak"
- Subtext: "Build habits that stick with visual streaks and celebrations"
- CTA: "Build My First Habit"

### Screen 2: Area Selection
**Purpose:** Personalize and create investment
**Visual:** Large emoji-topped cards
**Copy:**
- Headline: "What area do you want to improve?"
- Options (multi-select allowed):
  - Health (heart emoji) -- exercise, water, sleep
  - Mindfulness (brain emoji) -- meditate, journal, gratitude
  - Productivity (rocket emoji) -- reading, study, deep work
  - Self-Care (sparkle emoji) -- skincare, stretching, screen time
  - Custom (pencil emoji) -- create your own
**Data collected:** `areas` array

### Screen 3: Habit Pack Selection
**Purpose:** Pre-populate habits so user has instant content
**Visual:** Curated habit cards based on selected areas
**Copy:**
- Headline: "Starter habits for you"
- Shows 3-5 habits based on area selection, each with:
  - Habit name, emoji icon, suggested frequency
  - Toggle to include/exclude
- Subtext: "You can always add more later"
- CTA: "Add These Habits"
**Key moment:** User now has 3-5 habits set up. They've invested in building their plan.

### Screen 4: Complete Your First Habit (Value Moment)
**Purpose:** Dopamine hit. The celebration IS the product demo.
**Visual:** One of their selected habits shown with a large tap-to-complete button
**Copy:**
- Headline: "Complete your first habit right now"
- Large circle button: Tap to complete
- On tap: Ring fills, confetti animation, haptic feedback, streak counter shows "1"
- After completion: "Day 1 of your streak. Don't let it break."
**Key moment:** The celebration animation must be genuinely satisfying. This is what brings users back.

### Screen 5: Notification Permission
**Purpose:** Contextual permission request
**Visual:** Phone showing a reminder notification for their first habit
**Copy:**
- "Want a daily reminder to keep your streak alive?"
- CTA: "Enable Reminders" | "Not now"

### Screen 6: Paywall
**Purpose:** Convert with invested user
**Visual:** Light background, habit rings preview, streak calendar heatmap
**Copy:**
- Headline: "You've already started. Keep going."
- Subtext: "Your [3] habits are set up and ready"
- Free: 3 habits, basic stats
- Premium: Unlimited habits, detailed analytics, streak protection (miss 1 day without breaking), themes, export
- Trial: "7 days free, then $24.99/year (just $2.08/month)"
- CTA: "Start Free Trial"
- Skip: "Continue with 3 habits"

---

## Mise (Meal Planner)

**Category:** Health & Fitness > Nutrition
**Competitors studied:** MyFitnessPal, Noom, Cal AI, Mealime, Paprika
**Onboarding model:** Quiz-to-Plan (like Noom, shorter)
**Target conversion:** 12%+ download-to-trial

### Screen 1: Welcome
**Purpose:** Differentiate from calorie counters
**Visual:** Clean, light background. Food photography (meal prep containers, colorful meals).
**Copy:**
- Headline: "Plan meals. Not calories."
- Subtext: "Weekly meal plans, smart shopping lists, and zero food waste"
- CTA: "Plan My Week"

### Screen 2: Dietary Preferences
**Purpose:** Personalize meal suggestions
**Visual:** Large tappable dietary cards
**Copy:**
- Headline: "Any dietary preferences?"
- Options (multi-select):
  - No restrictions
  - Vegetarian
  - Vegan
  - Gluten-free
  - Dairy-free
  - Halal
  - Keto
  - Paleo
**Data collected:** `dietaryPreferences` array

### Screen 3: Household Size + Cooking Skill
**Purpose:** Size portions and complexity
**Visual:** Simple selectors
**Copy:**
- "Cooking for how many?" [1 / 2 / 3-4 / 5+]
- "Your cooking level?" [Beginner / Intermediate / Chef mode]
- "Max time per meal?" [15 min / 30 min / 45 min / No limit]
**Data collected:** `householdSize`, `cookingLevel`, `maxCookTime`

### Screen 4: Value Moment (Your Week Preview)
**Purpose:** Show personalized meal plan before paywall
**Visual:** Weekly calendar with meal cards (breakfast, lunch, dinner). Each shows a recipe photo, cook time, and servings.
**Copy:**
- Headline: "Your meal plan for this week"
- 7-day view with 2-3 meals per day populated
- Subtext: "Tap any meal to see the recipe"
- Let user tap ONE recipe and see ingredients (free preview)
**Key moment:** Seeing a full week planned for you feels like instant value. The "calculating..." animation while generating the plan builds anticipation.

### Screen 5: Paywall
**Purpose:** Convert with invested user who just saw their plan
**Visual:** Meal plan preview blurred behind paywall
**Copy:**
- Headline: "Your personalized meal plan is ready"
- Features:
  - Unlimited weekly meal plans
  - Smart shopping list (auto-generated)
  - Leftover management (reduce food waste)
  - Recipe import (paste any URL)
  - Nutritional info per meal
  - Offline recipe access
- Trial: "7 days free, then $29.99/year"
- CTA: "Start Free Trial"
- Skip: "Browse free recipes" (limited library)

---

## Steplock (Walk Tracker)

**Category:** Health & Fitness > Fitness
**Competitors studied:** Strava, Apple Fitness, Pedometer++, Forest (gamification), Pokémon Go (walking game)
**Onboarding model:** Value-First with gamification (like Forest)
**Target conversion:** 10%+ download-to-trial

### Screen 1: Welcome
**Purpose:** Communicate the unique lock mechanic
**Visual:** Sunrise gradient background. Phone with a lock icon that transforms into footsteps.
**Copy:**
- Headline: "Walk to unlock"
- Subtext: "Lock your favorite apps until you hit your step goal. No cheating."
- CTA: "Set My Step Goal"

### Screen 2: Step Goal
**Purpose:** Set the core mechanic
**Visual:** Large step counter with slider
**Copy:**
- Headline: "Your daily step goal"
- Slider: 1,000 to 20,000 steps (default 5,000)
- Below slider: Contextual info based on selection:
  - 5,000: "A good starting point. About 30 minutes of walking."
  - 8,000: "The sweet spot. Linked to lower risk of heart disease."
  - 10,000: "The classic target. About 60-90 minutes of walking."
- CTA: "Set Goal"
**Data collected:** `dailyStepGoal`

### Screen 3: App Lock Selection
**Purpose:** Set up the gamification mechanic
**Visual:** Grid of app icons
**Copy:**
- Headline: "Which apps to lock until you walk?"
- Show installed apps (social media, games highlighted)
- Subtext: "These apps will be locked until you hit your daily steps"
- Suggested: Instagram, TikTok, X, YouTube, games
- CTA: "Lock These Apps"
**Data collected:** `lockedApps` array
**Permission:** Screen Time API / accessibility permission

### Screen 4: Health Permission + Value Moment
**Purpose:** Get HealthKit access, show immediate step count
**Visual:** Step counter showing current steps from HealthKit
**Copy:**
- "Connect to Apple Health to track your steps automatically"
- After permission: Shows today's step count
- Large number: "2,341 steps so far today"
- Progress bar toward goal
- Subtext: "[2,659] more steps to unlock your apps"
**Key moment:** Seeing real-time progress toward unlocking creates immediate engagement

### Screen 5: Paywall
**Purpose:** Convert
**Visual:** Step progress visualization, locked/unlocked app icons
**Copy:**
- Headline: "Ready to walk more?"
- Free: 1 locked app, basic step tracking
- Premium: Unlimited app locks, step streaks, distance tracking, route maps, challenges, widget
- Trial: "7 days free, then $24.99/year"
- CTA: "Start Free Trial"
- Skip: "Start with free"

---

## Hilal (Ramadan Tracker)

**Category:** Lifestyle > Faith/Ramadan
**Competitors studied:** Muslim Pro, Athan Pro, Fastic, SAUM, FastTrekker
**Onboarding model:** Quick Setup + Seasonal Value (like Athan)
**Target conversion:** 15%+ download-to-trial (high-intent seasonal audience)

**CRITICAL TIMING:** Ramadan 2026 starts around February 28. Launch MUST happen before February 20 to capture early adopters preparing for Ramadan.

### Screen 1: Welcome
**Purpose:** Seasonal greeting, set context
**Visual:** Deep green + gold gradient. Crescent moon and stars animation. Islamic geometric patterns as subtle background.
**Copy:**
- Headline: "Ramadan Mubarak"
- Subtext: "Your complete Ramadan companion: fasting timer, Quran tracker, dua library, and charity counter"
- CTA: "Set Up My Ramadan"

### Screen 2: Location + Calculation Method
**Purpose:** Essential for accurate prayer/fasting times
**Visual:** Qibla compass animation
**Copy:**
- "Allow location for accurate fasting times" [Allow / Enter manually]
- "Calculation method:" [Dropdown: ISNA, MWL, Egyptian, Karachi, etc.]
- "Madhab:" [Hanafi / Shafi'i]
**Data collected:** `location`, `calcMethod`, `madhab`
**Permission:** Location

### Screen 3: Ramadan Goals
**Purpose:** Personalize the experience
**Visual:** Goal cards with Islamic motifs
**Copy:**
- Headline: "Your Ramadan goals this year"
- Options (multi-select):
  - Complete the entire Quran (30 juz)
  - Pray all 5 salah on time
  - Make dua daily
  - Give charity regularly
  - Improve sleep schedule for tahajjud
  - Reduce screen time
- CTA: "Set My Goals"
**Data collected:** `ramadanGoals` array

### Screen 4: Value Moment (Today's Schedule)
**Purpose:** Show immediate value with today's fasting times
**Visual:** Beautiful fasting schedule card. Suhoor and Iftar times prominently displayed. Countdown timer to next event.
**Copy:**
- Headline: "Your fasting schedule"
- Large card: "Suhoor ends: 5:23 AM" / "Iftar: 6:47 PM"
- Countdown: "Next: Iftar in 4h 23m"
- Below: Today's prayer times (all 5)
- Quran progress: "Day 1 / 30 -- Juz 1: Al-Fatiha to Al-Baqarah 141"
**Key moment:** Seeing accurate, personalized fasting times with countdown creates immediate utility

### Screen 5: Notification Permission
**Purpose:** Context-rich permission request
**Visual:** Phone mockup showing "Suhoor in 30 minutes -- time to eat"
**Copy:**
- "Get reminded for Suhoor, Iftar, and prayer times?"
- CTA: "Enable Reminders" | "Not now"

### Screen 6: Paywall (Seasonal Urgency)
**Purpose:** Convert with Ramadan urgency
**Visual:** Green + gold theme. Feature comparison.
**Copy:**
- Headline: "Make this your best Ramadan"
- Free: Basic fasting timer, prayer times, limited duas
- Premium: Full Quran tracker with audio, complete dua library, charity tracker, daily reflection journal, Ramadan analytics, no ads
- **Urgency element:** "Ramadan starts in [X] days"
- Trial: "7 days free, then $19.99/year" (lower price point, faith audience is price-sensitive)
- Or: Lifetime $29.99 (strong for seasonal apps -- users don't want to re-subscribe each Ramadan)
- CTA: "Start Free Trial"
- Skip: "Use basic features"

---

## PrayerLock (Prayer Consistency)

**Category:** Lifestyle > Faith
**Competitors studied:** Muslim Pro, Athan Pro (neither gamifies prayer consistency)
**Onboarding model:** Quick Setup (like Athan -- fastest onboarding in faith category)
**Target conversion:** 10%+ download-to-trial

### Screen 1: Welcome
**Purpose:** Communicate unique value (accountability, not just times)
**Visual:** Teal gradient with gold accent. Activity rings showing prayer completion.
**Copy:**
- Headline: "Never miss a prayer"
- Subtext: "Track your salah consistency, build streaks, and stay accountable"
- CTA: "Get Started"

### Screen 2: Location + Calculation
**Purpose:** Essential for prayer times
**Visual:** Qibla direction indicator
**Copy:**
- "Allow location for accurate prayer times" [Allow / Enter manually]
- "Calculation method:" [ISNA / MWL / Egyptian / etc.]
- "Madhab:" [Hanafi / Shafi'i]
**Data collected:** `location`, `calcMethod`, `madhab`
**Permission:** Location

### Screen 3: Prayer Goals
**Purpose:** Set accountability parameters
**Visual:** 5 prayer time cards with toggles
**Copy:**
- Headline: "Which prayers do you want to track?"
- Show all 5 daily prayers with their times:
  - Fajr: 5:23 AM [Toggle ON by default]
  - Dhuhr: 12:15 PM [Toggle ON]
  - Asr: 3:30 PM [Toggle ON]
  - Maghrib: 6:02 PM [Toggle ON]
  - Isha: 7:15 PM [Toggle ON]
- Optional: "Also track Sunnah prayers?" [Toggle]
- Optional: "Also track Tahajjud?" [Toggle]
**Data collected:** `trackedPrayers` array

### Screen 4: Value Moment (Tap to Log)
**Purpose:** First prayer logged = first streak started
**Visual:** Current prayer highlighted with large completion button. Streak counter below.
**Copy:**
- Headline: "Log your most recent prayer"
- Large prayer card with time and "Mark as Prayed" button
- On tap: Ring fills, subtle celebration, streak shows "1"
- "Day 1 of your prayer streak. In sha Allah, many more to come."
**Key moment:** Simple, respectful celebration. No over-the-top confetti (cultural sensitivity). Clean ring completion.

### Screen 5: Notification Permission
**Purpose:** Prayer time reminders (the core utility)
**Visual:** Phone showing "Dhuhr in 10 minutes" notification
**Copy:**
- "Get reminded before each prayer time?"
- "We'll notify you [5/10/15] minutes before each prayer"
- CTA: "Enable Reminders" | "Not now"

### Screen 6: Paywall (Light)
**Purpose:** Convert, but keep faith app accessible
**Visual:** Teal + gold, prayer ring visualization
**Copy:**
- Headline: "Stay consistent in your prayers"
- Free: Prayer times, basic logging, current streak
- Premium: Detailed statistics, streak protection, Qibla compass, dua after each prayer, weekly insights, prayer heatmap, export data
- Trial: "7 days free, then $19.99/year"
- Lifetime: $29.99 (faith users prefer one-time -- no recurring billing anxiety)
- CTA: "Start Free Trial"
- Skip: "Continue with free"

**Note:** Faith apps should prioritize accessibility. The free tier must be genuinely useful. Gate analytics and extras, not core prayer tracking.

---

## When to Show the Paywall: Decision Matrix

| Scenario | Timing | Rationale |
|----------|--------|-----------|
| User completed quiz/goals | End of onboarding | Invested, personalized, highest conversion |
| User completed first action | After first habit/prayer/timer | Experienced value, emotional hook |
| User hit feature limit | Organic during use | Self-selected high-intent user |
| Returning user (Day 2+) | After opening app | Proven interest, not new-user anxiety |
| Seasonal urgency (Ramadan) | During onboarding with countdown | Time pressure drives conversion |

---

## A/B Test Priorities (Run These First)

| Test | Hypothesis | Expected Impact |
|------|-----------|----------------|
| Hard vs soft paywall | Hard paywall converts more downloads but soft paywall retains better | 2-5x difference in conversion |
| 3-day vs 7-day trial | Shorter trials create urgency but risk less attachment | 10-20% conversion difference |
| Annual default vs monthly default | Annual pre-selected reduces monthly churn but may scare new users | 30%+ revenue per user difference |
| Quiz length (5 vs 10 screens) | Longer quiz builds more investment but risks drop-off | 15-25% conversion difference |
| Paywall with vs without animation | Animated feature lists draw attention | 15-30% conversion uplift |
| With vs without lifetime option | Lifetime captures subscription-averse users | 5-10% incremental revenue |

---

## Sources

- [RevenueCat State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025/)
- [Airbridge - Get 100% of Users to Your Paywall](https://www.airbridge.io/blog/subscription-app-onboarding)
- [Dev.to - Complete Onboarding Breakdown: 9 Steps](https://dev.to/paywallpro/complete-onboarding-breakdown-9-steps-from-first-screen-to-paywall-2j7)
- [AppAgent - 5 Paywall Optimization Strategies](https://appagent.com/blog/mobile-app-onboarding-5-paywall-optimization-strategies/)
- [ScreensDesign - Cal AI Showcase](https://screensdesign.com/showcase/cal-ai-calorie-tracker)
- [ScreensDesign - Zero Fasting Showcase](https://screensdesign.com/showcase/zero-fasting-health-tracker)
- [ScreensDesign - Finch Showcase](https://screensdesign.com/showcase/finch-self-care-pet)
- [ScreensDesign - Fabulous Showcase](https://screensdesign.com/showcase/fabulous-daily-habit-tracker)
- [Adapty - iOS Paywall Design Guide](https://adapty.io/blog/how-to-design-ios-paywall/)
- [Apphud - Best Performing Paywalls](https://apphud.com/blog/best-performing-paywallls)
