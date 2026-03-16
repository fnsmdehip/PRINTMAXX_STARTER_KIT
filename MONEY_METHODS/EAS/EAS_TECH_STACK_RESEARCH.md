# EAS Tech Stack — Research-Backed Recommendations (March 2026)

## Ranked Production Stack

| Rank | Tool | Category | Cost | Why It Wins |
|------|------|----------|------|-------------|
| 1 | n8n (self-hosted) | Workflow Engine | Free | Foundation layer. 177K stars, 400+ integrations. Clients understand visual workflows. |
| 2 | Composio | Integration Platform | $29/mo | 900+ connectors with managed OAuth. Eliminates weeks of auth integration work per project. |
| 3 | LangGraph | Agent Orchestration | Free + $39/seat LangSmith | Best production agent framework. Checkpointing, time-travel debugging, graph-based state machines. |
| 4 | Claude Agent SDK | Agent Framework | API rates only | Build Claude Code-level autonomous agents. Same harness powering Claude Code. v0.1.48. |
| 5 | Retell AI | Voice Agents | $0.11-0.15/min | 600ms latency (fastest), 99.99% uptime, HIPAA included free. Clear winner over Bland/Vapi. |
| 6 | MCP Protocol | Tool Integration | Free standard | 97M monthly downloads, Linux Foundation standard. Enterprise adoption wave starting NOW. |
| 7 | Qdrant | Vector DB / RAG | Free self-hosted | Best open-source vector DB. 50ms p99, advanced filtering. Free self-host or $25/mo cloud. |
| 8 | CrewAI | Agent Orchestration | Free-$99/mo | Best for demos and MVPs. Clients can read agent definitions. Native MCP + A2A in v1.10.1. |
| 9 | Windmill | Workflow Engine | Free self-hosted | 10x faster than Airflow. Rust scheduler. For when n8n isn't performant enough. |
| 10 | Temporal | Workflow Engine | Free self-hosted | Mission-critical only. Never loses state. Reserve for enterprise engagements. |

## Voice Platform Comparison

| Platform | Latency | Uptime | Cost/min (all-in) | HIPAA | Best For |
|----------|---------|--------|-------------------|-------|----------|
| Retell AI | 600ms | 99.99% | $0.11-0.15 | Included free | Production deployments (our default) |
| Vapi | 700ms | 99.9% | $0.13-0.31 | $1,000/mo add-on | Deep custom integrations only |
| Bland AI | 800ms | 99.5% | $0.09 connected | Not stated | High-volume outbound campaigns |

## Hype Traps (AVOID)
- **Synthflow, Air AI** — Marketing hype, consistently ranked below Retell/Vapi/Bland on benchmarks
- **AutoGen / AG2** — Microsoft rewrite still unstable. Skip for client work.
- **MetaGPT** — Research project, not consulting-grade
- **Most "AI content tools"** — Thin GPT wrappers with UI. Build your own with n8n + Claude API.
- **Relevance AI** — Credit-based pricing escalates fast. Third choice behind Composio and Lindy.

## Key Strategic Insight

The gap between "I connected Zapier to ChatGPT" and "I built a production multi-agent system with observability, checkpointing, and MCP integrations" is where the serious money is. Every competitor will have n8n + basic RAG. The differentiation layer is: custom multi-agent systems (LangGraph/Claude Agent SDK), MCP enterprise integrations (Composio), voice AI (Retell), and autonomous pipelines.

## Sources
Full research with URLs in agent output (March 16, 2026).
