# Ralph Loops - PRINTMAXX Overnight Builds

## Quick Start

Run all loops overnight:
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph
./run_all_loops.sh
```

Run individual loop:
```bash
./loops/content_social/run.sh 15     # 15 iterations
./loops/automation_scripts/run.sh 5  # 5 iterations
./loops/cold_email/run.sh 6          # 6 iterations
./loops/landing_copy/run.sh 7        # 7 iterations
./loops/competitor_research/run.sh 6 # 6 iterations
./loops/app_discovery/run.sh 10      # 10 iterations (perpetual research)
```

## How It Works

Each loop follows the canonical Ralph pattern:
1. Static `prompt.md` file (never changes)
2. `state.md` tracks what's done (checkboxes)
3. Bash `run.sh` loops until complete
4. Each iteration: fresh context, reads state, does ONE task, marks done
5. Outputs `<promise>COMPLETE</promise>` when all tasks done

## Loop Directory Structure

```
ralph/
├── run_all_loops.sh          # Master runner (parallel)
├── guardrails.md             # Shared rules
├── progress.md               # Session progress tracking
├── loops/
│   ├── content_social/
│   │   ├── prompt.md         # Static task definition
│   │   ├── state.md          # Completion tracking
│   │   └── run.sh            # Bash loop
│   ├── automation_scripts/
│   ├── cold_email/
│   ├── landing_copy/
│   ├── competitor_research/
│   └── app_discovery/        # Perpetual research for new app opportunities
└── logs/                     # Output logs per run
```

## Available Loops

| Loop | Tasks | Max Iterations | Output |
|------|-------|----------------|--------|
| content_social | 15 batches (150 posts) | 15 | CONTENT/social/{niche}/ |
| automation_scripts | 4 Python scripts | 5 | AUTOMATIONS/scripts/ |
| cold_email | 5 email sequences | 6 | CONTENT/email_sequences/cold/ |
| landing_copy | 6 app landing pages | 7 | builds/{app}/LANDING_COPY.md |
| competitor_research | 5 market categories | 6 | research/*.md |
| app_discovery | 10 niche categories | 10 | LEDGER/APP_OPPORTUNITIES/ |

## Monitoring Progress

Check state files:
```bash
cat loops/content_social/state.md
cat loops/automation_scripts/state.md
```

Watch logs:
```bash
tail -f logs/content_social_*.log
```

## Reset a Loop

To re-run a loop from scratch:
```bash
# Reset state file to unchecked
cat > loops/content_social/state.md << 'EOF'
# Content Social Loop State

- [ ] Batch 1: Faith 001-010
- [ ] Batch 2: Faith 011-020
...
EOF

# Run again
./loops/content_social/run.sh 15
```

## The Key Insight

From the RALPH_LOOP_GUIDE:
- Context rots after 40-60 minutes
- Don't try to preserve memory, throw it away
- Progress lives in FILES, not in chat
- Each iteration starts fresh, picks next task
- Loop is external to Claude (bash controls termination)

## Adding New Loops

1. Create `loops/new_loop/` directory
2. Write `prompt.md` with static tasks
3. Write `state.md` with checkbox list
4. Copy `run.sh` template
5. Add to `run_all_loops.sh` if desired

## Guardrails

All loops read `ralph/guardrails.md` first. Add patterns here when something breaks repeatedly. Lessons accumulate, mistakes evaporate.
