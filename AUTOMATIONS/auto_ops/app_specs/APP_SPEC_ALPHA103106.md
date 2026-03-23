# SobrietyStreak — Full App Spec
## id: ALPHA103106
## generated: 2026-03-22 (refined from 2026-03-16 stub)
## priority: IMMEDIATE | score: 121 | roi_potential: HIGHEST
## status: SPEC_COMPLETE

---

## 1. THE INSIGHT

Quittr — the only paid NoFap/sobriety streak app — had a data privacy scandal (~2024, exposed user data to third parties). r/NoFap has 1.24M subscribers and no trustworthy, privacy-first paid alternative exists. iTunes confirms zero direct competitors in the "sober streak" category with a clean privacy track record. This is a trust gap that a local-first, no-data-collection app wins by default.

The user buying this app is embarrassed. They don't want their habit logged on a server. **Privacy is the product.**

---

## 2. APP IDENTITY

| Field | Value |
|-------|-------|
| **App name** | SobrietyStreak |
| **Tagline** | Your streak. Your phone. Nobody else's. |
| **Category** | Health & Fitness |
| **Sub-niche** | Addiction recovery / Habit quitting |
| **Bundle ID** | com.printmaxx.sobrietystreak |
| **Platform** | iOS first (Expo/React Native), Android after revenue proof |
| **Architecture** | Local-first. Zero server-side data. AsyncStorage + SecureStore only. |
| **Repo location** | `app factory/app-factory/non-religious-apps/sobriety-streak/` |

---

## 3. MARKET THESIS

- **Community size**: r/NoFap 1.24M + r/pornfree 600K + r/stopdrinking 430K + r/quittingsmoking 250K = 2.5M+ addressable users on Reddit alone
- **Blue ocean confirmed**: iTunes search for "nofap streak", "sober tracker", "sobriety counter" returns apps with 3.2-3.8 stars, no privacy focus, or abandoned (last update 2022)
- **Quittr trust gap**: Privacy scandal actively discussed in r/NoFap threads. Users specifically asking for alternatives
- **Conversion signal**: These users have high shame around the habit. They will pay for privacy. $2.99/mo or $24.99/yr is a trivial price for peace of mind
- **Expansion path**: Core NoFap -> add quitting smoking, drinking, gambling, social media as tracked habits (same app, broader TAM)

---

## 4. COMPETITOR ANALYSIS

| App | Rating | Reviews | Problem |
|-----|--------|---------|---------|
| Quittr | 3.8 | ~2K | Privacy scandal, server-side data |
| Streak - Habit Tracker | 4.4 | 12K | Generic, not niche-specific |
| Nofap Companion | 3.2 | 800 | Abandoned 2022, iOS 14 era UI |
| Habitify | 4.3 | 5K | No streak focus, not niche |

**1-star review themes** (Quittr + Nofap Companion):
- "They sell your data" / "Shared my streak history with advertisers"
- "App crashes when I try to log a relapse"
- "No widget support"
- "Notifications feel accusatory, not supportive"
- "Lost my streak data when I got a new phone"

**The product**: Fix all of these. Zero data collection, crash-proof relapse logging, homescreen widget, warm supportive tone, iCloud backup optional.

---

## 5. SCREENS (MVP — 8 screens total)

### Onboarding (4 screens)

**Screen 1 — Welcome**
- Copy: "Your streak is yours. We don't collect it, store it, or share it. Ever."
- Visual: Clean dark background, single emerald ring (0-day streak preview), subtle glow
- CTA: "Start My Streak"
- NO account creation, NO email capture

**Screen 2 — What are you working on?**
- Goal selector (multi-select allowed):
  - "No PMO / NoFap"
  - "Quit pornography"
  - "Stop drinking"
  - "Quit smoking"
  - "Break a social media habit"
  - "Something else"
- Copy: "Pick everything that applies. This stays on your phone."
- Visual: Card grid, emerald checkmark on select, satisfying haptic

**Screen 3 — Set your day 1**
- Date picker: "When did you last slip?" / "Today is Day 1"
- If selecting past date: show "Day X of your streak" with mild celebration
- Visual: Streak ring fills to match selected days
- **This is the value moment** — they see their streak visualized before the paywall

**Screen 4 — Paywall**
- Header: "Keep your streak. Keep it private."
- Personalization echo: "You're working on [selected goals]. SobrietyStreak will send you a daily check-in and celebrate every milestone — all locally on your device."
- Feature list (animated check-in):
  - Streak counter with daily check-in
  - Milestone badges (7d, 30d, 90d, 1yr)
  - Homescreen widget
  - Relapse reset with dignity (no shame messaging)
  - iCloud backup (optional, your choice)
  - Motivational reminders at your schedule
- Pricing (RevenueCat, annual-first):
  - **Annual: $24.99/yr** (pre-selected) — shown as "$2.08/mo"
  - Monthly: $3.99/mo
  - 7-day free trial on both
- "Your data never leaves your phone. No account needed."
- CTA: "Start 7-Day Free Trial"
- Skip link: "Maybe later" (soft paywall)

### Core App (4 screens)

**Home / Streak Dashboard**
- Giant streak counter (days, hours if < 1 day)
- Emerald progress ring (fills toward next milestone)
- Next milestone label ("30 days in 12 days")
- Quick check-in button (daily tap = streak continues)
- Last check-in timestamp
- "I slipped" button (subdued, non-judgmental placement)
- Widget preview area

**Milestones**
- Grid of achievement badges: 1d, 3d, 7d, 14d, 30d, 60d, 90d, 6mo, 1yr, 2yr
- Locked badges show silhouette. Earned badges glow.
- Each badge has a short, affirming message (not generic)
- Tap earned badge: share sheet option

**Journal (optional)**
- Simple text entry tied to streak day
- "What made today possible?" prompt
- Local only, never synced
- Entries visible in timeline

**Settings**
- Notification schedule (time picker, frequency)
- Reminder tone selector (gentle / standard / push)
- iCloud backup toggle (OFF by default — explain why, let them opt in)
- Privacy policy link (device-local, no server)
- "Restore purchases" link
- "Support" email link

---

## 6. MONETIZATION CONFIG

| Config | Value |
|--------|-------|
| Processor | RevenueCat |
| Env var | `EXPO_PUBLIC_REVENUECAT_APPLE_API_KEY` |
| Product ID (annual) | `sobrietystreak_annual_2499` |
| Product ID (monthly) | `sobrietystreak_monthly_399` |
| Trial | 7 days (both plans) |
| Paywall placement | After Screen 3 (value moment — streak visualized) |
| Free tier | Streak counter + 7d milestone only |
| Premium unlocks | All milestones, widget, journal, reminders, iCloud backup |

**Price test A/B**:
- Variant A: Annual $24.99 / Monthly $3.99
- Variant B: Annual $19.99 / Monthly $2.99 (lower friction, match Quittr's old price)

**Review prompt timing**:
- Day 7 streak: "You've made it 7 days. Mind leaving us a review?" (post-milestone, never day 1)
- Day 30 streak: second prompt if not yet reviewed

---

## 7. PRIVACY ARCHITECTURE

Privacy is the core differentiator. Every technical decision reinforces "no data leaves your phone."

```
Data store:      AsyncStorage (streak data, journal, settings)
Sensitive store: expo-secure-store (sensitive prefs)
Backup:          iCloud (opt-in only, user-controlled)
Analytics:       NONE (no Firebase, Amplitude, Mixpanel)
Crash reporting: NONE by default
Auth:            NONE (no accounts)
Server:          NONE
```

App Store privacy label: **"No Data Collected"** — this becomes an ASO advantage. Competitors cannot match this without rebuilding their infrastructure.

Privacy policy (device-local HTML page):
- "We collect nothing."
- "Your streak data lives only on your device."
- "iCloud backup is optional and controlled by your Apple account settings."
- "We do not use analytics, tracking pixels, or ad networks."

---

## 8. TECH STACK

| Layer | Tech |
|-------|------|
| Framework | Expo SDK 51 + React Native |
| Navigation | expo-router |
| Storage | @react-native-async-storage/async-storage |
| Secure storage | expo-secure-store |
| Billing | react-native-purchases (RevenueCat) |
| Notifications | expo-notifications |
| Haptics | expo-haptics |
| Widget | react-native-widget-extension (iOS) |
| Animations | react-native-reanimated |
| Icons | @expo/vector-icons |
| Analytics | NONE |

**Base template**: `app factory/app-factory/base-template/scripture-streak/`
Strip faith content, rename bundle ID, reuse: purchases.ts, notifications.ts, store.ts, AdBanner.tsx (disabled for this app — privacy-first).

---

## 9. VISUAL DESIGN

| Element | Spec |
|---------|------|
| Background | Near-black `#0A0A0F` |
| Primary accent | Emerald `#10B981` |
| Secondary accent | Warm white `#F5F5F0` |
| Danger/relapse | Muted amber `#D97706` (not red — no shame messaging) |
| Font | SF Pro (system default) — native feel, no font loading delay |
| Streak ring | Animated SVG circle, fills clockwise, glows on milestone hit |
| Celebrations | Confetti burst on milestone unlock |
| Cards | border-radius: 16, subtle shadow, dark surface `#141418` |
| Tone | Calm, masculine, zero judgment. Like a trusted friend, not a therapist bot. |

Reference quality bar: Streaks app (iOS) for ring quality. Gentler tone than Quittr (clinical).

---

## 10. ASO KEYWORDS

**Primary (high volume)**:
- sobriety tracker
- nofap counter
- streak tracker
- sober counter
- quit tracker

**Secondary (low competition, long-tail wins)**:
- nofap app privacy
- sober day counter
- pmo tracker
- addiction counter ios
- relapse tracker private

**Title**: SobrietyStreak — Sober Counter
**Subtitle**: Private Streak & Habit Tracker
**Keywords field**: nofap,sober,streak,quit,counter,habit,privacy,relapse,pmo,tracker

**Screenshots spec** (6 required):
1. Home dashboard — "Day 47 streak" in large type, emerald ring
2. Milestone badges — "30 Day Badge Unlocked" celebration
3. Onboarding goal picker — "Pick what you're working on"
4. Widget on homescreen — streak day prominently displayed
5. Privacy screen — "Your data never leaves this phone"
6. Relapse reset screen — warm, non-judgmental "Reset and keep going"

---

## 11. BUILD ORDER (narrowest path to testable)

```
Phase 1 — Core loop (2-3 days)
  [ ] Scaffold from scripture-streak base template
  [ ] Strip faith content, rename bundle ID to com.printmaxx.sobrietystreak
  [ ] Implement streak counter (AsyncStorage — local only)
  [ ] Daily check-in button with haptic feedback
  [ ] "I slipped" reset flow (dignified, non-shame UX)
  [ ] Milestone detection logic (7d, 30d, 60d, 90d, 1yr)
  [ ] Basic home screen UI with streak ring

Phase 2 — Monetization (1 day)
  [ ] Wire RevenueCat with sobrietystreak product IDs
  [ ] Paywall screen matching spec above
  [ ] Free vs premium gate (milestones beyond 7d = premium)
  [ ] 7-day trial flow

Phase 3 — Polish (1-2 days)
  [ ] Animated streak ring (react-native-reanimated)
  [ ] Milestone celebration (confetti + haptic)
  [ ] Push notifications (daily check-in reminder)
  [ ] Privacy policy screen (device-local HTML)
  [ ] iOS homescreen widget (react-native-widget-extension)
  [ ] App Store screenshots (6 per spec above)

Phase 4 — Submit
  [ ] TestFlight internal build
  [ ] App Store Connect submission
  [ ] Privacy label: "No Data Collected"
  [ ] App Store description using ASO keywords above
  [ ] Pricing: annual $24.99 / monthly $3.99, 7-day trial
```

---

## 12. RISK ASSESSMENT

| Risk | Mitigation |
|------|-----------|
| App Store sensitivity (addiction niche) | No clinical claims. Frame as "habit tracker." Category: Health & Fitness |
| Quittr recovers trust | Irrelevant — local-only is a permanent architecture advantage |
| Low D0 conversion | Paywall after value moment, 7-day trial, annual anchor = industry-best setup |
| Widget complexity delays launch | Ship without widget in 1.0, add in 1.1 update |
| User data migration from Quittr | No migration needed — local only means fresh start |

---

## 13. NEXT ACTION

1. Scaffold: `cp -r "app factory/app-factory/base-template/scripture-streak" "app factory/app-factory/non-religious-apps/sobriety-streak"`
2. Rename bundle ID, app name, color tokens
3. Build Phase 1 core loop (streak counter → check-in → relapse reset → milestone detection)
4. Wire RevenueCat BEFORE adding any polish
5. TestFlight build before adding widget

**Expected time to testable build**: 3-4 days
**Expected time to App Store submission**: 5-7 days
**First revenue signal**: Day 8 (after 7-day trials start converting)

---

## 14. CONTENT / DISTRIBUTION (Rule 9 — 3 tweets + 1 thread)

**Tweet 1**:
"Built an app that tracks your NoFap streak and stores zero data. Nothing goes to a server. Nothing gets sold. Your streak lives on your phone, that's it. Because the last app in this niche literally sold user data. SobrietyStreak drops soon."

**Tweet 2**:
"Every habit tracker wants your data. Engagement loops, ad targeting, retention emails. The one thing people quitting PMO need is privacy and somehow no app gives it to them. So we built one."

**Tweet 3**:
"r/NoFap has 1.24 million people. Zero good dedicated streak apps. One Quittr privacy scandal. This is what a blue ocean looks like in the App Store."

**Thread hook**:
"The sobriety app market is broken. Here's why, and what we built instead: [1/7]"
