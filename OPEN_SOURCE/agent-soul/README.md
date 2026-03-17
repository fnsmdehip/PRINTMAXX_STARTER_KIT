# sovrun

the cognitive and behavioral layer for autonomous AI agent systems. 10 modules, stdlib only, extracted from a production system.

## what this is

sovrun is 10 Python modules that give your AI agents: a voice model trained on YOUR prompts, correction chain learning that mines YOUR feedback into transferable rules, soul drift scoring that catches when agents start producing slop, a bias-null protocol that filters out LLM default behaviors, closed-loop decision execution, resilience primitives (circuit breaker, file locking, retry), and session continuity across context windows.

it was extracted from a production autonomous system. the modules are the reusable core. they don't depend on any specific agent framework, LLM provider, or orchestration pattern. wire them into whatever you're building.

## the problem

your AI agents run on default LLM knowledge and produce generic output. you correct them. they don't learn from the corrections. you correct them again. same mistakes. you've told your AI the same thing 50 times across different sessions and it still defaults to the behavior you hate.

meanwhile, nobody checks if agent output matches your actual voice. nobody scores whether agents are drifting from their intended behavior. nobody closes the loop between "agent decided X" and "X actually happened." nobody audits the system for AI slop creeping into your own config files.

sovrun solves each of these with a dedicated module.

## what's in the box

```
sovrun/
  core/
    voice_extractor.py     # your prompts -> voice model -> inject into any agent
    cognitive_engine.py    # correction chains -> meta-rules -> "would have prevented this"
    pattern_miner.py       # find what frustrates you, what satisfies you, what you correct
    user_sim_refiner.py    # simulate YOUR critique autonomously on any project
    loop_closer.py         # decisions -> execution -> feedback -> soul drift scoring
    self_audit.py          # the system audits itself for slop, bloat, broken scripts
    decision_engine.py     # closed-loop decisions with CSV audit trail
    resilience.py          # retry, file locking (fcntl), circuit breaker, loop detection
    conversation_logger.py # extract Claude session transcripts -> searchable JSONL
    session_briefing.py    # "what happened since last session" from git + state files
  templates/
    SOUL.md                # agent identity + behavioral directives template
    bias-null.md           # 5-point pre-output bias correction protocol
    voice-config.json      # example voice model structure
    CLAUDE.md              # template for wiring sovrun into system instructions
  examples/
    example_correction_chains.json
    example_meta_rules.md
```

## modules

### voice extractor

reads your prompt history (JSONL), identifies your vocabulary, tone, banned words, sentence patterns, and correction frequency. outputs a compact voice model JSON. then generates an injection string you prepend to any agent prompt so its output sounds like you instead of generic assistant.

```bash
python3 -m sovrun.core.voice_extractor --extract   # build model from prompts
python3 -m sovrun.core.voice_extractor --inject    # get injection string
python3 -m sovrun.core.voice_extractor --status    # model stats
python3 -m sovrun.core.voice_extractor --diff      # compare current vs previous
```

### cognitive engine

the core learning module. reads your prompt history, identifies when you're correcting vs starting new work using timestamp-proximate clustering, builds correction chains (sequences of prompts where you kept fixing the same thing), then extracts meta-rules that would have prevented each correction.

from production: 168 correction chains extracted, 6.9 average corrections per chain before the system produced what was actually wanted. target: 1.

```bash
python3 -m sovrun.core.cognitive_engine --build-model    # full cognition model
python3 -m sovrun.core.cognitive_engine --lookup "TASK"   # find similar past tasks
python3 -m sovrun.core.cognitive_engine --rules           # show meta-rules
python3 -m sovrun.core.cognitive_engine --chain-analysis  # correction chain stats
```

### pattern miner

finds three types of signals in your prompt history:
- **correction markers**: "no not that", "wrong", "lazy", "that's not what I said"
- **escalation triggers**: "deeper", "above and beyond", "surprise me", "actually think"
- **satisfaction signals**: "perfect", "exactly", "ship it"

mines these into transferable rules: what makes you happy, what pisses you off, what patterns to avoid.

```bash
python3 -m sovrun.core.pattern_miner --mine          # extract all patterns
python3 -m sovrun.core.pattern_miner --similar "Q"   # find similar past prompts
python3 -m sovrun.core.pattern_miner --corrections   # correction sequences
python3 -m sovrun.core.pattern_miner --effective     # satisfaction triggers
```

### user sim refiner

the autonomous critique loop. takes your extracted cognitive architecture (meta-rules, voice model, bias-null protocol) and simulates what YOU would criticize about a project's current state. outputs the critique for another agent or human to act on.

this is the perpetual improvement system. it applies your own thinking discipline when you're not in the room.

### loop closer

closes 4 open loops that plague autonomous systems:

1. **decision execution**: reads pending decisions, executes them, logs results
2. **feedback tracking**: did the agent's work lead to downstream results?
3. **pipeline advancement**: are things moving forward or stuck?
4. **soul drift scoring**: scores every agent output 0-10 against behavioral directives in SOUL.md. alerts when system average drops below 6/10.

safety: max 10 actions per cycle, allowlisted action types only, full audit trail.

```bash
python3 -m sovrun.core.loop_closer --cycle      # run all 4 loops
python3 -m sovrun.core.loop_closer --drift      # soul drift scoring only
python3 -m sovrun.core.loop_closer --status     # loop health
python3 -m sovrun.core.loop_closer --dry-run    # preview without executing
```

### self audit

the system that audits the system. checks your project for:
- AI slop vocabulary in your own config files
- context bloat (instruction files wasting tokens every session)
- missing meta-cognition protocols
- orphan scripts not wired into any automation
- prompt pattern health (are you learning from corrections?)

```bash
python3 -m sovrun.core.self_audit --audit    # full audit
python3 -m sovrun.core.self_audit --report   # latest findings
```

### decision engine

closed-loop autonomous decision pipeline: scan data sources, score opportunities, take action (within safety limits), log every decision with reasoning to CSV audit trail, update progress trackers. supports both rule-based threshold checks and LLM-delegated judgment calls.

```bash
python3 -m sovrun.core.decision_engine --cycle     # one decision cycle
python3 -m sovrun.core.decision_engine --status    # pipeline status
python3 -m sovrun.core.decision_engine --dry-run   # preview
```

### resilience

shared module that makes any agent production-grade:
- **retry with exponential backoff + jitter**: handles transient failures
- **file locking (fcntl)**: prevents concurrent file corruption
- **circuit breaker**: CLOSED -> OPEN -> HALF_OPEN -> CLOSED state machine
- **input sanitization**: prompt injection defense
- **trajectory logging**: append-only JSONL audit trail of agent decisions
- **loop detection**: guards against runaway agents

```python
from sovrun.core.resilience import retry, locked_file, CircuitBreaker
from sovrun.core.resilience import sanitize_for_prompt, TrajectoryLogger
```

### conversation logger

extracts user and assistant messages from Claude Code session transcript files (JSONL), stores them in a searchable format. supports incremental processing (tracks byte offsets), keyword search, statistics, and recent message display.

```bash
python3 -m sovrun.core.conversation_logger --extract       # process new transcripts
python3 -m sovrun.core.conversation_logger --search "kw"   # search history
python3 -m sovrun.core.conversation_logger --stats         # totals
python3 -m sovrun.core.conversation_logger --recent 20     # last N exchanges
```

### session briefing

generates a concise "what happened since last session" briefing from git diffs, state files, task trackers, and agent output directories. no LLM calls. pure file reading. finishes in under 30 seconds.

```bash
python3 -m sovrun.core.session_briefing --save    # save briefing
python3 -m sovrun.core.session_briefing --json    # JSON output
```

## templates

### SOUL.md

agent identity file. defines who the agent is, what it values, what anti-patterns to avoid. includes sections for: bias-null stack, competitive cognition protocol, constitutional self-correction rules, soul drift anti-patterns (hedging, AI slop, orphan docs, corporate voice, over-building).

the soul drift scorer in loop_closer reads this file and scores agent outputs against it.

### bias-null.md

5-point pre-output filter. run silently before any major output:

1. **legacy smuggling?** defaulting to "industry standard says X" when it doesn't apply?
2. **preemptive appeasement?** adding "but of course there are tradeoffs" when the answer is clearly one-directional?
3. **lived-gap check?** does this recommendation match observable reality or is it academic?
4. **popular-default trap?** recommending this because it appeared most in training data, or because it's genuinely best for THIS system?
5. **training-bias correction?** LLMs over-index on caution, consensus, credentialism. actively counterweight.

### voice-config.json

example of the voice model structure the voice extractor produces: tone profile, preferred terms, banned patterns, correction history summary.

### CLAUDE.md

template for wiring sovrun into your project's system instructions. session start hooks, reference file pointers, core rules, voice injection commands, loop closing schedule, self-audit cron.

## quick start

```bash
git clone https://github.com/fnsmdehip/sovrun.git
cd sovrun
pip install -e .

export SOVRUN_ROOT=/path/to/your/project
mkdir -p data output state logs

# extract your Claude Code transcripts
python3 -m sovrun.core.conversation_logger --extract

# build voice model from your prompt history
python3 -m sovrun.core.voice_extractor --extract

# build cognition model (correction chains + meta-rules)
python3 -m sovrun.core.cognitive_engine --build-model

# mine patterns
python3 -m sovrun.core.pattern_miner --mine

# see what the system learned about you
python3 -m sovrun.core.voice_extractor --status

# inject voice into your agent prompts
python3 -m sovrun.core.voice_extractor --inject

# close all loops
python3 -m sovrun.core.loop_closer --cycle

# audit the system
python3 -m sovrun.core.self_audit --audit
```

## what makes this different

| | sovrun | CrewAI | AutoGen | LangGraph | DSPy |
|---|---|---|---|---|---|
| what it is | cognitive layer (10 modules) | agent framework | conversation framework | state machine framework | prompt optimizer |
| learns from | your corrections + prompt history | nothing | nothing | nothing | labeled examples |
| voice modeling | extracts your style, injects into agents | none | none | none | none |
| correction chains | mines past failures into rules | none | none | none | none |
| soul drift | 0-10 scoring per output | none | none | none | none |
| bias correction | 5-point pre-output filter | none | none | none | none |
| loop closing | decisions -> execution -> feedback | none | none | none | none |
| self-audit | catches slop in your own system | none | none | none | none |
| resilience | circuit breaker, file locking, retry, loop detection | basic retry | basic retry | none | none |
| session continuity | transcript extraction + session briefing | none | none | none | none |
| user simulation | autonomous critique using your patterns | none | none | none | none |
| dependencies | stdlib only | many | many | langchain | pytorch |

## data format

sovrun reads JSONL files. each line is a JSON object with at minimum:

```json
{"ts": "2026-03-15T14:30:00", "prompt": "your prompt text here"}
```

optional fields: `role` (user/assistant), `session_id`, `content_length`. you can use `content` or `text` instead of `prompt`.

## environment variables

all paths are configurable. nothing is hardcoded.

| variable | default | description |
|----------|---------|-------------|
| `SOVRUN_ROOT` | cwd | project root directory |
| `SOVRUN_PROMPTS` | `data/prompts.jsonl` | prompt history file |
| `SOVRUN_CONVERSATIONS` | `data/conversations.jsonl` | conversation history |
| `SOVRUN_VOICE_MODEL` | `output/voice_model.json` | voice model output |
| `SOVRUN_SOUL_MD` | `templates/SOUL.md` | agent identity file |
| `SOVRUN_INSTRUCTIONS` | `templates/CLAUDE.md` | system instructions |
| `SOVRUN_TRANSCRIPT_DIRS` | `~/.claude/projects` | transcript directories (comma-separated) |

## production numbers

these are from the production system sovrun was extracted from:

- 1,510 prompts analyzed
- 168 correction chains extracted
- 6.9 average corrections per chain before resolution (target: 1)
- 451 satisfaction signals identified
- 0 external dependencies

the parent system uses sovrun's modules to power: voice injection across all agents, soul drift scoring with auto-alert at <6/10, correction chain learning that feeds meta-rules back into agent prompts, bias-null filtering on every major output, and loop closing that verifies agent decisions led to real outcomes.

## dependencies

none. stdlib only. python 3.10+.

`resilience.py` uses `fcntl` for file locking which is unix/macOS only. on windows, the locking won't work but everything else will.

## license

MIT
