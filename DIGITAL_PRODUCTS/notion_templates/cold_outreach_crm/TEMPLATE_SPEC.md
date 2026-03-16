# Cold Outreach CRM: Template Specification

## Overview
6 interconnected databases purpose-built for cold outreach (email and DM). Pipeline tracking, email templates, follow-up automation, revenue tracking, analytics, and lead scoring.

---

## Database 1: Lead Pipeline (Master Database)

### Properties

| Property | Type | Details |
|----------|------|---------|
| Lead Name | Title | Contact name |
| Company | Text | Company name |
| Email | Email | Contact email |
| LinkedIn | URL | LinkedIn profile URL |
| Twitter/X | Text | @handle |
| Phone | Phone | Phone number (optional) |
| Stage | Select | Options: New, Contacted, Replied, Booked, Closed, Dead |
| Platform | Select | Options: Cold Email, X DM, LinkedIn DM, Instagram DM, WhatsApp, Other |
| Lead Source | Select | Options: Manual Research, Scraper, Referral, Inbound, List Purchase, LinkedIn Search, X Search |
| ICP Match | Select | Options: Perfect Match, Good Match, Partial Match, Mismatch |
| Industry | Select | User-defined. Pre-loaded: SaaS, Agency, E-commerce, Consulting, Creator, Local Business, Finance, Health/Fitness |
| Company Size | Select | Options: Solo, 2-10, 11-50, 51-200, 200+ |
| Deal Value | Number (currency $) | Estimated or actual deal value |
| First Contact Date | Date | When you first reached out |
| Last Contact Date | Date | Most recent touchpoint |
| Follow-up Date | Date | When to follow up next |
| Follow-up Count | Number | How many times you've followed up |
| Response Time | Formula | `if(not empty(prop("Last Contact Date")) and not empty(prop("First Contact Date")) and prop("Stage") != "New", dateBetween(prop("Last Contact Date"), prop("First Contact Date"), "days"), 0)` |
| Days Since Contact | Formula | `if(not empty(prop("Last Contact Date")), dateBetween(now(), prop("Last Contact Date"), "days"), if(not empty(prop("First Contact Date")), dateBetween(now(), prop("First Contact Date"), "days"), 999))` |
| Overdue Follow-up | Formula | `if(not empty(prop("Follow-up Date")) and now() > prop("Follow-up Date") and prop("Stage") != "Closed" and prop("Stage") != "Dead", true, false)` |
| Lead Score | Formula | See Lead Scoring section below |
| Temperature | Formula | `if(prop("Lead Score") >= 8, "Hot", if(prop("Lead Score") >= 5, "Warm", "Cold"))` |
| Email Template Used | Relation → Email Templates | Which template was sent |
| Linked Revenue | Relation → Revenue Tracker | Revenue from this lead (if closed) |
| Notes | Text (long) | Communication log, context, objections, personal details |
| Tags | Multi-select | User-defined custom tags |
| Meeting Link | URL | Calendly/Cal.com link for booked meetings |
| Meeting Date | Date | When the meeting is scheduled |
| Rejection Reason | Select | Options: No Reply, Not Interested, Bad Timing, No Budget, Wrong Person, Competitor, Other (only used when Stage = Dead) |
| Created | Created time | Auto-populated |

### Lead Score Formula
```
(ICP Match == "Perfect Match" ? 3 : ICP Match == "Good Match" ? 2 : 1) +
(Stage == "Replied" ? 3 : Stage == "Booked" ? 4 : Stage == "Contacted" ? 1 : 0) +
(Follow-up Count >= 3 and Stage != "Dead" ? 1 : 0) +
(Days Since Contact < 3 ? 2 : Days Since Contact < 7 ? 1 : 0)
```
Max score: 10. Hot: 8+, Warm: 5-7, Cold: 0-4.

### Views

1. **Pipeline Board** (Board/Kanban) - Grouped by Stage. Cards show Lead Name, Company, Deal Value, Temperature pill. Column counts and sum of Deal Value per stage.
2. **All Leads** (Table) - No filter. Sorted by Lead Score descending. All columns visible.
3. **Today's Follow-ups** (Table) - Filter: Follow-up Date = today. Sorted by Lead Score descending. Shows Lead Name, Company, Follow-up Count, Notes, Email Template Used.
4. **Overdue Follow-ups** (Table) - Filter: Overdue Follow-up = true. Sorted by Follow-up Date ascending (oldest overdue first). Red-flagged.
5. **Hot Leads** (Table) - Filter: Temperature = Hot. Sorted by Lead Score descending.
6. **Dead Leads** (Table) - Filter: Stage = Dead. Grouped by Rejection Reason. Archive of lost leads with reasons.
7. **By Source** (Table) - Grouped by Lead Source. Shows count per source and total Deal Value per source.
8. **By Platform** (Table) - Grouped by Platform. Shows count and conversion metrics per platform.
9. **Booked Meetings** (Calendar) - Filter: Stage = Booked. Calendar view by Meeting Date.
10. **New Leads** (Table) - Filter: Stage = New. Sorted by Created descending. Leads you haven't contacted yet.

---

## Database 2: Email Templates

### Properties

| Property | Type | Details |
|----------|------|---------|
| Template Name | Title | e.g., "Initial Outreach - Value First" |
| Category | Select | Options: Initial Outreach, Follow-up, Meeting Request, Post-Call, Re-engagement, Breakup |
| Subject Line | Text | Email subject line with [PERSONALIZATION] placeholders |
| Body | Text (long) | Full email body with [FIRST NAME], [COMPANY], [PAIN POINT] placeholders |
| Personalization Notes | Text | What to customize before sending |
| When to Use | Text | Scenario description |
| Expected Reply Rate | Number (%) | Industry benchmark or your actual data |
| Actual Reply Rate | Formula | Calculated from linked leads (replied / total sent using this template) |
| Times Sent | Rollup | Count of Lead Pipeline entries using this template |
| Replies Received | Rollup | Count where Stage >= Replied and template matches |
| Platform | Select | Options: Email, LinkedIn, X DM, Instagram DM |
| Tone | Select | Options: Professional, Casual, Direct, Friendly |
| Length | Select | Options: Short (<50 words), Medium (50-100), Long (100+) |

### Pre-loaded Templates (12)

**Initial Outreach (3):**

1. **Direct Outreach**
```
Subject: quick question about [COMPANY]'s [SPECIFIC THING]

hey [FIRST NAME],

noticed [COMPANY] is [SPECIFIC OBSERVATION]. I help [ICP DESCRIPTION] [SPECIFIC RESULT] in [TIMEFRAME].

recently helped [SIMILAR COMPANY] [SPECIFIC RESULT WITH NUMBER].

worth a 15-min call this week?

[YOUR NAME]
```
- When to use: When you have a specific observation about their business
- Expected reply rate: 5-8%

2. **Value-First Outreach**
```
Subject: [SPECIFIC THING] for [COMPANY]

[FIRST NAME],

I put together a quick [AUDIT/ANALYSIS/RECOMMENDATION] for [COMPANY]'s [AREA].

[2-3 SPECIFIC FINDINGS OR SUGGESTIONS]

no pitch. just thought you'd find it useful.

if any of this resonates, happy to walk through it.

[YOUR NAME]
```
- When to use: When you can provide upfront value
- Expected reply rate: 8-12%

3. **Mutual Connection**
```
Subject: [MUTUAL CONNECTION] suggested I reach out

hey [FIRST NAME],

[MUTUAL CONNECTION] mentioned you might be looking for help with [PAIN POINT].

I [WHAT YOU DO] for [ICP TYPE]. recently worked with [SIMILAR COMPANY] on [SIMILAR PROBLEM] - [RESULT].

open to a quick chat?

[YOUR NAME]
```
- When to use: When you have a referral or mutual connection
- Expected reply rate: 15-25%

**Follow-up Sequence (3):**

4. **Bump (Day 3)**
```
Subject: re: [ORIGINAL SUBJECT]

[FIRST NAME],

just bumping this up. know you're busy.

quick version: I help [ICP] [RESULT]. thought [COMPANY] could benefit.

15 minutes. this week or next?

[YOUR NAME]
```

5. **New Angle (Day 7)**
```
Subject: thought of [COMPANY] when I saw this

[FIRST NAME],

saw [RELEVANT INDUSTRY NEWS/DATA/TREND] and thought of [COMPANY].

[1-2 SENTENCES CONNECTING THE NEWS TO THEIR BUSINESS]

might be worth discussing how this affects [THEIR SPECIFIC AREA].

[YOUR NAME]
```

6. **Breakup (Day 14)**
```
Subject: closing the loop

[FIRST NAME],

I've reached out a couple times about [TOPIC]. no worries if the timing isn't right.

I'll close this loop, but if [PAIN POINT] becomes a priority later, here's my calendar: [LINK]

[YOUR NAME]
```

**Meeting Request (2):**

7. **Soft Ask**
```
Subject: quick question

[FIRST NAME],

would it make sense to spend 15 minutes discussing [SPECIFIC TOPIC]?

I work with [2-3 SIMILAR COMPANIES] on [WHAT YOU DO]. happy to share what's working for them.

here's my calendar if it's easier: [LINK]

[YOUR NAME]
```

8. **Direct Ask**
```
Subject: 15 min this week?

[FIRST NAME],

based on [SPECIFIC REASON], I think we should talk.

I can share how [SIMILAR COMPANY] [ACHIEVED RESULT] using [YOUR APPROACH].

available [DAY] at [TIME] or [DAY] at [TIME]?

[YOUR NAME]
```

**Post-Call (2):**

9. **Proposal Follow-up**
```
Subject: [COMPANY] x [YOUR COMPANY] - next steps

[FIRST NAME],

great talking today. as discussed:

- [KEY POINT 1]
- [KEY POINT 2]
- [KEY POINT 3]

I'll have the [PROPOSAL/SCOPE/QUOTE] over by [DATE].

anything I missed?

[YOUR NAME]
```

10. **Check-in**
```
Subject: checking in on [PROJECT/PROPOSAL]

[FIRST NAME],

wanted to check in on the [PROPOSAL/QUOTE] I sent [DATE].

any questions I can answer? happy to hop on a quick call to walk through anything.

[YOUR NAME]
```

**Re-engagement (2):**

11. **New Offer**
```
Subject: something new at [YOUR COMPANY]

[FIRST NAME],

we chatted [TIMEFRAME] ago about [TOPIC]. timing wasn't right then.

since then I've [NEW DEVELOPMENT/CASE STUDY/OFFER].

thought of [COMPANY] because [SPECIFIC REASON].

worth revisiting?

[YOUR NAME]
```

12. **Social Proof**
```
Subject: [SIMILAR COMPANY] just hit [MILESTONE]

[FIRST NAME],

remember when we discussed [TOPIC]?

just helped [SIMILAR COMPANY] [ACHIEVE SPECIFIC RESULT].

[COMPANY] has similar [CHARACTERISTICS]. could see similar results.

open to a quick call?

[YOUR NAME]
```

### Views

1. **All Templates** (Table) - Grouped by Category. Shows template name, subject line, expected reply rate, times sent.
2. **By Category** (Board) - Grouped by Category. Card shows template name and expected reply rate.
3. **Best Performers** (Table) - Sorted by Actual Reply Rate descending. Shows real performance data.
4. **By Platform** (Table) - Grouped by Platform. For DM-specific templates.

---

## Database 3: Follow-up Scheduler

This is implemented as filtered views of Lead Pipeline, not a separate database.

### Dedicated Page: Follow-up Command Center

**Section 1: Today's Follow-ups**
Linked view from Lead Pipeline:
- Filter: Follow-up Date = today
- Sorted by Lead Score descending (work hottest leads first)
- Columns: Lead Name, Company, Stage, Follow-up Count, Email Template Used, Notes

**Section 2: Overdue Follow-ups**
Linked view:
- Filter: Overdue Follow-up = true
- Sorted by Follow-up Date ascending
- Red indicator on days overdue

**Section 3: This Week's Schedule**
Linked view:
- Filter: Follow-up Date = this week
- Grouped by day
- Shows daily follow-up load

**Section 4: Follow-up Cadence Guide (Static content)**
```
Recommended follow-up intervals:
- After initial outreach: 3 days
- After first follow-up: 4 days (Day 7 total)
- After second follow-up: 7 days (Day 14 total)
- After third follow-up: 14 days (Day 28 total)
- After fourth follow-up: 30 days (Day 58 total) - breakup email

Max follow-ups per lead: 5
After 5 with no reply: move to Dead with reason "No Reply"
```

---

## Database 4: Revenue Tracker

### Properties

| Property | Type | Details |
|----------|------|---------|
| Entry | Title | e.g., "Web design project - Acme Corp" |
| Amount | Number (currency $) | Deal value |
| Close Date | Date | When the deal closed |
| Linked Lead | Relation → Lead Pipeline | Which lead this revenue came from |
| Payment Status | Select | Options: Pending, Partial, Paid, Overdue |
| Payment Date | Date | When payment was received |
| Notes | Text | Invoice number, payment terms, etc. |
| Month | Formula | `formatDate(prop("Close Date"), "YYYY-MM")` |

### Views

1. **Monthly Revenue** (Table) - Grouped by Month. Sum on Amount. Sorted chronologically.
2. **All Deals** (Table) - Sorted by Close Date descending.
3. **Pending Payment** (Table) - Filter: Payment Status = Pending or Overdue.
4. **Revenue by Source** (Table) - Shows Linked Lead > Lead Source. Grouped by source.

### Dashboard Metrics (Calculated on page)

- **Total Revenue (All Time):** Sum of all Amount
- **Revenue This Month:** Sum where Month = current
- **Average Deal Size:** Total Revenue / Count of entries
- **Close Rate:** (Count of Closed leads / Count of Contacted leads) * 100
- **Revenue per Email Sent:** Total Revenue / Total emails sent (from analytics)

---

## Database 5: Outreach Analytics

This is a page with linked views and formula callouts, not a separate database. All data pulls from Lead Pipeline.

### Analytics Page Layout

**Row 1: Key Metrics (4 columns)**
- Total Leads: Count of all Lead Pipeline entries
- Contacted: Count where Stage != New
- Reply Rate: (Replied + Booked + Closed) / Contacted * 100
- Close Rate: Closed / Contacted * 100

**Row 2: Stage Funnel**
Linked view from Lead Pipeline:
- Grouped by Stage
- Count per stage
- Conversion rate between each stage (formula callouts)
```
New (247) → Contacted (198) [80% contact rate]
Contacted (198) → Replied (34) [17% reply rate]
Replied (34) → Booked (18) [53% book rate]
Booked (18) → Closed (11) [61% close rate]
```

**Row 3: Performance by Template**
Linked view from Email Templates:
- Shows Times Sent, Replies Received, Actual Reply Rate
- Sorted by Actual Reply Rate descending
- Identifies best and worst templates

**Row 4: Performance by Lead Source**
Linked view from Lead Pipeline:
- Grouped by Lead Source
- Count, reply rate, close rate per source
- Identifies best lead sources

**Row 5: Performance by Platform**
Same structure, grouped by Platform (email vs DM channels)

**Row 6: Time Analysis**
- Average days from first contact to reply
- Average days from reply to booked
- Average days from booked to closed
- Total average sales cycle length

---

## Database 6: Lead Scoring Configuration

This is a reference page, not a database. Documents the scoring logic so the user can adjust thresholds.

### Scoring Criteria (Static content block)

```
LEAD SCORE (0-10 scale):

ICP Match (0-3 points):
  Perfect Match: 3
  Good Match: 2
  Partial Match: 1
  Mismatch: 0

Stage Progression (0-4 points):
  New: 0
  Contacted: 1
  Replied: 3
  Booked: 4

Engagement Signals (0-2 points):
  3+ follow-ups without going Dead: 1
  Responded within 3 days: 2
  Responded within 7 days: 1

TEMPERATURE:
  Hot (8-10): Work these leads first. High intent.
  Warm (5-7): Promising. Keep following up.
  Cold (0-4): Low priority. Batch process.
```

---

## Cross-Database Relations Map

```
Lead Pipeline ←→ Email Templates (template tracking)
Lead Pipeline ←→ Revenue Tracker (closed deal revenue)
```

Simpler relation structure than other templates because this is a focused, single-purpose tool.

---

## Late Payment Follow-up Templates (Static content in Revenue Tracker page)

```
POLITE NUDGE (3 days overdue):
Subject: invoice #[NUMBER] - quick reminder

hey [FIRST NAME],

just a quick reminder that invoice #[NUMBER] for $[AMOUNT] was due [DATE].

no rush if it's already in process. just wanted to make sure it didn't slip through the cracks.

payment details are in the original invoice. let me know if you need me to resend.

[YOUR NAME]

---

FIRM REMINDER (7 days overdue):
Subject: invoice #[NUMBER] - 7 days overdue

[FIRST NAME],

following up on invoice #[NUMBER] for $[AMOUNT], now 7 days past due.

could you confirm when I can expect payment? happy to discuss if there are any issues with the invoice.

[YOUR NAME]

---

FINAL NOTICE (14 days overdue):
Subject: invoice #[NUMBER] - payment needed

[FIRST NAME],

invoice #[NUMBER] for $[AMOUNT] is now 14 days overdue.

I need to resolve this by [DATE - 7 days from now]. please let me know the status.

if there's an issue with the amount or scope, I'm open to discussing. but I do need a response.

[YOUR NAME]
```

---

## Setup Instructions

1. Duplicate this template to your Notion workspace
2. Review the 12 email templates - customize [YOUR NAME], [YOUR COMPANY], [WHAT YOU DO] placeholders
3. Set your ICP criteria in the Lead Scoring configuration page
4. Import existing leads (CSV import into Lead Pipeline)
5. Or start adding leads manually as you research
6. Set follow-up dates as you send outreach
7. Check the Follow-up Command Center every morning
8. After calls/meetings, update the Stage and add Notes
9. When deals close, create Revenue Tracker entries
10. Review Analytics page weekly to optimize

Time to setup: 10 minutes (plus template customization)
