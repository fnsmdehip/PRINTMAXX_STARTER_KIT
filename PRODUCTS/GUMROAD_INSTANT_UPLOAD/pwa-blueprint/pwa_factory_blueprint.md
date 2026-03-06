# PWA App Factory Blueprint

## how to build, ship, and monetize apps in 24-48 hours using Claude Code

---

## Part 1: The PWA Factory Pipeline

most people treat app development like a project. one app, months of work, hope it works. the factory model flips this: build fast, test fast, kill losers, double winners. 7 apps shipped in under 2 months using this exact pipeline.

### the pipeline

```
idea (1 hour) -> validate (2 hours) -> build overnight (8 hours) ->
test (2 hours) -> polish (4 hours) -> deploy (1 hour) ->
App Store submit (1 hour) -> ASO + monetize (ongoing)
```

total time per app: 19 hours of your attention, 8 hours of Claude Code doing the building.

### idea validation (kill bad ideas fast)

before building anything, run this 5-minute check:

1. **search the App Store for your keyword.** if the top 5 results have under 100 reviews each, the niche has room. if the top result has 50,000 reviews, pick a different angle.

2. **search "site:reddit.com [your app idea]".** if people are asking for it and nobody's built it, you found gold. if people are asking for it and the responses are "use [competitor]," study that competitor.

3. **check Google Trends for the keyword.** trending up = good. trending down = bad. flat = okay if the niche is big enough.

4. **estimate willingness to pay.** B2B and productivity tools: people pay. social apps: people don't. health/fitness: mixed. utilities: pay if unique.

5. **can you build an MVP in one overnight session?** if the core feature needs more than 8 hours of Claude Code, the scope is too big. cut features until it fits.

if an idea fails any of these checks, move to the next one. ideas are cheap. execution time is expensive.

---

## Part 2: The Overnight Build Loop

this is the core of the factory. you set up a task list at night, Claude Code works through it, you wake up to a working app.

### the PROMPT.md template

this file tells Claude Code what to build. the structure matters. here's the exact template:

```markdown
# build: [APP NAME]

## what this app does
[one sentence. if you need two sentences, your scope is too big.]

## tech stack
- HTML/CSS/JavaScript (vanilla) OR Next.js
- no external dependencies unless absolutely necessary
- must work as PWA (offline capable)
- mobile-first responsive design

## screens to build

### screen 1: [name]
- [exact UI description]
- [what happens when user interacts]
- [data that needs to persist]

### screen 2: [name]
- [same format]

### screen 3: [name]
- [same format]

## data model
- [what data the app stores]
- [use localStorage for MVP]
- [structure: { key: value }]

## PWA requirements
- manifest.json with all required fields
- service worker with cache-first strategy
- offline fallback page
- install prompt handling

## state management
- read STATE.md before starting each task
- update STATE.md after completing each screen
- one screen per iteration

## quality bar
- must look like a top-10 app in its category
- dark mode by default
- no placeholder text
- transitions and animations where appropriate
- loading states for all async operations
```

### the STATE.md template

```markdown
# app build state

## completed
(none)

## current screen
(none)

## errors
(none)

## notes
(none)
```

### the loop script

```bash
#!/bin/bash
# build_app.sh

APP_DIR="/path/to/app"
MAX_ITERATIONS=15

for i in $(seq 1 $MAX_ITERATIONS); do
    echo "=== iteration $i at $(date) ==="

    cat "$APP_DIR/PROMPT.md" | claude --dangerously-skip-permissions --print \
        --project-dir "$APP_DIR"

    # check if build is complete
    if grep -q "ALL SCREENS COMPLETE" "$APP_DIR/STATE.md" 2>/dev/null; then
        echo "build complete at iteration $i"
        break
    fi

    sleep 3
done
```

### running the overnight build

```bash
# start at midnight
chmod +x build_app.sh
nohup ./build_app.sh > build.log 2>&1 &

# check progress in the morning
tail -50 build.log
cat STATE.md
```

### prompt engineering tips for Claude Code

1. **be specific about layout.** "a card with rounded corners" fails. "a 320px wide card with 12px border-radius, 16px padding, #141414 background, 1px solid #222 border" works.

2. **describe interactions.** "user can add items" fails. "when user types in the input field and presses Enter or clicks the Add button, the item appears at the top of the list with a fade-in animation, and the input field clears" works.

3. **specify the data shape.** "store user data" fails. "store in localStorage under key 'app_data' as JSON: { items: [{ id: string, text: string, createdAt: ISO8601, completed: boolean }] }" works.

4. **include error states.** "handle errors" fails. "if the API call fails, show a red banner at the top of the screen that says 'connection failed, tap to retry' and auto-dismisses after 5 seconds" works.

5. **reference real apps.** "make it look good" fails. "layout similar to Apple Reminders: clean list, swipe actions, bottom tab bar, SF-style font" works.

---

## Part 3: manifest.json Template

copy this, change the values, done.

```json
{
  "name": "Your App Name",
  "short_name": "AppName",
  "description": "One sentence description of what the app does",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#22c55e",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/icons/icon-72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["productivity"],
  "screenshots": [
    {
      "src": "/screenshots/screen1.png",
      "sizes": "1080x1920",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ]
}
```

### icon generation

you need 8 icon sizes. do this once:

1. create a 1024x1024 icon (Figma, Canva, or even DALL-E)
2. use a resizer tool (realfavicongenerator.net or sharp in Node.js)
3. save all sizes in `/icons/`

```bash
# quick resize with ImageMagick
for size in 72 96 128 144 152 192 384 512; do
    convert icon-1024.png -resize ${size}x${size} icons/icon-${size}.png
done
```

### linking manifest in HTML

```html
<head>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#22c55e">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <link rel="apple-touch-icon" href="/icons/icon-192.png">
</head>
```

---

## Part 4: Service Worker Template

this handles offline mode, caching, and push notifications.

```javascript
// sw.js - service worker

const CACHE_NAME = 'app-cache-v1';
const OFFLINE_URL = '/offline.html';

// files to cache on install
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/manifest.json',
  OFFLINE_URL,
];

// install: cache core files
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS);
    })
  );
  self.skipWaiting();
});

// activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// fetch: cache-first for assets, network-first for API
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // skip non-GET requests
  if (request.method !== 'GET') return;

  // API calls: network first, fall back to cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // everything else: cache first, fall back to network
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;

      return fetch(request)
        .then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return response;
        })
        .catch(() => {
          // offline fallback for navigation requests
          if (request.mode === 'navigate') {
            return caches.match(OFFLINE_URL);
          }
        });
    })
  );
});

// push notifications (optional)
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const options = {
    body: data.body || 'New notification',
    icon: '/icons/icon-192.png',
    badge: '/icons/icon-72.png',
    data: { url: data.url || '/' },
  };
  event.waitUntil(self.registration.showNotification(data.title || 'App', options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url));
});
```

### registering the service worker

```javascript
// in your main app.js
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => console.log('SW registered:', reg.scope))
      .catch((err) => console.log('SW failed:', err));
  });
}
```

### the offline fallback page

```html
<!-- offline.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>offline</title>
  <style>
    body {
      background: #0a0a0a;
      color: #e0e0e0;
      font-family: -apple-system, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      text-align: center;
    }
    h1 { font-size: 1.5rem; margin-bottom: 8px; }
    p { color: #888; }
  </style>
</head>
<body>
  <div>
    <h1>you're offline</h1>
    <p>check your connection and try again.</p>
  </div>
</body>
</html>
```

---

## Part 5: Capacitor Bridge (PWA to App Store)

Capacitor wraps your web app in a native shell. your PWA runs inside WKWebView (iOS) or WebView (Android). same code, native distribution.

### setup

```bash
# in your project directory
npm init -y
npm install @capacitor/core @capacitor/cli
npx cap init "App Name" "com.yourcompany.appname"
```

this creates `capacitor.config.ts`:

```typescript
import { CapacitorConfig } from '@capacitor/core';

const config: CapacitorConfig = {
  appId: 'com.yourcompany.appname',
  appName: 'App Name',
  webDir: 'dist',  // or 'build' or 'out' depending on your framework
  server: {
    // for development, point to local server
    // url: 'http://localhost:3000',
    // cleartext: true,
  },
  plugins: {
    SplashScreen: {
      launchAutoHide: true,
      androidSplashResourceName: 'splash',
      showSpinner: false,
    },
  },
};

export default config;
```

### adding platforms

```bash
# build your web app first
npm run build  # or whatever your build command is

# add iOS
npm install @capacitor/ios
npx cap add ios

# add Android
npm install @capacitor/android
npx cap add android

# sync web code to native projects
npx cap sync
```

### running on iOS Simulator

```bash
npx cap open ios
# this opens Xcode. hit the play button to run in Simulator.
```

### running on Android

```bash
npx cap open android
# opens Android Studio. run on emulator or device.
```

### the sync workflow

every time you change your web code:
```bash
npm run build   # rebuild web
npx cap sync    # copy to native projects
npx cap open ios  # or android
```

### common Capacitor issues

1. **white screen on iOS.** your `webDir` in capacitor.config.ts is wrong. check that `dist/` (or whatever) contains your index.html.

2. **API calls fail on device.** iOS blocks mixed content (HTTP from HTTPS). make sure all API calls use HTTPS.

3. **status bar overlaps content.** add `safe-area-inset-top` padding to your app's top element:
```css
body { padding-top: env(safe-area-inset-top); }
```

4. **keyboard pushes layout up.** add `Keyboard` plugin:
```bash
npm install @capacitor/keyboard
```

---

## Part 6: App Store Submission

### Apple App Store ($99/year developer account)

**pre-submission checklist:**

- [ ] app icon: 1024x1024 PNG, no alpha/transparency
- [ ] screenshots: at least 3 per device size (6.7", 6.5", 5.5" iPhones + iPad)
- [ ] app name: under 30 characters, include primary keyword
- [ ] subtitle: under 30 characters, include secondary keyword
- [ ] description: 4000 characters max, first 3 lines visible without "more"
- [ ] keywords: 100 characters, comma-separated, no spaces after commas
- [ ] privacy policy URL: required even if you collect zero data
- [ ] support URL: can be a simple webpage
- [ ] age rating: fill out the questionnaire honestly
- [ ] pricing: free with IAP, or paid upfront

**submission process:**

1. archive in Xcode (Product > Archive)
2. upload to App Store Connect via Xcode Organizer
3. fill out app information in App Store Connect
4. submit for review
5. review takes 1-3 days (usually 24 hours for simple apps)

**common rejection reasons and fixes:**

- "app is too simple" -> add at least 3 distinct screens/features
- "app crashes" -> test on real devices, not just Simulator
- "metadata issue" -> screenshots must match actual app UI
- "guideline 4.2 minimum functionality" -> make sure the app does something a website can't (offline mode, notifications)
- "privacy" -> add App Privacy section even if you collect nothing (select "Data Not Collected")

### Google Play Store ($25 one-time)

simpler process. submit an AAB file (Android App Bundle). review is usually under 24 hours. less strict than Apple but still check for crashes and policy compliance.

---

## Part 7: ASO (App Store Optimization)

ASO is SEO for the App Store. it determines whether anyone finds your app.

### keyword research process

1. **brainstorm seed keywords.** what would someone search to find your app? list 20 terms.

2. **check competition.** for each keyword, search the App Store. count the number of results with 1000+ reviews. if all top 10 have 1000+ reviews, the keyword is too competitive.

3. **find long-tail keywords.** "timer" is competitive. "focus timer for studying" is not. "habit tracker" is competitive. "daily water habit tracker" is not.

4. **use App Store autocomplete.** type your keyword and see what Apple suggests. these are real searches people make.

5. **tools (optional).** AppFollow, Sensor Tower, AppTweak. free tiers give enough data for indie apps.

### title optimization

your title is the strongest ranking signal. format:

```
[Brand Name] - [Primary Keyword Phrase]
```

examples:
- "FocusLock - Pomodoro Study Timer"
- "WaterLog - Daily Hydration Tracker"
- "ShiftCalc - Tip Calculator & Splitter"

### keyword field (iOS only)

100 characters. comma-separated. no spaces after commas. no duplicates of words already in your title.

```
pomodoro,focus,study,timer,productivity,concentration,deep,work,session,break
```

tips:
- use singular, not plural (Apple matches both)
- don't repeat words from your title
- test different keywords monthly based on impression data

### description optimization

first 3 lines are visible without tapping "more." put your best pitch there.

```
track your daily water intake in 3 seconds. set your goal, tap to log,
see your streak. no account needed. works offline.

features:
- one-tap logging
- daily/weekly/monthly charts
- reminder notifications
- widget for home screen
- data export to CSV
- zero ads in free version
```

### screenshots that convert

1. first screenshot = main value proposition ("track your water in 3 seconds")
2. second screenshot = key feature ("see your streaks")
3. third screenshot = social proof or differentiator ("100% offline, no account")
4. use device frames (mockuphone.com or screenshots.pro)
5. text on screenshots should be 40pt+ (readable in search results)

---

## Part 8: Monetization with RevenueCat

RevenueCat handles in-app purchases across iOS, Android, and web. one SDK, all platforms.

### setup

```bash
npm install @revenuecat/purchases-capacitor
npx cap sync
```

### configuration

```typescript
import { Purchases } from '@revenuecat/purchases-capacitor';

// initialize on app start
async function initRevenueCat() {
  await Purchases.configure({
    apiKey: 'your_revenuecat_api_key',
    // appUserID: 'optional-user-id',
  });
}

// check subscription status
async function checkSubscription() {
  const { customerInfo } = await Purchases.getCustomerInfo();
  const isSubscribed = customerInfo.entitlements.active['pro'] !== undefined;
  return isSubscribed;
}

// show available packages
async function getOfferings() {
  const { offerings } = await Purchases.getOfferings();
  if (offerings.current) {
    return offerings.current.availablePackages;
  }
  return [];
}

// purchase
async function purchasePackage(pkg) {
  try {
    const { customerInfo } = await Purchases.purchasePackage({ aPackage: pkg });
    return customerInfo.entitlements.active['pro'] !== undefined;
  } catch (e) {
    if (e.userCancelled) return false;
    throw e;
  }
}

// restore purchases
async function restorePurchases() {
  const { customerInfo } = await Purchases.restorePurchases();
  return customerInfo.entitlements.active['pro'] !== undefined;
}
```

### paywall strategy

**what to gate:**

- free: core functionality (enough to be useful and get reviews)
- paid: advanced features, no ads, export, themes, unlimited items

**pricing that works for indie apps:**

- $2.99/month or $19.99/year (most common)
- $4.99 one-time unlock (simpler but less revenue long-term)
- free trial (3 or 7 days) increases conversion 2-3x

**paywall placement:**

- show after the user has experienced value (not on first open)
- trigger when they hit a limit ("you've tracked 7 habits, upgrade for unlimited")
- settings screen always has a "restore purchases" and "upgrade" option

### RevenueCat dashboard setup

1. create a project in RevenueCat
2. add your Apple/Google credentials
3. create an "Entitlement" called "pro"
4. create "Products" matching your App Store Connect / Google Play products
5. create an "Offering" with "Packages" (monthly, yearly, lifetime)
6. test with sandbox accounts before going live

---

## Part 9: 7 Real Prompts from Shipped Apps

these are actual PROMPT.md files (simplified) from apps that are live in the App Store right now.

### prompt 1: habit tracker

```
build a minimal habit tracker. user creates habits with a name and color.
each day they tap to mark complete. show a streak counter and a 30-day
grid (green = done, gray = missed). localStorage. dark mode. 5 screens:
habits list, add habit, habit detail with grid, settings, stats.
```

### prompt 2: tip calculator

```
tip calculator for restaurants. input: bill amount, tip percentage
(slider 0-30%), number of people. output: tip amount, total, per-person
amount. one screen. big numbers. large touch targets. save last 10
calculations. dark mode.
```

### prompt 3: focus timer

```
pomodoro timer. 25 min focus, 5 min break, 15 min long break every 4
sessions. start/pause/reset. audio notification when timer ends. daily
stats (sessions completed, total focus time). weekly chart. localStorage.
dark mode. prevent screen from sleeping during focus.
```

### prompt 4: water tracker

```
log water intake. one tap to add a glass (250ml). daily goal: 8 glasses
(configurable). progress ring on main screen. history view with last
30 days. reminder notifications every 2 hours. widget shows today's
progress. localStorage. dark mode.
```

### prompt 5: expense splitter

```
split expenses between friends. create a group, add members, add
expenses with who paid and who benefited. calculate optimal settlements
(minimize number of transactions). share results via native share.
localStorage. dark mode. handle unequal splits.
```

### prompt 6: decision maker

```
helps make decisions. user inputs options (2-10). app runs weighted
comparison: rate each option on criteria they define (1-10 scale).
shows winner with radar chart. save past decisions. share results.
localStorage. dark mode. gamified reveal animation.
```

### prompt 7: daily journal

```
one-screen journal. prompt with today's question (rotating list of 365
questions). text input area. save with date. calendar view to see past
entries. export all entries as markdown. word count tracker. localStorage.
dark mode. end-of-year review summary.
```

---

## Part 10: The Factory Workflow (Putting It All Together)

### week 1: build 3 apps

- monday: validate 5 ideas, pick the best 3
- monday night: start overnight build #1
- tuesday: test and polish app #1, start overnight build #2
- wednesday: test and polish app #2, start overnight build #3
- thursday: test and polish app #3
- friday: deploy all 3 as PWAs (surge.sh or Vercel)

### week 2: submit to App Store

- monday: Capacitor bridge for app #1, submit to App Store
- tuesday: Capacitor bridge for app #2, submit
- wednesday: Capacitor bridge for app #3, submit
- thursday: ASO for all 3 (keywords, screenshots, descriptions)
- friday: set up RevenueCat for all 3

### week 3+: measure and iterate

- check App Store Connect analytics weekly
- track: impressions, downloads, retention, revenue
- kill apps with under 10 downloads/week after 30 days
- double down on winners (add features, improve ASO)
- start next batch of 3

### the math

7 apps. if 2 get 100 downloads/month. 5% conversion to $2.99/month sub.

- 2 apps x 100 downloads x 5% x $2.99 = $29.90/month
- after Apple's 30% cut: $20.93/month
- not life-changing, but that's just 2 working apps out of 7
- scale to 20 apps, find better niches, improve conversion
- the factory advantage: you can test 3 ideas per week instead of 1 per quarter

---

## what to do right now

1. pick one app idea from Part 9 or your own list
2. write a PROMPT.md using the template from Part 2
3. run the overnight loop tonight
4. tomorrow morning: test, polish, deploy
5. by this weekend: submit to App Store

the bottleneck is never "can I build this." with Claude Code, you can build anything in a night. the bottleneck is "am I building the right thing." that's why the validation step in Part 1 matters more than everything else combined.
