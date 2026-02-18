# Cross-Pollination Report Generator

Analyzes the CROSS_POLLINATION_MATRIX.csv and MONEY_METHODS_TRACKER.csv to generate actionable reports on method synergies, underexploited combinations, and prioritized recommendations.

## Usage

```bash
# Full report
python3 generate_report.py

# Only high-synergy stacks (85+)
python3 generate_report.py --min-score 85

# Report for specific method
python3 generate_report.py --method MM001

# Only active methods
python3 generate_report.py --active-only

# Custom output path
python3 generate_report.py --output /path/to/report.md
```

## Report Sections

1. **Top Synergy Stacks** - Highest-scoring method combinations
2. **Underexploited Combinations** - High-synergy stacks with inactive partners
3. **Automation Stacks** - Methods that can share infrastructure
4. **Audience Overlap Map** - Groups methods by shared audience
5. **Recommendations** - Prioritized actions to maximize synergy
6. **Full Matrix Summary** - Score distribution and method status

## Key Metrics

| Metric | Description |
|--------|-------------|
| Synergy Score | 0-100 rating of method combination potential |
| Automation Combo | Whether methods can share Playwright/posting scripts |
| Cross-Sell Products | Revenue paths between methods |
| Shared Audience | Overlapping user demographics |

## Data Sources

- `LEDGER/CROSS_POLLINATION_MATRIX.csv` - Synergy scores and combinations
- `LEDGER/MONEY_METHODS_TRACKER.csv` - Method status and details
- `LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv` - Comprehensive method data (preferred)

## Output

- `output/cross_pollination_report_YYYYMMDD.md` - Full report

## Dependencies

None (stdlib only).
