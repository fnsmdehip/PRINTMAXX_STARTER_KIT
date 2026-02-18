# Ralph Task: App Factory Build

Build, test, and prepare apps for submission. Full autonomous pipeline.

---

## Context

Read these files before starting:
- `LEDGER/APP_CLONE_OPPORTUNITIES.csv` - Which apps to build
- `MONEY_METHODS/APP_FACTORY/APP_MONETIZATION_STRATEGY.md` - Revenue models
- `MONEY_METHODS/APP_FACTORY/APP_STORE_REJECTION_GUIDE.md` - Avoid rejection
- `MONEY_METHODS/APP_FACTORY/APP_LAUNCH_FULL_STACK.md` - Launch checklist
- `MONEY_METHODS/APP_FACTORY/products/` - Existing PRDs

Output to:
- `MONEY_METHODS/APP_FACTORY/builds/[app-name]/`
- `LEDGER/APP_BUILD_LOG.csv`

---

## Success Criteria

### Step 1: Select app to build

1. [ ] Read `LEDGER/APP_CLONE_OPPORTUNITIES.csv`
2. [ ] Filter for priority=HIGH and status=RESEARCHING or HAS_REPO
3. [ ] Check if MIT repo exists
4. [ ] If repo exists, clone and audit
5. [ ] If no repo, check for React Native/Flutter templates

### Step 2: Fork or scaffold

**If MIT repo exists:**
6. [ ] Clone repo
7. [ ] Audit code quality
8. [ ] List required modifications for niche version
9. [ ] Create modification plan

**If building from scratch:**
6. [ ] Use React Native or Flutter template
7. [ ] Scaffold basic app structure
8. [ ] Create component list from PRD

### Step 3: Implement core features

For each feature in PRD:
10. [ ] Implement feature
11. [ ] Write basic tests
12. [ ] Test on simulator
13. [ ] Document any issues

### Step 4: Add monetization

14. [ ] Integrate RevenueCat SDK
15. [ ] Create paywall UI
16. [ ] Configure subscription products (document IDs)
17. [ ] Add trial logic
18. [ ] Test subscription flow (sandbox)

### Step 5: Add analytics

19. [ ] Integrate Mixpanel or Amplitude
20. [ ] Add key event tracking:
    - App launch
    - Onboarding completion
    - Feature usage
    - Trial start
    - Purchase
21. [ ] Test events fire correctly

### Step 6: Pre-submission testing

22. [ ] Test on real device (document which)
23. [ ] Test on older device
24. [ ] Test offline behavior
25. [ ] Test edge cases from PRD
26. [ ] Run automated tests
27. [ ] Check for crashes

### Step 7: Prepare store assets

28. [ ] Generate app icon (use ASSET_GENERATION_GUIDE.md)
29. [ ] Create screenshots
30. [ ] Write app description
31. [ ] Write keywords
32. [ ] Prepare privacy policy content

### Step 8: Document for human submission

33. [ ] Create submission checklist
34. [ ] List manual steps required
35. [ ] Document any blockers
36. [ ] Update `LEDGER/APP_BUILD_LOG.csv`

---

## Build Log CSV Format

```csv
id,app_name,started,completed,status,repo_used,features_complete,tests_passing,blockers,notes
1,PrayerLock,2026-01-21,pending,IN_PROGRESS,github.com/...,5/7,12/15,none,Building paywall
```

---

## Per-App Output Structure

```
MONEY_METHODS/APP_FACTORY/builds/prayerlock/
├── README.md              # Build notes, how to run
├── SUBMISSION_CHECKLIST.md # What human needs to do
├── src/                   # App source code
├── tests/                 # Test files
├── assets/
│   ├── icon/              # App icons
│   ├── screenshots/       # Store screenshots
│   └── marketing/         # Promo images
├── store_listing/
│   ├── description.md     # App Store description
│   ├── keywords.txt       # ASO keywords
│   └── privacy_policy.md  # Privacy policy
└── config/
    ├── revenuecat.json    # RevenueCat product IDs
    └── analytics.json     # Event definitions
```

---

## Guardrails

### Do NOT:
- Submit to app stores (human must do this)
- Input payment credentials
- Access live RevenueCat/Stripe (use sandbox)
- Skip testing
- Build without PRD

### Always:
- Follow copy-style.md for all content
- Check APP_STORE_REJECTION_GUIDE.md before finalizing
- Document blockers in errors.log
- Update progress.md

---

## Testing Matrix

| Test | Required | Notes |
|------|----------|-------|
| Simulator launch | YES | Basic functionality |
| Real device launch | YES | Catch real issues |
| Offline mode | YES | Handle gracefully |
| Paywall display | YES | Pricing visible |
| Trial flow | YES | RevenueCat sandbox |
| Crash on launch | YES | Must pass |
| Memory leaks | RECOMMENDED | Long session test |
| IPv6 network | RECOMMENDED | Apple requirement |

---

## Feature Implementation Order

1. **Core mechanic** - The main thing the app does
2. **Onboarding** - First-time user experience
3. **Paywall** - Revenue generation
4. **Settings** - User preferences
5. **Analytics** - Tracking
6. **Polish** - Animations, micro-interactions

---

## After Completion

1. Update `.ralph/progress.md`
2. Update `LEDGER/APP_BUILD_LOG.csv`
3. Create human action items in `MANUAL_SETUP_TASKS.md`
4. Notify about blockers if any

---

test_command: "ls MONEY_METHODS/APP_FACTORY/builds/*/README.md | wc -l"
