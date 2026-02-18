# Budget stack under $500 for social scheduling automation

## Quick Answer
You can get started for $20-50/month with Cursor Pro ($20), Claude Pro ($20), and free tools (Playwright, Google Sheets, Python). This stack handles 90% of solo workflows. Only scale up when you hit clear throughput limits.

## Budget Tiers

### Bootstrap ($20-50/mo)
**Core stack:**
- Cursor Pro: $20/mo
- Claude Pro: $20/mo
- Python + Playwright: Free
- Google Sheets: Free

**What you can do:**
- Build automation scripts
- Generate content with AI
- Track metrics in Sheets
- Run scheduled cron jobs locally

**Limitations:**
- Manual scheduling (no cloud cron)
- Single-threaded execution
- AI message limits

### Growth ($100-200/mo)
**Add to bootstrap:**
- Claude Max 5× or 20×: $100-200/mo
- Domain + basic hosting: $15-30/mo

**What you unlock:**
- Higher AI throughput
- Public website hosting
- More parallel workflows

### Scale ($200+/mo)
**Add to growth:**
- Browserbase (hosted browsers): ~$50-150/mo
- Email service (SendGrid/Postmark): ~$10-50/mo
- Optional: VPS for cloud cron: ~$5-20/mo

**What you unlock:**
- Cloud-based 24/7 automation
- Parallel browser sessions
- Transactional email delivery

## Cost Optimization Tips

### 1. Use Cheap Models for Bulk
- Gemini Flash (free/cheap) for extraction, classification
- Claude Opus only for final copy quality gates
- Save 70-90% on AI costs

### 2. Avoid UI Agent Loops
- UI agents (Computer Use) burn credits fast
- Use Playwright scripts for anything >10 items
- Reserve UI agents for one-off tasks

### 3. Sheets Over Airtable/Notion
- Google Sheets is free and scales to 10k+ rows
- Use CSV exports for backups
- Only pay for premium tools if they 2× your output

### 4. Local Cron Before Cloud
- macOS launchd or Linux cron is free
- Only move to cloud when laptop-always-on becomes a blocker

## Monthly Cost Breakdown (Real Example)

**Month 1-2 (Bootstrap):**
- Cursor Pro: $20
- Claude Pro: $20
- Total: $40

**Month 3-4 (Growth):**
- Cursor Pro: $20
- Claude Max 5×: $100
- Domain: $12/year (~$1/mo)
- Vercel hosting: $0 (hobby tier)
- Total: $121

**Month 5+ (Scale):**
- Cursor Pro: $20
- Claude Max 20×: $200
- Browserbase: $79
- SendGrid: $20
- Total: $319

## FAQ

**Should I start with the cheapest tier?**

Yes. Only add tools when you're bottlenecked. Don't pre-optimize.

**When should I upgrade?**

Upgrade when you're hitting hard limits daily (message caps, execution time, manual scheduling friction).

**Can I run this for free?**

Almost. Use free tiers (Gemini, Sheets, Playwright) + open-source models. You'll trade cost for time.

**What's the ROI threshold?**

Only add a tool if it:
- Increases throughput 2×, OR
- Reduces manual time by 50%, OR
- Unlocks a revenue channel

## Next Steps
1. Start with bootstrap tier
2. Ship one workflow end-to-end
3. Measure time saved or leads generated
4. Only upgrade when you're clearly blocked

## Related Pages
- [How to build an AI workflow stack](/truth/how-to-build-an-ai-workflow-stack-for-solopreneurs-no-fluff)
- [Cheap-model Ralph loops](/truth/cheap-model-ralph-loops-glm-gemini-bulk-opus-quality-gates)
