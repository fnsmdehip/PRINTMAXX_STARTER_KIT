# Monitoring Setup Guide

Production crash reporting and performance monitoring setup for React Native apps.

## Provider Comparison

| Feature | Sentry | Firebase Crashlytics | Bugsnag |
|---------|--------|---------------------|---------|
| **Pricing** | Free tier: 5K errors/mo | Free (unlimited) | Free tier: 7.5K events/mo |
| **Native crash support** | Yes | Yes | Yes |
| **JS error support** | Yes | Partial | Yes |
| **Performance monitoring** | Yes | Firebase Performance | Basic |
| **Breadcrumbs** | Yes | Manual logging | Yes |
| **User context** | Yes | Limited | Yes |
| **Release tracking** | Yes | Yes | Yes |
| **Source maps** | Yes | Limited | Yes |
| **Integrations** | Slack, Jira, PagerDuty | Firebase ecosystem | Slack, Jira, PagerDuty |
| **React Native support** | Excellent | Good | Good |
| **Expo support** | Excellent | Requires dev client | Good |

## Recommendation

- **Sentry**: Best all-around choice. Strong JS support, excellent source maps, good integrations.
- **Crashlytics**: Use if already in Firebase ecosystem. Free unlimited events. Native crash focus.
- **Bugsnag**: Good middle ground. Feature flag integration. Good for larger teams.

For most React Native apps: **Start with Sentry**.

---

## Sentry Setup

### 1. Install dependencies

```bash
npx expo install @sentry/react-native
```

### 2. Configure in app entry

```typescript
// App.tsx or _layout.tsx
import { sentryProvider } from '@/shared/monitoring/providers/sentry_setup';
import { crashReportingService } from '@/shared/monitoring';

// Initialize at app startup
async function initializeCrashReporting() {
  await crashReportingService.initialize(
    {
      dsn: process.env.EXPO_PUBLIC_SENTRY_DSN!,
      environment: __DEV__ ? 'development' : 'production',
      release: `${APP_NAME}@${APP_VERSION}+${BUILD_NUMBER}`,
      debug: __DEV__,
      tracesSampleRate: 0.2,
    },
    [sentryProvider]
  );
}

// Call in useEffect or before rendering
initializeCrashReporting();
```

### 3. Configure source maps (EAS Build)

```json
// eas.json
{
  "build": {
    "production": {
      "env": {
        "SENTRY_AUTH_TOKEN": "@sentry_auth_token"
      }
    }
  }
}
```

```javascript
// app.config.js
export default {
  plugins: [
    [
      "@sentry/react-native/expo",
      {
        organization: "your-org",
        project: "your-project",
        url: "https://sentry.io/"
      }
    ]
  ]
};
```

### 4. Set environment variables

```bash
# .env
EXPO_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/123

# eas.json secret (for source maps)
eas secret:create --scope project --name sentry_auth_token --value "your-auth-token"
```

### 5. Configure alerts in Sentry

1. Go to Project Settings > Alerts
2. Create "New Alert Rule"
3. Recommended alerts:
   - Error rate > 1% of sessions
   - New issue detected (first seen)
   - Issue regression (fixed issue recurs)
   - High-volume issue (>100 events/hr)

---

## Firebase Crashlytics Setup

### 1. Install dependencies

```bash
npx expo install @react-native-firebase/app @react-native-firebase/crashlytics
```

### 2. Configure Firebase

Download and add config files:
- iOS: `GoogleService-Info.plist` in ios/
- Android: `google-services.json` in android/app/

### 3. Initialize in app

```typescript
// App.tsx
import { crashlyticsProvider } from '@/shared/monitoring/providers/crashlytics_setup';
import { crashReportingService } from '@/shared/monitoring';

async function initializeCrashReporting() {
  await crashReportingService.initialize(
    {
      environment: __DEV__ ? 'development' : 'production',
      release: `${APP_VERSION}`,
      enabled: !__DEV__, // Disable in dev
    },
    [crashlyticsProvider]
  );
}
```

### 4. Configure native builds

```ruby
# ios/Podfile
pod 'Firebase/Crashlytics'
```

```gradle
// android/build.gradle
buildscript {
  dependencies {
    classpath 'com.google.firebase:firebase-crashlytics-gradle:2.9.9'
  }
}

// android/app/build.gradle
apply plugin: 'com.google.firebase.crashlytics'
```

### 5. Upload dSYMs (iOS)

```bash
# Run after archive build
./Pods/FirebaseCrashlytics/upload-symbols -gsp ios/GoogleService-Info.plist -p ios path/to/dSYMs
```

### 6. Configure alerts in Firebase Console

1. Go to Crashlytics > Settings
2. Enable crash-free users alert
3. Set up Slack/email notifications

---

## Bugsnag Setup

### 1. Install dependencies

```bash
npx expo install @bugsnag/react-native
```

### 2. Initialize

```typescript
// App.tsx
import { bugsnagProvider } from '@/shared/monitoring/providers/bugsnag_setup';
import { crashReportingService } from '@/shared/monitoring';

async function initializeCrashReporting() {
  await crashReportingService.initialize(
    {
      apiKey: process.env.EXPO_PUBLIC_BUGSNAG_API_KEY!,
      environment: __DEV__ ? 'development' : 'production',
      release: APP_VERSION,
    },
    [bugsnagProvider]
  );
}
```

### 3. Configure source maps

```bash
# Install CLI
npm install -g @bugsnag/source-maps

# Upload after build
bugsnag-source-maps upload-react-native \
  --api-key YOUR_API_KEY \
  --app-version 1.0.0 \
  --platform ios \
  --source-map path/to/main.jsbundle.map \
  --bundle path/to/main.jsbundle
```

### 4. Configure alerts

1. Go to Project Settings > Collaborators & notifications
2. Set up Slack integration
3. Configure alert rules for:
   - New errors
   - Error spikes
   - Stability score drops

---

## Source Maps Configuration

Source maps are critical for debugging minified/bundled JS errors.

### Expo/EAS Build

Source maps are handled automatically with the Sentry Expo plugin.

### Manual Metro builds

```javascript
// metro.config.js
module.exports = {
  transformer: {
    minifierPath: 'metro-minify-terser',
    minifierConfig: {
      sourceMap: {
        includeSources: true,
      },
    },
  },
};
```

### Upload source maps

```bash
# Sentry
sentry-cli releases files VERSION upload-sourcemaps ./dist --rewrite

# Bugsnag
bugsnag-source-maps upload-react-native \
  --api-key KEY \
  --app-version VERSION \
  --source-map ./dist/main.jsbundle.map

# Crashlytics (limited support)
# Use Firebase Performance for JS-level tracing
```

---

## Dashboard Setup

### Sentry Dashboard

Key views to create:

1. **Error Overview**
   - Group by: error type
   - Filter: unresolved
   - Sort: frequency

2. **User Impact**
   - Filter: users affected > 1
   - Group by: release

3. **Performance**
   - Transaction: app.start
   - Metric: LCP, FCP

### Crashlytics Dashboard

Key metrics:

1. Crash-free users %
2. Crash-free sessions %
3. Trends by version
4. Top issues by users affected

### Bugsnag Dashboard

Create views for:

1. Unresolved errors
2. Errors by release stage
3. Errors by user segments

---

## Testing Crash Reporting

### Test crash (development)

```typescript
// In a test component
import { crashReportingService } from '@/shared/monitoring';

function TestCrash() {
  return (
    <Button
      title="Test Error"
      onPress={() => {
        crashReportingService.captureException(
          new Error('Test error from development'),
          { tags: { test: 'true' } }
        );
      }}
    />
  );
}
```

### Test native crash (Crashlytics)

```typescript
import { crashlyticsProvider } from '@/shared/monitoring/providers/crashlytics_setup';

// WARNING: This will crash the app
crashlyticsProvider.testCrash();
```

### Verify in dashboard

1. Trigger test error
2. Wait 1-2 minutes
3. Check dashboard for event
4. Verify stack trace is readable (source maps working)

---

## Checklist

Before shipping to production:

- [ ] Crash reporting SDK initialized
- [ ] DSN/API key set via environment variable (not hardcoded)
- [ ] Source maps uploading in CI/CD
- [ ] User context being set after auth
- [ ] Test error captured and visible in dashboard
- [ ] Stack traces are readable (not minified)
- [ ] Alerts configured for critical errors
- [ ] Team members added to project
- [ ] Error triage workflow documented

---

## Troubleshooting

### Events not appearing

1. Check DSN/API key is correct
2. Verify `enabled: true` in config
3. Check network connectivity
4. In dev, check if events are filtered out

### Source maps not working

1. Verify source maps are uploaded with correct version
2. Check release name matches exactly
3. Ensure source maps include original source
4. For Expo, check Sentry plugin is in app.config.js

### High event volume

1. Implement sampling: `sampleRate: 0.1` (10%)
2. Filter out known/expected errors in `beforeSend`
3. Group similar errors using fingerprints
4. Set up rate limits in dashboard

### Duplicate events

1. Check multiple SDKs aren't initialized
2. Verify error boundary isn't re-throwing
3. Check global error handler configuration
