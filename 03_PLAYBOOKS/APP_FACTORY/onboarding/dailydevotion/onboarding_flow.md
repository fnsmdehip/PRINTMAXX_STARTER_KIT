# DailyDevotion Onboarding Flow

**App:** DailyDevotion
**Screens:** 5
**Goal:** Select denomination/tradition, choose reading plan, set reminder, start trial, begin day 1
**Target conversion:** Trial start > 65% (freemium model)
**Mascot:** Dove

---

## Screen 1: Denomination

**Screen name:** denomination
**Progress:** 1/5

### Copy

**Headline:** Welcome to DailyDevotion

**Dove says:** "Let's personalize your experience."

**Body:** What faith tradition do you follow? This helps us suggest relevant content.

### Options

| Tradition | Value | Notes |
|-----------|-------|-------|
| Protestant | protestant | Baptist, Methodist, Presbyterian, etc. |
| Catholic | catholic | Roman Catholic tradition |
| Non-denominational | nondenominational | Bible-focused, no specific denomination |
| Orthodox | orthodox | Eastern Orthodox traditions |
| Other Christian | other | Doesn't fit above categories |
| Just exploring | exploring | Curious about faith |

### Privacy note

"We use this to personalize your experience. Your selection is stored locally and never shared."

### Image/Animation spec

Dove icon with soft glow. Calming purple/gold color palette. Rounded selection cards.

### CTA

**Button text:** Continue
**Skip option:** Yes (small text "Skip personalization")

---

## Screen 2: Reading Plan

**Screen name:** reading_plan
**Progress:** 2/5

### Copy

**Headline:** How do you want to read Scripture?

**Dove says:** "Pick a plan that fits your life. No pressure."

**Body:** You can change this anytime. Most people start with Verse of the Day.

### Options

| Plan | Duration | Description | Premium |
|------|----------|-------------|---------|
| Verse of the Day | Daily | One verse with reflection | Free |
| New Testament in 90 Days | 90 days | Read through the gospels and letters | Free |
| Psalms and Proverbs | 30 days | Wisdom literature focus | Free |
| Whole Bible in 1 Year | 365 days | Complete Bible reading plan | Premium |
| Topical Studies | Varies | Gratitude, peace, purpose, etc. | Premium |
| Custom Plan | Varies | Build your own reading schedule | Premium |

### Premium indicator

Lock icon on premium plans. "Premium" badge.

### Image/Animation spec

Book/Bible icon for each plan. Progress preview showing what the plan looks like. Soft, inviting design.

### CTA

**Button text:** Select [plan name]
**Skip option:** Yes (small text "I'll choose later" - defaults to Verse of the Day)

---

## Screen 3: Reminder

**Screen name:** reminder_setup
**Progress:** 3/5

### Copy

**Headline:** When should we remind you?

**Dove says:** "A gentle nudge at the right time makes all the difference."

**Body:** Users who set reminders complete their reading 78% more often.

### Options

Time picker wheel. Default: 7:00 AM

Quick presets:
- Dawn (5:30 AM) - "Before the day begins"
- Morning (7:00 AM) - "Start your day grounded"
- Midday (12:00 PM) - "Pause and reflect"
- Evening (8:00 PM) - "Wind down with Scripture"
- Custom

### Notification preview

"Your daily verse is waiting. Take 2 minutes for your soul."

### Image/Animation spec

Dove with soft bell. Sunrise/sunset gradient based on time selected.

### CTA

**Button text:** Set reminder
**Skip option:** Yes (small text "I'll remember on my own")

---

## Screen 4: Trial

**Screen name:** paywall_trial
**Progress:** 4/5

### Copy

**Headline:** Build habits that matter

**Dove says:** "Your spiritual growth is worth investing in."

**Body:**
Start with our free features. Upgrade when you're ready for more.

### Free vs Premium

| Feature | Free | Premium |
|---------|------|---------|
| Up to 5 habits | Yes | Unlimited |
| 3 reading plans | Yes | All plans |
| Daily verse | Yes | Yes |
| Streak tracking | Yes | Yes |
| Dove encouragement | Yes | Yes |
| Advanced statistics | No | Yes |
| Multiple translations | No | Yes |
| Cloud backup | No | Yes |
| No ads | No | Yes |

**Price display:**
- Premium: $4.99/month or $29.99/year (save 50%)
- 7-day free trial of Premium

### Image/Animation spec

Dove with gentle animation. Side-by-side comparison. Purple/gold color scheme. "Best value" badge on annual.

### CTA

**Primary button:** Try Premium free for 7 days
**Secondary button:** Continue with free
**Tertiary:** Restore purchase (small text link)
**Skip option:** Yes (Continue with free)

---

## Screen 5: Day 1

**Screen name:** first_day
**Progress:** 5/5

### Copy

**Headline:** Day 1 begins now

**Dove says:** "Your journey starts with a single verse."

**Body:** Here's your first reading. Take a moment. Let it sink in.

### Dynamic content

**Display today's verse:**
[Verse from bible-api.com based on selected plan]

Example:
"Be still, and know that I am God." - Psalm 46:10 (KJV)

### Reflection prompt

"What does this verse mean to you today?"

Optional text input for journaling (local storage only).

### Image/Animation spec

Verse displayed in beautiful typography. Soft background. Dove with peaceful animation. "Mark as read" checkbox.

### CTA

**Primary button:** Mark as read
**Secondary:** Save to journal (if reflection entered)
**Skip option:** No

---

## Post-Onboarding: Success Screen

**Screen name:** welcome_complete

### Copy

**Headline:** You're all set

**Dove says:** "See you tomorrow. Same time, same place."

**Body:**
- Your reminder is set for [time]
- Reading plan: [plan name]
- Faithfulness streak: 1 day

"Consistency is faithfulness in action."

### CTA

**Button text:** Go to home
**Skip option:** No

---

## A/B Test Variations

### Screen 1: Denomination (Variant B - Focus question)

**Headline:** What area of faith do you want to grow?

**Body:** We'll suggest content that matches your focus.

**Options:**
- Prayer life (want to pray more consistently)
- Scripture knowledge (want to know the Bible better)
- Gratitude (want to cultivate thankfulness)
- Peace (struggling with anxiety or stress)
- Purpose (seeking direction in life)
- General growth (all of the above)

**Hypothesis:** Focus-based onboarding may feel more actionable than denomination-based.

---

### Screen 2: Reading Plan (Variant B - Commitment levels)

**Headline:** How much time do you have?

**Body:** Be honest. A 2-minute habit beats a 30-minute intention.

**Options:**
- 2 minutes (One verse + reflection)
- 5 minutes (Short passage)
- 15 minutes (Chapter reading)
- 30+ minutes (Deep study)

**Then:** Auto-suggest plan based on time selection.

**Hypothesis:** Time-based selection may reduce overwhelm and increase plan completion.

---

### Screen 4: Trial (Variant B - Mission framing)

**Headline:** Invest in your soul

**Dove says:** "You spend money on your body, your mind. Why not your spirit?"

**Body:**
$29.99/year = $0.57/week

Less than a coffee. For daily spiritual growth.

**Hypothesis:** Investment framing may resonate with faith-focused users.

---

### Screen 5: Day 1 (Variant B - Audio option)

**Headline:** Listen or read

**Body:** Your first verse is ready. Pick how you want to receive it.

**Options:**
- Read the verse (shows text)
- Listen to the verse (audio player)

**Hypothesis:** Audio option may increase engagement for users who prefer listening.

---

## Dove Messages Throughout Onboarding

| Screen | Dove Message |
|--------|--------------|
| Denomination | "Let's personalize your experience." |
| Reading Plan | "Pick a plan that fits your life. No pressure." |
| Reminder | "A gentle nudge at the right time makes all the difference." |
| Trial | "Your spiritual growth is worth investing in." |
| Day 1 | "Your journey starts with a single verse." |
| Complete | "See you tomorrow. Same time, same place." |

---

## Technical Notes

### Permissions requested
- Notification permission (Screen 3, optional but encouraged)

### Data stored locally
- denomination: string
- selected_plan: string
- reminder_enabled: boolean
- reminder_time: string (HH:MM)
- is_premium: boolean
- trial_start_date: timestamp (if applicable)
- onboarding_completed: boolean
- day_1_completed: boolean
- first_verse_date: timestamp

### API integration
- Bible verse: bible-api.com
- Cache verse locally for offline access
- Support KJV (free, public domain) as default

### Analytics events
- onboarding_started
- denomination_selected (with value) / skipped
- plan_selected (with value)
- reminder_set (with time) / reminder_skipped
- paywall_shown
- trial_started / free_selected
- day_1_verse_shown
- day_1_marked_read
- reflection_entered (boolean, not content)
- onboarding_completed
