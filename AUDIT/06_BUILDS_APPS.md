# BUILDS & APPS AUDIT

**Auditor:** Claude Opus 4.6
**Date:** 2026-02-14
**Scope:** All deployed sites, build artifacts, landing pages, Ralph, app factory, terminal app

---

## Summary Stats

- Total distinct projects/builds on disk: 18
- Deployed/live on surge.sh (verified 200 OK): 14
- Returning 404 (broken): 2 (printmaxx-demos.surge.sh, printmaxx-local-demos.surge.sh)
- Working with real functionality: 2 (SiteScore site-scorer, programmatic SEO index)
- Static demos / portfolio pieces (no backend, no real data): 12
- Revenue currently generated: $0
- Revenue infrastructure (payment, Stripe, RevenueCat): ZERO integrated

---

## Deployed Sites Inventory (Live Verification Feb 14 2026)

| # | Name | URL | HTTP | What It Actually Is | Real Functionality? | Revenue Potential |
|---|------|-----|------|---------------------|---------------------|-------------------|
| 1 | Programmatic SEO | printmaxx-seo.surge.sh | 200 | 602 static HTML pages (12 services x 50 cities) | Directory/index pages with service descriptions. No forms, no backend, no lead capture. | LOW - surge.sh blocks Google indexing (Disallow: / in robots.txt). Zero organic traffic possible. |
| 2 | Ramadan Tracker (Hilal) | hilal-ramadan.surge.sh | 200 | PWA - bilingual EN/AR Ramadan companion | Frontend-only PWA with prayer times, fasting tracker. Installable. No backend persistence. | LOW - Ramadan 2026 already passed (Feb 28). Seasonal. No monetization hook. |
| 3 | FocusLock | focuslock-app.surge.sh | 200 | PWA productivity timer | Single-page HTML/JS app. Timer UI. No backend, no accounts, no payments. | NONE as deployed. Would need native app + subscriptions to monetize. |
| 4 | HabitForge | habitforge-app.surge.sh | 200 | PWA habit tracker | Single-page HTML/JS app. Streak tracking in localStorage. No backend. | NONE as deployed. |
| 5 | SleepMaxx | sleepmaxx-app.surge.sh | 200 | PWA sleep tracker | Single-page HTML/JS. 6 files, ~51KB total. Minimal. | NONE as deployed. |
| 6 | WalkToUnlock | walktounlock-app.surge.sh | 200 | PWA fitness tracker | Single-page HTML/JS. 6 files, ~49KB total. Minimal. | NONE as deployed. |
| 7 | MealMaxx | mealmaxx-app.surge.sh | 200 | PWA nutrition tracker | Single-page HTML/JS. 6 files, ~52KB total. Minimal. | NONE as deployed. |
| 8 | SiteScore SaaS | sitescore-app.surge.sh | 200 | Website analyzer tool | FUNCTIONAL: Uses Google PageSpeed Insights API. Enter URL, get real scores. 559-line app.js. | MEDIUM - actually works. Could add paid tier. No payment integration exists. |
| 9 | SiteScore Analyzer | sitescore-analyzer.surge.sh | 200 | SEO competitor analyzer | Static HTML with hardcoded "30,200+ businesses scored" claim. Input form but analysis is client-side mock. | LOW - mostly a portfolio demo. |
| 10 | ShopMetrics Dashboard | shopmetrics-dashboard.surge.sh | 200 | Analytics dashboard demo | Pure static HTML/CSS. Hardcoded fake data. No real analytics. | NONE - portfolio piece only. |
| 11 | Flowstack Landing | flowstack-demo.surge.sh | 200 | SaaS landing page demo | 2,003-line static HTML. Beautiful design. Zero functionality. No backend, no signup. | NONE - portfolio piece for freelance proposals. |
| 12 | Pipeline Dashboard | printmaxx-dashboard.surge.sh | 200 | Bloomberg-style internal dashboard | Generated HTML with Chart.js. Shows pipeline metrics from CSV data at generation time. Static snapshot. | NONE - internal tool. |
| 13 | Portfolio Site | printmaxx-portfolio.surge.sh | 200 | Agency credibility site | Static landing page for cold outreach. Lists services, pricing, links to demo sites. | LOW - lead gen tool for freelance, not direct revenue. |
| 14 | Website Analyzer | printmaxx-analyzer.surge.sh | 200 | Website scoring lead-gen tool | Animated scanning UI. Likely uses PageSpeed API like site-scorer. | LOW - lead capture, not direct revenue. |
| 15 | Demo Sites (motion) | printmaxx-demos.surge.sh | **404** | Local biz animated demos (dental, restaurant, realtor) | BROKEN - returning 404. Was redeployed Feb 13 but down again. | NONE while down. |
| 16 | Local Biz Demos | printmaxx-local-demos.surge.sh | **404** | 6 business demo sites | BROKEN - returning 404. Referenced in docs but not live. | NONE while down. |

### Sites Referenced But Never Verified Deployed

These URLs appear in documentation but were never confirmed with actual deployment commands:

- dental-demo.surge.sh, restaurant-site-demo.surge.sh, fitness-demo.surge.sh, legal-demo.surge.sh, plumber-demo.surge.sh, realtor-demo.surge.sh (listed in LOCAL_BIZ_EXECUTION_STATUS.md but deployment status unclear)
- dental-motion.surge.sh, realtor-motion.surge.sh, restaurant-motion.surge.sh (individual motion template URLs)

---

## Ralph AI Assessment

**What Ralph is:** An autonomous agent loop system. Not a chatbot or product. It is a pattern for running Claude CLI (`claude --dangerously-skip-permissions`) in a `while true` loop, where each iteration reads a prompt file, does one task, writes state to disk, and exits. Memory lives on the filesystem, not in context.

**Architecture:**
- 62 loop directories under `ralph/loops/` (a01-a08, af01-af02, c01-c10, e01-e07, g01-g03, o01-o03, p01-p04, s01-s06, plus named loops like app_factory, content_machine, daily_ops, etc.)
- Swarm orchestration system at `ralph/.swarm/` (documented in SWARM_ORCHESTRATION_V3.md)
- Progress monitor: `ralph/progress_monitor.py` (Rich TUI showing loop progress)
- Overnight runner: `ralph/run_overnight_sprint.sh`

**Does it work?**
- The swarm system (`ralph/.swarm/`) reportedly worked and produced 184 alpha entries.
- Individual loops (`ralph/loops/*/run.sh`) are documented as BROKEN due to invalid `--max-tokens` flag.
- The mega loop (`ralph/loops/mega/`) is documented but NOT BUILT on disk.
- The `.ralph/` config directory contains CSV files for content farming and progress tracking, plus guardrails and error logs.
- The overnight orchestration scripts exist but depend on the Claude CLI and API tokens, making autonomous operation fragile.

**Bottom line:** Ralph is an interesting autonomous agent architecture, but it is an internal development tool, not a product. It has no revenue potential on its own. Its output (alpha entries, content, app builds) is the value, and that output is mixed quality.

---

## App Factory Assessment

### Legacy App Factory (`app factory/`)

- Contains "Scripture Streak" - an Expo/React Native app with actual node_modules, iOS/Android dirs, Supabase SQL, and a `.env` file with what appears to be real API keys.
- Has an `app-factory/` subdirectory with shell scripts for batch app creation (religious apps, non-religious apps, expanded apps), marketing automation, and Apple Store guidelines.
- Contains screenshots of actual mobile app UIs (paywall screens, onboarding, settings).
- **Status:** Old project from Jan 2025. Not deployed. Has node_modules bloat (481 dirs). Not actively maintained.

### New App Factory Output (`ralph/loops/app_factory/output/`)

6 PWA apps built and deployed to surge.sh:

| App | Files | Size | Actual Quality |
|-----|-------|------|----------------|
| ramadan-tracker | 10 files | ~3.6 MB (with docs) | Most complete. Has manifest.json, service worker, deploy guide. Bilingual EN/AR. |
| focuslock-web | 7 files | ~656 KB | Single index.html + manifest + service worker. Functional timer. |
| habitforge-web | 7 files | ~672 KB | Same structure. Habit tracking in localStorage. |
| sleepmaxx-web | 6 files | ~51 KB | Minimal. Basic sleep log. |
| walktounlock-web | 6 files | ~49 KB | Minimal. Step tracking concept (no actual pedometer - needs native). |
| mealmaxx-web | 6 files | ~52 KB | Minimal. Basic meal log. |

**Quality verdict:** The larger apps (FocusLock, HabitForge, Ramadan) are functional but basic PWAs. The smaller ones (SleepMaxx, WalkToUnlock, MealMaxx) at ~50KB are extremely minimal - barely more than styled HTML forms. None have backends, user accounts, payment integration, or real data persistence beyond localStorage. The code-level audit in `APP_QUALITY_AUDIT_REAL.md` scored the portfolio average at 42.7/100.

**What is the app factory actually producing?** Single-file HTML/JS/CSS apps wrapped as PWAs with manifest.json and service workers. No React, no build system, no component architecture. The apps have hover states designed for desktop (not mobile), no RevenueCat or payment SDK, and zero monetization hooks.

---

## Landing Pages Assessment

### Next.js Landing Site (`07_LANDING/printmaxx-site/`)

- **Stack:** Next.js 16.1.3 with App Router, Turbopack, Tailwind CSS
- **Routes:** Homepage, /truth (content pages), /truth/[slug] (dynamic), /magnet/stack-generator, /apps, API routes
- **Status:** Has `.next` build directory and `out/` export. NOT deployed to any public URL. Development only.
- **Quality:** Has real route structure, components directory, content directory. Most complete frontend project in the repo.
- **Conversion potential:** Contains lead capture form concept but no evidence of actual leads captured. No analytics, no A/B testing, no CRM integration.

### Programmatic SEO Pages (`builds/programmatic_seo/`)

- 602 HTML files across 12 service categories x 50 cities
- Each page is a static service landing page for a specific city (e.g., "Web Design in Austin")
- Has sitemap.xml (123KB) and robots.txt
- **Quality:** Template-generated. Same structure per page, different city/service names swapped in. Basic but functional SEO pages.
- **Conversion potential:** ZERO while on surge.sh (free tier injects `Disallow: /` in robots.txt, blocking Google indexing entirely). Would need migration to Vercel/Cloudflare Pages to have any SEO value.

### Portfolio/Demo Pages (`builds/portfolio/`)

- `landing-page/index.html` - 2,003-line Flowstack SaaS demo (also deployed as flowstack-demo.surge.sh)
- `dashboard/index.html` - ShopMetrics analytics dashboard (44KB, also deployed as shopmetrics-dashboard.surge.sh)
- `chrome-ext/`, `discord-bot/`, `scraper/` - All EMPTY directories (0 files)
- **Quality:** The HTML files are well-designed visually. Professional dark themes with gradients. But purely static with fake/hardcoded data.

### LANDING/ directory

- **Empty.** Zero files. The directory exists but contains nothing.

---

## Tech Stack Summary

| Layer | Technology | Usage |
|-------|-----------|-------|
| Static sites | Plain HTML/CSS/JS | All deployed surge.sh sites, programmatic SEO pages, portfolio demos |
| PWA apps | HTML/JS + manifest.json + service worker | 6 apps (FocusLock, HabitForge, etc.) |
| Landing site (dev) | Next.js 16.1.3, React, Tailwind CSS, TypeScript | 07_LANDING/printmaxx-site (NOT deployed) |
| Legacy mobile app | Expo/React Native, TypeScript | app factory/scripture-streak (NOT deployed) |
| Build scripts | Python 3 | Dashboard generator, programmatic SEO generator |
| Charts/viz | Chart.js | Dashboard, pipeline visualizations |
| API integration | Google PageSpeed Insights API | SiteScore site-scorer (the one actually functional tool) |
| Hosting | surge.sh (free tier) | All deployments. $0 cost. SSL included. CDN. |
| iOS wrapping | Capacitor 7.5/8.x | Config files exist for 6 apps but no evidence of App Store submission |
| Automation | Python + Playwright + Claude CLI | Ralph loops, scrapers, lead pipeline (internal tooling) |
| Terminal app | macOS .app bundle (bash launcher) | Launches printmaxx_tui.py in Terminal.app |
| Cal AI project | Screenshots only | Old UI/UX mockups from Apr 2025. No code found in this directory. |

---

## PRINTMAXX Terminal.app Assessment

- A macOS .app bundle that launches `AUTOMATIONS/printmaxx_tui.py` in Terminal.app
- Just a bash script wrapper using osascript
- Version 3.0, bundle ID `com.printmaxx.terminal`
- Has a custom AppIcon.icns (102KB)
- Not a real application - convenience launcher for the TUI dashboard
- Not deployable/distributable to others

---

## Critical Gaps

1. **ZERO revenue infrastructure.** No Stripe, no RevenueCat, no payment forms, no checkout pages across ANY deployed site. The 14 live sites cannot accept money.

2. **Surge.sh SEO blocker.** Free tier injects `Disallow: /` in robots.txt. All 602 programmatic SEO pages are invisible to Google. The entire SEO strategy is blocked until migration to Vercel/Cloudflare Pages.

3. **No backends.** Every deployed site is pure static HTML. No databases, no user accounts, no data persistence beyond browser localStorage. The PWA apps lose all data if the browser is cleared.

4. **2 sites currently 404.** printmaxx-demos.surge.sh and printmaxx-local-demos.surge.sh are returning 404, despite being listed as core demo assets for cold outreach.

5. **App quality is low.** Portfolio average 42.7/100 per the project's own audit. Single-file monoliths, hover states on mobile apps, no native plugins actually working, no monetization.

6. **Inflated site counts.** The deploy log claims "20 SITES PERMANENTLY DEPLOYED" but actual verification shows 14 returning 200, 2 returning 404, and several referenced URLs that may or may not be distinct deployments (individual motion template pages are sub-pages, not separate sites).

7. **No App Store presence.** Despite iOS wrapping infrastructure (Capacitor configs, Podfiles), zero apps have been submitted to the App Store. No Apple Developer account confirmed.

8. **Next.js site never deployed.** The most complete frontend project (07_LANDING/printmaxx-site) with proper routing, components, and content structure has never been deployed to a public URL.

9. **Empty portfolio directories.** `builds/portfolio/chrome-ext/`, `discord-bot/`, `scraper/` are empty folders - planned but never built.

10. **Cal AI is screenshots only.** The `cal ai/` directory contains 35 PNG screenshots from Apr 2025 and a UI/UX subfolder with 6 more screenshots. No code, no app, no build artifacts.

---

## Strengths

1. **14 sites actually live and serving 200 OK.** This is non-trivial. The deployment pipeline works and sites are reachable worldwide via CDN with SSL.

2. **SiteScore (site-scorer) is genuinely functional.** It calls the Google PageSpeed Insights API and returns real analysis. This is the one deployed tool that does something real for a visitor.

3. **Programmatic SEO at scale.** 602 properly structured HTML pages with sitemap.xml is real work. If moved to an indexable host, these could drive organic traffic.

4. **$0 infrastructure cost.** Everything runs on surge.sh free tier. No monthly burn. Smart for bootstrapping.

5. **Solid internal tooling.** The Ralph loop system, lead pipeline (2.87M leads qualified, 30K+ analyzed), cold email generator, and automation scripts represent significant engineering. The backend/scraping code quality (8.5/10 per rigor audit) far exceeds the customer-facing assets (5.5/10).

6. **Comprehensive deployment documentation.** DEPLOY_LOG.md has exact redeploy commands, teardown commands, and deployment history. Any agent can redeploy in seconds.

7. **600 personalized demos generated.** `output/personalized_demos/` contains 601 generated demo pages mapped to real business leads. These could be powerful cold outreach assets if deployed.

8. **Well-structured build pipeline.** Python generators (generate_dashboard.py, programmatic_seo.py, personalize_demos.py) can regenerate all static sites from data. Reproducible builds.

---

## Verdict

The project has 14 live sites but they are almost entirely static HTML with no functionality beyond what you see when you load the page. Only 1 (SiteScore) does something genuinely useful for a visitor. The rest are portfolio demos with hardcoded data, minimal PWAs with no backend, or template-generated SEO pages that Google cannot index.

The total revenue-generating capability of all deployed assets combined is $0. There is no payment integration, no App Store presence, no product for sale, and no way for any visitor to give money to PRINTMAXX through any of these sites.

The real value is in the internal automation tooling (scraper pipeline, lead qualifier, cold email generator, Ralph loop system) and the 602 SEO pages waiting for an indexable host. The gap between "infrastructure built" and "revenue generated" is the project's defining characteristic.
