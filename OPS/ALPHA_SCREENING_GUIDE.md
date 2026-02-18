# Alpha Screening System - Institutional Grade

**File:** `AUTOMATIONS/alpha_screening.py`

This is a rigorous multi-factor alpha screening system designed to pass review at a quant fund's solopreneurship arm. NOT a keyword matcher.

## Quick Start

```bash
# Screen single alpha
python3 AUTOMATIONS/alpha_screening.py ALPHA524

# Screen all pending
python3 AUTOMATIONS/alpha_screening.py --pending

# Screen by category
python3 AUTOMATIONS/alpha_screening.py --pending --category COLD_OUTBOUND

# Filter by minimum score
python3 AUTOMATIONS/alpha_screening.py --pending --min-score 60

# Export detailed report
python3 AUTOMATIONS/alpha_screening.py --pending --export-report
```

## Scoring Breakdown (Exactly 100 Points)

| Component | Max Points | What It Measures |
|-----------|-----------|------------------|
| Evidence Quality | 30 | Hard evidence vs vague claims |
| Replicability | 20 | Can we actually implement this? |
| Time Decay | 20 | How fresh is this alpha? |
| Historical Performance | 15 | Did similar tactics work before? |
| ROI Weight | 15 | HIGHEST vs LOW potential |

### Decision Thresholds

| Score | Decision | Action |
|-------|----------|--------|
| >= 70 | SCALE | Deploy with confidence |
| 50-69 | PAPER_TRADE | Test with $0-100 first |
| < 50 | KILL | Do not pursue |

## Category-Specific Decay Rates

Alpha decays at different rates depending on category. Platform arbitrage windows close FAST. App tactics are relatively stable.

| Category | Monthly Decay | 3-Month Value |
|----------|---------------|---------------|
| PLATFORM_ARBITRAGE | 50% | 22% remaining |
| ALGO_TRADING | 40% | 30% remaining |
| ECOM_ARB | 35% | 35% remaining |
| GROWTH_HACK | 30% | 41% remaining |
| AI_INFLUENCER | 25% | 47% remaining |
| TOOL_ALPHA | 20% | 55% remaining |
| COLD_OUTBOUND | 20% | 55% remaining |
| CONTENT_FARM | 15% | 64% remaining |
| SEO_GEO_ASO | 15% | 64% remaining |
| APP_FACTORY | 10% | 74% remaining |
| MONETIZATION | 10% | 74% remaining |

**Implication:** A PLATFORM_ARBITRAGE alpha from 3 months ago loses 78% of its time score. Act fast on arbitrage opportunities.

## Evidence Quality Scoring (30 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Verified revenue | 10 | Tax docs, bank statements, public records |
| Unverified revenue claim | 5 | Screenshot or text claim |
| Specific percentages | 4 | Has % metrics |
| Timeline data | 4 | "in 30 days", "within weeks" |
| Multiple sources | 5 | Confirmed by 2+ independent sources |
| Verified source | 3 | Single credible source |
| Case study | 3 | Real example documented |
| Authentic engagement | 4 | Not botted/suspicious |

**Key insight:** Verified earnings + multiple sources = high confidence. Unverified claims with suspicious engagement = wide confidence interval.

## Replicability Scoring (20 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Clear steps | 4 | Numbered steps or clear methodology |
| Specific tools | 4 | Named tools, not generic "use X" |
| Action verbs | 3 | "create", "build", "send" vs vague descriptions |
| Resources available | 3 | We can actually do this |
| Complexity LOW | 6 | Quick to implement |
| Complexity MEDIUM | 4 | Moderate effort |
| Complexity HIGH | 2 | Significant undertaking |
| Complexity EXTREME | 0 | Massive project |

## Confidence Intervals

Each screening result includes a confidence interval based on evidence quality:

- **High evidence quality:** Tight interval (e.g., 68-82)
- **Low evidence quality:** Wide interval (e.g., 32-68)
- **Unverified earnings:** +5 uncertainty
- **Suspicious engagement:** +8 uncertainty

**Example:** Score 60 with wide interval (40-80) means the alpha could actually be anywhere from mediocre to great. More validation needed.

## Historical Performance Cross-Reference

The system checks `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv` for similar tactics:

- If similar tactics in the same category previously succeeded (SCALE/PAPER_TRADE), score increases
- If similar tactics failed (KILL), score decreases
- No history = neutral (50% assumed)

This creates a feedback loop: deploy methods that historically worked, avoid categories with poor track records.

## ROI Potential Weighting

The ROI_POTENTIAL field from ALPHA_STAGING.csv affects scoring:

| ROI Potential | Weight |
|---------------|--------|
| HIGHEST | 100% |
| HIGH | 85% |
| MEDIUM | 70% |
| LOW | 55% |
| UNKNOWN | 75% |

A LOW ROI potential alpha loses 45% of its ROI component (7 points instead of 15).

## Output Files

- **Results:** `LEDGER/BACKTESTS/BACKTEST_RESULTS.csv`
- **Reports:** `LEDGER/BACKTESTS/SCREENING_REPORT_*.md`

## Key Differences from Old System

| Old (backtest_alpha.py) | New (alpha_screening.py) |
|------------------------|--------------------------|
| Points summed to 115 (wrong) | Exactly 100 points |
| Pure keyword matching | Evidence-based scoring |
| No decay modeling | Category-specific decay |
| No historical cross-reference | Checks past results |
| No confidence intervals | Uncertainty quantified |
| No ROI weighting | ROI potential affects score |
| Binary true/false checks | Graduated scoring |

## Workflow Integration

1. **Daily Research:** Alpha discovered, staged to ALPHA_STAGING.csv
2. **Screening:** `python3 alpha_screening.py --pending`
3. **Review SCALE decisions:** These are ready to deploy
4. **Paper trade PAPER_TRADE decisions:** Test with minimal capital
5. **Ignore KILL decisions:** Do not pursue
6. **Feedback loop:** Results inform future screening

## Example Output

```
SCREENING RESULT: ALPHA930
==================================================
Final Score: 77/100
Confidence Interval: (68 - 86)
Decision: SCALE

Category: COLD_OUTBOUND
ROI Potential: HIGHEST
Age: 0.0 months
Decay Rate: 20%/month

--- Score Breakdown ---
Evidence Quality: 21/30
  Verified revenue, Specific %, Multi-source, Authentic engagement
Replicability: 15/20
  Clear steps, Named tools, Resources available, Complexity: MEDIUM
Time Freshness: ~20/20
Historical Performance: ~7/15
  0 similar tactics, 50% success
ROI Weight: ~15/15
```

## Best Practices

1. **Screen before deploying any alpha** - Never skip this step
2. **Pay attention to confidence intervals** - Wide intervals = more validation needed
3. **Act fast on PLATFORM_ARBITRAGE** - 50% decay per month
4. **Build track record** - More historical data = better future screening
5. **Review SCALE decisions weekly** - These are your highest-conviction bets
6. **Use --export-report for deep analysis** - Get detailed breakdowns of top performers

## Comparison to Renaissance Technologies Approach

| RenTech Principle | Implementation |
|-------------------|----------------|
| Statistical validation | 0-100 scoring with evidence weighting |
| Pattern recognition | Historical cross-reference |
| Decay modeling | Category-specific alpha decay |
| Risk management | Confidence intervals + ROI weighting |
| Continuous learning | Results feed back into historical data |
| No emotional attachment | KILL decisions are final |
