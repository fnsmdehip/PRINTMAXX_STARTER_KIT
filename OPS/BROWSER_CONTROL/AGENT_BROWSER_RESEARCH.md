# Agent-Browser + Browser-Use Research

**Last Updated:** 2026-01-26
**Source:** Twitter bookmark @shawn_pana, GitHub repos
**Status:** CRITICAL for browser automation stack

---

## TL;DR

**agent-browser** (Vercel Labs) + **browser-use** (Browser Use) = the most powerful browser automation combo for Claude Code.

- **agent-browser**: CLI tool optimized for AI agents (Rust + Node.js, snapshot-based refs)
- **browser-use**: Python library with cloud browser infrastructure, anti-bot bypass, profile sync

Together they solve our Chrome MCP limitations: captchas, anti-bot, authenticated sessions.

---

## Agent-Browser (Vercel Labs)

**Repo:** https://github.com/vercel-labs/agent-browser
**License:** Apache-2.0
**Stack:** Rust CLI with Node.js fallback, Playwright under the hood

### What It Is

Headless browser automation CLI specifically designed for AI agents. Fast Rust native binary with comprehensive command set.

### Key Features

1. **Snapshot-Based Refs** - Get accessibility tree with element refs (@e1, @e2), then interact using refs
2. **AI-Optimized Workflow** - `snapshot -i --json` returns machine-readable output
3. **Session Isolation** - Multiple isolated browser instances via `--session`
4. **Persistent Profiles** - Save cookies/localStorage across restarts via `--profile`
5. **Streaming** - WebSocket viewport streaming for "pair browsing"
6. **Cloud Provider Integrations** - Browserbase, Browser Use, Kernel

### Installation

```bash
# npm (recommended)
npm install -g agent-browser
agent-browser install  # Download Chromium

# From source (for Rust native binary)
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install && pnpm build && pnpm build:native
pnpm link --global
```

### Core Workflow for AI Agents

```bash
# 1. Navigate
agent-browser open example.com

# 2. Get snapshot with refs
agent-browser snapshot -i --json
# Returns: {"success":true,"data":{"snapshot":"...","refs":{"e1":{"role":"heading",...}}}}

# 3. Interact using refs
agent-browser click @e2
agent-browser fill @e3 "test@example.com"

# 4. Re-snapshot after page changes
agent-browser snapshot -i --json
```

### Claude Code Skill Integration

```bash
npx skills add vercel-labs/agent-browser
```

This works with Claude Code, Cursor, Codex, GitHub Copilot, Windsurf, etc.

### Key Commands

| Command | Description |
|---------|-------------|
| `open <url>` | Navigate to URL |
| `snapshot -i` | Get interactive elements with refs |
| `click @e1` | Click by ref |
| `fill @e2 "text"` | Fill input by ref |
| `get text @e1` | Get text content |
| `screenshot [path]` | Take screenshot |
| `--profile <path>` | Persistent browser profile |
| `--session <name>` | Isolated session |
| `-p browseruse` | Use Browser Use cloud |

### Cloud Provider Integration

```bash
# Browser Use (anti-bot, captcha bypass)
export BROWSER_USE_API_KEY="your-api-key"
agent-browser -p browseruse open https://protected-site.com

# Browserbase
export BROWSERBASE_API_KEY="your-api-key"
export BROWSERBASE_PROJECT_ID="your-project-id"
agent-browser -p browserbase open https://example.com

# Kernel (stealth mode, persistent profiles)
export KERNEL_API_KEY="your-api-key"
agent-browser -p kernel open https://example.com
```

---

## Browser-Use

**Repo:** https://github.com/browser-use/browser-use
**License:** MIT
**Stack:** Python 3.11+, Playwright

### What It Is

Python library that makes websites accessible for AI agents. Includes cloud infrastructure with stealth browsers, anti-bot bypass, and CAPTCHA handling.

### Key Features

1. **LLM Integration** - `ChatBrowserUse()` model optimized for browser tasks (3-5x faster)
2. **Stealth Browsers** - Cloud browsers designed to avoid detection
3. **Profile Sync** - Sync authenticated sessions across local and cloud
4. **Custom Tools** - Extend agent capabilities with custom actions
5. **Sandbox Mode** - Deploy agents next to browsers for minimal latency

### Installation

```bash
uv init
uv add browser-use
uv sync
uvx browser-use install  # Install Chromium
```

### Quick Start

```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def example():
    browser = Browser(
        # use_cloud=True,  # Uncomment for stealth cloud browser
    )
    llm = ChatBrowserUse()  # Optimized for browser tasks
    agent = Agent(
        task="Find the number of stars of the browser-use repo",
        llm=llm,
        browser=browser,
    )
    history = await agent.run()
    return history

if __name__ == "__main__":
    asyncio.run(example())
```

### Claude Code Skill

```bash
mkdir -p ~/.claude/skills/browser-use
curl -o ~/.claude/skills/browser-use/SKILL.md \
  https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

### Profile Sync (CRITICAL FEATURE)

This is what @shawn_pana was excited about. Sync your authenticated Chrome profile to cloud:

```bash
# Sync local auth profile to Browser Use cloud
curl -fsSL https://browser-use.com/profile.sh | BROWSER_USE_API_KEY=XXXX sh
```

This means:
- Login once locally to any site
- Sync profile to cloud
- Cloud browser has your authenticated session
- Bypass login flows, access protected content

### Custom Tools

```python
from browser_use import Tools

tools = Tools()

@tools.action(description='Extract price from page')
def extract_price(selector: str) -> str:
    # Custom logic here
    return f"Price: $99"

agent = Agent(
    task="Get product price",
    llm=llm,
    browser=browser,
    tools=tools,
)
```

### ChatBrowserUse Pricing

Optimized model for browser tasks:
- Input: $0.20/1M tokens
- Cached input: $0.02/1M tokens
- Output: $2.00/1M tokens

---

## Integration: Agent-Browser + Browser-Use

The combo @shawn_pana mentioned. Use agent-browser CLI with Browser Use cloud backend.

### Setup

```bash
# 1. Install agent-browser
npm install -g agent-browser
agent-browser install

# 2. Get Browser Use API key (free $10 credits)
# https://browser-use.com/cloud

# 3. Configure
export BROWSER_USE_API_KEY="your-key"
```

### Usage

```bash
# Use Browser Use cloud for anti-bot sites
agent-browser -p browseruse open https://protected-site.com
agent-browser snapshot -i
agent-browser click @e1
```

### Why This Combo Is Powerful

| Feature | Chrome MCP | agent-browser + browser-use |
|---------|------------|----------------------------|
| Anti-bot bypass | No | Yes (stealth browsers) |
| CAPTCHA handling | No | Yes (cloud solve) |
| Auth sessions | Manual | Profile sync |
| AI-optimized output | Limited | Snapshot refs + JSON |
| Persistent profiles | No | Yes |
| Cloud scaling | No | Yes |
| CLI for Claude Code | Limited | Native support |

---

## PRINTMAXX Applications

### 1. Twitter/X Scraping (Authenticated)

```bash
# Sync your logged-in Twitter session
curl -fsSL https://browser-use.com/profile.sh | BROWSER_USE_API_KEY=XXXX sh

# Now scrape with auth
agent-browser -p browseruse open https://x.com/i/bookmarks
agent-browser snapshot -i --json
agent-browser click @e5  # Click into tweet
```

### 2. LinkedIn Scraping (Auth + Anti-Bot)

```bash
# Profile sync handles login
agent-browser -p browseruse open https://linkedin.com/sales/search
agent-browser snapshot -i
# No CAPTCHA, no blocks - stealth browser handles it
```

### 3. Competitor Research (Protected Sites)

```bash
# Access sites with aggressive anti-bot
agent-browser -p browseruse open https://competitor-dashboard.com
agent-browser snapshot -i --json
agent-browser screenshot competitor.png
```

### 4. App Store Research

```bash
# iOS App Store (JS-heavy)
agent-browser open https://apps.apple.com/search?term=prayer
agent-browser snapshot -i --json
agent-browser get text @e1
```

### 5. Lead Generation

```bash
# Sales Navigator with auth
agent-browser -p browseruse --profile ~/.linkedin-profile open https://linkedin.com/sales
agent-browser snapshot -i
agent-browser fill @e2 "CEO fintech"
agent-browser click @e3
```

---

## Comparison: Current Tools vs New Stack

| Task | Current (Chrome MCP) | New (agent-browser) |
|------|---------------------|---------------------|
| Simple screenshot | Works | Works |
| JS-heavy pages | Often fails | Works |
| Anti-bot sites | Blocked | Stealth bypass |
| Login-required | Manual | Profile sync |
| AI workflow | Limited | Snapshot refs |
| Batch processing | Slow | Fast (Rust CLI) |
| Cloud scaling | No | Yes |

---

## Setup Guide for PRINTMAXX

### Step 1: Install Tools

```bash
# agent-browser (Vercel Labs)
npm install -g agent-browser
agent-browser install

# browser-use (Python)
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT
uv add browser-use
```

### Step 2: Get API Keys

1. **Browser Use Cloud** (RECOMMENDED)
   - Go to https://browser-use.com/cloud
   - Sign up (free $10 credits)
   - Get API key
   - Add to `.env`: `BROWSER_USE_API_KEY=xxx`

2. **Browserbase** (ALTERNATIVE)
   - Go to https://browserbase.com
   - Get API key + project ID
   - Add to `.env`: `BROWSERBASE_API_KEY=xxx`, `BROWSERBASE_PROJECT_ID=xxx`

### Step 3: Sync Profiles (Optional but Powerful)

```bash
# Sync your Chrome profile with logged-in sessions
export BROWSER_USE_API_KEY=your-key
curl -fsSL https://browser-use.com/profile.sh | sh
```

### Step 4: Add Claude Code Skill

```bash
npx skills add vercel-labs/agent-browser
```

### Step 5: Update BROWSER_AGENT_GUIDE.md

Add agent-browser to the fallback chain:

```
Chrome MCP fails
    ↓
agent-browser (local)
    ↓
agent-browser -p browseruse (cloud + stealth)
    ↓
Playwriter MCP
    ↓
Playwright scripts
```

---

## Security Considerations

### Profile Sync Safety

- Profile sync uploads cookies/localStorage to Browser Use cloud
- Only sync profiles for non-sensitive accounts
- Use separate Chrome profiles for work vs personal
- Never sync profiles with banking/payment sessions

### API Key Security

- Store in `.env`, never commit
- Use environment variables in scripts
- Rotate keys if exposed

### Session Isolation

```bash
# Use sessions for different tasks
agent-browser --session twitter open x.com
agent-browser --session linkedin open linkedin.com
# Sessions are isolated - one compromise doesn't affect others
```

---

## Cost Analysis

### Browser Use Cloud

| Usage | Cost |
|-------|------|
| Free credits | $10 on signup |
| Per browser minute | ~$0.01-0.03 |
| ChatBrowserUse model | $0.20/1M input, $2/1M output |

For our use case (research, scraping, not high-volume):
- Estimated: $5-20/month
- ROI: Hours saved on manual auth, anti-bot issues

### agent-browser Local

- Free (runs local Chromium)
- Only pay for cloud when needed (-p browseruse)

---

## Next Steps

1. **Install agent-browser** - `npm install -g agent-browser`
2. **Get Browser Use API key** - Free $10 to start
3. **Sync Twitter profile** - For authenticated bookmark extraction
4. **Test on protected site** - Verify anti-bot bypass works
5. **Update fallback chain** - Add to BROWSER_AGENT_GUIDE.md
6. **Create ralph loop** - For overnight research with stealth browsers

---

## References

- **agent-browser repo:** https://github.com/vercel-labs/agent-browser
- **browser-use repo:** https://github.com/browser-use/browser-use
- **Browser Use Cloud:** https://browser-use.com/cloud
- **Original tweet:** @shawn_pana (Jan 25, 2026)
- **Skill install:** `npx skills add vercel-labs/agent-browser`

---

## Alpha Rating

**ALPHA STATUS:** HIGHEST ROI

This solves our #1 browser automation pain point: accessing authenticated and protected sites programmatically. The profile sync feature alone is worth the setup time.

**Action Items:**
1. Install and test this week
2. Sync Twitter profile for bookmark extraction
3. Replace manual Chrome MCP workflows where applicable
4. Add to overnight ralph loops for protected site research
