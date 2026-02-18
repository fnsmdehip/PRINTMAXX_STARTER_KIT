# Onboarding flow

Turn new joins into active community members in 7 days.

---

## The first 7 days matter

**Statistics:**
- 40% of Discord members never post
- 70% of inactive members decided within first 24 hours
- Members who post in first 48 hours = 3x more likely to stay

**Goal:** Get every new member to take meaningful action within 48 hours.

---

## Onboarding stages

```
Join (Day 0)
    |
    v
Welcome (0-1 hour) - Orientation + quick win
    |
    v
Introduce (24 hours) - First post + connection
    |
    v
Engage (48 hours) - Reply to others
    |
    v
Participate (Day 3-5) - Join challenge/thread
    |
    v
Contribute (Day 7) - Help someone else
    |
    v
ACTIVATED
```

---

## Stage 1: Welcome (0-1 hour)

### Automatic welcome DM

Trigger: On join
Sender: Bot (MEE6 or Carl-bot)

```
Welcome to [Community Name]!

You're now part of [X] members working on [shared goal].

Here's your 3-minute start:

1. Read #rules (takes 60 seconds)
2. React with :white_check_mark: to get access
3. Post your intro in #introductions

Questions? Drop them in #questions. We respond fast.

See you inside!
[Bot name]
```

### Public welcome message

Channel: #welcome (or #general)

```
Welcome @[username]! Head to #introductions when you're ready.
```

Keep it short. Elaborate welcomes feel overwhelming.

### What NOT to do

- Wall of text DMs (nobody reads)
- 10 links to click
- Complex verification
- No clear next step

---

## Stage 2: Introduction (24 hours)

### Introduction template

Post in #introductions channel description:

```
Tell us about yourself! Copy this template:

**Name:**
**Location:**
**What brings you here:**
**Current goal:**
**Fun fact:**

Can't wait to meet you!
```

### Mod response to intros

Within 30 minutes of new intro:

```
Welcome [name]! [Personal comment on something they shared].

You'll fit right in here. Check out #[relevant-channel] for [specific thing they mentioned].

Tag me anytime if you need help!
```

**Key:** Reference something specific from their intro. Shows you read it.

### Intro engagement tactics

1. **Pin best intros** - Shows what good looks like
2. **@mention veterans** - "Hey @veteran, [new member] is also into X!"
3. **Ask follow-up question** - Keeps conversation going
4. **React with emojis** - Even lurkers will react back

### If they don't introduce (24h)

Send personal DM:

```
Hey [name]! Saw you joined yesterday. Welcome!

Quick tip: Posting an intro in #introductions is the fastest way to connect with people here. Even a one-liner works.

Any questions about getting started? Happy to help.
```

---

## Stage 3: Engage (48 hours)

### Goal: Get them replying to others

### Tactics

**1. Tag them in relevant discussions**
```
[In #general when relevant topic comes up]
@newmember mentioned they're working on this in their intro - any thoughts?
```

**2. Easy engagement prompts**
```
[Daily prompt in #general]
Quick poll: [Easy question with 2-3 options]
React :one: for Option A
React :two: for Option B
```

**3. Welcome thread**
```
[Create weekly welcome thread]
This week's new members: @user1 @user2 @user3

Say hi! What's one thing you want to accomplish this week?
```

### If they haven't engaged (48h)

DM check-in:

```
Hey [name]! Just checking in.

Finding everything okay? The community can feel big at first. Here are 3 easy ways to jump in:

1. React to a message you like
2. Drop a comment in #wins celebrating someone
3. Ask a question in #questions

No pressure - just want to make sure you're not lost. Here to help!
```

---

## Stage 4: Participate (Day 3-5)

### Goal: Deeper involvement

### Tactics

**1. Challenge invitation**
```
[DM or mention]
Hey [name]! We just started a [challenge name]. Perfect timing for you since you mentioned [goal from intro].

Join us in #current-challenge. It's low-pressure and everyone's supportive.
```

**2. Accountability group matching**
```
[DM]
Saw you're working on [goal]. We have accountability groups that meet [frequency]. Want me to connect you with one?
```

**3. Live event invitation**
```
[DM before event]
Heads up - we have a [event type] this [day] at [time]. Great way to meet people. You in?
```

### If they haven't participated (Day 5)

Last check-in:

```
Hey [name]!

Just wanted to see if [Community] is what you expected. If it's not clicking, totally fine - I'd love your honest feedback.

If it IS working for you, what would help you participate more?

Either way, thanks for being here.
```

---

## Stage 5: Contribute (Day 7)

### Goal: Give value to others

### Tactics

**1. Spot opportunities to help**
```
[When newbie has relevant experience]
Hey @newmember, saw you have experience with [X]. Would love your take on @othermember's question.
```

**2. Ask for input**
```
[In relevant channel]
Working on [topic]. Anyone have experience with this? @newmember @othernewmember - you two are fresh eyes, what do you think?
```

**3. Celebrate their wins**
```
[When they post a win]
This is awesome, [name]! First week and already crushing it.

Everyone - check out what [name] did: [screenshot/quote]
```

---

## Activation tracking

### Activation criteria

Member is "activated" when they've completed:
- [ ] Introduction posted
- [ ] Replied to someone else's post
- [ ] Participated in a challenge OR attended an event
- [ ] Helped another member

### Tracking spreadsheet

| Member | Join date | Intro | First reply | Challenge | Help | Activated |
|--------|-----------|-------|-------------|-----------|------|-----------|
| @user1 | 1/15 | 1/15 | 1/16 | 1/18 | - | Partial |
| @user2 | 1/15 | 1/15 | 1/15 | 1/17 | 1/19 | Yes |
| @user3 | 1/15 | - | - | - | - | No |

### Activation rate targets

- Day 1 intro: 70%+
- Day 3 engagement: 50%+
- Day 7 full activation: 30%+

---

## Onboarding automation

### Discord bot sequence (Carl-bot)

**Day 0 (on join):**
```
!autoresponder add welcdm {user.mention}
Welcome to [Community]! Check your DMs for how to get started.
```

**Day 1 (if no intro):**
Set up scheduled DM reminder via MEE6 premium or manual mod task.

**Day 3 (if no engagement):**
Second DM check-in.

**Day 7 (if not activated):**
Final personal outreach or survey.

### Manual mod tasks (daily)

1. Check new joins from past 24h
2. Reply to all intros from past 24h
3. DM any Day 2 members without intros
4. Tag inactive members in relevant convos
5. Update activation tracker

---

## Onboarding content checklist

### #welcome channel

- [ ] Server overview (2-3 sentences)
- [ ] Clear next steps (numbered list)
- [ ] Link to #rules
- [ ] Reaction to unlock channels

### #rules channel

- [ ] Community values (3-5 points)
- [ ] Behavior expectations
- [ ] Consequences for violations
- [ ] How to get help

### #start-here channel

- [ ] App download links
- [ ] Key resources
- [ ] FAQ
- [ ] How to use different channels

### Welcome DM

- [ ] Warm greeting
- [ ] 3 clear action steps
- [ ] One easy win to accomplish
- [ ] How to get help

---

## Common onboarding failures

### 1. Information overload

**Problem:** 5 DMs, 20 channels, wall of text rules
**Fix:** One DM, one clear next step

### 2. No human touch

**Problem:** All automated, no personal connection
**Fix:** Mod replies to every intro personally

### 3. Too slow

**Problem:** First response takes 24+ hours
**Fix:** Set up notification for intros, respond within 1 hour

### 4. No clear path

**Problem:** "Welcome! Enjoy!" with no guidance
**Fix:** Specific numbered steps to take

### 5. No quick win

**Problem:** First achievement takes weeks
**Fix:** Create easy early wins (first post, first reaction, first badge)

---

## Measuring onboarding success

### Key metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Intro rate | Intros / New joins | 70%+ |
| 7-day retention | Active at Day 7 / Joined | 60%+ |
| Time to first post | Avg time from join to post | < 24h |
| Activation rate | Fully activated / Joined | 30%+ |

### Weekly review questions

1. What % of new members introduced themselves?
2. What % engaged with others in first 48h?
3. How many dropped off without any activity?
4. What's working? What's not?
5. Any member feedback on onboarding experience?
