# Claude Code Audit Brief: OpenClaw Worker Isolation Stack

Date: 2026-02-18
Owner: PRINTMAXX
Audience: Claude Code (auditor)

## Objective

Audit the newly implemented OpenClaw + worker isolation process and determine the best production setup for:

- Main machine: M1 Max 64GB (control/orchestration only)
- Worker machine: M2 16GB (remote ClawDBot/OpenClaw runtime)
- Budget: hard cap $100/mo via OpenRouter key-level limits
- Requirement: prevent runaway API spend + prevent agent loops from damaging main machine files

You are not asked to preserve my implementation if you find better architecture. You are asked to give the best final design.

## Current Changes To Audit

### New files

1. `AUTOMATIONS/openrouter_budget_guard.py`
2. `OPS/OPENROUTER_BUDGET_POLICY.json`
3. `scripts/setup_openclaw_worker_stack.sh`
4. `scripts/setup_control_to_worker_ssh.sh`
5. `OPS/openclaw/openclaw_worker_template.json5`
6. `OPS/OPENCLAW_WORKER_ISOLATION_RUNBOOK_2026_02_18.md`
7. `AUDIT/META_VISION_2026_02_18_OPENCLAW_WORKER_INTEGRATION.md`

### Updated files

1. `AUTOMATIONS/crontab_secure_minimal.txt`
2. `scripts/install_secure_cron.sh`
3. `CODEX.md`

### Official upstream source available

- `external/openclaw-official`

## Required Reading Order

1. `.claude/CLAUDE.md`
2. `CODEX.md`
3. `OPS/OPENCLAW_WORKER_ISOLATION_RUNBOOK_2026_02_18.md`
4. `AUDIT/META_VISION_2026_02_18_OPENCLAW_WORKER_INTEGRATION.md`
5. New/updated files listed above
6. `external/openclaw-official/README.md`

## Scope Constraints

- Focus audit on OpenClaw worker isolation + budget enforcement path.
- Ignore unrelated dirty files in git status.
- Do not do destructive commands.
- Keep legal/safe posture: no explicit TOS-breaking implementation details.

## Audit Checklist (must answer each)

### A) Architecture correctness

1. Is M1 control / M2 worker separation correctly enforced in practice?
2. Are there hidden paths where worker loops can impact control node files?
3. Is this the right role split for OpenClaw + Ship Captain coexistence?

### B) Reliability / ops

1. Are bootstrap scripts idempotent and safe for reruns?
2. Are SSH/bootstrap flows brittle in any way?
3. Is daemon startup/restart strategy sufficient for 24/7 ops?

### C) Budget safety

1. Does OpenRouter key-level limit logic truly prevent daily overspend?
2. Any edge case where spend can exceed the intended daily cap?
3. Is cron-based enforcement enough, or should policy be enforced more frequently?

### D) Security / blast radius

1. Any secret leakage risk in scripts/logs/artifacts?
2. Any unsafe defaults in OpenClaw worker config template?
3. Any missing hardening for remote gateway access?

### E) Best final architecture decision

Pick one and justify:

1. Keep current hybrid: Ship Captain primary + official OpenClaw sidecar
2. Make official OpenClaw primary, move Ship Captain to tool lane
3. Keep custom stack only, use upstream repo as reference only

Provide exact reasoning with tradeoffs and expected failure modes.

## Commands You Should Run

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# Sanity checks
bash -n scripts/setup_openclaw_worker_stack.sh
bash -n scripts/setup_control_to_worker_ssh.sh
python3 -m py_compile AUTOMATIONS/openrouter_budget_guard.py
python3 AUTOMATIONS/openrouter_budget_guard.py --help
python3 AUTOMATIONS/openrouter_budget_guard.py --enforce --dry-run

# Read relevant files
sed -n '1,260p' OPS/OPENCLAW_WORKER_ISOLATION_RUNBOOK_2026_02_18.md
sed -n '1,260p' OPS/openclaw/openclaw_worker_template.json5
sed -n '1,340p' AUTOMATIONS/openrouter_budget_guard.py
sed -n '1,220p' scripts/setup_openclaw_worker_stack.sh
sed -n '1,220p' scripts/setup_control_to_worker_ssh.sh
sed -n '1,220p' external/openclaw-official/README.md
```

## Output Format Required

Use this exact structure:

1. `Verdict` (one paragraph)
2. `Critical findings` (severity-ordered, file + line references)
3. `Architecture decision` (choose 1/2/3 from above)
4. `Minimal patch list` (exact edits/commands)
5. `Go-live runbook` (M1 + M2 commands in order)
6. `Residual risks` (what still cannot be fully mitigated)

## Decision Bar

Do not give generic suggestions.
Give concrete, implementable recommendations for this exact repo and hardware.

If you disagree with current implementation, provide replacement commands/files explicitly.
