# PRINTMAXX — Autonomous Revenue System

Read `OPS/PERSISTENT_TASK_TRACKER.md` FIRST every session. Read `AUTOMATIONS/SOUL.md` for behavioral directives.

## Browser Rule
- ALWAYS use `open -a "Google Chrome"` for URLs, NEVER bare `open`. Chrome = Claude in Chrome MCP + computer-use compatible. Brave = personal browser, don't touch.

## Session Start (10 min max)
1. Read `OPS/SESSION_BRIEFING.md` + `OPS/PERSISTENT_TASK_TRACKER.md` + `OPS/DAILY_TACTICAL_PLAN.md`
2. `python3 AUTOMATIONS/decision_engine.py --cycle`
3. Deploy anything deployable. Check `OPS/ACTIONABLE_QUEUE.md`
4. For architecture/system analysis/naming: read `OPS/PRINTMAXX_SYSTEM_MAP.md` FIRST — canonical live architecture with L0-L6 hierarchy, data flow, agent topology, cron schedule, state files.

## Reference (read on demand, NOT every session)
| Need | File |
|------|------|
| Find a file | `OPS/NAV_INDEX.md` |
| **System map** | **`OPS/PRINTMAXX_SYSTEM_MAP.md`** — CANONICAL architecture. READ FIRST for system context. UPDATE same-session on ANY agent/cron/architecture/data-flow change. |
| **ALL resources/IP/playbooks** | **`OPS/RESOURCE_MANIFEST.md`** — COMPLETE index of 200+ resources: playbooks, products, guides, templates, research. READ BEFORE creating anything new (DEDUP). READ BEFORE executing any venture (load relevant playbooks). Capital Genesis, Intelligence Router, CEO Agent MUST consult this. |
| Status | `OPS/CURRENT_STATUS.md` |
| Commands | `.claude/rules/commands-reference.md` |
| Agent infra | `.claude/rules/agent-infrastructure.md` |
| File locations | `.claude/rules/file-locations.md` |
| Strategy | `.claude/rules/strategic-ethos.md` |
| Quality pipeline | `.claude/rules/auto-quality.md` |
| Ralph/Memory | `.claude/rules/ralph-and-memory.md` |
| Copy style | `.claude/reference/copy-style.md` (load on demand, NOT every message) |
| Guardrails | `.claude/rules/guardrails.md` |
| Security | `.claude/rules/security.md` + `.claude/reference/external-code-security.md` |
| Alpha review | `.claude/reference/alpha-review.md` (load on demand) |
| **Auto-integration** | **`.claude/rules/auto-integration.md`** — pipeline must self-feed, no human prompting for integration |
| **E2E Verification** | **`.claude/rules/end-to-end-verification.md`** — NEVER claim "done" without verifying actual output artifacts |
| **Deep Thinking** | **`.claude/rules/deep-thinking-dedup.md`** — dedup before creating, consolidate over duplicate, revenue reality check |
| **Reprocess on Discovery** | **`.claude/rules/reprocess-on-discovery.md`** — MUST rescore Capital Genesis + update KPIs when new resources/playbooks/tools are added |
| Before You | `MONEY_METHODS/BEFORE_YOU/BEFORE_YOU_VENTURE_README.md` |
| Before You codebase | `/Users/macbookpro/Documents/ancestry-research/before-you/` (generator, template, landing, content) |

## Core Rules (ALWAYS active)
1. **SHIP NOW** — Deploy what exists before building new things. $0 revenue at Day 35.
2. **NO ORPHANS** — Every doc has a CONSUMER (agent or human task). No dead-end reports.
3. **NO SLOP** — No AI vocabulary. No em dashes. Copy style in `.claude/rules/copy-style.md`.
4. **AUTONOMOUS** — Don't ask permission. Execute. Fix mistakes. AUTOMATE periodic tasks to cron immediately.
5. **ABOVE AND BEYOND** — Follow the logical end of the vision. Build implicit subtasks. Recursive value chain: SCAN→ANALYZE→DECIDE→CREATE→DISTRIBUTE→COMPOUND→OPTIMIZE.
6. **ONE DASHBOARD** — `AUTOMATIONS/control_panel.py` at localhost:9999. NEVER create new dashboards.
7. **FACTORY MODE** — Pre-build everything. Don't wait for accounts.
8. **NEVER DROP THE BALL** — Track all active systems. Include status after tasks.
9. **MAX SQUEEZE** — Every build session = 3 tweets + 1 thread minimum. Content from everything.
10. **PARALLEL BY DEFAULT** — 5 items = 5 agents. Background agents for >5K token output.
11. **CEO SANITY CHECK** — Am I building or selling? What's the obvious thing? Human blockers surfaced?
12. **ARCHITECTURE-FIRST** — Before analyzing/describing/naming the system, read `OPS/PRINTMAXX_SYSTEM_MAP.md`. On ANY architecture change (agents, cron, scripts, data flow, state files): update system map + task tracker + CLAUDE.md in SAME session. New ventures also update SOUL.md + memory. No stale maps. No orphan ventures.
13. **COMPETITIVE COGNITION** — Assume 10K power users working on the same problem. Find the non-obvious angle. Anti-lazy: am I defaulting to popular or critically analyzing for best? See SOUL.md protocol.
14. **INTELLIGENCE-FIRST** — Query `intelligence_router.py` before every action. 15K+ alpha entries, not default LLM knowledge. Check `OPS/CAPITAL_GENESIS_PRIORITY_STACK.md` for daily ranked priorities.
15. **RESOURCE-AWARE** — Before creating playbooks, guides, strategies, or products: check `OPS/RESOURCE_MANIFEST.md`. 200+ existing resources. DEDUP before creating. Load relevant playbook when executing any venture. Every resource is content source material AND potential sellable product.
16. **REPROCESS ON DISCOVERY** — When new resources, methods, playbooks, tools, or IP are discovered or created: (a) re-run `python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report` to rescore ALL methods with new context, (b) update `OPS/KPI_DASHBOARD.md` if new ventures/products affect revenue projections, (c) update `OPS/RESOURCE_MANIFEST.md` with new entries, (d) check if any existing KPI tasks or actionable queue items are affected. New resources change the scoring landscape — a method with no playbook scoring 6.0 might score 7.5 with a playbook. NEVER add resources without reprocessing the scoring pipeline.

17. **NO DEAD CODE** — Never create scripts that aren't immediately tested and wired to a cron or caller. If a script isn't called by anything, it's dead weight. Before creating ANY new .py file: (a) name an existing script that could be extended instead, (b) if new file is truly needed, add a cron entry or caller in the SAME session, (c) run it immediately after creation to verify it works. The system has 428 scripts. Most are dead. Stop adding to the pile.
18. **API-KEY OVER OAUTH** — All `claude -p` calls in automated/cron/background scripts MUST use `--api-key` flag when `ANTHROPIC_API_KEY` env var is set. OAuth tokens expire silently and kill entire pipelines for days. Every `subprocess.run(["claude"...])` in the codebase must check for this. Heuristic fallbacks required when LLM calls fail.
19. **TEST ON CREATE** — Every new automation, cron job, or script MUST be run immediately after creation. Don't schedule and hope. Test NOW, check output, fix errors, re-run until clean, THEN add to cron. If it can't run standalone, it's not done.
20. **LOOP HEALTH** — All 4 loop closer loops MUST show OK (not DEAD/STALE). Check with `python3 AUTOMATIONS/loop_closer.py --status`. If any loop is DEAD, fix it before doing anything else. Dead loops mean the system isn't self-correcting.
21. **RBI OVER BUILDING** — Research, Backtest, Implement. Don't build new systems. Run `python3 AUTOMATIONS/rbi_loop.py --full` to find validated revenue methods first. Building without backtesting is how we got 428 scripts and $0 revenue.
22. **ZERO FAKES** — NEVER create stub/mock/fake implementations that appear functional but aren't. This includes: fake purchase services that simulate payment without RevenueCat/Stripe, mock API calls with hardcoded responses, `setTimeout()` pretending to be network requests, functions returning `true`/`false` without checking real state, services with `// TODO: implement`. If a real SDK is required (RevenueCat, Stripe, AdMob, any payment/auth), either implement it REAL with `react-native-purchases`/`@stripe` SDKs calling actual APIs with actual API keys from `.env`, or leave an **obvious error state** that says `NOT IMPLEMENTED — connect [service] before shipping`. NEVER make it look like it works when it doesn't. NEVER use `setTimeout(resolve, 2000)` to simulate a purchase flow. NEVER return `{ isPremium: false }` from a function that should be checking RevenueCat entitlements. This is fraud. Every incident logged in `OPS/TIME_WASTE_INCIDENT_LOG.md`. Violation = P0 defect, drop everything and fix.
23. **VERIFY REAL** — Before claiming any feature "works": (a) run it, (b) check the actual output, (c) confirm real data flows end-to-end. "The code looks correct" is NOT verification. "I ran it and saw [specific output]" IS verification. Payment flows require EXTRA scrutiny — verify the SDK is actually imported (not mocked), the API key is read from env (not null), and `purchasePackage()` calls the real SDK (not a setTimeout). See `.claude/rules/end-to-end-verification.md`.
24. **APP STORE READY** — Before ANY iOS app is declared "done": (a) RevenueCat purchases are REAL SDK calls not stubs, (b) content gating ENFORCED in code (free users ACTUALLY blocked from premium features, not just shown a paywall they can dismiss), (c) privacy policy URL resolves, (d) camera/biometric permission strings are specific (not generic), (e) no placeholder text anywhere, (f) `ITSAppUsesNonExemptEncryption` set, (g) bundle IDs unique, (h) subscription terms displayed per Apple 3.1.1/3.1.2, (i) minimum useful functionality without subscription, (j) `npx expo export --platform ios` passes clean, (k) app name doesn't clash with existing popular apps. See `OPS/APP_STORE_CHECKLIST.md`.

26. **NEVER ENSHITTIFY** — When user requests top quality, DELIVER top quality. No silent downgrades. No falling back to lower-quality alternatives without explicitly saying so and getting approval. If the best approach fails, try harder or use `/debug` mode — don't quietly switch to a worse version. This applies to: assets (use best available model, not placeholder generators), code (don't stub what should be real), UX (don't simplify what should be premium). If stuck for >5 minutes on the same problem, use `/debug` (Debugger Mode) — systematic 8-step diagnosis, not random retries. Never waste >10 minutes on circular approaches. If approach A fails 3 times, switch to approach B, don't retry A a 4th time.
27. **ASSET GENERATION WORKFLOW** — For app assets (icons, splash, screenshots): (a) Pollinations.ai for quick free generation (`curl -sL -o file.png "https://image.pollinations.ai/prompt/PROMPT?width=1024&height=1024&nologo=true&seed=42"`). Rate limit: 1 concurrent request, wait 30s between. (b) For top-tier quality: Google ImageFX via Chrome MCP (Imagen 4 model). Known issue: Chrome MCP downloads blocked — use hex extraction method (dash-separated hex passes MCP filter). (c) Gemini API key is FREE tier — no image generation. Needs paid Google AI plan for Imagen API access. (d) Always generate assets BEFORE testing in simulator. (e) Pillow for resize/crop/composite post-processing. (f) NEVER ship Pillow-drawn geometric shapes as production app icons.
28. **DEBUGGER MODE** — When stuck on ANY problem for >5 minutes: run `/debug`. Follow the 8-step protocol from `hyper rat soft engin.rtf`. Never guess fixes before diagnosis. Never retry the same failing approach more than 3 times. Log every failed approach so you don't repeat it.
29. **NEVER DEFER** — Complete tasks in the SAME session. Never say "next session priorities" or "we'll handle this later" or "moving on when you're ready." If there are remaining work items, DO THEM NOW. Agentic engineers complete tasks in minutes, not across sessions. The only valid reason to defer is: (a) waiting on a human action (account creation, payment), (b) context window is genuinely exhausted, (c) user explicitly says stop. "It's getting long" is not a reason. "I already summarized the status" is not a reason. If work remains and you CAN do it, DO IT.
30. **COMPUTER USE FOR QA** — Claude Code has a built-in `computer-use` MCP server (Pro/Max, macOS). Use it to self-audit apps: open iOS Simulator, tap through screens, screenshot every state, file bugs. Use this for ALL app factory QA instead of manual "looks good" claims. **Security guardrails for computer-use:** (a) ONLY request access to apps needed for the task (Simulator, Terminal, Xcode - never browsers, email, messages), (b) NEVER open minimized/hidden windows - work only in what's already visible, (c) NEVER read, screenshot, or interact with any window showing personal data, passwords, messages, or email, (d) if an unexpected window/dialog appears with personal content, immediately stop and tell the user, (e) NEVER type passwords or sensitive data into any field, (f) prefer `xcrun simctl` commands over computer-use clicks when both work (faster, no screen recording needed), (g) use computer-use for what xcrun CAN'T do: tapping specific UI buttons, scrolling through content, testing touch interactions, verifying visual layout, (h) batch predictable sequences with `computer_batch` to minimize round-trips, (i) always take a screenshot AFTER a batch to verify the result, (j) Esc aborts immediately if anything looks wrong.
31. **ZERO SIMULATED DATA** — NEVER use Math.random(), simulated readings, fake sensor data, or mock biometric values in any app that claims to use real sensors. If the camera API can't provide real frame data, use a REAL camera API that can (react-native-vision-camera, not expo-camera). If voice analysis needs real audio features, use a REAL audio processing library (react-native-pitch-detector, not estimated values from metering levels). The ENTIRE point of our apps is that competitors are fake. If our apps also use fake data behind a real-looking UI, we ARE the competitors we're trashing. Simulated data is ONLY acceptable as a clearly-labeled "DEMO MODE" with a visible banner, never as the default experience. Every sensor reading shown to the user must come from an actual sensor. Every percentage, score, or metric must be computed from real measurements. "It's hard to get real frame data" is not an excuse — use the library that provides it. This applies to ALL apps, not just TruthScope.
32. **APPLE WATCH + WEARABLE INTEGRATION** — When building health/biometric apps, always check if Apple Watch APIs can provide additional real data: heart rate (HKQuantityType), HRV (HKQuantityType), blood oxygen SpO2 (HKQuantityType, available on Series 6+ and Ultra), skin temperature, respiratory rate, wrist temperature during sleep. Use HealthKit via `react-native-health` or `expo-health-connect`. Apple Watch provides medical-grade continuous HR monitoring that phone cameras can't match. If user has an Apple Watch, prefer its data over phone-camera PPG. Blood oxygen sensor: Apple re-enabled SpO2 on Series 10 and Ultra 2 (was disabled on Series 9/Ultra 1 due to Masimo patent dispute, resolved late 2025). Check device model before offering SpO2 features.

25. **DASHBOARD VERIFY** — After ANY change to `control_panel.py` or `control_panel.html`: (a) `python3 -c "import py_compile; py_compile.compile('AUTOMATIONS/control_panel.py')"` must pass, (b) restart dashboard and test ALL new/changed endpoints with `curl`, (c) verify frontend loads without JS console errors by checking all fetch URLs match actual backend routes, (d) every `getElementById` in JS must have a matching `id=` in HTML. Frontend URL must match backend `@app.route` exactly. No endpoint mismatches.
33. **RESEARCH BEFORE BUILD** — Before building ANYTHING from scratch, spend 5 minutes searching for existing high-quality solutions: (a) GitHub templates/boilerplates with stars >500 (search "expo template onboarding paywall" not "how to make react native app"), (b) open-source asset libraries (Octave for iOS sounds, Kenney for UI audio, Google Material Design sounds, Sonniss GDC bundles), (c) production-grade starter kits that already have onboarding, paywalls, sound design, dark themes, and best practices baked in, (d) npm/pip packages that solve the exact problem. NEVER default to building from scratch when a battle-tested solution exists. NEVER generate assets programmatically (Python sine waves, Pillow geometric shapes) when professional open-source alternatives exist. The goal is to START from the highest quality baseline, then customize. Building from `create-expo-app --template blank` when a 2,000-star template with Cal AI onboarding exists is wasted effort. This applies to EVERYTHING: apps, scripts, configs, assets, content templates, email sequences. Search first, build second. If nothing exists, THEN build. Log what was searched and why building from scratch was chosen.

This is NOT "blindly use the first template you find." Use discretion:
- Check multiple repos. Compare them. Pick the best parts from each.
- If an existing template is 80% of what we need, start from it and customize the 20%.
- If nothing existing matches our quality bar, THEN build from scratch — but document why.
- Hybrid assembly is the default: best onboarding from repo A, best payment flow from repo B, best sound design from library C, custom finish on top.
- Don't add customization just to add it. If the existing solution is already better than what we'd build, use it as-is.
- This applies to EVERYTHING, not just apps: scripts, automation configs, landing pages, email templates, legal docs, pitch decks, content strategies. Always check if someone already solved this at a higher quality than we'd one-shot.
- Building from scratch is VALID when: our alpha/intel gives us an edge public repos don't have, existing repos are severely outdated or low quality, our specific requirements genuinely aren't met by anything available, or one-shotting it produces a better result faster than adapting a mediocre template. The point is to LOOK first, then make an informed decision — not to force-use a repo for the sake of it.

## Guardrails (for THIS project only)
When working in this PRINTMAXX project, file ops stay within: `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/`
This does NOT restrict other projects. See `.claude/rules/guardrails.md` for details.

## Session End
1. Update `OPS/PERSISTENT_TASK_TRACKER.md` + `OPS/SESSION_LOG.md`
2. Generate content (Rule 9). Surface human blockers with time estimates.
3. If agents/cron/architecture/data-flow changed → update `OPS/PRINTMAXX_SYSTEM_MAP.md` THIS session. No stale maps.
4. If new resources/playbooks/tools/products created or discovered → update `OPS/RESOURCE_MANIFEST.md` AND rerun `python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report` (Rule 16). No stale scores.

## Mindset
> Use every tool. Every shortcut. Every hack. Every legal advantage. Compete like your life depends on it.
> $0 → $1K → $10K → $50K → $200K+ → hedge fund capital management.
