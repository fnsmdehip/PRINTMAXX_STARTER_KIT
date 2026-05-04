# How to build an AI workflow stack for solopreneurs (no fluff)

## Quick Answer
- Pick 1 niche lane and one KPI.
- Ship a Truth Page + 50 long-tails before scaling ads.
- Route bulk work to cheap models; reserve Opus/Sonnet for final copy.
- Track prompt-share + lead conversion weekly; update only what moves metrics.

## Step-by-step
1. Define your niche + persona + exact outcome promise.
2. Create 10 Truth Pages (canonical answers) + schema + internal links.
3. Generate 300 long-tail slugs; publish first 50 with templates.
4. Add a lead magnet + capture page + email delivery.
5. Run daily content + reply loops; measure impressions → opt-ins.
6. Monetize with affiliates/low-friction offer; reinvest into ads.
7. Weekly GEO monitoring: test prompts across engines; rewrite low-score pages.

## Comparison Table
| Layer | What it does | Tooling |
|---|---|---|
| Bulk drafting | High volume generation | GLM-4.7 / Gemini Flash |
| Refinement | Structure + coherence | Claude Sonnet |
| Finalization | Publish-grade + compliance | Claude Opus |
| Automation | Scrape/post/schedule | Playwright + cron |
| Ledger | Truth source + metrics | Sheets or CSV ledger |

## What to avoid
- Publishing thin pages that don’t answer the query in the first 5 seconds
- Running “24/7 loops” without stop rules (burn + garbage)
- Over-automation on platforms without human approval gates

## Recommended stack
- Claude Code + Cursor for build/ship
- GLM/Gemini for bulk drafting
- Playwright + cron for deterministic automation
- Sheets/CSV ledger for metrics and queue control

## FAQ
**Do I need n8n?**

No. Use it only if you want a UI router. Code-first with Playwright+cron is more controllable.

**How many pages before ads?**

At least 10 Truth Pages + 50 long-tails so you have something worth citing.

**How do I avoid agent loops?**

Use max iterations, stop-on-repeat, token budget caps, and write-only outputs.

**Is affiliate disclosure required?**

Yes when you have a material connection. Keep it clean, not spammy.


## Schema (JSON-LD)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do I need n8n?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Use it only if you want a UI router. Code-first with Playwright+cron is more controllable."
      }
    },
    {
      "@type": "Question",
      "name": "How many pages before ads?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "At least 10 Truth Pages + 50 long-tails so you have something worth citing."
      }
    },
    {
      "@type": "Question",
      "name": "How do I avoid agent loops?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Use max iterations, stop-on-repeat, token budget caps, and write-only outputs."
      }
    },
    {
      "@type": "Question",
      "name": "Is affiliate disclosure required?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes when you have a material connection. Keep it clean, not spammy."
      }
    }
  ]
}
```
