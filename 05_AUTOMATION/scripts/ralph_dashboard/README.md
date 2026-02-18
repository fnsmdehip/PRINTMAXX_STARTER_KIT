# Mega Ralph Tracker Dashboard

Generates a summary dashboard from MEGA_RALPH_TRACKER.csv and ralph loop state files. Shows task completion, findings, quality scores, phase progress, and checkpoint items.

## Usage

```bash
# Full dashboard
python3 generate_dashboard.py

# Filter by phase
python3 generate_dashboard.py --phase EXECUTION

# Filter by day cycle
python3 generate_dashboard.py --day-cycle 1

# Compact summary (one-liner stats)
python3 generate_dashboard.py --compact

# Custom output path
python3 generate_dashboard.py --output /path/to/dashboard.md
```

## Dashboard Sections

1. **Overview** - Total tasks, completion rate, findings, quality scores
2. **Progress Bar** - Visual completion indicator
3. **Phase Breakdown** - Stats per loop phase (DAILY_RESEARCH, REFLECTION, etc.)
4. **Category Breakdown** - Tasks by category (OUTBOUND, APP_FACTORY, etc.)
5. **Human Checkpoints** - Pending items needing human review
6. **Recent Tasks** - Last 10 tasks with status
7. **Current Loop Progress** - From progress.md state file
8. **Priority Queue** - Top items from priorities.md
9. **Error Summary** - Recent errors from errors.log
10. **Efficiency Metrics** - Avg duration, findings per hour

## Data Sources

- `LEDGER/MEGA_RALPH_TRACKER.csv` - Task tracking data
- `ralph/loops/mega/.ralph/progress.md` - Current phase state
- `ralph/loops/mega/.ralph/priorities.md` - Priority queue
- `ralph/loops/mega/.ralph/guardrails.md` - Learned constraints
- `ralph/loops/mega/.ralph/activity.log` - Activity count
- `ralph/loops/mega/.ralph/errors.log` - Error tracking
- `ralph/loops/mega/checkpoints/` - Human-in-loop items

## Output

Default: `ralph/loops/mega/output/dashboard_summary.md`

## Dependencies

None (stdlib only).
