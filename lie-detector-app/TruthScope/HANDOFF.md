# TruthScope Handoff — For Fresh CLI Session

## STATUS: App RUNS on simulator. Home screen verified. Needs full screen-by-screen QA.

**Location:** `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/lie-detector-app/TruthScope/`

## FIXED BUGS (already resolved)
1. Folder renamed from `lie detector app` to `lie-detector-app` (spaces broke xcodebuild)
2. Using native dev build (`expo run:ios`) instead of Expo Go (Reanimated 4.x incompatible with Expo Go)
3. Missing `babel.config.js` with reanimated plugin — created
4. Missing `babel-preset-expo` — installed

## WHAT TO DO (in order)

### Step 1: Enable Computer Use (one-time setup)
```
/mcp
# Select "computer-use" → Enable
# Grant macOS Accessibility + Screen Recording permissions in System Settings
# Click "Try again" after granting
```

### Step 2: Launch the app
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/lie-detector-app/TruthScope
npx expo run:ios
```
If it says "Build Succeeded" the app is installed. If not, run:
```bash
rm -rf ios .expo && npx expo prebuild --platform ios --clean && npx expo run:ios
```

### Step 3: QA every screen with Computer Use
Once computer-use is enabled, ask Claude:
```
Open the iOS Simulator. The TruthScope app should be running.
Tap through every screen and screenshot each one:
1. Home screen (should show 4 mode cards + Party Mode banner)
2. Tap "Finger Pulse" → Detection screen with camera view
3. Go back, tap "Face Scan" → Detection with front camera
4. Go back, tap "Voice Analysis" → Detection with waveform
5. Go back, tap settings gear → Settings screen
6. Go back, tap "Party Mode" → Party setup screen
7. Add 2 players, start game → Question screen
8. Tap "Analyze" → Analysis animation
File bugs for any screen that crashes or looks broken.
```

Alternative without computer-use (xcrun simctl screenshots):
```bash
# Screenshot current screen
xcrun simctl io booted screenshot /tmp/ts_screen.png

# Deep link to specific screens (linking configured)
xcrun simctl openurl booted "truthscope://home"
xcrun simctl openurl booted "truthscope://detection/finger"
xcrun simctl openurl booted "truthscope://settings"
xcrun simctl openurl booted "truthscope://party"
xcrun simctl openurl booted "truthscope://onboarding"
```
Note: Deep links trigger an "Open in TruthScope?" dialog. Dismiss it via Simulator click.

### Step 4: Fix any broken screens
Common issues to watch for:
- Red error screens → check Metro terminal for the actual JS error
- Blank screens → missing export (check default vs named exports)
- Camera screens → Camera won't work in Simulator, but UI should render with placeholder
- Reanimated animations → should work in native build, if not check babel.config.js

### Step 5: Final verification
```bash
npx tsc --noEmit                    # TypeScript check
npx expo export --platform ios      # Bundle check
xcrun simctl io booted screenshot /tmp/final_verify.png  # Visual check
```

## WHAT'S BUILT

### App (17 files, ~8,315 lines TypeScript)
| File | Lines | What |
|------|-------|------|
| `src/engines/PPGEngine.ts` | 373 | Finger-on-camera heart rate (PPG) |
| `src/engines/VoiceEngine.ts` | 298 | Voice stress analysis |
| `src/engines/FaceEngine.ts` | 339 | Facial micro-expression tracking |
| `src/engines/DeceptionAnalyzer.ts` | 246 | Multi-modal fusion scorer |
| `src/screens/OnboardingScreen.tsx` | 1,654 | 14-screen Cal AI-style onboarding |
| `src/screens/DetectionScreen.tsx` | 1,419 | Main detection UI + real-time viz |
| `src/screens/PartyModeScreen.tsx` | 1,575 | 6-phase party game (viral feature) |
| `src/screens/HomeScreen.tsx` | 862 | Dashboard with mode cards |
| `src/screens/ResultScreen.tsx` | 322 | Analysis results + share |
| `src/screens/SettingsScreen.tsx` | 276 | Settings + science explanation |
| `src/components/ScoreGauge.tsx` | 175 | Animated score circle |
| `src/components/PulseWaveform.tsx` | 125 | SVG pulse + ECG waveform |
| `src/components/MetricCard.tsx` | 202 | HR, HRV, signal quality bars |
| `src/navigation/AppNavigator.tsx` | 100 | Stack nav + deep linking |
| `src/store/index.ts` | 75 | AsyncStorage persistence |
| `src/theme/index.ts` | 64 | Dark theme colors |
| `src/utils/types.ts` | 94 | TypeScript types |
| `src/utils/partyQuestions.ts` | 64 | 34 party questions |
| `src/legal/disclaimer.ts` | 62 | Legal disclaimers |

### Stripe (LIVE on production)
- Monthly $4.99: `https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F` (prod_UFr5UfHXrdFre7)
- Annual $29.99: `https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G` (prod_UFrIVBd0jWOBIQ)

### Other deliverables
- `APP_STORE_LISTING.md` — ASO-optimized App Store copy (8KB)
- `CONTENT/social/posting_queue/20260401_truthscope_launch.md` — 3 tweets + 1 thread
- `LANDING/truthscope/index.html` — Pre-launch landing page (14KB, deploy blocked by Surge free tier)
- `RESEARCH.md` — iPhone biometric science (PPG, voice, face accuracy)
- `COMPETITIVE_RESEARCH.md` — App Store gap analysis
- `NEW_CLAUDE_CAPABILITIES.md` — Computer-use, KAIROS, agent teams

### Config
- `app.json` — Bundle ID: com.printmaxx.truthscope, dark theme, camera+mic permissions
- `babel.config.js` — babel-preset-expo + reanimated/plugin
- Deep linking: truthscope:// scheme with routes for all screens

## KNOWN LIMITATIONS
- Camera doesn't work in Simulator (shows blank/placeholder) — normal, works on real device
- Pillow-generated icon is placeholder quality — need Imagen 4 from Google ImageFX for production
- Detection engines use simulated data for UI testing — real sensor processing needs react-native-vision-camera (for PPG frame processing) and react-native-pitch-detector (for real voice analysis)
- Surge free tier blocks deployment of landing page
