# dogwalk

a fully autonomous multi-agent operating system. not a framework. a turnkey system you clone and run.

## what this does

dogwalk orchestrates 33 AI agents across 8 parallel venture types using a 7-layer command hierarchy. a CEO agent (L0) delegates to venture managers (L1) who dispatch specialist swarm agents with smart model routing (Opus for strategy, Sonnet for execution, Haiku for maintenance). every agent queries 15K+ curated intelligence entries before acting. every output gets scored for alignment drift. every decision gets adversarial review before execution.

the result: a self-healing, self-improving system that treats your operations like a hedge fund. it runs 10+ ventures simultaneously, auto-kills underperformers, doubles down on winners, and compounds synergies across the portfolio (4.5x-8.7x multipliers measured).

## the problem

every agent framework gives you building blocks and says "good luck." CrewAI gives you agent classes. AutoGen gives you conversation patterns. LangGraph gives you state machines. DSPy gives you prompt optimizers. you still have to architect the system, wire the intelligence, build the review pipeline, handle crashes, prevent drift, and close every loop yourself.

then your agents run on default LLM knowledge. no curated intelligence. no adversarial review. no outcome verification. no correction learning. they produce output. nobody checks if the output was good. nobody checks if downstream actions happened. the loop never closes.

dogwalk ships the entire operating system. 7 layers of command hierarchy. adversarial challengers that review every major decision. circuit breakers that recover from crashes. soul drift scoring that catches when agents start producing slop. correction chain learning that mines YOUR feedback to predict what you actually want.

your agent framework optimizes for benchmarks. this optimizes for your approval.

## architecture

```
L0  CEO ORCHESTRATOR
    24/7 cycle. 16 phases. delegates everything. decides nothing alone.
    |
L1  VENTURE MANAGERS (8 parallel)
    each manages one venture type. own schedule, own state, own kill criteria.
    |
L2  INTELLIGENCE LAYER
    15K+ curated entries. queried before every action. not LLM defaults.
    |
L3  EXECUTION SWARM (25 specialist agents)
    smart model routing: Opus (strategy) / Sonnet (execution) / Haiku (maintenance)
    |
L4  COLLECTION + INGESTION
    scrapers, monitors, alpha processors. raw signal in, structured intel out.
    |
L5  QUALITY + REVIEW
    adversarial challengers. soul drift scoring. writer != reviewer enforced.
    |
L6  MAINTENANCE + SELF-HEALING
    watchdog, crash recovery, atomic checkpoints, circuit breakers, file locking.
```

## highlights

### 6to1 correction chain learning

the core metric. 6.9 average corrections per task before the system produced what was actually wanted. that's 5.9 wasted round trips per task. dogwalk mines your correction history using timestamp-proximate prompt clustering, identifies when you're correcting vs starting new work, builds a correction chain model, and extracts meta-rules that would have prevented each correction. target: 1 correction or less.

### adversarial review

major decisions get reviewed by challenger agents before execution. Devil's Advocate, Risk Assessor, Market Reality Checker. writer != reviewer enforced at the architecture level. cross-model validation (Opus reviews Sonnet output, Sonnet reviews Opus output). no single agent can approve its own work.

### portfolio theory

the system treats operations like a hedge fund portfolio. 10+ ventures run simultaneously with independent kill criteria and double-down triggers. app under $100 MRR after 60 days gets killed. content under 500 followers after 90 days gets killed. anything showing 20%+ growth at $500+ gets doubled. synergy multipliers (4.5x-8.7x) compound across ventures that feed each other.

### bias-null protocol

5-point pre-output filter that runs silently before every major output. catches: legacy smuggling (defaulting to "industry standard says X"), preemptive appeasement (hedging when the answer is one-directional), lived-gap check (does this match observable reality or is it academic), popular-default trap (recommending what appeared most in training data vs what's best for THIS system), training-bias correction (counterweighting Claude's over-indexing on caution and consensus).

### soul drift scoring

continuous 0-10 alignment scoring of every agent output against behavioral directives in SOUL.md. anti-patterns detected: hedging, AI slop vocabulary, orphan documents, corporate voice, over-building. alert triggers when system average drops below 6/10. the system catches its own quality decay before you notice it.

### blocking gates

deterministic state machine. every major action goes through PENDING, then APPROVED or REJECTED. there is no path from REJECTED to APPROVED without human override. no workaround. no agent can bypass the gate. the state machine is the law.

### intelligence-first execution

every agent queries 15K+ curated intelligence entries before acting. not default LLM knowledge. not whatever was popular in training data. curated, scored, categorized entries from 484 mapped documents with 98.3% coverage. the intelligence layer is the difference between an agent that sounds smart and an agent that IS informed.

### self-healing

24/7 watchdog process. crash recovery with atomic checkpoints (CycleCheckpoint class with stale detection and resume-on-crash). circuit breakers that trip after repeated failures. file locking (fcntl.flock) preventing concurrent corruption. stale lock cleanup. retry with exponential backoff. the system assumes it will crash and builds recovery into every operation.

### user voice injection

extracts YOUR communication style from prompt history. tone profile, preferred vocabulary, banned words, correction patterns. injects this into every agent's prompt so output matches your voice on the first try. not "configure your agent's personality." automatic extraction from how you actually write.

## components

| module | what it does |
|--------|-------------|
| `voice_extractor` | analyzes prompt history, outputs tone profile + banned words + preferred vocabulary |
| `cognitive_engine` | builds correction chains from timestamp-proximate prompts, extracts meta-rules |
| `pattern_miner` | finds correction markers, escalation triggers, satisfaction signals |
| `user_sim_refiner` | simulates your critique on project files using extracted cognitive architecture |
| `loop_closer` | 4 loops: decisions, feedback, pipeline advancement, soul drift scoring |
| `self_audit` | checks system files for AI slop, context bloat, missing protocols, broken scripts |
| `decision_engine` | rule-based + LLM decision pipeline with CSV audit trail. every decision logged |
| `resilience` | retry with backoff, file locking (fcntl), circuit breaker, prompt injection defense |
| `conversation_logger` | extracts user+assistant messages from session transcripts into searchable JSONL |
| `session_briefing` | generates "what happened since last session" from git + state files. no LLM calls |

## what makes this different

| | dogwalk | CrewAI | AutoGen | LangGraph | DSPy |
|---|---|---|---|---|---|
| what it is | turnkey OS | framework | framework | framework | optimizer |
| primary signal | your corrections | task outputs | conversations | state transitions | labeled examples |
| intelligence | 15K+ curated entries pre-action | LLM defaults | LLM defaults | LLM defaults | labeled examples |
| adversarial review | challenger agents + cross-model | none | none | none | none |
| portfolio theory | kill losers, double winners, synergy stacks | none | none | none | none |
| self-healing | circuit breaker, crash recovery, atomic checkpoints | basic retry | basic retry | none | none |
| user voice | extracted from prompt history | none | none | none | none |
| soul drift | 0-10 scoring per output | none | none | none | none |
| blocking gates | deterministic state machine | none | none | state-based | none |
| task dependencies | real DAGs, not cron timing | sequential | conversation flow | graph edges | pipeline |
| dependencies | stdlib only | many | many | langchain | pytorch |

## quick start

```bash
# clone and install
git clone https://github.com/fnsmdehip/dogwalk.git
cd dogwalk
pip install -e .

# set your project root
export DOGWALK_ROOT=/path/to/your/project

# create directories
mkdir -p data output state logs

# if you have Claude Code transcripts, extract them
python3 -m dogwalk.core.conversation_logger --extract

# build voice model from your prompt history
python3 -m dogwalk.core.voice_extractor --extract

# build cognition model (correction chains + meta-rules)
python3 -m dogwalk.core.cognitive_engine --build-model

# mine patterns (corrections, escalations, satisfactions)
python3 -m dogwalk.core.pattern_miner --mine

# see what the system learned about you
python3 -m dogwalk.core.voice_extractor --status

# get injection string for your agent prompts
python3 -m dogwalk.core.voice_extractor --inject

# run self-audit
python3 -m dogwalk.core.self_audit --audit

# generate session briefing
python3 -m dogwalk.core.session_briefing --save

# close all loops (decisions, feedback, pipeline, soul drift)
python3 -m dogwalk.core.loop_closer --cycle
```

## data format

dogwalk reads JSONL files. each line is a JSON object with at minimum:

```json
{"ts": "2026-03-15T14:30:00", "prompt": "your prompt text here"}
```

optional fields: `role` (user/assistant), `session_id`, `content_length`.

you can also use `content` or `text` instead of `prompt`.

decision engine outputs CSV audit trails:

```csv
timestamp,decision_id,action,reasoning,outcome,score
2026-03-15T14:30:00,d_001,deploy_app,high_growth_signal,success,8.2
```

## environment variables

all paths are configurable. nothing is hardcoded.

| variable | default | description |
|----------|---------|-------------|
| `DOGWALK_ROOT` | cwd | project root directory |
| `DOGWALK_PROMPTS` | `data/prompts.jsonl` | prompt history file |
| `DOGWALK_CONVERSATIONS` | `data/conversations.jsonl` | conversation history |
| `DOGWALK_VOICE_MODEL` | `output/voice_model.json` | voice model output |
| `DOGWALK_SOUL_MD` | `templates/SOUL.md` | agent identity file |
| `DOGWALK_INSTRUCTIONS` | `templates/CLAUDE.md` | system instructions |
| `DOGWALK_TRANSCRIPT_DIRS` | `~/.claude/projects` | transcript directories (comma-separated) |

## the numbers

from real usage across 200+ sessions:

- 33 autonomous agents running (8 venture + 25 swarm)
- 7-layer execution hierarchy (L0-L6)
- 15,000+ curated intelligence entries
- 484 documents mapped in intelligence router (98.3% coverage)
- 1,510 prompts analyzed
- 168 correction chains extracted
- 6.9 average corrections per chain before resolution (target: 1)
- 451 satisfaction signals identified
- 112 active cron entries
- 4.5x-8.7x synergy multipliers across venture portfolio
- 0 external dependencies

## use cases

**solo founders running AI-first businesses.** you need 10 things happening simultaneously. content, outbound, app development, lead gen, monetization. dogwalk runs all of them as parallel ventures with independent kill criteria, shared intelligence, and synergy multipliers. you do account creation and payments. the system does everything else.

**teams shipping autonomous agent systems.** your agents need consistent identity, adversarial review, crash recovery, and closed-loop verification. dogwalk provides the full stack: soul drift scoring catches quality decay, challenger agents review major decisions, circuit breakers handle failures, and the loop closer verifies downstream actions actually happened.

**anyone who's corrected their AI 1000+ times.** those corrections contain transferable rules. dogwalk extracts them, builds a cognitive model of what you actually want, and injects it into every agent output. the system learns YOUR patterns so you stop repeating yourself.

**content teams maintaining voice across AI output.** the voice extractor builds a tone profile from real prompts. banned words, preferred vocabulary, sentence structure patterns. inject it into any agent and the output matches your style instead of generic assistant voice.

## templates

the `templates/` directory contains starting points for the behavioral layer:

- `SOUL.md` -- agent identity file with bias-null stack, competitive cognition protocol, constitutional self-correction, soul drift anti-patterns
- `bias-null.md` -- the 5-point pre-output filter (legacy smuggling, preemptive appeasement, lived-gap check, popular-default trap, training-bias correction)
- `voice-config.json` -- example voice model showing the extracted data structure (tone, vocabulary, banned words, correction history)
- `CLAUDE.md` -- template for wiring dogwalk into your system instructions with intelligence-first execution rules

## project structure

```
dogwalk/
  core/
    voice_extractor.py     # analyze prompts, build voice model, inject into agents
    cognitive_engine.py    # correction chains + meta-rules + task indexing
    pattern_miner.py       # find corrections, escalations, satisfaction signals
    user_sim_refiner.py    # simulate user critique autonomously
    loop_closer.py         # 4 loops: decisions, feedback, pipeline, soul drift
    self_audit.py          # meta-improvement audit (the system that audits the system)
    decision_engine.py     # rule-based + LLM decision pipeline with CSV audit trail
    resilience.py          # retry, file locking, circuit breaker, sanitization, loop detection
    conversation_logger.py # extract session transcripts into searchable JSONL
    session_briefing.py    # generate session start briefings (no LLM calls, pure file reads)
  templates/
    SOUL.md                # agent identity + behavioral directives
    bias-null.md           # 5-point bias correction protocol
    voice-config.json      # example extracted voice model
    CLAUDE.md              # system wiring template
  examples/
    example_correction_chains.json   # sample correction chain data
    example_meta_rules.md            # sample extracted meta-rules
```

## dependencies

none. stdlib only. python 3.10+.

`resilience.py` uses `fcntl` for file locking which is unix/macOS only. on windows, the locking won't work but everything else will.

## license

MIT
