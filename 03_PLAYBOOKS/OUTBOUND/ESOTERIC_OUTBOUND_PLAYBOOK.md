# Esoteric Outbound Playbook

**Last Updated:** 2026-01-23
**Source:** @pipelineabuser (Caiden), @seanb2b, @caiden_cole + high-signal outbound alpha
**Status:** Ready for implementation

---

## Philosophy

Most people do cold email wrong. They start with volume and automation, when they should start with:
1. Deliverability
2. Offer
3. Messaging
4. Process
5. THEN scale

This playbook covers the unconventional, esoteric lead gen tactics that actually work in 2026.

---

# SECTION 1: INTELLIGENCE-LED LEAD GEN

## 1.1 LinkedIn Customer Mining

**Source:** @pipelineabuser

**The Tactic:**
LinkedIn literally shows you competitor customer lists if you know where to look.

**How it works:**

```
1. Go to competitor's LinkedIn company page
2. Click "People"
3. Filter by "Customer Success" or "Account Manager"
4. Look at who those employees are connected to
5. Those connections = their book of business
6. Cross-reference with people who engage on competitor posts
```

**Why it works:**
- Customer Success managers connect with their accounts
- Account Managers maintain relationships via LinkedIn
- Post engagers are active customers showing pain

**Execution:**

1. **List 5 direct competitors**
2. **For each competitor:**
   - Find their LinkedIn page
   - Note CS/AM employees
   - Export their connections (Sales Nav or manual)
3. **Cross-reference:**
   - Who engages on competitor posts?
   - Who comments with questions/complaints?
   - Who tags competitors in posts?
4. **Build prospect list from overlaps**

**Tools needed:**
- LinkedIn (free or Sales Navigator)
- Spreadsheet for tracking
- Apollo or similar for email enrichment

---

## 1.2 FOIA Lead Gen for Government Sales

**Source:** @pipelineabuser

**The Tactic:**
File FOIA requests to get competitor customer lists, pricing, and contract details. It's free and government must respond.

**How it works:**

```
1. Go to USAspending.gov
   - Shows who won federal contracts
   - Total values, award dates, agencies

2. File FOIA request for details:
   - Vendor names
   - Contract values
   - Award dates
   - Losing bidders (!)
   - Sometimes: winning proposals
   - Evaluation criteria
   - Budget breakdowns

3. Now you know:
   - Exactly who to call
   - What they're paying
   - When contracts renew
   - Who's hungry after losing
```

**Why it works:**
- Public record - government must respond
- Most people don't do this (feels like work)
- It's literally just a form
- Losing bidders are HUNGRY and receptive

**Execution:**

1. **Research your space:**
   ```
   USAspending.gov > Advanced Search >
   Filter by: Agency, NAICS code, keywords
   ```

2. **Identify targets:**
   - Contract renewals in next 6-12 months
   - Losing bidders from recent awards
   - Agencies with budget increases

3. **File FOIA:**
   ```
   Each agency has FOIA office
   Use template: "Request for vendor contract documents,
   evaluation criteria, and unsuccessful proposals for
   [Contract Number/Name]"
   ```

4. **Outreach to losers:**
   ```
   Subject: Saw you bid on [contract]

   Hey [Name],

   Noticed [Company] was in the running for [contract].

   We help companies like yours [benefit] which often
   makes the difference in competitive bids.

   Worth a 15-min call to discuss your next bid?
   ```

**Timeline:** FOIA responses take 20-30 days. Plan ahead.

---

## 1.3 Change Detection Intelligence

**Source:** @pipelineabuser mentions visualping.io approach

**The Tactic:**
Monitor competitor websites for changes that signal buying intent or opportunity.

**What to monitor:**

```
PRICING PAGES:
- They raise prices → their customers might switch
- They drop prices → they're desperate, their customers are unhappy

CAREERS PAGES:
- Hiring sales = expanding
- Hiring engineers = building features you might have
- Laying off = budget cuts, need cheaper alternatives

LEADERSHIP PAGES:
- New CEO/CTO = strategic shifts
- New VP Sales = new targets
- Departures = instability

PRODUCT PAGES:
- Feature launches = what they think matters
- Feature removals = what's failing
- Integrations = who they partner with
```

**Tools:**
- Visualping.io ($0-13/mo)
- Distill.io (free tier)
- ChangeTower
- Custom n8n workflow

**Execution:**

1. **Set up monitors for 10 competitors:**
   - Pricing page
   - Careers page
   - Product/features page
   - Leadership/about page

2. **Create alert workflow:**
   ```
   Change detected →
   Evaluate significance →
   Add to outreach queue with context
   ```

3. **Outreach based on change:**
   ```
   PRICING INCREASE:
   "Saw [Competitor] raised prices again.
   Happy with what you're getting?"

   LEADERSHIP CHANGE:
   "Congrats on the new [role].
   Usually a good time to evaluate vendors."

   FEATURE REMOVAL:
   "Noticed [Competitor] sunset [feature].
   That's actually our specialty."
   ```

---

## 1.4 Job Posting Intelligence

**Source:** Multiple high-signal accounts

**The Tactic:**
Companies hiring for roles your product replaces = qualified leads.

**Signals:**

```
HIRING SALES OPS → Need CRM/automation
HIRING DATA ANALYST → Need analytics tool
HIRING CONTENT WRITER → Need AI writing tool
HIRING EMAIL MARKETER → Need email platform
HIRING SOCIAL MEDIA → Need scheduling tool
```

**How it works:**

1. **Monitor job boards:**
   - Indeed API
   - LinkedIn Jobs
   - BuiltIn
   - AngelList/Wellfound

2. **Filter for relevant roles:**
   ```
   "Marketing Automation" → Sell automation tool
   "Cold Email Specialist" → Sell email platform
   "Content Manager" → Sell AI writing
   ```

3. **Outreach to hiring manager:**
   ```
   Subject: Saw you're hiring for [role]

   Hey [Name],

   Noticed [Company] is hiring a [role].

   Before you spend $80k/year on salary + benefits,
   wanted to share how [Product] does [X] of that job
   for $[monthly cost]/month.

   Might still make sense to hire, but could save
   the new hire 20 hours/week.

   Worth a look?
   ```

**Tools:**
- Apollo job change alerts
- LinkedIn recruiter activity
- Custom scraper (Apify/Phantombuster)

---

## 1.5 Review Mining

**Source:** GTM_REVENUE_INTELLIGENCE.md CH022

**The Tactic:**
Monitor competitor reviews. Unhappy customers = warm leads.

**Where to monitor:**

```
B2B:
- G2.com
- Capterra
- TrustRadius
- GetApp

B2C/Apps:
- App Store reviews
- Google Play reviews
- ProductHunt comments

General:
- Twitter mentions/complaints
- Reddit threads
- Hacker News
```

**Signals to watch:**

```
1-2 STAR REVIEWS:
"Support is terrible" → Outreach about better support
"Missing [feature]" → If you have it, lead with that
"Too expensive" → Lead with pricing
"Buggy/slow" → Lead with reliability

REDDIT COMPLAINTS:
"[Competitor] alternative?" → Jump in with value
"Problems with [Competitor]" → DM the poster
```

**Outreach template:**

```
Subject: Saw your review of [Competitor]

Hey [Name],

Read your G2 review of [Competitor] - especially the part
about [specific complaint].

We built [Product] specifically because [Competitor]
[has that problem]. [One sentence on how you solve it.]

Would you be open to a 15-min demo? No commitment,
just want to show you how we handle [their pain point].

[Name]
```

---

# SECTION 2: UNCONVENTIONAL CHANNELS

## 2.1 Voice Note Outbound

**Source:** @pipelineabuser

**The Tactic:**
```
"the best outbound campaigns i've seen recently aren't even cold email
they're cold dm → voice note → email followup
the voice note is doing stupid numbers rn"
```

**Why it works:**
- Pattern interrupt (nobody sends voice notes)
- Builds trust faster (they hear your voice)
- Harder to ignore than text
- Shows effort

**Channel flow:**

```
Day 1: LinkedIn DM with value hook
Day 2: Voice note (60s max) via LinkedIn
Day 3: Email followup referencing voice note
Day 5: Second voice note if no response
Day 7: Final email with calendar link
```

**Voice note script (60 seconds max):**

```
"Hey [Name], it's [You] from [Company].

Saw you're [role] at [Company] and wanted to
share something quick.

[One specific observation about their business]

We help companies like yours [specific result].
Just helped [similar company] [specific outcome].

Would love to chat for 15 minutes and see if
we can help. I'll drop you an email with some times.

Talk soon!"
```

**Where to send:**
- LinkedIn voice messages
- Instagram voice DMs
- Twitter voice DMs (limited)
- WhatsApp if you have number

---

## 2.2 Loom Video Prospecting

**Source:** @alexberman, GTM doc

**The Tactic:**
Personalized Loom videos in cold email. Getting 40%+ reply rates for high-value deals.

**When to use:**
- Deals $10k+
- Named accounts
- Hard-to-reach prospects
- After no response to text emails

**Video structure (60s max):**

```
0-10s: Show their website/LinkedIn on screen
"Hey [Name], looking at [Company] here..."

10-30s: Specific observation
"Noticed you're [doing X] but [problem]..."

30-50s: Your solution
"What we do at [Company] is [specific solution]..."

50-60s: CTA
"Would love to show you how. Link below to book 15 mins."
```

**Pro tips:**
- Thumbnail shows their name/company
- Keep under 60 seconds
- Show their stuff on screen (proves it's custom)
- Add calendar link in email below video

**Tools:**
- Loom (free tier works)
- Vidyard
- Sendspark

---

## 2.3 Event & Conference Hijacking

**The Tactic:**
Target attendees of industry conferences before, during, and after.

**Pre-event (2 weeks before):**

```
1. Get attendee list (often public or purchasable)
2. Find speakers on event website
3. Research exhibitors
4. Outreach: "See you at [Event]?"
```

**During event:**

```
1. Monitor event hashtag
2. Engage with attendee posts
3. DM people posting from event
4. "Saw your post about [topic]. We should connect."
```

**Post-event (within 3 days):**

```
Subject: Following up from [Event]

Hey [Name],

Saw you were at [Event] too.

[Reference something specific - a talk, booth, etc.]

We help [audience] with [problem]. Seemed relevant
to what [Company] is doing.

Worth a 15-min call this week?

[Name]
```

---

## 2.4 Podcast Guest Prospecting

**The Tactic:**
Target podcast guests in your niche. They're thought leaders, have budget, and are accessible.

**How it works:**

```
1. Find podcasts in your niche
2. Check recent guest lists
3. Those guests are:
   - Decision makers (invited to share expertise)
   - Active thought leaders (want visibility)
   - Often have budget (successful enough to be invited)

4. Outreach references their episode
```

**Outreach template:**

```
Subject: Loved your episode on [Podcast]

Hey [Name],

Just listened to your episode on [Podcast] about [topic].
The part about [specific insight] really resonated.

Actually building something in that space - [Product]
helps [audience] with [exact thing they discussed].

Would love to get your take on it. 15 mins?

[Name]
```

**Where to find guests:**
- Apple Podcasts (check episode descriptions)
- Listen Notes (podcast search engine)
- Spotify (episode details)
- Podcast host Twitter (they tag guests)

---

# SECTION 3: TIMING-BASED TRIGGERS

## 3.1 Funding Trigger

**The Tactic:**
Companies that just raised have money to spend and mandates to grow.

**Timing:** Outreach 1-2 weeks after funding announcement

**Where to find:**
- Crunchbase (free tier)
- TechCrunch
- PitchBook (paid)
- Twitter (founders announce)
- Product Hunt launches

**Outreach template:**

```
Subject: Congrats on the round!

Hey [Name],

Saw [Company] just closed your [Series X]. Congrats!

Usually after funding, teams are looking to
[scale marketing / hire faster / automate ops].

We help companies like yours [specific result].
Just worked with [similar company post-funding].

Worth a quick call to see if we can help deploy
some of that capital effectively?

[Name]
```

---

## 3.2 New Hire Trigger

**The Tactic:**
New hires in relevant roles are eager to make changes and prove themselves.

**Target roles:**
- New VP Marketing = new tools budget
- New Head of Sales = new tech stack
- New CEO = strategic overhaul
- New IT Director = infrastructure changes

**Timing:** First 30-90 days in role

**Where to find:**
- LinkedIn job changes (Sales Navigator alerts)
- Apollo job change alerts
- Press releases (leadership changes)

**Outreach template:**

```
Subject: Congrats on the new role

Hey [Name],

Saw you just started as [Role] at [Company].
Congrats on the move!

In my experience, the first 90 days are when
[specific challenge for role] is top priority.

We help [new role type] at companies like [Company]
[specific result] in their first quarter.

Worth a 15-min call to share some quick wins?

[Name]
```

---

## 3.3 Contract Renewal Trigger

**The Tactic:**
Target companies 60-90 days before their contracts with competitors renew.

**How to find renewal dates:**
- FOIA requests (government)
- Ask in sales calls ("When does your current contract end?")
- Industry standard terms (annual, 2-year)
- G2/Capterra reviews mention start dates

**Outreach template:**

```
Subject: Before your [Competitor] renewal

Hey [Name],

Not sure when your [Competitor] contract renews,
but wanted to plant a seed before you auto-renew.

A few things that might matter:
- [Your differentiator 1]
- [Your differentiator 2]
- [Pricing advantage]

Would you be open to a 15-min comparison call
before you sign another year?

[Name]
```

---

# SECTION 4: MULTI-CHANNEL SEQUENCES

## 4.1 The Surround Sequence

**Flow:**

```
Day 1: LinkedIn connection request + note
Day 2: LinkedIn DM with value
Day 3: Cold email
Day 5: LinkedIn voice note
Day 7: Second email
Day 10: Twitter follow + engage with their content
Day 12: Third email (breakup)
Day 14: Final LinkedIn message
```

**Why it works:**
- They see your name everywhere
- Multi-touch increases response rate
- Each channel hits differently
- Shows persistence (valued in sales)

---

## 4.2 The Reference Sequence

When you have mutual connections or shared experiences.

```
Email 1:
"[Mutual connection] mentioned you're dealing with [problem].
They thought we should connect."

Email 2:
"Following up - [Mutual] said [specific thing about prospect].
Want to share how we helped them with the same."

Email 3:
"Last note - happy to loop in [Mutual] if helpful.
Just 15 mins to see if there's fit."
```

---

# SECTION 5: COLD EMAIL STACK 2026

**Source:** @pipelineabuser, @seanb2b, @caiden_cole

## Priority Order (Do NOT Skip Steps)

```
1. DELIVERABILITY - Can emails even reach inbox?
2. OFFER - Does anyone want what you're selling?
3. MESSAGING - Does copy match offer to ICP?
4. PROCESS - Reply handling, follow-ups, tracking
5. SCALE - Then and only then: volume, automation, VAs
```

Most people start at 5. That's why they fail.

## Modern Stack

| Component | Tool | Cost |
|-----------|------|------|
| Enrichment + Intent | Clay | $150/mo |
| Contact Data | Apollo | $49/mo |
| Sending | Instantly | $30/mo |
| Warmup | Built into Instantly | $0 |
| CRM | Close.com or HubSpot | $0-50/mo |

## Key 2026 Shifts

1. **Intent signals > spray and pray**
   - Who's hiring, raising, searching, reviewing competitors?

2. **AI does 80% of research**
   - Use Clay/AI to find relevant triggers
   - Human reviews and approves personalization

3. **Dedicated IPs only**
   - Shared IPs are dead
   - Warmup 14-21 days minimum

4. **Plain text > HTML**
   - Strip formatting
   - Send from real names, not "Company Team"

5. **First email matters most**
   - 58% of replies come from first email
   - Don't save your best for follow-ups

---

# SECTION 6: MEASUREMENT & OPTIMIZATION

## Key Metrics

| Metric | Target | Elite |
|--------|--------|-------|
| Open Rate | 40%+ | 60%+ |
| Reply Rate | 3%+ | 10%+ |
| Positive Reply | 1%+ | 5%+ |
| Meeting Booked | 0.5%+ | 2%+ |

## Weekly Review

```
1. Check deliverability (any inbox warnings?)
2. Review reply quality (positive vs negative)
3. A/B test results (subject, hook, CTA)
4. Prospect quality (are right people responding?)
5. Process efficiency (reply speed, follow-up gaps)
```

## Kill Criteria

Stop a campaign if:
- Open rate < 20% (deliverability issue)
- Reply rate < 1% after 500 sends (offer/list issue)
- All replies negative (messaging issue)
- No meetings after 10 positive replies (process issue)

---

# QUICK REFERENCE: ESOTERIC TACTICS

| Tactic | Effort | ROI | Best For |
|--------|--------|-----|----------|
| LinkedIn Customer Mining | Low | High | B2B sales |
| FOIA Lead Gen | Medium | High | Government sales |
| Change Detection | Low | Medium | Competitor displacement |
| Job Posting Intel | Low | High | Replacement sales |
| Review Mining | Low | High | Competitor displacement |
| Voice Note Outbound | Medium | Highest | High-value deals |
| Loom Prospecting | High | Highest | Enterprise deals |
| Funding Trigger | Low | High | Startups/tech |
| New Hire Trigger | Low | High | All B2B |

---

## Resources

- USAspending.gov (government contracts)
- Visualping.io (change detection)
- Clay.com (enrichment + intent)
- Instantly.ai (cold email)
- Apollo.io (contact data)
- Loom.com (video prospecting)
