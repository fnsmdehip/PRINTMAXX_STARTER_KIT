# Moderation guidelines

How to keep the community healthy without being a dictator.

---

## Moderation philosophy

**Goal:** Create environment where good behavior is easy and bad behavior is rare.

**Approach:**
- Prevention > enforcement
- Education > punishment
- Private correction > public shaming
- Consistency > leniency

**Remember:** Every moderation action affects three audiences:
1. The person being moderated
2. Everyone watching
3. Future community culture

---

## Response framework

### The 4-step response

1. **Assess** - Is this actually a problem? (Read context)
2. **Warn** - Private DM with clear explanation
3. **Enforce** - Temporary action (mute/timeout)
4. **Remove** - Permanent action (ban) if pattern continues

### Response by severity

| Severity | Example | Action |
|----------|---------|--------|
| Minor | Off-topic message | Redirect to correct channel |
| Low | Mild rudeness | Friendly reminder in thread |
| Medium | Argument escalation | Private DM warning |
| High | Harassment, hate speech | Immediate mute + review |
| Critical | Threats, illegal content | Immediate ban + document |

---

## Common situations

### 1. Off-topic conversation

**Situation:** Discussion drifts from channel purpose

**Response:**
```
Hey! This is a great convo but might fit better in #off-topic. Mind moving it there? Thanks!
```

**Escalation:** Redirect message + delete if they continue

### 2. Heated argument

**Situation:** Two members getting personal

**Response:**
```
[Public in channel]
Let's cool this down. Disagreement is fine, but keep it respectful. Take 5 and come back fresh.

[DM to both]
Hey, I noticed things got heated in #general. No formal warning, just wanted to check in. Everything okay?
```

**Escalation:** Temp mute both for 1 hour if continues

### 3. Spam or self-promotion

**Situation:** Member drops link without context

**Response:**
```
[DM]
Hey! Saw your link in #general. We love when members share resources, but please add some context about why it's helpful. Dropping links without explanation comes across as spam.
```

**Escalation:** Delete message + warning if pattern

### 4. Harmful content

**Situation:** Hate speech, threats, or illegal content

**Response:**
1. Screenshot for records
2. Delete immediately
3. Mute/ban depending on severity
4. Document in mod log

```
[DM - only if salvageable]
Your message in #channel was removed because it violated our community guidelines on [specific rule]. This is a formal warning.
```

### 5. Mental health crisis

**Situation:** Member expresses self-harm thoughts

**Response:**
```
[DM - compassionate, not clinical]
Hey, I saw your message and wanted to reach out. I'm not a professional, but I care about you. If you're in crisis, please reach out to:

- Crisis Text Line: Text HOME to 741741
- National Suicide Prevention: 988
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

We're here for you, but please also talk to someone trained to help.
```

**Do not:** Delete the message publicly (can feel invalidating)
**Do:** Follow up next day

---

## Warning system

### Warning levels

| Level | Consequence | Reset after |
|-------|-------------|-------------|
| 1st warning | Verbal (DM) | 30 days |
| 2nd warning | Written + 24h mute | 60 days |
| 3rd warning | 7-day suspension | 90 days |
| 4th warning | Permanent ban | N/A |

### Warning template

```
Subject: Community Guidelines Notice

Hi [name],

This is a formal warning regarding your message in #[channel] on [date].

What happened: [Specific description of the issue]

Why it matters: [How it affects the community]

Our expectations: [What we need going forward]

This is warning [X] of 3. Further violations may result in temporary or permanent removal from the community.

If you have questions or want to discuss, reply to this message.

[Mod name]
```

### Warning log

Maintain in private mod channel or spreadsheet:

| Date | Member | Channel | Issue | Action | Mod |
|------|--------|---------|-------|--------|-----|
| 1/15 | @user | #general | Spam links | Verbal warning | ModA |
| 1/18 | @user | #questions | Rude to newbie | Written warning + 24h mute | ModB |

---

## Ban policy

### When to ban immediately

- Threats of violence
- Hate speech / slurs
- Doxxing or sharing private info
- Illegal content
- Spam bots
- Raid participants

### When to warn first

- Rudeness / bad attitude
- Rule misunderstandings
- Excessive self-promotion
- Off-topic persistent behavior
- Minor ToS violations

### Ban message template

```
Subject: Removal from [Community Name]

Hi [name],

You have been removed from [Community Name] for [specific reason].

This decision was made because: [Details]

Your warning history: [Previous warnings if any]

If you believe this was in error, you may appeal by emailing [email].

[Community Name] Team
```

### Appeal process

1. Member emails appeal
2. Different mod reviews case
3. Decision within 7 days
4. If overturned, provide re-entry path

---

## Moderator conduct

### Do

- Stay calm always
- Be consistent with rules
- Document everything
- Ask for second opinion on edge cases
- Take breaks when frustrated
- Assume good intent first

### Don't

- Moderate when emotional
- Make exceptions for friends
- Argue publicly with members
- Share mod discussions publicly
- Ghost members who were warned
- Use mod powers for personal disputes

### Mod disagreement protocol

1. Discuss privately in mod channel
2. If still divided, escalate to admin
3. Present unified decision to community
4. Debrief afterwards

---

## Proactive moderation

### Daily tasks

- Check reported messages queue
- Scan active channels for tone
- Welcome new verified members
- Review any flagged posts

### Weekly tasks

- Review warning log
- Identify emerging issues
- Recognize positive members
- Team sync on approach consistency

### Monthly tasks

- Audit rule effectiveness
- Update automod filters
- Review banned member appeals
- Moderator feedback session

---

## Automod configuration

### Words/phrases to flag

- Slurs and hate speech (auto-delete + flag)
- Competitor names (flag for review)
- Excessive caps (warn)
- Link domains (whitelist approved)
- Spam patterns (auto-delete)

### Automod rules (Carl-bot example)

```
Rule: No Discord invites
Trigger: discord.gg OR discord.com/invite
Action: Delete + DM warning
Exception: Moderator role

Rule: Spam detection
Trigger: Same message 3x in 10 minutes
Action: Delete + 1h mute

Rule: Excessive mentions
Trigger: More than 5 mentions in one message
Action: Delete + flag for review
```

---

## Escalation matrix

| Issue | First response | Escalate to | Escalate if |
|-------|----------------|-------------|-------------|
| Off-topic | Any mod | - | Repeated after redirect |
| Rudeness | Any mod | Senior mod | Pattern or unclear case |
| Harassment | Senior mod | Admin | Any threat or doxxing |
| Legal concern | Admin | Legal counsel | Actual legal risk |
| Mental health | Any mod | Admin | Immediate danger |

---

## Moderator wellbeing

### Signs of burnout

- Dreading opening Discord
- Snapping at minor issues
- Taking things personally
- Avoiding the community

### Prevention

- Rotate high-stress duties
- Set offline hours (enforce them)
- Celebrate mod wins
- Regular 1:1s with admin
- Permission to take breaks

### When to step back

- You're emotionally invested in a decision
- The situation involves someone you know personally
- You've had previous conflict with the member
- You're not sure what the right call is

Hand off to another mod. No shame in it.

---

## Cheat sheet

### Quick responses

**Off-topic:** "Great point! Mind moving to #off-topic?"

**Argument:** "Let's dial it back. Both have good points. Take 5?"

**Question in wrong channel:** "Good question! You'll get faster help in #questions."

**Self-promo spam:** [Delete + DM about guidelines]

**First warning:** "Hey, quick note about [issue]. Please [correction]. Thanks!"

**Second warning:** "This is a formal warning. [Issue] isn't okay here. Next one = timeout."

**Timeout:** "Taking a break from the server. Back in [time]. DM if questions."

**Ban:** "Removed for [reason]. Appeal via [email]."
