# APP FACTORY - Build Issues to Fix

**Priority:** CRITICAL - Blocks testing and App Store submission
**Updated:** 2026-01-21

---

## Summary

4 apps have blocking issues that prevent builds from succeeding:
- **3 apps missing main entry point** (crashes on launch)
- **1 app with non-standard structure** (navigation issues)

---

## Issue #1: DailyAnchor - Missing Entry Point

**Severity:** 🔴 CRITICAL
**Location:** `/MONEY_METHODS/APP_FACTORY/builds/dailyanchor`
**Error:** App will crash - no main component

### Problem
```
✓ app/_layout.tsx exists (navigation wrapper)
✗ app/index.tsx MISSING (main screen)
✗ app.tsx NOT FOUND
```

### Impact
- App won't launch
- Expo build will fail
- Can't test or submit

### Solution
Create `app/index.tsx` with basic devotion screen:

```typescript
// app/index.tsx
import { View, Text, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#F8FAFC' }}>
      <ScrollView contentContainerStyle={{ flexGrow: 1, padding: 16 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>
          Daily Anchor
        </Text>
        <Text style={{ fontSize: 16, color: '#666', lineHeight: 24 }}>
          Your daily devotional. Start your day with Scripture and reflection.
        </Text>
        {/* Add devotion content here */}
      </ScrollView>
    </SafeAreaView>
  );
}
```

**Estimated Time:** 30 minutes
**Ref Pattern:** Use `focusprayer/app/index.tsx` or `biomaxx/app/index.tsx` as template

---

## Issue #2: DevotionFlow - Missing Entry Point

**Severity:** 🔴 CRITICAL
**Location:** `/MONEY_METHODS/APP_FACTORY/builds/devotionflow`
**Error:** App will crash - no main component

### Problem
```
✓ app/_layout.tsx exists (navigation wrapper)
✗ app/index.tsx MISSING (main screen)
✗ app.tsx NOT FOUND
```

### Impact
- App won't launch
- Expo build will fail
- Can't test or submit

### Solution
Create `app/index.tsx` with devotion flow screen:

```typescript
// app/index.tsx
import { View, Text, ScrollView, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#F5F0E8' }}>
      <ScrollView contentContainerStyle={{ flexGrow: 1, padding: 16 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>
          DevotionFlow
        </Text>
        <Text style={{ fontSize: 16, color: '#666', marginBottom: 24 }}>
          Follow your devotion journey. Scripture, reflection, and growth.
        </Text>

        <Pressable style={{ backgroundColor: '#4F46E5', padding: 12, borderRadius: 8 }}>
          <Text style={{ color: 'white', fontSize: 16, fontWeight: 'bold' }}>
            Start Today's Devotion
          </Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}
```

**Estimated Time:** 30 minutes
**Ref Pattern:** Use `focusprayer/app/index.tsx` as template

---

## Issue #3: PelvicPro - Missing Entry Point + Documentation

**Severity:** 🔴 CRITICAL
**Location:** `/MONEY_METHODS/APP_FACTORY/builds/pelvicpro`
**Error:** App will crash - no main component + zero documentation

### Problem
```
✓ app/_layout.tsx exists (navigation wrapper)
✗ app/index.tsx MISSING (main screen)
✗ app.tsx NOT FOUND
✗ README.md NOT FOUND
```

### Impact
- App won't launch
- Expo build will fail
- No development guidance
- Can't submit to App Store

### Solution

**Step 1: Create entry point** - `app/index.tsx`
```typescript
// app/index.tsx
import { View, Text, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#FFF9F5' }}>
      <ScrollView contentContainerStyle={{ flexGrow: 1, padding: 16 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>
          PelvicPro
        </Text>
        <Text style={{ fontSize: 16, color: '#666', lineHeight: 24 }}>
          Your personal pelvic floor wellness companion. Track exercises, progress, and health insights.
        </Text>
        {/* Add health tracking UI here */}
      </ScrollView>
    </SafeAreaView>
  );
}
```

**Step 2: Create README.md**
```markdown
# PelvicPro - Pelvic Floor & Women's Health App

Women's health app focused on pelvic floor exercises, wellness tracking, and health insights.

## Features
- Guided pelvic floor exercises
- Daily workout logging
- Progress tracking
- Health metrics dashboard
- Personalized recommendations

## Tech Stack
- React Native (Expo)
- TypeScript
- NativeWind (Tailwind CSS)
```

**Step 3: Create COMPETITIVE_ANALYSIS.md**
Reference: Kegel training apps, Elvie, Perifit

**Estimated Time:** 1.5 hours total

---

## Issue #4: PromptVault - Non-Standard Structure

**Severity:** 🟡 MEDIUM
**Location:** `/MONEY_METHODS/APP_FACTORY/builds/promptvault`
**Error:** Non-standard React Native structure (app.tsx instead of _layout.tsx + index.tsx)

### Problem
```
✓ app.json exists
✓ app.tsx EXISTS (non-standard)
✗ app/_layout.tsx MISSING (standard navigation)
✗ app/index.tsx NOT FOUND (standard entry)
```

### Impact
- Navigation may not work properly
- Stack navigator not configured
- Tab navigation may be broken
- Inconsistent with other apps

### Solution

**Option A: Verify current structure works (recommended first)**
```bash
cd /MONEY_METHODS/APP_FACTORY/builds/promptvault
npm run build
# If successful, structure is fine - skip rest
```

**Option B: If build fails, refactor to standard structure**

Create proper _layout.tsx:
```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: true,
        headerStyle: {
          backgroundColor: '#1a1a2e',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Stack.Screen name="index" />
    </Stack>
  );
}
```

Then move content from app.tsx to app/index.tsx:
```bash
mv app/app.tsx app/index.tsx
# Update imports if needed
```

**Estimated Time:** 30 minutes if refactor needed (or 0 if current structure works)

---

## Verification Checklist

After fixing each app:

```bash
# For DailyAnchor, DevotionFlow, PelvicPro:
cd /MONEY_METHODS/APP_FACTORY/builds/{app_name}

# 1. Verify entry point exists
[ -f app/index.tsx ] && echo "✓ Entry point exists" || echo "✗ MISSING"

# 2. Try to build
npm run build
# Should succeed or show clear TypeScript errors (not missing file errors)

# 3. Verify no 404s for app files
[ -f app.json ] && echo "✓ app.json" || echo "✗"
[ -f app/_layout.tsx ] && echo "✓ Layout" || echo "✗"
[ -f app/index.tsx ] && echo "✓ Index" || echo "✗"
```

---

## Testing Order

1. **Fix all 4 apps** (2-3 hours)
2. **Run build for each** (verify no errors)
3. **Publish to Expo** (test on device)
4. **Verify iOS/Android submission** (prep for App Store)

---

## Files to Create/Fix

| App | Action | File | Type |
|-----|--------|------|------|
| DailyAnchor | CREATE | app/index.tsx | TypeScript |
| DevotionFlow | CREATE | app/index.tsx | TypeScript |
| PelvicPro | CREATE | app/index.tsx | TypeScript |
| PelvicPro | CREATE | README.md | Markdown |
| PelvicPro | CREATE | COMPETITIVE_ANALYSIS.md | Markdown |
| PromptVault | VERIFY | app.tsx structure | (Test build) |

---

## Time Investment

| Task | Time | Difficulty |
|------|------|-----------|
| DailyAnchor entry point | 30 min | Easy |
| DevotionFlow entry point | 30 min | Easy |
| PelvicPro entry point | 30 min | Easy |
| PelvicPro README | 20 min | Easy |
| PelvicPro COMPETITIVE_ANALYSIS | 20 min | Medium |
| PromptVault verification | 15 min | Easy |
| Build & test all | 30 min | Easy |
| **TOTAL** | **3 hours** | |

---

## Next Steps

1. **TODAY:** Fix all 4 apps (3 hours max)
2. **VERIFY:** Run `npm run build` for each app
3. **UPDATE:** Change APP_STATUS_DASHBOARD.md statuses from ⚠️ to ✅
4. **PROCEED:** Move to marketing documentation phase

---

## Questions/Issues

If entry point creation causes errors:
1. Check app/_layout.tsx for proper navigation setup
2. Compare with working app (biomaxx, focusprayer)
3. Verify TypeScript types are imported
4. Check that React Native components are imported

**Reference Apps:**
- `/builds/biomaxx/app/index.tsx` - Simple structure
- `/builds/focusprayer/app/index.tsx` - Prayer screen example
- `/builds/learnlock/app/index.tsx` - Study focused

---

**Created:** 2026-01-21
**Status:** Ready for implementation
**Owner:** Dev team
