# agent-soul

6.9 corrections to reach what the user wanted. this system gets there in 1.

## what this does

agent-soul is a meta-cognition framework for AI agents. it analyzes how you correct your AI, extracts transferable rules from those corrections, and feeds them back into the system so it stops making the same mistakes. your agents learn YOUR thinking patterns, not generic benchmarks.

the output is a closed loop: prompts go in, corrections get tracked, rules get extracted, agents get better, fewer corrections needed.

## the problem

every agent framework optimizes for the wrong thing. they benchmark on HumanEval, MMLU, whatever synthetic test tells VCs the number went up. but when you actually USE an AI agent, the quality signal is in your corrections. "no not that." "i said X not Y." "bruh this is surface level." "stop asking and just do it."

that's the real training data. 168 correction chains across 1,510 prompts. avg 6.9 corrections before the system produced what was actually wanted. that's 5.9 wasted round trips per task. multiply by every task, every day, every user.

the reason: LLMs default to median output. popular opinion, safe hedging, "it depends" non-answers, AI vocabulary nobody actually uses. your agent sounds like every other agent because it's optimizing for generic approval, not YOUR approval.

agent-soul fixes this by making YOUR corrections the primary training signal.

## architecture

```
USER PROMPTS (jsonl)
       |
       v
  VOICE EXTRACTOR -----> voice model (tone, vocabulary, banned words)
       |
       v
  PATTERN MINER -------> correction markers, escalation triggers, satisfaction signals
       |
       v
  COGNITIVE ENGINE -----> correction chains, task index, meta-rules
       |
       v
  USER-SIM REFINER -----> simulated critique using extracted cognitive architecture
       |
       v
  LOOP CLOSER ----------> soul drift scoring (0-10 alignment check)
       |
       v
  SELF AUDIT -----------> meta-improvement (the system that audits the system)
       |
       +----> feeds back into SOUL.md + voice model + agent prompts
              (correction chain gets shorter each cycle)
```

## components

| module | what it does | why it matters |
|--------|-------------|----------------|
| `voice_extractor` | analyzes prompt history, outputs tone profile + banned words + preferred vocabulary | your agent matches YOUR communication style, not generic assistant voice |
| `cognitive_engine` | builds correction chains from timestamp-proximate prompts, extracts meta-rules | identifies exactly WHERE and WHY the system fails you repeatedly |
| `pattern_miner` | finds correction markers, escalation triggers, satisfaction signals | quantifies what makes you push back vs what makes you say "perfect" |
| `user_sim_refiner` | simulates your critique on project files using extracted cognitive architecture | autonomous improvement loop that asks "what would the user complain about?" |
| `loop_closer` | three loops: decision execution, feedback tracking, soul drift scoring | closes the gap between "agent produced output" and "output led to results" |
| `self_audit` | checks system files for AI slop, context bloat, missing protocols, broken scripts | the system that improves the system. meta-improvement on a cron schedule |
| `decision_engine` | rule-based + LLM decision pipeline with full audit trail (csv ledger) | every decision logged with reasoning. no black box actions |
| `resilience` | retry with backoff, file locking (fcntl), circuit breaker, prompt injection defense | agents crash. this module makes them crash gracefully and recover |
| `conversation_logger` | extracts user+assistant messages from Claude session transcripts | builds the raw data that everything else feeds on |
| `session_briefing` | generates "what happened since last session" from git + state files | no LLM calls. pure file reading. < 30 seconds. agents wake up informed |

## what makes this different

| | agent-soul | DSPy | LangGraph | generic prompt engineering |
|---|---|---|---|---|
| primary signal | your actual corrections | synthetic benchmarks | execution graphs | vibes |
| learns from | prompt history (real) | labeled examples (curated) | state transitions | nothing |
| voice matching | yes (tone, vocabulary, banned words) | no | no | manual |
| soul drift detection | yes (0-10 scoring per output) | no | no | no |
| bias-null protocol | yes (5-point filter on every output) | no | no | no |
| user simulation | yes (simulates YOUR critique) | no | no | no |
| closed-loop audit | decide > act > log > learn > improve | optimize > deploy | build graph > run | write prompt > hope |
| dependencies | stdlib only (python 3.10+) | pytorch, many | langchain ecosystem | none |

the core difference: correction chains as primary signal. not "does this pass a benchmark" but "does this stop the user from saying 'no not that' for the 7th time."

## quick start

```bash
# install
pip install -e .

# set your project root
export AGENT_SOUL_ROOT=/path/to/your/project

# create data directory and seed with your prompt history
mkdir -p data output state logs

# if you have Claude Code transcripts, extract them
python3 -m agent_soul.core.conversation_logger --extract

# build voice model from your prompt history
python3 -m agent_soul.core.voice_extractor --extract

# build cognition model (correction chains + meta-rules)
python3 -m agent_soul.core.cognitive_engine --build-model

# mine patterns
python3 -m agent_soul.core.pattern_miner --mine

# see what the system learned about you
python3 -m agent_soul.core.voice_extractor --status

# get injection string for your agent prompts
python3 -m agent_soul.core.voice_extractor --inject

# run self-audit
python3 -m agent_soul.core.self_audit --audit

# generate session briefing
python3 -m agent_soul.core.session_briefing --save

# close loops
python3 -m agent_soul.core.loop_closer --cycle
```

### prompt data format

agent-soul reads JSONL files. each line is a JSON object with at minimum:

```json
{"ts": "2026-03-15T14:30:00", "prompt": "your prompt text here"}
```

optional fields: `role` (user/assistant), `session_id`, `content_length`.

you can also use `content` or `text` instead of `prompt`.

### environment variables

all paths are configurable. nothing is hardcoded.

| variable | default | description |
|----------|---------|-------------|
| `AGENT_SOUL_ROOT` | cwd | project root directory |
| `AGENT_SOUL_PROMPTS` | `data/prompts.jsonl` | prompt history file |
| `AGENT_SOUL_CONVERSATIONS` | `data/conversations.jsonl` | conversation history |
| `AGENT_SOUL_VOICE_MODEL` | `output/voice_model.json` | voice model output |
| `AGENT_SOUL_SOUL_MD` | `templates/SOUL.md` | agent identity file |
| `AGENT_SOUL_INSTRUCTIONS` | `templates/CLAUDE.md` | system instructions |
| `AGENT_SOUL_TRANSCRIPT_DIRS` | `~/.claude/projects` | transcript directories (comma-separated) |

## the numbers

from real usage across 200+ sessions:

- 1,510 prompts analyzed
- 168 correction chains extracted
- 6.9 average corrections per chain before resolution
- 451 satisfaction signals identified
- 31 "wrong direction" corrections (system misread intent)
- 23 "anti-lazy" corrections (system defaulted to shallow output)
- 18 "depth-first" escalations (user wanted more and system didn't anticipate)
- 14 "execute don't ask" corrections (system asked permission instead of acting)

the goal: reduce that 6.9 to 1. the system learns your patterns so the AI stops making the same mistakes.

## use cases

**solo founders who want their AI to think like them.** you've spent 100+ hours correcting your AI. those corrections contain transferable rules. agent-soul extracts them so you stop repeating yourself.

**AI teams shipping autonomous agents.** agents need consistent identity and quality. soul drift scoring catches when an agent starts hedging, using AI slop, or producing output that doesn't match the intended voice.

**content teams maintaining voice across AI output.** the voice extractor builds a tone profile from real prompts. inject it into any agent prompt and the output matches your style instead of generic assistant voice.

**anyone running AI agents on a cron schedule.** loop closer turns "agent produced a report" into "agent produced a report, downstream agent acted on it, results were tracked." without loop closing, autonomous agents produce output nobody reads.

## templates

the `templates/` directory contains generic starting points:

- `SOUL.md` -- agent identity file with bias-null stack, competitive cognition protocol, constitutional self-correction
- `bias-null.md` -- the 5-point filter that catches default LLM priors before they reach output
- `voice-config.json` -- example voice model showing the data structure
- `CLAUDE.md` -- template for wiring agent-soul into your system instructions

## project structure

```
agent-soul/
  core/
    voice_extractor.py     # analyze prompts, build voice model
    cognitive_engine.py    # correction chains + meta-rules
    pattern_miner.py       # find corrections, escalations, satisfactions
    user_sim_refiner.py    # simulate user critique autonomously
    loop_closer.py         # close loops: decide, act, log, learn
    self_audit.py          # meta-improvement audit
    decision_engine.py     # rule-based decision pipeline
    resilience.py          # retry, locks, circuit breaker, sanitization
    conversation_logger.py # extract session transcripts
    session_briefing.py    # generate session start briefings
  templates/
    SOUL.md                # agent identity template
    bias-null.md           # bias correction protocol
    voice-config.json      # example voice model
    CLAUDE.md              # system wiring template
  examples/
    example_correction_chains.json   # sample correction chain data
    example_meta_rules.md            # sample extracted meta-rules
```

## dependencies

none. stdlib only. python 3.10+.

the framework uses `fcntl` for file locking which is unix/macOS only. if you're on windows, the locking in `resilience.py` won't work but everything else will.

## license

MIT
