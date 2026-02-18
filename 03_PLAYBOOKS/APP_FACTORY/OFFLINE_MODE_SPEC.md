# Offline mode spec for Lock Apps

Built from ALPHA972917 (Reddit user demand: finance, health, privacy, offline-first apps), Day 5 EXECUTION priority EX-05 (score 8.5: "Reddit demand signal: offline capability requested. No competitor has it.").

**Bottom line:** All Lock Apps (PrayerLock, WalkToUnlock, StudyLock, biomaxx) must work without internet. The core value proposition (lock phone until condition met) requires zero server dependency. Offline-first is both a competitive differentiator and a reliability requirement. No competitor does this well.

---

## Why offline mode matters

### User demand signals

1. **Reddit r/nosurf, r/getdisciplined** - Users repeatedly request apps that work in airplane mode (a common distraction-reduction tactic is airplane mode before bed)
2. **App Store reviews of competitors** - Opal, one sec, ScreenZen all have 1-star reviews about failing without connection
3. **Use case alignment** - Someone trying to reduce phone use may intentionally disable wifi/cellular
4. **Geographic reality** - Users in areas with poor connectivity (camping, commuting underground, rural) still need the lock
5. **Privacy-conscious users** - A growing segment wants apps that don't phone home

### Competitive gap

| Competitor | Offline Support | Issue |
|------------|----------------|-------|
| Opal | Partial | Screen time tracking requires connection for sync |
| one sec | No | Server-validated sessions, fails without internet |
| ScreenZen | Partial | Basic blocking works, advanced features don't |
| Flipd | No | Server-dependent lock mechanism |
| Forest | Partial | Tree growing works offline, social features don't |
| **Lock Apps (ours)** | **Full** | **Core lock + tracking + streaks + paywall all offline** |

---

## Architecture: offline-first

### Design principle

Everything works locally by default. Sync is additive, never required.

```
LOCAL (always works)                 CLOUD (nice-to-have)
├── Lock mechanism                   ├── Cross-device sync
├── Timer/countdown                  ├── Leaderboards
├── Streak tracking                  ├── Cloud backup
├── Prayer/step/study progress       ├── Social sharing
├── Paywall state (cached)           ├── Remote config updates
├── Bible verses (bundled)           ├── Analytics
├── Settings                         ├── Push notification scheduling
└── Emergency unlock                 └── RevenueCat receipt validation
```

### Data storage layer

**AsyncStorage (current implementation, keep):**
- Settings (wake time, duration, haptics, notifications)
- Streak data (current, longest, total minutes)
- Emergency unlock count
- Last completed session timestamp

**Add: SQLite via expo-sqlite (for structured history):**
```
Table: sessions
- id: INTEGER PRIMARY KEY
- type: TEXT (prayer|walk|study|bio)
- started_at: TEXT (ISO 8601)
- completed_at: TEXT (ISO 8601)
- duration_seconds: INTEGER
- condition_met: BOOLEAN (prayer finished, steps reached, study time done)
- synced: BOOLEAN (false until cloud sync succeeds)
- app_version: TEXT

Table: streaks
- id: INTEGER PRIMARY KEY
- date: TEXT (YYYY-MM-DD)
- completed: BOOLEAN
- type: TEXT
- synced: BOOLEAN

Table: subscription_cache
- product_id: TEXT PRIMARY KEY
- is_active: BOOLEAN
- expires_at: TEXT
- last_verified_at: TEXT
- receipt_data: TEXT (encrypted)
```

### Offline paywall handling

This is the critical edge case. RevenueCat needs internet to verify purchases. Solution:

```
PURCHASE FLOW (online):
1. User taps "Subscribe" → RevenueCat processes payment
2. On success → cache subscription state locally
3. Store: product_id, is_active=true, expires_at, receipt_data
4. Set local flag: user_is_premium = true

VERIFICATION (offline):
1. App launches → check local subscription_cache
2. If is_active = true AND expires_at > now → grant premium
3. If expires_at < now → check grace period (7 days)
4. If grace period expired → revert to free (prompt to go online)
5. When internet returns → validate with RevenueCat → update cache

GRACE PERIOD LOGIC:
- Subscription expired + no internet: 7-day grace period
- Grace period keeps premium active offline
- After 7 days offline past expiry: downgrade to free
- Reason: prevents abuse (cancel then go offline forever)
  but generous enough for camping trips and connectivity gaps
```

**RevenueCat offline handling code (React Native):**

```typescript
// subscription_cache.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

const CACHE_KEY = 'subscription_cache';
const GRACE_PERIOD_DAYS = 7;

interface SubscriptionCache {
  isActive: boolean;
  productId: string;
  expiresAt: string;
  lastVerifiedAt: string;
  gracePeriodEnd: string;
}

export async function checkSubscriptionOffline(): Promise<boolean> {
  const cached = await AsyncStorage.getItem(CACHE_KEY);
  if (!cached) return false;

  const sub: SubscriptionCache = JSON.parse(cached);
  const now = new Date();
  const expires = new Date(sub.expiresAt);
  const graceEnd = new Date(sub.gracePeriodEnd);

  // Active and not expired
  if (sub.isActive && expires > now) return true;

  // Expired but within grace period
  if (sub.isActive && graceEnd > now) return true;

  // Past grace period
  return false;
}

export async function cacheSubscription(
  productId: string,
  isActive: boolean,
  expiresAt: Date
): Promise<void> {
  const gracePeriodEnd = new Date(expiresAt);
  gracePeriodEnd.setDate(gracePeriodEnd.getDate() + GRACE_PERIOD_DAYS);

  const cache: SubscriptionCache = {
    isActive,
    productId,
    expiresAt: expiresAt.toISOString(),
    lastVerifiedAt: new Date().toISOString(),
    gracePeriodEnd: gracePeriodEnd.toISOString(),
  };

  await AsyncStorage.setItem(CACHE_KEY, JSON.stringify(cache));
}
```

### Offline content bundles

Each app bundles its content locally. No API calls for core functionality.

**PrayerLock:**
```
Bundled assets (ship with app):
- 365 Bible verses (JSON, ~50KB)
- 52 weekly prayer prompts (JSON, ~15KB)
- 30 prayer timer sounds (compressed audio, ~2MB)
- Salah prayer times calculation (offline algorithm, not API)
  → Aladhan calculation method (no internet needed)
  → Uses device GPS for Qibla direction
  → Prayer times computed from lat/long + date
```

**WalkToUnlock:**
```
Bundled assets:
- Step counter uses device accelerometer (no API)
- Health data from HealthKit (iOS) / Health Connect (Android)
- 30 motivational walk prompts (JSON, ~10KB)
- Route maps: NOT bundled (optional, requires connection)
  → Graceful fallback: show step count without map
```

**StudyLock:**
```
Bundled assets:
- Pomodoro timer logic (all local)
- 20 study session templates (JSON, ~8KB)
- Subject tracking (local SQLite)
- Focus sounds (compressed audio, ~2MB)
```

**biomaxx:**
```
Bundled assets:
- Supplement database (JSON, ~100KB)
- Daily protocol templates (JSON, ~30KB)
- Progress tracking (local SQLite)
- Biometric baselines (local storage)
```

---

## Implementation per app

### Phase 1: Core offline (all apps, 2-3 days dev)

Changes to existing code:

1. **Add network state detection:**
```typescript
// useNetworkState.ts
import NetInfo from '@react-native-community/netinfo';
import { useEffect, useState } from 'react';

export function useNetworkState() {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected ?? false);
    });
    return unsubscribe;
  }, []);

  return { isConnected };
}
```

2. **Add sync queue for when connection returns:**
```typescript
// syncQueue.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

const QUEUE_KEY = 'sync_queue';

interface SyncItem {
  type: 'session' | 'streak' | 'analytics';
  data: Record<string, unknown>;
  createdAt: string;
}

export async function queueForSync(item: SyncItem): Promise<void> {
  const queue = await getQueue();
  queue.push(item);
  await AsyncStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

export async function getQueue(): Promise<SyncItem[]> {
  const raw = await AsyncStorage.getItem(QUEUE_KEY);
  return raw ? JSON.parse(raw) : [];
}

export async function processQueue(): Promise<void> {
  const queue = await getQueue();
  const failed: SyncItem[] = [];

  for (const item of queue) {
    try {
      await syncItem(item);
    } catch {
      failed.push(item);
    }
  }

  await AsyncStorage.setItem(QUEUE_KEY, JSON.stringify(failed));
}

async function syncItem(item: SyncItem): Promise<void> {
  // Send to analytics, cloud backup, etc.
  // Implement per item.type
}
```

3. **Modify paywall to cache state locally** (see code above)

4. **Bundle content JSON files** into app assets

### Phase 2: Sync layer (nice-to-have, Week 2+)

- Cloud backup of session history (Firebase/Supabase)
- Cross-device streak sync
- Social leaderboards (only when connected)
- Remote config for A/B tests (fallback to local defaults)

### Phase 3: Offline-specific features (differentiation)

These features only make sense offline:

1. **Airplane Mode Challenge:** "Go 24 hours in airplane mode. Track your streak."
   - Actually incentivizes being offline
   - Unique to our apps (competitors break in airplane mode)
   - Social proof: "I survived 24h offline" sharable card

2. **Offline Focus Score:** Track how much time spent offline vs online
   - Gamification of disconnection
   - Daily/weekly/monthly scores
   - Aligns with digital minimalism megatrend (ALPHA972897)

3. **Cache-Forward Downloads:** When connected, pre-download tomorrow's content
   - Bible verse of the day (PrayerLock)
   - Tomorrow's workout prompt (WalkToUnlock)
   - Study schedule for next session (StudyLock)
   - Protocol updates (biomaxx)

---

## Testing checklist

### Offline scenario tests

| Scenario | Expected Behavior | Test Method |
|----------|-------------------|-------------|
| App launch with no internet | Lock screen appears, timer works, streaks show | Airplane mode |
| Complete session offline | Session saved locally, syncs when connected | Airplane mode + complete |
| Subscription active, go offline | Premium features work for 7+ days | Disconnect after purchase |
| Subscription expired, offline | Grace period (7 days), then downgrade | Set device clock forward |
| Week of data offline, reconnect | All sessions sync, no data loss | Extended airplane mode |
| Purchase attempt offline | Clear error: "Connect to subscribe" | Airplane mode + tap subscribe |
| Emergency unlock offline | Works (fully local mechanism) | Airplane mode + triple tap |
| PrayerLock Salah mode offline | Prayer times computed locally from GPS + date | Airplane mode + check times |

### Performance targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Offline app launch | <1 second | No network calls blocking startup |
| Offline session start | <200ms | Local only |
| Storage per 1 year sessions | <5MB | SQLite + JSON efficient |
| Sync after reconnect | <5 seconds for 100 sessions | Batch upload |
| Battery impact of offline mode | Zero additional drain | No background network polling |

---

## Dependencies to add

```json
{
  "@react-native-community/netinfo": "^11.x",
  "expo-sqlite": "~14.x"
}
```

**Do NOT add** SQLite if AsyncStorage is sufficient for current data volume. Only add when session history exceeds what AsyncStorage handles well (~2MB practical limit).

For launch: AsyncStorage is enough. SQLite is a Phase 2 optimization.

---

## Marketing angle

Offline mode is a marketing differentiator, not just a technical feature.

**App Store description bullets:**
- "Works in airplane mode. Your phone lock doesn't need wifi."
- "Your data stays on your device. No cloud. No tracking."
- "Built for anywhere: camping, commuting, or just unplugging."

**Social post angle:**
```
most phone-blocking apps stop working in airplane mode.

that's like a gym that closes when it rains.

our lock works everywhere: airplane mode, underground,
no signal, camping. your phone stays locked until you
[pray/walk/study]. no internet required.

because the whole point is using your phone less.
why would that need wifi?
```

**ASO keywords to target:**
- "offline phone blocker"
- "phone lock no internet"
- "airplane mode app blocker"
- "screen time app offline"
- "focus app without wifi"

---

## Cross-pollination

| Method | Offline Mode Integration |
|--------|------------------------|
| CONTENT_FARM | "Works in airplane mode" as viral hook. Competitor comparison content. |
| COLD_EMAIL | Selling offline capability to businesses (employee phone management) |
| DIGITAL_PRODUCTS | "Building Offline-First Apps" Gumroad guide ($17) |
| NEWSLETTER | "Why your phone blocker needs airplane mode" article angle |
| PMax ADS | "Works without wifi" as ad headline variant |
| APP_STORE | ASO keyword targeting for "offline phone blocker" |

---

## Implementation priority

| Task | Priority | Effort | Impact |
|------|----------|--------|--------|
| Bundle Bible verses JSON (PrayerLock) | HIGH | 1 hour | Core functionality offline |
| Cache subscription state locally | HIGH | 2 hours | Premium works offline |
| Add network state detection | HIGH | 30 min | UX (show online/offline indicator) |
| Sync queue for reconnection | MEDIUM | 2 hours | No data loss |
| Offline Salah prayer time calculation | MEDIUM | 3 hours | PrayerLock Salah mode works offline |
| SQLite session history | LOW | 4 hours | Only if AsyncStorage limit hit |
| Airplane Mode Challenge feature | LOW | 6 hours | Differentiation, gamification |
| Cloud backup sync layer | LOW | 8 hours | Nice-to-have, not blocking launch |

**Total for launch-blocking offline features: ~5.5 hours dev time.**
**Everything else is post-launch enhancement.**
