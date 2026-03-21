# Growth Plan: Zero PRINTMAXX Android apps. 72% global market share untappe

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Cross-promote Android launch in existing iOS app update notes
2. ASO keyword stuffing for Android-specific long-tail (e.g. 'bible streak tracker android')
3. Submit to F-Droid for open-source streak apps (free distribution channel)
4. Reddit posts in r/android, r/androidapps announcing each launch
5. Play Store has lower competition than App Store for religious/streak niches — exploit first-mover
6. Use existing 47 landing pages — add Play Store badge next to App Store badge

## Budget Tier Strategies

### FREE
ASO optimization, cross-promo from iOS, Reddit/Twitter launch posts, Play Store badge on all 47 landing pages, F-Droid submission for OSS variants

### LOW
$25/mo Google Ads UAC campaigns targeting 'daily streak' and 'bible reading tracker' keywords on Play Store

### MID
$100/mo for influencer seeding in Android-focused YouTube channels + Google Ads scaling on winners

## Daily Actions

- [ ] BLOCKER: Human must create Google Play Developer account ($25 one-time) — add to PERSISTENT_TASK_TRACKER
- [ ] Audit all 47 deployed apps: which have Capacitor config (easy Android build) vs HTML-only (need TWA wrap)
- [ ] Select top 3 by niche demand: scripture-streak (religious niche huge on Android), prayerlock (Ramadan urgency), focuslock (ADHD productivity)
- [ ] Generate Android keystore and signing config (automate via keytool)
- [ ] Run capacitor add android + capacitor build android for Capacitor apps
- [ ] For HTML-only apps: use Bubblewrap CLI to generate TWA-wrapped APK
- [ ] Generate ASO-optimized Play Store listings using procedural memory skill
- [ ] Create Play Store screenshots via image_factory (existing Playwright HTML-to-image pipeline)
- [ ] Submit AAB bundles to Play Console
- [ ] Add Play Store badges to all 47 landing pages (batch script)
- [ ] Wire android_build_pipeline.py into app_factory_autopilot.py so future apps auto-build for both platforms

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for Play Store screenshots and feature graphics"
}
```
