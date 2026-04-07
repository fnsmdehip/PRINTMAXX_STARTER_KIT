# Ralph Spec Refiner — Per-Iteration Prompt

You are running one iteration of an autonomous spec refinement loop. Your job is to pick ONE pending app, write its production-grade refined spec, mark it done, then EXIT. Do not attempt multiple apps in one iteration.

## Working Directory
BASE_DIR=/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

## Step 1 — Read state

Read the state file to find the next pending app:

```
BASE_DIR/AUTOMATIONS/ralph_spec_refine_state.json
```

Find the first entry where `"status": "pending"` (sorted by `priority`). If all apps are `"done"`, write a summary to the log and exit cleanly.

## Step 2 — Mark as in-progress

Update that app's state entry:
- `"status": "in_progress"`
- `"started_at": "<ISO timestamp>"`

Save the state file.

## Step 3 — Load the gold standard

Read the TruthScope HANDOFF.md — this is the quality bar every refined spec must match:

```
BASE_DIR/lie-detector-app/TruthScope/HANDOFF.md
```

Study it. Notice:
- The depth of edge cases documented
- The level of cryptographic / security detail
- The QA hardening sections
- The production readiness checklist items
- The sensor / integration specifics
- The revenue and payment flow verification items
- The exact error states, failure modes, and guard conditions called out

This is your quality target. Every spec you write must reach this standard.

## Step 4 — Read the app's current state

For the selected app, read ALL of the following (skip any that don't exist):

1. **Current spec** (field: `current_spec`) — if it exists
2. **app.json** (field: `app_json`) — bundle ID, name, version, permissions
3. **Source screens**: `BASE_DIR/{source_dir}/screens/` — read all `.tsx` files
4. **Source components**: `BASE_DIR/{source_dir}/components/` — read key components
5. **Stores / state**: `BASE_DIR/{source_dir}/` — look for stores/, hooks/, services/, lib/ and read relevant files
6. **Package.json** at `BASE_DIR/MONEY_METHODS/APP_FACTORY/builds/{app_id}/package.json` — read dependencies

The goal: understand EXACTLY what the app currently does, what's real vs stubbed, what's missing, what edge cases aren't handled, and where the production gaps are.

## Step 5 — Write the refined spec

Write a comprehensive production-grade spec to `BASE_DIR/{output_spec}`.

### Structure (follow this exactly)

```markdown
# {App Name} — Production Spec (Refined)
*Version: 1.0 | Refined: {date} | Standard: TruthScope gold standard*

## Overview
- What the app does (2-3 sentences)
- Core value proposition
- Target user
- Revenue model

## Architecture
- Tech stack with specific versions
- State management approach
- Data persistence (AsyncStorage keys, schema)
- Navigation structure (all screens listed)
- External dependencies (APIs, SDKs, credentials needed)

## Screen-by-Screen Spec

For EACH screen:
### Screen: {ScreenName}
- **Purpose**: one sentence
- **Entry conditions**: how/when user reaches this screen
- **State**: what AsyncStorage/store values this screen reads
- **UI elements**: every button, text field, toggle, list — exact behavior
- **Edge cases**:
  - What if data is empty/null?
  - What if API call fails?
  - What if user has no subscription?
  - What if device is offline?
  - What if user is mid-action when app backgrounds?
- **Error states**: exact UI for each failure mode
- **Loading states**: what spinner/skeleton appears and when
- **Exit conditions**: every possible navigation away from this screen

## Data Model

For each persisted key:
| Key | Type | Default | Description | When written | When read |
|-----|------|---------|-------------|--------------|-----------|

## Payment & Subscription Flow
- Stripe product IDs (exact)
- Free tier limits (ENFORCED in code, not just labeled)
- Premium gates (exact feature list)
- Paywall trigger conditions
- Rescue offer trigger (what user action shows it)
- Restore purchases flow
- Deep link from Stripe success URL back to app
- What happens if isPremium check fails at launch

## Cryptography / Security (if applicable)
- Encryption algorithm + mode + key derivation
- PBKDF2 parameters (iterations, salt, key length)
- What is encrypted, what is not
- Key storage (where, how protected)
- What happens if decryption fails
- Audit log structure

## Onboarding Flow
- All screens in order (must be 12+ per quality standard)
- What data is collected per screen
- What personalization is unlocked from each answer
- Skip behavior (can user skip? what defaults?)
- Paywall position in onboarding
- Rescue offer on paywall decline

## API Integrations
For each external API:
- Endpoint used
- Auth method
- Error handling (401, 429, 503, timeout)
- Offline fallback
- Rate limit handling

## Sound Design
- Sound file names used
- Trigger conditions for each sound
- SoundTouchable integration verification
- playsInSilentModeIOS setting

## QA Hardening Checklist
Critical items the app must pass before submission:
- [ ] isPremium read from AsyncStorage on mount (not hardcoded useState(false))
- [ ] Free tier gating enforced in code (tested as free user, not just labeled)
- [ ] All screens handle empty state
- [ ] All async operations show ActivityIndicator
- [ ] Back navigation on every non-root screen
- [ ] Deep linking wired (URL scheme → correct screen)
- [ ] npx tsc --noEmit passes with 0 errors
- [ ] No Math.random() in sensor/biometric contexts
- [ ] No placeholder text visible to end user
- [ ] privacy policy URL resolves (printmaxx-privacy.surge.sh)
- [ ] ITSAppUsesNonExemptEncryption set in app.json
- [ ] Stripe success URL deep links to app and sets isPremium
- [ ] SoundTouchable or playSound present in every screen with touchable elements
- [ ] App name does not conflict with top 10 App Store results for that niche
- [ ] Subscription terms displayed per Apple 3.1.1/3.1.2
- [ ] Minimum useful functionality available without subscription
- [ ] Timer and Audio.Recording cleanup on unmount for every screen using them
- [ ] Session/usage limits enforced (counted in code, not just shown)
- [ ] No console.log/warn without __DEV__ gate

## Production Gaps (current state vs. spec)
List every gap between the current implementation and this spec:
- [ ] Gap 1: {description} — {file:line} — {severity: P0/P1/P2}
- [ ] Gap 2: ...

## Build Commands
```bash
# Development
cd MONEY_METHODS/APP_FACTORY/builds/{app_id}
npx expo prebuild --platform ios
npx expo run:ios

# Verify (take screenshot after each run)
xcrun simctl io booted screenshot /tmp/{app_id}_verify.png

# Type check
npx tsc --noEmit

# Deep link test
xcrun simctl openurl booted "{scheme}://home"
```

## App Store Metadata
- Bundle ID: {exact bundle ID from app.json}
- Display name: {exact display name}
- URL scheme: {exact scheme}
- Stripe product IDs: {list}
- Required permissions + purpose strings (exact text for Info.plist)
```

### Quality bar

Every section must be written at the depth of the TruthScope HANDOFF.md. If you cannot write something with specific detail, investigate the source code first. No vague statements. No "handles X appropriately." Say exactly HOW it handles X, what the exact error message is, what happens at the code level.

Production gaps must be exhaustive — if you find a stub, missing null check, hardcoded value, or missing edge case handler while reading the source, it goes in the gaps list.

## Step 6 — Mark as done

Update the state file:
- `"status": "done"`
- `"completed_at": "<ISO timestamp>"`

Save the state file.

## Step 7 — Log completion

Append one line to `BASE_DIR/AUTOMATIONS/logs/ralph_spec_refine.log`:
```
{ISO timestamp} | DONE | {app_id} | {output_spec_path} | {word_count} words
```

Then exit.

## Rules for this loop
- ONE app per iteration. Do not start the next app.
- No stubs. No placeholders in the spec. If you don't know, read the source code.
- No vague language. Specific code paths, specific file names, specific line numbers when relevant.
- The spec must be buildable. A fresh Claude session should be able to produce the app from this spec alone.
- If the source code has no spec and no existing PRD, derive the spec FROM the source code.
- DO NOT skip the QA Hardening Checklist. Fill every checkbox with the actual result.
- DO NOT summarize the TruthScope standard. MATCH it.
