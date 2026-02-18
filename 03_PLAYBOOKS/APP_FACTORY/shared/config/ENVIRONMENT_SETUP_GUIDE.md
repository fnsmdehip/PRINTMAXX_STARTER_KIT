# Environment setup guide

Complete guide for managing environment variables, secrets, and build configurations across all APP_FACTORY apps.

---

## Environment variable management

### Local development

Create a `.env` file in your app root (never commit this file):

```bash
# .env.development (local development)
APP_ENV=development
DEV_API_URL=http://localhost:3000/api

# RevenueCat (sandbox)
REVENUECAT_IOS_KEY=appl_sandbox_xxxx
REVENUECAT_ANDROID_KEY=goog_sandbox_xxxx

# Analytics (disabled in dev, but configured)
MIXPANEL_TOKEN=your_dev_token
AMPLITUDE_KEY=your_dev_key

# Push notifications
ONESIGNAL_APP_ID=your_onesignal_app_id

# Error tracking
SENTRY_DSN=your_sentry_dsn

# Build info
APP_VERSION=1.0.0
BUILD_NUMBER=1
```

### Staging environment

```bash
# .env.staging
APP_ENV=staging
STAGING_API_URL=https://staging.api.printmaxx.com

REVENUECAT_IOS_KEY=appl_sandbox_xxxx
MIXPANEL_TOKEN=your_staging_token
SENTRY_DSN=your_staging_sentry_dsn
```

### Production environment

```bash
# .env.production
APP_ENV=production
PROD_API_URL=https://api.printmaxx.com

REVENUECAT_IOS_KEY=appl_prod_xxxx
MIXPANEL_TOKEN=your_prod_token
SENTRY_DSN=your_prod_sentry_dsn
```

---

## react-native-config setup

### Installation

```bash
npm install react-native-config
cd ios && pod install
```

### iOS configuration

1. Open Xcode project
2. Add `Config.xcconfig` for each scheme:

```
// ios/Config/Development.xcconfig
#include? "tmp.xcconfig"
APP_ENV = development
BUNDLE_ID_SUFFIX = .dev
```

```
// ios/Config/Staging.xcconfig
#include? "tmp.xcconfig"
APP_ENV = staging
BUNDLE_ID_SUFFIX = .staging
```

```
// ios/Config/Production.xcconfig
#include? "tmp.xcconfig"
APP_ENV = production
BUNDLE_ID_SUFFIX =
```

3. Update `Info.plist`:

```xml
<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)$(BUNDLE_ID_SUFFIX)</string>
```

4. Add Build Phase script:

```bash
# Build Phases > New Run Script Phase
"${SRCROOT}/../node_modules/react-native-config/ios/ReactNativeConfig/BuildXCConfig.rb" "${SRCROOT}/.." "${SRCROOT}/tmp.xcconfig"
```

### Android configuration

1. Add to `android/app/build.gradle`:

```gradle
apply from: project(':react-native-config').projectDir.getPath() + "/dotenv.gradle"

android {
    defaultConfig {
        resValue "string", "build_config_package", "com.yourapp"
    }

    flavorDimensions "environment"
    productFlavors {
        development {
            dimension "environment"
            applicationIdSuffix ".dev"
        }
        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
        }
        production {
            dimension "environment"
        }
    }
}
```

2. Create flavor-specific `.env` files:

```
.env.development
.env.staging
.env.production
```

### Usage in code

```typescript
import Config from 'react-native-config';

const apiUrl = Config.API_URL;
const revenueCatKey = Config.REVENUECAT_IOS_KEY;
```

---

## iOS scheme configuration

### Create schemes

1. In Xcode, click scheme dropdown > Manage Schemes
2. Duplicate the main scheme for each environment
3. Rename: `AppName-Dev`, `AppName-Staging`, `AppName`

### Configure each scheme

**Development scheme:**
- Build Configuration: Debug
- Pre-actions: `echo ".env.development" > /tmp/.envfile`

**Staging scheme:**
- Build Configuration: Release
- Pre-actions: `echo ".env.staging" > /tmp/.envfile`

**Production scheme:**
- Build Configuration: Release
- Pre-actions: `echo ".env.production" > /tmp/.envfile`

### Run with specific scheme

```bash
# Development
npx react-native run-ios --scheme "AppName-Dev"

# Staging
npx react-native run-ios --scheme "AppName-Staging"

# Production
npx react-native run-ios --scheme "AppName"
```

---

## Android build variants

### Build types in build.gradle

```gradle
android {
    buildTypes {
        debug {
            applicationIdSuffix ".debug"
            debuggable true
        }
        staging {
            initWith release
            applicationIdSuffix ".staging"
            matchingFallbacks = ['release']
        }
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### Run with specific variant

```bash
# Development
npx react-native run-android --variant=developmentDebug

# Staging
npx react-native run-android --variant=stagingRelease

# Production
npx react-native run-android --variant=productionRelease
```

---

## Secrets in CI/CD

### GitHub Actions

Store secrets in repository settings > Secrets:

```yaml
# .github/workflows/build.yml
name: Build App

on:
  push:
    branches: [main]

jobs:
  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - name: Create .env file
        run: |
          echo "APP_ENV=production" >> .env.production
          echo "REVENUECAT_IOS_KEY=${{ secrets.REVENUECAT_IOS_KEY }}" >> .env.production
          echo "MIXPANEL_TOKEN=${{ secrets.MIXPANEL_TOKEN }}" >> .env.production
          echo "SENTRY_DSN=${{ secrets.SENTRY_DSN }}" >> .env.production

      - name: Install dependencies
        run: npm ci

      - name: Install CocoaPods
        run: cd ios && pod install

      - name: Build iOS
        run: |
          xcodebuild -workspace ios/App.xcworkspace \
            -scheme "App" \
            -configuration Release \
            -archivePath build/App.xcarchive \
            archive
```

### Fastlane integration

```ruby
# fastlane/Fastfile
platform :ios do
  desc "Build for production"
  lane :build_production do
    # Load environment
    Dotenv.load('.env.production')

    build_app(
      scheme: "AppName",
      configuration: "Release",
      export_options: {
        method: "app-store"
      }
    )
  end
end
```

### EAS Build (Expo)

```json
// eas.json
{
  "build": {
    "development": {
      "env": {
        "APP_ENV": "development"
      }
    },
    "staging": {
      "env": {
        "APP_ENV": "staging"
      }
    },
    "production": {
      "env": {
        "APP_ENV": "production"
      }
    }
  }
}
```

Store secrets in EAS:

```bash
eas secret:create --name REVENUECAT_IOS_KEY --value "appl_xxx" --scope project
eas secret:create --name MIXPANEL_TOKEN --value "xxx" --scope project
```

---

## Required secrets per app

Each app needs these secrets configured:

| Secret | Development | Staging | Production |
|--------|-------------|---------|------------|
| `REVENUECAT_IOS_KEY` | Sandbox key | Sandbox key | Production key |
| `REVENUECAT_ANDROID_KEY` | Sandbox key | Sandbox key | Production key |
| `MIXPANEL_TOKEN` | Optional | Staging token | Production token |
| `AMPLITUDE_KEY` | Optional | Optional | Production key |
| `SENTRY_DSN` | Optional | Staging DSN | Production DSN |
| `ONESIGNAL_APP_ID` | Test app | Test app | Production app |
| `APPLE_TEAM_ID` | Your team ID | Your team ID | Your team ID |

---

## Validation checklist

Before each release:

- [ ] All production secrets are set in CI/CD
- [ ] `.env.production` is NOT committed to git
- [ ] Bundle ID matches App Store Connect
- [ ] RevenueCat production key is configured
- [ ] Analytics tokens are production tokens
- [ ] Sentry DSN points to production project
- [ ] Debug mode is disabled in production config

---

## Troubleshooting

### Environment not loading

1. Clean build folder: `rm -rf ios/build android/app/build`
2. Clear Metro cache: `npx react-native start --reset-cache`
3. Reinstall pods: `cd ios && rm -rf Pods && pod install`

### Wrong environment in build

1. Check scheme configuration in Xcode
2. Verify `.env` file exists for the environment
3. Check build logs for react-native-config output

### Secrets not available in CI

1. Verify secret names match exactly (case-sensitive)
2. Check secret scope (repository vs organization)
3. Verify workflow has access to secrets

---

Created: 2026-01-21
