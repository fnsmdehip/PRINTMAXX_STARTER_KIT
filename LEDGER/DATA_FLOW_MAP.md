# PRINTMAXX Quant System Data Flow Map

**Generated:** 2026-02-04
**Purpose:** Document all CSV file connections used by the quant infrastructure

---

## Data Flow Diagram (ASCII)

```
                              ┌─────────────────────────────────────┐
                              │      RESEARCH / DISCOVERY           │
                              │   (Twitter, Reddit, GitHub, etc)    │
                              └──────────────┬────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                           ALPHA_STAGING.csv                                     │
│                     (3,364 rows - Source of Truth)                              │
│  Columns: alpha_id, source, source_url, category, tactic, roi_potential,       │
│  priority, status, applicable_methods, applicable_niches, synergy_score,       │
│  reviewer_notes, quality_issues, engagement_authenticity, earnings_verified,   │
│  extracted_method, compliance_notes, date_added                                │
└────────────────────────────────┬───────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
┌───────────────────────────────┐   ┌────────────────────────────────────────────┐
│   backtest_alpha.py           │   │        CROSS_POLLINATION_MATRIX.csv        │
│   (Reads ALPHA_STAGING)       │   │              (371 synergies)               │
│                               │   │  Columns: synergy_id, method_1, method_2,  │
│   Score 0-100                 │   │  synergy_score, synergy_type,              │
│   Decision: SCALE/PAPER_TRADE │   │  revenue_multiplier, implementation_notes, │
│   /KILL                       │   │  example_stack, priority                   │
└───────────────┬───────────────┘   └────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                    BACKTESTS/BACKTEST_RESULTS.csv                              │
│                            (731 rows)                                          │
│  Columns: alpha_id, backtest_score, decision, category, source, timestamp,    │
│  multiple_sources, has_numbers, has_timeline, still_valid_2026,               │
│  engagement_data, conversion_data, replicable                                 │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
           (score >= 70) │              (50 <= score < 70)
                         ▼                             ▼
            ┌────────────────────────┐   ┌────────────────────────────────────────┐
            │  Direct to EXECUTION   │   │         paper_trade.py                 │
            │  (SCALE decision)      │   │    (Reads BACKTEST_RESULTS)            │
            └────────────────────────┘   │    Test with $0-100 budget             │
                                         │    7-14 day validation                 │
                                         └──────────────────┬─────────────────────┘
                                                            │
                                                            ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                       PAPER_TRADES/PAPER_TRADES.csv                            │
│                              (1 active trade)                                  │
│  Columns: trade_id, method_id, alpha_id, budget, duration_days, start_date,   │
│  end_date, status, decision, notes, capital_invested, time_invested_hours,    │
│  revenue_generated, leads_generated, conversion_rate, revenue_per_hour,       │
│  scalability_score, platform_risk                                             │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                                        ▼ (When trade completes)
┌───────────────────────────────────────────────────────────────────────────────┐
│                    PAPER_TRADES/PAPER_TRADE_RESULTS.csv                        │
│                              (1 completed trade)                               │
│  Columns: trade_id, method_id, alpha_id, decision, revenue_per_hour,          │
│  scalability_score, platform_risk, total_revenue, total_time_hours,           │
│  total_investment, roi_percent, completed_date, notes                         │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                          (SCALE decision: revenue/hr >= $20)
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                      FINANCIALS/REVENUE_TRACKER.csv                            │
│                          (0 rows - header only)                                │
│  Columns: date, method_id, method_name, revenue, expenses, profit, source,    │
│  notes                                                                         │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                          quant_dashboard.py                                    │
│                    (Reads for Portfolio View panel)                            │
│                                                                                │
│                       Also reads:                                              │
│                       - ALPHA_STAGING.csv (Alpha Discovery panel)              │
│                       - MONEY_METHODS_TRACKER.csv (Method Performance)         │
│                       - BACKTESTS/BACKTEST_RESULTS.csv (Backtest panel)        │
└───────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                          revenue_projector.py                                  │
│                    (Monte Carlo + Kelly Criterion)                             │
│                                                                                │
│  Reads:                                                                        │
│  - MONEY_METHODS_TRACKER.csv (method parameters)                               │
│  - BACKTESTS/BACKTEST_RESULTS.csv (backtest scores)                            │
│  - CROSS_POLLINATION_MATRIX.csv (synergy multipliers)                          │
│  - FINANCIALS/REVENUE_TRACKER.csv (historical performance)                     │
│  - PAPER_TRADES/PAPER_TRADE_RESULTS.csv (validation data)                      │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Quant Files Summary

### Primary Data Stores

| File | Location | Rows | Purpose | Read By | Written By |
|------|----------|------|---------|---------|------------|
| ALPHA_STAGING.csv | LEDGER/ | 3,364 | All alpha entries | backtest_alpha.py, quant_dashboard.py, agent_monitor.py | Research loops, manual entry |
| BACKTEST_RESULTS.csv | LEDGER/BACKTESTS/ | 731 | Alpha validation scores | paper_trade.py, quant_dashboard.py, revenue_projector.py | backtest_alpha.py |
| PAPER_TRADES.csv | LEDGER/PAPER_TRADES/ | 1 | Active paper trades | paper_trade.py | paper_trade.py |
| PAPER_TRADE_RESULTS.csv | LEDGER/PAPER_TRADES/ | 1 | Completed trades | revenue_projector.py | paper_trade.py |
| REVENUE_TRACKER.csv | FINANCIALS/ | 0 (header) | Actual revenue | quant_dashboard.py, revenue_projector.py | Manual entry |
| MONEY_METHODS_TRACKER.csv | LEDGER/ | 68 | Method definitions | quant_dashboard.py, revenue_projector.py | Manual entry |
| CROSS_POLLINATION_MATRIX.csv | LEDGER/ | 371 | Method synergies | revenue_projector.py | Research loops |

### Supporting Data Stores

| File | Location | Rows | Purpose | Read By | Written By |
|------|----------|------|---------|---------|------------|
| HIGH_SIGNAL_SOURCES.csv | LEDGER/ | 175 | Research sources | Twitter scraper, research loops | Manual entry |
| NICHES.csv | LEDGER/ | 38 | Niche definitions | quant_dashboard.py | Manual entry |
| BACKTEST_PRIORITY_QUEUE.csv | LEDGER/ | 731 | Prioritized alpha for backtest | backtest_alpha.py | Research loops |
| MEGA_RALPH_TRACKER.csv | LEDGER/ | 0 (header) | Ralph loop tracking | quant_dashboard.py | Mega ralph loop |
| FUNNEL_METRICS.csv | LEDGER/ | 0 (header) | Conversion tracking | quant_dashboard.py | Manual entry |
| TIME_TRACKING.csv | LEDGER/ | 0 (header) | Time investment tracking | revenue_projector.py | Manual entry |

---

## Quant Tool Connection Map

### backtest_alpha.py

**Reads:**
- `LEDGER/ALPHA_STAGING.csv` - Gets alpha entries to backtest (filters by status)

**Writes:**
- `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` - Appends backtest scores and decisions

**Decision Logic:**
- Score >= 70: SCALE (deploy immediately)
- Score 50-69: PAPER_TRADE (test with minimal capital)
- Score < 50: KILL (do not pursue)

---

### paper_trade.py

**Reads:**
- `LEDGER/PAPER_TRADES/PAPER_TRADES.csv` - Active trades
- `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` - For trade creation context

**Writes:**
- `LEDGER/PAPER_TRADES/PAPER_TRADES.csv` - Creates and updates trades
- `LEDGER/PAPER_TRADES/PAPER_TRADE_RESULTS.csv` - Completes trades with final metrics

**Decision Logic:**
- Revenue/hour >= $20 AND scalability >= 7 AND platform_risk <= 5: SCALE
- Revenue/hour >= $15: ITERATE
- Otherwise: KILL

---

### quant_dashboard.py

**Reads:**
- `LEDGER/ALPHA_STAGING.csv` - Alpha Discovery panel (last 20 entries)
- `LEDGER/MONEY_METHODS_TRACKER.csv` - Method Performance panel
- `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` - Backtest Results panel
- `FINANCIALS/REVENUE_TRACKER.csv` - Portfolio View panel
- Agent task output files (for Agent Activity panel)

**Writes:**
- None (display only)

---

### agent_monitor.py

**Reads:**
- `LEDGER/ALPHA_STAGING.csv` - Alpha stats (total, pending, approved counts)
- `ralph/loops/mega/.ralph/progress.md` - Ralph loop status
- Agent task output files

**Writes:**
- None (display only)

---

### revenue_projector.py

**Reads:**
- `LEDGER/MONEY_METHODS_TRACKER.csv` - Method parameters
- `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` - Validation scores
- `LEDGER/CROSS_POLLINATION_MATRIX.csv` - Synergy multipliers
- `LEDGER/PAPER_TRADES/PAPER_TRADE_RESULTS.csv` - Historical paper trade data
- `FINANCIALS/REVENUE_TRACKER.csv` - Actual revenue history

**Writes:**
- Projection output (console or file)

**Calculation:**
- Monte Carlo simulation for revenue projections
- Kelly Criterion for optimal capital allocation
- Synergy multipliers from cross-pollination matrix

---

## Data Pipeline Integrity Checks

### Connection Verification Status

| Connection | Status | Notes |
|------------|--------|-------|
| ALPHA_STAGING -> backtest_alpha.py -> BACKTEST_RESULTS | VERIFIED | 731 backtests completed |
| BACKTEST_RESULTS -> paper_trade.py -> PAPER_TRADES | VERIFIED | 1 trade completed |
| PAPER_TRADES -> PAPER_TRADE_RESULTS | VERIFIED | SCALE decision recorded |
| PAPER_TRADE_RESULTS -> REVENUE_TRACKER | MISSING | No manual revenue entry yet |
| REVENUE_TRACKER -> quant_dashboard | BROKEN | File has header only |
| MONEY_METHODS_TRACKER -> quant_dashboard | VERIFIED | 68 methods tracked |
| CROSS_POLLINATION_MATRIX -> revenue_projector | VERIFIED | 371 synergies |

### Missing Files Created

| File | Created | Status |
|------|---------|--------|
| MEGA_RALPH_TRACKER.csv | 2026-02-04 | Header only - ready for use |
| FUNNEL_METRICS.csv | 2026-02-04 | Header only - ready for use |
| TIME_TRACKING.csv | 2026-02-04 | Header only - ready for use |

---

## Column Schema Reference

### ALPHA_STAGING.csv
```
alpha_id          - Unique ID (ALPHA001, ALPHA002, etc.)
source            - Source handle or site (@levelsio, Reddit, etc.)
source_url        - Direct link to source
category          - APP_FACTORY, COLD_OUTBOUND, MONETIZATION, etc.
tactic            - Description of the tactic
roi_potential     - HIGHEST, HIGH, MEDIUM, LOW
priority          - IMMEDIATE, HIGH, MEDIUM, BACKLOG
status            - PENDING_REVIEW, APPROVED, REJECTED, etc.
applicable_methods - Comma-separated method IDs (MM001, MM002)
applicable_niches  - Comma-separated niche IDs (N001, N002)
synergy_score     - 1-100 synergy potential
reviewer_notes    - Manual review notes
quality_issues    - Any quality concerns
engagement_authenticity - AUTHENTIC, SUSPICIOUS
earnings_verified  - TRUE, FALSE, N/A
extracted_method   - Core method if extracted
compliance_notes   - FTC/legal concerns
date_added        - ISO date when added
```

### BACKTEST_RESULTS.csv
```
alpha_id           - References ALPHA_STAGING.alpha_id
backtest_score     - 0-100 validation score
decision           - SCALE, PAPER_TRADE, KILL
category           - Copied from alpha
source             - Copied from alpha
timestamp          - ISO timestamp of backtest
multiple_sources   - TRUE/FALSE
has_numbers        - TRUE/FALSE
has_timeline       - TRUE/FALSE
still_valid_2026   - TRUE/FALSE
engagement_data    - TRUE/FALSE
conversion_data    - TRUE/FALSE
replicable         - TRUE/FALSE
```

### PAPER_TRADES.csv
```
trade_id            - Unique ID (PAPER_TRADE_001, etc.)
method_id           - Method being tested (MM001, MM007)
alpha_id            - Alpha being validated
budget              - Capital allocated ($)
duration_days       - Test duration
start_date          - ISO start date
end_date            - ISO end date
status              - RUNNING, COMPLETE, KILLED
decision            - PENDING, SCALE, ITERATE, KILL
notes               - Manual notes
capital_invested    - Actual capital used
time_invested_hours - Hours spent
revenue_generated   - Revenue during test
leads_generated     - Leads captured
conversion_rate     - Leads to revenue
revenue_per_hour    - Key metric
scalability_score   - 1-10 assessment
platform_risk       - 1-10 assessment
```

### REVENUE_TRACKER.csv
```
date              - ISO date
method_id         - Method generating revenue
method_name       - Human-readable name
revenue           - Revenue amount ($)
expenses          - Expenses amount ($)
profit            - Net profit ($)
source            - Revenue source (Gumroad, App Store, etc.)
notes             - Additional context
```

### MONEY_METHODS_TRACKER.csv
```
method_id          - Unique ID (MM001, MM002, CF001, AI001)
method_name        - Human-readable name
category           - CORE, ECOM, EDGE, CONTENT_FARM, AI_INFLUENCER
status             - Active, Planning, Research
revenue_model      - IAP + Subs, One-time, Commission, etc.
time_to_first_dollar - Estimated days
effort_level       - Low, Medium, High
revenue_potential  - Estimated monthly potential
scalability        - Scale factor
automation_level   - Low, Medium, High
platform_risk      - 1-10
legal_risk         - 1-10
priority           - Phase1, Phase2, Phase3
notes              - Implementation notes
```

---

## Recommended Actions

### Immediate (Complete Data Flow)

1. **Add revenue entries to REVENUE_TRACKER.csv** when first dollar earned
2. **Track time in TIME_TRACKING.csv** for revenue/hour calculations
3. **Log funnel metrics to FUNNEL_METRICS.csv** for conversion tracking

### Short-term (System Integrity)

1. **Run backtest_alpha.py --pending** periodically to score new alpha
2. **Create paper trades** for all PAPER_TRADE decisions
3. **Complete paper trades** and log results

### Long-term (Automation)

1. **Connect paper trade SCALE decisions** to automatic REVENUE_TRACKER entries
2. **Build funnel tracking integration** with analytics platforms
3. **Automate time tracking** via session logging

---

## File Locations Quick Reference

```
QUANT SYSTEM FILES
├── AUTOMATIONS/
│   ├── backtest_alpha.py      # Alpha validation
│   ├── paper_trade.py         # Minimal capital testing
│   ├── quant_dashboard.py     # Terminal dashboard
│   ├── agent_monitor.py       # Live agent tracking
│   └── revenue_projector.py   # Monte Carlo projections
│
├── LEDGER/
│   ├── ALPHA_STAGING.csv      # 3,364 alpha entries
│   ├── BACKTESTS/
│   │   └── BACKTEST_RESULTS.csv   # 731 backtest scores
│   ├── PAPER_TRADES/
│   │   ├── PAPER_TRADES.csv       # Active trades
│   │   ├── PAPER_TRADE_RESULTS.csv # Completed trades
│   │   └── SYNC_LOG.csv           # Sync tracking
│   ├── CROSS_POLLINATION_MATRIX.csv  # 371 synergies
│   ├── MONEY_METHODS_TRACKER.csv     # 68 methods
│   ├── BACKTEST_PRIORITY_QUEUE.csv   # 731 prioritized
│   ├── HIGH_SIGNAL_SOURCES.csv       # 175 sources
│   ├── NICHES.csv                    # 38 niches
│   ├── MEGA_RALPH_TRACKER.csv        # Ralph tracking (NEW)
│   ├── FUNNEL_METRICS.csv            # Funnel data (NEW)
│   └── TIME_TRACKING.csv             # Time tracking (NEW)
│
└── FINANCIALS/
    └── REVENUE_TRACKER.csv    # Revenue (header only)
```
