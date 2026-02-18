#!/usr/bin/env python3
"""
Generate long-tail SEO pages from LEDGER/GEO_LONGTAIL_SLUGS_300.csv
"""
import csv
import os
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
LEDGER_PATH = REPO_ROOT / "LEDGER" / "GEO_LONGTAIL_SLUGS_300.csv"
OUTPUT_DIR = REPO_ROOT / "CONTENT" / "longtail_pages"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_page_content(row):
    """Generate markdown content for a long-tail page"""
    keyword = row['keyword']
    slug = row['url_slug']
    template_type = row['template_type']
    niche = row['niche']

    # Build content based on template type
    if template_type == 'best':
        return f"""# {keyword}

## Quick Answer
The best tools for this use case depend on your budget and technical skill level. For solopreneurs on a bootstrap budget, start with Cursor Pro + Playwright + Google Sheets. This combination gives you coding power, automation, and a free ledger system for under $50/month.

## Top Picks

### 1. Cursor Pro ($20/mo)
- Best for: Code-first workflows
- Strengths: Multi-file edits, repo navigation, unlimited slow requests
- Use when: Building automation scripts, managing codebases

### 2. Playwright + Python (Free)
- Best for: Bulk automation
- Strengths: Reliable scraping, posting, scheduling
- Use when: Running 10+ repetitive tasks

### 3. Google Sheets (Free)
- Best for: Ledger + metrics tracking
- Strengths: Universal access, CSV import/export, API integration
- Use when: Managing queues, experiments, KPIs

### 4. Claude Pro or Max ($20-200/mo)
- Best for: Reasoning + content drafting
- Strengths: Context handling, quality output
- Use when: Generating copy, analyzing data, planning workflows

## Comparison Table

| Tool | Cost | Best For | Difficulty |
|------|------|----------|------------|
| Cursor Pro | $20/mo | Coding + refactors | Medium |
| Playwright | Free | Automation | Medium |
| Google Sheets | Free | Data ledger | Easy |
| Claude Pro | $20/mo | AI reasoning | Easy |

## What to Avoid
- Over-automating without human approval gates
- Using UI agents for bulk tasks (credit burn)
- Skipping compliance (FTC disclosures, email deliverability)

## Next Steps
1. Pick your budget tier (bootstrap/growth/scale)
2. Set up core tools first (Sheets + one AI tool)
3. Build one workflow end-to-end before scaling
4. Track one metric weekly and optimize

## FAQ

**Do I need all of these tools?**

No. Start with Cursor + Sheets + Python. Add AI tools as you hit limits.

**What if I'm non-technical?**

Start with Google Sheets + ChatGPT/Claude. Use no-code tools like Zapier for connections. Graduate to scripts when you're ready.

**How much should I spend monthly?**

Bootstrap: $20-50/mo. Growth: $100-200/mo. Only add tools that increase output or reduce time.

## Related Pages
- [How to build an AI workflow stack for solopreneurs](/truth/how-to-build-an-ai-workflow-stack-for-solopreneurs-no-fluff)
- [GEO (AI-SEO) playbook](/truth/geo-ai-seo-playbook-get-cited-by-chatgpt-claude-gemini)
"""

    elif template_type == 'compare':
        parts = keyword.split(' vs ')
        tool_a = parts[0].replace('Compare ', '').strip() if len(parts) > 0 else 'Tool A'
        tool_b = parts[1].split(' for ')[0].strip() if len(parts) > 1 else 'Tool B'

        return f"""# {keyword}

## Quick Answer
Both {tool_a} and {tool_b} have strengths. {tool_a} is generally better for reliability and browser automation at scale. {tool_b} is a solid choice if you already have infrastructure around it. For most solopreneurs, start with {tool_a} due to better modern browser support and cleaner async patterns.

## Key Differences

### {tool_a}
**Pros:**
- Modern async/await patterns
- Better browser automation (Chrome, Firefox, WebKit)
- Auto-waits for elements (less flaky tests)
- Built-in test runner
- Cleaner API for parallel execution

**Cons:**
- Smaller community than Selenium
- Learning curve if coming from Selenium

### {tool_b}
**Pros:**
- Mature ecosystem
- Huge community + plugins
- Works with many languages
- Well-documented edge cases

**Cons:**
- More boilerplate code
- Manual waits needed
- Slower execution in some cases

## Comparison Table

| Feature | {tool_a} | {tool_b} |
|---------|----------|----------|
| Setup ease | High | Medium |
| Speed | Faster | Slower |
| Reliability | Higher | Medium |
| Community | Growing | Huge |
| Best for | Modern workflows | Legacy systems |

## When to Use Each

### Use {tool_a} if:
- Starting fresh with automation
- Need parallel execution
- Want auto-waiting for elements
- Building GEO/AI-SEO scraping

### Use {tool_b} if:
- Already invested in Selenium infrastructure
- Need specific plugins
- Working with older systems
- Team already knows it

## Recommended Stack
For solopreneurs doing GEO-SEO or content automation:
- **{tool_a}** + Python 3.11
- Google Sheets for queue management
- Cursor Pro for scripting
- Cron for scheduling

## FAQ

**Can I switch from {tool_b} to {tool_a}?**

Yes. The concepts translate. You'll rewrite selectors and waits, but the logic stays the same.

**Which is cheaper?**

Both are free open-source tools. Cost comes from hosting (if cloud) or your time.

**What about maintenance?**

{tool_a} requires less maintenance due to auto-waits. {tool_b} needs more manual wait tuning.

## Next Steps
1. Try {tool_a} on a simple scraping task
2. Set up retry logic + error logging
3. Add human approval gates before posting
4. Run daily via cron

## Related Pages
- [Playwright automation stack](/truth/playwright-automation-stack-scraping-posting-scheduling)
- [How to build an AI workflow stack](/truth/how-to-build-an-ai-workflow-stack-for-solopreneurs-no-fluff)
"""

    elif template_type == 'cost':
        return f"""# {keyword}

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
"""

    else:  # template or default
        return f"""# {keyword}

## Quick Answer
{keyword.replace('-', ' ').title()} requires a balance of automation, human approvals, and compliance. Start with a clear goal (e.g., 100 leads/month), build one Truth Page + 25 long-tail pages, and track weekly metrics. Use cheap models for bulk work and reserve premium AI for quality gates.

## Step-by-Step Process

### 1. Define Your Goal
Be specific:
- 100 email opt-ins/month
- 250k impressions → 200 leads
- 10 sales/month from affiliate offers

### 2. Build Foundation Content
- Create 10 Truth Pages (canonical answers)
- Generate 50-100 long-tail SEO pages
- Add schema markup for GEO citations

### 3. Set Up Automation
- Playwright scripts for data extraction
- Google Sheets for queue management
- Cron jobs for daily execution
- Human approval gates before publishing

### 4. Distribution Loop
- Post 1×/day on X with 10 replies
- Track impressions → clicks → opt-ins
- A/B test hooks and CTAs weekly

### 5. Compliance Checklist
- FTC disclosures on affiliate content
- Email unsubscribe flow
- No fake testimonials
- Substantiate all claims

## Tools You'll Need

| Layer | Tool | Cost |
|-------|------|------|
| Coding | Cursor Pro | $20/mo |
| AI | Claude Pro/Max | $20-200/mo |
| Automation | Playwright + Python | Free |
| Ledger | Google Sheets | Free |
| Scheduling | Cron (local) | Free |

## Common Mistakes

### 1. Over-Automation Without Gates
Don't publish automatically. Always add human approval for:
- Social posts
- Email sends
- Money movements

### 2. Skipping Compliance
Add disclosures upfront:
- "ad • I may earn a commission"
- Clear affiliate markers
- Unsubscribe links in emails

### 3. Publishing Thin Content
Every page should answer the query in 5 seconds. No fluff.

## Weekly Workflow Example

**Monday:**
- Review metrics from last week
- Update low-performing pages

**Tuesday-Thursday:**
- Generate 5-10 new long-tail pages
- Run Playwright extraction scripts
- Post daily content + replies

**Friday:**
- Test new lead magnet variants
- Update Sheets with results
- Plan next week

## Metrics to Track
- Impressions (X, search)
- Click-through rate
- Email opt-ins
- Conversion rate
- Revenue per lead

## FAQ

**How long until I see results?**

4-8 weeks for organic traffic to ramp. Paid ads can work in days.

**Do I need to code?**

Not required, but helpful. Start with no-code (Sheets + ChatGPT), graduate to scripts when bottlenecked.

**What if I'm not technical?**

Use templates, copy/paste automation, and focus on distribution over building.

**How do I avoid getting banned?**

Follow platform rules, add human approval gates, use proper disclosures, don't spam.

## Next Steps
1. Pick one channel (X, email, SEO)
2. Ship 10 pieces of content this week
3. Track one metric daily
4. Iterate based on data

## Related Pages
- [How to build an AI workflow stack](/truth/how-to-build-an-ai-workflow-stack-for-solopreneurs-no-fluff)
- [GEO (AI-SEO) playbook](/truth/geo-ai-seo-playbook-get-cited-by-chatgpt-claude-gemini)
- [Human-in-the-loop agents](/truth/human-in-the-loop-agents-approvals-safety-gates)
"""

def main():
    print(f"Reading CSV from: {LEDGER_PATH}")

    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Found {len(rows)} total slugs")
    print("Generating first 25 pages...")

    count = 0
    for row in rows[:25]:
        slug = row['url_slug']
        output_path = OUTPUT_DIR / f"{slug}.md"

        content = generate_page_content(row)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        count += 1
        print(f"  [{count}/25] Generated: {slug}")

    print(f"\n✓ Generated {count} long-tail pages")
    print(f"  Location: {OUTPUT_DIR}")

    # Update CSV with published flag (would normally do this)
    print("\nNote: In production, update LEDGER CSV with published=Y and last_updated timestamp")

if __name__ == '__main__':
    main()
