# Module 2: Build Your First PWA in 2 Hours

## What You'll Have After This Module

A fully functional Progressive Web App — installable on phones, works offline, looks professional — built from a single Claude Code session. Not a tutorial project. A real app you could charge money for.

## The App: A Habit Tracker That Actually Works

We're building "StreakPad" — a habit tracker that stores data locally, works offline, and installs like a native app. Habit trackers sell. There are 47 of them on the App Store charging $4.99-$9.99/month. You're going to build one in 2 hours for $0.

Why a habit tracker? Three reasons:
1. Simple data model (habits + daily check-ins = two arrays)
2. High perceived value (people pay $60/year for these)
3. Zero backend needed (localStorage handles everything until you have 1000+ users)

## Hour 1: Core Functionality (0:00 - 1:00)

Open your terminal in your project directory and launch Claude Code:

```bash
cd streakpad && claude
```

Give Claude this prompt. Copy it exactly:

```
Build a Progressive Web App called StreakPad — a habit tracker.

Requirements:
- Single page app, vanilla JS, no frameworks
- Users can add habits with a name and target frequency (daily, weekly)
- Main screen shows today's habits with tap-to-complete toggles
- Streak counter shows consecutive days completed for each habit
- All data stored in localStorage
- Dark mode by default with a light mode toggle
- Mobile-first, max-width 480px centered on desktop
- PWA manifest and service worker for offline + installable
- Color scheme: #0A0A0A background, #00FF88 accent, #FFFFFF text

File structure:
- index.html (entry point)
- css/style.css
- js/app.js (main logic)
- js/storage.js (localStorage wrapper)
- manifest.json
- sw.js (service worker)
- icons/ (generate simple SVG icons, 192x192 and 512x512)

Start with the data layer (storage.js), then UI, then PWA features.
```

Claude will create all these files. Watch the output — it's building your app in real-time, file by file. This takes about 10-15 minutes.

Once it's done, test it:

```bash
npx serve .
```

Open `localhost:3000` in Chrome. You should see a dark-themed habit tracker. Add a habit. Check it off. Refresh the page — it should persist.

### Fixing What's Broken

First build is never perfect. Here are the three things you'll likely need to fix:

**Problem 1: The toggle doesn't feel right.**

Tell Claude:
```
The habit toggle needs haptic feedback. Add a subtle CSS animation on tap —
scale to 0.95 then back to 1.0 over 150ms. Also add a checkmark SVG that
animates in with a draw effect over 300ms when a habit is completed.
```

**Problem 2: The streak calculation is wrong.**

Tell Claude:
```
The streak counter is broken. A streak should count consecutive days where
the habit was completed, ending yesterday or today. If today is incomplete,
the streak should still show based on yesterday. If yesterday was missed,
streak resets to 0 regardless of today's status. Fix the calculateStreak
function in storage.js.
```

**Problem 3: It doesn't look professional.**

Tell Claude:
```
The UI needs polish:
1. Add a subtle gradient on the header (from #0A0A0A to #1A1A2E)
2. Habit cards should have a 1px border of rgba(255,255,255,0.08)
3. Add a floating action button (bottom-right, +) for adding new habits
4. The empty state should say "No habits yet. Tap + to start building streaks."
5. Add a stats section at the top: total habits, active streaks, completion rate today
```

Each fix takes 2-5 minutes. You're iterating on a working product, not building from scratch.

## Hour 2: PWA Features + Polish (1:00 - 2:00)

### Make It Installable (15 minutes)

Your manifest.json should already exist. Verify it has these fields:

```json
{
  "name": "StreakPad",
  "short_name": "StreakPad",
  "description": "Track habits. Build streaks. No account needed.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0A0A0A",
  "theme_color": "#00FF88",
  "icons": [
    { "src": "/icons/icon-192.svg", "sizes": "192x192", "type": "image/svg+xml" },
    { "src": "/icons/icon-512.svg", "sizes": "512x512", "type": "image/svg+xml" }
  ]
}
```

Tell Claude to verify the service worker caches all assets:

```
Update sw.js to use a cache-first strategy. Cache these files on install:
/, /index.html, /css/style.css, /js/app.js, /js/storage.js, /manifest.json
Version the cache name as 'streakpad-v1' so we can bust it on updates.
Add a fetch handler that serves from cache first, falls back to network.
```

Test installability: Open Chrome DevTools > Application > Manifest. You should see a green checkmark next to "Installable." Click "Install" in the browser bar.

### Add Notifications (15 minutes)

```
Add a daily reminder feature. When a user creates a habit, they can optionally
set a reminder time. Use the Notification API (request permission on first use).
Store reminder times in localStorage. Check every minute if any reminders
should fire. Show a notification with the habit name and current streak count.
No backend needed — this runs entirely in the service worker.
```

### Add Data Export (10 minutes)

```
Add a settings page (gear icon in header) with:
1. Export data as JSON (downloads a file)
2. Import data from JSON (file picker)
3. Clear all data (with confirmation dialog)
4. App version number
This page should slide in from the right with a CSS transition.
```

### Final Polish (20 minutes)

```
Final polish pass:
1. Add page transitions — when navigating to settings, slide the current view left
   and slide settings in from right. 300ms ease-out.
2. Add a "weekly view" — a 7-column grid showing completion status for the past week.
   Green squares for completed, dark gray for missed. Like GitHub's contribution graph.
3. Add an onboarding overlay for first-time users: "Welcome to StreakPad" with
   3 quick tips (swipe through). Show once, set a flag in localStorage.
4. Make the FAB pulse gently on first visit until the user taps it.
```

## Deploy It

```bash
npx surge ./ streakpad-app.surge.sh
```

Your app is now live at `streakpad-app.surge.sh`. Free. Instant. SSL included.

Open it on your phone. Tap "Add to Home Screen." You now have a native-feeling app on your phone that you built in 2 hours.

## What You Actually Built

Let's be specific about what you have:

- A PWA that installs on iOS and Android without an app store
- Offline functionality via service worker
- Local data persistence (no server costs)
- Push notification reminders
- Data import/export
- A polished UI with animations and transitions
- An onboarding flow

This is not a toy project. This is what $5K freelance clients pay for. The difference is you built it in 2 hours and spent $0.80 in API credits.

## The Exercise

Before moving to Module 3, build a second app. Pick one:

1. **Pomodoro timer** with session logging and daily stats
2. **Expense splitter** for groups (like Splitwise but simpler)
3. **Daily journal** with mood tracking and streaks

Same process. Same 2-hour window. The goal is speed, not perfection. Ship ugly, fix later, validate first.

If your second app takes longer than 2.5 hours, re-read your CLAUDE.md. You're probably letting Claude over-engineer it.

Next module: Getting your app on a custom domain and accessible to real users.
