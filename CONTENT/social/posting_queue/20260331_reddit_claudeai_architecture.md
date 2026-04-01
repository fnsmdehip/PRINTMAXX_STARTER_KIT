# Reddit -- r/ClaudeAI Agent Architecture
**Platform:** Reddit
**Subreddits:** r/ClaudeAI, r/artificial, r/MachineLearning
**Flair:** Discussion / Project
**Best time:** 11am EST
**Status:** READY TO POST

**Title:** I run 33 autonomous AI agents from cron jobs on a MacBook. Here's the actual architecture.

---

been running a system of 33 autonomous agents for ~2 months. not a framework. not a demo. actual production agents that run 24/7 via crontab.

architecture:

**layer 0 -- infrastructure**
- cron watchdog (checks every hour that all 10 required crons are alive, auto-restores if wiped)
- perpetual guardian (safety commits 3x/day, auto-fixes broken state)
- system health monitor (disk, processes, api health)

**layer 1 -- intelligence**
- competitive intel scraper (finds 15-20 new blue ocean niches/day, zero llm cost, just public api analysis)
- twitter/reddit/hn scrapers (49K entries collected)
- alpha auto-processor (routes scraped intel to the right venture pipeline)

**layer 2 -- decision**
- ceo agent (orchestrates 16-phase daily cycle)
- swarm brain (meta-agent that evaluates all other agents, hibernates underperformers, 603 decisions across 45 cycles)
- capital genesis ranker (scores revenue methods on 7 dimensions)

**layer 3 -- execution**
- seo optimizer (audits 50+ pages/cycle, fixes og tags, twitter cards, schema, redeploys)
- venture agents (8 types: outbound, content, app, local biz, research, monetize, product, scraping)
- playwright tester (auto-tests 156 deployed sites, 82% passing)

**layer 4 -- quality**
- loop closer (3 feedback loops: decision execution, feedback tracking, pipeline advancement)
- quality gate (blocks slop before deployment)

total token burn: ~8K tokens/day. mostly the swarm brain evaluating agent performance.

the swarm brain is the interesting one. it runs every user session, evaluates all 33 agents, hibernates ones with no wake conditions met, and maintains a running plateau counter. we're at 22 consecutive zero-delta cycles right now because the system is waiting for human account creation to unblock revenue.

happy to go deeper on any layer. the whole thing runs on python + claude code api + cron. no langchain, no langgraph, no vector databases, no kubernetes.
