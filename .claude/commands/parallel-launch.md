---
name: parallel-launch
description: Launch multiple agents in parallel for bulk operations. Maximum efficiency mode.
---

# Parallel Agent Launch

Launch multiple specialized agents simultaneously for maximum throughput.

## Available Parallel Configurations

### Content Blitz (3 agents)
```
Agent A: Generate 25 longtail pages (Haiku)
Agent B: Generate 40 social posts (Haiku)
Agent C: Review 20 alpha entries (Sonnet)
```

### Full Stack (4 agents)
```
Agent A: Longtail generation
Agent B: Social post generation
Agent C: Alpha review + integration
Agent D: Validation suite
```

### Research Mode (2 agents)
```
Agent A: Run alpha extractor on X accounts
Agent B: Run alpha extractor on Reddit
```

## Usage

Specify which configuration to run:
- `/parallel-launch content` - Content Blitz
- `/parallel-launch full` - Full Stack
- `/parallel-launch research` - Research Mode

## Coordination

- Agents write to separate files (no conflicts)
- LEDGER updates are sequential (Agent C waits for A/B)
- Summary provided when all complete
