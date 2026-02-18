# Claude Code Optimization - Complete Refactor

**Date:** 2026-01-19
**Status:** ✅ Optimized for Claude Code native features

---

## What Changed

Your PRINTMAXX repo has been refactored to align with **Claude Code's native architecture** instead of fighting against it with custom systems.

### ❌ Removed (Over-Engineered)
- `scripts/claim_folder.py` / `release_folder.py` - Folder locking system (unnecessary)
- `scripts/build_context_packet.py` - Manual context packets (use native memory)
- `CLAUDE.md` at root - Moved to `.claude/CLAUDE.md`
- `Makefile` - Replaced with natural language commands to subagents

### ✅ Added (Claude Code Native)
```
.claude/
├── CLAUDE.md                      # Main project instructions (auto-loaded)
├── settings.json                  # Project configuration
├── agents/
│   ├── validator.md               # Validation subagent (Haiku)
│   ├── reviewer.md                # Code review subagent (Sonnet)
│   ├── content-generator.md       # Content creation subagent (Sonnet)
│   └── deployer.md                # Deployment subagent (Haiku)
└── rules/
    ├── security.md                # Security policies (auto-loaded)
    ├── performance.md             # Performance standards (auto-loaded)
    └── code-style.md              # Code conventions (auto-loaded)
```

---

## How to Use Claude Code Effectively

### 1. **Memory is Automatic**
No need for context packets. Claude Code automatically loads:
- `.claude/CLAUDE.md` - Your project instructions
- `.claude/rules/*.md` - All guidelines (security, performance, style)
- Previous session history when you resume

### 2. **Use Specialized Subagents**

Instead of running commands, just ask Claude:

```
Use the validator to check my recent changes
```

```
Use the reviewer to check my implementation of the lead capture form
```

```
Use content-generator to create 25 longtail pages from the CSV queue
```

```
Use deployer to run pre-flight checks for production
```

Each subagent knows its role, has the right tools, and uses the appropriate model (Haiku for fast/cheap, Sonnet for quality).

### 3. **Resume Sessions** (Not Fresh Chats)

Instead of "building context packets":
```bash
# Continue your most recent work
claude --continue

# Resume a specific session
claude --resume content-generation

# Pick from a list
claude --resume
```

Full context is preserved—nothing lost.

### 4. **Parallel Work with Worktrees**

If you need true parallel sessions (not common):
```bash
# Create a worktree for parallel feature work
git worktree add ../printmaxx-feature-x feature-x

# Work in separate terminal/Claude session
cd ../printmaxx-feature-x
claude
```

Each worktree has isolated file state. No manual folder locking needed.

---

## New Workflows

### Validate Before Committing
```
Use the validator to check my changes before I commit
```

The validator (Haiku model) will check:
- Code style and linting
- SEO requirements
- Security issues
- Performance impact
- LEDGER sync status

### Get Code Review
```
Use the reviewer to review my implementation
```

The reviewer (Sonnet model) provides:
- Architecture feedback
- Security analysis
- Testing gaps
- Documentation needs
- Specific improvement suggestions

### Generate Content
```
Use content-generator to create a truth page about AI workflow automation
```

```
Use content-generator to generate 25 longtail pages
```

The content generator (Sonnet model) will:
- Research existing content for style/tone
- Generate SEO-optimized content
- Add proper frontmatter and meta tags
- Update LEDGER CSV with published status

### Deploy Safely
```
Use deployer to run pre-flight checks for production
```

The deployer (Haiku model) will:
- Run full test suite
- Check build output
- Validate environment variables
- Verify no hardcoded secrets
- Create deployment checklist

---

## Model Routing (Built-In)

Model selection is now handled by:
1. **Global default:** Set in `.claude/settings.json` (currently: Sonnet)
2. **Subagent-specific:** Each agent specifies its model
   - validator: Haiku (fast checks)
   - reviewer: Sonnet (quality feedback)
   - content-generator: Sonnet (quality content)
   - deployer: Haiku (checklist execution)
3. **Session override:** `claude --model opus` when needed

**No more manual MODEL_ROUTING_POLICY checks needed.**

---

## Rules Are Automatic

Every session automatically loads:
- **security.md** - No hardcoded credentials, input validation, etc.
- **performance.md** - Bundle size limits, Core Web Vitals, caching
- **code-style.md** - Naming conventions, TypeScript usage, formatting

You don't need to reference them—Claude Code enforces them automatically.

---

## Progress Tracking Simplified

### Old System (Removed)
- LEDGER/MASTER_TASKS.md
- LEDGER/STATUS_BOARD.md
- Manual runlog creation
- Folder lock tracking

### New System (Native)
- `.claude/CLAUDE.md` - Current status section (update as needed)
- Session resumption - Full history preserved
- Natural conversation - Just continue where you left off

**Update `.claude/CLAUDE.md` Current Status section when major milestones complete.** That's it.

---

## Example Session Flow

### Starting Work
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT
claude
```

Claude automatically loads `.claude/CLAUDE.md` and all rules.

### Generate Content
```
Use content-generator to create 25 longtail pages
```

Generator creates content, updates LEDGER CSV, reports completion.

### Validate
```
Use the validator to check the new pages
```

Validator checks SEO, style, security. Reports any issues.

### Review
```
Use the reviewer to review before I commit
```

Reviewer provides feedback on quality, suggests improvements.

### Commit
```
Create a git commit for these new pages
```

Claude handles git operations with proper commit message.

### Deploy
```
Use deployer to check if we're ready for production
```

Deployer runs full pre-flight checklist, reports status.

### Continue Later
Next day:
```bash
claude --continue
```

Full context restored. No "catch up" needed.

---

## Quick Reference

### Get help from specialized agents
- `Use the validator` - Fast quality checks
- `Use the reviewer` - Detailed code review
- `Use content-generator` - Create SEO content
- `Use deployer` - Deployment workflows

### Resume work
- `claude --continue` - Resume last session
- `claude --resume` - Pick from session list

### Override model
- `claude --model opus` - Use Opus for critical work
- `claude --model haiku` - Use Haiku for simple tasks

### Update project state
Edit `.claude/CLAUDE.md` → Current Status section

---

## What to Keep

### Still Useful
- **LEDGER/*.csv** - Source of truth for content tracking
- **OPS/prompts/** - Reusable prompt templates
- **MASTER_DOC/** - Full operating system documentation
- **README.md** - Project overview

### Use When Needed
- **OPS/logs/** - Can still create manual logs for audit trail
- **OPS/TOKEN_COST_CHECKPOINTS.md** - Cost management guidelines

---

## Cost Optimization

With subagents, you control costs better:
- **validator** (Haiku) - Cheap, fast checks
- **reviewer** (Sonnet) - Quality review when needed
- **content-generator** (Sonnet) - Quality content creation
- **deployer** (Haiku) - Fast deployment checks

Reserve **Opus** for critical decisions only.

---

## Benefits of This Refactor

1. **Less friction** - No manual context building, folder locking, step counting
2. **Native features** - Uses Claude Code's built-in memory and resumption
3. **Specialized agents** - Right tool for each job, right model for each task
4. **Automatic enforcement** - Rules loaded automatically, no manual checks
5. **Session continuity** - Resume anytime with full context
6. **Cost efficient** - Smart model routing per task

---

## Need Help?

All project context is in `.claude/CLAUDE.md` - Claude Code loads it automatically.

All rules are in `.claude/rules/` - Enforced automatically.

All workflows use subagents - Just ask Claude to use them.

**The system now works WITH Claude Code, not against it.**
