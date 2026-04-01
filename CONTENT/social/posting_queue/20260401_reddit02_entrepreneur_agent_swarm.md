# Reddit Post -- r/Entrepreneur: AI Agent Swarm on $200/mo
**Platform:** Reddit
**Subreddit:** r/Entrepreneur (also good for r/artificial, r/MachineLearning)
**Status:** READY TO POST

---

**Title:** I run 23 AI agents 24/7 for $200/mo with zero frameworks. Here's the architecture.

**Body:**

I see a lot of posts about AI agent frameworks (LangGraph, CrewAI, AutoGen) and expensive agent platforms. I wanted to share an alternative approach that costs almost nothing and has been running autonomously for 57 days.

**The setup:**
- 23 Python scripts, each 100-400 lines
- macOS launchd (basically cron) runs them on schedules (every 2-6 hours)
- JSON files for state, markdown files for reports
- One Claude Max subscription ($200/mo) for LLM calls
- No frameworks, no vector databases, no orchestration platforms

**What they do:**

| Agent | Schedule | Output |
|-------|----------|--------|
| SEO optimizer | 2h | Fixed 62 pages last cycle |
| Revenue tracker | 4h | Full channel audit with revenue leak detection |
| Lead machine | 4h | 10 scored leads per cycle, email drafts written |
| Gap hunter | 3h | Finds broken pages, missing assets, deployment issues |
| Site health monitor | 2h | 388 sites tracked, 94.2% uptime |
| Competitor intel | 6h | 615 blue ocean niches tracked |
| Cross-pollinator | 4h | Routes outputs between ventures (1,177 connections) |
| Asset deployer | 2h | Auto-deploys to surge.sh |
| Guardian | 8h | Safety commits to git 3x/day |
| + 14 more | Various | Content, testing, scoring, alerting |

**The "swarm brain":**

Every 4 hours, a master agent reviews all other agents' reports and makes decisions:
- MAINTAIN agents producing useful work
- KILL agents wasting tokens
- ESCALATE blockers that need human action
- CREATE compound actions (chain agents together)

Last cycle it identified that two agents (gap_hunter + asset_deployer) could work together to embed payment links into pages -- something neither could do alone.

**The zombie discovery:**

5 agents I tried to kill kept running because the brain updates a JSON state file, but macOS launchd doesn't read that file. These "zombie" agents deployed more sites and fixed more bugs than my actively managed ones.

Takeaway: the best agent management strategy might be no management at all. Clear prompt + scheduled execution + filesystem state = agents that don't need supervision.

**What I'd do differently:**
- Start with 3 agents, not 23. Most of mine are redundant.
- Wire payment/distribution FIRST, automation SECOND. I have 202 sites earning nothing.
- Test each agent with a single run before scheduling. I have dead scripts I never tested.

**Cost breakdown:**
- Claude Max: $200/mo
- Surge.sh hosting: $0 (free tier)
- Everything else: $0

Total: $200/mo for 23 agents running 24/7.

Ask me anything about the architecture.

---

**Engagement strategy:** r/Entrepreneur audience wants practical, cost-conscious solutions. Lead with the cost ($200/mo vs expensive platforms). The agent table is the hook. The "what I'd do differently" section shows maturity and prevents "why did you over-build" criticism. Answer every comment for first 3 hours.
