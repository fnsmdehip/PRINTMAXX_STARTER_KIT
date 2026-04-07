# PRD: NutriSnap — Production-Quality App Spec
# Version: 1.0 — Full Edge-Case Hardened
# Date: 2026-04-07
# Status: READY FOR ONE-SHOT BUILD

> This spec covers every screen, every edge case, every security boundary, and every
> App Store requirement. An agent reading ONLY this doc should be able to build NutriSnap
> to production quality without asking clarifying questions.

---

## 1. APP OVERVIEW

**Name:** NutriSnap
**Bundle ID:** com.printmaxx.nutrisnap
**Slug:** nutrisnap
**URL Scheme:** nutrisnap://
**Tagline:** AI Food Scanner & Calorie Log
**App Store Subtitle:** AI Food Scanner & Calorie Log
**Category:** Health & Fitness
**Target User:** Anyone who wants to track calories and macros without manual entry. One tap to photograph a meal and get calorie + macro breakdown. Primary demographic: 18-45, weight-conscious, fitness-adjacent. Not hardcore bodybuilders (they use MyFitnessPal). This is the lazy person's calorie tracker.
**Monetization:** Stripe Payment Links — Annual $29.99, Monthly $4.99
**Free Tier:** 3 AI food scans per day, weekly analytics only (no monthly view), no ad-free (ads stub in code but removed for compliance simplicity)

---

## 2. TECH STACK

| Layer | Library | Version |
|-------|---------|---------|
| Framework | Expo SDK | ~52.0.0 |
| Language | TypeScript strict | ^5.8.3 |
| Navigation | @react-navigation/native + native-stack + bottom-tabs | ^7.x |
| Stack navigator | @react-navigation/stack | ^7.2.10 |
| State | Redux Toolkit + redux-persist | ^2.2.6 / ^6.0.0 |
| Persistence | @react-native-async-storage/async-storage | 1.23.1 |
| Camera | expo-camera (CameraView API) | ~15.0.14 |
| Image picker | expo-image-picker | ~15.1.0 |
| Image processing | expo-image-manipulator | ~12.0.5 |
| AI food scanning | Google Gemini 1.5 Flash (REST API) | generativelanguage.googleapis.com/v1 |
| Charts | react-native-chart-kit (LineChart, PieChart) | ^6.12.0 |
| SVG (calorie ring) | react-native-svg | 15.2.0 |
| Animations | react-native-reanimated | ~3.10.1 |
| Gradients | expo-linear-gradient | ~13.0.2 |
| Haptics | expo-haptics | ~13.0.1 |
| Sound | expo-av | ~15.0.2 |
| Store review | expo-store-review | ~7.0.1 |
| Notifications | expo-notifications | ~0.28.10 |
| Updates | expo-updates | ~0.25.18 |
| Safe area | react-native-safe-area-context | 4.10.5 |
| Icons | @expo/vector-icons (Ionicons) | ^14.0.2 |
| Payment | Stripe Payment Links via Linking.openURL | — |
| Ad service | REMOVED (no-op stubs only) | — |
| HealthKit | react-native-health (installed, not wired to UI yet) | ^1.19.0 |
| Date picker | @react-native-community/datetimepicker | 8.0.1 |

**Build command (native, required for expo-camera 15.x):**
```bash
npx expo prebuild --platform ios && npx expo run:ios
```
Never use `expo start --ios` — expo-camera's CameraView requires a native build, not Expo Go.

**EAS Project ID:** 04c7bff1-f241-49d8-9c24-b4ee680c1579
**EAS Owner:** fnsmdehip

---

## 3. DATA TYPES (canonical)

```typescript
// ─── Store: userSlice ──────────────────────────────────────────────
type Gender = 'male' | 'female' | 'other';
type Goal = 'lose' | 'maintain' | 'gain';
type ActivityLevel = 'sedentary' | 'light' | 'moderate' | 'very_active' | 'athlete';
type DietType = 'regular' | 'pescatarian' | 'vegetarian' | 'vegan';
type DietPreference = 'none' | 'vegetarian' | 'vegan' | 'keto' | 'paleo' | 'gluten_free';
type GoalTimeline = '1_month' | '3_months' | '6_months' | '1_year';

interface UserProfile {
  gender: Gender | null;
  age: number | null;            // range 20-80
  heightCm: number | null;       // converted from feet/inches at save
  weightKg: number | null;       // converted from lbs at save
  goalWeight: number | null;     // kg
  goal: Goal | null;
  activityLevel: ActivityLevel | null;
  dietType: DietType | null;
  dietPreference: DietPreference | null;
  goalTimeline: GoalTimeline | null;
  dailyCalories: number;         // default 2000
  proteinGoal: number;           // grams, default 150
  carbGoal: number;              // grams, default 200
  fatGoal: number;               // grams, default 70
  useImperial: boolean;          // default true (lbs/feet)
}

interface UserState {
  isAuthenticated: boolean;
  hasCompletedOnboarding: boolean;
  userProfile: UserProfile;
  onboardingProgress: number;
}

// ─── Store: nutritionSlice ─────────────────────────────────────────
interface Food {
  id: string;         // food-<timestamp>
  name: string;       // from Gemini: e.g. "Spaghetti Bolognese"
  calories: number;   // rounded to nearest integer
  protein: number;    // grams, rounded
  carbs: number;      // grams, rounded
  fat: number;        // grams, rounded
  imageUrl?: string;  // local URI of captured photo
  timestamp: number;  // Date.now() milliseconds
}

interface NutritionState {
  dailyGoal: {
    calories: number;   // default 2000
    protein: number;    // default 150g
    carbs: number;      // default 200g
    fat: number;        // default 70g
  };
  consumedItems: { [date: string]: Food[] };  // date key = ISO YYYY-MM-DD
  processing: boolean;
  processingStatus: string;
  activeDate: string;  // ISO YYYY-MM-DD (today on mount)
}

// ─── Store: subscriptionSlice ──────────────────────────────────────
type SubscriptionTier = 'free' | 'monthly' | 'yearly' | 'lifetime';

interface SubscriptionState {
  tier: SubscriptionTier;           // default 'free'
  isPremium: boolean;               // true if tier !== 'free'
  dailyScansUsed: number;           // resets at midnight
  dailyScanLimit: number;           // 3 for free, 999 for premium
  lastScanResetDate: string;        // ISO date, used for midnight reset logic
  foodScansCompleted: number;       // total since install (for store review trigger)
  isLoading: boolean;
  error: string | null;
}

// ─── Gemini API response shape (Camera.tsx) ─────────────────────────
interface GeminiNutritionResponse {
  name: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}
```

---

## 4. CONSTANTS

### Stripe Payment Links (hardcoded in purchases.ts)
| Plan | Price | Stripe Link |
|------|-------|-------------|
| Annual | $29.99/year ($2.50/mo) | https://buy.stripe.com/7sY6oI9XWaZTdxTdj93F60x |
| Monthly | $4.99/month | https://buy.stripe.com/cNi14oc647NH8dzfrh3F60y |
| AsyncStorage key | — | `@nutrisnap_premium` |
| Value when premium | — | `'true'` (string) |

### Onboarding
| Constant | Value |
|----------|-------|
| TOTAL_STEPS | 16 (steps 0-15) |
| Default height | 5'10" |
| Default current weight | 170 lbs |
| Default target weight | 155 lbs |
| Default age | 30 |
| Default timeline | 3_months |
| Default diet | none |
| Weight range | 80-400 lbs (5-lb increments) |
| Height range (feet) | 4-7 |
| Height range (inches) | 0-11 |
| Age range | 20-80 |

### Free Tier Limits
| Feature | Free | Premium |
|---------|------|---------|
| Daily AI scans | 3 | Unlimited (999) |
| Analytics - weekly view | Yes | Yes |
| Analytics - monthly view | No (gated, redirects to paywall) | Yes |
| Ads | Removed (no-op) | Removed |

### Scan Reset Logic
Daily scan count resets when `lastScanResetDate !== today (ISO date)`. When a new day is detected at scan time (in `incrementDailyScans`), `dailyScansUsed` resets to 1 (counts the current scan) and `lastScanResetDate` is updated to today.

### Store Review Trigger
Fired when the 5th total food item is logged across all days. Implemented in `Camera.tsx confirmAndSave`: counts total items in `consumedItems`, fires when count equals 4 before the `addConsumedItem` dispatch (making it 5 after). Uses `expo-store-review`. 2-second delay before prompt. Non-critical — errors silently swallowed.

### Deep Link: Premium Activation
The URL scheme `nutrisnap://premium-activated` (also `nutrisnap://payment-success`) sets premium status to true. Wired in App.tsx via `Linking.addEventListener`. Stripe success URL should be configured to this deep link so returning users from checkout get auto-activated.

---

## 5. TDEE CALCULATION ENGINE (nutrition.ts)

### Formula: Mifflin-St Jeor BMR
```
Male:   10 * weight_kg + 6.25 * height_cm - 5 * age + 5
Female: 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
Other:  average of male/female (midpoint = -78)
```

### Activity Multipliers
| Level | Multiplier |
|-------|-----------|
| sedentary | 1.2 |
| light | 1.375 |
| moderate | 1.55 |
| very_active | 1.725 |
| athlete | 1.9 |

### Calorie Adjustment by Goal
| Goal | Adjustment |
|------|-----------|
| lose | TDEE - 500 |
| maintain | TDEE |
| gain | TDEE + 300 |

### Macro Split Algorithm
1. **Protein:** `min(weight_lbs * 0.8, dailyCalories * 0.30 / 4)` grams
2. **Fat:** `dailyCalories * 0.25 / 9` grams
3. **Carbs:** `(dailyCalories - protein_kcal - fat_kcal) / 4` grams (never negative)

### Unit Conversions
```
feetInchesToCm(feet, inches) = Math.round((feet * 12 + inches) * 2.54)
lbsToKg(lbs) = lbs * 0.453592
kgToLbs(kg) = kg * 2.20462
```

### Weight Goal Estimation
```
lose goal: weeks = ceil(diff_lbs / 1.0)   — ~1 lb/week
gain goal: weeks = ceil(diff_lbs / 0.5)   — ~0.5 lb/week
maintain: 0 weeks
```

### Weight Projection Curve
Smooth exponential ease (1 - (1-progress)^2). Used in onboarding Screen 8 graph.

---

## 6. AI FOOD SCANNING ENGINE (Camera.tsx)

### Which AI
**Google Gemini 1.5 Flash** (REST API, NOT SDK). Endpoint:
```
https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_AI_API_KEY}
```

### API Key Handling
Key is read from `Constants.expoConfig?.extra?.googleAiApiKey` (Expo `app.json` extra, injected from `GOOGLE_AI_API_KEY` env var). If missing, `GEMINI_API_KEY` is empty string and all scan attempts will fail with a 400/403. **Production requirement: set GOOGLE_AI_API_KEY in EAS secret or env.** This is the only AI integration — no OpenAI, no Claude, no other model.

### Image Pre-processing
Before Gemini call:
1. `ImageManipulator.manipulateAsync(uri, [{ resize: { width: 768 } }], { compress: 0.7, format: JPEG, base64: true })`
2. Image is resized to max 768px width, compressed to 70% quality, encoded as base64 JPEG inline data

### Gemini Prompt (exact)
```
"Analyze this food image. Return ONLY a valid JSON object with these exact keys: "name" (string, the food name), "calories" (number, estimated total kcal), "protein" (number, grams), "carbs" (number, grams), "fat" (number, grams). No markdown, no explanation, just the JSON object."
```
`temperature: 0.1`, `maxOutputTokens: 256`

### Response Parsing
1. Strip markdown code fences (` ```json `, ` ``` `)
2. `JSON.parse()` the cleaned text
3. Validate all 5 fields exist with correct types (name=string, others=number)
4. Round all numbers to integers
5. On any error: show Alert "Analysis Failed, please try again"

### Scan Gate (free tier enforcement)
Before calling Gemini, in `analyzePicture`:
```typescript
if (!isPremium && scansRemaining !== null && scansRemaining <= 0) {
  // Show "Daily Limit Reached" Alert with Upgrade button
  // Navigate to Paywall if user taps Upgrade
  return;
}
```
`scansRemaining = isPremium ? null : Math.max(0, dailyScanLimit - dailyScansUsed)`

### Scan Counter
`incrementDailyScans()` is dispatched AFTER successful Gemini response (not before). Counter includes midnight reset logic. `foodScansCompleted` is a cumulative count for store review trigger.

---

## 7. NAVIGATION STRUCTURE

```
App (Provider + PersistGate)
  └── AppContent (phase manager)
        ├── phase='splash'     → SplashScreen (auto-advances ~2.5s)
        ├── phase='onboarding' → OnboardingFlow (16 steps, handles paywall)
        └── phase='app'        → NavigationContainer
              └── Stack.Navigator
                    ├── Main (default) → MainTabs (bottom tab navigator)
                    │     ├── Home      → HomeScreen        (label: "Today")
                    │     ├── Camera    → CameraScreen      (label: "Scan")
                    │     ├── Analytics → AnalyticsScreen   (label: "Insights")
                    │     └── Settings  → SettingsScreen    (label: "Settings")
                    └── Paywall (modal presentation) → PaywallScreen
```

### Tab Bar Config
- Background: `#1A2B45` (surface)
- Active tint: `#2ED573` (primary green)
- Inactive tint: `#6B7280`
- Height: 88, paddingBottom: 28, paddingTop: 8
- All tab presses trigger `haptics.light()`

### Phase Logic (App.tsx AppContent)
1. Always starts at `splash` phase
2. On splash finish: check `redux.user.hasCompletedOnboarding`
   - true → `app`
   - false → `onboarding`
3. Onboarding complete callback → `app`

### Premium Status Check on Startup
On App mount: `initPurchases()` then `checkEntitlements()` → dispatches `setPremiumStatus()` to Redux. Reads from `@nutrisnap_premium` AsyncStorage key. Fallback: sets `isPremium = false` on any error.

---

## 8. SCREEN-BY-SCREEN SPEC

### Screen 0: SplashScreen
**Purpose:** Animated brand intro, resolves to onboarding or main app.
**Duration:** ~2.5s total (spring animations + 600ms delay + 350ms fade out)
**Animation sequence:**
1. Logo icon (leaf) springs in + fades in (300ms)
2. Ring border springs in (250ms)
3. Title "NutriSnap" slides up + fades in (350ms)
4. Subtitle "Smart nutrition tracking" fades in (300ms)
5. 600ms hold
6. Full screen fades out (350ms) → `onFinish()` callback
7. Logo pulses (1.0-1.08 scale, 1s loop) runs throughout, stops on finish
**States:** single state, no interaction
**Back navigation:** none (not a nav screen, AppContent phase)

---

### OnboardingFlow (16 Steps, Steps 0-15)

**Container behavior:**
- Progress bar at top (animated from 0-100% across steps 0-15)
- Back chevron (step > 0 and step < 15): calls `goBack()` which animates slide-right
- At step 15 (paywall): X icon calls `handleDeclinePaywall()`
- Step 0: placeholder (no back button)
- Step transitions: fade + slide (150ms out, 200ms in)
- Sound: `playSound('swipe')` on every step advance or retreat
- Haptics: `haptics.light()` on every step change

---

#### Step 0: Welcome
**Shows:**
- Large gradient circle with scan icon (72px) + food emojis (salad, apple, avocado)
- Hero title: "Track calories effortlessly with AI"
- Subtitle: "Just snap a photo of your food. NutriSnap identifies it instantly."
- 3 badges: "Instant AI scan", "95% accuracy", "50K+ users"
- "Get Started" button with forward arrow
**Gate:** always advanceable (no gate)
**Data collected:** none

---

#### Step 1: Goal Selection
**Shows:** 4 goal option cards in a 2x2 grid
**Options:**
| key | label | icon | desc |
|-----|-------|------|------|
| lose | Lose weight | trending-down | Burn fat and get lean |
| gain | Gain muscle | trending-up | Build strength and size |
| maintain | Maintain weight | swap-horizontal | Stay where you are |
| healthier | Eat healthier | leaf | Better nutrition habits |

**Note:** 'healthier' maps to `Goal = 'maintain'` internally via `effectiveGoal` derived state: `selectedGoal === 'healthier' ? 'maintain' : selectedGoal`
**Gate:** requires selectedGoal !== null
**Data stored:** `selectedGoal` (local state in OnboardingFlow)

---

#### Step 2: Current Stats (Height + Weight)
**Shows:**
- Height picker: +/- buttons for feet (4-7) and inches (0-11), imperial always
- Current weight picker: +/- circle buttons, 5-lb steps, range 80-400 lbs, displays "NNN lbs"
**Gate:** always advanceable (defaults pre-set: 5'10", 170 lbs)
**Data stored:** `heightFeet`, `heightInches`, `weightLbs`

---

#### Step 3: Target Weight + Timeline
**Title:** varies by goal:
- lose: "What's your goal weight?"
- gain: "What weight do you want to reach?"
- maintain: "Let's set a healthy target"

**Shows:**
- Target weight picker: same +/- style, 5-lb steps, 80-400 lbs, default 155 lbs
- Timeline chips: "1 month", "3 months", "6 months", "1 year"
**Gate:** always advanceable (defaults pre-set)
**Data stored:** `targetWeightLbs`, `selectedTimeline`

---

#### Step 4: Activity Level
**Shows:** 4 list options (full-width, icon + title + description)
| key | label | desc | icon |
|-----|-------|------|------|
| sedentary | Sedentary | Desk job, little exercise | desktop-outline |
| light | Lightly active | Light exercise 1-3 days/week | walk-outline |
| moderate | Moderately active | Moderate exercise 3-5 days/week | bicycle-outline |
| very_active | Very active | Hard exercise 6-7 days/week | barbell-outline |

**Gate:** requires selectedActivity !== null
**Data stored:** `selectedActivity`

---

#### Step 5: Dietary Preferences
**Shows:** 6 chips in a 2-col-ish wrap
| key | label | icon |
|-----|-------|------|
| none | No preference | restaurant-outline |
| vegetarian | Vegetarian | leaf-outline |
| vegan | Vegan | flower-outline |
| keto | Keto | flame-outline |
| paleo | Paleo | fish-outline |
| gluten_free | Gluten-free | nutrition-outline |

**Gate:** always advanceable (default 'none')
**Data stored:** `selectedDiet`

---

#### Step 6: Biological Sex
**Shows:** 2 option cards (Male / Female) with Ionicon
**Note:** 'other' gender is supported in the data type but NOT shown as an onboarding option. Onboarding only offers male/female. 'other' gender defaults BMR to midpoint between male and female.
**Gate:** requires selectedGender !== null
**Data stored:** `selectedGender`

---

#### Step 7: Age
**Shows:** +/- buttons, range 20-80, default 30, "years old" label
**Gate:** always advanceable (default set)
**Data stored:** `selectedAge`

---

#### Step 8: Validation (Goal Achievable + Weight Graph)
**Computes:** TDEE plan from all collected data via `calculateFullPlan()`
**Shows:**
- Badge icon (checkmark-circle)
- Title: "Your goal is achievable!" or "Ambitious but doable!" (if rate > 2 lbs/week)
- Subtitle: loss/gain amount + timeline or "maintain at X lbs"
- For non-maintain: weight projection graph (custom dot-based visualization, NOT react-native-chart-kit here)
  - Y-axis: current weight (top) and target weight (bottom) or vice-versa
  - Dots distributed exponentially along the curve
- Stats row: daily calories | protein grams | rate lbs/week (or "Balanced" for maintain)
**Gate:** always advanceable
**Data stored:** none (derived from previous steps)

---

#### Step 9: Calorie Breakdown (Macro Pie)
**Title:** "Your daily nutrition"
**Shows:**
- "Pie chart" visualization (actually stacked flex bars in a ring container with center text)
- Center: `{plan.dailyCalories} cal/day`
- 3 colored segments: protein (red #FF6B6B), carbs (green #2ED573), fat (blue #5B8DEF)
- 3 macro cards with grams and % of total calories
**Gate:** always advanceable

---

#### Step 10: Social Proof
**Title:** "Join 50,000+ users tracking smarter"
**Shows:**
- 3 testimonial cards with avatar initial, name, 5-star rating, and quote text:
  - Sarah M.: "Lost 22 lbs in 3 months just by scanning my meals."
  - James K.: "So much easier than manually logging everything."
  - Priya R.: "The AI accuracy is unreal. Saved me hours every week."
- Social proof banner: "4.9 ★ | 50K+ users | #1 AI tracker"
**Gate:** always advanceable

---

#### Step 11: Magic Moment (AI Demo)
**Title:** "See how it works"
**Shows:**
- Camera viewfinder mockup (static green-tinted frame with corner indicators and scan line)
- Center food emoji: 🍝
- "Detected" overlay showing hardcoded demo result:
  - "Spaghetti Bolognese", 520 cal, 28g protein, 62g carbs, 18g fat
- Caption: "Point. Snap. Track. That simple."
**Note:** This is a STATIC demo. No real camera is invoked here.
**Gate:** always advanceable

---

#### Step 12: Feature Showcase
**Title:** "Everything you need"
**Shows:** 5 feature items in a list with icon + title + desc:
| icon | title | desc |
|------|-------|------|
| camera | AI Food Scan | Point your camera at any meal |
| nutrition | Macro Tracking | Detailed macro breakdown |
| time | Meal History | Track everything you eat |
| trending-up | Progress Tracking | Watch your journey unfold |
| pie-chart | Macro Breakdown | Protein, carbs, and fat |

**Gate:** always advanceable

---

#### Step 13: Notification Permission
**Title:** "Stay on track"
**Shows:**
- Large notification bell icon in gradient circle
- Notification preview mockup card: "Time to log lunch!" + "You've had 820 cal so far..."
- "Enable Reminders" (primary button) — sets `notifRequested = true` then advances
- "Maybe later" (secondary button) — advances without requesting
**Note:** `expo-notifications` is installed but `Notifications.requestPermissionsAsync()` is NOT called here. Code comment says "In a real app, call Notifications.requestPermissionsAsync() here". **P1 gap: notification permission is never actually requested.**
**Gate:** always advanceable

---

#### Step 14: Plan Ready
**Title:** "Your personalized nutrition plan is ready!"
**Shows:**
- Green checkmark badge with gradient
- Summary card with rows: Daily Calories, Protein, Carbs, Fat, Goal, Timeline (if not maintain)
- All values from `plan` (calculateFullPlan result)
- CTA: "Unlock My Plan" with lock-open icon
**Gate:** always advanceable

---

#### Step 15: Paywall (Onboarding)
**Two states:** main paywall or rescue offer (shown after first decline tap on X)

**Main paywall state:**
- 3-dot trial timeline: Today FREE → Day 2 Reminder → Day 3 Billing
- "No payment due now" text
- Monthly plan card: $9.99/month (anchor price — note: this is $9.99, NOT the $4.99 shown in Paywall.tsx)
- Annual plan card: $29.99/year, "BEST VALUE" badge, "$2.50/mo - Save 79%", yearly selected by default
- 4 benefits: Unlimited AI food scans, Detailed macro tracking, Progress insights & trends, Monthly analytics view
- "Start My Free Trial" CTA (gradient green button)
- "Cancel anytime. No commitment."
- Social proof: "4.9 ★ | 50,000+ users"
- "Restore purchases" link

**PRICING DISCREPANCY TO NOTE:** The onboarding paywall shows Monthly at $9.99 as an anchor price. The in-app Paywall.tsx screen shows Monthly at $4.99. Both point to the same `STRIPE_MONTHLY_LINK` ($4.99 actual). The $9.99 in onboarding is a visual anchor-pricing trick (not what gets charged — Stripe charges $4.99). This is NOT a bug intentionally but creates user expectation mismatch. **P2 issue: anchor price in onboarding doesn't match actual Stripe charge.**

**Purchase handler (`handlePurchase`):**
1. Get offerings → select annual or monthly pkg based on `selectedPlan`
2. Call `purchasePackage(pkg)` → opens Stripe URL in browser
3. Wait for app to return to foreground
4. Show Alert: "Did you complete your payment?" (Yes / No)
5. On Yes: `AsyncStorage.setItem('@nutrisnap_premium', 'true')` → dispatch `setPremiumStatus(true)` → `playSound('premium')` → `saveOnboardingData()` → `onComplete()`
6. On No: throws `PurchaseCancelledError` (silently caught)

**Decline / X button behavior:**
1. First X tap: sets `showRescue = true` (shows rescue offer, does NOT exit)
2. Second decline (rescue offer "No thanks"): calls `saveOnboardingData()` + `onComplete()` → enters app as free user

**Rescue offer state:**
- Header: gift emoji + "Wait! Special offer just for you"
- Original price: $29.99/year (strikethrough)
- Rescue price: $19.99/year ("That's just $1.67/month", "Still includes 3-day free trial")
- "Claim This Offer" CTA (gold gradient) → same `handleRescuePurchase` which uses annual Stripe link (charges $29.99 regardless — $19.99 is display only, NOT a separate Stripe product). **P0 gap: rescue offer claims $19.99 but charges $29.99. Needs a separate Stripe price or the rescue offer text must match actual charge.**
- "No thanks, continue with free" → `saveOnboardingData()` + `onComplete()`

---

### HomeScreen (Main tab: "Today")

**Layout:**
- LinearGradient header (#0F2240 → #0B1A2E, top 35%)
- SafeAreaView inside
- Pull-to-refresh (800ms fake refresh, no data reload needed)
- FAB (floating camera button) bottom-right, opens Camera tab

**Header row:**
- Left: "Good {Morning/Afternoon/Evening}" (time-based) + date string (e.g. "Monday, April 7")
- Right (free users only): scan badge showing "{N} scans left" with camera icon, taps → Paywall

**Calorie Ring Card:**
- SVG Circle with stroke-dashoffset progress indicator (green → red when over goal)
- Center: "{remaining} cal left" (large number) + "cal left" label
- Right side: Goal, Consumed, Remaining values in rows
- Ring size: 140px, stroke: 8px
- Ring color: `#2ED573` below goal, `#FF6B6B` at or above goal

**Macro Card:**
- "Macros" section title
- 3 macro bars: Protein (red), Carbs (green), Fat (blue)
- Each shows: dot + label, consumed/goal text, animated progress bar fill
- Progress is `min(1, consumed/goal)` — capped at 100%

**Recently Logged section:**
- "Recently Logged" title
- Empty state: icon + "No food logged yet" + "Scan Food" action button (opens Camera)
- Populated state: food items in reverse-chronological order (newest first via `.slice().reverse()`)
- Each food card: restaurant icon, food name, macros summary (cal · P: Xg · C: Xg · F: Xg), time string (hh:mm AM/PM)
- No swipe-to-delete in current implementation. Tapping a food card only triggers `haptics.light()`. **P2 gap: no way to delete a logged food item from Home screen.**

**Edge cases:**
- `todayItems` keys from `consumedItems[activeDate] ?? []`. If activeDate is not today (nav bug), shows different day's data.
- Over-goal state: calorie ring turns red, no other UI change
- All macros at 100%: bars stay full (no overflow visual)

---

### CameraScreen (Main tab: "Scan")

**4 UI states (state machine):**

**State 1: Loading permissions**
- White pulsing circle placeholder
- No interaction possible

**State 2: Permission denied**
- Camera icon in green circle
- "Camera Access Required" title + explanation text
- If `permission.canAskAgain`: "Grant Camera Access" button → `requestPermission()`
- Else: "Open Settings" button → `Linking.openSettings()`
- Always shows: "Choose from Gallery Instead" link (bypasses camera permission, uses image picker)

**State 3: Live camera view (default)**
- Full-screen `CameraView` (back camera, `facing="back"`)
- Top bar: X (close/go back) | scan badge "{N} scans left" (free only) | gallery icon
- Focus guide: 260x260 rounded-corner frame with 4 corner markers in green
- "Center your food in the frame" text
- Bottom: circular capture button (white ring, white fill, 76px diameter)
- Gallery icon opens `launchImageLibraryAsync` (square crop, 0.8 quality)
- Capture button calls `takePictureAsync({ quality: 0.8 })`

**State 4: Image preview (captured but not analyzed)**
- Full-screen image preview
- Two buttons overlay at bottom:
  - "Retake" (closes icon, dismisses back to camera state)
  - "Analyze Food" (sparkles icon, calls `analyzePicture()`)
- While `isAnalyzing = true`: `AnalyzingOverlay` shown over image
  - Spinning ring + sparkles icon + "Analyzing your food" title
  - 3 animated dots
  - Step list: "Identifying food items" / "Estimating portions" / "Calculating nutrition" (only first is "active" — not truly animated through steps)

**State 5: Analysis result**
- Captured image (260px height, full width)
- Card overlapping image (card has negative marginTop -30)
- Food name (24px bold, centered)
- 4 macro items: Calories | Protein (red) | Carbs (green) | Fat (blue)
- Two buttons:
  - "Retake" (resets all state, back to camera)
  - "Log Food" (dispatches `addConsumedItem`, triggers store review if 5th item, navigates back)

**Scan limit enforcement location:** `analyzePicture()` before Gemini call. Shows Alert with Upgrade option.

**Paywall navigation:** `navigation.navigate('Paywall')` — this requires the parent Stack to have a Paywall screen. CameraScreen is within the Tab navigator which is within the Stack that has Paywall. Works correctly.

---

### AnalyticsScreen (Main tab: "Insights")

**Header:**
- "Analytics" title
- PRO badge (star icon + "PRO" text) shown only when NOT premium; taps → Paywall

**Time range toggle (week / month):**
- Week: always available
- Month: gated — if not premium, tapping the "Monthly" toggle redirects to Paywall and does NOT switch the view
- Monthly toggle shows lock icon (lock-closed, 12px) when not premium

**Chart data sources:**
- `calorieData`: Loops back N days from today, sums `consumedItems[dateKey]` calories. Weekly shows 7 bars/points. Monthly shows every 5th day + last day (to avoid label crowding).
- `macroData`: Sums protein/carbs/fat across the selected day range. Falls back to daily goal values if no data.
- `streak`: Consecutive days back from today with at least 1 food item logged. Max 365.
- `summary`: daysLogged (days with > 0 calories), dailyAvg, goalPercent (dailyAvg / dailyGoal.calories)

**Charts (require react-native-chart-kit):**
1. `LineChart`: Calorie trends with 2 datasets — consumed (green) and daily goal (red, no dots)
2. `PieChart`: Macro distribution (protein/carbs/fat). Uses `absolute` mode (shows gram values not %).

**Empty state:** if no data in any day, shows `EmptyState` component with "Scan Your First Meal" CTA (navigates to Camera tab).

**Premium upsell block:** Always shown at bottom when not premium. "Unlock Full Analytics" card with lock icon and "Go Premium" button.

**Summary stats grid (3 cards):**
- Daily Avg calories (flame icon, red)
- Days Logged count (calendar icon, blue)
- Goal Hit % (trending-up icon, green)

**Streak card:** flame icon + "{N} day logging streak"

---

### SettingsScreen (Main tab: "Settings")

**Subscription section:**
- Card shows: star icon (gold if premium, grey if free) + "NutriSnap Premium/Free" + tier label
- "Manage" (premium) or "Upgrade" (free) button
  - Premium: Alert with link to `https://billing.stripe.com/p/login/printmaxx` (Stripe customer portal)
  - Free: Alert with Upgrade action → navigates to Paywall with `playSound('premium')`
- When premium: shows "Status: Active" badge + "Cancel Subscription" → Alert linking to `https://apps.apple.com/account/subscriptions`
- "Restore Purchases" button (always visible, not just free)
  - Reads `@nutrisnap_premium` from AsyncStorage
  - If 'true': dispatch setPremiumStatus(true), playSound('success'), haptics.success
  - If not found: Alert explaining Stripe subscription management (does NOT set premium)

**Nutrition section (3 rows with chevron — all are Alert placeholders):**
- Daily Goals: shows Alert "Configure your daily calorie and macro targets."
- Units: shows Alert "Unit preferences will be available in a future update."
- Dietary Preferences: shows Alert about profile section.
**P1 gap: None of the Nutrition settings actually open editable UI. All are Alert stubs.**

**Preferences section:**
- Meal Reminders: Switch (local state, not persisted to AsyncStorage, not wiring to notifications system)
- Health Sync (switch): local state, no actual HealthKit integration in UI
**P1 gap: Notification reminders toggle is not persisted and does not wire to expo-notifications.**

**About section:**
- Privacy Policy: opens `https://printmaxx-privacy.surge.sh`
- Terms of Service: opens `https://printmaxx-tos.surge.sh`
- Rate NutriSnap: `StoreReview.requestReview()` (from expo-store-review)
- Support: opens `mailto:support@printmaxx.com`
- App version: `Constants.expoConfig?.version ?? '1.0.0'`

---

### PaywallScreen (Modal stack screen)

**Accessed from:** Home scan badge, Analytics PRO badge, Camera scan limit alert, Settings Upgrade button.

**Layout:** Modal presentation (slides up from bottom).

**Header:** X button (top right, closes modal with `navigation.goBack()`)

**Hero section:**
- Star icon in gold circle
- Personalized headline generated by `getHeadline()`:
  - If user has dailyCalories + goal + goalWeight: "Your {N} calorie plan to reach {X} lbs is ready"
  - If calories + goal: "Your {N} calorie plan is ready"
  - Fallback: "Unlock your personalized nutrition plan"
- Personalized subtext: "Premium gives you the tools to {lose weight / maintain your weight / build muscle} effectively"

**Feature chips (5, wrapping row):**
- Unlimited AI food scans
- Advanced analytics & trends
- Detailed macro breakdown
- Completely ad-free
- Progress analytics

**Plan cards (side by side):**
| Feature | Annual | Monthly |
|---------|--------|---------|
| Title | Annual | Monthly |
| Price | $29.99 | $4.99 |
| Period | /year | /month |
| Per month | $2.50/mo | — |
| Per day | $0.08/day | $0.17/day |
| Badge | "BEST VALUE" (green banner) | — |
| Trial | "7-day free trial" chip | — |
| Default | Selected (radio filled) | Not selected |

**CTA button:** "Start Free Trial" (annual) or "Subscribe Now" (monthly). Gradient from primary colors. Pulses (1.0-1.02 scale loop). Slides up from 30px offset on mount.

**Below CTA:**
- "Cancel anytime. No commitment."
- "Restore Purchases" underlined link

**Legal text (Apple 3.1.1 compliance):**
Full subscription disclosure including: charge at confirmation, auto-renew, manage in App Store settings, unused trial forfeiture.

---

## 9. SOUND DESIGN

### Sound Files (all in `assets/sounds/`)
| File | Triggered on |
|------|-------------|
| tap.wav | General button taps |
| tap_heavy.wav | Heavy tap interactions |
| toggle.wav | Toggle switches |
| swipe.wav | Every onboarding step transition |
| success.wav | Successful operations |
| error.wav | Error states |
| permission_granted.wav | Permission granted |
| premium.wav | Premium purchase success, Upgrade button tap |
| analyze_complete.wav | Food analysis complete (not yet called in code — P2 gap) |

### Preloaded on startup: `tap`, `success`, `toggle`
### All others: lazy loaded on first use
### `playsInSilentModeIOS: true` — sounds play even in silent mode
### Volume: 70% master volume, configurable via `setMuted()` / `getMuted()` / `masterVolume`

### Sound calls currently in code:
- `playSound('swipe')` — every onboarding step transition (goNext / goBack)
- `playSound('premium')` — in Paywall: onboarding purchase success + Settings Upgrade button
- `playSound('success')` — Settings restore purchases success
- `playSound('tap')` — Settings manage subscription button
- **`playSound('analyzeComplete')` is NOT called anywhere.** The `analyze_complete.wav` file exists but is never triggered. P2 gap.

---

## 10. FREE vs PRO GATING ENFORCEMENT MATRIX

| Feature | Gate Location | Gate Mechanism | Grep to verify |
|---------|--------------|----------------|----------------|
| AI food scans (>3/day) | Camera.tsx `analyzePicture()` | `if (!isPremium && scansRemaining <= 0)` | `grep -n "scansRemaining <= 0" app/screens/Camera.tsx` |
| Scan counter badge in header | Camera.tsx CameraView | `{!isPremium && scansRemaining !== null && ...}` | `grep -n "cameraScanBadge" app/screens/Camera.tsx` |
| Scan remaining badge on Home | Home.tsx header | `{!isPremium && scansRemaining !== null && ...}` | `grep -n "scanBadge" app/screens/Home.tsx` |
| Monthly analytics view | Analytics.tsx toggle | `if (isPremium) setTimeRange('month') else navigate('Paywall')` | `grep -n "isPremium" app/screens/Analytics.tsx` |
| PRO badge in Analytics | Analytics.tsx header | `{!isPremium && <premiumBadge/>}` | same file |
| Premium upsell CTA in Analytics | Analytics.tsx bottom | `{!isPremium && <premiumCta/>}` | same file |
| Subscription management | Settings.tsx | `if (isPremium) manage else upgrade` | `grep -n "isPremium" app/screens/Settings.tsx` |
| Paywall accessible from Settings | Settings.tsx | `navigation.navigate('Paywall')` | `grep -n "navigate.*Paywall" app/screens/Settings.tsx` |

**NOT gated (free users can access):**
- Home screen calorie ring and macro bars
- All food logging (scan + history)
- Weekly analytics
- All settings rows (they are stubs anyway)

---

## 11. PURCHASE FLOW (Stripe Payment Links)

### Flow overview
1. User taps "Start Free Trial" / "Subscribe Now"
2. `purchasePackage(pkg)` → `Linking.openURL(stripeLink)` → browser opens
3. App state goes to background
4. `waitForForeground()` monitors `AppState`:
   - Waits for app to go background (wentBackground = true)
   - Then resolves when state returns to 'active'
   - Safety timeout: resolves after 3000ms regardless
5. After foreground return: Alert "Did you complete your payment?" (No / Yes I paid)
6. User says Yes → `AsyncStorage.setItem('@nutrisnap_premium', 'true')` → dispatch `setPremiumStatus(true)`
7. User says No → throws `PurchaseCancelledError` (silently swallowed)

### Restore Purchases
- Reads `AsyncStorage.getItem('@nutrisnap_premium')` → returns `value === 'true'`
- No network call, no Stripe verification

### Known risks
- Honor system: user can tap "Yes I paid" without actually paying. No server-side verification.
- For high-scale, add a webhook + server-side entitlement check.
- `@nutrisnap_premium` key is plain 'true'/'false', not expiry-based. Once set, premium is permanent until app reinstall.

### Deep link activation
`nutrisnap://premium-activated` or `nutrisnap://payment-success` in App.tsx `Linking.addEventListener` sets `@nutrisnap_premium` = JSON with `{isPremium: true, purchasedAt, plan: 'deep-link'}`. NOTE: `checkEntitlements()` checks `value === 'true'` but deep link writes a JSON object string, not the string `'true'`. **P0 bug: deep link activation writes JSON object but restore reads for `=== 'true'`, so deep link restores won't work on next app launch. Needs `AsyncStorage.setItem(STORAGE_KEY, 'true')` (not JSON) in the deep link handler.**

---

## 12. APP STORE SUBMISSION CHECKLIST

### iOS Info.plist permissions (set in app.json infoPlist)
| Permission key | Value |
|----------------|-------|
| NSCameraUsageDescription | "NutriSnap uses your camera to photograph meals and estimate nutritional content including calories, protein, carbs, and fat." |
| NSPhotoLibraryUsageDescription | "NutriSnap needs access to your photos to analyze food images for nutrition tracking." |
| NSHealthShareUsageDescription | "NutriSnap reads your health data to sync nutrition and activity information for a complete wellness overview." |

**Missing permissions to add before submission:**
- No `NSMicrophoneUsageDescription` (not needed — no audio recording)
- No `NSLocationWhenInUseUsageDescription` (not needed)
- If adding HealthKit write: add `NSHealthUpdateUsageDescription`

### Required app.json settings
| Setting | Value | Status |
|---------|-------|--------|
| ITSAppUsesNonExemptEncryption | false | Set |
| UIRequiresFullScreen | true | Set |
| UIStatusBarHidden | false | Set |
| Bundle ID | com.printmaxx.nutrisnap | Set |
| Privacy Policy URL | https://printmaxx-privacy.surge.sh | Set in extra |
| Terms of Service URL | https://printmaxx-tos.surge.sh | Set in extra |
| Support email | support@printmaxx.com | Set in extra |

### Expo plugins
Configured in app.json: `expo-camera`, `expo-image-picker`, `expo-font`
Required before native build: all must be in plugins array.

### Subscription disclosure (Apple 3.1.2)
Legal text present in Paywall.tsx (full disclosure paragraph). Also present as "Cancel anytime" text. Compliant.

### Minimum functionality without subscription
Free users can: scan 3 meals/day, view daily calorie/macro totals, log unlimited items (only scan-based), see weekly analytics. Complies with Apple guideline requiring minimum viable use case for free tier.

---

## 13. KNOWN PRODUCTION GAPS

### P0 — Must fix before shipping

1. **Deep link premium activation bug.** In `App.tsx` deep link handler, `AsyncStorage.setItem` writes a JSON object string (`{isPremium: true, ...}`). But `checkEntitlements()` and `restorePurchases()` both check `value === 'true'`. On next app launch, premium status is lost. Fix: change deep link handler to write `'true'` not `JSON.stringify({...})`.

2. **Rescue offer charges wrong price.** Rescue offer text shows $19.99/year. The actual Stripe link is the $29.99 annual. Either: (a) create a $19.99 Stripe product and use a different URL for rescue, or (b) change rescue offer copy to show $29.99 with a percentage discount framing.

3. **Gemini API key not configured.** `GOOGLE_AI_API_KEY` must be set in EAS secrets or `.env` before building. Without it, all food scans fail silently with a 400 error. The app shows "Analysis Failed" but the root cause is no API key. Add a startup check: if key is empty, show "AI scanning is temporarily unavailable" instead of failing per-scan.

### P1 — Should fix before launch

4. **Notification permission never requested.** Step 13 has "Enable Reminders" button but `expo-notifications Notifications.requestPermissionsAsync()` is never called. The button just advances the step. Fix: call `Notifications.requestPermissionsAsync()` on button press and wire meal reminder scheduling.

5. **Settings Nutrition rows are stubs.** "Daily Goals", "Units", and "Dietary Preferences" all show Alert dialogs instead of actual edit screens. Users expect to edit their nutrition targets in settings. At minimum, "Daily Goals" should open a modal to update calorie and macro goals. "Units" can stay as a future TODO but should say so honestly.

6. **No food deletion.** Users cannot delete an incorrectly logged food item from the Home screen or anywhere. Only `removeConsumedItem` action exists in Redux but it is never dispatched from any screen. Fix: add swipe-to-delete or long-press menu on food cards in Home screen.

7. **Meal reminder toggle not persisted.** Settings `notificationsEnabled` state is local only. On app restart, it defaults back to `true` visually but does nothing regardless. Either wire it to AsyncStorage + expo-notifications, or remove the toggle until implemented.

8. **Monthly anchor price mismatch.** Onboarding paywall step 15 shows Monthly at $9.99 (anchor price trick) but Stripe charges $4.99. This is visible if users check their Stripe receipt vs the in-app display. Not technically illegal but creates trust issues.

### P2 — Improvements for quality

9. **`analyzeComplete` sound never called.** The sound file `analyze_complete.wav` exists and is in the sound map, but no screen calls `playSound('analyzeComplete')`. Should be called in `CameraScreen.confirmAndSave()` or when `setAnalysisResult` fires.

10. **activeDate is set at app start only.** `nutritionSlice` initializes `activeDate` to today at store creation. If the user leaves the app running overnight, `activeDate` does not update. On app return the next day, the Home screen shows yesterday's data as "today." Fix: reset `activeDate` to today on app foreground in App.tsx.

11. **Weight projection graph is a custom dot visualization, not react-native-chart-kit.** Functional but visually crude. Consider replacing with a LineChart from react-native-chart-kit for consistency.

12. **HealthKit integration installed but not wired.** `react-native-health` is in package.json and `NSHealthShareUsageDescription` is set in plist. But no screen reads from HealthKit. Worth either removing the dependency (reduces bundle + removes unnecessary permission prompt) or wiring it to the analytics screen for step count / active calories context.

13. **USDA food database service exists but not exposed in UI.** `foodDatabase.ts` implements USDA FoodData Central API + Open Food Facts barcode lookup. There is no barcode scanner screen or text search screen in the app. The service code is dead weight. Either build a food search screen (adds significant value) or remove the service to reduce dead code.

14. **`Onboarding.tsx` exists but is unused.** There is both `Onboarding.tsx` and `OnboardingFlow.tsx` in screens. Only `OnboardingFlow.tsx` is imported in `App.tsx`. `Onboarding.tsx` appears to be a legacy file. Should be deleted.

---

## 14. QA CHECKLIST

### TDEE Formula Verification
Run these calculations manually to verify:
```
Input: Male, 30yo, 5'10" (177.8cm), 170lbs (77.1kg), moderate activity, lose goal
BMR = 10 * 77.1 + 6.25 * 177.8 - 5 * 30 + 5 = 771 + 1111.25 - 150 + 5 = 1737.25
TDEE = 1737.25 * 1.55 = 2692.7 → 2693
Daily calories = 2693 - 500 = 2193
Protein = min(170 * 2.20462 * 0.8, 2193 * 0.30 / 4) = min(300, 164.5) = 165g
Fat = 2193 * 0.25 / 9 = 60.9 → 61g
Carbs = (2193 - 165*4 - 61*9) / 4 = (2193 - 660 - 549) / 4 = 984 / 4 = 246g
```

Expected output for above: 2193 cal, 165g protein, 246g carbs, 61g fat. Verify this matches what the onboarding Step 9 displays for these inputs.

### AI Scanning
- [ ] Gemini API key is set (check `Constants.expoConfig.extra.googleAiApiKey` is non-empty)
- [ ] Take a photo of a clearly visible meal — verify response is parseable JSON
- [ ] Take a photo of a non-food item — verify graceful error handling (not crash)
- [ ] Take a blurry/dark photo — verify graceful error handling
- [ ] Free user reaches 3 scans — verify 4th scan shows "Daily Limit Reached" alert
- [ ] After midnight (or fake by changing device date) — verify scan count resets
- [ ] Premium user — verify no scan limit shown, no limit enforced

### Purchase Flow
- [ ] Tap "Start Free Trial" → browser opens with correct Stripe URL
- [ ] Return to app → "Did you complete your payment?" appears
- [ ] Tap "Yes I paid" → isPremium = true, scan limit removed, analytics monthly unlocked
- [ ] Tap "No" → PurchaseCancelledError silently swallowed, remain free
- [ ] Tap "Restore Purchases" with `@nutrisnap_premium = 'true'` in AsyncStorage → premium restored
- [ ] Deep link `nutrisnap://premium-activated` → sets premium (after P0 bug fix)
- [ ] App restart with premium set → checkEntitlements reads AsyncStorage, premium persists

### Onboarding Regression
- [ ] All 16 steps advance and back correctly
- [ ] Back from step 1 goes to step 0 (no back button visible at step 0)
- [ ] X on step 15 shows rescue offer, second X allows continuing free
- [ ] `saveOnboardingData()` dispatches all 8+ Redux actions and writes AsyncStorage
- [ ] After completing onboarding, `hasCompletedOnboarding = true` → app goes directly to Main tabs on next launch

### Navigation
- [ ] Home → Camera tab → capture → analyze → "Log Food" → returns to Home showing new item
- [ ] Home → Camera tab → scan limit alert → "Upgrade" → Paywall modal opens
- [ ] Paywall back-navigation: X closes and returns to previous screen
- [ ] Analytics: Weekly toggle works. Monthly toggle redirects to Paywall for free user.
- [ ] Deep link `nutrisnap://home` → opens app to Home screen

### Sound
- [ ] Sound plays on every onboarding step advance
- [ ] No crash when sound file missing (errors silently caught)
- [ ] `playSound('premium')` plays on purchase success
- [ ] Sounds work with iOS hardware mute switch (playsInSilentModeIOS = true)

---

## 15. SOUND DESIGN REQUIREMENTS (complete list)

All 9 required sounds are present. Missing wire-up:

| Sound | File | Wired? | Fix |
|-------|------|--------|-----|
| tap | tap.wav | Partially (Settings only) | Add to all primary CTAs |
| tapHeavy | tap_heavy.wav | No | Wire to heavy action buttons |
| toggle | toggle.wav | No (toggle settings not called) | Wire to Settings switches |
| swipe | swipe.wav | Yes (onboarding) | OK |
| success | success.wav | Yes (restore purchases) | Also fire on food log save |
| error | error.wav | Not via SoundEngine (haptics only) | Wire to analysis failure |
| permissionGranted | permission_granted.wav | No | Wire to camera grant |
| premium | premium.wav | Yes (purchase + upgrade tap) | OK |
| analyzeComplete | analyze_complete.wav | No | Wire to Camera state 5 entry |

---

## 16. ENVIRONMENT VARIABLES REQUIRED

| Variable | Purpose | Required for |
|----------|---------|-------------|
| GOOGLE_AI_API_KEY | Gemini 1.5 Flash food scanning | Core functionality (P0) |
| REVENUECAT_PUBLIC_KEY | In app.json but RevenueCat SDK is NOT used — Stripe is used instead | Remove or leave as placeholder |

Set via EAS: `eas secret:create --scope project --name GOOGLE_AI_API_KEY --value "your_key"`

---

## 17. FILE LOCATIONS (canonical)

```
nutriai/
  app.json                    — bundle ID, permissions, EAS config, env var injection
  package.json                — all deps
  babel.config.js             — Reanimated plugin required
  app/
    App.tsx                   — root, provider, phase manager, deep link handler
    screens/
      SplashScreen.tsx        — animated splash
      OnboardingFlow.tsx      — 16-step onboarding + embedded paywall
      Onboarding.tsx          — LEGACY, unused, delete
      Home.tsx                — Today tab: calorie ring, macro bars, food log
      Camera.tsx              — Scan tab: camera, Gemini scan, result
      Analytics.tsx           — Insights tab: charts, streak, summary
      Settings.tsx            — Settings tab: subscription, nutrition, preferences
      Paywall.tsx             — Modal paywall (post-onboarding access)
    services/
      purchases.ts            — Stripe Payment Links logic
      foodDatabase.ts         — USDA + Open Food Facts (unused in UI — P2)
      ads.ts                  — AdMob stubs (all no-ops, removed)
    store/
      index.ts                — Redux store + persistor config
      hooks.ts                — useAppSelector, useAppDispatch typed hooks
      userSlice.ts            — user profile + onboarding state
      nutritionSlice.ts       — daily food log + goals
      subscriptionSlice.ts    — premium status + scan counters
    sounds/
      SoundEngine.ts          — expo-av wrapper with preload + playSound()
    utils/
      theme.ts                — colors, typography, spacing, border, shadow constants
      nutrition.ts            — TDEE/BMR calculations (Mifflin-St Jeor)
      haptics.ts              — expo-haptics wrapper
    components/
      common/
        Button.tsx            — reusable button
        Card.tsx              — reusable card
        EmptyState.tsx        — empty state with icon + CTA
        SkeletonLoader.tsx    — loading placeholder
        SoundTouchable.tsx    — TouchableOpacity wrapper with sound
        Typography.tsx        — text components
      ads/
        BannerAdView.tsx      — AdMob banner (stub, no-op)
    assets/
      sounds/                 — 9 WAV files (tap, tapHeavy, toggle, swipe, success,
                                error, permissionGranted, premium, analyzeComplete)
      icon.png, splash-icon.png, adaptive-icon.png, favicon.png
```
