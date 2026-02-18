# META VISION: PRINTMAXX Full-Context Audit (v4)

**Date:** 2026-02-16 14:53:28  
**Method:** Parallel swarm ingest + raw chunk corpus + metrics sweep  
**Prior audit preserved:** `AUDIT/META_VISION.md` (2026-02-14)  

---

## 1. Full-Context Corpus (No Summaries)

This audit run generated a raw, chunked corpus of repository file contents for deep review in subagent-sized windows.
The temporary `FULL_CONTEXT_2026_02_16` chunk directory was removed after capture to control storage footprint; metrics and inventory artifacts were preserved.

- Preserved inventory artifact: `AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv`
- Preserved metrics: `AUDIT/META_VISION_2026_02_16_TOP_LEVEL_METRICS.csv`
- Preserved core-dir metrics: `AUDIT/META_VISION_2026_02_16_CORE_DIR_METRICS.csv`
- Preserved largest-files metrics: `AUDIT/META_VISION_2026_02_16_LARGEST_FILES.csv`

Captured scope:

| Metric | Value |
|---|---:|
| `files_total` | 1,306,998 |
| `text_files` | 1,294,618 |
| `binary_files` | 12,366 |
| `error_files` | 14 |
| `total_chunks` | 3,189,282 |
| `total_bytes` | 16,000,773,306 (~14.9 GB) |
| `chunk_chars` | 5,000 |
| `workers` | 10 |

---

## 2. Repository-Scale Snapshot (From Swarm Metrics)

Source files:
- `AUDIT/META_VISION_2026_02_16.md`
- `AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv`
- `AUDIT/META_VISION_2026_02_16_TOP_LEVEL_METRICS.csv`
- `AUDIT/META_VISION_2026_02_16_CORE_DIR_METRICS.csv`
- `AUDIT/META_VISION_2026_02_16_LARGEST_FILES.csv`

Current measured scale:

| Metric | Value |
|---|---:|
| Total files | 1,307,326 |
| Total directories | 203,761 |
| Total disk footprint (files) | 17.85 GB |
| Python files | 430 |
| CSV files | 2,340 |
| Markdown files | 60,244 |

---

## 3. Current Runtime/Revenue State Extract

From runtime artifacts and latest manifests:

- Node role: `worker`
- Pending approvals: `9`
- Approved keys: `1`
- Accounts active/ready: `0`
- Freelance draft rows: `104`
- Gumroad pending listings: `5`
- Gumroad live listings: `0`
- Clawdbot intent rows: `57`
- Clawdbot syndication rows: `420`
- Clawdbot directory rows: `900`
- ClawWork sidecar budget state: `NORMAL`
- ClawWork sampled expected profit: `$234.63`

---

## 4. Agent Swarm Read Pattern (Chunked)

Use this pattern to avoid overloading a single context window while preserving full detail:

1. Select file set from `AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv`.
2. Process in deterministic batches by top-level folder or extension to avoid context overload.
3. Write findings back into lane-specific audit artifacts under `AUDIT/` or `OPS/`.
4. Keep references to exact file paths for traceability.

---

## 5. Control Notes

- Old audit was preserved and not deleted.
- New ClawWork sidecar lane is active:
  - Script: `AUTOMATIONS/clawwork_sidecar.py`
  - Policy: `OPS/CLAWWORK_SIDECAR_POLICY.json`
  - Plan: `OPS/CLAWWORK_MINIMAL_SIDECAR_PLAN.md`
- Ship Captain now includes sidecar step `clawwork_sidecar` in `AUTOMATIONS/ship_captain.py`.

---

## 6. Rebuild Commands

```bash
# Full raw corpus rebuild (storage-smart: compressed + deduped chunk shards)
python3 AUTOMATIONS/full_context_swarm_dump.py --write --workers 10 --chunk-chars 5000 --max-records-per-shard 2500 --compress-shards --dedupe-content

# Metrics + navigation-layer META_VISION refresh
python3 AUTOMATIONS/meta_vision_swarm_audit.py --write --tag 2026_02_16
```
