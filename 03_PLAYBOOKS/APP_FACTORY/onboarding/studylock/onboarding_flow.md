# StudyLock Onboarding Flow

**App:** StudyLock
**Screens:** 5
**Goal:** Set study session length, configure schedule, select blocked apps, start trial
**Target conversion:** Trial start > 75%

---

## Screen 1: Study Goal

**Screen name:** study_goal
**Progress:** 1/5

### Copy

**Headline:** How long can you focus?

**Body:** StudyLock uses the Pomodoro method. You study for a set time, then get a break. Most students start with 25 minutes.

### Options

| Option | Value | Subtext | Break time |
|--------|-------|---------|------------|
| 15 min | 15 | Quick focus | 3 min break |
| 25 min | 25 | Classic Pomodoro | 5 min break |
| 45 min | 45 | Deep work | 10 min break |
| 60 min | 60 | Marathon mode | 15 min break |

### Image/Animation spec

Timer illustration. Books/study materials in background. Clean, focused aesthetic. No distracting elements.

### CTA

**Button text:** Set my session
**Skip option:** No

---

## Screen 2: Schedule

**Screen name:** study_schedule
**Progress:** 2/5

### Copy

**Headline:** When do you study?

**Body:** We'll lock your apps during these times. You can still override if needed, but it'll cost your streak.

### Options

**Quick presets:**
- Weekday mornings (6am-12pm)
- Weekday afternoons (12pm-6pm)
- Weekday evenings (6pm-11pm)
- Weekends (all day)
- Custom schedule

**Day selection:** M T W T F S S (toggles)

**Time range:** Start time - End time pickers

### Image/Animation spec

Weekly calendar grid. Selected days highlighted. Clock showing active hours.

### CTA

**Button text:** Set schedule
**Skip option:** Yes (small text "I'll study whenever" - enables 24/7 blocking)

---

## Screen 3: Blocked Apps

**Screen name:** blocked_apps
**Progress:** 3/5

### Copy

**Headline:** What kills your focus?

**Body:** These apps stay locked during study sessions. Be honest - the apps you want to keep are probably the ones you need to block.

### Pre-selected defaults

- TikTok
- Instagram
- Snapchat
- YouTube
- Twitter/X
- Discord
- Reddit

### Display

Grid of app icons with checkboxes. "Time wasters" section pre-selected. "Add all social" quick button.

### Image/Animation spec

App icons with lock overlays. Subtle red "blocked" indicator. Clean grid layout.

### CTA

**Button text:** Lock these apps
**Skip option:** No

---

## Screen 4: Trial

**Screen name:** paywall_trial
**Progress:** 4/5

### Copy

**Headline:** 7 days free. Then decide.

**Body:**
Full access to StudyLock. Cancel anytime before the trial ends and pay nothing.

**Price display:**
- 7 days free
- Then $6.99/month or $34.99/year (save 58%)

**Social proof:**
"Went from C's to A's. Not kidding. My screen time dropped from 6 hours to 2." - Alex T., UCLA

### Features list

- Block apps during study sessions
- Pomodoro timer with breaks
- Track study hours and streaks
- Session history and stats
- Emergency unlock (counts against you)

### Student angle

**Subtext:** That's less than the cost of one coffee per week.

### Image/Animation spec

Student studying (illustration, not photo). Books, laptop, focused environment. Timer showing progress.

### CTA

**Primary button:** Start 7-day free trial
**Secondary:** Restore purchase (small text link)
**Skip option:** No (hard paywall)

---

## Screen 5: Start

**Screen name:** ready_to_study
**Progress:** 5/5

### Copy

**Headline:** Your focus zone is ready

**Body:** Tap "Start Session" when you're ready to study. Your [blocked apps count] selected apps will be locked for [X] minutes.

**Subtext:** First session starts when you tap the button. Take a breath. Then let's go.

### Quick stats display

- Session length: [25] minutes
- Break length: [5] minutes
- Apps blocked: [7] apps
- Schedule: [Weekdays 6pm-11pm]

### Image/Animation spec

Large "Start Session" button. Timer ready to begin. Calm, focused design.

### CTA

**Button text:** Start first session
**Skip option:** Yes (small text "I'll start later" - goes to home screen)

---

## A/B Test Variations

### Screen 1: Study Goal (Variant B - Guilt angle)

**Headline:** That 5-minute break that became 3 hours

**Body:** You know the feeling. StudyLock makes sure it doesn't happen. Pick your focus time.

**Hypothesis:** Guilt-based copy may resonate with students who recognize the pattern.

---

### Screen 4: Trial (Variant B - GPA angle)

**Headline:** What's one letter grade worth?

**Body:**
Students who use StudyLock report studying 40% more. Most say their grades improved within one semester.

**Price display:**
- 7 days free
- $34.99/year = $0.67/week

**Social proof:**
"My GPA went from 2.8 to 3.4. This app forced me to actually study." - Jordan P., Texas State

**Hypothesis:** GPA improvement framing may increase perceived value for grade-focused students.

---

### Screen 4: Trial (Variant C - Parent payment angle)

**Headline:** Ask your parents. They'll say yes.

**Body:**
$35/year is nothing compared to tuition. Tell them it's for your grades.

**Price display:**
- 7 days free
- $34.99/year (one textbook costs more)

**Hypothesis:** Some students will forward to parents. Lower friction for family payment.

---

## Technical Notes

### Permissions requested
- Notification permission (for session end alerts)
- Screen Time / Usage Access (Screen 3, required for blocking)

### Data stored locally
- session_length: int (minutes)
- break_length: int (minutes)
- schedule_days: array[string]
- schedule_start: string (HH:MM)
- schedule_end: string (HH:MM)
- blocked_apps: array[string]
- trial_start_date: timestamp
- onboarding_completed: boolean

### Analytics events
- onboarding_started
- session_length_selected (with value)
- schedule_configured (with days, times)
- apps_selected (with count)
- trial_started
- onboarding_completed
- first_session_started
