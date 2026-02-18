# At-risk user campaign

Goal: Re-engage users showing churn signals before they leave.

Early intervention converts 15-25% of at-risk users back to active. Waiting until they're gone drops that to 2-5%.

---

## At-risk user definition

A user is "at risk" when they show these signals:

### Primary signals (high confidence)

| Signal | Risk level | Time to churn |
|--------|------------|---------------|
| No session in 3 days | Medium | 5-7 days |
| No session in 5 days | High | 2-4 days |
| No session in 7 days | Critical | 0-2 days |
| Disabled notifications | High | Variable |
| Never completed onboarding | Critical | 1-3 days |

### Secondary signals (supporting evidence)

| Signal | Meaning |
|--------|---------|
| Session length declining | Losing interest |
| Core actions declining | Not getting value |
| App opens without actions | Looking for something not found |
| Negative feedback/rating | Active dissatisfaction |

---

## Engagement score monitoring

Track users by engagement score (0-100):

```
Score components:
- Sessions last 7 days: up to 20 points
- Core actions last 7 days: up to 30 points
- Streak length: up to 15 points
- Notifications enabled: 15 points
- Features used: up to 20 points
```

**At-risk thresholds:**
- Score drops >20 points in 7 days: At risk
- Score drops below 30: At risk
- Score drops below 15: Critical

---

## Intervention sequence

### Stage 1: Gentle nudge (3 days inactive)

**Push notification:**

**Faith app:**
```
Your daily verse misses you
[Compelling snippet from today's content]. 2 minutes to reconnect.
```

**Fitness app:**
```
Quick check-in
Your body remembers movement. 5-minute workout waiting.
```

**Productivity app:**
```
Ready when you are
One focus session. Start whenever.
```

**Timing:** 9am local time

**Tone:** Friendly, no pressure

---

### Stage 2: Value reminder (5 days inactive)

**Push notification:**

**Faith app:**
```
3 minutes for your spirit
Life gets busy. Your faith doesn't have to wait.
```

**Fitness app:**
```
Movement is medicine
Even 7 minutes makes a difference. We kept your streak saved.
```

**Productivity app:**
```
Pick up where you left off
Your session history is waiting. One tap to restart.
```

**Email:**

**Subject:** We noticed you've been away

**Body:**
```
Hey [Name],

It's been 5 days. Life happens.

Quick reminder of what's waiting for you:
- [Personalized content based on their history]
- [Progress they've made so far]
- [New content added since they left]

No pressure. Just wanted you to know we're here when you're ready.

[CTA Button: Come Back]

- [App Name] team
```

**Tone:** Understanding, not guilt-tripping

---

### Stage 3: Concern (7 days inactive)

**Push notification:**

**Faith app:**
```
Is everything okay?
We're here if you need us. Your journey can continue anytime.
```

**Fitness app:**
```
We saved your spot
Your workout plan is right where you left it.
```

**Productivity app:**
```
Your focus sessions are waiting
Ready to restart whenever you are.
```

**Email:**

**Subject:** We miss you (and we have something for you)

**Body:**
```
Hey [Name],

It's been a week. We hope you're doing well.

We know life gets in the way. Here's something to make coming back easier:

[Offer: 7 days of premium free, exclusive content unlock, etc.]

No strings. Just a thank you for giving [App Name] a try.

[CTA Button: Claim Offer]

- [App Name] team
```

**Tone:** Concerned, with incentive

---

### Stage 4: Last attempt (14 days inactive)

**Push notification:**

**Faith app:**
```
We'll be here
If you ever want to come back, your progress is saved.
```

**Fitness app:**
```
Your workouts are waiting
Whenever you're ready, we're here.
```

**Productivity app:**
```
Focus is just a tap away
Come back anytime.
```

**Email:**

**Subject:** Before you go

**Body:**
```
Hey [Name],

It's been 2 weeks. We're not going to keep bothering you.

Before we stop reaching out, we wanted to ask:

What could we do better?

[Quick survey: 3 options]
- App didn't fit my routine
- Content wasn't what I expected
- Technical issues
- Other: [text field]

Your feedback helps us improve for others.

If you ever want to come back, your account and progress will be waiting.

Thanks for trying [App Name].

- [App Name] team
```

**Tone:** Respectful, exit survey

---

## In-app interventions

### Welcome back modal

**Trigger:** User returns after 3+ days inactive

```
Welcome back!

We kept everything ready for you:
- Your progress: [summary]
- Your streak: [X days saved/lost]
- New since you left: [content count]

Ready to pick up where you left off?

[Continue] [Start fresh]
```

### Streak save offer

**Trigger:** User is about to lose streak (24h before)

**Push:**
```
Your [X]-day streak ends tonight
Open [App Name] to keep it going. 2 minutes is all it takes.
```

**In-app (if opened):**
```
Streak save!

You almost lost your [X]-day streak.

Good news: We saved it this time.

[Use streak freeze] [Continue to today's content]
```

### Re-onboarding option

**Trigger:** User returns after 14+ days

```
Things have changed since you left

Want a quick tour of what's new?

[Show me] [Skip, I'll explore]
```

---

## Segment-specific approaches

### Segment: Never activated

**Profile:** Installed, opened once, never completed core action

**Approach:**
- Focus on activation, not re-engagement
- Show simplest path to value
- Remove all friction
- Consider "one-tap" content

**Push:**
```
Try this instead
[App Name] has a 2-minute option. Perfect for busy days.
```

### Segment: Activated but fading

**Profile:** Completed D1-D7, then dropped off

**Approach:**
- Remind of progress made
- Highlight what they'll lose
- Offer streak recovery

**Push:**
```
Your [X]-day streak
We can restore it. One session today keeps it alive.
```

### Segment: Long-term user declining

**Profile:** Active for 30+ days, now slipping

**Approach:**
- Ask what changed
- Offer new content/challenges
- Consider premium incentive

**Email:**
```
Subject: Quick question

Hey [Name],

You've been with us for [X] days. Lately, we noticed you're using [App Name] less.

Did something change? We'd love to know how we can help.

- Different content preferences?
- Time constraints?
- Technical issues?

Hit reply and let us know. We read every response.

- [App Name] team
```

---

## What not to do

### Don't guilt trip
Bad: "You're letting yourself down by not using [App Name]"
Good: "We're here when you're ready"

### Don't spam
Bad: Daily notifications to inactive users
Good: Escalating sequence with decreasing frequency

### Don't promise what you can't deliver
Bad: "Come back and everything will be different"
Good: "Here's something specific that might help"

### Don't ignore the exit
Bad: No feedback collection
Good: Exit survey to learn and improve

---

## Metrics to track

| Metric | Target | Current |
|--------|--------|---------|
| At-risk identification rate | >90% of churners flagged | - |
| Stage 1 re-engagement rate | >20% | - |
| Stage 2 re-engagement rate | >15% | - |
| Stage 3 re-engagement rate | >10% | - |
| Exit survey completion | >10% | - |
| Re-engaged user D30 retention | >40% | - |

---

## Automation setup

### Firebase/OneSignal rules

```
Segment: at_risk_stage_1
Condition: last_session > 3 days AND last_session < 5 days
Action: Send at_risk_nudge_1 push

Segment: at_risk_stage_2
Condition: last_session > 5 days AND last_session < 7 days
Action: Send at_risk_value_reminder push + email

Segment: at_risk_stage_3
Condition: last_session > 7 days AND last_session < 14 days
Action: Send at_risk_concern push + email with offer

Segment: at_risk_stage_4
Condition: last_session > 14 days AND last_session < 30 days
Action: Send at_risk_exit push + exit survey email
```

### Suppression rules

- Don't send at-risk messages to users who just unsubscribed from premium
- Don't send after exit survey completed
- Maximum 1 push per 48 hours to at-risk users
- Stop all outreach after 30 days inactive
