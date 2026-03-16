# Self-Learning Systems Research — March 2026

## Top Finds (deploy immediately)

### 1. claude-reflect (BayramAnnakov)
- URL: github.com/BayramAnnakov/claude-reflect
- Detects correction patterns in real-time, queues with confidence scores
- `/reflect --scan-history` retroactively mines past sessions
- `/reflect-skills --days 30` discovers automation candidates from repeated patterns
- DEPLOY: as Claude Code skill/plugin

### 2. claude-meta (aviadr1)
- URL: github.com/aviadr1/claude-meta
- Meta-rules about how to write rules. "Reflect, abstract, generalize, add to CLAUDE.md"
- Zero dependencies. Already similar to our MARS protocol but more formalized.

### 3. Takiko Auto-Skill Generation
- URL: zenn.dev/takiko/articles/claude-code-skill-from-logs
- Extracts workflow patterns along WHAT/HOW/FLOW axes
- Auto-generates SKILL.md files from session history

### 4. Reflexion (NeurIPS 2023)
- URL: github.com/noahshinn/reflexion
- Verbal reinforcement learning — agents reflect on failures in text
- Store reflections in episodic memory, inject in future cycles
- Maps to: CEO agent verbal reflection after each cycle

### 5. EvoPrompt (prompt evolution)
- URL: github.com/beeevita/EvoPrompt
- Evolutionary algorithm for prompt optimization
- Treats prompts as population, applies mutations, evaluates fitness
- Maps to: evolving our 25 swarm agent prompts using loop_closer feedback

### 6. Hindsight (structured memory)
- URL: github.com/vectorize-io/hindsight
- 4 memory networks: World, Experiences, Opinion, Observation
- SOTA on LongMemEval benchmark
- Maps to: deep extraction from our 12K conversation entries

## Key Insight
The most practical systems use VERBAL/TEXTUAL self-improvement — storing reflections, corrections, and patterns as text injected into future contexts. NOT fine-tuning. This maps perfectly to our CLAUDE.md rules, session briefings, and agentic loop prompts.

## Implementation Priority
Phase 1: Deploy claude-reflect --scan-history on our logs
Phase 2: Add Reflexion buffer to CEO agent
Phase 3: EvoPrompt on swarm agent prompts
