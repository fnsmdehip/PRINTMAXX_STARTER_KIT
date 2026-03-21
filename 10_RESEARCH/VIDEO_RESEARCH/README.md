# VIDEO RESEARCH HUB

central command for all video tool research, pipeline design, and integration.

## folder structure

```
VIDEO_RESEARCH/
  comparisons/          -- tool-vs-tool comparisons, updated perpetually
  templates/            -- viral format templates, hooks, structures
  pipeline/             -- automated video production pipeline specs
  tools_tracker/        -- perpetual tool tracking data (CSVs, snapshots)
```

## key files

| file | purpose |
|------|---------|
| `comparisons/MASTER_VIDEO_TOOLS_2026.md` | canonical comparison, auto-updated |
| `comparisons/EDITING_TOOLS.md` | editing/post-production tools |
| `comparisons/SCHEDULING_TOOLS.md` | distribution/scheduling tools |
| `pipeline/VIDEO_AUTOPILOT_SPEC.md` | full pipeline: generate > edit > schedule > post |
| `pipeline/CLAUDE_DISPATCH_CAPCUT.md` | claude-dispatched auto-editing system |
| `tools_tracker/ALL_TOOLS_TRACKER.csv` | perpetual tracker for ALL tool categories |
| `templates/VIRAL_FORMATS.md` | trending video formats/templates library |

## integration points

- Capital Genesis KPI: scores tool ROI, auto-ranks by value/quality
- `ai_video_content_pipeline.py`: script generation uses best-ranked tools
- `daily_tool_scout.py`: feeds new tool discoveries here
- `viral_content_scanner.py`: feeds viral templates here
- `LEDGER/AI_VIDEO_CONTENT_TRACKER.csv`: production tracking

## consumers

- CEO agent (tool selection decisions)
- content pipeline (which tool to use for which content type)
- Capital Genesis ranker (tool cost feeds into venture scoring)
