# PLAYWRIGHT TESTER REPORT
**Test Date:** 2026-04-01 04:41:30
**Total Sites Tested:** 48

## Summary
| Status | Count | % |
|--------|-------|----|
| 🟢 GREEN (HTTP 200) | 40 | 83.3% |
| 🟡 YELLOW (redirects) | 0 | 0.0% |
| 🔴 RED (failures) | 8 | 16.7% |
| ⏱ TIMEOUT | 0 | 0.0% |

**Pass Rate: 83.3%**

## ✓ GREEN (40 sites)
- ai-stack-2026.surge.sh
- best-ai-tools-2026.surge.sh
- best-blood-pressure-supplement-men-over-55.surge.sh
- best-memory-supplement-men-over-60.surge.sh
- best-testosterone-booster-men-over-50.surge.sh
- buddhist-streak.surge.sh
- claude-code-agent-bible.surge.sh
- cnsnt-web.surge.sh
- cold-email-roi-calculator.surge.sh
- coldmaxx-vs-instantly.surge.sh
- coldmaxx.surge.sh
- fnsmdehip-research.surge.sh
- focuslock-vs-opal.surge.sh
- focuslock-web.surge.sh
- hilal-landing.surge.sh
- invoiceforge.surge.sh
- mcp-marketplace.surge.sh
- n8n-vs-zapier-vs-make.surge.sh
- nutriai.surge.sh
- pagescorer.surge.sh
- prayerlock-vs-hallow.surge.sh
- prayerlock-web.surge.sh
- printmaxx-apps.surge.sh
- printmaxx-site.surge.sh
- printmaxx-store.surge.sh
- printmaxx.surge.sh
- quran-streak.surge.sh
- ramadan-daily-planner.surge.sh
- ramadan-tracker.surge.sh
- revenue-leak-audit.surge.sh
- roicalc.surge.sh
- saas-stack-audit.surge.sh
- scripture-streak.surge.sh
- sleepmaxx-landing.surge.sh
- sleepmaxx-vs-sleepcycle.surge.sh
- smartlead-vs-instantly.surge.sh
- stackmaxx.surge.sh
- subject-line-grader.surge.sh
- tasksmash-web.surge.sh
- walktounlock-landing.surge.sh

## ✗ RED (8 sites)
- focuslock-landing.surge.sh
- mealmaxx-web.surge.sh
- mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh
- prayerlock-landing.surge.sh
- sikh-streak.surge.sh
- top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh
- torah-streak.surge.sh
- window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh

## Root Causes
- **DNS Failures (HTTP 000):** Surge.sh has 63-char DNS label limit. Sites with subdomains >63 chars fail.
- **Redirects (3xx):** Surge caching or redirect rules.
- **Timeouts:** Rare; likely network intermittency or heavy JS load.

## Recommendations
1. Rename overly-long subdomains to fit <63 chars (use abbreviations or remove redundant words)
2. Test loading performance on large JS-heavy sites
3. Monitor favicon 404s (minor, non-blocking)
