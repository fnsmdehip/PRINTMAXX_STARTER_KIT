# App Monetization Audit — 2026-03-07

## SCORECARD

| Layer | PrayerLock | ColdMaxx | FocusLock | WalkToUnlock | SleepMaxx | MealMaxx | Store |
|---|---|---|---|---|---|---|---|
| Email capture | YES | YES | YES | YES | YES | YES | YES |
| Affiliate links | NO | NO | NO | NO | NO | NO | NO |
| Premium/paywall | NO | NO | NO | NO | Partial | Partial | YES (mailto) |
| Gumroad links | NO | NO | NO | NO | NO | NO | NO |
| Analytics | NO | NO | NO | NO | NO | NO | NO |

## CRITICAL FINDINGS

1. **5 apps mention pricing but have ZERO payment links.** Every "unlock pro" button goes to email capture instead of checkout. Buyers who want to pay cannot pay.
2. **Store uses mailto: for ALL purchases.** 13 products listed, $197 bundle available, but every "Get It" button opens an email. 3-step friction kills conversion.
3. **Zero analytics on any page.** Building blind - no idea which apps get traffic.
4. **Zero affiliate links despite mentioning competitors by name.** SleepMaxx mentions WHOOP and Oura Ring without monetizing those mentions.

## PRIORITY FIXES

1. Store: Replace mailto: with Gumroad links (blocked on account)
2. Analytics: Add Plausible/GA to all 7 pages
3. ColdMaxx: Add payment link for $12/mo (blocked on Stripe)
4. SleepMaxx: Add affiliate links for WHOOP, Oura Ring
5. MealMaxx + SleepMaxx: Replace email CTAs with payment links on Pro sections

## WHAT AGENT CAN DO NOW (no human needed)

- Add analytics script to all pages
- Add affiliate links to SleepMaxx, ColdMaxx, MealMaxx
- Redeploy updated pages to surge.sh
