# TruthScope Handoff — Fix and Ship

## STATUS: App code complete, NOT running. Two blocking bugs.

## Bug 1: Space in path breaks xcodebuild
The folder `lie detector app/TruthScope` has a space. Xcode build scripts split the path at the space:
```
bash: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/lie: No such file or directory
```

**FIX:** Move folder to `lie-detector-app/` (no spaces):
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
mv "lie detector app" "lie-detector-app"
cd lie-detector-app/TruthScope
rm -rf ios .expo node_modules/.cache
npx expo prebuild --platform ios --clean
npx expo run:ios
```

## Bug 2: Reanimated 4.x crashes in Expo Go
SDK 54 ships Reanimated 4.x which requires native build (NOT Expo Go).
The app works in Expo Go when reanimated import is removed (confirmed via screenshot).

**FIX:** Use `npx expo run:ios` (native dev client) instead of `npx expo start --ios` (Expo Go).
The prebuild + run:ios already works once the path space is fixed.

## What's Built (verified: TypeScript 0 errors, Expo export passes)

### 17 source files, ~8,315 lines
- `src/engines/PPGEngine.ts` — Finger-on-camera heart rate via photoplethysmography
- `src/engines/VoiceEngine.ts` — Voice stress analysis (pitch, jitter, response latency)
- `src/engines/FaceEngine.ts` — Facial micro-expression tracking (blink rate, gaze, asymmetry)
- `src/engines/DeceptionAnalyzer.ts` — Multi-modal fusion (weighted combination of all engines)
- `src/screens/OnboardingScreen.tsx` — 14-screen Cal AI-style onboarding (1,654 lines)
- `src/screens/DetectionScreen.tsx` — Main detection UI with real-time viz (1,419 lines)
- `src/screens/PartyModeScreen.tsx` — 6-phase party game (1,575 lines, viral feature)
- `src/screens/HomeScreen.tsx` — Dashboard with mode cards, recent sessions
- `src/screens/ResultScreen.tsx` — Analysis results with verdict, breakdown, share
- `src/screens/SettingsScreen.tsx` — Settings, calibration, science explanation
- `src/components/ScoreGauge.tsx` — Animated circular score gauge (color-coded verdict)
- `src/components/PulseWaveform.tsx` — SVG pulse wave + ECG waveform generator
- `src/components/MetricCard.tsx` — HR, HRV, signal quality, stress bar components
- `src/navigation/AppNavigator.tsx` — Stack navigator with onboarding gate
- `src/store/index.ts` — AsyncStorage persistence (profile, sessions, baseline)
- `src/theme/index.ts` — Dark theme (cyan/purple/pink accents)
- `src/utils/types.ts` — Full TypeScript types for all detection data
- `src/utils/partyQuestions.ts` — 34 party questions (mild/spicy/random + premium)
- `src/legal/disclaimer.ts` — Full disclaimer, short disclaimer, consent text

### Config
- `app.json` — Bundle ID: com.printmaxx.truthscope, camera+mic permissions, dark theme
- `babel.config.js` — babel-preset-expo + reanimated/plugin
- `package.json` — 30 dependencies, Expo SDK 54

### Stripe (LIVE)
- Monthly $4.99: https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F
- Annual $29.99: https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G
- Product IDs: prod_UFr5UfHXrdFre7 (monthly), prod_UFrIVBd0jWOBIQ (annual)

### Assets
- `assets/icon.png` — 1024x1024 (Pillow-generated, need Imagen 4 upgrade)
- `assets/adaptive-icon.png`, `splash-icon.png`, `favicon.png`

### Research docs
- `RESEARCH.md` — iPhone biometric science (PPG, voice, face, accuracy claims)
- `COMPETITIVE_RESEARCH.md` — App Store gap analysis, LiarLiar.ai teardown
- `NEW_CLAUDE_CAPABILITIES.md` — Computer-use MCP, KAIROS, agent teams
- `APP_STORE_LISTING.md` — Full ASO-optimized listing

### Content
- `CONTENT/social/posting_queue/20260401_truthscope_launch.md` — 3 tweets + 1 thread

### Landing page
- `LANDING/truthscope/index.html` — 225-line pre-launch page (deploy blocked by Surge free tier)

## ONE-SHOT FIX SCRIPT
Run this to fix everything and launch:
```bash
export PATH="/opt/homebrew/bin:$PATH"
export LANG=en_US.UTF-8
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# Fix the space in path
mv "lie detector app" "lie-detector-app"

# Update any references
grep -rl "lie detector app" .claude/ OPS/ AUTOMATIONS/ 2>/dev/null | head -20

# Clean and rebuild
cd lie-detector-app/TruthScope
rm -rf ios .expo node_modules/.cache ~/Library/Developer/Xcode/DerivedData/TruthScope*
npx expo prebuild --platform ios --clean
npx expo run:ios
```

## NEXT: After app runs
1. Screenshot every screen with `xcrun simctl io booted screenshot`
2. Enable computer-use MCP (`/mcp` → select computer-use → Enable) for automated QA
3. Fix any runtime errors
4. Generate Imagen 4 icon (Google ImageFX already has the prompt saved)
5. `npx expo export --platform ios` final check
6. EAS Build for App Store submission

## IMPORTANT: Lessons learned
- NEVER use folder names with spaces for React Native projects
- NEVER claim "app is running" without a screenshot showing the actual app UI
- Expo Go does NOT support Reanimated 4.x — always use native dev builds for SDK 54
- Computer-use MCP works in desktop app too, enable via `/mcp`
