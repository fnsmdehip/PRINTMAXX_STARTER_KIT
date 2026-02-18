# Tool Stack Reference

**Last Updated:** 2026-01-23
**Status:** Active

---

## Browser Automation Tools

### Current Setup: Chrome MCP

**What we use now:** Claude-in-Chrome MCP
- Direct Chrome control via extension
- Works for simple automation
- No additional setup needed

### Recommended Addition: Playwriter

**Repo:** [remorses/playwriter](https://github.com/remorses/playwriter)
**Stars:** 2.5k | **License:** MIT

**Why add it:**
- Controls YOUR actual Chrome window (not headless)
- Runs Playwright code in stateful sandbox
- @ryanvogel (prev Databricks/Neon) says "it's the bomb"
- Better for complex multi-step browser tasks

**Install:**
```bash
# 1. Install Chrome extension from Chrome Web Store
# 2. Add to Claude MCP config
```

### Alternative: Vercel agent-browser

**Repo:** [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
**Stars:** 10k | **License:** Apache-2.0

**What it is:** CLI for AI agents (not MCP)
**Use case:** Building standalone browser agents
**Status:** v0.7.5 (very active, released 6 hours ago)

**When to use:** If building dedicated browser automation agents outside Claude Code.

### Cloud QA: Browserbase agent-browse

**Repo:** [browserbase/agent-browse](https://github.com/browserbase/agent-browse)
**Stars:** 412

**What it is:** Claude Agent SDK + Stagehand for cloud browsers
**Use case:**
- Sandboxed, secure browser execution
- Session recording and debugging
- Scalable QA testing

**Install:**
```bash
npx skills add browserbase/agent-browse
```

**When to use:** Production QA at scale. Overkill for local dev.

---

## Browser Tool Decision Matrix

| Task | Best Tool |
|------|-----------|
| Quick screenshots, simple clicks | Chrome MCP |
| Complex multi-step flows | Playwriter |
| Building standalone browser agents | agent-browser (Vercel) |
| Production QA at scale | browserbase/agent-browse |
| Accessibility-tree based automation | Microsoft Playwright MCP |

---

## Cold Email & Outbound

| Tool | Cost | Purpose |
|------|------|---------|
| Instantly | $30/mo | Sending + warmup |
| Apollo | $49/mo | Contact data |
| Clay | $150/mo | Enrichment + intent signals |
| Close.com | $0-50/mo | CRM |

---

## Content & Automation

| Tool | Cost | Purpose |
|------|------|---------|
| Remotion | Free/OSS | Video generation |
| Buffer | $0-15/mo | Social scheduling |
| Playwright | Free/OSS | Browser automation scripts |

---

## Monitoring & Intelligence

| Tool | Cost | Purpose |
|------|------|---------|
| Visualping.io | $0-13/mo | Website change detection |
| Distill.io | Free tier | Change monitoring |
| appkittie.com | Free | App store movers |
| algrow.online | Free | YouTube termination tracking |

---

## App Development

| Tool | Cost | Purpose |
|------|------|---------|
| RevenueCat | Free-$99/mo | Subscription management |
| Expo | Free | React Native framework |
| Branch | Free tier | Deep linking + attribution |

---

## Research & Discovery

| Tool | Cost | Purpose |
|------|------|---------|
| IdeaBrowser.com | Free | Community signals |
| Listen Notes | Free tier | Podcast search |
| Crunchbase | Free tier | Funding data |
| USAspending.gov | Free | Government contracts |

---

## Roblox Game Development

### Roblox Studio MCP (Official - USE THIS)

**Source:** [Roblox DevForum Announcement](https://devforum.roblox.com/t/introducing-the-open-source-studio-mcp-server/3649365)
**Cost:** FREE | **License:** Open Source

**What it does:**
- Claude directly manipulates Roblox Studio
- Insert models from Creator Store
- Run Luau code via prompts
- Build entire games by describing what you want

**Setup:**
```bash
# 1. Have Roblox Studio + Claude Desktop
# 2. Download MCP plugin from devforum
# 3. Restart both apps
# 4. Prompt Claude, watch game build itself
```

**Example prompts:**
- "Make a zombie game"
- "Insert a cat and make it spin around really fast"
- "Make some trees from basic parts"
- "Attach a UI image and generate UI code"

**Money play:** Use your Claude Max subscription to pump out obby/tycoon/simulator games → monetize via Robux.

### Lux Plugin (Alternative)

**Source:** [Roblox DevForum](https://devforum.roblox.com/t/lux-cursorclaude-code-but-for-roblox-free-plugin/4207506)
**Cost:** FREE

**What it does:**
- Cursor/Claude Code but for Roblox
- Reads scripts, understands structure, makes changes
- Uses Gemini (cheaper than Claude)

**When to use:** If you want cheaper API costs (Gemini vs Claude).

### Clawdbot (DON'T USE FOR THIS)

**What it is:** Personal AI assistant via WhatsApp/Telegram/Discord
**Why skip:** You already have Claude Code Max. Clawdbot is a chat wrapper, not needed.

---

## BREAKTHROUGH TOOLS (January 2026)

### Sleepless Agent - 24/7 Claude Code Usage

**Repo:** [context-machine-lab/sleepless-agent](https://github.com/context-machine-lab/sleepless-agent)
**Stars:** 787 | **Status:** Active development

**THE BIG UNLOCK:** Sleep while Claude Code builds.

**What it does:**
- AgentOS daemon that runs Claude Code overnight via Slack
- Auto-processes tasks, manages Git commits/PRs
- Optimizes day/night usage thresholds for Claude Max
- Submit task via Slack, wake up to completed PR

**Setup:**
```bash
pip install sleepless-agent
sle daemon  # Start 24/7 daemon
```

**Use case:** Maximize your Claude Max subscription. Build 24 hours per day. Submit tasks before bed, review PRs in morning.

**ROI:** HIGHEST. If you have Claude Max, this 10x's your throughput.

---

### Vercel agent-browser - Fastest AI Browser Automation

**Repo:** [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
**Stars:** 10,121 | **Released:** January 11, 2026

**THE BIG UNLOCK:** Faster, more token-efficient browser automation than Playwright.

**What it does:**
- Rust CLI (Node.js fallback) for browser automation
- Accessibility-tree based (no screenshots = lower tokens)
- Reference-based clicking (@e2, @e3) instead of selectors
- Ultra-active development (10k stars in 2 weeks)

**Setup:**
```bash
npm install -g agent-browser
agent-browser install
agent-browser open example.com
agent-browser snapshot  # Get accessibility tree with refs
agent-browser click @e2 # Click by ref
```

**Use case:** Replace Playwright for AI-driven browser tasks. Faster, cheaper, better DX.

**ROI:** HIGHEST. Reduces token usage for browser automation by ~60%.

---

### BrowserWing - Visual Script Recording to MCP/Skills

**Repo:** [browserwing/browserwing](https://github.com/browserwing/browserwing)
**Stars:** 552

**THE BIG UNLOCK:** Stop writing browser automation prompts. Record once, export to Claude Skills.

**What it does:**
- Visual browser action recording
- Export to MCP commands or Claude Skills files
- 26+ HTTP API endpoints for full browser control
- LLM-powered semantic extraction

**Setup:**
```bash
npm install -g browserwing
browserwing --port 8080  # GUI at http://localhost:8080
```

**Workflow:**
1. Record browser actions visually
2. Edit script in GUI
3. Export to Claude Skill
4. Use skill repeatedly with natural language

**Use case:** Build reusable browser automation skills without prompt engineering.

**ROI:** HIGHEST. Eliminates repetitive browser automation prompts.

---

### Marketing Skills for AI Agents

**Repo:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
**Stars:** 4,243

**THE BIG UNLOCK:** Pre-built SEO/CRO/copywriting skills for Claude Code.

**What it includes:**
- CRO (conversion rate optimization)
- Copywriting frameworks
- SEO optimization
- Analytics interpretation
- Growth engineering workflows

**Setup:**
```bash
git clone https://github.com/coreyhaines31/marketingskills
# Copy relevant skills to .claude/skills/
```

**Use case:** Faster GTM optimization. Don't reinvent SEO/CRO workflows.

**ROI:** HIGHEST for content/marketing automation.

---

### OpenSkills - Universal Skills Loader

**Repo:** [numman-ali/openskills](https://github.com/numman-ali/openskills)
**Stars:** 6,948

**THE BIG UNLOCK:** Share skills across Claude Code, Cursor, Copilot.

**What it does:**
- Load skills from any source into any AI agent
- Browse skill libraries
- Universal format across tools

**Setup:**
```bash
npm install -g openskills
openskills browse  # Discover skills
openskills load <skill-id>  # Load into agent
```

**Use case:** Skill discovery and cross-tool compatibility.

---

### 200+ Curated Agent Skills

**Repo:** [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)
**Stars:** 2,163

**What it is:** Battle-tested skill collection for Claude Code/Cursor. Includes official Anthropic and Vercel skills.

**Use case:** Browse before building. Avoid reinventing common workflows.

---

## Tool Priority (Updated January 2026)

**MUST ADD:**
1. **Sleepless Agent** (if you have Claude Max) - 24/7 builds
2. **agent-browser** (replace Playwright) - Faster, cheaper browser automation
3. **BrowserWing** (for repeated browser tasks) - Visual recording to skills
4. **marketingskills** (for GTM optimization) - Pre-built SEO/CRO

**NICE TO HAVE:**
5. **OpenSkills** - Skill discovery
6. **antigravity-awesome-skills** - Skill library reference

---

## Notes

- **Playwriter vs Playwright MCP:** Different things. Playwriter (by @__morse) is an MCP that runs Playwright code. Playwright MCP (Microsoft) uses accessibility trees without screenshots.
- **agent-browser vs agent-browse:** Vercel's agent-browser is a CLI. Browserbase's agent-browse is a Claude skill for cloud browsers.
- **Clawdbot:** 7.1k stars, but just a chat interface to Claude. Skip if you have Claude Code.
- **Roblox MCP:** Official + free. Don't build a competitor - just use it to make games.
- **Sleepless Agent vs Ralph Loops:** Sleepless is Slack-based daemon for Claude Max. Ralph is local overnight build pattern. Use both together.
