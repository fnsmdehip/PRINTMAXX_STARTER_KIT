# Discord bot commands

Essential bots, setup instructions, and command references.

---

## Recommended bot stack

### Tier 1: Must-have

| Bot | Purpose | Cost |
|-----|---------|------|
| MEE6 | Welcome, leveling, moderation | Free (Premium $12/mo) |
| Carl-bot | Reaction roles, automod, logging | Free |
| Statbot | Analytics, tracking | Free (Premium $5/mo) |

### Tier 2: Nice-to-have

| Bot | Purpose | Cost |
|-----|---------|------|
| Dyno | Moderation, custom commands | Free |
| Apollo | Event scheduling | Free |
| Ticket Tool | Support tickets | Free |

---

## MEE6 setup

### Installation

1. Go to mee6.xyz
2. Click "Add to Discord"
3. Select your server
4. Authorize permissions

### Welcome messages

**Dashboard > Welcome**

```
Welcome message (DM):
Welcome to [Server Name], {user}!

Here's how to get started:
1. Read the rules in #rules
2. Introduce yourself in #introductions
3. Check out #start-here for resources

Questions? Ask in #questions. We're here to help.
```

```
Welcome message (channel):
Hey {user}, welcome to the community! Head to #introductions and tell us about yourself.
```

### Leveling system

**Dashboard > Levels**

Enable: ON

Level-up message:
```
{user} just reached level {level}! Keep it up.
```

**Level rewards (role assignments):**
| Level | Role | Perks |
|-------|------|-------|
| 5 | Regular | Access to #off-topic |
| 10 | Active | Can create threads |
| 20 | Veteran | Special color, voice priority |
| 50 | Legend | Access to #inner-circle |

### XP settings

- XP per message: 15-25 (randomized)
- XP cooldown: 60 seconds
- No XP in: #off-topic, #memes (prevents spam farming)

---

## Carl-bot setup

### Installation

1. Go to carl.gg
2. Click "Invite Carl-bot"
3. Select server and authorize

### Reaction roles

**Dashboard > Reaction Roles**

Example setup for #welcome:

```
!rr make

Title: Get your roles!
Description: React to unlock channels

Roles:
:muscle: - Fitness Focus
:brain: - Mindset Focus
:pray: - Faith Focus
:bell: - Announcement Pings
```

### Auto-moderation

**Dashboard > Automod**

Enable:
- Link blacklist (spam domains)
- Word filter (slurs, spam phrases)
- Mention spam (max 5 mentions)
- Caps filter (80% caps = warning)
- Invite filter (no Discord invites)

### Logging

**Dashboard > Logging**

Log to #mod-log:
- Message deletes
- Message edits
- Member joins/leaves
- Role changes
- Bans/kicks

---

## Statbot setup

### Installation

1. Go to statbot.net
2. Add to Discord
3. Authorize

### Key commands

```
/stats server - Overall server stats
/stats channel #channel-name - Channel activity
/stats member @user - Individual stats
/stats messages - Message analytics
/stats growth - Member growth chart
```

### Dashboard setup

1. Go to statbot.net/dashboard
2. Select your server
3. Configure tracking preferences
4. Set up weekly report DM

### Metrics to track

- Daily active members
- Messages per day
- Peak activity hours
- Most active channels
- Member retention (7/30/90 day)

---

## Custom bot commands (using Carl-bot)

### Information commands

```
!tag create faq
[Post the command response here - FAQ content]
```

Usage: `!faq` returns the FAQ

### Useful tags to create

**!resources**
```
Here are the key resources:
- Getting started guide: [link]
- FAQ: [link]
- App download: [link]
- Support: #questions
```

**!rules**
```
Quick rules reminder:
1. Be respectful
2. No spam or self-promo
3. Keep it on topic
4. Help others when you can
5. Have fun

Full rules: #rules
```

**!challenge**
```
Current challenge: [Challenge name]
Duration: [dates]
How to participate: [instructions]
Check-ins: #challenge-check-ins
```

---

## Streak tracking bot

### Option 1: MEE6 Levels as proxy

Not true streaks, but XP leveling creates similar engagement.

### Option 2: Custom streak bot (Statbot Pro)

Track:
- Daily login streaks
- Posting streaks
- Challenge completion streaks

### Option 3: Manual tracking

Create a #streak-check-in channel:
1. Members post daily check-in
2. Moderator maintains Google Sheet
3. Weekly streak updates posted

**Check-in format:**
```
Day [X] check-in:
- What I did today:
- Tomorrow's goal:
```

---

## Event bot (Apollo)

### Installation

1. Go to apollo.fyi
2. Add to Discord
3. Authorize

### Creating events

```
/event create
Title: Weekly Hangout
Description: Casual voice chat - bring your questions
Channel: #events
Date: Every Saturday 2PM EST
Duration: 1 hour
```

### RSVP tracking

Apollo automatically:
- Creates event thread
- Sends reminders (24h, 1h before)
- Tracks RSVPs
- Shows attendance

---

## Support ticket bot (Ticket Tool)

### Installation

1. Go to tickettool.xyz
2. Add to Discord
3. Configure panel

### Setup

Create ticket panel in #support:
```
Need help? Click the button below to open a private support ticket.

A team member will respond within 24 hours.
```

### Ticket categories

- General question
- Technical issue
- Billing/subscription
- Feature request
- Report a problem

---

## Moderation commands quick reference

### MEE6

| Command | Action |
|---------|--------|
| !warn @user reason | Issue warning |
| !mute @user time | Temp mute |
| !unmute @user | Remove mute |
| !kick @user reason | Kick from server |
| !ban @user reason | Ban from server |
| !clear 50 | Delete last 50 messages |

### Carl-bot

| Command | Action |
|---------|--------|
| !warn @user reason | Issue warning |
| !mute @user 1h reason | Temp mute |
| !kick @user reason | Kick |
| !ban @user reason | Ban |
| !slowmode #channel 30 | Set slowmode |
| !lock #channel | Lock channel |
| !unlock #channel | Unlock channel |

### Dyno

| Command | Action |
|---------|--------|
| ?warn @user reason | Warn |
| ?mute @user 1h | Mute |
| ?kick @user | Kick |
| ?ban @user | Ban |
| ?note @user note | Add mod note |
| ?warnings @user | View warnings |

---

## Automation sequences

### New member welcome flow

```
Trigger: Member joins

1. Carl-bot: Assign @Member role
2. MEE6: Send welcome DM
3. MEE6: Post welcome in #welcome

After reaction in #welcome:
4. Carl-bot: Assign @Verified role
5. Carl-bot: Send "getting started" DM

After first post in #introductions:
6. Mod manually verifies + welcomes
```

### Win celebration automation

```
Trigger: Post in #wins containing "streak"

1. Auto-react with celebration emojis
2. If contains "100 days" - ping @Moderator to feature
```

### Inactivity re-engagement

```
Trigger: Member inactive 14 days

1. Send DM: "We miss you! Here's what's happened..."
2. Include recent wins, challenges
3. Invite back to participate
```

---

## Bot troubleshooting

### Bot not responding

1. Check bot is online (green dot)
2. Verify bot has permissions in channel
3. Check command prefix is correct
4. Review bot dashboard for errors

### Permissions issues

Ensure bot role is:
1. Above roles it needs to manage
2. Has required permissions enabled
3. Not blocked by channel overwrites

### Common fixes

- Re-invite bot with correct permissions
- Move bot role higher in hierarchy
- Check channel-specific permission overwrites
- Review audit log for recent changes
