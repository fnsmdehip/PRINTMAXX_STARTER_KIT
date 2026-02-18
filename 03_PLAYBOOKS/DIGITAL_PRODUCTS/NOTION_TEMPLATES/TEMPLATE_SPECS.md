# Notion Template Product Specifications

**Lane 2: Capital Genesis - $0 Startup, Day 1 Revenue**
**Platform:** Gumroad
**Total SKUs:** 5 templates across 3 niches (Faith, Fitness, Productivity/AI)
**Price Range:** $7 - $27
**Revenue Target:** $500-2,000/mo within 60 days

---

## Template 1: Prayer Warrior Daily Tracker

**Niche:** Faith (N002)
**Price:** $9
**Target Buyer:** Christians 18-35 wanting consistent daily devotional practice. People who have tried journaling or prayer apps but never stuck with them. The "I keep forgetting to pray" crowd.
**Buyer Psychology:** Guilt about inconsistency + desire for spiritual depth + love of organization systems

### Pages

1. **Daily Devotional Log** - Date, scripture reading, key takeaway, prayer time, personal reflection. Pre-formatted with morning/evening sections. Includes a "What is God saying to me today?" prompt field.

2. **Prayer Request Tracker** - Central hub for all prayer requests. Columns: Request, Person/Situation, Date Added, Status (Praying/Answered/Ongoing), Date Answered, How God Answered. Gallery view for visual tracking. Answered prayers move to a "Praise Report" archive automatically.

3. **Scripture Memory System** - Card-based system. Each card: Verse reference, full text, topic tag, difficulty level (1-5), last reviewed date, mastery status. Spaced repetition logic: surfaces verses you haven't reviewed in 7+ days. Gallery view shows verse cards. Board view groups by mastery level.

4. **Gratitude Journal** - Daily 3-item gratitude log. Fields: Date, three things grateful for, one person to thank today, blessing count (running total). Calendar view shows streaks. Monthly summary auto-generates.

5. **Weekly Reflection** - End-of-week review page. Prompts: What did God teach me this week? Where did I see Him working? What prayer was answered? What am I carrying into next week? Rating: Spiritual growth (1-5), Prayer consistency (1-5), Scripture engagement (1-5).

### Databases

1. **Prayer Requests DB**
   - Properties: Request (title), Person (text), Category (select: Family/Health/Career/Relationship/World/Church/Personal), Status (select: Praying/Answered/Ongoing/Paused), Date Added (date), Date Answered (date), How Answered (text), Urgency (select: Daily/Weekly/As Led), Notes (text)
   - Views: Active Prayers (filtered: status = Praying), Answered Prayers (filtered: status = Answered), By Category (board), Timeline (calendar by date added)

2. **Scripture Memory Bank**
   - Properties: Reference (title), Full Text (text), Topic (multi-select: Faith/Love/Strength/Wisdom/Peace/Courage/Provision/Grace), Book of Bible (select), Difficulty (number 1-5), Last Reviewed (date), Times Reviewed (number), Mastered (checkbox)
   - Views: Review Queue (sorted by last reviewed, ascending), By Topic (board), Mastered (filtered: mastered = true), All Verses (table)

3. **Daily Faith Tracker**
   - Properties: Date (title), Prayed Today (checkbox), Scripture Read (checkbox), Gratitude Logged (checkbox), Minutes in Prayer (number), Mood (select: Joyful/Peaceful/Grateful/Struggling/Seeking/Hopeful), Energy Level (select: High/Medium/Low), Journal Entry (text)
   - Views: This Week (filtered by date range), Monthly Calendar, Streak Counter (filtered: all 3 checkboxes = true), Mood Board (board by mood)

### Automations

- **Daily Entry Auto-Create:** Template button creates new daily log entry pre-filled with today's date, empty checkboxes, and rotating scripture prompt
- **Weekly Reflection Reminder:** Template button at week's end generates reflection page linked to that week's daily entries
- **Prayer Answer Prompt:** When status changes to "Answered," auto-prompts for "How God Answered" field

### Design Specifications

- **Color Palette:** Warm earth tones. Primary: #8B6F47 (warm brown). Secondary: #D4A574 (soft gold). Accent: #E8D5B7 (cream). Background: #FFF8F0 (warm white). Text: #3D2B1F (dark brown)
- **Typography:** Serif headings (suggest: Georgia or Playfair Display feel). Clean sans-serif body text.
- **Icons:** Cross, dove, open Bible, praying hands, olive branch, candle. Use Notion native emoji or simple Unicode symbols.
- **Header Images:** Soft watercolor-style banners. Sunrise/sunset tones. No stock photo people.
- **Layout:** Clean, spacious. Heavy use of callout blocks for scripture quotes. Dividers between sections. Toggle blocks for longer reflections.

### Gumroad Product Description (150 words max)

Your prayer life deserves better than a forgotten journal in your nightstand drawer.

Prayer Warrior Daily Tracker gives you one place for everything: daily devotionals, prayer requests with status tracking, scripture memorization with spaced repetition, gratitude logging, and weekly spiritual check-ins.

Built for Christians who want consistency without complexity.

What you get:
- Daily devotional log with morning/evening sections
- Prayer request database that tracks answered prayers (watch your faith grow)
- Scripture memory system with spaced repetition
- Gratitude journal with streak tracking
- Weekly reflection prompts that actually make you think

Stop feeling guilty about your inconsistent quiet time. Start building a prayer habit that sticks.

Duplicate the template. Fill in today's entry. That's it. Takes 5 minutes.

Over 40 pre-built prayer prompts included. Works on desktop and mobile.

---

## Template 2: 12-Week Body Recomp System

**Niche:** Fitness (N003)
**Price:** $17
**Target Buyer:** Men 25-45 wanting a structured fitness system. Intermediate lifters who know exercises but lack programming structure. The "I go to the gym but don't track anything" guy.
**Buyer Psychology:** Desire for structure + frustration with inconsistent results + willingness to invest in self-improvement

### Pages

1. **Program Overview** - 12-week macro view. Phase 1 (Weeks 1-4): Foundation. Phase 2 (Weeks 5-8): Growth. Phase 3 (Weeks 9-12): Peak. Each phase: training focus, calorie targets, progression rules, deload protocol.

2. **Weekly Workout Tracker** - 12 weekly pages. Each contains: 4-5 training days, exercises with sets/reps/weight fields, RPE tracker, session notes, weekly volume totals. Pre-populated with a proven Push/Pull/Legs split. Users can swap exercises from the library.

3. **Meal Prep Planner** - Weekly meal prep template. Breakfast/lunch/dinner/snacks for 7 days. Auto-calculates daily macros from meal database entries. Grocery list auto-generates from selected meals. Prep day checklist with time estimates.

4. **Progress Photo Log** - Bi-weekly photo reminder system. Fields: Date, weight, front/side/back photo placeholders, body fat estimate, energy level, sleep quality, notes. Comparison view shows Week 1 vs Current side by side.

5. **Supplement Tracker** - Daily supplement log. Current stack with dosage, timing, cost per serving. Monthly spend calculator. Effectiveness rating per supplement over time. Links to examine.com for evidence ratings.

6. **Body Measurements** - Bi-weekly measurement log. Chest, waist, hips, arms, thighs, calves, neck, shoulders. Auto-calculates changes from baseline. Chart-ready data format. Navy method body fat estimator.

### Databases

1. **Exercise Library DB**
   - Properties: Exercise Name (title), Muscle Group (multi-select: Chest/Back/Shoulders/Arms/Quads/Hamstrings/Glutes/Core/Calves), Equipment (select: Barbell/Dumbbell/Cable/Machine/Bodyweight/Bands), Movement Type (select: Compound/Isolation), Difficulty (select: Beginner/Intermediate/Advanced), Video Link (URL), Cues (text), Common Mistakes (text), Alternatives (relation to Exercise Library)
   - Pre-loaded with 80+ exercises across all muscle groups
   - Views: By Muscle Group (board), By Equipment (board), Full Library (table), Favorites (filtered: favorited = true)

2. **Meal Database**
   - Properties: Meal Name (title), Meal Type (select: Breakfast/Lunch/Dinner/Snack/Pre-Workout/Post-Workout), Calories (number), Protein (number), Carbs (number), Fat (number), Prep Time (number, minutes), Ingredients (text), Instructions (text), Batch Friendly (checkbox), Budget (select: $/$$/$$$)
   - Pre-loaded with 40 meals across all types
   - Views: By Meal Type (board), High Protein (filtered: protein > 30g), Quick Meals (filtered: prep < 15 min), Full List (table)

3. **Weekly Check-In DB**
   - Properties: Week Number (title), Weight (number), Body Fat % (number), Avg Sleep Hours (number), Energy (select: 1-5), Soreness (select: 1-5), Adherence % (number), PRs This Week (text), Adjustments Needed (text), Phase (select: Foundation/Growth/Peak/Deload)
   - Views: Progress Timeline (table sorted by week), Phase Overview (board by phase)

### Automations

- **Weekly Plan Generator:** Template button creates new week pre-filled with that phase's workout split from the exercise DB. User adjusts weights.
- **Grocery List Builder:** Selecting meals for the week auto-populates a grocery list page with all ingredients combined and quantities summed.
- **Deload Week Alert:** Week 4, 8, and 12 entries auto-tag as deload weeks with reduced volume recommendations.

### Design Specifications

- **Color Palette:** Dark mode default. Background: #1A1A2E (near black). Primary: #E94560 (bold red). Secondary: #16213E (dark blue). Accent: #0F3460 (steel blue). Text: #EAEAEA (light gray). Success: #00E676 (green for PRs).
- **Typography:** Bold sans-serif headings (Impact/Oswald feel). Clean body text. Numbers displayed prominently.
- **Icons:** Dumbbell, flame, target, chart-up arrow, clock, scale. Notion native emoji heavily used for quick scanning.
- **Header Images:** Dark gradient banners with fitness iconography. No stock photos. Clean typography overlays.
- **Layout:** Data-dense but scannable. Heavy use of table views. Number properties displayed large. Progress bars where possible. Toggle blocks for exercise instructions.

### Gumroom Product Description (150 words max)

You go to the gym 4 days a week and still look the same as 6 months ago.

The problem isn't effort. It's tracking.

12-Week Body Recomp System gives you the full stack: structured programming across 3 phases, 80+ exercises with video links, 40 pre-built meals with macros, progress photo tracking, body measurements, and weekly check-ins that force accountability.

What you get:
- 12 weeks of pre-programmed Push/Pull/Legs training
- Exercise library with 80+ movements, cues, and video links
- Meal database with auto-calculated macros and grocery lists
- Bi-weekly progress photo and measurement tracking
- Supplement tracker with cost analysis
- Weekly check-ins with built-in deload protocols

This is the system that replaces your $150/mo personal trainer.

Duplicate the template. Log your Week 1 numbers. Follow the program. See the difference in 12 weeks.

---

## Template 3: AI Tool Stack Dashboard

**Niche:** Productivity/AI (N001)
**Price:** $12
**Target Buyer:** Solopreneurs and creators 25-40 who use 5+ AI tools and lose track of what works, what costs what, and which prompts actually produce good output. The "I have 12 AI subscriptions and use 3 of them" person.
**Buyer Psychology:** Fear of wasting money on tools + FOMO about new AI tools + desire to systematize what works

### Pages

1. **Tool Comparison Matrix** - Master view of all AI tools in your stack. Side-by-side comparison on: cost, primary use case, output quality rating, speed, learning curve, integration with other tools. Sortable by any column. "Worth it?" column with ROI assessment.

2. **Workflow Builder** - Document your AI workflows step by step. Template: Workflow name, trigger, tools involved (in order), estimated time saved, output quality, frequency of use. Pre-built example workflows: Content repurposing, email drafting, research synthesis, code generation, image creation.

3. **Prompt Library** - Organized prompt collection. Each prompt: title, category, which AI model it works best with, the full prompt text, example output, quality rating, times used, notes on variations. Searchable and filterable by category and model.

4. **Cost Tracker** - Monthly AI spend dashboard. Each tool: monthly cost, annual cost, cost per use (estimated), ROI justification. Monthly total with budget limit. Alerts when spend exceeds threshold. Year-over-year comparison.

5. **Output Quality Ratings** - Rate the output of each tool/prompt combination over time. Track quality trends. Identify which tools are getting better/worse. Monthly review prompts: "Which tool surprised me? Which disappointed? What should I cancel?"

### Databases

1. **AI Tools DB**
   - Properties: Tool Name (title), Category (select: Writing/Image/Video/Audio/Code/Research/Automation/Other), Monthly Cost (number), Annual Cost (number), Primary Use Case (text), Output Quality (select: 1-5 stars), Speed (select: Fast/Medium/Slow), Learning Curve (select: Easy/Medium/Hard), Free Tier (checkbox), API Available (checkbox), Last Used (date), Worth Keeping (select: Yes/Maybe/Cancel), URL (URL), Notes (text)
   - Pre-loaded with 30 popular AI tools (ChatGPT, Claude, Midjourney, ElevenLabs, Cursor, Perplexity, etc.)
   - Views: Active Stack (filtered: worth keeping = Yes), By Category (board), Cost Analysis (table sorted by monthly cost desc), Underused (filtered: last used > 30 days ago)

2. **Prompt Library DB**
   - Properties: Prompt Name (title), Category (multi-select: Content/Email/Research/Code/Social/Strategy/Creative), Best Model (select: GPT-4/Claude/Gemini/Llama/Any), Full Prompt (text), Example Output (text), Quality Rating (select: 1-5), Times Used (number), Last Used (date), Tokens Est. (number), Notes (text)
   - Views: By Category (board), Top Rated (sorted by quality desc), Most Used (sorted by times used desc), Full Library (table)

3. **Monthly Spend Tracker DB**
   - Properties: Month (title), Tool (relation to AI Tools DB), Amount (number), Usage Count (number), Cost Per Use (formula), Notes (text)
   - Views: Monthly Summary (table grouped by month), By Tool (board), Spend Trend (table sorted by month)

### Design Specifications

- **Color Palette:** Clean minimalist with tech edge. Background: #FAFAFA (light gray). Primary: #6C63FF (electric purple). Secondary: #2D3436 (charcoal). Accent: #00B894 (teal green). Text: #2D3436. Code blocks: #1E1E1E (VS Code dark).
- **Typography:** Monospace for code/prompts (Fira Code feel). Clean sans-serif for everything else. Small caps for labels.
- **Icons:** Robot, brain, lightning bolt, terminal, chart, gear. Minimal, functional.
- **Header Images:** Clean gradient from purple to teal. No illustrations. Typography-focused.
- **Layout:** Dashboard-first. Numbers prominent. Toggle blocks for prompt text (keeps views clean). Inline databases for quick reference. Minimal scrolling on main page.

### Gumroad Product Description (150 words max)

You pay for 12 AI tools and actually use 3 of them well.

AI Tool Stack Dashboard is where you track every tool, every prompt, and every dollar spent on AI. See which tools earn their subscription. Find which prompts produce the best output. Kill the tools bleeding your wallet.

What you get:
- Tool comparison matrix with ROI tracking for 30+ AI tools
- Prompt library with quality ratings and best-model tagging
- Monthly cost tracker with per-use cost calculations
- 5 pre-built AI workflow templates (content, email, research, code, images)
- Output quality trends so you can see which tools are improving or declining

The average solopreneur wastes $87/month on AI tools they barely use. This template pays for itself the first month you cancel one subscription.

Duplicate. Add your tools. Rate your prompts. Cut what doesn't work.

---

## Template 4: Content Creator Command Center

**Niche:** Productivity/AI (N001/N016)
**Price:** $27
**Target Buyer:** Content creators managing 3+ platforms who feel scattered. The person who posts on TikTok, YouTube, Twitter, and Instagram but has no system to plan, track, or optimize across platforms. Full-time or aspiring full-time creators.
**Buyer Psychology:** Overwhelm from multi-platform management + desire for a "cockpit" view + willingness to pay more for a premium system

### Pages

1. **Content Calendar** - Visual calendar view of all content across all platforms. Drag and drop scheduling. Color-coded by platform. Status tracking: Idea, Drafting, Ready, Scheduled, Published, Analyzing. Weekly and monthly views. Filter by platform, niche, or content type.

2. **Idea Bank** - Capture ideas the moment they hit. Quick-add template: title, platform, content type, niche, why it might work, reference links. Priority scoring: Trending potential (1-5), Ease of creation (1-5), Monetization potential (1-5). Auto-calculates priority score.

3. **Analytics Dashboard** - Per-platform performance tracking. Fields per post: views, likes, comments, shares, saves, clicks, revenue generated. Weekly rollup of best performers. Monthly growth tracking: followers, engagement rate, revenue. "What's working" section auto-highlights top 10% posts.

4. **Platform Tracker** - Account details for every platform. Fields: username, follower count (updated weekly), engagement rate, monetization status (eligible/active/pending), content frequency target, actual posting frequency, notes. Health check: green/yellow/red status per platform.

5. **Monetization Tracker** - Every dollar tracked. Sources: sponsorships, affiliate, ad revenue, products, tips, memberships. Per-deal tracking: brand name, deal value, deliverables, deadline, payment status (invoiced/paid/overdue). Monthly and annual revenue dashboards. Tax-ready categorization.

6. **Collab Tracker** - Manage creator collaborations. Fields: creator name, platform, follower count, niche overlap score, collab type (guest/duet/shoutout/series), status (pitched/confirmed/completed/ghosted), results, notes. Pipeline view from outreach to completion.

### Databases

1. **Content Pieces DB**
   - Properties: Title (title), Platform (multi-select: YouTube/TikTok/Instagram/Twitter/LinkedIn/Newsletter/Blog/Podcast), Content Type (select: Short Video/Long Video/Carousel/Thread/Story/Article/Audio), Status (select: Idea/Scripting/Filming/Editing/Ready/Scheduled/Published/Analyzing), Niche (select: user-defined), Publish Date (date), Views (number), Likes (number), Comments (number), Shares (number), Revenue (number), Hook (text), Script/Copy (text), Links (URL), Thumbnail (files), Notes (text)
   - Views: Content Calendar (calendar by publish date), Kanban Board (by status), By Platform (board), Top Performers (sorted by views desc), Revenue Generators (filtered: revenue > 0)

2. **Monetization DB**
   - Properties: Source Name (title), Type (select: Sponsorship/Affiliate/Ad Revenue/Product/Tip/Membership/Other), Amount (number), Platform (select), Date Received (date), Invoice Status (select: Pending/Invoiced/Paid/Overdue), Brand Contact (text), Deliverables (text), Deadline (date), Recurring (checkbox), Notes (text)
   - Views: Monthly Revenue (table grouped by month), By Source Type (board), Pipeline (filtered: status = Pending or Invoiced), Annual Summary (table)

3. **Ideas DB**
   - Properties: Idea Title (title), Platform (multi-select), Content Type (select), Niche (select), Why It Works (text), Trending Score (number 1-5), Ease Score (number 1-5), Money Score (number 1-5), Priority (formula: avg of 3 scores), Reference URLs (URL), Added Date (date), Status (select: Fresh/Researching/Approved/Rejected)
   - Views: Priority Queue (sorted by priority desc), By Platform (board), Fresh Ideas (filtered: status = Fresh), Approved (filtered: status = Approved)

### Design Specifications

- **Color Palette:** Vibrant but professional. Background: #FFFFFF. Primary: #FF6B6B (coral red). Secondary: #4ECDC4 (teal). Accent: #FFE66D (yellow). Platform Colors: YouTube red, TikTok pink/cyan, IG gradient, Twitter blue, LinkedIn blue. Text: #2C3E50 (dark navy).
- **Typography:** Modern sans-serif throughout. Bold headings. Clean data presentation.
- **Icons:** Camera, film reel, chart, dollar sign, handshake, lightbulb, megaphone. Platform logos as emoji references.
- **Header Images:** Gradient banners with creator-themed icons. Bold, energetic. Abstract shapes over photos.
- **Layout:** Dashboard-first landing page with key metrics. Quick-add buttons prominently placed. Gallery views for visual content. Minimal clicks to log anything.

### Gumroad Product Description (150 words max)

You post on 4 platforms and have no idea what's working or how much money you're actually making.

Content Creator Command Center is the operating system for your creator business. One dashboard for content planning, analytics tracking, monetization logging, collaboration management, and idea capture across every platform.

What you get:
- Content calendar with drag-and-drop scheduling across all platforms
- Idea bank with automatic priority scoring (trending + ease + money potential)
- Analytics tracker per post with top-performer highlighting
- Revenue dashboard: sponsorships, affiliates, ads, products, tips all in one place
- Collab pipeline from pitch to completion
- Platform health tracker with weekly growth logging

This replaces your spreadsheet, your notes app, your sticky notes, and the 14 tabs you keep open.

Professional creators use systems. This is yours.

Duplicate. Add your platforms. Start tracking everything.

---

## Template 5: Morning Grace 7-Day Challenge

**Niche:** Faith (N002)
**Price:** $7
**Target Buyer:** Christians who want to start a morning devotional habit but feel overwhelmed by where to begin. Entry-level product designed to convert into Template 1 (Prayer Warrior Daily Tracker) buyers.
**Buyer Psychology:** Low commitment threshold + desire for guided experience + "challenge" format creates urgency and completion motivation

### Pages

1. **Welcome + How This Works** - Simple intro page. What you'll do each morning (15 minutes). What you'll need (Bible, this template, quiet space). How to set yourself up for success. Accountability partner setup section with a shareable invitation text.

2. **Day 1: Gratitude Awakening** - Theme: Starting with thankfulness. Scripture: Psalm 118:24. Prompt: List 10 things you're grateful for before your feet hit the floor. Prayer template: "Lord, thank you for..." (fill in). Reflection: What does gratitude change about how I start my day?

3. **Day 2: Listening Prayer** - Theme: Being still. Scripture: Psalm 46:10. Prompt: Set a 5-minute timer. Sit in silence. Write down whatever comes to mind afterward. Prayer template: "Lord, I'm listening for..." Reflection: What's hard about being quiet? What did you hear?

4. **Day 3: Scripture Meditation** - Theme: Going deeper into one verse. Scripture: Joshua 1:8. Prompt: Read the verse 3 times slowly. Write it in your own words. What does God want you to understand today? Prayer template: "Lord, write this on my heart..." Reflection: How does this verse apply to your current situation?

5. **Day 4: Confession + Freedom** - Theme: Letting go of weight. Scripture: 1 John 1:9. Prompt: What are you carrying that you need to release? Write it down (you can delete it after). Prayer template: "Lord, I confess..." Reflection: How does it feel to name it and let it go?

6. **Day 5: Intercession** - Theme: Praying for others. Scripture: James 5:16. Prompt: Write 5 names of people who need prayer. Pray specifically for each one. Prayer template: "Lord, I lift up [name] because..." Reflection: How does praying for others change your own perspective?

7. **Day 6: Worship + Declaration** - Theme: Speaking truth over your life. Scripture: Psalm 100:4. Prompt: Write 3 declarations about who God says you are. Say them out loud. Prayer template: "Lord, I declare that..." Reflection: Which declaration felt most powerful? Why?

8. **Day 7: Commissioning** - Theme: Taking this forward. Scripture: Proverbs 3:5-6. Prompt: What did you learn this week? What morning habit will you keep? Prayer template: "Lord, as I go forward..." Reflection: Letter to yourself about what you want your morning practice to become. CTA: Continue your journey with Prayer Warrior Daily Tracker (link to Template 1).

9. **Accountability Partner Setup** - Shareable summary page. "Hey [name], I'm doing a 7-day morning devotional challenge. Want to join me? Here's the link: [Gumroad link]. We can check in daily." Pre-written text message and email templates for inviting a friend.

### Design Specifications

- **Color Palette:** Soft sunrise theme. Background: #FFF9F0 (warm cream). Primary: #E8976D (sunrise coral). Secondary: #F5C77E (golden morning). Accent: #A8D8B9 (soft sage green). Text: #4A3728 (warm dark brown).
- **Typography:** Gentle serif headings. Clean body text. Scripture references in italic. Prompts in slightly different weight for distinction.
- **Icons:** Sunrise, candle, open hands, heart, dove, scroll. Soft, watercolor feel.
- **Header Images:** Watercolor sunrise gradient for each day. Day number prominently displayed. Gentle and inviting.
- **Layout:** One-page-per-day format. No database complexity. Simple text blocks, callouts for scripture, toggle blocks for journal entries. Feels like opening a devotional book, not a dashboard.

### Gumroad Product Description (150 words max)

You keep saying you'll start a morning prayer habit. Tomorrow. Next Monday. After things settle down.

Morning Grace is 7 days. 15 minutes each morning. Everything laid out for you.

Each day gives you:
- One scripture to sit with
- One journaling prompt that actually makes you think
- One prayer template so you're never staring at a blank page
- One reflection question to close

Day 1: Gratitude. Day 2: Listening prayer. Day 3: Scripture meditation. Day 4: Confession. Day 5: Praying for others. Day 6: Worship declarations. Day 7: Making it permanent.

No theological degree required. No 45-minute quiet time needed. Just you, your Bible, and 15 minutes before the day starts.

Includes accountability partner templates so you can invite a friend to do it with you.

Start tomorrow morning. See what 7 days changes.

---

## Cross-Template Relationships

```
Morning Grace ($7) ──upsell──> Prayer Warrior ($9) ──bundle──> Faith Bundle ($14)
                                                                      |
AI Tool Stack ($12) ──bundle with──> Content Creator ($27) = Productivity Bundle ($35)
                                                                      |
12-Week Recomp ($17) ──standalone or──> Complete Bundle ($47) <───────┘
```

## Production Notes

- Build order: Morning Grace first (simplest, fastest to create, lowest price = highest conversion)
- Each template should take 2-4 hours to build in Notion
- Export as Notion template link for Gumroad delivery
- All templates must work on mobile Notion app (test before listing)
- Include a "How to Use This Template" toggle on every template's main page
- Include PRINTMAXX branding subtly (small "Built by PRINTMAXX" in footer of welcome page)
