# Ralph Loop Guide

The overnight autonomous build pattern. Named after Ralph Wiggum - naive, relentless persistence.

**Source:** [github.com/snarktank/ralph](https://github.com/snarktank/ralph)
**Key posts:** [@damianplayer](https://x.com/damianplayer/status/2013338667964604909), [@agrimsingh](https://x.com/agrimsingh/status/2010412150918189210)

---

## The Core Insight

AI coding sessions rot after 40-60 minutes. The context window fills with:
- Files it read
- Commands it ran
- Wrong turns it took
- Half-baked plans it hallucinated

Once polluted, adding more instructions doesn't help. The ball is in the gutter.

**Ralph's solution:** Don't clean the memory. Throw it away and start fresh.

---

## What Most People Get Wrong (@damianplayer)

**Source:** [x.com/damianplayer/status/2014327653264744566](https://x.com/damianplayer/status/2014327653264744566)

### The Compaction Problem

Even Anthropic's official plugin misses the point. Instead of wiping context completely, it **compacts** - the AI guesses what's important to carry forward.

**Fatal flaw:** The AI doesn't know what's actually important. When it guesses wrong:
- Critical information disappears
- Bugs compound
- Features break in ways that don't make sense

### The Growing File Problem

Don't let the AI modify its own instructions on each loop (like an agents.md file that grows).

**Why it breaks:** Models are verbose by default. Each loop adds tokens. Ten iterations in, you've stuffed the context window before the actual task even starts.

**The canonical ralph keeps the prompt static.** The only thing that changes is a simple flag marking tasks complete. Nothing else grows.

### What Jeff Huntley Actually Intended

The original implementation is brutally simple:
```bash
while :; do cat prompt.md | claude ; done
```

One bash while loop. Reads a prompt file. Runs claude. Waits for it to finish. Loops again.

**No compaction. No growing memory files. No clever additions.**

The prompt tells the AI: read the plan, pick the most important incomplete task, implement it, test it, commit it, mark it done. Exit when everything passes.

**Key:** The loop lives outside the model's control. The AI can't decide when to stop. It just executes tasks until the external script sees everything marked complete.

---

## How It Works

```
Progress persists. Failures don't.
```

| Bad (Context) | Good (Files + Git) |
|---------------|-------------------|
| Dies with the convo | Only what you write |
| Persists forever | Can be rolled back |
| Polluted by dead ends | Git doesn't hallucinate |
| "Memory" can drift | State is explicit |

Each fresh agent:
1. Starts clean
2. Reads the anchor file (source of truth)
3. Picks a task
4. Builds it
5. Tests it
6. Saves if it works
7. Logs if it fails
8. Next agent starts fresh

---

## The Simplest Ralph Loop

```bash
while :; do cat prompt.md | agent ; done
```

That's it. Same task. New brain each iteration.

The "memory" is not the chat. It's the filesystem + git.

**If it's not written to a file, it doesn't exist.**

---

## PRINTMAXX Ralph Setup

### Anchor File Structure

Create `ralph_task.md` in project root:

```markdown
---
task: [what you're building]
test_command: "npm test" or "make validate"
---

# Task: [Title]

## Context
- Read CLAUDE.md for project rules
- Read .claude/rules/copy-style.md for content
- Output to [specific folder]

## Success Criteria
1. [ ] First thing (machine-verifiable)
2. [ ] Second thing (pass/fail)
3. [ ] Third thing (yes/no)

## Constraints
- Follow copy-style.md (no AI cringe)
- No em dashes
- Specific numbers over vague claims
```

### State Files

Create `.ralph/` folder:

```
.ralph/
├── guardrails.md    # Learned constraints ("don't do X")
├── progress.md      # What's done / what's next
├── errors.log       # What blew up
└── activity.log     # Token tracking
```

### Guardrails (How Ralph Stops Repeating Mistakes)

When something breaks, add to `.ralph/guardrails.md`:

```markdown
### Sign: Check file exists before editing
- Trigger: Editing a file
- Instruction: Verify file exists first
- Added after: Iteration 3 (file not found error)

### Sign: No em dashes in content
- Trigger: Writing any content
- Instruction: Use commas or periods, never —
- Added after: Iteration 5 (copy-style violation)
```

Guardrails are append-only. Mistakes evaporate. Lessons accumulate.

---

## When to Use Ralph

### Use Ralph When:
- Specs are crisp
- Success is machine-verifiable (tests, types, lint)
- Work is bulk execution (CRUD, migrations, refactors, content generation)
- You can clearly define "done" as checkboxes

### Don't Use Ralph When:
- Still deciding what to build
- Taste and judgment matter more than correctness
- Can't define what "done" means
- Real work is thinking/exploring

**If you can't write checkboxes, you're not ready to loop. You're ready to think.**

---

## PRINTMAXX Ralph Tasks (Ready to Run)

### Content Generation Loops

```markdown
# Task: Generate 50 social posts for Faith niche

## Success Criteria
1. [ ] 50 posts written to CONTENT/social/faith/
2. [ ] Each post < 280 characters
3. [ ] No em dashes in any post
4. [ ] No banned AI vocabulary (see copy-style.md)
5. [ ] Each post has specific number or example
6. [ ] Posts saved as individual .md files
```

```markdown
# Task: Generate 20 cold email sequences

## Success Criteria
1. [ ] 20 sequences written to MONEY_METHODS/COLD_OUTBOUND/sequences/
2. [ ] Each sequence has 3-5 emails
3. [ ] Each email has subject line + body + CTA
4. [ ] No promotional adjectives
5. [ ] Follows cold email best practices
```

```markdown
# Task: Generate landing page copy for 3 info products

## Success Criteria
1. [ ] Headlines for each product (< 10 words)
2. [ ] Subheadlines (who + what they get)
3. [ ] 5 bullet points per product
4. [ ] CTA copy for each
5. [ ] Written to MONEY_METHODS/INFO_PRODUCTS/products/*/LANDING_COPY.md
```

### Code Generation Loops

```markdown
# Task: Build Playwright posting scripts

## Success Criteria
1. [ ] x_poster.py posts to X with proxy support
2. [ ] ig_poster.py posts to Instagram with mobile proxy
3. [ ] Scripts use human-like delays
4. [ ] Scripts load from session files
5. [ ] Scripts log success/failure
6. [ ] All scripts in AUTOMATIONS/scripts/
```

```markdown
# Task: Build email templates (HTML)

## Success Criteria
1. [ ] Welcome email template
2. [ ] Launch email template
3. [ ] Nurture email template
4. [ ] All templates responsive
5. [ ] All templates under 100kb
6. [ ] Templates in LANDING/printmaxx-site/emails/
```

### Research Loops

```markdown
# Task: Research competitors for each money method

## Success Criteria
1. [ ] 5 competitors per money method
2. [ ] Pricing documented
3. [ ] Features compared
4. [ ] Gaps identified
5. [ ] Written to MONEY_METHODS/*/research/COMPETITORS.md
```

---

## Running Ralph with Claude Code

### Option 1: Manual Loop (Simple)

```bash
# Terminal 1: Run the loop
while true; do
  claude "Read ralph_task.md and .ralph/guardrails.md. Complete the next unchecked item. Update progress.md when done."
  sleep 5
done

# Terminal 2: Watch progress
tail -f .ralph/progress.md
```

### Option 2: Parallel Agents (PRINTMAXX Style)

Launch multiple independent tasks:

```
Agent 1: Generate faith niche content
Agent 2: Generate fitness niche content
Agent 3: Generate AI niche content
Agent 4: Write cold email sequences
Agent 5: Research competitors
```

Each agent has its own anchor file, outputs to different folders.

### Option 3: Cursor Ralph (Full Setup)

Install: [github.com/agrimsingh/ralph-wiggum-cursor](https://github.com/agrimsingh/ralph-wiggum-cursor)

```bash
curl -fsSL https://raw.githubusercontent.com/agrimsingh/ralph-wiggum-cursor/main/install.sh | bash
```

Features:
- Token tracking
- Gutter detection (same failure repeatedly)
- Model selection per iteration
- Real-time monitoring

---

## Cost Expectations

Typical Ralph run: 10 rounds = ~$30

One builder shipped entire app for under $300 (would have cost $50k to hire).

**PRINTMAXX estimate:**
- Content batch (50 posts): ~$5-10
- Full money method docs: ~$20-30
- Complete overnight build: ~$50-100

---

## The Win Condition

Ralph gets 90% there. You spend 1 hour fixing the last 10%.

**Old way:** 6-8 hours writing code per feature
**Ralph way:** 1 hour on requirements, wake up to finished work

That's 5x output with same hours. Compound over 3 months.

---

## Common Failures and Fixes

### "It keeps making the same mistake"
Add to guardrails.md. Next iteration reads it first.

### "It's going in circles"
Task too big. Break into smaller checkboxes.

### "Output quality is bad"
Success criteria too vague. Add specific, machine-verifiable checks.

### "It stopped making progress"
Context rotted. Kill session, start fresh. That's the whole point.

---

## PRINTMAXX Ralph Checklist

Before running:

- [ ] Anchor file written with clear checkboxes
- [ ] Output folders exist
- [ ] .ralph/ folder initialized
- [ ] guardrails.md has copy-style rules
- [ ] Each task is machine-verifiable
- [ ] No task requires human judgment mid-loop

After running:

- [ ] Review outputs for quality
- [ ] Check guardrails for new lessons
- [ ] Approve content for publishing
- [ ] Update progress tracking

---

## Related Documents

- `OPS/AUTONOMOUS_TASKS.md` - Full list of what can run unattended
- `OPS/MANUAL_SETUP_CHECKLIST.md` - What requires human action
- `.claude/rules/copy-style.md` - Content rules for guardrails
- `AUTOMATIONS/` - Scripts that Ralph can generate/improve

---

## Quick Start Tonight

1. Pick a content generation task
2. Write anchor file with 5-10 checkboxes
3. Create `.ralph/guardrails.md` with copy-style rules
4. Launch loop
5. Sleep
6. Morning: review outputs

That's Ralph. Progress persists. Failures evaporate.

---

Last updated: 2026-01-21
