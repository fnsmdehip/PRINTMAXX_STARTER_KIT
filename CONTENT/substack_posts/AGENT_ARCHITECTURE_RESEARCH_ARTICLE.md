# I spent 3 days researching every agent architecture on GitHub. here's what actually works.

**Status:** PENDING_REVIEW
**Platform:** Substack
**Type:** Research article (~2200 words)
**Voice:** copy-style.md compliant

---

I run 62 autonomous agent loops overnight on two MacBooks. have for 3 months. 282 scripts, 57 cron jobs, 0 context rot incidents.

wanted to know if the architecture was good or if I was missing something obvious. so I dug into every serious agent system on GitHub.

here's what I found after analyzing 10 architectures, 50+ MCP integrations, and 4 active research papers on self-improving agents.

## the landscape (February 2026)

there are exactly 5 serious agent architectures worth studying right now.

**OpenHands** (65K stars). event-sourced, stateless, composable. the most architecturally rigorous system for coding tasks. 72% on SWE-Bench. if you're building a software engineering agent, this is the gold standard.

**SWE-agent** (18K stars). Princeton. formal Agent-Computer Interface that constrains what the agent can do. history processors that manage context window. strong benchmarks. again, coding-focused.

**Goose** (27K stars, Block). model-agnostic, MCP-first. works with any LLM. all tools are MCP servers, so extending it means adding a server, not modifying core code. the context revision step (active pruning each iteration) is smart.

**Claude Flow** (14K stars). queen-led hierarchical swarms with Byzantine fault-tolerant consensus. 15+ concurrent agents. impressive claims (84.8% SWE-Bench) but I haven't independently verified them.

**snarktank/ralph** (10.6K stars). the canonical implementation of Geoffrey Huntley's Ralph Wiggum loop. simple bash loop, stateless, filesystem memory. Anthropic liked it enough to ship an official plugin.

## the pattern everyone converges on

every successful system uses the same core pattern:

```
while (tool_call):
    execute tool
    observe result
    decide next action
```

that's it. Claude Code, OpenHands, SWE-agent, Goose, continuous-claude. same loop. the differences are in what happens around the loop: memory, verification, tool constraints, context management.

## finding 1: context rot is real and measurable

Chroma Research tested 18 leading LLMs. adding 113K tokens of conversation history drops accuracy by 30%.

the practical number: keep context utilization below 40%. the middle 40-60% of the context window is a dead zone where reasoning degrades 15-20 percentage points. they call it the "dumb zone."

position-aware placement matters. critical information at the beginning or end of context gets 70-75% accuracy. middle positions: 55-60%.

Claude degrades the slowest of all models tested. Gemini the earliest.

**takeaway:** kill the agent every iteration (Ralph pattern). don't try to maintain long-running context. the research says it makes agents worse, not better.

## finding 2: memory over reasoning

Stanford and Harvard published this in late 2025: agents that store short, structured lessons from past successes and failures outperform agents relying on longer reasoning chains.

remembering what worked matters more than thinking harder.

the state of the art:

**Zep** (temporal knowledge graph). tracks when facts become invalid. bitemporal: "this was true from January 5 to February 12." LLMs compare new information against existing facts and auto-invalidate contradictions. 18.5% higher accuracy than baselines.

**FadeMem** (biologically-inspired forgetting). implements Ebbinghaus forgetting curves. frequently accessed memories strengthen. unused memories fade. 82.1% retention using 55% storage. the insight: your agent should forget irrelevant information, just like humans do.

**Mem0** (production memory layer). separates short-term and long-term memory with episodic, semantic, and procedural types. 26% improvement over OpenAI baseline. 91% lower p95 latency.

the consensus: no single memory approach is sufficient. the best systems combine context window (short-term), filesystem (medium-term), and knowledge graph (long-term).

**takeaway:** a flat progress.txt file works for simple continuity. but for systems running 62+ loops across months, you need structured memory with temporal invalidation. stale intel is worse than no intel.

## finding 3: the Judge Agent pattern

Vercel's ralph-loop-agent implements something subtle: the agent that does the work is NOT the agent that evaluates the work.

the Judge Agent has read-only access. it can approve or reject, but it cannot modify the output. this prevents the agent from "fixing" its own problems by changing the code until tests pass (which often introduces new bugs).

when the Judge rejects, the feedback gets injected as a user message in the next iteration. the worker reads the feedback and tries again with specific guidance.

```typescript
verifyCompletion: async () => {
    const checks = await runAllChecks();
    return {
        complete: checks.every(Boolean),
        reason: checks.every(Boolean) ? 'Done' : 'Checks failed: ...'
    };
}
```

**takeaway:** separating execution from verification is cheap (one extra Haiku call per iteration) and significantly improves output quality. the verifier can't cheat.

## finding 4: self-improvement is real but early

**SICA** (ICLR 2025). an LLM-based coding agent that autonomously edits its own codebase to improve benchmark performance. went from 17% to 53% on SWE-Bench. when it started with only file-overwrite capability, it invented its own smart editing tools. this is legitimately impressive.

**DSPy/MIPROv2** (Stanford). programmatic prompt optimization via Bayesian optimization. you define input/output specifications, DSPy automatically finds better prompts and few-shot examples. it's AutoML but for LLM prompts.

**DARWIN** (Georgia Tech, February 2026). evolutionary prompt optimization. multiple prompt variants compete. winners propagate. uses persistent JSON memory to track which changes led to improvements.

**OpenAI's Self-Evolving Agents Cookbook**. the GEPA (Genetic-Pareto) framework: sample agent trajectories, reflect on them in natural language, propose prompt revisions, evolve through iterative feedback loops.

**takeaway:** you don't need to do anything as aggressive as SICA (agent edits its own code). store successful run patterns as few-shot examples and run monthly prompt optimization. the research says that alone produces meaningful improvement.

## finding 5: only 1-5% of enterprises get agents past pilot

Cleanlab surveyed 1,837 organizations. only 95 had agents live in production. roughly 5%. Cleanlab's CEO says agentic AI "won't really gel until 2027."

the failure modes:
- 5% unpredictable failure rate. 95 tasks work perfectly, the 96th completely fails. dealbreaker for critical processes.
- 70% of regulated enterprises replace their AI stack every 3 months. the infrastructure keeps changing under you.
- long-horizon planning breaks beyond 10-15 steps. 20-30 step tasks with branching logic cause cascade failures.
- integration issues, not LLM failures, kill most agent pilots (Composio report). "dumb RAG," "brittle connectors," and "polling tax" are the three killers.

**takeaway:** the bar for competition is low. most companies can't get past pilot stage. running 62 loops in production for 3 months on consumer hardware puts you ahead of 95% of enterprises. the moat is operational experience, not architecture.

## finding 6: the competitive moat is data + speed

McKinsey 2025: 79% of organizations report competitors making similar AI investments. only 23% believe they're building sustainable advantages.

model access is commoditized. everyone has Claude, GPT-4, Gemini. the edge comes from:

1. **proprietary data** — your operation trajectories, your alpha intel, your scored leads. competitors can't recreate your specific interaction data.

2. **speed of the improvement loop** — how fast you go from insight to deployed improvement. the hedge fund analogy: the firm that can research, backtest, deploy, monitor, and retire strategies fastest wins.

3. **vertical specialization** — industry-specific AI agents show 3-5x higher retention than horizontal solutions. "agent for business ops" is too broad. "agent that runs 62 overnight research-to-content pipelines for solopreneurs" is specific enough to have a moat.

4. **the flywheel** — more usage generates more data, data improves agents, better agents attract more usage. every operation you run is training data that competitors don't have.

## finding 7: guardrails are mature enough

the tooling exists:

- **Anthropic's framework**: deny-all permissions, explicit allowlisting, human-in-the-loop for high-stakes decisions.
- **NeMo Guardrails** (NVIDIA): 50% better protection, ~0.5s latency. content safety, topic control, jailbreak detection.
- **Guardrails AI**: Apache 2.0, composable validators, real-time output validation.

the pattern: 4-layer defense (input/reasoning/action/output). risk-based autonomy (low-risk tasks run autonomously, high-risk tasks require approval). human escalation as a tool call, not a system shutdown.

## what I'm building next

upgrading the memento system based on this research:

1. **temporal knowledge graph** (Zep) replacing flat progress files. structured memory with automatic fact invalidation.
2. **Judge Agent** for verification. separate read-only verifier for every loop.
3. **trajectory storage** for self-improvement. successful runs become few-shot examples.
4. **MCP-first tool integration**. Tavily for search, Resend for email, Telegram for notifications.
5. **4-layer guardrails** with risk-based autonomy levels.
6. **monthly prompt mutation** via DSPy for continuous improvement.

total infrastructure cost increase: ~$50/mo. everything is self-hosted, MIT licensed, runs on the existing 2 MacBooks.

the repo stays MIT licensed at github.com/fnsmdehip/memento. the core loop pattern is Huntley's. the ops tooling is mine. the self-improvement layer is new.

## sources

the full research corpus: OpenHands, SWE-agent, Claude Code Agent SDK, Goose (Block), Claude Flow, continuous-claude, Vercel ralph-loop-agent, 12-Factor Agents, DSPy/MIPROv2 (Stanford), SICA (ICLR 2025), DARWIN (Georgia Tech), Man Group AlphaGPT, ARIA (EMNLP 2025), Mem0, Zep/Graphiti, FadeMem, NeMo Guardrails, Guardrails AI, Composio, Chroma context rot research, Cleanlab 2025 production survey, Google/Amazon deployment reports, Stanford/Harvard agentic AI study.
