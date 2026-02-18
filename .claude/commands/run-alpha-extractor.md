---
name: run-alpha-extractor
description: Run the daily alpha extractor to scan high-signal sources for new tactics.
---

# Alpha Extraction

Run the daily alpha extractor against HIGH_SIGNAL_SOURCES.csv.

## Process

1. Run: `python3 AUTOMATIONS/daily_alpha_extractor.py`
2. Review output for errors
3. Check LEDGER/ALPHA_STAGING.csv for new entries
4. Report count of new findings

## Arguments

- `--dry-run` - Preview what will be processed
- `--platform [X|Reddit|YouTube|Web]` - Filter by platform
- `--tier [HIGHEST|HIGH|MEDIUM]` - Filter by signal tier

Example: `/run-alpha-extractor --platform X --tier HIGHEST`
