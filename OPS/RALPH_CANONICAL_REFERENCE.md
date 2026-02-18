# Ralph Wiggum Agent Loop: Canonical Research Document

**Research Date:** 2026-02-05
**Sources:** GitHub repos, original blog posts, podcast transcripts, community documentation
**Purpose:** Authoritative reference for the TRUE ralph pattern from primary sources

---

## Table of Contents

1. [Origin Story and Creator](#1-origin-story-and-creator)
2. [The Core Loop](#2-the-core-loop)
3. [Key Insight: Context Rot and Stateless Resampling](#3-key-insight-context-rot-and-stateless-resampling)
4. [File Structure (Canonical)](#4-file-structure-canonical)
5. [prd.json Format](#5-prdjson-format)
6. [prompt.md / CLAUDE.md Authoring](#6-promptmd--claudemd-authoring)
7. [progress.txt: Filesystem Memory](#7-progresstxt-filesystem-memory)
8. [AGENTS.md: Discovered Patterns](#8-agentsmd-discovered-patterns)
9. [ralph.sh: The Loop Runner](#9-ralphsh-the-loop-runner)
10. [Backpressure and Feedback Loops](#10-backpressure-and-feedback-loops)
11. [Geoffrey Huntley's Advanced Playbook](#11-geoffrey-huntleys-advanced-playbook)
12. [Anthropic's Official Plugin](#12-anthropics-official-plugin)
13. [Best Practices and Anti-Patterns](#13-best-practices-and-anti-patterns)
14. [The Ecosystem](#14-the-ecosystem)
15. [Key Quotes Collection](#15-key-quotes-collection)

---

## 1. Origin Story and Creator

### Geoffrey Huntley (ghuntley.com)

Geoffrey Huntley is the original creator of the Ralph Wiggum technique. The technique went viral in the final weeks of 2025.

**Name origin:** The technique is named after Ralph Wiggum from The Simpsons, embodying "ignorance, persistence, and optimism." It is also a tribute to 1980s slang for vomiting ("ralph").

**Key quote from The Register (Jan 27, 2026):**
> "A bash loop that feeds an AI's output (errors and all) back into itself until it dreams up the correct answer."

**Ryan Carson (snarktank)** later built the most popular structured implementation at github.com/snarktank/ralph, adding PRD-driven task management, skills, and multi-tool support (Amp + Claude Code).

**First encounter:** Dex (HumanLayer) first met Geoff at a June 2025 meetup discussing agentic coding, where Geoff "completely steals the show" presenting on ralph, cursed lang, and autonomous coding concepts.

**Proof of concept:** Huntley used Ralph to create "Cursed," a programming language described as "cursed in its lexical structure, it's cursed in how it was built, it's cursed that this is possible" -- built by running Claude in a loop for three months.

**Economics:** One engineer used Ralph on a contract valued at $50,000 USD and completed a tested, reviewed MVP for approximately $297 USD in API costs. The approach consumes approximately $10 per hour in compute.

**Industry adoption:** Y Combinator startups embraced Ralph. Boris Cherny, Claude Code's creator, confirmed using the technique. Anthropic created an official Ralph Wiggum Plugin for Claude Code.

---

## 2. The Core Loop

### The Purest Form

From ghuntley.com/ralph:
> "Ralph is a technique. In its purest form, Ralph is a Bash loop."

```bash
while :; do cat PROMPT.md | claude-code ; done
```

That's it. Everything else is refinement.

### How One Iteration Works

1. Bash loop pipes `PROMPT.md` (or `CLAUDE.md`) into the AI agent
2. Agent reads its instructions from the prompt
3. Agent reads `prd.json` (or `IMPLEMENTATION_PLAN.md`) to find pending work
4. Agent reads `progress.txt` for learnings from previous iterations
5. Agent picks ONE task (highest priority where `passes: false`)
6. Agent implements that single task
7. Agent runs quality checks (typecheck, tests, lint)
8. If checks pass: agent commits, updates prd.json to `passes: true`, appends to progress.txt
9. Agent exits (context is destroyed)
10. Loop restarts with a completely fresh agent instance
11. New agent reads the SAME prompt but sees updated files on disk
12. Repeat until all tasks have `passes: true`

### Stop Condition

From snarktank/ralph README:
> "When all stories have `passes: true`, Ralph outputs `<promise>COMPLETE</promise>` and the loop exits."

---

## 3. Key Insight: Context Rot and Stateless Resampling

This is the foundational insight that makes Ralph work.

### The Problem: Context Rot

> "Context rot is when the longer you go, the stupider the output."

Standard agent loops suffer from context accumulation. Every failed attempt stays in the conversation history. After a few iterations, the model must process a long history of noise before it can focus on the task. Context windows fill up, quality degrades, and the AI starts making increasingly poor decisions.

### The Solution: Stateless Resampling

> "The core innovation of the Wiggum pattern involves a technique called stateless resampling. Instead of maintaining a growing conversation history that eventually leads to context rot, the system resets the context window for every iteration."

**Key principles:**
- Each iteration spawns a NEW AI instance with CLEAN context
- The only memory between iterations is on DISK (git history, progress.txt, prd.json)
- Context is DISPOSABLE -- treat it as scratch space, not permanent memory
- State persists in FILES, not in the AI's context window
- "Progress doesn't persist in the LLM's context window -- it lives in your files and git history"

### Context Window Economics

From Geoffrey Huntley's playbook:
- Typical 200K token context is approximately 176K usable tokens
- ~40-60% represents optimal "smart zone"
- Tight task scope + one task per loop = 100% smart zone utilization
- Use main agent as scheduler; spawn subagents for expensive work
- Subagents get ~156kb garbage-collected memory each

### Why Not Exit-Hook Plugins?

> "Unlike exit-hook approaches that force continuous sessions (causing context overflow and quality degradation), Ralph terminates cleanly between tasks. This prevents the 'lossy compaction' problem where AI gets confused by stale reasoning."

The Anthropic official plugin uses a stop-hook approach (loop happens inside the session). The original bash loop approach terminates and restarts cleanly between tasks, which some practitioners prefer for avoiding context degradation.

---

## 4. File Structure (Canonical)

### snarktank/ralph (Ryan Carson's Implementation)

```
project-root/
├── scripts/ralph/
│   ├── ralph.sh              # The bash loop that spawns fresh AI instances
│   ├── prompt.md             # Prompt template for Amp
│   ├── CLAUDE.md             # Prompt template for Claude Code
│   ├── prd.json              # User stories with passes status (the task list)
│   ├── prd.json.example      # Example PRD format for reference
│   ├── progress.txt          # Append-only learnings for future iterations
│   ├── .last-branch          # Tracks current branch for archiving
│   ├── archive/              # Archived previous runs
│   └── skills/               # Amp/Claude skills (prd, ralph)
├── AGENTS.md                 # Project-wide discovered patterns
└── flowchart/                # Interactive visualization
```

### Geoffrey Huntley's Playbook Structure

```
project-root/
├── loop.sh                    # Ralph loop script
├── PROMPT_build.md           # Build mode instructions
├── PROMPT_plan.md            # Plan mode instructions
├── AGENTS.md                 # Operational guide (loaded each iteration)
├── IMPLEMENTATION_PLAN.md    # Prioritized task list (replaces prd.json)
├── specs/                    # Requirement specs
│   ├── [jtbd-topic-a].md
│   └── [jtbd-topic-b].md
├── src/                      # Application source code
└── src/lib/                  # Shared utilities & components
```

### Key File Purposes

| File | Purpose | Persistence | Mutability |
|------|---------|-------------|------------|
| `prompt.md` / `CLAUDE.md` | Static instructions fed to agent each iteration | Permanent | NEVER changes during loop |
| `prd.json` / `IMPLEMENTATION_PLAN.md` | Task list with completion status | Permanent | Agent updates `passes` field |
| `progress.txt` | Append-only learnings across iterations | Permanent | Append-only (never replace) |
| `AGENTS.md` | Discovered codebase patterns | Permanent | Agent adds reusable patterns |
| `ralph.sh` / `loop.sh` | Loop runner script | Permanent | Human modifies for config |
| `.last-branch` | Previous branch tracking for archiving | Ephemeral | Auto-updated |

---

## 5. prd.json Format

### Canonical Example (from snarktank/ralph prd.json.example)

```json
{
  "project": "MyApp",
  "branchName": "ralph/task-priority",
  "description": "Task Priority System - Add priority levels to tasks",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority field to database",
      "description": "As a developer, I need to store task priority so it persists across sessions.",
      "acceptanceCriteria": [
        "Add priority column to tasks table: 'high' | 'medium' | 'low' (default 'medium')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display priority indicator on task cards",
      "description": "As a user, I want to see task priority at a glance.",
      "acceptanceCriteria": [
        "Each task card shows colored priority badge (red=high, yellow=medium, gray=low)",
        "Priority visible without hovering or clicking",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Add priority selector to task edit",
      "description": "As a user, I want to change a task's priority when editing it.",
      "acceptanceCriteria": [
        "Priority dropdown in task edit modal",
        "Shows current priority as selected",
        "Saves immediately on selection change",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter tasks by priority",
      "description": "As a user, I want to filter the task list to see only high-priority items.",
      "acceptanceCriteria": [
        "Filter dropdown with options: All | High | Medium | Low",
        "Filter persists in URL params",
        "Empty state message when no tasks match filter",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Key Fields

- **`project`**: Project name
- **`branchName`**: Git branch for this feature (ralph creates/checks out this branch)
- **`description`**: Feature description
- **`userStories[]`**: Array of tasks
  - **`id`**: Unique identifier (US-001, US-002, etc.)
  - **`title`**: Short descriptive title
  - **`description`**: User story format ("As a ..., I want ...")
  - **`acceptanceCriteria`**: Array of specific, testable criteria
  - **`priority`**: Numeric priority (1 = highest, agent picks lowest number first)
  - **`passes`**: Boolean -- `false` means pending, `true` means completed
  - **`notes`**: Agent can add notes about implementation details

### Story Sizing Rules

From the README:
> "Each PRD item should be small enough to complete in one context window."

**Right-sized stories:**
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

**Too big (split these):**
- "Build the entire dashboard"
- "Add authentication"
- "Refactor the API"

### Adjustable Mid-Flight

From aihero.dev tips:
> "Reset `passes` to false with new notes, or add missing features even while Ralph runs."

---

## 6. prompt.md / CLAUDE.md Authoring

### The Static Prompt (snarktank/ralph CLAUDE.md -- verbatim)

```markdown
## Your Task

1. Read the PRD at `prd.json` (in the same directory as this file)
2. Read the progress log at `progress.txt` (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it out or create from main.
4. Pick the **highest priority** user story where `passes: false`
5. Implement that single user story
6. Run quality checks (e.g., typecheck, lint, test - use whatever your project requires)
7. Update CLAUDE.md files if you discover reusable patterns (see below)
8. If checks pass, commit ALL changes with message: `feat: [Story ID] - [Story Title]`
9. Update the PRD to set `passes: true` for the completed story
10. Append your progress to `progress.txt`

## Progress Report Format

APPEND to progress.txt (never replace, always append):

## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered (e.g., "this codebase uses X for Y")
  - Gotchas encountered (e.g., "don't forget to update Z when changing W")
  - Useful context (e.g., "the evaluation panel is in component X")
---

## Consolidate Patterns

If you discover a **reusable pattern** that future iterations should know, add it to
the `## Codebase Patterns` section at the TOP of progress.txt (create it if it doesn't
exist). This section should consolidate the most important learnings.

Only add patterns that are **general and reusable**, not story-specific details.

## Update CLAUDE.md Files

Before committing, check if any edited files have learnings worth preserving in nearby
CLAUDE.md files.

**Examples of good CLAUDE.md additions:**
- "When modifying X, also update Y to keep them in sync"
- "This module uses pattern Z for all API calls"
- "Tests require the dev server running on PORT 3000"

**Do NOT add:**
- Story-specific implementation details
- Temporary debugging notes
- Information already in progress.txt

## Quality Requirements

- ALL commits must pass your project's quality checks (typecheck, lint, test)
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns

## Browser Testing (If Available)

For any story that changes UI, verify it works in the browser if you have browser
testing tools configured.

## Stop Condition

After completing a user story, check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:
<promise>COMPLETE</promise>

If there are still stories with `passes: false`, end your response normally
(another iteration will pick up the next story).

## Important

- Work on ONE story per iteration
- Commit frequently
- Keep CI green
- Read the Codebase Patterns section in progress.txt before starting
```

### Geoffrey Huntley's Advanced Prompt Structure

Huntley uses TWO separate prompts for two modes:

#### PROMPT_plan.md (Planning Mode)

**Phase 0 (Orientation):**
- Study specs with up to 250 parallel Sonnet subagents
- Study `IMPLEMENTATION_PLAN.md` if present
- Study `src/lib/*` with up to 250 subagents
- Reference application source in `src/*`

**Phase 1 (Analysis & Planning):**
- Compare specs against existing code (gap analysis)
- Use up to 500 Sonnet subagents for searches/reads
- Use Opus subagent for analysis and prioritization
- Create/update `IMPLEMENTATION_PLAN.md` sorted by priority
- **Critical:** "Don't assume functionality is missing; confirm with code search first"
- Plan only -- do NOT implement

#### PROMPT_build.md (Building Mode)

**Phase 0 (Orientation):**
- Study specs with up to 500 parallel Sonnet subagents
- Study `IMPLEMENTATION_PLAN.md`

**Phase 1 (Task Selection & Investigation):**
- Follow `IMPLEMENTATION_PLAN.md`, choose most important item
- Search codebase before making changes
- Use up to 500 Sonnet subagents for searches/reads
- Only 1 Sonnet subagent for build/tests
- Opus subagents for complex reasoning

**Phase 2 (Implementation):**
- Implement per specifications
- Run tests after changes
- Update `IMPLEMENTATION_PLAN.md` with findings

**Phase 3 (Validation & Commit):**
- When tests pass: update plan, stage, commit, push
- Create git tags incrementing from 0.0.0

### Prompt Authoring Best Practices

From Anthropic's official plugin README:

**1. Clear Completion Criteria**

Bad: "Build a todo API and make it good."

Good:
```markdown
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README with API docs
- Output: <promise>COMPLETE</promise>
```

**2. Incremental Goals**

Bad: "Create a complete e-commerce platform."

Good:
```markdown
Phase 1: User authentication (JWT, tests)
Phase 2: Product catalog (list/search, tests)
Phase 3: Shopping cart (add/remove, tests)

Output <promise>COMPLETE</promise> when all phases done.
```

**3. Self-Correction**

Bad: "Write code for feature X."

Good:
```markdown
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Refactor if needed
6. Repeat until all green
7. Output: <promise>COMPLETE</promise>
```

**4. Escape Hatches**

Always use `--max-iterations` as a safety net:
```bash
/ralph-loop "Try to implement feature X" --max-iterations 20
```

In prompt, include what to do if stuck:
```markdown
After 15 iterations, if not complete:
- Document what's blocking progress
- List what was attempted
- Suggest alternative approaches
```

### Huntley's Key Language Patterns

Specific phrasing from the official playbook:
- "study" (not "read" or "look at")
- "don't assume not implemented"
- "using parallel subagents" / "up to N subagents"
- "only 1 subagent for build/tests"
- "Ultrathink" (for deep reasoning)
- "capture the why"
- "keep it up to date"
- "if functionality is missing then it's your job to add it"
- "resolve them or document them"

### Critical Prompt Rules

From Huntley's playbook PROMPT_build.md:
- "Implement functionality completely. Placeholders and stubs waste efforts"
- "When authoring documentation, capture the why"
- "Single sources of truth, no migrations/adapters"
- "Keep IMPLEMENTATION_PLAN.md current with learnings"
- "Keep AGENTS.md operational only"

---

## 7. progress.txt: Filesystem Memory

### Purpose

progress.txt is the agent's ONLY persistent memory between iterations. It survives context reset. Each iteration reads it for context and appends new learnings.

### Structure

```
## Codebase Patterns
- Use `sql<number>` template for aggregations
- Always use `IF NOT EXISTS` for migrations
- Export types from actions.ts for UI components

---

## [Date/Time] - [Story ID]
Thread: https://ampcode.com/threads/$AMP_CURRENT_THREAD_ID
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered
  - Gotchas encountered
  - Useful context
---

## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - ...
---
```

### Key Rules

1. **APPEND-ONLY** -- never replace, always append
2. **Codebase Patterns section at TOP** -- consolidated reusable patterns
3. **Include thread URL** -- so future iterations can reference previous work
4. **Learnings section is critical** -- helps future iterations avoid repeating mistakes
5. **Delete when sprint ends** -- it's session-specific documentation, not permanent record

From aihero.dev:
> "AI agents are like super-smart experts who forget everything between tasks." progress.txt solves this.

### What Goes In progress.txt

- Tasks completed in this session
- Decisions made and reasoning
- Blockers encountered
- Files changed
- PRD item references
- Architectural notes for future iterations

### Why Commits Also Matter

From aihero.dev:
> "Each feature gets its own commit, providing clean git history, diff capability, and rollback points. This combination of progress file plus git history gives Ralph full context without token waste."

---

## 8. AGENTS.md: Discovered Patterns

### Purpose

From snarktank/ralph README:
> "After each iteration, Ralph updates the relevant AGENTS.md files with learnings. This is key because AI coding tools automatically read these files, so future iterations (and future human developers) benefit from discovered patterns, gotchas, and conventions."

### What to Add

**Good AGENTS.md additions:**
- "When modifying X, also update Y to keep them in sync"
- "This module uses pattern Z for all API calls"
- "Tests require the dev server running on PORT 3000"
- "Field names must match the template exactly"
- Patterns discovered ("this codebase uses X for Y")
- Gotchas ("do not forget to update Z when changing W")
- Useful context ("the settings panel is in component X")

**Do NOT add:**
- Story-specific implementation details
- Temporary debugging notes
- Information already in progress.txt

### Key Distinction from progress.txt

- **progress.txt** = iteration-specific notes, task logs, story-specific details
- **AGENTS.md** = general, reusable patterns that apply to ALL future work in that directory

### Huntley's View on AGENTS.md

From the playbook:
> "Keep AGENTS.md operational only" -- it should contain build/test commands, validation approaches, and discovered patterns. Status updates belong in IMPLEMENTATION_PLAN.md.

---

## 9. ralph.sh: The Loop Runner

### snarktank/ralph Implementation (Complete Script)

```bash
#!/bin/bash
# Ralph Wiggum - Long-running AI agent loop
# Usage: ./ralph.sh [--tool amp|claude] [max_iterations]

set -e

# Parse arguments
TOOL="amp"
MAX_ITERATIONS=10

while [[ $# -gt 0 ]]; do
  case $1 in
    --tool)
      TOOL="$2"
      shift 2
      ;;
    --tool=*)
      TOOL="${1#*=}"
      shift
      ;;
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        MAX_ITERATIONS="$1"
      fi
      shift
      ;;
  esac
done

if [[ "$TOOL" != "amp" && "$TOOL" != "claude" ]]; then
  echo "Error: Invalid tool '$TOOL'. Must be 'amp' or 'claude'."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRD_FILE="$SCRIPT_DIR/prd.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"
ARCHIVE_DIR="$SCRIPT_DIR/archive"
LAST_BRANCH_FILE="$SCRIPT_DIR/.last-branch"

# Archive previous run if branch changed
if [ -f "$PRD_FILE" ] && [ -f "$LAST_BRANCH_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || echo "")

  if [ -n "$CURRENT_BRANCH" ] && [ -n "$LAST_BRANCH" ] && [ "$CURRENT_BRANCH" != "$LAST_BRANCH" ]; then
    DATE=$(date +%Y-%m-%d)
    FOLDER_NAME=$(echo "$LAST_BRANCH" | sed 's|^ralph/||')
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$DATE-$FOLDER_NAME"

    echo "Archiving previous run: $LAST_BRANCH"
    mkdir -p "$ARCHIVE_FOLDER"
    [ -f "$PRD_FILE" ] && cp "$PRD_FILE" "$ARCHIVE_FOLDER/"
    [ -f "$PROGRESS_FILE" ] && cp "$PROGRESS_FILE" "$ARCHIVE_FOLDER/"
    echo "  Archived to: $ARCHIVE_FOLDER"

    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
  fi
fi

# Track current branch
if [ -f "$PRD_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  if [ -n "$CURRENT_BRANCH" ]; then
    echo "$CURRENT_BRANCH" > "$LAST_BRANCH_FILE"
  fi
fi

# Initialize progress file if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Progress Log" > "$PROGRESS_FILE"
  echo "Started: $(date)" >> "$PROGRESS_FILE"
  echo "---" >> "$PROGRESS_FILE"
fi

echo "Starting Ralph - Tool: $TOOL - Max iterations: $MAX_ITERATIONS"

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "==============================================================="
  echo " Ralph Iteration $i of $MAX_ITERATIONS ($TOOL)"
  echo "==============================================================="

  if [[ "$TOOL" == "amp" ]]; then
    OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | amp --dangerously-allow-all 2>&1 | tee /dev/stderr) || true
  else
    OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/CLAUDE.md" 2>&1 | tee /dev/stderr) || true
  fi

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "Ralph completed all tasks!"
    echo "Completed at iteration $i of $MAX_ITERATIONS"
    exit 0
  fi

  echo "Iteration $i complete. Continuing..."
  sleep 2
done

echo ""
echo "Ralph reached max iterations ($MAX_ITERATIONS) without completing all tasks."
echo "Check $PROGRESS_FILE for status."
exit 1
```

### Geoffrey Huntley's Enhanced Loop Script

Huntley's version accepts mode selection:

```bash
./loop.sh              # Build mode, unlimited
./loop.sh 20           # Build mode, max 20 iterations
./loop.sh plan         # Plan mode, unlimited
./loop.sh plan 5       # Plan mode, max 5 iterations
```

**Claude CLI flags used:**
- `-p` (headless): Non-interactive, reads from stdin
- `--dangerously-skip-permissions`: Auto-approve all tool calls
- `--output-format=stream-json`: Structured output for logging
- `--model opus`: Primary agent for complex reasoning
- `--verbose`: Detailed execution logging

### Key Differences Between Implementations

| Feature | snarktank/ralph | Huntley playbook |
|---------|----------------|------------------|
| Task format | prd.json (JSON) | IMPLEMENTATION_PLAN.md (Markdown) |
| Modes | Single mode | Plan mode + Build mode |
| Subagents | Not used | Up to 500 parallel Sonnet subagents |
| Archiving | Automatic on branch change | Manual |
| Skills | PRD + Ralph skills for Amp/Claude | N/A |
| Tools | Amp or Claude Code | Claude Code primarily |

---

## 10. Backpressure and Feedback Loops

### Geoffrey Huntley on Backpressure (ghuntley.com/pressure)

> "If you aren't capturing your back-pressure then you are failing as a software engineer."

> "Back pressure for agents refers to automated quality feedback that enables agents to identify errors as they work."

Back pressure requires calibration: "just enough" to reject invalid outputs, but excessive resistance creates bottlenecks. It's "part art, part engineering and a whole bung of performance engineering."

### Types of Feedback Loops (from aihero.dev)

| Mechanism | Catches |
|-----------|---------|
| TypeScript types | Type mismatches, missing props |
| Unit tests | Broken logic, regressions |
| Playwright MCP | UI bugs, broken interactions |
| ESLint/linting | Code style, potential bugs |
| Pre-commit hooks | Blocks bad commits entirely |

### Implementation

From snarktank/ralph README:
> "Ralph only works if there are feedback loops: Typecheck catches type errors. Tests verify behavior. CI must stay green (broken code compounds across iterations)."

Best practice: Block commits unless everything passes. Ralph cannot declare victory with red tests.

From prompt templates, include explicit requirements:
```
TypeScript: `npm run typecheck` (must pass)
Tests: `npm run test` (must pass)
Lint: `npm run lint` (must pass)
Do NOT commit if any fails.
```

### Guardrails (Escape Hatches)

From aihero.dev tips:
> "Add guardrails to PROMPT.md if you notice patterns Ralph might get wrong, such as: If tests fail 3 times on the same issue, STOP and output: STUCK."

From the official plugin:
> "Always use `--max-iterations` as a safety net to prevent infinite loops on impossible tasks."

From Huntley's playbook:
- Ctrl+C stops the loop
- `git reset --hard` reverts uncommitted changes
- Regenerate plan if trajectory goes wrong

---

## 11. Geoffrey Huntley's Advanced Playbook

### Source: github.com/ghuntley/how-to-ralph-wiggum

### Three Phases, Two Prompts, One Loop

**Phase 1: Define Requirements** - LLM conversation to identify Jobs to Be Done (JTBD) and create requirement specs

**Phase 2: Planning Mode** - Gap analysis comparing specifications against existing code, generating prioritized implementation tasks

**Phase 3: Building Mode** - Autonomous implementation of tasks from the plan, with tests providing backpressure

### Core Architecture Principles

**Context Is Everything:**
- 200K token context is approximately 176K usable
- ~40-60% represents optimal "smart zone"
- Tight task scope + one task per loop = 100% smart zone utilization
- Main agent as scheduler; subagents for expensive work

**Steering Ralph -- Upstream:**
- Allocate first ~5,000 tokens for specifications
- Ensure deterministic setup with consistent context files per loop
- Existing codebase patterns shape what Ralph generates

**Steering Ralph -- Downstream:**
- Create backpressure via tests, typechecks, lints, builds
- AGENTS.md specifies project-specific validation commands
- LLM-as-judge tests provide backpressure for subjective criteria

**Let Ralph Ralph:**
- Lean into LLM's self-identification and self-correction abilities
- Eventual consistency achieved through iteration
- Observe failure patterns and adjust reactively
- The plan is disposable -- regenerate when needed

**Move Outside the Loop:**
- Ralph should do ALL work, including task selection
- Your role: sit on the loop, not in it
- Engineer the setup and environment for Ralph's success
- "Tune like a guitar -- observe and adjust reactively"

### Building Mode Workflow (10 Steps)

1. **Orient** -- Subagents study specs
2. **Read plan** -- Study IMPLEMENTATION_PLAN.md
3. **Select** -- Pick most important task
4. **Investigate** -- Study relevant source code
5. **Implement** -- N subagents for file operations
6. **Validate** -- 1 subagent for build/tests (backpressure)
7. **Update plan** -- Mark task done, note discoveries
8. **Update AGENTS.md** -- If operational learnings
9. **Commit** -- Push changes
10. **Loop ends** -- Context cleared, next iteration starts fresh

### When to Regenerate the Plan

- Ralph is implementing wrong things or duplicating work
- Plan feels stale or doesn't match current state
- Too much clutter from completed items
- You've made significant spec changes
- You're confused about what's actually done

Cost is one Planning loop -- cheap compared to Ralph circling.

### Topic Scope Test

> "Can you describe it in one sentence without conjoining unrelated capabilities? If you need 'and,' it's probably multiple topics."

### Security & Sandboxing

**Ralph requires `--dangerously-skip-permissions`:**
- Bypasses all permission prompts for fully autonomous operation
- This requires sandboxing as your only security boundary

From Huntley:
> "It's not if it gets popped, it's when. What is the blast radius?"

**Running safely:**
- Only provide API keys and deploy keys needed for the task
- No access to private data beyond requirements
- Restrict network connectivity where possible
- Options: Docker sandboxes (local), Fly Sprites/E2B (remote/production)

---

## 12. Anthropic's Official Plugin

### Source: github.com/anthropics/claude-code/plugins/ralph-wiggum

### Different Approach: Stop Hook (Not Bash Loop)

The official plugin uses a STOP HOOK that intercepts Claude's exit attempts:

```bash
# You run ONCE:
/ralph-loop "Your task description" --completion-promise "DONE"

# Then Claude Code automatically:
# 1. Works on the task
# 2. Tries to exit
# 3. Stop hook blocks exit
# 4. Stop hook feeds the SAME prompt back
# 5. Repeat until completion
```

The loop happens INSIDE your current session. The stop hook in `hooks/stop-hook.sh` creates the self-referential feedback loop by blocking normal session exit.

### Commands

- `/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"` -- Start loop
- `/cancel-ralph` -- Cancel active loop

### Key Difference from Bash Loop

The plugin keeps the SAME session running (with stop hooks preventing exit), while the bash loop TERMINATES and RESTARTS with a fresh context each iteration. Some practitioners prefer the bash approach for avoiding context degradation in very long sessions.

### Real-World Results

From the plugin README:
- Successfully generated 6 repositories overnight in Y Combinator hackathon testing
- One $50k contract completed for $297 in API costs
- Created entire programming language ("cursed") over 3 months using this approach

---

## 13. Best Practices and Anti-Patterns

### From aihero.dev "11 Tips"

**1. Start with HITL, Then Go AFK**
- HITL (Human-in-the-Loop): Run once, watch, intervene when needed. Best for learning.
- AFK (Away From Keyboard): Run in a loop with capped iterations. Best for bulk work.
- "Learn with HITL, then transition to AFK once your prompt is solid."

**2. Prioritize Risky Tasks First**
Ralph defaults to easy tasks first. Instead, guide it to tackle hard problems:
1. Architectural decisions and core abstractions
2. Integration points between modules
3. Unknown unknowns and spike work
4. Standard features and implementation
5. Polish, cleanup, and quick wins

Use HITL Ralph for risky architectural work. Deploy AFK Ralph on lower-risk tasks.

**3. Explicitly Define Software Quality**
> "The agent doesn't know if this is a throwaway prototype or production code that will be maintained for years."

| Repo Type | Instruction | Expected Behavior |
|-----------|------------|-------------------|
| Prototype | Speed over perfection | Takes shortcuts, skips edge cases |
| Production | Must be maintainable | Follows best practices, adds tests |
| Library | Backward compatibility matters | Careful about breaking changes |

**4. Your Instructions Compete With Your Codebase**
> "Agents amplify what they see. Poor code leads to poorer code."

Thousands of lines of existing code outweigh a few instruction lines. Ralph will follow poor patterns in the repo rather than written guidance.

**5. Use Docker Sandboxes for AFK**
```bash
docker sandbox run claude
```
Optional for HITL (you're watching), essential for AFK, especially overnight.

**6. The Rate of Feedback Is Your Speed Limit**
> "The rate at which you can get feedback is your speed limit."

Smaller tasks = tighter feedback loops = better code quality.

### Universal Loop Pattern

From aihero.dev:
> "Any task describable as 'examine repo, improve something, report findings' fits the Ralph pattern. Loop structure stays identical; only the prompt changes."

**Alternative loop types beyond features:**
- **Test Coverage Loop:** Find uncovered lines, write tests until target achieved
- **Duplication Loop:** Find duplicate code, refactor into shared utilities
- **Linting Loop:** Feed linting errors, fix one-by-one
- **Entropy Loop:** Scan for code smells, clean them up

### Anti-Patterns

1. **Too-large stories** -- Agent runs out of context before finishing, produces poor code
2. **No feedback loops** -- Without tests/typecheck, broken code compounds
3. **Modifying the prompt during the loop** -- Prompt must be STATIC
4. **Not capping iterations** -- Always set --max-iterations as safety
5. **Trusting inflated earnings claims about productivity** -- Start HITL, validate
6. **Skipping progress.txt** -- Future iterations repeat the same mistakes
7. **Not using git** -- Commits provide rollback and context for future iterations
8. **Multi-agent communication in the loop** -- Huntley warns against: "Consider what microservices would look like if the microservices themselves are non-deterministic -- a red hot mess"

---

## 14. The Ecosystem

### Primary Sources

| Resource | URL | Author |
|----------|-----|--------|
| Original technique | ghuntley.com/ralph | Geoffrey Huntley |
| Everything is a loop | ghuntley.com/loop | Geoffrey Huntley |
| Don't waste backpressure | ghuntley.com/pressure | Geoffrey Huntley |
| Official playbook | github.com/ghuntley/how-to-ralph-wiggum | Geoffrey Huntley |
| snarktank/ralph (most popular impl) | github.com/snarktank/ralph | Ryan Carson |
| Anthropic official plugin | github.com/anthropics/claude-code/plugins/ralph-wiggum | Anthropic |
| awesome-ralph (curated list) | github.com/snwfdhmp/awesome-ralph | Community |

### Notable Implementations

| Implementation | Stars | Key Feature |
|---------------|-------|-------------|
| snarktank/ralph | Popular | PRD-driven, Amp+Claude, skills, archiving |
| frankbria/ralph-claude-code | 463 | Intelligent exit detection, dashboard |
| ralph-orchestrator | - | Rust, 7 AI backends, TUI mode |
| vercel-labs/ralph-loop-agent | - | TypeScript SDK, multi-agent |
| mj-meyer/choo-choo-ralph | - | Beads-powered 5-phase workflow |

### Community

- **Reddit:** r/RalphCoding
- **Discord:** ralph-coding community server
- **Hacker News:** 6 major discussion threads
- **Podcast:** Dev Interrupted episode with Geoffrey Huntley

---

## 15. Key Quotes Collection

### Geoffrey Huntley

> "Ralph is a technique. In its purest form, Ralph is a Bash loop."

> "A bash loop that feeds an AI's output (errors and all) back into itself until it dreams up the correct answer."

> "That's the beauty of Ralph -- the technique is deterministically bad in an undeterministic world."

> "If you aren't capturing your back-pressure then you are failing as a software engineer."

> "Software development as a profession is effectively dead. Software engineering is more alive -- and critical -- than ever before."

> "It's not if it gets popped, it's when. What is the blast radius?"

> "Ralph can potentially replace the majority of outsourcing at most companies for greenfield projects."

> "Computers can be indeed programmed."

> "Software becomes clay on the pottery wheel."

### On Context Management

> "Context rot is when the longer you go, the stupider the output."

> "The core innovation of the Wiggum pattern involves a technique called stateless resampling."

> "Progress doesn't persist in the LLM's context window -- it lives in your files and git history."

> "Unlike exit-hook approaches that force continuous sessions (causing context overflow and quality degradation), Ralph terminates cleanly between tasks."

### On Prompt Engineering

> "The agent chooses the task, not you."

> "Sit on the loop, not in it."

> "Tune like a guitar -- observe and adjust reactively."

> "Implement functionality completely. Placeholders and stubs waste efforts."

> "Don't assume functionality is missing; confirm with code search first."

### On Quality

> "Agents amplify what they see. Poor code leads to poorer code."

> "The rate at which you can get feedback is your speed limit."

> "The agent doesn't know if this is a throwaway prototype or production code that will be maintained for years."

### On Scale

> "It might be inefficient, but for complex tasks, stubbornness is proving to be a quality all its own."

> "Dumb things can work surprisingly well, so what could we expect from a smart version?"

> "The loop is the hero, not the model."

---

## Summary: The TRUE Ralph Pattern

### What It IS:

1. A bash `while` loop that pipes a static prompt into an AI agent
2. Each iteration: fresh context, read state from files, do ONE task, write state to files, exit
3. Memory lives on disk (progress.txt, prd.json, git), NOT in context
4. Backpressure via tests/typecheck/lint prevents bad commits
5. Stories are small enough to complete in one context window
6. The prompt NEVER changes during the loop
7. The agent picks the task, not the human
8. Quality gates block bad code from accumulating

### What It Is NOT:

1. NOT a single long-running session (that causes context rot)
2. NOT multi-agent orchestration (Huntley explicitly warns against this complexity)
3. NOT a planning tool (it's an execution loop; planning happens separately)
4. NOT magic (it requires well-sized stories, good prompts, and feedback loops)
5. NOT the stop-hook approach (though Anthropic's plugin uses this variant)

### The Minimal Implementation:

```bash
# loop.sh
while :; do cat PROMPT.md | claude --dangerously-skip-permissions --print ; done
```

```markdown
# PROMPT.md
1. Read prd.json
2. Read progress.txt
3. Pick highest priority story where passes: false
4. Implement it
5. Run tests
6. If pass: commit, update prd.json, append to progress.txt
7. If ALL stories pass: output <promise>COMPLETE</promise>
```

```json
// prd.json
{
  "branchName": "ralph/feature",
  "userStories": [
    {
      "id": "US-001",
      "title": "Task title",
      "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
      "priority": 1,
      "passes": false
    }
  ]
}
```

```
# progress.txt (starts empty, grows via append)
## Codebase Patterns
- Pattern 1
- Pattern 2
---
## 2026-02-05 - US-001
- Implemented X
- Learned Y
---
```

That's the pattern. Everything else is enhancement.

---

## Sources

- [snarktank/ralph GitHub](https://github.com/snarktank/ralph) -- Ryan Carson's structured implementation
- [ghuntley.com/ralph](https://ghuntley.com/ralph/) -- Geoffrey Huntley's original technique
- [ghuntley/how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum) -- Official playbook
- [Anthropic Claude Code Ralph Plugin](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md) -- Official Anthropic implementation
- [The Register Article (Jan 27, 2026)](https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/) -- "Ralph Wiggum prompts Claude to vibe-clone software"
- [HumanLayer: Brief History of Ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph) -- Timeline and context
- [Dev Interrupted Podcast](https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator) -- Geoffrey Huntley interview
- [aihero.dev: 11 Tips](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum) -- Practical best practices
- [awesome-ralph](https://github.com/snwfdhmp/awesome-ralph) -- Curated ecosystem list
- [ghuntley.com/loop](https://ghuntley.com/loop/) -- "Everything is a Ralph Loop"
- [ghuntley.com/pressure](https://ghuntley.com/pressure/) -- "Don't Waste Your Back Pressure"
- [ralph-wiggum.ai](https://ralph-wiggum.ai/) -- Simplified overview
