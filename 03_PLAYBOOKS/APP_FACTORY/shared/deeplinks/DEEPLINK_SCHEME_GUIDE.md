# Deep Link Scheme Guide

Complete reference for deep link URL structures across all apps.

---

## URL Format Overview

### Custom Scheme Format
```
{scheme}://{action}/{resource_id}?{params}
```

### Universal Link Format
```
https://{domain}/{action}/{resource_id}?{params}
```

---

## App-Specific Schemes

### PrayerLock

**Custom Scheme:** `prayerlock://`
**Universal Domain:** `prayerlock.app`

| Action | URL Example | Description |
|--------|-------------|-------------|
| Open app | `prayerlock://open` | Opens app to home screen |
| View prayer | `prayerlock://prayer?id=abc123` | Opens specific prayer |
| View prayer (path) | `prayerlock://open/prayer/abc123` | Alternative format |
| Share streak | `prayerlock://share/streak?days=30` | Share streak achievement |
| Start prayer | `prayerlock://start` | Opens prayer timer |
| View profile | `prayerlock://profile?user=xyz` | Opens user profile |
| Invite | `prayerlock://invite?ref=USER123` | Referral invite link |
| Premium | `prayerlock://premium` | Opens paywall |
| Settings | `prayerlock://settings` | Opens settings |
| Content | `prayerlock://content?id=devotion123` | Opens specific content |

**Route Configuration:**
```typescript
const prayerlockRoutes: DeepLinkRoute[] = [
  {
    pattern: '/open',
    screen: 'Home',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/prayer/:id',
    screen: 'PrayerDetail',
    params: { id: 'prayerId' },
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/open/prayer/:id',
    screen: 'PrayerDetail',
    params: { id: 'prayerId' },
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/share/streak',
    screen: 'StreakShare',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/start',
    screen: 'PrayerTimer',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/profile/:user',
    screen: 'UserProfile',
    params: { user: 'userId' },
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/invite',
    screen: 'Onboarding',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/premium',
    screen: 'Paywall',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/settings',
    screen: 'Settings',
    stack: 'SettingsStack',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/content/:id',
    screen: 'ContentDetail',
    params: { id: 'contentId' },
    authRequired: false,
    premiumRequired: true,
  },
];
```

---

### WalkToUnlock

**Custom Scheme:** `walktounlock://`
**Universal Domain:** `walktounlock.app`

| Action | URL Example | Description |
|--------|-------------|-------------|
| Open app | `walktounlock://open` | Opens app to home |
| Challenge | `walktounlock://challenge?goal=10000` | Opens with goal challenge |
| Join challenge | `walktounlock://challenge/join?id=CH123` | Join specific challenge |
| View stats | `walktounlock://stats?period=week` | Opens statistics view |
| Share steps | `walktounlock://share/steps?count=12500&date=2024-01-20` | Share daily steps |
| Invite | `walktounlock://invite?ref=USER456` | Referral invite |
| Unlock reward | `walktounlock://reward?id=RW789` | Claim specific reward |
| Leaderboard | `walktounlock://leaderboard?type=weekly` | Open leaderboard |
| Premium | `walktounlock://premium` | Open paywall |

**Route Configuration:**
```typescript
const walktounlockRoutes: DeepLinkRoute[] = [
  {
    pattern: '/open',
    screen: 'Home',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/challenge',
    screen: 'ChallengeSetup',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/challenge/join/:id',
    screen: 'ChallengeJoin',
    params: { id: 'challengeId' },
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/stats',
    screen: 'Statistics',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/share/steps',
    screen: 'StepsShare',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/invite',
    screen: 'Onboarding',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/reward/:id',
    screen: 'RewardDetail',
    params: { id: 'rewardId' },
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/leaderboard',
    screen: 'Leaderboard',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/premium',
    screen: 'Paywall',
    authRequired: false,
    premiumRequired: false,
  },
];
```

---

### FaithStreak

**Custom Scheme:** `faithstreak://`
**Universal Domain:** `faithstreak.app`

| Action | URL Example | Description |
|--------|-------------|-------------|
| Open app | `faithstreak://open` | Opens app to home |
| Daily devotion | `faithstreak://devotion?date=2024-01-20` | Opens specific devotion |
| Share streak | `faithstreak://share/streak?days=100` | Share streak milestone |
| Reading plan | `faithstreak://plan?id=PLAN123` | Opens reading plan |
| Join group | `faithstreak://group/join?code=ABC123` | Join accountability group |
| Verse | `faithstreak://verse?ref=John3:16` | Opens specific verse |
| Invite | `faithstreak://invite?ref=USER789` | Referral invite |
| Premium | `faithstreak://premium` | Open paywall |

**Route Configuration:**
```typescript
const faithstreakRoutes: DeepLinkRoute[] = [
  {
    pattern: '/open',
    screen: 'Home',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/devotion',
    screen: 'DailyDevotion',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/share/streak',
    screen: 'StreakShare',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/plan/:id',
    screen: 'ReadingPlan',
    params: { id: 'planId' },
    authRequired: true,
    premiumRequired: true,
  },
  {
    pattern: '/group/join',
    screen: 'GroupJoin',
    authRequired: true,
    premiumRequired: false,
  },
  {
    pattern: '/verse',
    screen: 'VerseDetail',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/invite',
    screen: 'Onboarding',
    authRequired: false,
    premiumRequired: false,
  },
  {
    pattern: '/premium',
    screen: 'Paywall',
    authRequired: false,
    premiumRequired: false,
  },
];
```

---

## Common Parameters

### Attribution Parameters

These parameters are extracted for attribution tracking:

| Parameter | Alias | Description |
|-----------|-------|-------------|
| `utm_source` | - | Traffic source (google, facebook, etc.) |
| `utm_medium` | - | Marketing medium (cpc, social, email) |
| `utm_campaign` | `campaign`, `c` | Campaign name |
| `utm_content` | - | Ad creative identifier |
| `utm_term` | - | Search keyword |
| `channel` | `source` | Marketing channel |
| `campaign` | `c` | Campaign ID |
| `adgroup` | `ad_group`, `ag` | Ad group ID |
| `creative` | `ad` | Creative ID |
| `referrer` | `ref`, `r` | Referrer user ID |
| `click_id` | `gclid`, `fbclid`, `ttclid` | Click tracking ID |

### Adjust Parameters

| Parameter | Description |
|-----------|-------------|
| `adjust_tracker` | Adjust tracker token |
| `adj_tracker` | Adjust tracker (alias) |
| `adj_campaign` | Campaign name |
| `adj_adgroup` | Ad group |
| `adj_creative` | Creative name |

### AppsFlyer Parameters

| Parameter | Description |
|-----------|-------------|
| `pid` | Media source |
| `c` | Campaign |
| `af_ad` | Ad name |
| `af_adset` | Ad set name |
| `af_channel` | Channel |
| `af_status` | Attribution status |

### Branch Parameters

| Parameter | Description |
|-----------|-------------|
| `~feature` | Feature name |
| `~channel` | Channel |
| `~campaign` | Campaign |
| `~stage` | Funnel stage |
| `+match_guaranteed` | Match confidence |

---

## URL Examples by Use Case

### Organic Sharing

User shares their streak:
```
https://prayerlock.app/share/streak?days=30&ref=USER123
```

User invites friend:
```
https://walktounlock.app/invite?ref=USER456&campaign=word_of_mouth
```

### Paid Campaign Links

Facebook campaign:
```
https://prayerlock.app/premium?utm_source=facebook&utm_medium=paid&utm_campaign=jan_promo&utm_content=video_ad_1&fbclid=xyz
```

Google UAC:
```
https://walktounlock.app/challenge?goal=10000&utm_source=google&utm_medium=cpc&utm_campaign=fitness_q1&gclid=abc
```

TikTok:
```
https://faithstreak.app/invite?utm_source=tiktok&utm_medium=paid&utm_campaign=new_year&ttclid=123
```

### Adjust Tracking Link

```
https://app.adjust.com/abc123?campaign=summer_sale&adgroup=us_18_25&creative=video_1&deep_link=prayerlock%3A%2F%2Fpremium
```

### AppsFlyer OneLink

```
https://yourapp.onelink.me/abc123?pid=facebook&c=jan_campaign&af_dp=prayerlock%3A%2F%2Fpremium
```

### Branch Link

```
https://yourapp.app.link/abc123?~feature=referral&~channel=email&~campaign=winback
```

---

## Platform Configuration

### iOS: Info.plist

```xml
<!-- Custom URL Scheme -->
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>prayerlock</string>
    </array>
    <key>CFBundleURLName</key>
    <string>com.yourcompany.prayerlock</string>
  </dict>
</array>

<!-- Universal Links -->
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:prayerlock.app</string>
  <string>applinks:*.prayerlock.app</string>
</array>
```

### iOS: apple-app-site-association

Host at: `https://prayerlock.app/.well-known/apple-app-site-association`

```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAMID.com.yourcompany.prayerlock",
        "paths": [
          "/open/*",
          "/prayer/*",
          "/share/*",
          "/invite",
          "/premium",
          "/content/*"
        ]
      }
    ]
  }
}
```

### Android: AndroidManifest.xml

```xml
<!-- Custom Scheme -->
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="prayerlock" />
</intent-filter>

<!-- Universal Links (App Links) -->
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="https" android:host="prayerlock.app" />
</intent-filter>
```

### Android: assetlinks.json

Host at: `https://prayerlock.app/.well-known/assetlinks.json`

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.yourcompany.prayerlock",
      "sha256_cert_fingerprints": [
        "YOUR_SHA256_FINGERPRINT"
      ]
    }
  }
]
```

---

## Testing Deep Links

### iOS Simulator

```bash
# Custom scheme
xcrun simctl openurl booted "prayerlock://prayer?id=abc123"

# Universal link
xcrun simctl openurl booted "https://prayerlock.app/prayer/abc123"
```

### Android Emulator

```bash
# Custom scheme
adb shell am start -W -a android.intent.action.VIEW -d "prayerlock://prayer?id=abc123" com.yourcompany.prayerlock

# Universal link
adb shell am start -W -a android.intent.action.VIEW -d "https://prayerlock.app/prayer/abc123" com.yourcompany.prayerlock
```

### Development Testing

```typescript
// In React Native
import { Linking } from 'react-native';

// Simulate receiving a deep link
const testUrl = 'prayerlock://prayer?id=test123&utm_source=test';
Linking.emit('url', { url: testUrl });
```

---

## Validation Checklist

- [ ] Custom scheme registered in iOS Info.plist
- [ ] Custom scheme registered in Android manifest
- [ ] Universal link domain configured in iOS entitlements
- [ ] apple-app-site-association file hosted and accessible
- [ ] assetlinks.json file hosted and accessible
- [ ] All route patterns defined in config
- [ ] Attribution parameters being extracted
- [ ] Deep links work on cold start
- [ ] Deep links work while app is open
- [ ] Deep links requiring auth store as pending
- [ ] Pending links process after authentication
- [ ] Share link generation works
- [ ] Referral links include user ID
