# PrayerLock Muslim Salah Mode Spec

**Created:** 2026-02-02 (MEGA RALPH Day 3, Iteration 13, EX-03)
**Task ID:** MEGA_061
**Status:** SPEC READY (not yet implemented)
**Priority:** 9.5 (1.8B Muslims, zero behavior enforcement competitors)

---

## Why this matters

PrayerLock currently serves Christians only. Bible verses. Single prayer time. The Muslim market is:

- 1.8 billion Muslims worldwide
- 5 mandatory prayers per day (Fajr, Dhuhr, Asr, Maghrib, Isha)
- Zero apps that LOCK the phone until prayer is complete
- Muslim Pro (top competitor) has 120M+ downloads but is content-only (reminders, Quran, no enforcement)
- Hallow ($51.4M/yr revenue) proved faith apps can scale, but serves Christians only
- Spiritual wellness market: $2.16B (2024) to $7.31B by 2033 at 14.6% CAGR

Muslim users need PrayerLock MORE than Christians. 5 prayers per day vs 1-2. the accountability gap is 5x larger.

**The Lock App thesis applies perfectly:** Muslim prayer apps remind. PrayerLock locks. you don't unlock until you pray. at every salah time. 5 times a day.

---

## Current state of PrayerLock

| Component | Status | Muslim Support |
|-----------|--------|---------------|
| Timer system | complete | works (duration-based, religion-agnostic) |
| Streak tracking | complete | works for daily streaks |
| Emergency unlock | complete | works (typed phrase unlock) |
| Notifications | complete | needs multi-prayer scheduling |
| Scripture reader | complete | Bible only. needs Quran integration |
| Onboarding | complete | needs faith selection screen |
| Settings | complete | needs calculation method + Hanafi/Shafi toggle |
| Paywall | placeholder | works for both faiths |

**Key insight:** 70% of existing code works for Muslims already. the timer, streak, emergency unlock, paywall, and core UI are faith-agnostic. we add a faith selection layer and Muslim-specific features on top.

---

## Architecture: faith selection layer

### Onboarding change

Current onboarding: 4 slides (Welcome, Setup Time, Features, Start Trial)

New onboarding: 5 slides (Welcome, **Select Faith**, Setup Time, Features, Start Trial)

**Slide 2: Select Faith**

```
which tradition do you pray in?

[Christian]     →  current flow (single time, Bible verse)
[Muslim]        →  salah flow (5 prayers, Quran verse, Qibla)
[Hindu]         →  puja flow (morning/evening, mantra) [future]
[Other/General] →  generic flow (custom times, no scripture)
```

Store in userStore: `faithTradition: 'christian' | 'muslim' | 'hindu' | 'general'`

### Muslim-specific onboarding sub-flow

After selecting Muslim:

```
screen 2a: select calculation method
  → auto-detect by country (show recommended)
  → manual override available
  → options: MWL, ISNA, Egyptian, Umm al-Qura, Karachi, Tehran, Jafari

screen 2b: select juristic school for Asr timing
  → Shafi/Maliki/Hanbali (shadow = object height) [default]
  → Hanafi (shadow = 2x object height)

screen 2c: select which prayers to lock
  → [x] Fajr (dawn)
  → [x] Dhuhr (noon)
  → [x] Asr (afternoon)
  → [x] Maghrib (sunset)
  → [x] Isha (night)
  → start with all 5 selected, allow deselect
```

---

## Prayer time calculation

### Primary: Aladhan API (free, no API key needed)

```
GET https://aladhan.com/prayer-times-api/v1/timings/{timestamp}
  ?latitude={lat}
  &longitude={lon}
  &method={method_id}
  &school={0_or_1}
```

**Method IDs:**
| ID | Method | Region |
|----|--------|--------|
| 0 | Jafari (Shia) | Iran, Iraq |
| 1 | Karachi | Pakistan, India, Bangladesh |
| 2 | ISNA | USA, Canada |
| 3 | MWL (Muslim World League) | Europe, Far East |
| 4 | Umm al-Qura | Saudi Arabia |
| 5 | Egyptian General Authority | Africa, Middle East |
| 7 | Tehran | Iran |

**School parameter:**
- 0 = Shafi (shadow = object height) - default
- 1 = Hanafi (shadow = 2x object height)

**Response structure:**
```json
{
  "data": {
    "timings": {
      "Fajr": "05:30",
      "Sunrise": "06:52",
      "Dhuhr": "12:15",
      "Asr": "15:34",
      "Maghrib": "17:38",
      "Isha": "18:58",
      "Midnight": "00:07"
    },
    "date": {
      "hijri": {
        "date": "07-08-1447",
        "month": { "en": "Sha'ban" }
      }
    },
    "meta": {
      "method": { "name": "ISNA" }
    }
  }
}
```

### Offline fallback

Store 30-day prayer time calendar locally (fetched once per month). Calculate locally using PrayTimes.org algorithm if API unreachable. Library: praytimes.js (open source, battle-tested).

### Auto-detection by country

| Country | Recommended Method | Recommended School |
|---------|-------------------|-------------------|
| USA/Canada | ISNA (2) | Shafi (0) |
| UK/Europe | MWL (3) | Shafi (0) |
| Saudi Arabia | Umm al-Qura (4) | Shafi (0) |
| Egypt/Syria/Lebanon | Egyptian (5) | Shafi (0) |
| Pakistan/India/Bangladesh | Karachi (1) | Hanafi (1) |
| Iran | Tehran (7) | Jafari |
| Turkey | MWL (3) | Hanafi (1) |
| Malaysia/Indonesia | MWL (3) | Shafi (0) |

**Implementation:** Use device locale or IP geolocation to auto-detect country. Show recommended method with "change" option.

---

## Lock mechanism (5 prayers per day)

### How the lock works for Salah

```
USER FLOW (example: Dhuhr prayer at 12:15 PM)

12:00 PM  → 15-min advance notification: "Dhuhr in 15 minutes. prepare for salah."
12:15 PM  → phone LOCKS. screen shows:
             "it's Dhuhr time. pray to unlock."
             [Qibla compass arrow]
             [timer: 10:00]
             [emergency unlock]

user prays → taps "I have prayed" after minimum time (5 min default)
           → phone UNLOCKS
           → streak incremented for this prayer

if user doesn't pray:
  → phone stays locked until prayer window closes (Asr time)
  → at window close: phone auto-unlocks, prayer marked MISSED
  → streak broken if any prayer missed in a day
```

### Lock duration per prayer

| Prayer | Default Lock Duration | User Adjustable |
|--------|----------------------|-----------------|
| Fajr | 10 min | 5-30 min |
| Dhuhr | 10 min | 5-30 min |
| Asr | 10 min | 5-30 min |
| Maghrib | 5 min | 5-15 min |
| Isha | 10 min | 5-30 min |

Maghrib shorter because the prayer window between sunset and Isha is shorter.

### Lock timing options

```
settings:

lock trigger: [at exact prayer time] [5 min after] [10 min after] [15 min after]

  → "at exact prayer time" = lock immediately when adhan would be called
  → delay options for users who want a buffer to prepare (wudu, find prayer space)

pre-lock notification: [15 min before] [10 min before] [5 min before] [off]

  → heads-up that lock is coming
```

---

## UI components: Muslim mode

### Home screen (Muslim variant)

```
┌────────────────────────────┐
│  assalamu alaikum, [name]  │
│                            │
│  ┌────────────────────┐    │
│  │ 🔥 14-day streak   │    │
│  │ 5/5 prayers today  │    │
│  └────────────────────┘    │
│                            │
│  NEXT PRAYER               │
│  ┌────────────────────┐    │
│  │ Asr at 3:34 PM     │    │
│  │ locks in 1h 22m    │    │
│  │ ←─── Qibla: 65° NE │    │
│  └────────────────────┘    │
│                            │
│  TODAY'S PRAYERS            │
│  ✅ Fajr    5:30 AM        │
│  ✅ Dhuhr   12:15 PM       │
│  ⏳ Asr     3:34 PM        │
│  ⬜ Maghrib 5:38 PM        │
│  ⬜ Isha    6:58 PM        │
│                            │
│  [open quran] [qibla]      │
└────────────────────────────┘
```

### Lock screen (Muslim variant)

```
┌────────────────────────────┐
│                            │
│     🔒 phone locked        │
│                            │
│     it's Dhuhr time.       │
│     pray to unlock.        │
│                            │
│     ←── Qibla: 65° NE     │
│     (arrow rotates with    │
│      compass heading)      │
│                            │
│     ┌──────────────┐       │
│     │   08:42      │       │
│     │  remaining   │       │
│     └──────────────┘       │
│                            │
│  [i have prayed]           │
│                            │
│  emergency unlock           │
│  (small gray text)          │
└────────────────────────────┘
```

### Qibla compass

Simple compass arrow pointing toward Mecca (21.4225°N, 39.8252°E).

**Calculation:**
```typescript
function calculateQibla(userLat: number, userLon: number): number {
  const meccaLat = 21.4224779 * (Math.PI / 180);
  const meccaLon = 39.8251832 * (Math.PI / 180);
  const lat = userLat * (Math.PI / 180);
  const lon = userLon * (Math.PI / 180);
  const dLon = meccaLon - lon;

  const x = Math.sin(dLon);
  const y = Math.cos(lat) * Math.tan(meccaLat) - Math.sin(lat) * Math.cos(dLon);
  let qibla = Math.atan2(x, y) * (180 / Math.PI);

  return (qibla + 360) % 360; // normalize to 0-360 degrees from North
}
```

Uses `expo-sensors` for device compass heading. Arrow points in Qibla direction relative to phone orientation.

---

## Quran integration (replaces Bible for Muslims)

### Daily verse rotation

Replace `bibleService.ts` with `scriptureService.ts` that serves both:

```typescript
interface ScriptureService {
  getDailyVerse(faith: 'christian' | 'muslim'): {
    text: string;
    reference: string;
    translation?: string;
  };
}
```

**For Muslim users:**
- 30 short Quran verses (one per day, rotating monthly)
- Focus on prayer-related and gratitude verses
- Show Arabic text + English translation
- Source: Quran.com API or embedded static data

**Example verses (curated for prayer context):**

| Day | Surah:Ayah | English |
|-----|-----------|---------|
| 1 | 29:45 | "indeed, prayer prohibits immorality and wrongdoing" |
| 2 | 2:45 | "seek help through patience and prayer" |
| 3 | 20:14 | "establish prayer for my remembrance" |
| 4 | 4:103 | "prayer has been decreed upon the believers at specified times" |
| 5 | 23:1-2 | "successful are the believers who offer prayers with humility" |
| ... | ... | ... |

### Post-prayer reflection

After prayer completion, show:
```
alhamdulillah. prayer complete.

[verse of the day]

"indeed, prayer prohibits immorality and wrongdoing"
- surah al-ankabut 29:45

[continue to phone]
```

---

## Streak system (Muslim variant)

### Daily streak logic

Muslim daily streak = all enabled prayers completed that day.

```
streak rules:
  - if user has Fajr+Dhuhr+Asr+Maghrib+Isha enabled (5)
  - ALL 5 must be completed for day to count toward streak
  - if 4/5 completed: day NOT counted (streak breaks)
  - exception: if user has only 3 prayers enabled, all 3 must be completed

streak display:
  - "5/5 prayers today" (or "4/5 prayers today")
  - current streak: 14 days
  - longest streak: 28 days
  - total prayers: 347
```

### Prayer-level tracking

```typescript
interface DailyPrayerLog {
  date: string; // YYYY-MM-DD
  fajr: { completed: boolean; time?: string; duration?: number };
  dhuhr: { completed: boolean; time?: string; duration?: number };
  asr: { completed: boolean; time?: string; duration?: number };
  maghrib: { completed: boolean; time?: string; duration?: number };
  isha: { completed: boolean; time?: string; duration?: number };
  streakCounted: boolean; // true only if ALL enabled prayers completed
}
```

---

## Notification schedule (5 per day)

```
for each enabled prayer:
  1. pre-lock notification: "{prayer} in {X} minutes. prepare for salah."
     → X = user setting (5/10/15 min before lock)

  2. lock notification: "phone locked. {prayer} time. pray to unlock."
     → triggers lock screen

  3. post-window notification (if missed): "you missed {prayer}. may Allah accept your intention."
     → only if prayer window passed without completion

evening summary (after Isha):
  "today: 4/5 prayers. keep going tomorrow."
```

**Notification respect:**
- silent/do not disturb mode during prayer (no buzzing while praying)
- gentle Adhan-style tone option (short, not full 3-minute call)
- vibration-only mode for work/school

---

## Ramadan mode

### Auto-activation

Detect Ramadan dates from Hijri calendar (Aladhan API returns Hijri dates). Prompt user: "Ramadan starts tomorrow. enable Ramadan mode?"

### Ramadan features

```
1. Suhoor alarm
   → 30 min before Fajr
   → "suhoor time. eat before Fajr."

2. Iftar countdown
   → visible on home screen
   → countdown to Maghrib
   → "iftar in 2h 15m"

3. Taraweeh reminder
   → optional notification after Isha
   → "Taraweeh prayer tonight?"

4. Laylat al-Qadr alerts
   → last 10 nights of Ramadan (odd nights especially)
   → "tonight could be Laylat al-Qadr. increase your worship."

5. Fasting tracker
   → toggle: "fasting today? [yes] [no]"
   → streak for consecutive fast days
```

---

## Jummah (Friday) mode

```
on Fridays:
  → replace Dhuhr lock with Jummah lock
  → earlier lock time (12:00 PM instead of 12:15 PM typical)
  → longer duration (30 min default, includes khutbah)
  → optional: nearby mosque notification
```

---

## Settings (Muslim mode)

```
PRAYER SETTINGS
  calculation method: [ISNA ▼] (auto-detected, changeable)
  juristic school (Asr): [Shafi ▼]
  prayer time adjustment: [0 min] (±1-5 for local mosque sync)

LOCK SETTINGS
  which prayers to lock:
    [x] Fajr    [x] Dhuhr    [x] Asr    [x] Maghrib    [x] Isha
  lock duration per prayer: [10 min ▼] (applies to all, or customize per prayer)
  lock trigger delay: [0 min ▼] (0/5/10/15 after adhan time)
  pre-lock notification: [15 min before ▼]

QURAN
  daily verse: [on ▼]
  show Arabic text: [on ▼]

RAMADAN
  ramadan mode: [auto-detect ▼]
  suhoor alarm: [on ▼]
  iftar countdown: [on ▼]
  taraweeh reminder: [on ▼]

QIBLA
  show on lock screen: [on ▼]
  compass calibration: [calibrate]
```

---

## Implementation plan

### Phase 1: Core Salah Mode (7 days)

| Day | Task | Details |
|-----|------|---------|
| 1 | Faith selection layer | New onboarding slide. userStore.faithTradition field. Conditional routing. |
| 2 | Aladhan API integration | New prayerTimeService.ts. Fetch/cache prayer times. Auto-detect method. |
| 3 | 5-prayer lock schedule | Modify notification service for 5 daily locks. Per-prayer lock screen. |
| 4 | Muslim home screen | Next prayer countdown. Today's 5-prayer checklist. Qibla direction. |
| 5 | Quran integration | scriptureService.ts (replaces bibleService for Muslims). 30 curated verses. |
| 6 | Muslim streak system | Per-prayer tracking. All-or-nothing daily streak. Prayer log history. |
| 7 | Settings + testing | Calculation method, school, per-prayer duration. Full flow testing. |

### Phase 2: Polish (3 days)

| Day | Task | Details |
|-----|------|---------|
| 8 | Qibla compass | expo-sensors magnetometer. Lock screen compass arrow. Calibration. |
| 9 | Ramadan mode | Hijri date detection. Suhoor/Iftar/Taraweeh. Auto-activation prompt. |
| 10 | Jummah + offline | Friday prayer mode. PrayTimes.org local calculation fallback. |

### Phase 3: ASO + Launch (2 days)

| Day | Task | Details |
|-----|------|---------|
| 11 | App Store copy | Muslim-specific screenshots. Dual-listing A/B test (generic vs Muslim-forward). |
| 12 | Submit + content | TestFlight Muslim testers. Reddit r/islam and r/MuslimLounge posts. |

**Total: 12 days** (within one 14-day build cycle)

---

## New files needed

```
src/services/prayerTimeService.ts     → Aladhan API integration, caching, offline fallback
src/services/scriptureService.ts      → Unified verse service (Bible + Quran)
src/services/qiblaService.ts          → Qibla direction calculation
src/stores/salahStore.ts              → Per-prayer completion tracking
app/qibla.tsx                         → Qibla compass screen
```

### Modified files

```
app/_layout.tsx                       → Add faith-based routing
app/onboarding.tsx                    → Add faith selection slide
app/(tabs)/index.tsx                  → Conditional Muslim/Christian home
app/(tabs)/settings.tsx               → Muslim prayer settings section
app/timer.tsx                         → Prayer name display, Qibla on lock
src/stores/userStore.ts               → Add faithTradition, calculationMethod, school
src/services/notificationService.ts   → 5-prayer notification scheduling
```

---

## ASO for Muslim market

### Keywords (separate from Christian listing)

**iOS Keywords (100 chars):**
```
salah,prayer,muslim,islamic,adhan,quran,qibla,ramadan,fajr,lock,accountability,habit,daily
```

**Title options to A/B test:**
- "PrayerLock - Pray to Unlock" (current, generic)
- "PrayerLock - Salah Reminder" (Muslim-forward)
- "PrayerLock - Islamic Prayer Lock" (most explicit)

### Muslim-specific screenshot overlays

1. "phone locked. it's Dhuhr. pray to unlock." (lock screen with Qibla arrow)
2. "5 daily prayers. 5 daily locks." (home screen with prayer checklist)
3. "Fajr ✅ Dhuhr ✅ Asr ✅ Maghrib ⏳ Isha ⬜" (progress view)
4. "47-day salah streak" (streak display)
5. "Ramadan mode: suhoor alarm + iftar countdown" (Ramadan features)
6. "prayer > doomscrolling" (motivational lock screen)

---

## Revenue impact

### Conservative estimate

```
PrayerLock current (Christian only):
  → TAM: 2.4B Christians, but realistic addressable = Gen Z/Millennial English speakers
  → estimated: 50K-200K downloads first year

PrayerLock with Salah mode:
  → adds 1.8B Muslims to TAM
  → Muslim market is MORE underserved (zero behavior enforcement apps)
  → 5 daily prayers = 5x daily engagement (vs 1-2 for Christians)
  → higher retention (daily habit is stronger with 5 touchpoints)
  → estimated: 150K-500K downloads first year

revenue at $4.99/mo, 10% conversion, 50K paying users:
  → $249,500/mo = $3M/yr from ONE app

even at 1% of this:
  → $2,495/mo from PrayerLock alone
```

### Competitive moat

Muslim Pro has 120M+ downloads. they remind. we lock.

if we capture 0.1% of Muslim Pro's user base:
- 120,000 users
- 10% conversion at $4.99/mo
- = $59,880/mo

the lock mechanism is the moat. nobody else does it.

---

## Risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Prayer time inaccuracy | HIGH | use Aladhan API (battle-tested), allow ±5 min adjustment |
| Cultural insensitivity | HIGH | consult Muslim testers, use respectful language, no cartoon imagery |
| App Store rejection (religious) | MEDIUM | position as "productivity" not "religious obligation" |
| Compass accuracy | MEDIUM | calibration screen, "point phone North to calibrate" |
| Ramadan date disputes | LOW | support multiple Hijri calendars, allow manual date override |
| High-latitude prayer times | LOW | offer "nearest latitude" method option |

### Cultural sensitivity notes

- use "salah" not "namaz" (Arabic is universal, "namaz" is Urdu/Turkish specific)
- Quran verses: use Sahih International translation (widely accepted)
- no images of prophets, no images of the Kaaba in mockup style
- green color associated with Islam (consider green accent for Muslim mode)
- respect: "may Allah accept your prayers" not "great job praying!"
- the app does NOT claim to replace mosque attendance for Jummah

---

## QA checklist

- [ ] Prayer times match Aladhan API (within 1 minute)
- [ ] Qibla direction accurate (within 5 degrees, tested 5+ locations)
- [ ] All 5 prayer locks trigger at correct times
- [ ] Streak resets correctly when ANY prayer missed
- [ ] Ramadan mode activates on correct Hijri dates
- [ ] Jummah replaces Dhuhr on Fridays
- [ ] Offline fallback calculates prayer times correctly
- [ ] Muslim onboarding flow completes without errors
- [ ] Quran verses display Arabic + English correctly
- [ ] RTL text rendering for Arabic (if applicable)
- [ ] Emergency unlock still works during prayer lock
- [ ] Notification scheduling handles timezone changes
- [ ] Settings persist across app restarts (calculation method, school)
- [ ] Cross-faith: switching between Christian and Muslim modes works
