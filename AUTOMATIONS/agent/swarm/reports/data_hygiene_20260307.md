# DATA HYGIENE REPORT — 2026-03-07
**Agent:** DATA_JANITOR | **Cycle:** 12-hour | **Run time:** ~4 min

---

## SUMMARY

| Task | Status | Result |
|------|--------|--------|
| DEDUPLICATE | DONE | 6,304 rows removed from ALPHA_STAGING.csv |
| STALE PENDING | DONE | 0 entries stale (all 60 PENDING are <7 days old) |
| ARCHIVE LOGS | DONE | 233 old logs + 16 JSON status files compressed |
| VALIDATE JSON | DONE | All 23 agent state files valid |
| ORPHAN CLEANUP | DONE | 0 orphaned referenced files, 0 temp files |
| SIZE REPORT | DONE | 4 critical large dirs flagged — see below |
| BACKUP | DONE | ALPHA_STAGING.janitor_backup_20260307_115417.csv |

---

## 1. DEDUPLICATION

### ALPHA_STAGING.csv
- **Before:** 16,832 rows, 8.3MB
- **After:** 10,528 rows, 4.6MB
- **Removed:** 6,304 duplicate rows (37.5% of file was dupes)
- **Method:** Content fingerprint (source_url + tactic[:100]) — kept lowest alpha_id (original), removed re-imports
- **Root cause:** Same entries were re-imported across ~6 alpha_processor migration cycles

**Status breakdown (post-dedup):**
```
ARCHIVED:           4,654
ENGAGEMENT_BAIT:    4,796
APPROVED:           1,294
REPURPOSE_ONLY:     1,039
UNCHECKED:          1,327
AUTHENTIC:          1,041
FLAGGED_FOR_HUMAN:    776
AUTO_APPROVED:        715
INTEGRATED:           621
PENDING_REVIEW:        60
ROUTED_TO_VENTURE:    145
CONVERTED_TO_RESEARCH: 73
EXAGGERATED_BUT_SIGNAL: 60
REJECTED:               2
```

**Data quality issue flagged:** ~160+ rows have dates (e.g., `2026-02-15`) or numbers (`73`, `68`) in the `status` column — likely CSV row-shift corruption from malformed multi-line cells. These need human review but were NOT auto-deleted.

### Other key CSVs
All clean — no duplicates found:
- `COPY_STYLE_CORPUS.csv`: 454 rows, 0 dupes
- `FREELANCE_DEMAND_SCAN.csv`: 15,146 rows, 0 dupes
- `SHIP_CAPTAIN_RUNS.csv`: 28,701 rows, 0 dupes
- `AB_TESTS_MASTER.csv`: 42 rows, 0 dupes
- `ACCOUNTS.csv`: 48 rows, 0 dupes

---

## 2. STALE PENDING DATA

- **Total PENDING_REVIEW entries:** 60
- **Stale (>7 days):** 0
- **Recent (<7 days):** 60
- **Action required:** None — all pending are current

---

## 3. LOG ARCHIVING

### AUTOMATIONS/logs/
- **Before:** ~16MB, 419 files
- **Files compressed:** 233 old `.log` files (>3 days) + 16 `overnight_status_*.json` files
- **Compression destination:** `AUTOMATIONS/logs/archive/` (gzip)
- **Archive size:** 4.6MB (down from ~8MB of old logs)
- **Kept uncompressed:** 117 recent log files (last 3 days)

### LEDGER/archive/
- **Moved:** 13x `ALPHA_STAGING.before_migrate_*.csv` + 5 other old backups
- **Archive size:** 65MB consolidated
- **Freed from LEDGER root:** ~65MB

---

## 4. JSON VALIDATION

- **Agent state files checked:** 23 files in `AUTOMATIONS/agent/`
- **All valid:** Yes — 0 corrupt, 0 empty
- **Project-wide check:** 6,282 JSON files scanned

**False positives (not corrupt, just JSONC):**
- `.claude/remotion-skills/tsconfig.json` (and 9 worktree copies) — TypeScript JSONC with comments
- `scripts/ralph/flowchart/tsconfig.*.json` — TypeScript JSONC
- `external/openclaw-official/vendor/` — external code, ignore

**Real issues (JSONL format, not single JSON):**
- 16x `AUTOMATIONS/logs/overnight_status_*.json` — These were JSONL format (multiple objects per file). Now archived/compressed.

---

## 5. ORPHAN CLEANUP

- **Missing referenced files:** 0
  - All scripts referenced in `swarm_state.json` exist
  - All scripts referenced in `autonomy_state.json` exist
- **Temp/stale files (*.tmp, *.bak, *.old):** 0
- **Unreferenced files:** N/A (too broad to enumerate without false positives)

---

## 6. SIZE REPORT

### Project total: ~56GB

| Directory | Size | Flag |
|-----------|------|------|
| `.claude/` | 28GB | CRITICAL — contains worktrees with large duplicate files |
| `.git/` | 5.8GB | Expected — git history |
| `app factory/` | 5.3GB | HIGH — many app copies with node_modules |
| `.hf-cache/` | 4.2GB | HIGH — Qwen3-TTS model cache |
| `models/` | 4.2GB | HIGH — possible duplicate of .hf-cache |
| `AUTOMATIONS/` | 1.9GB | MEDIUM — leads bulk CSVs are large |
| `.venv-qwen3-tts/` | 1.1GB | MEDIUM — Python venv |
| `.uv-cache/` | 1.0GB | MEDIUM — uv package cache |
| `07_LANDING/` | 943MB | MEDIUM — Next.js apps with node_modules |
| `MEDIA/` | 487MB | LOW — acceptable |

### Specific large files flagged (>50MB):

**CRITICAL — .claude/worktrees duplicating large files:**
- `.claude/worktrees/suspicious-boyd/AUDIT/FULL_CONTEXT_2026_02_16/file_manifest.csv` — 265MB
- `.claude/worktrees/trusting-taussig/AUDIT/FULL_CONTEXT_2026_02_16/file_manifest.csv` — 265MB
- `.claude/worktrees/suspicious-boyd/AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv` — 195MB
- `.claude/worktrees/trusting-taussig/AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv` — 195MB

**CRITICAL — Model duplication (.hf-cache vs models/):**
- `.hf-cache/hub/models--Qwen--Qwen3-TTS-12Hz-1.7B-CustomVoice/blobs/...` — 3.6GB + 650MB
- `models/Qwen3-TTS-12Hz-1.7B-CustomVoice/model.safetensors` — 3.6GB

This is likely the SAME model stored in two locations. If confirmed, deleting one copy saves ~4.2GB.

**LARGE LEADS BULK FILES (normal, but flag):**
- `AUTOMATIONS/leads/bulk/US_LEADS_MASTER.csv` — 603MB
- `AUTOMATIONS/leads/qualified/PREFILTERED_LEADS.csv` — 407MB
- `AUTOMATIONS/leads/bulk/US_LEADS_RESTAURANT.csv` — 212MB

---

## 7. RECOMMENDED HUMAN ACTIONS

These require manual confirmation before action:

1. **Verify model duplication:** Check if `.hf-cache/` and `models/Qwen3-TTS-12Hz-1.7B-CustomVoice/` are the same model. If yes, delete one copy → saves ~4.2GB.

2. **Review worktree bloat:** `.claude/worktrees/` contains full project copies. If worktrees `suspicious-boyd` and `trusting-taussig` are no longer needed, removing them saves ~530MB of AUDIT file duplicates alone.

3. **Fix corrupt status values in ALPHA_STAGING.csv:** ~160 rows have dates/numbers in the `status` column. These are row-shift corruptions. Script available to isolate them.

4. **`app factory/` at 5.3GB:** Likely has node_modules inside many nested app directories. Running `find "app factory/" -name "node_modules" -type d` would show if they can be pruned.

---

## ARTIFACTS

- **Backup:** `LEDGER/ALPHA_STAGING.janitor_backup_20260307_115417.csv` (8.3MB — pre-dedup original)
- **Archive:** `LEDGER/archive/` (65MB — 18 old ALPHA_STAGING backups)
- **Log archive:** `AUTOMATIONS/logs/archive/` (4.6MB gzipped — 249 old files)
- **This report:** `AUTOMATIONS/agent/swarm/reports/data_hygiene_20260307.md`

---

*Next run: 2026-03-07 23:00 (12h cycle)*
