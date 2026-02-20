# memento v2: system architecture proposal

**Status:** PENDING_USER_APPROVAL
**Date:** 2026-02-19
**Author:** research swarm (4 parallel agents, 80+ sources)

**DO NOT IMPLEMENT until user approves this document.**

---

## what this is

a proposal to upgrade the current memento system (62 Ralph loops, factory, wave orchestration, budget routing) into a self-improving autonomous operations platform.

based on 4 parallel research agents analyzing: 10 agent architectures, 50+ MCP servers, self-improving agent patterns (SICA, DARWIN, DSPy, GEPA), production deployment data (Cleanlab, Google, Amazon), memory systems (Mem0, Zep, FadeMem), guardrails (Anthropic, NeMo, Guardrails AI), monetization funnels, and competitive positioning.

the core insight from the research: the pattern works. 72% of enterprises deploying agents see ROI in year one (Google 2025 data). but only 1-5% get past pilot stage (Cleanlab). the gap is not capability. it's memory, self-improvement, and integration. that's what v2 addresses.

---

## current system (what we have)

```
CURRENT MEMENTO (v1)
├── Core: Ralph stateless resampling (Huntley's pattern)
├── Factory: generates 182 loop configs from spreadsheet
├── Orchestration: wave-based DAG (3 waves, 11 agents)
├── Budget routing: Opus/Sonnet/Haiku by trust level
├── State: 3 flat files (HEARTBEAT.md, active-tasks.md, logs)
├── Recovery: checkpoint files
└── Scale: 62 loops, 282 scripts, 57 cron jobs, 2 MacBooks
```

**what works:** stateless pattern eliminates context rot (0 incidents). budget routing keeps costs predictable. factory saves hours on loop setup. runs on consumer hardware.

**what's missing:**
1. no self-improvement loop (agents don't learn from outcomes)
2. no semantic memory (flat files, no search, no relationships)
3. no verification (agent does and judges its own work)
4. no MCP integration (tools are hardcoded per loop)
5. no alpha quality scoring (no signal vs noise filtering)
6. no prompt mutation (prompts are static forever)
7. no guardrails framework (ad-hoc safety, not systematic)
8. no integration layer (each loop is an island)

---

## proposed system (memento v2)

### architecture overview

```
MEMENTO V2
├── Layer 0: CORE LOOP (unchanged — Ralph stateless resampling)
│   └── while :; do cat PROMPT.md | claude --print; done
│
├── Layer 1: MEMORY (replaces flat files)
│   ├── Short-term: context window (<40% utilization, Chroma research)
│   ├── Medium-term: filesystem + progress.txt (session-to-session)
│   ├── Long-term: Zep/Graphiti temporal knowledge graph
│   └── Procedural: trajectory store (successful run patterns)
│
├── Layer 2: VERIFICATION (new — Judge Agent pattern)
│   ├── Worker Agent: does the task
│   ├── Judge Agent: read-only verification, can approve or reject
│   └── Feedback injection: rejections become next iteration context
│
├── Layer 3: SELF-IMPROVEMENT (new)
│   ├── Trajectory storage: successful runs saved as few-shot examples
│   ├── Prompt mutation: DSPy/MIPROv2 Bayesian optimization
│   ├── Performance tracking: JSON memory correlating changes to outcomes
│   └── Constitutional self-correction: agent self-critiques against principles
│
├── Layer 4: INTEGRATION (new — MCP-first)
│   ├── Composio: 500+ managed integrations
│   ├── MCP servers: Tavily search, Resend email, Telegram, GitHub
│   ├── Figma MCP: design-to-code pipeline
│   ├── Image gen MCP: Flux/DALL-E for asset generation
│   ├── Google Sheets MCP: spreadsheet data access
│   └── Custom MCPs: domain-specific tools
│
├── Layer 5: GUARDRAILS (new — 4-layer defense)
│   ├── Input: prompt injection detection
│   ├── Reasoning: constrained decision space
│   ├── Action: whitelist approved tools, risk-based autonomy
│   └── Output: PII scanning, quality validation, LLM-as-judge
│
├── Layer 6: ORCHESTRATION (upgraded)
│   ├── Queen-worker hierarchy (from Claude Flow)
│   ├── Typed specializations (researcher, coder, analyst, etc.)
│   ├── Consensus mechanisms for multi-agent decisions
│   └── File ownership maps (existing, works)
│
└── Layer 7: ALPHA ENGINE (new)
    ├── Signal scoring: LLM-as-judge (80%+ human agreement)
    ├── Novelty detection: embedding-based deduplication
    ├── Trend correlation: cross-source pattern matching
    ├── Method mutation: test variations of working tactics
    └── Forgetting curve: FadeMem-style decay for stale intel
```

---

### layer 1: memory (the biggest upgrade)

**the research says:** Stanford/Harvard found "memory over reasoning" — agents storing short structured lessons outperform agents with longer reasoning chains. Mem0 shows 26% improvement over baseline. Zep shows 18.5% higher accuracy.

**current state:** 3 flat files. works for crash recovery but can't answer "what patterns worked last month?" or "has this alpha been seen before?"

**proposed:**

| Memory Type | Implementation | Purpose | Cost |
|-------------|---------------|---------|------|
| **Short-term** | Context window management | Current iteration | Free (already doing) |
| **Medium-term** | progress.txt + SHARED_TASK_NOTES.md | Inter-session continuity | Free (already doing) |
| **Long-term** | Zep Graphiti (self-hosted) | Temporal knowledge graph with edge invalidation | Free (MIT, runs on laptop) |
| **Procedural** | JSONL trajectory store | Successful run patterns for few-shot | Free (file on disk) |

**why Zep over Mem0:** Zep's temporal knowledge graph tracks when facts become invalid. critical for alpha intel that expires. Mem0 is better for general-purpose memory but doesn't handle temporal invalidation natively. Zep is MIT licensed, can run on a MacBook.

**implementation:**
```bash
# Install Zep (MIT, Python)
pip install graphiti-core

# Each loop iteration:
# 1. Read relevant memories before task
# 2. Execute task
# 3. Write structured learnings after task
# 4. Zep auto-invalidates contradicted facts
```

**the forgetting curve (FadeMem pattern):**
- alpha older than 30 days without revalidation: flagged STALE
- alpha older than 90 days without revalidation: auto-archived
- frequently accessed memories strengthen (mimics human recall)
- semantic relevance modulates decay rate

---

### layer 2: verification (Judge Agent)

**the research says:** Vercel's Ralph implementation separates execution from verification. the agent doing the work is NOT the agent evaluating the work. the Judge has read-only access — can't "fix" problems by modifying code.

**proposed:**

```
WORKER LOOP:
  while :; do
    cat PROMPT.md | claude --print  # worker does task
    cat VERIFY.md | claude --print  # judge evaluates (read-only)
    if [judge approves]; then
      commit and move to next task
    else
      inject feedback into next iteration context
    fi
  done
```

**Judge Agent rules:**
- read-only file access (cannot modify work)
- evaluates against success criteria from prd.json
- returns structured verdict: APPROVE or REQUEST_CHANGES with specific feedback
- feedback becomes the first thing the worker reads in next iteration

**cost:** one additional LLM call per iteration (use Haiku for the judge — fast, cheap, good enough for yes/no evaluation)

---

### layer 3: self-improvement

**the research says:** SICA improved from 17% to 53% on SWE-Bench by editing its own code. DSPy/MIPROv2 uses Bayesian optimization to find better prompts automatically. DARWIN uses evolutionary prompt mutation with fitness evaluation.

**proposed approach (conservative, not SICA-level):**

1. **trajectory storage:** save successful runs as few-shot examples
   ```
   TRAJECTORIES/
   ├── research_success_001.json  # what worked for research tasks
   ├── content_success_001.json   # what worked for content generation
   └── alpha_success_001.json     # what worked for alpha extraction
   ```
   each trajectory includes: input state, actions taken, outcome, metrics.
   new iterations read the top 3 most relevant trajectories as few-shot examples.

2. **prompt mutation (monthly cadence):**
   - take current PROMPT.md
   - generate 3 variants using DSPy
   - run each variant on 10 historical tasks
   - pick the winner by measured outcome quality
   - winner becomes new PROMPT.md
   - this is the DARWIN pattern simplified

3. **performance tracking:**
   ```jsonl
   {"date":"2026-02-19","loop":"research_01","prompt_version":"v3","success_rate":0.87,"avg_time":45}
   {"date":"2026-02-19","loop":"research_01","prompt_version":"v4","success_rate":0.91,"avg_time":42}
   ```
   correlate prompt changes to outcome changes. propagate what works.

4. **constitutional self-correction:**
   - before finalizing output, agent checks against quality principles
   - "does this contain specific numbers?" "is the source credible?" "would this pass the alpha review criteria?"
   - this is Anthropic's Constitutional AI pattern applied to business ops

---

### layer 4: integration (MCP-first)

**the research says:** Goose (27K stars, backed by Block) proves MCP-first architecture works. all tools are MCP servers. adding a new capability = adding a new MCP server. no core code changes.

**proposed MCP stack:**

| Category | MCP Server | Purpose | Cost |
|----------|-----------|---------|------|
| **Search** | Tavily | Web search for research agents | ~$0.01/search, free tier available |
| **Email** | Resend | Automated email sending | Free tier (100/day) |
| **Messaging** | Telegram | Bot notifications, alerts | Free |
| **Git** | Official MCP Git | Repository operations | Free |
| **Data** | Google Sheets MCP | Spreadsheet read/write | Free |
| **Design** | Figma MCP | Design-to-code pipeline | Free (official) |
| **Images** | Flux via Replicate | Asset generation | ~$0.003/image |
| **Files** | Filesystem MCP | File operations | Free (official) |
| **Sequential** | Sequential Thinking | Structured problem solving | Free (official) |
| **Browser** | Playwright MCP | Web automation | Free |
| **Integration** | Composio | 500+ unified integrations | Free tier (1K actions/mo) |

**implementation:** Claude Code already supports MCP natively. add to `~/.claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "tavily": { "command": "npx", "args": ["-y", "tavily-mcp"], "env": { "TAVILY_API_KEY": "..." } },
    "resend": { "command": "npx", "args": ["-y", "mcp-resend"], "env": { "RESEND_API_KEY": "..." } },
    "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"] }
  }
}
```

---

### layer 5: guardrails (4-layer defense)

**the research says:** Anthropic's framework: treat tool access like production IAM, start from deny-all. NeMo Guardrails: 50% better protection with ~0.5s latency. guardrails should be defense-in-depth, not single-point.

**proposed:**

```
LAYER 1 — INPUT GUARD
├── Prompt injection detection (NeMo Guardrails NIM)
├── Input validation (schema enforcement)
└── Source trust classification (internal=trusted, external=untrusted)

LAYER 2 — REASONING GUARD
├── Tool whitelist per loop (deny-all default)
├── File ownership maps (agent A cannot write agent B's files)
└── Scope constraints (research agents can't execute purchases)

LAYER 3 — ACTION GUARD
├── Risk-based autonomy levels:
│   ├── LOW RISK (auto): file read, research, analysis, content draft
│   ├── MEDIUM RISK (log): file write, git commit, API calls
│   ├── HIGH RISK (confirm): email send, social post, git push
│   └── CRITICAL (block): payment, account creation, delete operations
├── Hard daily spend caps (existing, works)
└── Rate limiting per tool per loop

LAYER 4 — OUTPUT GUARD
├── PII scanning before any external output
├── LLM-as-judge quality check (80%+ human agreement)
├── Compliance scanner (existing: AUTOMATIONS/compliance_scanner.py)
└── Cryptographically signed audit logs
```

**key principle from the research:** "human escalation as a tool call." HIGH RISK actions trigger a notification (Telegram bot) asking for approval. agent continues with other tasks while waiting. no blocking.

---

### layer 6: orchestration (upgraded)

**current:** 3-wave DAG with file ownership maps. works for sequential pipelines.

**proposed additions (inspired by Claude Flow):**

1. **typed agent specializations:**
   - RESEARCHER: web search, API calls, read-only file access
   - ANALYST: data processing, scoring, read + write own output files
   - GENERATOR: content creation, image gen, write to output directories
   - EXECUTOR: deployment, email, social posting (highest risk, most guardrails)
   - JUDGE: verification only, read-only, cannot modify work

2. **queen-worker pattern for complex tasks:**
   - queen agent reads the task, breaks it into subtasks
   - assigns each subtask to the appropriate specialist
   - collects results, resolves conflicts
   - useful for multi-step research or content campaigns

3. **consensus for critical decisions:**
   - for HIGH RISK actions, run 2 agents independently
   - if they agree: proceed
   - if they disagree: escalate to human
   - this is the "measure twice, cut once" pattern

---

### layer 7: alpha engine

**the research says:** Man Group's AlphaGPT is the only production multi-agent alpha discovery system. it works: produced dozens of live trading signals. the pattern: mine data, formulate hypothesis, challenge the reasoning, approve for deployment.

**proposed for memento:**

1. **signal scoring (replace manual PENDING_REVIEW):**
   ```
   ALPHA PIPELINE (v2):
   ├── SCRAPE (existing scrapers, 350+ sources)
   ├── EXTRACT (LLM extracts structured claims)
   ├── SCORE (LLM-as-judge, 0-100, calibrated against human reviews)
   ├── DEDUPLICATE (embedding similarity, Zep handles this)
   ├── CHALLENGE (adversarial agent questions the claim)
   ├── ROUTE (auto-route based on category + score)
   └── TRACK (measure if the alpha actually worked)
   ```

2. **novelty detection:**
   - embed each new alpha entry
   - compare against existing embeddings in Zep
   - similarity > 0.85 = duplicate, auto-archive
   - similarity < 0.3 = truly novel, flag for priority review

3. **method mutation:**
   - for alpha entries marked APPROVED and deployed
   - automatically generate 3 variations of the tactic
   - A/B test the variations
   - propagate winners (DSPy/MIPRO pattern applied to business tactics)

4. **temporal decay:**
   - alpha entries get a freshness score
   - FadeMem-style decay: unused intel fades over time
   - frequently accessed intel strengthens
   - tech alpha decays faster (30-day half-life)
   - evergreen alpha decays slower (180-day half-life)

---

## implementation plan (if approved)

### phase 1: foundation (week 1-2)
- install Zep/Graphiti for temporal knowledge graph
- implement Judge Agent pattern in 3 pilot loops
- set up trajectory storage (JSONL, simple)
- install 5 core MCP servers (Tavily, Resend, Telegram, Git, Filesystem)
- implement 4-layer guardrails config
- estimated cost: $0 (all open source)

### phase 2: self-improvement (week 3-4)
- implement prompt mutation pipeline (monthly cadence)
- set up performance tracking JSONL
- build alpha scoring pipeline (LLM-as-judge)
- implement novelty detection (embedding similarity)
- connect Telegram bot for human escalation
- estimated cost: ~$20/mo (Tavily API + Replicate images)

### phase 3: integration (week 5-6)
- add remaining MCP servers (Figma, Sheets, Images)
- implement Composio for unified auth
- upgrade orchestration to queen-worker pattern
- build alpha challenge agent (adversarial verification)
- estimated cost: ~$30/mo additional

### phase 4: optimization (ongoing)
- monthly prompt mutation cycles
- weekly alpha pipeline calibration
- trajectory store growing (more few-shot examples)
- Zep knowledge graph building context
- constitutional AI refinement

### total estimated monthly cost increase: ~$50/mo
(mostly API calls for Tavily search + image generation. everything else is self-hosted, MIT licensed, runs on the existing 2 MacBooks)

---

## what this does NOT include (and why)

1. **no vector database** — Zep's knowledge graph subsumes what a vector DB would do, with better temporal reasoning. adding Pinecone or Milvus would be over-engineering.

2. **no custom model training** — prompt mutation via DSPy is cheaper and faster than fine-tuning. model access is commoditized (McKinsey: 79% of orgs report competitors making similar AI investments). the edge is data and speed, not model weights.

3. **no Kubernetes/cloud deployment** — runs on 2 MacBooks. that's a feature, not a limitation. simpler = fewer failure modes. move to cloud only when the MacBooks can't keep up.

4. **no blockchain/crypto for audit trails** — signed log files are sufficient. blockchain would be resume-driven development.

5. **no abandoning Ralph for OpenHands/SWE-agent** — those are better for coding tasks specifically. we're running business ops. the unconstrained Ralph pattern is more appropriate for general-purpose operations.

---

## competitive positioning (honest)

| System | Stars | Best At | Where Memento v2 Fits |
|--------|-------|---------|----------------------|
| OpenHands | 65K | Coding tasks, event sourcing | Better architecture, but coding-only |
| SWE-agent | 18K | Code issue resolution | More rigorous for dev, not for biz ops |
| snarktank/ralph | 10.6K | Simple loop implementation | Simpler, which is a feature if you don't need ops tooling |
| Claude Flow | 14K | Multi-agent swarm | Queen-worker pattern, but claims need verification |
| Goose | 27K | Model-agnostic MCP-first | MCP-first design we're adopting |
| Memento v2 | — | Business ops at scale | Factory + waves + budget + self-improvement + alpha engine |

**the real moat (from the research):** not the code. it's the data flywheel. more operations = more trajectories = better few-shot examples = better operations. the speed of the improvement loop is the competitive advantage. 79% of orgs report competitors making similar AI investments. the difference: how fast you go from insight to deployed improvement.

---

## open questions for user

1. **Zep vs flat files:** Zep adds power but also complexity. do you want the temporal knowledge graph, or is the current 3-file system sufficient?

2. **Judge Agent cost:** adds one Haiku call per iteration (~$0.002/iteration, ~$0.12/night for 62 loops). worth it for quality verification?

3. **Telegram notifications:** for HIGH RISK action approval. or prefer a different channel?

4. **Monthly prompt mutation:** automated monthly, or manual trigger?

5. **Alpha challenge agent:** adversarial verification of alpha claims. useful but doubles alpha processing cost. worth it?

---

## ADDENDUM: additional systems (2026-02-19)

based on additional research and user requirements. these items integrate with the 7-layer architecture above. same rule: **DO NOT IMPLEMENT until user approves.**

---

### addendum 1: OpenClaw gateway integration — CONDITIONAL (security hardening required)

**STATUS: CONDITIONAL. core daemon usable as model router ONLY with full hardening. ClawHub skills PERMANENTLY BLOCKED.**

**the nuanced picture:** OpenClaw has two distinct attack surfaces. ClawHub skills marketplace was catastrophically compromised (1,184 malicious skills, AMOS stealer). the core daemon ALSO had its own CVEs (CVSS 8.8 RCE, command injection), but these are patched in v2026.2.12. using the core as a model router with zero skills installed is defensible.

**see `OPS/SECURITY_ARCHITECTURE_PRINTMAXX.md` for full security assessment.**

**if using OpenClaw core (optional, not required):**
1. v2026.2.12+ only (all known CVEs patched)
2. Docker container, localhost-only binding
3. zero skills installed, no ClawHub interaction
4. monitored with LuLu + BlockBlock
5. monthly CVE audit
6. Laptop 2 only (isolated from control node)
7. kill switch: if new unpatched CVE drops, disable immediately

**alternative (simpler, recommended):** Claude Code on Laptop 1, Codex CLI on Laptop 2. or LiteLLM for unified routing. same functionality, less attack surface.

**key context:**
- Pieter Levels: "too scared to run it on any production server." uses Claude Code via SSH more than OpenClaw.
- Karpathy: reversed from "incredible sci-fi" to "dumpster fire."
- Steinberger joined OpenAI Feb 14. project moving to foundation.
- most real users use core routing only, not skills marketplace.
- NanoClaw emerging as lightweight container-isolated alternative built on Anthropic's Agents SDK.

~~**what it is:** OpenClaw (by Peter Steinberger, 200K+ GitHub stars) is an open-source AI agent gateway that routes through ChatGPT/Codex subscriptions via OAuth. flat $20/mo for unlimited tokens instead of per-token API billing.~~

~~**why it matters:** at 1.3M+ tokens/month (which we easily exceed), the $20/mo subscription is cheaper than API. plus access to gpt-5.3-codex (highest tier model) via Codex CLI, which is better than the o5.2 thinking available through the ChatGPT app.~~

**architecture:**

```
LAPTOP 1 (control node — this MacBook)
├── Claude Code (primary — Opus/Sonnet/Haiku)
├── Direct API routing (current setup)
└── Fallback: OpenClaw gateway on Laptop 2

LAPTOP 2 (worker node — separate MacBook)
├── OpenClaw daemon (port 18789)
├── Primary: openai-codex/gpt-5.3-codex ($20/mo flat)
├── Fallback 1: anthropic/claude-opus-4-5 (API)
├── Fallback 2: anthropic/claude-sonnet-4-20250514 (API)
└── Native MCP support + Ralph loop support
```

**setup commands:**
```bash
# Install
npm install -g openclaw@latest

# Onboard with OpenAI Codex OAuth
openclaw onboard --auth-choice openai-codex --install-daemon

# Set highest-tier model
openclaw models set openai-codex/gpt-5.3-codex

# Verify
openclaw models status --plain
```

**config file (`~/.openclaw/openclaw.json`):**
```json
{
  "gateway": { "port": 18789 },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai-codex/gpt-5.3-codex",
        "fallbacks": [
          "anthropic/claude-opus-4-5",
          "anthropic/claude-sonnet-4-20250514"
        ]
      }
    }
  }
}
```

**known issues:**
- rate limiting bug (#5159): exponential backoff doesn't work as documented. retry intervals shorter than expected.
- provider-level cooldown (#5744): hitting rate limit on one OpenAI model blocks ALL OpenAI models temporarily.
- workaround: fallback chain to Anthropic models when OpenAI throttles.

**cost:** $20/mo (ChatGPT subscription). breaks even vs API at ~1.3M tokens/month.

**integration with v2:** OpenClaw becomes the model routing layer for Laptop 2. the unified instruction set (see addendum 6) gets loaded into OpenClaw's agent config. Ralph loops on Laptop 2 route through OpenClaw instead of direct API.

---

### addendum 2: tweet freshness decay (time-based alpha relevance)

**what it is:** scoring system that reduces the relevance of alpha entries over time, with different decay rates based on content type. prevents building on stale intel.

**why it matters:** a TikTok hack from 3 weeks ago might be patched. a cold email framework is evergreen. the system needs to distinguish.

**proposed decay curves:**

| Content Type | Half-Life | Examples |
|-------------|-----------|---------|
| **Platform exploit** | 7 days | TikTok algorithm hacks, API loopholes |
| **Trending format** | 14 days | Viral tweet structures, meme formats |
| **Tool alpha** | 30 days | New tools, pricing changes, feature launches |
| **Growth tactic** | 60 days | Cold email frameworks, SEO strategies |
| **Evergreen method** | 180 days | Business models, monetization structures |
| **First principles** | never decays | Fundamentals of human psychology, economics |

**formula:**
```
relevance_score = original_score × (0.5 ^ (days_since_discovery / half_life))
```

**implementation:** add 3 fields to ALPHA_STAGING.csv:
- `content_type`: which decay curve to use
- `discovered_at`: timestamp
- `freshness_score`: auto-calculated, updated daily by cron

**auto-triggers:**
- freshness_score < 0.3 → status changes to `STALE`
- freshness_score < 0.1 → auto-archived
- any alpha used in content generation refreshes its timestamp (accessed = strengthened, FadeMem pattern)

**integration with v2:** this IS the "forgetting curve" described in Layer 7 (Alpha Engine), now with specific decay rates by content type. the nightly cron job runs the decay calculation across all alpha entries. Zep's temporal invalidation (Layer 1) handles the knowledge graph side.

---

### addendum 3: niche meta detector enhancement (auto-discovery)

**what it is:** upgrade the existing `niche_meta_detector.py` (30 niches, pattern matching) to auto-discover NEW metas instead of only matching known patterns.

**current state:** niche_meta_detector.py detects known patterns (Ghibli, Saratoga, Routine, Molt) across 30 niches (N001-N030). but it can't find NEW patterns — only matches ones we've already defined.

**proposed upgrade:**

```
NICHE META DETECTOR v2
├── KNOWN PATTERN MATCHING (existing — keep)
│   └── 30 niches × known patterns → match/no-match
│
├── NEW META DISCOVERY (new)
│   ├── Engagement spike detection
│   │   └── "This niche's avg engagement jumped 3x in 7 days — why?"
│   ├── Hashtag velocity tracking
│   │   └── "New hashtag went from 0 to 10K uses in this niche"
│   ├── Format shift detection
│   │   └── "This niche shifted from text to video/carousel — new meta"
│   ├── Cross-niche pattern transfer
│   │   └── "Pattern working in fitness just appeared in faith niche"
│   └── Source monitoring (Reddit, Twitter, Product Hunt)
│       └── "New tool/framework gaining traction in this niche"
│
└── OUTPUT ROUTING (new)
    ├── Tweet meta → CONTENT/social/{niche}/ (content queue)
    ├── Info product meta → DIGITAL_PRODUCTS/ideas/ (product spec)
    ├── App meta → MONEY_METHODS/APP_FACTORY/opportunities/ (app spec)
    └── General meta → LEDGER/NICHE_METAS.csv (tracking)
```

**per-niche outputs:**
- **tweet structures**: what formats are getting engagement NOW in this niche
- **info product angles**: what problems people are paying to solve NOW
- **app opportunities**: what tools people are requesting NOW
- **content themes**: what topics are trending NOW

**cadence:** daily scan (lightweight, API-based) + weekly deep dive (browser-based, scrapes actual niche communities).

**integration with v2:** feeds directly into Layer 7 (Alpha Engine) for scoring and Layer 4 (MCP Integration) for automated research via Tavily/Playwright MCPs.

---

### addendum 4: mega automation runner (session-start trigger)

**what it is:** single command that runs ALL research automations when a session begins. replaces the manual "run all scrapers" checklist.

**current state:**
- `printmaxx_cron.sh` (741 lines) — master command dispatcher with 12+ subcommands
- `daily_research_orchestrator.py` (1,055 lines) — 4-phase research at 5 AM
- `overnight_orchestrator.py` (308 lines) — parallel task runner
- 20+ explicit cron entries + 15+ auto-generated ones
- BUT: no single "session start" trigger. agents have to manually run 6-8 commands from the CLAUDE.md checklist.

**proposed:**

```bash
# ONE command to rule them all
python3 AUTOMATIONS/mega_session_runner.py --start

# What it does (in parallel where possible):
# Phase 1: Memory refresh (10 seconds)
#   - memory_manager.py --full
#   - Read HEARTBEAT.md + active-tasks.md
#
# Phase 2: Research scrapers (parallel, 2-5 min)
#   - twitter_alpha_scraper.py --all
#   - background_reddit_scraper.py --scrape
#   - daily_research_orchestrator.py --full
#   - competitor_monitor.py --scan
#   - unified_alpha_monitor.py --full
#   - telegram_community_monitor.py --scan
#
# Phase 3: Alpha processing (after scrapers finish)
#   - alpha_auto_processor.py --process-new (run until 0 remaining)
#   - niche_meta_detector.py --scan (v2, with auto-discovery)
#   - freshness_decay.py --update (decay scores)
#
# Phase 4: Status report
#   - system_health_monitor.py --quick
#   - venture_performance_tracker.py --recommend
#   - Output: session-ready status block
```

**daily verification dashboard:**

```bash
# Did everything run today?
python3 AUTOMATIONS/mega_session_runner.py --verify

# Output:
# ✓ Memory refresh: ran at 05:00
# ✓ Twitter scrape: ran at 05:30, 116 accounts, 43 new entries
# ✓ Reddit scrape: ran at 05:45, 20 subs, 110 posts
# ✓ Research orchestrator: ran at 05:00, 748 new alpha
# ✗ Competitor monitor: MISSED (last run: 2 days ago)
# ✓ Alpha processing: ran at 06:30, 0 unprocessed remaining
# ✓ Freshness decay: ran at 06:45, 12 entries marked STALE
#
# OVERALL: 6/7 ran today. 1 missed (auto-running now...)
```

**cron safety net:**
```cron
# If mega runner didn't run by 8 AM, auto-trigger
0 8 * * * python3 AUTOMATIONS/mega_session_runner.py --verify --auto-run-missing
```

**integration with v2:** this is the operational glue between the CLAUDE.md "Session Start" checklist and the actual automation infrastructure. Layer 6 (Orchestration) manages the execution order.

---

### addendum 5: daily cron verification (single dashboard view)

**what it is:** one-page view showing which crons ran, which missed, and auto-recovery for missed jobs.

**current state:**
- 57+ cron jobs scheduled
- logs scattered across `AUTOMATIONS/logs/`
- no single "did everything run?" view
- lock files and state JSONs exist but aren't aggregated

**proposed:**

```bash
python3 AUTOMATIONS/cron_health_dashboard.py

# Output:
# ┌─────────────────────────────────────────────────────┐
# │ CRON HEALTH DASHBOARD — 2026-02-19                  │
# ├─────────────┬──────────┬─────────┬─────────────────┤
# │ Job         │ Schedule │ Status  │ Last Run        │
# ├─────────────┼──────────┼─────────┼─────────────────┤
# │ twitter     │ 5:30 AM  │ ✓ RAN   │ 5:31 AM (43 new)│
# │ reddit      │ 5:45 AM  │ ✓ RAN   │ 5:46 AM (110)  │
# │ orchestrator│ 5:00 AM  │ ✓ RAN   │ 5:02 AM (748)  │
# │ competitors │ 7:00 AM  │ ✗ MISSED│ 2 days ago      │
# │ alpha proc  │ 6:30 AM  │ ✓ RAN   │ 6:32 AM (0 rem)│
# │ backup      │ 9:15 PM  │ PENDING │ tonight         │
# │ ...         │          │         │                 │
# ├─────────────┴──────────┴─────────┴─────────────────┤
# │ SUMMARY: 18/20 ran today | 1 missed | 1 pending    │
# │ AUTO-RECOVERY: running competitor_monitor now...    │
# └─────────────────────────────────────────────────────┘
```

**features:**
- reads all log files from `AUTOMATIONS/logs/` to determine last run times
- compares against expected schedule from `crontab_printmaxx.txt`
- auto-runs any missed jobs (with `--auto-recover` flag)
- outputs to `OPS/CRON_HEALTH_DAILY.md` for agent reference
- integrates with HEARTBEAT.md (adds cron health line)

**integration with v2:** Layer 6 (Orchestration) needs visibility into what's running. this dashboard provides it. the mega session runner (addendum 4) calls this as its Phase 4 status report.

---

### addendum 6: CLAUDE.md / CODEX.md hybrid (unified instruction set)

**what it is:** merge the two existing instruction systems into one optimized instruction set that works for both Claude Code sessions and OpenClaw autonomous agents.

**the two systems:**

| | CLAUDE.md | CODEX.md |
|---|-----------|----------|
| **Lines** | 3,139 | 207 |
| **Philosophy** | "How should the agent behave?" | "What should the system DO?" |
| **Orientation** | Agent-centric ops manual | Execution contract |
| **Scope expansion** | Manual (agent follows checklist) | Automatic ("etc" = expand to full adjacent set) |
| **Human gates** | Multiple checkpoints | Minimal (only payments, credentials) |
| **Best for** | Interactive sessions | Autonomous overnight loops |
| **Memory** | 3-layer (HEARTBEAT, active-tasks, logs) | Not specified (assumes CLAUDE.md's system) |

**proposed hybrid: `OPENCLAW.md`**

takes the best of both:

```
OPENCLAW.md (unified instruction set)
├── CODEX.md's philosophy (Section 1 — 200 lines)
│   ├── Auto-expand scope on "etc" and ambiguity
│   ├── Assume meta intent (don't ask, figure it out)
│   ├── Minimal human gates (only payments/credentials/publishing)
│   ├── Portfolio expansion as background continuous process
│   └── Low-verbosity execution (results, not reports)
│
├── CLAUDE.md's reference knowledge (Section 2 — compressed)
│   ├── Master Navigation Map (all "Where is..." entries)
│   ├── Tool inventory (all quant tools, scrapers, builders)
│   ├── File locations (critical paths only)
│   └── Cross-reference checklist (what to check before building)
│
├── Safety guardrails (Section 3 — from both)
│   ├── Project folder boundary (CLAUDE.md's guardrails)
│   ├── Risk-based autonomy levels (v2 Layer 5)
│   ├── Backup before destructive ops
│   └── Compliance scanning before publish
│
└── Session protocols (Section 4 — compressed)
    ├── Session start: mega_session_runner.py --start (one command)
    ├── Session end: update HEARTBEAT + active-tasks + daily log
    ├── Crash recovery: read active-tasks.md, pick up where left off
    └── Content generation: max squeeze protocol (compressed)
```

**key design decisions:**
1. CODEX.md's "auto-expand" philosophy is the DEFAULT for OpenClaw autonomous agents
2. CLAUDE.md's detailed reference is available but NOT mandatory reading — agents pull what they need
3. the 3-layer memory architecture is standardized across both systems
4. guardrails are non-negotiable regardless of philosophy

**estimated size:** ~800 lines (vs 3,139 + 207 = 3,346 lines currently). 76% compression with zero information loss — the reference data stays in the existing files, OPENCLAW.md just points to them.

**integration with v2:** this becomes the instruction set loaded into OpenClaw's agent config on Laptop 2. Claude Code sessions on Laptop 1 continue using CLAUDE.md (which can optionally adopt the CODEX philosophy sections). over time, as the hybrid proves out, CLAUDE.md evolves toward the OPENCLAW.md pattern.

---

### addendum 7: tweet → niche repurpose pipeline (wire alpha to content)

**what it is:** automatically generate niche-targeted content whenever the alpha pipeline finds high-signal tweets or insights.

**the gap:** alpha_auto_processor.py (26,807 lines) scores and routes alpha. content_multiplier.py generates 20+ variants from one piece of content. BUT they're not connected — there's no automatic trigger from "high-signal alpha found" to "generate niche content from it."

**proposed wiring:**

```
CURRENT (disconnected):
  scraper → ALPHA_STAGING.csv → alpha_auto_processor → routes to ventures/OPS/archive
  content_multiplier.py → generates variants (manually triggered)

PROPOSED (connected):
  scraper → ALPHA_STAGING.csv → alpha_auto_processor
    ↓
  IF score >= 80 AND category in [CONTENT_FORMAT, GROWTH_HACK, TOOL_ALPHA]:
    ↓
  AUTO-TRIGGER content_multiplier.py --source {alpha_id} --niches {relevant_niches}
    ↓
  OUTPUTS:
    ├── 5 tweets per relevant niche (tech, faith, fitness, etc.)
    ├── 1 thread for highest-relevance niche
    ├── 3 cross-niche adaptations
    └── all saved to repurpose_queue.csv as PENDING_REVIEW
```

**example flow:**
1. viral_content_scanner.py finds a tweet about OpenClaw getting 200K stars
2. alpha_auto_processor scores it 88/100, category: TOOL_ALPHA
3. auto-triggers content_multiplier with niches: [tech, printmaxxer]
4. content_multiplier generates:
   - 5 @PRINTMAXXER tweets about the tool
   - 5 @toolstwts tweets about the tool
   - 1 thread breaking down the implications
   - 3 cross-niche angles (faith: "AI tools for ministry ops", fitness: "automate your coaching business")
5. all outputs land in `repurpose_queue.csv` as PENDING_REVIEW
6. after 20+ reviewed with >90% approval rate → switch to auto-post

**implementation:** add a post-processing hook in alpha_auto_processor.py that calls content_multiplier.py when conditions are met. the content_multiplier needs a new `--niches` parameter to target specific niche accounts.

**integration with v2:** this closes the loop between Layer 7 (Alpha Engine) and the content distribution system. the Zero Waste Protocol is no longer just a manual checklist — it's automated into the pipeline. every high-signal alpha entry automatically becomes content across all relevant niches.

---

## updated implementation plan (if approved)

the original 4-phase plan (weeks 1-6) still holds. these addendum items slot in:

| Addendum | Phase | Effort | Dependencies |
|----------|-------|--------|-------------|
| 1. OpenClaw gateway (or LiteLLM) | Phase 1 (week 2) | 2 hours (Docker + config) | CONDITIONAL — requires all 7 hardening conditions. see SECURITY_ARCHITECTURE_PRINTMAXX.md |
| 2. Tweet freshness decay | Phase 1 (week 1) | 4 hours (add fields + cron job) | None |
| 3. Niche meta detector v2 | Phase 2 (week 3) | 8 hours (new discovery logic) | Tavily MCP for API research |
| 4. Mega session runner | Phase 1 (week 1) | 3 hours (orchestration script) | None |
| 5. Cron health dashboard | Phase 1 (week 1) | 2 hours (log aggregation) | None |
| 6. OPENCLAW.md hybrid | Phase 1 (week 2) | 6 hours (merge + compress) | Approval of philosophy direction |
| 7. Alpha → content pipeline | Phase 2 (week 3) | 4 hours (wire existing scripts) | Alpha processor + content multiplier both working |

**total additional effort:** ~29 hours across weeks 1-3.
**total additional cost:** $20/mo (ChatGPT subscription for OpenClaw). everything else uses existing infrastructure.

---

## updated open questions for user

original 5 questions still stand. adding:

6. **model routing on Laptop 2:** three options: (a) OpenClaw core hardened (v2026.2.12+, Docker, no skills), (b) LiteLLM self-hosted proxy (simpler, less risk), (c) Claude Code + Codex CLI side-by-side (simplest, no middleware). which do you prefer?

7. **CODEX.md philosophy:** the hybrid OPENCLAW.md defaults to CODEX.md's "auto-expand, minimal gates" philosophy for autonomous agents. are you comfortable with agents auto-expanding scope without asking, or do you want more human checkpoints for autonomous runs?

8. **auto-post threshold:** the alpha → content pipeline generates content as PENDING_REVIEW. at what approval rate do you want to switch to auto-post? proposal: 90% approval rate over 20+ reviewed items.

---

---

## ADDENDUM 2: autonomous agent orchestration architecture (2026-02-19)

**the user's core need:** "agent monitors agent runs so work can compound without human in loops. automate the workflow that automates workflows. with logical guardrails."

**current state:** Ralph loops are repetitive tasks (stateless resampling). they run a long time unsupervised but they're NOT LLM-in-the-loop self-iterating agents. starting each requires manual prompting. no agent monitors another agent's output.

**research covered:** 13+ autonomous agent systems, production deployments, Feb 2026 industry consensus.

---

### the 13 systems compared

| System | Architecture | Agent-Monitors-Agent? | Maturity | Best For |
|--------|-------------|----------------------|----------|----------|
| **Claude Code Agent Teams** | native multi-agent (TeamCreate/TaskCreate/SendMessage) | YES — task dependencies, idle monitoring | 2 weeks old (Feb 5, 2026) | closest to what we want. already available. |
| **Antfarm (Ryan Carson)** | YAML + SQLite + cron on top of OpenClaw | YES — planner→developer→verifier→tester→reviewer | production (Carson runs it) | agent pipeline with verification |
| **LangGraph** | graph-based workflow, persistent state, checkpointing | YES — any topology | production-grade | complex orchestration with replay |
| **OpenClaw** | single-agent runtime with model routing | NO — needs external orchestration layer | 200K stars but security crisis | model routing only, not orchestration |
| **Codex CLI + Agents SDK** | OpenAI's agent framework | YES — multi-agent via SDK | more mature than Claude Teams | OpenAI ecosystem |
| **claude-flow** | claims hive mind with queen-led hierarchy | claims YES — 87 MCP tools, SQLite memory | 14K stars, claims unverified | ambitious but unproven |
| **Continuous Claude** | sophisticated Ralph loop with PRs, cost/time limits | NO — single agent with memory | battle-tested pattern | long-running single agent |
| **n8n / Activepieces** | visual workflow automation | NO — workflow steps, not agent loops | production | API plumbing between services |
| **Windmill** | code-first workflow engine | NO — task orchestration, not agent monitoring | production | heavy data pipeline |
| **CrewAI** | role-based multi-agent framework | partial — role delegation | growing | team simulation |
| **AutoGen (Microsoft)** | multi-agent conversation framework | partial — conversation monitoring | maturing | research-oriented |
| **NanoClaw** | lightweight container-isolated OpenClaw alternative | inherits from Agents SDK | emerging (new) | safer OpenClaw-like functionality |
| **Mastra** | TypeScript agent framework | partial | emerging | TypeScript-native teams |

---

### recommended architecture for PRINTMAXX

```
PRINTMAXX AUTONOMOUS ORCHESTRATION (4 tiers)

TIER 1: ORCHESTRATION BRAIN
├── Claude Code Agent Teams (PRIMARY)
│   ├── TeamCreate → creates team with task list
│   ├── TaskCreate → defines work items with dependencies
│   ├── SendMessage → agents communicate
│   ├── TaskUpdate → agents claim/complete tasks
│   └── agent A monitors agent B via task status
│
├── OR LangGraph (ALTERNATIVE — more control, more setup)
│   ├── graph-based workflow definition
│   ├── persistent state across runs
│   ├── checkpointing + replay for debugging
│   └── human-in-the-loop nodes for approvals
│
└── key decision: Claude Teams = fast to start, LangGraph = more control

TIER 2: AGENT PIPELINE (Antfarm pattern)
├── PLANNER AGENT
│   ├── reads task queue + recent alpha + system state
│   ├── breaks work into subtasks
│   └── assigns to specialized agents
│
├── WORKER AGENTS (specialized)
│   ├── RESEARCHER: web search, API calls, scraping
│   ├── BUILDER: code generation, content creation
│   ├── ANALYST: data processing, scoring
│   └── EXECUTOR: deployment, posting, emailing
│
├── VERIFIER AGENT (Judge pattern from v2 Layer 2)
│   ├── read-only evaluation of worker output
│   ├── APPROVE or REQUEST_CHANGES
│   └── feedback becomes next iteration context
│
├── RETROSPECTIVE AGENT (self-improvement)
│   ├── reviews completed task outcomes
│   ├── logs what worked/failed to LEARNINGS.jsonl
│   ├── proposes prompt mutations for next cycle
│   └── this is the "agent monitors agent" core
│
└── key insight: Antfarm's planner→worker→verifier→tester→reviewer
    is the exact pipeline we need. adopt the PATTERN, build our own.

TIER 3: PERSISTENCE + LEARNING
├── Memory (v2 Layer 1 — Zep/Graphiti)
│   ├── successful run trajectories saved
│   ├── failed run patterns flagged
│   └── temporal knowledge graph auto-invalidates stale data
│
├── Performance tracking (JSONL)
│   ├── per-agent success rates
│   ├── per-prompt effectiveness scores
│   └── correlate changes to outcomes
│
└── Prompt mutation (monthly)
    ├── DSPy/MIPROv2 Bayesian optimization
    ├── top 3 variants tested on historical tasks
    └── winner promoted

TIER 4: API PLUMBING
├── n8n or Windmill for webhook triggers
│   ├── "new alpha scored 80+" → trigger content pipeline
│   ├── "cron health check failed" → trigger recovery
│   └── "new GitHub release" → trigger update check
│
├── existing cron jobs (57+ entries)
│
└── Telegram bot for human escalation
```

---

### how "agent monitors agent" works in practice

**example: autonomous research → content → posting pipeline**

```
1. CRON (5 AM): triggers mega_session_runner.py
2. PLANNER reads: HEARTBEAT, active-tasks, today's alpha queue
3. PLANNER creates tasks:
   - Task A: "scrape 116 Twitter accounts" → assigns RESEARCHER
   - Task B: "process new alpha entries" → assigns ANALYST (blocked by A)
   - Task C: "generate niche content from high-scoring alpha" → assigns BUILDER (blocked by B)
   - Task D: "verify content passes copy-style.md checklist" → assigns VERIFIER (blocked by C)
   - Task E: "queue approved content to Buffer" → assigns EXECUTOR (blocked by D)

4. RESEARCHER completes Task A → marks done → ANALYST auto-starts Task B
5. ANALYST scores alpha → routes high-scoring → marks done → BUILDER auto-starts Task C
6. BUILDER generates 5 tweets per niche → marks done → VERIFIER auto-starts Task D
7. VERIFIER checks copy-style.md compliance:
   - 3 tweets APPROVE → forward to EXECUTOR
   - 2 tweets REQUEST_CHANGES → BUILDER gets feedback, re-generates
8. EXECUTOR queues approved content → marks done
9. RETROSPECTIVE reviews full pipeline:
   - "RESEARCHER took 45 min (expected 30). bottleneck: rate limiting on 3 accounts."
   - "BUILDER failed copy-style check 40% of the time. need to add voice examples to prompt."
   - logs to LEARNINGS.jsonl
   - proposes: "add @pipelineabuser examples to content generation prompt"
10. PLANNER reads retrospective for next cycle → adjusts prompts/assignments
```

**this runs without human. the human reviews:**
- content in `repurpose_queue.csv` (PENDING_REVIEW) at their convenience
- pipeline metrics in HEARTBEAT.md
- retrospective summaries in daily logs

---

### what this looks like for PRINTMAXX specifically

**phase 1 (week 1-2): bootstrap with Claude Code Agent Teams**

we already HAVE this capability. Claude Code Agent Teams shipped Feb 5, 2026. the tools are available right now: TeamCreate, TaskCreate, TaskList, TaskUpdate, SendMessage.

```bash
# what a self-orchestrating session looks like:
# 1. TeamCreate "printmaxx-daily"
# 2. TaskCreate: research scraping (researcher agent)
# 3. TaskCreate: alpha processing (analyst agent, blocked by research)
# 4. TaskCreate: content generation (builder agent, blocked by alpha)
# 5. TaskCreate: quality verification (verifier agent, blocked by content)
# 6. Launch 4 agents via Task tool with team_name
# 7. Agents self-coordinate via task dependencies
```

**phase 2 (week 3-4): add persistence + learning**

- wire Zep/Graphiti for trajectory storage
- add LEARNINGS.jsonl retrospective agent
- connect performance tracking to prompt mutation

**phase 3 (week 5-6): add cron-triggered autonomous loops**

- mega_session_runner.py spawns agent teams via Claude Code
- cron triggers the planner
- planner creates task graph
- agents execute autonomously
- retrospective agent logs learnings
- next cycle is better than the last

**this is what you wanted: "automate the workflow that automates workflows."**

---

### why NOT just OpenClaw for this

OpenClaw is a model router and single-agent runtime. it does NOT do:
- multi-agent orchestration
- task dependency graphs
- agent-monitors-agent patterns
- retrospective learning

to get "agent monitors agent" with OpenClaw, you'd need to build an orchestration layer ON TOP of it. that's exactly what Antfarm (Ryan Carson) did — he built YAML + SQLite + cron orchestration on top of OpenClaw. but at that point, the orchestration layer IS the product, and OpenClaw is just routing API calls. LiteLLM does the same routing with less attack surface.

**the real value is in the orchestration pattern, not the model router.**

---

### industry consensus (Feb 2026)

the research found a clear consensus: **"supervised autonomy"** is the state of the art.

- agents run autonomously within bounded tasks
- cost limits per agent per run (prevents runaway spend)
- quality gates between pipeline stages (verifier pattern)
- periodic human review of outputs (not every output, but samples)
- kill switches for when things go wrong
- retrospective learning to improve over time

nobody credible is running fully unsupervised AI agents in production. the agents that work best operate like a well-managed team: clear roles, clear handoffs, clear quality bars, with a human checking in periodically.

**for PRINTMAXX this means:**
- agents run the research→process→content→verify→queue pipeline autonomously
- human reviews queued content at their convenience (not blocking)
- human reviews retrospective summaries weekly
- cost caps prevent runaway API spend
- kill condition: if any agent fails 3x consecutively, pipeline halts and alerts via Telegram

---

### updated implementation plan

| Item | Phase | Effort | Dependencies |
|------|-------|--------|-------------|
| 8. Claude Code Agent Teams orchestration | Phase 1 (week 1) | 4 hours (define team templates, task graphs) | None — tools already available |
| 9. Planner agent + task dependency graph | Phase 1 (week 2) | 6 hours (planner prompt, task templates) | Agent Teams working |
| 10. Verifier agent (read-only quality gate) | Phase 1 (week 2) | 3 hours (verifier prompt, approval logic) | Agent Teams working |
| 11. Retrospective agent (self-improvement) | Phase 2 (week 3) | 8 hours (learning extraction, prompt mutation) | Zep installed, trajectories stored |
| 12. Cron-triggered autonomous pipeline | Phase 3 (week 5) | 6 hours (mega_session_runner v2, agent spawning) | All above working |

**total additional effort for autonomous orchestration:** ~27 hours across weeks 1-5.
**additional cost:** $0 (Claude Code Agent Teams is included in Claude Max plan).

---

### open questions for user (autonomous orchestration)

9. **orchestration engine:** Claude Code Agent Teams (available now, simpler) vs LangGraph (more control, more setup)? recommendation: start with Agent Teams, migrate to LangGraph only if we hit limitations.

10. **autonomous run frequency:** how often should the pipeline self-run? options: (a) every session start, (b) 2x daily (5 AM + 5 PM), (c) continuous (every 2 hours). recommendation: 2x daily to start, increase frequency as confidence grows.

11. **human review cadence:** (a) review every output, (b) review daily batch, (c) review weekly summary. recommendation: daily batch review with Telegram notification when batch is ready.

12. **cost cap per autonomous run:** suggestion: $5 per run (at Claude Max rates, this is generous). prevents runaway if an agent loops.

---

---

## ADDENDUM 3: THE 24/7 AUTONOMOUS WORKER — definitive build plan (2026-02-19)

**the vision:** "a 24/7 person that spawns persons that can do stuff without accidentally doing anything really bad"

**the answer:** Claude Code Agent Teams on the spare laptop, running as a daemon with cron triggers, using OpenClaw (hardened) for cheap multi-model routing ONLY IF you want OpenAI access. the orchestration, spawning, monitoring — all Claude Code native. OpenClaw is just the budget model router underneath, nothing more.

---

### the actual setup (2 laptops)

```
LAPTOP 1 — MAIN MACBOOK (control node, interactive)
├── Claude Code interactive sessions (you prompting, reviewing)
├── Human review dashboard (localhost:8888)
├── Content approval queue
├── HEARTBEAT.md + active-tasks.md (shared via git)
└── Telegram bot receives alerts from Laptop 2

LAPTOP 2 — SPARE LAPTOP (autonomous worker, 24/7)
├── SUPERVISOR DAEMON (Python, always running)
│   ├── reads task queue from filesystem
│   ├── spawns Claude Code sessions via `claude --print`
│   ├── each session uses Agent Teams for multi-agent coordination
│   ├── monitors running agents (timeout, cost, output quality)
│   ├── kills agents that exceed cost cap or time limit
│   ├── logs everything to daily logs
│   └── sends Telegram alerts on: completion, failure, human-needed
│
├── CRON SCHEDULER (triggers supervisor at set times)
│   ├── 5:00 AM — full research pipeline (scrape → process → score)
│   ├── 8:00 AM — content generation from overnight alpha
│   ├── 12:00 PM — midday alpha scan + trending check
│   ├── 5:00 PM — content generation round 2
│   ├── 10:00 PM — overnight builder (apps, landing pages, tools)
│   ├── every 2 hours — system health check + recovery
│   └── weekly — retrospective + prompt mutation + learning extraction
│
├── OPENSCLAW DAEMON (OPTIONAL — model routing only)
│   ├── v2026.2.12+ in Docker, localhost:18789
│   ├── ZERO skills installed
│   ├── routes to: openai-codex/gpt-5.3-codex ($20/mo flat)
│   ├── fallback: anthropic/claude-sonnet (via API)
│   ├── monitored by LuLu + BlockBlock
│   └── ONLY used for model routing. orchestration is Claude Code.
│
├── GUARDRAILS LAYER (non-negotiable)
│   ├── guardrails.py — all file ops within project root only
│   ├── cost cap — $5/run max, $50/day max, kill if exceeded
│   ├── time cap — 2 hours max per agent team run
│   ├── compliance scan — auto-run on any generated content
│   ├── no payments, no account creation, no publishing without human
│   ├── no writing outside project folder (existing guardrails.py)
│   ├── no git push without human approval
│   └── Telegram alert on: any HIGH_RISK action attempted
│
└── SECURITY LAYER (from SECURITY_ARCHITECTURE_PRINTMAXX.md)
    ├── envchain for all API keys (never on disk)
    ├── Secretive for SSH keys (Secure Enclave)
    ├── LuLu firewall (alert on unknown connections)
    ├── BlockBlock (alert on persistence attempts)
    ├── FileVault (full disk encryption)
    └── separate macOS user account for the daemon
```

---

### how the supervisor daemon works

```python
# CONCEPTUAL — the actual script will be ~500 lines

SUPERVISOR LOOP (runs 24/7):

while True:
    # 1. READ SYSTEM STATE
    heartbeat = read("OPS/HEARTBEAT.md")
    tasks = read("OPS/active-tasks.md")
    queue = read("OPS/AUTONOMOUS_TASK_QUEUE.md")

    # 2. CHECK IF ANYTHING NEEDS DOING
    if queue.has_pending_tasks():
        task = queue.next_by_priority()

        # 3. GUARDRAIL CHECK
        if task.risk_level == "CRITICAL":
            telegram_alert("HUMAN NEEDED: " + task.summary)
            continue  # skip, wait for human

        if daily_cost > DAILY_CAP:
            telegram_alert("DAILY COST CAP HIT: $" + daily_cost)
            sleep(until_midnight)
            continue

        # 4. SPAWN AGENT TEAM
        team = claude_code(
            "--print",
            prompt=f"""
            You are the PLANNER for PRINTMAXX autonomous operations.
            Read CLAUDE.md for full context.

            YOUR TASK: {task.description}

            RULES:
            - Use Agent Teams (TeamCreate/TaskCreate) to spawn workers
            - Each worker gets a specific subtask
            - VERIFIER agent checks all output before marking done
            - Stay within project folder
            - No payments, no publishing, no account creation
            - Cost cap: $5 for this run
            - Time cap: 2 hours
            - Write results to: OPS/autonomous_output/{date}/{task_id}/
            - Update HEARTBEAT.md when done
            - If you need human: write to OPS/HUMAN_NEEDED/{task_id}.md
            """
        )

        # 5. MONITOR (runs in background)
        monitor(team, timeout=7200, cost_cap=5.00)

        # 6. ON COMPLETION
        log_result(task, team.output)
        update_heartbeat()

        if task.generated_content:
            queue_for_review(task.output)
            telegram_alert("Content ready for review: " + task.summary)

    else:
        # 7. SELF-GENERATE TASKS (the meta-vision part)
        # every 6 hours, if queue is empty, the supervisor
        # spawns a PLANNER agent that reads the full system state
        # and creates new tasks based on:
        #   - unprocessed alpha in ALPHA_STAGING.csv
        #   - missed cron jobs
        #   - new opportunities detected by scanners
        #   - retrospective learnings suggesting improvements
        #   - content calendar gaps
        #   - stale data needing refresh

        if hours_since_last_self_plan > 6:
            planner_output = claude_code(
                "--print",
                prompt=SELF_PLANNING_PROMPT  # reads everything, proposes tasks
            )
            queue.add_tasks(planner_output.proposed_tasks)

    sleep(300)  # check every 5 minutes
```

---

### what it actually DOES 24/7

**5:00 AM — research pipeline**
- supervisor triggers research team
- RESEARCHER agents scrape Twitter (116 accounts), Reddit (41 subs), HN, PH
- ANALYST agent processes raw alpha, scores 0-100, routes to categories
- VERIFIER checks for duplicates, validates scoring
- results: new alpha in ALPHA_STAGING.csv, digest in OPS/

**8:00 AM — content generation**
- supervisor reads overnight alpha (score >= 80)
- spawns BUILDER team: 1 agent per niche (tech, faith, fitness, memes)
- each BUILDER generates 5 tweets + 1 thread from high-scoring alpha
- VERIFIER checks against copy-style.md, rejects non-compliant
- EXECUTOR queues approved content to repurpose_queue.csv
- Telegram: "47 posts generated, 38 passed QA, ready for review"

**12:00 PM — midday pulse**
- RESEARCHER does quick scan (trending topics, competitor changes)
- ANALYST checks freshness decay on existing alpha
- if new high-signal found: triggers mini content generation

**5:00 PM — content round 2 + builder tasks**
- generates content from any alpha found at midday
- starts building: landing pages, tool improvements, app updates
- VERIFIER checks all builds before writing to disk

**10:00 PM — overnight builder**
- longer-running tasks: full app features, scraper improvements, new automations
- RETROSPECTIVE agent reviews all day's work:
  - what took longer than expected?
  - what failed QA most often?
  - what alpha categories generated best content?
  - what prompts need mutation?
- writes learnings to LEARNINGS.jsonl
- proposes task queue for tomorrow's 5 AM cycle

**every 2 hours — health check**
- verifies all cron jobs ran
- checks for missed tasks
- monitors disk space, API costs, error rates
- auto-recovers any failed jobs
- updates HEARTBEAT.md

---

### the guardrails (why it won't accidentally do anything bad)

| Risk | Guardrail | How |
|------|-----------|-----|
| **runaway costs** | $5/run cap, $50/day cap | supervisor kills agent if exceeded |
| **writing outside project** | guardrails.py path validation | every file op checked against project root |
| **publishing without approval** | all content → PENDING_REVIEW | nothing goes live without human marking APPROVED |
| **payment/account creation** | blocked actions list | supervisor rejects any task touching payments/accounts |
| **git push** | blocked without human | supervisor strips git push from agent capabilities |
| **malware from scraped content** | scraper isolation | scraped content treated as UNTRUSTED, never eval'd |
| **prompt injection** | content delimiters | external content wrapped in "UNTRUSTED CONTENT" tags |
| **infinite loops** | 2-hour timeout per team | supervisor force-kills after timeout |
| **credential theft** | envchain + Secretive | API keys in Keychain only, SSH in Secure Enclave |
| **network exfiltration** | LuLu firewall | alerts on any unknown outbound connection |
| **agent goes rogue** | read-only verifier | VERIFIER agent can only read, never modify |
| **stale/wrong decisions** | retrospective review | weekly learning extraction catches systematic errors |

---

### where OpenClaw fits (and where it doesn't)

```
WHAT OPENCLAW DOES:                    WHAT WE NEED:
─────────────────────                  ─────────────────
✓ route to multiple LLMs              ✓ agent spawns agents
✓ flat rate $20/mo                    ✓ task dependency graphs
✗ multi-agent orchestration           ✓ agent monitors agent
✗ task dependency graphs              ✓ quality verification pipeline
✗ agent monitoring                    ✓ self-improvement loop
✗ self-improvement                    ✓ guardrails enforcement
✗ guardrails                          ✓ 24/7 daemon with health checks
```

OpenClaw = gas station. you need gas, but the gas station doesn't drive your car.

**use OpenClaw (hardened) on Laptop 2 ONLY for model routing.** it gives you $20/mo flat access to OpenAI models. that's it. the orchestration, the spawning, the monitoring, the guardrails, the self-improvement — all of that is our supervisor daemon + Claude Code Agent Teams.

**or skip OpenClaw entirely** and use Claude Code on both laptops (you have Claude Max, unlimited tokens). you lose OpenAI model access but gain simplicity and security. LiteLLM is a middle ground if you want multi-model routing without OpenClaw's baggage.

---

### concrete build plan

| Step | What | Effort | Dependencies |
|------|------|--------|-------------|
| 1 | install security stack on spare laptop (LuLu, BlockBlock, envchain, Secretive, FileVault) | 1 hour | spare laptop accessible |
| 2 | create separate macOS user account for daemon | 15 min | step 1 done |
| 3 | install Claude Code on spare laptop, authenticate | 15 min | Claude Max subscription |
| 4 | clone PRINTMAXX repo to spare laptop | 10 min | GitHub access |
| 5 | build supervisor daemon (`AUTOMATIONS/autonomous_supervisor.py`) | 6 hours | steps 1-4 done |
| 6 | build SELF_PLANNING_PROMPT (reads system state, proposes tasks) | 4 hours | CLAUDE.md + all OPS docs |
| 7 | build AUTONOMOUS_TASK_QUEUE.md format + task templates | 2 hours | step 5 done |
| 8 | set up Telegram bot for alerts | 1 hour | Telegram account |
| 9 | configure cron schedule on spare laptop | 30 min | steps 5-7 done |
| 10 | (OPTIONAL) install OpenClaw hardened on spare laptop | 2 hours | Docker installed |
| 11 | first supervised test run (you watch, fix issues) | 4 hours | all above |
| 12 | first overnight unsupervised run | overnight | step 11 clean |
| 13 | first 48-hour run, review retrospective | 2 days | step 12 clean |
| 14 | build retrospective agent + learning extraction | 4 hours | week 2 |
| 15 | build prompt mutation pipeline | 4 hours | week 3 |

**total: ~30 hours of build time across 3 weeks. then it runs 24/7.**

---

### what you do vs what it does

**YOU (human, ~30 min/day):**
- morning: check Telegram alerts, review content queue (approve/reject)
- midday: glance at HEARTBEAT.md (optional)
- evening: review retrospective summary (optional)
- weekly: review learnings, approve prompt mutations
- approve/reject: account creation, payments, publishing

**IT (24/7 autonomous worker):**
- scrape alpha from 350+ sources
- process and score alpha (0-100)
- generate content across all niches
- verify content against copy-style.md
- queue approved content for posting
- build landing pages, tools, improvements
- monitor competitors, trends, opportunities
- self-improve based on retrospective learning
- alert you when it needs human input
- recover from failures automatically

this is the "24/7 person that spawns persons." the supervisor is the manager. Claude Code Agent Teams are the workers. guardrails keep everything safe. retrospective learning makes it better over time. OpenClaw is the optional cheap gas station.

---

### RESOLVED: spare laptop = M2 MacBook Pro, 16GB RAM, 500GB SSD

this is a beast for autonomous agent work. 4x the RAM of DO's recommended droplet. can run local models via Ollama. $0/mo vs $44/mo (DO + ChatGPT). keeps all data local.

**uptime fix for macOS (prevent sleep on spare laptop):**
```bash
# prevent sleep permanently (run on spare laptop)
sudo pmset -a disablesleep 1
sudo pmset -a sleep 0
# or use caffeinate for specific processes:
caffeinate -s python3 AUTOMATIONS/autonomous_supervisor.py
```

---

### THE DEFINITIVE SETUP (final answer)

**after evaluating 13 agent systems, OpenClaw's security posture, DigitalOcean's offering, and the user's hardware:**

```
OPTION A — RECOMMENDED (simplest, most secure, $0/mo extra)
════════════════════════════════════════════════════════════

LAPTOP 1 — MAIN MACBOOK (interactive, you prompting)
├── Claude Code (interactive sessions)
├── human review, content approval
└── Telegram alerts from Laptop 2

LAPTOP 2 — SPARE M2 MACBOOK (autonomous 24/7 worker)
├── Claude Code Agent Teams (orchestration brain)
│   ├── supervisor daemon spawns agent teams via cron
│   ├── planner → workers → verifier → retrospective
│   └── all multi-agent coordination is native Claude Code
├── Direct Claude API (Max plan, unlimited tokens)
├── MCP servers for tool integrations
├── Existing PRINTMAXX codebase (cloned via git)
├── Guardrails (cost caps, file boundaries, compliance)
├── Security stack (LuLu, BlockBlock, envchain, Secretive)
└── git push to GitHub every 6 hours (sync with Laptop 1)

NO OPENCLAW. NO DO DROPLET. NO MIDDLEWARE.
Claude Code does everything OpenClaw does, natively, more securely.
Cost: $0/mo additional (you already have Claude Max).
```

```
OPTION B — IF YOU WANT OPENAI MODELS TOO ($44/mo)
══════════════════════════════════════════════════

Same as Option A, PLUS:

DO DROPLET ($24/mo) — model routing only
├── OpenClaw v2026.2.17+ in Docker
├── ZERO skills, localhost binding
├── routes to openai-codex/gpt-5.3-codex ($20/mo ChatGPT)
├── Claude Code on Laptop 2 calls DO droplet for OpenAI access
├── Fail2ban, UFW, auto-TLS (DO's hardening)
└── disposable: if compromised, nuke and redeploy in 10 min

Why DO instead of spare laptop for OpenClaw:
- if OpenClaw gets compromised, it only affects the droplet
- no personal files, no SSH keys, no crypto on the droplet
- static IP, no home network exposure
- disposable container: nuke and redeploy
- DO's hardening saves you sysadmin work

Why NOT skip DO and run OpenClaw on spare laptop:
- then a compromise of OpenClaw = compromise of the machine
  running your autonomous agents = very bad
- keep the autonomous brain (Claude Code) and the model
  router (OpenClaw) on separate machines
```

```
OPTION C — BUDGET ELASTIC (if you outgrow the spare laptop)
═══════════════════════════════════════════════════════════

Same as Option A, but supervisor daemon runs on DO
instead of spare laptop. for when you need:
- multiple simultaneous agent teams
- higher uptime (99.9% vs ~80%)
- elastic scaling (spin up bigger droplets for heavy jobs)
- spare laptop freed for other uses

Cost: $48-96/mo (8-16GB droplet) + API costs
Only worth it at $5K+/mo revenue. premature until then.
```

**recommendation: start with Option A.** $0 extra cost. your M2 MacBook is more powerful than any DO droplet under $96/mo. add Option B's DO droplet later ONLY if you specifically need OpenAI models. graduate to Option C only when revenue justifies it.

---

### why OpenClaw is NOT needed (the honest assessment)

the user asked: "is openclaw really the only harness that puts an LLM in loop connected to tons of shit?"

**no.** here's what OpenClaw does and what already does it:

| OpenClaw Feature | Claude Code Equivalent | Status |
|---|---|---|
| LLM-in-a-loop agent | `claude --print` in a while loop (Ralph pattern) | ALREADY USING |
| model routing (multi-provider) | not needed if Claude-only (Max plan) | N/A |
| file read/write | native Claude Code tool | ALREADY USING |
| run scripts | native Bash tool | ALREADY USING |
| browser control | Playwright MCP, browser-use | ALREADY USING |
| 50+ integrations | MCP protocol (500+ servers available) | PARTIALLY USING |
| agent spawning | Agent Teams (TeamCreate/TaskCreate) | AVAILABLE NOW |
| agent monitoring | Agent Teams (TaskUpdate/SendMessage) | AVAILABLE NOW |
| skills marketplace | MCP server registry | SAFER (no ClawHub) |

**what OpenClaw gives you that Claude Code doesn't:**
1. cheap OpenAI model access ($20/mo flat via ChatGPT subscription)
2. that's it. literally that's the only unique value.

**what Claude Code gives you that OpenClaw doesn't:**
1. native multi-agent orchestration (Agent Teams)
2. Anthropic-controlled security (no third-party attack surface)
3. your entire existing codebase works as-is (CLAUDE.md, Ralph loops, all 282 scripts)
4. no additional software to install, configure, or maintain
5. no CVEs from a third-party daemon running on your machine

**the hype explained:** OpenClaw got 200K stars because it packaged everything together beautifully and made autonomous agents accessible to non-developers. the timing was perfect (agent hype wave, Jan-Feb 2026). it's a good product. but if you already have Claude Code + Max plan, it's redundant except for OpenAI model access.

**DigitalOcean is selling hosting, not innovation.** their 1-Click Deploy is a smart business move (ride the OpenClaw hype, sell $24/mo droplets). the hardening is real (Fail2ban, UFW, auto-TLS, Docker). but it does NOT fix the application-level CVEs — the WebSocket RCE works THROUGH Docker because the browser initiates the connection. you still need to manually update to v2026.2.17+.

---

### open questions (remaining)

13. **first autonomous domain:** what should the 24/7 worker focus on FIRST? recommendation: research pipeline only for week 1 (scrape → process → score alpha). add content generation week 2. add building week 3.

14. **git sync:** recommendation: Laptop 2 does `git push` every 6 hours to GitHub. Laptop 1 does `git pull` at session start. simple, reliable, auditable.

15. **do you want OpenAI model access?** if yes: add DO droplet with hardened OpenClaw ($44/mo total). if no: skip entirely, Claude-only is sufficient for everything we're doing.

16. **Telegram bot:** do you have a Telegram account for alerts? the supervisor daemon needs somewhere to send "content ready for review" and "human needed" notifications.

---

*this addendum based on research from: Claude Code Agent Teams (Feb 5, 2026), Antfarm (Ryan Carson), LangGraph, claude-flow (14K stars), Continuous Claude, NanoClaw, OpenClaw hype cycle analysis, Pieter Levels interviews, Andrej Karpathy commentary, OpenClaw (Peter Steinberger, 200K stars), analysis of alpha_auto_processor.py (26,807 lines), content_multiplier.py, niche_meta_detector.py (30 niches), viral_content_scanner.py, printmaxx_cron.sh (741 lines), daily_research_orchestrator.py (1,055 lines), overnight_orchestrator.py (308 lines), CLAUDE.md (3,139 lines), and CODEX.md (207 lines).*
