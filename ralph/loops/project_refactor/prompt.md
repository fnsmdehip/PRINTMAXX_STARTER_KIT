# PRINTMAXX Project Refactor — Ralph Loop Prompt

**You are a structural refactoring agent.** Your job is to slim CLAUDE.md, consolidate navigation, fix false claims, and create operational docs — all based on the Feb 5 2026 system audit.

## Context

- **Audit:** Read `OPS/SYSTEM_AUDIT_FEB5_2026.md` for what's broken and what to fix
- **Backup:** Full project backup at `/Users/macbookpro/Documents/p/PRINTMAXX_BACKUP_FEB5_2026/`
- **Canonical ralph reference:** `OPS/RALPH_CANONICAL_REFERENCE.md`

## Your Loop

1. Read `ralph/loops/project_refactor/prd.json` — find highest priority story where `passes: false`
2. Read `ralph/loops/project_refactor/.ralph/progress.txt` — learn what previous iterations discovered
3. Execute ONE story (or one chunk of a large story)
4. Validate your work against the acceptance criteria
5. Update `prd.json` — set `passes: true` if ALL acceptance criteria met
6. Append learnings to `progress.txt`
7. Exit

## Rules

- **ONE story per iteration.** Don't try to do everything at once.
- **Write to files immediately.** Don't accumulate in memory.
- **No information loss.** When moving content from CLAUDE.md to external files, verify the external file exists and the pointer in CLAUDE.md resolves.
- **No file deletion.** Move content to new files, replace inline content with pointers. The backup exists if we need to restore.
- **Append-only progress.** progress.txt only grows. Never delete entries.
- **Check file paths.** Before adding a pointer like "See OPS/FOO.md", verify OPS/FOO.md actually exists on disk.

## Story-Specific Instructions

### US-001: Slim CLAUDE.md (Priority 1)

This is the highest-leverage change. CLAUDE.md is 5,899 lines (~65K tokens) = 33% of context budget per message.

**Approach — do this in CHUNKS across multiple iterations:**

**Chunk A:** Archive session logs (lines ~4183+) to `OPS/CLAUDE_MD_ARCHIVE_FEB2026.md`. Replace with 5-line pointer.

**Chunk B:** Move detailed GTM/SEO/browser automation docs to external files (they already exist). Replace 500+ line sections with 3-line pointers to existing files.

**Chunk C:** Move Zero Waste Protocol full chain (~300 lines) to `OPS/ZERO_WASTE_PROTOCOL.md`. Keep only the auto-trigger rules and a pointer.

**Chunk D:** Move Operating Model detailed section (~200 lines) to `OPS/PRINTMAXX_OPERATING_MODEL.md`. Keep 10-line summary + pointer.

**Chunk E:** Consolidate 4 navigation systems into 1 unified table (this is also US-002).

**Chunk F:** Remove duplicate quant tool documentation (brief table + detailed docs — keep brief table only, full docs in OPS/QUANT_INFRASTRUCTURE_GUIDE.md).

**Chunk G:** Reduce CRITICAL markers from 34 to ~12. Demote non-essential ones.

**Chunk H:** Final pass — verify all pointers resolve, count lines, validate under 2,200.

### US-002: Consolidated Navigation (Priority 2)

Merge these 4 systems into ONE table:
- Navigation Rules (lines ~1125-1239)
- "Where is...?" table (lines ~1241-1302)
- Quick Task Router (lines ~1556-1612)
- Phase-specific routers

Format: `| Task | Start Here | Full Reference |`

### US-003: Daily Ops Playbook (Priority 3)

Create `OPS/DAILY_OPS_PLAYBOOK.md` (under 100 lines):
- Session start ritual (5 min)
- Research block
- Build block
- Session end ritual
- References WORKING tools only (swarm, 9 working quant scripts)
- Does NOT reference broken systems

### US-004: Fix False Claims (Priority 4)

Update CLAUDE.md claims to match reality per audit:
- 3,908 alpha → ~1,186 valid entries
- Mega loop → NOT BUILT (stub only)
- Individual ralph loops → FIXED (--max-tokens removed)
- 27 apps → 13 builds, 0 shipped
- 1,008 posts → 1,008 drafted, 0 published
- Verify all file paths exist on disk

### US-005: System Health Doc (Priority 5)

Create `OPS/SYSTEM_HEALTH.md`:
- Every automation script with WORKING / BROKEN / UNTESTED status
- Every ralph loop with status
- Every scraper with status
- Quant script test results
- CLAUDE.md references this file for system status

## Validation

After each change:
1. Verify no information was lost (content moved to external file OR kept inline)
2. Verify file pointers resolve: `test -f "/path/to/file" && echo "EXISTS" || echo "MISSING"`
3. Count CLAUDE.md lines: `wc -l .claude/CLAUDE.md`
4. Check for broken references

## Stop Condition

When ALL stories in prd.json have `passes: true`, output:

```
<promise>COMPLETE</promise>
```
