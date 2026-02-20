# deadloop launch thread

**Status:** PENDING_REVIEW
**Platform:** X/Twitter (@PRINTMAXXER)
**Type:** Launch thread (10 tweets)
**Voice:** copy-style.md compliant

---

## tweet 1 (hook)

my agents kept getting dumber the longer they ran.

so I killed them. on purpose. every single iteration.

here's the open source framework I built to do it. 🧵

---

## tweet 2 (problem)

the problem nobody talks about: context rot.

run an AI agent for 2+ hours. watch it hallucinate. watch it forget instructions. watch it make increasingly worse decisions.

your context window is not an asset. it's a ticking time bomb.

---

## tweet 3 (fix)

the fix is counterintuitive.

kill the agent every single iteration. fresh context. one task. clean exit. state lives on disk, not in the context window.

I call it deadloop. the loop where agents die on purpose.

---

## tweet 4 (architecture)

deadloop architecture:

1. bash while loop restarts claude with fresh context
2. agent reads state from files (prompt.md + prd.json + progress.txt)
3. picks ONE task. executes it. writes state back to disk.
4. exits clean. loop restarts.

memory = filesystem. agent = disposable. work = permanent.

---

## tweet 5 (results)

ran 62 of these loops overnight. 182+ operations covered.

woke up to:
- 14 new ventures identified
- 25 existing ops bolstered with new intel
- 477 noise entries auto-archived
- 0 hallucinations
- 0 forgotten instructions

all autonomous. zero context rot.

---

## tweet 6 (factory)

built a factory system that generates these loops for any operation.

feed it a spreadsheet of 182 ops. one command. it outputs canonical loop structures for every single one.

prompt.md, prd.json, progress.txt, run.sh. ready to run.

`deadloop factory --from ops.xlsx`

---

## tweet 7 (swarm)

layer 2: wave-based swarm orchestration.

wave 1: 5 research agents run in parallel
wave 2: 3 processing agents compile results
wave 3: 3 output agents ship deliverables

interface contracts between waves. file ownership maps. agents never stomp each other's work.

---

## tweet 8 (memory)

layer 3: 3-tier memory that survives agent death.

- HEARTBEAT.md: 20 lines of pure numbers. 3 second system pulse.
- active-tasks.md: crash recovery. agent dies mid-task, next one picks up exact same spot.
- daily logs: append-only. every tool call, every pipeline step.

no vector DB. no embeddings. just files.

---

## tweet 9 (positioning)

where this fits:

openclaw = messaging gateway (13 platforms, voice, companion apps). the frontend.

deadloop = autonomous execution engine. loops that grind through 182+ ops while you sleep. the backend.

use both. openclaw talks to your users. deadloop ships your product.

---

## tweet 10 (close + CTA)

open sourcing the whole thing. MIT license.

- 62 loop templates
- factory system for any operation
- swarm orchestration (wave-based)
- 3-layer filesystem memory
- budget-first model routing
- crash recovery

if your agents get dumber the longer they run, your architecture is wrong.

github link in bio.
