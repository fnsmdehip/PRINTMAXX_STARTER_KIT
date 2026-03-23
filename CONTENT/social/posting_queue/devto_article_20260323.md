# Dev.to Article Draft - 2026-03-23
# Channel: Dev.to
# Status: READY TO POST (when Dev.to account is created)

---

## ARTICLE 1: The Claude Code Ebook Suite

**Title:** I Built 177 Apps With Claude Code in 44 Days. Here Are 9 Guides Covering Everything I Learned.

**Tags:** claudecode, ai, productivity, webdev

**Body:**

Over the past 44 days I've been running an autonomous development pipeline powered by Claude Code. The system generates apps from specs, deploys them, creates marketing content, and monitors uptime.

Along the way I documented every workflow, shortcut, and pattern that actually works in production (not just in demos).

I compiled everything into 9 focused guides:

**For developers:**
- **Claude Code Agent Bible** - How to build autonomous agent systems with cron jobs, filesystem state, and zero frameworks. The same architecture running 33 agents in production right now.
- **Claude Code Mastery** - Advanced patterns: parallel agents, worktrees, MCP servers, context management at scale.
- **Prompt Vault** - 100+ production-tested prompts for code generation, debugging, refactoring, and analysis.

**For non-developers:**
- **Claude Code for Solopreneurs** - Ship products without a technical co-founder. The spec-to-deploy pipeline.
- **Claude Code for Non-Technical Founders** - Managing Claude Code as a product development tool when you don't write code.
- **Claude Code for Content Creators** - Content pipelines, social media automation, bulk generation.

**For specific use cases:**
- **Cold Email System** - End-to-end cold outreach: lead scraping, scoring, personalization, sequence generation.
- **Reddit Money Machine** - How to find real demand signals in Reddit comments and turn them into products.
- **Before You Family Story Workbook** - A non-tech product built entirely with Claude Code.

The common thread: Claude Code is not just a coding assistant. It's a full business operations layer when you wire it into cron, filesystem state management, and multi-agent coordination.

All 9 are available as PDFs. Listing on Gumroad this week.

If you're using Claude Code and want the guide for your specific use case, let me know which one in the comments.

---

## ARTICLE 2: 33 Autonomous Agents, Zero Frameworks

**Title:** I Run 33 AI Agents in Production Using Only Cron Jobs and JSON Files. No LangChain. No Vector DBs.

**Tags:** ai, python, automation, devops

**Body:**

The AI agent ecosystem is obsessed with frameworks. LangChain, CrewAI, AutoGen, LangGraph. 10,000+ stars. Conference talks. Twitter threads.

I've been running 33 autonomous agents in production for 44 days. Here's the entire tech stack:

- Python scripts
- Cron jobs (launchd on macOS)
- JSON files for state
- The filesystem for communication
- Claude Code for the LLM layer

That's it.

### The Architecture

Each agent is a Python script that:
1. Reads its state from a JSON file
2. Reads inputs from other agents' output files
3. Does its work (scraping, analysis, content generation, deployment)
4. Writes its output to a file
5. Updates its state JSON
6. Exits

Cron runs each agent on a schedule. The "swarm brain" agent reads all other agents' outputs and makes routing decisions.

### Why This Works Better Than Frameworks

**Debuggability.** Every agent's state is a JSON file you can cat. Every decision is a line in a JSONL log. When something breaks, you read a file. You don't trace through 47 framework abstractions.

**Reliability.** Cron doesn't crash. If a script fails, cron runs it again next cycle. The script checks its state file and picks up where it left off. Crash recovery is automatic.

**Simplicity.** Adding a new agent = write a Python script + add a cron entry. No dependency graphs. No orchestrator configs. No YAML.

**Cost.** $0 infrastructure. No vector databases. No hosted agent platforms. Just your machine's cron daemon.

### The Agents

A few examples from the 33:

- **Lead Machine**: Scrapes business directories, scores websites on 8 dimensions, generates personalized cold emails.
- **Gap Hunter**: Scans all deployed assets, finds gaps (missing PDFs, broken links, undeployed builds), fixes what it can.
- **Competitor Stalker**: Monitors competitor pricing, features, and market positioning. Generates counter-move content.
- **System Healer**: Monitors disk usage, cron health, process counts. Auto-fixes common issues.

### The Results

- 177 sites/apps deployed
- 22 digital products with PDFs generated
- 1,274 content pieces in posting queue
- 192,700 business leads analyzed
- 17,484 hot leads identified

Revenue: $0. (The agents can't create Stripe accounts for me.)

### The Takeaway

Before reaching for a framework, ask: would a cron job and a JSON file solve this?

9 times out of 10, the answer is yes. And it'll be easier to debug at 3am when something breaks.

The boring stack wins in production.
