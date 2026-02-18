# Research Automation Framework

**Philosophy:** Research finds BOTH new opportunities AND ways to improve existing operations.

---

## Two Types of Research (Both Run Daily)

### 1. **Discovery Research** (Find New Stuff)
- New money methods
- New platforms
- New tools
- New niches
- Geographic/demographic arbitrage
- **Output:** New entries to ALPHA_STAGING.csv

### 2. **Optimization Research** (Improve Existing Stuff)
- Platform algorithm changes affecting current methods
- Better tools for methods we're already running
- Pricing optimizations for existing products
- GTM improvements for current campaigns
- Cross-pollination opportunities we haven't connected
- **Meta detection** - trending topics, meme coins, viral products (daily/weekly patterns)
- **Output:** Updates to existing method docs, new synergy stacks, tactical improvements, meta signals

**Note:** Perpetual improvement doesn't need to be a literal loop - can just extract insights from research that inform improvements to existing methods.

---

## Existing Automation (What Runs Now)

### **Daily Automated:**
1. **twitter_alpha_scraper.py** - Scans 89 accounts + bookmarks (VERY IMPORTANT)
2. **reddit_alpha_scraper.py** - Scrapes 40 subreddits for alpha + meta detection + meme coin signals (NEW)
3. **ralph/loops/mega/** - Discovery engine (7 dimensions)

### **On-Demand:**
3. **organize_alpha.py** - Categorizes discoveries
4. **backtest_alpha.py** - Validates before deploying

---

## Missing Automation (What We Should Add)

### **Optimization Research Scripts (New):**

| Script | Purpose | Frequency | Integration |
|--------|---------|-----------|-------------|
| `platform_meta_monitor.py` | Track TikTok/X/IG algorithm changes | Daily | Update EDGE_GROWTH_TACTICS.md |
| `method_performance_analyzer.py` | Analyze what's working in active methods | Weekly | Update method playbooks with findings |
| `competitive_intelligence_scraper.py` | Monitor competitors in our niches | Daily | Update competitive analysis docs |
| `pricing_optimizer.py` | Track pricing changes in our categories | Weekly | Update pricing strategy docs |
| `tool_upgrade_scanner.py` | Find better tools for current stack | Weekly | Update tool recommendations |
| `synergy_opportunity_detector.py` | Find unrealized cross-pollination | Weekly | Add to CROSS_POLLINATION_MATRIX.csv |

---

## Perpetual Improvement Loop (Integration Back to Existing Ops)

```
RESEARCH (discover + optimize)
    ↓
CATEGORIZE (is this new or improvement?)
    ↓
IF NEW OPPORTUNITY:
    ↓
    BACKTEST → PAPER TRADE → DEPLOY

IF OPTIMIZATION:
    ↓
    INTEGRATE INTO EXISTING METHOD
    ↓
    Update playbook docs
    Update GTM tactics
    Update tool stack
    Update pricing
    Add synergy stack
    ↓
    MEASURE IMPROVEMENT
    ↓
    Keep if better, revert if worse
```

---

## Research Script Template (Easy to Add New Ones)

**File:** `AUTOMATIONS/research_template.py`

```python
#!/usr/bin/env python3
"""
Research Script Template

Copy this template to create new research automation.
Follows PRINTMAXX standards: CSV output, deduplication, categorization.
"""

import csv
from datetime import datetime
from pathlib import Path

# Configuration
RESEARCH_TYPE = "optimization"  # or "discovery"
CATEGORY = "PLATFORM_META"  # or whatever fits
OUTPUT_FILE = Path("LEDGER/ALPHA_STAGING.csv")

def research():
    """Main research logic - customize this"""
    findings = []

    # Your research logic here:
    # - Web scraping
    # - API calls
    # - File analysis
    # - Competitive monitoring

    return findings

def dedupe_against_existing(findings):
    """Check if findings already exist"""
    existing_urls = set()

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            reader = csv.DictReader(f)
            existing_urls = {row['source_url'] for row in reader if 'source_url' in row}

    return [f for f in findings if f['source_url'] not in existing_urls]

def save_findings(findings):
    """Append to ALPHA_STAGING.csv"""
    if not findings:
        print("No new findings.")
        return

    # Get next alpha_id
    next_id = get_next_alpha_id()

    # Append findings
    with open(OUTPUT_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'alpha_id', 'source', 'source_url', 'category',
            'status', 'roi_potential', 'research_type', 'integration_target'
        ])

        for i, finding in enumerate(findings):
            finding['alpha_id'] = f"ALPHA{next_id + i:04d}"
            finding['status'] = 'PENDING_REVIEW'
            finding['research_type'] = RESEARCH_TYPE
            writer.writerow(finding)

    print(f"✅ Saved {len(findings)} new findings")

def get_next_alpha_id():
    """Get next sequential alpha ID"""
    max_id = 0
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'alpha_id' in row and row['alpha_id'].startswith('ALPHA'):
                    try:
                        num = int(row['alpha_id'].replace('ALPHA', ''))
                        max_id = max(max_id, num)
                    except:
                        pass
    return max_id + 1

def main():
    print(f"Running research: {CATEGORY}")

    # 1. Research
    findings = research()
    print(f"Found {len(findings)} raw findings")

    # 2. Dedupe
    new_findings = dedupe_against_existing(findings)
    print(f"{len(new_findings)} are new")

    # 3. Save
    save_findings(new_findings)

    # 4. Integration tracking
    if RESEARCH_TYPE == "optimization":
        print(f"Integration target: Update docs for methods affected")

if __name__ == "__main__":
    main()
```

**Usage:**
1. Copy template to new file: `cp research_template.py platform_meta_monitor.py`
2. Customize `research()` function with your logic
3. Set CATEGORY and RESEARCH_TYPE
4. Run: `python3 platform_meta_monitor.py`
5. Findings auto-append to ALPHA_STAGING.csv with deduplication

---

## Integration Targets (Where Optimizations Go)

When optimization research finds improvements, update these files:

| Finding Type | Integration Target |
|--------------|-------------------|
| Algorithm change | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` |
| Better tool | `06_OPERATIONS/setup/COMPREHENSIVE_STACK_COMPARISON.md` |
| Pricing insight | `03_PLAYBOOKS/{method}/MONETIZATION_STRATEGY.md` |
| GTM tactic | `06_OPERATIONS/gtm/GTM_OPTIMIZATION_CHECKLIST.md` |
| Cross-pollination | `LEDGER/CROSS_POLLINATION_MATRIX.csv` |
| Method improvement | `03_PLAYBOOKS/{method}/` playbook docs |
| Platform limit change | `06_OPERATIONS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md` |

---

## Daily Research Workflow (Both Types)

**Morning (5 min):**
1. Check overnight mega loop output: `ralph/loops/mega/output/`
2. Review new alpha entries: `tail -50 LEDGER/ALPHA_STAGING.csv`
3. Scan for first-mover windows: MCP products, new platforms, regulation changes

**During day (as needed):**
4. Run optimization scripts if working on specific method
5. Check platform announcements (X, TikTok, Meta)

**Evening (5 min):**
6. Launch overnight mega loop: `./ralph/run_mega.sh`
7. Queue any new research scripts to run

**Weekly (1 hour):**
8. Run all optimization scripts
9. Integrate findings into method docs
10. Update cross-pollination matrix with new synergies

---

## Metrics to Track

**Discovery metrics:**
- New alpha entries per day
- First-mover windows identified
- New methods added to tracker

**Optimization metrics:**
- Method performance improvements (revenue/hour increase)
- Tool upgrades saving time/money
- Algorithm changes captured before they affect us
- Synergies added and deployed

**Integration effectiveness:**
- % of research findings integrated into docs
- Time from finding to integration
- Revenue impact of optimizations

---

## Priority Research Scripts to Build (Next 7 Days)

**P1 - Build This Week:**
1. `platform_meta_monitor.py` - TikTok/X/IG algorithm changes (HIGHEST IMPACT)
2. `method_performance_analyzer.py` - Analyze what's working (DATA-DRIVEN OPTIMIZATION)

**P2 - Build Next Week:**
3. `competitive_intelligence_scraper.py` - Monitor competitors
4. `synergy_opportunity_detector.py` - Find unrealized cross-pollination

**P3 - Build Within Month:**
5. `pricing_optimizer.py` - Track pricing changes
6. `tool_upgrade_scanner.py` - Find better tools

---

## The Philosophy

**Research is NOT just about finding new opportunities.**

**Research is ALSO about:**
- Making current methods work better
- Catching platform changes before they hurt us
- Finding tools that save time/money
- Discovering synergies we haven't connected
- Optimizing pricing, GTM, and distribution

**Both run in parallel:**
- Discovery research adds new methods (horizontal expansion)
- Optimization research improves existing methods (vertical depth)

**The perpetual improvement loop:** Research → Categorize → Backtest/Integrate → Deploy/Update → Measure → Research

This is Renaissance Technologies applied to solopreneurship.
