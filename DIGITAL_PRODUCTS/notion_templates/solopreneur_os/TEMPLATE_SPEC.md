# SoloOS: Template Specification

## Overview
7 interconnected Notion databases with pre-built views, formulas, relations, and rollups. Every database connects to at least 2 others.

---

## Database 1: Revenue Tracker

### Properties

| Property | Type | Details |
|----------|------|---------|
| Entry Name | Title | e.g., "Gumroad Sales - March 2026" |
| Amount | Number (currency $) | Revenue amount |
| Date | Date | Transaction/period date |
| Revenue Source | Select | Options: Products, Services, Affiliate, Ads, Consulting, Subscriptions, Other |
| Type | Select | Options: One-time, Recurring |
| Is Expense | Checkbox | Toggle for expenses (negative values) |
| Category | Select | Options: Revenue, COGS, Marketing, Tools, Hosting, Contractor, Other Expense |
| Linked Project | Relation → Project Pipeline | Which project generated this revenue |
| Linked Client | Relation → Client CRM | Which client paid this |
| Notes | Text | Context, invoice number, etc. |
| Month | Formula | `formatDate(prop("Date"), "YYYY-MM")` |
| Quarter | Formula | `"Q" + format(ceil(toNumber(formatDate(prop("Date"), "M")) / 3))` |

### Views

1. **Monthly Revenue** (Table) - Grouped by Month formula, sorted by Date descending. Filter: Is Expense = unchecked. Sum on Amount column.
2. **Revenue by Source** (Table) - Grouped by Revenue Source. Sum on Amount. Filter: Is Expense = unchecked.
3. **Expenses** (Table) - Filter: Is Expense = checked. Grouped by Category. Sum on Amount.
4. **P&L Monthly** (Table) - Grouped by Month. Shows both revenue and expenses. Running total via rollup.
5. **Revenue Trend** (Chart/Board) - Grouped by Month, sorted chronologically. Visual revenue trend.
6. **All Transactions** (Table) - No filter, sorted by Date descending.

### Formulas (Template-level, shown in dashboard)

- **Total Revenue (MTD):** Filter current month, sum Amount where Is Expense = false
- **Total Expenses (MTD):** Filter current month, sum Amount where Is Expense = true
- **Profit Margin:** `(Revenue - Expenses) / Revenue * 100`
- **MRR:** Filter Type = Recurring, sum current month Amount

---

## Database 2: Content Calendar

### Properties

| Property | Type | Details |
|----------|------|---------|
| Content Title | Title | Title or hook of the content piece |
| Platform | Multi-select | Options: X/Twitter, YouTube, TikTok, LinkedIn, Newsletter, Blog |
| Status | Select | Options: Idea, Outline, Draft, Review, Scheduled, Published, Analyzed |
| Publish Date | Date | Scheduled or actual publish date |
| Content Type | Select | Options: Post, Thread, Video, Carousel, Article, Newsletter Issue, Story, Reel |
| Topic | Select | User-defined topics (pre-loaded: Business, Tutorial, Behind-the-scenes, Opinion, Case Study, Listicle) |
| Hook | Text | Opening line / hook text |
| Body | Text (long) | Full content or outline |
| Media | Files & Media | Attached images, videos, thumbnails |
| Repurposed From | Relation → Content Calendar (self-relation) | Links to original content piece |
| Linked Goal | Relation → Goals Dashboard | Which goal this content serves |
| Views | Number | Post views/impressions |
| Engagement | Number | Likes + comments + shares |
| Clicks | Number | Link clicks |
| Engagement Rate | Formula | `if(prop("Views") > 0, round(prop("Engagement") / prop("Views") * 10000) / 100, 0)` (outputs %) |
| Performance | Formula | `if(prop("Engagement Rate") > 5, "High", if(prop("Engagement Rate") > 2, "Medium", if(prop("Engagement Rate") > 0, "Low", "")))` |
| Repurpose Count | Rollup | Count of items in Repurposed From (reverse relation) |

### Views

1. **Content Calendar** (Calendar) - By Publish Date. Color-coded by Platform.
2. **Pipeline Board** (Board/Kanban) - Grouped by Status. Shows Content Title, Platform pills, Publish Date.
3. **By Platform** (Table) - Grouped by Platform. Filtered to Status != Idea.
4. **Ideas Bank** (Gallery) - Filtered to Status = Idea. Shows Content Title, Topic, Platform.
5. **Performance Tracker** (Table) - Filtered to Status = Published or Analyzed. Sorted by Engagement Rate descending. Shows Views, Engagement, Clicks, Performance.
6. **Repurposing Map** (Table) - Shows Repurposed From and Repurpose Count. Helps identify content that hasn't been repurposed yet (count = 0).
7. **This Week** (Table) - Filtered to Publish Date = this week. Sorted by date.

---

## Database 3: Project Pipeline

### Properties

| Property | Type | Details |
|----------|------|---------|
| Project Name | Title | |
| Status | Select | Options: Backlog, In Progress, Review, Shipped, On Hold, Cancelled |
| Priority | Select | Options: P0 (Critical), P1 (High), P2 (Medium), P3 (Low) |
| Start Date | Date | When work began |
| Deadline | Date | Target completion |
| Actual Ship Date | Date | When it actually shipped |
| Project Type | Select | Options: Product, Feature, Content, Marketing, Operations, Research |
| Description | Text (long) | Project brief, scope, success criteria |
| Hours Logged | Number | Total hours spent |
| Linked Revenue | Relation → Revenue Tracker | Revenue entries attributed to this project |
| Linked Goal | Relation → Goals Dashboard | Which goal this project drives |
| Linked Client | Relation → Client CRM | If client-related |
| Dependencies | Relation → Project Pipeline (self-relation) | Blocking/blocked-by projects |
| Revenue Generated | Rollup | Sum of Amount from Linked Revenue |
| Revenue per Hour | Formula | `if(prop("Hours Logged") > 0, round(prop("Revenue Generated") / prop("Hours Logged") * 100) / 100, 0)` |
| Days to Ship | Formula | `if(not empty(prop("Actual Ship Date")) and not empty(prop("Start Date")), dateBetween(prop("Actual Ship Date"), prop("Start Date"), "days"), 0)` |
| Overdue | Formula | `if(not empty(prop("Deadline")) and empty(prop("Actual Ship Date")) and now() > prop("Deadline"), true, false)` |

### Views

1. **Kanban Board** (Board) - Grouped by Status. Shows Project Name, Priority pill, Deadline.
2. **Active Projects** (Table) - Filter: Status = In Progress or Review. Sorted by Priority then Deadline.
3. **Shipped** (Table) - Filter: Status = Shipped. Shows Revenue Generated, Hours Logged, Revenue per Hour.
4. **Overdue** (Table) - Filter: Overdue = true. Sorted by Deadline ascending.
5. **By Goal** (Table) - Grouped by Linked Goal. Shows project count and revenue per goal.
6. **Timeline** (Timeline) - Start Date to Deadline. Visual project schedule.

---

## Database 4: Client CRM

### Properties

| Property | Type | Details |
|----------|------|---------|
| Client Name | Title | |
| Status | Select | Options: Lead, Prospect, Active, Completed, Referral, Churned |
| Company | Text | Company name |
| Email | Email | Primary contact email |
| Phone | Phone | Phone number |
| Source | Select | Options: Referral, Cold Outreach, Inbound, Social Media, Marketplace, Other |
| First Contact | Date | When you first connected |
| Last Contact | Date | Most recent interaction |
| Notes | Text (long) | Communication log, preferences, context |
| Linked Projects | Relation → Project Pipeline | All projects for this client |
| Linked Revenue | Relation → Revenue Tracker | All revenue from this client |
| Lifetime Value | Rollup | Sum of Amount from Linked Revenue |
| Project Count | Rollup | Count of Linked Projects |
| Avg Project Value | Formula | `if(prop("Project Count") > 0, round(prop("Lifetime Value") / prop("Project Count") * 100) / 100, 0)` |
| Days Since Contact | Formula | `if(not empty(prop("Last Contact")), dateBetween(now(), prop("Last Contact"), "days"), 999)` |
| Needs Follow-up | Formula | `prop("Days Since Contact") > 30 and (prop("Status") == "Active" or prop("Status") == "Prospect")` |

### Views

1. **Pipeline Board** (Board) - Grouped by Status. Shows Client Name, Company, Lifetime Value.
2. **Active Clients** (Table) - Filter: Status = Active. Sorted by Last Contact descending.
3. **Needs Follow-up** (Table) - Filter: Needs Follow-up = true. Sorted by Days Since Contact descending.
4. **Top Clients** (Table) - Sorted by Lifetime Value descending. Shows LTV, Project Count, Avg Project Value.
5. **All Clients** (Table) - No filter. Grouped by Status.
6. **Lead Funnel** (Board) - Filter: Status = Lead or Prospect. Sorted by First Contact.

---

## Database 5: Goals Dashboard

### Properties

| Property | Type | Details |
|----------|------|---------|
| Goal | Title | e.g., "Reach $5K MRR" |
| Quarter | Select | Options: Q1 2026, Q2 2026, Q3 2026, Q4 2026 (extend as needed) |
| Category | Select | Options: Revenue, Growth, Product, Content, Operations, Personal |
| Target Value | Number | Numeric target (e.g., 5000 for $5K MRR) |
| Current Value | Number | Manually updated or pulled from rollup |
| Unit | Select | Options: $, %, count, hours |
| Status | Formula | `if(prop("Progress") >= 100, "Complete", if(prop("Progress") >= 70, "On Track", if(prop("Progress") >= 40, "At Risk", "Behind")))` |
| Progress | Formula | `if(prop("Target Value") > 0, min(round(prop("Current Value") / prop("Target Value") * 100), 100), 0)` |
| Deadline | Date | End of quarter or specific deadline |
| Linked Projects | Relation → Project Pipeline | Projects driving this goal |
| Linked Content | Relation → Content Calendar | Content supporting this goal |
| Linked Habits | Relation → Habit Tracker | Habits that drive this goal |
| Key Results | Text (long) | 2-3 measurable key results |
| Project Count | Rollup | Count of Linked Projects |

### Views

1. **Current Quarter** (Gallery) - Filtered to current quarter. Shows Goal, Progress bar (via formula), Status pill, Category. Card preview shows Key Results.
2. **All Goals** (Table) - Grouped by Quarter. Shows Progress, Status, Target vs Current.
3. **By Category** (Board) - Grouped by Category. Shows goal progress.
4. **At Risk** (Table) - Filter: Status = "At Risk" or "Behind". Sorted by Progress ascending.
5. **Completed** (Table) - Filter: Status = "Complete". Celebration view.

---

## Database 6: Habit Tracker

### Properties

| Property | Type | Details |
|----------|------|---------|
| Habit | Title | e.g., "Post 1 piece of content" |
| Frequency | Select | Options: Daily, Weekdays, Weekly, 3x/week |
| Category | Select | Options: Content, Outreach, Learning, Health, Operations |
| Linked Goal | Relation → Goals Dashboard | Which goal this habit drives |
| Mon | Checkbox | |
| Tue | Checkbox | |
| Wed | Checkbox | |
| Thu | Checkbox | |
| Fri | Checkbox | |
| Sat | Checkbox | |
| Sun | Checkbox | |
| Week Of | Date | Monday of the tracking week |
| Completion Rate | Formula | Count checked days / expected days based on Frequency |
| Current Streak | Number | Manually updated (or tracked via separate streak logic) |
| Best Streak | Number | All-time best streak |
| Active | Checkbox | Whether this habit is currently being tracked |

### Views

1. **This Week** (Table) - Filter: Week Of = this week, Active = true. Shows Habit, Mon-Sun checkboxes, Completion Rate.
2. **Streaks** (Table) - Sorted by Current Streak descending. Shows Habit, Current Streak, Best Streak.
3. **By Goal** (Table) - Grouped by Linked Goal. Shows which habits feed which goals.
4. **Weekly History** (Table) - Grouped by Week Of. Shows completion rates over time.
5. **Habit Setup** (Table) - Shows all habits with Frequency, Category, Active toggle. For adding/editing habits.

### Usage Pattern
- Each week, duplicate the habit row set and update Week Of to current Monday
- Check off each day as completed
- Streak tracking updates at end of week

---

## Database 7: Weekly Review

### Properties

| Property | Type | Details |
|----------|------|---------|
| Review Title | Title | Auto-format: "Week of [DATE]" |
| Week Of | Date | Monday of the review week |
| Revenue This Week | Rollup | Sum from Revenue Tracker where Date = this week |
| Content Published | Rollup | Count from Content Calendar where Publish Date = this week and Status = Published |
| Habits Completed | Number | Manual entry or rollup from Habit Tracker |
| Wins | Text (long) | What went well this week |
| Blockers | Text (long) | What's stuck or slowing you down |
| Lessons | Text (long) | What you learned |
| Decisions Made | Text (long) | Key decisions and reasoning |
| Next Week Priorities | Text (long) | Top 3-5 priorities for next week |
| Energy Level | Select | Options: High, Medium, Low |
| Overall Rating | Select | Options: Great, Good, OK, Rough |
| Linked Projects | Relation → Project Pipeline | Projects worked on this week |
| Projects Shipped | Rollup | Count of Linked Projects where Status = Shipped |

### Views

1. **Latest Review** (Page) - Most recent review, full page layout with all fields visible.
2. **Review History** (Table) - Sorted by Week Of descending. Shows Revenue, Content Published, Overall Rating.
3. **Trends** (Table) - Shows Revenue This Week and Content Published over time for trend analysis.

### Template
Each new review page is pre-filled with this structure:

```
## Wins
-

## Numbers
- Revenue: $[auto-populated]
- Content published: [auto-populated]
- Habits completed: X/Y

## Blockers
-

## Lessons
-

## Decisions Made
| Decision | Reasoning | Outcome |
|----------|-----------|---------|
|          |           |         |

## Next Week Priorities
1.
2.
3.

## Energy Check
How did I feel this week? What drained me? What energized me?
```

---

## Cross-Database Relations Map

```
Revenue Tracker ←→ Project Pipeline (revenue attribution)
Revenue Tracker ←→ Client CRM (client revenue tracking)
Content Calendar ←→ Goals Dashboard (content-goal alignment)
Content Calendar ←→ Content Calendar (self-relation for repurposing)
Project Pipeline ←→ Goals Dashboard (project-goal linkage)
Project Pipeline ←→ Client CRM (client projects)
Project Pipeline ←→ Project Pipeline (self-relation for dependencies)
Goals Dashboard ←→ Habit Tracker (habit-goal connection)
Goals Dashboard ←→ Content Calendar (content-goal alignment)
Weekly Review ←→ Project Pipeline (projects worked on)
```

Total relations: 10 (including 2 self-relations)

---

## Dashboard Page Layout

The main dashboard page (landing page of the template) uses Notion columns and linked database views:

**Row 1 (Full width):**
- Template title: "SoloOS" with subtitle and last updated date

**Row 2 (3 columns):**
- Col 1: Revenue This Month (number callout from Revenue Tracker rollup)
- Col 2: Content Published This Week (count from Content Calendar)
- Col 3: Goals On Track (count from Goals Dashboard where Status = "On Track" or "Complete")

**Row 3 (2 columns):**
- Col 1: Active Projects kanban (linked view from Project Pipeline, filtered to In Progress/Review)
- Col 2: This Week's Content (linked view from Content Calendar, filtered to this week)

**Row 4 (2 columns):**
- Col 1: Habits This Week (linked view from Habit Tracker, this week)
- Col 2: Needs Follow-up (linked view from Client CRM, filtered to Needs Follow-up = true)

**Row 5 (Full width):**
- Latest Weekly Review (linked view, most recent entry)

**Row 6 (Full width):**
- Quick Links: Jump to each database full view

---

## Pre-loaded Content

### Content Calendar Hook Library (50 entries)
Pre-load 50 hook templates as Idea-status entries in Content Calendar:
- 10 list hooks ("7 tools that...", "5 mistakes when...")
- 10 story hooks ("I spent 6 months...", "Last year I...")
- 10 contrarian hooks ("Stop doing X. Do Y instead.", "Everyone says X. They're wrong.")
- 10 data hooks ("I analyzed 500...", "Here are the numbers...")
- 10 question hooks ("Why does nobody talk about...", "What happens when...")

Each tagged with Platform suggestions and Content Type.

---

## Setup Instructions (included in template)

1. Duplicate this template to your Notion workspace
2. Go to Revenue Tracker > add your current month's revenue entries
3. Go to Client CRM > add your active clients
4. Go to Project Pipeline > add your current projects
5. Go to Goals Dashboard > set your quarterly goals
6. Go to Habit Tracker > customize habits to your routine
7. Go to Content Calendar > start adding content ideas (50 hooks already loaded)
8. Every Friday: create a new Weekly Review entry (template auto-populates numbers)
9. Dashboard page auto-updates as you add data

Time to setup: 15 minutes
