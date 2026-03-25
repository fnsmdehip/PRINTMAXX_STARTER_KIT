# Test Report: scripture-streak
Generated: 2026-03-25 15:03
Overall: **FAIL**
Results: 9 passed, 1 failed, 1 warnings, 0 skipped / 11 total

## Results

| Status | Test | Message |
|--------|------|---------|
| PASS | app_json | app.json is valid JSON |
| PASS | bundle_id | Bundle ID: com.printmaxx.scripturestreak |
| PASS | app_name | App name: scripture streak |
| PASS | encryption_flag | ITSAppUsesNonExemptEncryption is set |
| PASS | permissions | Permission strings look specific |
| FAIL | placeholder_text | Found 7 placeholder(s): src/screens/StreaksScreen.tsx: contains 'xxx'; src/scree |
| PASS | hardcoded_keys | No hardcoded API keys detected |
| WARN | privacy_policy | Cannot reach privacy URL https://printmaxx.com/privacy: HTTP Error 404: Not Foun |
| PASS | subscription_terms | Subscription terms found (2/3 required phrases) |
| PASS | min_functionality | 15 TSX files with interactive elements |
| PASS | assets | Required assets present |

## Required Fixes (must fix before submission)

- **placeholder_text**: Found 7 placeholder(s): src/screens/StreaksScreen.tsx: contains 'xxx'; src/screens/BibleScreen.tsx: contains 'xxx'; src/screens/BibleScreen.tsx: contains 'placeholder'; src/screens/PlansScreen.tsx: contains 'xxx'; src/screens/SettingsScreen.tsx: contains 'xxx'

## Warnings (should fix)

- **privacy_policy**: Cannot reach privacy URL https://printmaxx.com/privacy: HTTP Error 404: Not Found