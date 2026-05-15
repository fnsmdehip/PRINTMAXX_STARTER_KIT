# Audit: Open Source + External
**Date**: 2026-05-15
**Scope**: `OPEN_SOURCE/`, `external/`

## Inventory

### `OPEN_SOURCE/` (2 subprojects)
| Path | Purpose | Last Active | Lines/Files |
|---|---|---|---|
| `OPEN_SOURCE/agent-soul/` | **sovrun** — autonomous agent OS framework (24 core .py files, 5 layers) | Apr 4 (cache), Mar 19 (last commit), Mar 20 (last dir touch) | ~24 modules, ~480KB Python source |
| `OPEN_SOURCE/agent-soul/website/` | Next.js 16 marketing site (separate git repo) | Mar 18 last commit, untracked files exist | Next.js 16 + React 19 + Tailwind 4 |
| `OPEN_SOURCE/agent-soul/site/` | Static HTML alternative (deployed via surge.sh) | Mar 19 | 3 HTML files (index, docs, pricing) |
| `OPEN_SOURCE/remote-control-daisy-chain/` | Sanitized remote-Mac-control bundle (Tailscale + CodeRelay + RustDesk) | Mar 13 only | docs/, examples/, launchd/, scripts/ |

### `external/` (2 cloned repos)
| Path | Source | Purpose |
|---|---|---|
| `external/hcom/` | `github.com/aannoo/hcom` v0.7.2 | Third-party Rust/Python plugin tool, not authored here. Inactive — user memory says "NO hcom hooks". |
| `external/openclaw-official/` | `github.com/openclaw/openclaw` | Reference clone of OpenClaw monorepo (massive — pnpm workspace, Rust, Swift, fly/render configs). Read-only reference. Memory notes "OpenClaw had 512 vulns and 20% malicious skills". |

## agent-soul status (publish readiness + open decisions like name)

**The name was already decided**: `sovrun` (sovereign autonomous multi-agent OS). The candidate list in MEMORY.md (dogwalk, 6to1, slopnull, nerve, coldloop) is **stale** — the rename happened in git commit `d64fcf0` ("rename dogwalk -> sovrun across all 17 files"). Naming is no longer an open decision.

**Publish readiness — already partially shipped**:
- Public GitHub repo exists: `https://github.com/fnsmdehip/sovrun.git` (origin in `OPEN_SOURCE/agent-soul/.git`)
- 16 commits on `main`, last commit Mar 19 (`add 8 tools to connector registry (134 total)`)
- README.md is polished (17.6KB, full module catalog, comparison matrix vs LangGraph/CrewAI/AutoGen/DSPy/OpenClaw/Hermes, production numbers, env vars, MIT license)
- `pyproject.toml` declares 17 entry points (`sovrun-voice`, `sovrun-engine`, `sovrun-loops`, etc.), Python >=3.10, deps = `tenacity` + `httpx`
- LICENSE = MIT, 2026 copyright
- 134 MCP connectors in `connectors/registry.json` (80KB)
- Templates: `SOUL.md`, `bias-null.md`, `voice-config.json`, `CLAUDE.md`
- Examples: correction_chains.json, meta_rules.md

**Deploy state**:
- Static site (`site/index.html`, 29KB hand-rolled CSS) is wired into cron Sunday 5:04 AM via `surge` to `sovrun-agent-os.surge.sh`
- Next.js marketing site (`website/`) is a SEPARATE git repo with its own `.git/`, 2 commits, **uncommitted changes**: 5 modified files (`package.json`, `globals.css`, `layout.tsx`, `page.tsx`, `package-lock.json`) + untracked `docs/`, `pricing/`, `comparison-table.tsx`, `footer.tsx`, `link-button.tsx`. **Not deployed** — only static `site/` is.
- Parent agent-soul repo shows `M website` (submodule pointer dirty)

**Open decisions for sovrun**:
1. Sync uncommitted Next.js website changes — likely the real comparison table, pricing, docs pages — into deployable form OR delete and standardize on static `site/`
2. Decide whether `site/` (static, deployed) or `website/` (Next.js, more polished but unpublished) is canonical
3. Strip `site/index.html.backup.*` cruft before public attention
4. README still mentions "sovrun.git" as homepage which matches reality, good
5. The Sunday surge deploy currently overrides any updates to `website/` since only `site/` is targeted

**Wired into PRINTMAXX**: confirmed in `AUTOMATIONS/_common.py`, `agent_swarm.py`, `ceo_agent.py`, `venture_autonomy.py`, `loop_closer.py`, `control_panel.py`, `morning_intelligence_dag.py`, `seed_skills.py`, `auto_approve.py`. Also dozens of generated `dag_runner_*.py` scripts import from it. The `commands-reference.md` rule has 2 procedural-memory commands using `sys.path.insert(0,'OPEN_SOURCE/agent-soul')`.

**Critical coupling**: `agent_swarm.py` skills DB is at `AUTOMATIONS/agent/sovrun/skills.db`. If sovrun is ever extracted to a separate machine/install, the import path `OPEN_SOURCE/agent-soul` must remain stable OR PRINTMAXX needs `pip install -e ./OPEN_SOURCE/agent-soul` to register `sovrun` proper.

## Other open-source candidates

**`OPEN_SOURCE/remote-control-daisy-chain/`** — small, focused, clearly sanitized for public release. README explicitly defines security boundary: scripts/templates/docs safe to publish, no config values or tailnet names. Status: appears **ready** but **stalled** since Mar 13. Has no GitHub remote configured (no `.git` directory at root — confirmed not present in `ls -la`). Needs: (a) create GitHub repo, (b) push, (c) add LICENSE file (none present), (d) decide if it deserves a separate landing page. Low surface area, low risk.

Nothing else in `OPEN_SOURCE/` — only the two subdirectories.

## external/ contents (purpose, status)

**`external/openclaw-official/`** — full clone of OpenClaw monorepo (Feb 18, 2026 snapshot). Massive: pnpm-lock.yaml is 387KB, includes Swift app `Swabble/`, Rust + Node + Swift sources, fly.toml, render.yaml, 84 scripts, CHANGELOG is 263KB. Latest commit visible: `test(infra): dedupe update-runner fixture setup`. Used for: studying their patterns. Memory says they had 512 vulns + 20% malicious skills — this is **reference-only, do NOT execute their code**. No active development here.

**`external/hcom/`** — third-party tool (`github.com/aannoo/hcom`), v0.7.2 with "Termux/Android support and code consolidation". Includes Rust source (`src/`), plugin/, skills/, tests/. User memory explicitly says: **NO hcom hooks**. Inactive in this project — not imported anywhere.

Neither external repo is under active development by us. Both are reference clones. `.git/` directories present so they can be `git pull`'d for updates but no fork/branch work happening here.

## Top 3 Risks

1. **Two parallel websites, one deployed, the other has uncommitted UX upgrades** — Sunday cron deploys static `site/` but the Next.js `website/` has modified `page.tsx` + new `docs/`/`pricing/` routes that have never shipped. Risk: someone visits `sovrun-agent-os.surge.sh` and sees the stale hand-rolled HTML while the polished Next.js work rots locally. The 2-commit `website/` git repo will also drift further from main agent-soul repo until reconciled.

2. **Open-source release timing vs PRINTMAXX coupling** — sovrun is imported by 10+ PRINTMAXX scripts via path injection (`sys.path.insert(0, 'OPEN_SOURCE/agent-soul')`). If someone clones the public sovrun repo and `pip install -e .`s it, the package name resolves to `sovrun` not `OPEN_SOURCE.agent-soul` — PRINTMAXX's bespoke import path is inconsistent with the published package. Either rename the local directory to `sovrun/` or install it locally as a proper package.

3. **No CI, no tests visible, no security audit gate before public attention** — sovrun README claims "production-grade", "2 dependencies", "126 MCP connectors with auto-setup". Publishing without tests + without confirming the 134 connectors don't ship known-malicious MCP server commands is a reputational risk. The `external/openclaw-official/` lesson (512 vulns) was learned for inputs; the output (sovrun) hasn't been similarly vetted. `remote-control-daisy-chain/` also has no LICENSE file yet.

## Top 3 Opportunities

1. **Ship the Next.js website** — reconcile the uncommitted website changes, build, and update the cron deploy to push `website/.next/` (or migrate sovrun's public face to Vercel). The hand-rolled `site/index.html` is functional but the Next.js version with shadcn components, comparison table, pricing page, and docs page is clearly the intended next state. Marketing matters for OSS adoption.

2. **Publish `remote-control-daisy-chain`** — it's small, focused, well-documented, sanitized, and would attract a different audience (Mac power users, remote workers) than sovrun. Cheap visibility win. Needs only: LICENSE, GitHub repo, push. 30 minutes of work blocks zero PRINTMAXX revenue.

3. **Turn sovrun's connector registry into a standalone product** — `connectors/registry.json` is 80KB of 134 curated MCP connectors with capability tags. This could be its own searchable index/site or a discovery tool independent of the agent OS. Lower-effort second OSS surface that drafts on sovrun traffic.

## For the /goal long-run command

**Recommendation: `/goal` should SKIP open-source maintenance by default. Create a separate `/publish` (or `/oss`) command.**

Reasons:
- Open-source work is **publish-cadence**, not daily-grind. The Sunday 5:04 AM surge cron already handles the only live deploy. Daily attention adds no value.
- The dominant `/goal` directive in MEMORY.md is **revenue** ("$0 revenue at Day 35", "SHIP NOW", "execute don't document"). Open-source work is reputation/funnel — important but orthogonal to direct revenue.
- The Anti-Entropy rule explicitly says "Revenue Reality Check: will this specific action lead to a dollar entering a bank account?". Open-source maintenance fails this for `/goal`'s scope.

**However, `/goal` SHOULD touch open-source in these cases (overlap flags)**:

- **When a PRINTMAXX pattern emerges that belongs in sovrun** — Rule from `sovrun-sync.md`: "When PRINTMAXX patterns emerge that should be in sovrun: extract the reusable pattern into `OPEN_SOURCE/agent-soul/core/`". `/goal` already extends PRINTMAXX scripts; if the extension is generic, the extraction is one-line.
- **When uncommitted website changes block a planned release** — flag if `git status` in `OPEN_SOURCE/agent-soul/website/` shows >5 modified files for >7 days.
- **When sovrun import paths break PRINTMAXX** — sovrun is imported by 10+ scripts; if `OPEN_SOURCE/agent-soul/core/*.py` changes break callers, `/goal` MUST notice (run a smoke test, not just claim "wired").
- **When new MCP connectors arrive in `daily_tool_scout` output** — should funnel into `connectors/registry.json` automatically (this is content for OSS but came from the daily flow).

**Suggested `/publish` command scope** (NOT for `/goal`):
1. Reconcile `website/` uncommitted changes; build and deploy.
2. Push any local agent-soul commits to `origin/main`.
3. Run a security pass on connector registry additions.
4. Create GitHub repo + LICENSE for `remote-control-daisy-chain` (one-time).
5. Cadence: weekly (mirrors the Sunday surge deploy) or on-demand.

**Quick win for `/goal` overlap**: in the daily run, log a one-line "OSS drift" status if (a) `website/` has uncommitted changes >7 days old, or (b) `agent-soul/` has unpushed commits, or (c) sovrun imports fail in any PRINTMAXX core script. This is monitoring without owning the release workflow.

**Files for `/goal` to leave alone**: anything under `OPEN_SOURCE/agent-soul/website/` (separate git repo, separate cadence), `external/*` (third-party, read-only), `OPEN_SOURCE/agent-soul/site/index.html.backup.*` (cruft to be deleted by `/publish`, not `/goal`).
