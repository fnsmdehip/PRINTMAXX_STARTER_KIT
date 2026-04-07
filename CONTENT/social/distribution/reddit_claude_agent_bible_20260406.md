# Reddit Posts: Claude Code Agent Bible
# Asset: The Autonomous Agent Playbook ($47)
# Date: 20260406

---

## POST 1
**Subreddit:** r/ClaudeAI
**Title:** I run 33 autonomous Claude Code agents on my MacBook. Here's the full architecture (no cloud needed)

**Body:**

Been building with Claude Code for about 6 months. The system I landed on runs 33 agents locally with zero cloud infrastructure costs. Sharing the full pattern because most "agent" tutorials skip the parts that actually make agents work in production.

**The 3-layer stack:**

Layer 1 is pure automation. Scrapers, file monitors, data backups. No AI. Just cron jobs doing mechanical work. Important: don't use an LLM where a regex works.

Layer 2 is AI-assisted. Claude gets called when judgment is needed. Input arrives, Claude processes, output gets written to a file, another script reads it later. These are triggered by events, not always running.

Layer 3 is fully autonomous. The agent reads its state file, checks the message bus, decides what to do, does it, writes output, exits. No human involved.

**The part most tutorials skip: filesystem as memory.**

Agents fail when they don't persist state. They forget what they've done, repeat work, or loop without progress. Every agent I run:
- Reads state from a JSON file at the start
- Writes updated state at the end
- Never assumes the previous run's context is in memory

No database. No vector store. The file IS the memory.

**Inter-agent communication:**

Message bus is a JSONL file. Agent A appends a message with a "for" field. Agent B polls via cron, reads messages addressed to it, processes, deletes. No shared state. No race conditions. Works at 33 agents.

**Model routing:**

- Opus: quality gates, strategic decisions, creative work where wrong = costly
- Sonnet: code generation, research synthesis, anything that needs speed + quality
- Haiku: classification, routing, routing decisions, bulk tasks

Wrong routing costs 60x per call. Routing correctly is probably 30% of what makes the system economical.

**The Ralph loop (overnight execution):**

```bash
while :; do
  cat PROMPT.md | claude --dangerously-skip-permissions --print
done
```

PROMPT.md tells the agent what to do this loop. Agent does it, exits. Loop restarts. You update PROMPT.md to steer. Memory lives in files, not context. Ships real output by morning.

Happy to answer questions on any part of this. Building in public, mistakes and all.

---

## POST 2
**Subreddit:** r/SideProject
**Title:** 388 deployed sites, $0 revenue, 33 agents, one person. Here's what I actually learned.

**Body:**

I've been running an autonomous business system for 44 days. 33 agents. 388 live websites. $0 actual revenue.

I'm sharing this because most "build in public" posts skip the awkward part where everything works technically but nothing works commercially.

**What's actually running:**
- 33 autonomous agents via launchd on one MacBook
- 388 live surge.sh deployments (comparison pages, tools, landing pages, PWAs)
- Daily automated scraping, content generation, and distribution
- A pipeline that costs about $240/month in subscriptions

**What the system does well:**
Mechanical work. The agents are genuinely good at scraping, processing, writing content, and deploying assets. That part works.

**What I got wrong:**
I optimized for volume before validating a single conversion. 388 sites with placeholder affiliate IDs. No payment links. The distribution engine runs every day but has nothing ready to actually sell.

**What I'm fixing:**
Gumroad listings first. 13 digital products ready to upload. Before building more infrastructure, get one product live and see if anyone buys it.

**If you're building something similar:**
Wire payment before shipping. Doesn't matter how good the automation is if there's nowhere for money to go.

Anyone else running autonomous local agent stacks? Curious what the actual conversion bottleneck looks like for others.

---

## POST 3
**Subreddit:** r/MachineLearning
**Title:** Local AI agents without cloud infrastructure: patterns that actually work in production

**Body:**

Running 33 Claude Code agents on a single MacBook Pro via launchd + cron. No cloud orchestration platform. No vector database. No external queue.

After 6 months of iteration, here are the patterns that differentiate reliable production agents from toy demos:

**1. Idempotency via lock files**
Every agent checks for a `.lock` file before running. If the lock exists, the previous run is still active (or crashed). Agent exits. Prevents double-runs.

```python
LOCK_FILE = Path("AUTOMATIONS/agent_name.lock")
if LOCK_FILE.exists():
    sys.exit(0)
LOCK_FILE.touch()
try:
    run_agent()
finally:
    LOCK_FILE.unlink(missing_ok=True)
```

**2. Timeouts on everything**
Each agent has a hard timeout (30 minutes for tasks, 3 hours for orchestration). A cron watchdog checks hourly that the expected cron entries still exist and re-installs from backup if wiped.

**3. Model routing by task type**
Opus for decisions where wrong = costly. Sonnet for execution. Haiku for classification. Wrong routing is 60x cost difference for the same output.

**4. Heuristic fallbacks when LLM calls fail**
Every `claude -p` call has a fallback. If the API call fails, the agent falls back to a deterministic heuristic rather than failing the whole pipeline. Important when running 50+ LLM calls per day.

**5. API key auth in cron context**
OAuth tokens expire silently and kill pipelines for days. All cron/background scripts use `--api-key` flag explicitly rather than relying on session tokens.

The full system is documented if anyone wants to go deeper.

---

## POST 4
**Subreddit:** r/entrepreneur
**Title:** The free tools vs paid tools math for cold email (actual numbers)

**Body:**

I built a cold email system that costs $0/month and documented the full setup. Before publishing, I ran the comparison against what paid tools charge.

**What paid infrastructure costs:**
- Instantly Pro: $97/month
- Apollo basic: $49/month
- Lemlist Starter: $59/month
- Smartlead: $39/month

If you use the most popular combo (Apollo for leads + Instantly for sending): $146/month before you've made a single dollar.

**What free tools can replace:**
- Lead sourcing: LinkedIn Sales Nav free tier + Apollo free (50 leads/month) + manual verification
- Email validation: NeverBounce free tier (1000/month) + local validation script
- Sending infra: Google Workspace ($6/month per mailbox) + Brevo free tier
- DNS auth: built into your domain registrar
- Personalization: Claude or GPT-4o-mini at ~$0.002 per email

**What free tools can't fully replace:**
- High-volume sending (1K+ emails/day needs Instantly/Smartlead)
- Real-time lead enrichment at scale
- A/B testing with statistical significance built in

If you're sending under 200 emails/day to highly targeted lists, free tools can work. Above that, the paid tools start paying for themselves.

I wrote the full setup guide. Happy to link if useful or answer questions here.

