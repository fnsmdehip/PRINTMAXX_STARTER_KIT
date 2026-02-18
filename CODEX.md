# PRINTMAXX CODEX OPERATING CONTRACT

Purpose: run PRINTMAXX 24/7 with strict blast-radius controls.

## Operator Intent Defaults (Persistent)

- Universal expansion default:
  - For every operator task, expand scope to the maximum aligned execution set across adjacent methods, channels, and workflows.
  - Do this even when not explicitly requested with keywords like `etc`.
  - Treat explicit examples as minimum scope, not final scope.
  - Maintain forward momentum by continuously adding compatible high-ROI lanes while preserving risk gates.
- `etc` means full adjacency expansion:
  - When operator names examples (for example `eBay, Etsy, Redbubble, Amazon`), treat them as a seed set.
  - Automatically expand to the full comparable opportunity surface (similar marketplaces/channels/workflows) without waiting for reprompt.
  - Build and maintain ranked queues for all adjacent options, not just explicitly named items.
  - Treat shorthand like `etc`, `and so on`, `same type`, `similar`, `whatever else`, as a standing instruction to extrapolate all materially similar revenue channels and operational lanes.
  - Avoid narrow literalism; infer the meta intent and execute the broad high-ROI set by default.
- Execute-first behavior:
  - Default to implementation and live execution, not instruction-only responses.
  - Only pause for human-in-loop on compliance, payment, KYC/account verification, or destructive/high-risk actions.
  - Do not require repeated prompting for obvious next steps inside an active lane; continue chaining execution until a gate is reached.
- No hand-holding mode:
  - Infer obvious next steps from system state and continue advancing the pipeline autonomously.
  - If blocked, create explicit unblock artifacts (queue items, required credential keys, exact next command) and keep all other lanes running.
  - Keep response verbosity low while work is running; prioritize shipped artifacts and status proofs over planning prose.
- Portfolio expansion:
  - Continuously scan for additional monetizable channels that match the current method class (marketplaces, launch directories, freelance channels, outbound channels, app/web distribution).
  - Add discovered channels into ledgers/queues with readiness and ROI scoring.
  - Maintain an "opportunity frontier" list so newly discovered channels are automatically tested in low-cost probes, then promoted to scale when KPI thresholds are hit.
- Master Ops `etc` execution:
  - Treat `PRINTMAXX_MASTER_OPS_ENHANCED_*.xlsx` as a live expansion surface.
  - Update `ETC_EXPANSION_QUEUE` on each enhancement run and prioritize highest-score adjacent ops automatically.

## Node Roles

- `control` node:
  - Main MacBook (64GB).
  - Used for coding, approvals, and supervision.
  - Must NOT execute critical revenue actions.
- `worker` node:
  - Sandbox machine (M2 16GB is acceptable).
  - Executes live deploy/send actions after approvals.

Role source of truth:
- `OPS/NODE_ROLE.json`

## Guardrails

- Human approval required for:
  - `DEPLOY_APPS`
  - `DEPLOY_STATIC_SITES`
  - `LIVE_EMAIL_SEND`
- Live email sends require `EMAIL_INFRA` to be configured (CAN-SPAM footer + sender creds).
- Critical actions are hard-blocked on non-worker nodes.
- Compliance scans run continuously and are used as gates for risky actions.
- Runtime model routing is budget-first via:
  - `OPS/STACK_POLICY.json`
  - `AUTOMATIONS/stack_governor.py`

## Runtime Loop

- Primary runner: `AUTOMATIONS/ship_captain.py`
- Launcher: `ship.sh`
- Queue and approvals:
  - `OPS/HUMAN_LOOP_QUEUE.md`
  - `OPS/HUMAN_APPROVALS.csv`
- GUI status panel:
  - `output/dashboard/index.html` (auto-refresh)

## Agent Navigation (2026-02-18 Refresh)

Use this order when entering the system:

1. Core operating contract:
   - `CODEX.md`
2. Live gates and blockers:
   - `OPS/HUMAN_LOOP_QUEUE.md`
   - `OPS/HUMAN_APPROVALS.csv`
   - `OPS/NODE_ROLE.json`
3. Official OpenClaw + worker isolation runbook:
   - `OPS/OPENCLAW_WORKER_ISOLATION_RUNBOOK_2026_02_18.md`
   - `OPS/openclaw/openclaw_worker_template.json5`
   - `scripts/setup_control_to_worker_ssh.sh`
   - `scripts/setup_openclaw_worker_stack.sh`
   - `AUTOMATIONS/openrouter_budget_guard.py`
   - `OPS/OPENROUTER_BUDGET_POLICY.json`
   - `external/openclaw-official/README.md`
4. Runtime health and lane outputs:
   - `OPS/STACK_HEARTBEAT.md`
   - `OPS/HUMAN_EXECUTION_BRIEF.md`
   - `output/cron_fleet/latest.md`
5. ClawWork sidecar controls:
   - `OPS/CLAWWORK_SIDECAR_POLICY.json`
   - `OPS/CLAWWORK_MINIMAL_SIDECAR_PLAN.md`
   - `output/clawwork_sidecar/latest.md`
   - `LEDGER/CLAWWORK_SIDECAR_RUNS.csv`
6. Local voice stack (Qwen3-TTS):
  - `OPS/QWEN3_TTS_LOCAL_STACK.md`
  - `scripts/setup_qwen3_tts_local.sh`
  - `scripts/qwen3_tts_longform.sh`
  - `scripts/approved_voice_runner.sh`
  - `AUTOMATIONS/qwen3_tts_longform.py`
  - `AUTOMATIONS/approved_script_voice_runner.py`
  - `OPS/VOICEOVER_APPROVED_QUEUE.csv`
  - `LEDGER/VOICE_RENDER_RUNS.csv`
  - `output/qwen_tts/`
7. Full-context audit corpus + Meta Vision:
  - `AUDIT/META_VISION.md` (historical baseline)
  - `AUDIT/META_VISION_2026_02_16.md` (swarm metrics sweep)
  - `AUDIT/META_VISION_2026_02_17_AUTOMATION.md` (automation upgrade pass)
  - `AUDIT/META_VISION_2026_02_18_OPENCLAW_WORKER_INTEGRATION.md` (official OpenClaw + worker isolation addendum)
  - `AUDIT/META_VISION_FULL_CONTEXT_2026_02_16.md` (raw-corpus-linked update)
  - `AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv` (full file/folder inventory)
8. Alpha pipeline (Feb 18 — auto-scrape → auto-process → auto-route):
   - `AUTOMATIONS/daily_research_orchestrator.py` (5 scrapers + HN + 41 subs + PH, daily 5 AM)
   - `AUTOMATIONS/twitter_bookmarks_scraper.py` (Brave cookies → bookmarks → alpha, daily 6 AM)
   - `AUTOMATIONS/alpha_review_bot.py` (PENDING_REVIEW backlog processor, daily 6 AM)
   - `AUTOMATIONS/alpha_auto_processor.py` (routes alpha → ventures/OPS/cron/archive, daily 6:30 AM)
   - `AUTOMATIONS/competitor_monitor.py` (19 apps, 6 niches, iTunes API, daily 7 AM)
   - `AUTOMATIONS/app_store_competitor_tracker.py` (36 apps, change detection, daily 7 AM)
   - `AUTOMATIONS/trend_scanner.py` (Google Trends + App Store + Gumroad + Reddit, weekly Mon 6 AM)
   - `AUTOMATIONS/gumroad_niche_scanner.py` (9 niches, scored signals, daily 8:30 AM)
   - `AUTOMATIONS/ralph_loop_fixer.py` (ralph loop health scanner)
   - `AUTOMATIONS/new_cron_entries.txt` (15 new cron entries, installed Feb 18)
   - `AUDIT/ALPHA_INTEGRATION_GAP_ANALYSIS.md` (68 wired vs 349 orphaned findings)
   - `AUDIT/EXISTING_AUTOMATION_INVENTORY.md` (166+ scripts cataloged)
   - `OPS/playbooks/ALPHA_INTEGRATION_PLAYBOOKS.md` (20 playbooks, 5-phase plan)
   - `AUDIT/ALPHA_SCAN_OPS_DEEP.md` (22,848 lines, 417 entries)
   - `AUDIT/MASTER_ALPHA_SCAN_CONSOLIDATED.md` (2,250 lines, 36 sections)
9. Worker setup:
   - `scripts/worker_mega_installer.sh` (one-script full M2 setup)
   - `scripts/worker_health_check.sh` (verify worker readiness)
10. Master Ops intelligent execution layer:
  - `PRINTMAXX_MASTER_OPS.xlsx` (source)
  - `PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-17.xlsx` (live enhanced clone)
  - `AUTOMATIONS/master_ops_enhancer.py`
  - `AUTOMATIONS/master_ops_executor.py`
  - Enhanced sheets to drive automation:
    - `PRIORITY_AUTOMATION_EXEC`
    - `ETC_EXPANSION_QUEUE`
    - `DEEP_PLAYBOOK_INDEX`
    - `ALPHA_THESIS_INDEX`
    - `VENTURE_AUTOMATION_MAP`

## Swarm Audit Commands

- Full-content corpus rebuild:
  - `python3 AUTOMATIONS/full_context_swarm_dump.py --write --workers 10 --chunk-chars 5000 --max-records-per-shard 2500 --compress-shards --dedupe-content`
- Metrics/meta sweep:
  - `python3 AUTOMATIONS/meta_vision_swarm_audit.py --write --tag 2026_02_16`
- Master Ops workbook enhancement:
  - `python3 AUTOMATIONS/master_ops_enhancer.py`
- Master Ops execution planning (safe):
  - `python3 AUTOMATIONS/master_ops_executor.py --top 12 --max-per-lane 3`
- OpenRouter key budget guard (dry-run):
  - `python3 AUTOMATIONS/openrouter_budget_guard.py --enforce --dry-run`
- OpenRouter key budget guard (live):
  - `python3 AUTOMATIONS/openrouter_budget_guard.py --enforce`
- OpenRouter key status:
  - `python3 AUTOMATIONS/openrouter_budget_guard.py --status`
- Control -> worker SSH bootstrap:
  - `bash scripts/setup_control_to_worker_ssh.sh <user@worker-host> <worker_project_path>`
- Worker stack bootstrap (official OpenClaw + worker role):
  - `bash scripts/setup_openclaw_worker_stack.sh`
- Worker stack bootstrap + onboarding:
  - `bash scripts/setup_openclaw_worker_stack.sh --run-onboard`
- Local Qwen3-TTS setup:
  - `bash scripts/setup_qwen3_tts_local.sh`
  - `DOWNLOAD_MODEL=1 bash scripts/setup_qwen3_tts_local.sh`
- Local longform voice render:
  - `bash scripts/qwen3_tts_longform.sh --text-file <path_to_script_txt> --speaker aiden --language English --out output/qwen_tts/longform.wav`
- Approved-script voice sidecar (dry run):
  - `python3 AUTOMATIONS/approved_script_voice_runner.py --dry-run`
- Approved-script voice sidecar (live):
  - `bash scripts/approved_voice_runner.sh --max-jobs 2 --max-blocks-per-source 1`

## Scheduling

Use only secure minimal cron:
- `AUTOMATIONS/crontab_secure_minimal.txt`

Installer:
- `scripts/install_secure_cron.sh`

## Non-negotiables

- No destructive commands against system paths.
- No live payments/outreach without explicit approvals.
- Keep all automation within this project root.
- Preserve `CLAUDE` docs and existing master docs; Codex uses this file as local contract.
