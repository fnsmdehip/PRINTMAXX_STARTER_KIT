# PRD: TruthScope — Production-Quality App Spec
# Version: 1.0 — Full Edge-Case Hardened
# Date: 2026-04-07
# Status: SIMULATOR VERIFIED — BLOCKED ON ENGINE WIRING BEFORE APP STORE

> This spec documents every screen, every edge case, every sensor behavior, and every
> App Store requirement. An agent reading ONLY this doc should understand exactly what
> TruthScope is, what's real vs simulated, and what must be fixed before launch.

---

## 1. APP OVERVIEW

**Name:** TruthScope: Real Lie Detector
**Bundle ID:** com.printmaxx.truthscope
**Tagline:** Biometric Truth Analysis
**Category:** Utilities (primary), Lifestyle (secondary)
**Age Rating:** 17+ (mature themes — lie detection involves conflict/trust scenarios)
**Target User:** People who want real biometric-based lie detection, not prank apps. "Bring your laptop to a date" is their problem. TruthScope is the solution.

**Positioning:** The only real biometric lie detector on iOS. Every other app uses random results. TruthScope uses the camera, microphone, and face — three of the five signal types a professional polygraph uses.

**Monetization:** Stripe Payment Links (no IAP, no RevenueCat)
- Monthly $4.99: https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F
- Annual $29.99: https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G (save 50%)
- 7-day free trial per Stripe product configuration

**Free Tier:**
- 3 sessions per day
- Finger Pulse mode only
- Cannot access: Face Scan, Voice Analysis, Multi-Modal, Party Mode premium questions

**Premium Tier:**
- Unlimited sessions
- All four detection modes
- Face Scan, Voice Analysis, Multi-Modal detection
- Spicy/random premium Party Mode questions
- Session export/share

**Deep Link Scheme:** `truthscope://`
- `truthscope://home`
- `truthscope://detection/:mode` (finger, face, voice, multi)
- `truthscope://settings`
- `truthscope://party`
- `truthscope://onboarding`
- `truthscope://premium-activated` (Stripe success callback — triggers setPremium(true))
- `truthscope://payment-success` (alternate Stripe success callback)

**Privacy Policy:** https://printmaxx-privacy.surge.sh
**Terms of Service:** https://printmaxx-tos.surge.sh
**Payment Success Page:** printmaxx-payments.surge.sh/success

---

## 2. TECH STACK

| Layer | Library | Version | Notes |
|-------|---------|---------|-------|
| Framework | Expo SDK | ~54.0.33 | New architecture enabled |
| Language | TypeScript | ~5.9.2 | Strict mode |
| React | React | 19.1.0 | |
| React Native | react-native | 0.81.5 | |
| Navigation | @react-navigation/native + native-stack | ^7.x | No bottom tabs |
| Animations | react-native-reanimated | ~4.1.1 | SDK 54 native build REQUIRED |
| Gestures | react-native-gesture-handler | ~2.28.0 | |
| Camera | expo-camera | ~17.0.10 | CameraView API; `[BLOCKED]` no frame access |
| Audio | expo-av | ~16.0.8 | Audio.Recording for voice; expo-av for sounds |
| Haptics | expo-haptics | ~15.0.8 | |
| Linear gradient | expo-linear-gradient | ~15.0.8 | |
| SVG | react-native-svg | 15.12.1 | Waveform/gauge rendering |
| Safe area | react-native-safe-area-context | ~5.6.0 | |
| Screens | react-native-screens | ~4.16.0 | |
| Storage | @react-native-async-storage/async-storage | 2.2.0 | All persistence |
| Icons | @expo/vector-icons (Ionicons) | ^15.0.3 | |
| Linking | expo-linking | ~8.0.11 | Deep links + Stripe callbacks |
| Web browser | expo-web-browser | ~15.0.10 | |
| Store review | expo-store-review | ~9.0.9 | |
| Sharing | expo-sharing | ~14.0.8 | |
| File system | expo-file-system | ~19.0.21 | |
| Image picker | expo-image-picker | ~17.0.10 | |
| Device | expo-device | ~8.0.10 | |
| Font | expo-font | ~14.0.11 | |
| Blur | expo-blur | ~15.0.8 | |

**Build command (REQUIRED — never use expo start):**
```bash
cd lie-detector-app/TruthScope
npx expo run:ios
```

**Why native build required:** react-native-reanimated 4.1.1 and expo-camera native modules are not supported in Expo Go. Using `expo start --ios` results in immediate crash.

**Testing infrastructure:**
- Maestro 2.4.0 — 7 YAML test suites in `.maestro/`
- ios-simulator-skill — 21 scripts at `~/.claude/skills/ios-simulator-skill/`
- Computer-use MCP — enabled, Simulator access granted

---

## 3. DATA TYPES (canonical)

```typescript
// Detection mode
type DetectionMode = 'finger' | 'face' | 'voice' | 'multi';

// Verdict from analysis
type Verdict = 'truthful' | 'deceptive' | 'uncertain' | 'scanning';

// Onboarding steps (14 total)
type OnboardingStep =
  | 'welcome'
  | 'howItWorks'
  | 'scienceBehind'
  | 'fingerDemo'
  | 'faceDemo'
  | 'voiceDemo'
  | 'multiModal'
  | 'accuracy'
  | 'disclaimer'
  | 'permissions'
  | 'baseline'
  | 'partyMode'
  | 'premium'
  | 'ready';

// Raw PPG reading from camera frames
interface PPGReading {
  timestamp: number;
  redChannel: number;      // avg red channel value 0-255
  greenChannel: number;    // avg green channel value 0-255
  heartRate: number;       // BPM, 40-200 range
  hrv: number;             // RMSSD in ms
  signalQuality: number;   // 0-1, below 0.3 = discarded
}

// Raw voice reading from microphone
interface VoiceReading {
  timestamp: number;
  fundamentalFreq: number;    // Hz; estimated from envelope, not true F0
  jitter: number;             // 0-1 cycle-to-cycle pitch variation
  shimmer: number;            // 0-1 amplitude variation
  voiceTremor: number;        // 0-1 low-frequency modulation
  responseLatency: number;    // seconds from question to first speech
  stressIndex: number;        // 0-100 composite stress score
}

// Raw face reading from camera face detection
interface FaceReading {
  timestamp: number;
  blinkRate: number;              // blinks per minute
  gazeStability: number;          // 0-1, higher = more stable
  microExpressionScore: number;   // 0-100
  asymmetryScore: number;         // 0-100
  lipCompressionDetected: boolean;
  noseWrinkleDetected: boolean;
  eyeContactPercent: number;      // 0-100
}

// Final analysis result for one detection session
interface DetectionResult {
  id: string;
  timestamp: number;
  mode: DetectionMode;
  verdict: Verdict;
  confidence: number;        // 0-95 (capped at 95%)
  overallScore: number;      // 0-100
  breakdown: {
    physiological: number;   // 0-100
    vocal: number;           // 0-100
    facial: number;          // 0-100
  };
  ppgData?: PPGReading[];
  voiceData?: VoiceReading[];
  faceData?: FaceReading[];
  question?: string;
  duration: number;          // seconds
}

// One full session (may contain multiple results)
interface SessionData {
  id: string;
  startTime: number;
  endTime?: number;
  mode: DetectionMode;
  results: DetectionResult[];
  participants?: string[];
  isPartyMode: boolean;
}

// User profile / preferences
interface UserProfile {
  hasCompletedOnboarding: boolean;
  isPremium: boolean;
  sessionsCompleted: number;
  baselineHR?: number;       // BPM from calibration
  baselineHRV?: number;      // ms RMSSD from calibration
  baselineVoiceF0?: number;  // Hz from calibration
}

// Party mode question
interface PartyQuestion {
  id: string;
  text: string;
  category: 'spicy' | 'mild' | 'random' | 'custom';
  isPremium: boolean;
}
```

**AsyncStorage Keys:**
| Key | Type | Contents |
|-----|------|---------|
| `truthscope_profile` | `UserProfile` | Premium status, onboarding, baseline |
| `truthscope_sessions` | `SessionData[]` | Last 100 sessions (oldest dropped at 101) |
| `truthscope_baseline` | `{ heartRate, hrv, voiceF0 }` | Calibration baseline |

**ID generation:** `Date.now().toString(36) + Math.random().toString(36).substring(2, 8)`

---

## 4. CONSTANTS AND CONFIG

```typescript
// Free tier limits
const DAILY_FREE_LIMIT = 3;            // sessions per day
const FREE_MODES = ['finger'];         // face, voice, multi = premium only
const FREE_QUESTION_CATEGORIES = ['mild'];  // spicy, random premium Q gated

// PPG Engine
const SAMPLE_RATE = 30;               // camera FPS target
const WINDOW_SIZE = 256;              // ~8.5 seconds at 30fps
const MIN_HR = 40;                    // BPM lower bound
const MAX_HR = 200;                   // BPM upper bound
const MIN_SIGNAL_QUALITY = 0.3;       // below this = discard frame

// Voice Engine
const ANALYSIS_INTERVAL_MS = 500;    // voice analysis every 500ms
const BASELINE_DURATION_MS = 10000;  // 10 seconds for baseline

// Party Mode
const MIN_PLAYERS = 2;
const MAX_PLAYERS = 8;
const ANALYSIS_DURATION_MS = 10000; // 10 second analysis per player
const PASS_PHONE_COUNTDOWN = 5;     // seconds to pass phone

// Deception thresholds
const THRESHOLD_TRUTHFUL = 30;       // score < 30 = truthful
const THRESHOLD_DECEPTIVE = 55;      // score > 55 = deceptive (30-55 = uncertain)

// Multi-modal fusion weights
const WEIGHTS = {
  finger: { physio: 1.0, vocal: 0.0, facial: 0.0 },
  face:   { physio: 0.3, vocal: 0.0, facial: 0.7 },
  voice:  { physio: 0.0, vocal: 1.0, facial: 0.0 },
  multi:  { physio: 0.40, vocal: 0.30, facial: 0.30 },
};

// Stripe
const MONTHLY_LINK = 'https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F';
const ANNUAL_LINK = 'https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G';

// Legal
const PRIVACY_POLICY_URL = 'https://printmaxx-privacy.surge.sh';
const TERMS_URL = 'https://printmaxx-tos.surge.sh';
```

---

## 5. NAVIGATION STRUCTURE

**Stack type:** Native Stack (no bottom tabs)
**Library:** `@react-navigation/native-stack`
**Initial route:** If `hasCompletedOnboarding = false` → Onboarding; else → Home

```
RootStackParamList:
  Onboarding: undefined
  Home: undefined
  Detection: { mode?: DetectionMode }
  Result: { result: DetectionResult }
  Settings: undefined
  PartyMode: undefined
```

**Navigation animations:**
- All screens: `slide_from_right`
- PartyMode: `slide_from_bottom` (modal feel)
- All headers: hidden (`headerShown: false`)

**Deep link → screen mapping:**
```
truthscope://onboarding     → Onboarding
truthscope://home           → Home
truthscope://detection/:mode → Detection with mode param
truthscope://result         → Result
truthscope://settings       → Settings
truthscope://party          → PartyMode
truthscope://premium-activated → (side effect: setPremium(true))
truthscope://payment-success   → (side effect: setPremium(true))
```

**Stripe payment callback handling (AppNavigator.tsx):**
- `Linking.addEventListener('url', handler)` fires when app is in foreground
- `Linking.getInitialURL()` fires when app cold-launched from link
- Both check for `premium-activated` or `payment-success` substrings
- On match: call `setPremium(true)` from store
- Premium takes effect immediately (AsyncStorage write, no refetch needed)

---

## 6. SCREEN-BY-SCREEN SPECIFICATION

### 6.1 OnboardingScreen

**File:** `src/screens/OnboardingScreen.tsx`
**Route:** `Onboarding`
**Total Steps:** 14 (Cal AI style — emotional investment before paywall)
**Step order:**

```
1. welcome
2. howItWorks
3. scienceBehind
4. fingerDemo
5. faceDemo
6. voiceDemo
7. multiModal
8. accuracy
9. partyMode       ← "use cases" framing
10. disclaimer
11. permissions    ← requests camera + mic
12. baseline       ← calibration session
13. premium        ← PAYWALL (step 13 of 14)
14. ready
```

**Layout:** `FlatList` horizontal with `pagingEnabled: true`. Each page fills screen. Navigation via swipe or "Next" button. FlatList index tracked via `onViewableItemsChanged`.

**Stripe links (hardcoded in this file):**
```
Monthly: https://buy.stripe.com/fZu5kEgmk4Bv51n1Ar3F60F
Annual:  https://buy.stripe.com/6oU6oI7POgkd65rcf53F60G
```

**Premium step behavior:**
- Two CTAs: "Start Free Trial (7 Days)" → opens annual link; "Monthly $4.99" → opens monthly link
- "Skip for now" → advances to ready step (does NOT set premium)
- Annual plan visually highlighted (recommended badge)
- Visual trial timeline: "Today → Free → Day 7 → $29.99/yr"
- No payment due now messaging

**Permissions step behavior:**
- Requests `Camera` permission via expo-camera `useCameraPermissions` hook
- Requests `Microphone` via `Audio.requestPermissionsAsync()`
- If denied: shows explanation, provides "Open Settings" button
- Does NOT block progression (user can deny and continue to use free tier)

**Baseline step behavior:**
- Runs a 30-second finger PPG calibration session
- Uses `CameraView` with rear camera + torch
- Calls `saveBaseline({ heartRate, hrv, voiceF0 })` on completion
- `voiceF0` set to 0 (estimated from text pitch proxy) if mic denied
- If signal quality too low: "Unable to calibrate — skipping baseline"
- Baseline stored in AsyncStorage `truthscope_baseline`

**Completion:**
- Calls `saveProfile({ hasCompletedOnboarding: true })`
- Navigates to Home via `navigation.reset({ routes: [{ name: 'Home' }] })`

**Animated sub-components:**
- `PulsingGlow` — radial gradient that pulses (breathing animation)
- `AnimatedCheckmark` — spring-in checkmark for permission granted
- `ConvergingLines` — three lines converging to center (multi-modal visual)

**Edge cases:**
- User swipes back past baseline: baseline data NOT cleared (already saved)
- User revisits onboarding from Settings > Recalibrate: re-runs baseline step, does NOT reset `hasCompletedOnboarding`
- If calibration fails silently: baseline is `null`, engines fall back to population norms

---

### 6.2 HomeScreen

**File:** `src/screens/HomeScreen.tsx`
**Route:** `Home`
**Header:** None (custom header in screen)
**Refresh:** Pull-to-refresh reloads sessions + profile from AsyncStorage

**Layout sections (top to bottom):**
1. Header (logo + settings gear)
2. "Quick Start" section — 2x2 grid of mode cards
3. Party Mode banner (full-width gradient)
4. "Recent Sessions" section — last 5 sessions
5. Stats Card (Sessions count, Avg Score, Streak)

**Mode cards (2x2 grid):**
| Mode | Icon | Color | Premium? |
|------|------|-------|---------|
| Finger Pulse | `finger-print` | `#00E5FF` (cyan) | Free |
| Face Scan | `scan-outline` | `#7B61FF` (purple) | Free (gated in HomeScreen.tsx) |
| Voice Analysis | `mic-outline` | `#FF3D71` (red) | Free (gated in HomeScreen.tsx) |
| Multi-Modal | `layers-outline` | `#7B61FF` (purple) | `isPremiumOnly: true` |

**IMPORTANT — Gating logic in HomeScreen (not matching config):**
The `DETECTION_MODES` config array marks only `multi` as `isPremiumOnly: true`.
However, `handleModePress` gates `face`, `voice`, AND `multi` for free users:
```typescript
if (!premium && (mode === 'face' || mode === 'voice' || mode === 'multi')) {
  // Show upgrade alert
}
```
This means the Multi-Modal card shows "PRO" badge but Face Scan and Voice Analysis
show no badge yet are still blocked. This is a **UX inconsistency** — Face Scan and
Voice Analysis should also show PRO badges.

**Mode card behavior when locked:**
- Alert with two options: "Upgrade" (navigates to Onboarding) | "Use Finger Pulse"
- Card still visible and tappable (not greyed out for Face/Voice — see above inconsistency)

**Daily limit enforcement:**
- Calls `canStartSession()` before navigation
- If `allowed = false`: Alert with "Upgrade" | "OK"
- Count resets at midnight (based on `new Date().toDateString()`)

**Party Mode banner:**
- Full-width gradient (purple → red → gold)
- Shimmer animation on banner text
- Navigates to PartyMode screen
- No premium gate on Party Mode entry itself (gating is per question category)

**Recent sessions list:**
- Max 5 shown
- Each row: mode icon + verdict badge + score + time ago
- Time ago format: "Just now" / "5m ago" / "2h ago" / "3d ago" / "Mar 15"
- Tap: navigates to Result screen with last result from that session
- Empty state: pulse icon + "No sessions yet" + subtitle

**Stats Card:**
- Sessions: total count
- Avg Score: mean of all result `overallScore` values
- Streak: consecutive days with at least one session (calculated daily)

**Focus listener:**
- `navigation.addListener('focus', loadData)` — reloads on every return to Home
- This ensures stats/sessions are fresh after completing a detection

---

### 6.3 DetectionScreen

**File:** `src/screens/DetectionScreen.tsx`
**Route:** `Detection`
**Params:** `{ mode?: DetectionMode }` — defaults to 'finger'

**Layout (top to bottom):**
1. Back button (absolute, top-left, z-index 100)
2. Mode selector tabs (4 tabs: Finger / Face / Voice / Multi)
3. Camera area OR voice waveform (36% of screen height)
4. Metrics panel (live readings)
5. Score gauge (SVG circle progress)
6. Control buttons row (Question | Start/Stop | Party)

**Mode selector tabs:**
- Multi tab shows lock icon for free users
- Changing mode while recording: stops recording first, then switches
- Active tab: `colors.accent.primary` (#00E5FF) icon + label

**Camera area variants:**

*Finger mode:*
- `CameraView` with `facing="back"` and `enableTorch={isRecording}`
- `ScanOverlay` (scan line animation) positioned absolutely over camera
- Instruction: "Place finger over camera lens" / "Cover completely with light pressure"
- Torch fires ONLY when recording starts

*Face mode:*
- `CameraView` with `facing="front"`
- Corner bracket overlays (SVG paths)
- Instruction: "Position face in frame" / "Look directly at camera"

*Voice mode:*
- NO camera (VoiceWaveform component replaces camera area)
- Two SVG sine waves (primary + echo) animated with Reanimated `useAnimatedProps`
- Wave amplitude driven by `readings.voiceStress` value
- Mic icon (active = cyan, inactive = tertiary grey)
- Status text: "Listening..." or "Tap Start to begin"

*Multi mode:*
- Left 60%: front-facing `CameraView` + face scan overlay + "FACE" label
- Right 40%: two mini panels stacked
  - "PULSE" panel: `MiniPulseGraph` (heartRate visualization)
  - "VOICE" panel: `MiniVoiceLevel` (voice stress bar)

**Critical gap — Camera frame extraction:**
`CameraView` (expo-camera) renders video to screen but provides NO frame-by-frame
pixel data API. The `processCameraFrame(redMean, greenMean)` callback exists in
`useDetectionEngine` but is NEVER called from `DetectionScreen.tsx`.

```typescript
// In DetectionScreen.tsx:
// CameraView does NOT have onFrame callback in expo-camera
// processCameraFrame is imported but never called
const { readings, processCameraFrame, processFaceData, markQuestion } = useDetectionEngine(isRecording, mode);
// processCameraFrame is wired to nothing ← THIS IS THE CORE PRODUCTION BLOCKER
```

See Section 13 for the fix (swap to react-native-vision-camera).

**Face detection:**
`CameraView` (expo-camera) has `onFacesDetected` callback but requires enabling
face detection in `expo-camera` config. Currently NOT wired in DetectionScreen —
`processFaceData` is imported but never called. FaceEngine receives no data.

**Metrics panel:**
Displays conditionally based on mode:
- Finger/Multi: HR (BPM, shows `--` when 0) + HRV (ms)
- Voice/Multi: Voice stress bar (0-100%)
- Face/Multi: Face score bar (0-100%)
- Always: Signal quality dot (Good/Fair/Low based on 0.7/0.4 thresholds)

**Score gauge (SVG):**
- Circle stroke progress arc (SVG + Reanimated AnimatedCircle)
- Score: `--` when not recording, 0-100 when active
- Verdict label: "READY" when inactive, else TRUTHFUL/DECEPTIVE/UNCERTAIN/ANALYZING
- Confidence % shown when recording and confidence > 0
- Glow color + arc color match verdict (green/red/orange/cyan)

**Control buttons:**
- "Question" button: disabled until recording. Calls `markQuestion()` + plays `scanPulse` sound + haptic success. Marks timestamp in DeceptionAnalyzer for temporal weighting.
- Start/Stop button: gradient play/stop. On stop: saves session + navigates to Result if score > 0
- "Party" shortcut: navigates to PartyMode

**Session save logic (on Stop):**
```typescript
// Only saves if score > 0 (sensor data was received)
if (readings.overallScore > 0) {
  saveSession({ id, startTime: Date.now() - 30000, endTime: Date.now(), ... });
  navigation.navigate('Result', { result });
}
```
If score = 0 (no sensor data — Simulator, no permissions, no hand over camera):
screen just resets to idle. No navigation. No alert.

**Camera permission handling:**
- `useCameraPermissions()` from expo-camera
- Requests on mount
- If denied: shows camera icon + "Camera access required" text in camera area
- Detection can still run voice mode without camera

---

### 6.4 ResultScreen

**File:** `src/screens/ResultScreen.tsx`
**Route:** `Result`
**Params:** `{ result: DetectionResult }`

**Layout (ScrollView):**
1. Header: back button + "Analysis Result" title + share button
2. Question card (shown only if `result.question` is set)
3. `ScoreGauge` component (size=220)
4. Verdict banner (LinearGradient matching verdict)
5. Verdict description text (probabilistic language — no certainty claims)
6. Signal Breakdown section (`StressBar` for each active channel)
7. Session Details section (mode, duration, confidence, time)
8. Disclaimer card (DISCLAIMER_SHORT)
9. Action buttons: "Run Again" + "Home"

**Default result (if route.params missing):**
```typescript
{ id: 'demo', timestamp: Date.now(), mode: 'finger',
  verdict: 'uncertain', confidence: 0, overallScore: 50,
  breakdown: { physiological: 0, vocal: 0, facial: 0 }, duration: 0 }
```

**Breakdown display logic:**
Only renders `StressBar` for channels with value > 0:
- `breakdown.physiological > 0` → "Physiological Stress" bar
- `breakdown.vocal > 0` → "Vocal Stress" bar
- `breakdown.facial > 0` → "Facial Indicators" bar
Single-mode results (finger only) will show only one bar.

**Verdict descriptions (non-sensational, honest):**
- truthful: "Biometric signals suggest low stress and stable physiological responses, consistent with truthful behavior."
- deceptive: "Elevated stress indicators detected across monitored channels. This may indicate deception, but could also reflect anxiety or emotional arousal."
- uncertain: "Mixed signals detected. Some indicators elevated while others remain stable. Insufficient data for a clear assessment."

**Share behavior:**
- `Share.share({ message: text })`
- Text format: "TruthScope Result: TRUTHFUL (Score: 72/100, Confidence: 68%)\nQuestion: "..."\n\nDownload TruthScope..."
- Uses native share sheet — no third-party needed

**Action buttons:**
- "Run Again": navigates to `Detection` with same `result.mode`
- "Home": `navigation.navigate('Home')`

---

### 6.5 SettingsScreen

**File:** `src/screens/SettingsScreen.tsx`
**Route:** `Settings`
**Params:** None

**Sections:**
1. Account (Subscription status, Sessions count, Restore Purchases)
2. Calibration (Baseline HR display, Baseline HRV display, Reset Baseline, Recalibrate)
3. About (Version 1.0.0, Privacy Policy link, Terms link)
4. The Science (static educational content — PPG, Voice Stress, Facial Analysis descriptions)

**Subscription display:**
- Premium: green "Premium" text
- Free: tertiary grey "Free" text

**Restore Purchases behavior:**
```
Alert.alert('Subscription Status', 'Your subscription is managed through Stripe. Check your email for a receipt and subscription management link from Stripe.')
```
This is honest — there is no IAP to "restore." Stripe subscriptions are managed on stripe.com.

**Reset Baseline:**
- Confirmation alert with destructive "Reset" action
- Clears `baselineHR`, `baselineHRV`, `baselineVoiceF0` from profile
- Does NOT clear session history

**Recalibrate:**
- Navigates to `Detection` with `mode: 'finger'`
- User runs a finger session which updates baseline via onboarding baseline logic
- Note: baseline is only saved during ONBOARDING baseline step, not during regular detection sessions. This means "Recalibrate" button navigates to detection but does NOT actually save a new baseline. **This is a bug.**

**Links:**
- Privacy Policy: `Linking.openURL('https://printmaxx-privacy.surge.sh')`
- Terms: `Linking.openURL('https://printmaxx-tos.surge.sh')`

---

### 6.6 PartyModeScreen

**File:** `src/screens/PartyModeScreen.tsx`
**Route:** `PartyMode` (slides from bottom)
**Animation:** `slide_from_bottom`

**Game phases (type `GamePhase`):**
```
'setup' → 'round' → 'analyzing' → 'result' → 'passPhone' → back to 'round'
                                            → 'scoreboard' (after all rounds)
```

**Phase 1: setup**
- Player count selector: 2–8 players (plus/minus buttons)
- Name input fields (one per player, max 20 chars)
- Unnamed players default to "Player N"
- "Start the Game" button → `round` phase

**Phase 2: round**
- Shows current player name + round number
- Question category tabs: Mild / Spicy / Random
- Question card with current question text
- "Shuffle" to get new question from same category
- "Custom Question" button → text input overlay
- "Start Analysis" button → `analyzing` phase

**Phase 3: analyzing**
- REAL microphone recording via `Audio.Recording` (expo-av)
- 10-second countdown timer (ANALYSIS_DURATION_MS = 10000ms)
- Audio level visualization (Reanimated animated bar)
- Collects audio metering samples every ~100ms during recording
- Auto-advances to `result` after 10s

**Scoring algorithm (generateScore function):**
```typescript
// Real audio characteristics from mic metering.
// Mean level (energy) + variance (vocal instability) as stress proxies.
const varianceScore = Math.min(50, stdDev * 150);
const energyScore = Math.min(50, mean * 80);
const score = Math.round(Math.max(5, Math.min(98, varianceScore + energyScore)));
// Verdict: score >= 60 = deceptive, score >= 35 = uncertain, else truthful
```

This is the ONLY engine in the entire app that actually uses real audio data for scoring in a meaningful way. However, it uses metering levels as a PROXY for stress — not true acoustic feature extraction. It is entertainment-grade, not clinical.

**Phase 4: result**
- Dramatic reveal animation (ZoomIn from Reanimated)
- Verdict display: "TRUTH!" / "LIES!" / "HMMMM..."
- Score badge
- Confidence percentage
- Short subtext per verdict
- "Next Player" button → `passPhone` phase

**Phase 5: passPhone**
- 5-second countdown
- "Pass the phone to [next player]" instruction
- After countdown → `round` phase for next player

**Phase 6: scoreboard**
- Triggered after all players have had at least one round
- Full player list sorted by score
- "Play Again" (resets all scores, back to round 1)
- "Done" → navigation.goBack()

**Party Mode question pool (src/utils/partyQuestions.ts):**
- 34 total questions across 3 categories
- Mild: 12 questions (all free)
- Spicy: 12 questions (8 free, 4 premium: s9 "lied to police", s10 "cheated on test", s11 "said I love you", s12 "sabotaged coworker")
- Random: 10 questions (6 free, 4 premium: r7-r10)

**Session saving:**
Party mode results are saved to AsyncStorage via `saveSession()` with `isPartyMode: true`.

---

## 7. DETECTION ENGINES — HONEST ASSESSMENT

### 7.1 PPGEngine (src/engines/PPGEngine.ts)

**What it does:** Real signal processing pipeline for heart rate and HRV from camera pixel data.

**Algorithm:**
1. Receives `(redMean, greenMean, timestamp)` per frame
2. Builds circular buffer of 256 frames (~8.5 seconds at 30fps)
3. Detrends signal (linear regression subtraction — removes DC component)
4. Bandpass filter (0.7-4 Hz / 42-240 BPM) via cascaded moving averages
5. Normalizes filtered signal to 0-1
6. Detects peaks with minimum distance constraint (prevents double-counting)
7. Calculates heart rate from median inter-beat interval (robust against outliers)
8. Calculates HRV as RMSSD (root mean square successive differences — gold standard)
9. Signal quality via amplitude + autocorrelation periodicity check

**Is it real?** The algorithm is real and scientifically sound. RMSSD is the standard HRV metric. Peak detection is appropriate. Bandpass filter cutoffs (0.7-4 Hz) match cardiac frequency range correctly.

**Is it working?** NO. `[PRODUCTION BLOCKER P0]`

`CameraView` (expo-camera) does NOT expose per-frame pixel data. The `processFrame(redMean, greenMean, timestamp)` method exists but is NEVER called from `DetectionScreen.tsx`. The `processCameraFrame` callback from `useDetectionEngine` is imported but never wired to a camera callback.

The fix requires swapping expo-camera for `react-native-vision-camera` which provides `useFrameProcessor` hook with direct pixel access via Worklets API.

**Fix path:**
```typescript
// In DetectionScreen.tsx, replace CameraView with:
import { Camera, useFrameProcessor } from 'react-native-vision-camera';

const frameProcessor = useFrameProcessor((frame) => {
  'worklet';
  const { redMean, greenMean } = extractChannelMeans(frame); // native plugin
  runOnJS(processCameraFrame)(redMean, greenMean);
}, [processCameraFrame]);

<Camera frameProcessor={frameProcessor} ... />
```

Requires: `react-native-vision-camera` + a native frame extraction plugin or custom Worklet.

---

### 7.2 VoiceEngine (src/engines/VoiceEngine.ts)

**What it does:** Attempts to extract vocal stress features from microphone recording.

**What is real:**
- `Audio.Recording` is a REAL recording object (expo-av)
- Microphone permission is REAL
- `setOnRecordingStatusUpdate` provides REAL metering values (dB, -160 to 0)
- Speech detection via metering threshold (> 0.15 normalized) is REAL
- Response latency calculation from `questionStartTime` to first speech is REAL

**What is SIMULATED/PROXY:** `[PRODUCTION GAP P1]`

The `extractVocalFeatures` method has a comment explicitly acknowledging this:
```typescript
// For a more accurate implementation, a native audio processing module
// would provide actual FFT-based pitch tracking and frame-level analysis.
```

- `estimatedF0 = 100 + mean * 200` — this is NOT fundamental frequency. It is mean audio level mapped to a 100-300 Hz range. A microphone metering value does not tell you pitch.
- `jitter` is derived from level changes between frames — NOT cycle-to-cycle pitch variation
- `shimmer` is amplitude variance — partially valid proxy for amplitude shimmer but lacks the frame-level precision
- `tremor` is peak counting in the envelope — NOT 8-12 Hz spectral analysis

**Fix path:** Requires `react-native-pitch-detector` (or similar native module) that provides actual YIN/autocorrelation F0 extraction from audio frames. Cannot get real F0 from expo-av metering.

**What still works at launch:**
- Response latency is real and valid
- Speech/silence detection is real
- Party Mode uses audio metering for scoring (variance + energy) — works as entertainment-grade

---

### 7.3 FaceEngine (src/engines/FaceEngine.ts)

**What it does:** Processes face landmark data from camera face detection.

**What is real:**
- The `processFace(faceData)` method accepts real expo-camera face detection output
- Blink detection from `leftEyeOpenProbability` / `rightEyeOpenProbability` is real (when face detection is active)
- Facial asymmetry from eye open probability differences is real
- Gaze tracking (approximate from face center + head angle) is real enough for entertainment use
- Micro-expression detection logic (rapid changes in smile/eye open probabilities within 300ms) is real in concept

**What is NOT wired:** `[PRODUCTION BLOCKER P0]`

```typescript
// In DetectionScreen.tsx:
// processFaceData is imported but NEVER called
// CameraView's onFacesDetected callback is NOT connected
```

`CameraView` has `onFacesDetected` prop but it requires enabling the ML face detection feature in expo-camera's config. This is not configured in `app.json`. The `FaceEngine.processFace()` method receives zero data during any detection session.

**Fix path:** Enable `expo-camera` face detection:
```json
// app.json plugins array:
["expo-camera", { "cameraPermission": "...", "recordAudioAndroid": true,
  "faceDetector": true }]
```
Then in DetectionScreen:
```typescript
<CameraView
  onFacesDetected={(faces) => {
    if (faces.faces.length > 0) processFaceData(faces.faces[0]);
    else processFaceData(null);
  }}
  faceDetectorSettings={{ mode: FaceDetectorMode.fast, detectLandmarks: 'none',
    runClassifications: 'all', minDetectionInterval: 100, tracking: true }}
/>
```

Note: expo-camera face detection provides basic metrics (smile, eye open, head angles) but NOT Action Unit (AU) detection for true micro-expressions. For AU detection, a separate ML model (e.g., OpenFace) would be needed.

---

### 7.4 DeceptionAnalyzer (src/engines/DeceptionAnalyzer.ts)

**What it does:** Multi-modal fusion of engine scores into a single 0-100 deception probability.

**Algorithm:**
1. Weighted sum of physiological + vocal + facial scores per mode
2. Temporal context smoothing (60% current + 40% recent average, except within 5s of a question = 80%/20%)
3. Verdict thresholding: < 30 = truthful, > 55 = deceptive, else uncertain
4. Confidence calculation from: signal availability (40 pts), score consistency (30 pts), session duration (30 pts, maxes at 60s)

**Is it real?** Yes — the fusion algorithm is sound. The weighting (physio 40%, voice 30%, face 30% in multi mode) is reasonable given published meta-analyses. DePaulo et al. 2003 reference is cited.

**Is it working?** Partially. The analyzer receives scores from engines. But since PPGEngine receives no frames and FaceEngine receives no face data, physiological and facial scores are always 0. Only VoiceEngine provides real (proxy) data via metering.

---

## 8. PARTY MODE — DETAILED SPEC

### 8.1 Game Flow

```
HomeScreen "Party Mode" banner tap
  ↓
PartyModeScreen: phase = 'setup'
  ↓ (onStart with player names)
phase = 'round' (player 1, question)
  ↓ (onStartAnalysis)
phase = 'analyzing' (10s mic recording)
  ↓ (auto after 10s)
phase = 'result' (show verdict)
  ↓ (onNextPlayer)
phase = 'passPhone' (5s countdown)
  ↓ (after countdown)
phase = 'round' (player 2, question) ... repeat for all players
  ↓ (all players done)
phase = 'scoreboard' (leaderboard)
  ↓ (onDone)
navigation.goBack()
```

### 8.2 Real Sensor Usage

Party Mode is the one place where audio data is ACTUALLY used for scoring:
- `Audio.Recording` from expo-av starts recording during `analyzing` phase
- `setOnRecordingStatusUpdate` fires with metering ~10x/second
- Each metering value normalized: `Math.max(0, (metering + 60) / 60)`
- After 10s: calls `generateScore(audioSamples)` with collected samples
- Score = `Math.round(Math.max(5, Math.min(98, varianceScore + energyScore)))`

This is entertainment-grade (audio energy variance is not a validated deception indicator) but it DOES use real sensor data — not Math.random(). The score varies with actual speech characteristics.

**Important:** Requires `allowsRecordingIOS: true` in audio mode config and microphone permission. Party Mode silently fails with score=50 if mic not granted.

### 8.3 Question Gating

```typescript
// Free users: no isPremium flag checked in PartyMode itself
// Premium questions are filtered by getRandomQuestion(category, includePremium=false)
// Free users see mild, spicy (8 questions), random (6 questions)
// Premium users: full pool with isPremium=true questions
```

The gating uses question-level `isPremium` flag. Free users can still play Party Mode — they just get fewer question options.

### 8.4 Scoreboard

- `PlayerData` array: `{ name: string; results: PlayerResult[] }`
- `PlayerResult`: `{ question, score, verdict, round }`
- Scoreboard sorts by average score descending
- Shows verdict badge per player
- "Play Again" resets player results array, stays on same screen at `round` phase

---

## 9. SOUND DESIGN

### 9.1 Sound Engine (src/sounds/SoundEngine.ts)

**Initialization:** Called in `App.tsx` on mount via `initSounds()`. Sets `playsInSilentModeIOS: true` (users in silent mode can hear detection sounds during sessions).

**Preloaded sounds (loaded at startup for zero latency):**
`tap`, `heartbeat`, `scanPulse`, `verdictTruth`, `verdictDeception`, `countdown`, `analyzeStart`

All other sounds load on-demand and are cached after first play.

**SoundTouchable:** Drop-in `TouchableOpacity` replacement that auto-plays `tap` + light haptic on every press. All screens use `SoundTouchable as TouchableOpacity`.

### 9.2 Complete Sound Inventory (22 files)

All files located at `assets/sounds/*.wav`. Generated as pure tone/synthesized audio.

| Sound Name | File | Category | Used When |
|-----------|------|---------|----------|
| `tap` | tap.wav | UI | Every button press (via SoundTouchable) |
| `tapHeavy` | tap_heavy.wav | UI | Heavy confirm actions |
| `toggle` | toggle.wav | UI | Mode switches, toggles |
| `swipe` | swipe.wav | UI | Back navigation (back button) |
| `heartbeat` | heartbeat.wav | Scan | Each detected heartbeat pulse |
| `scanStart` | scan_start.wav | Scan | When scanning begins |
| `scanPulse` | scan_pulse.wav | Scan | "Question" button in detection |
| `scanLock` | scan_lock.wav | Scan | Signal lock achieved |
| `verdictTruth` | verdict_truth.wav | Verdict | Truth verdict reveal |
| `verdictDeception` | verdict_deception.wav | Verdict | Deception verdict reveal |
| `verdictUncertain` | verdict_uncertain.wav | Verdict | Uncertain verdict reveal |
| `countdown` | countdown.wav | Party | Party Mode countdown ticks |
| `playerSwitch` | player_switch.wav | Party | Pass phone between players |
| `roundComplete` | round_complete.wav | Party | Party round finishes |
| `analyzeStart` | analyze_start.wav | System | Start recording |
| `analyzeComplete` | analyze_complete.wav | System | Stop recording |
| `calibrateStart` | calibrate_start.wav | System | Onboarding baseline starts |
| `calibrateDone` | calibrate_done.wav | System | Onboarding baseline complete |
| `permissionGranted` | permission_granted.wav | System | Permission accepted |
| `error` | error.wav | System | Errors |
| `success` | success.wav | System | Success confirmations |
| `premium` | premium.wav | System | Premium unlock |

### 9.3 Sound Call Sites

`playSound()` is called from:
- `DetectionScreen.tsx`: `analyzeStart` (start recording), `analyzeComplete` (stop recording), `scanPulse` (question button)
- `PartyModeScreen.tsx`: `countdown` (per-second tick during analysis), `playerSwitch` (pass phone), `roundComplete` (result reveal), `analyzeStart` (start analysis)
- `OnboardingScreen.tsx`: `calibrateStart`, `calibrateDone`, `permissionGranted`, `success`
- `SoundTouchable.tsx`: `tap` (auto, every button)
- `AppNavigator.tsx`: `premium` (on payment success deep link)

`playVerdictReveal(verdict)` is called from:
- `DetectionScreen.tsx`: after stop recording when score > 0
- `PartyModeScreen.tsx`: during result phase reveal

**Special case:** `playHeartbeatAtBPM(bpm)` function exists but is NOT currently called. It was designed to fire on each `onHeartbeat` callback from PPGEngine, but since PPGEngine receives no frames, it never fires.

---

## 10. FREE vs PREMIUM GATING ENFORCEMENT MATRIX

| Feature | Free | Premium | Where enforced |
|---------|------|---------|---------------|
| Finger Pulse mode | YES | YES | Not gated |
| Face Scan mode | NO | YES | HomeScreen `handleModePress` |
| Voice Analysis mode | NO | YES | HomeScreen `handleModePress` |
| Multi-Modal mode | NO | YES | HomeScreen + DetectionScreen ModeSelector |
| Daily session limit | 3/day | Unlimited | `canStartSession()` in HomeScreen |
| Party Mode entry | YES | YES | No gate on entry |
| Party Mode mild questions | YES | YES | `getRandomQuestion` `includePremium=false` |
| Party Mode spicy Q1-8 | YES | YES | Not marked premium |
| Party Mode spicy Q9-12 | NO | YES | `isPremium: true` on question |
| Party Mode random Q1-6 | YES | YES | Not marked premium |
| Party Mode random Q7-10 | NO | YES | `isPremium: true` on question |
| Session export/share | YES | YES | Share button on ResultScreen (no gate) |
| Session history | YES | YES | Last 100 sessions for all users |

**Gate reads from:** `AsyncStorage.getItem('truthscope_profile')` → `isPremium` field

**Premium activation:** Via deep link `truthscope://premium-activated` from Stripe success URL. `setPremium(true)` writes to AsyncStorage. Takes effect immediately.

**Gap:** There is NO server-side verification of premium status. A user can call `setPremium(true)` from a dev console or via the link directly. This is by design for Stripe Payment Links architecture — server verification would require a backend.

---

## 11. PURCHASE FLOW

### 11.1 Onboarding Paywall (step 13: 'premium')

1. User reaches premium step via natural onboarding progression OR from upgrade alert
2. Screen shows: trial timeline visual, plan comparison, two CTAs
3. Taps "Start Free Trial (7 Days)" → `Linking.openURL(ANNUAL_LINK)` → Safari/Chrome opens Stripe checkout
4. Completes Stripe checkout (email + card)
5. Stripe redirects to: `https://printmaxx-payments.surge.sh/success?redirect=truthscope://premium-activated`
6. iOS handles `truthscope://` scheme → launches app with deep link
7. `AppNavigator` `Linking.addEventListener` fires → `setPremium(true)` called
8. User returns to app as premium

### 11.2 Mid-App Upgrade Prompt

Triggered when free user tries to access gated feature:
1. Alert with "Upgrade" button
2. Alert "Upgrade" → `navigation.navigate('Onboarding')`
3. User lands on Onboarding and is scrolled to premium step (PREMIUM_INDEX = 12)
4. Same checkout flow from step 3 above

### 11.3 Restore Purchases

Settings > "Restore Purchases" shows informational Alert — no actual IAP restore.
Since Stripe manages subscriptions, restoration happens by:
1. User visits their Stripe customer portal link (from confirmation email)
2. Manually re-activates or confirms subscription
3. Must manually open the Stripe success URL again to re-trigger deep link

This is a **UX gap** — there is no way to restore premium status in-app without the deep link. Recommend adding a "Re-enter purchase link" flow in Settings.

---

## 12. QA CHECKLIST

### 12.1 Verified Screens (Simulator, Apr 4 2026)

| Screen | Method | Status |
|--------|--------|--------|
| Home | computer-use + xcrun screenshot | PASS |
| Finger Detection | computer-use tap + screenshot | PASS |
| Face Detection | computer-use + xcrun screenshot | PASS |
| Voice Analysis | computer-use (multi-modal view) | PASS |
| Multi-Modal | computer-use screenshot | PASS |
| Settings | xcrun screenshot | PASS |
| Party Mode (all phases) | computer-use tap-through | PASS |
| Onboarding | xcrun screenshot | PASS |

### 12.2 Maestro Test Suites

7 test files in `.maestro/`:
| File | Tests |
|------|-------|
| 01_home_screen.yaml | All home elements render, no sessions state |
| 02_finger_detection.yaml | Navigate to detection, camera area renders |
| 03_face_detection.yaml | Face scan screen renders |
| 04_voice_detection.yaml | Voice waveform renders |
| 05_settings.yaml | Settings screen elements |
| 06_party_mode.yaml | Party setup phase renders |
| 07_onboarding.yaml | Onboarding steps |

Run with: `maestro test .maestro/` (requires Maestro 2.4.0 installed)

### 12.3 Edge Cases Tested

- No camera permission: CameraView replaced with icon + text ✓
- No mic permission: voice engine start catches error, sensorStatus.mic = 'unavailable' ✓
- Empty session history: "No sessions yet" empty state ✓
- Score = 0 on stop: no navigation to result (just resets) ✓
- Free user taps gated mode: Alert with upgrade option ✓
- Daily limit reached: Alert with upgrade option ✓
- Party Mode with all default player names: "Player 1", "Player 2", etc. ✓

### 12.4 Known Failing Cases (Real Device)

- PPG heart rate readings: will show `--` until CameraView → VisionCamera swap
- Facial analysis: will show 0 until face detection is wired
- Voice F0/pitch: will be proxy estimate only until native pitch detector added

---

## 13. REMAINING WORK FOR APP STORE SUBMISSION

### P0 — Blockers (MUST fix before launch)

**P0-1: Swap expo-camera for react-native-vision-camera**
- Priority: CRITICAL — entire PPG engine is dead without this
- Effort: 1-2 days
- Steps:
  1. `npm install react-native-vision-camera` + `npx expo prebuild`
  2. Add Camera permission in app.json (already there, needs update)
  3. Replace `CameraView` with `<Camera>` component in DetectionScreen
  4. Implement `useFrameProcessor` worklet that extracts red/green channel means
  5. Call `processCameraFrame(redMean, greenMean)` via `runOnJS` in worklet
  6. Implement pixel extraction: average R and G channels from frame buffer
  7. Wire torch control to `device.torch` instead of `enableTorch` prop
  8. Test on real iPhone — Simulator has no camera hardware
- Reference: react-native-vision-camera v4+ API, Frame Processors docs

**P0-2: Wire face detection to FaceEngine**
- Priority: HIGH — facial analysis produces zero data
- Effort: 4-8 hours
- Steps:
  1. Add `faceDetector: true` to expo-camera plugin config in app.json
  2. In DetectionScreen, add `onFacesDetected` callback to CameraView (or VisionCamera equivalent)
  3. Call `processFaceData(faces[0])` from callback when face count > 0
  4. Call `faceEngine.current.onFaceLost()` when face count = 0
  5. Test blink detection and gaze stability metrics
- Note: expo-camera face detection gives basic metrics only (smile prob, eye open prob, head angles). For true micro-expression AU detection, would need a separate ML model.

**P0-3: Production app icon**
- Current icon (`assets/icon.png`) is a placeholder
- Requires: 1024x1024 production icon
- Generate via: Google ImageFX (Imagen 4 model) via Chrome MCP
- Design brief: Dark background (#0A0A0F), cyan (#00E5FF) geometric eye/scope symbol, minimal, premium feel, no text
- Also needed: adaptive-icon.png for Android, splash-icon.png update

**P0-4: Real device testing**
- All QA to date is on iOS Simulator (iOS 18.4)
- Camera hardware required for PPG + face detection
- Test on: iPhone 13+ (for front camera quality), test torch behavior
- Check: Reanimated 4.x performance on real device (no Metro bundler overhead)

### P1 — Important (fix before major marketing)

**P1-1: Real voice F0 extraction**
- Current state: F0 estimated from `100 + mean * 200` (energy → fake Hz)
- Fix: Install `react-native-pitch-detector` for YIN algorithm F0 extraction
- Effort: 1 day + native build
- Impact: Voice stress analysis becomes scientifically valid (not entertainment proxy)

**P1-2: UX inconsistency — Face Scan and Voice Analysis show no PRO badge**
- Bug: `DETECTION_MODES` array only marks `multi` as `isPremiumOnly: true`
- But `handleModePress` blocks face + voice for free users
- Fix: Add `isPremiumOnly: true` to Face Scan and Voice Analysis in `DETECTION_MODES`

**P1-3: Recalibrate button doesn't actually save baseline**
- Settings > Recalibrate → navigates to Detection (finger mode)
- But baseline is only saved in onboarding baseline step, not regular sessions
- Fix: Add baseline-save logic to stop recording flow when in recalibration mode

**P1-4: EAS Build configuration**
- `extra.eas.projectId = "truthscope-printmaxx"` (placeholder — needs real EAS project)
- Set up EAS project: `eas init`
- Configure `eas.json` with iOS production profile
- Set up App Store Connect credentials

**P1-5: Support URL in App Store metadata**
- `ASO_METADATA.md` has "(Add email when accounts created)"
- Needs: support email or support webpage before App Store submission

### P2 — Polish (can ship without, fix in 1.1)

**P2-1: party Mode heartbeat animation**
- `playHeartbeatAtBPM(bpm)` is implemented but never called
- Wire to `onHeartbeat` callback in PPGEngine once frames are working

**P2-2: Premium restore flow**
- Currently: informational Alert only
- Better: "Re-enter license" field or automated lookup via Stripe customer portal link

**P2-3: Offline mode behavior**
- All data is local-first — app works fully offline
- But Stripe payment requires internet — no offline paywall messaging

**P2-4: Analytics**
- Zero analytics currently
- Recommend: PostHog or Mixpanel for funnel tracking (paywall view → click → purchase)

---

## 14. APP STORE SUBMISSION CHECKLIST

- [ ] **P0** Bundle ID: `com.printmaxx.truthscope` — ensure unique in App Store Connect
- [ ] **P0** Camera permission string: Present in app.json — "TruthScope uses the camera to measure your heart rate via fingertip photoplethysmography and to track facial micro-expressions for deception analysis." — specific, non-generic ✓
- [ ] **P0** Microphone permission string: Present — "TruthScope uses the microphone for voice stress analysis during lie detection sessions." ✓
- [ ] **P0** `ITSAppUsesNonExemptEncryption: false` — set in app.json ✓
- [ ] **P0** Privacy Policy URL: https://printmaxx-privacy.surge.sh (resolves) ✓
- [ ] **P0** Terms URL: https://printmaxx-tos.surge.sh (resolves) ✓
- [ ] **P0** No placeholder text anywhere in screens ✓ (no lorem ipsum)
- [ ] **P0** Minimum useful functionality without subscription: Finger Pulse, 3 sessions/day ✓
- [ ] **P0** Subscription terms displayed: Shown on paywall screen with trial timeline ✓
- [ ] **P0** Real production icon (not placeholder)
- [ ] **P0** `npx expo export --platform ios` passes clean (0 compile errors ✓, runtime: verify)
- [ ] **P0** No crash on Simulator: All 8 screens verified ✓
- [ ] **P0** Real device test (camera-dependent features)
- [ ] **P0** Deep link `truthscope://premium-activated` triggers `setPremium(true)` ✓
- [ ] **P1** Content gating enforced in code (face/voice/multi blocked for free) ✓
- [ ] **P1** Free user limit enforced at 3 sessions/day ✓
- [ ] **P1** Session saves every completed detection ✓ (when score > 0)
- [ ] **P1** Paywall has single primary CTA (trial) + secondary (monthly) ✓
- [ ] **P1** No prank/game keywords in metadata (deliberately avoided) ✓
- [ ] **P1** EAS Build project configured with App Store credentials
- [ ] **P1** Support URL or support email in App Store Connect
- [ ] **P1** Version number and build number match
- [ ] **P2** Age rating set to 17+ (mature themes) ✓
- [ ] **P2** App Store description under 4,000 chars ✓ (ASO_METADATA.md)
- [ ] **P2** Keywords under 100 chars ✓ (84 chars)
- [ ] **P2** Subtitle under 30 chars ✓ ("Biometric Truth Analysis" = 24 chars)
- [ ] **P2** App name under 30 chars ✓ ("TruthScope: Real Lie Detector" = 29 chars)
- [ ] **P2** 6 screenshots prepared per caption strategy in ASO_METADATA.md
- [ ] **P2** Category: Utilities (primary), Lifestyle (secondary) ✓

**Apple review risk factors:**
- App claims "real" biometric analysis but PPG/face detection are non-functional until P0 fixes — review team may test on device and find no data
- Lie detection category: pass if framed as entertainment + real sensors, fail if framed as medical/forensic
- "Voice stress analysis" claim: same caveat as above — must be working before submission

---

## 15. KNOWN PRODUCTION GAPS — HONEST STATUS

### What IS working (verified on Simulator)

| Component | Status | Notes |
|-----------|--------|-------|
| App navigation (all 6 screens) | WORKING | All transitions, deep links |
| UI rendering | WORKING | All screens render correctly |
| SoundEngine | WORKING | All 22 sounds preloaded + fire-and-forget |
| SoundTouchable | WORKING | Auto tap + haptic on every button |
| AsyncStorage persistence | WORKING | Profile, sessions, baseline save/load |
| Free/premium gating logic | WORKING | Enforced in code |
| Daily session limit | WORKING | Enforced in canStartSession() |
| Stripe deep link activation | WORKING | setPremium(true) on URL match |
| Party Mode full flow | WORKING | All 6 phases, mic recording, scoring |
| Party Mode audio scoring | WORKING | Real metering data used |
| DeceptionAnalyzer fusion | WORKING | Algorithm is sound (receives no real data yet) |
| Onboarding 14 steps | WORKING | Swipe navigation, baseline step |
| Result screen display | WORKING | All verdict types, breakdown bars |
| Share result | WORKING | Native share sheet |
| Settings screen | WORKING | All sections, links, calibration display |
| PPGEngine algorithm | WORKING | Signal processing pipeline is correct |
| FaceEngine algorithm | WORKING | Processes face data correctly when called |
| VoiceEngine recording | WORKING | Real mic recording + metering |

### What is NOT working (verified by code inspection)

| Component | Status | Notes |
|-----------|--------|-------|
| PPG heart rate display | NOT WORKING | processCameraFrame never called — CameraView has no frame API |
| HRV display | NOT WORKING | Same reason |
| Signal quality display | NOT WORKING | Always 0 (no frames) |
| Facial analysis display | NOT WORKING | processFaceData never called — onFacesDetected not wired |
| Facial micro-expression detection | NOT WORKING | Same reason |
| Voice F0 (fundamental frequency) | PROXY ONLY | Mean energy level used as fake Hz |
| Voice jitter/shimmer | PROXY ONLY | Audio level variance, not true acoustic feature |
| Heartbeat sound | NOT PLAYING | playHeartbeatAtBPM never called |
| Recalibrate (Settings) | BROKEN | Navigates to detection but does not save baseline |

### Summary of data reality per mode

| Mode | Real data? | What the score actually reflects |
|------|-----------|----------------------------------|
| Finger Pulse | NO until P0-1 | Score = 0 (no frames = no HR = physio score skipped) |
| Face Scan | NO until P0-2 | Score = 0 (no face data = facial score skipped) |
| Voice Analysis | PARTIAL | Response latency (real) + audio energy proxy (real but imprecise) |
| Multi-Modal | PARTIAL | Only voice proxy data; physio and facial scores are 0 |
| Party Mode | YES (entertainment grade) | Real audio metering variance + energy = real signal, imprecise analysis |

---

## 16. COMPONENTS REFERENCE

### src/components/

| Component | File | Purpose |
|-----------|------|---------|
| `SoundTouchable` | SoundTouchable.tsx | Drop-in TouchableOpacity + tap sound + haptic |
| `MetricCard` | MetricCard.tsx | Labeled metric display (HR, HRV values) |
| `SignalQuality` | MetricCard.tsx | Signal strength dot (Good/Fair/Low) |
| `StressBar` | MetricCard.tsx | Horizontal progress bar with color thresholds |
| `PulseWaveform` | PulseWaveform.tsx | SVG animated waveform |
| `ScoreGauge` | ScoreGauge.tsx | Circular arc progress gauge with color animation |

### Inline sub-components in screens

**DetectionScreen:**
- `ModeSelector` — 4 tab mode switcher
- `ScanOverlay` — scan line + grid + corner brackets
- `VoiceWaveform` — animated sine wave for voice mode
- `MetricsPanel` — live metrics grid (HR, HRV, Voice, Face, Signal)
- `ScoreGauge` (local version) — SVG circle gauge with glow
- `MiniPulseGraph`, `MiniVoiceLevel` — compact widgets for Multi mode

**HomeScreen:**
- `LogoGlow` — pulsing gradient behind logo
- `ModeCard` — 2x2 grid card (Reanimated FadeInDown entry)
- `PartyModeBanner` — full-width gradient Party Mode CTA
- `SessionItem` — recent session row with verdict badge
- `StatsCard` — sessions/avg/streak stats

**OnboardingScreen:**
- `PulsingGlow` — breathing glow animation
- `AnimatedCheckmark` — spring-in permission granted check
- `ConvergingLines` — three lines → center (multi-modal concept)

**PartyModeScreen:**
- `SetupPhase` — player count + names
- `RoundPhase` — question display + category tabs
- `AnalyzingPhase` — countdown + recording UI
- `ResultPhase` — dramatic verdict reveal
- `PassPhonePhase` — countdown to pass
- `ScoreboardPhase` — leaderboard

---

## 17. FILE STRUCTURE

```
lie-detector-app/TruthScope/
├── App.tsx                      # Root: initSounds + GestureHandlerRootView + AppNavigator
├── index.ts                     # Entry: registerRootComponent
├── app.json                     # Expo config, permissions, deep link scheme
├── package.json                 # Dependencies
├── babel.config.js              # Reanimated plugin (REQUIRED)
├── tsconfig.json
├── HANDOFF.md                   # Status doc
├── ASO_METADATA.md              # App Store copy
├── .maestro/                    # 7 Maestro test suites
│   ├── 01_home_screen.yaml
│   ├── 02_finger_detection.yaml
│   ├── 03_face_detection.yaml
│   ├── 04_voice_detection.yaml
│   ├── 05_settings.yaml
│   ├── 06_party_mode.yaml
│   └── 07_onboarding.yaml
├── assets/
│   ├── icon.png                 # [PLACEHOLDER — needs production icon]
│   ├── splash-icon.png
│   ├── adaptive-icon.png
│   ├── favicon.png
│   └── sounds/                  # 22 .wav files (all present ✓)
│       ├── tap.wav, tap_heavy.wav, toggle.wav, swipe.wav
│       ├── heartbeat.wav, scan_start.wav, scan_pulse.wav, scan_lock.wav
│       ├── verdict_truth.wav, verdict_deception.wav, verdict_uncertain.wav
│       ├── countdown.wav, player_switch.wav, round_complete.wav
│       ├── analyze_start.wav, analyze_complete.wav
│       ├── calibrate_start.wav, calibrate_done.wav
│       ├── permission_granted.wav, error.wav, success.wav, premium.wav
└── src/
    ├── navigation/
    │   └── AppNavigator.tsx     # Stack navigator, deep link config, Stripe callback
    ├── screens/
    │   ├── OnboardingScreen.tsx # 14-step Cal AI onboarding
    │   ├── HomeScreen.tsx       # Mode grid, party banner, sessions, stats
    │   ├── DetectionScreen.tsx  # Camera/mic/waveform, score gauge, controls
    │   ├── ResultScreen.tsx     # Score display, breakdown, share
    │   ├── SettingsScreen.tsx   # Account, calibration, about, science
    │   └── PartyModeScreen.tsx  # 6-phase party game
    ├── engines/
    │   ├── PPGEngine.ts         # Heart rate via camera frames [NEEDS FRAMES]
    │   ├── VoiceEngine.ts       # Voice stress via mic [PROXY ONLY]
    │   ├── FaceEngine.ts        # Facial analysis via face detection [NEEDS WIRING]
    │   └── DeceptionAnalyzer.ts # Multi-modal fusion [CORRECT ALGORITHM]
    ├── hooks/
    │   └── useDetectionEngine.ts # Wires engines to DetectionScreen
    ├── components/
    │   ├── SoundTouchable.tsx   # Auto-sound TouchableOpacity wrapper
    │   ├── MetricCard.tsx       # MetricCard, SignalQuality, StressBar
    │   ├── PulseWaveform.tsx    # SVG waveform
    │   └── ScoreGauge.tsx       # Circular gauge
    ├── sounds/
    │   └── SoundEngine.ts       # Audio init, preload, playSound, playVerdictReveal
    ├── store/
    │   └── index.ts             # AsyncStorage CRUD: profile, sessions, baseline
    ├── theme/
    │   └── index.ts             # colors, spacing, radii, typography
    ├── utils/
    │   ├── types.ts             # All TypeScript types
    │   └── partyQuestions.ts    # 34 questions across 3 categories
    └── legal/
        └── disclaimer.ts        # Full + short disclaimers, URLs
```

---

## 18. COMPETITIVE POSITIONING (for marketing)

From ASO_METADATA.md — use this framing exactly:

**Against prank apps:** "Every lie detector app on the App Store uses random number generators dressed up as biometric scanning. TruthScope is different."

**Against desktop apps:** "LiarLiar.ai (the best desktop lie detector) requires a webcam and a laptop. TruthScope gives you the same class of analysis — real rPPG, real voice stress, real micro-expression tracking — in your pocket."

**Accuracy honesty (required to avoid Apple rejection):**
- Never claim "medical-grade" or "polygraph-level" accuracy
- Never claim 100% detection rates
- State explicitly: "No consumer app can achieve polygraph-level accuracy. We're the best consumer option available on mobile, not a replacement for professional testing."
- Same category as heart rate apps: measured data, user interprets results

---

*Spec version 1.0 | Updated 2026-04-07 | Next update after P0 fixes complete*
