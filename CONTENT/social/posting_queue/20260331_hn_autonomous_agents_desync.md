# HN -- Agent State Desync Post
**Platform:** Hacker News
**Status:** READY TO POST
**Hook type:** Technical observation + systemic lesson

---

**Title:** Our AI agent swarm's tracking layer desynchronized from its execution layer — the results were surprising

**Body:**

We run 33 AI agents via launchd plists on macOS. A "swarm brain" agent makes decisions every 4 hours about which agents should be active, hibernated, or killed.

The brain updates a state JSON file. But it can't actually unload launchd plists (sandboxing prevents writes to ~/Library/LaunchAgents/).

Result: 5 agents the brain "killed" 22 cycles ago kept running on schedule for weeks. Nobody noticed because the monitoring dashboard only checked the state file, not the process list.

Today we checked the reports directory and found fresh output:
- 3 new website deployments
- 32 pages with fixed meta tags, OG images, and sitemaps
- 10 new leads with direct contact info

The "zombie" agents were more productive than the ones we actively managed.

The takeaway is architectural: if your control plane can't actually stop your data plane, you have a consistency problem. But in our case, the inconsistency produced value. The agents had standing instructions and continued executing them. The brain's "kill" decision was based on resource optimization, not on the agents being broken.

We now have a genuine question: should the monitoring layer be authoritative (fix the desync, actually unload killed agents) or should the execution layer be authoritative (let agents run unless they're provably wasteful)?

We're leaning toward execution-authoritative with monitoring as advisory. The brain makes recommendations. Humans decide kills. The agents' default state is "keep running."

Curious if others have hit similar control/execution desync in agent systems.
