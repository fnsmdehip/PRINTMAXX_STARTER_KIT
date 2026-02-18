# Day 1 activation campaign

Goal: Get users to complete one core action within 24 hours of install.

Users who complete a core action on D1 retain 3x better at D30.

---

## Push notification sequence

### Push 1: Welcome (immediate)

**Timing:** 30 seconds after first app open

**Condition:** User has not completed core action

**Faith app:**
```
Welcome to [App Name]
Your first devotional is ready. Tap to start your journey.
```

**Fitness app:**
```
Welcome to [App Name]
Your first workout takes 7 minutes. Ready when you are.
```

**Productivity app:**
```
Welcome to [App Name]
Start your first focus session. Just 25 minutes.
```

---

### Push 2: Reminder (6 hours)

**Timing:** 6 hours after install, if no core action

**Condition:** App opened but core action not completed

**Faith app:**
```
Your daily verse is waiting
Take 2 minutes to reflect. It makes a difference.
```

**Fitness app:**
```
Quick win waiting
7-minute workout designed for today. No equipment needed.
```

**Productivity app:**
```
Ready to focus?
One session builds the habit. Start with 25 minutes.
```

---

### Push 3: End of day (8pm local)

**Timing:** 8pm local time, day of install

**Condition:** Still no core action completed

**Faith app:**
```
End your day with peace
Tonight's evening devotional takes 3 minutes.
```

**Fitness app:**
```
5 minutes before bed?
Quick stretch routine. Perfect for winding down.
```

**Productivity app:**
```
Plan tomorrow in 5 minutes
Set one goal for tomorrow. Start fresh.
```

---

## Email sequence

### Email 1: Welcome (immediate)

**Subject:** You're in. Here's how to get started.

**Body:**
```
Hey [Name],

Welcome to [App Name].

Here's what to do first:

1. Open the app
2. [Complete core action - specific to app type]
3. Done. You're 90% ahead of most people.

Most users who do this on day one stick around. Give it 3 minutes.

[CTA Button: Open App]

- [App Name] team
```

---

### Email 2: Getting started tips (12 hours)

**Subject:** The one thing that makes [App Name] work

**Condition:** No core action completed

**Faith app:**
```
Hey [Name],

Quick tip: the users who stick with [App Name] all have one thing in common.

They read their first devotional on day one.

Not because of some magic. Because it proves the app works for them.

Takes 2 minutes. Try it now.

[CTA Button: Read Today's Devotional]
```

**Fitness app:**
```
Hey [Name],

Quick tip: the users who actually get results have one thing in common.

They did their first workout on day one.

Doesn't matter if it's perfect. Starting is the whole point.

7 minutes. No equipment. Try it now.

[CTA Button: Start First Workout]
```

**Productivity app:**
```
Hey [Name],

Quick tip: the users who actually get focused have one thing in common.

They did their first session on day one.

25 minutes of real focus. That's it.

[CTA Button: Start Focus Session]
```

---

## In-app experience

### First open checklist

Show a simple 3-step checklist on first open:

```
Get started (3 steps)
[ ] Complete profile (optional)
[ ] [Core action - specific to app]
[ ] Enable daily reminders

2/3 complete - You're almost there
```

### Core action nudge

If user navigates away from core action:

**Modal trigger:** User taps back or tries to leave main screen

**Copy:**
```
Almost there

Finish your first [devotional/workout/session] to unlock daily features.

[Continue] [Maybe later]
```

### Success celebration

When core action completed:

**Animation:** Confetti or subtle celebration

**Copy:**
```
Day 1 complete!

You're now part of the [X]% who finished on day one.
Come back tomorrow to keep your streak going.

[Set daily reminder] [Done]
```

---

## Targeting and segmentation

### High-value segment (prioritize)

Users who:
- Enabled notifications
- Spent >2 minutes on D1
- Viewed multiple screens

**Extra touchpoint:** Send personalized push at 7pm if still no core action

### Medium-value segment

Users who:
- Opened app but bounced in <30 seconds
- Did not enable notifications

**Focus:** Re-engagement email with value prop reminder

### Low-value segment

Users who:
- Installed but never opened
- Likely from incentivized installs

**Approach:** Single reminder, then suppress to save quota

---

## Metrics to track

| Metric | Target | Current |
|--------|--------|---------|
| D1 core action rate | >40% | - |
| Push 1 open rate | >15% | - |
| Push 2 open rate | >10% | - |
| Email 1 open rate | >35% | - |
| Email 1 click rate | >8% | - |
| Onboarding completion | >60% | - |

---

## A/B test ideas

1. Welcome push: immediate vs 5-minute delay
2. Push copy: benefit-focused vs action-focused
3. Email subject: question vs statement
4. In-app checklist: visible vs hidden
5. Core action prompt: modal vs inline
6. Success celebration: confetti vs badge unlock
