# App Spec: STREAKR V2 — Swipe Habits + Minimum Viable Day
## source: priority queue convergence RF_002, RF_006, rank-5 paywall alpha, ALPHA1773997578
## generated: 2026-03-22
## roi_potential: HIGH
## build_decision: BUILD_NEW_NOW (no existing Streakr build exists — greenfield)
## score: 122 (convergence of 3 queue items)
## estimated_time_to_first_win: 4-7 days post-deploy (based on HabitSwipe 2-month reference)

---

## Why This Now

Queue convergence signal: RF_002 (HabitSwipe $799/2mo, 2.5K users), RF_006 (MVD 307 upvotes), and rank-5 paywall framework all point at the same gap — a minimalist, swipe-based habit tracker with an emotionally lighter framing than Fabulous or generic streak counters.

SoberStreak (deployed March 21) validated the swipe + MVD implementation. Streakr takes the same tech stack and applies it to the widest-market general habit audience.

Competitor gap: Fabulous (87K reviews, 4.45 stars) is the only major monetized habit app. It is overengineered, subscription-aggressive, and designed for self-improvement completionists. Our target user is the person who downloaded Fabulous, felt overwhelmed after 3 days, and quit. They want 3 non-negotiables and a satisfying swipe.

---

## Product Identity

**Name:** Streakr
**Tagline:** Track fewer things. Actually keep them.
**Category:** Health & Fitness (App Store) / Health & Fitness (Google Play)
**Secondary category:** Productivity
**Target user:** 22-40, had a bad habit app experience, wants simplicity, embarrassed to track 10 habits that aren't sticking
**Privacy promise:** No account. Nothing leaves your device.

---

## Core Promise

One swipe per habit. Three non-negotiables. That's a win.

Not "build 12 atomic habits at once." Not a productivity system. Not a life coach.

A quiet app that makes one daily check-in feel satisfying instead of shameful.

---

## Feature Set (MVP — build this version first)

### 1. Onboarding (5 screens max)
- Screen 1: "What do you want to actually keep?" — hero with animated swipe card demo
- Screen 2: Pick mode — **Classic Streaks** (track everything) OR **Minimum Viable Day** (3 non-negotiables)
- Screen 3: Set 1-3 starter habits (pre-filled suggestions by category: movement, learning, mindfulness, creation)
- Screen 4: Complete ONE habit right now — swipe up on the card → haptic buzz → "Day 1 starts now" celebration
- Screen 5: Reminder permission — shown AFTER the first win, never before

Onboarding exits directly into the main screen with Day 1 already started. No login wall.

### 2. Main Screen — Swipe Cards
- Full-screen card stack: each habit is a card
- Swipe UP to complete — threshold 45px vertical, <40px horizontal drift (same as SoberStreak)
- Haptic feedback on completion: `navigator.vibrate(30)`
- Card shows: habit name, current streak count, ring progress (0-100%)
- Completed cards sink to bottom with subtle green overlay and checkmark
- If all cards swiped: confetti animation + day complete state

### 3. Minimum Viable Day (MVD) Mode
- Toggle in settings (also offered at onboarding)
- User defines 3 non-negotiables (can edit any time)
- MVD section appears above card stack when enabled
- Three tap-to-complete goal items
- When all 3 done: "Win achieved" gold badge animates in
- MVD completion state persists per-day, resets at midnight
- Daily history shows MVD win/loss over trailing 30 days

### 4. Streak View
- Tap any habit card to see: current streak, longest streak, completion calendar (GitHub-style heatmap), milestones achieved
- Milestones at: 3, 7, 14, 30, 90, 180, 365 days
- Streak repair (premium): one slip forgiven per 30-day window
- Share card for milestones: pre-generated graphic, no watermark, branded "Streakr"

### 5. Review Prompt
- Fires ONLY at Day 3 or Day 7 streak on ANY habit — whichever comes first
- Never fires on session 1 or session 2
- 90-day cooldown after first prompt
- 5-day delay if user taps "maybe later"
- Uses StoreKit requestReview() (native) / Play InAppReview API (Android)

### 6. Paywall
- Shown AFTER first habit completion (post-value, not pre-value)
- Free tier: up to 3 habits, basic streak view, no MVD history
- Paid tier: unlimited habits, streak repair (1/month), MVD full history, share cards, themes, CSV export
- Paywall headline: "You already started. Keep the streak alive."
- Sub-headline: "Day 1 is done. Let's make sure Day 7 happens."
- Pricing display order: Annual ($24.99/yr, shown first and largest) → Monthly ($4.99/mo, shown smaller)
- 7-day trial on annual only
- No monthly trial (reduces cannibalization)
- LTD test (Phase 2 only, after 500 installs): $29.99 lifetime anchor

### 7. Data + Privacy
- All state in localStorage — zero server calls
- Export: CSV of all streaks (premium)
- Privacy policy: dedicated `/privacy-policy.html`
- Terms: `/terms.html`
- EULA: link to Apple standard EULA (no custom required)
- No analytics SDK, no crash reporter, no ad network
- Subscription disclaimer in App Store description: "Streakr offers a 7-day free trial. Subscription auto-renews unless cancelled 24 hours before renewal date."

---

## Monetization Config

| Item | Value |
|------|-------|
| Primary revenue | RevenueCat subscription |
| iOS product ID (annual) | `streakr.annual.2999` |
| iOS product ID (monthly) | `streakr.monthly.499` |
| iOS product ID (LTD) | `streakr.lifetime.2999` (Phase 2) |
| Trial | 7 days on annual only |
| Annual price test A | $24.99/yr |
| Annual price test B | $29.99/yr |
| Monthly price | $4.99/mo |
| RevenueCat env var | `EXPO_PUBLIC_REVENUECAT_IOS_KEY` |
| Paywall timing | After first habit completion |
| Free tier cap | 3 habits |

**Implementation note:** Wire RevenueCat from the start. Do not ship a fake `isPremium = false` boolean. If RevenueCat keys are not yet available, gate with a `PAYWALL_ENABLED` env flag and show paywall UI in demo mode that clearly labels itself as demo.

---

## Technical Spec

### Stack
- PWA HTML/CSS/JS (same pattern as SoberStreak) for Day 1 deploy on Surge
- Expo + React Native for App Store native build (Phase 2)
- RevenueCat iOS SDK for IAP
- No external APIs, no auth layer, no backend

### Key Files (PWA phase)
```
MONEY_METHODS/APP_FACTORY/builds/streakr/
  index.html          — main app (single file for PWA deploy)
  manifest.json       — PWA manifest (name, icons, theme_color)
  sw.js               — service worker (offline cache, cache-first strategy)
  privacy-policy.html — required for App Store
  terms.html          — required for App Store
  robots.txt          — allow indexing
  sitemap.xml         — SEO baseline
  ASO_KEYWORDS.md     — keyword targeting doc
```

### State Model (localStorage key: `streakr_v2`)
```json
{
  "habits": [
    { "id": "h1", "name": "Morning walk", "emoji": "🚶", "category": "movement", "streak": 3, "longest": 7, "history": {"2026-03-22": true} }
  ],
  "mvdEnabled": false,
  "mvdGoals": ["", "", ""],
  "mvdCompleted": {"2026-03-22": [0, 2]},
  "lastReviewPrompt": null,
  "isPremium": false,
  "trialStarted": null,
  "installDate": "2026-03-22"
}
```

### Swipe Implementation (copy from SoberStreak, parameterized)
```js
// Applied to each habit card element
function attachSwipe(cardEl, habitId) {
  let startY = 0, startX = 0;
  cardEl.addEventListener('touchstart', e => {
    startY = e.touches[0].clientY;
    startX = e.touches[0].clientX;
  }, {passive: true});
  cardEl.addEventListener('touchend', e => {
    const dy = startY - e.changedTouches[0].clientY;
    const dx = Math.abs(startX - e.changedTouches[0].clientX);
    if (dy > 45 && dx < 40) {
      if (navigator.vibrate) navigator.vibrate(30);
      completeHabit(habitId);
    }
  }, {passive: true});
}
```

### Review Prompt (copy from March 21 pattern)
```js
function maybeShowReviewPrompt() {
  const milestones = [3, 7, 14, 30, 90];
  const anyMilestone = state.habits.some(h => milestones.includes(h.streak));
  if (!anyMilestone) return;
  if (state.lastReviewPrompt) {
    const daysSince = (Date.now() - new Date(state.lastReviewPrompt)) / 86400000;
    if (daysSince < 90) return;
  }
  // iOS: window.webkit.messageHandlers.requestReview?.postMessage({})
  // Web: show modal with "Leave a Review?" prompt linking to store page
  state.lastReviewPrompt = new Date().toISOString();
  saveState();
}
```

---

## Visual Direction

- Background: warm ivory `#faf8f5`
- Accent: emerald `#10b981` for active streaks, charcoal `#1c1c1e` for text
- Progress rings: thick stroke, smooth `stroke-dashoffset` animation
- Cards: rounded-xl, soft shadow, no border lines
- Completion state: ring fills green, card gets subtle green glow, satisfying pop
- Milestone badges: gold `#f59e0b` on dark background
- Typography: system-ui (SF Pro on iOS, Roboto on Android) — no Google Fonts import
- No hover states that feel like a website — every tap element has a tap scale effect

---

## Onboarding Paywall Funnel (A/B test plan)

| Variant | Paywall trigger | Expected trial rate |
|---------|----------------|---------------------|
| A (default) | After first habit completion | 8-11% |
| B | After onboarding completes, before main screen | 5-7% |
| C | After Day 3 streak | 4-6% |

Run variant A first. Switch to B only if trial rate < 5% at 200 installs.

---

## ASO Strategy

### Primary keywords
- habit tracker app
- streak counter
- daily habits app
- habit app no account
- swipe habit tracker

### Secondary keywords
- minimum viable day
- daily routine tracker
- simple habit app
- habit streak app 2026
- private habit tracker

### App Store description (first 252 chars = shown without truncation)
"The habit app for people who hate habit apps. Pick 3 non-negotiables. Swipe to complete. That's a win. No account. No servers. All your data stays on your phone."

### Screenshots spec (6 screenshots required for App Store)
1. Hero: swipe-to-complete animation mid-swipe
2. Main screen: 3 cards with 1 completed (green glow)
3. MVD mode: "Win achieved" gold badge moment
4. Streak view: 7-day heatmap with milestone badge
5. Paywall screen: annual plan selected
6. Onboarding screen 2: mode selection

### Review prompt timing (already specced above)
Day 3 or Day 7 streak. Drives organic App Store rating without annoying new users.

---

## App Store Submission Checklist (from ALPHA1773997578)

Before submitting native build to App Store review:

- [ ] `/privacy-policy.html` live at `https://streakr.surge.sh/privacy-policy`
- [ ] `/terms.html` live at `https://streakr.surge.sh/terms`
- [ ] EULA: link to `https://www.apple.com/legal/internet-services/itunes/dev/stdeula/` (no custom EULA needed)
- [ ] Subscription disclaimer in App Store description
- [ ] "Requires subscription" note in app metadata if using hard paywall variant
- [ ] No use of private APIs (audit React Native deps before submit)
- [ ] Screenshots at 6.9" (iPhone 16 Pro Max) and 6.5" (older) minimum
- [ ] Privacy manifest (PrivacyInfo.xcprivacy) for any tracking-adjacent APIs
- [ ] Age rating: 4+ (no objectionable content)
- [ ] Support URL: `https://streakr.surge.sh` (surge URL fine for initial submit)

---

## Build Order

### Phase 1: PWA (deploy in < 1 day)
1. Create `MONEY_METHODS/APP_FACTORY/builds/streakr/`
2. Build `index.html` with: habit card stack, swipe-to-complete, MVD section, paywall screen (demo mode), review prompt logic
3. Generate `manifest.json`, `sw.js` (offline cache), `privacy-policy.html`, `terms.html`, `robots.txt`
4. Deploy: `surge MONEY_METHODS/APP_FACTORY/builds/streakr/ streakr.surge.sh`
5. Cross-post link: r/productivity, r/habittracking, r/nosurf, r/getdisciplined

### Phase 2: Native (after 200 PWA installs OR App Store account ready)
1. Initialize Expo project from scripture-streak base template
2. Wire RevenueCat with `streakr.annual.2999` and `streakr.monthly.499` products
3. Implement `StoreKit requestReview()` at milestones
4. Build App Store screenshots at 6.9" and 6.5"
5. Submit with all checklist items verified

### Phase 3: Iterate (after 500 installs)
1. Run paywall variant A vs B
2. Add LTD $29.99 lifetime plan as anchor test
3. Add 5 pre-built habit packs (Morning Routine, Deep Work, Fitness, Learning, Mindfulness)
4. Share cards for milestones (social distribution engine)

---

## Success Metrics

| Metric | Target | Measure at |
|--------|--------|-----------|
| Day 7 retention | > 30% | 200 installs |
| Trial start rate | > 8% | 200 installs |
| Trial conversion | > 40% | 100 trials |
| App Store rating | > 4.3 | 50 reviews |
| Monthly revenue | > $100 | 60 days |

Kill criteria: if Day-7 retention < 20% at 500 installs, the core loop is broken. Don't iterate pricing — rebuild the daily check-in flow.

Double-down criteria: if trial rate > 10% at 500 installs, expand to 5 more habit-adjacent niches using the same template.

---

## Distribution Plan

### Launch week (no budget, organic only)
- Post on r/productivity with "built this because I kept quitting habit apps" narrative (mirror HabitSwipe approach)
- Tweet thread: "Stop tracking 10 habits. Define your minimum viable day instead." (repurpose RF_006 viral concept)
- Reply to "best habit app" threads in r/selfimprovement, r/nosurf, r/getdisciplined
- Submit to Product Hunt (after basic App Store listing live)
- Add to app-factory apps list in OPS/DEPLOYMENT_URLS.md

### Content assets to generate after deploy
- 3 tweets (short form): swipe demo gif, MVD concept hook, streak milestone share
- 1 thread: "I analyzed why 90% of people quit habit apps in 3 days"
- Reddit post copy (ready for r/productivity, r/habittracking)

---

## Human Blockers

| Blocker | Time | Impact |
|---------|------|--------|
| App Store account ($99/yr) | 20 min | Blocks native iOS submit |
| RevenueCat account | 15 min | Blocks real IAP |
| App Store Connect IAP products | 30 min | Blocks real billing |
| Stripe account | 10 min | Blocks web payment backup |

PWA deploy to `streakr.surge.sh` requires ZERO accounts. Build and deploy the PWA first while waiting on account creation.

---

## Relationship to Existing Apps

This spec does NOT replace or conflict with:
- **SoberStreak** (`soberstreak.surge.sh`): niche sobriety/NoFap vertical — different user, different ASO
- **Scripture Streak** (`scripture-streak`): faith vertical — different audience entirely
- **PrayerLock** (`prayerlock-web`): prayer/devotional — different user intent

Streakr is the HORIZONTAL layer — a general-purpose habit app with no niche. SoberStreak, Scripture Streak, PrayerLock are VERTICAL specializations. They can cross-link to Streakr as the "general habits" companion.
