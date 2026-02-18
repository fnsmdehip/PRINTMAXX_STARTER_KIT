# PrayerLock Muslim Salah Mode - Implementation Spec

**Created:** 2026-02-03
**Priority:** 9.5 (multi-faith = 3B TAM with minimal engineering)
**Build Time:** 3-5 days from current codebase
**MEGA_RALPH:** EX-03 Day 4 Iteration 13

---

## The Opportunity

PrayerLock is Christian-only. 2.4B Christians worldwide. Adding Muslim Salah mode adds 2B Muslims. Same app, same core mechanism (phone locks until you pray), 83% larger addressable market.

Muslim prayer is BETTER for this app than Christian prayer:
- 5 mandatory daily prayers (Fajr, Dhuhr, Asr, Maghrib, Isha)
- Fixed time windows (based on sun position)
- Missing a prayer = religiously significant
- Phone addiction during prayer times = common complaint in Muslim communities
- r/islam and r/MuslimLounge regularly discuss phone addiction during Salah

**Zero direct competitors** lock phones for Salah. Existing apps: Muslim Pro (200M downloads, content/azan only), Athan (azan/qibla only), MyDuaa (dua tracking only). None enforce behavior.

---

## Architecture Changes

### 1. Faith Selector (Onboarding)

Add faith selection as FIRST onboarding screen (before prayer duration picker).

```typescript
// New type in AppContext.tsx
type FaithType = 'christianity' | 'islam' | 'hinduism' | 'general';

// Add to UserSettings interface
interface UserSettings {
  // ... existing fields
  faith: FaithType;
  salahSettings?: {
    calculationMethod: 'MWL' | 'ISNA' | 'Egypt' | 'Makkah' | 'Karachi';
    madhab: 'Shafi' | 'Hanafi';
    fajrEnabled: boolean;
    dhuhrEnabled: boolean;
    asrEnabled: boolean;
    maghribEnabled: boolean;
    ishaEnabled: boolean;
    lockWindowMinutes: number; // how long before/after adhan to lock (default: 30)
  };
}
```

**UI:** Simple faith selector with icons:
- Cross icon: Christianity
- Crescent icon: Islam
- Om icon: Hinduism (future)
- Heart icon: General/Non-denominational

Default: Christianity (matches current v1 users).

### 2. Salah Times Integration

**API:** Aladhan API (free, no key required, reliable)
- Endpoint: `https://api.aladhan.com/v1/timingsByCity`
- Parameters: city, country, method (calculation), school (madhab)
- Returns: Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha times for any location

**Implementation:**

```typescript
// New file: src/services/salahTimes.ts

interface SalahTimes {
  fajr: string;    // "05:23"
  sunrise: string; // "06:45"
  dhuhr: string;   // "12:15"
  asr: string;     // "15:30"
  maghrib: string; // "17:45"
  isha: string;    // "19:15"
}

// Fetch daily, cache in AsyncStorage
// Recalculate on location change
// Offline fallback: use last cached times
```

**Calculation Methods:**
| Method | Region | Code |
|--------|--------|------|
| Muslim World League | Europe, Americas | MWL |
| ISNA | North America | ISNA |
| Egyptian General Authority | Africa, Middle East | Egypt |
| Umm Al-Qura, Makkah | Saudi Arabia | Makkah |
| University of Islamic Sciences, Karachi | South Asia | Karachi |

Default: Auto-detect by location. ISNA for US, MWL for Europe, Makkah for Middle East.

### 3. Lock Window Logic

**Christian mode (existing):** Lock phone once per day until user completes prayer session of chosen duration (5-30 min).

**Muslim Salah mode (new):** Lock phone 5 times per day at each Salah time window.

```
Lock activation logic:
1. Salah time arrives (e.g., Dhuhr at 12:15)
2. Phone locks X minutes before adhan (configurable, default 0)
3. Phone stays locked until:
   a. User taps "Start Prayer" and completes minimum duration (default 5 min)
   b. OR lock window expires (configurable, default 30 min after adhan)
4. If lock window expires without prayer: mark as MISSED, increment shame counter
5. Next Salah: cycle repeats
```

**Lock duration per Salah:**
| Salah | Typical Duration | Default Lock Min |
|-------|-----------------|------------------|
| Fajr | 2-4 min (2 rakat) | 3 min |
| Dhuhr | 5-8 min (4 rakat) | 5 min |
| Asr | 5-8 min (4 rakat) | 5 min |
| Maghrib | 3-5 min (3 rakat) | 4 min |
| Isha | 5-10 min (4 rakat + witr) | 6 min |

Users can customize all durations.

### 4. Content Data

**New file: src/data/quran_verses.json**

Structure matches existing verses.json pattern:

```json
[
  {
    "id": 1,
    "text": "Indeed, prayer prohibits immorality and wrongdoing.",
    "reference": "Quran 29:45",
    "arabic": "إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ",
    "transliteration": "Inna as-salata tanha ani al-fahsha'i wal-munkar"
  }
]
```

**Include 30 Quranic verses about:**
- Prayer (Salah) importance
- Patience and discipline
- Phone/distraction resistance (modern interpretation)
- Remembrance of Allah (dhikr)

**Source:** Quran.com API or static JSON (30 verses, curated for relevance).

**Display:** Show English translation + Arabic text + reference. Arabic renders right-to-left.

### 5. UI Changes

**Minimal changes needed. Most screens work across faiths.**

| Screen | Christian Mode | Muslim Salah Mode | Change Required |
|--------|---------------|-------------------|-----------------|
| HomeScreen | Daily streak, verse, timer | 5 prayer tracker, verse, next Salah | Moderate - add SalahTracker component |
| TimerScreen | Single prayer timer | Per-Salah timer with rakat count | Minor - pass Salah name + duration |
| LockScreen | "Pray First, Phone Second" | "Salah Time, Phone Locked" | Minor - conditional text |
| SettingsScreen | Duration, blocked apps | Salah times config, calculation method, blocked apps | Moderate - add Salah settings section |
| PaywallScreen | Same | Same | None |

**New Components:**

1. **SalahTracker** (HomeScreen widget)
   - Shows 5 circles for each Salah
   - Green = completed, Gray = upcoming, Red = missed
   - Current Salah highlighted with countdown to next prayer time
   - Tap = start that Salah's prayer timer

2. **FaithSelector** (Onboarding screen)
   - 4 faith options with icons
   - Clean, respectful design
   - Selecting Islam shows Salah configuration (method, madhab)

3. **QiblaCompass** (optional premium feature)
   - Shows direction to Makkah using device compass
   - Premium upsell opportunity

### 6. Localization Strings

```typescript
// src/constants/strings.ts

const STRINGS = {
  christianity: {
    lockMessage: 'Pray First, Phone Second',
    timerLabel: 'Prayer Time',
    streakLabel: 'Prayer Streak',
    completionMessage: 'Prayer complete. God bless your day.',
    emergencyLabel: 'Skip Prayer (breaks streak)',
  },
  islam: {
    lockMessage: 'Salah Time. Phone Locked.',
    timerLabel: (salah: string) => `${salah} Prayer`,
    streakLabel: 'Salah Streak',
    completionMessage: (salah: string) => `${salah} complete. May Allah accept your prayer.`,
    emergencyLabel: 'Skip Salah (marks as missed)',
    prayerNames: {
      fajr: 'Fajr',
      dhuhr: 'Dhuhr',
      asr: 'Asr',
      maghrib: 'Maghrib',
      isha: 'Isha',
    },
  },
};
```

### 7. Streak Tracking Updates

**Christian mode:** 1 prayer per day = streak maintained.

**Muslim Salah mode:** Configurable threshold:
- Strict: 5/5 Salah = streak maintained
- Moderate (default): 3/5 Salah = streak maintained
- Lenient: 1/5 Salah = streak maintained

```typescript
interface SalahStreakData extends StreakData {
  dailySalahCompleted: {
    fajr: boolean;
    dhuhr: boolean;
    asr: boolean;
    maghrib: boolean;
    isha: boolean;
  };
  totalSalahCompleted: number; // lifetime count
  totalSalahMissed: number;   // lifetime count
  streakThreshold: 'strict' | 'moderate' | 'lenient';
}
```

---

## Implementation Plan

### Phase 1: Data Layer (Day 1)
- [ ] Add `FaithType` and `salahSettings` to AppContext
- [ ] Create `src/services/salahTimes.ts` (Aladhan API integration)
- [ ] Create `src/data/quran_verses.json` (30 curated verses)
- [ ] Update `src/utils/storage.ts` for faith-specific data persistence
- [ ] Add localization strings

### Phase 2: UI Components (Day 2)
- [ ] Build FaithSelector onboarding screen
- [ ] Build SalahTracker component (5-prayer dashboard widget)
- [ ] Update HomeScreen to conditionally render SalahTracker vs single prayer
- [ ] Update LockScreen text for Muslim mode
- [ ] Update TimerScreen to accept Salah name + duration

### Phase 3: Lock Logic (Day 3)
- [ ] Implement 5x daily lock trigger based on Salah times
- [ ] Add lock window expiration logic
- [ ] Update streak calculation for Salah threshold
- [ ] Add missed prayer tracking
- [ ] Notification scheduling for each Salah time

### Phase 4: Settings + Polish (Day 4)
- [ ] Add Salah settings section (calculation method, madhab, enabled prayers)
- [ ] Location detection for auto Salah times
- [ ] Arabic text rendering (RTL support for verse display)
- [ ] QiblaCompass component (premium feature)
- [ ] Edge cases: Ramadan times, travel mode, DST changes

### Phase 5: Testing (Day 5)
- [ ] Test all 5 calculation methods with known cities
- [ ] Test offline fallback (cached times)
- [ ] Test streak logic with all 3 thresholds
- [ ] Test lock/unlock cycle for each Salah
- [ ] Test Arabic text rendering on various devices

---

## Revenue Impact

**Current:** Christian-only PrayerLock targets 2.4B Christians.

**With Salah mode:** Adds 2B Muslims. 83% TAM increase.

**Muslim-specific monetization:**
- Ramadan premium features (extended night prayers, Taraweeh tracking)
- Hajj/Umrah prayer mode (special prayers at holy sites)
- QiblaCompass (premium feature)
- Islamic calendar integration (prayer adjustments for special days)

**Pricing unchanged:** $4.99/mo or $29.99/yr. Same hard paywall. Same trial.

**Distribution:**
- r/islam (1.2M members), r/MuslimLounge (200K), r/Hijabis (120K)
- Muslim TikTok (#muslimtiktok 24B views)
- Islamic podcast sponsorships
- Muslim student associations (MSAs) at universities
- Ramadan launch timing (March 2026 = peak Muslim app installs)

---

## Competitive Moat

| App | What It Does | Phone Lock? | Multi-Faith? |
|-----|-------------|-------------|-------------|
| Muslim Pro | Azan, Quran, prayer times | No | Muslim only |
| Athan | Azan, qibla | No | Muslim only |
| Hallow | Guided meditation, content | No | Christian only |
| Pray.com | Audio prayers, podcasts | No | Multi-faith (content) |
| **PrayerLock** | **Locks phone until you pray** | **Yes** | **Yes (Christian + Muslim)** |

PrayerLock is the ONLY app that:
1. Locks the phone (behavior enforcement, not just reminders)
2. Supports multiple faiths
3. Has a shame counter (emergency unlock tracking)
4. Tracks prayer streaks across faith traditions

---

## App Store Considerations

**Keyword expansion:**
- Add: "salah timer", "prayer lock muslim", "islamic prayer app", "namaz reminder"
- Multi-faith positioning in description: "For Christians, Muslims, and anyone building a daily prayer habit"

**Screenshots:**
- Add Salah tracker screenshot (5 prayer circles)
- Add Arabic verse display screenshot
- Keep Christian screenshots (different localization)

**Age rating:** No change needed. Prayer content is suitable for all ages.

**Regional focus:** US, UK, Canada, UAE, Saudi Arabia, Indonesia, Pakistan, Malaysia, Turkey.

---

## Cross-Pollination

- **Content farm:** Muslim prayer content for TikTok/Reels (#muslimtiktok 24B views)
- **Newsletter:** Faith Forward newsletter covers Muslim prayer topics
- **Reddit:** r/islam posts about phone addiction during Salah (genuine value-first)
- **Info product:** "Building a Daily Salah Habit" guide ($7 Gumroad)
- **High-ticket:** "Muslim community app customization" service ($2K)

---

## Hindu Mode (Future - Phase 2)

Quick notes for next expansion:
- Puja timing (morning + evening)
- Sanskrit shloka verses
- Festival calendar integration (Diwali, Navratri, etc.)
- 1.2B Hindus = another major TAM expansion
- r/hinduism (350K members)

Build the multi-faith infrastructure now (faith selector, verse system, localized strings) and Hindu mode becomes a 2-day add.
