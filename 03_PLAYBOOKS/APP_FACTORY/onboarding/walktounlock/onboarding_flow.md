# WalkToUnlock Onboarding Flow

**App:** WalkToUnlock
**Screens:** 6
**Goal:** Connect health data, set step goal, select blocked apps, start trial
**Target conversion:** Trial start > 80%

---

## Screen 1: Health Permission

**Screen name:** health_permission
**Progress:** 1/6

### Copy

**Headline:** Connect your step data

**Body:** WalkToUnlock reads your steps from Apple Health (or Google Fit). We only read step count. Nothing else.

**Privacy note:** Your health data stays on your device. We never upload it.

### Image/Animation spec

Shield icon with heart rate line. Clean, trustworthy design. Apple Health / Google Fit logo shown.

### CTA

**Primary button:** Connect Health
**Skip option:** No (required for app to function)

### Error state

If permission denied:
**Headline:** We need step access to work
**Body:** WalkToUnlock counts your steps to unlock your apps. Without this, the app can't function. Open Settings to enable.
**Button:** Open Settings

---

## Screen 2: Step Goal

**Screen name:** step_goal
**Progress:** 2/6

### Copy

**Headline:** How many steps before you unlock?

**Body:** Your apps stay locked until you hit this number. The average person walks 3,000-4,000 steps per day.

### Options

| Option | Value | Subtext | Time estimate |
|--------|-------|---------|---------------|
| 3,000 | 3000 | Light | ~30 min walking |
| 5,000 | 5000 | Moderate (most popular) | ~50 min walking |
| 8,000 | 8000 | Active | ~80 min walking |
| 10,000 | 10000 | Very active | ~100 min walking |

Custom slider: 1,000 - 20,000 steps

### Image/Animation spec

Animated step counter incrementing. Shoe/footprint icon. Progress ring showing goal completion.

### CTA

**Button text:** Set my goal
**Skip option:** No

---

## Screen 3: Blocked Apps

**Screen name:** blocked_apps
**Progress:** 3/6

### Copy

**Headline:** Which apps keep you on the couch?

**Body:** These apps stay locked until you hit your step goal. Add more anytime in settings.

### Pre-selected defaults

- Instagram
- TikTok
- Twitter/X
- YouTube
- Netflix
- Reddit

### Display

Grid of app icons with checkboxes. Pre-selected apps highlighted. "Select all social" quick button.

### Image/Animation spec

App icons in grid. Padlock overlay on selected apps. Couch icon with red X (subtle).

### CTA

**Button text:** Lock these apps
**Skip option:** No

---

## Screen 4: Notification

**Screen name:** notification_setup
**Progress:** 4/6

### Copy

**Headline:** Get notified when you unlock

**Body:** We'll send you a message when you hit your step goal. Plus a reminder if you're close but haven't finished by evening.

### Options

Toggle switches:
- Goal reached notification (default: on)
- Evening reminder at 8pm if not complete (default: on)
- Motivational nudges (default: off)

### Image/Animation spec

Phone with notification preview. Celebration confetti on the notification.

### CTA

**Button text:** Enable notifications
**Skip option:** Yes (small text "Maybe later")

---

## Screen 5: Trial

**Screen name:** paywall_trial
**Progress:** 5/6

### Copy

**Headline:** Try WalkToUnlock free for 3 days

**Body:**
Full access. Cancel anytime. No charge if you cancel before the trial ends.

**Price display:**
- 3 days free
- Then $7.99/month or $39.99/year (save 58%)

**Social proof:**
"I went from 2,000 to 7,000 steps per day. My doctor noticed." - James R.

### Features list

- Block unlimited apps until goal hit
- Auto-unlock when steps reached
- Track your walking streak
- Progress charts and stats
- Emergency unlock for real emergencies

### Image/Animation spec

Person walking with phone. Progress ring filling up. Clean, fitness-focused aesthetic.

### CTA

**Primary button:** Start free trial
**Secondary:** Restore purchase (small text link)
**Skip option:** No (hard paywall)

---

## Screen 6: Go

**Screen name:** ready_to_walk
**Progress:** 6/6

### Copy

**Headline:** Time to walk

**Body:** Your apps are now locked. They'll unlock automatically when you hit [X] steps. Today's count: [current steps].

**Subtext:** Already walked today? Your progress counts. Check your current step count.

### Current status display

Progress ring showing current steps vs goal.
Example: "1,247 / 5,000 steps"
"3,753 steps to go"

### Image/Animation spec

Large progress ring. Walking animation. Green checkmark ready to appear when goal hit.

### CTA

**Button text:** Let's go
**Skip option:** No

---

## A/B Test Variations

### Screen 2: Step Goal (Variant B - Social proof)

**Headline:** Most users start with 5,000 steps

**Body:** That's about 50 minutes of walking. You can adjust this anytime. Start achievable, then build up.

**Hypothesis:** Anchoring to "most users" may increase 5,000 selection and reduce drop-off from overwhelm.

---

### Screen 5: Trial (Variant B - Health angle)

**Headline:** Your phone is keeping you sedentary

**Body:**
Average screen time: 4+ hours/day. Average steps: 3,000/day. WalkToUnlock fixes both.

**Price display:**
- 3 days free, then $39.99/year (just $0.77/week)

**Social proof:**
"Lost 8 pounds in 2 months. Didn't change my diet, just walked more." - Michelle K.

**Hypothesis:** Health consequences + per-week pricing may increase conversions.

---

### Screen 5: Trial (Variant C - Simplicity)

**Headline:** Walk more. Scroll less.

**Body:**
That's it. That's the app.

3 days free. Then $39.99/year.

**Hypothesis:** Minimal copy may outperform longer explanations for clarity-seekers.

---

## Technical Notes

### Permissions requested
- HealthKit / Google Fit read access (Screen 1, required)
- Notification permission (Screen 4, optional but encouraged)
- Screen Time / Usage Access (Screen 3, required for blocking)

### Data stored locally
- step_goal: int
- blocked_apps: array[string]
- notifications_enabled: boolean
- evening_reminder: boolean
- trial_start_date: timestamp
- onboarding_completed: boolean

### Health data handling
- Read-only access to step count
- Query daily step total
- Background refresh every 5 minutes
- Cache last known count for offline display

### Analytics events
- onboarding_started
- health_permission_granted / denied
- step_goal_selected (with value)
- apps_selected (with count)
- notifications_enabled (with settings)
- trial_started
- onboarding_completed
