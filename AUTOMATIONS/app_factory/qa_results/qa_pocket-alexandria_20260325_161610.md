# Deep QA Report: pocket-alexandria

**Date:** 2026-03-25 16:16
**Type:** generic
**Result:** FAIL

| Status | Check | Detail |
|--------|-------|--------|
| PASS | dead_imports | All relative imports resolve |
| PASS | console_errors | No suspicious console.error usage |
| PASS | async_error_handling | All async functions have error handling |
| FAIL | empty_screens | Screens returning null: OnboardingScreen.tsx, OnboardingFlow.tsx |
| PASS | hardcoded_strings | No test/debug strings found |
| PASS | payment_flow | Stripe Payment Links wired in purchases.ts |
| WARN | onboarding | OnboardingFlow.tsx: 1996 lines, only ~3 screens detected |
| WARN | onboarding | OnboardingScreen.tsx: 1140 lines, only ~4 screens detected |
| WARN | onboarding | OnboardingFlow.tsx: 1996 lines, only ~3 screens detected |
| PASS | paywall_rescue | Rescue offer found in OnboardingFlow.tsx |
