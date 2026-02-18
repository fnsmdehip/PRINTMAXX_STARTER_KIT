# RobloxMaxx - Unit economics (BYOK model)

## The model

BYOK-only (Bring Your Own Key). We never hold, store, or pay for any AI API key. Every user brings their own Claude, OpenAI, or Gemini API key. We sell the intelligence layer (prompts, genre awareness, meta advisor, game scanner, templates), not the compute.

**Zero marginal cost per user for AI.** This is the correct model.

## Revenue

| Plan | Price | What they get | Our cost to serve |
|------|-------|---------------|-------------------|
| Free | $0 | Plugin + basic code gen (BYOK) + community templates | $0 |
| Pro | $9.99/mo | Meta advisor, revenue estimator, game scanner, 5 genre templates, premium game design intelligence | $0 (AI cost = user's key) |

Revenue = Pro subscribers x $9.99/mo.

## Cost structure

| Expense | Monthly cost | Notes |
|---------|-------------|-------|
| Vercel hosting | ~$20/mo | Pro plan, handles API + landing page |
| Domain (robloxmaxx.com) | ~$1/mo ($12/yr) | Namecheap |
| Stripe fees | 2.9% + $0.30 per transaction | ~$0.59 per $9.99 charge |
| Total fixed costs | ~$21/mo | Before any revenue |

## Margin analysis

| Metric | Value |
|--------|-------|
| Revenue per Pro user | $9.99/mo |
| Stripe fee per user | ~$0.59/mo |
| Net revenue per user | ~$9.40/mo |
| API cost per user | **$0** (user pays their own) |
| Marginal cost per user | $0 |
| **Gross margin** | **~94% after Stripe fees** |

## Break-even analysis

| Metric | Value |
|--------|-------|
| Fixed costs | ~$21/mo |
| Break-even subscribers | 3 Pro users ($9.40 x 3 = $28.20) |
| Target: $1K MRR | 100 Pro users |
| Target: $5K MRR | 500 Pro users |
| Target: $10K MRR | 1,000 Pro users |

## Why BYOK is superior

1. **Zero API cost risk.** No surprise bills from heavy users. No margin collapse if someone scaffolds 500 games in a month.
2. **No model routing complexity.** Don't need to decide Haiku vs Sonnet. User picks their model (and pays for it).
3. **Higher trust.** Users see their own API key going directly to Anthropic/OpenAI. No middleman markup anxiety.
4. **Simpler infrastructure.** No usage limits to track, no overage alerts, no credit top-ups.
5. **Better conversion.** Free tier is genuinely unlimited (they just need their own $5 API key). No "50 actions then paywall" friction.

## What we actually sell

The value is NOT the AI calls. Any kid can pipe prompts to Claude. The value is:

1. **Genre-specific system prompts** that produce working Roblox code (tycoon, obby, simulator, RPG, horror)
2. **Meta advisor** - what genres are hot, what monetization works, competitor analysis
3. **Revenue estimator** - DAU to Robux/USD projections per genre
4. **Game scanner** - automated code health checks, exploit detection, performance scoring
5. **Premium templates** - one-click complete games (not 5-line starters)
6. **The Roblox Studio plugin itself** - seamless integration, undo history, multi-turn context

This is an intelligence product, not a compute product. We sell the brain, not the electricity.

## Sensitivity: what if we want to add managed credits later?

If demand emerges for "I don't want to deal with API keys," we can add a managed tier:
- $29/mo for 500 managed actions (we hold the API key, user doesn't need one)
- Use Haiku routing for simple requests, Sonnet for scaffolds
- Weighted avg ~$0.022/action = $11 cost for 500 actions = $18 margin

But start BYOK-only. Add managed credits only if users explicitly ask for it.
