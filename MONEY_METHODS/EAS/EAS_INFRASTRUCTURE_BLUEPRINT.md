# EAS Infrastructure & Safety Blueprint — March 2026

## Deployment Options (Client-Facing)

### Default: Hetzner VPS ($8-15/mo per client)
- CX32: 4 vCPU, 8GB RAM, 80GB SSD — $7.50/mo
- One VM per client (clean isolation)
- Snapshots at $0.01/GB/mo (40GB VM = $0.40/mo for daily snapshots)
- Private networks between VMs at no cost
- US datacenter in Ashburn, VA
- Tailscale for remote management

### Premium: Mac Mini On-Premise ($499-599 one-time)
- For regulated industries (legal, medical, financial)
- Data never leaves client's premises
- Pair with: UPS ($60), Tailscale (remote access), external SSD backup
- Power cost: $3-5/mo

### Dev/Test Only: Oracle Cloud Free Tier
- 2 free ARM VMs forever (up to 24GB RAM)
- Risk: Oracle reclaims "idle" instances
- Never for client-facing production

## Container Architecture

One container stack per client (NOT one container per agent):

```
Per-Client Container:
├── supervisord (process manager)
├── Agent 1 (cron-scheduled)
├── Agent 2 (cron-scheduled)
├── Agent N...
├── /data/ (bind mount, per-client, encrypted)
├── /config/ (read-only bind mount)
└── /logs/ (bind mount to host)
```

Security hardening:
- Run as non-root (USER 1000:1000)
- Drop all caps (--cap-drop=ALL)
- Read-only root filesystem
- Memory limit (512MB)
- CPU limit (0.5 cores)
- no-new-privileges
- Seccomp default profile

## Three-Level Circuit Breaker

**Level 1 (Per-Action):** 3 consecutive failures → exponential backoff (1min→5min→15min→1hr)
**Level 2 (Per-Agent):** Health <50% over 20 actions → pause agent + alert
**Level 3 (System-Wide):** >30% agents in breaker state → pause ALL + alert

Critical: circuit breaker logic OUTSIDE the model. The AI doesn't decide whether to stop itself.

## Action Budget System

Each agent gets per-cycle limits enforced by supervisor:
- Max API calls: 10
- Max file writes: 5
- Max external actions (emails, API writes): 2
- Max tokens: configurable per model tier
- Max spend: $X/day hard cap

## Approval Gates

| Action Level | Auto-Approve? | Examples |
|---|---|---|
| LOW | Yes (log only) | Read data, log events |
| MEDIUM | Yes (log + monitor) | Write data, call APIs |
| HIGH | Requires human approval | Send emails, modify configs, spend money |
| CRITICAL | Requires 2 humans | Delete data, change permissions |

## Killswitch

Every deployment includes:
1. `killswitch.sh` — stops all containers, disables cron, creates lockfile, alerts Slack
2. Every agent checks for lockfile before executing
3. Remote trigger via SSH/Tailscale or Hetzner API (stop VM)
4. Per-client kill (docker stop by label) — doesn't affect other clients
5. Recovery requires explicit human action (not automated)

## Model-Agnostic Architecture

Use **LiteLLM** as local proxy:
- All agents hit localhost:4000
- LiteLLM routes to Claude, GPT, Gemini, or open-source
- Provider switch = config change, not code change
- Fallback routing: if Claude API down → auto-route to GPT-4
- Supports Azure OpenAI for EU data residency requirements

### Smart Model Routing (6x cost reduction)

| Task Type | Model | Cost/Cycle |
|---|---|---|
| Routine checks (60%) | Haiku / GPT-4o-mini | $0.002 |
| Standard decisions (30%) | Sonnet / GPT-4o | $0.03 |
| Complex reasoning (10%) | Opus | $0.19 |
| **Blended (48 cycles/day)** | **Mixed** | **$1.43/day = $43/mo** |

vs. all-Opus: $270/mo per agent (6x more expensive)

## Client Cost Model

Per agent: $43/mo API + $3/mo compute = $46/mo cost
Client pays: $75-315/mo per agent (depending on tier)
Margin: 40-85%

At 5 agents per client: $375-1,575/mo
vs. part-time employee: $2,000-3,000/mo

## Risk Disclosure Per Agent

Every deployed agent gets a one-page risk card:
- What it CAN do (specific permissions)
- What COULD go wrong (specific risks with likelihood/impact)
- Controls in place (circuit breakers, budgets, approval gates)
- How to stop it (killswitch instructions)
- Client responsibilities (review digests, respond to approvals)
- Our responsibilities (monitoring, patches, monthly reports)

## Monitoring Minimum Viable Stack

1. Healthchecks.io (free: 20 checks) — cron monitoring
2. Structured JSON logs with daily cost report
3. Slack webhooks for P0/P1 alerts
4. Monthly agent performance report

## Network Isolation

- Container network isolation (each client on own Docker bridge)
- Egress whitelist (only approved API endpoints)
- API proxy for logging/rate limiting
- DNS control for high-security clients
- VLANs for on-premise only
