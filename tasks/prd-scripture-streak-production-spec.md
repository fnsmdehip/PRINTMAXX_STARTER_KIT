# PRD: Scripture Streak — Production-Quality App Spec
# Version: 1.0 — Full Edge-Case Hardened
# Date: 2026-04-07
# Status: READY FOR ONE-SHOT BUILD

> This spec covers every screen, every edge case, every security boundary, and every
> App Store requirement. An agent reading ONLY this doc should be able to build
> Scripture Streak to production quality without asking clarifying questions.

---

## 1. APP OVERVIEW

**Name:** Scripture Streak
**Bundle ID:** com.printmaxx.scripturestreak
**Tagline:** Daily Bible Verses & Streaks
**Category:** Lifestyle (primary), Education (secondary)
**Target User:** Christians who want to build a consistent daily Bible reading habit. Ranges from new believers who have never read the Bible to seasoned readers who want structure and accountability.
**Monetization:** Stripe Payment Links (NOT RevenueCat IAP)
**Free Tier:** Daily verse (KJV only), basic streak tracking (current/longest/total), calendar, milestone badges, save/copy/share verse
**Premium Tier ($2.99/mo or $19.99/yr):** All Bible translations (NIV, ESV, NLT, NASB, MSG), Reading Plans, Advanced Stats (this week/month/year, most active day, reading trend), unlimited bookmarks implied

**Stripe Products (LIVE, hardcoded in purchases.ts):**
- Annual: `https://buy.stripe.com/00weVe7POd81dxT2Ev3F60z` — $19.99/year (Save 44%)
- Monthly: `https://buy.stripe.com/aFa28s3zyfg9alH4MD3F60A` — $2.99/month
- Customer Portal: `https://billing.stripe.com/p/login/printmaxx`

**Privacy Policy:** https://printmaxx-privacy.surge.sh
**Terms of Service:** https://printmaxx-tos.surge.sh
**Support URL:** https://printmaxx.com/apps/scripture-streak/support
**Support Email:** support@printmaxx.com

---

## 2. TECH STACK

| Layer | Library | Version |
|-------|---------|---------|
| Framework | Expo SDK 52 | ~52.0.0 |
| Language | TypeScript | ^5.3.0 |
| Navigation | @react-navigation/bottom-tabs + native | ^7.x |
| State | React hooks + AsyncStorage | — |
| Storage | @react-native-async-storage/async-storage | 1.23.1 |
| Sound | expo-av | ~15.0.2 |
| Haptics | expo-haptics | ~14.0.1 |
| Notifications | expo-notifications | ~0.29.14 |
| Clipboard | expo-clipboard | ~7.0.1 |
| Sharing | expo-sharing | ~13.0.1 |
| Linking | expo-linking | ~7.0.5 |
| Store Review | expo-store-review | ~8.0.1 |
| Linear Gradient | expo-linear-gradient | ~14.0.2 |
| Safe Area | react-native-safe-area-context | 4.12.0 |
| Fonts | @expo-google-fonts/crimson-text, inter | ^0.4.x |
| Icons | @expo/vector-icons (Ionicons) | latest |
| Payment | Stripe Payment Links via Linking.openURL | — |
| Bible API | bible-api.com (free, no API key, KJV public domain) | — |
| React Native | 0.76.9 | — |

**Build command (native required for SDK 52):**
```bash
npx expo prebuild --platform ios && npx expo run:ios
```
Never use `expo start --ios` — Reanimated and native modules do not work in Expo Go.

**New Architecture:** Enabled (`newArchEnabled: true` in app.json)

---

## 3. DATA TYPES (canonical)

```typescript
// Core verse structure used everywhere
interface Verse {
  book: string;         // Display name, e.g. "Genesis", "1 Samuel"
  chapter: number;
  verse: number;
  text: string;         // Plain text, no HTML
  translation: string;  // e.g. "KJV", "NIV"
}

// Per-user streak tracking — persisted to AsyncStorage @ss_streak_data
interface StreakData {
  currentStreak: number;          // consecutive days including today if read
  longestStreak: number;          // all-time best
  totalDaysRead: number;          // cumulative, never decrements
  readDates: string[];            // ISO date strings "YYYY-MM-DD", sorted ascending
  lastReadDate: string | null;    // "YYYY-MM-DD" or null
  freezesUsedThisMonth?: number;  // streak freeze count (not yet UI-exposed)
  lastFreezeMonth?: string;       // "YYYY-MM" for freeze reset tracking
}

// User preferences — persisted to AsyncStorage @ss_user_settings
interface UserSettings {
  notificationTime: string;      // "HH:MM" 24h, e.g. "08:00"
  preferredTranslation: string;  // default "NIV"; free users forced to "KJV"
  streakReminders: boolean;      // notification toggle
  dailyGoalVerses: number;       // 1–10, counter in Settings
  isPremium: boolean;            // local cache of Stripe purchase state
}

// Onboarding answers — persisted to AsyncStorage @ss_onboarding_v2_answers
interface OnboardingAnswers {
  goal: string;       // 'deepen' | 'habit' | 'whole' | 'peace'
  experience: string; // 'new' | 'some' | 'regular' | 'deep'
  frequency: string;  // 'daily' | '5x' | '3x'
  time: string;       // 'morning' | 'afternoon' | 'evening' | 'bed'
  duration: string;   // '5' | '10' | '15' | '20'
}

// Onboarding completion state
interface OnboardingState {
  completed: boolean;
  translation: string;
  dailyGoal: 'verse' | 'chapter' | 'custom';
  customGoalCount: number;
  notificationTime: string;
  notificationsEnabled: boolean;
}

// Reading plan definition (static, from src/constants/plans.ts)
interface ReadingPlan {
  id: string;           // e.g. 'genesis-30'
  title: string;
  description: string;
  book: string;         // primary book name
  totalChapters: number;
  durationDays: number;
  icon: string;         // emoji
}

// Reading plan progress per user — persisted under @ss_reading_plans (object keyed by planId)
interface ReadingPlanProgress {
  planId: string;
  startDate: string;        // "YYYY-MM-DD"
  completedDays: string[];  // "YYYY-MM-DD" dates when Mark Today was tapped
  currentDay: number;       // 1-indexed, increments on each Mark Today
  lastReadDate: string | null;
}

// Bookmark entry
interface BookmarkEntry {
  id: string;     // "{book}-{chapter}-{verse}-{timestamp}"
  verse: Verse;
  date: string;   // ISO 8601
  note?: string;
}

// BibleBook metadata (static, 66 books)
interface BibleBook {
  name: string;
  chapters: number;
  testament: 'old' | 'new';
}

// Advanced stats (computed by StreakIntelligence.calculateStats)
interface StreakStats {
  currentStreak: number;
  longestStreak: number;
  totalDaysRead: number;
  consistencyLast30: number;    // 0–100 percent
  daysThisWeek: number;
  daysThisMonth: number;
  daysThisYear: number;
  averagePerWeek: number;
  weeklyTrend: 'up' | 'down' | 'stable';
  estimatedReadingMinutes: number; // totalDaysRead * 5
  mostReadDayOfWeek: string;       // 'Sunday'–'Saturday' | 'N/A'
  readingPace: number;             // same as averagePerWeek (chapters/week estimate)
}

// Stripe purchase metadata — persisted to AsyncStorage @scripture_streak_premium
interface StripePurchaseRecord {
  isPremium: boolean;
  purchasedAt: string;  // ISO 8601
  plan: string;         // 'annual' | 'monthly' | 'deep-link'
}
```

---

## 4. CONSTANTS

### AsyncStorage Keys
```typescript
const KEYS = {
  STREAK_DATA:      '@ss_streak_data',
  USER_SETTINGS:    '@ss_user_settings',
  BOOKMARKS:        '@ss_bookmarks',
  READING_PROGRESS: '@ss_reading_progress',
  LAST_VERSE_INDEX: '@ss_last_verse_index',
  ONBOARDING:       '@ss_onboarding',
  READING_PLANS:    '@ss_reading_plans',
};
const STRIPE_PREMIUM_KEY = '@scripture_streak_premium';
const ONBOARDING_COMPLETE_KEY = '@ss_onboarding_v2_complete';
const ONBOARDING_ANSWERS_KEY = '@ss_onboarding_v2_answers';
const BIBLE_CHAPTER_CACHE_PREFIX = '@ss_bible_';  // + "{book}_{chapter}"
```

### Default Values
```typescript
// Default UserSettings
{
  notificationTime: '08:00',
  preferredTranslation: 'NIV',    // NOTE: free users are forced to KJV at read time
  streakReminders: true,
  dailyGoalVerses: 1,
  isPremium: false,
}
// Default StreakData
{ currentStreak: 0, longestStreak: 0, totalDaysRead: 0, readDates: [], lastReadDate: null }
```

### Pricing (hardcoded in PaywallScreen and OnboardingFlow)
| Plan | Price | Label |
|------|-------|-------|
| Yearly | $19.99/year | "BEST VALUE — Save 44%" ($1.67/month) |
| Monthly | $2.99/month | Standard |
| Free trial | 7 days free | Shows on subscribe button |

### Free Tier Limits
| Feature | Free | Premium |
|---------|------|---------|
| Daily Verse | KJV only | KJV only (same verse, any translation in Bible tab) |
| Bible Translations | KJV only | NIV, ESV, KJV, NLT, NASB, MSG |
| Reading Plans | Blocked (alert shown) | All 6 plans |
| Advanced Stats | Blocked (upsell card shown) | Full stats row |
| Basic Streaks | Full access | Full access |
| Calendar | Full access | Full access |
| Milestone Badges | Full access | Full access |
| Bookmarks | Full access | Full access |

### Available Translations (in order)
`['NIV', 'ESV', 'KJV', 'NLT', 'NASB', 'MSG']`

### Available Reading Plans (6 plans)
| ID | Title | Book | Chapters | Days |
|----|-------|------|----------|------|
| genesis-30 | Journey Through Genesis | Genesis | 50 | 30 |
| psalms-30 | Psalms of Praise | Psalms | 150 | 30 |
| proverbs-31 | Wisdom for Every Day | Proverbs | 31 | 31 |
| john-21 | The Gospel of John | John | 21 | 21 |
| romans-16 | Romans Deep Dive | Romans | 16 | 16 |
| matthew-28 | Walk with Matthew | Matthew | 28 | 28 |

### Milestone Thresholds
| Days | Tier | Icon | Color |
|------|------|------|-------|
| 7 | Bronze | star | #CD7F32 |
| 30 | Silver | flame | #C0C0C0 |
| 100 | Gold | diamond | #FFD700 |
| 365 | Diamond | trophy | #B9F2FF |

### Streak Freeze Limits
- Free: 1 freeze per month
- Premium: Unlimited (UI exists in StreakIntelligence but not yet surfaced in any screen)

### Bible Data
- 66 books (39 OT, 27 NT) as static BIBLE_BOOKS array
- 1,189 total chapters (KJV)
- 365 daily verses in `src/data/verses.ts` — KJV, public domain, static
- Full verse counts per chapter in `src/services/verse.ts` (VERSE_COUNTS table)

### App Version
1.0.0 (build 1)

### Notification Times Available in Settings
06:00, 07:00, 08:00, 09:00, 12:00, 18:00, 20:00, 21:00

---

## 5. APP SCREEN FLOW (state machine)

```
App Launch
    │
    ▼
[SplashScreen]  (navy background, animated cross/wordmark, ~2s)
    │
    ├── onboarding NOT complete ──▶ [OnboardingFlow] (12 steps + paywall)
    │                                    │
    │                                    ▼
    │                              [TabNavigator]  ◀────────────
    │                                                           │
    └── onboarding complete ──────────────────────────────────▶┘
```

### Onboarding Check Logic (App.tsx)
1. Read `@ss_onboarding_v2_complete` from AsyncStorage
2. If `'true'` → go to `main`
3. Else read legacy `@ss_onboarding` → if `completed: true` → go to `main`
4. Else → go to `onboarding`

### Deep Link: `scripture-streak://premium-activated` or `scripture-streak://payment-success`
Writes `@scripture_streak_premium` with `{ isPremium: true }` — used for Stripe success URL redirect.

---

## 6. NAVIGATION STRUCTURE

### Root Navigation
Single NavigationContainer wrapping TabNavigator. No modal stacks, no native-stack — everything is bottom-tab with in-component view mode switching.

### Bottom Tab Navigator (5 tabs)
```
Daily     (sunny / sunny-outline icon)
Streaks   (flame / flame-outline icon)
Bible     (book / book-outline icon)
Plans     (list / list-outline icon)
Settings  (settings / settings-outline icon)
```

Tab bar style:
- Background: #FFFFFF
- Active color: #E2B53F (gold)
- Inactive color: #9E9EB0 (textMuted)
- Border top: 1px #F0EBE3
- Height: 88px iOS, 72px Android
- Label font: 10px SF Pro Text (iOS), system (Android), weight 600

### In-Tab View Switching (NOT React Navigation — local state)
BibleScreen: `books` → `chapters` → `verses` (local `viewMode` state + Animated slide)
PlansScreen: plan list → plan detail (local `selectedPlan` state)
OnboardingFlow: step 0–11 (local `step` state + fade/slide animation)

---

## 7. SCREEN-BY-SCREEN SPEC

---

### 7.1 SplashScreen

**File:** `src/screens/SplashScreen.tsx`
**Trigger:** App launch, shown while checking onboarding state
**Duration:** Animated, calls `onFinish` when animation completes or `isReady` becomes true

**States:**
- Loading: navy background (#1A1A2E), animated cross icon, "Scripture Streak" wordmark, subtitle "Your daily Bible companion"
- No error state — always proceeds to next screen

**Behavior:**
- Fade/scale animation plays on mount
- `onFinish` prop called after animation
- App.tsx checks onboarding state independently on mount; whichever finishes first drives the transition

**Edge cases:**
- If `checkOnboardingState` resolves before splash animation ends, splash stays until animation finishes
- No user interaction required

---

### 7.2 OnboardingFlow (12 Steps)

**File:** `src/screens/OnboardingFlow.tsx`
**Total steps:** `TOTAL_STEPS = 12` (steps 0–11)
**Storage:** `@ss_onboarding_v2_complete` + `@ss_onboarding_v2_answers`

**Progress bar:** Animated horizontal bar at top, fills to `(step + 1) / 12` with 300ms timing animation. Navy fill on dark background.

**Back navigation:** Chevron-back button in top-left. On step 0 = no back. On paywall rescue = dismisses rescue, not going back a step.

**Skip button:** Shown on steps 2, 7, 8 only (Experience, Social Proof, Features). Tapping advances to next step without saving an answer.

**Next button:** Navy background, gold text. Disabled/not shown when `canAdvance()` returns false (step 1 requires goal selection, step 2 requires experience selection).

**Animation between steps:** Fade out (150ms) → set new step → slide in + fade in (250ms). Direction: forward = slide from right (+60px), back = slide from left (–60px).

**Sound:** `playSound('swipe')` on every step transition, `playSound('toggle')` on option selection.

#### Step 0: Welcome
Title: "Your Daily Scripture Journey Starts Here"
Body: "Build a life-changing habit of daily Bible reading with personalized plans, streak tracking, and daily inspiration."
Feature list rows (3 items):
- Ionicons `flame-outline` — "Track your daily reading streak"
- Ionicons `book-outline` — "Beautiful daily readings & plans"
- Ionicons `notifications-outline` — "Gentle daily reminders"
CTA: "Get Started" (navy button). No selection required.

#### Step 1: Goal
Title: "What's your spiritual goal?"
Sub: "This helps us personalize your reading journey."
4 option cards (required, must select one to advance):
| id | label | icon | desc |
|----|-------|------|------|
| deepen | Deepen my faith | heart-outline | Grow closer to God through His Word |
| habit | Build a daily habit | flame-outline | Make Scripture part of every day |
| whole | Read the whole Bible | book-outline | Cover Genesis to Revelation |
| peace | Find peace & comfort | leaf-outline | Let God's promises calm your heart |

Selected card: gold border + gold background tint, gold radio dot. Unselected: muted border, empty radio.

#### Step 2: Experience
Title: "How familiar are you with the Bible?"
Sub: "No wrong answers here. We meet you where you are."
4 option cards (skippable, required for canAdvance):
| id | label | icon | desc |
|----|-------|------|------|
| new | New to the Bible | sparkles-outline | Just getting started |
| some | Read some passages | layers-outline | Familiar with key stories |
| regular | Read regularly | library-outline | Have a reading practice |
| deep | Know it well | school-outline | Years of study |

#### Step 3: Frequency
Title: "How often do you want to read?"
Sub: "Consistency matters more than quantity."
3 option cards (default: 'daily'):
| id | label | icon | days/week |
|----|-------|------|-----------|
| daily | Every day | sunny-outline | 7 |
| 5x | 5 days / week | calendar-outline | 5 |
| 3x | 3 days / week | time-outline | 3 |

#### Step 4: Time of Day
Title: "When works best for you?"
Sub: "We'll send a gentle reminder at this time."
2x2 grid of time cards (default: 'morning'):
| id | label | icon | time | desc |
|----|-------|------|------|------|
| morning | Morning | sunny-outline | 07:00 | Start your day with Scripture |
| afternoon | Afternoon | partly-sunny-outline | 12:00 | A midday moment of peace |
| evening | Evening | moon-outline | 18:00 | Wind down with God's Word |
| bed | Before bed | bed-outline | 21:00 | End the day in faith |

Selected card: gold background, navy text. Unselected: dark navy with gold icon.

#### Step 5: Duration
Title: "How long can you read each day?"
Sub: (implied from layout)
4 option cards (default: '10'):
| id | label | minutes | desc |
|----|-------|---------|------|
| 5 | 5 min | 5 | Quick and focused |
| 10 | 10 min | 10 | Steady and thoughtful |
| 15 | 15 min | 15 | Deep and meaningful |
| 20 | 20+ min | 20 | Immersive study |

#### Step 6: Validation / Projection Screen
Title: Your personalized reading plan
Displays computed projection based on answers:
- Chapters per week = `chaptersPerSession * daysPerWeek` where `chaptersPerSession = max(1, round(duration / 4))`
- Target: depends on goal:
  - `peace` → Psalms & Proverbs (181 chapters)
  - `whole` → entire Bible (1,189 chapters)
  - `deepen`/`habit` → New Testament (260 chapters)
- Days to complete = `ceil(targetChapters / chaptersPerSession / daysPerWeek) * 7`
Shows: "You could read [milestone] in [N] days at your pace" with icon.

#### Step 7: Social Proof (skippable)
3 testimonial cards (scrollable or stacked):
| name | streak | text |
|------|--------|------|
| Sarah M. | 90 | "I've never been so consistent with my Bible reading. 90 days and counting!" |
| James K. | 45 | "The daily reminders keep me accountable. My faith has grown so much." |
| Maria L. | 120 | "I love how it tracks my progress. Makes reading feel achievable." |

#### Step 8: Features Showcase (skippable)
4 feature cards:
| icon | title | desc |
|------|-------|------|
| flame-outline | Streak Tracking | Stay motivated with daily streaks and milestone badges |
| book-outline | Daily Readings | Curated verses with beautiful typography and context |
| language-outline | Multiple Translations | NIV, ESV, KJV, NLT, and more at your fingertips |
| map-outline | Reading Plans | Guided journeys through books of the Bible |

#### Step 9: Notifications Permission
Title: "Never miss a day"
Sub: "Get a daily reminder at your chosen time"
Shows the selected time from step 4 (e.g. "Morning — 7:00 AM").
Primary CTA: "Enable Reminders" → calls `NotificationService.requestPermissions()` → schedules daily reminder at selected time → advances to step 10.
Secondary: "Maybe later" → advances to step 10 without requesting permissions.

#### Step 10: Plan Ready / Almost Done
Title: "Your plan is ready!"
Shows a summary of their choices (frequency, time, goal).
Encouragement text: "Join thousands of believers building their daily Scripture habit."
CTA: "Let's Go" → advances to step 11 (paywall).

#### Step 11: Paywall (embedded in onboarding)
This is NOT PaywallScreen.tsx — it is rendered inline within OnboardingFlow.

**Normal state:**
Header: "Unlock the Full Scripture Experience" with PREMIUM badge
Feature comparison table (same as PaywallScreen — 6 rows: Daily Verse, Basic Streaks, All Translations, Reading Plans, Offline Access, Advanced Stats)
Plan selector: Yearly (BEST VALUE, default) and Monthly
Subscribe button: "Start Free Trial" + "7 days free, then $X"
"Continue with Free Plan" (smaller, secondary, triggers rescue offer first)

**Rescue Offer state (shown when user taps "Continue with Free Plan" first time):**
Shown when `showRescue = true`. Second tap on decline → `saveAndComplete()` with free tier.
Rescue offer content is handled by `showRescue` state — the exact rescue UI is NOT defined in the code read (needs implementation or verification).

**Purchase flow in OnboardingFlow:**
1. `handlePurchase()` calls `getOfferings()` → gets Stripe URL package
2. Calls `purchasePackage(pkg)` → opens Stripe URL in browser, waits for app return, shows "Did you complete?" alert
3. On 'Yes' → saves `isPremium: true` to both `@scripture_streak_premium` and `UserSettings`
4. Calls `saveAndComplete()` → writes `@ss_onboarding_v2_complete = 'true'` → calls `onComplete()`

**Restore Purchases in OnboardingFlow:**
Calls `restorePurchases()` → reads `@scripture_streak_premium` → if found and isPremium, saves and completes.

**`saveAndComplete()` logic (important for onboarding completion):**
1. Plays `success` sound
2. Sets `@ss_onboarding_v2_complete = 'true'`
3. Sets `@ss_onboarding_v2_answers = JSON.stringify(answers)`
4. Calls `StorageService.completeOnboarding()` which writes `UserSettings` from answers:
   - `notificationTime`: from `TIMES[answers.time].time`
   - `translation`: hardcoded `'NIV'` (regardless of user's prior selection — default settings will use NIV, but free users forced to KJV in Bible tab)
   - `dailyGoal`: `'chapter'`
   - `customGoalCount`: `max(1, round(parseInt(answers.duration) / 4))`
   - `notificationsEnabled`: `true`
   - `isPremium`: `false` (unless purchase confirmed)
5. Calls `onComplete()` → App navigates to main

---

### 7.3 PaywallScreen

**File:** `src/screens/PaywallScreen.tsx`
**When shown:** NOT currently reachable in v1 flow. The paywall is embedded in OnboardingFlow. PaywallScreen exists as a standalone component but is NOT wired to any navigator screen. It accepts `onContinueFree` and `onSubscribe` callbacks.

**States:**
- Default: Yearly selected
- Monthly selected: Plan card highlights with gold border
- Purchasing: Button opacity 0.6, disabled
- Purchase success: `isPremium: true` saved, `onSubscribe()` called
- Error: Silent catch (user cancelled)
- Restore: Alert — "No Purchase Found" or "Error" or success

**Layout (top to bottom):**
1. Close button (×) top-right — calls `onContinueFree` immediately (no rescue)
2. PREMIUM badge (gold pill)
3. Title: "Unlock the Full Scripture Experience"
4. Subtitle: "Deepen your faith with unlimited access to every feature."
5. Feature comparison table (6 rows)
6. Plan selector (Yearly/Monthly radio cards)
7. Subscribe CTA button
8. "Continue with Free Plan" (secondary)
9. Legal text (subscription terms)
10. Terms | Privacy | Restore Purchases links

**Entry point to premium:** PaywallScreen explicitly persists `isPremium: false` to AsyncStorage when user taps "Continue with Free Plan" (ensures free state is written, not just defaulted).

---

### 7.4 DailyScreen (Tab: Daily)

**File:** `src/screens/DailyScreen.tsx`

**Data loaded on mount:**
1. `VerseService.getVerseOfTheDay()` — static lookup from 365-verse array by day-of-year
2. `StorageService.getStreakData()` — async AsyncStorage read
3. `StorageService.hasReadToday()` — checks if today's date in `readDates`

**Loading state:** Skeleton screens — header skeleton (2 gray lines), verse card skeleton (3 lines centered), button skeleton. No spinner.

**Loaded state (has not read today):**

Header section:
- Greeting: "Good [Morning/Afternoon/Evening]" (based on hour: <12 Morning, <17 Afternoon, else Evening)
- Date: full weekday + month + day (e.g. "Monday, April 7")
- StreakBadge component: shows `streak.currentStreak` with flame icon

Hero verse card (animated fade + translateY from 16px):
- Label: "VERSE OF THE DAY" (gold, uppercase)
- Gold divider line (40px wide, 2px tall, 50% opacity)
- Verse text: italic Georgia (iOS) / serif font, 22px, centered
- Reference: "{Book} {chapter}:{verse} ({translation})" gold bold
- Action row: Save | Copy | Share (separated by vertical dividers, minimum 44pt touch)

"Mark Today as Read" button (navy, prominent):
- Icon: `checkmark-circle` white
- Text: "Mark Today as Read" (white, bold)
- Sub: "Keep your streak alive" (white 55% opacity)
- On tap: `playSound('success')`, haptic success, `StorageService.recordReading()`, updates streak state, animates completion card in
- Store review: At 7, 14, 30 total days read → `StoreReview.requestReview()` after 2s delay

Quick stats row (after mark-as-read button):
3 columns: Total Days | Best Streak | Current Streak
Current streak value in gold, others in navy
Font: 48px weight 200, tabular-nums

Encouraging message card:
- Gold `sparkles` icon
- Text from `StreakIntelligence.getEncouragingMessage(streak)` or inline `getEncouragingMessage(0)` if streak null

**Loaded state (has read today):**
- Mark as Read button replaced by completion card
- Green background (#E8F5E9), checkmark-circle (4CAF50), "Today's reading complete", "Come back tomorrow to continue your streak"
- Checkmark animated with spring (scale from 0 to 1)

**Pull to refresh:** Reloads verse + streak data, refreshes all sections.

**Bookmark behavior:**
- Tapping Save: saves to AsyncStorage `@ss_bookmarks` with key `{book}-{chapter}-{verse}-{timestamp}`
- Toggle: `bookmarked` state flips icon (bookmark-outline → bookmark filled)
- NOTE: Bookmarks cannot be un-bookmarked from DailyScreen — state is local, no remove

**Copy behavior:**
- Formats: `"[verse text]" — [Book chapter:verse] ([translation])`
- Shows "Copied" state for 2 seconds, then reverts to "Copy"

**Share behavior:**
- iOS: system share sheet via `Share.share({ message: text })`
- Web: `Clipboard.setStringAsync(text)` fallback
- Error fallback: clipboard copy

**Edge cases:**
- Verse null: verse card not rendered (Animated.View skipped by conditional)
- Streak null: StreakBadge not rendered, quick stats not rendered, encouraging message uses inline function with 0

---

### 7.5 StreaksScreen (Tab: Streaks)

**File:** `src/screens/StreaksScreen.tsx`

**Premium sync on mount:** Calls `checkSubscription()` → compares to stored `isPremium` → if different, saves updated setting and sets local state.

**Loading state:** Skeleton — centered circle (140px diameter), 2 skeleton lines.

**Loaded state:**

Title: "Your Streaks"
Subtitle: "Track your daily Scripture journey"

Hero streak ring (160px diameter animated):
- Outer ring animates scale from 0 (spring, friction 6, tension 60)
- Inner glow ring rotates continuously (8s loop, 360deg)
- Inner circle (140px): shows icon + streak count + "DAYS" label
- Icon selection by `currentStreak`:
  - 0 = `leaf-outline` (success green)
  - 1–6 = `leaf` (success green)
  - 7–29 = `star` (gold)
  - 30–99 = `flame` (streakFire orange)
  - 100+ = `trophy` (gold)
- Streak number: 48px weight 200, gold, tabular-nums
- Streak message below ring (gold text):
  - 0: "Start reading today to begin your streak"
  - 1–6: "Great start! Keep growing!"
  - 7–29: "One week strong!"
  - 30–99: "On fire! Incredible faithfulness!"
  - 100+: "Legendary dedication!"

Basic stats row (3 cards — FREE):
Best Streak (trophy, gold) | Total Days (book, navy) | Weekly Avg (bar-chart, primaryLight)

Extended stats row (3 cards — PREMIUM ONLY):
This Week (calendar, success) | This Month (calendar-outline, gold) | This Year (ribbon, streakFire)

For FREE users: extended stats replaced by a upsell card ("lock-closed" icon, "Unlock Advanced Stats", "This Week, This Month, This Year breakdowns and Reading Insights").

Calendar:
- Month/year header with prev/next nav buttons (chevron-back, chevron-forward)
- CalendarGrid component: grid of day cells, gold for read days, navy border for today
- Legend: gold dot = Read, navy border circle = Today
- "N days this month" count (bottom right of legend)
- NOTE: Calendar navigation goes back to any historical month

30-Day Consistency card:
- Progress bar (gold fill on #F0EBE3 background)
- Percentage from `stats.consistencyLast30`

Reading Insights card (PREMIUM ONLY, only if `totalDaysRead > 0`):
3 columns: MOST ACTIVE DAY | EST. READING TIME (minutes) | WEEKLY TREND (trending-up/down/remove icon)

Milestone badges (free for all):
4 badges: 1 Week (star, bronze), 1 Month (flame, silver), 100 Days (diamond, gold), 1 Year (trophy, diamond)
Locked badges: 50% opacity, lock-closed icon, "N to go" label
Unlocked: full opacity, tier icon with tier color, tier label

Encouraging message card (gold sparkles, italic body text from StreakIntelligence)

**Pull to refresh:** Reloads streak data and re-runs stats calculation.

---

### 7.6 BibleScreen (Tab: Bible)

**File:** `src/screens/BibleScreen.tsx`

**View modes (local state):** `'books'` → `'chapters'` → `'verses'`

**Premium sync on mount:** Same pattern as StreaksScreen — `checkSubscription()` syncs and saves if changed.

**Free user translation rule:**
- On mount: if `!isPremium`, force `selectedTranslation = 'KJV'`
- If premium: load `preferredTranslation` from UserSettings
- Translation picker locks non-KJV options with 🔒 for free users (shows Alert on tap)

**books view:**
Header:
- Title "Bible"
- Search input (min-height 44pt, debounced by `useMemo` on `searchQuery`)
- Filter row: All | Old Testament | New Testament (pill buttons, navy active)
- Translation selector button (language icon, gold text, dropdown chevron)
- Translation picker (only in books view): scrollable row of 6 translation pills

Book list (FlatList):
Each book item: book name (bold) + "{N} chapters" + OT/NT badge + chevron-forward
OT badge: gold text on accentMuted background
NT badge: green text on successLight background
Min height 56pt
On tap: haptic light, sets selectedBook, switches to `chapters` mode

Empty state (search returned 0): search icon, "No Books Found", "Try a different search term"

**chapters view:**
Breadcrumb: "← Back" (gold, minimum 44pt) + "{BookName}"
Card with "Select a Chapter" title
Grid: flex-wrap, 52×52pt cells, chapter numbers 1..N
On tap: haptic light, sets selectedChapter, switches to `verses` mode

**verses view:**
Breadcrumb: "← Back" + "{BookName} {chapter}"
Loading state: ActivityIndicator (gold, large) + "Loading verses..." text
Loaded: FlatList of verse items
Each verse item: verse number (left, 28px wide, tabular-nums) + verse text (Georgia/serif, 17px, 28px line height) + action row (bookmark, copy, share — 36×36pt circle buttons)
Chapter title header: "{BookName} {chapter}" (h2, centered)
On bookmark: brief visual confirmation (icon changes to checkmark-circle for 1.5s)
On copy: icon changes to checkmark-circle for 1.5s, copies with full citation format

**Bible API integration:**
- API: `bible-api.com` (free, no key, KJV public domain)
- URL pattern: `https://bible-api.com/{book}+{chapter}:1-{verseCount}?translation=kjv`
- Verse count from static `VERSE_COUNTS` table (complete KJV, all 66 books, all chapters)
- Timeout: 10s AbortController
- Cache: AsyncStorage key `@ss_bible_{book}_{chapter}` — stores full verse array as JSON
- On cache hit: instant, works offline
- On API failure: `buildPlaceholderVerses()` — real verse count, shows "Loading {Book} {ch}:{v}... Connect to the internet to download this chapter."
- Translation note: API always returns KJV. Translation label on verses is tagged with `selectedTranslation` after fetch, but actual text is always KJV. Non-KJV translations are NOT fetched from any API — they display KJV text with the translation label. This is a P0 gap (see section 13).

**Animation:** `slideAnim` translateX — ±30px on mode change, 250ms timing ease.

---

### 7.7 PlansScreen (Tab: Plans)

**File:** `src/screens/PlansScreen.tsx`

**Premium sync on mount:** Same pattern.

**Plans list view:**
Title: "Reading Plans"
Subtitle: "Guided journeys through Scripture"

"IN PROGRESS" section (only if active plans exist):
- Each active plan card: icon (52×52pt accentMuted square) + plan title + mini progress bar + "N% complete [• Done today]" + chevron-forward

"CHOOSE A PLAN" / "AVAILABLE PLANS" section:
- Lock icon (gold) shown on each plan card for free users
- Empty state: library icon, "Choose a Reading Plan", "Start a guided journey through Scripture"

On tap any plan → selectedPlan set → plan detail view renders

**Plan detail view:**
Back button: "← All Plans"
Large plan icon (56px, gold)
Plan title + description

Stats card (3 columns): Book | Chapters | Days

Progress card (only if started):
- Progress bar (gold fill)
- "N% complete" + "N of M days"
- Completion banner: ribbon icon, "Plan Complete!"

Today's action block (contextual):
- Not started: "Start Plan" button (navy) → `handleStartPlan()` → PREMIUM GATE (Alert if free)
- Started, not done today: "Mark Today's Reading" button (gold) with day details from `getPlanDaySchedule(planId, currentDay)` (shows chapter range + verse count + study note)
- Started, done today: completion card "Today's reading is done / Come back tomorrow for day N"
- Completed: nothing (or redundant badge from progress card)

Reading Schedule (only if started):
Full schedule list — all days, each showing: check/radio icon + "Day N: {chapter range}" + "{verse count}" + study note excerpt
Completed days: 50% opacity, checkmark-circle (green)
Current day: bold title text, radio-button-on (gold)
Future days: normal, radio-button-off (muted)

**Premium gate enforcement in handleStartPlan:**
```typescript
if (!isPremium) {
  Alert.alert('Premium Feature', 'Reading Plans are available with Scripture Streak Premium...');
  return;
}
```

**Plan progress storage:** Keyed by `planId` inside single `@ss_reading_plans` JSON object.

**Progress calculation:** `completedDays.length / plan.durationDays * 100`

**Edge case — Mark Today idempotent:** Checks `progress.completedDays.includes(today)` before recording; no-ops if already counted.

---

### 7.8 SettingsScreen (Tab: Settings)

**File:** `src/screens/SettingsScreen.tsx`

**Premium sync on mount:** Same pattern as other screens.

**Loading state:** 2 skeleton lines + card skeleton.

**Sections:**

SUBSCRIPTION:
- Badge: "PREMIUM" or "FREE" (gold pill, navy text)
- Description: status summary
- Free users: "Upgrade to Premium" row with sparkles icon, $19.99/yr price → triggers `getOfferings()` + `purchasePackage()` flow
- Premium users: "Manage Subscription" → opens `https://billing.stripe.com/p/login/printmaxx`
- Premium users: "Restore Purchases" → checks AsyncStorage for stored premium flag
- Restore alert for premium users explains Stripe subscription management (not Apple IAP)

NOTIFICATIONS:
- "Streak Reminders" toggle (Switch component) — calls `NotificationService.scheduleDailyReminder()` or `cancelAllScheduled()` on change
- "Reminder Time" selector → opens time picker (8 pill options inline) → scheduling also triggered on time change if reminders enabled

READING PREFERENCES:
- "Preferred Translation" selector → locked to KJV for free users (Alert shown if non-KJV tapped)
- "Daily Goal" counter (minus/plus, min 1, max 10) — stored in settings but not enforced anywhere in UI (no gate checks dailyGoalVerses)

DATA & PRIVACY:
- "Reset All Data" (red text) → Alert with destructive confirmation
  - On confirm: `StorageService.resetAllData()` clears all AsyncStorage keys, restores default settings in local state
  - Does NOT reset `@scripture_streak_premium` — premium status survives data reset (this is correct)

ABOUT:
- Version: 1.0.0 (static)
- Rate the App: TouchableOpacity with chevron, NO `StoreReview.requestReview()` call wired (gap — tapping does nothing)
- Privacy Policy → opens `printmaxx-privacy.surge.sh`
- Terms of Service → opens `printmaxx-tos.surge.sh`
- Support → opens `printmaxx.com/apps/scripture-streak/support`

Footer: "Scripture Streak v1.0.0" + "Build your daily Scripture habit"

---

## 8. FREE VS PRO GATING ENFORCEMENT MATRIX

| Feature | Gate Location | Gate Mechanism | Grep Command |
|---------|--------------|----------------|--------------|
| Bible translations (non-KJV) | BibleScreen.tsx | `isLocked = !isPremium && trans !== 'KJV'` + Alert | `grep -n "isLocked" src/screens/BibleScreen.tsx` |
| Reading Plans (start) | PlansScreen.tsx | `if (!isPremium) { Alert.alert(...); return; }` in `handleStartPlan` | `grep -n "isPremium" src/screens/PlansScreen.tsx` |
| Advanced Stats row | StreaksScreen.tsx | `{stats && isPremium && (<View>...extended stats...</View>)}` | `grep -n "isPremium" src/screens/StreaksScreen.tsx` |
| Reading Insights | StreaksScreen.tsx | `{stats && stats.totalDaysRead > 0 && isPremium && ...}` | `grep -n "isPremium && " src/screens/StreaksScreen.tsx` |
| Translation in Settings | SettingsScreen.tsx | `isLocked = !settings.isPremium && trans !== 'KJV'` + Alert | `grep -n "isLocked" src/screens/SettingsScreen.tsx` |
| Daily verse translation | DailyScreen.tsx | Verse is ALWAYS KJV (no translation toggle on DailyScreen) | (no gate needed — static KJV) |

**Premium state source of truth:** `@scripture_streak_premium` AsyncStorage key.
**Premium state sync pattern:** Each screen on mount reads `checkSubscription()` (reads AsyncStorage) → compares to cached `UserSettings.isPremium` → if different, updates UserSettings → updates local state.
**Premium state is NOT synced in real-time** between screens. If user purchases on PaywallScreen, other tabs will sync on their next mount/focus.

---

## 9. PURCHASE FLOW (Stripe Payment Links — complete spec)

### Architecture
No RevenueCat SDK. No Apple IAP. Purchase is:
1. Open Stripe checkout URL in device browser
2. User completes Stripe checkout (or doesn't)
3. User returns to app (AppState 'active' event)
4. App shows "Did you complete your purchase?" Alert
5. User taps "Yes" → premium activated locally
6. User taps "No" → error thrown, purchase flow exits

### Stripe URLs (hardcoded in `src/services/purchases.ts`)
```
Annual:   https://buy.stripe.com/00weVe7POd81dxT2Ev3F60z
Monthly:  https://buy.stripe.com/aFa28s3zyfg9alH4MD3F60A
Portal:   https://billing.stripe.com/p/login/printmaxx
```

### purchasePackage() Logic (complete)
```
1. Extract __stripeUrl from package object
2. canOpenURL(stripeUrl) check — throws if false
3. Linking.openURL(stripeUrl) — opens browser
4. AppState.addEventListener('change') — waits for 'active' state
5. Safety timeout: 10 minutes — resolves(false) if no return
6. If timed out: throws 'Purchase flow timed out'
7. Alert.alert('Complete Purchase', 'Did you complete your purchase?')
   - 'No' → throws 'Purchase not confirmed by user'
   - 'Yes' → continues
8. AsyncStorage.setItem('@scripture_streak_premium', JSON.stringify({
     isPremium: true,
     purchasedAt: new Date().toISOString(),
     plan: pkg.identifier
   }))
9. Returns mock customerInfo: {
     entitlements: { active: { premium: { isActive: true } } }
   }
```

### getOfferings() return shape
```typescript
{
  annual: {
    __stripeUrl: 'https://buy.stripe.com/...',
    identifier: 'annual',
    packageType: 'ANNUAL',
    product: { title, description, priceString: '$19.99/year', price: 19.99 }
  },
  monthly: {
    __stripeUrl: 'https://buy.stripe.com/...',
    identifier: 'monthly',
    packageType: 'MONTHLY',
    product: { title, description, priceString: '$2.99/month', price: 2.99 }
  },
  availablePackages: [annual, monthly]
}
```

### Restore Purchases Logic
Reads `@scripture_streak_premium` from AsyncStorage. Returns `isPremium` boolean. Does NOT contact Stripe — honor system.

### Deep Link Activation (App.tsx)
Listening for `scripture-streak://premium-activated` or `scripture-streak://payment-success`. Sets `@scripture_streak_premium` with `{ isPremium: true, plan: 'deep-link' }`. Stripe success URL should be configured to redirect to `scripture-streak://payment-success`.

### Important Limitation
There is NO server-side subscription validation. Premium status is purely client-side in AsyncStorage. A user who reinstalls the app loses their premium status unless they tap "Restore Purchases" (which also relies on the same AsyncStorage key — so reinstall ALSO loses on restore). This is a P0 gap.

---

## 10. BIBLE API SPEC

### Provider
**bible-api.com** — free, no API key, KJV text only, public domain.

### Request Format
```
GET https://bible-api.com/{urlEncodedBook}+{chapter}:1-{verseCount}?translation=kjv
```
Example: `https://bible-api.com/genesis+1:1-31?translation=kjv`

Book name mapping: display names → API names via `BOOK_NAME_MAP`:
- Most books: lowercase ("genesis", "matthew")
- Numbered books: concatenated ("1samuel", "2kings", "1corinthians")
- Song of Solomon: "song of solomon"

### Response Parsing
```typescript
data.verses.map(v => ({
  book: displayName,           // from our BIBLE_BOOKS list
  chapter: v.chapter,
  verse: v.verse,
  text: v.text.replace(/\n/g, ' ').trim(),
  translation: 'KJV',
}))
```

### Caching Strategy
- Cache key: `@ss_bible_{book}_{chapter}` (AsyncStorage)
- Cache hit: read synchronously (instant, offline)
- Cache write: after successful API response
- Cache expiry: NEVER expires (static KJV text is immutable)
- Cache read failure: silently proceeds to API
- Cache write failure: silently ignored (not critical)

### Timeout
10 seconds via AbortController. On timeout: `buildPlaceholderVerses()`.

### Offline Mode
- If chapter cached: works perfectly offline
- If chapter never loaded: shows placeholder text "Loading {Book} {ch}:{v}... Connect to the internet to download this chapter."
- First load requires internet. Subsequent loads work offline.

### Non-KJV Translations (P0 Gap)
The app currently fetches KJV text regardless of selected translation. It tags verses with `selectedTranslation` but returns KJV text. bible-api.com does not support NIV/ESV/NLT/NASB/MSG (copyright). To implement real multi-translation support, a different API is needed (e.g. API.Bible with copyright-licensed translations).

### Verse Count Table
Complete static table in `src/services/verse.ts` (`VERSE_COUNTS`) — all 66 books, all chapters. Fallback: 25 if book/chapter not found (should not occur).

---

## 11. STREAK LOGIC (complete specification)

### Recording a Reading (`StorageService.recordReading()`)
```
1. Load StreakData from AsyncStorage @ss_streak_data
2. Get today as "YYYY-MM-DD" (device local time, no UTC conversion)
3. If readDates.includes(today): return unchanged (idempotent)
4. Push today to readDates
5. totalDaysRead += 1
6. Get yesterday as "YYYY-MM-DD"
7. If lastReadDate === yesterday: currentStreak += 1  (continuing streak)
   Else if lastReadDate !== today: currentStreak = 1  (broken or first day)
8. lastReadDate = today
9. If currentStreak > longestStreak: longestStreak = currentStreak
10. Save to AsyncStorage
11. Return updated StreakData
```

### Streak Reset Conditions
A streak is broken if `lastReadDate` is neither today nor yesterday. The streak resets to 1 (not 0) on the next read. There is NO grace period in the current implementation.

### Grace Period
**None implemented.** If you miss a day, streak resets. `StreakIntelligence.isStreakBroken()` detects this for UI messaging but does not protect the streak.

### Timezone Handling
`getToday()` uses `new Date()` with JS local date methods (getFullYear, getMonth, getDate). No UTC. No timezone library. This means: if user is flying and crosses midnight in a different timezone, the date used for streak tracking shifts with device timezone. No normalization.

### Date Format
"YYYY-MM-DD" using zero-padded month/day. Hardcoded formatting (not ISO string sliced — manual formatting to avoid UTC offset issues).

### hasReadToday()
Returns `streak.readDates.includes(getToday())`.

### Milestone Trigger
Milestones are visual only (badges in StreaksScreen). No push notification is sent at milestone (notification code exists in `NotificationService.sendMilestoneNotification()` but is never called from any screen or service).

### Store Review Trigger (DailyScreen only)
```typescript
const reviewMilestones = [7, 14, 30]; // total days read (not streak)
if (reviewMilestones.includes(updated.totalDaysRead)) {
  setTimeout(() => StoreReview.requestReview(), 2000);
}
```

### Streak Freeze
Data fields exist (`freezesUsedThisMonth`, `lastFreezeMonth`). Logic exists in `StreakIntelligence.getStreakFreezeInfo()`. No UI exposes it. P2 gap.

### isStreakBroken()
```typescript
if (!streak.lastReadDate) return false;  // never started
return last !== today && last !== yesterday && streak.currentStreak > 0;
```
Note: if currentStreak is 0 and lastReadDate exists, NOT considered broken (streak was already reset).

---

## 12. NOTIFICATIONS SPEC

### Provider
`expo-notifications` (v0.29.14)

### Permission Request
Triggered at onboarding step 9 ("Enable Reminders" button). Uses `requestPermissionsAsync()`. If denied, app continues without notifications (no retry).

### Daily Reminder Scheduling
- Cancels all existing scheduled notifications first
- Schedules ONE daily notification using `DAILY` trigger (recurring at set time)
- Title: "Today's Verse: {Book chapter:verse}"
- Body: First 120 chars of verse text + "..."
- Subtitle: "Scripture Streak"
- Data: `{ type: 'daily_verse', verseRef: ref }`
- Sound: true
- Badge: false
- The verse shown in notification is TOMORROW's verse (next day-of-year index)

### Re-scheduling
When notification time changes in Settings: old notifications cancelled, new one scheduled immediately if reminders are enabled.

### Milestone Notifications
`sendMilestoneNotification()` exists but is never called. P2 gap.

### Background Modes
`UIBackgroundModes: ['remote-notification']` in Info.plist.

### Platform
Web: all notification calls are no-ops (Platform.OS === 'web' early return).
iOS: requires notification permission, schedules via expo-notifications.

---

## 13. SOUND DESIGN

### Sound Engine
File: `src/sounds/SoundEngine.ts`
Using: `expo-av` Audio
Silent mode: `playsInSilentModeIOS: true`
Master volume: 0.7 (global, non-configurable in UI)
Mute state: `isMuted` boolean (no UI toggle — mute not exposed)

### Preloaded Sounds (on app init)
`tap`, `success`, `toggle` — preloaded during `initSounds()` called in App.tsx.

### Lazy-loaded Sounds
`tapHeavy`, `swipe`, `error`, `permissionGranted`, `premium`, `analyzeComplete` — loaded on first play, cached.

### Sound Files (all WAV, in `assets/sounds/`)
| File | Used When |
|------|-----------|
| tap.wav | Bookmark, copy actions |
| tap_heavy.wav | (available, not wired) |
| toggle.wav | Onboarding option selection |
| swipe.wav | Onboarding step transition |
| success.wav | Mark as Read, purchase success, onboarding complete |
| error.wav | (available, not wired) |
| permission_granted.wav | (available, not wired) |
| premium.wav | Upgrade button in Settings |
| analyze_complete.wav | (available, not wired) |

### Wired Sound Calls (verify with grep)
```bash
grep -rn "playSound" src/screens/
# Expected calls:
# DailyScreen: 'success' (mark as read), 'tap' (bookmark)
# OnboardingFlow: 'swipe' (step transition), 'toggle' (option select), 'success' (complete)
# SettingsScreen: 'success' (purchase success), 'tap' (restore)
```

### Missing Sound Wiring (gaps)
- StreaksScreen: no `playSound` calls despite touchable elements
- BibleScreen: no `playSound` calls
- PlansScreen: no `playSound` calls (only haptic calls)
- tap_heavy, error, permissionGranted, analyzeComplete: loaded in cache but never played

---

## 14. QA CHECKLIST

### Functional Tests

**Onboarding flow:**
- [ ] All 12 steps render without crash
- [ ] Progress bar fills correctly at each step
- [ ] Back navigation works from steps 1–11
- [ ] Goal selection required before advancing from step 1
- [ ] Stripe URL opens in browser (Linking.canOpenURL returns true)
- [ ] AppState listener fires on return from browser
- [ ] Alert shows "Did you complete your purchase?"
- [ ] Yes → premium stored in AsyncStorage, onboarding completes
- [ ] No → error thrown, onboarding paywall stays
- [ ] "Continue with Free Plan" first tap → rescue offer shown
- [ ] Second decline → `saveAndComplete()` called, enters app as free
- [ ] After onboarding: `@ss_onboarding_v2_complete = 'true'` written

**DailyScreen:**
- [ ] Verse of the day shows correct KJV verse for current day-of-year
- [ ] Verse changes at midnight (day-of-year index increments)
- [ ] "Mark Today as Read" increments streak
- [ ] Tapping twice: second tap no-ops (idempotent)
- [ ] After marking: completion card shows, button disappears
- [ ] Pull-to-refresh: streak data reloads
- [ ] Share: system share sheet opens with formatted verse text
- [ ] Copy: clipboard set, "Copied" shown for 2s
- [ ] Bookmark: saved to AsyncStorage, icon fills
- [ ] At 7 total days: review prompt fires after 2s delay
- [ ] Store review prompt does NOT fire on day 1

**StreaksScreen:**
- [ ] Current streak number matches `streak.currentStreak`
- [ ] Ring animation plays on load (scale + rotation)
- [ ] Calendar shows correct days in gold for read dates
- [ ] Month navigation works forward and backward
- [ ] Milestone badges unlock at 7, 30, 100, 365 days
- [ ] Free users: extended stats row NOT visible
- [ ] Free users: upsell card visible with lock icon
- [ ] Premium users: extended stats row visible (week/month/year)
- [ ] Consistency bar: accurate 30-day calculation

**BibleScreen:**
- [ ] Books list loads all 66 books
- [ ] Search filters books in real time
- [ ] OT/NT filter works
- [ ] Tap book → chapter grid shows correct number of cells
- [ ] Tap chapter → verse loading spinner shows → verses load from API
- [ ] Verse text shows in Georgia/serif font
- [ ] Cache works: closing and re-opening same chapter loads instantly (no spinner)
- [ ] Offline: previously loaded chapters show cached text
- [ ] Offline: unloaded chapters show placeholder text
- [ ] Free user: tapping NIV shows Premium alert
- [ ] Premium user: translation picker changes label but text is still KJV (known gap)
- [ ] Breadcrumb back button works from verses → chapters → books

**PlansScreen:**
- [ ] 6 plans visible in list
- [ ] Free user: lock icon shown on each plan card
- [ ] Free user: tapping "Start Plan" shows Premium alert (not crash)
- [ ] Premium user: Start Plan creates progress entry
- [ ] Mark Today increments day count
- [ ] Mark Today idempotent (double-tap same day no-ops)
- [ ] Progress bar updates after Mark Today
- [ ] Plan detail "Reading Schedule" shows all days

**SettingsScreen:**
- [ ] Notification time change re-schedules daily reminder
- [ ] Toggle off: `cancelAllScheduled()` called
- [ ] Toggle on: `scheduleDailyReminder()` called
- [ ] Reset All Data: confirmation alert shows
- [ ] Reset All Data: clears streak, does NOT remove premium
- [ ] Translation picker: non-KJV locked for free users
- [ ] Daily goal counter: min 1, max 10
- [ ] Upgrade button opens Stripe annual URL
- [ ] "Manage Subscription" opens Stripe portal
- [ ] Privacy, Terms, Support links open correct URLs

### Edge Cases

- **Zero streak state:** App fresh install — streak shows 0, no ring animation crash
- **First day read:** currentStreak becomes 1, longestStreak becomes 1
- **Broken streak message:** `lastReadDate` is 3 days ago — `isStreakBroken()` returns true, message changes
- **Reset then re-read:** After data reset, reading again starts streak at 1
- **Year rollover:** Day-of-year index wraps back to 1 on Jan 1 (uses `Math.floor(diff / oneDay)` from start of year)
- **Bible API rate limit:** If 429 returned, placeholder verses shown (API error catch is broad)
- **AsyncStorage full:** All writes silently catch — app degrades gracefully
- **Notification time "06:00":** Edge case — if user opens app at 5:59 AM and notification fires at 6:00, no conflict
- **Multiple tab mounts:** Premium sync called on every tab mount — if user buys on one tab, others sync on next focus
- **Deep link before onboarding complete:** Handled — `@scripture_streak_premium` written, but user still sees onboarding

### Build Checks

```bash
# TypeScript compile
npx tsc --noEmit

# Expo export (pre-submission)
npx expo export --platform ios

# Native build
npx expo prebuild --platform ios
npx expo run:ios

# Verify sound files exist
ls assets/sounds/*.wav | wc -l  # should be 9

# Verify AsyncStorage keys don't conflict with other apps
grep -rn "@ss_" src/ | grep -v ".test."

# Verify no hardcoded test data in production screens
grep -rn "TODO\|FIXME\|PLACEHOLDER\|MOCK\|stub" src/ --include="*.tsx" --include="*.ts"
```

---

## 15. APP STORE SUBMISSION CHECKLIST

### Bundle & Metadata
- [x] Bundle ID: `com.printmaxx.scripturestreak` (unique)
- [x] Version: 1.0.0 / Build 1
- [x] Display name: "Scripture Streak"
- [x] Category: Lifestyle (LSApplicationCategoryType = public.app-category.lifestyle)
- [x] Orientation: portrait only
- [x] Tablet support: `supportsTablet: true`

### Privacy & Legal
- [x] Privacy Policy URL resolves: printmaxx-privacy.surge.sh
- [x] Terms URL resolves: printmaxx-tos.surge.sh
- [x] Notification permission string: "Scripture Streak sends daily verse reminders to help you maintain your reading streak"
- [x] ITSAppUsesNonExemptEncryption: false
- [x] No camera, microphone, contacts, location usage (no permission strings needed)

### Subscription Compliance (Apple 3.1.1 / 3.1.2)
- [x] Subscription auto-renewal disclosure on paywall: "Subscription automatically renews unless canceled at least 24 hours before the end of the current period."
- [x] "Manage subscriptions in your Apple ID account settings" — present on PaywallScreen
- [ ] NOTE: App uses Stripe (external payment), NOT Apple IAP. Apple may flag this as a violation. Risk: app rejection if Apple detects external payment for digital content. See P0 gap below.
- [x] Restore Purchases button: present on PaywallScreen and SettingsScreen
- [x] Terms and Privacy links on paywall: present

### Content
- [x] No placeholder text in production screens
- [x] Real Bible verse content (KJV public domain — no rights issues)
- [x] App name does not clash with "Bible Streak" or "YouVersion" — unique enough
- [x] No user-generated content (no moderation needed)
- [x] Religious content: covered under free expression, no age restriction needed

### Assets Required (check before submit)
- [ ] App icon: 1024×1024 PNG, no alpha channel (`assets/icon.png` exists — verify dimensions)
- [ ] Splash screen icon (`assets/splash-icon.png` exists)
- [ ] Adaptive icon for Android (`assets/adaptive-icon.png` exists)
- [ ] Screenshots: minimum 3 per device size (6.5" and 5.5" required)
- [ ] App preview video: optional but recommended

### Technical
- [ ] `npx expo export --platform ios` passes with 0 errors
- [ ] No console.log/console.warn in production paths (check: `grep -rn "console\." src/ --include="*.tsx" --include="*.ts"`)
- [ ] All required sound files present in `assets/sounds/`
- [ ] CrimsonText and Inter fonts properly configured in expo-font plugin

---

## 16. KNOWN PRODUCTION GAPS

### P0 (Ship Blocker)

**P0-1: Stripe vs Apple IAP — Rejection Risk**
Apple requires that apps selling digital subscriptions use Apple IAP (App Store Guidelines 3.1.1). Using Stripe Payment Links (external browser) for digital content subscriptions may result in app rejection. The "honor system" confirmation ("Did you complete your purchase?") is not a supported purchase flow.
**Fix:** Implement RevenueCat + Apple IAP. Stripe is currently the ONLY payment method.
**Grep:** `grep -n "Linking.openURL" src/services/purchases.ts`

**P0-2: Premium State Lost on Reinstall**
Premium status stored in AsyncStorage only. Reinstall clears all AsyncStorage. "Restore Purchases" reads the same AsyncStorage key — also cleared after reinstall. User pays, reinstalls, pays again.
**Fix:** Server-side entitlement check (RevenueCat solves this) OR at minimum, Stripe customer email lookup on restore.

**P0-3: Non-KJV Translations Show KJV Text**
Bible API only provides KJV. When a premium user selects NIV/ESV/NLT/NASB/MSG in BibleScreen, the verses fetched and displayed are still KJV. The translation label shows "NIV" but text is KJV. This is misleading.
**Fix:** Integrate API.Bible or Scripture API with licensed translations. Or clearly disclose "KJV text provided for all translations" (weaker fix).
**Grep:** In `BibleScreen.tsx`: `setChapterVerses(verses.map(v => ({ ...v, translation: selectedTranslation })))` — this re-labels KJV as NIV.

### P1 (Fix Before Marketing)

**P1-1: Rate the App — Dead Tap**
Settings "Rate the App" row has chevron but no action wired. Tap does nothing.
**Fix:** `await StoreReview.requestReview()` or `Linking.openURL(APP_STORE_URL)`.
**Grep:** `grep -A5 "Rate the App" src/screens/SettingsScreen.tsx`

**P1-2: Paywall Screen Not Reachable in Main App**
`PaywallScreen.tsx` exists as a standalone component but is never mounted in any navigator screen. Users who start as free and want to upgrade mid-flow have to go through Settings only.
**Fix:** Wire PaywallScreen as a modal in SettingsScreen upgrade flow OR accept Settings-only upgrade path is sufficient (it has the upgrade button inline).

**P1-3: Sound Missing on Streaks, Bible, Plans Screens**
StreaksScreen, BibleScreen, PlansScreen have no `playSound()` calls despite having touchable elements. The app feels inconsistent — tapping in Daily triggers sounds, tapping in Bible is silent.
**Fix:** Add `playSound('tap')` to all touchable actions in these screens.

**P1-4: Milestone Notifications Never Fire**
`NotificationService.sendMilestoneNotification()` exists but is never called. User hits 7-day streak, nothing happens.
**Fix:** Call from `StorageService.recordReading()` or from `DailyScreen.handleMarkAsRead()` after checking milestone thresholds.

**P1-5: Restore Purchases Misleading for Free Users Who Never Purchased**
Tapping "Restore Purchases" for a user who never paid but sees the button in PaywallScreen gives "No Purchase Found." The help text on SettingsScreen explains Stripe subscription management, but the experience is confusing.
**Fix:** Clearer UX copy explaining Stripe-based subscriptions and how to look up purchase status.

### P2 (Nice to Have)

**P2-1: Streak Freeze UI Never Exposed**
`StreakIntelligence.getStreakFreezeInfo()` and `StreakData.freezesUsedThisMonth` exist but no UI shows or uses streak freezes.

**P2-2: dailyGoalVerses Setting Unused**
Counter in Settings can be set 1–10 but no screen checks this value or adjusts daily goals.

**P2-3: ReadingProgress Object Unused**
`@ss_reading_progress` tracks currentBook/chapter/completedBooks/completedChapters but nothing writes to it from BibleScreen or reads from it to show progress.

**P2-4: Error Sound Never Played**
`error.wav` is loaded but `playSound('error')` is never called (purchase errors are caught silently).

**P2-5: No Haptic on Mark as Read Success Animation**
`handleMarkAsRead` fires haptic success notification (correct), but the spring animation could also use an `impactAsync` on completion.

**P2-6: OnboardingScreen.tsx Unused File**
`src/screens/OnboardingScreen.tsx` exists (separate from OnboardingFlow.tsx). Not imported anywhere. Dead code.

**P2-7: Verse of the Day Always KJV**
DailyScreen always shows KJV from static DAILY_VERSES_KJV. Premium users' preferred translation is not applied to the daily verse. Consistent with app behavior, but may be unexpected.

---

## 17. COLOR SYSTEM REFERENCE

```typescript
// src/constants/theme.ts — Colors
background:    '#FFFBF5'  // warm white
surface:       '#FFFFFF'
navy:          '#1A1A2E'  // primary dark
gold:          '#E2B53F'  // primary accent
goldLight:     '#F0D078'
goldDark:      '#C49A2A'
goldMuted:     '#E2B53F30' // 19% opacity
textPrimary:   '#1A1A2E'
textSecondary: '#6B6B80'
textMuted:     '#9E9EB0'
textOnDark:    '#FFFBF5'
success:       '#4CAF50'
successLight:  '#E8F5E9'
error:         '#D32F2F'
streakFire:    '#FF6B35'
border:        '#E8E0D4'
borderLight:   '#F0EBE3'
```

---

## 18. TYPOGRAPHY SYSTEM REFERENCE

```typescript
// src/constants/theme.ts — Typography
h1:            28px, weight 700, navy, -0.5 letterSpacing, SF Pro Display (iOS)
h2:            22px, weight 700, navy, -0.3 letterSpacing
h3:            18px, weight 600, navy
body:          16px, weight 400, navy, 24px line height
bodySmall:     14px, weight 400, textSecondary, 20px line height
caption:       12px, weight 600, textMuted, 1.0 letterSpacing, UPPERCASE
verseText:     22px, weight 400, 36px line height, CrimsonText_400Regular
verseRef:      14px, weight 700, gold, 0.5 letterSpacing
button:        17px, weight 600, 0.2 letterSpacing
heroNumber:    48px, weight 200, gold, -2 letterSpacing, tabular-nums
```

---

## 19. BUILD AND RUN COMMANDS

```bash
# Development
npx expo prebuild --platform ios
npx expo run:ios

# Production export check
npx expo export --platform ios

# TypeScript check
npx tsc --noEmit

# Verify onboarding key written
# (in Expo DevTools or Metro Bundler — AsyncStorage inspector)

# Verify sounds load
# (check metro logs for require() errors on assets/sounds/*.wav)

# Screenshot QA (after build)
xcrun simctl io booted screenshot /tmp/scripture-streak-daily.png
open /tmp/scripture-streak-daily.png

# Deep link test
xcrun simctl openurl booted "scripture-streak://premium-activated"

# Full clean rebuild
cd ios && pod install && cd ..
npx expo prebuild --clean --platform ios
npx expo run:ios --no-install
```

---

## 20. SPEC COMPLETENESS

This spec was derived from reading the following source files in full:
- `App.tsx` — root navigation, onboarding check, deep link handler
- `app.json` — bundle config, permissions, plugins
- `package.json` — all dependencies and versions
- `src/screens/OnboardingFlow.tsx` — 12-step onboarding with embedded paywall
- `src/screens/PaywallScreen.tsx` — standalone paywall component
- `src/screens/DailyScreen.tsx` — daily verse, mark as read, streaks
- `src/screens/StreaksScreen.tsx` — streak visualization, calendar, milestones
- `src/screens/BibleScreen.tsx` — Bible navigator, translations, verse browsing
- `src/screens/PlansScreen.tsx` — reading plans with premium gate
- `src/screens/SettingsScreen.tsx` — all settings, purchase management
- `src/navigation/TabNavigator.tsx` — 5-tab bottom navigation
- `src/services/verse.ts` — bible-api.com integration, caching, VERSE_COUNTS
- `src/services/storage.ts` — all AsyncStorage operations, streak logic
- `src/services/purchases.ts` — Stripe Payment Links, premium state
- `src/services/notifications.ts` — expo-notifications daily scheduling
- `src/services/streakIntelligence.ts` — advanced stats, milestones, messages
- `src/sounds/SoundEngine.ts` — expo-av sound engine, 9 sound files
- `src/constants/theme.ts` — colors, typography, spacing
- `src/constants/bible.ts` — 66 BIBLE_BOOKS, 6 TRANSLATIONS
- `src/constants/plans.ts` — 6 READING_PLANS definitions
- `src/types/index.ts` — all TypeScript interfaces

An agent building from this spec should produce an app functionally identical to the current codebase with all P0 gaps addressed.
