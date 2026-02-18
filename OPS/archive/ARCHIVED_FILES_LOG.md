# Archived Files Log

**Date:** 2026-02-02
**Source:** OPS/DEPRECATED_FILES.txt (generated from OPS_AUDIT_REPORT_FEB_2026.md)
**Confidence level:** HIGH only (safe to archive, superseded or duplicate)
**Total files archived:** 29
**Total empty directories deleted:** 3
**Total size freed from active context:** ~280KB (7,944 lines)
**Estimated token savings per session:** 20-40K tokens

---

## OPS/setup/archive/ (12 files, ~132KB)

All superseded by the canonical setup docs:
- `OPS/setup/RETARDMAXX_MANUAL_TODO.md` (canonical for setup tasks)
- `OPS/setup/HUMAN_INFRA_CHECKLIST.md` (canonical for infra tracking)
- `OPS/SESSION_HANDOFF.md` (canonical for session handoff)

| File | Size | Reason | Superseded By |
|------|------|--------|---------------|
| MANUAL_SETUP_CHECKLIST.md | 5.1KB | Earlier version of RETARDMAXX_MANUAL_TODO | setup/RETARDMAXX_MANUAL_TODO.md |
| MANUAL_SETUP_TASKS.md | 6.4KB | Another version with RevenueCat steps | setup/RETARDMAXX_MANUAL_TODO.md |
| MASTER_MANUAL_SETUP.md | 7.0KB | Tiered approach, same items | setup/RETARDMAXX_MANUAL_TODO.md |
| SETUP_CHECKLIST.md | 7.2KB | Oldest version, references Decodo (now SOAX) | setup/RETARDMAXX_MANUAL_TODO.md |
| ACCOUNT_CREATION_CHECKLIST.md | 5.6KB | Subset of setup tasks (accounts only) | setup/RETARDMAXX_MANUAL_TODO.md |
| BOOTSTRAP_STACK_CHECKLIST.md | 10.6KB | Same items in "tell Claude when done" format | setup/RETARDMAXX_MANUAL_TODO.md |
| COMPLETE_BOOTSTRAP_STACK.md | 12.8KB | Phased approach, more tools, same core | setup/RETARDMAXX_MANUAL_TODO.md |
| MANUAL_FOUNDATIONAL_STACK.md | 10.7KB | Monthly cost breakdown version | setup/RETARDMAXX_MANUAL_TODO.md |
| TECH_STACK_FOUNDATION.md | 5.8KB | CONFLICTING info (says Apple Dev active, wrong) | setup/HUMAN_INFRA_CHECKLIST.md |
| HANDOFF.md | 21.9KB | Old session handoff in setup/ (obsolete) | OPS/SESSION_HANDOFF.md |
| SESSION_HANDOFF.md | 9.7KB | Another handoff file in setup/ | OPS/SESSION_HANDOFF.md |
| HANDOFF_RETARDMAXX_SETUP.md | 7.9KB | Setup-specific handoff with old path | OPS/SESSION_HANDOFF.md |

---

## OPS/archive/ (17 files, ~148KB)

### Orphaned files (13 files) - not referenced in CLAUDE.md, mega ralph, or canonical files

| File | Size | Reason | Superseded By |
|------|------|--------|---------------|
| FRESH_CHAT_PROMPT.md | 1.7KB | Old project path, superseded by CLAUDE.md | .claude/CLAUDE.md |
| DECISION_REQUEST_TEMPLATE.md | 0.2KB | Empty template (159 bytes), never used | N/A |
| NEXT_ACTIONS_TEMPLATE.md | 0.3KB | Empty template (316 bytes), never used | N/A |
| MANAGER_RUNBOOK.md | 1.0KB | Superseded by mega ralph loop | ralph/loops/mega/prompt.md |
| MODEL_ROUTING_POLICY.md | 2.7KB | Irrelevant: user has Claude Max plan, always Opus | N/A |
| TOKEN_COST_CHECKPOINTS.md | 2.3KB | Irrelevant: user has unlimited Max plan | N/A |
| DAILY_RESEARCH_REPORT_TEMPLATE.md | 2.6KB | Superseded by /daily-research skill | .claude/commands/daily-research.md |
| SIMPLE_TASK_LIST.md | 5.9KB | Superseded by CAPITAL_GENESIS_DASHBOARD | OPS/CAPITAL_GENESIS_DASHBOARD.md |
| MASTER_ACTION_PLAN.md | 15.9KB | Jan 21, superseded by Capital Genesis plans | OPS/CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md |
| OPPORTUNITY_WINDOWS_ANALYSIS.md | 10.4KB | Jan 23, superseded by DIRECTIONAL_SIGNALS_2026 | OPS/DIRECTIONAL_SIGNALS_2026.md |
| YOUTUBE_SHORTS_RESEARCH_2025.md | 11.8KB | 2025-dated, outdated | OPS/YOUTUBE_2026_TACTICS_AND_COMPLIANCE.md |
| AI_VOICE_TOOLS_COMPARISON_2025.md | 9.1KB | 2025-dated, outdated | N/A |
| METRICS_DASHBOARD_SPEC.md | 8.4KB | Spec for dashboard that was built differently | AUTOMATIONS/quant_dashboard.py |

### Superseded strategic doc (1 file)

| File | Size | Reason | Superseded By |
|------|------|--------|---------------|
| SURGICAL_EXECUTION_PLAN.md | 14.9KB | Superseded by REPRIORITIZED (marked v2, same date) | OPS/CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md |

### SEO/GEO duplicates (3 files)

| File | Size | Reason | Superseded By |
|------|------|--------|---------------|
| SEO_AGENT_READABILITY_GUIDE.md | 8.0KB | Content merged into canonical SEO playbook | OPS/ENTITY_SEO_AGENT_READINESS_PLAYBOOK.md |
| GEO_RESEARCH_2025.md | 9.6KB | 2025-dated, stats conflict with canonical | OPS/ENTITY_SEO_AGENT_READINESS_PLAYBOOK.md |
| SEO_GEO_ASO_RESEARCH_SUMMARY_2026.md | 10.9KB | Research summary, content in canonical | OPS/ENTITY_SEO_AGENT_READINESS_PLAYBOOK.md |

---

## Empty directories deleted (3)

| Directory | Reason |
|-----------|--------|
| OPS/NICHE_RESEARCH/ | Empty, never populated |
| OPS/reports/ | Empty, never populated |
| OPS/research/ | Empty, never populated |

---

## Recovery

To recover any archived file:
```bash
# From setup archive
mv OPS/setup/archive/FILENAME.md OPS/setup/

# From OPS archive
mv OPS/archive/FILENAME.md OPS/
```

---

## Not archived (deferred)

- **MEDIUM confidence files (38):** Need review before archiving. See OPS/DEPRECATED_FILES.txt.
- **LOW confidence files (5):** May still have dependencies. See OPS/DEPRECATED_FILES.txt.
- **LEDGER batch files (6):** Handled by separate agent (merge then delete, not archive).
