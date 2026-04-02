# DEAD SCRIPTS AUDIT REPORT
**Generated:** 2026-04-02 15:47 UTC  
**Status:** ⚠️ REVIEW NEEDED

---

## Critical Finding: Dead Script Accumulation

**DANGER ZONE:** 524 out of 538 scripts (97.4%) appear to be dead code.

### Statistics
| Metric | Count |
|--------|-------|
| Total .py files | 538 |
| Scripts called by cron | 10 |
| Scripts referenced in code | 3 |
| **Potentially dead** | **525** |
| **Estimated disk waste** | **~45 MB** |

### Active Scripts (Called by Cron/Code)
These 13 scripts are actually used:
1. agent_swarm.py
2. venture_autonomy.py
3. ceo_agent.py
4. loop_closer.py
5. decision_engine.py
6. autonomous_orchestrator.py
7. control_panel.py
8. data_janitor_v2.py ← newly added
9. aggressive_dedup.py ← newly added
10. cleanup_backups.py ← newly added
11. find_dead_scripts.py ← newly added
12. (2-3 others verified in CLAUDE.md)

---

## Potential Dead Scripts (Sample - First 50)

```
account_creation_helper.py (12.7KB)
actionable_aggregator.py (20.0KB)
ad_budget_tracker.py (9.2KB)
agent_monitor.py (8.1KB)
agent_resilience.py (11.5KB)
agentic_discovery.py (26.9KB)
ai_actor_ad_generator.py (21.8KB)
ai_agent_qa_monitor.py (28.1KB)
ai_agent_security_content_pipeline.py (0.0KB) ← EMPTY
ai_fatigue_content_router.py (18.3KB)
ai_notetaker_affiliate_content.py (30.6KB)
ai_policy_engagement_converter.py (12.7KB)
ai_video_content_pipeline.py (41.9KB)
algo_ban_prevention.py (56.4KB)
alpha_auto_approver.py (6.2KB)
alpha_auto_processor.py (26.9KB)
alpha_backlog_scanner.py (20.3KB)
alpha_csv_parser.py (10.2KB)
alpha_monitor.py (26.8KB)
[... 30+ more ...]
```

---

## Warnings & Considerations

⚠️ **Before deleting any scripts:**
1. Some may be called by venture-specific automation (not in main cron)
2. Some may be manually triggered by user
3. Some may be used by background agents
4. Some may be fallback/error-recovery scripts
5. Deletion should be reviewed per-script, not bulk

### Safe Candidates for Deletion
(These are clearly obsolete or empty)
- `ai_agent_security_content_pipeline.py` (0 bytes - empty file)
- Any scripts with "old_", "deprecated_", "test_" prefix
- Any scripts older than 60 days with no git commits

---

## Recommendation

### Immediate Action (Safe)
1. **Audit in user session** - User reviews which scripts can be safely deleted
2. **Create whitelist** - Document which scripts are actually part of active ventures
3. **Batch delete** - Remove confirmed dead scripts (potentially 300-400 scripts = ~30-40 MB)

### Automation (Medium Priority)
Add to monthly hygiene check:
```bash
python3 AUTOMATIONS/find_dead_scripts.py --report --archive-old
```

This would:
- Move scripts untouched for 90+ days to archive/
- Report any that could be safely deleted
- Keep whitelist of known-active scripts

---

## Risk Assessment

**Current State:** 97% dead code bloat  
**Impact:** 
- Slower directory listings
- Confusion when debugging (more files to scan)
- Maintenance overhead
- Potential licensing issues (if scripts contain copyrighted code)

**Recommended Cleanup:** Delete 300-400 confirmed dead scripts (~30 MB recovery)

---

## Next Steps

1. User reviews this report
2. User indicates which scripts to keep/delete
3. DATA JANITOR re-runs with --delete-confirmed-dead flag
4. Verify no breaking changes to active pipelines
5. Commit cleanup to git with audit trail

---

*This report is for review purposes. No scripts were deleted without explicit user approval.*
