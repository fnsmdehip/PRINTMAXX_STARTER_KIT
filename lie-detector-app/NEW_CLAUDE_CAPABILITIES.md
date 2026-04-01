# New Claude Code Capabilities (March-April 2026)

Researched 2026-04-01. Separates shipped features from leaked/rumored ones.

---

## 1. COMPUTER USE -- App Self-Auditing via Screenshots

**Status: SHIPPED (Research Preview, March 23 2026)**

Claude Code can now control your macOS desktop -- open apps, click, type, scroll, take screenshots, and analyze what it sees. This is the official "computer use" feature, not a third-party hack.

### How It Works
- Built-in MCP server called `computer-use`, disabled by default
- Enable via `/mcp` in an interactive Claude Code session, then select `computer-use` > Enable
- Requires macOS Accessibility + Screen Recording permissions
- Pro or Max plan only. NOT available on Team/Enterprise. NOT available with `-p` flag (non-interactive)
- Requires Claude Code v2.1.85+

### What It Can Actually Do
- Build a Swift/macOS app, launch it, click through every control, screenshot the result -- all in one conversation
- Open iOS Simulator, launch an app, tap through onboarding screens, report performance issues
- Resize windows to reproduce layout bugs, screenshot broken state, patch CSS, verify fix
- Drive GUI-only tools (design tools, hardware panels, proprietary apps with no CLI/API)

### Self-Audit Workflow (from real-world usage)
One developer (Christopher Meiklejohn) built a daily automated QA system:
- Android emulator + iOS Simulator boot at 8:47 AM via scheduled task
- Claude sweeps 25 screens on each platform
- Captures screenshots, analyzes for layout breaks, error messages, missing images
- Files bug reports automatically to a production forum
- Uses `ios-simulator-mcp` tool for precise UI element probing via accessibility labels
- Key tool: `ui_describe_point` -- point at any coordinate, get accessibility label + role + frame

### How Claude Decides What Tool to Use (priority order)
1. MCP server for the service (most precise)
2. Bash/shell command
3. Claude in Chrome (browser work)
4. Computer use (broadest, slowest -- last resort)

### Safety Guardrails
- Per-app approval each session (you choose which apps Claude can control)
- Terminal window excluded from screenshots (Claude never sees its own output)
- Press Esc anywhere to abort immediately
- Machine-wide lock -- only one computer use session at a time
- Apps are hidden while Claude works to prevent interference
- Browsers and trading platforms are VIEW-ONLY, terminals are CLICK-ONLY

### vs. What PRINTMAXX Already Has
PRINTMAXX uses Playwright MCP + Chrome MCP for browser testing, which is faster and more precise for web-based apps. Computer use is NOT a replacement for those -- it's for native apps, simulators, and GUI-only tools where no API exists. The two complement each other:
- **Use Chrome MCP / Playwright MCP** for web app testing (faster, more reliable)
- **Use Computer Use** for iOS Simulator testing, native macOS apps, desktop tools
- **Key upgrade**: Claude can now build an Expo app, open it in Simulator, tap through onboarding, screenshot every screen, and file bugs -- all without leaving the terminal

**Source**: https://code.claude.com/docs/en/computer-use

---

## 2. LONG-RUNNING AUTONOMOUS AGENTS

### 2a. Background Agents (SHIPPED, v2.0.60+)

**Status: SHIPPED**

Not new rumors -- this is the existing `run_in_background` feature matured:
- Subagents can run in background while you continue working
- Press Ctrl+B to move any sub-agent to background
- Each background agent works in an independent git worktree (no interference)
- Status, token usage, and progress visible in UI
- Ctrl+F kills all background agents (two-press confirmation)
- Output persists to files after completion

### 2b. Agent Teams (SHIPPED, March 2026)

**Status: SHIPPED**

New coordinated multi-agent system:
- Spawn named teammates via Agent tool with `name` parameter
- In-process teammates with `type: "in_process"`
- Agent isolation via `isolation: "worktree"` for independent git worktrees
- Custom agent models via `model:` frontmatter in `.claude/agents/*.md`
- Agent frontmatter: `effort`, `maxTurns`, `disallowedTools`, `initialPrompt`
- Team task lists, task assignment, idle detection
- `TeammateIdle`/`TaskCompleted` hooks for automation
- Shift+Down to cycle between active teammates

### 2c. Scheduled Tasks / Remote Triggers (SHIPPED)

**Status: SHIPPED**

Two types of scheduling now available:
- **Session-scoped (`/loop`)**: Run prompts on intervals within a session. `/loop 5m /health` checks every 5 minutes. Dies when session exits.
- **Persistent (Desktop)**: Survive restarts, run on visual schedule while app is open
- **Remote triggers**: Schedule tasks that run on Anthropic's cloud infrastructure -- tasks execute even when your machine is off
- CronCreate tool with standard 5-field cron expressions
- Recurring tasks auto-expire after 7 days (session-scoped) or 3 days (some implementations)

### 2d. KAIROS -- Persistent Background Agent (NOT YET SHIPPED)

**Status: LEAKED / UNRELEASED (found in npm source leak March 31 2026)**

From the Claude Code source leak (512K lines of TypeScript accidentally published):
- Persistent background mode where Claude watches your working environment 24/7
- Runs on heartbeat loops, evaluates context, decides whether to act or stay quiet
- Writes daily observation logs
- Three exclusive tools: push notifications, file delivery, PR subscriptions
- Append-only daily logs + `autoDream` memory consolidation during idle
- 15-second blocking budget per tick (won't interrupt your flow)
- Gated behind `PROACTIVE` and `KAIROS` feature flags -- NOT public yet
- References suggest April 1-7 as teaser window, May 2026 for full launch
- Persists across sessions (unlike current background agents)

**Source**: https://aiia.ro/blog/kairos-claude-code-proactive-agent/ and https://codepointer.substack.com/p/claude-code-architecture-of-kairos

### vs. What PRINTMAXX Already Has
PRINTMAXX's Ralph loops are filesystem-based autonomous loops (`while :; do cat PROMPT.md | claude --dangerously-skip-permissions --print ; done`). This is actually more flexible than what Claude Code ships natively because:
- Ralph loops run indefinitely (no 7-day expiry)
- Ralph uses filesystem as memory (survives any context loss)
- Ralph can run headless via cron without interactive session
- KAIROS (when shipped) would be the first native equivalent -- persistent, session-surviving, with push notifications

**Recommendation**: Keep Ralph loops for heavy autonomous work. Use `/loop` for lightweight in-session polling. Watch for KAIROS launch (May 2026?) as potential Ralph replacement with better integration.

---

## 3. OTHER MAJOR NEW FEATURES (March-April 2026)

### Git Worktrees (SHIPPED)
- `--worktree` (`-w`) CLI flag starts Claude in isolated git worktree
- Sparse checkout support for large monorepos (`worktree.sparsePaths`)
- Custom hooks for VCS setup/teardown
- Background agents auto-use worktrees for isolation
- Stale worktree auto-cleanup

### Voice Mode (SHIPPED)
- Push-to-talk with rebindable keys
- 20 languages supported (10 new in March: Russian, Polish, Turkish, Dutch, etc.)
- Improved accuracy with dev terms (regex, OAuth, JSON)

### Remote Control (SHIPPED)
- `/remote-control` bridges CLI sessions to claude.ai/code (continue from browser/phone)
- `--channels` permission relay -- approve tool calls from your phone
- AI-generated session titles
- Deep link support up to 5,000 characters

### PowerShell Tool (SHIPPED, Windows)
- Native PowerShell execution (opt-in preview)
- Version-specific guidance for PS 5.1 vs 7+
- Dangerous removal detection for Windows drive roots

### MCP OAuth Improvements (SHIPPED)
- RFC 9728 compliance for OAuth discovery
- Step-up auth (elevated scope via 403)
- Proper refresh token re-authorization
- MCP elicitation -- servers can request structured input mid-task via dialog

### `--bare` Flag (SHIPPED)
- Skips hooks, LSP, plugins for scripted `-p` calls
- Useful for Ralph loops and cron jobs -- faster startup, fewer side effects

### Analytics API (SHIPPED)
- Programmatic access to daily aggregated usage metrics
- Productivity metrics, tool usage stats, cost data
- For organizations managing multiple Claude Code users

### Permission System Upgrades (SHIPPED)
- `PermissionDenied` hook fires after auto-mode denials (return `{retry: true}` to retry)
- `defer` permission decision -- pause at tool call, resume later
- Hook conditional `if` field for filtering by permission rule
- Managed domain blocking for enterprise

### Memory System (SHIPPED)
- `/memory` command for managing auto-memory
- Custom directory via `autoMemoryDirectory` setting
- Memory timestamps for freshness reasoning
- 25KB / 200 line index cap
- PostCompact hook

### Model Changes
- Opus 4 and 4.1 REMOVED -- auto-migrated to Opus 4.6
- Sonnet 4.5 1M replaced by Sonnet 4.6 on Max plan
- Effort levels simplified: low/medium/high (removed max)
- `/effort` command for per-session override

---

## 4. COMPARISON: New Features vs. PRINTMAXX Stack

| Capability | PRINTMAXX Current | New Claude Code | Winner | Action |
|---|---|---|---|---|
| Web app testing | Playwright MCP + Chrome MCP | Same (unchanged) | Tie | Keep current stack |
| Native app / Simulator testing | Manual or ios-simulator-mcp | Computer Use (built-in) | NEW | Enable for app factory QA |
| Autonomous loops | Ralph (filesystem, cron, indefinite) | /loop (session-scoped, 7-day max) | PRINTMAXX | Keep Ralph for production |
| Persistent agent | Ralph + cron | KAIROS (unreleased, May 2026?) | PRINTMAXX (for now) | Watch KAIROS launch |
| Background agents | run_in_background + subagents | Same + worktree isolation + teams | NEW | Upgrade to agent teams |
| Browser control | 8-level fallback chain | Chrome MCP + Computer Use | Tie | Add Computer Use as L0 for native |
| Scheduled tasks | crontab + launchd | /loop + CronCreate + remote triggers | NEW for remote | Use remote triggers for cloud tasks |
| Permission relay | N/A | --channels (phone approvals) | NEW | Enable for overnight runs |
| Scripted calls | claude -p --api-key | claude -p --bare --api-key | NEW | Use --bare for faster cron |

### Top 3 Actions for PRINTMAXX

1. **Enable Computer Use for App Factory QA** -- Wire `computer-use` MCP into the app factory pipeline. After `expo export`, have Claude open Simulator, tap through every screen, screenshot results, compare against expected states. This replaces manual QA entirely.

2. **Use `--bare` flag in all cron/Ralph scripts** -- Skips hooks, LSP, plugins. Faster startup for headless automation. Update `schedule_claude.sh` and all `subprocess.run(["claude"...])` calls.

3. **Watch for KAIROS (May 2026)** -- If it ships as described in the leak, it's a native Ralph replacement with push notifications and PR subscriptions built in. Could eliminate the need for custom cron-based Ralph loops.

---

## Sources

- Claude Code Changelog: https://code.claude.com/docs/en/changelog
- Computer Use Docs: https://code.claude.com/docs/en/computer-use
- Scheduled Tasks Docs: https://code.claude.com/docs/en/scheduled-tasks
- Mobile QA Blog Post: https://christophermeiklejohn.com/ai/zabriskie/development/android/ios/2026/03/22/teaching-claude-to-qa-a-mobile-app.html
- KAIROS Architecture Analysis: https://codepointer.substack.com/p/claude-code-architecture-of-kairos
- KAIROS Feature Analysis: https://aiia.ro/blog/kairos-claude-code-proactive-agent/
- Claude Code Source Leak Coverage: https://thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html
- Computer Use Announcement: https://claude.com/blog/dispatch-and-computer-use
- Long-Running Agents Research: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- GitHub Releases: https://github.com/anthropics/claude-code/releases
