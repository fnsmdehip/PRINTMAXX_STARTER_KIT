# Broken Surge.sh Site Fix Report

**Date:** 2026-03-29
**Issue:** 8 local business demo sites had subdomain names exceeding the 63-character DNS label limit, causing DNS resolution failures.
**Root cause:** Original site names were generated from full business listing titles without truncation.
**Source directory:** `AUTOMATIONS/leads/openclaw/_sites/`

## All 8 Sites Redeployed Successfully

| # | Old Domain (Broken, >63 chars) | New Domain (Fixed) | Status |
|---|---|----|--------|
| 1 | mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok | okc-champion-detailing | DEPLOYED |
| 2 | top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok | okc-pure-prof-detailing | DEPLOYED |
| 3 | window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or | portland-allpro-windows | DEPLOYED |
| 4 | mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham-al | bham-magic-city-detail | DEPLOYED |
| 5 | home-professional-mobile-detailing-amp-products-super-store-birmingham-al | bham-home-detailing | DEPLOYED |
| 6 | the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv | lv-handyman-homeguide | DEPLOYED |
| 7 | local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky | louisville-pinks-windows | DEPLOYED |
| 8 | residential-and-commercial-window-cleaning-cherry-window-cle-louisville-ky | louisville-cherry-windows | DEPLOYED |

## New Live URLs

- https://okc-champion-detailing.surge.sh
- https://okc-pure-prof-detailing.surge.sh
- https://portland-allpro-windows.surge.sh
- https://bham-magic-city-detail.surge.sh
- https://bham-home-detailing.surge.sh
- https://lv-handyman-homeguide.surge.sh
- https://louisville-pinks-windows.surge.sh
- https://louisville-cherry-windows.surge.sh

## Files Updated

- `OPS/DEPLOYMENT_URLS.md` -- added "Local Business Demo Pages (DNS-Fixed Redeployments)" section with all 8 new URLs and mapping to old broken domains.

## Prevention

Future site name generation should truncate subdomain labels to under 50 characters (leaving margin for the `.surge.sh` suffix within the 63-char DNS limit). The naming pattern used here (city-abbreviation + business-keyword) keeps names short and recognizable.
