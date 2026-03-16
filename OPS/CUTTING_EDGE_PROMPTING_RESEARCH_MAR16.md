# CUTTING-EDGE LLM PROMPTING & META-COGNITION RESEARCH
## March 16, 2026 — Competitive Intelligence Brief

---

## 1. BEST CLAUDE.md / SYSTEM PROMPT PATTERNS (State of the Art)

### The "Under 60 Lines" Rule
HumanLayer keeps their CLAUDE.md under 60 lines. Over 80 lines, Claude starts ignoring portions. Over 200 lines, you're actively degrading performance. If Claude already does something correctly without the instruction, DELETE IT or convert it to a hook.

### Hierarchy (Three-Tier Loading)
```
~/.claude/CLAUDE.md          → Global personal preferences (loads first, lowest priority)
.claude/CLAUDE.md             → Project-level shared with team
.claude/local.md              → Local personal overrides (highest priority)
.claude/rules/*.md            → Auto-loaded, same priority as project CLAUDE.md
subdirectory/CLAUDE.md        → On-demand, only when working in that directory
```

### Path-Scoped Rules (On-Demand Context Injection)
```yaml
# .claude/rules/api-rules.md
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API routes MUST validate input with zod schemas
- NEVER return raw database objects — use DTOs
- All errors MUST use the AppError class from src/utils/errors.ts
```
These ONLY load when Claude touches files matching the glob. This is how you keep CLAUDE.md lean while having deep domain rules.

### The "4-Block Contract" Pattern (Best System Prompts)
```
INSTRUCTIONS — What you are, what you do, your constraints
CONTEXT — Project state, architecture, conventions
TASK — Current objective with acceptance criteria
OUTPUT FORMAT — Exact structure of expected deliverable
```

### What Goes in CLAUDE.md vs Hooks vs Rules
| CLAUDE.md | Hooks | Rules Directory |
|-----------|-------|----------------|
| Behavioral guidance | Actions that MUST happen every time | Domain-specific patterns |
| Judgment-based rules | Linting, formatting | Path-scoped expertise |
| Project overview | Blocking dangerous commands | Module-level conventions |
| Common commands | Logging, backups | Team standards |

### High-Impact CLAUDE.md Patterns
```markdown
# CRITICAL RULES (use sparingly — if everything is IMPORTANT, nothing is)
IMPORTANT: Never modify the migrations folder directly.
YOU MUST run tests before committing.

# Pointers, Not Copies
- Don't paste code into CLAUDE.md — it goes stale
- Reference file paths: "See src/utils/errors.ts for error handling patterns"

# Negative Instructions (what NOT to do)
- NEVER use console.log for debugging — use the logger from src/utils/logger
- NEVER create new dashboard scripts — use OPS/control_panel.py
- NEVER import directly from node_modules internals

# Verification Requirements
- After ANY file change, run: npm run typecheck
- Before committing: npm test -- --bail
```

### File Imports with @-syntax
```markdown
# CLAUDE.md
@.claude/rules/coding-standards.md
@.claude/rules/testing-requirements.md
```
Referenced files are expanded inline at load time (NOT lazily). Paths resolve relative to the CLAUDE.md containing the import.

---

## 2. META-COGNITIVE PROMPTING FRAMEWORKS

### MIT Recursive Meta-Cognition (110% improvement over standard prompting)
Developed at MIT CSAIL (January 2026). Instead of one linear thought process, the model simulates a **collaborative team of experts** with iterative self-reflection.

**Implementation Pattern:**
```
Step 1: DECOMPOSE — Break the problem into sub-components
Step 2: MULTI-PERSPECTIVE — Generate solutions from 3+ expert viewpoints
Step 3: EVALUATE — Each "expert" critiques the others' approaches
Step 4: SYNTHESIZE — Merge the strongest elements into a unified solution
Step 5: META-REFLECT — Evaluate the synthesis process itself for blind spots
Step 6: ITERATE — Repeat steps 3-5 until convergence
```

**Critical caveat:** The 110% figure is for complex reasoning tasks. Recursive processes consume 3-5x more tokens. Interventions succeed in only ~22.5% of cases despite high acceptance rates. Use selectively on high-stakes decisions, not routine tasks.

### MARS Framework (Metacognitive Agent Reflective Self-improvement)
Three-phase framework that converts failures into prompt enhancements:

```
Phase 1: AGGREGATE FAILURES — Collect all errors/suboptimal outputs from recent runs
Phase 2: PRINCIPLED REFLECTION — Extract normative rules ("Always check X before Y")
Phase 3: PROCEDURAL REFLECTION — Derive step-by-step strategies from successes
→ Output: Enhanced system prompt incorporating both avoidance rules and success procedures
```

MARS achieves self-evolution in a SINGLE recurrence cycle vs. multi-turn recursive systems. Key insight: treat errors as systematic patterns, not isolated incidents.

### Metacognitive Prompting (MP) — 5-Step Process
```
1. INTERPRET — Parse the input and identify what's actually being asked
2. INITIAL JUDGMENT — Form a preliminary answer
3. CRITICAL EVALUATION — Subject the judgment to self-reflection (the metacognitive step)
4. FINAL DECISION — Finalize with explicit reasoning chain
5. CONFIDENCE ASSESSMENT — Rate confidence 0-100% with justification
```

### DSPy Framework (Stanford) — Automated Prompt Optimization
DSPy eliminates manual prompt engineering entirely. Instead of writing prompts, you:
1. Define input/output **signatures** (typed specs)
2. Select a **module** (strategy for invoking the LLM)
3. Define a **metric** (how to score success)
4. Run an **optimizer** that automatically generates the best prompt

**Key Optimizers:**
- **MIPROv2**: Bootstraps traces of good behavior, generates instructions + few-shot examples, uses Bayesian Optimization to search the prompt space
- **SIMBA**: Identifies challenging examples with high output variability, uses LLM introspection to generate self-reflective improvement rules
- **GEPA**: Reflects on program trajectory to identify what worked/didn't, proposes prompts addressing gaps

**For PRINTMAXX:** DSPy could optimize agent prompts automatically. Define metrics (completion rate, accuracy, soul-drift score) and let the optimizer find better prompts than any human could write.

---

## 3. COMPETITIVE INTELLIGENCE — WHAT THE BEST USERS DO

### The 7 Levels of Claude Code Mastery
Most users are stuck at Level 2-3. Here's the full progression:

```
Level 1: Basic prompting (90% of users)
Level 2: Plan Mode — read-only analysis before code changes
Level 3: CLAUDE.md — persistent project knowledge
Level 4: Hooks — deterministic automation (formatting, linting, guards)
Level 5: Custom Subagents — specialized AI workers with scoped tools
Level 6: Agent Teams — parallel multi-agent coordination via git
Level 7: Autonomous Pipelines — overnight runs, self-improving loops
```

### Power User Patterns That Scale
1. **Writer-Reviewer Pattern**: One Claude writes, another reviews. Chain: `generate draft → review against criteria → refine based on review`. Each step is a separate call so you can log, evaluate, or branch.

2. **Self-Correction Loop**: The most common chaining pattern. 2-3x quality improvement from adding verification.

3. **Plan Before Code**: Use Plan Mode (`/plan`) before every non-trivial change. Claude reads the codebase, asks clarifying questions, proposes a complete plan. THEN execute.

4. **Smaller Prompts Win**: Agentic coding is NOT a one-shot interaction. Smaller, focused prompts lead to better reasoning, cleaner implementations, fewer hidden assumptions.

5. **Documentation Drift Detection**: Agents scan git history to identify when code changes have rendered documentation outdated. Automated, not manual.

6. **Mistake Pattern Documentation**: After PR reviews, document mistake patterns in CLAUDE.md/AGENTS.md. Every review tightens the quality bar for future work.

7. **Subagent Specialization**: Each subagent gets its own context, system prompt, tool access, and permissions. A code-reviewer subagent only needs Read/Glob/Grep. A deployer gets Bash.

### The Self-Improving Agent Pattern (Addy Osmani)
```
After each task:
1. Log key learnings to AGENTS.md
   - "The codebase uses Library X for Y — follow that pattern"
   - "Gotcha: When updating user model, also update audit log"
2. Agent reads AGENTS.md at session start
3. Each improvement makes future improvements easier
4. The agent accumulates knowledge of what the codebase looks like
```

**This is the compound interest of AI coding.** If you have to repeat the same preference every session, you're babysitting a fast intern, not using an agent.

---

## 4. ANTI-PATTERN DETECTION — FAILURE MODES

### The 6 Deadly Anti-Patterns

**1. Context Rot**
Over long sessions, instructions from 20 minutes ago get forgotten. Solution: Intentional `/compact` at milestones, not waiting for auto-compaction.

**2. The Kitchen Sink Session**
Starting with one task, asking something unrelated, going back — filling context with irrelevant noise. Solution: One task per session, or explicit `/compact` between unrelated tasks.

**3. Infinite Retry Loop**
Claude fails at something, retries the exact same approach 5 times, burns 30 minutes. Solution: After 2 failed corrections, CLEAR context and rewrite a better initial prompt.

**4. The "Almost Right" Trap (The 80% Problem)**
66% of developers report "the 80% problem" — AI solutions that are almost right but not quite. 45% say debugging AI code takes longer than writing it themselves. Solution: Verification hooks, not trust.

**5. Reinventing the Wheel**
AI ignores battle-tested libraries and generates from-scratch implementations. Solution: Explicit CLAUDE.md rule: "ALWAYS check if an existing library handles this before writing custom code."

**6. Bloated CLAUDE.md**
Complex slash commands, bloated context windows, and write-time hooks all degrade performance. Solution: CLAUDE.md under 60 lines, move enforcement to hooks, move domain knowledge to path-scoped rules.

### The Productivity Paradox
"The mechanical work got dramatically faster, but the judgment work barely moved. More PRs per developer doesn't mean better software faster. If review times are climbing and defect rates are flat, the bottleneck moved from writing to reviewing."

### Security Blind Spot
AI coding agents keep repeating decade-old security mistakes. Security isn't part of AI agents' default thinking — they miss adding authentication logic, create security flaws, and skip input validation. Solution: Security audit hooks that run after every code generation.

---

## 5. PERSISTENT IMPROVEMENT ARCHITECTURE

### The Compaction-to-Memory Bridge (Infinite Context)
```
PreCompact Hook fires →
  1. Chunk conversation turns
  2. Summarize chunks
  3. Embed summaries
  4. Store in memory backend (SQLite/PostgreSQL/JSON)

SessionStart Hook fires →
  1. Query stored memory for relevant context
  2. Inject most relevant archived context into new session
```
No monkey-patching required. Uses official PreCompact and SessionStart hooks. Reduces critical information loss by 30% during compactions.

### Session Memory Hierarchy
```
CLAUDE.md files     → ALWAYS survive compaction (re-read from disk)
Auto memory         → Accumulates learnings from corrections/preferences
Session memory      → Cross-session persistence via compaction summaries
Path-scoped rules   → On-demand injection based on file access patterns
Skills              → Loaded dynamically when task matches
```

### The Compound Learning Loop
```
Session N:
  1. Agent works on task
  2. Makes mistake X
  3. User corrects mistake X
  4. Correction logged to auto memory OR explicitly added to CLAUDE.md/AGENTS.md

Session N+1:
  1. Agent reads updated memory
  2. Mistake X never happens again
  3. Agent discovers mistake Y
  4. Cycle continues

Session N+100:
  → Agent has accumulated 100 learned corrections
  → Each correction prevents future errors
  → Compounding improvement with zero repeated instruction
```

### PreCompact Hook (Preserve Critical Context)
```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "command": "python3 scripts/save_context_snapshot.py"
      }
    ]
  }
}
```
The "auto" matcher ensures snapshots only happen on automatic compaction, not manual.

---

## 6. THE "EDGE" REASONING FRAMEWORKS

### Chain-of-Thought vs Tree-of-Thought vs Graph-of-Thought

| Method | Best For | How It Works | Token Cost |
|--------|----------|-------------|------------|
| **CoT** | Sequential reasoning | Linear step-by-step | 1x |
| **ToT** | Exploration + backtracking | Branch at decision points, prune bad paths | 3-5x |
| **GoT** | Complex multi-dimensional problems | Arbitrary graph connections between thoughts | 5-10x |

**2026 Verdict:** GoT surpasses CoT and ToT by allowing reasoning nodes to have multiple parents (aggregation). But CoT is sufficient for 80% of tasks. Use ToT for problems requiring exploration. Use GoT only for genuinely complex synthesis tasks.

**For PRINTMAXX:** CoT for routine agent tasks. ToT for strategic decisions (venture selection, alpha evaluation). GoT is overkill for this use case.

### Self-Reflection Prompting (Draft-Critique-Rewrite)
MIT testing showed accuracy jump from 80% to 91% with this pattern.

**Exact Template:**
```
You are a {creator_role}.

Task 1 (Draft): Write a {deliverable} for {audience}. Include {key_elements}.

Task 2 (Self-Review): Now act as a {critic_role}. Identify the top {5} issues, specifically: {flaw_types}.

Task 3 (Improve): Rewrite the {deliverable} as the final version, fixing every issue you listed.

Output both: {final_version} + {a short change log}.
```

### Constitutional AI Self-Correction
The model critiques its own output guided by randomly chosen principles from a "constitution":
```
Constitution Example:
1. Outputs must be actionable, not theoretical
2. Every claim must have a verification method
3. Prefer existing tools over custom implementations
4. Security considerations must be addressed explicitly
5. Edge cases must be enumerated, not ignored
```

The model generates → critiques against a random principle → revises → critiques against another principle → revises again.

### Reflexion Framework
```
1. Actor generates output
2. Evaluator scores the output against objectives
3. Self-Reflection module analyzes the gap between desired and actual
4. Reflective feedback is stored in episodic memory
5. Actor retries with access to reflection history
6. Loop until quality threshold met OR max iterations
```

### Adversarial Verification Pattern
```
Agent A: Generate solution
Agent B: Red-team the solution — find every flaw
Agent A: Address all flagged issues
Agent B: Verify fixes, flag remaining issues
→ Iterate until Agent B finds zero critical issues
```

---

## 7. WHAT POWER USERS AUTOMATE

### The 10 Automations That Separate Levels 5-7

1. **PR Review as Agent Training** — Every PR review finding gets appended to CLAUDE.md/AGENTS.md. Review process itself improves the agent.

2. **PreCompact Context Snapshots** — Never lose critical information during auto-compaction.

3. **PostToolUse Auto-Formatting** — `black`, `prettier`, `rustfmt` run automatically after every file write.

4. **PostToolUse Command Logging** — Every bash command Claude runs gets logged: `jq -r '.tool_input.command' >> ~/.claude/command-log.txt`

5. **PreToolUse Safety Guards** — Block destructive operations (rm -rf, DROP TABLE, force push) with exit code 2.

6. **Git Auto-Backup Before Big Changes** — PreToolUse hook creates a temporary commit before Claude makes large changes.

7. **Documentation Drift Scanning** — Automated git history analysis to flag when docs are outdated.

8. **Overnight Pipeline Runs** — claude -p with structured prompts running cron jobs that produce finished work by morning.

9. **Headless CI/CD Integration** — Claude reviews PRs, generates changelogs, updates docs, triages issues — all in headless mode.

10. **Self-Improving AGENTS.md** — After each task, agent appends discovered patterns for future iterations.

### Skills Architecture (The New Frontier)
```
.claude/skills/
  skill-name/
    SKILL.md          (required — YAML frontmatter + instructions)
    scripts/           (executable code)
    references/        (docs loaded into context)
    assets/            (files used in output)
```
Skills are discovered automatically by task matching. 1,234+ community skills available covering everything from AWS CloudFormation to product thinking to multilingual documentation.

### Agent Teams (Opus 4.6 Feature)
```
Lead Agent: Understands overall task, decomposes into subtasks
  ├── Subagent A: Backend implementation (Bash, Write tools)
  ├── Subagent B: Test writing (Read, Write tools)
  ├── Subagent C: Code review (Read, Glob, Grep tools)
  └── Subagent D: Documentation (Read, Write tools)

Coordination: Git-based task claiming via text files in current_tasks/
Best Practice: 3-5 teammates, 5-6 tasks each, NO same-file edits
```
Anthropic used 16 agents to build a 100,000-line Rust C compiler over 2,000 sessions.

---

## 8. FUTURE-PROOFING — WHAT'S COMING

### Already Shipped (Feb-Mar 2026)
- **Opus 4.6**: 1M token context, 14.5-hour task completion horizon, agent teams
- **Sonnet 4.6** (was "Sonnet 5"/"Fennec"): Coding surpasses Opus 4.5, 50% cheaper, Dev Team multi-agent mode
- **Agent Skills**: Modular capability bundles with dynamic loading
- **Enterprise Agents Program**: Pre-built agents for finance, legal, HR
- **Context compaction API**: Server-side summarization for "effectively infinite conversations"
- **Memory tool**: Cross-session persistence via memory API
- **Web search/fetch GA**: Dynamic filtering for better performance
- **March 2026**: /context command with actionable suggestions, memory timestamps, /loop mode, voice mode

### Coming Next
- **Claude 5** (next flagship): Leaked in Google Vertex AI logs, codename unclear, expected to dramatically advance reasoning
- **EU AI Act compliance deadline**: August 2, 2026 — high-risk AI systems need full compliance, red teaming obligations
- **Agent autonomy expansion**: Longer task horizons (14.5h already, trending toward 24h+)
- **Skills marketplace**: Community-contributed skills with quality ratings
- **Deeper MCP integration**: More third-party tool servers becoming first-class

### What to Build Now to Stay Ahead
1. **PreCompact memory bridges** — Store and retrieve context across compactions
2. **Path-scoped rules** for every venture/domain in the system
3. **Custom skills** for every repeating workflow
4. **Self-improving AGENTS.md** with automatic mistake documentation
5. **Verification hooks** on all code-generating agents
6. **Agent Teams** for parallelizable work (research, reviews, content)
7. **DSPy-style metric-driven prompt optimization** for core agent prompts
8. **Constitutional AI principles** baked into SOUL.md for automatic self-correction

---

## 9. ACTIONABLE INJECTION TARGETS FOR PRINTMAXX

### Immediate CLAUDE.md Optimizations
1. **Prune to under 80 lines** — move domain rules to `.claude/rules/`
2. **Add path-scoped rules** for each venture type, each automation module
3. **Convert enforcement rules to hooks** — anything that says "ALWAYS" or "NEVER" should be a hook, not a suggestion
4. **Add verification requirements** — after every code change, run tests

### New Hooks to Implement
```json
{
  "PreCompact": [{
    "matcher": "auto",
    "command": "python3 AUTOMATIONS/save_context_snapshot.py"
  }],
  "PostToolUse": [
    {
      "matcher": "Write",
      "command": "python3 -m black --quiet $TOOL_INPUT_FILE_PATH 2>/dev/null || true"
    },
    {
      "matcher": "Bash",
      "command": "jq -r '.tool_input.command' >> LEDGER/AGENT_COMMANDS.log"
    }
  ],
  "PreToolUse": [{
    "matcher": "Bash",
    "command": "bash AUTOMATIONS/hooks/safety_guard.sh"
  }]
}
```

### Self-Improvement Loop to Build
```python
# After every agent task completion:
def post_task_learning(task_result, agent_name):
    if task_result.had_errors:
        # Extract principled rule from failure
        rule = llm.generate(f"""
        The agent {agent_name} failed at: {task_result.error}
        The correct approach was: {task_result.correction}

        Write a ONE-LINE rule that would prevent this failure in the future.
        Format: "RULE: [category] — [instruction]"
        """)
        append_to_agents_md(rule)

    if task_result.discovered_pattern:
        # Document successful pattern
        pattern = f"PATTERN: {task_result.pattern_description}"
        append_to_agents_md(pattern)
```

### MARS-Style Prompt Enhancement Cycle
```
Every 48 hours (via cron):
1. Scan LEDGER/ for agent errors from past 48h
2. Aggregate errors by category (security, logic, style, missed context)
3. For each category with 2+ errors:
   a. Generate a PRINCIPLED rule (normative: "Always do X")
   b. Generate a PROCEDURAL rule (step-by-step: "To do X, first Y then Z")
4. Inject rules into relevant .claude/rules/ file
5. Log injection to LEDGER/PROMPT_EVOLUTION.jsonl
```

### Constitutional AI Integration with SOUL.md
```markdown
# SOUL.md — Constitutional Principles for Self-Correction

Before finalizing ANY output, evaluate against these principles:

1. ACTIONABILITY — Is this output something that can be EXECUTED, or is it just analysis?
   → If just analysis, add specific next steps with commands/file paths
2. VERIFICATION — Does this output include a way to VERIFY it worked?
   → If not, add a test command or expected output
3. SIMPLICITY — Am I building something new when an existing tool/file handles this?
   → Check existing system before creating anything new
4. SECURITY — Have I considered auth, input validation, and data exposure?
   → If code touches user data or external APIs, add security review
5. SOUL ALIGNMENT — Does this output sound like the user's voice model?
   → Check against OPS/USER_VOICE_MODEL.json
```

---

## SOURCES

### CLAUDE.md & System Prompts
- [Claude Code Best Practices (Official)](https://code.claude.com/docs/en/best-practices)
- [CLAUDE.md Best Practices — Arize](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
- [Writing a Good CLAUDE.md — HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [CLAUDE.md Examples 2026 — MorphLLM](https://www.morphllm.com/claude-md-examples)
- [Claude Code System Prompts (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Claude Code Best Practice (GitHub)](https://github.com/shanraisshan/claude-code-best-practice)
- [CLAUDE.md Templates (GitHub)](https://github.com/abhishekray07/claude-md-templates)
- [Claude Code Rules — Stop Stuffing One CLAUDE.md](https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433)
- [Path-Scoped Rules — ClaudeFast](https://claudefa.st/blog/guide/mechanics/rules-directory)
- [Persistent Memory Architecture — Dev.to](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d)

### Meta-Cognition & Self-Improvement
- [MIT Recursive Meta-Cognition — 110% improvement](https://blockchain.news/ainews/mit-s-recursive-meta-cognition-boosts-chatgpt-performance-by-110-advanced-prompt-engineering-for-ai-reasoning)
- [Recursive Meta-Cognition — Grokipedia](https://grokipedia.com/page/Recursive_Meta-Cognition)
- [MARS Framework — ArXiv](https://arxiv.org/abs/2503.19271)
- [Meta-Cognitive Reflection for Self-Improvement — ArXiv](https://arxiv.org/html/2601.11974v1)
- [DSPy Framework — Stanford](https://dspy.ai/)
- [DSPy Optimizers](https://dspy.ai/learn/optimization/optimizers/)
- [Self-Improving Agents — Addy Osmani](https://addyosmani.com/blog/self-improving-agents/)
- [Self-Reflection Prompting Guide (91% accuracy)](https://mindwiredai.com/2026/03/02/self-reflection-prompting-guide/)
- [Godel Agent — Recursive Self-Improvement](https://arxiv.org/abs/2410.04444)
- [PromptWizard — Microsoft Research](https://www.microsoft.com/en-us/research/blog/promptwizard-the-future-of-prompt-optimization-through-feedback-driven-self-evolving-prompts/)

### Power User Patterns
- [Claude Code Ultimate Guide (GitHub)](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)
- [Awesome Claude Code (GitHub)](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Code 7 Levels of Mastery](https://algeriatech.news/claude-code-mastery-7-levels-2026/)
- [How I Use Claude Code — Builder.io](https://www.builder.io/blog/claude-code)
- [Claude Code Advanced Users — Cuttlesoft](https://cuttlesoft.com/blog/2026/02/03/claude-code-for-advanced-users/)
- [9 Parallel Review Subagents — HAMY](https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents)

### Anti-Patterns & Failure Modes
- [Claude Code Anti-Patterns — KDnuggets](https://ai-report.kdnuggets.com/p/claude-code-anti-patterns-exposed)
- [Claude Keeps Making Same Mistakes — Medium](https://medium.com/@elliotJL/your-ai-has-infinite-knowledge-and-zero-habits-heres-the-fix-e279215d478d)
- [AI Coding Agent Security Mistakes — Help Net Security](https://www.helpnetsecurity.com/2026/03/13/claude-code-openai-codex-google-gemini-ai-coding-agent-security/)
- [The Productivity Paradox — Dev.to](https://dev.to/cwilkins507/the-claude-code-productivity-paradox-47go)

### Hooks & Automation
- [Claude Code Hooks Guide (Official)](https://code.claude.com/docs/en/hooks-guide)
- [Hooks Practical Guide — DataCamp](https://www.datacamp.com/tutorial/claude-code-hooks)
- [Hooks Automation — GitButler](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks/)
- [Infinite Context via Compaction Bridge (GitHub)](https://gist.github.com/ruvnet/29f8fa68582fdc1ca2da30136f538dba)
- [Context Buffer Management — ClaudeFast](https://claudefa.st/blog/guide/mechanics/context-buffer-management)

### Reasoning Frameworks
- [CoT vs ToT vs GoT — Weights & Biases](https://wandb.ai/sauravmaheshkar/prompting-techniques/reports/Chain-of-thought-tree-of-thought-and-graph-of-thought-Prompting-techniques-explained---Vmlldzo4MzQwNjMx)
- [Demystifying Chains, Trees, Graphs — ArXiv](https://arxiv.org/html/2401.14295v3)
- [Reflexion — Prompting Guide](https://www.promptingguide.ai/techniques/reflexion)
- [Self-Correcting Agents Reflection Pattern — Fast.io](https://fast.io/resources/reflection-pattern-self-correcting-agents/)

### Future-Proofing
- [Opus 4.6 + Agent Teams — TechCrunch](https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/)
- [Claude 5 News Roundup](https://help.apiyi.com/en/claude-5-latest-news-2026-features-release-en.html)
- [Agent Skills — The New Stack](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/)
- [Enterprise Agents — TechCrunch](https://techcrunch.com/2026/02/24/anthropic-launches-new-push-for-enterprise-agents-with-plugins-for-finance-engineering-and-design/)
- [Agent Teams (Official Docs)](https://code.claude.com/docs/en/agent-teams)
- [Claude Code Skills (Official Docs)](https://code.claude.com/docs/en/skills)
- [Subagents (Official Docs)](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Memory (Official Docs)](https://code.claude.com/docs/en/memory)
