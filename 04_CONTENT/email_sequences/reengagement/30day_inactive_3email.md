# 30-Day Inactive - Re-engagement Sequence

**Purpose:** Win back subscribers who haven't opened emails in 30+ days
**Trigger:** No email opens in last 30 days
**Works for:** All niches (customize per brand)

---

## Email 1: The check-in

**Send timing:** Day 31 of inactivity
**Segment:** No opens in 30 days

### Subject line
Still interested in [TOPIC]?

**A/B variants:**
- A: Did we lose you?
- B: [FIRST_NAME], quick check-in

### Preview text
Honest question inside

### Body

Hey [FIRST_NAME],

I noticed you haven't opened any emails from [BRAND] in a while.

No guilt trip here. Just checking if you still want to hear from me.

Two options:

**1. Stay subscribed**
Just click here: [I want to stay]

I'll keep sending you [CONTENT_TYPE]. Maybe even send you something good as a thank you for sticking around.

**2. Unsubscribe**
No hard feelings. Click here: [Unsubscribe]

I'd rather have a smaller list of people who actually want to hear from me than a big list of ghosts.

Either way, thanks for being here at some point.

[NAME]
[BRAND]

### CTA button (primary)
I want to stay

### CTA button (secondary)
Unsubscribe me

---

## Email 2: The value reminder

**Send timing:** Day 35 of inactivity (4 days after Email 1)
**Segment:** No opens in 30+ days, didn't click Email 1

### Subject line
Here's what you've missed

**A/B variants:**
- A: Quick catch-up from [BRAND]
- B: 3 things from the past month

### Preview text
In case you want to catch up

### Body

Hey [FIRST_NAME],

Quick summary of what you might have missed:

[NICHE-SPECIFIC SUMMARY]

**For AI niche (StackPilot):**
- The prompt structure that gets better results (copy-paste ready)
- 3 AI tools most solopreneurs can cancel today
- How to batch your AI work to save 2+ hours/week

**For Faith niche (Daily Anchor):**
- The 60-second reset for anxious days
- This week's anchor verse (Psalm 46:10)
- Why most morning routines fail (and what works instead)

**For Fitness niche (3HourPhysique):**
- The 10-minute minimum workout (for busy weeks)
- Why 3 hours/week beats 6 hours/week for most people
- The hand method for nutrition (no calorie counting)

If any of that sounds useful, click here to re-engage: [I'm back]

If not, you can unsubscribe here: [Remove me]

[NAME]

### CTA button (primary)
I'm back

### CTA button (secondary)
Remove me from list

---

## Email 3: The last email

**Send timing:** Day 42 of inactivity (7 days after Email 2)
**Segment:** No opens in 30+ days, didn't engage with Emails 1 or 2

### Subject line
Removing you from the list

**A/B variants:**
- A: Final email from [BRAND]
- B: Cleaning up my list

### Preview text
Unless you click this

### Body

Hey [FIRST_NAME],

This is my last email to you.

You haven't engaged with [BRAND] emails in over a month. I'm going to remove you from the list to keep things clean.

If you want to stay, this is your last chance: [Keep me subscribed]

If you click that link, I'll keep you on the list and send you something good as a thank you.

If I don't hear from you, I'll remove you in 48 hours. No hard feelings. You can always re-subscribe later if you change your mind.

Thanks for being here.

[NAME]

### CTA button
Keep me subscribed

---

## Post-sequence actions

**If they clicked "stay" or "I'm back":**
- Tag as "reengaged_[date]"
- Send welcome-back email with a free resource
- Move back to active nurture sequence
- Monitor engagement for next 30 days

**If no engagement after Email 3:**
- Wait 48 hours
- Move to "inactive" segment
- Stop all regular emails
- Keep on list for annual re-engagement attempt (optional)
- Or remove entirely (recommended for deliverability)

---

## Brand-specific variables

| Variable | AI (StackPilot) | Faith (DailyAnchor) | Fitness (3HourPhysique) |
|----------|-----------------|---------------------|-------------------------|
| BRAND | StackPilot | Daily Anchor | 3-Hour Physique |
| TOPIC | AI workflows | faith + productivity | minimalist fitness |
| CONTENT_TYPE | AI tips and workflows | weekly devotionals | workouts and motivation |
| SENDER | hello@stackpilot.ai | hello@dailyanchor.co | hello@3hourphysique.com |

---

## Welcome-back email (for re-engaged subscribers)

**Send timing:** Immediately after re-engagement click
**Segment:** Clicked "stay" or "I'm back" in re-engagement sequence

### Subject line
Welcome back + a thank you

**A/B variants:**
- A: Thanks for sticking around
- B: Here's something for coming back

### Preview text
Free resource inside

### Body

Hey [FIRST_NAME],

Thanks for clicking. I'm glad you're sticking around.

As a thank you, here's [FREE_RESOURCE]:

**For AI niche:** My top 10 prompts that I use every week (PDF)
**For Faith niche:** A bonus 7-day verse guide on rest (PDF)
**For Fitness niche:** The 15-minute bodyweight routine (video)

Download here: [Get your free resource]

I'll go back to sending you regular [CONTENT_TYPE]. If it ever feels like too much, just reply and let me know. I read everything.

Glad to have you back.

[NAME]

### CTA button
Get your free resource

---

## Sequence metrics to track

| Metric | Target |
|--------|--------|
| Email 1 open rate | 15%+ (they're inactive, so lower is expected) |
| Email 1 re-engagement rate | 5%+ |
| Email 2 re-engagement rate | 3%+ |
| Email 3 re-engagement rate | 2%+ |
| Total re-engagement rate | 8-12% |
| Unsubscribe rate | 5-10% (expected and healthy) |

---

## Automation notes

- Trigger: subscriber has 0 opens in last 30 days
- Use a different "from" name or add "[Important]" to subject for Email 3
- Stop sequence if subscriber opens any other email during this time
- Track re-engaged subscribers separately for 60 days
- If re-engaged subscribers go inactive again within 60 days, remove from list
- Clean up fully inactive subscribers to maintain deliverability

---

## Deliverability impact

Removing inactive subscribers improves:
- Open rates (fewer ghosts in denominator)
- Click rates (same reason)
- Sender reputation (fewer unopened emails)
- Inbox placement (ISPs track engagement)

Don't be afraid to remove people. A smaller, engaged list outperforms a large, dead list.

---

## Alternative: Sunset policy

Instead of re-engagement emails, some brands use automatic sunset:
- 60 days no opens: move to "at risk"
- 90 days no opens: remove automatically

This is simpler but gives no chance for re-engagement. The 3-email sequence is better for most cases.
