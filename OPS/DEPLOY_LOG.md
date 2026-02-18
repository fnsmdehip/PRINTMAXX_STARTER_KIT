# DEPLOY LOG - 2026-02-12

## Status: 20 SITES PERMANENTLY DEPLOYED ON SURGE.SH

All deployed with $0 cost via surge.sh (account: fnsmdehip@proton.me).
HTTPS + global CDN (10 edge locations) included free.

---

## PERMANENT LIVE URLs (surge.sh - always online)

### Ramadan Tracker (URGENT - Ramadan starts Feb 28!)
| Item | Value |
|------|-------|
| **URL** | **https://hilal-ramadan.surge.sh** |
| **Platform** | surge.sh (permanent, CDN-backed) |
| **Source** | `ralph/loops/app_factory/output/ramadan-tracker/` |
| **App Name** | Hilal - Ramadan Companion |
| **Features** | Bilingual EN/AR, RTL support, prayer times, fasting tracker, Quran progress, PWA installable |
| **Size** | 138 files, 3.6 MB |
| **Verified** | 200 OK |

### Programmatic SEO Site (601 pages)
| Item | Value |
|------|-------|
| **URL** | **https://printmaxx-seo.surge.sh** |
| **Platform** | surge.sh (permanent, CDN-backed) |
| **Source** | `builds/programmatic_seo/` |
| **Pages** | 601 HTML pages across 12 service categories x 50 cities |
| **Total Size** | 602 files, 6.6 MB |
| **Has Sitemap** | Yes - `https://printmaxx-seo.surge.sh/sitemap.xml` |
| **Categories** | branding, content-writing, e-commerce-development, email-marketing, google-ads-management, local-seo, logo-design, seo-services, social-media-management, video-production, web-design, website-maintenance |
| **Verified** | 200 OK |

### PWA Apps (5)
| App | URL | Files | Size | Verified |
|-----|-----|-------|------|----------|
| FocusLock | **https://focuslock-app.surge.sh** | 76 | 655.6 KB | 200 OK |
| HabitForge | **https://habitforge-app.surge.sh** | 76 | 671.6 KB | 200 OK |
| SleepMaxx | **https://sleepmaxx-app.surge.sh** | 6 | 50.8 KB | 200 OK |
| WalkToUnlock | **https://walktounlock-app.surge.sh** | 6 | 48.9 KB | 200 OK |
| MealMaxx | **https://mealmaxx-app.surge.sh** | 6 | 52.1 KB | 200 OK |

### Local Biz Motion Templates (demos for cold outreach)
| Template | URL | Verified |
|----------|-----|----------|
| Dental | **https://printmaxx-demos.surge.sh/dental_motion.html** | 200 OK |
| Restaurant | **https://printmaxx-demos.surge.sh/restaurant_motion.html** | 200 OK |
| Realtor | **https://printmaxx-demos.surge.sh/realtor_motion.html** | 200 OK |

### Portfolio Pieces (for freelance proposals + client demos)
| Asset | URL | Verified |
|-------|-----|----------|
| SiteScore SaaS (website analyzer) | **https://sitescore-app.surge.sh** | 200 OK |
| SiteScore Competitor Analyzer (SEO reports) | **https://sitescore-analyzer.surge.sh** | 200 OK |
| ShopMetrics Dashboard (analytics) | **https://shopmetrics-dashboard.surge.sh** | 200 OK |
| Flowstack Landing Page (SaaS demo) | **https://flowstack-demo.surge.sh** | 200 OK |

---

## Deployment Infrastructure

### surge.sh Details
- **Account:** fnsmdehip@proton.me (Student plan, free)
- **SSL:** Wildcard certificate valid 113 more days
- **CDN:** 10 edge locations worldwide (SFO, LHR, YYZ, JFK, AMS, FRA, SGP, BLR, SYD, NRT)
- **Cost:** $0
- **Persistence:** Permanent until manually torn down

### Redeploy Commands
```bash
# Ramadan Tracker
cd ralph/loops/app_factory/output/ramadan-tracker && npx surge . hilal-ramadan.surge.sh

# Programmatic SEO
cd builds/programmatic_seo && npx surge . printmaxx-seo.surge.sh

# PWA Apps
cd ralph/loops/app_factory/output/focuslock-web && npx surge . focuslock-app.surge.sh
cd ralph/loops/app_factory/output/habitforge-web && npx surge . habitforge-app.surge.sh
cd ralph/loops/app_factory/output/sleepmaxx-web && npx surge . sleepmaxx-app.surge.sh
cd ralph/loops/app_factory/output/walktounlock-web && npx surge . walktounlock-app.surge.sh
cd ralph/loops/app_factory/output/mealmaxx-web && npx surge . mealmaxx-app.surge.sh

# Motion Templates
cd MONEY_METHODS/LOCAL_BIZ/motion_templates && npx surge . printmaxx-demos.surge.sh

# SEO Competitor Analyzer
cd builds/seo-analyzer-web && npx surge . sitescore-analyzer.surge.sh
```

### Teardown Commands
```bash
npx surge teardown hilal-ramadan.surge.sh
npx surge teardown printmaxx-seo.surge.sh
npx surge teardown focuslock-app.surge.sh
npx surge teardown habitforge-app.surge.sh
npx surge teardown sleepmaxx-app.surge.sh
npx surge teardown walktounlock-app.surge.sh
npx surge teardown mealmaxx-app.surge.sh
npx surge teardown printmaxx-demos.surge.sh
```

---

## Deployed Asset Inventory

| Category | Count | Details |
|----------|-------|---------|
| PWA Apps | 6 | Hilal, HabitForge, FocusLock, SleepMaxx, WalkToUnlock, MealMaxx |
| SEO Pages | 601 | 12 services x 50 cities + index + sitemap |
| Portfolio Pieces | 4 | SiteScore, SiteScore Analyzer, ShopMetrics, Flowstack |
| Motion Demos | 3 | Dental, Restaurant, Realtor |
| **Total Pages Live** | **614+** | All permanent, CDN-backed, HTTPS |

---

## Deploy History

| Timestamp | Action | Sites | Method |
|-----------|--------|-------|--------|
| 2026-02-12 01:45 EST | Initial tunnel deploy | 10 sites | ngrok + localtunnel (temporary) |
| 2026-02-12 02:08 EST | Permanent surge deploy | 8 sites | surge.sh (permanent) |
| 2026-02-12 02:10 EST | Tunnels killed | - | `deploy_all_tunnels.sh stop` |
| 2026-02-13 01:51 EST | Redeployed motion demos | 1 site | surge.sh (printmaxx-demos was 404) |
| 2026-02-13 01:51 EST | Deployed SEO analyzer | 1 site | surge.sh (sitescore-analyzer.surge.sh) |

---

## SEO Status (2026-02-12)

### Completed
- robots.txt created with `Allow: /` and Sitemap directive
- apps.html link hub created with cross-links to all 6 PWAs, 3 demos, and SEO pages
- apps.html deployed and verified (200 OK): `https://printmaxx-seo.surge.sh/apps.html`
- IndexNow API submission: 202 Accepted (5 URLs submitted to Bing/Yandex/Seznam/Naver)
- All 5 PWAs already have full meta tags (description, og:title, og:description, twitter:card)

### Google/Bing Ping Results
- Google ping: **deprecated** (404, removed June 2023)
- Bing ping: **deprecated** (410 Gone)
- IndexNow API: **202 Accepted** (working alternative)

### BLOCKER: Surge.sh Free Tier Robots.txt
Surge free tier auto-injects `Disallow: /` in robots.txt. Our custom robots.txt is overridden.
This means Google will NOT index any surge.sh pages.

**Fix options (pick one):**
1. **Cloudflare Pages** (recommended for SEO) - `npx wrangler pages deploy .` allows custom robots.txt. Need `wrangler login`.
2. **Vercel** - `vercel deploy --prod` allows custom robots.txt. Need `vercel login`.
3. **Netlify** - `npx netlify-cli deploy --prod` allows custom robots.txt. Need `netlify login`.
4. **Surge Plus** ($13/mo) - Paid plan allows custom robots.txt.
5. **Custom domain on surge** - May allow robots.txt override (untested).

**For now:** Surge works for sharing PWA links, demo URLs in cold outreach, and direct traffic. Just not for SEO crawling.

### PWA Meta Tags (all verified present)
| App | description | og:title | og:description | twitter:card |
|-----|-------------|----------|----------------|--------------|
| Hilal (Ramadan) | YES | YES | YES | YES |
| Vault (FocusLock) | YES | YES | YES | YES |
| Streakr (HabitForge) | YES | YES | YES | YES |
| Dusk (SleepMaxx) | YES | YES | YES | YES |
| Steplock (WalkToUnlock) | YES | YES | YES | YES |
| Mise (MealMaxx) | YES | YES | YES | YES |

---

## Next Steps

1. **PRIORITY: Move SEO site to Cloudflare Pages or Vercel** to fix robots.txt blocker (surge blocks Google)
2. **Submit sitemap** to Google Search Console after moving to indexable host
3. **Share Ramadan tracker** on social media (16 days until Ramadan)
4. **Use motion demo URLs** in cold outreach emails to local businesses
5. **Share PWA links** for beta testing and feedback
6. **Custom domains** when ready ($10-15/year via Cloudflare Registrar)
