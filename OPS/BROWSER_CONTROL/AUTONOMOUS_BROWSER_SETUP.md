# Autonomous Browser Setup

**Purpose:** Configure Chrome MCP for unattended/overnight browser automation runs

---

## The Problem

Every time Claude uses Chrome MCP to navigate to a new domain, you get a permission popup:
- "Allow this action" - One-time approval
- "Always allow actions on this site" - Whitelist that domain

For ralph loops and overnight automation, you need to either:
1. **Enable "On all sites" access (BEST - one-time setup)**
2. Pre-whitelist domains you'll use
3. Use WebSearch/WebFetch which don't require permission

---

## Solution 1: Enable "Act Without Asking" Mode (BEST)

**This is the one-time fix that eliminates ALL future permission popups.**

1. Click the **Claude extension icon** to open the side panel
2. Click the **three-dot menu (⋮)** in the upper right of the side panel
3. Select **"Settings"**
4. Change permission mode to **"Act without asking"**

You'll see a yellow warning: "HIGH RISK: Claude can take most actions on the internet now."

Done. No more permission popups.

### Security Consideration

"Act without asking" gives Claude full browser control including your logged-in sessions. For sensitive tasks (banking, payments, personal accounts), consider:
- Using WebSearch/WebFetch instead (no browser control)
- Using Playwriter MCP (isolated Playwright sandbox)
- Doing those tasks manually

---

## Solution 2: Pre-Whitelist Common Domains (If "All Sites" Feels Too Open)

Before running autonomous tasks, manually whitelist domains you know Claude will access.

**How to whitelist:**
1. When the popup appears, click **"Always allow actions on this site"** (bottom option, `⌘ ↵`)
2. This permanently whitelists that domain

**Domains to pre-whitelist for PRINTMAXX:**
```
x.com (Twitter)
github.com
devforum.roblox.com
roblox.com
reddit.com
producthunt.com
indiehackers.com
news.ycombinator.com
g2.com
capterra.com
linkedin.com
romonitorstats.com
```

**To pre-whitelist:**
1. Start a browser session
2. Navigate to each domain once
3. Click "Always allow" for each
4. Now they're whitelisted for future sessions

---

## Solution 2: Check Extension Settings

The Chrome MCP extension may have settings to configure broader permissions.

**To access:**
1. Open Chrome
2. Go to `chrome://extensions`
3. Find "Claude for Chrome" or similar
4. Click "Details" or settings icon
5. Look for permission settings

**What to look for:**
- "Allow on all sites" option
- Domain whitelist management
- Permission level settings

---

## Solution 3: Use update_plan Tool

Before browser-heavy tasks, use `mcp__Claude_in_Chrome__update_plan` to pre-approve domains:

```
Approach: ["Navigate to X", "Screenshot", "Extract data"]
Domains: ["x.com", "github.com", "devforum.roblox.com"]
```

This tells the extension upfront what domains you'll access, potentially reducing prompts.

---

## For Ralph Loops / Overnight Runs

**Best practice:**
1. Before starting overnight run, do a quick "warmup" session
2. Visit all domains the task will need
3. Click "Always allow" for each
4. Then start the ralph loop

**Example warmup script:**
```markdown
# Browser Warmup for [TASK]

Visit these domains and whitelist:
1. x.com - for Twitter research
2. github.com - for repo analysis
3. devforum.roblox.com - for Roblox research

After whitelisting, start main task.
```

---

## Fallback: Avoid Browser for Autonomous Tasks

If browser permissions are blocking autonomous runs, use non-browser alternatives:

| Task | Instead of Browser | Use This |
|------|-------------------|----------|
| Web search | Chrome MCP | WebSearch tool |
| Fetch page content | Chrome MCP navigate | WebFetch tool |
| API data | Browser scraping | Bash + curl |
| GitHub repos | Browser | `gh` CLI via Bash |

**WebSearch and WebFetch don't require permission popups.**

---

## CLAUDE.md Note

Add this to your understanding:

> **Browser Permission Handling:** If Chrome MCP triggers permission popups that block autonomous runs, prefer WebSearch/WebFetch for research. Only use Chrome MCP when you need:
> - Screenshots of rendered pages
> - Interactive elements (clicks, forms)
> - JavaScript-rendered content
> - Logged-in sessions

---

## Quick Fix for Current Session

**Best permanent fix:** Enable "On all sites" via puzzle piece menu (Solution 1 above). Takes 10 seconds, fixes it forever.

**Temporary fix:** Click "Always allow actions on this site" (bottom option) on each popup. Use keyboard shortcut `⌘ + Enter` if available.

---

## TL;DR

1. Click Claude extension icon → open side panel
2. Three-dot menu (⋮) in upper right → Settings
3. Change to **"Act without asking"**
4. Never see permission popups again

**For sensitive tasks:** Use WebSearch/WebFetch or Playwriter MCP instead of Chrome MCP.
