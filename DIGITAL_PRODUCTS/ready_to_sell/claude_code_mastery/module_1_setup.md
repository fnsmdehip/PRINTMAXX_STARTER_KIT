# Module 1: Getting Started with Claude Code

## What You'll Have After This Module

A fully configured development environment with Claude Code installed, a CLAUDE.md file that acts as your persistent project brain, and hooks that enforce your standards automatically. Total time: 20 minutes.

## Step 1: Install Claude Code (3 minutes)

Open your terminal. Run:

```bash
npm install -g @anthropic-ai/claude-code
```

That's it. No Docker. No virtual environments. No config files to hunt down.

Verify it works:

```bash
claude --version
```

You need an Anthropic API key. Go to console.anthropic.com, create an account, add $20 in credits (this will last you weeks of heavy building), and grab your key.

Set it:

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Add that line to your `~/.zshrc` or `~/.bashrc` so it persists across terminal sessions.

## Step 2: Create Your First Project (2 minutes)

```bash
mkdir my-first-app && cd my-first-app
claude
```

Claude Code is now running inside your project directory. Everything it creates goes here. Every file it reads comes from here. It's sandboxed to your project — it won't touch your system files.

Type `/init` to generate a starter CLAUDE.md. But don't use the default one. Replace it with what's in Step 3.

## Step 3: The CLAUDE.md That Actually Works (10 minutes)

Your CLAUDE.md is the single most important file in your project. Claude reads it at the start of every session. It's your persistent memory, your coding standards, your architectural decisions — all in one file.

Here's the template that ships products:

```markdown
# Project: [YOUR APP NAME]

## What This App Does
[One sentence. If you can't describe it in one sentence, you don't know what you're building.]

## Tech Stack
- Frontend: Vanilla JS + HTML + CSS (no frameworks until you need them)
- Backend: None (start static, add Supabase when you need auth/data)
- Hosting: Surge.sh (free, instant deploys)

## Architecture Rules
1. Every feature goes in its own file. No 500-line index.js files.
2. CSS uses BEM naming. No inline styles.
3. All user-facing text lives in a constants.js file (makes i18n easy later).
4. Error handling on every fetch call. No silent failures.
5. Mobile-first. Every layout starts at 320px and scales up.

## Current Status
- [x] Project initialized
- [ ] Core feature: [describe it]
- [ ] Stripe integration
- [ ] Deploy to production

## Commands
- `surge ./ my-app-name.surge.sh` — deploy
- `npx serve .` — local dev server

## Do NOT
- Add TypeScript (overhead isn't worth it for MVPs)
- Add React/Vue/Svelte (vanilla JS ships faster for simple apps)
- Create a database until we have 10+ users
- Write tests until the core loop is validated with real users
```

Save this as `CLAUDE.md` in your project root. Every time you start a Claude Code session, it reads this file first. Update it as your project evolves.

The key insight most people miss: **CLAUDE.md is not documentation. It's a control mechanism.** The "Do NOT" section is where the magic happens. Without it, Claude will add TypeScript, install 14 npm packages, and architect a microservices backend for your landing page.

## Step 4: Set Up Hooks (5 minutes)

Hooks run automatically before or after Claude takes actions. They're your guardrails.

Create the hooks directory:

```bash
mkdir -p .claude/hooks
```

Create a pre-commit hook that prevents Claude from adding dependencies you didn't approve:

```bash
cat > .claude/hooks/pre-tool-use.sh << 'EOF'
#!/bin/bash
# Block npm install unless explicitly approved
if echo "$CLAUDE_TOOL_INPUT" | grep -q "npm install"; then
  echo "BLOCKED: npm install detected. Add the package to CLAUDE.md approved list first."
  exit 1
fi
EOF
chmod +x .claude/hooks/pre-tool-use.sh
```

Create a post-session hook that auto-updates your CLAUDE.md status:

```bash
cat > .claude/hooks/post-session.sh << 'EOF'
#!/bin/bash
# Log what changed this session
echo "## Session $(date +%Y-%m-%d_%H:%M)" >> .claude/session_log.md
git diff --stat >> .claude/session_log.md 2>/dev/null
EOF
chmod +x .claude/hooks/post-session.sh
```

Configure hooks in your `.claude/config.json`:

```json
{
  "hooks": {
    "pre-tool-use": ".claude/hooks/pre-tool-use.sh",
    "post-session": ".claude/hooks/post-session.sh"
  }
}
```

## What You Should Have Now

1. Claude Code installed and authenticated
2. A project directory with a CLAUDE.md that controls Claude's behavior
3. Hooks that prevent scope creep and log your progress

If any of these aren't working, don't move to Module 2. Fix them now. Every minute you spend on setup saves 10 minutes of debugging later.

## Common Mistakes to Avoid

**Mistake 1: Using Claude Code without CLAUDE.md.** Claude will make reasonable decisions, but "reasonable" means "generic." Your CLAUDE.md makes it make YOUR decisions.

**Mistake 2: Making CLAUDE.md too long.** Keep it under 100 lines. Claude reads the whole thing every session. If it's 500 lines, you're wasting tokens and diluting the important instructions.

**Mistake 3: Not updating CLAUDE.md.** After every major decision (chose Supabase over Firebase, decided to add dark mode, pivoted the pricing), update CLAUDE.md. It's your project's source of truth.

**Mistake 4: Treating Claude Code like ChatGPT.** You don't paste code into it and ask for fixes. You tell it what to build, and it creates, edits, and runs files directly on your machine. It's a coworker with terminal access, not a chatbot.

Next module: You'll build a complete PWA in 2 hours using everything you just set up.
