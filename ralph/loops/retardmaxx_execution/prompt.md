# Retardmaxx Execution Ralph Loop

**Task:** Execute ALL Capital Genesis retardmaxx tasks to ship revenue-generating assets

**Reference Files:**
- `OPS/setup/RETARDMAXX_MANUAL_TODO.md` - Manual task list
- `OPS/setup/RETARDMAXX_MANUAL_SETUP_CHECKLIST.md` - Detailed setup
- `OPS/CAPITAL_GENESIS_HUMAN_TASKS.md` - Human blockers
- `OPS/FIRST_1K_REVENUE_PLAN.md` - Revenue execution plan
- `OPS/GUMROAD_PRODUCT_SPECS.md` - Products to list
- `LEDGER/CONTENT_CALENDAR_30DAY.csv` - Content to post

## Execution Priorities (In Order)

### Priority 1: Immediate Revenue (0-3 Days)
**Can execute without human blockers:**

1. **Social Posts (295+ ready)**
   - Location: `AUTOMATIONS/content_posting/` (12 Buffer CSVs)
   - Action: Generate upload instructions for Buffer/Publer
   - Revenue impact: Algorithm reach → bio link traffic → Gumroad sales

2. **Gumroad Product Listings (4 PDFs ready)**
   - Location: `OPS/GUMROAD_PRODUCT_SPECS.md`
   - Action: Create full listing copy for all 4 products
   - Revenue impact: $7-47 per sale, conservative Week 1: $451

3. **Medium Articles (Ready to publish)**
   - Location: `CONTENT/medium_articles/`
   - Action: Format for Medium Partner Program
   - Revenue impact: Partner Program earnings + authority

4. **Reddit GEO Posts (6 ready)**
   - Location: `CONTENT/reddit/`
   - Action: Post to relevant subreddits with GEO optimization
   - Revenue impact: Organic search traffic → Gumroad

### Priority 2: Content Generation (3-7 Days)
**Build more content assets:**

5. **Newsletter Sequences (3 niches)**
   - Location: `MONEY_METHODS/NEWSLETTER/LAUNCH_ASSETS/generated/`
   - Action: Generate welcome sequences for faith/fitness/tech
   - Revenue impact: Email list growth → product sales

6. **AI UGC Scripts (10 videos)**
   - Location: `MONEY_METHODS/AI_INFLUENCER/ugc_scripts/`
   - Action: Generate video scripts for TikTok/Reels
   - Revenue impact: Platform creator fund + bio link traffic

7. **Cold Email Sequences (3 industries)**
   - Location: `CONTENT/email_sequences/cold/`
   - Action: Generate healthcare, legal, dental sequences
   - Revenue impact: High-ticket service sales ($500-2K)

### Priority 3: App Execution (7-14 Days)
**Ship apps to stores:**

8. **biomaxx Final Polish**
   - Location: `MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/`
   - Action: Final QA, generate App Store assets
   - Blocker: Apple Developer account (human)

9. **PrayerLock Salah Mode**
   - Location: `MONEY_METHODS/APP_FACTORY/builds/prayerlock/`
   - Action: Implement Salah mode spec
   - Revenue impact: 2B Muslim market, zero competitors

10. **Lock Apps Icon Generation**
   - Location: `MONEY_METHODS/APP_FACTORY/assets/`
   - Action: Generate icons using v3 prompts
   - Revenue impact: Higher conversion from better icons

### Priority 4: Service Packages (14-30 Days)
**Launch done-for-you services:**

11. **Service Package Landing Pages**
   - Location: `OPS/SERVICE_OFFERING_PACKAGES.md`
   - Action: Generate landing page copy for 8 services
   - Revenue impact: $300-2K per client

12. **Service Fulfillment SOPs**
   - Action: Document step-by-step for each service
   - Revenue impact: Scale via VA delegation

## Execution Rules

**SHIP, DON'T POLISH:**
- 80% quality ships, 100% never ships
- Done is better than perfect
- Revenue validates, not perfection

**WRITE ACTUAL FILES:**
- No planning-only work
- All outputs must be tangible deliverables
- Code, copy, assets - not just notes

**PARALLEL EXECUTION:**
- Work on Priority 1 + Priority 2 simultaneously
- Don't wait for one to complete before starting next
- Maximum velocity

## Output Files

**Create these deliverables:**

1. `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md` - How to bulk upload
2. `DIGITAL_PRODUCTS/listings/GUMROAD_LISTING_*.md` - All 4 product listings
3. `CONTENT/medium_articles/FORMATTED_FOR_MEDIUM.md` - Ready to copy-paste
4. `CONTENT/reddit/POSTING_SCHEDULE.md` - Which subreddit, when, what
5. `NEWSLETTER/LAUNCH_ASSETS/generated/WELCOME_SEQUENCES_*.md` - All 3 niches
6. `AI_INFLUENCER/ugc_scripts/UGC_BATCH_01.md` - 10 video scripts
7. `CONTENT/email_sequences/cold/HEALTHCARE_DENTAL_*.md` - Full sequences
8. `APP_FACTORY/builds/biomaxx-sdk54/APP_STORE_ASSETS.md` - Screenshots, copy
9. `APP_FACTORY/builds/prayerlock/SALAH_MODE_IMPLEMENTATION.md` - Code specs
10. `APP_FACTORY/assets/icons/GENERATED_ICONS.md` - All app icons
11. `SERVICE_OFFERING_PACKAGES/landing_pages/*.md` - All 8 services
12. `SERVICE_OFFERING_PACKAGES/sops/*.md` - All fulfillment guides

## Progress Tracking

Use `.ralph/progress.md` to track:
- Priority 1 tasks completed (out of 4)
- Priority 2 tasks completed (out of 3)
- Priority 3 tasks completed (out of 3)
- Priority 4 tasks completed (out of 2)
- Revenue estimate from completed tasks
- Blockers encountered

## Workflow Per Iteration

1. Check progress.md for next uncompleted task
2. Read relevant reference files
3. Generate deliverable (actual file, not plan)
4. Save to appropriate location
5. Update progress.md with completion + revenue estimate
6. Move to next task
7. Exit (next iteration starts fresh)

## Human Blockers to Flag

If you encounter these, flag in progress.md but continue with non-blocked tasks:
- Apple Developer account needed
- Google Play account needed
- Gumroad signup needed
- Stripe connect needed
- Domain/DNS setup needed
- Tool subscriptions needed

## Safety Rules

- Read only, no bash commands
- Create new files as needed
- All file writes within project directory only
- No deletions

## Success Criteria

- Complete all Priority 1 tasks (4/4)
- Complete 80%+ of Priority 2 tasks (2-3/3)
- Generate 50+ tangible deliverables
- Flag human blockers clearly
- Estimate conservative revenue from completed work
