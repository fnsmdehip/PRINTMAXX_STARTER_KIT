# Intelligence Router

## Overview

Routes 15,000+ alpha intelligence entries across 9 venture types with auto-enrichment from structured operational data. Every agent in the system queries the router before executing any task, ensuring decisions are based on accumulated intelligence rather than default LLM knowledge. The router aggregates alpha CSVs, strategy docs, swarm reports, method-specific CSVs, and growth tactics into a single, venture-specific intelligence brief.

## Architecture

The router operates as a centralized intelligence hub with multiple data source integrations converging into a unified query interface.

```
                       +-------------------+
                       | Intelligence      |
                       | Router            |
                       +--------+----------+
                                |
        +-----------+-----------+-----------+-----------+
        |           |           |           |           |
   Alpha CSVs  Strategy    Swarm       Method      Growth
   (scored,    Docs        Reports     CSVs        Tactics
    ranked)    (playbooks) (agent      (LEDGER/)   (platform
                            intel)                  guides)
```

**Data flow:**

1. Agent requests intelligence for a specific venture + task (e.g., `CONTENT` + `posting`)
2. Router loads the intelligence catalog (JSON index of 400+ docs with summaries)
3. Queries the alpha staging CSV via the alpha query module for venture-relevant entries
4. Matches strategy documents from a hardcoded intelligence map (venture -> docs, dirs, CSVs, task-specific docs)
5. Pulls latest swarm reports from agent-generated intel
6. Auto-enriches with Master Ops xlsx data via a bridge module (ops scores, synergy stacks, blockers, playbooks)
7. Applies cache with TTL to avoid redundant disk reads
8. Returns a unified intelligence brief (JSON or human-readable)

**Venture types supported:** CONTENT, OUTBOUND, APP_FACTORY, LOCAL_BIZ, MONETIZATION, PRODUCT, RESEARCH, SCRAPING, GROWTH

**Task types per venture:** Each venture has 8-10 task types that narrow the intelligence to the most relevant subset. For example, CONTENT supports: posting, warmup, engagement, distribution, repurpose, scheduling, reply, thread, carousel, video.

## Required Inputs

- **Alpha staging CSV** -- scored alpha entries with columns: source, category, roi_potential, status, reviewer_notes, engagement_authenticity, venture_tag
- **Intelligence catalog JSON** -- index of all docs with `high_value_summary` field, auto-merged from deep scans
- **Strategy documents** -- markdown playbooks, growth guides, platform research (organized by venture type in ops directories)
- **Swarm reports** -- agent-generated intelligence reports from the 25-agent operational swarm
- **Method CSVs** -- venture-specific tracking CSVs in the LEDGER directory (winning content structures, marketing channels, app factory methods)
- **Master Ops xlsx** (optional) -- the operational spreadsheet with 182 ops, automation scores, synergy stacks, and venture maps

## Outputs

- **JSON intelligence brief** -- structured output for agent consumption with keys: `alpha` (top entries), `docs` (relevant doc paths + summaries), `swarm_reports` (latest agent intel), `methods` (method CSV paths), `tactics` (extracted tactical directives), `brief` (one-paragraph summary)
- **Human-readable brief** -- markdown-formatted summary for interactive sessions
- **Enriched agent contexts** -- when auto-enrichment is enabled, includes ops scores, synergy multipliers, blocker status, and playbook steps from the Master Ops bridge
- **Stats output** -- index health metrics: total docs mapped, coverage percentage, docs by venture

## Setup

1. **Create the directory structure:**
   ```
   project/
   ├── AUTOMATIONS/
   │   ├── intelligence_router.py
   │   ├── alpha_query.py
   │   └── master_ops_bridge.py (optional)
   ├── LEDGER/
   │   ├── ALPHA_STAGING.csv
   │   └── MEGA_SHEET/ (method CSVs)
   ├── OPS/
   │   └── INTELLIGENCE_CATALOG.json
   └── [venture-specific strategy doc directories]
   ```

2. **Populate the alpha staging CSV** with your intelligence entries. Minimum columns: `source`, `category`, `roi_potential`, `status`.

3. **Build the intelligence catalog** by scanning your docs directory and generating a JSON index with summaries per document.

4. **Configure the intelligence map** in the router -- map each venture type to its relevant docs, directories, CSVs, and task-specific documents.

5. **Set up the alpha query module** to support venture-based filtering and keyword search across the alpha CSV.

6. **(Optional) Wire in a Master Ops bridge** if you track operations in a spreadsheet -- the bridge provides ops scores, synergy stacks, and blockers as enrichment data.

## Example Usage

Query intelligence before building content:
```bash
python3 intelligence_router.py --venture CONTENT --task posting --brief
```

Get JSON output for an automated agent to consume:
```bash
python3 intelligence_router.py --venture OUTBOUND --task outreach --json
```

Check index health and coverage:
```bash
python3 intelligence_router.py --stats
```

List all indexed documents:
```bash
python3 intelligence_router.py --catalog
```

Use as a Python module inside an agent:
```python
from intelligence_router import get_intelligence

intel = get_intelligence("APP_FACTORY", task_type="launch")
# intel["alpha"]  -> top alpha entries for app launches
# intel["docs"]   -> relevant strategy docs with summaries
# intel["brief"]  -> one-paragraph summary
```

## Key Patterns

- **Venture-based routing** -- intelligence is partitioned by venture type, so agents only receive signal relevant to their domain. No information overload.
- **Task-type narrowing** -- within a venture, task types further filter to the most relevant docs. A "posting" task surfaces different docs than a "warmup" task, even within the same CONTENT venture.
- **Auto-enrichment pipeline** -- the router automatically enriches its output with data from the Master Ops bridge (automation scores, synergy multipliers, blockers) without the caller needing to know about the bridge.
- **Cache with TTL** -- the xlsx bridge cache has a 12-hour TTL, rebuilt via cron. The router itself caches doc reads to avoid redundant disk I/O during a single cycle.
- **Fallback chains** -- the catalog reader falls back from `high_value_summary` to `buried_gold_summary` if the primary key is missing, ensuring backward compatibility as the catalog format evolves.
- **Path guardrails** -- every file path is validated against the project root before access. Paths outside the project are blocked with a ValueError.
- **Intelligence-first mandate** -- the system enforces that every agent queries the router before executing any task. This is a rule, not a suggestion. Actions taken on default LLM knowledge when 15,000+ alpha entries exist are considered failures.

## Limitations

- The intelligence map (venture -> docs) is hardcoded and must be manually updated when new strategy documents are added. An auto-discovery mechanism would improve this.
- Alpha CSV must be pre-scored and pre-categorized. The router consumes processed alpha, not raw scraper output.
- The Master Ops bridge enrichment requires openpyxl and a specific xlsx schema. Without the bridge, the router still works but returns less context.
- Cache invalidation is time-based (TTL), not event-based. If a new alpha batch is processed mid-cycle, the router may serve stale data until the cache expires.
- The router does not rank or re-score intelligence entries -- it passes through the scores assigned during alpha processing. Ranking logic lives in the alpha query module.
- Swarm report aggregation is directory-based (reads all files in a reports directory). If swarm reports are stored elsewhere, the router won't find them without configuration changes.
