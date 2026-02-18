# WalkToUnlock - Technical Specification

---

## Stack Overview

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Framework | React Native | Cross-platform, same codebase as PrayerLock |
| Language | TypeScript | Type safety |
| State | Zustand | Lightweight state management |
| Storage | AsyncStorage + MMKV | Fast local persistence |
| Health Data | HealthKit (iOS) / Google Fit (Android) | Official platform APIs |
| Subscriptions | RevenueCat | Handles subscriptions |
| Analytics | Mixpanel | Free tier sufficient |
| Push | Firebase Cloud Messaging | Free, reliable |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      WalkToUnlock App                        │
├─────────────────────────────────────────────────────────────┤
│  Screens                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Onboard  │ │  Home    │ │ Progress │ │ Settings │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│  Core Services                                               │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│  │  StepService   │ │ BlockerService │ │ StreakService  │   │
│  └────────────────┘ └────────────────┘ └────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Native Modules                                              │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│  │ HealthKit(iOS) │ │GoogleFit(And)  │ │  AppBlocker    │   │
│  └────────────────┘ └────────────────┘ └────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  External                                                    │
│  ┌──────────┐ ┌──────────┐                                  │
│  │RevenueCat│ │ Firebase │                                  │
│  └──────────┘ └──────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Platform-Specific Implementation

### iOS (HealthKit)

**Permissions Required:**
- `NSHealthShareUsageDescription` - Read step count
- Background App Refresh enabled

**Key Implementation:**
```swift
import HealthKit

let healthStore = HKHealthStore()
let stepType = HKQuantityType.quantityType(forIdentifier: .stepCount)!

// Request authorization
healthStore.requestAuthorization(toShare: nil, read: [stepType]) { success, error in
    // Handle result
}

// Query today's steps
let startOfDay = Calendar.current.startOfDay(for: Date())
let predicate = HKQuery.predicateForSamples(withStart: startOfDay, end: Date())

let query = HKStatisticsQuery(quantityType: stepType,
                               quantitySamplePredicate: predicate,
                               options: .cumulativeSum) { _, result, _ in
    let steps = result?.sumQuantity()?.doubleValue(for: .count()) ?? 0
    // Return steps to React Native
}
healthStore.execute(query)
```

**React Native Bridge:**
Use `react-native-health` package or create custom native module.

---

### Android (Google Fit)

**Permissions Required:**
- `ACTIVITY_RECOGNITION`
- Google Fit API access

**Key Implementation:**
```kotlin
import com.google.android.gms.fitness.Fitness
import com.google.android.gms.fitness.data.DataType

// Request permissions
val fitnessOptions = FitnessOptions.builder()
    .addDataType(DataType.TYPE_STEP_COUNT_DELTA, FitnessOptions.ACCESS_READ)
    .build()

// Get today's steps
val response = Fitness.getHistoryClient(context, account)
    .readDailyTotal(DataType.TYPE_STEP_COUNT_DELTA)
    .addOnSuccessListener { dataSet ->
        val steps = dataSet.dataPoints.firstOrNull()
            ?.getValue(Field.FIELD_STEPS)?.asInt() ?: 0
        // Return steps to React Native
    }
```

**React Native Bridge:**
Use `react-native-google-fit` package.

---

### App Blocking (Same as PrayerLock)

Reuse blocking implementation from PrayerLock:
- iOS: Screen Time API (FamilyControls)
- Android: UsageStats + Accessibility Service

---

## Data Models

### User Settings
```typescript
interface UserSettings {
  stepGoal: number;              // 1000-20000
  blockedApps: string[];         // Bundle IDs
  dailyResetTime: string;        // "00:00" (midnight default)
  notificationsEnabled: boolean;
  emergencyUnlockEnabled: boolean;
}
```

### Step Data
```typescript
interface StepData {
  date: string;           // YYYY-MM-DD
  steps: number;
  goalMet: boolean;
  unlockedAt: number | null;  // timestamp
  wasEmergencyUnlock: boolean;
}
```

### Streak Data
```typescript
interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  completedDates: string[];
  lastCompletedDate: string | null;
}
```

### App State
```typescript
interface AppState {
  currentSteps: number;
  stepGoal: number;
  isUnlocked: boolean;
  lastUpdated: number;    // timestamp
  todayCompleted: boolean;
}
```

---

## Background Step Fetching

### Strategy
1. App launch: Fetch current steps
2. Background refresh: Every 15 minutes (iOS limit)
3. Pull-to-refresh: Manual update
4. When app becomes active: Refresh immediately

### iOS Background Fetch
```typescript
// Configure in AppDelegate
UIApplication.shared.setMinimumBackgroundFetchInterval(
  UIApplication.backgroundFetchIntervalMinimum
)

// Handle background fetch
func application(_ application: UIApplication,
                 performFetchWithCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {
    // Fetch steps from HealthKit
    // Check if goal met
    // Update blocking state
    // Send notification if unlocked
    completionHandler(.newData)
}
```

### Android Background Service
```kotlin
class StepCheckService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Check steps every 5 minutes
        // Update blocking state
        // Send notification if unlocked
        return START_STICKY
    }
}
```

---

## Unlock Logic

```typescript
async function checkUnlockStatus(): Promise<boolean> {
  const settings = await getSettings();
  const steps = await fetchCurrentSteps();

  // Already unlocked today?
  const today = getCurrentDate();
  const todayData = await getStepData(today);
  if (todayData?.goalMet) {
    return true; // Stay unlocked
  }

  // Check if goal met
  if (steps >= settings.stepGoal) {
    await markGoalMet(today, steps);
    await unblockApps();
    await sendUnlockNotification();
    await updateStreak();
    return true;
  }

  return false;
}
```

---

## File Structure

```
walktounlock/
├── src/
│   ├── screens/
│   │   ├── OnboardingScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── ProgressScreen.tsx
│   │   ├── StatsScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── PaywallScreen.tsx
│   ├── components/
│   │   ├── StepProgress.tsx
│   │   ├── ProgressRing.tsx
│   │   ├── GoalSelector.tsx
│   │   ├── AppSelector.tsx
│   │   ├── StreakBadge.tsx
│   │   └── CalendarView.tsx
│   ├── services/
│   │   ├── stepService.ts
│   │   ├── blockerService.ts
│   │   ├── streakService.ts
│   │   └── subscriptionService.ts
│   ├── stores/
│   │   ├── userStore.ts
│   │   └── stepStore.ts
│   ├── native/
│   │   ├── ios/
│   │   │   ├── HealthKitManager.swift
│   │   │   └── AppBlocker.swift
│   │   └── android/
│   │       ├── GoogleFitModule.kt
│   │       └── AppBlockerModule.kt
│   ├── utils/
│   │   ├── dateUtils.ts
│   │   └── constants.ts
│   └── App.tsx
├── ios/
├── android/
├── package.json
└── tsconfig.json
```

---

## Native Module: HealthKitManager (iOS)

```swift
import HealthKit

@objc(HealthKitManager)
class HealthKitManager: NSObject {

    private let healthStore = HKHealthStore()
    private let stepType = HKQuantityType.quantityType(forIdentifier: .stepCount)!

    @objc
    func requestPermissions(_ resolve: @escaping RCTPromiseResolveBlock,
                           reject: @escaping RCTPromiseRejectBlock) {
        healthStore.requestAuthorization(toShare: nil, read: [stepType]) { success, error in
            if success {
                resolve(true)
            } else {
                reject("HEALTH_ERROR", error?.localizedDescription, error)
            }
        }
    }

    @objc
    func getTodaySteps(_ resolve: @escaping RCTPromiseResolveBlock,
                       reject: @escaping RCTPromiseRejectBlock) {
        let startOfDay = Calendar.current.startOfDay(for: Date())
        let predicate = HKQuery.predicateForSamples(withStart: startOfDay, end: Date())

        let query = HKStatisticsQuery(
            quantityType: stepType,
            quantitySamplePredicate: predicate,
            options: .cumulativeSum
        ) { _, result, error in
            if let error = error {
                reject("QUERY_ERROR", error.localizedDescription, error)
                return
            }
            let steps = result?.sumQuantity()?.doubleValue(for: .count()) ?? 0
            resolve(Int(steps))
        }
        healthStore.execute(query)
    }
}
```

---

## Native Module: GoogleFitModule (Android)

```kotlin
class GoogleFitModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName() = "GoogleFit"

    @ReactMethod
    fun requestPermissions(promise: Promise) {
        val fitnessOptions = FitnessOptions.builder()
            .addDataType(DataType.TYPE_STEP_COUNT_DELTA, FitnessOptions.ACCESS_READ)
            .build()

        // Handle Google Sign-In and permissions
        // Resolve promise on success
    }

    @ReactMethod
    fun getTodaySteps(promise: Promise) {
        val response = Fitness.getHistoryClient(context, getLastSignedInAccount(context)!!)
            .readDailyTotal(DataType.TYPE_STEP_COUNT_DELTA)

        response.addOnSuccessListener { dataSet ->
            val steps = dataSet.dataPoints.firstOrNull()
                ?.getValue(Field.FIELD_STEPS)?.asInt() ?: 0
            promise.resolve(steps)
        }

        response.addOnFailureListener { e ->
            promise.reject("FIT_ERROR", e.message)
        }
    }
}
```

---

## Progress Ring Component

```typescript
// components/ProgressRing.tsx
import Svg, { Circle } from 'react-native-svg';

interface Props {
  progress: number;  // 0-1
  steps: number;
  goal: number;
}

export function ProgressRing({ progress, steps, goal }: Props) {
  const radius = 100;
  const strokeWidth = 15;
  const circumference = 2 * Math.PI * radius;
  const progressOffset = circumference * (1 - progress);

  return (
    <View style={styles.container}>
      <Svg width={250} height={250}>
        {/* Background circle */}
        <Circle
          cx={125}
          cy={125}
          r={radius}
          stroke="#E5E5E5"
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Progress circle */}
        <Circle
          cx={125}
          cy={125}
          r={radius}
          stroke="#4CAF50"
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={progressOffset}
          strokeLinecap="round"
          transform="rotate(-90 125 125)"
        />
      </Svg>
      <View style={styles.textContainer}>
        <Text style={styles.steps}>{steps.toLocaleString()}</Text>
        <Text style={styles.goal}>/ {goal.toLocaleString()}</Text>
        <Text style={styles.remaining}>
          {Math.max(0, goal - steps).toLocaleString()} to go
        </Text>
      </View>
    </View>
  );
}
```

---

## Security Considerations

### Step Data Integrity
- Only read from official HealthKit/Google Fit APIs
- Don't accept manual step entry in MVP
- Users can game with third-party step apps, accept this tradeoff

### Privacy
- Step data stays on device
- No server uploads for MVP
- Clear privacy policy about health data usage

### Preventing Bypasses
- Same approach as PrayerLock
- Emergency unlock with friction
- Log all bypasses

---

## Performance Targets

| Metric | Target |
|--------|--------|
| App launch | < 2s |
| Step fetch | < 1s |
| Background update | Every 15 min (iOS) / 5 min (Android) |
| Battery impact | < 3% daily |
| Storage usage | < 30MB |

---

## Testing Strategy

### Unit Tests
- Streak calculation
- Progress percentage
- Date utilities

### Integration Tests
- HealthKit/Google Fit mocks
- Subscription flow
- Blocking state changes

### Manual Testing
- Real devices with actual step data
- Background fetch behavior
- Edge cases (midnight rollover, timezone changes)
- Step goal edge (exactly at goal, one under)

---

## Deployment

### iOS
- TestFlight beta
- App Store with health category
- Required: Privacy nutrition label for HealthKit

### Android
- Internal testing track
- Google Play (Health & Fitness category)
- Required: Google Fit API approval

### CI/CD
- GitHub Actions
- Fastlane
- Semantic versioning

---

## Cost Estimate

| Item | Monthly Cost |
|------|--------------|
| RevenueCat | Free (until $2.5k MRR) |
| Firebase | Free tier |
| Mixpanel | Free tier |
| Apple Developer | $8.25 |
| Google Play | $2.08 |
| Google Fit API | Free |
| **Total** | ~$10/mo |

---

## Code Sharing with PrayerLock

### Reusable Components
- App selector UI
- Paywall screen
- Streak tracking logic
- Calendar view
- Settings screens
- Emergency unlock flow

### Reusable Services
- Blocker service (platform-specific)
- Subscription service
- Streak service
- Analytics wrapper

### Potential Monorepo Structure
```
apps/
├── prayerlock/
├── walktounlock/
└── shared/
    ├── components/
    ├── services/
    └── native/
```

This allows faster development of the second app.
