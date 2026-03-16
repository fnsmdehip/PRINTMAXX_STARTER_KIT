# Freelance Command Center: Template Specification

## Overview
6 interconnected databases covering the complete freelance business: gig pipeline, proposals, client management, invoices, portfolio, and analytics.

---

## Database 1: Gig Tracker (Master Database)

### Properties

| Property | Type | Details |
|----------|------|---------|
| Gig Name | Title | Project/gig name |
| Client | Relation → Client Database | Which client this gig is for |
| Status | Select | Options: Lead, Proposal Sent, Negotiating, Active, Delivered, Paid, Cancelled |
| Gig Type | Select | Options: Web Development, Design, Content/Copy, Consulting, Marketing, Social Media, Video/Photo, Other |
| Quoted Price | Number (currency $) | What you quoted |
| Final Price | Number (currency $) | What you actually charged (after negotiation) |
| Actual Hours | Number | Hours spent on the gig |
| Hourly Rate | Formula | `if(prop("Actual Hours") > 0 and not empty(prop("Final Price")), round(prop("Final Price") / prop("Actual Hours") * 100) / 100, 0)` |
| Rate vs Target | Formula | `if(prop("Hourly Rate") > 0, if(prop("Hourly Rate") >= 100, "Above Target", if(prop("Hourly Rate") >= 75, "On Target", "Below Target")), "")` (user adjusts target) |
| Deadline | Date | When the gig is due |
| Start Date | Date | When work began |
| Delivered Date | Date | When deliverables were sent |
| Paid Date | Date | When payment was received |
| Days to Complete | Formula | `if(not empty(prop("Delivered Date")) and not empty(prop("Start Date")), dateBetween(prop("Delivered Date"), prop("Start Date"), "days"), 0)` |
| Days to Pay | Formula | `if(not empty(prop("Paid Date")) and not empty(prop("Delivered Date")), dateBetween(prop("Paid Date"), prop("Delivered Date"), "days"), 0)` |
| Overdue | Formula | `if(not empty(prop("Deadline")) and empty(prop("Delivered Date")) and now() > prop("Deadline"), true, false)` |
| Awaiting Payment | Formula | `prop("Status") == "Delivered" and prop("Status") != "Paid"` |
| Source | Select | Options: Upwork, Fiverr, Referral, Cold Outreach, X/Twitter, LinkedIn, Website, Repeat Client, Other |
| Linked Proposal | Relation → Proposal Templates | Which proposal was sent |
| Linked Invoice | Relation → Invoice Tracker | Invoice(s) for this gig |
| Scope | Text (long) | Detailed scope of work |
| Deliverables | Text | List of deliverables |
| Client Satisfaction | Select | Options: 5 Stars, 4 Stars, 3 Stars, 2 Stars, 1 Star, Not Rated |
| Notes | Text (long) | Communication log, changes, issues |
| Created | Created time | Auto |

### Views

1. **Pipeline Board** (Board/Kanban) - Grouped by Status. Cards show Gig Name, Client, Final Price (or Quoted Price), Deadline. Column sums on price.
2. **Active Gigs** (Table) - Filter: Status = Active. Sorted by Deadline ascending. Shows Hours Logged, Deadline, Overdue flag.
3. **Awaiting Payment** (Table) - Filter: Awaiting Payment = true. Shows Delivered Date, Final Price, Days to Pay. Yellow/red urgency indicators.
4. **All Gigs** (Table) - No filter. Sorted by Created descending. Full view.
5. **By Client** (Table) - Grouped by Client relation. Shows gig count, total revenue per client.
6. **By Source** (Table) - Grouped by Source. Count and total revenue per source. Identifies best lead channels.
7. **Monthly Revenue** (Table) - Grouped by month (from Paid Date). Sum of Final Price. Revenue trend.
8. **Calendar** (Calendar) - By Deadline. Shows upcoming delivery dates.
9. **Overdue** (Table) - Filter: Overdue = true. Sorted by Deadline ascending. Red flags.
10. **Rate Analysis** (Table) - Filter: Status = Paid. Shows Hourly Rate, Rate vs Target. Sorted by Hourly Rate descending.

---

## Database 2: Proposal Templates

### Properties

| Property | Type | Details |
|----------|------|---------|
| Proposal Name | Title | e.g., "Web Dev Proposal - [CLIENT]" |
| Template Type | Select | Options: Web Development, Content/Copy, Consulting, Marketing, General Services |
| Status | Select | Options: Template, Draft, Sent, Won, Lost |
| Client | Relation → Client Database | Who received this proposal |
| Linked Gig | Relation → Gig Tracker | Gig created from this proposal (if won) |
| Date Sent | Date | When the proposal was sent |
| Date Response | Date | When client responded |
| Response Time | Formula | `if(not empty(prop("Date Response")) and not empty(prop("Date Sent")), dateBetween(prop("Date Response"), prop("Date Sent"), "days"), 0)` |
| Quoted Amount | Number (currency $) | What you quoted |
| Won | Formula | `prop("Status") == "Won"` |
| Lost Reason | Select | Options: Too Expensive, Chose Competitor, Bad Timing, No Response, Scope Mismatch, Other |
| Notes | Text | Context, objections, feedback |
| Proposal Body | Text (long) | Full proposal text |

### Pre-loaded Templates (5)

Each template is a full page with the following structure:

**Template 1: Web Development / Design**
```
# Proposal: [PROJECT NAME]
## Prepared for [CLIENT NAME] | [DATE]

### About This Project
[2-3 sentences about the client's problem and what you'll build]

### Scope of Work
Phase 1: [Discovery & Planning] - [X days]
- [Deliverable 1]
- [Deliverable 2]

Phase 2: [Design] - [X days]
- [Deliverable 1]
- [Deliverable 2]

Phase 3: [Development] - [X days]
- [Deliverable 1]
- [Deliverable 2]

Phase 4: [Testing & Launch] - [X days]
- [Deliverable 1]
- [Deliverable 2]

### What's NOT Included
- [Out of scope item 1]
- [Out of scope item 2]
(Prevents scope creep. List explicitly.)

### Investment Options

| Package | What's Included | Timeline | Price |
|---------|----------------|----------|-------|
| Basic | [Core features only] | [X weeks] | $[PRICE] |
| Standard | [Core + extras] | [X weeks] | $[PRICE] |
| Premium | [Everything + priority] | [X weeks] | $[PRICE] |

Most clients choose Standard.

### Timeline
- Start date: [DATE] (upon deposit)
- Milestone 1: [DATE]
- Milestone 2: [DATE]
- Completion: [DATE]

### Terms
- 50% deposit to start, 50% on delivery
- 2 rounds of revisions included
- Additional revisions: $[X]/hour
- Source files included on final payment

### Next Steps
1. Reply to this proposal with questions or your chosen package
2. I'll send an agreement for signature
3. Invoice for deposit
4. We start on [DATE]

[YOUR NAME]
[YOUR EMAIL]
[YOUR WEBSITE]
```

**Template 2: Content / Copywriting**
(Same structure, adapted for content deliverables: blog posts, email sequences, landing pages, social content packs)

**Template 3: Consulting / Strategy**
(Adapted for consulting: discovery session, strategy document, implementation roadmap, ongoing advisory)

**Template 4: Marketing / Social Media**
(Adapted for marketing: audit, strategy, content creation, management, reporting cadence)

**Template 5: General Services**
(Generic template that works for any service type, minimal specific assumptions)

### Win Rate Tracking

The Proposal database tracks win rates automatically:
- **Win Rate (Overall):** Count where Status = Won / (Count where Status = Won + Lost)
- **Win Rate by Type:** Same calculation, grouped by Template Type
- **Average Response Time:** Days between Sent and Response

### Views

1. **Active Proposals** (Table) - Filter: Status = Draft or Sent. Sorted by Date Sent descending.
2. **Templates** (Gallery) - Filter: Status = Template. Shows template type and preview.
3. **Won** (Table) - Filter: Status = Won. Shows Quoted Amount, Client, Response Time.
4. **Lost** (Table) - Filter: Status = Lost. Grouped by Lost Reason. Identifies patterns.
5. **Win Rate** (Table) - All proposals excluding templates. Shows won/lost counts and rates.

---

## Database 3: Client Database

### Properties

| Property | Type | Details |
|----------|------|---------|
| Client Name | Title | |
| Company | Text | Company name |
| Email | Email | Primary contact |
| Phone | Phone | |
| Website | URL | Client's website |
| Industry | Select | User-defined |
| Status | Select | Options: Prospect, Active, Completed, Repeat, Referral Source, Churned |
| Communication Preference | Select | Options: Email, Slack, WhatsApp, Zoom, Phone |
| Timezone | Select | Common timezones |
| Decision Maker | Text | Who approves payments/work |
| First Contact Date | Date | When you first connected |
| Source | Select | Options: Referral, Cold Outreach, Inbound, Marketplace, Social, Repeat |
| Referred By | Text | Who referred them (if applicable) |
| Linked Gigs | Relation → Gig Tracker | All gigs for this client |
| Linked Invoices | Relation → Invoice Tracker | All invoices for this client |
| Linked Proposals | Relation → Proposal Templates | All proposals sent |
| Lifetime Value | Rollup | Sum of Final Price from Linked Gigs where Status = Paid |
| Gig Count | Rollup | Count of Linked Gigs |
| Avg Gig Value | Formula | `if(prop("Gig Count") > 0, round(prop("Lifetime Value") / prop("Gig Count") * 100) / 100, 0)` |
| Avg Payment Speed | Rollup | Average of Days to Pay from Linked Gigs |
| Last Gig Date | Rollup | Latest Paid Date from Linked Gigs |
| Days Since Last Gig | Formula | `if(not empty(prop("Last Gig Date")), dateBetween(now(), prop("Last Gig Date"), "days"), 999)` |
| Is Repeat Client | Formula | `prop("Gig Count") >= 2` |
| Satisfaction Score | Rollup | Average of Client Satisfaction from Linked Gigs |
| Notes | Text (long) | Client preferences, communication style, project history notes |
| Onboarding Status | Select | Options: Not Started, In Progress, Completed |

### Onboarding Checklist (Sub-page template per client)

```
## Client Onboarding: [CLIENT NAME]

- [ ] Welcome message sent
- [ ] Contract/agreement signed
- [ ] Payment method confirmed (card on file / invoice / PayPal)
- [ ] Project brief received and reviewed
- [ ] Access/credentials collected (login info, brand assets, etc.)
- [ ] Communication channel set up (Slack channel / WhatsApp group / email thread)
- [ ] Kickoff call scheduled
- [ ] Project timeline shared and agreed upon
- [ ] File sharing set up (Google Drive / Notion / Dropbox)
- [ ] Emergency contact confirmed (who to reach if you're stuck)
```

### Views

1. **Active Clients** (Table) - Filter: Status = Active. Sorted by Last Gig Date descending.
2. **All Clients** (Board) - Grouped by Status. Cards show Client Name, Company, LTV.
3. **Top Clients** (Table) - Sorted by Lifetime Value descending. Shows LTV, Gig Count, Avg Gig Value.
4. **Needs Re-engagement** (Table) - Filter: Days Since Last Gig > 90, Status != Churned. Clients you should reach out to.
5. **Repeat Clients** (Table) - Filter: Is Repeat Client = true. Your best clients.
6. **Client Directory** (Table) - All clients with contact info. Quick reference.
7. **Slow Payers** (Table) - Sorted by Avg Payment Speed descending. Clients who take longest to pay.
8. **Referral Sources** (Table) - Filter: Status = Referral Source. Who sends you business.

---

## Database 4: Invoice Tracker

### Properties

| Property | Type | Details |
|----------|------|---------|
| Invoice | Title | e.g., "INV-2026-001" |
| Client | Relation → Client Database | |
| Gig | Relation → Gig Tracker | Which gig this invoice covers |
| Amount | Number (currency $) | Invoice amount |
| Tax | Number (currency $) | Tax amount (if applicable) |
| Total | Formula | `prop("Amount") + prop("Tax")` |
| Status | Select | Options: Draft, Sent, Overdue, Paid, Disputed, Written Off |
| Date Sent | Date | When invoice was sent |
| Date Due | Date | Payment due date |
| Date Paid | Date | When payment was received |
| Days to Pay | Formula | `if(not empty(prop("Date Paid")) and not empty(prop("Date Sent")), dateBetween(prop("Date Paid"), prop("Date Sent"), "days"), 0)` |
| Days Overdue | Formula | `if(prop("Status") != "Paid" and not empty(prop("Date Due")) and now() > prop("Date Due"), dateBetween(now(), prop("Date Due"), "days"), 0)` |
| Payment Method | Select | Options: Bank Transfer, PayPal, Stripe, Check, Cash, Crypto |
| Invoice Link | URL | Link to actual invoice (Stripe, Wave, custom) |
| Notes | Text | Payment terms, special conditions |
| Month | Formula | `formatDate(prop("Date Sent"), "YYYY-MM")` |

### Views

1. **All Invoices** (Table) - Sorted by Date Sent descending. Shows all columns.
2. **Outstanding** (Table) - Filter: Status = Sent or Overdue. Sorted by Date Due ascending.
3. **Overdue** (Table) - Filter: Status = Overdue (or Days Overdue > 0). Sorted by Days Overdue descending. Red indicators.
4. **Monthly Summary** (Table) - Grouped by Month. Sum on Amount. Shows invoiced vs paid.
5. **By Client** (Table) - Grouped by Client. Shows total invoiced, total paid, outstanding per client.
6. **Paid** (Table) - Filter: Status = Paid. Sorted by Date Paid descending.

### Late Payment Follow-up Templates (Static content on page)

```
POLITE NUDGE (3 days after due date):
Subject: invoice [NUMBER] - quick reminder

hey [CLIENT NAME],

just a heads up that invoice [NUMBER] for $[AMOUNT] was due [DATE].
probably just slipped through the cracks. no rush if it's already in process.

let me know if you need me to resend or if there's any issue.

[YOUR NAME]

---

FIRM REMINDER (7 days overdue):
Subject: invoice [NUMBER] - follow up

[CLIENT NAME],

following up on invoice [NUMBER] for $[AMOUNT], now 7 days past the due date of [DATE].

could you let me know when I can expect payment?

[YOUR NAME]

---

FINAL NOTICE (14+ days overdue):
Subject: invoice [NUMBER] - overdue payment

[CLIENT NAME],

invoice [NUMBER] for $[AMOUNT] is now [X] days past due.

I need to resolve this within the next 7 days. please let me know the status or if there's an issue I should be aware of.

[YOUR NAME]
```

---

## Database 5: Portfolio

### Properties

| Property | Type | Details |
|----------|------|---------|
| Project Title | Title | |
| Client | Relation → Client Database | (optional - some clients prefer anonymity) |
| Show Client Name | Checkbox | Whether to display client name publicly |
| Category | Select | Options: Web Development, Design, Content, Marketing, Consulting, Other |
| Description | Text (long) | What the project was about |
| The Challenge | Text | What problem the client had |
| The Solution | Text | What you built/delivered |
| The Result | Text | Measurable outcomes (numbers) |
| Testimonial | Text (long) | Client quote |
| Testimonial Author | Text | Who said it (name + title) |
| Project URL | URL | Live link to the work (if applicable) |
| Images | Files & Media | Screenshots, mockups, before/after |
| Tools Used | Multi-select | Tools/tech used on this project |
| Date Completed | Date | |
| Featured | Checkbox | Is this a featured portfolio piece |
| Published | Checkbox | Show in public portfolio view |

### Views

1. **Public Portfolio** (Gallery) - Filter: Published = true. Sorted by Date Completed descending. Shows Project Title, Category, Description, Images as cover. This view can be shared via public Notion link.
2. **Featured** (Gallery) - Filter: Featured = true. Top portfolio pieces.
3. **All Projects** (Table) - Full list with all fields.
4. **By Category** (Board) - Grouped by Category.
5. **Needs Testimonial** (Table) - Filter: Testimonial is empty and Status = Completed. Projects where you should request a testimonial.

---

## Database 6: Freelance Analytics (Page with linked views)

Not a separate database. Pulls from Gig Tracker, Client Database, Invoice Tracker, and Proposals.

### Analytics Page Layout

**Row 1: Key Metrics (4 columns)**
- Monthly Revenue: Sum of Paid gigs this month
- Active Gigs: Count where Status = Active
- Win Rate: Proposals won / (won + lost) * 100
- Average Hourly Rate: Total revenue / Total hours (all paid gigs)

**Row 2: Revenue Trend**
Linked view from Gig Tracker:
- Grouped by month (Paid Date)
- Sum of Final Price per month
- Shows 6-month revenue trend

**Row 3: Utilization Rate**
```
Available Hours per Month: 160 (adjustable)
Billable Hours This Month: [sum of Actual Hours on active/delivered/paid gigs]
Utilization Rate: Billable / Available * 100

Target: 60-70% (leaves room for admin, marketing, learning)
```

**Row 4: Client Concentration**
```
Top Client Revenue: [highest LTV client's revenue this month]
Total Revenue This Month: [sum all revenue]
Concentration: Top Client / Total * 100

WARNING: If > 50%, you're one email away from losing half your income.
Diversify by adding 2-3 smaller clients.
```

**Row 5: Gig Source ROI**
Linked view from Gig Tracker:
- Grouped by Source
- Columns: Source, Gig Count, Total Revenue, Avg Gig Value
- Identifies which channels bring the best gigs (not just the most gigs)

**Row 6: Payment Speed**
Linked view from Invoice Tracker:
- Average Days to Pay across all clients
- Slowest payers identified
- Fastest payers identified

**Row 7: Rate Progression**
Linked view from Gig Tracker:
- Hourly Rate over time (by Paid Date)
- Shows if you're raising rates or stagnating

**Row 8: Proposals Performance**
- Win rate by proposal type
- Average response time
- Most common lost reason

---

## Cross-Database Relations Map

```
Gig Tracker ←→ Client Database (client assignment)
Gig Tracker ←→ Invoice Tracker (gig invoicing)
Gig Tracker ←→ Proposal Templates (proposal-to-gig conversion)
Client Database ←→ Invoice Tracker (client invoices)
Client Database ←→ Proposal Templates (client proposals)
Client Database ←→ Portfolio (client projects)
```

Total relations: 6

---

## Dashboard Page Layout

**Row 1: Welcome + Date**
"Freelance Command Center" + current date

**Row 2: Quick Stats (4 columns)**
- Monthly Revenue
- Active Gigs Count
- Pending Invoices ($X outstanding)
- Win Rate

**Row 3: Pipeline (2 columns)**
- Col 1: Gig Pipeline kanban (linked view, Active + Delivered + Paid)
- Col 2: Overdue/Awaiting Payment alerts

**Row 4: This Week (Full width)**
- Calendar view of deadlines this week

**Row 5: Client Health (2 columns)**
- Col 1: Top 5 clients by LTV
- Col 2: Needs Re-engagement list

**Row 6: Quick Links**
- Jump to: Full Gig Tracker, Proposals, Invoices, Portfolio, Clients, Analytics

---

## Setup Instructions

1. Duplicate this template to your Notion workspace
2. Go to Client Database > add your current and past clients
3. Go to Gig Tracker > add current active gigs and recent completed gigs
4. Go to Invoice Tracker > add any outstanding invoices
5. Review the 5 proposal templates > customize with your info, services, and pricing
6. Go to Portfolio > add your best completed projects
7. Request testimonials from clients (use the "Needs Testimonial" view)
8. Set your target hourly rate in the Analytics page
9. Check the Dashboard daily, Analytics page weekly

Time to setup: 10 minutes (plus proposal customization)
