# Browser Automation Fallback Chain (10 Options)
**Last updated:** 2026-02-05
**Extracted from:** CLAUDE.md for context savings

---

## Core principle

When browser tasks fail, automatically try the next tool. Don't ask user.

**Full guide:** `OPS/BROWSER_CONTROL/BROWSER_AGENT_GUIDE.md`

---

## Complete tool arsenal (10 options)

| Priority | Tool | Best For | Install/Access |
|----------|------|----------|----------------|
| 1 | **Chrome MCP** | Simple tasks, logged-in sessions | Pre-installed Claude Desktop |
| 2 | **agent-browser** (Vercel Labs) | AI-optimized, snapshot refs, anti-bot | `npm install -g agent-browser` |
| 3 | **Playwriter MCP** | Control YOUR Chrome, complex flows | Chrome extension + MCP config |
| 4 | **Playwright MCP** (Microsoft) | Headless, accessibility tree | `npm install @anthropic/mcp-playwright` |
| 5 | **Bash + Playwright scripts** | Custom scripts, batch ops | `npx playwright test script.ts` |
| 6 | **Selenium** | Legacy scripts, cross-browser | `pip install selenium` + chromedriver |
| 7 | **Python requests** | APIs, JSON endpoints (Reddit!) | `pip install requests` |
| 8 | **Browserbase** | Cloud isolation, stealth | `npx skills add browserbase/agent-browse` |
| 9 | **Claude Browser Extension** | Manual assist, last resort | Chrome Web Store |
| 10 | **Manual console extraction** | When all else fails | Copy/paste from DevTools |

---

## Automatic fallback chain (DO THIS WITHOUT ASKING)

```
Chrome MCP fails (blank page, timeout, JS error)
    ↓ TRY NEXT AUTOMATICALLY
agent-browser (AI-optimized refs)
    ↓ TRY NEXT AUTOMATICALLY
agent-browser -p browseruse (stealth cloud)
    ↓ TRY NEXT AUTOMATICALLY
Playwriter MCP (controls real Chrome)
    ↓ TRY NEXT AUTOMATICALLY
Playwright script via Bash
    ↓ TRY NEXT AUTOMATICALLY
Python requests (for APIs like Reddit)
    ↓ TRY NEXT AUTOMATICALLY
Selenium (legacy fallback)
    ↓ TRY NEXT AUTOMATICALLY
Browserbase cloud browser
    ↓ TRY NEXT AUTOMATICALLY
Claude browser extension (human assist)
    ↓ LAST RESORT
Manual console extraction
```

---

## Tool details

### Priority 1: Chrome MCP (default)
```
Tools: mcp__Claude_in_Chrome__*
- tabs_context_mcp, navigate, computer, read_page, find, form_input, get_page_text
```
Best for simple interactions where user is logged in.

### Priority 2: agent-browser (Vercel Labs)
```bash
npm install -g agent-browser && agent-browser install
agent-browser open https://example.com
agent-browser snapshot -i --json  # Get refs (@e1, @e2)
agent-browser click @e1
# For anti-bot: agent-browser -p browseruse open https://protected.com
```
Best for AI-optimized automation, anti-bot bypass, persistent auth sessions.

### Priority 3: Playwriter MCP
**Repo:** github.com/remorses/playwriter (2.5k stars)
Controls YOUR Chrome - sees logged-in sessions, real user context.
Install Chrome extension + add to MCP config.

### Priority 4: Playwright MCP (Microsoft)
Headless testing, accessibility selectors.

### Priority 5: Bash + Playwright scripts
```bash
cd AUTOMATIONS && npx playwright test scraper.spec.ts
python AUTOMATIONS/twitter_alpha_scraper.py
```

### Priority 6: Selenium (legacy)
```python
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/path/to/profile")
driver = webdriver.Chrome(options=options)
```

### Priority 7: Python requests (API-based, no browser)
```python
import requests
# Reddit JSON API - bypasses ALL browser detection!
resp = requests.get("https://www.reddit.com/r/SaaS/top.json?t=week",
                    headers={'User-Agent': 'Mozilla/5.0'})
posts = resp.json()['data']['children']
```
Reddit blocks Playwright/Selenium but requests works.

### Priority 8: Browserbase cloud
`npx skills add browserbase/agent-browse`
Best for production QA, sandboxed execution, stealth.

### Priority 9: Claude browser extension
User opens page → activates extension → Claude analyzes content.

### Priority 10: Manual console extraction
See: `AUTOMATIONS/x_bookmarks/MANUAL_EXTRACTION_WORKFLOW.md`

---

## Platform-specific tool selection

| Platform | Recommended | Why |
|----------|-------------|-----|
| **Reddit** | Python `requests` (JSON API) | Blocks all browsers, JSON works |
| **Twitter/X** | agent-browser --profile | Needs auth, stealth helps |
| **LinkedIn** | agent-browser -p browseruse | Heavy anti-bot |
| **GitHub** | requests or Chrome MCP | Easy access |
| **App Store** | Chrome MCP | Simple pages |
| **TikTok** | agent-browser -p browseruse | Anti-bot |
| **Product Hunt** | requests or Chrome MCP | Easy access |

## Task-to-tool quick reference

| Task | Primary | Fallback 1 | Fallback 2 |
|------|---------|------------|------------|
| Screenshot webpage | Chrome MCP | agent-browser | Playwright |
| Twitter/X content | agent-browser | Chrome MCP (logged in) | Manual |
| Reddit scraping | requests (JSON API) | agent-browser | Manual |
| Multi-step login | agent-browser | Playwriter | Selenium |
| Anti-bot sites | agent-browser -p browseruse | Browserbase | Manual |
| Batch URLs | Playwright script | agent-browser CLI | Selenium |

## When Chrome MCP fails

Don't stop and ask. Just try the next tool:

1. Blank/broken page → agent-browser or Playwriter
2. Timeout → agent-browser wait command
3. Can't find element → agent-browser `snapshot -i --json`
4. Twitter JS error → agent-browser --profile
5. Anti-bot detected → agent-browser -p browseruse
6. Reddit blocked → Python requests (JSON API)
7. Auth session needed → agent-browser --profile
