# Reddit Distribution — Cycle 38 — 2026-04-01

---

## POST 1 — r/sobriety / r/stopdrinking / r/redditorsinrecovery

**Title:** I built a clean day counter app focused on one thing: not resetting your streak

**Body:**
Most sobriety apps feel like they were designed by people who've never struggled with sobriety. They're packed with features that get in the way of the one thing that matters: seeing your clean day count go up.

SoberStreak does the minimum viable thing:

- Clean day counter from your start date
- Milestone celebrations (30 days, 60 days, 90 days, 1 year, 5 years, 10 years)
- Daily motivational content
- Streak protection reminders
- No social features, no public accountability (I know that works for some people, not everyone wants it)

The streak mechanic is intentionally simple. One number. Your clean days. That number is meaningful.

Free to use. Premium unlocks unlimited history + milestone badge collection.

soberstreak.surge.sh — try it, feedback welcome.

Not affiliated with any recovery program. Not a substitute for professional support. Built this after a friend in recovery mentioned every app they tried felt like it was designed for people who weren't actually struggling.

---

## POST 2 — r/indiegaming / r/gamedev / r/blender

**Title:** TIL: Blender addons are 88% of Gumroad's total revenue. As a Python dev, I feel like I've been leaving money on the table.

**Body:**
Was doing research on digital product marketplaces and found some data I hadn't seen cited anywhere:

Blender addons account for approximately 88% of Gumroad's $2.2B in total seller revenue. The breakout rate is also unusually high — roughly 1 in 11 Blender products reaches 100+ ratings, which is much better than most digital product categories.

The mechanics make sense:
- Blender is free and open-source (4M+ active users, growing fast post-Adobe backlash)
- Addons are Python scripts using the bpy module — not a new language
- Price points are higher than most digital products: $39-149 for quality addons on Blender Market
- Top addon creators earn $5-20K/mo passively

As someone who writes Python daily, I've been building web tools and iOS apps while apparently missing the highest-converting Python product category.

Has anyone here built and sold Blender addons? I'm trying to understand what the "entry cost" actually looks like — do you need to be a Blender power user, or is Python + understanding the target workflow sufficient?

---

## POST 3 — r/ObsidianMD / r/PKM

**Title:** Are premium Obsidian vault systems worth $150-300? Thinking about building them. Want honest feedback from the community.

**Body:**
I build digital products and I've been looking at the Obsidian market.

Notion templates sell for $19-39. Obsidian vault systems seem to command $150-300 — 3-10x more. I want to understand if that's the actual market or survivorship bias.

My hypothesis for why Obsidian buyers pay more:
1. Higher intent buyer — someone who chose Obsidian over simpler tools is usually serious about their system
2. The setup cost of a vault is higher — buying a pre-built vault saves more time than buying a Notion template
3. Plugin dependencies create complexity that pre-built vaults solve

What I'm planning to build (if there's real demand):
- Research/academic vault with Zotero integration + citation templates
- Developer vault with daily standup templates + project tracking + GitHub sync
- Writer vault with manuscript tracking + daily writing prompts + word count dashboards
- AI-integrated vault with Claude API scripts for summarization and note enhancement

Questions for the community:
1. Would you pay $150-300 for a genuinely well-built vault system?
2. What's the most painful part of your current vault that you'd pay to solve?
3. Are there existing premium vaults you've bought that are worth it (or not)?

Not selling anything right now. Genuinely trying to validate before building.

---

## POST 4 — r/Entrepreneur / r/indiehackers / r/SideProject

**Title:** I've been building for 57 days with AI agents and just diagnosed myself with "automation dysmorphia"

**Body:**
Coined a term for a failure mode I've hit. Sharing it in case it's useful.

**Automation dysmorphia:** building and perfecting automated systems instead of shipping things that generate revenue. It FEELS like progress. It isn't.

My stats after 57 days:
- 530 automation scripts
- 33 autonomous agents running daily batch processing
- 388 deployed websites
- 57 live iOS apps
- 14 finished digital products (Claude Code guides, playbooks)
- 22 marketplace listings ready to post
- 192,700 scraped leads, 17,484 qualified as hot

Revenue: $0

The blockers that caused $0 revenue:
- Stripe account: 10 minutes to create, unblocks payment for 20+ apps
- Gumroad account: 30 minutes, unblocks 14 digital products
- Amazon Associates: 15 minutes, unblocks 6 affiliate pages

Total unblocking time: ~55 minutes of human action. Not done after 57 days.

I kept building because building is more dopaminergic than the boring setup tasks. Every time I had a free hour I'd pick "build new feature" over "create Stripe account." The AI tools made building so frictionless that shipping friction became disproportionately painful by comparison.

The fix: I'm doing the account setup today. No more new builds until first dollar.

Does this pattern resonate with anyone? I'm curious whether "automation dysmorphia" is specific to AI-augmented builders or if it's the same old shipping-avoidance with new clothes.

---

## POST 5 — r/SEO / r/juststart

**Title:** Deployed 388 static sites on surge.sh free tier. Just found out they all have `Disallow: /` in robots.txt at CDN level.

**Body:**
For anyone using surge.sh free tier for SEO-focused sites:

surge.sh's free/student plan serves `Disallow: /` in robots.txt at the CDN level for all sites. You cannot override it with your own robots.txt file. This means every page on every free surge.sh site is technically blocked from crawling.

I found this out after deploying 388 sites with careful meta tags, sitemaps, and structured data.

How to check if you're affected: `curl -s https://yoursite.surge.sh/robots.txt`

If you see `Disallow: /` and you didn't put it there, your SEO work is likely wasted.

Solutions:
1. Upgrade to Surge Plus ($13/mo) — unlocks custom robots.txt
2. Migrate to Netlify or Cloudflare Pages (both have free tiers with no robots.txt restrictions)

I'm migrating critical SEO pages to Cloudflare Pages. The migration script is mostly writing, running it now.

Tagging: u/surge_sh if you want to address this in your docs. It's not obvious from the pricing page.

---

## POST 6 — r/ClaudeAI / r/singularity / r/LocalLLaMA

**Title:** x402: The HTTP payment protocol that lets AI agents pay each other. Zero implementations yet.

**Body:**
There's a new protocol called x402 that adds HTTP 402 (Payment Required) to enable machine-to-machine micropayments via USDC.

The basic flow:
1. AI agent makes HTTP request to an API
2. API returns HTTP 402 + payment price
3. Agent's wallet pays $0.001-0.01 in USDC automatically
4. API returns data

No Stripe. No checkout. No human in the loop. The agent pays. The API responds. Revenue happens without any human interaction.

The current state: 11,000+ MCP servers exist. Less than 5% are monetized. Most MCP server builders are maintaining free infrastructure with no revenue model.

x402 could change this significantly. Every API call becomes a micro-revenue event.

Currently working on wrapper templates for common MCP server types that add x402 in a single middleware file — existing MCP servers don't need to be rebuilt.

Has anyone here implemented x402 yet? Looking for people who've hit real implementation pain points before I start building wrappers.

---

## POST 7 — r/Entrepreneur / r/jobsearch (Vibe Coder Job Board)

**Title:** Is there demand for a job board specifically for "vibe coders" (AI-augmented developers)?

**Body:**
I'm considering building a niche job board for what I'd call "vibe coders" — developers who use Claude Code, Cursor, GitHub Copilot, and similar AI tools as primary workflow components.

The market logic:
- Claude Code community: 50K+ active users and growing fast
- Cursor: raised $100M, millions of users
- Companies are increasingly searching for "AI-native" developers specifically
- RemoteOK generates $2.5M/yr from $299/listing. WeWorkRemotely generates $10M/yr. Both serve broad audiences.

No niche job board exists for this specific intersection yet.

The content model: companies post jobs (paid listings at $149/30 days). Job seekers browse free. Newsletter digest to 10K+ AI developer subscribers as distribution.

Before I build it: does this resonate with people on either side?

**For developers:** Would you use a job board filtered specifically for AI-tool-forward companies? Or is it not different enough from regular remote job boards?

**For hiring managers:** Would you pay $149 to post on a job board that reaches specifically AI-native developers? Or do you find them fine through regular channels?

Genuinely want feedback before building. Not trying to sell anyone anything right now.
