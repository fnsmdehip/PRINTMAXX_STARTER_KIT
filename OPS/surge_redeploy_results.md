# Surge Batch Redeploy Results

**Date:** 2026-03-07
**Surge account:** fnsmdehip@proton.me (Student)
**Total sites attempted:** 51
**Succeeded:** 27
**Failed (permission denied):** 22
**Skipped (no index.html):** 2

---

## SUCCEEDED (27 sites redeployed)

### LANDING/app-marketing-pages (26 sites)

| # | Directory | Domain | Status |
|---|-----------|--------|--------|
| 1 | LANDING/app-marketing-pages/ | printmaxx-apps.surge.sh | OK |
| 2 | LANDING/app-marketing-pages/ | printmaxx-site.surge.sh | OK |
| 3 | LANDING/app-marketing-pages/adhd-streak | adhd-streak.surge.sh | OK |
| 4 | LANDING/app-marketing-pages/ai-stack-2026 | ai-stack-2026.surge.sh | OK |
| 5 | LANDING/app-marketing-pages/anglican-streak | anglican-streak.surge.sh | OK |
| 6 | LANDING/app-marketing-pages/baptist-streak | baptist-streak.surge.sh | OK |
| 7 | LANDING/app-marketing-pages/catholic-streak | catholic-streak.surge.sh | OK |
| 8 | LANDING/app-marketing-pages/coldmaxx | coldmaxx.surge.sh | OK |
| 9 | LANDING/app-marketing-pages/convertkit-vs-beehiiv | convertkit-vs-beehiiv.surge.sh | OK |
| 10 | LANDING/app-marketing-pages/episcopal-streak | episcopal-streak.surge.sh | OK |
| 11 | LANDING/app-marketing-pages/evangelical-streak | evangelical-streak.surge.sh | OK |
| 12 | LANDING/app-marketing-pages/focuslock | focuslock-web.surge.sh | OK |
| 13 | LANDING/app-marketing-pages/hilal | hilal-app.surge.sh | OK |
| 14 | LANDING/app-marketing-pages/lutheran-streak | lutheran-streak.surge.sh | OK |
| 15 | LANDING/app-marketing-pages/mealmaxx | mealmaxx-web.surge.sh | OK |
| 16 | LANDING/app-marketing-pages/methodist-streak | methodist-streak.surge.sh | OK |
| 17 | LANDING/app-marketing-pages/orthodox-streak | orthodox-streak.surge.sh | OK |
| 18 | LANDING/app-marketing-pages/pentecostal-streak | pentecostal-streak.surge.sh | OK |
| 19 | LANDING/app-marketing-pages/prayerlock | prayerlock-web.surge.sh | OK |
| 20 | LANDING/app-marketing-pages/presbyterian-streak | presbyterian-streak.surge.sh | OK |
| 21 | LANDING/app-marketing-pages/protestant-streak | protestant-streak.surge.sh | OK |
| 22 | LANDING/app-marketing-pages/shia-streak | shia-streak.surge.sh | OK |
| 23 | LANDING/app-marketing-pages/sleepmaxx | sleepmaxx-web.surge.sh | OK |
| 24 | LANDING/app-marketing-pages/sunni-streak | sunni-streak.surge.sh | OK |
| 25 | LANDING/app-marketing-pages/thanks | printmaxx-thanks.surge.sh | OK |
| 26 | LANDING/app-marketing-pages/walktounlock | walktounlock-web.surge.sh | OK |

### LANDING/printmaxx-local-demos (1 site)

| # | Directory | Domain | Status |
|---|-----------|--------|--------|
| 27 | LANDING/printmaxx-local-demos/ | printmaxx-local-demos.surge.sh | OK |

---

## SUCCEEDED (from APP_FACTORY/builds, same account)

| # | Directory | Domain | Status |
|---|-----------|--------|--------|
| - | builds/art-streak-landing | art-streak-app.surge.sh | OK |
| - | builds/buddhist-streak-landing | sutra-streak-app.surge.sh | OK |

---

## FAILED - Permission Denied (22 sites)

These domains were originally deployed under a DIFFERENT surge account (not fnsmdehip@proton.me). The current account does not have publish permission.

### APP_FACTORY/builds - Streak Landing Pages (11 sites)

| # | Directory | Domain | Error |
|---|-----------|--------|-------|
| 1 | builds/coding-streak-landing | coding-streak-app.surge.sh | permission denied |
| 2 | builds/fitness-streak-landing | fitness-streak-app.surge.sh | permission denied |
| 3 | builds/gita-streak-landing | gita-streak-app.surge.sh | permission denied |
| 4 | builds/journal-streak-landing | journal-streak-app.surge.sh | permission denied |
| 5 | builds/language-streak-landing | language-streak-app.surge.sh | permission denied |
| 6 | builds/meditation-streak-landing | meditation-streak-app.surge.sh | permission denied |
| 7 | builds/mormon-streak-landing | scripture-streak-lds.surge.sh | permission denied |
| 8 | builds/quran-streak-landing | quran-streak-app.surge.sh | permission denied |
| 9 | builds/reading-streak-landing | reading-streak-app.surge.sh | permission denied |
| 10 | builds/sikh-streak-landing | guru-streak-app.surge.sh | permission denied |
| 11 | builds/torah-streak-landing | torah-streak-app.surge.sh | permission denied |

### APP_FACTORY/builds - Tools/Web Apps (11 sites)

| # | Directory | Domain | Error |
|---|-----------|--------|-------|
| 12 | builds/coldmaxx | coldmaxx.surge.sh | permission denied (LANDING version deployed OK) |
| 13 | builds/focuslock-web | focuslock.surge.sh | permission denied |
| 14 | builds/invoiceforge | invoiceforge.surge.sh | permission denied |
| 15 | builds/pagescorer | pagescorer.surge.sh | permission denied |
| 16 | builds/pitchdeck | pitchdeck.surge.sh | permission denied |
| 17 | builds/prayerlock-web | prayerlock.surge.sh | permission denied |
| 18 | builds/roicalc | roicalc.surge.sh | permission denied |
| 19 | builds/sleepmaxx-web | sleepmaxx.surge.sh | permission denied |
| 20 | builds/walktounlock-web | walktounlock.surge.sh | permission denied |
| 21 | builds/stackmaxx | stackmaxx.surge.sh | permission denied |
| 22 | builds/prospectmaxx | prospectmaxx.surge.sh | permission denied |

---

## SKIPPED (no index.html)

| Directory | Reason |
|-----------|--------|
| builds/roblox_tycoon | no index.html |
| builds/robloxmaxx | no index.html |
| builds/biomaxx-sdk54 | no index.html |

---

## Root Cause for Permission Failures

The APP_FACTORY/builds domains were originally deployed from a different surge account. The currently logged-in account (fnsmdehip@proton.me) does not own these domains. To fix:

1. **Option A:** Log into the original surge account that deployed these domains, then redeploy
2. **Option B:** Run `surge teardown <domain>` from the original account, then redeploy from current account
3. **Option C:** Deploy to NEW domains from the current account (e.g., `coding-streak-landing.surge.sh` instead of `coding-streak-app.surge.sh`)

To check which surge account owns a domain: `surge list` from the other account.

---

## Summary

- 27 of 51 deployable sites successfully redeployed (53%)
- All LANDING/app-marketing-pages sites (26) deployed successfully
- LANDING/printmaxx-local-demos deployed successfully
- 2 APP_FACTORY builds (art-streak-app, sutra-streak-app) deployed successfully
- 22 APP_FACTORY builds failed due to domain ownership on a different surge account
- 3 builds directories skipped (no index.html)
