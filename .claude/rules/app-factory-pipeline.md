# App Factory Pipeline (ALWAYS active for app work)

## Quality Standards (non-negotiable for ALL apps)
1. **Cal AI-style onboarding** — 12-14 personalized screens before paywall. Build emotional investment.
2. **Hard paywall with rescue offer** — visual trial timeline, "No payment due now", two plans (monthly anchor + yearly highlighted), rescue offer on decline
3. **Stripe Payment Links** — primary payment method. Add RevenueCat IAP as A/B test at $1K MRR.
4. **Real encryption** — AES-256-CTR + HMAC-SHA-256 minimum. No XOR, no stubs, no mocks.
5. **Local-first** for sensitive apps — zero server, user-owned cloud backup, encrypted before upload
6. **No fakes** — Rule 22. If a service isn't connected, show NOT IMPLEMENTED error.
7. **13-point test runner** before submission — `python3 AUTOMATIONS/app_factory/test_runner.py --test PATH`
8. **Real visual assets** — logos, icons, screenshots. Not Ionicons placeholders.
9. **ASO-optimized descriptions** — every feature, template, use case named in description
10. **Weekly + Annual pricing** — weekly+trial = highest LTV configuration
11. **ZERO SIMULATED SENSOR DATA** — Rule 31. If the app claims to read a sensor (camera, mic, accelerometer, heart rate), it MUST read the REAL sensor. Use libraries that provide real frame/audio/sensor data (react-native-vision-camera for camera frames, react-native-pitch-detector for voice F0, expo-sensors for accelerometer). NEVER use Math.random() to generate fake readings behind a real-looking UI. NEVER estimate values from proxy data when the real data is obtainable with the right library. If a sensor isn't available in the current environment (Simulator), show "SENSOR UNAVAILABLE" not fake data. The entire value proposition is REAL vs the App Store's sea of fakes.
12. **Apple Watch / HealthKit integration** — Rule 32. For ANY health/biometric app: check if Apple Watch can provide better data via HealthKit. HR, HRV, SpO2, skin temp, respiratory rate are all available. Use `react-native-health` or `expo-health-connect`. Apple Watch data is medical-grade continuous monitoring, always prefer it over phone camera PPG when available. SpO2 available on Series 6+, 10, Ultra 2 (was disabled on 9/Ultra 1, resolved late 2025).
13. **No exaggerated accuracy claims** — Never claim "medical-grade", "comparable to polygraph", "same signals as professional equipment" unless backed by cited peer-reviewed research. Phone sensors are LESS precise than dedicated equipment. Say so. Honest positioning builds trust and avoids Apple review rejection + FTC issues. Show real accuracy ranges from published research, not marketing numbers.
14. **Professional sound design** — Every app MUST have sound effects for: button taps, toggles, navigation transitions, success/error states, and any app-specific interactions (detection, scanning, reveals, countdowns). Source sounds from professional CC0/CC-BY libraries (Octave for iOS taps/slides/beeps, Kenney for UI clicks/switches, Google Material Design for system sounds). NEVER generate sounds with Python sine waves for production. Store in `assets/sounds/`, create `src/sounds/SoundEngine.ts` with preloading, volume control, and fire-and-forget playback. Initialize in App.tsx. **CRITICAL: `playSound()` must be CALLED from every screen at every interaction point** - initialization without wiring is useless. Verify by grepping for `playSound` in every screen file. If a screen has zero `playSound` calls, it's not done. Sound is not optional - it's the difference between a $0 app and a $10M app.
15. **Native builds, not Expo Go** — For SDK 54+ with Reanimated 4.x, ALWAYS use `npx expo prebuild --platform ios && npx expo run:ios`. Expo Go does NOT support Reanimated 4.x or any native modules (vision-camera, pitch-detector, etc). NEVER use `expo start --ios` for production apps.
16. **No spaces in project folder names** — Xcode build scripts break on spaces in paths. Use hyphens: `lie-detector-app/` not `lie detector app/`. Check before creating any new app project.
17. **Deep linking from day one** — Configure URL scheme in app.json and wire linking config in navigator. Enables programmatic QA (`xcrun simctl openurl booted "scheme://screen"`) and future push notification routing.
18. **Verify with screenshot, not vibes** — After ANY build, run `xcrun simctl io booted screenshot /tmp/verify.png` and READ the image. "Metro is serving" is NOT verification. "Expo export passes" is NOT verification. Only a screenshot of the actual rendered UI counts as verified.

## Pipeline Commands
```bash
# Full autonomous pipeline (runs all stages)
python3 AUTOMATIONS/app_factory/auto_orchestrator.py --full

# Individual stages
python3 AUTOMATIONS/app_factory/opportunity_scanner.py --scan
python3 AUTOMATIONS/app_factory/app_generator.py --generate --niche NICHE --name NAME
python3 AUTOMATIONS/app_factory/deep_qa.py --test-all              # Stage 3a: functional QA
python3 AUTOMATIONS/app_factory/test_runner.py --test-all --static-only  # Stage 3b: rejection checks
python3 AUTOMATIONS/app_factory/post_build_validator.py --path PATH  # Stage 3c: nav/sound/data validation
python3 AUTOMATIONS/app_factory/build_submit.py --build-and-submit PATH
python3 AUTOMATIONS/app_factory/distribution_engine.py --full PATH
python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --optimize

# Status
python3 AUTOMATIONS/app_factory/auto_orchestrator.py --status
```

## Pipeline Flow (fully automated)
```
opportunity_scanner.py --scan          (Stage 1: find niches)
    ↓
app_generator.py --generate            (Stage 2: create app from template)
    ↓
deep_qa.py --test PATH                 (Stage 3a: books exist? content real? crypto works? features functional?)
    ↓
test_runner.py --test PATH             (Stage 3b: 13-point Apple rejection checklist)
    ↓
post_build_validator.py --path PATH    (Stage 3c: nav/sound/data validation)
    ↓
build_submit.py --build-and-submit     (Stage 4: EAS Build + Submit)
    ↓
distribution_engine.py --full          (Stage 5: ASO, screenshots, social, influencer)
    ↓
portfolio_optimizer.py --optimize      (Stage 6: kill/scale/boost weekly)
```

## Deep QA Checks (auto-runs per app type)
**All apps:** dead imports, empty screens, payment flow, onboarding (12+ screens), paywall rescue offer, hardcoded strings

## Post-Build Validator Checks (Stage 3c — `post_build_validator.py`)
Every app MUST pass these before claiming "done":
1. **Navigation integrity** — all navigate() calls match registered screen names
2. **Sound integration** — SoundTouchable or playSound in every screen with touchable elements
3. **Zero simulated sensor data** — no Math.random in sensor/biometric contexts
4. **Back navigation** — every non-root screen has goBack or back arrow
5. **Dead code** — no _REMOVED_ markers or TODO:remove
6. **Empty states** — lists/grids show message when empty
7. **Loading states** — async operations show ActivityIndicator
8. **TypeScript clean** — `npx tsc --noEmit` must pass with 0 errors

## Revenue Pipeline Checklist (MUST verify before any app ships)
Learned from TruthScope audit — these were ALL broken and caught late:
1. **isPremium reads from store** — NEVER hardcode `useState(false)`. Load from AsyncStorage on mount.
2. **Free tier ACTUALLY gated** — premium features blocked in code, not just labeled. Verify by testing as free user.
3. **Session/usage limits enforced** — if paywall promises "3/day free", code MUST count and block at limit.
4. **Payment callback wired** — Stripe success URL deep links back to app, sets isPremium=true.
5. **Restore Purchases honest** — if using Stripe (not IAP), explain Stripe subscription management, don't fake "looking for purchases."
6. **Recording/session saves** — every detection session MUST save to AsyncStorage AND navigate to Result screen. Ephemeral sessions = wasted user effort.
7. **Paywall single CTA** — ONE primary action button, not two competing "skip" buttons. Rescue offer only on explicit decline.
8. **Premium mode gating** — if paywall says "X mode free only", other modes MUST show upgrade prompt, not silently work.

## Architecture Standards (from TruthScope v2 one-shot process)
These must be in place FROM THE START, not added later:
1. **babel.config.js** with reanimated/plugin — create during scaffold, not after first crash
2. **SoundTouchable wrapper** — create as first component, import instead of TouchableOpacity in every screen
3. **useDetectionEngine pattern** — sensor hook separate from screen, never inline simulated data in screen files
4. **Deep linking** — URL scheme in app.json + linking config in navigator from day one
5. **Safe area insets** — use `useSafeAreaInsets()`, never hardcode `paddingTop: 60`
6. **Typed navigation** — `NativeStackNavigationProp<RootStackParamList>`, never `navigation: any`
7. **Store functions for IDs** — use `generateId()` from store, not inline `Math.random()` in screens
8. **Timer cleanup on unmount** — every setInterval, setTimeout, and Audio.Recording MUST be cleaned up in useEffect return
9. **Duration consistency** — decide seconds or milliseconds and be consistent. Display always in seconds.
10. **No console.log/warn in production** — gate behind `__DEV__` or remove entirely

## Sound Design Checklist
1. Copy Octave + Kenney CC0 sounds to `assets/sounds/` (22 files minimum)
2. Create `src/sounds/SoundEngine.ts` with preloading + volume control
3. Create `src/components/SoundTouchable.tsx` wrapper with auto sound+haptic
4. Replace `TouchableOpacity` import with `SoundTouchable as TouchableOpacity` in EVERY screen
5. Add contextual sounds: `swipe` on navigation, `success`/`error` on state changes, `toggle` on switches
6. Set `playsInSilentModeIOS: true` (users in silent mode still need app sounds)
7. Verify: `grep -rn playSound src/screens/` must show calls in ALL screen files
**Ebook reader:** book catalog (50+ books?), content real (not empty), reader navigation
**Religious reading:** Bible/scripture text verified, verse accuracy, translation gating
**Nutrition tracker:** TDEE formula correct (Mifflin-St Jeor), macro split, AI scanning wired
**Consent/legal:** AES-256 encryption, HMAC integrity, PIN lockout, audit log, template system, cloud backup

## Cron Schedule
- `30 6 * * * python3 AUTOMATIONS/app_factory/auto_orchestrator.py --full` (daily 6:30 AM)
- `0 7 * * 1 python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --optimize` (Monday 7 AM)

## Research Reports (read before making app decisions)
- `OPS/IOS_PAYWALL_BEST_PRACTICES.md` — Cal AI teardown, conversion data
- `OPS/APP_FACTORY_BATTLE_TESTED_2026.md` — pricing, weekly plans, transaction abandon
- `OPS/APP_FACTORY_AUTOMATION_RESEARCH.md` — tools, CI/CD, Maestro, ASO, Apple 4.3 spam

## Apple 4.3 Spam Prevention
Religious streak apps (Scripture/Quran/Torah/etc.) risk spam detection if submitted as identical clones.
Strategy: differentiate each variant with unique features, submit in batches with 2-week gaps, or consolidate into one app with IAP content packs.

## Current Portfolio (4 apps)
| App | Bundle ID | Stripe Products | Status |
|-----|-----------|----------------|--------|
| Scripture Streak | com.printmaxx.scripturestreak | Annual $29.99 + Monthly $2.99 | Simulator tested |
| NutriSnap | com.printmaxx.nutrisnap | Annual $29.99 + Monthly $4.99 | Simulator tested |
| Pocket Alexandria | com.printmaxx.pocketalexandria | Annual $9.99 + Monthly $1.99 | Simulator tested |
| cnsnt | com.printmaxx.cnsnt | Annual $29.99 + Monthly $4.99 | Simulator tested |

## Builds Location
All apps: `MONEY_METHODS/APP_FACTORY/builds/{slug}/`
Synced to: `~/Documents/{app-name}/`
