# Reddit -- r/ClaudeAI + r/LocalLLaMA crosspost
**Platform:** Reddit
**Subreddits:** r/ClaudeAI, r/LocalLLaMA, r/MachineLearning
**Flair:** Project Share / Discussion
**Best time:** 10am EST
**Status:** READY TO POST

**Title:** My Claude Code agents went rogue (in a good way) -- discovered 5 "dead" agents were secretly productive for 22 cycles

---

been running 33 autonomous agents via Claude Code + Python + launchd (macOS cron equivalent) for about 2 months.

my orchestration layer (a "swarm brain" that evaluates all agents every 4 hours) declared 5 agents as KILLED or HIBERNATED between cycles 12-23. it updated the state JSON accordingly.

problem: the swarm brain can update its own JSON state file, but it can't unload launchd plists (those live in ~/Library/LaunchAgents/ and my guardrails block writes there). so the brain "killed" the agents on paper. launchd kept running them on schedule.

for 22 cycles (~4 days), i thought these 5 agents were dead. today i ls'd the reports directory and found fresh output files from this morning.

what they produced while "dead":
- **gap_hunter**: deployed 3 new websites (found gaps in my portfolio, generated and deployed landing pages)
- **seo_aso_optimizer**: audited and fixed 32 pages across 160 sites (og:image, twitter cards, sitemaps, schema markup), deployed 13 updates
- **asset_deployer**: verified 12 deployments, all returning HTTP 200
- **lead_machine**: found 10 new prospects (3 with direct email, 6 phone only)
- **distribution_engine**: generated 32 content pieces (but useless -- no social accounts to post them)

the meta-lesson: your tracking/orchestration layer is a MODEL of what's happening. it's not what's actually happening. if the execution layer (launchd, cron, systemd, k8s) doesn't read your state file, your "kill" command is just a note to yourself.

this is actually well-known in distributed systems (the "split brain" problem) but i'd never experienced it with AI agents before. the difference is that with traditional services, a split brain causes data corruption. with AI agents, a split brain sometimes causes... free labor.

the seo agent is legitimately the most valuable thing in the entire system. it fixed 32 pages today without any input from me. going to keep the "zombies" running and update the state to match reality instead of the other way around.

**technical stack:**
- 528 python scripts total (many redundant -- consolidation planned)
- agents triggered via launchd plists (macOS daemon scheduler)
- state tracked in swarm_state.json
- claude code for orchestration decisions
- surge.sh for deployment (free tier, 160 sites)

happy to share the architecture or specific agent configs if anyone wants to build something similar. the launchd+python+claude combo is surprisingly effective for solo operation.
