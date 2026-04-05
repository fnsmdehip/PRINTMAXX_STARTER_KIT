# Vibe Coding Research: What to Steal for Our App Factory

Research date: 2026-04-04
Sources: Replit Agent 3/4, Bolt.new v2, Lovable 2.0, v0 by Vercel, Cursor/Windsurf, Vibecode, Expo Skills, Callstack agent-skills, cursor.directory, Augment Code failure patterns

---

## 1. TOOL-BY-TOOL BREAKDOWN

### Replit Agent (v3/v4, March 2026)

**What they do that we don't:**
- **Self-testing with real browsers.** Agent spins up Playwright, navigates the app like a user, clicks buttons, fills forms, checks outputs. If something breaks, it fixes it automatically before presenting to the user. They call this "REPL-based verification" and it catches "Potemkin interfaces" (UIs that look right but don't function).
- **Automatic checkpoints.** Every meaningful state is saved. User can roll back to any previous working version. We have git but no structured checkpoint system per-feature.
- **Parallel fork execution (Agent 4).** Large tasks split into sub-agents that work concurrently on independent parts, then merge results with conflict-resolution sub-agents. Build time dropped from 15-20 min to 3-5 min.
- **200-minute autonomous sessions.** Agent 3+ can work for hours without human input, self-correcting along the way.

**What to steal:**
1. Post-build Playwright self-test that navigates every screen, taps every button, checks for crashes
2. Checkpoint system: git tag after each passing screen/feature
3. Parallel sub-agent pattern for independent app components (onboarding, settings, core feature can be built simultaneously)

### Bolt.new v2 (StackBlitz, 2026)

**What they do that we don't:**
- **WebContainer runtime.** Full Node.js in-browser, no local setup. Not applicable to native apps but the preview-and-fix loop is instant.
- **Autonomous debugging that reduces error loops by 98%.** When code fails, Bolt v2 doesn't just retry the same approach. It reasons about the error, tries a different strategy, and validates the fix.
- **Integrated infrastructure.** Database, auth, payments, hosting, SEO all auto-managed in one prompt. For our Expo apps, the equivalent would be: Expo Router + Zustand + Stripe + RevenueCat + EAS wired from the template.
- **Figma import.** Drop a design, get working code. We should use screenshot-to-code for UI consistency.

**What to steal:**
1. Error-loop breaker: if the same error appears 3 times, switch strategy (we have this in Rule 28 but don't enforce it in code generation)
2. Infrastructure-from-template: every new app starts with payments, auth, analytics, deep linking already wired (not added later)

### Lovable 2.0 (February 2026)

**What they do that we don't:**
- **Vulnerability scanning on every publish.** Checks for exposed env vars, insecure API calls, improper auth patterns automatically before deploy.
- **Chat Mode Agent.** Can reason about problems without editing code. Useful for architecture decisions before touching files.
- **Cleanest React output** of any builder according to comparative tests.

**What to steal:**
1. Pre-deploy security scan: check for hardcoded keys, exposed secrets, missing auth guards
2. Separate "think" mode before "build" mode for each feature

### v0 by Vercel (February 2026 update)

**What they do that we don't:**
- **Git-native workflow.** Every chat creates a branch. PRs are first-class. Previews deploy automatically on merge. Non-engineers can ship production code through proper git workflows.
- **Database connectivity.** Direct Snowflake/AWS integration from the builder.
- **shadcn/ui + Tailwind + Next.js** as the default stack produces consistent, production-grade output.
- **40+ React best practices** shipped as an agent skill that auto-validates output.

**What to steal:**
1. Component library as constraint: lock the AI to a specific UI kit (we should standardize on React Native Paper or Tamagui) so output is always consistent
2. Vercel's React Best Practices skill: 40+ rules the AI checks against. We need the equivalent for React Native/Expo.

### Cursor / Windsurf (2026)

**What they do that we don't:**
- **Codebase indexing via Merkle tree.** Cursor indexes the entire project, so when generating a new component it understands existing patterns, imports, and conventions. Our Claude Code sessions lose this context between compactions.
- **Arena Mode (Windsurf).** Blind evaluation of outputs from different models. Pick the best generation without knowing which model wrote it.
- **Inline completions + agent mode combo.** Power users use Cursor for autocomplete and Windsurf for heavy agent tasks.

**What to steal:**
1. Project convention file (CLAUDE.md / .cursorrules) that explicitly defines: naming conventions, file structure, import patterns, navigation patterns, styling approach. We have this partially but need React Native specifics.
2. Force the agent to read existing layout files before generating new screens (prevents hallucinated navigation)

### Vibecode (vibecodeapp.com)

**What it is:** Mobile app (iOS + web) that generates native mobile apps from text prompts. Uses Expo under the hood. Aimed at non-coders. Lets you preview on your actual phone.

**What to steal:**
1. On-device preview loop: generate -> preview on phone -> iterate. We should use Expo Go or EAS Update for rapid preview cycles.

---

## 2. EXPO SKILLS AND AGENT-SKILLS ECOSYSTEM

This is the biggest thing we should integrate immediately.

### Expo Official Skills (github.com/expo/skills)
- Structured instruction files that teach AI agents how to build/deploy/debug Expo apps
- Auto-discovered by Claude Code and Cursor based on context
- Cover: project setup, routing, EAS Build, EAS Update, native modules, debugging

### Callstack Agent Skills (github.com/callstackincubator/agent-skills)
- React Native best practices packaged as agent skills
- Built by dozens of engineers from Callstack + Expo + community
- Cover: memoization, React Compiler, atomic state, moving work off JS thread, FlatList optimization

### Vercel React Best Practices Skill
- 40+ performance rules auto-checked during generation
- Component structure, hooks usage, accessibility, TypeScript patterns

### How to install for Claude Code:
These skills go into `.claude/` as markdown files. The agent auto-loads them based on context. We should pull the Expo skills and Callstack agent-skills into our app factory template.

---

## 3. THE 8 FAILURE PATTERNS IN AI-GENERATED CODE

From Augment Code's research and cross-referenced with Sonar, LogRocket, and real-world testing:

### Pattern 1: Phantom Imports (Hallucinated APIs)
- AI generates imports for packages that don't exist, or calls methods that sound plausible but aren't real
- 1 in 5 AI code samples contains references to fake libraries
- **Auto-check:** `npx tsc --noEmit` catches missing types. ESLint `import/no-unresolved` catches phantom packages. Run `npm ls` to verify all imports resolve.

### Pattern 2: Stale / Deprecated APIs
- AI uses patterns from training data that are now outdated (e.g., old React Native APIs, deprecated Expo methods)
- **Auto-check:** Pin dependency versions in the template. Use `expo-doctor` to check compatibility. Keep a blocklist of deprecated APIs.

### Pattern 3: Happy-Path-Only Code
- AI writes the success case well but error handlers, retry logic, and edge cases are weak or missing
- **Auto-check:** Grep for `catch` blocks that are empty or just `console.log`. Check that every `fetch` / `async` call has error handling. Verify loading states exist for every data-fetching screen.

### Pattern 4: Dead Code and Unused Imports
- AI adds imports it doesn't use, creates helper functions nothing calls, leaves commented-out code
- **Auto-check:** ESLint `no-unused-vars`, `no-unused-imports`. TypeScript `noUnusedLocals`. Tree-shaking analysis.

### Pattern 5: Missing Loading / Empty / Error States
- Screens that fetch data show nothing while loading, show nothing when data is empty, crash on error
- **Auto-check:** For every component that fetches data, verify three states exist: loading indicator, empty state message, error state with retry.

### Pattern 6: Navigation to Non-Existent Screens
- AI generates `navigation.navigate('ProfileScreen')` but no such screen exists in the navigator
- **Auto-check:** Parse all `navigate()` / `router.push()` calls and verify target routes exist in the Expo Router file tree. Automated: walk `app/` directory, extract route names, compare against all navigation calls.

### Pattern 7: Inconsistent State Management
- AI mixes different state approaches (useState + Redux + Context + Zustand) in the same app
- **Auto-check:** Grep for state management imports. If more than one approach is used, flag it. Template should enforce ONE approach (Zustand for our stack).

### Pattern 8: Security Anti-Patterns
- API keys in source code, missing input validation, exposed environment variables, client-side-only auth
- **Auto-check:** `grep -r "sk_live\|sk_test\|api_key\|apiKey\|API_KEY\|password" --include="*.ts" --include="*.tsx"` to catch hardcoded secrets. Verify `.env` is in `.gitignore`. Check that sensitive operations happen server-side.

---

## 4. APP-SPECIFIC FAILURE CHECKLIST (STEAL THIS)

Beyond the 8 patterns, these are mobile-app-specific failures we've observed or that other builders catch:

### Navigation & UX
- [ ] Every screen has a back button or swipe-back gesture
- [ ] Tab bar shows correct active state
- [ ] Deep links resolve to correct screens (`xcrun simctl openurl booted "scheme://route"`)
- [ ] Keyboard doesn't cover input fields (KeyboardAvoidingView on every input screen)
- [ ] Safe area insets respected on all screens (notch, home indicator)
- [ ] Orientation lock set correctly (portrait for most apps)

### Sound & Haptics
- [ ] Button taps have haptic feedback (`expo-haptics`)
- [ ] Success/error states have distinct sounds
- [ ] Sound can be toggled off in settings
- [ ] Sound files are preloaded at app init, not loaded on demand
- [ ] No audio playback on silent mode unless user explicitly enabled

### Data & State
- [ ] App works offline (or shows clear offline state)
- [ ] Pull-to-refresh on list screens
- [ ] Pagination on long lists (not loading 10K items at once)
- [ ] State persists across app restarts (AsyncStorage / MMKV)
- [ ] Logout clears all user data

### Performance
- [ ] FlatList (not ScrollView) for any list > 20 items
- [ ] Images use proper caching (`expo-image`, not `<Image>`)
- [ ] No re-renders on every keystroke in search/input fields (debounce)
- [ ] Animations run on native driver (`useNativeDriver: true` or Reanimated)
- [ ] Bundle size under 20MB for initial download

### Payment & Premium
- [ ] Free users ACTUALLY blocked from premium features (not just shown paywall they can dismiss)
- [ ] Restore purchases button exists and works
- [ ] Subscription terms displayed per Apple 3.1.1/3.1.2
- [ ] Cancel subscription instructions accessible
- [ ] Payment failure shows clear error, not silent fail

### Apple Compliance
- [ ] No placeholder text anywhere
- [ ] Privacy policy URL resolves and is accurate
- [ ] Camera/mic/location permission strings are specific (not generic)
- [ ] `ITSAppUsesNonExemptEncryption` set correctly
- [ ] Minimum useful functionality without subscription (Apple 3.1.1)
- [ ] No exaggerated accuracy/health claims

---

## 5. THE STRUCTURED PROMPT APPROACH (WHAT ACTUALLY WORKS)

Consensus across all 2026 research: one-shot full-app prompts produce buggy, inconsistent results. The winning approach is **structured multi-phase generation with validation gates between phases.**

### Phase 1: Architecture Spec (think, don't code)
```
You are a senior React Native architect. Do NOT write code yet.

Given this app concept: [CONCEPT]

Output:
1. Screen list with navigation hierarchy (tab/stack/drawer)
2. State management approach (Zustand stores needed)
3. External APIs/SDKs required
4. Data models (TypeScript interfaces)
5. File structure following Expo Router conventions
6. Premium vs free feature boundaries
```

### Phase 2: Skeleton Generation (structure, not content)
```
Using the architecture from Phase 1, generate:
1. Expo Router file structure (app/ directory with _layout.tsx files)
2. Empty screen components with proper TypeScript types
3. Navigation wired and testable
4. Zustand stores with initial state
5. Type definitions in src/types/

Do NOT implement features yet. Every screen should render a
centered text saying "[ScreenName] - TODO".
Navigation between ALL screens must work.
```

### Phase 3: Feature Implementation (one screen at a time)
```
Implement [SCREEN_NAME] with these requirements:
- [Feature 1]
- [Feature 2]

Constraints:
- Use existing types from src/types/
- Use existing Zustand store from src/stores/
- Include loading, empty, and error states
- Include haptic feedback on button taps
- Follow existing code patterns from other implemented screens
```

### Phase 4: Polish Pass
```
Review the entire app for:
1. Missing error states (add try/catch + error UI)
2. Missing loading states (add ActivityIndicator)
3. Missing empty states (add "No data" messages)
4. Unused imports (remove them)
5. Console.log statements (remove them)
6. Hardcoded strings (extract to constants)
7. Missing TypeScript types (add them)
8. Accessibility labels on interactive elements
```

### Phase 5: Pre-Submit Validation
```
Run these checks:
1. npx tsc --noEmit (zero errors)
2. npx expo export --platform ios (clean build)
3. Verify every route in app/ has a matching navigation call
4. Verify no hardcoded API keys in source
5. Verify all images/assets exist at referenced paths
6. Verify payment flow blocks free users from premium content
7. Screenshot every screen via Simulator
```

---

## 6. THE SPEC-DRIVEN APPROACH (Inferno Red / Codex Pattern)

The best AI-app-building teams use a "planning folder" that persists across sessions:

```
planning/
  change-log.md      -- What changed and why (prevents repeated mistakes)
  codex-config.md    -- Architecture decisions, code style, constraints
  progress-plan.md   -- Sequential feature list with checkboxes
  history.md         -- What was prompted and when
```

**Why this works:** AI agents lose context. The planning folder IS the context. Every new session reads the plan, picks up where it left off, and doesn't drift. This is exactly our Ralph pattern (filesystem = memory) applied to app building.

**What to steal:** Create a `planning/` folder in every app factory project with these 4 files auto-generated from the initial spec.

---

## 7. THE .CURSORRULES / CLAUDE.MD FOR REACT NATIVE

Best practices aggregated from cursor.directory, Expo docs, and Callstack:

```markdown
# React Native / Expo App Rules

## Stack
- Expo SDK 54+ with Expo Router (file-based routing)
- TypeScript strict mode
- Zustand for state management
- TanStack React Query for data fetching
- React Native Reanimated 4.x for animations
- expo-image (not <Image>) for all images
- MMKV for fast local storage
- NativeWind or Tamagui for styling (pick ONE)

## Code Style
- Functional components only (no class components)
- Arrow functions with proper TypeScript return types
- camelCase for variables/functions, PascalCase for components
- Separate styles from component code
- One component per file
- Explicit return types on all exported functions

## File Structure (Expo Router)
app/
  _layout.tsx          -- Root layout (providers, fonts, splash)
  (tabs)/
    _layout.tsx        -- Tab navigator
    index.tsx          -- Home tab
    settings.tsx       -- Settings tab
  (auth)/
    _layout.tsx        -- Auth stack
    login.tsx
    onboarding.tsx
  [feature]/
    index.tsx
    [id].tsx

src/
  components/          -- Reusable UI components
  stores/              -- Zustand stores
  types/               -- TypeScript interfaces
  hooks/               -- Custom hooks
  utils/               -- Helper functions
  constants/           -- App constants, theme, colors
  sounds/              -- Sound engine + audio files
  services/            -- API calls, payment service

## Navigation Rules
- NEVER navigate to a route that doesn't exist in app/ directory
- ALWAYS use typed routes: router.push('/screen') not navigation.navigate('Screen')
- Every stack must have a back button or swipe-back gesture
- Read ALL _layout.tsx files before generating new screens

## State Rules
- ONE state management library (Zustand). No mixing with Context or Redux.
- Persist critical state with MMKV
- Server state through TanStack Query, not Zustand
- No prop drilling beyond 2 levels -- use store or context

## Performance Rules
- FlatList for any list > 10 items
- React.memo() on components receiving stable props
- useCallback/useMemo for expensive operations
- Animations on native thread (Reanimated, not Animated API)
- Debounce search inputs (300ms)
- Lazy-load screens with React.lazy + Suspense

## Required States for EVERY Data Screen
- Loading: ActivityIndicator or skeleton
- Empty: meaningful message + action
- Error: message + retry button
- Success: the actual content

## Sound & Haptics (REQUIRED)
- expo-haptics on every button press
- Sound effects from professional CC0 libraries
- SoundEngine.ts with preloading
- Mute toggle in settings that persists

## Security (MANDATORY)
- All API keys in .env (never in source)
- .env in .gitignore
- No console.log in production
- Input validation on all user inputs
- Sensitive data encrypted at rest (SecureStore for tokens)

## Build Commands
- Dev: npx expo run:ios (NEVER expo start --ios for native modules)
- Prebuild: npx expo prebuild --platform ios --clean
- Export check: npx expo export --platform ios
- Type check: npx tsc --noEmit
```

---

## 8. AUTOMATED QUALITY GATES (ADD TO OUR PIPELINE)

What other tools do automatically that we should add to `test_runner.py`:

### Gate 1: TypeScript Compilation
```bash
npx tsc --noEmit
# MUST pass with 0 errors. No exceptions.
```

### Gate 2: Route Integrity
```bash
# Script: verify every navigate/push/replace call targets an existing route
# Parse all .tsx files for router.push/navigate calls
# Compare against actual files in app/ directory
# FAIL if any route target doesn't exist
```

### Gate 3: Import Verification
```bash
# Run ESLint with import/no-unresolved
# Or: npx tsc --noEmit catches missing module imports
# Also check: no unused imports (eslint no-unused-imports)
```

### Gate 4: State Completeness
```bash
# For every component that uses useQuery/fetch/async data:
# Verify existence of: isLoading check, error check, empty data check
# Grep pattern: files with "useQuery" must also contain "isLoading" and "isError"
```

### Gate 5: Security Scan
```bash
# Grep for hardcoded keys
grep -rn "sk_live\|sk_test\|api_key\b\|apiKey\|API_KEY\|password\s*=" \
  --include="*.ts" --include="*.tsx" src/ app/
# FAIL if any matches found

# Verify .env in .gitignore
grep -q "\.env" .gitignore || echo "FAIL: .env not in .gitignore"
```

### Gate 6: Dead Code Detection
```bash
# Unused exports
# Unused imports
# Functions defined but never called
# Components defined but never rendered
npx ts-prune  # or eslint with unused rules
```

### Gate 7: Accessibility Baseline
```bash
# Every TouchableOpacity/Pressable must have accessibilityLabel
# Every Image must have accessibilityLabel or accessibilityRole
grep -rn "Pressable\|TouchableOpacity" --include="*.tsx" | \
  grep -v "accessibilityLabel"
# Flag any without labels
```

### Gate 8: Asset Verification
```bash
# Every require('./path/to/asset') must resolve to an existing file
# Every source={{ uri: 'url' }} should be validated
# App icon and splash screen must exist at correct paths
```

### Gate 9: Build Verification
```bash
npx expo export --platform ios
# MUST succeed. This catches missing native modules, bad configs, etc.
```

### Gate 10: Screenshot Verification (Replit-style)
```bash
# Build and launch in Simulator
npx expo run:ios --device "iPhone 16 Pro"
sleep 10
# Screenshot every screen
xcrun simctl io booted screenshot /tmp/screen_home.png
# Open deep links to navigate
xcrun simctl openurl booted "truthscope://settings"
xcrun simctl io booted screenshot /tmp/screen_settings.png
# Verify screenshots are not error screens (red boxes, white screens)
```

---

## 9. WHAT TO IMPLEMENT NOW (Priority Order)

### Immediate (this session)
1. Pull Expo Skills into our app template: `https://github.com/expo/skills`
2. Pull Callstack agent-skills: `https://github.com/callstackincubator/agent-skills`
3. Add the `.cursorrules`-equivalent React Native rules to our CLAUDE.md (Section 7 above)

### This week
4. Add Route Integrity check to `test_runner.py` (Gate 2)
5. Add State Completeness check to `test_runner.py` (Gate 4)
6. Add Security Scan to `test_runner.py` (Gate 5)
7. Add Dead Code Detection to `test_runner.py` (Gate 6)
8. Create `planning/` folder template for every new app

### Next sprint
9. Implement Playwright self-test (Replit-style): build, launch, screenshot every screen, check for red error screens
10. Implement parallel sub-agent pattern for independent screens
11. Add error-loop-breaker: if same TypeScript error 3 times, switch approach
12. Pre-wire template with: Stripe, haptics, sound engine, Zustand, Expo Router, deep linking

---

## 10. KEY INSIGHT: THE TEMPLATE IS THE MOAT

Every winning tool (Replit, Bolt, Lovable, v0) has converged on the same truth: the quality of AI-generated apps depends more on the TEMPLATE and CONSTRAINTS than on the prompt.

- Replit's template includes self-testing infrastructure
- Bolt's template includes database, auth, payments pre-wired
- Lovable's template produces clean React because shadcn/ui constrains the output
- v0's template is Next.js + Tailwind + shadcn, always consistent

**Our equivalent:** A hardened Expo template with Expo Router + Zustand + Stripe + Sound Engine + Haptics + Reanimated + Deep Linking + 12-screen onboarding + paywall pre-wired. The AI fills in the specifics. The template guarantees the quality floor.

Build the template once. Every app inherits the quality. The prompt just customizes the content.

---

## Sources

- [8 Vibe Coding Best Practices (Softr)](https://www.softr.io/blog/vibe-coding-best-practices)
- [Vibe Coding Workflow Guide (vibecoding.app)](https://vibecoding.app/blog/vibe-coding-workflow-examples)
- [Replit Agent 4 (replit.com)](https://replit.com/agent4)
- [Replit Self-Testing at Scale (blog.replit.com)](https://blog.replit.com/automated-self-testing)
- [What Changed Agent 3 to Agent 4 (blog.replit.com)](https://blog.replit.com/whats-changed-agent3-to-agent4)
- [Bolt.new v2 (bolt.new)](https://bolt.new/blog/bolt-v2)
- [Bolt.new Review (banani.co)](https://www.banani.co/blog/bolt-new-ai-review-and-alternatives)
- [Lovable Review (taskade.com)](https://www.taskade.com/blog/lovable-review)
- [v0 by Vercel Complete Guide (nxcode.io)](https://www.nxcode.io/resources/news/v0-by-vercel-complete-guide-2026)
- [Introducing the New v0 (vercel.com)](https://vercel.com/blog/introducing-the-new-v0)
- [Cursor vs Windsurf 2026 (nxcode.io)](https://www.nxcode.io/resources/news/windsurf-vs-cursor-2026-ai-ide-comparison)
- [Cursor vs Windsurf for React Native (medium.com)](https://medium.com/@arslannaz195/cursor-vs-windsurf-for-react-native-development-which-ai-ide-should-you-choose-in-2026-d2f4b4bf6579)
- [Vibecode App (vibecodeapp.com)](https://www.vibecodeapp.com/)
- [Debugging AI-Generated Code: 8 Failure Patterns (augmentcode.com)](https://www.augmentcode.com/guides/debugging-ai-generated-code-8-failure-patterns-and-fixes)
- [Vibe Then Verify (sonarsource.com)](https://www.sonarsource.com/blog/how-to-navigate-the-risks-of-ai-generated-code)
- [Fixing AI-Generated Code (logrocket.com)](https://blog.logrocket.com/fixing-ai-generated-code/)
- [15 Rules of Vibe Coding React Native (medium.com)](https://medium.com/@sisongqolosi/15-rules-of-vibe-coding-react-native-expo-d89e2ea01772)
- [Spec-Driven Dev Expo Starter (blog.infernored.com)](https://blog.infernored.com/spec-driven-development-react-native-starter-app-with-expo-codex/)
- [Expo Skills for AI Agents (docs.expo.dev)](https://docs.expo.dev/skills/)
- [Callstack Agent Skills (github.com)](https://github.com/callstackincubator/agent-skills)
- [React Native Best Practices for AI (callstack.com)](https://www.callstack.com/blog/announcing-react-native-best-practices-for-ai-agents)
- [Expo Cursor Rules (cursor.directory)](https://cursor.directory/expo-react-native-typescript-cursor-rules)
- [React Native Cursor Rules (cursorrules.org)](https://cursorrules.org/article/react-native-expo-cursorrules-prompt-file)
- [Prompts for Vibe Coding (base44.com)](https://base44.com/blog/prompts-for-vibe-coding)
- [Vibe Coder's Prompting Guide (medium.com)](https://annaarteeva.medium.com/the-vibe-coders-prompting-guide-e04ba0295a18)
- [RapidNative AI Builder (rapidnative.com)](https://www.rapidnative.com/blogs/vibe-coding-complete-guide)
- [Vercel React Best Practices Skill (vercel.com)](https://vercel.com/blog/introducing-react-best-practices)
- [AI Code Quality Guide 2026 (codeintelligently.com)](https://codeintelligently.com/blog/ai-code-quality-guide-2026)
