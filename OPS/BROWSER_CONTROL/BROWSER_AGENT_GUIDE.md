# Browser Agent Control Guide

**Last Updated:** 2026-01-26
**Purpose:** Optimal browser automation tool selection and fallback chains

---

## Tool Priority Order

When browser automation is needed, try tools in this order:

### Priority 1: Chrome MCP (Default)
**Use for:** Simple tasks - screenshots, single clicks, form fills, navigation

```
Tools: mcp__Claude_in_Chrome__*
- tabs_context_mcp (get tab context first)
- navigate (go to URL)
- computer (screenshot, click, scroll, type)
- read_page (accessibility tree)
- find (natural language element search)
- form_input (fill forms)
- get_page_text (extract text)
```

**When it works:**
- Page loads normally
- Simple interactions
- No complex JS apps
- Single-page tasks

**When it fails:**
- Heavy JS apps that don't render
- Complex multi-step flows
- Need to control user's actual browser
- Background browser needed

---

### Priority 2: agent-browser (Vercel Labs) - NEW
**Use for:** AI-optimized automation, snapshot-based refs, protected sites

**Repo:** [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)

**Install:**
```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
npx skills add vercel-labs/agent-browser  # Claude Code skill
```

**When to use:**
- Need AI-optimized output (snapshot refs)
- Protected sites with anti-bot
- Persistent authenticated sessions
- Batch CLI automation
- Sites requiring stealth (use `-p browseruse`)

**Core workflow:**
```bash
agent-browser open https://example.com
agent-browser snapshot -i --json  # Get refs (@e1, @e2)
agent-browser click @e1
agent-browser fill @e2 "text"
```

**For anti-bot/auth sites:**
```bash
export BROWSER_USE_API_KEY="your-key"
agent-browser -p browseruse open https://protected-site.com
```

**Full docs:** `OPS/BROWSER_CONTROL/AGENT_BROWSER_RESEARCH.md`

---

### Priority 3: Playwriter MCP
**Use for:** Complex multi-step flows, controlling YOUR Chrome window

**Repo:** [remorses/playwriter](https://github.com/remorses/playwriter) (2.5k stars)

**Install:**
1. Chrome extension from Web Store
2. Add to Claude MCP config

**When to escalate here:**
- Chrome MCP screenshots show blank/broken pages
- Need stateful multi-step automation
- Want to see browser actions in real-time
- Complex form sequences

---

### Priority 4: Playwright MCP (Microsoft)
**Use for:** Accessibility-tree based automation, headless testing

**Repo:** [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)

**When to use:**
- Need headless browser
- Accessibility-based selectors
- Testing/validation flows
- Don't need visual feedback

---

### Priority 5: Bash + Playwright Scripts
**Use for:** Custom automation scripts, batch operations

**When to use:**
- Need custom logic
- Batch URL processing
- Scheduled automation
- Full Playwright API access

```bash
# Example
cd AUTOMATIONS && npx playwright test scrape-task.spec.ts
```

---

### Priority 6: Browserbase Cloud (agent-browse)
**Use for:** Production QA, sandboxed execution, session recording

**Install:** `npx skills add browserbase/agent-browse`

**When to use:**
- Need cloud browser isolation
- Session recording/debugging
- Scalable parallel testing
- Can't use local browser

---

## Automatic Fallback Chain

When a browser task fails, try the next tool automatically:

```
Chrome MCP fails (blank page, timeout, JS error)
    ↓
Try agent-browser local (AI-optimized, snapshot refs)
    ↓
agent-browser local fails (anti-bot, auth required)
    ↓
Try agent-browser -p browseruse (stealth cloud + profile sync)
    ↓
browseruse fails (specific use case)
    ↓
Try Playwriter MCP (controls real Chrome)
    ↓
Playwriter fails (extension issue, page blocks)
    ↓
Try Playwright MCP (headless, accessibility tree)
    ↓
Playwright fails (complex JS)
    ↓
Try Bash + custom Playwright script
    ↓
Script fails (need cloud isolation)
    ↓
Use Browserbase cloud browser
```

---

## Task-to-Tool Matching

| Task Type | Best Tool | Fallback |
|-----------|-----------|----------|
| Screenshot webpage | Chrome MCP | agent-browser |
| Fill simple form | Chrome MCP | agent-browser |
| Multi-step login flow | agent-browser --profile | Playwriter |
| Scrape dynamic JS app | agent-browser | Playwright script |
| Extract text from article | Chrome MCP get_page_text | agent-browser |
| Click through wizard | agent-browser (snapshot refs) | Chrome MCP |
| Test production site | Browserbase | Playwright |
| Batch URL processing | agent-browser CLI | Playwright script |
| Monitor competitor site | Chrome MCP | Visualping.io |
| Extract Twitter/X content | agent-browser -p browseruse | Chrome MCP (logged in) |
| Anti-bot protected sites | agent-browser -p browseruse | Manual |
| LinkedIn scraping | agent-browser -p browseruse | Manual |
| Authenticated sessions | agent-browser --profile | Playwriter |

---

## Common Failure Modes & Fixes

### Chrome MCP shows blank/broken page
**Cause:** Heavy JS app, page requires login, anti-bot
**Fix:** Use agent-browser with `snapshot -i` for refs, or Playwriter

### Screenshot timeout
**Cause:** Page slow to load
**Fix:** Use agent-browser with `wait` command, or Playwriter with explicit waits

### Can't find element
**Cause:** Dynamic content, shadow DOM, iframes
**Fix:** Use agent-browser `snapshot -i --json` for precise refs

### Twitter/X returns JS error
**Cause:** X requires JavaScript
**Fix:** Use agent-browser -p browseruse with synced profile, or Chrome MCP with logged-in session

### Form submission fails
**Cause:** CSRF tokens, hidden fields
**Fix:** Use agent-browser fill command or Playwriter to interact like real user

### Page detects automation
**Cause:** Anti-bot measures
**Fix:** Use agent-browser -p browseruse (stealth cloud browser) or manual

### Need authenticated session
**Cause:** Site requires login
**Fix:** Use agent-browser --profile for persistent login, or sync profile to browseruse cloud

---

## Quick Reference Commands

### Chrome MCP
```bash
# Check Chrome MCP tabs
mcp__Claude_in_Chrome__tabs_context_mcp

# Navigate and screenshot
mcp__Claude_in_Chrome__navigate → url
mcp__Claude_in_Chrome__computer → action: screenshot

# Find element by description
mcp__Claude_in_Chrome__find → query: "login button"

# Fill form field
mcp__Claude_in_Chrome__form_input → ref, value

# Get page text (articles)
mcp__Claude_in_Chrome__get_page_text

# Read accessibility tree
mcp__Claude_in_Chrome__read_page → depth: 3
```

### agent-browser (Vercel Labs)
```bash
# Basic workflow
agent-browser open https://example.com
agent-browser snapshot -i --json          # Get refs
agent-browser click @e1                   # Click by ref
agent-browser fill @e2 "text"             # Fill by ref
agent-browser screenshot page.png
agent-browser close

# Persistent profile (auth sessions)
agent-browser --profile ~/.myapp open https://myapp.com/dashboard

# Stealth cloud browser (anti-bot)
export BROWSER_USE_API_KEY="your-key"
agent-browser -p browseruse open https://protected-site.com

# Isolated sessions
agent-browser --session twitter open x.com
agent-browser --session linkedin open linkedin.com
```

---

## Integration with PRINTMAXX

### For Twitter/X bookmark extraction
**Recommended:** agent-browser with profile sync
1. Sync Twitter profile: `curl -fsSL https://browser-use.com/profile.sh | BROWSER_USE_API_KEY=xxx sh`
2. `agent-browser -p browseruse open https://x.com/i/bookmarks`
3. `agent-browser snapshot -i --json`
4. Extract to ALPHA_STAGING.csv

**Fallback:** Chrome MCP (user logged in)
1. Navigate to bookmarks
2. Screenshot + read_page
3. Extract to ALPHA_STAGING.csv

### For competitor monitoring
1. Chrome MCP for simple pages
2. agent-browser for JS-heavy pages
3. agent-browser -p browseruse for protected dashboards
4. Visualping.io for automated change detection

### For app store research
1. Chrome MCP for App Store pages
2. agent-browser for bulk scraping
3. appkittie.com for trending (Chrome MCP)

### For LinkedIn/Protected Sites
1. `agent-browser -p browseruse open https://linkedin.com/sales`
2. Profile sync handles auth
3. Stealth browser bypasses anti-bot

---

## Files Reference

| File | Purpose |
|------|---------|
| `OPS/TOOL_STACK.md` | Full tool comparison |
| `OPS/BROWSER_CONTROL/BROWSER_AGENT_GUIDE.md` | This file |
| `OPS/BROWSER_CONTROL/AGENT_BROWSER_RESEARCH.md` | agent-browser + browser-use deep dive |
| `OPS/BROWSER_CONTROL/AUTONOMOUS_BROWSER_SETUP.md` | Chrome MCP permissions |
| `AUTOMATIONS/` | Custom Playwright scripts |
| `.claude/` | MCP configurations |
