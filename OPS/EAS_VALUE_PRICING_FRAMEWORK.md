# EAS Value-Based Pricing Framework (T021)

Source: BotBorne 2026 survey — solopreneurs using AI agents report 340% avg revenue increase.

## The Problem

EAS pilots priced at $500-1,500 (time-cost). If EAS automates 8-15h/week for a $150K/yr business:
- Hourly rate: ~$72/hr
- Weekly time saved: 8-15h = $576-$1,080/week = $2,304-$4,320/month
- Current pricing captures 12-35% of first-month value
- Should capture 25-30% of ongoing value (standard SaaS multiple)

## Value Calculator

```
Inputs:
  team_size: int
  avg_hourly_rate: float (default $72 for $150K business)
  automatable_hours_per_week: float (default 10)

Outputs:
  monthly_value_recovered = team_size * avg_hourly_rate * automatable_hours_per_week * 4.33
  recommended_pilot_price = monthly_value_recovered * 0.30  # 30% of first month
  recommended_retainer = monthly_value_recovered * 0.15     # 15% ongoing
```

## Pricing Tiers

| Tier | Client Profile | Automatable Hours | Monthly Value | Pilot Price | Retainer |
|------|---------------|-------------------|---------------|-------------|----------|
| Starter | Solo operator, $80K rev | 5h/week | $1,730 | $520 | $260/mo |
| Growth | Small team (2-3), $250K rev | 12h/week | $4,150 | $1,245 | $620/mo |
| Scale | Agency (5-10), $500K+ rev | 25h/week | $8,660 | $2,598 | $1,300/mo |

## Anchoring Strategy

1. Lead with value recovered, not features delivered
2. Show ROI calculator on EAS website (interactive)
3. Case study template: "Client X spent Y hours/week on Z. After EAS automation: 2 hours/week. Value recovered: $W/month."
4. Position pilot as "risk-free ROI test" — if automation doesn't save 3x pilot cost in month 1, full refund

## Implementation

- Add interactive ROI calculator to enterpriseautomation.solutions
- Update cold email templates with value-first framing
- Shakespeare agent generates content around "implementation gap costs you $X/month" angle
- Quinn agent warm outreach references specific value potential based on lead's company size


---

## Pending Enhancement (ALPHA24134, Score: 32)

**Source:** @dwarkesh_sp (high-signal-accounts) | **URL:** https://x.com/dwarkesh_sp/status/2032528369028370806
**Added:** 2026-03-13T16:50:49-04:00

The AI supply chain has the craziest value cascade of any industry in the world.

thinks that over the next five years, the biggest bottleneck to deploying AI will be EUV machines.

ASML sells EUV machines for $300-400 million. You need about three and a half machines, so $1.2

