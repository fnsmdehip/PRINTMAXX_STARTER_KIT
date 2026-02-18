# PrayerLock Onboarding Flow

**App:** PrayerLock
**Screens:** 5
**Goal:** Set prayer commitment, select blocked apps, start trial
**Target conversion:** Trial start > 85%

---

## Screen 1: Prayer Goal

**Screen name:** prayer_goal
**Progress:** 1/5

### Copy

**Headline:** How long do you want to pray each morning?

**Body:** PrayerLock blocks distracting apps until you complete your prayer time. Most users start with 10 minutes.

### Options

| Option | Value | Subtext |
|--------|-------|---------|
| 5 minutes | 5 | Quick start |
| 10 minutes | 10 | Most popular |
| 15 minutes | 15 | Build the habit |
| 20+ minutes | 20 | Deep devotion |

### Image/Animation spec

Minimal illustration of a person in prayer posture. Soft morning light gradient background (warm gold to soft blue). No faces shown.

### CTA

**Button text:** Continue
**Skip option:** No

---

## Screen 2: Notification Time

**Screen name:** notification_time
**Progress:** 2/5

### Copy

**Headline:** When should we remind you?

**Body:** Pick a time before your usual scroll starts. 82% of users who set a reminder complete their prayer goal.

### Options

Time picker wheel. Defaults to 6:30 AM.

Preset buttons:
- 5:30 AM
- 6:00 AM
- 6:30 AM
- 7:00 AM
- Custom

### Image/Animation spec

Clock icon with gentle pulse animation. Sunrise gradient in background.

### CTA

**Button text:** Set reminder
**Skip option:** Yes (small text "Skip for now")

---

## Screen 3: Blocked Apps

**Screen name:** blocked_apps
**Progress:** 3/5

### Copy

**Headline:** What distracts you most?

**Body:** These apps stay locked until you finish praying. You can change this later in settings.

### Pre-selected defaults

- Instagram
- TikTok
- Twitter/X
- Facebook
- YouTube
- Snapchat

### Display

Grid of app icons with checkboxes. Pre-selected apps have blue check. Users can add/remove.

### Image/Animation spec

App icons in a clean grid. Locked padlock icon next to each selected app.

### CTA

**Button text:** Lock these apps
**Skip option:** No

---

## Screen 4: Trial

**Screen name:** paywall_trial
**Progress:** 4/5

### Copy

**Headline:** Start your 3-day free trial

**Body:**
Full access to PrayerLock. Cancel anytime before the trial ends and pay nothing.

**Price display:**
- 3 days free
- Then $9.99/month or $49.99/year (save 58%)

**Social proof:**
"I went from 0 to 15 minutes of daily prayer in 2 weeks." - Sarah M.

### Features list

- Block unlimited apps
- Track your prayer streak
- Daily scripture reading
- Emergency unlock (for real emergencies)

### Image/Animation spec

Soft gradient background. Small cross icon or dove. No aggressive sales imagery.

### CTA

**Primary button:** Start free trial
**Secondary:** Restore purchase (small text link)
**Skip option:** No (paywall is hard)

---

## Screen 5: Welcome

**Screen name:** welcome_success
**Progress:** 5/5

### Copy

**Headline:** You're ready to start

**Body:** Tomorrow at [reminder time], your selected apps will be locked until you complete [X] minutes of prayer.

**Subtext:** Your first morning starts tomorrow. Today is your setup day.

### Image/Animation spec

Celebration animation. Soft confetti or gentle light rays. Dove or cross icon with subtle glow.

### CTA

**Button text:** Begin my journey
**Skip option:** No

---

## A/B Test Variations

### Screen 1: Prayer Goal (Variant B)

**Headline:** Most Christians pray less than 2 minutes a day

**Body:** PrayerLock users average 12 minutes. Pick your starting goal.

**Hypothesis:** Guilt-driven copy may increase commitment to higher prayer times.

---

### Screen 4: Trial (Variant B - Urgency)

**Headline:** Unlock your prayer life

**Body:**
Join 10,000+ Christians who stopped scrolling and started praying.

**Price display:**
- 3 days free, then $49.99/year (just $0.96/week)

**Social proof:**
"My screen time dropped 2 hours and my prayer time went up 15 minutes." - Michael T.

**Hypothesis:** Community proof + per-week price framing may increase trial starts.

---

### Screen 4: Trial (Variant C - Loss framing)

**Headline:** What would you do with 15 extra minutes each morning?

**Body:**
Most people spend their first waking minutes on social media. PrayerLock flips that.

**Hypothesis:** Focusing on what they gain (not what they pay) may increase conversions.

---

## Technical Notes

### Permissions requested
- Notification permission (Screen 2)
- Screen Time/Usage Access (Screen 3, required for blocking)

### Data stored locally
- prayer_goal_minutes: int
- reminder_time: string (HH:MM)
- blocked_apps: array[string]
- trial_start_date: timestamp
- onboarding_completed: boolean

### Analytics events
- onboarding_started
- prayer_goal_selected (with value)
- reminder_set (with time)
- apps_selected (with count)
- trial_started
- onboarding_completed
