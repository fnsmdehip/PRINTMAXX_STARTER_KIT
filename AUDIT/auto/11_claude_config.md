# Audit: Claude Code meta-config
**Date**: 2026-05-15
**Scope**: `.claude/`, `skills/`, `scripts/`, `.superpowers/`, `.qodo/`, `.ralph/`, `.firecrawl/`, `.playwright-mcp/`, `.guardrails/`

---

## 1. `settings.json` summary (keys + structure, no secrets)

`/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/.claude/settings.json` (165 lines, redacted summary):

```
env:
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"
  LETTA_BASE_URL = "http://localhost:8283"
  LETTA_API_KEY  = <redacted>
  LETTA_MODE     = "full"
  LETTA_AGENT_ID = <redacted>
model: "opus"
permissionMode: "acceptEdits"
hooks:
  SessionStart  [7 commands]
  PreToolUse    [3 matchers: Write|Edit, AskUserQuestion|ExitPlanMode, *]
  UserPromptSubmit  [2 commands]
  PostToolUse   [Edit|Write, 5 commands]
  PreCompact    [1 command — save_context_snapshot.py]
  Stop          [2 commands]
```

`settings.local.json` (308 lines) — **stale paths bug**. Almost every allowlisted Bash/Edit/Write/Read permission references the old project root `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/` (single, no `ttttt` suffix). The current working directory is `…/PRINTMAXX_STARTER_KITttttt/` (with `ttttt`). This means most cached permission entries don't actually match against the current path, so the user is getting more permission prompts than they think.

---

## 2. Slash command catalog (19 commands) — purpose + invocation style

| Command | Model | Args | Purpose |
|---|---|---|---|
| `/printmaxx` | (default) | — | Session-startup loader. Reads HANDOFF, MASTER_TASKS, ALPHA_STAGING, GTM, then asks "what do you want to tackle?" |
| `/parallel-launch` | (default) | `content\|full\|research` | Launch 2-4 sub-agents in parallel; preset configs (Content Blitz, Full Stack, Research Mode). |
| `/loops` | (default) | `status\|fix\|cycle\|decisions\|feedback\|pipeline\|drift` (default `status`) | Routes via $ARGUMENTS into `python3 AUTOMATIONS/loop_closer.py --<sub>`; has full Fix Protocol per loop. |
| `/rbi` | (default) | `research\|backtest\|implement\|full\|status\|top N` | Routes into `AUTOMATIONS/rbi_loop.py`; PASS methods get implemented, CONDITIONAL → actionable queue. |
| `/health` | (default) | — | Runs 6 health scripts in parallel (system_health_monitor, loop_closer, cron_watchdog, venture_autonomy, rbi_loop, revenue check), unified dashboard. |
| `/status` | sonnet | — | Apps/content/accounts/metrics + loop health + RBI status + cron health. |
| `/refine` | opus | `<path> [num_cycles=3]` | Hybrid cognitive refinement: Phase 0 backup, Phase 1 load voice model + meta-rules + bias-null, Phase 2 cognitive_engine lookup, Phase 3 N cycles with live meta-rule lenses, Phase 4 review, Phase 5 approve/revert, Phase 6 self-update. Most sophisticated command. |
| `/edge` | opus | `<target> [num_cycles=3]` | Competitive edge: Baseline audit → synergy mining → MEV extraction. WebSearch in Cycle 1. |
| `/debug` | (default) | — | 8-step Debugger Mode protocol (5-7 hypotheses → distill → diagnostic logs → check logs → analysis → fix → cleanup). |
| `/daily-research` | haiku | `--platform --tier --dry-run` | Scans HIGH_SIGNAL_SOURCES.csv, stages alpha as PENDING_REVIEW. |
| `/review-alpha` | sonnet | — | Reviews PENDING_REVIEW, routes APPROVED to APP_FACTORY/MARKETING/CONTENT/TOOLS CSVs. |
| `/run-alpha-extractor` | (default) | `--dry-run --platform --tier` | Runs `AUTOMATIONS/daily_alpha_extractor.py`. |
| `/brand-names` | sonnet | — | Generates branded account names for 3-niche system. |
| `/generate-longtail` | haiku | `[count=10]` | Bulk SEO longtail page gen. Every 10th page goes through Sonnet quality review. |
| `/generate-posts` | haiku | `--niche --count --platform` | 3-niche social post bulk generation. |
| `/remotion-video` | (default) | — | Pointers into `.claude/remotion-skills/skills/remotion/rules/` for Remotion video compositions. |
| `/deploy-check` | sonnet | — | Pre-deploy checklist for `LANDING/printmaxx-site` (build, env, perf, SEO, compliance). |
| `/validate` | sonnet | — | Validation suite (content, code, LEDGER, compliance). |
| `/warmup-sop` | sonnet | `--platform --niche` | Generate platform-specific account warmup SOPs. |

---

## 3. Agent catalog (38 agents) — purpose + model + tools

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| content-generator | sonnet | Read, Write, Grep, Bash | SEO truth pages + longtail pages, copy-style.md compliance. |
| deployer | haiku | Read, Bash, Grep | Pre-deploy checklist + rollback. |
| design-brand / design-motion / design-ui | sonnet | std | Visual identity + motion + UI design. |
| eng-backend | sonnet | Read, Write, Edit, Bash, Grep, Glob | Python scripts, pipelines, cron, CLI tools. |
| eng-devops / eng-frontend / eng-fullstack / eng-mobile | sonnet | std | Specialized engineering. |
| mkt-affiliate / mkt-content / mkt-email / mkt-growth / mkt-seo / mkt-social | sonnet | std | Marketing specializations. |
| pm-compliance / pm-quality / pm-sprint / pm-task | sonnet | std (no Bash on pm-task) | Compliance, quality, sprint coord (decomposition + parallel), task tracker. |
| prod-analyst / prod-designer / prod-manager / prod-researcher | sonnet/opus | std | Product lifecycle. |
| research-competitor | sonnet | + WebSearch, WebFetch | Competitive intel. |
| research-market | **opus** | + WebSearch, WebFetch | Market sizing, demand validation. Highest-tier model. |
| reviewer | sonnet | Read, Grep, Bash | Code review (no Write — read-only review agent). |
| studio-alpha | **opus** | Read, Write, Edit, Bash, Grep, Glob | Alpha scoring + routing. Strictest skepticism. |
| studio-deploy / studio-monitor / studio-pipeline / studio-quant / studio-scraper / studio-security | sonnet | std | Studio ops. |
| test-e2e / test-integration / test-perf / test-unit | sonnet / haiku | std | Test specializations. |
| validator | **haiku** | Read, Grep, Bash | Fast/cheap validation gate. |

Frontmatter is consistent: `name`, `description`, `tools`, `model`. No `color` field is used in any of these agents.

Model distribution: **2 opus** (studio-alpha, research-market), **~32 sonnet**, **~4 haiku** (validator, deployer, daily-research, generate-longtail/posts via slash, plus a few tests).

---

## 4. Hooks configured (event → script → purpose)

| Event | Matcher | Script | Purpose | Timeout |
|---|---|---|---|---|
| SessionStart | `*` | `AUTOMATIONS/session_cron_check.sh` | Verify cron jobs alive | 5s |
| SessionStart | `*` | `AUTOMATIONS/subconscious/session_start_injector.sh` | Inject memories from `.jsonl` store | 10s |
| SessionStart | `*` | `AUTOMATIONS/hooks/check_cron_critical_agents.sh` | Critical agent health check | 5s |
| SessionStart | `*` | `AUTOMATIONS/session_briefing.py --save` | Generate `OPS/SESSION_BRIEFING.md` | 25s |
| SessionStart | `*` | `AUTOMATIONS/launch_control_panel.sh` | Auto-launch localhost:9999 dashboard | 8s |
| SessionStart | `*` | `claude-subconscious/scripts/session_start.ts` (plugin) | Plugin: session start | 10s |
| SessionStart | `*` | `claude-subconscious/scripts/sync_letta_memory.ts` (plugin) | Plugin: sync Letta memory | 15s |
| PreToolUse | `Write\|Edit` | `AUTOMATIONS/hooks/validate_path.sh` | **Guardrail** — block writes outside project | 5s |
| PreToolUse | `AskUserQuestion\|ExitPlanMode` | `claude-subconscious/scripts/plan_checkpoint.ts` | Save plan to checkpoint | 10s |
| PreToolUse | `*` | `claude-subconscious/scripts/pretool_sync.ts` | Plugin: pre-tool sync | 5s |
| UserPromptSubmit | `*` | `AUTOMATIONS/hooks/log_user_prompts.sh` | **Prompt logger** → `LEDGER/USER_PROMPTS.jsonl` | 3s |
| UserPromptSubmit | `*` | `claude-subconscious/scripts/sync_letta_memory.ts` | Plugin: sync memory on prompt | 10s |
| PostToolUse | `Edit\|Write` | `AUTOMATIONS/hooks/py_compile_check.sh` | Auto-compile Python after edit | 10s |
| PostToolUse | `Edit\|Write` | `AUTOMATIONS/hooks/secret_detector.sh` | Block committed secrets | 5s |
| PostToolUse | `Edit\|Write` | `AUTOMATIONS/hooks/check_safe_path_discard.py` | Path validation post-write | 5s |
| PostToolUse | `Edit\|Write` | `AUTOMATIONS/hooks/check_file_handle_leaks.py` | Leak check | 5s |
| PostToolUse | `Edit\|Write` | `AUTOMATIONS/hooks/check_type_hints.py` | Type-hint enforcement | 5s |
| **PreCompact** | `*` | `AUTOMATIONS/hooks/save_context_snapshot.py` | **Save state before compaction** (30% less info loss) | 10s |
| Stop | `*` | `AUTOMATIONS/subconscious/session_end_processor.sh` | Extract memories via `claude -p` | 15s |
| Stop | `*` | `claude-subconscious/scripts/send_messages_to_letta.ts` | Plugin: ship messages to Letta on stop | 15s |

20 total hooks. The user memory's claim about "guardrail + prompt logger + PreCompact" is confirmed — plus a lot more (subconscious memory loop into Letta, file-handle/type-hint checks, secret detector).

---

## 5. Local skills / skill dirs

- **`/skills/`** (top-level, project-local) — 5 skills, each just a `SKILL.md`:
  - `printmaxx-alpha-processor/SKILL.md` (11K)
  - `printmaxx-ceo-orchestrator/SKILL.md` (10K) — describes 16-phase CEO cycle
  - `printmaxx-compliance-scanner/`
  - `printmaxx-intelligence-router/SKILL.md` (8K)
  - `printmaxx-revenue-tracker/`
- **`.claude/remotion-skills/`** — a full sub-package (Remotion + skills + src + tsconfig + own `.git`)
- **`.claude/reference/`** — alpha-review.md (14K), copy-style.md (17K), code-style.md, performance.md, external-code-security.md (load-on-demand pointers from CLAUDE.md)
- **`.claude/rules/`** — 20 always-active rule files (anti-entropy, app-factory-pipeline, auto-integration, bias-null, deep-thinking-dedup, edge-mindset, end-to-end-verification, guardrails, payment-integration, reprocess-on-discovery, security, sovrun-sync, system-map-maintenance, etc.). All auto-loaded each session per system reminder.

A **massive ecosystem of plugin skills** is also live via Claude Code plugin cache (~85 skills shown in system reminder): superpowers (brainstorming, writing-plans, dispatching-parallel-agents, executing-plans, subagent-driven-development, systematic-debugging, test-driven-development, verification-before-completion), claude-code-setup, claude-md-management, code-review, commit-commands, feature-dev, firecrawl, frontend-design, hookify, plugin-dev, posthog (40+ sub-skills), pinecone, pr-review-toolkit, ralph-loop, sentry, scheduler, simplify, slack, stripe, qodo-skills, semgrep, and the agent-sdk-dev family.

---

## 6. Plugin state (`.ralph`, `.qodo`, `.firecrawl`, `.playwright-mcp`, `.superpowers`, `.guardrails`)

- **`.ralph/`** — Ralph Loop plugin local state. Last touched Jan 24 (4 months stale). Files: `append_alpha.py`, `errors.log`, `guardrails.md`, `progress.md` (19K), 4 temp/staged CSVs. Plugin itself is wired via `ralph-loop:ralph-loop` plugin skill. Local artifacts look frozen — this is content-staging working dir, not active loop output.
- **`.qodo/`** — Empty shell (`agents/` and `workflows/` are both empty). Plugin installed, never populated.
- **`.firecrawl/`** — Just `competitor-research/` (empty). Plugin installed, no local data accumulated.
- **`.playwright-mcp/`** — **VERY active.** 138 console log files, dated Mar 7 → Apr 1. Active MCP browser session telemetry.
- **`.superpowers/`** — `brainstorm/28532-1773642541/` (one brainstorm session from Mar 16-19).
- **`.guardrails/`** — Custom internal guardrail layer (NOT a plugin). Files: `audit.jsonl`, `operations.log`, `shell_operations.log`, `checkpoints/`. This is the substrate behind the PreToolUse `validate_path.sh` hook + path-safety enforcement.

`.claude/worktrees/recursing-wescoff/` is an active git worktree containing a partial snapshot of the project (AUTOMATIONS, EMAIL, MEDIA, etc.) for parallel agent work, dated Apr 24 - May 3.

`.claude/scripts/set-path.sh` is a single-line PATH export for the Homebrew Node binary.

`.claude/external-tools.yaml` is a Codex/Gemini adapter stub — disabled, but reserved for cross-model adversarial review (writer != reviewer).

---

## 7. Patterns observed in existing commands (argument syntax, invocation, output)

**Frontmatter:**
```yaml
---
name: <slug>
description: <one-line + Usage hint with $ARGUMENTS syntax>
model: sonnet|opus|haiku  (optional — defaults to root model)
---
```

**Argument syntax (3 styles in use):**
1. **Sub-command routing** — `/loops status|fix|cycle`, `/rbi research|backtest|implement|full|status`. The command body parses `$ARGUMENTS` and dispatches via a small routing table.
2. **Positional + optional N** — `/refine <path> [num_cycles=3]`, `/edge <target> [num_cycles=3]`, `/generate-longtail [count=10]`.
3. **Flag-style passthroughs** — `/daily-research --platform X --tier HIGHEST`, `/warmup-sop --platform x --niche ai`. The command body doesn't actually parse flags — they get strung onto a downstream Python invocation.

**Bash invocation pattern:** Many commands are thin wrappers around `python3 AUTOMATIONS/<script>.py --<flag>`. The slash command's job is mainly (a) route args, (b) parse output, (c) present clean dashboard, (d) call out follow-on actions ("If PASS methods exist, run `/rbi implement`").

**Sub-agent invocation:** No command directly invokes a named sub-agent via Task tool syntax — `/parallel-launch` just describes a configuration in prose. The complex commands (`/refine`, `/edge`) phase-load context files and run inline; they don't delegate.

**Output:** Tables, status dashboards, "Issues requiring attention" lists, follow-on recommendations. CRITICAL/DEGRADED/OK severity is the implicit standard.

**Phase structure:** The advanced commands (`/refine`, `/edge`) define explicit `Phase 0`…`Phase N` sections with rules per phase. This is the right scaffold for long-running work.

---

## 8. Patterns observed in existing agents (frontmatter, tool restrictions)

**Frontmatter:**
```yaml
---
name: <slug>
description: <one-line capability statement>
tools: Read, Write, Edit, Bash, Grep, Glob   (or trimmed subset)
model: sonnet|opus|haiku
---
```

**Tool-restriction patterns:**
- **Review/audit agents** (reviewer, validator) get **no Write** — they can only Read, Grep, Bash. Prevents accidental destructive writes during code review.
- **Research agents** (research-market, research-competitor) add **WebSearch + WebFetch** to the standard set.
- **Engineering/studio agents** get the full set (Read, Write, Edit, Bash, Grep, Glob).
- **pm-task** is Read/Write/Edit/Grep/Glob (no Bash — pure file-management role).

**Model-selection logic:**
- **Opus** reserved for strategic/skeptical/high-leverage roles (studio-alpha, research-market).
- **Haiku** reserved for cheap-and-fast roles (validator, deployer).
- **Sonnet** is the default workhorse for ~80% of agents.

**Prompt structure:** Persona statement → domain bullets → patterns/standards section → "How to use me" hint → output format section → rules/quality gates. Very consistent.

**No `color` field** is used in any of the 38 agents.

---

## 9. Top 3 Risks

1. **`settings.local.json` references a stale project root.** Almost every Bash/Read/Write/Edit permission allowlists `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/**` (no `ttttt`). The current cwd is `…/PRINTMAXX_STARTER_KITttttt/`. Result: the user is hitting permission prompts that the allowlist was supposed to silence — and may have been doing so silently for the entire renamed-folder period.

2. **Heavy hook chain (SessionStart=7, PostToolUse=5) creates session-start latency budget of ~78s + per-edit overhead.** Several hooks chain to a remote Letta server on `localhost:8283`. If Letta is down, every session start waits out timeouts. The PreToolUse `validate_path.sh` is critical (guardrail), but the subconscious/Letta hooks could be made async to reduce friction.

3. **Dead/stale plugins (`.qodo` empty, `.ralph` 4-month stale, `.firecrawl` no data accumulated).** Three plugins consume slot space in the activation chain but produce no current value. The `ralph-loop:ralph-loop` plugin is wired but the local `.ralph/` state is from January. Either retire them or wire them in.

---

## 10. Top 3 Opportunities

1. **Standardize the "phase-structured long-run" command pattern.** `/refine` and `/edge` already use it (Phase 0 backup, Phase 1 load, Phase 2 lookup, Phase 3 N-cycles, Phase 4 review). This is exactly the scaffold `/goal` needs. Copy directly, including:
   - Phase 0 backup before destructive work
   - Phase 1 context loading (voice model, meta-rules, bias-null, relevant rules)
   - Phase 3 cycle structure driven by live meta-rules (not hardcoded)
   - Phase 6 self-update (write learnings back into the meta-rules feedback loop)

2. **Wire `/goal` into the existing sub-agent topology.** There are 38 specialized agents with clear domains and pm-sprint already exists as the decomposer/coordinator. `/goal` should delegate, not duplicate. Particularly: `pm-sprint` for decomposition + parallel coordination, `pm-task` for persistent tracking, `studio-pipeline` for data flow, `eng-fullstack` for cross-stack work, `reviewer` for gates, `validator` for fast Haiku checks.

3. **Leverage the resilience scaffolding already in place.** PreCompact hook + checkpoint-resume (CycleCheckpoint in CEO agent) + agent_resilience.py + cron_watchdog + `OPS/active-tasks.md` (crash-recovery file) are all available. A long-running `/goal` should write a checkpoint each phase to `OPS/goal_checkpoint_<id>.json` and resume gracefully on compact or crash.

---

## 11. For the `/goal` long-run command — CRITICAL

### What design patterns from existing commands should `/goal` copy?

- **Phase-structured body** (from `/refine`, `/edge`): explicit `Phase 0` backup/setup, `Phase 1` context load, `Phase 2` intelligence lookup, `Phase 3` cycle/iteration, `Phase 4` review, `Phase 5` resolution, `Phase 6` self-update. This already won out twice as the right scaffold for long work.
- **Sub-command routing table** (from `/loops`, `/rbi`): support `/goal new|status|resume|pause|cancel <id>` so a user can manage a running goal without typing the whole goal again.
- **Live meta-rule lenses** (from `/refine`): read `OPS/prompt_intelligence/comprehensive_meta_rules.md` and `OPS/USER_VOICE_MODEL.json` at Phase 1, use them to shape iteration. Don't hardcode lenses.
- **Bias-null filter pass** (from `/refine`, `/edge`, the global rule): silently apply the 5-point bias-null filter before each major claim/output.
- **Backup + approve/revert resolution** (from `/refine` Phase 0+5): if the goal involves destructive edits, snapshot first; final step asks for approve/revert.
- **WebSearch in Cycle 1** (from `/edge`): if the goal involves anything novel, web-search current state-of-the-art before iterating internally.

### Which existing agents should `/goal` delegate to?

| Role in `/goal` | Delegate to |
|---|---|
| Plan decomposition + parallel coord | `pm-sprint` (this is its job) |
| Persistent task tracking | `pm-task` |
| Data/pipeline work | `studio-pipeline` |
| Backend builds | `eng-backend` |
| Frontend/full-stack | `eng-fullstack`, `eng-frontend` |
| Research before build | `research-market`, `research-competitor` |
| Alpha review/integration | `studio-alpha` |
| Content output (Rule 9) | `content-generator`, `mkt-content`, `mkt-social` |
| Mid-flight quality gate | `validator` (Haiku, fast/cheap) |
| Final review | `reviewer` (Sonnet, deeper) |
| Deploy step | `studio-deploy`, `deployer` |

The `/goal` command should NOT do work directly — it should be an orchestrator that delegates each phase's work to the right specialist agent and aggregates output.

### How should `/goal` handle long-running execution?

- **Background tasks via `run_in_background: true`** for any sub-agent run >5 min (pattern already in pm-sprint).
- **Checkpoint per phase** to `OPS/goal_checkpoints/<goal_id>.json` with `{phase, status, sub_agent_id, started_at, last_heartbeat, artifacts}`. Mirror the `CycleCheckpoint` pattern from `ceo_agent.py` (atomic write, stale detection, resume-on-crash).
- **PreCompact hook coverage** — the existing `save_context_snapshot.py` will fire automatically before compaction. `/goal` should also write its own phase state to the checkpoint at every major step so a fresh session can resume via `/goal resume <id>`.
- **Heartbeat** to `OPS/active-tasks.md` (crash-recovery file already in the system) every phase boundary.
- **Wall-clock budget** — set a per-phase timeout (default 30 min, configurable). On timeout, mark phase as STUCK in checkpoint, surface to user, don't loop silently. Rule 28 (DEBUGGER MODE) says: stuck for >5 minutes → switch approach; don't retry the same failing approach more than 3 times.
- **Token budget tracking** — write tokens-used per phase to checkpoint. Stop autonomously approaching limits and write a clean resume point per the prompt logger / context-snapshot pattern.

### Argument syntax — should `/goal` take args? Sub-commands? Just run?

Hybrid:
- `/goal <free-form goal description>` — start a new goal. Auto-generates `goal_id`, runs Phase 0.
- `/goal status [id]` — show progress of running goals (or the most recent if no id).
- `/goal resume <id>` — pick up from last checkpoint.
- `/goal pause <id>` — graceful pause, checkpoint, exit.
- `/goal cancel <id>` — abort + cleanup.
- `/goal list` — recent goals + status.

Default with no args: list active goals + ask "new goal?".

Goal description should be free-form; the command parses it into an Intent + Success Criteria internally via the `pm-task` priority-scoring framework (Revenue 40%, Blocking 25%, Effort 20%, Strategic 15%).

### Output format — final report? Stream as it goes?

**Both**, with the bias toward stream-as-it-goes per the user-memory note: "user won't read reports — system consumes its own reports and acts."

- **Stream per-phase summary** to stdout as the command runs: `[Phase 1/N] [agent: pm-sprint] [status: complete] [duration: 4m12s] [next: Phase 2]`.
- **Write detailed phase outputs** to `OPS/goal_runs/<goal_id>/phase_<N>.md` so subsequent sessions or agents can consume them.
- **Final concise summary** at the end: what was achieved, what's blocked, what's the recommended next `/goal` (or other command), and any human-action blockers with time estimates (Rule 8: NEVER DROP THE BALL, Rule 11: surface human blockers).
- **Rule 9 — Max Squeeze** — every `/goal` run automatically generates 3 tweets + 1 thread about the session and writes them to `CONTENT/social/posting_queue/`. Free Content squeeze.
- **NO orphan documents** — every artifact `/goal` writes must have a documented consumer (an agent, a cron, or a human task). Rule 2.

### Critical guardrails for `/goal`

- Honor Rule 17 (NO DEAD CODE): if `/goal` proposes a new script, it must be tested, wired, and called in the same session.
- Honor Rule 23 (VERIFY REAL): every phase's claim of "done" must be backed by actual file/URL/output verification, not vibes.
- Honor Rule 29 (NEVER DEFER): goals shouldn't span sessions unless the user explicitly stops or context truly exhausts.
- Honor Rule 33 (RESEARCH BEFORE BUILD): in any "build" goal, Phase 1 must search GitHub/n8n/template repos for >500-star existing solutions before generating new code.
- Honor the always-active rules at `.claude/rules/` (anti-entropy, deep-thinking-dedup, end-to-end-verification, bias-null, auto-integration, sovrun-sync, reprocess-on-discovery).
