# App Discovery & Distribution Engine

**Created:** 2026-02-12
**Status:** ACTIVE -- run weekly cadence
**Purpose:** Unified system for finding, analyzing, building, and distributing winning app concepts. Replaces ad-hoc discovery with a repeatable, data-driven pipeline.
**Supersedes:** Individual discovery files (APP_CLONE_REBRAND_STRATEGY.md, CLONECHART_DATA_EXTRACT.md, APP_ARBITRAGE_MATRIX.md, COMPETITOR_GTM_TACTICS.md, APP_STORE_AUDIT_FEB2026.md, APP_UIUX_RESEARCH.md, TOP_APP_AUDIT.md, APP_FACTORY_GTM_MASTER.md). Those files remain as deep-dive references. This engine UNIFIES them.

---

## 1. Revenue Intelligence Sources

Every app discovery decision starts with data. These are the platforms that show what's making money RIGHT NOW.

### Tier 1: Primary Discovery (Use Weekly)

| Platform | URL | What It Shows | Cost | How We Use It |
|----------|-----|--------------|------|---------------|
| **CloneChart.io** | https://clonechart.io/ | 12,000+ iOS apps with AI clone prompts, revenue estimates, tech stack, clone difficulty ratings (Easy/Medium/Hard). Updated daily. | Free browse, paid for full prompts | Filter: Easy-to-Clone + Revenue $5K+/mo. Pull clone prompts for Cursor/Claude. Check every Monday. |
| **Appkittie** | https://waitlist.appkittie.com | Revenue per app, downloads, winning ads, viral videos, winning apps updated daily. By @jacobrodri_. | Early access / waitlist | Join waitlist NOW. This shows the EXACT ads and viral content driving downloads. Gold for GTM. |
| **AppMagic** | https://appmagic.rocks/ | Revenue and download estimates for App Store and Google Play. Revenue Per Download (RpD) metric approximates LTV. ~10% monthly discrepancy on estimates. | Free tier limited, paid plans | Cross-reference CloneChart revenue estimates. Use RpD to identify high-LTV categories. Check top charts weekly. |
| **AppTweak** | https://www.apptweak.com/ | ASO intelligence, keyword research, download/revenue estimates powered by ML on 10+ years of data. Free Starter plan with lifetime access to basic estimates. | Free Starter plan, paid from $69/mo | Primary ASO tool. Free tier gives download + revenue estimates for any app. Use for keyword research before every app launch. |
| **RevenueCat State of Subscription Apps** | https://www.revenuecat.com/state-of-subscription-apps-2025/ | Annual report with conversion benchmarks, churn data, pricing analysis across 50K+ apps. The single most important data source for subscription pricing decisions. | Free (annual report) | Read once, reference constantly. Key numbers: 6.2% median trial start, 37.1% trial-to-paid, $0.38 median day-60 RPI on iOS. Our benchmark targets. |

### Tier 2: Validation & Deep Analysis

| Platform | URL | What It Shows | Cost | How We Use It |
|----------|-----|--------------|------|---------------|
| **Appfigures** | https://appfigures.com/ | Developer-focused analytics: keyword rank tracking, review monitoring, sales analytics, competitor benchmarking. Direct App Store Connect / Google Play Console integration. | Free: 5 apps tracked. $9.99/mo Connect plan. | Track OUR apps once launched. Monitor keyword rankings. Review monitoring for competitor 1-star reviews (feature gap mining). |
| **data.ai (App Annie)** | https://www.data.ai/ | Category rankings by country, download estimates, revenue estimates, engagement metrics. Still the largest app intelligence database. | Free tier limited, enterprise pricing | Check category rankings in target countries (Saudi Arabia, Brazil, India, Japan, Indonesia). Validate regional gaps. |
| **Sensor Tower** | https://sensortower.com/ | Top charts by country, keyword rankings, ad intelligence, audience demographics. | Free tier very limited, enterprise pricing | Use free tier for top chart browsing only. The paid product is enterprise-grade and overpriced for indie. |
| **Similarweb** | https://www.similarweb.com/ | Traffic and download estimates, in-app purchase intelligence, audience overlap. | Free tier limited | Quick validation: check if a competitor's downloads match their claimed revenue. |
| **Appark** | (search for latest URL) | Emerging in 2026 as indie-friendly alternative. Self-service model. | Varies | Evaluate as CloneChart/AppMagic alternative. Newer platform. |

### Tier 3: Community Intelligence (Free, High Signal)

| Source | URL | What It Shows | How We Use It |
|--------|-----|--------------|---------------|
| **Indie Hackers** | https://www.indiehackers.com/ | Revenue posts from real indie devs. "My app hit $X MRR" with proof. Portfolio strategies. | Filter for "app" posts with revenue numbers. Extract: what they built, how long, what worked. Add to ALPHA_STAGING.csv. |
| **r/SideProject** | https://reddit.com/r/SideProject | Real app launches with honest feedback. Revenue updates. | Monitor weekly. When someone posts revenue, note the app concept and check if we can niche/regional-arb it. |
| **r/indiehackers** | https://reddit.com/r/indiehackers | Revenue milestones, growth tactics, tool recommendations. | Same as above. Cross-reference with CloneChart data. |
| **Product Hunt** | https://www.producthunt.com/ | Daily trending apps and tools. Real user voting. | Check our categories (Health, Productivity, Lifestyle, Faith) weekly. Trending apps = validated demand. |
| **Twitter build-in-public** | Follow: @levelsio @tdinh_me @dannypostmaa @marc_louvion @jacobrodri_ | Real-time revenue reveals, growth tactics, tool recommendations. | Already in our HIGH_SIGNAL_SOURCES.csv. Cross-reference any revenue claims with CloneChart/AppMagic. |
| **Market Clarity** | https://mktclarity.com/blogs/news/indie-apps-top | Top 15 Most Profitable Indie Apps list with revenue data, growth strategies. | Quarterly reference. Check if any top indie apps are in categories we target. |
| **dabo.dev** | https://dabo.dev/revealing-my-revenue-metrics | Indie dev diary with actual revenue metrics exposed publicly. | Study real indie app economics: downloads, conversion, revenue, costs. |

### Tier 4: App Store Direct (Free, Mandatory)

| Method | What It Shows | How We Use It |
|--------|--------------|---------------|
| **App Store category browsing** | Real-time top charts, new apps, editorial picks. Switch regions. | Switch to SA (Arabic), MX (Spanish), IN (Hindi), BR (Portuguese), ID (Indonesian), TR (Turkish), JP (Japanese). Search our categories. If top results are English-only or poorly localized = opportunity. |
| **App Store reviews** | Actual user complaints and feature requests. | Read 1-2 star reviews of top 5 apps in every target category. Group complaints by theme. Top 3 complaint themes = our app's core features. This is FREE market research. |
| **App Store search suggest** | What users actually search for. Autocomplete = real demand. | Type "ramadan", "prayer", "fasting", "habit", "sleep" and see what autocomplete suggests. Those are real search terms with real volume. |
| **Apple iTunes RSS API** | https://rss.applemarketingtools.com/ | Real-time top charts data in JSON format. Free. No API key needed. | Automate weekly top chart pulls. Track position changes over time. See which new apps are climbing. |

---

## 2. Systematic App Discovery Process

### Phase 1: Find Winners (Monday, 1-2 hours)

**Goal:** Identify 5-10 app opportunities per week with validated revenue.

**Step 1: CloneChart scan**
- Open https://clonechart.io/chart/browse?show=1000
- Filter by categories: Health & Fitness, Productivity, Lifestyle, Education, Finance
- Sort by revenue (highest first)
- Filter clone difficulty: Easy to Clone
- Capture any app with: Easy difficulty + $5K+/mo revenue estimate
- Record in `LEDGER/APP_CLONE_OPPORTUNITIES.csv`: app_name, category, revenue_est, difficulty, clone_chart_url, date_found

**Step 2: AppMagic cross-reference**
- For each CloneChart candidate, search on AppMagic
- Compare revenue estimates (if >50% discrepancy, flag for manual validation)
- Check the Revenue Per Download (RpD) metric: apps with RpD > $1.00 have strong monetization
- Note download trends (growing vs declining)

**Step 3: AppTweak keyword check**
- Use free Starter plan
- For each candidate, check primary keywords
- Identify keyword difficulty score and search volume
- If keyword difficulty < 50 and search volume > 1K/month = strong ASO opportunity
- Check which languages the app supports (gaps = our opportunity)

**Step 4: Community scan**
- Search Indie Hackers for recent posts mentioning the app or category
- Search r/SideProject and r/indiehackers for related revenue posts
- Check Twitter for build-in-public mentions of similar concepts
- Note any real revenue numbers or user counts shared publicly

**Step 5: App Store direct**
- Search the App Store for the candidate's primary keyword
- Count the number of results and note the top 5 competitors
- Switch to Arabic, Spanish, Hindi, Japanese, Portuguese, Indonesian, Turkish stores
- For each language: is there a quality localized alternative? If not = regional arb opportunity
- Read 20-30 of the 1-star and 2-star reviews of the top 3 competitors
- Group complaints by theme. Top 3 complaints = our feature differentiation

**Output:** 5-10 validated opportunities added to `LEDGER/APP_CLONE_OPPORTUNITIES.csv` with columns: app_name, category, revenue_est_clonechart, revenue_est_appmagic, difficulty, primary_keywords, keyword_difficulty, languages_supported, language_gaps, top_complaints, regional_arb_score (0-10), niche_arb_score (0-10), composite_score, date_found, status

---

### Phase 2: Analyze Winners (Tuesday, 2-3 hours per app)

Pick the top 1-2 opportunities from Phase 1. Deep dive each.

**Step 1: Revenue verification**
Cross-reference revenue from 2+ sources:
- CloneChart.io estimate
- AppMagic estimate
- AppTweak download/revenue data
- Indie Hackers / Twitter public revenue claims
- Sensor Tower free tier (if available)
- Back-of-envelope calc: (estimated downloads/month) x (trial start rate 6.2%) x (trial-to-paid 37.1%) x (average price) = sanity check

Mark confidence level:
- HIGH: 2+ sources agree within 30%
- MEDIUM: estimates vary 30-60%
- LOW: only 1 source or >60% variance

**Step 2: Onboarding teardown**
- Download the app (or use screenshots from ScreensDesign.com / App Store preview)
- Document every screen: what it shows, what data it collects, where the paywall appears
- Note: number of screens, paywall type (hard/soft/feature-gated), trial length, pricing
- Compare against our benchmarks from `APP_UIUX_RESEARCH.md`:
  - Quiz-to-Diagnosis: 15-25% trial start (Noom, Cal AI, Rise)
  - Value-First Soft: 8-15% trial start but 40-50% trial-to-paid (ShutEye, Finch)
  - Feature-Gated: 5-10% trial start, steady over time (Structured, Muslim Pro)
  - Emotional Investment: 12-18% trial start (Fabulous, Finch)

**Step 3: Paywall analysis**
- What is the trial length? (3/7/14/30 days)
- What is the pricing? (monthly, annual, lifetime options)
- What does the paywall screen look like? (animated? personalized? loss-aversion framing?)
- Does it echo onboarding answers? (up to 65% conversion uplift per AppAgent data)
- Compare against RevenueCat 2025 benchmarks:
  - Health & Fitness: 5.3% median download-to-trial, 39.9% trial-to-paid
  - Productivity: 4.8% median, 42.3% trial-to-paid
  - Lower-priced apps ($3-5/mo): 47.8% trial-to-paid vs 28.4% for $10+/mo

**Step 4: Marketing copy analysis**
- App Store title, subtitle, description, keywords
- Website copy (if exists)
- Social media presence (Twitter, TikTok, Instagram)
- What channels do they use for acquisition?
- Do they have a blog for SEO? What do they rank for?

**Step 5: GTM reverse-engineering**
How did they get their first 1K-10K users? Check:
- Product Hunt launch (search PH for the app name)
- Reddit posts (search Reddit for the app name)
- Press coverage (Google News search)
- Influencer partnerships (search YouTube/TikTok for app name)
- Paid ads (check Facebook Ad Library for their ads)
- Reference our `COMPETITOR_GTM_TACTICS.md` for proven patterns

**Step 6: Review mining (THE MOST VALUABLE STEP)**
- Pull all 1-star and 2-star reviews from App Store
- Use Appfigures or AppFollow free tier for bulk review access
- Run through Claude: "Group these complaints by theme. Rank by frequency. For each theme, suggest a feature that solves it."
- Top 3 complaint themes = our app's core differentiators
- "I wish this had..." statements = direct feature roadmap
- This is free market research. Apple literally shows you what to build.

**Step 7: Tech stack identification**
- Check CloneChart for tech analysis (if available)
- Check BuiltWith.com for web tech
- Search GitHub: "{app name} clone" license:mit
- Search GitHub: "{app concept} react-native" OR "{app concept} nextjs" license:mit
- If MIT repo exists with 50+ stars and recent commits = fork-and-customize candidate

**Output per app:** Deep analysis doc saved to `MONEY_METHODS/APP_FACTORY/analysis/{app_name}_teardown.md`

---

### Phase 3: Repurpose Strategy (Wednesday, 1-2 hours)

For each analyzed winner, identify ALL possible repackaging angles.

**Angle 1: Regional arbitrage**
Check language support. If English-only or <10 languages:

| Target Language | Market Size | Competition Check | Priority |
|----------------|------------|-------------------|----------|
| Arabic | 400M+ speakers, mobile-first, huge faith market | Switch App Store to SA, search in Arabic | HIGHEST if faith/health app |
| Spanish | 550M+ speakers, LATAM mobile-first | Switch to MX, search in Spanish | HIGH for any category |
| Hindi | 600M+ speakers, India = fastest-growing app market | Switch to IN, search in Hindi | HIGH for faith/health |
| Portuguese | 260M+ speakers, Brazil = 5th largest app market | Switch to BR, search in Portuguese | HIGH for faith apps |
| Indonesian | 300M+ speakers, largest Muslim country | Switch to ID, search in Bahasa | HIGH for faith apps |
| Japanese | 125M speakers, high ARPU, Tamagotchi culture | Switch to JP, search in Japanese | HIGH for self-care/pet apps |
| Turkish | 80M+ speakers, high smartphone penetration | Switch to TR, search in Turkish | MEDIUM-HIGH |
| Korean | 50M speakers, high ARPU, wellness culture | Switch to KR, search in Korean | MEDIUM |
| French | 280M+ speakers, West Africa = fastest mobile growth | Switch to FR store | MEDIUM |
| German | 130M speakers, highest ARPU in Europe | Switch to DE store | MEDIUM |

**Angle 2: Demographic repackaging**
Can the same core concept serve a different audience?

| Demographic | Adaptations Needed | Example |
|-------------|-------------------|---------|
| Women | UI (softer palette, different imagery), features (cycle sync, pregnancy modes), copy (different voice) | "Fasting tracker" becomes "Cycle-synced fasting for women" |
| Men | UI (dark/matte, minimal), features (stoic philosophy, discipline framing), copy (direct/commanding) | "Affirmations" becomes "Stoic affirmations for men" |
| Teens/Students | UI (playful, gamified), features (study integration, exam countdowns, social), pricing (cheaper) | "Habit tracker" becomes "Study streak tracker for students" |
| Seniors | UI (large text, high contrast, simple nav), features (medication reminders, large buttons), copy (clear/patient) | "Water tracker" becomes "Hydration + medication reminder for seniors" |
| Parents | Features (family sharing, child tracking, parenting-specific habits) | "Mood tracker" becomes "Family mood check-in" |
| Specific professions | Features (shift-aware, industry-specific habits) | "Pomodoro timer" becomes "Clinical task timer for nurses" |
| Specific faiths | Features (prayer times, scripture, religious calendar), UI (faith-appropriate colors/imagery) | "Meditation timer" becomes "Dhikr + prayer timer for Muslims" |

**Angle 3: Niche vertical cloning (the niche ladder)**
```
Level 0: "Meditation app" (10,000+ competitors)
Level 1: "Meditation for anxiety" (1,000+ competitors)
Level 2: "Meditation for new mothers" (50-100 competitors)
Level 3: "Islamic meditation (Muraqaba) for women" (0-5 competitors) <-- TARGET THIS
```

Go as specific as possible. Zero competition at Level 3 means you rank for that keyword immediately.

**Angle 4: Feature gap exploitation**
From Phase 2 review mining: build the app that fixes what the top apps refuse to fix.

**Angle 5: Platform arbitrage**
- iOS-only app with 100K+ downloads? Build the Android version (or PWA that works everywhere).
- Mobile-only tool with web requests in reviews? Build the PWA with cross-device sync.
- Complex app with "too bloated" complaints? Build the lightweight version (10MB vs 600MB).

**The 3-3-3 differentiation test (before building ANY "inspired by" app):**
1. 3 unique features not found in the inspiration app
2. 3 UX improvements based on review mining
3. 3 design differences visible in screenshots

If you can't hit 3-3-3, the app isn't differentiated enough.

**Output:** Repurpose strategy added to `LEDGER/APP_CLONE_OPPORTUNITIES.csv` with: arb_type (regional/demographic/niche/platform/feature_gap), target_audience, target_language, unique_features_planned, estimated_build_time, estimated_revenue

---

### Phase 4: Build Fast (Thursday-Sunday, 3-7 days per app)

**Step 1: Check for existing MIT repos**
```
GitHub search:
- "{app concept} clone" license:mit stars:>50
- "{app concept}" license:mit language:typescript
- "{app concept}" license:mit language:javascript
- "{app concept} react-native" license:mit
- "{app concept} nextjs" license:mit
```
If found: fork, audit for security (no malware, no tracking, no API key leaks), customize.
If not found: build from scratch using our PWA template.

**Step 2: Get the CloneChart prompt (if available)**
- Copy the Cursor/Claude prompt from CloneChart
- Modify to add: our design system (AGGREGATE_DESIGN_SYSTEM.md), our niche features, our monetization model
- Use as starting architecture, not as final product

**Step 3: Build as PWA first**
- Stack: Next.js + Tailwind CSS + shadcn/ui
- Follow AGGREGATE_DESIGN_SYSTEM.md for visual design
- Follow ONBOARDING_PLAYBOOK.md for onboarding flow
- Implement paywall (RevenueCat for native, custom for PWA)
- Add analytics (Plausible or Umami, free tier)
- Build offline-first (service worker, IndexedDB)
- Target: under 50MB app size (most competitors are 200-600MB)

**Step 4: Native wrapper (if going to App Store)**
- Use Capacitor to wrap PWA for iOS/Android
- Add native features: haptics, push notifications, widgets, Apple Health
- Follow IOS_REJECTION_PREVENTION.md for submission
- Follow APP_QUALITY_STANDARDS.md for quality gate

**Step 5: Test**
- Run in iOS Simulator
- Test all onboarding screens
- Test paywall flow
- Test offline mode
- Lighthouse score > 90
- Check APP_QUALITY_STANDARDS.md pre-submission checklist

**Output:** Working app ready for deployment. Code in `ralph/loops/app_factory/output/{app-name}/` or `MONEY_METHODS/APP_FACTORY/builds/{app-name}/`

---

### Phase 5: Distribution (Launch Day + First 30 Days)

Our existing distribution infrastructure:
- 43 social accounts across 5 niches
- 4 newsletters (Beehiiv/Substack)
- 1,278 content posts ready for scheduling
- 16 live websites on surge.sh
- Cold email pipeline (3,000+ leads)
- Buffer CSVs ready for bulk upload

**Pre-launch (2 weeks before):**

| Action | Details | Time |
|--------|---------|------|
| ASO optimization | Title: [Brand] - [Primary Keyword]. Subtitle: [Secondary Keyword] + Benefit. Keyword field: 100 chars, no spaces after commas, include competitor names. | 2 hours |
| App Store screenshots | 6 screenshots. #1 = actual UI. #2 = differentiating feature. #3-5 = one feature each. #6 = social proof. Use phone mockup + text overlay (83% of top apps use this). | 3 hours |
| Reddit karma building | Comment helpfully in target subreddits for 2+ weeks. Do NOT just lurk. Build karma so your launch post doesn't get removed. | 30 min/day for 14 days |
| Product Hunt listing | Draft listing: tagline, description, images, first comment. Find a well-known hunter to submit. | 2 hours |
| TikTok content | Film 5 videos showing the app mechanic. NOT features. The mechanic. "I locked my phone until I walked 5000 steps" > "Steplock has step tracking." | 3 hours |
| Influencer outreach | Contact 10-20 nano-influencers in the niche. Offer free lifetime premium for honest review. | 2 hours |
| Blog post | "Why I built [app name]" for SEO + authenticity. | 2 hours |
| Landing page | Simple page: hero, screenshots, download link, email capture. Deploy on Vercel. | 1 hour |

**Launch Day (Tuesday or Wednesday, not Monday):**

| Hour | Action |
|------|--------|
| 12:01 AM PT | Product Hunt goes live |
| 6 AM | Tweet thread: build-in-public story from @PRINTMAXXER |
| 8 AM | Reddit post in 2-3 target subreddits: "I built this for [community]" |
| 9 AM | Email newsletter to existing users (cross-promote from other apps) |
| 10 AM-6 PM | Respond to EVERY Product Hunt and Reddit comment within 30 minutes |
| 12 PM | TikTok video 1 posted |
| 6 PM | Share early download numbers on Twitter (transparency = engagement) |

**Week 1 post-launch:**
- Post TikTok videos 2-5
- Engage in Reddit comments daily
- Ship one feature based on first user feedback (shows responsiveness)
- Share user testimonials on social
- Update ASO based on first search data from App Store Connect
- Cross-promote from existing portfolio apps

**Week 2-4:**
- Content marketing blog posts published (SEO long-tail targeting)
- Influencer reviews go live
- A/B test paywall (hard vs soft, trial length, pricing)
- Cross-promote from existing portfolio apps (in-app "More from PRINTMAXX" section)
- Track CPI per channel, double down on what works
- Begin next app build

**Distribution channels by app:**

| App | Primary Subreddits | TikTok Hook | Influencer Niche |
|-----|-------------------|-------------|-----------------|
| Hilal | r/islam (1.2M), r/MuslimLounge (200K), r/Ramadan (20K) | "My Ramadan routine with this tracker" | Muslim lifestyle creators |
| PrayerLock | r/islam, r/MuslimLounge, r/productivity (2M) | "Never missed a prayer in 30 days" | Islamic content creators |
| Dusk | r/sleep (400K), r/insomnia (100K), r/selfimprovement (2M) | "My sleep score before vs after" | Sleep/wellness creators |
| Vault | r/ADHD (1.7M), r/productivity (2M), r/getdisciplined (1M) | "This app locked TikTok until I finished my Pomodoro" | ADHD creators |
| Streakr | r/theXeffect (60K), r/getdisciplined (1M) | "Don't break the streak" challenge | Productivity YouTubers |
| Mise | r/MealPrepSunday (3M), r/EatCheapAndHealthy (3M) | "I meal prepped for a week in 30 minutes" | Meal prep creators |
| Steplock | r/walking (100K), r/loseit (3M), r/C25K (400K) | "This app locked my Instagram until I walked 5,000 steps" | Fitness/walking creators |

---

### Phase 6: A/B Test Everything (Ongoing)

Use `scripts/experiment_runner.py` to track all tests.

**Priority tests (run in this order):**

| # | Test | Why | Expected Impact |
|---|------|-----|-----------------|
| 1 | Hard vs soft paywall | 2-5x conversion difference. This is the single most impactful decision. | Revenue 2-5x |
| 2 | Trial length (3-day vs 7-day vs 14-day) | Shorter = more urgency. Longer = more attachment. 82% of trial starts happen day 0. | Conversion 10-30% |
| 3 | Annual vs monthly default selection | Annual = higher LTV. Monthly = lower barrier. Pre-select annual with monthly as option. | LTV 20-40% |
| 4 | Pricing ($19.99 vs $24.99 vs $29.99/year) | Sweet spot varies by category. Lower = 47.8% trial-to-paid. Higher = more revenue per sub. | Revenue varies |
| 5 | Onboarding length (3 screens vs 5 vs 7) | Quiz-to-diagnosis (7+ screens) converts 15-25%. Value-first (3 screens) converts 8-15% but retains better. | Conversion vs retention tradeoff |
| 6 | Paywall animation (static vs animated) | Strategic animation improves conversion 15-30% per AppAgent data. | Conversion 15-30% |
| 7 | Lifetime purchase option (include or not) | Captures subscription-averse users. $49.99 lifetime vs not offering it. | Revenue 5-15% (incremental) |
| 8 | App name (test 2-3 options for same concept) | Different names, same app. See which gets more downloads. | Downloads vary |
| 9 | Icon style (gradient vs dark vs light) | 8/15 top apps use gradient. 5/15 dark. 0/15 have text in icon. | Downloads vary |
| 10 | Paywall personalization echo | Re-state user's onboarding answers on paywall. Up to 65% conversion uplift. | Conversion up to 65% |

**How to run tests:**
```bash
# Start a new experiment
python3 scripts/experiment_runner.py start --name "hilal_hard_vs_soft_paywall" --variants "hard,soft" --metric "trial_start_rate"

# Log daily results
python3 scripts/experiment_runner.py log --name "hilal_hard_vs_soft_paywall" --variant "hard" --conversions 45 --impressions 500

# Check if statistically significant
python3 scripts/experiment_runner.py analyze --name "hilal_hard_vs_soft_paywall"
```

---

### Phase 7: Alpha Integration (Continuous)

**App-related alpha flows in from:**
- `LEDGER/ALPHA_STAGING.csv` (category: APP_FACTORY)
- Twitter scraper: `python3 AUTOMATIONS/twitter_alpha_scraper.py --all`
- Reddit scraper: `python3 AUTOMATIONS/background_reddit_scraper.py --scrape`
- Overnight ralph loops (daily_alpha, alpha_hunter)

**Weekly review process (Thursday):**
1. Filter ALPHA_STAGING.csv for APP_FACTORY category entries from the past week
2. For each APPROVED entry: does it suggest a new app? A new feature? A pricing insight? An ASO tip?
3. Route to appropriate action:
   - New app concept: add to `LEDGER/APP_CLONE_OPPORTUNITIES.csv`
   - New feature for existing app: add to that app's backlog
   - Pricing/conversion insight: update our A/B test defaults
   - ASO tip: apply to all relevant apps immediately
   - GTM tactic: add to `COMPETITOR_GTM_TACTICS.md`

**Monthly review (first Monday of month):**
1. Which A/B test results should change our defaults?
2. Which app concepts from alpha are still unbuilt?
3. Which apps are underperforming their CloneChart revenue estimates? Why?
4. What new categories or niches emerged from alpha this month?
5. Update this engine doc with any new patterns or sources discovered.

---

## 3. Weekly Cadence

| Day | Activity | Time | Output |
|-----|----------|------|--------|
| **Monday** | Scan CloneChart + AppMagic for new winners. Check Product Hunt trending. Browse App Store top charts in 5 categories x 5 countries. | 1-2 hours | 5-10 candidates in APP_CLONE_OPPORTUNITIES.csv |
| **Tuesday** | Deep teardown of top 1-2 candidates. Full revenue verification, onboarding teardown, review mining, tech stack ID. | 2-3 hours | Teardown doc in analysis/ folder |
| **Wednesday** | Repurpose strategy. Map all arb angles (regional, demographic, niche, platform, feature gap). 3-3-3 differentiation test. | 1-2 hours | Updated APP_CLONE_OPPORTUNITIES.csv with arb columns |
| **Thursday** | Review alpha feed for app-related tips. Check A/B test results. Update experiment defaults if significant results found. | 1 hour | Alpha routed, tests analyzed |
| **Friday** | Ship one iteration: new feature on existing app, new app build started, or new regional variant launched. | 3-8 hours | Shipped increment |
| **Saturday-Sunday** | Continue build if in progress. Content creation for upcoming launch. TikTok filming. Reddit engagement. | Optional | Content + build progress |

---

## 4. Integration with Existing Systems

### Quant Terminal
```bash
# System health including app metrics
python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary
```
The quant terminal pulls from LEDGER CSVs. App revenue logged via `scripts/revenue_intake.py` appears in the terminal dashboard.

### Alpha Staging
All app discovery findings that qualify as alpha go to `LEDGER/ALPHA_STAGING.csv` with category APP_FACTORY. Reviewed via `/review-alpha` workflow.

### Content Calendar
Every app launch generates content (per Max Squeeze Protocol):
- 3+ tweets
- 1 tweet thread ("How I built X")
- 1 Reddit launch post
- 1 newsletter section
- Scheduled via `LEDGER/CONTENT_CALENDAR_30DAY.csv`
- Buffer CSVs in `AUTOMATIONS/content_posting/`

### Experiment Runner
All A/B tests tracked via `scripts/experiment_runner.py`. Results feed back into discovery (Phase 7).

### Revenue Tracking
```bash
# Log app revenue
python3 scripts/revenue_intake.py log --method APP_FACTORY --amount 150 --source "hilal_appstore" --notes "Feb subscription revenue"

# View app revenue summary
python3 scripts/revenue_intake.py summary --method APP_FACTORY
```

### Account Tracker
```bash
# Track app submissions and account status
python3 scripts/account_tracker.py status
```

### Self-Test
```bash
# Validate app factory ops readiness
python3 scripts/self_test.py --op APP_FACTORY
```

### Cron Automation
The overnight system (`AUTOMATIONS/overnight_master_runner.sh`) runs:
- Alpha scrapers that feed app-related findings
- RBI scanner that identifies zero-cost app opportunities
- Daily TODO generator that surfaces app actions

---

## 5. Revenue Intelligence Benchmarks (Reference Card)

### RevenueCat 2025 Conversion Benchmarks

| Metric | Median | P90 (Top 10%) | Our Target |
|--------|--------|---------------|------------|
| Download-to-Trial (Health & Fitness) | 5.3% | 12.1% | 8%+ |
| Download-to-Trial (Productivity) | 4.8% | 11.2% | 8%+ |
| Trial-to-Paid (all categories) | 37.1% | - | 40%+ |
| Trial-to-Paid (lower price $3-5/mo) | 47.8% | - | 45%+ |
| Day-60 Revenue Per Install (iOS) | $0.38 | $1.10+ | $0.60+ |
| Day-60 Revenue Per Install (H&F) | $0.63 | $1.85+ | $1.00+ |

### Key Timing Data
- 82% of trial starts happen on Day 0 (same day as install)
- 78% of trial starts happen in first week
- "Not enough usage" is #1 cancellation reason (32-47%)

### Pricing Sweet Spots (from 24-app audit)

| Tier | Monthly | Annual | Lifetime |
|------|---------|--------|----------|
| Budget (faith/simple) | $2.99 | $19.99 | $29.99 |
| Standard (health/habit) | $3.99-$4.99 | $24.99-$29.99 | $49.99 |
| Premium (nutrition/sleep) | $6.99-$9.99 | $39.99-$49.99 | $79.99 |
| Ultra (coaching/AI) | $12.99-$14.99 | $69.99 | $149.99+ |

### Revenue Projections by Portfolio Size

| Apps | Monthly Downloads (each) | At Median Conversion | At P90 Conversion |
|------|------------------------|---------------------|-------------------|
| 5 | 1,000 | $1,200/mo | $3,600/mo |
| 7 | 3,000 | $5,500/mo | $16,500/mo |
| 10 | 5,000 | $15,500/mo | $46,500/mo |
| 15 | 5,000 | $23,000/mo | $70,000/mo |
| 30 | 5,000 | $46,000/mo | $140,000/mo |

These projections assume: $24.99/year average price, Health & Fitness conversion rates. Real-world performance depends on ASO, marketing, product quality, and niche competition.

---

## 6. Active Arbitrage Opportunities (from APP_ARBITRAGE_MATRIX.md)

### Top 15 Ranked by Composite Score

| Rank | ID | Opportunity | Score | Build Time | Revenue Est |
|------|-----|------------|-------|------------|-------------|
| 1 | ARB-003 | Spanish Gratitude Journal | 9.3 | 3-5 days | $2-5K/mo |
| 2 | ARB-008 | Stoic Affirmations for Men | 9.3 | 3-5 days | $3-10K/mo |
| 3 | ARB-001 | Arabic Fasting Tracker (Hilal) | 9.0 | 5-7 days | $5-15K/mo |
| 4 | ARB-005 | Hindi Hindu Spiritual App | 9.0 | 2-3 weeks | $10-30K/mo |
| 5 | ARB-004 | Portuguese Prayer App (Brazil) | 8.7 | 1-2 weeks | $3-8K/mo |
| 6 | ARB-011 | Sleep Sounds Without Tracking | 8.3 | 3-5 days | $2-5K/mo |
| 7 | ARB-002 | Japanese Self-Care Pet (Finch clone) | 8.0 | 3-4 weeks | $5-15K/mo |
| 8 | ARB-006 | Meditation-to-Prayer Timer Adapter | 8.0 | 1-3 days | $2-5K/mo |
| 9 | ARB-009 | Couples Habit Tracker | 8.0 | 2-3 weeks | $2-5K/mo |
| 10 | ARB-010 | Lightweight Pomodoro (10MB vs 617MB) | 8.0 | 1-2 days | $1-3K/mo |
| 11 | ARB-013 | Cycle-Synced Fasting for Women | 8.0 | 2-3 weeks | $5-15K/mo |
| 12 | ARB-015 | Desktop/Web Versions of Mobile-Only Apps | 7.7 | Varies | $1-3K/mo |
| 13 | ARB-012 | Privacy-First Habit Tracker (Local Only) | 7.3 | 1 week | $1-3K/mo |
| 14 | ARB-007 | Noom Psychology at 1/10th Price | 7.0 | 3-4 weeks | $5-20K/mo |
| 15 | ARB-014 | iOS Apps as Android PWAs | 7.0 | 1-2 weeks | $1-5K/mo |

### Quick-Ship Tier (build this week, 1-5 days each)
- Stoic Affirmations for Men (3 days, PWA)
- Spanish Gratitude Journal (3 days, PWA)
- Lightweight Pomodoro (1 day, PWA)
- Sleep Sounds (3 days, PWA + audio)
- Meditation-to-Prayer Timer (1-3 days, PWA)

Combined potential: $10-28K/month from 5 simple apps.

---

## 7. Proven Case Studies (Real Revenue, Real Numbers)

These are verified indie app success stories. Not guru claims. Real numbers from real developers.

| Developer | What They Built | Revenue | Time | Key Tactic |
|-----------|----------------|---------|------|------------|
| Max Artemov | 30-app portfolio (productivity/health) | $22K/mo | 1 year | Portfolio diversification, ASO focus |
| Anonymous | 30-app portfolio (rebuilt after Apple freeze) | $60K/mo | 2 years | Restarted from scratch, niche targeting |
| Studio (unnamed) | Subscription mobile app portfolio | $185K/mo MRR | 3 years | Subscription-first, cross-promotion |
| Cal AI founders | AI calorie tracker (two teenagers) | $2M+/month | 1 year | Quiz-to-diagnosis paywall, TikTok ads |
| Opal (Kenneth) | Screen time management | $10M ARR | 2 years | 11-person team, A/B test everything weekly, monetize from day 1 |
| Finch | Self-care virtual pet | $36M ARR | 4 years | TikTok organic, ambassador program, Gen-Z mental health positioning |
| Muslim Pro (Bitsmedia) | Islamic lifestyle app | $30-50M ARR | 10+ years | Zero marketing budget, pure utility, 22 languages, Ramadan seasonal spikes |
| Formula Bot | AI spreadsheet tool | $220K MRR | 18 months | Product Hunt launch ($6K in 48 hours), solo founder, no-code MVP |
| Roman Koch | Indie dev portfolio | Public metrics at dabo.dev | Ongoing | Transparent revenue metrics, building in public |
| Gary Brewer (BuiltWith) | Web technology profiler | ~$14M/yr | Long-running | Near-zero employees, automation-first |

**Key pattern across all:** Ship fast, measure, kill losers, double down on winners. Nobody got rich on their first app. The portfolio approach compounds.

---

## 8. Cross-Promotion Engine (Portfolio Flywheel)

Once 3+ apps have active users:

### In-App Cross-Promotion

| If User Has... | Promote... | Trigger | Message |
|----------------|-----------|---------|---------|
| Hilal (Ramadan) | PrayerLock | After Ramadan ends | "Keep your prayer streak going year-round" |
| PrayerLock | Hilal | 30 days before Ramadan | "Ramadan is coming. Track fasting, Quran, charity" |
| Dusk (sleep) | Vault (focus) | After 7-day streak | "Sleep better, focus better. Try Vault" |
| Vault (focus) | Streakr (habits) | After 14-day streak | "Build focus into a daily habit" |
| Streakr (habits) | All apps | After 30-day streak | "You're on a roll. More from PRINTMAXX" |
| Steplock (walking) | Dusk (sleep) | After 50K steps | "Walking improves sleep. Track yours" |
| Mise (meals) | Steplock | After meal plan created | "Eat clean, stay active" |

### Implementation
- Settings > "More Apps" section (standard placement)
- Post-achievement card (after milestone)
- In notification (once per app, not spammy)
- Expected lift: 30% increase in user acquisition across portfolio (industry benchmark)

---

## 9. Kill/Double-Down Decision Framework

### After 90 days, evaluate each app:

**KILL if ALL of these are true:**
- < 500 total downloads
- < 1% download-to-trial
- < 10% trial-to-paid
- Rating < 3.0
- No organic growth despite marketing effort

**DOUBLE DOWN if ANY of these are true:**
- Download-to-trial > 8% (above median)
- Trial-to-paid > 40%
- Organic downloads growing week-over-week
- Users requesting features (engagement signal)
- App Store featuring or editorial mention

**How to double down:**
1. Paid ads: Facebook/Instagram/TikTok (only if CPI < LTV)
2. Native version if currently PWA-only
3. Add top-requested features from reviews
4. Hire niche micro-influencers ($50-500/post)
5. Create premium tier at higher price
6. Expand to Google Play if iOS-only
7. Localize into 2-3 additional languages
8. Build regional variants

---

## 10. Existing Files Cross-Reference

| Need | File | Lines |
|------|------|-------|
| 24-app deep audit (color, typography, UI, reviews) | `TOP_APP_AUDIT.md` | 1,600+ |
| UI/UX patterns, paywall psychology, design trends | `APP_UIUX_RESEARCH.md` | 360+ |
| Screen-by-screen onboarding flows for all 7 apps | `ONBOARDING_PLAYBOOK.md` | - |
| How top apps got their first 10K users | `COMPETITOR_GTM_TACTICS.md` | 290+ |
| Budget-specific GTM ($0/$100/$500/$1K) | `GTM_BY_BUDGET.md` | - |
| 11-phase assembly line process | `PRINTMAXX_APP_PLAYBOOK.md` | - |
| Shared colors, typography, design tokens | `AGGREGATE_DESIGN_SYSTEM.md` | - |
| 15 scored arbitrage opportunities | `APP_ARBITRAGE_MATRIX.md` | 450+ |
| Clone/rebrand/regional arbitrage strategy | `APP_CLONE_REBRAND_STRATEGY.md` | 560+ |
| CloneChart data extraction | `CLONECHART_DATA_EXTRACT.md` | 280+ |
| App Store top charts + category analysis | `APP_STORE_AUDIT_FEB2026.md` | 700+ |
| Portfolio GTM master plan | `APP_FACTORY_GTM_MASTER.md` | 450+ |
| App naming rules | `APP_NAMING_AUDIT.md` | 794 |
| iOS rejection prevention | `IOS_REJECTION_PREVENTION.md` | - |
| Quality standards | `APP_QUALITY_STANDARDS.md` | - |
| Asset generation (icons, screenshots) | `APP_ASSET_GENERATION_PROMPTS.md` | - |
| Clone tracker (CSV) | `LEDGER/APP_CLONE_OPPORTUNITIES.csv` | - |
| Revenue intake | `scripts/revenue_intake.py` | - |
| Experiment runner | `scripts/experiment_runner.py` | - |
| Account tracker | `scripts/account_tracker.py` | - |
| Self-test validation | `scripts/self_test.py` | - |

---

## Sources

### Revenue Intelligence Platforms
- [CloneChart.io](https://clonechart.io/) - 12,000+ iOS apps with clone prompts and revenue estimates
- [Appkittie](https://waitlist.appkittie.com) - App revenue, downloads, winning ads, viral videos (early access)
- [AppMagic](https://appmagic.rocks/) - Revenue and download estimates, RpD metric
- [AppTweak](https://www.apptweak.com/) - ASO intelligence, keyword research, download/revenue estimates
- [Appfigures](https://appfigures.com/) - Developer-focused analytics, $9.99/mo
- [data.ai](https://www.data.ai/) - Category rankings by country
- [Sensor Tower](https://sensortower.com/) - Top charts, ad intelligence

### Benchmark Reports
- [RevenueCat State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025/)
- [Business of Apps - App Revenue Data 2026](https://www.businessofapps.com/data/app-revenues/)
- [Business of Apps - App Subscription Trial Benchmarks](https://www.businessofapps.com/data/app-subscription-trial-benchmarks/)

### Case Studies
- [30-app portfolio to $22K/mo (Indie Hackers)](https://www.indiehackers.com/post/tech/from-failed-app-to-30-app-portfolio-making-22k-mo-in-less-than-a-year-myy3U7K9evxGOVOHti8s)
- [App portfolio to $60K/mo after Apple freeze (Indie Hackers)](https://www.indiehackers.com/post/tech/building-an-app-portfolio-to-60k-mo-after-apple-froze-his-developer-account-LD7oNYzKSmWucRfKV1AO)
- [Mobile apps to $185K/mo (Indie Hackers)](https://www.indiehackers.com/post/tech/growing-a-portfolio-of-mobile-apps-to-185k-mo-hZ4hqICtByIljkiJECQv)
- [How Opal Built $10M ARR (Speedinvest)](https://www.speedinvest.com/knowledge/scaling-smart-how-opal-built-a-10m-arr-business-in-just-2-years)
- [Cal AI $2M/month (Medium)](https://medium.com/@sarah_70608/how-two-teenagers-built-a-2-million-month-ai-app-8e48de43583f)
- [Indie Dev Revenue Metrics (dabo.dev)](https://dabo.dev/revealing-my-revenue-metrics)
- [Roman Koch 2025 Indie Dev Recap](https://medium.com/@romankoch/my-2025-recap-as-an-indie-developer-6846593eaad6)
- [Top 15 Most Profitable Indie Apps (Market Clarity)](https://mktclarity.com/blogs/news/indie-apps-top)

### Growth & Marketing
- [Indie App Marketing Strategies 2026 (Rapid App Store)](https://rapidappstore.com/blog/indie-app-marketing-strategies)
- [Product Hunt Launch Guide (Demand Curve)](https://www.demandcurve.com/playbooks/product-hunt-launch)
- [App Launch Strategy 2026 (Moburst)](https://www.moburst.com/blog/app-launch-strategy/)
- [ASO Best Practices 2026 (AppTweak)](https://www.apptweak.com/en/aso-blog/app-store-optimization-aso-best-practices)
- [Best ASO Tools for Indie Developers 2026 (NeoAds)](https://neoads.tech/blog/the-best-aso-tools-for-indie-developers/)
- [Free App Competitor Analysis Tools 2026 (FamilyPro)](https://familypro.io/en/blog/free-mobile-app-competitor-analysis-tools-2026)

### Design & UX
- [App Design Library (ScreensDesign)](https://screensdesign.com/)
- [Mobile App Design Trends 2026 (UXPilot)](https://uxpilot.ai/blogs/mobile-app-design-trends)
- [Paywall Optimization Strategies (AppAgent)](https://appagent.com/blog/mobile-app-onboarding-5-paywall-optimization-strategies/)
- [High-Converting Paywalls (Apphud)](https://apphud.com/blog/design-high-converting-subscription-app-paywalls)
- [Paywall Types (Adapty)](https://adapty.io/blog/the-10-types-of-mobile-app-paywalls/)
