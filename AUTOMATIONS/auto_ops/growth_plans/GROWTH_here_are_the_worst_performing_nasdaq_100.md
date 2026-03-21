# Growth Plan: Here are the worst performing NASDAQ 100 $QQQ stocks so far 

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo content engagement + $500-2000/mo if outbound to struggling companies converts

---

## Tactics

1. Fintwit engagement farming — stock loss lists trigger loss-aversion sharing (2-5x normal engagement)
2. Quote-tweet major fintwit accounts with contrarian take on their picks
3. Cross-post data visualizations to LinkedIn for B2B reach
4. Tag company handles in posts — employees share/engage defensively
5. Thread format: worst 10 → what they have in common → contrarian bottom-fishing take

## Budget Tier Strategies

### FREE
Organic fintwit posts, quote-tweet strategy, LinkedIn cross-post, Reddit r/stocks r/investing threads, tag company handles for defensive engagement

### LOW
$10-30/mo boost top-performing stock data posts on Twitter, A/B test hook formats

### MID
$50-100/mo Twitter ads targeting fintwit audience, sponsor newsletter placement in finance newsletters

## Daily Actions

- [ ] Build nasdaq_underperformer_pipeline.py using yfinance (free) to pull NASDAQ 100 YTD performance
- [ ] Rank and format top 10-20 worst performers with % change, sector, and context
- [ ] Generate 3 tweet variants (list format, contrarian take, sector analysis) + 1 thread via engagement_bait_converter.py
- [ ] Flag companies with >25% decline as EAS outbound candidates (they are cutting vendor costs)
- [ ] Push content to CONTENT/social/posting_queue/, push leads to AUTOMATIONS/leads/
- [ ] Schedule cron: weekly Monday 7 AM
- [ ] Wire into existing content_factory chain for cross-platform distribution

## Tooling

```json
{
  "browser": "none",
  "email": "eas_lead_pipeline.py for outbound to struggling companies",
  "content": "content_factory + engagement_bait_converter.py"
}
```
