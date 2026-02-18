# OPS/ Directory Audit Report - February 2026

**Audit Date:** 2026-02-02
**Total Files Audited:** 289 (md + csv)
**Total Size:** 4.1MB
**Auditor:** Claude Opus 4.5

---

## Executive Summary

The OPS/ directory has grown organically over 15+ sessions from multiple agents. It contains valuable strategic intelligence and operational playbooks, but suffers from severe duplication in 4 clusters that waste agent context budget and create conflicting guidance. An estimated 40% of files (116 files, ~1.6MB) are duplicates, superseded, or orphaned. The highest-impact fix is consolidating the setup cluster (17 files saying the same thing).

**Top 3 Findings:**
1. **17 setup/manual checklist files** all covering "sign up for Apple Dev, buy domains, set up Cloudflare." One canonical file needed.
2. **8 SEO/GEO files** scattered across OPS/ root and OPS/growth/ with overlapping content and conflicting statistics.
3. **3 content repurposing files** covering the same "1 piece to 20+ pieces" pipeline with different tool recommendations and step counts.

**Estimated Context Budget Waste:** When an agent needs setup info, it may read 3-4 overlapping files consuming 30-50K tokens instead of 1 file at 8K tokens. Across typical sessions, this wastes 20-40% of context budget on redundant information.

---

## Cluster Analysis: Duplication Hotspots

### CLUSTER 1: Setup/Manual Checklists (CRITICAL - 17 files, 207KB)

All 17 files cover the same core content: sign up for Apple Dev ($99), Google Play ($25), buy domains, set up Cloudflare, create email infra.

| File | Size | Unique Value | Verdict |
|------|------|-------------|---------|
| setup/RETARDMAXX_MANUAL_TODO.md | 7KB | Stupidly simple format, direct URLs | **CANONICAL** |
| setup/RETARDMAXX_MANUAL_SETUP_CHECKLIST.md | 15KB | More detail than TODO, same items | MERGE into canonical |
| setup/HUMAN_INFRA_CHECKLIST.md | 5KB | Status tracking format (checkboxes) | MERGE (add status tracking to canonical) |
| setup/MANUAL_SETUP_CHECKLIST.md | 5KB | Earlier version, includes hosting comparison | ARCHIVE |
| setup/MANUAL_SETUP_TASKS.md | 6KB | Another version with RevenueCat steps | ARCHIVE |
| setup/MASTER_MANUAL_SETUP.md | 7KB | Tiered approach (good structure) | ARCHIVE |
| setup/SETUP_CHECKLIST.md | 7KB | Oldest version, Decodo proxies (now SOAX) | ARCHIVE |
| setup/ACCOUNT_CREATION_CHECKLIST.md | 6KB | Subset of above (accounts only) | ARCHIVE |
| setup/BOOTSTRAP_STACK_CHECKLIST.md | 11KB | Tell Claude when done format | ARCHIVE |
| setup/COMPLETE_BOOTSTRAP_STACK.md | 13KB | Phased approach, more tools | ARCHIVE |
| setup/MANUAL_FOUNDATIONAL_STACK.md | 11KB | Monthly cost breakdown | ARCHIVE |
| setup/TECH_STACK_FOUNDATION.md | 6KB | Conflicting info (says Apple Dev active) | ARCHIVE |
| setup/ULTIMATE_STACK_GUIDE.md | 45KB | Comprehensive tool/service reference | **KEEP as reference** |
| setup/COMPREHENSIVE_STACK_COMPARISON.md | 25KB | Tool comparison matrix (200+ tools) | **KEEP as reference** |
| CAPITAL_GENESIS_HUMAN_TASKS.md | 15KB | Revenue-lane-specific human tasks | **KEEP** (different purpose) |
| setup/HANDOFF.md | 22KB | Session handoff (obsolete) | ARCHIVE |
| setup/SESSION_HANDOFF.md | 10KB | Another handoff file | ARCHIVE |
| setup/HANDOFF_RETARDMAXX_SETUP.md | 8KB | Setup-specific handoff (old path) | ARCHIVE |

**Conflict Found:** TECH_STACK_FOUNDATION.md says Apple Developer active while every other file says not set up yet.

**Recommendation:** Create ONE canonical setup file combining RETARDMAXX format + HUMAN_INFRA status tracking. Move 12 files to setup/archive/. Keep ULTIMATE_STACK_GUIDE and COMPREHENSIVE_STACK_COMPARISON as deep reference.

**Impact:** Saves 15-25K tokens per session.

---

### CLUSTER 2: SEO/GEO/ASO (8+ files, ~180KB)

| File | Location | Verdict |
|------|----------|---------|
| ENTITY_SEO_AGENT_READINESS_PLAYBOOK.md | root | **CANONICAL** |
| SEO_AGENT_READABILITY_GUIDE.md | root | MERGE into canonical |
| GEO_OPTIMIZATION_PLAYBOOK.md | root | MERGE into canonical |
| GEO_RESEARCH_2025.md | root | ARCHIVE (2025 data) |
| SEO_AUDIT_2026-01-28.md | root | KEEP (historical audit) |
| COMPETITOR_SEO_ANALYSIS.md | root | KEEP (different purpose) |
| growth/SEO_GEO_ASO_TACTICS_2026.md | growth/ | Overlaps heavily with canonical |
| growth/SEO_GEO_ASO_RESEARCH_SUMMARY_2026.md | growth/ | ARCHIVE into logs |
| growth/SEO_GEO_ASO_ACTION_PLAN_2026.md | growth/ | MERGE key actions |
| growth/SEO_KEYWORD_RESEARCH_GUIDE.md | growth/ | KEEP (different purpose) |
| growth/GTM_OPTIMIZATION_CHECKLIST.md | growth/ | KEEP (different purpose) |

**Conflict:** GEO_RESEARCH_2025 says 12% ChatGPT citation overlap with top 10. ENTITY_SEO playbook says 90% come from outside top 20. Same insight stated so differently agents could misinterpret.

---

### CLUSTER 3: Content Repurposing (3 files, ~46KB)

| File | Size | Core Model |
|------|------|-----------|
| content/CONTENT_REPURPOSING_GUIDE.md | 9KB | 1:20 principle |
| content/CONTENT_REPURPOSING_PIPELINE.md | 20KB | 7-stage process |
| content/CONTENT_REPURPOSING_AUTOMATION.md | 17KB | Tool matrix |

All three describe the same process. Merge into single file keeping AUTOMATION as base.

---

### CLUSTER 4: X/Twitter Algorithm (4 files, ~50KB)

| File | Size | Focus |
|------|------|-------|
| growth/X_ALGORITHM_OPTIMIZATION.md | 6KB | Scoring formula |
| growth/X_TWITTER_ALGORITHM_RESEARCH_2025.md | 7KB | General mechanics |
| growth/TWITTER_META_JANUARY_2026.md | 16KB | Current meta |
| growth/TWITTER_GROWTH_PLAYBOOK_2026.md | 27KB | Comprehensive (references others) |

Playbook is designed as canonical. Add companion-doc headers to the other 3.

---

## Orphaned Files

### HIGH CONFIDENCE ORPHANS (safe to archive)

| File | Size | Reason |
|------|------|--------|
| FRESH_CHAT_PROMPT.md | 2KB | Old path, superseded by CLAUDE.md |
| DECISION_REQUEST_TEMPLATE.md | 159B | Empty template, never used |
| NEXT_ACTIONS_TEMPLATE.md | 316B | Empty template, never used |
| MANAGER_RUNBOOK.md | 1KB | Superseded by mega ralph loop |
| MODEL_ROUTING_POLICY.md | 3KB | User has Claude Max, always Opus |
| TOKEN_COST_CHECKPOINTS.md | 2KB | User has unlimited Max plan |
| DAILY_RESEARCH_REPORT_TEMPLATE.md | 3KB | Superseded by /daily-research skill |
| operations/SIMPLE_TASK_LIST.md | 6KB | Superseded by CAPITAL_GENESIS_DASHBOARD |
| operations/MASTER_ACTION_PLAN.md | 16KB | Jan 21, superseded |
| OPPORTUNITY_WINDOWS_ANALYSIS.md | 10KB | Jan 23, superseded |
| YOUTUBE_SHORTS_RESEARCH_2025.md | 12KB | 2025-dated, superseded |
| AI_VOICE_TOOLS_COMPARISON_2025.md | 9KB | 2025-dated |

### MODERATE CONFIDENCE ORPHANS

| File | Size | Reason |
|------|------|--------|
| DISCORD_COMMUNITIES_ALL_NICHES.md | 105KB | Largest file. Never referenced. |
| TELEGRAM_COMMUNITIES_ALL_NICHES.md | 94KB | Second largest. Never referenced. |
| TELEGRAM_COMMUNITY_GUIDE.md | 17KB | Not referenced |
| COMMUNITY_BUILDING_RESEARCH.md | 17KB | Not referenced |
| CUSTOMER_SUPPORT_GUIDE.md | 22KB | Premature (no customers) |
| CRISIS_RESPONSE_PLAYBOOK.md | 14KB | Premature (no public presence) |
| NEWSLETTER_MONETIZATION_RESEARCH.md | 7KB | Not cross-referenced |
| HASHTAG_STRATEGY_GUIDE.md | 10KB | Not referenced |
| METRICS_DASHBOARD_SPEC.md | 8KB | Built differently (quant_dashboard.py) |
| ELEVENLABS_MCP_INTEGRATION.md | 15KB | Not currently used |

**Combined orphans: ~460KB (11% of OPS/).**

---

## Empty Directories

| Directory | Verdict |
|-----------|---------|
| OPS/CONTENT_QA_QUEUE/ | KEEP (infrastructure) |
| OPS/NICHE_RESEARCH/ | DELETE |
| OPS/reports/ | DELETE |
| OPS/research/ | DELETE |

---

## 5 Conflicting Guidance Items

1. **Proxy Provider:** SETUP_CHECKLIST says Decodo. Everything else says SOAX. SOAX is canonical.
2. **Account Status:** TECH_STACK_FOUNDATION says Apple Dev active. HUMAN_INFRA_CHECKLIST says not started. HUMAN_INFRA is canonical.
3. **Budget:** MASTER_ACTION_PLAN says $200-1500. REPRIORITIZED says $500-800. SURGICAL says $40/mo. REPRIORITIZED is latest.
4. **Execution:** SURGICAL says sequential. REPRIORITIZED says parallel. REPRIORITIZED supersedes (marked v2).
5. **Session Handoff:** 3 different handoff files exist. OPS/SESSION_HANDOFF.md is canonical per CLAUDE.md.

---

## Premature Files (Built Before Need)

| File | Size | Why Premature |
|------|------|---------------|
| CUSTOMER_SUPPORT_GUIDE.md | 22KB | No customers |
| CRISIS_RESPONSE_PLAYBOOK.md | 14KB | No public presence |
| SUPPORT/ directory (12 files) | ~30KB | Canned responses for nonexistent products |
| operations/NOTIFICATION_STRATEGY_GUIDE.md | 10KB | Apps not shipped |
| SWARM_PROMOTION_PLAYBOOK.md | 8KB | No accounts exist |
| operations/DATABASE_BACKEND_GUIDE.md | 28KB | Using CSVs not databases |
| DISCORD_COMMUNITIES_ALL_NICHES.md | 105KB | No community exists |
| TELEGRAM_COMMUNITIES_ALL_NICHES.md | 94KB | No community exists |

**Combined: ~320KB premature documentation.**

---

## Capital Genesis Redundancy

| File | Size | Verdict |
|------|------|---------|
| CAPITAL_GENESIS_UNIFIED_PLAN.md | 40KB | **KEEP** (strategy) |
| CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md | 42KB | **KEEP** (canonical execution) |
| SURGICAL_EXECUTION_PLAN.md | 15KB | ARCHIVE (superseded) |
| CAPITAL_GENESIS_DASHBOARD.md | 24KB | **KEEP** (status tracker) |
| CAPITAL_GENESIS_FASTEST_PATH.md | 9KB | **KEEP** (quick reference) |

---

## Quant Infrastructure: Well-Structured (No Changes)

3 files with clear separation. No changes recommended.

---

## Stale SESSION_HANDOFF.md

Last updated Jan 27. CLAUDE.md session logs (Feb 4) are more current. CLAUDE.md is now the de facto handoff. Either update SESSION_HANDOFF or deprecate it.

---

## Summary of Recommendations

| Priority | Action | Files | Token Savings |
|----------|--------|-------|---------------|
| **P0** | Consolidate 17 setup files into 1 | 17 | 25K/session |
| **P0** | Archive 3 stale handoffs in setup/ | 3 | 10K |
| **P1** | Consolidate SEO/GEO to 3 files | 5 archived | 15K |
| **P1** | Merge 3 content repurposing files | 3 into 1 | 8K |
| **P1** | Archive SURGICAL_EXECUTION_PLAN | 1 | 5K |
| **P2** | Add companion headers to X/Twitter files | 3 modified | Prevents wrong-file-first |
| **P2** | Move premature files to archive/ | 9+ | 30K |
| **P2** | Delete 3 empty directories | 3 dirs | Marginal |
| **P3** | Archive orphaned templates | 4 | 2K |

**Total estimated context savings per session: 50-95K tokens (25-47% of context used on OPS/ files).**
