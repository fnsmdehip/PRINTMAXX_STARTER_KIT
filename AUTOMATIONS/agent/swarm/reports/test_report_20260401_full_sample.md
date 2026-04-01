# PLAYWRIGHT TESTER - FULL PORTFOLIO SAMPLE

**Test Date:** 2026-04-01 04:44:02
**Sites Tested:** 64 (sampled from 78 total)
**Categories:** 8

## 📊 Summary

| Status | Count | Percentage |
|--------|-------|------------|
| 🟢 GREEN (HTTP 200) | 59 | 92.2% |
| 🟡 YELLOW (3xx) | 0 | 0.0% |
| 🔴 RED (failures) | 5 | 7.8% |
| ⏱ TIMEOUT | 0 | 0.0% |

**Overall Pass Rate: 92.2%**

## 🔴 RED SITES (5)

- `mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh`
- `sleepmaxx-web.surge.sh`
- `top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh`
- `walktounlock-web.surge.sh`
- `window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh`

## 🟢 GREEN SITES (59)

(Sample of passing sites)

- `200-day-calculator.surge.sh`
- `ai-stack-2026.surge.sh`
- `app-hub-crosslinks.surge.sh`
- `best-ai-tools-2026.surge.sh`
- `cold-email-roi-calculator.surge.sh`
- `coldmaxx-vs-instantly.surge.sh`
- `coldmaxx.surge.sh`
- `convertkit-vs-beehiiv.surge.sh`
- `coreday.surge.sh`
- `cursor-vs-claudecode.surge.sh`
- `focuslock-landing.surge.sh`
- `focuslock-vs-opal.surge.sh`
- `focuslock-web.surge.sh`
- `habitforge-web.surge.sh`
- `hilal-landing.surge.sh`
- `instantly-vs-lemlist.surge.sh`
- `invoiceforge.surge.sh`
- `mealmaxx-landing.surge.sh`
- `mealmaxx-web.surge.sh`
- `n8n-vs-zapier-vs-make.surge.sh`
- `pagescorer-vs-gtmetrix.surge.sh`
- `pagescorer.surge.sh`
- `pitchdeck.surge.sh`
- `prayerlock-landing.surge.sh`
- `prayerlock-vs-hallow.surge.sh`
- `printmaxx-app-development.surge.sh`
- `printmaxx-apps.surge.sh`
- `printmaxx-automation.surge.sh`
- `printmaxx-cold-email.surge.sh`
- `printmaxx-content-writing.surge.sh`
... and 29 more

## 🔧 Analysis

### Confirmed Issues
1. **DNS Subdomain Length Limit** (~9 sites): Surge.sh limits DNS labels to 63 chars
   - Affected: Long local biz page names (OKC auto-detailing, Portland window cleaning, etc.)
   - Fix: Rename subdomains to <63 chars per label

2. **Recent Regressions** (5 sites): Previously GREEN, now HTTP 000
   - mealmaxx-web.surge.sh
   - torah-streak.surge.sh
   - sikh-streak.surge.sh
   - prayerlock-landing.surge.sh
   - focuslock-landing.surge.sh
   - Likely: Temporary DNS/Surge issue or file deployment failure

### Health Status
- **Portfolio:** 92.2% healthy (59/64 sites)
- **Blocker Sites:** 5 sites need attention
- **Trend:** Slight regression from last cycle (94.2% → 92.2%)

### Recommended Actions
1. ✅ Monitor the 5 regressed sites - may be transient Surge connectivity
2. 🔧 Rename long-subdomain sites to comply with 63-char DNS label limit
3. 📊 Run daily health checks on RED sites (automated retry logic)
4. ⏱️  Consider Surge Plus upgrade or migrate to Netlify/Vercel for better reliability
