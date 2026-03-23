# REDDIT DISTRIBUTION — PROMPTVAULT + MCP MARKETPLACE
# Generated: 2026-03-22 23:05
# Apps: promptvault.surge.sh, mcp-marketplace.surge.sh
# Distribution cycle: 31

---

## r/ClaudeAI (85K members) — VALUE POST
Title: Built a free prompt vault for Claude power users — stores your best prompts locally, no account

Body:
I keep my highest-value Claude prompts in a note on my phone. It's terrible.

Built promptvault.surge.sh as a browser-based library.

What it does:
- Store prompts by category (code review, debugging, writing, research, etc.)
- Tag and search them
- Copy with one click
- Everything stores in localStorage — nothing goes to a server

Prompts I keep there that made a real difference:
- "You are a senior security engineer. Review this code for OWASP top 10 vulnerabilities. Be specific about line numbers."
- "Rewrite this function so it handles edge cases. List every edge case you considered."
- "Act as an adversarial user trying to break this system. What would you try?"

Free: promptvault.surge.sh

What prompts do you use daily that you wish you had faster access to?

---

## r/ChatGPT (6.4M members) — VALUE POST
Title: I built a local prompt library because I kept re-writing the same prompts from memory

Body:
Every few weeks I'd re-invent the same "act as a code reviewer" prompt because I couldn't remember the exact wording from the version that worked best.

Built promptvault.surge.sh — a local prompt library that lives in your browser.

Features:
- Categories: code, writing, research, emails, creative
- Search by keyword
- One-click copy
- 100% local, no account, no sync (intentional — if it synced, I'd have to trust a server)

Works with ChatGPT, Claude, Gemini, or any LLM you use.

Free: promptvault.surge.sh

---

## r/PromptEngineering (95K members) — VALUE POST
Title: Prompt library tool for teams and solos — stores locally, no backend required

Body:
Built promptvault.surge.sh for personal prompt management.

The specific problem it solves: most prompt managers are either cloud-based (requires trust + account) or just a markdown file (no searchability).

This one:
- Runs in browser
- Searchable
- Categorizable
- localStorage only — no backend
- Can be self-hosted (it's a static site)

For personal prompt libraries or for teams that want to share a prompt vault without setting up a server, might be useful.

The source is straightforward HTML/CSS/JS if anyone wants to fork and extend it.

---

## r/mcp (growing community) — VALUE POST
Title: Made a vetted MCP server directory after the OpenClaw security issues

Body:
The OpenClaw incident was a useful reminder that "popular" doesn't mean "safe" in the MCP ecosystem.

Built mcp-marketplace.surge.sh as a filterable directory with basic quality signals.

What's different from just searching GitHub:
- Trust ratings based on org reputation and code audit
- Maintenance status (last commit, issue response time)
- Known issues highlighted
- License visibility
- Access scope (what the server can touch on your system)

MCP servers often have filesystem access, browser access, and credential access. Basic due diligence before running one seemed worth automating into a directory.

Currently ~80 servers. Adding more based on community suggestions.

Free static site: mcp-marketplace.surge.sh

---

## r/LocalLLaMA / r/MachineLearning — DISCUSSION POST
Title: How do you evaluate MCP servers before running them? Looking for community standards

Body:
After the OpenClaw vulnerability disclosure, I've been thinking about the right evaluation criteria for MCP servers before integrating them.

My current criteria:
1. Org reputation (large known org = more trust than random GitHub user)
2. License (MIT/Apache vs proprietary)
3. Star count AND maintenance activity (stars alone mean nothing)
4. Code review: any dynamic code execution? Any network calls to external services?
5. What access scope it requests (filesystem, browser, credentials)

Built a directory (mcp-marketplace.surge.sh) that applies these signals to ~80 servers.

Curious what criteria others use — especially for servers that handle credentials or filesystem access.
