# PrayerLock - Technical Specification

---

## Stack Overview

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Framework | React Native | Cross-platform, large community, mature ecosystem |
| Language | TypeScript | Type safety, better DX |
| State | Zustand | Simple, lightweight, no boilerplate |
| Storage | AsyncStorage + MMKV | Fast local persistence |
| Subscriptions | RevenueCat | Industry standard, handles all edge cases |
| Analytics | Mixpanel | Free tier sufficient for MVP |
| Bible API | bible-api.com | Free, no auth required |
| Push | Firebase Cloud Messaging | Free, reliable |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       PrayerLock App                         │
├─────────────────────────────────────────────────────────────┤
│  Screens                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Onboard  │ │  Home    │ │  Timer   │ │ Settings │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│  Core Services                                               │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│  │ BlockerService │ │ DevotionService│ │ StreakService  │   │
│  └────────────────┘ └────────────────┘ └────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Native Modules                                              │
│  ┌────────────────┐ ┌────────────────┐                      │
│  │ UsageStats (A) │ │ ScreenTime(iOS)│                      │
│  └────────────────┘ └────────────────┘                      │
├─────────────────────────────────────────────────────────────┤
│  External                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │RevenueCat│ │ BibleAPI │ │ Firebase │                    │
│  └──────────┘ └──────────┘ └──────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Platform-Specific Implementation

### iOS (Screen Time API)

Apple's Screen Time API (iOS 15+) allows apps to:
- Request permission to block apps
- Set app limits programmatically
- Create managed settings profiles

**Key APIs:**
```swift
import FamilyControls
import ManagedSettings
import DeviceActivity

// Request authorization
AuthorizationCenter.shared.requestAuthorization(for: .individual)

// Create managed settings
let store = ManagedSettingsStore()
store.shield.applications = selectedApps
```

**React Native Bridge:**
Use `react-native-screen-time-api` or create custom native module.

**Permissions Required:**
- Screen Time API authorization
- Notifications (optional)

---

### Android (UsageStats + Accessibility)

Android requires combination of APIs:
- UsageStats for detecting app launches
- Accessibility Service for blocking (overlay)
- Or Device Admin API for enterprise-level control

**Key Implementation:**
```kotlin
// Check current foreground app
val usm = getSystemService(USAGE_STATS_SERVICE) as UsageStatsManager
val stats = usm.queryUsageStats(...)

// Overlay when blocked app detected
val overlayView = LayoutInflater.inflate(R.layout.block_overlay, null)
windowManager.addView(overlayView, overlayParams)
```

**React Native Bridge:**
Use `react-native-app-usage` or create custom native module.

**Permissions Required:**
- `PACKAGE_USAGE_STATS`
- `SYSTEM_ALERT_WINDOW` (overlay)
- Accessibility Service enabled

---

## Data Models

### User Settings
```typescript
interface UserSettings {
  blockedApps: string[];           // Bundle IDs
  devotionDurationMinutes: number; // 5-60
  dailyResetTime: string;          // "05:00"
  requireScripture: boolean;
  requireTimer: boolean;
  emergencyUnlockEnabled: boolean;
  notificationsEnabled: boolean;
}
```

### Devotion Session
```typescript
interface DevotionSession {
  id: string;
  date: string;              // YYYY-MM-DD
  startedAt: number;         // timestamp
  completedAt: number | null;
  timerDuration: number;     // seconds
  scriptureRead: boolean;
  scripturePassage: string;
  wasEmergencyUnlock: boolean;
}
```

### Streak Data
```typescript
interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  completedDates: string[];  // YYYY-MM-DD array
  lastCompletedDate: string | null;
}
```

### Subscription State
```typescript
interface SubscriptionState {
  isSubscribed: boolean;
  trialEndsAt: number | null;
  subscriptionType: 'monthly' | 'annual' | 'lifetime' | null;
  expiresAt: number | null;
}
```

---

## API Integrations

### Bible API (bible-api.com)

**Endpoint:**
```
GET https://bible-api.com/john+3:16
```

**Response:**
```json
{
  "reference": "John 3:16",
  "verses": [
    {
      "book_id": "JHN",
      "book_name": "John",
      "chapter": 3,
      "verse": 16,
      "text": "For God so loved..."
    }
  ],
  "text": "For God so loved the world...",
  "translation_id": "web"
}
```

**Daily Verse Strategy:**
- Pre-define 365 passage references
- Index by day of year
- Cache responses locally

---

### RevenueCat Integration

**Setup:**
```typescript
import Purchases from 'react-native-purchases';

Purchases.configure({ apiKey: REVENUECAT_API_KEY });

// Check subscription status
const customerInfo = await Purchases.getCustomerInfo();
const isSubscribed = customerInfo.entitlements.active['pro'];

// Make purchase
const { customerInfo } = await Purchases.purchasePackage(selectedPackage);
```

**Products to Configure:**
| Product ID | Type | Price |
|------------|------|-------|
| prayerlock_monthly | Subscription | $9.99/mo |
| prayerlock_annual | Subscription | $49.99/yr |

**Entitlements:**
- `pro` - Full app access

---

### Firebase (Push Notifications)

**Use Cases:**
- Morning reminder (configurable time)
- Streak at risk warning (8pm if not completed)
- Weekly summary

**Implementation:**
```typescript
import messaging from '@react-native-firebase/messaging';

// Request permission
await messaging().requestPermission();

// Get token for targeting
const token = await messaging().getToken();

// Handle incoming
messaging().onMessage(async remoteMessage => {
  // Display local notification
});
```

---

## File Structure

```
prayerlock/
├── src/
│   ├── screens/
│   │   ├── OnboardingScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── TimerScreen.tsx
│   │   ├── ScriptureScreen.tsx
│   │   ├── StatsScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── PaywallScreen.tsx
│   ├── components/
│   │   ├── AppSelector.tsx
│   │   ├── TimerDisplay.tsx
│   │   ├── StreakBadge.tsx
│   │   ├── CalendarView.tsx
│   │   └── PaywallCard.tsx
│   ├── services/
│   │   ├── blockerService.ts
│   │   ├── devotionService.ts
│   │   ├── streakService.ts
│   │   ├── bibleService.ts
│   │   └── subscriptionService.ts
│   ├── stores/
│   │   ├── userStore.ts
│   │   └── devotionStore.ts
│   ├── native/
│   │   ├── ios/
│   │   │   └── ScreenTimeManager.swift
│   │   └── android/
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

## Native Module Requirements

### iOS Native Module: ScreenTimeManager

```swift
import FamilyControls
import ManagedSettings

@objc(ScreenTimeManager)
class ScreenTimeManager: NSObject {

    private let store = ManagedSettingsStore()

    @objc
    func requestAuthorization(_ resolve: @escaping RCTPromiseResolveBlock,
                              reject: @escaping RCTPromiseRejectBlock) {
        Task {
            do {
                try await AuthorizationCenter.shared.requestAuthorization(for: .individual)
                resolve(true)
            } catch {
                reject("AUTH_ERROR", error.localizedDescription, error)
            }
        }
    }

    @objc
    func blockApps(_ bundleIds: [String]) {
        // Implementation using ManagedSettings
    }

    @objc
    func unblockApps() {
        store.shield.applications = nil
    }
}
```

### Android Native Module: AppBlockerModule

```kotlin
class AppBlockerModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName() = "AppBlocker"

    @ReactMethod
    fun blockApps(packageNames: ReadableArray) {
        // Store blocked apps
        // Start foreground service
        // Monitor UsageStats
        // Show overlay when blocked app detected
    }

    @ReactMethod
    fun unblockApps() {
        // Clear blocked list
        // Stop monitoring
    }
}
```

---

## Security Considerations

### Preventing Bypasses

1. **App uninstall protection:**
   - Show warning on uninstall attempt
   - Log bypass to shame user

2. **Settings access:**
   - Optional: Block settings app too
   - Emergency unlock requires deliberate friction

3. **Time manipulation:**
   - Use server time for validation
   - Or detect system time changes

### Data Privacy

1. **Local-first:**
   - All data stored on device
   - No server-side user accounts for MVP

2. **Minimal permissions:**
   - Only request what's needed
   - Clear permission explanations

---

## Performance Targets

| Metric | Target |
|--------|--------|
| App launch | < 2s |
| Timer accuracy | +/- 1s |
| Battery impact | < 5% daily |
| Storage usage | < 50MB |
| Memory usage | < 100MB |

---

## Testing Strategy

### Unit Tests
- Streak calculation logic
- Date/time utilities
- Store state management

### Integration Tests
- RevenueCat purchase flow
- Bible API responses
- Push notification handling

### E2E Tests
- Full onboarding flow
- Complete devotion cycle
- Subscription purchase
- Emergency unlock

### Manual Testing
- App blocking on real device
- Background behavior
- Edge cases (midnight, timezone changes)

---

## Deployment

### iOS
- TestFlight for beta
- App Store Connect for release
- ASO: Keywords targeting "prayer", "devotional", "christian", "bible"

### Android
- Internal testing track for beta
- Google Play Console for release
- Similar ASO strategy

### CI/CD
- GitHub Actions for builds
- Fastlane for deployment automation
- Semantic versioning

---

## Cost Estimate

| Item | Monthly Cost |
|------|--------------|
| RevenueCat | Free (until $2.5k MRR) |
| Firebase | Free tier |
| Mixpanel | Free tier |
| Bible API | Free |
| Apple Developer | $8.25 ($99/yr) |
| Google Play | $2.08 ($25 one-time) |
| **Total** | ~$10/mo |

Scales to $0 variable cost until RevenueCat fees kick in at $2.5k MRR.
