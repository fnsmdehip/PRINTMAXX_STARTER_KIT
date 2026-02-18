# DailyAnchor Onboarding Flow

**App:** DailyAnchor
**Screens:** 5
**Goal:** Select habits, set reminder time, start trial, complete first habit
**Target conversion:** Trial start > 70%

---

## Screen 1: Habits Selection

**Screen name:** habits_selection
**Progress:** 1/5

### Copy

**Headline:** What habits do you want to build?

**Body:** Pick 2-3 to start. You can add more later. Small starts lead to lasting change.

### Options

| Habit | Icon | Default | Premium |
|-------|------|---------|---------|
| Read Bible | Book | Yes (selected) | No |
| Pray | Hands | Yes (selected) | No |
| Gratitude | Heart | Yes (selected) | No |
| Meditation | Lotus | No | Yes |
| Fasting | Plate | No | Yes |
| Scripture memory | Brain | No | Yes |
| Church attendance | Church | No | Yes |
| Serving others | Hands helping | No | Yes |

### Free tier limit

**Note:** Free users can select up to 3 habits. Premium badge on locked habits.

### Image/Animation spec

Clean checkbox cards. Icons for each habit. Premium habits have subtle lock indicator. Warm, calming color palette (golds, soft blues).

### CTA

**Button text:** Continue
**Skip option:** No

---

## Screen 2: Reminder Time

**Screen name:** reminder_time
**Progress:** 2/5

### Copy

**Headline:** When's your best time?

**Body:** Morning works for most people. We'll send a gentle reminder to help you stay consistent.

**Stat:** Users who set reminders are 3x more likely to build the habit.

### Options

Time picker wheel. Default: 7:00 AM

Quick presets:
- Early riser (5:30 AM)
- Morning (7:00 AM)
- Mid-day (12:00 PM)
- Evening (8:00 PM)
- Custom

### Image/Animation spec

Soft sunrise/sunset gradient based on time selected. Bell icon with gentle animation.

### CTA

**Button text:** Set reminder
**Skip option:** Yes (small text "I'll remember on my own")

---

## Screen 3: Trial

**Screen name:** paywall_trial
**Progress:** 3/5

### Copy

**Headline:** Start your 7-day free trial

**Body:**
Build your faith habits with full access. Cancel anytime before the trial ends.

**Price display:**
- 7 days free
- Then $9.99/month or $49.99/year (save 58%)

**Social proof:**
"I've prayed every morning for 47 days straight. This app made it stick." - Rebecca M.

### Free vs Premium

| Feature | Free | Premium |
|---------|------|---------|
| 3 core habits | Yes | Yes |
| Daily Bible verse | Yes | Yes |
| Streak tracking | Yes | Yes |
| 5+ additional habits | No | Yes |
| Reading plans | No | Yes |
| Advanced stats | No | Yes |
| Cloud backup | No | Yes |

### Image/Animation spec

Soft gradient background. Dove or cross icon. Warm, inviting aesthetic.

### CTA

**Primary button:** Start free trial
**Secondary button:** Continue with free
**Tertiary:** Restore purchase (small text link)
**Skip option:** Yes (Continue with free)

---

## Screen 4: First Habit

**Screen name:** first_habit_prompt
**Progress:** 4/5

### Copy

**Headline:** Let's start right now

**Body:** Your first [selected habit] takes less than 2 minutes. Ready?

**Dynamic based on first selected habit:**

If Bible reading:
"Today's verse is waiting. It's 2 sentences. Takes 30 seconds to read."

If Prayer:
"A simple prayer: 'God, help me be present today.' That counts."

If Gratitude:
"Think of 1 thing you're thankful for. Just one."

### Image/Animation spec

Focused on the single habit. Minimal distractions. Large, inviting action area.

### CTA

**Primary button:** Do it now
**Secondary:** I'll start tomorrow (goes to home screen)
**Skip option:** Yes (I'll start tomorrow)

---

## Screen 5: Success Confirmation

**Screen name:** first_completion
**Progress:** 5/5

### Copy

**Headline:** Day 1 complete

**Body:** That's it. You just started your [X]-day streak. Come back tomorrow to keep it going.

**Dynamic elements:**
- Streak counter: 1 day
- Next reminder: [time set]
- Today's progress: 1/[total habits] complete

**Motivational close:**
"Consistency beats intensity. See you tomorrow."

### Image/Animation spec

Gentle celebration. Confetti or soft light rays. Not over the top. Badge showing "1 day" streak.

### CTA

**Button text:** Go to home
**Skip option:** No

---

## A/B Test Variations

### Screen 1: Habits Selection (Variant B - Guided approach)

**Headline:** Start with 1 habit

**Body:** Most people fail by trying too much. Pick your most important habit. You can add more after 7 days.

**Options:** Same list, but single-select. After selection, asks "Want to add one more?" (optional)

**Hypothesis:** Forcing fewer habits may increase long-term retention by reducing overwhelm.

---

### Screen 3: Trial (Variant B - Commitment device)

**Headline:** Make a commitment to your faith

**Body:**
This isn't an app. It's accountability.

7 days free. Then $49.99/year.

That's $0.96/week to build habits that last a lifetime.

**Hypothesis:** Framing as commitment vs product may increase perceived value for faith users.

---

### Screen 3: Trial (Variant C - Social proof heavy)

**Headline:** Join 25,000 Christians building daily habits

**Body:**
- Average streak: 12 days
- Most completed habit: Bible reading
- 89% say it improved their consistency

**Testimonials (rotating):**
"Finally, an app that doesn't feel like work." - James T.
"My morning routine changed completely." - Sarah L.

**Hypothesis:** Community/social proof may be particularly effective for faith community.

---

### Screen 4: First Habit (Variant B - Verse first)

**Headline:** Here's today's verse

**Body:**
[Display actual verse from bible-api.com]

Read it. That's your first habit done.

**CTA:** Mark as read

**Hypothesis:** Showing actual content may increase immediate completion rate.

---

## Technical Notes

### Permissions requested
- Notification permission (Screen 2, optional but encouraged)

### Data stored locally
- selected_habits: array[string]
- reminder_time: string (HH:MM)
- reminder_enabled: boolean
- is_premium: boolean
- trial_start_date: timestamp (if applicable)
- onboarding_completed: boolean
- first_habit_completed: boolean

### Analytics events
- onboarding_started
- habits_selected (with array, count)
- reminder_set (with time) / reminder_skipped
- paywall_shown
- trial_started / free_selected
- first_habit_started
- first_habit_completed
- onboarding_completed
