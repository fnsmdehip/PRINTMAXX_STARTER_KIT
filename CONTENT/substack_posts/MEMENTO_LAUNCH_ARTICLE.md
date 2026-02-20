# I run 62 agent loops overnight on two laptops. here's the setup.

**Status:** PENDING_REVIEW
**Platform:** Substack
**Type:** Launch article (~1800 words)
**Voice:** copy-style.md compliant

---

I run 282 automation scripts. 62 autonomous agent loops. 57 cron jobs. research, content, outreach, competitive intel, product development. all running on two consumer laptops while I sleep.

this is not a framework announcement. it's a writeup of the system I actually use, the pattern it's based on, and what I added on top. open sourcing it because the operational tooling might save other people time.

## the pattern: stateless resampling

credit where it's due. the core pattern is Geoffrey Huntley's Ralph Wiggum loop. if you haven't read ghuntley.com/ralph, read that first. he figured this out before I did.

the idea: AI agents degrade the longer they run. this is well-documented now. Chroma Research calls it context rot. every tool call result, every file read, every prior decision piles up in the context window. signal-to-noise ratio drops. by hour 4 the agent is making worse decisions than it was at minute 10.

the fix: kill the agent every iteration. on purpose.

```bash
while :; do
  cat PROMPT.md | claude --dangerously-skip-permissions --print
done
```

each iteration starts fresh. reads state from files on disk. does one task. writes results back. exits clean. the bash loop restarts a new instance. the agent forgets everything. the files remember everything.

this isn't my insight. Huntley published it, Anthropic liked it enough to ship an official Ralph plugin in Claude Code, and snarktank/ralph has 10K+ stars on GitHub. the pattern works.

## what I actually built on top

most Ralph implementations are for software development. write code, run tests, commit, repeat. mine isn't.

I needed 182 business operations automated. research, content generation, ecommerce scanning, lead qualification, competitive monitoring, trend detection. things that aren't "write code and run tests." so I built tooling around the pattern for general-purpose ops.

### the factory

writing 182 separate loop configs by hand would take months. so I wrote a factory. feed it a spreadsheet with operation names, descriptions, success criteria, and tools needed:

```bash
memento factory --from ops.xlsx --generate-all
```

outputs 182 loop directories. each one has prompt.md tailored to that operation, prd.json with tasks broken into testable stories, progress.txt for learnings, and run.sh configured to go. this is just a scaffolding tool. yeoman for agent loops. but it saves real time when you're setting up dozens of operations.

### wave-based orchestration

I needed multiple agents working in parallel without stepping on each other. so I set up wave-based execution. standard pipeline pattern.

wave 1: 5 research agents run in parallel. each one has a defined scope and a file ownership map. agent A writes to `research/markets.md`. agent B writes to `research/competitors.md`. neither touches the other's files.

wave 2: 3 processing agents read wave 1's outputs (read-only). compile, deduplicate, score.

wave 3: 3 output agents read wave 2's results. generate final deliverables.

this is a DAG. same concept as Make, Airflow, GitHub Actions. the difference is the contracts are file-based and the executors are LLM agents instead of containers. simpler to set up. tradeoff is less robust error handling.

### 3 state files

I keep system state in three files. calling them "3-layer memory architecture" sounds impressive but they're just standard ops patterns:

1. a status file (HEARTBEAT.md). under 20 lines. revenue, leads, active loops, cron health. any new agent reads this in 3 seconds and knows the system state. this is just a monitoring dashboard in markdown.

2. a checkpoint file (active-tasks.md). if an agent dies mid-task, the next iteration reads this and picks up where it left off. this is crash recovery. same pattern as WAL in databases or checkpointing in batch processing.

3. append-only logs. every tool call, every pipeline step. never deleted. this is just log files.

no vector database. no embeddings. just files on disk. the simplicity has real value. complex memory systems introduce failure modes. files don't break in interesting ways.

### budget routing

62 loops running overnight on Claude API will burn money. I route every call through budget constraints:

- opus for processing untrusted external content. web scraping, third-party APIs. the extra reasoning capacity helps against prompt injection in scraped data.
- sonnet and haiku for internal operations. file management, CSV processing. faster, cheaper, safe because the data is trusted.
- hard daily spend caps. not alerts. the system stops when it hits the ceiling.

this is the part I've seen the fewest other people do. most Ralph implementations don't think about cost control because they're running one loop at a time. when you're running 62 overnight, you need guardrails.

## the numbers

battle-tested across my production system over 3 months:

- 282 automation scripts
- 62 autonomous loop directories
- 182+ operations with factory-generated loops
- 57 active cron jobs
- 11 agents across 3 waves for overnight runs
- 0 context rot incidents since adopting the stateless pattern

real context: this runs on two MacBooks. not a data center. not a cloud deployment. consumer hardware, cron jobs, markdown files.

## the 10 rules

inherited from Huntley's Ralph pattern. I didn't change them because they work:

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

## what else exists

being honest about where this fits.

**OpenHands** (65K stars) does the stateless principle better from an engineering standpoint. event sourcing, immutable components, reproducible sessions. it's what this would look like if a team of distributed systems engineers built it. if you need production-grade with proper fault tolerance, use that.

**SWE-agent** (18K stars) has a more principled approach to constraining what agents can do. formal benchmarks. per-issue fresh context. if you're doing software engineering tasks specifically, it's more battle-tested.

**snarktank/ralph** (10K stars) is the canonical implementation. simpler than what I built, which is a feature if you don't need the ops tooling.

**what mine adds:** the factory for generating loops from spreadsheets of non-coding operations, wave-based orchestration, budget routing, and the operational proof that this works for business ops at the 60+ loop scale. that's the gap I'm filling. not the loop pattern itself.

## the Memento parallel

I named it after the Nolan film. Leonard Shelby can't form new memories. uses Polaroid photos and tattoos as external memory. reads his own notes every morning to reconstruct context.

it's a good analogy for what these agents do. fresh context every iteration. external memory on disk. no continuity of experience between iterations, but full continuity of knowledge through the filesystem.

the philosophical question is real: if an agent reads all the same state files but has zero memory of prior iterations, is it the "same" agent? the practical answer is it doesn't matter. the work persists. the agent is temporary. the filesystem is the source of truth.

## open source

MIT licensed. take it, fork it, strip the parts you don't need.

what's included:
- 62 loop templates (research, content, ecommerce, growth, outbound, specialized)
- factory system for generating loops from any operation spreadsheet
- wave-based swarm orchestration with file ownership maps
- budget-first model routing with hard spend caps
- crash recovery via checkpoint files
- progress monitor for real-time loop status

repo: github.com/fnsmdehip/memento

the core loop pattern is Huntley's. the ops tooling around it is mine. use whatever's useful.
