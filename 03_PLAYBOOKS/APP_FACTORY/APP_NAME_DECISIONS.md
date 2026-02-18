# App Name Decisions

**Updated:** 2026-01-21
**Status:** Names verified against App Store + Play Store

---

## Availability Check Results

| Original Name | iOS Status | Android Status | Decision |
|--------------|------------|----------------|----------|
| PrayerLock | TAKEN | TAKEN | RENAME |
| WalkToUnlock | SIMILAR EXISTS | AVAILABLE | RENAME |
| StudyLock | TAKEN | TAKEN | RENAME |
| PromptVault | AVAILABLE | TAKEN | KEEP (iOS priority) |
| DailyAnchor | AVAILABLE | AVAILABLE | KEEP |
| FemFit | TAKEN | TAKEN | RENAME |
| DailyDevotion | TAKEN | TAKEN | RENAME |

---

## Final App Names

### 1. FocusPrayer (was PrayerLock)
- **Bundle ID:** com.printmaxx.focusprayer
- **Tagline:** "Pray before you scroll"
- **Rationale:** Reverses emphasis, avoids existing "Prayer Lock: Christian Focus"

### 2. StepUnlock (was WalkToUnlock)
- **Bundle ID:** com.printmaxx.stepunlock
- **Tagline:** "Walk to unlock your apps"
- **Rationale:** Simpler, clearer, avoids "WalkLock" confusion

### 3. LearnLock (was StudyLock)
- **Bundle ID:** com.printmaxx.learnlock
- **Tagline:** "Lock distractions, unlock focus"
- **Rationale:** Broader appeal (students + professionals)

### 4. PromptVault (KEEP)
- **Bundle ID:** com.printmaxx.promptvault
- **Tagline:** "Your AI prompt library"
- **Rationale:** Available on iOS (primary platform), can differentiate on Android

### 5. DailyAnchor (KEEP)
- **Bundle ID:** com.printmaxx.dailyanchor
- **Tagline:** "Start your day grounded"
- **Rationale:** Fully available on both platforms

### 6. PelvicPro (was FemFit)
- **Bundle ID:** com.printmaxx.pelvicpro
- **Tagline:** "Pelvic floor strength training"
- **Rationale:** More specific, clinical positioning, avoids trademark conflict with JUNOFEM's femfit

### 7. DevotionFlow (was DailyDevotion)
- **Bundle ID:** com.printmaxx.devotionflow
- **Tagline:** "Daily faith in motion"
- **Rationale:** Combines devotion + flow state concept, differentiates from existing apps

---

## Alternative Names (Backup)

If primary choices also taken:

| App | Alt 1 | Alt 2 | Alt 3 |
|-----|-------|-------|-------|
| FocusPrayer | SacredLock | PrayFirst | FaithGate |
| StepUnlock | MoveToFocus | StrideBlock | WalkFirst |
| LearnLock | MindLock | FocusFlow | StudyGate |
| PromptVault | PromptBox | AIVault | PromptKeep |
| DailyAnchor | MorningAnchor | AnchorHabit | DailyRoot |
| PelvicPro | FloorStrong | PelvicFlow | CoreWell |
| DevotionFlow | FaithFlow | DevotionDaily | DevoTime |

---

## Trademark Notes

Before final submission:
1. Search USPTO TESS database for each name
2. Check domain availability (optional but recommended)
3. Verify no pending trademark applications

---

## Update Required

The following files need app name updates:

### Build folders
```
builds/prayerlock/ → builds/focusprayer/
builds/walktounlock/ → builds/stepunlock/
builds/studylock/ → builds/learnlock/
builds/femfit/ → builds/pelvicpro/
builds/dailydevotion/ → builds/devotionflow/
```

### Landing pages
```
LANDING/printmaxx-site/app/apps/prayerlock/ → focusprayer/
LANDING/printmaxx-site/app/apps/walktounlock/ → stepunlock/
LANDING/printmaxx-site/app/apps/studylock/ → learnlock/
LANDING/printmaxx-site/app/apps/femfit/ → pelvicpro/
LANDING/printmaxx-site/app/apps/dailydevotion/ → devotionflow/
```

### Config files (per app)
- app.json (display name, bundle ID)
- package.json (name field)
- RevenueCat product IDs
- Analytics event names

---

## Human Action Required

- [ ] Verify final names against USPTO
- [ ] Update Apple Developer bundle IDs
- [ ] Update Google Play package names
- [ ] Update RevenueCat project names
