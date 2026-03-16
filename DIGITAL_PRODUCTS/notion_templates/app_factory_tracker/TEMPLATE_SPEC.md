# App Factory: Template Specification

## Overview
6 interconnected databases for managing a portfolio of apps from ideation through revenue generation. Includes kill/double-down decision logic as first-class features with auto-calculated thresholds.

---

## Database 1: Idea Vault

### Properties

| Property | Type | Details |
|----------|------|---------|
| Idea Name | Title | App name or working title |
| Problem | Text | What problem does this app solve? |
| Target Audience | Text | Who is this for? Be specific. |
| Monetization Model | Select | Options: Subscription, One-time Purchase, Freemium, Ads, In-App Purchases, API/Usage, Marketplace Commission |
| Estimated Build Time | Select | Options: 1 day, 2-3 days, 1 week, 2 weeks, 1 month, 2+ months |
| Category | Select | Options: SaaS, Mobile App, Chrome Extension, API/Tool, Marketplace, Desktop App, CLI Tool, Notion Template, Web App |
| Competition Level | Select | Options: None (Blue Ocean), Low (Few competitors), Medium (Competitive), High (Saturated), Dominated (1-2 winners own it) |
| Market Size | Select | Options: Niche (<10K potential users), Small (10K-100K), Medium (100K-1M), Large (1M+) |
| Tech Stack | Multi-select | Options: Next.js, React Native, Python, Node.js, Swift, Flutter, Chrome API, Notion API, Supabase, Firebase, Stripe |
| Status | Select | Options: Raw Idea, Evaluated, Promoted to Build, Passed, Archived |
| Idea Score | Formula | See scoring formula below |
| Score Breakdown | Formula | Shows individual factor scores for transparency |
| Source | Text | Where did this idea come from? (Alpha entry, conversation, personal pain) |
| Notes | Text (long) | Additional research, links, competitor URLs |
| Promoted To | Relation → Build Tracker | Link to active build if promoted |
| Evaluated Date | Date | When you last evaluated this idea |
| Created | Created time | Auto-populated |

### Idea Score Formula

```
Market Size Score (0-3):
  Large: 3, Medium: 2, Small: 1, Niche: 0

Monetization Score (0-3):
  Subscription: 3, Freemium: 2, One-time: 2, In-App: 2, Ads: 1, API: 2, Marketplace: 3

Build Speed Score (0-3):
  1 day: 3, 2-3 days: 3, 1 week: 2, 2 weeks: 1, 1 month: 0, 2+ months: 0

Competition Inverse (0-3):
  None: 3, Low: 2, Medium: 1, High: 0, Dominated: 0

TOTAL = (Market + Monetization + Build Speed + Competition Inverse)
Max: 12
```

Score Breakdown formula shows: `"MKT:" + MarketScore + " MON:" + MonScore + " SPD:" + SpeedScore + " COMP:" + CompScore`

### Views

1. **Top Ideas** (Table) - Sorted by Idea Score descending. Filter: Status = Raw Idea or Evaluated. Shows all scoring columns.
2. **By Category** (Board) - Grouped by Category. Card shows Idea Name, Score, Monetization Model.
3. **Graveyard** (Table) - Filter: Status = Passed or Archived. Shows why ideas were killed.
4. **Promoted** (Table) - Filter: Status = Promoted to Build. Links to Build Tracker.
5. **Evaluate Queue** (Table) - Filter: Status = Raw Idea. Sorted by Created descending. Ideas that need evaluation.

---

## Database 2: Build Tracker (Master Database)

### Properties

| Property | Type | Details |
|----------|------|---------|
| App Name | Title | |
| Stage | Select | Options: Spec, Design, Build, Test, Ship, Grow, Evaluate, Killed, Doubled Down |
| App Type | Select | Same categories as Idea Vault |
| Tech Stack | Multi-select | Same as Idea Vault |
| Repo URL | URL | GitHub/GitLab repo link |
| Deploy URL | URL | Live app URL |
| App Store URL | URL | If applicable |
| Build Start Date | Date | When development started |
| Ship Date | Date | When first version went live |
| Days to Ship | Formula | `if(not empty(prop("Ship Date")) and not empty(prop("Build Start Date")), dateBetween(prop("Ship Date"), prop("Build Start Date"), "days"), 0)` |
| Days Live | Formula | `if(not empty(prop("Ship Date")), dateBetween(now(), prop("Ship Date"), "days"), 0)` |
| Hours Logged | Number | Total dev hours |
| Monetization Model | Select | Same as Idea Vault |
| Pricing | Text | e.g., "$9/mo or $79/year" |
| Source Idea | Relation → Idea Vault | Which idea this came from |
| Linked Revenue | Relation → Revenue Dashboard | Revenue entries for this app |
| Linked ASO | Relation → ASO Tracker | ASO entries for this app |
| Linked Checklist | Relation → Deployment Checklist | Checklist for this app |
| MRR | Number (currency $) | Current monthly recurring revenue |
| Total Revenue | Rollup | Sum from Revenue Dashboard |
| DAU | Number | Daily active users (last reported) |
| MAU | Number | Monthly active users |
| Churn Rate | Number (%) | Monthly churn percentage |
| Retention 30d | Number (%) | 30-day retention rate |
| CAC | Number (currency $) | Customer acquisition cost |
| LTV | Number (currency $) | Lifetime value |
| Hosting Cost | Number (currency $) | Monthly hosting/infra cost |
| Marketing Spend | Number (currency $) | Monthly marketing spend |
| Total Monthly Cost | Formula | `prop("Hosting Cost") + prop("Marketing Spend")` |
| Monthly Profit | Formula | `prop("MRR") - prop("Total Monthly Cost")` |
| Profit Margin | Formula | `if(prop("MRR") > 0, round(prop("Monthly Profit") / prop("MRR") * 100), 0)` |
| Decision Status | Formula | See Kill/Double-Down formula below |
| Kill Score | Formula | Count of kill signals triggered |
| Growth Score | Formula | Count of double-down signals triggered |
| Revenue per Hour | Formula | `if(prop("Hours Logged") > 0, round(prop("Total Revenue") / prop("Hours Logged") * 100) / 100, 0)` |
| Notes | Text (long) | Build log, decisions, pivots |
| Last Updated | Last edited time | Auto |

### Kill/Double-Down Decision Formula

**Kill Score (0-5):**
```
(MRR < 100 and Days Live > 60 ? 1 : 0) +
(DAU < 50 and Days Live > 30 ? 1 : 0) +
(MRR growth negative for 3 weeks: manual checkbox, 1 if checked) +
(CAC > LTV ? 1 : 0) +
(Last Updated > 14 days ago ? 1 : 0)
```

**Growth Score (0-5):**
```
(MRR > 500 and MRR growth > 20%: manual checkbox, 1 if checked) +
(DAU growing without paid acquisition: manual checkbox, 1 if checked) +
(Users requesting features: manual checkbox, 1 if checked) +
(Retention 30d > 40 ? 1 : 0) +
(LTV > CAC * 3 ? 1 : 0)
```

**Decision Status:**
```
if Kill Score >= 2: "KILL"
else if Growth Score >= 2: "DOUBLE DOWN"
else if Days Live > 30: "EVALUATE"
else if Stage == "Grow": "GROW"
else: "BUILD"
```

### Additional Checkbox Properties (for manual signal tracking)

| Property | Type | Details |
|----------|------|---------|
| Negative Growth 3wk | Checkbox | MRR declined for 3 consecutive weeks |
| MRR Growth 20%+ | Checkbox | MRR growing 20%+ month-over-month |
| Organic User Growth | Checkbox | Users coming without paid acquisition |
| Feature Requests | Checkbox | Users actively requesting features |

### Views

1. **Pipeline Board** (Board/Kanban) - Grouped by Stage. Cards show App Name, MRR, Decision Status pill, Days Live.
2. **Portfolio Dashboard** (Table) - All apps. Columns: App Name, MRR, Total Revenue, DAU, Monthly Profit, Decision Status. Sorted by MRR descending.
3. **Decision Board** (Table) - Shows Kill Score, Growth Score, Decision Status. Sorted by Kill Score descending (worst performers first). Color-coded: KILL=red, DOUBLE DOWN=green, EVALUATE=yellow, BUILD=blue, GROW=purple.
4. **Revenue Leaders** (Table) - Sorted by MRR descending. Shows revenue metrics, profit margins.
5. **Active Builds** (Table) - Filter: Stage = Spec, Design, Build, Test. Shows Hours Logged, Build Start Date, estimated ship date.
6. **Killed Apps** (Table) - Filter: Stage = Killed. Shows Kill Score reasons, Days Live, Total Revenue (how much you recouped before killing).
7. **Doubled Down** (Table) - Filter: Stage = Doubled Down. Shows Growth Score, MRR trajectory.
8. **Timeline** (Timeline) - Build Start Date to Ship Date. Visual build schedule.
9. **Cost Analysis** (Table) - Shows Hosting Cost, Marketing Spend, Total Monthly Cost, Profit Margin per app. Sorted by Profit Margin descending.

---

## Database 3: Deployment Checklist

### Properties

| Property | Type | Details |
|----------|------|---------|
| Checklist Name | Title | e.g., "MyApp - Pre-Launch" |
| App | Relation → Build Tracker | Which app this checklist belongs to |
| Phase | Select | Options: Pre-Launch, Launch Day, Post-Launch (Week 1), Post-Launch (Month 1) |
| Platform | Select | Options: Web, App Store (iOS), Google Play, Chrome Web Store, Product Hunt |

### Checklist Items (Sub-pages or toggle blocks within each entry)

**Pre-Launch Checklist:**
- [ ] Domain registered and configured
- [ ] SSL certificate active
- [ ] Hosting deployed and tested
- [ ] Analytics installed (Plausible/PostHog/GA4)
- [ ] Error tracking installed (Sentry)
- [ ] Privacy policy page live
- [ ] Terms of service page live
- [ ] Stripe/payment integration tested
- [ ] Email capture working (if applicable)
- [ ] Landing page copy finalized
- [ ] Screenshots/demo video created
- [ ] Social preview images (OG tags) set
- [ ] Mobile responsive tested
- [ ] Load tested (basic)
- [ ] Backup system in place

**Launch Day Checklist:**
- [ ] Deploy final build
- [ ] Smoke test all critical paths
- [ ] Post on X/Twitter
- [ ] Post on Indie Hackers
- [ ] Post on relevant subreddits
- [ ] Submit to Product Hunt (if applicable)
- [ ] Email list announcement
- [ ] Update portfolio/personal site
- [ ] Share with beta testers
- [ ] Monitor error tracking dashboard

**Post-Launch Week 1:**
- [ ] Respond to all user feedback within 24h
- [ ] Fix critical bugs (if any)
- [ ] Monitor analytics daily
- [ ] Collect first testimonials
- [ ] Post Day 2-3 update thread
- [ ] A/B test landing page headline

**Post-Launch Month 1:**
- [ ] Review retention metrics
- [ ] Identify top feature requests
- [ ] Ship first iteration/update
- [ ] Optimize onboarding flow
- [ ] Set up automated emails (onboarding, feedback)
- [ ] Evaluate kill/double-down triggers
- [ ] Update ASO keywords (if app store)
- [ ] Start content marketing if metrics are positive

**Platform-Specific: App Store (iOS):**
- [ ] App icon (1024x1024)
- [ ] Screenshots (6.7", 6.5", 6.1", 5.5")
- [ ] App preview video (optional)
- [ ] Description and keywords
- [ ] Privacy nutrition labels filled
- [ ] Age rating selected
- [ ] Review notes for Apple reviewer
- [ ] TestFlight beta tested with 5+ users

**Platform-Specific: Google Play:**
- [ ] Feature graphic (1024x500)
- [ ] Screenshots (phone + tablet)
- [ ] Short description (80 chars)
- [ ] Full description (4000 chars)
- [ ] Content rating questionnaire
- [ ] Data safety form filled
- [ ] Internal testing track deployed

**Platform-Specific: Chrome Web Store:**
- [ ] Extension icon (128x128)
- [ ] Promo images (440x280 small, 920x680 large)
- [ ] Description
- [ ] Permissions justified
- [ ] Privacy policy URL

### Views

1. **By App** (Table) - Grouped by App relation. Shows all checklists per app.
2. **Active Checklists** (Table) - Filter: linked app Stage != Killed. Shows incomplete items.
3. **By Phase** (Board) - Grouped by Phase. Shows progress per phase.

---

## Database 4: ASO Tracker (App Store Optimization)

### Properties

| Property | Type | Details |
|----------|------|---------|
| Entry | Title | Keyword or tracking item |
| App | Relation → Build Tracker | Which app this belongs to |
| Type | Select | Options: Keyword, Competitor, A/B Test, Review |
| Keyword | Text | Target keyword (for keyword type) |
| Current Rank | Number | Your current rank for this keyword |
| Previous Rank | Number | Last recorded rank |
| Rank Change | Formula | `prop("Current Rank") - prop("Previous Rank")` (negative = improvement) |
| Search Volume | Select | Options: High, Medium, Low |
| Difficulty | Select | Options: Easy, Medium, Hard |
| Competitor App | Text | Competitor app name (for competitor type) |
| Competitor Rating | Number | Their app store rating |
| Competitor Downloads | Text | Estimated downloads |
| Competitor Price | Text | Their pricing |
| A/B Test Variant | Text | What was tested (for A/B test type) |
| A/B Result | Text | What won and by how much |
| Review Text | Text (long) | User review text (for review type) |
| Review Rating | Number | 1-5 stars |
| Review Response | Text (long) | Your response to the review |
| Date | Date | Date of entry |
| Notes | Text | Additional context |

### Views

1. **Keywords by App** (Table) - Filter: Type = Keyword. Grouped by App. Shows rank, change, volume.
2. **Competitors** (Table) - Filter: Type = Competitor. Shows side-by-side competitor analysis.
3. **A/B Tests** (Table) - Filter: Type = A/B Test. Shows test history and results.
4. **Reviews** (Table) - Filter: Type = Review. Sorted by Date descending. Shows rating, text, response.
5. **Rank Changes** (Table) - Filter: Type = Keyword. Sorted by Rank Change ascending (biggest improvements first).

---

## Database 5: Revenue Dashboard

### Properties

| Property | Type | Details |
|----------|------|---------|
| Entry | Title | e.g., "March 2026 - AppName Subscriptions" |
| App | Relation → Build Tracker | Which app generated this revenue |
| Amount | Number (currency $) | Revenue amount |
| Date | Date | Revenue period |
| Revenue Type | Select | Options: Subscription, One-time Sale, In-App Purchase, Ad Revenue, Affiliate, Other |
| Is Expense | Checkbox | Toggle for costs |
| Expense Category | Select | Options: Hosting, Marketing, Tools, Contractor, App Store Fee, Other |
| Month | Formula | `formatDate(prop("Date"), "YYYY-MM")` |

### Views

1. **Portfolio Revenue** (Table) - Grouped by App. Sum on Amount. Shows total revenue per app, sorted by total descending.
2. **Monthly Trend** (Table) - Grouped by Month. Sum on Amount. Chronological. Revenue + expenses.
3. **By Revenue Type** (Table) - Grouped by Revenue Type. Shows which monetization models work best.
4. **Expenses** (Table) - Filter: Is Expense = true. Grouped by Expense Category.
5. **P&L by App** (Table) - Shows revenue minus expenses per app per month.

### Portfolio Dashboard Page

**Row 1: Portfolio Metrics (4 columns)**
- Total Portfolio MRR (sum of all app MRR)
- Total Revenue (all time)
- Active Apps (count where Stage = Grow or Doubled Down)
- Average Revenue per App

**Row 2: App Comparison**
All apps side by side: MRR, DAU, Decision Status, Monthly Profit

**Row 3: Revenue Trend**
Monthly revenue over time, all apps stacked

**Row 4: Cost Efficiency**
Revenue per Hour Logged per app. Identifies which apps return the most per dev hour invested.

---

## Database 6: Daily Build Log

### Properties

| Property | Type | Details |
|----------|------|---------|
| Log Entry | Title | Date + short description |
| Date | Date | Log date |
| App | Relation → Build Tracker | Which app you worked on |
| Hours | Number | Hours spent today |
| What I Did | Text (long) | Detailed work log |
| Blockers | Text | What's blocking progress |
| Next Steps | Text | Tomorrow's plan |
| Shipped Something | Checkbox | Did you ship/deploy something today? |

### Views

1. **Today** (Table) - Filter: Date = today. Shows all work done today.
2. **By App** (Table) - Grouped by App. Shows total hours and recent entries.
3. **Ship Days** (Table) - Filter: Shipped Something = true. Calendar of days you actually shipped.
4. **Weekly Summary** (Table) - Grouped by week. Total hours, apps worked on, items shipped.

---

## Cross-Database Relations Map

```
Idea Vault → Build Tracker (idea promotion)
Build Tracker ←→ Revenue Dashboard (app revenue)
Build Tracker ←→ ASO Tracker (app optimization)
Build Tracker ←→ Deployment Checklist (launch process)
Build Tracker ←→ Daily Build Log (work tracking)
```

---

## 10-App 90-Day Framework (Pre-loaded content)

The template includes a static page with the build philosophy:

```
THE 90-DAY APP FACTORY PROTOCOL

Week 1-2: Idea Evaluation Sprint
- Dump 20+ ideas into the Idea Vault
- Score all of them
- Pick top 3 to build simultaneously
- Spec all 3 before building any

Week 3-4: Build Sprint 1
- Ship App 1 (simplest/fastest first)
- Start building App 2
- Evaluate App 1 metrics at Day 7

Week 5-6: Build Sprint 2
- Ship App 2
- Start building App 3
- Evaluate App 1 at Day 21 (first real signal)
- Evaluate App 2 at Day 7

Week 7-8: Build Sprint 3
- Ship App 3
- Review all 3 apps: kill/continue/double-down
- Pick next 2-3 ideas from vault
- Start building

Week 9-10: Build Sprint 4
- Ship Apps 4-5
- First kill/double-down decisions on Apps 1-3
- Reallocate time from killed apps to winners

Week 11-12: Build Sprint 5
- Ship Apps 6-8
- Kill/double-down cycle on all live apps
- Portfolio review: which apps are worth marketing spend?

Week 13 (Day 90): Portfolio Review
- Ship Apps 9-10 (or fewer if doubled-down on winners)
- Full portfolio audit
- Decision: next 90-day plan
- Expected outcome: 2-3 apps showing traction, 3-4 killed, rest in evaluation

TARGET: 10 apps shipped, 2-3 showing traction, 1 potential winner
REALITY: You'll likely ship 6-8 and kill 2-3. That's fine. The system works.
```

---

## Setup Instructions

1. Duplicate this template to your Notion workspace
2. Read the 90-Day Protocol page
3. Start dumping ideas into the Idea Vault (aim for 20+)
4. Score and evaluate ideas (the formula does most of the work)
5. Promote top 2-3 ideas to Build Tracker
6. Create Deployment Checklists for each app
7. Log daily work in the Daily Build Log
8. After shipping, update MRR, DAU, and other metrics weekly
9. Check Decision Status formula every 2 weeks for kill/double-down signals
10. Review Portfolio Dashboard monthly

Time to setup: 15 minutes
