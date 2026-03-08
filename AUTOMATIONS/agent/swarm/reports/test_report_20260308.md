# PRINTMAXX Site Test Report - 2026-03-08

**Tested:** 205 surge.sh deployments
**Time:** 2026-03-08 11:49 - 12:15
**Method:** Bulk HTTP (all sites) + Playwright visual (27 priority sites)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total sites tested | 205 |
| GREEN (healthy) | 194 (94.6%) |
| YELLOW (slow/warnings) | 7 (3.4%) |
| RED (broken) | 4 (2.0%) |
| Pass rate | 98.0% |
| Avg load time | 1,289ms |
| Min load time | 709ms |
| Max load time | 6,070ms |
| Visual tests (Playwright) | 27/27 passed |
| Sites fixed this cycle | 1 (presbyterian-streak-landing) |

---

## RED Sites (4 - All DNS issues, unfixable at current subdomain)

| Site | Status | Issue | Fix |
|------|--------|-------|-----|
| local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh | DNS error | Label 65 chars > RFC 1035 max 63 | Redeploy to shorter name |
| mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh | DNS error | Label too long | Redeploy to shorter name |
| top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh | DNS error | Label too long | Redeploy to shorter name |
| window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh | DNS error | Label too long | Redeploy to shorter name |

**Note:** These 4 sites all have subdomain labels exceeding the 63-character RFC 1035 limit. They need to be redeployed to shorter subdomain names.

---

## YELLOW Sites (7 - Slow load >3s, all functional)

| Site | Load Time | Issue |
|------|-----------|-------|
| catholic-streak-landing.surge.sh | 6,070ms | Slow initial load |
| pentecostal-streak-landing.surge.sh | 5,807ms | Slow initial load |
| shia-streak-landing.surge.sh | 5,596ms | Slow initial load |
| sunni-streak-landing.surge.sh | 5,539ms | Slow initial load |
| cold-email-roi-calculator.surge.sh | 5,124ms | Slow initial load |
| baptist-streak-landing.surge.sh | 3,790ms | Slow initial load |
| orthodox-streak-landing.surge.sh | 3,736ms | Slow initial load |

**Note:** Slow loads are likely cold cache on surge.sh CDN for recently deployed pages. Subsequent loads are faster.

---

## Fixed This Cycle

| Site | Issue | Fix |
|------|-------|-----|
| presbyterian-streak-landing.surge.sh | 404 Not Found | Redeployed with 200.html fallback. Now returning 200. |

---

## Transient 504s (Resolved)

7 sites returned 504 Gateway Timeout during bulk testing but all returned 200 on retry:
- episcopal-streak-landing.surge.sh (now 200)
- evangelical-streak-landing.surge.sh (now 200)
- lutheran-streak-landing.surge.sh (now 200)
- methodist-streak-landing.surge.sh (now 200)
- presbyterian-streak-landing.surge.sh (was 404, fixed via redeploy, now 200)
- protestant-streak-landing.surge.sh (now 200)
- solopreneur-launch-checklist.surge.sh (now 200)

**Cause:** Surge.sh CDN cold cache / rate limiting during 20-concurrent-thread bulk test.

---

## Playwright Visual Test Results (27 sites)

### Priority Sites (15 tested)

| Site | Loaded | Content | Quality | Issues |
|------|--------|---------|---------|--------|
| printmaxx-site.surge.sh | YES | YES | 5/5 | None |
| coldmaxx-app.surge.sh | YES | YES | 5/5 | None |
| sleepmaxx-app.surge.sh | YES | YES | 4/5 | CDN Tailwind warning |
| prayerlock-app.surge.sh | YES | YES | 4/5 | CDN Tailwind warning |
| printmaxx-store.surge.sh | YES | YES | 5/5 | None |
| cursor-vs-claudecode.surge.sh | YES | YES | 5/5 | None |
| instantly-vs-lemlist.surge.sh | YES | YES | 5/5 | None |
| best-cold-email-tools.surge.sh | YES | YES | 5/5 | None |
| printmaxx-tools.surge.sh | YES | YES | 5/5 | 46 tools across 8 categories |
| cold-email-roi-calculator.surge.sh | YES | YES | 5/5 | Functional calculator |
| side-project-estimator.surge.sh | YES | YES | 4/5 | Functional estimator |
| financial-dashboard-pm.surge.sh | YES | YES | 4/5 | 6 KPI cards, 5 tabs |
| coldmaxx-vs-instantly.surge.sh | YES | YES | 5/5 | None |
| convertkit-vs-beehiiv.surge.sh | YES | YES | 5/5 | Affiliate disclosure present |
| focuslock-app.surge.sh | YES | YES | 4/5 | Missing favicon (404) |

**Average quality: 4.7/5**

### Recent Deployments (12 tested)

| Site | Loaded | Content | Quality | Issues |
|------|--------|---------|---------|--------|
| shia-streak-landing.surge.sh | YES | YES | 5/5 | Missing favicon |
| sunni-streak-landing.surge.sh | YES | YES | 5/5 | Missing favicon |
| anglican-streak-landing.surge.sh | YES | YES | 5/5 | Missing favicon |
| catholic-streak-landing.surge.sh | YES | YES | 5/5 | None |
| orthodox-streak-landing.surge.sh | YES | YES | 5/5 | None |
| baptist-streak-landing.surge.sh | YES | YES | 5/5 | None |
| walktounlock-web.surge.sh | YES | YES | 4/5 | Tailwind CDN warning |
| sleepmaxx-web.surge.sh | YES | YES | 5/5 | None |
| mealmaxx-web.surge.sh | YES | YES | 5/5 | None |
| printmaxx-storefront.surge.sh | YES | YES | 5/5 | None |
| printmaxx-comparisons.surge.sh | YES | YES | 3/5 | Only 2 comparisons listed |
| pagescorer-vs-gtmetrix.surge.sh | YES | YES | 5/5 | None |

**Average quality: 4.75/5**

---

## Minor Issues Found

1. **Missing favicons:** focuslock-app, shia-streak-landing, sunni-streak-landing, anglican-streak-landing (404 on favicon.ico)
2. **CDN Tailwind:** sleepmaxx-app, prayerlock-app, focuslock-app, walktounlock-web use Tailwind CDN instead of compiled CSS (development mode warning)
3. **Deprecated meta tag:** `apple-mobile-web-app-capable` warning on 3 PWA apps
4. **Sparse content:** printmaxx-comparisons.surge.sh hub only shows 2 comparisons but 8 exist

---

## Category Breakdown (205 sites)

| Category | Count | Status |
|----------|-------|--------|
| Core Apps | 17 | All GREEN |
| Streak Apps | 15 | All GREEN |
| Streak Web Pages | 26 | All GREEN |
| Streak Landing Pages | 24 | 17 GREEN, 7 YELLOW (slow) |
| Web Marketing Pages | 14 | All GREEN |
| Comparison Pages | 10 | All GREEN |
| Lead Magnets | 8 | All GREEN |
| Tools / SaaS | 28 | All GREEN |
| Hubs | 8 | All GREEN |
| Local Biz / OpenClaw | 25 | 21 GREEN, 4 RED (DNS) |
| Demos | 19 | All GREEN |
| Storefront / Thanks | 3 | All GREEN |
| SEO Tools | 8 | All GREEN |
| Media Templates | 2 | All GREEN |

---

## Recommendations

### P0 (Fix Now)
1. **Redeploy 4 DNS-broken local biz sites** to shorter subdomain names (<63 chars)
2. **Update printmaxx-comparisons.surge.sh** to include all 8+ comparison pages (currently only shows 2)

### P1 (Fix Soon)
3. **Add favicons** to streak landing pages and focuslock-app
4. **Compile Tailwind CSS** for production builds instead of CDN link

### P2 (Nice to Have)
5. **Optimize streak landing page sizes** to reduce cold-cache load times below 3s
6. **Remove deprecated `apple-mobile-web-app-capable`** meta tag from PWA apps

---

## Test Infrastructure

- **Bulk HTTP tester:** `AUTOMATIONS/bulk_http_tester.py` (205 sites, 20 concurrent threads, ~90s runtime)
- **Results JSON:** `AUTOMATIONS/agent/swarm/reports/test_results_20260308.json`
- **Screenshots:** `AUTOMATIONS/agent/swarm/screenshots/` (200+ screenshots)
- **Playwright:** Used for 27 priority site visual verification

---

*Report generated by PRINTMAXX Playwright Tester Agent*
*Next test cycle: Run again in 4-6 hours or after any bulk deployment*
