# Quick Fix: CLAUDE.md Navigation (30 Minutes)

**Purpose:** Fast find/replace to fix 39 broken file path references in CLAUDE.md

**Estimated Time:** 30 minutes (automated find/replace)

---

## Find/Replace Operations (In Order)

**Tool:** Use your text editor's find/replace (Cmd+Shift+H in VSCode/Cursor)

**File:** `.claude/CLAUDE.md`

### 1. Strategic Docs → 01_STRATEGY/ (8 replacements)

| Find | Replace |
|------|---------|
| `OPS/CAPITAL_GENESIS_UNIFIED_PLAN.md` | `01_STRATEGY/CAPITAL_GENESIS_UNIFIED_PLAN.md` |
| `OPS/CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md` | `01_STRATEGY/CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md` |
| `OPS/CAPITAL_GENESIS_FASTEST_PATH.md` | `01_STRATEGY/CAPITAL_GENESIS_FASTEST_PATH.md` |
| `OPS/CAPITAL_GENESIS_HUMAN_TASKS.md` | `01_STRATEGY/CAPITAL_GENESIS_HUMAN_TASKS.md` |
| `OPS/HEDGE_FUND_INTELLIGENCE_REPORT.md` | `01_STRATEGY/HEDGE_FUND_INTELLIGENCE_REPORT.md` |
| `OPS/METHOD_STACKING_PLAYBOOK.md` | `01_STRATEGY/METHOD_STACKING_PLAYBOOK.md` |
| `OPS/ULTRATHINK_CAPITAL_STACKS.md` | `01_STRATEGY/ULTRATHINK_CAPITAL_STACKS.md` |
| `OPS/COHERENCE_AUDIT_2026-01-28.md` | `01_STRATEGY/COHERENCE_AUDIT_2026-01-28.md` |

### 2. Growth Docs → 06_OPERATIONS/growth/ (7 replacements)

| Find | Replace |
|------|---------|
| `OPS/growth/EDGE_GROWTH_TACTICS.md` | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` |
| `OPS/growth/ENGAGEMENT_FARMING_TACTICS.md` | `06_OPERATIONS/growth/ENGAGEMENT_FARMING_TACTICS.md` |
| `OPS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md` | `06_OPERATIONS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md` |
| `OPS/EDGE_GROWTH_TACTICS.md` | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` |
| `OPS/NICHE_POSTING_STRATEGY.md` | `06_OPERATIONS/growth/NICHE_POSTING_STRATEGY.md` |
| `OPS/GTM_OPTIMIZATION_CHECKLIST.md` | `06_OPERATIONS/growth/GTM_OPTIMIZATION_CHECKLIST.md` |
| `OPS/X_ALGORITHM_OPTIMIZATION.md` | `06_OPERATIONS/growth/X_ALGORITHM_OPTIMIZATION.md` |

### 3. GTM Docs → 06_OPERATIONS/gtm/ (3 replacements)

| Find | Replace |
|------|---------|
| `OPS/GUMROAD_PRODUCT_SPECS.md` | `06_OPERATIONS/gtm/GUMROAD_PRODUCT_SPECS.md` |
| `OPS/FASTEST_REVENUE_PATHS_FEB_2026.md` | `06_OPERATIONS/gtm/FASTEST_REVENUE_PATHS_FEB_2026.md` |
| `OPS/FIRST_1K_REVENUE_PLAN.md` | `06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md` |

### 4. Setup Docs → 06_OPERATIONS/setup/ (6 replacements)

| Find | Replace |
|------|---------|
| `OPS/setup/RETARDMAXX_MANUAL_TODO.md` | `06_OPERATIONS/setup/RETARDMAXX_MANUAL_TODO.md` |
| `OPS/setup/RETARDMAXX_MANUAL_SETUP_CHECKLIST.md` | `06_OPERATIONS/setup/RETARDMAXX_MANUAL_SETUP_CHECKLIST.md` |
| `OPS/setup/ULTIMATE_STACK_GUIDE.md` | `06_OPERATIONS/setup/ULTIMATE_STACK_GUIDE.md` |
| `OPS/setup/COMPREHENSIVE_STACK_COMPARISON.md` | `06_OPERATIONS/setup/COMPREHENSIVE_STACK_COMPARISON.md` |
| `OPS/HUMAN_INFRA_CHECKLIST.md` | `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` |
| `OPS/operations/HUMAN_INFRA_CHECKLIST.md` | `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` |

### 5. Research Docs → 06_OPERATIONS/research/ (3 replacements)

| Find | Replace |
|------|---------|
| `OPS/GREY_HAT_SOURCE_FILTERING.md` | `06_OPERATIONS/research/GREY_HAT_SOURCE_FILTERING.md` |
| `OPS/COPY_PSYCHOLOGY_MASTER_REFERENCE.md` | `06_OPERATIONS/research/COPY_PSYCHOLOGY_MASTER_REFERENCE.md` |
| `OPS/YOUTUBE_2026_TACTICS_AND_COMPLIANCE.md` | `06_OPERATIONS/research/YOUTUBE_2026_TACTICS_AND_COMPLIANCE.md` |

### 6. Automation Docs → 05_AUTOMATION/ and OPS/automation/ (2 replacements)

| Find | Replace |
|------|---------|
| `OPS/RALPH_LOOP_GUIDE.md` | `05_AUTOMATION/ralph/RALPH_LOOP_GUIDE.md` |
| `OPS/AUTONOMOUS_TASKS.md` | `OPS/automation/AUTONOMOUS_TASKS.md` |

---

## Quick Commands (Update These Too)

Find all instances of `cat OPS/` in the "Where is...?" table and Quick Task Router sections.

Replace with corrected paths from above.

**Example:**
```
BEFORE: cat OPS/EDGE_GROWTH_TACTICS.md
AFTER:  cat 06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md
```

---

## Verification (Run After Replacements)

```bash
# Check for remaining broken OPS/ references (should only find valid ones)
grep -n "OPS/growth/" .claude/CLAUDE.md   # Should return 0 results
grep -n "OPS/setup/" .claude/CLAUDE.md    # Should return 0 results
grep -n "OPS/CAPITAL_" .claude/CLAUDE.md  # Should return 0 results

# Count total OPS/ references (should be ~26 valid ones)
grep -c "OPS/" .claude/CLAUDE.md
```

---

## After Replacements Complete

1. ✅ Delete empty directories:
```bash
rmdir OPS/growth OPS/setup 2>/dev/null
```

2. ✅ Test a few navigation commands:
```bash
cat 01_STRATEGY/CAPITAL_GENESIS_UNIFIED_PLAN.md | head -50
cat 06_OPERATIONS/gtm/FIRST_1K_REVENUE_PLAN.md | head -50
cat 06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md | head -50
```

3. ✅ Update session log in CLAUDE.md with completion note

---

**Completion Checklist:**

- [ ] 8 strategic doc paths updated
- [ ] 7 growth doc paths updated
- [ ] 3 GTM doc paths updated
- [ ] 6 setup doc paths updated
- [ ] 3 research doc paths updated
- [ ] 2 automation doc paths updated
- [ ] Quick commands table updated
- [ ] Task router table updated
- [ ] Phase 1-13 tables updated
- [ ] Empty directories deleted
- [ ] Verification commands run
- [ ] Session log updated

**Total:** 39 broken references fixed
