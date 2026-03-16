# Enterprise Automation Solutions (EAS) — Venture Overview

## What it is

Productized automation consulting service. We sell fixed-scope packages to SMBs (dental, legal, HVAC, agencies), delivered by subcontractors following playbooks. DBA under existing Wyoming LLC.

## Domain

enterpriseautomation.solutions

## Revenue model

| Package | Price | Timeline | Margin |
|---------|-------|----------|--------|
| Signal Map | $1,500 flat | 5 days | 60-70% |
| Phone Pilot | $3,500 flat | 10 days | 55-65% |
| Ops Pilot | $4,500 flat | 10 days | 55-65% |
| Managed Ops | $1,500-3,000/mo | Ongoing | 50-65% |

Cash flow: 50% upfront, 50% on delivery. Subcontractors paid from client funds.

## Lead pipeline

PRINTMAXX scrapers repurposed for EAS:
1. `savvy_lead_scraper.py` — scores businesses 0-100 on website quality, phone presence, review count
2. `nationwide_scraper.py` — discovers businesses across 203 US cities
3. `mass_outreach.py` — sends personalized cold emails with specific website issues
4. `eas_lead_pipeline.py` — filters scored leads for EAS fit, generates outreach CSV

## Key files

| What | Where |
|------|-------|
| Website (7 pages) | `MONEY_METHODS/EAS/website/` |
| Legal templates | `MONEY_METHODS/EAS/legal/` |
| Delivery playbooks | `MONEY_METHODS/EAS/playbooks/` |
| Outreach templates | `MONEY_METHODS/EAS/outreach/` |
| Lead pipeline | `AUTOMATIONS/eas_lead_pipeline.py` |

## Delivery stack (research-backed, March 2026)

- **Claude API + Agent SDK** — AI brain. Build autonomous agents at Claude Code level.
- **n8n** (self-hosted) — Workflow orchestration backbone. 177K stars, 400+ integrations.
- **LangGraph** — Production multi-agent orchestration. Checkpointing, observability via LangSmith.
- **Retell AI** — Voice agents. 600ms latency, 99.99% uptime, HIPAA included. Best in class.
- **Composio** — 900+ tool integrations with managed OAuth. $29/mo. Saves weeks per project.
- **Qdrant** — Vector DB for RAG. Free self-hosted, 50ms p99. Enterprise: Pinecone.
- **MCP Protocol** — Standardized AI tool integration. 97M monthly downloads, Linux Foundation.
- **Cal.com** (free) — Scheduling
- **Instantly.ai** ($30/mo) — Cold email at scale
- **CrewAI** — Agent demos and client-readable agent definitions. Native MCP support.

See full research: `EAS_TECH_STACK_RESEARCH.md`

## Cross-pollination with other PRINTMAXX ventures

- EAS leads that need websites → LOCAL_BIZ pipeline (S02)
- EAS case studies → CONTENT pipeline (C04 Twitter, C05 Newsletter)
- EAS playbooks → PRODUCT pipeline (sell on Gumroad/Whop)
- EAS subcontractor network → FREELANCE pipeline (S01 reverse: we hire instead of get hired)

## Status

- Website: BUILDING
- Legal: BUILDING
- Lead pipeline: BUILDING
- Revenue: $0
- Blockers: DBA filing, bank account, Cal.com setup
