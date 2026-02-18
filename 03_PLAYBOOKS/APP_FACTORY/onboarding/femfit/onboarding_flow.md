# FemFit Onboarding Flow

**App:** FemFit
**Screens:** 6
**Goal:** Set fitness goal, assess level, configure schedule, enable notifications, start trial, begin first workout
**Target conversion:** Trial start > 75%
**Mascot:** Luna the cat

---

## Screen 1: Goal

**Screen name:** fitness_goal
**Progress:** 1/6

### Copy

**Headline:** Hey! What's your goal?

**Luna says:** "I'm Luna, your workout bestie. Tell me what we're working toward."

**Body:** Pick your main focus. We'll suggest exercises that match.

### Options

| Goal | Icon | Description |
|------|------|-------------|
| Build glutes | Peach | Grow and shape your glutes |
| Tone arms | Flexed arm | Sculpt lean, defined arms |
| Get stronger | Dumbbell | Build overall strength |
| General fitness | Heart | Feel better, move more |

### Image/Animation spec

Luna waving animation (Lottie). Soft coral background. Clean card selection UI. Rounded corners, friendly aesthetic.

### CTA

**Button text:** Continue
**Skip option:** No

---

## Screen 2: Fitness Level

**Screen name:** fitness_level
**Progress:** 2/6

### Copy

**Headline:** How long have you been working out?

**Luna says:** "No judgment here. We all start somewhere."

**Body:** This helps us suggest the right intensity.

### Options

| Level | Value | Description |
|-------|-------|-------------|
| New to fitness | beginner | Just getting started or coming back |
| Some experience | intermediate | Work out 1-2x per week |
| Regular gym-goer | advanced | Work out 3+ times per week |
| Experienced lifter | expert | Been training consistently for years |

### Image/Animation spec

Luna with encouraging expression. Progress bar shows levels. Soft, non-intimidating design.

### CTA

**Button text:** Continue
**Skip option:** No

---

## Screen 3: Schedule

**Screen name:** workout_schedule
**Progress:** 3/6

### Copy

**Headline:** How often do you want to train?

**Luna says:** "Consistency matters more than frequency. Pick what's realistic."

**Body:** You can always change this later.

### Options

| Frequency | Value | Luna comment |
|-----------|-------|--------------|
| 2x per week | 2 | "Great start!" |
| 3x per week | 3 | "Nice balance!" |
| 4x per week | 4 | "You've got this!" |
| 5+ per week | 5 | "Motivated!" |

### Day selection (optional)

Toggles for preferred days: M T W T F S S

### Image/Animation spec

Luna with calendar. Weekly view showing selected days. Soft animations on selection.

### CTA

**Button text:** Set my schedule
**Skip option:** Yes (small text "I'll decide later")

---

## Screen 4: Notification

**Screen name:** notification_setup
**Progress:** 4/6

### Copy

**Headline:** Can Luna remind you?

**Luna says:** "I'll send you a little nudge on workout days. No spam, promise."

**Body:** Most users who enable reminders work out 2x more often.

### Options

Toggle: Enable workout reminders (default: on)

Time picker: What time works best?
- Morning (7:00 AM)
- Lunch (12:00 PM)
- After work (6:00 PM)
- Evening (8:00 PM)
- Custom

### Image/Animation spec

Luna holding a small bell. Phone notification preview showing "Time to train with Luna."

### CTA

**Button text:** Enable reminders
**Skip option:** Yes (small text "Not now")

---

## Screen 5: Trial

**Screen name:** paywall_trial
**Progress:** 5/6

### Copy

**Headline:** Train with Luna for 3 days free

**Luna says:** "Let's see if we're a good fit. I'll be here cheering you on."

**Body:**
Full access to FemFit. Cancel anytime before the trial ends.

**Price display:**
- 3 days free
- Then $7.99/week or $59.99/year (save 63%)

**Social proof:**
"Luna makes gym days actually fun. Never thought I'd say that." - Ashley K.

### Features list

- 50+ exercises for women
- Log sets, reps, and weight
- Track progress and PRs
- Luna celebrates your wins
- Streak tracking (gentle, not punishing)

### Luna on paywall

Animation: Luna with pom-poms doing a little cheer.

### Image/Animation spec

Soft coral gradient. Luna prominently featured. Clean pricing cards. "Best value" badge on annual.

### CTA

**Primary button:** Start 3-day free trial
**Secondary:** Restore purchase (small text link)
**Skip option:** No (hard paywall)

---

## Screen 6: First Workout

**Screen name:** first_workout
**Progress:** 6/6

### Copy

**Headline:** Ready for your first workout?

**Luna says:** "I'm so excited! Let's do this together."

**Body:** Start with a quick workout or create your own. Either way, I'll be here.

### Options

**Quick start options:**

| Option | Duration | Exercises |
|--------|----------|-----------|
| Glute Starter | 20 min | Hip thrust, Glute bridge, Squats |
| Upper Body Tone | 25 min | Bicep curl, Tricep pushdown, Shoulder press |
| Full Body Quick | 30 min | Mix of all muscle groups |
| Create my own | - | Build from scratch |

### Image/Animation spec

Luna stretching (cat stretch animation). Workout cards with muscle group icons. Inviting "start" buttons.

### CTA

**Primary button:** Start [selected workout]
**Secondary:** I'll start later (goes to home)
**Skip option:** Yes (I'll start later)

---

## A/B Test Variations

### Screen 1: Goal (Variant B - Body part focus)

**Headline:** What do you want to focus on?

**Luna says:** "Every body is different. Let's work on what matters to you."

**Options:**
- Glutes & legs (lower body sculpting)
- Arms & shoulders (upper body definition)
- Core & abs (strengthen your center)
- Full body (balanced training)

**Hypothesis:** Body-part framing may resonate more than abstract goal language.

---

### Screen 5: Trial (Variant B - Transformation angle)

**Headline:** In 30 days, you'll feel different

**Luna says:** "I've seen it happen. Trust the process."

**Body:**
- Week 1: Learn the moves
- Week 2: Start feeling stronger
- Week 3: Notice the difference
- Week 4: Can't imagine stopping

3 days free. Then $59.99/year.

**Hypothesis:** Timeline framing may increase commitment by setting expectations.

---

### Screen 5: Trial (Variant C - Per-week pricing)

**Headline:** Less than a latte per week

**Luna says:** "Invest in yourself. You're worth it."

**Body:**
$59.99/year = $1.15/week

That's cheaper than one coffee.

**Features:** Same list

**Hypothesis:** Per-week pricing may reduce perceived cost for price-sensitive users.

---

### Screen 6: First Workout (Variant B - Luna leads)

**Headline:** Luna picked your first workout

**Luna says:** "Based on your goal, I think you'll love this one."

**Body:**
[Auto-selected based on Screen 1 goal]

Example for glute goal:
- Hip Thrust (3 sets)
- Glute Bridge (3 sets)
- Bulgarian Split Squat (3 sets)
- Cable Kickback (3 sets)

Estimated time: 25 minutes

**CTA:** Let's go

**Hypothesis:** Removing choice may reduce friction and increase first-workout completion.

---

## Luna Messages Throughout Onboarding

| Screen | Luna Message |
|--------|--------------|
| Goal | "I'm Luna, your workout bestie. Tell me what we're working toward." |
| Level | "No judgment here. We all start somewhere." |
| Schedule | "Consistency matters more than frequency. Pick what's realistic." |
| Notification | "I'll send you a little nudge on workout days. No spam, promise." |
| Trial | "Let's see if we're a good fit. I'll be here cheering you on." |
| First workout | "I'm so excited! Let's do this together." |

---

## Technical Notes

### Permissions requested
- Notification permission (Screen 4, optional but encouraged)

### Data stored locally
- fitness_goal: string
- fitness_level: string
- workout_frequency: int
- preferred_days: array[string]
- reminder_enabled: boolean
- reminder_time: string (HH:MM)
- trial_start_date: timestamp
- onboarding_completed: boolean
- first_workout_started: boolean
- luna_enabled: boolean (default: true)

### Analytics events
- onboarding_started
- goal_selected (with value)
- level_selected (with value)
- schedule_set (with frequency, days)
- notifications_enabled / skipped
- trial_started
- first_workout_selected (with workout name)
- first_workout_started
- first_workout_completed
- onboarding_completed
