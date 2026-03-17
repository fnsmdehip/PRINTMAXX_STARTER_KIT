# Playwright Tester Report — 2026-03-17
**Cycle:** 17 (Playwright Tester v2)
**Tested:** 15 sites (10 RED + 5 sample GREEN)
**Time:** 2026-03-17 10:54:56

## Test Results Summary
| Status | Count | % |
|--------|-------|-----|
| GREEN (Healthy) | 6 | 40% |
| YELLOW (Warnings) | 0 | 0% |
| RED (Broken) | 9 | 60% |
| **Total** | **15** | **100%** |

## GREEN Sites (Healthy ✓)
All sites return HTTP 200 with content:
- ✓ old-settlers-dental-p-a-austin-tx.surge.sh
- ✓ printmaxx.surge.sh
- ✓ prayerlock-web.surge.sh
- ✓ coldmaxx.surge.sh
- ✓ mcp-marketplace.surge.sh
- ✓ stackmaxx.surge.sh

## RED Sites Analysis

### DNS Failures (8 sites) — Root Cause Identified
Domain names exceed 63-character DNS label limit:

```
✗ mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh
✗ top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh
✗ window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh
✗ mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham-al.surge.sh
✗ home-professional-mobile-detailing-amp-products-super-store-birmingham-al.surge.sh
✗ the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv.surge.sh
✗ local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.surge.sh
✗ residential-and-commercial-window-cleaning-cherry-window-cle-louisville-ky.surge.sh
```

**Error:** `Failed to parse: '[domain]', label empty or too long`
**Cause:** Local business page generator created names by concatenating full company name + service + city + state, resulting in 80+ character domains
**Fix Required:** Rename with shorter algorithm (max 30 chars), then redeploy

### Blank Page (1 site)
```
✗ saas-stack-audit-200.surge.sh
  Status: HTTP 200 (responds)
  Issue: No meaningful content
  Source: Not found in codebase
  Action: Rebuild or remove
```

## Recommendations

### Immediate Priority
1. **Fix DNS naming:** Redeploy 8 DNS-broken sites with shorter names
2. **Name algorithm:** Enforce max 30-char limit in asset_deployer
3. **Pattern:** `{service}-{city-abbr}.surge.sh` (e.g., `fencing-lv.surge.sh`)

### Testing Methodology
- Used Python `requests` library for HTTP health checks
- Tested DNS resolution, status codes, and content verification
- All core apps (printmaxx, prayerlock, coldmaxx) passing
- Local business pages generator has naming issue

## Next Steps
1. Identify all sites with >63 char DNS labels (grep deployed_assets.json)
2. Generate mapping: old_name → new_short_name
3. Redeploy via `surge` CLI with new names
4. Re-test 100% of sites after fixes
5. Update name generation logic to prevent future issues

---
**Status:** Testing complete. 8 actionable issues identified.
**Report:** See `PLAYWRIGHT_TEST_SUMMARY_20260317.md` for full analysis
