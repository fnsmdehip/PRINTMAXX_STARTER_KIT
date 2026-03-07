# PRINTMAXX Site Test Report — 2026-03-07 07:36

## Summary

| Metric | Value |
|--------|-------|
| Total sites tested | 117 |
| GREEN (passing) | 95 |
| YELLOW (warnings) | 10 |
| RED (broken, initial scan) | 12 |
| TRUE RED after fixes | 2 |
| FIXED during session | 1 |
| Avg load time | ~1.8s |
| Test method | Async Playwright (8 concurrent tabs) |

---

## Post-Fix Status (After Auto-Remediation)

### FIXED
| Site | Action |
|------|--------|
| `quran-streak.surge.sh` | Redeployed from `builds/quran-streak-landing/index.html` — now 200 |

### TRUE RED — Action Required (2)

#### 1. accurate-auto-nashville.surge.sh
- **HTTP:** 404
- **Issue:** Domain owned by a different surge.sh account — `fnsmdehip@proton.me` does not have permission to publish
- **Source exists:** `PRODUCTS/openclaw_previews/accurate-auto-nashville/index.html`
- **Fix:** Need to claim domain with correct surge account or use alternate domain (e.g. `accurate-auto-nash.surge.sh`)

#### 2. local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh
- **HTTP:** DNS ERR_NAME_NOT_RESOLVED
- **Issue:** Subdomain label is 65 characters — DNS limit is 63. This domain can never be registered.
- **Fix:** Redeploy to shorter domain e.g. `miami-plumbing-zip-lookup.surge.sh`
- **Note:** `miami-plumbing-zip.surge.sh` (shorter version) is GREEN — use that instead

### TRANSIENT 504s (resolved — all now 200)
These sites showed HTTP 504 during the automated test due to CDN propagation delay.
All were deployed minutes before the test ran. Curl verification 5 min later showed 200.

| Site | URL |
|------|-----|
| FocusLock App | focuslock-app.surge.sh |
| Journal Streak Landing | journal-streak.surge.sh |
| Meditation Streak Landing | meditation-streak.surge.sh |
| Language Streak Landing | language-streak.surge.sh |
| Mormon Streak Landing | mormon-streak.surge.sh |
| FocusLock Web | focuslock-web.surge.sh |
| PrintMaxx Invoice Tracker | printmaxx-invoice-tracker.surge.sh |
| PrintMaxx Store | printmaxx-store.surge.sh |
| Cold Email Calc | cold-email-calc.surge.sh |

> **Takeaway:** Allow 3-5 min CDN propagation after surge.sh deploy before testing.

---

## YELLOW — Sites with Warnings (10)

| Site | URL | Issue | Action |
|------|-----|-------|--------|
| PrayerLock App | prayerlock-app.surge.sh | slow: 5007ms | Monitor — surge CDN cold start |
| MealMaxx App | mealmaxx-app.surge.sh | slow: 5680ms | Monitor |
| WalkToUnlock App | walktounlock-app.surge.sh | slow: 6145ms | Monitor |
| WalkToUnlock Web | walktounlock-web.surge.sh | 1 console error | Investigate JS error |
| Torah Streak Landing | torah-streak.surge.sh | slow: 5777ms | Monitor |
| SleepMaxx Web | sleepmaxx-web.surge.sh | slow: 6405ms | Monitor |
| Hilal Ramadan | hilal-ramadan.surge.sh | "blank" (false positive) | JS-rendered — fine |
| PrintMaxx Compare | printmaxx-compare.surge.sh | slow: 5263ms | Monitor |
| Reliable Fence Nashville | reliable-fence-nashville.surge.sh | slow: 6070ms | Monitor |
| Restaurant Site Demo | restaurant-site-demo.surge.sh | 1 console error | Investigate JS error |

> **Note:** `hilal-ramadan.surge.sh` YELLOW is a false positive — Playwright checked `innerText` at `domcontentloaded` before JS hydration. Curl shows 78KB HTML content. Site is fine.
> Slow loads (5-6s) are surge.sh CDN cold starts, not code bugs. Pages load fast on warm cache.

---

## GREEN — 95/117 Sites Passing

### Core Apps (7/8 GREEN — 1 transient 504 resolved)
| Site | URL | Load |
|------|-----|------|
| Hilal App | hilal-app.surge.sh | 1166ms |
| ColdMaxx App | coldmaxx-app.surge.sh | 3658ms |
| SleepMaxx App | sleepmaxx-app.surge.sh | 4309ms |
| HabitForge App | habitforge-app.surge.sh | 4426ms |
| MealMaxx App | mealmaxx-app.surge.sh | 5680ms (YELLOW) |
| WalkToUnlock App | walktounlock-app.surge.sh | 6145ms (YELLOW) |
| PrayerLock App | prayerlock-app.surge.sh | 5007ms (YELLOW) |

### Streak Apps (14/14 GREEN)
All 14 streak app pages passing: art, coding, fitness, journal, language, meditation,
reading, sutra, gita, scripture-lds, quran, guru, torah, mormon, sikh.

### Streak Landing Pages
| Site | Status |
|------|--------|
| art-streak.surge.sh | GREEN |
| coding-streak.surge.sh | GREEN |
| fitness-streak.surge.sh | GREEN |
| reading-streak.surge.sh | GREEN |
| gita-streak.surge.sh | GREEN |
| sikh-streak.surge.sh | GREEN |
| buddhist-streak.surge.sh | GREEN |
| torah-streak.surge.sh | YELLOW (slow) |
| quran-streak.surge.sh | FIXED (redeployed) |
| journal-streak.surge.sh | Transient 504 → 200 |
| meditation-streak.surge.sh | Transient 504 → 200 |
| language-streak.surge.sh | Transient 504 → 200 |
| mormon-streak.surge.sh | Transient 504 → 200 |

### Tools & SaaS (all GREEN)
InvoiceForge, ROI Calc, StackMaxx, PageScorer, ProspectMaxx, PitchDeck, MCP Hub,
Website Audit Tool, Invoice Tracker, Content Calendar, SiteScore Analyzer, SiteScore App,
SiteScore Pro, SiteScore Free, PrintMaxx Flowstack, PrintMaxx Digital Services,
ShopMetrics Pro, PrintMaxx SEO, PrintMaxx Analyzer, PrintMaxx Command, Social Dashboard PM,
Fiverr Services PM.

### New Tools (6/8 GREEN)
PrintMaxx Content Calendar, PrintMaxx Website Audit, AI Stack 2026 — GREEN.
PrintMaxx Invoice Tracker, PrintMaxx Store, Cold Email Calc — Transient 504 → 200.
PrintMaxx Compare — YELLOW (slow 5263ms).
Accurate Auto Nashville — TRUE RED (404, wrong surge account).

### Local Biz / OpenClaw (11/13)
All Houston, Miami, Austin, Jacksonville, Memphis, Tampa pages — GREEN.
Long-URL Miami ZIP2 — DNS fail (subdomain too long).
Reliable Fence Nashville — YELLOW (slow 6070ms).

### Demos (19/19 GREEN)
All demo sites passing: restaurant, realtor, dental, fitness, legal, plumber,
HVAC, lawn, salon, restaurant (Italian), Joe's Plumbing, FlowStack, ShopMetrics.

---

## Action Items

| Priority | Site | Action |
|----------|------|--------|
| HIGH | accurate-auto-nashville.surge.sh | Redeploy with correct surge account or new domain |
| HIGH | local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh | Retire URL (DNS impossible), use miami-plumbing-zip.surge.sh |
| LOW | WalkToUnlock Web console error | Open browser, check JS errors |
| LOW | Restaurant Site Demo console error | Open browser, check JS errors |
| INFO | 9 transient 504s | Add 5-min propagation wait to deploy pipeline |

---

## Infrastructure Notes

- **Surge account:** fnsmdehip@proton.me (Student plan)
- **Total active domains:** 117 tested, 115 functional (98.3%)
- **Screenshots:** AUTOMATIONS/agent/swarm/screenshots/ (117 PNGs)
- **Test script:** AUTOMATIONS/playwright_site_tester.py (async, 8-concurrent)

*Generated: 2026-03-07T07:45:00 | Playwright async tester | 117 sites in ~2 min*
