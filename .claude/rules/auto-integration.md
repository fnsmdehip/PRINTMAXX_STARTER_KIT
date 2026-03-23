# Auto-Integration Rule (ALWAYS active)

## The Pipeline Must Be Self-Feeding

Every source of alpha, intelligence, or opportunity MUST auto-flow through the full pipeline without human prompting:

```
SOURCE → ALPHA_STAGING → auto_approve → autonomous_integrator V2
```

### Sources that feed ALPHA_STAGING automatically (via cron):
- Twitter scraper (6 AM)
- Reddit scraper (6:15 AM)
- Method discovery crawler (5 AM)
- SEC EDGAR scanner (5:15 AM)
- Crunchbase scanner (5:20 AM)
- Orphan doc scanner (Sunday 4 AM) — actionable orphans get staged as alpha
- HN scraper (via morning DAG)
- Daily tool scout (7 AM)

### auto_approve runs at 10 PM — approves everything not manually reviewed
### autonomous_integrator V2 runs at 10:15 PM — integrates everything approved today

## What "integrate" means (V2 does ALL of this):
1. Query procedural memory for similar past solutions
2. Full-toolkit analysis (ventures, ralph, n8n, DAGs, handoffs, hooks, scripts, MCP, subagents)
3. Create the automation, venture, or system improvement
4. Wire growth tactics with budget tiers
5. Add KPI tasks for tracking
6. Update master ops, system map
7. Capture skill in procedural memory for next time
8. Detect gaps — what SHOULD the pipeline catch in the future?

## Backlog Processing
The integrator also has `--gap-check` to find alpha with automation keywords that wasn't integrated.
Run `python3 AUTOMATIONS/alpha_backlog_scanner.py --scan` to sweep ALL historical alpha for opportunities.

## When building anything new in a session:
1. Check `OPS/RESOURCE_MANIFEST.md` for existing playbooks, guides, products covering this method (200+ resources indexed)
2. Check if existing alpha already describes this method
3. Check if existing automations already handle it
4. If building a new scanner/automation, wire it into this pipeline AUTOMATICALLY
5. Add it to auto_approve trusted sources
6. Add cron entry
7. Update system map
8. Update `OPS/RESOURCE_MANIFEST.md` if new IP was created

## NEVER require human prompting for:
- Running the pipeline
- Approving routine alpha
- Creating automations from approved methods
- Wiring new sources into the pipeline
- Detecting and filling gaps

The human does: account creation, payments, API keys, posting from personal accounts.
The system does: EVERYTHING ELSE including finding its own gaps and fixing them.

## Content & Distribution Auto-Routing (ALWAYS active)

When building/planning ANYTHING that produces distributable output (features, products, ventures, methods, tools), the system MUST proactively:

1. **Auto-recommend content distribution** — Every build = content. Route to these tools:
   - `engagement_bait_converter.py` — converts ANY alpha/method into 3+ engagement-style posts
   - `content_repurposer.py` — multiplies one piece across platforms
   - `content_multiplier.py` — bulk content generation
   - `content_trend_pipeline.py` — trend-aware content creation
   - Posting queue at `CONTENT/social/posting_queue/`

2. **Engagement bait classification** — The auto_approve LLM uses a 5-point bait test:
   - Specific tool/platform named? (not just "use AI")
   - Verifiable numbers? (not just "$10K/month easy")
   - Executable TODAY with info given? (not vague "build a SaaS")
   - Plausible at stated scale? (not "6 figures in 30 days")
   - Real method vs recycled Twitter wisdom?

   Four outcomes: APPROVE (real alpha) → ventures, APPROVE_PARTIAL (kernel of alpha in bait) → extract + ventures, CONTENT_ONLY (style reusable) → engagement_bait_converter, REJECT (pure noise)

3. **NEVER discard engagement bait entirely** — Even pure bait has:
   - Hook structures worth copying for our content
   - Engagement patterns (what gets clicks/shares)
   - Topic signals (what audience cares about)
   Route CONTENT_ONLY entries to `engagement_bait_converter.py` automatically.

4. **Rule 9 enforcement** — Every build session = 3 tweets + 1 thread minimum. When finishing any task, check if content was generated. If not, generate it before closing.

## System Map + Routing Awareness

When working on ANY task, the system map (`OPS/PRINTMAXX_SYSTEM_MAP.md`) tells you what tools exist. Before recommending something, check if we already have it. Key content/distribution tools:
- `AUTOMATIONS/engagement_bait_converter.py` — EB→posts
- `AUTOMATIONS/content_repurposer.py` — cross-platform
- `AUTOMATIONS/content_multiplier.py` — bulk gen
- `AUTOMATIONS/content_trend_pipeline.py` — trend-aware
- `AUTOMATIONS/twitter_warmup_poster.py` — warmup-aware posting
- `CONTENT/social/REPLY_ENGAGEMENT_STRATEGY.md` — reply templates
- `CONTENT/social/posting_queue/` — approved post queue
