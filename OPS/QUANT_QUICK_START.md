# PRINTMAXX Quant Infrastructure - Quick Start

**All systems tested and operational. Phase 1-4 complete.**

---

## What Just Got Built

✅ **Phase 1:** Live agent progress monitor
✅ **Phase 2:** 6-panel Bloomberg-style dashboard
✅ **Phase 3:** Alpha backtesting framework (0-100 scoring)
✅ **Phase 4:** Paper trading system ($0-100 tests)

**This is Jane Street/RenTech infrastructure for solopreneurship.**

---

## Quick Commands

### Launch Dashboard (Bloomberg Terminal Style)
```bash
python3 AUTOMATIONS/quant_dashboard.py
```

**6 Panels showing:**
- Alpha Discovery Feed (newest entries)
- Method Performance (revenue/hour, win rate)
- Agent Activity (running agents)
- Portfolio View (capital allocation)
- Backtest Results (validation scores)
- Alerts (degradation, opportunities, risks)

**Keyboard:**
- `r` = Refresh all panels
- `q` = Quit

---

### Backtest Alpha (Validate Before Deploying)

```bash
# Backtest single alpha
python3 AUTOMATIONS/backtest_alpha.py ALPHA524

# Backtest all PENDING_REVIEW
python3 AUTOMATIONS/backtest_alpha.py --pending

# Backtest everything
python3 AUTOMATIONS/backtest_alpha.py --all
```

**Decision Logic:**
- Score ≥70 → **SCALE** (deploy method)
- Score 50-69 → **PAPER_TRADE** (test with $0-100 first)
- Score <50 → **KILL** (don't deploy)

**Results saved to:** `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv`

---

### Paper Trade (Test with Minimal Capital)

```bash
# Start paper trade
python3 AUTOMATIONS/paper_trade.py \
  --method MM007_COLD_OUTBOUND \
  --alpha ALPHA524 \
  --budget 100 \
  --days 14 \
  --notes "Testing cold email sequence"

# Update metrics daily
python3 AUTOMATIONS/paper_trade.py \
  --update PAPER_TRADE_001 \
  --time 5 \
  --revenue 125 \
  --leads 8 \
  --scalability 7 \
  --risk 4

# Complete and get decision
python3 AUTOMATIONS/paper_trade.py --complete PAPER_TRADE_001

# List active trades
python3 AUTOMATIONS/paper_trade.py --list

# View all results
python3 AUTOMATIONS/paper_trade.py --results
```

**Decision Matrix:**
- Revenue/hour ≥$20 + Scalability ≥7 + Platform risk ≤5 = **SCALE**
- Close to threshold = **ITERATE** (adjust and retest)
- Far from threshold = **KILL** (don't scale)

**Results saved to:** `LEDGER/PAPER_TRADES/`

---

## Example Workflow (Just Tested)

```bash
# 1. Backtest alpha
$ python3 AUTOMATIONS/backtest_alpha.py ALPHA004
Score: 30/100
Decision: KILL
→ Don't deploy (needs more proof)

# 2. Start paper trade (for score 50-69 alpha)
$ python3 AUTOMATIONS/paper_trade.py --method MM007_COLD_OUTBOUND --alpha ALPHA524 --budget 50 --days 7
Started: PAPER_TRADE_001
Budget: $50
Duration: 7 days

# 3. Update metrics after 5 hours work
$ python3 AUTOMATIONS/paper_trade.py --update PAPER_TRADE_001 --time 5 --revenue 125 --leads 8 --scalability 7 --risk 4
Revenue/Hour: $25.00  ← ABOVE $20 ✅
Scalability: 7/10     ← MEETS THRESHOLD ✅
Platform Risk: 4/10   ← BELOW 5 ✅

# 4. Complete paper trade
$ python3 AUTOMATIONS/paper_trade.py --complete PAPER_TRADE_001
Decision: SCALE
Recommendation: Increase budget 2x to $100
→ Deploy method with $100 budget
```

---

## The Complete System

**Alpha Discovery** → **Backtest** → **Paper Trade** → **Deploy** → **Monitor** → **Rebalance**

### 1. Alpha Discovery (Daily)
- Ralph loop scans 81+ sources automatically
- Manual: `/daily-research` or Twitter scraper
- Output: `LEDGER/ALPHA_STAGING.csv`

### 2. Backtest (Before Any Deployment)
- Score 0-100 based on: sources, numbers, timeline, still works 2026
- Decision: SCALE (≥70), PAPER_TRADE (50-69), KILL (<50)
- Output: `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv`

### 3. Paper Trade (For 50-69 Scores)
- Test with $0-100 budget, 7-14 days
- Track: time, revenue, leads, scalability, platform risk
- Decision: SCALE (revenue/hour ≥$20), ITERATE, KILL
- Output: `LEDGER/PAPER_TRADES/`

### 4. Deploy (For SCALE Decisions)
- Increase budget 2x from paper trade
- Track in `FINANCIALS/REVENUE_TRACKER.csv`
- Monitor daily in dashboard

### 5. Monitor (Daily Dashboard Check)
- Watch revenue/hour per method
- Alert on degradation (<$15/hr for 30d)
- Alert on concentration risk (>40% revenue from one method)

### 6. Rebalance (Manual for now, Automated Phase 6)
- **Kill:** Revenue/hour <$15 for 30d OR win rate <30% for 60d
- **Scale:** Revenue/hour >$50 consistently AND scalability ≥7
- **2x winners, kill bottom 50%**

---

## Key Metrics

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| **Backtest score** | ≥70 | Safe to deploy |
| **Revenue/hour** | ≥$20 | Meets minimum efficiency |
| **Scalability** | ≥7/10 | Can 10x without linear effort |
| **Platform risk** | ≤5/10 | Low ban/ToS risk |
| **Win rate** | ≥30% | Method still working |
| **Revenue %** | <40% | Diversification safety |

---

## File Locations

| File | Purpose |
|------|---------|
| `AUTOMATIONS/quant_dashboard.py` | 6-panel terminal dashboard |
| `AUTOMATIONS/backtest_alpha.py` | Alpha validation (0-100) |
| `AUTOMATIONS/paper_trade.py` | Minimal capital testing |
| `LEDGER/ALPHA_STAGING.csv` | All alpha entries |
| `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` | Backtest scores |
| `LEDGER/PAPER_TRADES/PAPER_TRADES.csv` | All paper trades |
| `LEDGER/PAPER_TRADES/PAPER_TRADE_RESULTS.csv` | Completed results |
| `OPS/QUANT_INFRASTRUCTURE_GUIDE.md` | Full documentation (800+ lines) |

---

## What Makes This Different

**Traditional solopreneurs:**
- No systematic validation
- Emotional attachment to failing methods
- No real-time monitoring
- Hope-based scaling

**Quant infrastructure:**
- Every tactic scored 0-100 before deployment
- Paper trade with $0-100 before full capital
- Kill decisions based on data (revenue/hour <$15)
- Real-time dashboard monitoring
- Portfolio approach (30 apps > 1 app)
- Automated rebalancing (Phase 6)

**This is Renaissance Technologies for solopreneurship.**

---

## Next Steps

1. **Launch dashboard:** `python3 AUTOMATIONS/quant_dashboard.py`
2. **Backtest pending alpha:** `python3 AUTOMATIONS/backtest_alpha.py --pending`
3. **Start first real paper trade:** Pick highest-scoring alpha (≥70), test with $100
4. **Monitor daily:** Check dashboard for method performance
5. **Build Phase 5-7:** Continue infrastructure (live revenue tracking, automated rebalancing, AI alpha agent)

---

**The infrastructure is production-ready. Use it.**
