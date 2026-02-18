# RETARDMAXX DAILY STARTUP PROTOCOL

**Philosophy:** Quantitative precision. Zero overthinking. Ship > plan.

---

## Template (What You See Every Morning)

```
## TODAY - [Date]

### CRITICAL (Do First - 30 min max)
- [ ] Manual task 1
- [ ] Manual task 2
- [ ] Manual task 3

### REVENUE (Focus - 2-4 hours)
- [ ] Revenue-generating task 1
- [ ] Revenue-generating task 2

### AUTOMATION (Run These - 5 min)
- [ ] python3 script1.py
- [ ] python3 script2.py
- [ ] ./ralph/run_mega.sh (overnight)

### REVIEW (If Time - 1 hour)
- [ ] Review agent outputs
- [ ] Approve alpha entries
- [ ] Check metrics

### META CHECK
Current focus: [What we're prioritizing this week]
Blockers: [What's blocking revenue]
Win: [What worked yesterday]

### RESEARCH (Always Running)
- [ ] Daily research auto-runs overnight (./ralph/run_mega.sh)
- [ ] Check for new platform changes (TikTok, X, IG algorithm updates)
- [ ] Monitor high-signal sources for short-term opportunities
- [ ] Review new alpha entries (LEDGER/ALPHA_STAGING.csv)
- [ ] Quick scan: Any first-mover windows? (MCP products, new platforms, regulation changes)

**Philosophy:** Research never stops. BUT execution of existing assets takes priority over discovering new assets until first dollar is made.

**Balance:**
- Pre-revenue: 80% execute existing, 20% research new
- Post-revenue: 60% execute existing, 40% research new
- Post-scale: 50% execute, 50% research (perpetual improvement loop)
```

---

## Generation Logic (What Agent Checks)

**Agent reads:**
1. `ralph/loops/mega/checkpoints/` - Human approval items
2. `LEDGER/ALPHA_STAGING.csv` - Pending review (count)
3. `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` - What scored SCALE
4. `FINANCIALS/REVENUE_TRACKER.csv` - What's generating revenue
5. `OPS/SESSION_HANDOFF.md` - What was in progress
6. `OPS/CAPITAL_GENESIS_HUMAN_TASKS.md` - Manual infrastructure blockers

**Agent generates:**
- **CRITICAL:** Highest-ROI manual tasks (payments, approvals, account setup)
- **REVENUE:** Focus on what can generate first dollar soonest
- **AUTOMATION:** Scripts to run (backtest, paper trade, dashboard, research)
- **REVIEW:** Low-priority batch tasks
- **META CHECK:** One-line zoom out

---

## Example (What It Actually Looks Like)

```
## TODAY - Feb 2, 2026

### CRITICAL (Do First)
- [ ] Gumroad signup + Stripe connect (5 min)
- [ ] List 4 PDFs on Gumroad ($0-$451 Week 1) (2 hours)
- [ ] Upload 12 Buffer CSVs (295 posts) (10 min)

### REVENUE (Focus)
- [ ] Compile Paywall Playbook PDF from existing docs
- [ ] Compile Cold Email Playbook PDF from existing docs
- [ ] Write Gumroad product descriptions (use copy-style.md)

### AUTOMATION (Run These)
- [ ] python3 AUTOMATIONS/quant_dashboard.py (leave running)
- [ ] python3 AUTOMATIONS/backtest_alpha.py --pending
- [ ] ./ralph/run_mega.sh (tonight before bed)

### REVIEW (If Time)
- [ ] /review-alpha (47 entries pending)
- [ ] Check ralph/loops/mega/checkpoints/PENDING_PURCHASES.md
- [ ] Read OPS/PRINTMAXX_STRATEGIC_SYNTHESIS_FEB_2026.md

### META CHECK
Focus: First dollar (Gumroad PDFs = highest probability)
Blocker: None - all files ready, just need to compile + list
Win: Extracted 2 major deliverables (revenue_projector.py, synthesis doc)

### RESEARCH (Running in Background)
- [✓] Mega loop running overnight (147 iterations complete)
- [ ] Platform check: TikTok announced 1+ min format pays 10-20x old fund
- [ ] Alpha review: 47 PENDING_REVIEW entries (backtest first)
- [ ] First-mover scan: MCP Apps launched Jan 26 (window shrinking)
```

---

## How to Use

**Every morning:**
1. Say: "Daily todo" or "What's the retardmaxx list"
2. Agent generates list based on current state
3. You execute top to bottom
4. Check off items as you go
5. No overthinking, just do

**Visual format:**
- Max 10 items total
- Checkbox format (satisfying to check off)
- Time estimates in parentheses
- One-line items (no paragraphs)

**Priority logic:**
1. Revenue-generating > infrastructure
2. Manual > automated (you're the bottleneck)
3. Unblocking > optimization
4. Shipping > planning

---

## Integration with Quant Systems

**Daily startup sequence:**
1. Generate todo list (agent reads overnight outputs)
2. Run quant dashboard (`python3 AUTOMATIONS/quant_dashboard.py`)
3. Execute CRITICAL section
4. Execute REVENUE section
5. Run AUTOMATION section
6. End of day: Launch overnight ralph loop

**This is the frictionless loop.**

---

## What This Prevents

❌ "What should I work on today?"
❌ Getting lost in one optimization rabbit hole
❌ Overthinking what to do next
❌ Analysis paralysis
❌ Forgetting to run overnight loops

✅ Start every day with clear priorities
✅ Zoom out view (META CHECK)
✅ Always know what's blocking revenue
✅ Ship > plan
✅ Quant precision without overthinking
