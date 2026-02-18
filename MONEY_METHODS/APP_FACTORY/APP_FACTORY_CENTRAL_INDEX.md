# App Factory Central Index

**Last updated:** 2026-02-12
**Purpose:** THE single file any agent reads to understand the entire App Factory. Every app, every doc, every status, every conflict, every next action.
**Portfolio verdict:** 42.7/100 average. NOT shippable. All 6 PWAs need major rework before iOS submission.

---

## 1. Portfolio overview (7 unique apps + 2 Roblox projects + 1 legacy app)

### Active PWA Apps (6 apps -- all need rework)

| # | Brand Name | Internal Name | Category | Canonical Location | Score | Status |
|---|-----------|--------------|----------|-------------------|-------|--------|
| 1 | **Hilal** | Ramadan Tracker | Faith/Fasting | `ralph/loops/app_factory/output/ramadan-tracker/` | **52/100** | BEST app. Has onboarding, bilingual, paywall screen. Fake IAP (localStorage boolean). Missing RevenueCat, haptics, real native plugin calls. HIGH rejection risk. |
| 2 | **Steplock** | WalkToUnlock | Walking/Fitness | `ralph/loops/app_factory/output/walktounlock-web/` | **44/100** | Has pedometer concept, Capacitor scaffolding, package.json. No monetization, no onboarding quiz. HIGH rejection risk. |
| 3 | **Mise** | MealMaxx | Meal Planning | `ralph/loops/app_factory/output/mealmaxx-web/` | **42/100** | Clean UI, has onboarding. No monetization, no Capacitor native calls. VERY HIGH rejection risk. |
| 4 | **Streakr** | HabitForge | Habit Tracking | `ralph/loops/app_factory/output/habitforge-web/` | **40/100** | Emerald theme, heat map, emoji habits. 12+ hover states. No monetization. VERY HIGH rejection risk. |
| 5 | **Dusk** | SleepMaxx | Sleep/Wellness | `ralph/loops/app_factory/output/sleepmaxx-web/` | **40/100** | Good dark theme, custom CSS (not Tailwind CDN). No onboarding quiz, no monetization. VERY HIGH rejection risk. |
| 6 | **Vault** | FocusLock | Focus/Productivity | `ralph/loops/app_factory/output/focuslock-web/` | **38/100** | WORST app. 26+ hover states, only 1 native plugin, zero monetization, weakest onboarding (3 static screens). VERY HIGH rejection risk. |

### Other Builds

| # | Name | Category | Location | Status |
|---|------|----------|----------|--------|
| 7 | **PrayerLock** | Faith/Prayer | `MONEY_METHODS/APP_FACTORY/builds/prayerlock-web/` | Functional PWA (72KB). No monetization. Deployable to Vercel now but not iOS-ready. NOT in ralph output (unique to builds/). |
| 8 | **Roblox Tycoon** | Roblox Game | `MONEY_METHODS/APP_FACTORY/builds/roblox_tycoon/` | Docs + Lua src files. Separate project from iOS apps. |
| 9 | **RobloxMaxx** | Roblox Game | `MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/` | More complete Roblox project with API, game scripts, social content, competitive analysis. |
| 10 | **biomaxx** | Circadian Rhythm | `MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/` | CODE MISSING. Only marketing docs (LAUNCH_ASSETS.md, SUBMISSION_CHECKLIST.md). Source code likely lost or in separate repo. React Native + Expo claimed. |

### Proposed / Specced Apps (Not Yet Built)

| App | Spec Location | Status |
|-----|--------------|--------|
| **KarmaMaxx** (NoFap/Addiction Recovery) | `MONEY_METHODS/APP_FACTORY/NOFAP_KARMAMAXX_APP_SPEC.md` (30KB) | SPEC ONLY. Market analysis done ($250K MRR competitor QUITTR). Not built. |
| AI Hairstyle Try-On | `MONEY_METHODS/APP_FACTORY/ANDROID_CLONE_SPECS.md` | Spec for 3 Android clones (hairstyle, video gen, music gen). Not built. |
| 8 Clone Opportunities | `LEDGER/APP_CLONE_OPPORTUNITIES.csv` (8 entries) | CLONE001-008 scored 65-85. GPS tracker, workout, storage cleaner, AI hairstyle, AI video, AI music, tai chi, AI tattoo. |

### Legacy App (Superseded)

| App | Location | Status |
|-----|----------|--------|
| **Scripture Streak** | `app factory/scripture-streak/` | LEGACY. Full React Native + Expo + Supabase app. Has node_modules, iOS/Android dirs, screenshots, subscription key file. Built Jan 2026. Superseded by PrayerLock. DO NOT USE this directory for new work. |

---

## 2. Duplicate files and canonical resolution

Three apps exist in BOTH `ralph/loops/app_factory/output/` AND `MONEY_METHODS/APP_FACTORY/builds/`. The ralph versions are newer and larger.

| App | Ralph Version (CANONICAL) | Builds Version (OUTDATED) | Difference |
|-----|--------------------------|--------------------------|------------|
| FocusLock/Vault | `ralph/.../focuslock-web/index.html` (77KB) | `builds/focuslock-web/index.html` (40KB) | Ralph is 37KB larger, more complete |
| SleepMaxx/Dusk | `ralph/.../sleepmaxx-web/index.html` (57KB) | `builds/sleepmaxx-web/index.html` (41KB) | Ralph is 16KB larger, has package.json + capacitor config |
| WalkToUnlock/Steplock | `ralph/.../walktounlock-web/index.html` (51KB) | `builds/walktounlock-web/index.html` (31KB) | Ralph is 20KB larger, has package.json + capacitor config |

**Rule:** Always use `ralph/loops/app_factory/output/{app}/` as canonical. The `builds/` copies are earlier iterations.

**Unique to builds/ only:** PrayerLock (72KB, builds/prayerlock-web/), biomaxx (docs only), roblox_tycoon, robloxmaxx.

**Unique to ralph/ only:** Hilal (ramadan-tracker), Streakr (habitforge-web), Mise (mealmaxx-web).

### Native wrapper status

Only 4 of 6 ralph apps have native-wrapper directories with Capacitor iOS scaffolding:

| App | Has native-wrapper | Has package.json | Has capacitor.config |
|-----|-------------------|-----------------|---------------------|
| Hilal (ramadan-tracker) | YES | NO | YES (in native-wrapper) |
| Vault (focuslock-web) | YES | NO | YES (in native-wrapper) |
| Streakr (habitforge-web) | YES | NO | NO |
| Mise (mealmaxx-web) | YES | NO | NO |
| Dusk (sleepmaxx-web) | NO | YES | YES |
| Steplock (walktounlock-web) | NO | YES | YES |

**Inconsistency:** Dusk and Steplock have package.json at web root level (with Capacitor deps). The other 4 have native-wrapper dirs with Xcode project scaffolding but no package.json at web root. Neither approach has working native plugin calls in the actual web code.

---

## 3. Critical deficiencies across ALL 6 apps

From APP_QUALITY_AUDIT_REAL.md (2026-02-12):

1. **ZERO RevenueCat integration.** No `@revenuecat/purchases-capacitor` in any package.json. Paywalls are cosmetic (localStorage booleans). No real IAP, no Stripe, no subscription revenue possible.

2. **All apps are single-file HTML monoliths.** Every app is one `index.html` (40KB-81KB) with inline CSS/JS. Tailwind loaded from CDN (not production-ready). No build system, no modules, no TypeScript.

3. **No native plugin calls from web code.** Some apps have Capacitor plugins in Podfile/package.json, but the JavaScript never calls `Haptics.impact()`, `PushNotifications.register()`, or any Capacitor API. Apple sees "website in a WebView" = Guideline 4.2 rejection.

4. **Hover states on 2 apps.** Vault has 26+ hover states. Streakr has 12+. iOS has no hover. This is a dead giveaway that the app is a website.

5. **No haptic feedback in any app.** AGGREGATE_DESIGN_SYSTEM.md requires haptics on button taps, habit completions, tab switches, milestones, timer events. Zero apps implement this.

6. **No privacy policy URL hosted.** Some apps have privacy text in .md files but no live HTTPS URL. Apple requires a live privacy policy URL.

---

## 4. Document authority map

### Category A: Quality standards and iOS submission

These docs answer "how do I make apps good enough for the App Store?"

| Document | Size | Purpose | Authority Status |
|----------|------|---------|-----------------|
| **APP_QUALITY_STANDARDS.md** | 31KB | THE institutional process doc. Defines minimum 7 screens, animation requirements, design system requirements, code architecture, testing, submission flow. Includes RevylAI Greenlight as mandatory Gate 2/Gate 3 requirement. | AUTHORITATIVE for process/standards. Read FIRST when building any app. |
| **APP_QUALITY_AUDIT_REAL.md** | 27KB | Rigorous code-level audit of all 6 current apps. Per-app scores, specific deficiencies, line-by-line code review. | AUTHORITATIVE for current portfolio status. Shows gap between standards and reality. |
| **IOS_SUBMISSION_PROCESS.md** | 48KB | Step-by-step submission checklist. Pre-build, during-build, metadata, screenshots, App Store Connect, review notes, post-submission. Every checkbox references a real Apple guideline number. Section 3.10 covers mandatory RevylAI Greenlight pre-submission scan. | AUTHORITATIVE for submission workflow. The most detailed and recent (2026-02-12). Use this for the actual submission process. |
| **IOS_REJECTION_PREVENTION.md** | 24KB | Top rejection reasons + prevention tactics. Focused on Capacitor-specific issues (4.2 minimum functionality, 2.1 completeness, 3.1.1 IAP, 5.1.1 privacy). Includes RevylAI Greenlight as automated rejection scanner with guideline mapping. | AUTHORITATIVE for understanding WHY apps get rejected. Focused on prevention reasoning, not step-by-step process. |
| **REJECTION_PREVENTION.md** | 31KB | Top 20 rejection reasons ranked by frequency, with real developer examples and specific prevention checklists. Broader scope than IOS_REJECTION_PREVENTION.md. | SUPPLEMENTARY. Overlaps with IOS_REJECTION_PREVENTION.md but has more breadth (20 reasons vs focused guide). Read both; this one for breadth, the other for Capacitor-specific depth. |
| **AUDIT_OUTPUT.md** | 25KB | Earlier audit from 2026-02-06 covering 3 apps (biomaxx, PrayerLock, roblox). Less rigorous than APP_QUALITY_AUDIT_REAL.md. | SUPERSEDED by APP_QUALITY_AUDIT_REAL.md for app quality assessment. Still useful for biomaxx/roblox info since those are not in the newer audit. |

**Overlap resolution: IOS_REJECTION_PREVENTION.md vs IOS_SUBMISSION_PROCESS.md**
- IOS_REJECTION_PREVENTION.md = "understand the dangers" (why apps get rejected, what to watch for)
- IOS_SUBMISSION_PROCESS.md = "follow the steps" (phase-by-phase checklist from pre-build to post-submission)
- Both are valid. Read IOS_REJECTION_PREVENTION.md for understanding, use IOS_SUBMISSION_PROCESS.md as the operational checklist.
- REJECTION_PREVENTION.md adds breadth (20 reasons vs focused). No real conflict, just different scopes.

**Overlap resolution: APP_QUALITY_STANDARDS.md vs APP_QUALITY_AUDIT_REAL.md**
- APP_QUALITY_STANDARDS.md = "the bar to hit" (what good looks like)
- APP_QUALITY_AUDIT_REAL.md = "where we are" (how far from the bar)
- No conflict. They complement each other. Standards define the target; audit measures the gap.

### Category B: Design, UI/UX, and onboarding

These docs answer "what should the apps look like and how should onboarding work?"

| Document | Size | Purpose | Authority Status |
|----------|------|---------|-----------------|
| **AGGREGATE_DESIGN_SYSTEM.md** | 26KB | Reusable design system for ALL apps. Color palettes by niche (sleep, productivity, faith, habit, meal, fitness), typography scales, spacing system, animation specs, component patterns, haptic feedback specs. | AUTHORITATIVE for implementation. Use this when building screens. Contains specific hex codes, font sizes, spacing values. |
| **APP_UIUX_RESEARCH.md** | 21KB | Market research synthesized from 20+ apps. Onboarding patterns ranked by conversion, paywall tactics, pricing benchmarks from RevenueCat data. | AUTHORITATIVE for market intelligence. References TOP_APP_AUDIT.md for raw data. Contains conversion benchmarks and pricing analysis. |
| **TOP_APP_AUDIT.md** | 65KB | Deep audit of 15+ competing apps: color schemes, typography, icon styles, onboarding flows, paywall placement, user complaints, revenue estimates. Raw data. | AUTHORITATIVE for competitor intelligence. The largest and most detailed competitor research file. Referenced by APP_UIUX_RESEARCH.md and AGGREGATE_DESIGN_SYSTEM.md. |
| **ONBOARDING_PLAYBOOK.md** | 25KB | Screen-by-screen onboarding flows for every app in the portfolio. Universal 4-rule framework + per-app specs with exact screen descriptions, copy, and conversion intent. | AUTHORITATIVE for onboarding implementation. Use this when building the onboarding flow for any specific app. |
| **APP_NAMING_AUDIT.md** | 47KB | Audit of all 7 app names against "would a normie say this out loud?" test. Naming rules, pattern analysis, verdict per app (AUTHENTIC/BORDERLINE/CRINGE), rename suggestions. | AUTHORITATIVE for naming decisions. Current names: PrayerLock (BORDERLINE), Dusk (AUTHENTIC), Vault (AUTHENTIC), Streakr (BORDERLINE), Mise (AUTHENTIC), Steplock (CRINGE), Hilal (AUTHENTIC). |
| **FAVICON_SVG_PACK.md** | 19KB | Inline SVG favicons for all 6 apps. Ready to paste into HTML/manifest. | AUTHORITATIVE for placeholder icons. NOT production app icons (those need 1024x1024 PNG from ImageFX). |

**Overlap resolution: AGGREGATE_DESIGN_SYSTEM.md vs APP_UIUX_RESEARCH.md vs TOP_APP_AUDIT.md**
- TOP_APP_AUDIT.md = raw competitive data (colors, features, revenue per competitor)
- APP_UIUX_RESEARCH.md = synthesized patterns from that data (what patterns win, conversion benchmarks)
- AGGREGATE_DESIGN_SYSTEM.md = our implementation system derived from those patterns (exact hex codes, spacing, typography for our apps)
- Flow: TOP_APP_AUDIT.md (data) -> APP_UIUX_RESEARCH.md (analysis) -> AGGREGATE_DESIGN_SYSTEM.md (implementation)
- No conflict. They are a research pipeline.

### Category C: Discovery, strategy, and arbitrage

These docs answer "what apps should we build and where are the opportunities?"

| Document | Size | Purpose | Authority Status |
|----------|------|---------|-----------------|
| **APP_DISCOVERY_ENGINE.md** | 41KB | Unified discovery system. Revenue intelligence sources (CloneChart, AppMagic, AppTweak, RevenueCat), validation pipeline, build criteria, distribution checklist. Claims to supersede several individual files but those remain as deep-dive references. | AUTHORITATIVE for the discovery process. The most recent (2026-02-12) and most comprehensive. Use this as the starting point for finding new apps to build. |
| **APP_CLONE_REBRAND_STRATEGY.md** | 26KB | Regional arbitrage (9 languages), demographic repackaging (women, teens, seniors), niche vertical cloning. Portfolio model (30+ apps at $500-2K/mo each). | AUTHORITATIVE for clone/rebrand methodology. Specific tactics for localization, 4.3 spam avoidance, review mining. |
| **APP_ARBITRAGE_MATRIX.md** | 21KB | 15+ scored opportunities (Demand + Competition + Build difficulty). Category A: language/region arb. Category B: demographic repackaging. Category C: feature gap exploitation. | AUTHORITATIVE for specific arbitrage opportunities. Scored and ranked. Start here when picking what to build next. |
| **ARB_OPPORTUNITIES_10.md** | 28KB | 10 detailed arbitrage opportunities with full specs: market size, competitor analysis, our version spec, revenue projection (base/bull case), build time estimate. | AUTHORITATIVE for top-10 actionable opportunities. More detailed per-opportunity than APP_ARBITRAGE_MATRIX.md. |
| **APP_STORE_AUDIT_FEB2026.md** | 27KB | Live App Store data from Feb 2026. Top free/paid charts, trending categories, international market analysis (10 markets), category-specific rankings. | AUTHORITATIVE for Feb 2026 market snapshot. Will need refreshing monthly. |
| **APP_STORE_TRENDS_FEB2026.md** | 20KB | Trend analysis derived from audit. Rising categories ranked (AI, Health, Prediction Markets, Self-Care, Faith, Fasting, Digital Wellness). | AUTHORITATIVE for Feb 2026 trend direction. Complements the raw audit data. |
| **CLONECHART_DATA_EXTRACT.md** | 10KB | Partial data extract from CloneChart.io (12,000+ iOS apps with clone difficulty ratings). Extraction was blocked, so this is partial/metadata only. | INCOMPLETE. Needs full scrape via browser. |
| **COMPETITOR_REAL_DATA.md** | 29KB | Verified pricing, revenue, features for competitors in each category (sleep, productivity, faith, habit, meal, fitness). Sourced from Sensor Tower, Business of Apps, company reports. | AUTHORITATIVE for competitor pricing/revenue data. Most recent (2026-02-12). Use this for pricing decisions. |
| **COMPETITOR_GTM_TACTICS.md** | 17KB | How top apps got their first 10K users. Forest (viral guilt mechanic), Strava (cycling clubs), Duolingo (streaks + mascot memes), Calm (Product Hunt), etc. | AUTHORITATIVE for acquisition tactic inspiration. Real case studies with specific tactics. |
| **ANDROID_CLONE_SPECS.md** | 10KB | Specs for 3 Android PWA clones: AI Hairstyle Try-On, AI Video Generator, AI Music Generator. | SUPPLEMENTARY. Android-focused opportunities. Not built. |
| **NOFAP_KARMAMAXX_APP_SPEC.md** | 30KB | Full app spec for porn addiction recovery app. Market analysis ($250K MRR competitor proof), feature list, monetization model, ethical framework. | AUTHORITATIVE for this specific app concept. Self-contained spec ready for build. |

**Note:** APP_DISCOVERY_ENGINE.md claims to "supersede" APP_CLONE_REBRAND_STRATEGY.md, CLONECHART_DATA_EXTRACT.md, APP_ARBITRAGE_MATRIX.md, COMPETITOR_GTM_TACTICS.md, APP_STORE_AUDIT_FEB2026.md, APP_UIUX_RESEARCH.md, TOP_APP_AUDIT.md, and APP_FACTORY_GTM_MASTER.md. This is not accurate. It UNIFIES them as an entry point but does not replace their detail. The individual files remain authoritative for deep-dive reference.

### Category D: GTM and launch

These docs answer "how do we launch and market these apps?"

| Document | Size | Purpose | Authority Status |
|----------|------|---------|-----------------|
| **APP_FACTORY_GTM_MASTER.md** | 20KB | Combined GTM strategy for the entire portfolio. Revenue model per app, shared audience mapping, launch sequence, "App Factory Week" Product Hunt plan, cross-promotion strategy. | AUTHORITATIVE for portfolio-level GTM strategy. References all research docs. |
| **GTM_BY_BUDGET.md** | 28KB | GTM playbooks at 4 budget levels ($0, $100, $500, $1,000). Channel-by-channel breakdown with expected CPI, conversion rates, timeline to ROI. | AUTHORITATIVE for budget-constrained launch tactics. Use this when deciding how much to spend. |
| **COMPETITOR_GTM_TACTICS.md** | 17KB | (Also listed in Category C) How top apps got first 10K users. | See above. |
| **PRINTMAXX_APP_PLAYBOOK.md** | 30KB | The 11-phase assembly line: Research -> Build -> Test -> Launch -> Monetize -> Cross-Promote -> Iterate. Includes competitive audit checklist, demand validation, design sprints, ASO optimization. | AUTHORITATIVE for the end-to-end build-to-launch process. More operational than GTM_MASTER (which is strategic). |

### Category E: Asset generation

These docs answer "how do I create icons, screenshots, and visual assets?"

| Document | Size | Purpose | Authority Status |
|----------|------|---------|-----------------|
| **APP_ASSET_GENERATION_PROMPTS.md** | 41KB | Google ImageFX / Imagen 3 prompts for all 6 apps. App icons, screenshots, marketing images. Prompt engineering tips specific to Imagen 3. | AUTHORITATIVE for ImageFX/Imagen prompts. Comprehensive per-app prompts. |
| **assets/ICON_GENERATION_PROMPTS_V3.md** | 14KB | Earlier icon prompt set. Uses different color specs for some apps (e.g., PrayerLock uses teal+gold here vs gold+deep blue in the newer file). | PARTIALLY SUPERSEDED. APP_ASSET_GENERATION_PROMPTS.md is more comprehensive and newer. Use this only for V3-specific prompt variants. |
| **FAVICON_SVG_PACK.md** | 19KB | SVG favicons for all 6 apps. | See Category B. |

### Category E2: Automated compliance tools

| Document / Tool | Location | Purpose | Authority Status |
|----------------|----------|---------|-----------------|
| **RevylAI Greenlight** | `https://github.com/RevylAI/greenlight` (external) | Open-source Apple App Store pre-submission compliance scanner. Checks metadata (Info.plist, icons, bundle ID), 30+ rejection-risk code patterns (private APIs, secrets, unauthorized payments, dynamic code), privacy compliance (PrivacyInfo.xcprivacy, Required Reason APIs, tracking SDKs), and IPA binary analysis. | MANDATORY tool. Run before every TestFlight upload and every App Store submission. See IOS_SUBMISSION_PROCESS.md Section 3.10. |
| **greenlight_checker.py** | `AUTOMATIONS/greenlight_checker.py` | PRINTMAXX wrapper script that runs Greenlight across all 6 portfolio apps, parses JSON output, shows pass/fail summary per app, exits with CI/CD-compatible codes. CLI: `--app <name>`, `--all`, `--fix`. | AUTHORITATIVE for portfolio-wide compliance scanning. |

### Category F: Restructure and process

| Document | Size | Purpose | Authority Status |
|----------|------|---------|-----------------|
| **APP_RESTRUCTURE_PLAN.md** | 21KB | Portfolio overview of all 10 app files found, duplicate resolution plan, per-app restructure recommendations. Identified that ralph versions are canonical. | AUTHORITATIVE for understanding the file layout and duplicates. Use this index (APP_FACTORY_CENTRAL_INDEX.md) going forward instead. |
| **VIBE_CODING_5_APPS_PLAN.md** | 8KB | Original plan to build 5 "lock" apps in 5 days via vibe coding. Only PrayerLock was built from this plan. | HISTORICAL. The plan was partially executed. The other 4 "lock" apps were built differently (as general-purpose apps, not lock-screen apps). |

---

## 5. Per-app file map (complete)

### Hilal (Ramadan Tracker)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `ralph/.../ramadan-tracker/index.html` | 81KB | Main app (single-file PWA, 1,608 lines) |
| sw.js | `ralph/.../ramadan-tracker/sw.js` | ~3KB | Service worker for offline |
| manifest.json | `ralph/.../ramadan-tracker/manifest.json` | ~1KB | PWA manifest |
| vercel.json | `ralph/.../ramadan-tracker/vercel.json` | ~1KB | Vercel deployment config |
| deploy.md | `ralph/.../ramadan-tracker/deploy.md` | ~2KB | Deployment instructions |
| DEPLOY_GUIDE.md | `ralph/.../ramadan-tracker/DEPLOY_GUIDE.md` | | Extended deployment guide |
| ASO_CONTENT.md | `ralph/.../ramadan-tracker/ASO_CONTENT.md` | | App Store Optimization content |
| MARKETING_BLITZ.md | `ralph/.../ramadan-tracker/MARKETING_BLITZ.md` | | Marketing campaign plan |
| PRODUCT_HUNT_LAUNCH.md | `ralph/.../ramadan-tracker/PRODUCT_HUNT_LAUNCH.md` | | Product Hunt launch plan |
| native-wrapper/ | `ralph/.../ramadan-tracker/native-wrapper/` | | Capacitor iOS project scaffold (Xcode project, Podfile, AppDelegate) |

**Highlights:** Bilingual EN/AR with RTL. Astronomical prayer calculator (no API needed). 5-tab interface (Home, Quran, Duas, Charity, Stats). Best onboarding of all apps (6 steps). Fake paywall (localStorage). URGENT: Ramadan 2026 starts Feb 28.

### Vault (FocusLock)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `ralph/.../focuslock-web/index.html` | 77KB | Main app (CANONICAL) |
| index.html | `builds/focuslock-web/index.html` | 40KB | OUTDATED copy |
| sw.js | `ralph/.../focuslock-web/sw.js` | | Service worker |
| manifest.json | `ralph/.../focuslock-web/manifest.json` | | PWA manifest |
| vercel.json | `ralph/.../focuslock-web/vercel.json` | | Vercel config |
| deploy.md | `ralph/.../focuslock-web/deploy.md` | | Deploy instructions |
| PRODUCT_HUNT_LAUNCH.md | `ralph/.../focuslock-web/PRODUCT_HUNT_LAUNCH.md` | | Launch plan |
| native-wrapper/ | `ralph/.../focuslock-web/native-wrapper/` | | Capacitor iOS scaffold |

**Critical issues:** 26+ hover states, weakest onboarding (3 static screens), zero monetization, only 1 Capacitor plugin.

### Streakr (HabitForge)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `ralph/.../habitforge-web/index.html` | 82KB | Main app |
| sw.js | `ralph/.../habitforge-web/sw.js` | | Service worker |
| manifest.json | `ralph/.../habitforge-web/manifest.json` | | PWA manifest |
| vercel.json | `ralph/.../habitforge-web/vercel.json` | | Vercel config |
| deploy.md | `ralph/.../habitforge-web/deploy.md` | | Deploy instructions |
| PRODUCT_HUNT_LAUNCH.md | `ralph/.../habitforge-web/PRODUCT_HUNT_LAUNCH.md` | | Launch plan |
| native-wrapper/ | `ralph/.../habitforge-web/native-wrapper/` | | Capacitor iOS scaffold |

**Critical issues:** 12+ hover states, no monetization, weak onboarding.

### Mise (MealMaxx)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `ralph/.../mealmaxx-web/index.html` | 55KB | Main app |
| sw.js | `ralph/.../mealmaxx-web/sw.js` | | Service worker |
| manifest.json | `ralph/.../mealmaxx-web/manifest.json` | | PWA manifest |
| vercel.json | `ralph/.../mealmaxx-web/vercel.json` | | Vercel config |
| deploy.md | `ralph/.../mealmaxx-web/deploy.md` | | Deploy instructions |
| PRODUCT_HUNT_LAUNCH.md | `ralph/.../mealmaxx-web/PRODUCT_HUNT_LAUNCH.md` | | Launch plan |
| native-wrapper/ | `ralph/.../mealmaxx-web/native-wrapper/` | | Capacitor iOS scaffold |

**Status:** Clean UI, decent onboarding (6/10). No monetization, no native plugin calls. Zero hover states (good).

### Dusk (SleepMaxx)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `ralph/.../sleepmaxx-web/index.html` | 57KB | Main app (CANONICAL) |
| index.html | `builds/sleepmaxx-web/index.html` | 41KB | OUTDATED copy |
| sw.js | `ralph/.../sleepmaxx-web/sw.js` | | Service worker |
| manifest.json | `ralph/.../sleepmaxx-web/manifest.json` | | PWA manifest |
| vercel.json | `ralph/.../sleepmaxx-web/vercel.json` | | Vercel config |
| package.json | `ralph/.../sleepmaxx-web/package.json` | | Has Capacitor deps |
| capacitor.config.json | `ralph/.../sleepmaxx-web/capacitor.config.json` | | Capacitor config at root |
| deploy.md | `ralph/.../sleepmaxx-web/deploy.md` | | Deploy instructions |
| PRODUCT_HUNT_LAUNCH.md | `ralph/.../sleepmaxx-web/PRODUCT_HUNT_LAUNCH.md` | | Launch plan |

**Note:** NO native-wrapper/ directory. Has package.json with Capacitor deps at web root instead. Different architecture from the other 4 apps.

### Steplock (WalkToUnlock)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `ralph/.../walktounlock-web/index.html` | 51KB | Main app (CANONICAL) |
| index.html | `builds/walktounlock-web/index.html` | 31KB | OUTDATED copy |
| sw.js | `ralph/.../walktounlock-web/sw.js` | | Service worker |
| manifest.json | `ralph/.../walktounlock-web/manifest.json` | | PWA manifest |
| vercel.json | `ralph/.../walktounlock-web/vercel.json` | | Vercel config |
| package.json | `ralph/.../walktounlock-web/package.json` | | Has Capacitor deps |
| capacitor.config.json | `ralph/.../walktounlock-web/capacitor.config.json` | | Capacitor config at root |
| deploy.md | `ralph/.../walktounlock-web/deploy.md` | | Deploy instructions |
| PRODUCT_HUNT_LAUNCH.md | `ralph/.../walktounlock-web/PRODUCT_HUNT_LAUNCH.md` | | Launch plan |

**Note:** Same pattern as Dusk (package.json at root, no native-wrapper/).

### PrayerLock (builds/ only)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| index.html | `builds/prayerlock-web/index.html` | 72KB | Main app (1,315 lines) |
| sw.js | `builds/prayerlock-web/sw.js` | 3KB | Service worker |
| manifest.json | `builds/prayerlock-web/manifest.json` | 3KB | PWA manifest |
| deploy.md | `builds/prayerlock-web/deploy.md` | 2KB | 5 deployment options |
| PRODUCT_HUNT_LAUNCH.md | `builds/prayerlock-web/PRODUCT_HUNT_LAUNCH.md` | 6KB | Launch plan |

**Status:** Functional PWA with prayer timer, streak tracker, Qibla compass, tasbih counter, daily verse, dark/light mode. No monetization. No Capacitor native wrapper. Can deploy to Vercel in 60 seconds.

---

## 6. Legacy directory: `app factory/` (project root)

This is the ORIGINAL app factory directory from Jan 2026. Contains Scripture Streak (React Native + Expo), marketing shell scripts, screenshots, and older planning docs. DO NOT use for new work.

| Path | Contents |
|------|----------|
| `app factory/APP-BUILD-SPECS.md` | 32KB build specs (Jan 2026) |
| `app factory/app-factory-playbook.md` | 21KB original playbook |
| `app factory/app-ideas-validated.md` | 13KB validated app ideas |
| `app factory/AUTOMATION-SETUP.md` | 8KB automation setup |
| `app factory/CURSOR-CHEATSHEET.md` | 11KB Cursor IDE tips |
| `app factory/SUCCESSFUL-PROMPTS.md` | 13KB prompts that worked |
| `app factory/app-factory/` | Nested directory with shell scripts (setup, launch, marketing), app-store-assets/, base-template/, expanded-apps/, non-religious-apps/, religious-apps/, partnerships/, marketing-campaigns/, docs-templates/ |
| `app factory/Scripture Streak/` | MASTER-LAUNCH-CHECKLIST.md, README.md |
| `app factory/scripture-streak/` | Full React Native app (package.json, tsconfig, app.json, src/, ios/, android/, node_modules/, screenshots/, supabase SQL, subscription key file) |
| `app factory/*.png` | 12 screenshots (paywall, onboarding, polished app, settings, etc.) |
| `app factory/app-demo.mp4` | 231KB demo video |

**IMPORTANT:** `app factory/scripture-streak/SubscriptionKey_9JRT5MB96F.p8` is a subscription key file. This should be in .gitignore if not already.

---

## 7. LEDGER tracking files

| File | Rows | Purpose |
|------|------|---------|
| `LEDGER/APP_CLONE_OPPORTUNITIES.csv` | 8 entries (CLONE001-008) | Scored clone opportunities from app_clone_finder.py |
| `LEDGER/MEGA_SHEET/TAB6_APPS_ECOM_MASTER.csv` | MISSING | Should contain app + ecom data but file does not exist |

**Gap:** There is no `LEDGER/APP_FACTORY_METHODS.csv` file despite being referenced in CLAUDE.md. No centralized tracking of app build status, deployment state, or revenue per app exists in LEDGER.

---

## 8. Complete document list (all 31 files in MONEY_METHODS/APP_FACTORY/)

| # | File | Size | Category | Quick Description |
|---|------|------|----------|------------------|
| 1 | AGGREGATE_DESIGN_SYSTEM.md | 26KB | Design | Color palettes, typography, spacing, animations per niche |
| 2 | ANDROID_CLONE_SPECS.md | 10KB | Strategy | 3 Android PWA clone specs (hairstyle, video, music) |
| 3 | APP_ARBITRAGE_MATRIX.md | 22KB | Strategy | 15+ scored arbitrage opportunities |
| 4 | APP_ASSET_GENERATION_PROMPTS.md | 41KB | Assets | ImageFX/Imagen 3 prompts for all 6 apps |
| 5 | APP_CLONE_REBRAND_STRATEGY.md | 26KB | Strategy | Regional/demographic/niche cloning methodology |
| 6 | APP_DISCOVERY_ENGINE.md | 41KB | Strategy | Unified discovery pipeline (supersedes older individual files as entry point) |
| 7 | APP_FACTORY_CENTRAL_INDEX.md | -- | Index | THIS FILE |
| 8 | APP_FACTORY_GTM_MASTER.md | 20KB | GTM | Portfolio-level go-to-market strategy |
| 9 | APP_NAMING_AUDIT.md | 47KB | Quality | Name audit for all 7 apps + naming rules |
| 10 | APP_QUALITY_AUDIT_REAL.md | 27KB | Quality | Rigorous code-level audit of all 6 PWAs (scores 38-52) |
| 11 | APP_QUALITY_STANDARDS.md | 31KB | Quality | THE institutional standards doc (what good looks like) |
| 12 | APP_RESTRUCTURE_PLAN.md | 21KB | Process | Duplicate resolution, per-app restructure plan |
| 13 | APP_STORE_AUDIT_FEB2026.md | 27KB | Research | Live App Store data snapshot Feb 2026 |
| 14 | APP_STORE_TRENDS_FEB2026.md | 20KB | Research | Trending categories Feb 2026 |
| 15 | APP_UIUX_RESEARCH.md | 21KB | Design | Synthesized UI/UX patterns from 20+ apps |
| 16 | ARB_OPPORTUNITIES_10.md | 28KB | Strategy | 10 detailed arbitrage opportunities with full specs |
| 17 | AUDIT_OUTPUT.md | 25KB | Quality | Earlier audit (Feb 6) covering biomaxx, PrayerLock, roblox |
| 18 | CLONECHART_DATA_EXTRACT.md | 10KB | Research | Partial CloneChart.io data (extraction blocked) |
| 19 | COMPETITOR_GTM_TACTICS.md | 17KB | GTM | How top apps got first 10K users |
| 20 | COMPETITOR_REAL_DATA.md | 29KB | Research | Verified competitor pricing, revenue, features |
| 21 | FAVICON_SVG_PACK.md | 19KB | Assets | SVG favicons for all 6 apps |
| 22 | GTM_BY_BUDGET.md | 28KB | GTM | GTM playbooks at $0/$100/$500/$1000 budgets |
| 23 | IOS_REJECTION_PREVENTION.md | 24KB | Quality | Rejection reasons + Capacitor-specific prevention |
| 24 | IOS_SUBMISSION_PROCESS.md | 48KB | Quality | Step-by-step submission checklist (most detailed) |
| 25 | NOFAP_KARMAMAXX_APP_SPEC.md | 30KB | Strategy | Full spec for NoFap recovery app |
| 26 | ONBOARDING_PLAYBOOK.md | 25KB | Design | Screen-by-screen onboarding flows for every app |
| 27 | PRINTMAXX_APP_PLAYBOOK.md | 30KB | Process | 11-phase assembly line playbook |
| 28 | REJECTION_PREVENTION.md | 31KB | Quality | Top 20 rejection reasons (broader scope) |
| 29 | TOP_APP_AUDIT.md | 65KB | Research | Deep audit of 15+ competing apps |
| 30 | VIBE_CODING_5_APPS_PLAN.md | 8KB | Historical | Original 5-lock-apps plan (partially executed) |
| 31 | assets/ICON_GENERATION_PROMPTS_V3.md | 14KB | Assets | Earlier icon prompts (partially superseded) |

**Total documentation size:** ~780KB across 31 files.

---

## 9. Reading order for new agents

### "I'm building a new app from scratch"
1. APP_QUALITY_STANDARDS.md (know the bar)
2. APP_DISCOVERY_ENGINE.md (find what to build)
3. AGGREGATE_DESIGN_SYSTEM.md (get the design tokens)
4. ONBOARDING_PLAYBOOK.md (design the flow)
5. IOS_SUBMISSION_PROCESS.md (prep for submission)

### "I'm fixing an existing app for iOS submission"
1. APP_QUALITY_AUDIT_REAL.md (know what's broken)
2. IOS_REJECTION_PREVENTION.md (understand why it'd get rejected)
3. APP_QUALITY_STANDARDS.md (know the target)
4. IOS_SUBMISSION_PROCESS.md (follow the checklist)

### "I'm deciding what app to build next"
1. APP_DISCOVERY_ENGINE.md (process)
2. APP_ARBITRAGE_MATRIX.md (scored opportunities)
3. ARB_OPPORTUNITIES_10.md (detailed specs)
4. COMPETITOR_REAL_DATA.md (market intel)
5. APP_STORE_TRENDS_FEB2026.md (trend direction)

### "I'm preparing to launch an app"
1. APP_FACTORY_GTM_MASTER.md (portfolio strategy)
2. GTM_BY_BUDGET.md (budget-appropriate tactics)
3. COMPETITOR_GTM_TACTICS.md (proven acquisition plays)
4. IOS_SUBMISSION_PROCESS.md (submission checklist)

---

## 10. Next actions (priority order)

### Blocking: Must do before ANY app can ship

1. **Integrate RevenueCat into at least 1 app.** Zero apps have payment infrastructure. Start with Hilal (highest score, Ramadan deadline). Install `@revenuecat/purchases-capacitor`, configure products in RevenueCat dashboard, replace localStorage boolean with real subscription check.

2. **Add native Capacitor plugin calls to web code.** Every app needs `Haptics.impact()` on button taps, `LocalNotifications.schedule()` for reminders, `StatusBar.setStyle()` for native feel. Currently: plugins exist in config files but are never called from JavaScript.

3. **Remove all hover states from Vault (26) and Streakr (12).** Replace with `:active` states or tap animations. Hover is a website signal on iOS.

4. **Replace Tailwind CDN with built CSS.** All apps load Tailwind from CDN which adds 300KB+ and is explicitly not for production. Either build Tailwind locally or use the custom CSS approach that Dusk already uses.

5. **Host privacy policy URLs.** Every app needs a live HTTPS privacy policy URL before App Store submission. Deploy to Vercel/Netlify free tier.

6. **Create Apple Developer account.** $99/year. Required for any App Store submission. Currently not created.

### High priority: Ramadan deadline (Feb 28, 2026)

7. **Deploy Hilal as PWA immediately.** Even without iOS submission, deploy to Vercel as a web app. Users searching "ramadan tracker" on Google can use it. `cd ralph/loops/app_factory/output/ramadan-tracker/ && vercel deploy --prod`

8. **Fix Hilal for iOS.** Add real RevenueCat IAP. Add Haptics/StatusBar/Preferences Capacitor calls. Add "Restore Purchases" button. Host privacy policy. Submit to App Store by Feb 20 (allows 1 week for review before Ramadan).

### Medium priority: Portfolio improvement

9. **Rebuild Vault (FocusLock) from scratch.** Score 38/100 with 26 hover states and zero monetization. The weakest app. Either rebuild or deprioritize.

10. **Add onboarding quiz to Dusk, Vault, Streakr.** These three have the weakest onboarding (3/10 each). The ONBOARDING_PLAYBOOK.md has exact screen specs.

11. **Build KarmaMaxx.** Full spec exists (NOFAP_KARMAMAXX_APP_SPEC.md). $250K MRR competitor validates the market. Low competition due to stigma.

### Low priority: Strategic

12. **Create LEDGER/APP_FACTORY_METHODS.csv.** No centralized tracking of app status exists. Create a CSV tracking: app name, build status, deployment URL, iOS submission status, revenue, downloads.

13. **Rebuild TAB6_APPS_ECOM_MASTER.csv.** This MEGA_SHEET tab is missing. The build script and 9 other tabs exist but Tab 6 was never generated.

14. **Scrape CloneChart.io fully.** CLONECHART_DATA_EXTRACT.md is partial. Need browser-based scrape for the full 12,000+ app database.

15. **Archive legacy `app factory/` directory.** Contains old Scripture Streak code, screenshots, and shell scripts. Keep for reference but mark clearly as legacy.

---

## 11. Quick reference paths

```
# Canonical app code (6 PWAs)
ralph/loops/app_factory/output/ramadan-tracker/     # Hilal - BEST (52/100)
ralph/loops/app_factory/output/walktounlock-web/     # Steplock (44/100)
ralph/loops/app_factory/output/mealmaxx-web/         # Mise (42/100)
ralph/loops/app_factory/output/habitforge-web/       # Streakr (40/100)
ralph/loops/app_factory/output/sleepmaxx-web/        # Dusk (40/100)
ralph/loops/app_factory/output/focuslock-web/        # Vault - WORST (38/100)

# PrayerLock (unique to builds/)
MONEY_METHODS/APP_FACTORY/builds/prayerlock-web/

# Strategy/research docs
MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_ENGINE.md    # Start here for "what to build"
MONEY_METHODS/APP_FACTORY/APP_QUALITY_STANDARDS.md   # Start here for "how to build"
MONEY_METHODS/APP_FACTORY/IOS_SUBMISSION_PROCESS.md  # Start here for "how to submit"

# Competitor data
MONEY_METHODS/APP_FACTORY/COMPETITOR_REAL_DATA.md    # Verified pricing/revenue
MONEY_METHODS/APP_FACTORY/TOP_APP_AUDIT.md           # Deep competitor teardowns

# Design system
MONEY_METHODS/APP_FACTORY/AGGREGATE_DESIGN_SYSTEM.md # Colors, typography, spacing
MONEY_METHODS/APP_FACTORY/ONBOARDING_PLAYBOOK.md     # Screen-by-screen flows

# Clone/arb opportunities
MONEY_METHODS/APP_FACTORY/APP_ARBITRAGE_MATRIX.md    # Scored opportunities
MONEY_METHODS/APP_FACTORY/ARB_OPPORTUNITIES_10.md    # Top 10 detailed

# GTM
MONEY_METHODS/APP_FACTORY/APP_FACTORY_GTM_MASTER.md  # Portfolio strategy
MONEY_METHODS/APP_FACTORY/GTM_BY_BUDGET.md           # Budget-tier tactics

# Asset generation
MONEY_METHODS/APP_FACTORY/APP_ASSET_GENERATION_PROMPTS.md  # ImageFX prompts

# Legacy (DO NOT use for new work)
app factory/                                          # Old Scripture Streak + Jan 2026 docs
```
