# Deep QA Report: scripture-streak

**Date:** 2026-03-25 16:16
**Type:** generic
**Result:** FAIL

| Status | Check | Detail |
|--------|-------|--------|
| PASS | dead_imports | All relative imports resolve |
| PASS | console_errors | No suspicious console.error usage |
| WARN | async_error_handling | 1 files with async but no try/catch: notifications.ts |
| FAIL | empty_screens | Screens returning null: BibleScreen.tsx, PlansScreen.tsx |
| PASS | hardcoded_strings | No test/debug strings found |
| PASS | payment_flow | Stripe Payment Links wired in purchases.ts |
| PASS | onboarding | OnboardingFlow.tsx: 1978 lines, ~11 screens |
| PASS | onboarding | OnboardingScreen.tsx: 692 lines, ~5 screens |
| PASS | onboarding | OnboardingFlow.tsx: 1978 lines, ~11 screens |
| PASS | paywall_rescue | Rescue offer found in OnboardingFlow.tsx |
