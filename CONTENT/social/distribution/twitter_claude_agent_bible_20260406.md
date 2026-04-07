# Twitter Thread: Claude Code Agent Bible
# Asset: The Autonomous Agent Playbook (14_CLAUDE_CODE_AGENT_BIBLE.html)
# Date: 20260406
# Target: Technical solopreneurs, indie devs, AI builders

---

## THREAD (7 tweets)

**Tweet 1 (hook)**
I have 33 AI agents running on one Mac right now.

No cloud bills. No orchestration platform. No venture funding.

Claude Code + Python + cron. That's it.

Here's the full architecture. 🧵

---

**Tweet 2**
Most "agent" tutorials give you a script that calls an API.

That's not an agent. That's a function with a chatbot wrapper.

A real agent has:
- Persistent memory (filesystem)
- Downstream consumers (other agents it feeds)
- Failure recovery (lock files, timeouts)
- A reason to run without human prompting

---

**Tweet 3**
The 3-layer stack I use:

Layer 1: Always-running cron scripts. Scrapers, monitors, backups. Zero AI needed.

Layer 2: AI-assisted workflows. Claude gets called when judgment is needed. Haiku for routing, Sonnet for execution, Opus for quality gates.

Layer 3: Full autonomous agents. Read state, make decision, write output, exit.

---

**Tweet 4**
The pattern most people skip: filesystem as memory.

Agents that don't persist state fail. They forget context, repeat work, loop forever.

Every agent I run reads from files at start, writes to files at end. State lives on disk. Agent is stateless per run.

No database. No vector store. Just consistent file schemas.

---

**Tweet 5**
Inter-agent communication without shared state:

Message bus = a JSONL file.

Agent A appends: {"type": "LEAD", "payload": {...}, "for": "agent_b"}
Agent B polls on cron. Reads its messages. Processes. Deletes.

No race conditions. No queues to manage. Works at 33 agents with zero infrastructure.

---

**Tweet 6**
Model routing matters more than people think.

Opus at $15/M tokens for a task Haiku can do at $0.25/M = 60x overspend.

My routing:
- Opus: strategy, quality gates, creative decisions
- Sonnet: code gen, research synthesis, content drafts
- Haiku: classification, routing, mechanical bulk tasks

---

**Tweet 7 (CTA)**
I wrote all of this up. 33 agents documented. Architecture. Cron templates. Inter-agent patterns. The Ralph loop. Model routing.

$47. The actual system, not a prompt pack.

Link in bio.

(If you found this useful, repost tweet 1. Took me 6 months to build this system.)

---

## SINGLES (standalone tweets, no thread)

**Single A (reply bait)**
Hot take: most Claude Code "agents" are just scripts with `claude -p` at the end.

Real agents have persistent memory, downstream consumers, and failure recovery.

The difference between a toy and a production system is about 200 lines of scaffolding.

What's your agent stack look like?

---

**Single B (numbers hook)**
My AI agent system costs $0/month in infrastructure.

33 agents. 8 hours of work per overnight run.

Tools: Claude Code (subscription I already pay for), Python stdlib, launchd (macOS built-in), cron (also built-in).

Cloud infra is optional, not required.

---

**Single C (educational)**
The Ralph loop. The thing that changed how I build.

```
while :; do
  cat PROMPT.md | claude --dangerously-skip-permissions --print
done
```

Iterate PROMPT.md. Agent picks up new instructions next loop. Memory = files on disk. Context = disposable.

Ships deliverables by morning without you watching it.

