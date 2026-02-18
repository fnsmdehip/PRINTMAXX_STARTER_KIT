# Expo & React Native Development Guide

Comprehensive guide for building PRINTMAXX apps with Expo SDK 54 and React Native. Covers project setup, native features, build pipeline, and deployment.

---

## Current Stack

**PRINTMAXX apps use:**
- Expo SDK 54 (~54.0.32)
- React Native 0.81.5
- React 19.1.0
- TypeScript 5.9.2
- Expo Router 6.x
- Zustand for state management

---

## 1. Project Setup

### Create New App

```bash
# Create new Expo project with TypeScript
npx create-expo-app@latest myapp --template tabs

# Or use blank template for more control
npx create-expo-app@latest myapp --template blank-typescript

cd myapp
```

### Recommended Project Structure

```
myapp/
├── app/                    # Expo Router pages
│   ├── (tabs)/            # Tab navigator group
│   │   ├── _layout.tsx    # Tab layout config
│   │   ├── index.tsx      # Home tab
│   │   └── settings.tsx   # Settings tab
│   ├── _layout.tsx        # Root layout
│   ├── onboarding.tsx     # Onboarding screen
│   └── paywall.tsx        # Paywall screen
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── index.ts       # Barrel export
│   ├── hooks/             # Custom hooks
│   │   ├── usePremium.ts
│   │   ├── useTimer.ts
│   │   └── index.ts
│   ├── services/          # External services
│   │   ├── purchases.ts   # RevenueCat
│   │   ├── analytics.ts   # Mixpanel/Amplitude
│   │   └── notifications.ts
│   ├── store/             # Zustand stores
│   │   └── useAppStore.ts
│   ├── constants/         # App constants
│   │   ├── Colors.ts
│   │   ├── Layout.ts
│   │   └── index.ts
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   └── utils/             # Utility functions
│       └── index.ts
├── assets/                # Static assets
│   ├── images/
│   ├── fonts/
│   └── icon.png
├── app.json               # Expo config
├── eas.json               # EAS Build config
├── package.json
└── tsconfig.json
```

### Essential Dependencies

```bash
# Navigation (already included with expo-router)
npm install expo-router expo-linking expo-constants

# UI & UX
npm install react-native-reanimated react-native-gesture-handler
npm install expo-haptics expo-status-bar

# Storage
npm install @react-native-async-storage/async-storage zustand

# Monetization
npm install react-native-purchases

# Notifications
npm install expo-notifications expo-device

# Analytics (pick one)
npm install @segment/analytics-react-native
# or
npm install @amplitude/analytics-react-native
# or
npm install mixpanel-react-native
```

### app.json Configuration

```json
{
  "expo": {
    "name": "PrayerLock",
    "slug": "prayerlock",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#1E3A5F"
    },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.printmaxx.prayerlock",
      "buildNumber": "1",
      "infoPlist": {
        "NSHealthShareUsageDescription": "PrayerLock uses health data to track your steps.",
        "NSMotionUsageDescription": "PrayerLock uses motion data to count your steps."
      }
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#1E3A5F"
      },
      "package": "com.printmaxx.prayerlock",
      "versionCode": 1,
      "permissions": [
        "ACTIVITY_RECOGNITION",
        "RECEIVE_BOOT_COMPLETED",
        "VIBRATE"
      ]
    },
    "web": {
      "bundler": "metro",
      "output": "static",
      "favicon": "./assets/favicon.png"
    },
    "plugins": [
      "expo-router",
      "expo-notifications",
      [
        "expo-build-properties",
        {
          "ios": {
            "useFrameworks": "static"
          }
        }
      ]
    ],
    "experiments": {
      "typedRoutes": true
    },
    "scheme": "prayerlock"
  }
}
```

---

## 2. Expo Router Navigation

### Root Layout (app/_layout.tsx)

```typescript
import { Stack } from 'expo-router';
import { useEffect } from 'react';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { initializePurchases } from '@/src/services/purchases';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [fontsLoaded] = useFonts({
    'Inter-Regular': require('../assets/fonts/Inter-Regular.ttf'),
    'Inter-Bold': require('../assets/fonts/Inter-Bold.ttf'),
  });

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  useEffect(() => {
    initializePurchases();
  }, []);

  if (!fontsLoaded) return null;

  return (
    <>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="onboarding" />
        <Stack.Screen
          name="paywall"
          options={{
            presentation: 'modal',
            animation: 'slide_from_bottom'
          }}
        />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
```

### Tab Navigator (app/(tabs)/_layout.tsx)

```typescript
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/src/constants';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors.primary,
        tabBarInactiveTintColor: Colors.textSecondary,
        headerShown: false,
        tabBarStyle: {
          backgroundColor: Colors.background,
          borderTopWidth: 0,
          elevation: 0,
          height: 80,
          paddingBottom: 20,
          paddingTop: 10,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="progress"
        options={{
          title: 'Progress',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="stats-chart" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="settings" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
```

### Navigation Patterns

```typescript
import { useRouter, useLocalSearchParams, Link } from 'expo-router';

// Programmatic navigation
const router = useRouter();
router.push('/paywall');
router.replace('/onboarding');
router.back();

// With params
router.push({
  pathname: '/details/[id]',
  params: { id: '123' }
});

// Read params
const { id } = useLocalSearchParams<{ id: string }>();

// Declarative navigation
<Link href="/settings">
  <Text>Go to Settings</Text>
</Link>
```

---

## 3. State Management with Zustand

### Create Store (src/store/useAppStore.ts)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AppState {
  // User settings
  isPremium: boolean;
  hasCompletedOnboarding: boolean;

  // App data
  streakCount: number;
  lastCompletedDate: string | null;

  // Actions
  setIsPremium: (value: boolean) => void;
  completeOnboarding: () => void;
  incrementStreak: () => void;
  resetStreak: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial state
      isPremium: false,
      hasCompletedOnboarding: false,
      streakCount: 0,
      lastCompletedDate: null,

      // Actions
      setIsPremium: (value) => set({ isPremium: value }),

      completeOnboarding: () => set({ hasCompletedOnboarding: true }),

      incrementStreak: () => {
        const today = new Date().toISOString().split('T')[0];
        const lastDate = get().lastCompletedDate;

        if (lastDate === today) return; // Already completed today

        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const yesterdayStr = yesterday.toISOString().split('T')[0];

        if (lastDate === yesterdayStr) {
          // Consecutive day
          set((state) => ({
            streakCount: state.streakCount + 1,
            lastCompletedDate: today,
          }));
        } else {
          // Streak broken, start new
          set({ streakCount: 1, lastCompletedDate: today });
        }
      },

      resetStreak: () => set({ streakCount: 0, lastCompletedDate: null }),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### Using Store in Components

```typescript
import { useAppStore } from '@/src/store/useAppStore';

export function HomeScreen() {
  // Select specific values (better for performance)
  const streakCount = useAppStore((state) => state.streakCount);
  const incrementStreak = useAppStore((state) => state.incrementStreak);

  // Or destructure multiple
  const { isPremium, setIsPremium } = useAppStore();

  return (
    <View>
      <Text>Streak: {streakCount} days</Text>
      <Button title="Complete" onPress={incrementStreak} />
    </View>
  );
}
```

---

## 4. Native Features for PRINTMAXX Apps

### Notifications (PrayerLock)

```typescript
// src/services/notifications.ts
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';

// Configure notification handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export async function registerForPushNotifications(): Promise<string | null> {
  if (!Device.isDevice) {
    console.log('Physical device required for push notifications');
    return null;
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    console.log('Failed to get push token for push notification');
    return null;
  }

  const token = (await Notifications.getExpoPushTokenAsync()).data;

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#1E3A5F',
    });
  }

  return token;
}

export async function scheduleDailyReminder(
  hour: number,
  minute: number,
  title: string,
  body: string
): Promise<string> {
  // Cancel existing daily reminder
  await Notifications.cancelAllScheduledNotificationsAsync();

  const identifier = await Notifications.scheduleNotificationAsync({
    content: {
      title,
      body,
      sound: true,
      priority: Notifications.AndroidNotificationPriority.HIGH,
    },
    trigger: {
      hour,
      minute,
      repeats: true,
    },
  });

  return identifier;
}

export async function cancelAllNotifications(): Promise<void> {
  await Notifications.cancelAllScheduledNotificationsAsync();
}

// Usage example for PrayerLock
export async function schedulePrayerReminders(settings: {
  morningTime: { hour: number; minute: number };
  eveningTime?: { hour: number; minute: number };
}): Promise<void> {
  await cancelAllNotifications();

  // Morning prayer reminder
  await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Morning Prayer Time',
      body: 'Start your day with intention. Your prayer session awaits.',
      sound: true,
    },
    trigger: {
      hour: settings.morningTime.hour,
      minute: settings.morningTime.minute,
      repeats: true,
    },
  });

  // Evening prayer reminder (optional)
  if (settings.eveningTime) {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Evening Reflection',
        body: 'Take a moment to reflect on your day.',
        sound: true,
      },
      trigger: {
        hour: settings.eveningTime.hour,
        minute: settings.eveningTime.minute,
        repeats: true,
      },
    });
  }
}
```

### Health Data Integration (WalkToUnlock/StepUnlock)

**Note:** Expo does not have a built-in health module. You need `react-native-health` for iOS or `react-native-google-fit` for Android, which require native code.

**Option 1: Use expo-sensors for basic step counting (limited)**

```typescript
// src/services/pedometer.ts
import { Pedometer } from 'expo-sensors';

export async function checkPedometerPermission(): Promise<boolean> {
  const { status } = await Pedometer.requestPermissionsAsync();
  return status === 'granted';
}

export async function getStepCount(startDate: Date, endDate: Date): Promise<number> {
  const hasPermission = await checkPedometerPermission();
  if (!hasPermission) return 0;

  try {
    const result = await Pedometer.getStepCountAsync(startDate, endDate);
    return result.steps;
  } catch (error) {
    console.error('Error getting step count:', error);
    return 0;
  }
}

export function subscribeToSteps(callback: (steps: number) => void): () => void {
  const subscription = Pedometer.watchStepCount((result) => {
    callback(result.steps);
  });

  return () => subscription.remove();
}

// Usage in component
import { useEffect, useState } from 'react';
import { getStepCount, subscribeToSteps } from '@/src/services/pedometer';

export function useStepCounter() {
  const [steps, setSteps] = useState(0);
  const [todaySteps, setTodaySteps] = useState(0);

  useEffect(() => {
    // Get today's steps
    const start = new Date();
    start.setHours(0, 0, 0, 0);
    const end = new Date();

    getStepCount(start, end).then(setTodaySteps);

    // Subscribe to live updates
    const unsubscribe = subscribeToSteps((newSteps) => {
      setSteps((prev) => prev + newSteps);
    });

    return unsubscribe;
  }, []);

  return { steps, todaySteps: todaySteps + steps };
}
```

**Option 2: Full HealthKit/Google Fit integration (requires development build)**

```bash
# Install health packages
npm install react-native-health  # iOS only
npm install react-native-google-fit  # Android only

# Create development build (required for native modules)
npx expo prebuild
npx expo run:ios
```

```typescript
// src/services/health.ts
import { Platform } from 'react-native';

// Conditional imports based on platform
let AppleHealthKit: any;
let GoogleFit: any;

if (Platform.OS === 'ios') {
  AppleHealthKit = require('react-native-health').default;
} else {
  GoogleFit = require('react-native-google-fit').default;
}

// iOS HealthKit
export async function initHealthKit(): Promise<boolean> {
  if (Platform.OS !== 'ios') return false;

  return new Promise((resolve) => {
    const permissions = {
      permissions: {
        read: [AppleHealthKit.Constants.Permissions.StepCount],
        write: [],
      },
    };

    AppleHealthKit.initHealthKit(permissions, (error: any) => {
      if (error) {
        console.error('HealthKit init error:', error);
        resolve(false);
      } else {
        resolve(true);
      }
    });
  });
}

export async function getTodayStepsIOS(): Promise<number> {
  return new Promise((resolve) => {
    const options = {
      date: new Date().toISOString(),
      includeManuallyAdded: false,
    };

    AppleHealthKit.getStepCount(options, (error: any, results: any) => {
      if (error) {
        console.error('Error getting steps:', error);
        resolve(0);
      } else {
        resolve(results.value || 0);
      }
    });
  });
}

// Android Google Fit
export async function initGoogleFit(): Promise<boolean> {
  if (Platform.OS !== 'android') return false;

  try {
    const options = {
      scopes: [
        GoogleFit.Scopes.FITNESS_ACTIVITY_READ,
        GoogleFit.Scopes.FITNESS_BODY_READ,
      ],
    };

    const authResult = await GoogleFit.authorize(options);
    return authResult.success;
  } catch (error) {
    console.error('Google Fit init error:', error);
    return false;
  }
}

export async function getTodayStepsAndroid(): Promise<number> {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const options = {
    startDate: today.toISOString(),
    endDate: new Date().toISOString(),
  };

  try {
    const result = await GoogleFit.getDailyStepCountSamples(options);
    const steps = result.find((source: any) =>
      source.source === 'com.google.android.gms:estimated_steps'
    );
    return steps?.steps?.[0]?.value || 0;
  } catch (error) {
    console.error('Error getting steps:', error);
    return 0;
  }
}

// Unified interface
export async function initHealthServices(): Promise<boolean> {
  if (Platform.OS === 'ios') {
    return initHealthKit();
  } else {
    return initGoogleFit();
  }
}

export async function getTodaySteps(): Promise<number> {
  if (Platform.OS === 'ios') {
    return getTodayStepsIOS();
  } else {
    return getTodayStepsAndroid();
  }
}
```

### Screen Time / App Blocking (StudyLock)

**Important:** iOS and Android heavily restrict apps from blocking other apps. True app blocking is only possible with MDM (Mobile Device Management) or Screen Time API (iOS only, requires special entitlement from Apple).

**Workaround strategies:**

1. **Focus Mode Integration (iOS 16+)**

```typescript
// This requires iOS native development
// No Expo equivalent exists
// Would need to use expo-dev-client with custom native module
```

2. **Notification-based reminders**

```typescript
// src/services/focusReminder.ts
import * as Notifications from 'expo-notifications';
import { AppState, AppStateStatus } from 'react-native';

let focusStartTime: Date | null = null;
let targetMinutes: number = 0;
let checkInterval: NodeJS.Timeout | null = null;

export function startFocusSession(minutes: number): void {
  focusStartTime = new Date();
  targetMinutes = minutes;

  // Schedule completion notification
  Notifications.scheduleNotificationAsync({
    content: {
      title: 'Focus Session Complete!',
      body: `Great job! You focused for ${minutes} minutes.`,
      sound: true,
    },
    trigger: {
      seconds: minutes * 60,
    },
  });

  // Check if user leaves app
  const subscription = AppState.addEventListener('change', handleAppStateChange);

  // Store subscription for cleanup
  checkInterval = setInterval(() => {
    // Could add periodic checks here
  }, 1000);
}

function handleAppStateChange(state: AppStateStatus): void {
  if (state === 'background' && focusStartTime) {
    // User left the app during focus session
    Notifications.scheduleNotificationAsync({
      content: {
        title: 'Stay Focused!',
        body: 'Come back to complete your session.',
        sound: true,
      },
      trigger: null, // Immediate
    });
  }
}

export function endFocusSession(): { completed: boolean; minutesFocused: number } {
  if (!focusStartTime) {
    return { completed: false, minutesFocused: 0 };
  }

  const now = new Date();
  const minutesFocused = Math.floor((now.getTime() - focusStartTime.getTime()) / 60000);
  const completed = minutesFocused >= targetMinutes;

  // Cleanup
  focusStartTime = null;
  if (checkInterval) {
    clearInterval(checkInterval);
    checkInterval = null;
  }

  // Cancel scheduled notifications
  Notifications.cancelAllScheduledNotificationsAsync();

  return { completed, minutesFocused };
}
```

3. **Background task approach**

```typescript
// src/services/backgroundFocus.ts
import * as TaskManager from 'expo-task-manager';
import * as BackgroundFetch from 'expo-background-fetch';

const FOCUS_TASK = 'FOCUS_CHECK_TASK';

TaskManager.defineTask(FOCUS_TASK, async () => {
  // This runs periodically in background
  // Can check if focus session is active and send reminders
  console.log('Background focus check');
  return BackgroundFetch.BackgroundFetchResult.NewData;
});

export async function registerFocusBackgroundTask(): Promise<void> {
  await BackgroundFetch.registerTaskAsync(FOCUS_TASK, {
    minimumInterval: 60, // 1 minute minimum
    stopOnTerminate: false,
    startOnBoot: true,
  });
}
```

---

## 5. EAS Build & Deployment

### Setup EAS

```bash
# Install EAS CLI globally
npm install -g eas-cli

# Login to Expo account
eas login

# Initialize EAS in project
eas build:configure
```

### eas.json Configuration

```json
{
  "cli": {
    "version": ">= 12.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "buildConfiguration": "Release"
      },
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "ios": {
        "buildConfiguration": "Release",
        "credentialsSource": "remote"
      },
      "android": {
        "buildType": "app-bundle"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "XXXXXXXXXX"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "production"
      }
    }
  }
}
```

### Build Commands

```bash
# Development build (for expo-dev-client)
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview build (internal testing)
eas build --profile preview --platform all

# Production build
eas build --profile production --platform ios
eas build --profile production --platform android
```

### Submit to Stores

```bash
# Submit iOS to App Store
eas submit --platform ios

# Submit Android to Google Play
eas submit --platform android

# Build and submit in one command
eas build --platform ios --auto-submit
```

### OTA Updates with EAS Update

```bash
# Setup EAS Update
eas update:configure

# Publish update (JavaScript-only changes)
eas update --branch production --message "Bug fix"

# Preview update before publishing
eas update --branch preview --message "Testing new feature"
```

**app.json additions for updates:**

```json
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/your-project-id"
    },
    "runtimeVersion": {
      "policy": "appVersion"
    }
  }
}
```

---

## 6. App Store Submission Checklist

### iOS (App Store Connect)

**Before submission:**
- [ ] App icon (1024x1024, no alpha)
- [ ] Screenshots for all required device sizes
  - 6.7" (iPhone 15 Pro Max): 1290 x 2796
  - 6.5" (iPhone 14 Plus): 1284 x 2778
  - 5.5" (iPhone 8 Plus): 1242 x 2208
  - 12.9" iPad Pro (if applicable): 2048 x 2732
- [ ] App preview video (optional, 15-30 seconds)
- [ ] App description (4000 chars max)
- [ ] Keywords (100 chars max)
- [ ] Support URL
- [ ] Privacy policy URL
- [ ] Copyright info
- [ ] Age rating configured
- [ ] Privacy nutrition labels completed
- [ ] In-app purchases configured (if applicable)

**App Store Review Guidelines to check:**
- [ ] 4.2: No placeholder content
- [ ] 4.3: No spam/clones of existing apps
- [ ] 3.1.1: In-app purchases use Apple IAP (not external payment)
- [ ] 5.1.1: Privacy policy accessible and complete
- [ ] 2.3.3: Screenshots reflect actual app experience

### Android (Google Play Console)

**Before submission:**
- [ ] App icon (512x512)
- [ ] Feature graphic (1024x500)
- [ ] Screenshots (min 2, up to 8 per device type)
  - Phone: 1080 x 1920 or similar
  - Tablet (if applicable)
- [ ] Short description (80 chars)
- [ ] Full description (4000 chars)
- [ ] Application type and category
- [ ] Content rating questionnaire completed
- [ ] Data safety form completed
- [ ] Target audience and content settings
- [ ] App signing configured

**Google Play policies to check:**
- [ ] Payments policy (use Google Play Billing for digital goods)
- [ ] User data policy (privacy policy required)
- [ ] Deceptive behavior policy (accurate descriptions)
- [ ] No malware or prohibited content

---

## 7. Performance Optimization

### Bundle Size

```bash
# Analyze bundle size
npx expo export --platform ios
npx source-map-explorer dist/bundles/ios-*.js

# Or use @expo/bundle-analyzer
npx expo customize metro.config.js
# Add bundle analyzer plugin
```

### Reduce Bundle Size

1. **Tree shaking**
```typescript
// BAD - imports entire library
import _ from 'lodash';

// GOOD - imports only what you need
import debounce from 'lodash/debounce';
```

2. **Lazy loading screens**
```typescript
import { lazy, Suspense } from 'react';

const HeavyScreen = lazy(() => import('./HeavyScreen'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyScreen />
    </Suspense>
  );
}
```

3. **Optimize images**
```typescript
// Use WebP format
// Resize images to actual display size
// Use expo-image for better caching

import { Image } from 'expo-image';

<Image
  source={{ uri: 'https://example.com/image.webp' }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  placeholder={blurhash}
  transition={200}
/>
```

### Animation Performance

```typescript
// Use react-native-reanimated for smooth 60fps animations
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
} from 'react-native-reanimated';

function AnimatedComponent() {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePress = () => {
    scale.value = withSpring(1.2);
  };

  return (
    <Animated.View style={animatedStyle}>
      <Pressable onPress={handlePress}>
        <Text>Press me</Text>
      </Pressable>
    </Animated.View>
  );
}
```

### List Performance

```typescript
import { FlashList } from '@shopify/flash-list';

// Use FlashList instead of FlatList for better performance
<FlashList
  data={items}
  renderItem={({ item }) => <ItemComponent item={item} />}
  estimatedItemSize={100}
  keyExtractor={(item) => item.id}
/>
```

### Memory Management

```typescript
// Clean up listeners and subscriptions
useEffect(() => {
  const subscription = someAPI.subscribe(handler);

  return () => {
    subscription.unsubscribe();
  };
}, []);

// Avoid storing large objects in state
// Use refs for values that don't need re-renders
const largeDataRef = useRef(null);
```

---

## 8. Testing

### Development Testing

```bash
# Start development server
npx expo start

# Run on iOS simulator
npx expo start --ios

# Run on Android emulator
npx expo start --android

# Run on physical device (scan QR code with Expo Go)
npx expo start
```

### Unit Testing with Jest

```bash
# Install testing dependencies
npm install --save-dev jest @testing-library/react-native jest-expo
```

```json
// package.json
{
  "scripts": {
    "test": "jest"
  },
  "jest": {
    "preset": "jest-expo",
    "transformIgnorePatterns": [
      "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)"
    ]
  }
}
```

```typescript
// __tests__/components/Button.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '@/src/components/Button';

describe('Button', () => {
  it('renders correctly', () => {
    const { getByText } = render(<Button title="Press me" onPress={() => {}} />);
    expect(getByText('Press me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(<Button title="Press me" onPress={onPressMock} />);

    fireEvent.press(getByText('Press me'));

    expect(onPressMock).toHaveBeenCalledTimes(1);
  });
});
```

### E2E Testing with Detox

```bash
# Install Detox
npm install --save-dev detox @types/detox

# Initialize Detox
npx detox init
```

---

## 9. Common Patterns for PRINTMAXX Apps

### Premium Feature Gating

```typescript
// src/components/PremiumGate.tsx
import { useRouter } from 'expo-router';
import { useAppStore } from '@/src/store/useAppStore';

interface PremiumGateProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function PremiumGate({ children, fallback }: PremiumGateProps) {
  const isPremium = useAppStore((state) => state.isPremium);
  const router = useRouter();

  if (!isPremium) {
    return (
      fallback || (
        <TouchableOpacity
          style={styles.lockedContainer}
          onPress={() => router.push('/paywall')}
        >
          <Ionicons name="lock-closed" size={24} color={Colors.textSecondary} />
          <Text style={styles.lockedText}>Unlock with Premium</Text>
        </TouchableOpacity>
      )
    );
  }

  return <>{children}</>;
}
```

### Onboarding Flow

```typescript
// app/onboarding.tsx
import { useState } from 'react';
import { useRouter } from 'expo-router';
import { useAppStore } from '@/src/store/useAppStore';

const ONBOARDING_STEPS = [
  {
    title: 'Welcome to PrayerLock',
    description: 'Start your day with intention',
    image: require('@/assets/onboarding/step1.png'),
  },
  {
    title: 'Set Your Prayer Time',
    description: 'Choose when to be reminded',
    image: require('@/assets/onboarding/step2.png'),
  },
  {
    title: 'Build Your Streak',
    description: 'Track your progress over time',
    image: require('@/assets/onboarding/step3.png'),
  },
];

export default function OnboardingScreen() {
  const [step, setStep] = useState(0);
  const router = useRouter();
  const completeOnboarding = useAppStore((state) => state.completeOnboarding);

  const handleNext = () => {
    if (step < ONBOARDING_STEPS.length - 1) {
      setStep(step + 1);
    } else {
      completeOnboarding();
      router.replace('/paywall'); // Show paywall after onboarding
    }
  };

  const currentStep = ONBOARDING_STEPS[step];

  return (
    <SafeAreaView style={styles.container}>
      <Image source={currentStep.image} style={styles.image} />
      <Text style={styles.title}>{currentStep.title}</Text>
      <Text style={styles.description}>{currentStep.description}</Text>

      <View style={styles.pagination}>
        {ONBOARDING_STEPS.map((_, index) => (
          <View
            key={index}
            style={[styles.dot, index === step && styles.activeDot]}
          />
        ))}
      </View>

      <Button
        title={step === ONBOARDING_STEPS.length - 1 ? 'Get Started' : 'Next'}
        onPress={handleNext}
      />
    </SafeAreaView>
  );
}
```

### Timer Component (for PrayerLock)

```typescript
// src/hooks/useTimer.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import * as Haptics from 'expo-haptics';

interface UseTimerOptions {
  initialSeconds: number;
  onComplete?: () => void;
  onTick?: (remaining: number) => void;
}

export function useTimer({ initialSeconds, onComplete, onTick }: UseTimerOptions) {
  const [seconds, setSeconds] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const start = useCallback(() => {
    setIsRunning(true);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  }, []);

  const pause = useCallback(() => {
    setIsRunning(false);
  }, []);

  const reset = useCallback(() => {
    setSeconds(initialSeconds);
    setIsRunning(false);
    setIsComplete(false);
  }, [initialSeconds]);

  useEffect(() => {
    if (isRunning && seconds > 0) {
      intervalRef.current = setInterval(() => {
        setSeconds((prev) => {
          const newValue = prev - 1;
          onTick?.(newValue);

          if (newValue === 0) {
            setIsRunning(false);
            setIsComplete(true);
            Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
            onComplete?.();
          }

          return newValue;
        });
      }, 1000);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning, seconds, onComplete, onTick]);

  const progress = 1 - seconds / initialSeconds;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  const display = `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;

  return {
    seconds,
    display,
    progress,
    isRunning,
    isComplete,
    start,
    pause,
    reset,
  };
}
```

---

## 10. Debugging Tips

### Common Issues

**"Unable to resolve module"**
```bash
# Clear Metro cache
npx expo start --clear

# Reset node_modules
rm -rf node_modules && npm install
```

**"Invariant Violation: Native module cannot be null"**
```bash
# Rebuild native modules
npx expo prebuild --clean
npx expo run:ios
```

**iOS Simulator issues**
```bash
# Reset simulator
Device > Erase All Content and Settings

# Or via command line
xcrun simctl erase all
```

**Android Emulator issues**
```bash
# Cold boot emulator
# In Android Studio: AVD Manager > Your Device > Cold Boot Now

# Clear app data
adb shell pm clear com.your.app.package
```

### Debugging Tools

```typescript
// Enable Flipper debugging
// flipper-plugin-react-native is built into Expo

// Use React DevTools
// Press 'j' in terminal to open debugger

// Network debugging
// Use React Native Debugger or Flipper

// Console logging (appears in terminal)
console.log('Debug:', variable);

// Native logs
// iOS: Xcode > Debug Area
// Android: Android Studio > Logcat
```

---

## 11. Quick Reference

### Expo CLI Commands

| Command | Description |
|---------|-------------|
| `npx expo start` | Start development server |
| `npx expo start --ios` | Start and open iOS simulator |
| `npx expo start --android` | Start and open Android emulator |
| `npx expo start --clear` | Start with cache cleared |
| `npx expo prebuild` | Generate native projects |
| `npx expo run:ios` | Build and run iOS locally |
| `npx expo run:android` | Build and run Android locally |
| `npx expo install package` | Install with compatible version |

### EAS CLI Commands

| Command | Description |
|---------|-------------|
| `eas build -p ios` | Build for iOS |
| `eas build -p android` | Build for Android |
| `eas submit -p ios` | Submit to App Store |
| `eas submit -p android` | Submit to Play Store |
| `eas update` | Push OTA update |
| `eas credentials` | Manage certificates/keys |

### Useful Expo Packages

| Package | Purpose |
|---------|---------|
| `expo-router` | File-based routing |
| `expo-notifications` | Push notifications |
| `expo-haptics` | Haptic feedback |
| `expo-device` | Device info |
| `expo-constants` | App constants |
| `expo-linking` | Deep linking |
| `expo-secure-store` | Secure storage |
| `expo-updates` | OTA updates |
| `expo-sensors` | Pedometer, gyroscope |
| `expo-image` | Optimized images |

---

## 12. PRINTMAXX App-Specific Requirements

### PrayerLock

**Required packages:**
- `expo-notifications` - Prayer reminders
- `expo-haptics` - Feedback during prayer
- `@react-native-async-storage/async-storage` - Streak persistence
- `react-native-purchases` - Subscriptions

**Key features to implement:**
- Morning notification scheduling
- Timer with haptic feedback
- Streak tracking with calendar view
- Daily verse display
- RevenueCat subscription

### WalkToUnlock/StepUnlock

**Required packages:**
- `expo-sensors` (Pedometer) - Basic step counting
- OR `react-native-health` + `react-native-google-fit` - Full health integration
- `expo-notifications` - Goal reminders
- `react-native-purchases` - Subscriptions

**Key features to implement:**
- Step goal setting
- Real-time step tracking
- Progress animations
- Daily/weekly statistics
- Health permission handling

### StudyLock

**Required packages:**
- `expo-notifications` - Focus reminders
- `expo-haptics` - Session feedback
- `expo-task-manager` - Background checks
- `react-native-purchases` - Subscriptions

**Key features to implement:**
- Focus timer with customizable durations
- App exit detection (AppState)
- Session statistics
- Pomodoro technique support
- Distraction logging

---

## Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Router Documentation](https://expo.github.io/router/docs/)
- [EAS Build Documentation](https://docs.expo.dev/build/introduction/)
- [RevenueCat React Native](https://docs.revenuecat.com/docs/reactnative)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Google Play Policy Center](https://support.google.com/googleplay/android-developer/answer/9876714)

---

Created: 2026-01-25
