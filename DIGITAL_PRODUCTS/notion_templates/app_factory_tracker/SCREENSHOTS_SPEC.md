# App Factory: Screenshots Specification

## Overview
8 screenshots total. Dark mode Notion. 16:9 aspect ratio. 2560x1440 resolution. PNG format.

---

## Screenshot 1: Portfolio Dashboard
**Purpose:** Hero image. Shows all apps side by side with key metrics and decision statuses.
**What to capture:**
- Table view with 8 apps listed
- Columns: App Name, Stage pill, MRR, DAU, Monthly Profit, Decision Status pill
- Decision Status colors: 2 "GROW" (purple), 1 "DOUBLE DOWN" (green), 2 "EVALUATE" (yellow), 1 "KILL" (red), 2 "BUILD" (blue)
- MRR values ranging from $0 (building) to $2,400 (top performer)
- The "KILL" app showing $12 MRR and 8 DAU (clearly not working)
- The "DOUBLE DOWN" app showing $2,400 MRR and 340 DAU
- Portfolio totals at bottom: Total MRR, Total Monthly Profit
**Crop:** Full table with all apps visible
**Used on:** Gumroad hero, Notion Marketplace hero, all marketplaces primary
**Filename:** `01_portfolio_dashboard.png`

## Screenshot 2: Build Pipeline Board
**Purpose:** Show the 8-stage development pipeline
**What to capture:**
- Kanban with columns: Spec (1), Design (1), Build (3), Test (1), Ship (0), Grow (4), Evaluate (2), Killed (1)
- Cards show: App Name, MRR (for live apps), Hours Logged, Days Live
- The "Killed" column card has a muted/grayed appearance
- Active builds showing tech stack pills
- More cards in Build and Grow stages (realistic distribution)
**Crop:** Full board view, all columns visible
**Used on:** Gumroad, Whop, Notion Marketplace
**Filename:** `02_build_pipeline.png`

## Screenshot 3: Idea Vault with Scoring
**Purpose:** Show the idea evaluation system with auto-scoring
**What to capture:**
- Table view sorted by Idea Score descending
- 10-12 ideas visible
- Columns: Idea Name, Category pill, Idea Score, Score Breakdown, Monetization Model, Build Time, Competition, Status
- Top idea showing score of 11/12
- Bottom ideas showing 3-4/12
- Mix of statuses: "Promoted to Build" (2), "Evaluated" (5), "Passed" (2), "Raw Idea" (3)
- Score Breakdown showing "MKT:3 MON:3 SPD:3 COMP:2" format
**Crop:** Table view, all scoring columns visible
**Used on:** Gumroad, all marketplaces
**Filename:** `03_idea_vault.png`

## Screenshot 4: Decision Board (Kill/Double-Down)
**Purpose:** Show the kill/double-down trigger system - the key differentiator
**What to capture:**
- Table view showing 6 live apps
- Columns: App Name, MRR, DAU, Kill Score, Growth Score, Decision Status, individual signal checkboxes
- One app with Kill Score = 3 showing red "KILL" status, checkboxes showing: <$100 MRR after 60d (checked), <50 DAU after 30d (checked), negative growth (checked)
- One app with Growth Score = 3 showing green "DOUBLE DOWN" status: MRR growth 20%+ (checked), organic growth (checked), feature requests (checked)
- Other apps showing EVALUATE or GROW
- Visual contrast between kill (red) and double-down (green) makes the system clear
**Crop:** Table with all decision columns visible
**Used on:** Gumroad hero variant, Whop, Notion Marketplace
**Filename:** `04_decision_board.png`

## Screenshot 5: Deployment Checklist
**Purpose:** Show the structured launch process
**What to capture:**
- Single app checklist page showing Pre-Launch phase
- 15 items visible, 10 checked off, 5 remaining
- Checkboxes clearly visible with completion progress
- Items like "Domain registered", "SSL active", "Analytics installed" checked
- Items like "Screenshots created", "Social preview set" unchecked
- App name and Phase visible in header
- Progress feels ~65% complete
**Crop:** Checklist page view
**Used on:** Gumroad, Etsy
**Filename:** `05_deployment_checklist.png`

## Screenshot 6: Revenue Dashboard
**Purpose:** Show portfolio-level revenue tracking
**What to capture:**
- Portfolio Metrics row: Total MRR ($4,127), Total Revenue ($18,940), Active Apps (5), Avg Revenue/App ($2,363)
- Revenue by app table showing 5 live apps with individual MRR and total revenue
- Monthly trend showing 3 months of growth (Jan: $2,100, Feb: $3,200, Mar: $4,127)
- Cost Efficiency section showing Revenue per Hour per app
**Crop:** Dashboard page showing metrics + tables
**Used on:** Gumroad, Notion Marketplace
**Filename:** `06_revenue_dashboard.png`

## Screenshot 7: Daily Build Log
**Purpose:** Show the daily work tracking system
**What to capture:**
- Table view showing 5 days of logs
- Columns: Date, App, Hours, What I Did (truncated), Shipped Something checkbox
- 2 days showing "Shipped" checked (green checkmarks)
- Hours ranging from 2-6 per day
- Different apps across different days (showing multi-app workflow)
- Weekly summary visible at bottom: Total Hours = 22, Apps Worked On = 3, Items Shipped = 2
**Crop:** Table with weekly summary
**Used on:** Gumroad, Whop
**Filename:** `07_build_log.png`

## Screenshot 8: ASO Tracker
**Purpose:** Show keyword and competitor tracking
**What to capture:**
- Keywords view showing 6-8 keywords for one app
- Columns: Keyword, Current Rank, Previous Rank, Rank Change, Search Volume, Difficulty
- Some keywords improving (green Rank Change: -3, -5)
- Some declining (red: +2)
- Search Volume pills (High, Medium, Low)
- Difficulty pills (Easy, Medium, Hard)
- One competitor entry visible below with rating and pricing
**Crop:** Table view with rank changes
**Used on:** Gumroad, Notion Marketplace
**Filename:** `08_aso_tracker.png`

---

## Marketplace-Specific Requirements

### Gumroad
- Cover: 1280x720 (Screenshot 1 or custom cover from LISTING.md spec)
- Gallery: Up to 7 images. Priority: 1, 4, 3, 2, 6, 5, 7

### Notion Marketplace
- Cover: 1600x900
- Gallery: Up to 5 images
- Priority: Screenshot 1, 4, 3, 6, 2

### Whop
- Cover: 1200x630
- Gallery: Up to 6 images
- Priority: Screenshot 1, 4, 2, 3, 6, 7

### Etsy
- Primary: 2700x2025 (reframed Screenshot 1)
- Gallery: Up to 10 images
- Use all 8 + 2 text-overlay slides (kill/double-down triggers explanation, 90-day protocol overview)

### Creative Market
- Cover: 1820x1214
- Preview: Up to 6 images
- Priority: Screenshot 1, 4, 3, 6, 2, 8

---

## Sample Data Guidelines

- Use realistic indie hacker app names (CalcStack, SnipBoard, QuickPoll, TweetMetrics, etc.)
- MRR range: $0 (building) to $2,400 (top performer) - realistic for indie apps
- DAU range: 0-500
- Build times: 2-14 days (fast shipper context)
- Show one clear winner, one clear loser, and rest in between
- Include at least one killed app to show the system handles failure
- Revenue numbers in the hundreds to low thousands (not inflated)
- Dark mode Notion theme for all screenshots
- Dates centered around January-March 2026 (showing 90-day arc in progress)
