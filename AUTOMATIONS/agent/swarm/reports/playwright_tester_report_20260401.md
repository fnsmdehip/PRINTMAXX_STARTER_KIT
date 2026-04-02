# Playwright Tester Report — April 1, 2026

**Test Date:** 2026-04-01 20:51:30  
**Sites Tested:** 33  
**Pass Rate:** 54.5% (18 GREEN, 6 YELLOW, 9 RED)  
**Avg Load Time:** 4,995ms

---

## Executive Summary

Health check on 33 surge.sh deployments shows **72.7% operational** (18 GREEN + 6 YELLOW). Nine sites completely broken due to:
- **8 DNS resolution failures** — domain names exceed 63-character DNS limit
- **1 blank page** — HTTP 200 but empty content

### Status Breakdown

| Status | Count | % | Issue |
|--------|-------|---|-------|
| GREEN | 18 | 54.5% | Working, <5s load time |
| YELLOW | 6 | 18.2% | Working, but slow (6-8s load) |
| RED | 9 | 27.3% | DNS failures or blank pages |

---

## GREEN Sites (18) ✅

All sites working perfectly, proper rendering, <5s load time.

**Streak landing pages:**
- pentecostal-streak-landing (4,278ms) ✅
- baptist-streak-landing (4,200ms) ✅
- scripture-streak-landing (3,938ms) ✅
- quran-streak-landing (4,077ms) ✅
- torah-streak-landing (4,057ms) ✅

**Brand & Education:**
- printmaxx-site (4,138ms) ✅
- printmaxx (4,135ms) ✅
- claude-code-agent-bible (4,251ms) ✅

**Tools & Calculators:**
- invoiceforge (4,267ms) ✅
- pagescorer (3,858ms) ✅
- roicalc (3,852ms) ✅
- cold-email-roi-calculator (4,096ms) ✅

**Checklists & Audits:**
- solopreneur-launch-checklist (4,139ms) ✅
- revenue-leak-audit (4,406ms) ✅

**Comparison Pages:**
- n8n-vs-zapier-vs-make (4,473ms) ✅
- cursor-vs-claudecode (4,344ms) ✅
- prayerlock-vs-hallow (4,062ms) ✅

**Other:**
- ramadan-tracker (4,681ms) ✅

---

## YELLOW Sites (6) ⚠️

All working but slow (>6s load time). Render correctly but need performance optimization.

| Site | Load Time | Status | Issue |
|------|-----------|--------|-------|
| prayerlock-web | 7,443ms | 200 | PWA slow load |
| focuslock-web | 7,422ms | 200 | PWA slow load |
| sleepmaxx-web | 6,846ms | 200 | PWA slow load |
| coldmaxx | 6,838ms | 200 | Tool app slow |
| handyman-service-in-dallas-tx | 8,653ms | 200 | Local biz page |
| atlanta-electricians | 8,340ms | 200 | Local biz page |

**Performance Target:** <5s load time (Web Vitals)  
**Recommendation:** Profile & optimize (lazy load, code split, compress assets)

---

## RED Sites (9) ❌

### Type 1: DNS Resolution Failures (8 sites)

**Error:** `net::ERR_NAME_NOT_RESOLVED`

**Root Cause:** Domain names exceed 63-character DNS limit (industry standard). Surge.sh enforces this.

| Domain | Length | Issue |
|--------|--------|-------|
| mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok | 89 | TOO LONG |
| top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok | 80 | TOO LONG |
| window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or | 71 | TOO LONG |
| mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham-al | 77 | TOO LONG |
| home-professional-mobile-detailing-amp-products-super-store-birmingham-al | 77 | TOO LONG |
| the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv | 77 | TOO LONG |
| local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky | 71 | TOO LONG |
| miami-pest-control-experts-reliable-extermination-services-miami-fl | 70 | TOO LONG |

**Fix:** Shorten to <63 chars, redeploy, update links:
```
OLD: mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh
NEW: mobile-detailing-okc-champion.surge.sh (38 chars)
```

### Type 2: Blank Page (1 site)

**saas-stack-audit-200**
- HTTP: 200 ✓
- Page height: 0px ✗
- No console errors
- Empty content

**Fix:** Check source file exists and has content, redeploy

---

## Performance Insights

- **Best performers:** pagescorer, roicalc, prayerlock-vs-hallow (3.8-4.0s)
- **Average:** Most sites 4-4.5s
- **Slow:** PWA apps and local biz pages (6-8s+)
- **Optimization opportunity:** ~600ms margin to target <5s

---

## Action Items

### P0 (Critical)
1. Shorten 8 DNS-broken domains to <63 chars
2. Investigate saas-stack-audit-200 blank page

### P1 (Performance)
3. Profile & optimize 6 YELLOW sites

### P2 (Prevention)
4. Add domain length validation to deployment pipeline

---

## Test Coverage

- **Tested:** 33 sites (11 brand/tool, 6 PWA, 8 comparison/lead magnet, 8+ local biz)
- **Screenshots:** 30 captured
- **Concurrent:** 5 browsers max
- **Timeout:** 15s per page
- **Viewport:** 1280x720
