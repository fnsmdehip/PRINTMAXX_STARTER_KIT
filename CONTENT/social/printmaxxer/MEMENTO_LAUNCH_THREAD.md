# memento launch thread

**Status:** PENDING_REVIEW
**Platform:** X/Twitter (@PRINTMAXXER)
**Type:** Launch thread (10 tweets)
**Voice:** copy-style.md compliant

---

## tweet 1 (hook)

I run 62 autonomous AI agent loops overnight on two laptops. 282 scripts. 57 cron jobs. research, content, outreach, competitive intel.

open sourcing the operational tooling. here's the full system.

---

## tweet 2 (problem)

the core problem with long-running AI agents: they get dumber the longer they run.

context rot. well-documented now. every tool call, every file read piles up. by hour 4 the agent is drowning in its own history.

---

## tweet 3 (pattern)

the fix is Geoffrey Huntley's Ralph pattern. credit where it's due. he figured this out.

kill the agent every iteration. fresh context. one task. writes state to files on disk. bash loop restarts a new instance.

```bash
while :; do
  cat PROMPT.md | claude --print
done
```

Anthropic liked it enough to ship an official plugin.

---

## tweet 4 (what I added)

most Ralph implementations are for coding. write code, run tests, commit.

mine isn't. I needed 182 business operations automated. research, ecom scanning, lead qualification, trend detection, content generation.

so I built ops tooling on top of the pattern. calling it memento.

---

## tweet 5 (factory)

the main thing: a factory that generates loop configs from a spreadsheet.

feed it 182 operations. one command. it scaffolds prompt.md, prd.json, progress.txt, run.sh for each one.

just a template generator. yeoman for agent loops. but it saves real time when you're setting up 60+ operations.

---

## tweet 6 (orchestration)

wave-based orchestration on top. standard pipeline pattern.

wave 1: 5 research agents (parallel, file ownership maps)
wave 2: 3 processing agents (compile, deduplicate)
wave 3: 3 output agents (deliverables)

it's a DAG with file-based contracts instead of API contracts. simpler to set up than Airflow. tradeoff is less strong.

---

## tweet 7 (budget)

the part nobody else seems to do: budget routing.

62 loops overnight will burn money if you're not careful.

opus for untrusted external content (web scraping). sonnet/haiku for internal ops. hard daily spend caps with enforcement, not alerts.

predictable overnight costs. not "I woke up to a $400 bill."

---

## tweet 8 (numbers)

3 months in production:
- 282 scripts, 62 loop directories, 57 cron jobs
- 182+ operations factory-generated
- 0 context rot incidents since going stateless
- runs on 2 MacBooks. not a data center.

---

## tweet 9 (honest positioning)

being honest about where this fits:

- OpenHands (65K stars) does stateless better architecturally. event sourcing.
- SWE-agent (18K stars) more rigorous for coding tasks.
- snarktank/ralph (10K stars) is the canonical, simpler implementation.

what mine adds: the factory for non-coding operations, wave orchestration, and budget routing at the 60+ loop scale.

---

## tweet 10 (close)

MIT licensed. named after the Nolan film. agents that forget everything, external memory on disk.

the core loop pattern is Huntley's. the ops tooling is mine.

- 62 loop templates
- factory system
- swarm orchestration
- budget routing
- crash recovery

github.com/fnsmdehip/memento
