# Growth Plan: MIT repo: agencyenterprise/react-native-health (1132 stars, 

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Gate 'Auto-verify with Apple Health' (step/workout auto-detection) behind $2.99/mo RevenueCat entitlement health_premium
2. Add 'Works with Apple Health' badge to all 6 app store screenshots — zero cost, high trust signal
3. ASO keyword injection: 'apple health integration', 'healthkit tracker', 'automatic fitness tracking', 'apple watch sync'
4. App Store Search Ads on 'healthkit' and 'apple health tracker' — low CPC, intent-matched, minimal competition vs generic fitness

## Budget Tier Strategies

### FREE
Add HealthKit permissions + auto-verify premium feature to all 6 apps via parameterized template. Update App Store listings with Works with Apple Health copy. RevenueCat entitlement at $2.99/mo adds premium tier justification to apps that currently have none.

### LOW
$20-30/mo Apple Search Ads on healthkit keyword cluster. Low bid floor vs generic 'fitness app' keywords, intent-matched to exactly our feature.

### MID
$75-150/mo broader fitness category promotion emphasizing Apple Watch/Health integration angle. Micro-influencer seeding targeting Apple Watch fitness creators (smaller audience, higher conversion).

## Daily Actions

- [ ] Check prior integration output — grep app-factory base template for react-native-health. If already present, skip install step.
- [ ] Add react-native-health to app-factory/base-template/package.json + update Podfile
- [ ] Create src/lib/healthkit.ts: permissions request, readSteps(), readWorkouts(), readSleep() — single reusable wrapper
- [ ] Wire RevenueCat entitlement 'health_premium' at $2.99/mo to gate auto-verify feature
- [ ] Parameterized inject across fitness-streak, running-streak, yoga-streak, meditation-streak, breathwork-streak, plank-streak
- [ ] Generate updated App Store metadata per app with HealthKit keyword cluster + Works with Apple Health screenshot badge
- [ ] Wire Firebase to log HealthKit sync timestamps for retention cohort analysis

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "app_factory"
}
```
