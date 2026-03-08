# PRINTMAXX Site Test Report — 2026-03-07 18:49

## CORRECTED Summary (post-investigation)

> 3 of 4 "RED" sites were **transient CDN 504s** from the test burst, not real failures.
> All 3 confirmed GREEN on immediate retest. 1 true permanent failure (DNS).
> `hilal-ramadan.surge.sh` confirmed working PWA (142-char body, 92KB HTML).

| Metric | Initial | Corrected |
|--------|---------|-----------|
| Total sites | 161 | 161 |
| GREEN (passing) | 146 | **150** |
| YELLOW (warnings) | 11 | **10** |
| RED (broken) | 4 | **1** |
| Pass rate | 90.7% | **93.2%** |
| Avg load time | 1893ms | 1893ms |

### Only True Issue
- **Plumber Miami ZIP2** (`local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh`) — **PERMANENT DNS FAILURE**
  - Subdomain is 65 chars; DNS label max is 63. This URL will never resolve.
  - Fix: deploy same content to a shorter domain.

### False Positives Cleared
| Site | Initial | Retested | Root Cause |
|------|---------|----------|------------|
| walktounlock-web.surge.sh | RED 504 | GREEN 200 774ms | Transient CDN spike during burst |
| pentecostal-streak.surge.sh | RED 504 | GREEN 200 774ms | Transient CDN spike during burst |
| methodist-streak.surge.sh | RED 504 | GREEN 200 767ms | Transient CDN spike during burst |
| hilal-ramadan.surge.sh | YELLOW blank | GREEN (PWA) | JS-rendered content, needs networkidle wait |

---

## Original Summary (raw test output)

| Metric | Value |
|--------|-------|
| Total sites | 161 |
| GREEN (passing) | 146 |
| YELLOW (warnings) | 11 |
| RED (broken) | 4 |
| Pass rate | 90.7% |
| Avg load time | 1893ms |

## RED — Broken Sites (Fix Immediately)

### WalkToUnlock Web
- **URL:** https://walktounlock-web.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Plumber Miami ZIP2
- **URL:** https://local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge

### Pentecostal Streak
- **URL:** https://pentecostal-streak.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Methodist Streak
- **URL:** https://methodist-streak.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

## YELLOW — Sites with Warnings

### Hilal App
- **URL:** https://hilal-app.surge.sh
- **HTTP:** 200 | Load: 5848ms
- **Warnings:** slow: 5848ms

### PrayerLock Web
- **URL:** https://prayerlock-web.surge.sh
- **HTTP:** 200 | Load: 5737ms
- **Warnings:** slow: 5737ms

### SleepMaxx Web
- **URL:** https://sleepmaxx-web.surge.sh
- **HTTP:** 200 | Load: 6296ms
- **Warnings:** slow: 6296ms

### MealMaxx Web
- **URL:** https://mealmaxx-web.surge.sh
- **HTTP:** 200 | Load: 5840ms
- **Warnings:** slow: 5840ms

### Hilal Ramadan
- **URL:** https://hilal-ramadan.surge.sh
- **HTTP:** 200 | Load: 2004ms
- **Warnings:** 200 OK but page blank/empty

### PrintMaxx Apps Hub
- **URL:** https://printmaxx-apps.surge.sh
- **HTTP:** 200 | Load: 5040ms
- **Warnings:** slow: 5040ms

### Restaurant Site Demo
- **URL:** https://restaurant-site-demo.surge.sh
- **HTTP:** 200 | Load: 1880ms
- **Warnings:** 1 console error(s)

### Sunni Streak
- **URL:** https://sunni-streak.surge.sh
- **HTTP:** 200 | Load: 5268ms
- **Warnings:** slow: 5268ms

### Anglican Streak
- **URL:** https://anglican-streak.surge.sh
- **HTTP:** 200 | Load: 5485ms
- **Warnings:** slow: 5485ms

### Baptist Streak
- **URL:** https://baptist-streak.surge.sh
- **HTTP:** 200 | Load: 5581ms
- **Warnings:** slow: 5581ms

### Protestant Streak
- **URL:** https://protestant-streak.surge.sh
- **HTTP:** 200 | Load: 6033ms
- **Warnings:** slow: 6033ms

## GREEN — All Passing

| Site | URL | Load ms | Title |
|------|-----|---------|-------|
| PrayerLock App | https://prayerlock-app.surge.sh | 1521 | PrayerLock - Your Phone Locks Itself at  |
| FocusLock App | https://focuslock-app.surge.sh | 1510 | FocusLock - Block Everything. Ship Somet |
| MealMaxx App | https://mealmaxx-app.surge.sh | 1464 | MealMaxx - Meal Prep in 10 Minutes. Groc |
| ColdMaxx App | https://coldmaxx-app.surge.sh | 1510 | ColdMaxx - Cold Emails That Get Replies. |
| SleepMaxx App | https://sleepmaxx-app.surge.sh | 767 | SleepMaxx - Your Sleep Sucks. This Fixes |
| WalkToUnlock App | https://walktounlock-app.surge.sh | 1458 | WalkToUnlock - Your Alarm Doesn't Stop U |
| HabitForge App | https://habitforge-app.surge.sh | 2197 | Streakr - Build Unbreakable Habits |
| Art Streak App | https://art-streak-app.surge.sh | 4338 | Art Streak — daily creativity habit trac |
| Coding Streak App | https://coding-streak-app.surge.sh | 930 | Coding Streak — daily tech habit tracker |
| Fitness Streak App | https://fitness-streak-app.surge.sh | 986 | Fitness Streak — daily fitness habit tra |
| Journal Streak App | https://journal-streak-app.surge.sh | 959 | Journal Streak — daily wellness habit tr |
| Language Streak App | https://language-streak-app.surge.sh | 993 | Language Streak — daily learning habit t |
| Meditation Streak App | https://meditation-streak-app.surge.sh | 977 | Meditation Streak — daily wellness habit |
| Reading Streak App | https://reading-streak-app.surge.sh | 1029 | Reading Streak — daily learning habit tr |
| Sutra Streak App | https://sutra-streak-app.surge.sh | 909 | Sutra Streak — daily faith habit tracker |
| Gita Streak App | https://gita-streak-app.surge.sh | 912 | Gita Streak — daily faith habit tracker |
| Scripture Streak LDS | https://scripture-streak-lds.surge.sh | 994 | Scripture Streak — daily faith habit tra |
| Quran Streak App | https://quran-streak-app.surge.sh | 994 | Quran Streak — daily faith habit tracker |
| Guru Streak App | https://guru-streak-app.surge.sh | 987 | Guru Streak — daily faith habit tracker |
| Torah Streak App | https://torah-streak-app.surge.sh | 1010 | Torah Streak — daily faith habit tracker |
| Mormon Streak App | https://mormon-streak-app.surge.sh | 1148 | Scripture Streak — daily faith habit tra |
| Sikh Streak App | https://sikh-streak-app.surge.sh | 901 | Guru Streak — daily faith habit tracker |
| Art Streak Landing | https://art-streak.surge.sh | 1044 | Art Streak — daily creativity habit trac |
| Coding Streak Landing | https://coding-streak.surge.sh | 1038 | Coding Streak — daily tech habit tracker |
| Fitness Streak Landing | https://fitness-streak.surge.sh | 1004 | Fitness Streak — daily fitness habit tra |
| Journal Streak Landing | https://journal-streak.surge.sh | 1123 | Journal Streak — daily wellness habit tr |
| Language Streak Landing | https://language-streak.surge.sh | 1112 | Language Streak — daily learning habit t |
| Meditation Streak Landing | https://meditation-streak.surge.sh | 955 | Meditation Streak — daily wellness habit |
| Reading Streak Landing | https://reading-streak.surge.sh | 966 | Reading Streak — daily learning habit tr |
| Quran Streak Landing | https://quran-streak.surge.sh | 1007 | Quran Streak — daily faith habit tracker |
| Gita Streak Landing | https://gita-streak.surge.sh | 971 | Gita Streak — daily faith habit tracker |
| Torah Streak Landing | https://torah-streak.surge.sh | 1043 | Torah Streak — daily faith habit tracker |
| Sikh Streak Landing | https://sikh-streak.surge.sh | 1004 | Guru Streak — daily faith habit tracker |
| Mormon Streak Landing | https://mormon-streak.surge.sh | 1061 | Scripture Streak — daily faith habit tra |
| Buddhist Streak Landing | https://buddhist-streak.surge.sh | 965 | Sutra Streak — daily faith habit tracker |
| FocusLock Web | https://focuslock-web.surge.sh | 4918 | FocusLock - Block Everything. Ship Somet |
| HabitForge Web | https://habitforge-web.surge.sh | 2220 | Streakr - Build Unbreakable Habits |
| ColdMaxx | https://coldmaxx.surge.sh | 4498 | ColdMaxx - Cold Emails That Get Replies. |
| FocusLock | https://focuslock.surge.sh | 2266 | 25:00 - Vault |
| Ramadan Tracker | https://ramadan-tracker.surge.sh | 921 | Hilal - Crowdsourced Moon Sighting For Y |
| PrayerLock | https://prayerlock.surge.sh | 2280 | PrayerLock - Build Your Prayer Habit |
| WalkToUnlock | https://walktounlock.surge.sh | 2275 | Steplock |
| SleepMaxx | https://sleepmaxx.surge.sh | 1767 | Dusk |
| MealMaxx | https://mealmaxx.surge.sh | 2197 | Mise |
| PrintMaxx Content Calendar | https://printmaxx-content-calendar.surge.sh | 922 | Content Calendar - Free Social Media Pla |
| PrintMaxx Website Audit | https://printmaxx-website-audit.surge.sh | 927 | Website Audit Tool - Free SEO and Perfor |
| PrintMaxx Invoice Tracker | https://printmaxx-invoice-tracker.surge.sh | 1003 | Invoice Tracker - Free Freelance Invoice |
| PrintMaxx Compare | https://printmaxx-compare.surge.sh | 1002 | App Comparisons - Honest Reviews and Alt |
| PrintMaxx Store | https://printmaxx-store.surge.sh | 989 | PRINTMAXX - Digital Products That Print |
| AI Stack 2026 | https://ai-stack-2026.surge.sh | 4554 | Best AI Tools for Solo Founders 2026 - T |
| Reliable Fence Nashville | https://reliable-fence-nashville.surge.sh | 1622 | Reliable Fence Company | Nashville's Tru |
| Accurate Auto Nashville | https://accurate-auto-nashville.surge.sh | 1599 | Accurate Automotive Repair | Honda & Acu |
| PrintMaxx Services | https://printmaxx-services.surge.sh | 1040 | PRINTMAXX Services | Web Dev, Automation |
| PrintMaxx Portfolio | https://printmaxx-portfolio.surge.sh | 1907 | PRINTMAXX - Websites That Rank on Google |
| PrintMaxx Dashboard | https://printmaxx-dashboard.surge.sh | 1910 | PRINTMAXX Command Center |
| InvoiceForge | https://invoiceforge.surge.sh | 2045 | InvoiceForge - Professional Invoice Gene |
| ROI Calc | https://roicalc.surge.sh | 914 | ROI Calculator — See Your Website Redesi |
| StackMaxx | https://stackmaxx.surge.sh | 972 | StackMaxx — Solopreneur Tech Stack Build |
| PageScorer | https://pagescorer.surge.sh | 955 | PageScorer — Landing Page Audit in 30 Se |
| ProspectMaxx | https://prospectmaxx.surge.sh | 983 | ProspectMaxx — Local Business Lead Finde |
| PitchDeck | https://pitchdeck.surge.sh | 1833 | PitchDeck - Micro Pitch Deck Builder |
| MCP Hub | https://mcphub.surge.sh | 1510 | MCPHub - find the MCP server you need in |
| Website Audit Tool | https://website-audit-tool.surge.sh | 936 | Website Audit Tool |
| Invoice Tracker | https://invoicetracker.surge.sh | 946 | Invoice Tracker |
| Content Calendar | https://contentcalendar.surge.sh | 934 | Content Calendar |
| SiteScore Analyzer | https://sitescore-analyzer.surge.sh | 792 | SiteScore Pro - Local SEO Competitor Ana |
| SiteScore App | https://sitescore-app.surge.sh | 1456 | SiteScore - Free Website Performance Ana |
| Fiverr Services PM | https://fiverr-services-pm.surge.sh | 921 | PRINTMAXX Services | Web Dev, Automation |
| SiteScore Pro | https://sitescore-pro.surge.sh | 909 | SiteScore Pro - Local SEO Competitor Ana |
| SiteScore Free | https://sitescore-free.surge.sh | 1794 | SiteScore - Free Website Performance Ana |
| PrintMaxx Flowstack | https://printmaxx-flowstack.surge.sh | 1179 | Flowstack - Project Management That Actu |
| PrintMaxx Digital Services | https://printmaxx-digital-services.surge.sh | 948 | PRINTMAXX - Professional Digital Service |
| ShopMetrics Pro | https://shopmetrics-pro.surge.sh | 1048 | ShopMetrics - Analytics Dashboard |
| PrintMaxx SEO | https://printmaxx-seo.surge.sh | 825 | PRINTMAXX - Professional Digital Service |
| PrintMaxx Analyzer | https://printmaxx-analyzer.surge.sh | 1757 | Website Analyzer | PRINTMAXX |
| PrintMaxx Command | https://printmaxx-command.surge.sh | 1778 | PRINTMAXX Command Center |
| Social Dashboard PM | https://social-dashboard-pm.surge.sh | 996 | PRINTMAXX Social Media Dashboard |
| Cold Email Calc | https://cold-email-calc.surge.sh | 960 | Cold Email ROI Calculator — how much is  |
| Plumber Houston MeetAPlumber | https://find-plumbers-in-houston-texas-meetaplumber-com-houston-tx.surge.sh | 998 | Find Plumbers in Houston, Texas - MeetAP |
| Plumber Houston ZIP | https://plumbers-just-enter-your-zip-code-houston-tx.surge.sh | 972 | Plumbers - Just Enter Your Zip Code | Ho |
| Plumber Houston Local | https://local-plumbing-experts-replace-plumbing-houston-tx.surge.sh | 933 | Local Plumbing Experts - Replace Plumbin |
| Plumber Miami ZIP | https://plumbers-just-enter-your-zip-code-miami-fl.surge.sh | 1043 | Plumbers - Just Enter Your Zip Code | Mi |
| Plumber Miami Local | https://local-plumbing-miami-fl.surge.sh | 1117 | Local Plumbing Experts - Plumbers - Just |
| Dentist Austin | https://best-dentist-office-austin-your-neighborhood-dentist-austin-tx.surge.sh | 1124 | Best Dentist Office Austin - Your Neighb |
| Handyman Jacksonville | https://handyman-matters-jacksonville-jacksonville-fl.surge.sh | 959 | Handyman Matters Jacksonville | Jacksonv |
| Emergency Plumber Jacksonville | https://jacksonville-emergency-plumber-jacksonville-fl.surge.sh | 1068 | Jacksonville Emergency Plumber | Jackson |
| Plumbing HVAC Memphis | https://professional-plumbing-heating-cooling-memphis-tn.surge.sh | 1083 | Professional Plumbing Heating Cooling |  |
| Locksmith Tampa | https://south-tampa-locksmith-tampa-fl.surge.sh | 1025 | South Tampa Locksmith | Tampa FL |
| Miami Plumbing ZIP | https://miami-plumbing-zip.surge.sh | 911 | Local Plumbing Experts - Plumbers - Just |
| PrintMaxx Local Demos | https://printmaxx-local-demos.surge.sh | 4755 | PRINTMAXX Local Business Website Demos | |
| Restaurant Motion | https://restaurant-motion.surge.sh | 1598 | Ember & Oak | Farm-to-Table Restaurant |
| Realtor Motion | https://realtor-motion.surge.sh | 1326 | Sarah Mitchell | Top Real Estate Agent i |
| Dental Motion | https://dental-motion.surge.sh | 806 | Bright Smile Dental | Modern Family Dent |
| Realtor Demo | https://realtor-demo.surge.sh | 1754 | {{BUSINESS_NAME}} — {{CITY}} Real Estate |
| Plumber Demo | https://plumber-demo.surge.sh | 2044 | {{BUSINESS_NAME}} — Licensed Plumbing &  |
| Legal Demo | https://legal-demo.surge.sh | 1723 | {{BUSINESS_NAME}} — {{PRACTICE_AREA:Pers |
| Fitness Demo | https://fitness-demo.surge.sh | 1813 | {{BUSINESS_NAME}} — Gym & Personal Train |
| Dental Demo | https://dental-demo.surge.sh | 1982 | {{BUSINESS_NAME}} — Family & Cosmetic De |
| FlowStack Demo | https://flowstack-demo.surge.sh | 990 | Flowstack - Project Management That Actu |
| ShopMetrics Dashboard | https://shopmetrics-dashboard.surge.sh | 943 | ShopMetrics - Analytics Dashboard |
| PrintMaxx Demos | https://printmaxx-demos.surge.sh | 1025 | PrintMaxx Demos |
| Mike's HVAC Demo | https://mikes-hvac-demo.surge.sh | 2237 | Mike's HVAC | Heating & Cooling Speciali |
| Elite Fitness Demo | https://elite-fitness-demo.surge.sh | 2243 | Elite Fitness Center | Transform Your Li |
| Smith Dentistry Demo | https://smith-dentistry-demo.surge.sh | 2250 | Smith Family Dentistry | Creating Beauti |
| Perfect Lawn Demo | https://perfect-lawn-demo.surge.sh | 2229 | Perfect Lawn Landscaping | Creating Outd |
| Bella's Salon Demo | https://bellas-salon-demo.surge.sh | 2108 | Bella's Salon | Where Beauty Meets Artis |
| Tony's Restaurant Demo | https://tonys-restaurant-demo.surge.sh | 1952 | Tony's Italian Restaurant | Where Every  |
| Joe's Plumbing Demo | https://joes-plumbing-demo.surge.sh | 1984 | Joe's Plumbing | Licensed & Insured Plum |
| PrintMaxx Main | https://printmaxx.surge.sh | 951 | PRINTMAXX - Apps That Fix Real Problems |
| PrintMaxx Site | https://printmaxx-site.surge.sh | 4388 | PRINTMAXX - Apps That Fix Real Problems |
| PrintMaxx Control Panel | https://printmaxx-control-panel.surge.sh | 1011 | PRINTMAXX Control Panel |
| PrintMaxx Thanks | https://printmaxx-thanks.surge.sh | 3233 | you're in. - PRINTMAXX |
| PrintMaxx Magnets | https://printmaxx-magnets.surge.sh | 985 | Cold Email ROI Calculator — how much is  |
| PrintMaxx Storefront | https://printmaxx-storefront.surge.sh | 946 | PRINTMAXX - Digital Products That Print |
| ConvertKit vs Beehiiv | https://convertkit-vs-beehiiv.surge.sh | 3000 | ConvertKit vs Beehiiv 2026: Which Email  |
| PrayerLock vs Hallow | https://prayerlock-vs-hallow.surge.sh | 1181 | App Comparisons - Honest Reviews and Alt |
| FocusLock vs Opal | https://focuslock-vs-opal.surge.sh | 1594 | App Comparisons - Honest Reviews and Alt |
| PrintMaxx Comparisons | https://printmaxx-comparisons.surge.sh | 1180 | App Comparisons - Honest Reviews and Alt |
| Website Analyzer PM | https://website-analyzer-pm.surge.sh | 2164 | Website Analyzer | PRINTMAXX |
| ADHD Streak Landing | https://adhd-streak.surge.sh | 4731 | ADHD-Streak - Build Focus Habits That Ac |
| Solopreneur Checklist | https://solopreneur-launch-checklist.surge.sh | 969 | Ship Your First App in 7 Days - Interact |
| Ramadan Daily Planner | https://ramadan-daily-planner.surge.sh | 1031 | Ramadan Daily Planner — build your sched |
| Hilal Ramadan App | https://hilal.surge.sh | 1384 | Hilal - Ramadan 2026 Moon Sighting App | |
| Fitness Streak Landing2 | https://fitness-streak-landing.surge.sh | 999 | Fitness Streak — daily fitness habit tra |
| Coding Streak Landing2 | https://coding-streak-landing.surge.sh | 951 | Coding Streak — daily tech habit tracker |
| Buddhist Streak Landing2 | https://buddhist-streak-landing.surge.sh | 928 | Sutra Streak — daily faith habit tracker |
| Art Streak Landing2 | https://art-streak-landing.surge.sh | 980 | Art Streak — daily creativity habit trac |
| Shia Streak | https://shia-streak.surge.sh | 4281 | Shia Streak - Daily Shia Islamic Prayer  |
| Presbyterian Streak | https://presbyterian-streak.surge.sh | 3235 | Presbyterian Streak - Daily Presbyterian |
| Evangelical Streak | https://evangelical-streak.surge.sh | 3188 | Evangelical Streak - Daily Evangelical B |
| Episcopal Streak | https://episcopal-streak.surge.sh | 3516 | Episcopal Streak - Daily Episcopal Praye |
| Lutheran Streak | https://lutheran-streak.surge.sh | 3049 | Lutheran Streak - Daily Lutheran Devotio |
| Orthodox Streak | https://orthodox-streak.surge.sh | 4777 | Orthodox Streak - Daily Orthodox Christi |
| Catholic Streak | https://catholic-streak.surge.sh | 4962 | Catholic Streak - Build Your Daily Catho |
| Magnolia Cafe Austin | https://magnolia-cafe-austin.surge.sh | 2343 | Magnolia Cafe | Austin TX |
| Kelly Personal Training | https://kelly-personal-training-austin.surge.sh | 992 | Kelly Personal Training | Austin TX |
| Galaxia Dental Austin | https://galaxia-dental-austin.surge.sh | 944 | Galaxia Dental Austin | Austin TX |
| Barton Springs Saloon | https://barton-springs-saloon-austin.surge.sh | 922 | Barton Springs Saloon | Austin TX |
| Zax Pints Plates Austin | https://zax-pints-plates-austin.surge.sh | 984 | Zax Pints and Plates | Austin TX |
| Artz Rib House Austin | https://artz-rib-house-austin.surge.sh | 891 | Artz Rib House | Austin TX |
| Memphis Plumbing Preview | https://memphis-plumbing-preview.surge.sh | 951 | Professional Plumbing Heating Cooling |  |
| JAX Emergency Plumber | https://jax-emergency-plumber-preview.surge.sh | 966 | Jacksonville Emergency Plumber | Jackson |
| S Tampa Locksmith Preview | https://south-tampa-locksmith-preview.surge.sh | 1019 | South Tampa Locksmith | Tampa FL |
| Atlanta Roofing Preview | https://atlanta-roofing-company-preview.surge.sh | 1032 | Atlanta Roofing Company - Roofing Contra |
| JSS Janitorial Memphis | https://jss-janitorial-memphis.surge.sh | 1306 | JSS Janitorial Services & Supplies | Mem |
| Shop of Memphis Preview | https://shop-of-memphis-preview.surge.sh | 985 | The Shop of Memphis | ASE-Certified Auto |

## Full Results

| # | Site | Category | Grade | HTTP | Load ms | Notes |
|---|------|----------|-------|------|---------|-------|
| 1 | PrayerLock App | core_apps | GREEN | 200 | 1521 |  |
| 2 | FocusLock App | core_apps | GREEN | 200 | 1510 |  |
| 3 | Hilal App | core_apps | YELLOW | 200 | 5848 | slow: 5848ms |
| 4 | MealMaxx App | core_apps | GREEN | 200 | 1464 |  |
| 5 | ColdMaxx App | core_apps | GREEN | 200 | 1510 |  |
| 6 | SleepMaxx App | core_apps | GREEN | 200 | 767 |  |
| 7 | WalkToUnlock App | core_apps | GREEN | 200 | 1458 |  |
| 8 | HabitForge App | core_apps | GREEN | 200 | 2197 |  |
| 9 | Art Streak App | streak_apps | GREEN | 200 | 4338 |  |
| 10 | Coding Streak App | streak_apps | GREEN | 200 | 930 |  |
| 11 | Fitness Streak App | streak_apps | GREEN | 200 | 986 |  |
| 12 | Journal Streak App | streak_apps | GREEN | 200 | 959 |  |
| 13 | Language Streak App | streak_apps | GREEN | 200 | 993 |  |
| 14 | Meditation Streak App | streak_apps | GREEN | 200 | 977 |  |
| 15 | Reading Streak App | streak_apps | GREEN | 200 | 1029 |  |
| 16 | Sutra Streak App | streak_apps | GREEN | 200 | 909 |  |
| 17 | Gita Streak App | streak_apps | GREEN | 200 | 912 |  |
| 18 | Scripture Streak LDS | streak_apps | GREEN | 200 | 994 |  |
| 19 | Quran Streak App | streak_apps | GREEN | 200 | 994 |  |
| 20 | Guru Streak App | streak_apps | GREEN | 200 | 987 |  |
| 21 | Torah Streak App | streak_apps | GREEN | 200 | 1010 |  |
| 22 | Mormon Streak App | streak_apps | GREEN | 200 | 1148 |  |
| 23 | Sikh Streak App | streak_apps | GREEN | 200 | 901 |  |
| 24 | Art Streak Landing | streak_landing | GREEN | 200 | 1044 |  |
| 25 | Coding Streak Landing | streak_landing | GREEN | 200 | 1038 |  |
| 26 | Fitness Streak Landing | streak_landing | GREEN | 200 | 1004 |  |
| 27 | Journal Streak Landing | streak_landing | GREEN | 200 | 1123 |  |
| 28 | Language Streak Landing | streak_landing | GREEN | 200 | 1112 |  |
| 29 | Meditation Streak Landing | streak_landing | GREEN | 200 | 955 |  |
| 30 | Reading Streak Landing | streak_landing | GREEN | 200 | 966 |  |
| 31 | Quran Streak Landing | streak_landing | GREEN | 200 | 1007 |  |
| 32 | Gita Streak Landing | streak_landing | GREEN | 200 | 971 |  |
| 33 | Torah Streak Landing | streak_landing | GREEN | 200 | 1043 |  |
| 34 | Sikh Streak Landing | streak_landing | GREEN | 200 | 1004 |  |
| 35 | Mormon Streak Landing | streak_landing | GREEN | 200 | 1061 |  |
| 36 | Buddhist Streak Landing | streak_landing | GREEN | 200 | 965 |  |
| 37 | PrayerLock Web | web_marketing | YELLOW | 200 | 5737 | slow: 5737ms |
| 38 | FocusLock Web | web_marketing | GREEN | 200 | 4918 |  |
| 39 | WalkToUnlock Web | web_marketing | RED | 504 | 6010 | HTTP 504 |
| 40 | SleepMaxx Web | web_marketing | YELLOW | 200 | 6296 | slow: 6296ms |
| 41 | MealMaxx Web | web_marketing | YELLOW | 200 | 5840 | slow: 5840ms |
| 42 | HabitForge Web | web_marketing | GREEN | 200 | 2220 |  |
| 43 | ColdMaxx | web_marketing | GREEN | 200 | 4498 |  |
| 44 | FocusLock | web_marketing | GREEN | 200 | 2266 |  |
| 45 | Ramadan Tracker | web_marketing | GREEN | 200 | 921 |  |
| 46 | PrayerLock | web_marketing | GREEN | 200 | 2280 |  |
| 47 | WalkToUnlock | web_marketing | GREEN | 200 | 2275 |  |
| 48 | SleepMaxx | web_marketing | GREEN | 200 | 1767 |  |
| 49 | MealMaxx | web_marketing | GREEN | 200 | 2197 |  |
| 50 | Hilal Ramadan | web_marketing | YELLOW | 200 | 2004 | 200 OK but page blank/empty |
| 51 | PrintMaxx Content Calendar | new_tools | GREEN | 200 | 922 |  |
| 52 | PrintMaxx Website Audit | new_tools | GREEN | 200 | 927 |  |
| 53 | PrintMaxx Invoice Tracker | new_tools | GREEN | 200 | 1003 |  |
| 54 | PrintMaxx Compare | new_tools | GREEN | 200 | 1002 |  |
| 55 | PrintMaxx Store | new_tools | GREEN | 200 | 989 |  |
| 56 | AI Stack 2026 | new_tools | GREEN | 200 | 4554 |  |
| 57 | Reliable Fence Nashville | new_tools | GREEN | 200 | 1622 |  |
| 58 | Accurate Auto Nashville | new_tools | GREEN | 200 | 1599 |  |
| 59 | PrintMaxx Apps Hub | hubs | YELLOW | 200 | 5040 | slow: 5040ms |
| 60 | PrintMaxx Services | hubs | GREEN | 200 | 1040 |  |
| 61 | PrintMaxx Portfolio | hubs | GREEN | 200 | 1907 |  |
| 62 | PrintMaxx Dashboard | hubs | GREEN | 200 | 1910 |  |
| 63 | InvoiceForge | tools_saas | GREEN | 200 | 2045 |  |
| 64 | ROI Calc | tools_saas | GREEN | 200 | 914 |  |
| 65 | StackMaxx | tools_saas | GREEN | 200 | 972 |  |
| 66 | PageScorer | tools_saas | GREEN | 200 | 955 |  |
| 67 | ProspectMaxx | tools_saas | GREEN | 200 | 983 |  |
| 68 | PitchDeck | tools_saas | GREEN | 200 | 1833 |  |
| 69 | MCP Hub | tools_saas | GREEN | 200 | 1510 |  |
| 70 | Website Audit Tool | tools_saas | GREEN | 200 | 936 |  |
| 71 | Invoice Tracker | tools_saas | GREEN | 200 | 946 |  |
| 72 | Content Calendar | tools_saas | GREEN | 200 | 934 |  |
| 73 | SiteScore Analyzer | tools_saas | GREEN | 200 | 792 |  |
| 74 | SiteScore App | tools_saas | GREEN | 200 | 1456 |  |
| 75 | Fiverr Services PM | tools_saas | GREEN | 200 | 921 |  |
| 76 | SiteScore Pro | tools_saas | GREEN | 200 | 909 |  |
| 77 | SiteScore Free | tools_saas | GREEN | 200 | 1794 |  |
| 78 | PrintMaxx Flowstack | tools_saas | GREEN | 200 | 1179 |  |
| 79 | PrintMaxx Digital Services | tools_saas | GREEN | 200 | 948 |  |
| 80 | ShopMetrics Pro | tools_saas | GREEN | 200 | 1048 |  |
| 81 | PrintMaxx SEO | tools_saas | GREEN | 200 | 825 |  |
| 82 | PrintMaxx Analyzer | tools_saas | GREEN | 200 | 1757 |  |
| 83 | PrintMaxx Command | tools_saas | GREEN | 200 | 1778 |  |
| 84 | Social Dashboard PM | tools_saas | GREEN | 200 | 996 |  |
| 85 | Cold Email Calc | tools_saas | GREEN | 200 | 960 |  |
| 86 | Plumber Houston MeetAPlumber | local_biz | GREEN | 200 | 998 |  |
| 87 | Plumber Houston ZIP | local_biz | GREEN | 200 | 972 |  |
| 88 | Plumber Houston Local | local_biz | GREEN | 200 | 933 |  |
| 89 | Plumber Miami ZIP | local_biz | GREEN | 200 | 1043 |  |
| 90 | Plumber Miami Local | local_biz | GREEN | 200 | 1117 |  |
| 91 | Plumber Miami ZIP2 | local_biz | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://local-plumbing-expert |
| 92 | Dentist Austin | local_biz | GREEN | 200 | 1124 |  |
| 93 | Handyman Jacksonville | local_biz | GREEN | 200 | 959 |  |
| 94 | Emergency Plumber Jacksonville | local_biz | GREEN | 200 | 1068 |  |
| 95 | Plumbing HVAC Memphis | local_biz | GREEN | 200 | 1083 |  |
| 96 | Locksmith Tampa | local_biz | GREEN | 200 | 1025 |  |
| 97 | Miami Plumbing ZIP | local_biz | GREEN | 200 | 911 |  |
| 98 | PrintMaxx Local Demos | local_biz | GREEN | 200 | 4755 |  |
| 99 | Restaurant Motion | demos | GREEN | 200 | 1598 |  |
| 100 | Realtor Motion | demos | GREEN | 200 | 1326 |  |
| 101 | Dental Motion | demos | GREEN | 200 | 806 |  |
| 102 | Restaurant Site Demo | demos | YELLOW | 200 | 1880 | 1 console error(s) |
| 103 | Realtor Demo | demos | GREEN | 200 | 1754 |  |
| 104 | Plumber Demo | demos | GREEN | 200 | 2044 |  |
| 105 | Legal Demo | demos | GREEN | 200 | 1723 |  |
| 106 | Fitness Demo | demos | GREEN | 200 | 1813 |  |
| 107 | Dental Demo | demos | GREEN | 200 | 1982 |  |
| 108 | FlowStack Demo | demos | GREEN | 200 | 990 |  |
| 109 | ShopMetrics Dashboard | demos | GREEN | 200 | 943 |  |
| 110 | PrintMaxx Demos | demos | GREEN | 200 | 1025 |  |
| 111 | Mike's HVAC Demo | demos | GREEN | 200 | 2237 |  |
| 112 | Elite Fitness Demo | demos | GREEN | 200 | 2243 |  |
| 113 | Smith Dentistry Demo | demos | GREEN | 200 | 2250 |  |
| 114 | Perfect Lawn Demo | demos | GREEN | 200 | 2229 |  |
| 115 | Bella's Salon Demo | demos | GREEN | 200 | 2108 |  |
| 116 | Tony's Restaurant Demo | demos | GREEN | 200 | 1952 |  |
| 117 | Joe's Plumbing Demo | demos | GREEN | 200 | 1984 |  |
| 118 | PrintMaxx Main | hubs | GREEN | 200 | 951 |  |
| 119 | PrintMaxx Site | hubs | GREEN | 200 | 4388 |  |
| 120 | PrintMaxx Control Panel | hubs | GREEN | 200 | 1011 |  |
| 121 | PrintMaxx Thanks | hubs | GREEN | 200 | 3233 |  |
| 122 | PrintMaxx Magnets | lead_magnets | GREEN | 200 | 985 |  |
| 123 | PrintMaxx Storefront | hubs | GREEN | 200 | 946 |  |
| 124 | ConvertKit vs Beehiiv | comparison_pages | GREEN | 200 | 3000 |  |
| 125 | PrayerLock vs Hallow | comparison_pages | GREEN | 200 | 1181 |  |
| 126 | FocusLock vs Opal | comparison_pages | GREEN | 200 | 1594 |  |
| 127 | PrintMaxx Comparisons | comparison_pages | GREEN | 200 | 1180 |  |
| 128 | Website Analyzer PM | tools_saas | GREEN | 200 | 2164 |  |
| 129 | ADHD Streak Landing | streak_landing | GREEN | 200 | 4731 |  |
| 130 | Solopreneur Checklist | lead_magnets | GREEN | 200 | 969 |  |
| 131 | Ramadan Daily Planner | lead_magnets | GREEN | 200 | 1031 |  |
| 132 | Hilal Ramadan App | apps | GREEN | 200 | 1384 |  |
| 133 | Fitness Streak Landing2 | streak_landing | GREEN | 200 | 999 |  |
| 134 | Coding Streak Landing2 | streak_landing | GREEN | 200 | 951 |  |
| 135 | Buddhist Streak Landing2 | streak_landing | GREEN | 200 | 928 |  |
| 136 | Art Streak Landing2 | streak_landing | GREEN | 200 | 980 |  |
| 137 | Sunni Streak | streak_landing | YELLOW | 200 | 5268 | slow: 5268ms |
| 138 | Shia Streak | streak_landing | GREEN | 200 | 4281 |  |
| 139 | Presbyterian Streak | streak_landing | GREEN | 200 | 3235 |  |
| 140 | Anglican Streak | streak_landing | YELLOW | 200 | 5485 | slow: 5485ms |
| 141 | Evangelical Streak | streak_landing | GREEN | 200 | 3188 |  |
| 142 | Pentecostal Streak | streak_landing | RED | 504 | 5970 | HTTP 504 |
| 143 | Episcopal Streak | streak_landing | GREEN | 200 | 3516 |  |
| 144 | Lutheran Streak | streak_landing | GREEN | 200 | 3049 |  |
| 145 | Methodist Streak | streak_landing | RED | 504 | 5995 | HTTP 504 |
| 146 | Baptist Streak | streak_landing | YELLOW | 200 | 5581 | slow: 5581ms |
| 147 | Protestant Streak | streak_landing | YELLOW | 200 | 6033 | slow: 6033ms |
| 148 | Orthodox Streak | streak_landing | GREEN | 200 | 4777 |  |
| 149 | Catholic Streak | streak_landing | GREEN | 200 | 4962 |  |
| 150 | Magnolia Cafe Austin | local_biz | GREEN | 200 | 2343 |  |
| 151 | Kelly Personal Training | local_biz | GREEN | 200 | 992 |  |
| 152 | Galaxia Dental Austin | local_biz | GREEN | 200 | 944 |  |
| 153 | Barton Springs Saloon | local_biz | GREEN | 200 | 922 |  |
| 154 | Zax Pints Plates Austin | local_biz | GREEN | 200 | 984 |  |
| 155 | Artz Rib House Austin | local_biz | GREEN | 200 | 891 |  |
| 156 | Memphis Plumbing Preview | local_biz | GREEN | 200 | 951 |  |
| 157 | JAX Emergency Plumber | local_biz | GREEN | 200 | 966 |  |
| 158 | S Tampa Locksmith Preview | local_biz | GREEN | 200 | 1019 |  |
| 159 | Atlanta Roofing Preview | local_biz | GREEN | 200 | 1032 |  |
| 160 | JSS Janitorial Memphis | local_biz | GREEN | 200 | 1306 |  |
| 161 | Shop of Memphis Preview | local_biz | GREEN | 200 | 985 |  |

*Generated: 2026-03-07T18:49:58.736352*
*Screenshots: AUTOMATIONS/agent/swarm/screenshots/*