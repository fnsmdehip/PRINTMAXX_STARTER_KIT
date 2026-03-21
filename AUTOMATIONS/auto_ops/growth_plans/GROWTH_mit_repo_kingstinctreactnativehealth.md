# Growth Plan: MIT repo: kingstinct/react-native-healthkit (636 stars, Type

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo incremental across fleet from retention improvement

---

## Tactics

1. ASO: add 'works with Apple Health', 'HealthKit', 'auto-track workouts' to all fitness app keywords
2. Screenshot slot 1: show Health.app badge + 'syncs automatically' callout
3. Reddit: post in r/HealthyBeing, r/loseit, r/running — 'finally a streak app that doesn't make you log manually'
4. App Store review prompt after first successful HealthKit sync (highest satisfaction moment)
5. Cross-promote: users of water-streak see pushup-streak in-app ('also tracks via Apple Health')

## Budget Tier Strategies

### FREE
ASO keyword update across all 8 fitness builds, update app descriptions to mention HealthKit, Reddit organic posts in fitness subreddits targeting 'automatic tracking' pain point, add Apple Health badge to all app store screenshots

### LOW
$20-30/mo on Apple Search Ads for 'HealthKit app' + 'automatic fitness tracker' keywords — low competition, high intent

### MID
$50-100/mo: micro-influencer seeding with fitness creators who already use Apple Watch (HealthKit power users), target r/AppleWatch community

## Daily Actions

- [ ] Run audit phase: identify all fitness-category builds in app factory (fitness-streak, runningstreak, pushup-streak, plank-streak, yoga-streak, water-streak, breathwork-streak, meditation-streak)
- [ ] Check if agencyenterprise/react-native-health already installed in base-template — if yes, evaluate kingstinct as TypeScript-typed replacement, don't install both
- [ ] Add @kingstinct/react-native-healthkit to app factory base-template package.json
- [ ] Create src/lib/healthkit.ts with useHealthKitData hook + permission request + graceful fallback to manual input when HealthKit unavailable (Android users)
- [ ] Wire HKQuantityTypeIdentifierStepCount to walking/running apps, HKWorkoutType to fitness apps, HKQuantityTypeIdentifierDietaryWater to water-streak
- [ ] Add required Info.plist entries (NSHealthShareUsageDescription) to base template
- [ ] Update app store metadata: add 'Apple Health' badge, 'auto-tracks from HealthKit' to screenshots and descriptions for all 8 builds
- [ ] Re-deploy affected builds to Surge/App Store TestFlight
- [ ] Add KPI entry to OPS/KPI_DASHBOARD.md: D7 retention comparison HealthKit vs manual

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "existing app factory template system",
  "library": "@kingstinct/react-native-healthkit (TypeScript, 636 stars, MIT)",
  "note": "Prior integration used agencyenterprise/react-native-health \u2014 check for overlap before installing both. kingstinct has better TypeScript support."
}
```
