# your agents are supposed to die. that's the feature.

**Status:** PENDING_REVIEW
**Platform:** Substack
**Type:** Launch article (~1800 words)
**Voice:** copy-style.md compliant

---

I built 282 automation scripts. 62 autonomous agent loops. 57 cron jobs. a factory that generates agent loops for 182+ operations from a spreadsheet.

the single biggest problem I hit wasn't prompt engineering. wasn't model quality. wasn't rate limits.

it was context rot.

## the problem nobody talks about

run a Claude or GPT agent for 30 minutes. it's sharp. it follows instructions. it makes good decisions.

run it for 2 hours. it starts drifting. forgets constraints. hallucinates details from earlier in the conversation. makes worse decisions the longer it runs.

by hour 4, you're babysitting an increasingly confused agent that's burning tokens on garbage output.

I watched this happen across 282 scripts. the pattern was consistent: agent performance degrades as context accumulates. every tool call result, every file read, every previous decision... it all piles up in the context window like sediment. eventually the agent is drowning in its own history.

most people solve this with "context management." summarization. pruning old messages. compacting. RAG retrieval.

all of these are bandaids. they reduce the problem. they don't eliminate it.

## the counterintuitive fix

I eliminated it.

the fix: kill the agent. every single iteration. on purpose.

each loop iteration:
1. starts with completely fresh context (zero accumulated garbage)
2. reads ALL state from the filesystem (prompt.md, prd.json, progress.txt)
3. picks exactly ONE task where `passes: false`
4. executes that one task
5. writes results back to disk (updates prd.json, appends to progress.txt)
6. exits clean

then the bash while loop restarts a brand new agent instance. fresh context. reads the updated filesystem state. picks the next task. repeat.

memory lives in the filesystem. not the context window. the agent is disposable. the work is permanent.

I call it deadloop.

## how it actually works

the core loop is dead simple:

```bash
while :; do
  cat PROMPT.md | claude --dangerously-skip-permissions --print
done
```

each iteration gets three files:

**prompt.md** (static, never changes during execution): tells the agent who it is, what tools it has, and the rules it follows. this file is identical every single iteration. no drift.

**prd.json** (task list): array of tasks with `passes: true/false`. the agent scans for the first task where `passes: false`, executes it, marks it `passes: true` if it meets quality gates.

**progress.txt** (append-only learnings): after each task, the agent appends what it learned. next iteration reads this file and benefits from all prior iterations' discoveries without the context rot of keeping those iterations alive.

when all tasks in prd.json have `passes: true`, the agent outputs `<promise>COMPLETE</promise>` and the loop exits.

that's it. no framework. no dependencies. no SDK. bash + files.

## why this beats every other agent framework

**vs context-managed agents (LangChain, CrewAI, AutoGen):** these frameworks try to manage context within a single long-running session. summarization, memory modules, retrieval. it helps. but every iteration still inherits some accumulated context. deadloop inherits zero accumulated context. fresh start every time. the filesystem IS the memory.

**vs OpenClaw:** OpenClaw is a multi-channel messaging gateway. 210k GitHub stars. creator got hired by OpenAI. it routes messages from WhatsApp, Telegram, Slack, Discord (13+ platforms) to an AI agent. it's the frontend. deadloop is the backend. OpenClaw talks to your users. deadloop grinds through your ops. use both.

**vs simple cron + scripts:** closer to what deadloop actually is. but deadloop adds: a factory system that generates canonical loop structures for any operation, wave-based swarm orchestration for parallel execution, 3-layer filesystem memory for crash recovery, and budget-first model routing so you don't blow $500 on overnight runs.

## the factory: loops for anything in one command

I had 182+ operations I wanted to automate. writing a custom loop for each one would take months.

so I built a factory. feed it a spreadsheet of operations (name, description, success criteria, tools needed). one command:

```bash
deadloop factory --from ops.xlsx --generate-all
```

outputs 182 canonical loop directories. each one has: prompt.md (tailored to that operation), prd.json (tasks broken into atomic testable stories), progress.txt (empty, ready for learnings), run.sh (configured launcher).

ready to run immediately. each loop follows the exact same stateless resampling pattern. each loop is independently crash-recoverable.

## swarm orchestration: parallel agents that don't fight

solo loops are powerful. coordinated loops are 10x.

deadloop's swarm system uses wave-based orchestration:

**wave 1:** 5 research agents run in parallel. each has a defined scope, file ownership map (what it can write to), and output format.

**wave 2:** 3 processing agents. they read wave 1's outputs (read-only). compile, deduplicate, score, route.

**wave 3:** 3 output agents. they read wave 2's compiled results. generate final deliverables.

the key: interface contracts between waves. wave 1 agents know exactly what format wave 2 expects. file ownership is explicit. agent A owns `research/markets.md`. agent B owns `research/competitors.md`. neither touches the other's files.

no conflicts. no stomping. no "merge hell." just clean parallel execution.

## 3-layer filesystem memory

every piece of state lives in one of three layers:

**layer 1: HEARTBEAT.md** (<20 lines of pure numbers). any new agent reads this in 3 seconds and knows the full system state. revenue, leads, alpha count, active loops, cron health. updated every cycle.

**layer 2: active-tasks.md** (crash recovery). if an agent dies mid-task, the next iteration reads this file and picks up from the exact step where the previous agent died. no lost work. no duplicated effort.

**layer 3: daily logs** (append-only). every tool call, every pipeline step, every decision. never deleted. only appended. full audit trail.

no vector database. no embeddings. no retrieval pipeline. just markdown files on disk. readable by any agent, any framework, any human with a text editor.

## budget-first model routing

overnight agent loops can burn serious money if you're not careful.

deadloop's stack governor routes every API call through budget constraints first:

- opus for external/untrusted content (web scraping, third-party APIs). the extra reasoning protects against prompt injection.
- sonnet/haiku for internal operations (file management, CSV processing, code gen). faster, cheaper, safe because the data is trusted.
- hard daily spend caps with automatic enforcement. not "alerts when you're close." enforcement. the system stops spending when it hits the limit.

62 loops running overnight. average cost: predictable and capped. not "I woke up to a $300 bill."

## the numbers

battle-tested across my actual production system:

- 282 automation scripts
- 62 autonomous loop directories
- 182+ operations with factory-generated loops
- 57 active cron jobs
- 3-layer memory architecture
- 11-agent swarm orchestration across 3 waves
- overnight runs processing 700+ alpha entries per session
- 0 context rot incidents since switching to stateless resampling

this is not a proof of concept. it's what runs my entire automation stack.

## the 10 canonical rules

inherited from Geoffrey Huntley's Ralph pattern and battle-hardened across 3 months of production use:

1. static prompts (never modified during execution)
2. filesystem memory (not context window)
3. append-only logs (never delete, only append)
4. one task per iteration (no multi-task drift)
5. quality gates before marking complete
6. agent picks its own next task (autonomous prioritization)
7. small stories (atomic, testable, independent)
8. git commits per iteration (full audit trail)
9. max iterations with backpressure (no runaway loops)
10. graceful stop conditions (clean exit, not crash)

break any of these and you'll reinvent the context rot problem you were trying to solve.

## open source

the full framework is MIT licensed. take it. fork it. build on it.

what's included:
- 62 loop templates across research, content, ecommerce, growth, outbound, and specialized operations
- factory system for generating loops from any operation spreadsheet
- wave-based swarm orchestration with interface contracts
- 3-layer filesystem memory (heartbeat, active-tasks, daily logs)
- budget-first model routing with hard spend caps
- crash recovery via active-tasks.md pattern
- progress monitor TUI for real-time loop status

repo: github.com/fnsmdehip/deadloop

if your agents get dumber the longer they run, your architecture is wrong.

context is a liability. filesystem is memory. agents are disposable. work is permanent.

that's deadloop.
