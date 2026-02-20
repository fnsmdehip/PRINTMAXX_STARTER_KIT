# agent architecture research thread

**Status:** PENDING_REVIEW
**Platform:** X/Twitter (@PRINTMAXXER)
**Type:** Research thread (10 tweets)
**Voice:** copy-style.md compliant

---

## tweet 1 (hook)

I analyzed every serious agent architecture on GitHub. 10 systems, 65K+ combined stars, 50+ MCP servers, 4 research papers on self-improving agents.

most of what people are building is wrong. here's what actually works.

---

## tweet 2 (context rot)

Chroma Research tested 18 LLMs. adding 113K tokens of history drops accuracy 30%.

the middle 40-60% of your context window is a dead zone. 15-20 point accuracy drop.

kill the agent every iteration. fresh context. read state from files. the research says long-running agents get dumber, not smarter.

---

## tweet 3 (memory)

Stanford/Harvard finding that changed how I think about agents:

"agents that store short structured lessons outperform agents with longer reasoning chains."

remembering what worked > thinking harder.

flat progress.txt files work for simple loops. at 62+ loops you need a temporal knowledge graph that auto-invalidates stale facts.

---

## tweet 4 (judge pattern)

Vercel figured something out with their Ralph implementation: separate the worker from the verifier.

Judge Agent has read-only access. can approve or reject but cannot modify the output. prevents the agent from "fixing" problems by introducing new ones.

costs one extra Haiku call per iteration. ~$0.12/night for 62 loops.

---

## tweet 5 (self-improvement)

SICA (ICLR 2025): an agent that edits its own code went from 17% to 53% on SWE-Bench.

you don't need to go that far. store successful run patterns as few-shot examples. run monthly prompt optimization via DSPy.

the agent gets better every month without you touching it.

---

## tweet 6 (the gap)

Cleanlab surveyed 1,837 orgs. only 95 have agents live in production. roughly 5%.

the 5% unpredictable failure rate is the dealbreaker. 95 tasks work perfectly. the 96th completely fails. for critical business processes that's unacceptable.

running 62 loops for 3 months with 0 failures puts you ahead of 95% of enterprises.

---

## tweet 7 (moat)

McKinsey 2025: 79% of orgs report competitors making similar AI investments. model access is not a moat.

the moat is:
- proprietary operational data (your trajectories, your alpha intel)
- speed of improvement loop (insight to deployed improvement)
- vertical specialization (3-5x better retention than horizontal)

---

## tweet 8 (MCP)

the MCP ecosystem hit 3,000+ servers. Tavily for search ($0.01/query). Resend for email (100 free/day). Figma for design-to-code. Flux for image gen ($0.003/image).

Goose (27K stars, Block) proved it: MCP-first architecture means adding a capability = adding a server. no core code changes.

---

## tweet 9 (guardrails)

the guardrails tooling is finally mature.

NeMo Guardrails (NVIDIA): 50% better protection, 0.5s latency.
Guardrails AI: Apache 2.0, composable validators.
Anthropic's framework: deny-all permissions, risk-based autonomy.

4-layer defense: input / reasoning / action / output. treat tool access like production IAM.

---

## tweet 10 (close)

upgrading memento based on this research:

- temporal knowledge graph (Zep, MIT licensed)
- Judge Agent for verification
- trajectory storage for self-improvement
- MCP-first tools
- 4-layer guardrails
- monthly prompt mutation

$50/mo cost increase. runs on 2 MacBooks. MIT licensed.

full research writeup on Substack. github.com/fnsmdehip/memento

---
