# Ralph Task: Roblox Game Factory

**Task ID:** 11_roblox_game_factory
**Status:** READY
**Priority:** Phase 4 (Month 3+)
**Prerequisites:** Roblox Studio MCP installed, Claude Desktop configured

---

## Objective

Build profitable Roblox experiences using Claude + Roblox Studio MCP. Target: $1k-5k/mo passive from Robux earnings within 6 months.

---

## Ralph Loop Configuration

```bash
# Run with Claude Code
./scripts/ralph/ralph.sh --tool claude 20

# Or create dedicated prd.json (see below)
```

### prd.json Template

```json
{
  "project": "PRINTMAXX",
  "branchName": "ralph/roblox-game-001",
  "description": "Build Roblox game: Prayer Obby - faith-themed obstacle course",
  "userStories": [
    {
      "id": "RBX-001",
      "title": "Setup Roblox Studio project",
      "description": "Create new Roblox project with basic terrain",
      "acceptanceCriteria": [
        "New place created in Roblox Studio",
        "Basic spawn location set",
        "Lighting configured for theme"
      ],
      "priority": 1
    },
    {
      "id": "RBX-002",
      "title": "Build core obby sections",
      "description": "Create 10 obby stages with increasing difficulty",
      "acceptanceCriteria": [
        "10 unique obby stages",
        "Checkpoints between stages",
        "Kill bricks/lava configured"
      ],
      "priority": 2
    },
    {
      "id": "RBX-003",
      "title": "Add faith theming",
      "description": "Add prayer/faith visual elements",
      "acceptanceCriteria": [
        "Cross/faith themed decor",
        "Peaceful ambient sounds",
        "Inspirational text displays"
      ],
      "priority": 3
    },
    {
      "id": "RBX-004",
      "title": "Implement monetization",
      "description": "Add Robux purchases",
      "acceptanceCriteria": [
        "Skip stage pass (10 Robux)",
        "VIP pass for cosmetics (50 Robux)",
        "Developer products for coins"
      ],
      "priority": 4
    },
    {
      "id": "RBX-005",
      "title": "Test and publish",
      "description": "Playtest and publish to Roblox",
      "acceptanceCriteria": [
        "All stages playable",
        "No critical bugs",
        "Published with SEO title/description"
      ],
      "priority": 5
    }
  ]
}
```

---

## Game Ideas Queue (Niche Adapted)

| Game # | Type | Niche Adaptation | Monetization |
|--------|------|------------------|--------------|
| 001 | Obby | Prayer Obby - faith themed | Skip stage, VIP |
| 002 | Idle/Cozy | Grow A Prayer Garden | Rare seeds, tools |
| 003 | Simulator | Bible Study Simulator | Speed boosts, pets |
| 004 | Tycoon | Church Tycoon | Decorations, expansions |
| 005 | Roleplay | Christian Youth Camp RP | Outfits, cabins |
| 006 | Obby | Fitness Obby - gym themed | Muscle skins |
| 007 | Simulator | Study Simulator | Brain pets, focus boosts |
| 008 | Horror | Scripture Escape Room | Hints, flashlight |

---

## MCP Commands Reference

Use these prompts with Roblox Studio MCP:

### Basic Setup
```
"Create a new obby baseplate with spawn location"
"Add checkpoints every 5 studs vertically"
"Insert lava bricks that kill on touch"
```

### Faith Theming
```
"Add a glowing cross decoration at the end"
"Insert peaceful ambient music"
"Create floating bible verse text"
```

### Monetization
```
"Create a developer product for 10 Robux that skips current stage"
"Add VIP door that requires gamepass ownership"
```

---

## Success Metrics

| Metric | Target (30 days) | Target (90 days) |
|--------|------------------|------------------|
| DAU | 100 | 500 |
| Robux earned | 5,000 | 25,000 |
| Premium payouts | $10 | $50 |
| Rating | 70%+ | 80%+ |

---

## Marketing Integration

After game launches:
1. Create TikTok gameplay clips via Remotion
2. Post to Roblox-focused content accounts
3. Cross-promote in CONTENT_FARM channels
4. Track in LEDGER/ROBLOX_GAMES_TRACKER.csv

---

## Guardrails for Roblox Ralph

Add to .ralph/guardrails.md:

```markdown
### Sign: Test all obby stages
- Trigger: Publishing Roblox game
- Instruction: Playtest every stage before publish
- Source: Player experience

### Sign: Monetization must be optional
- Trigger: Adding Robux purchases
- Instruction: Game must be completeable without spending
- Source: Roblox community expectations

### Sign: Faith content must be positive
- Trigger: Creating faith-themed games
- Instruction: Uplifting only, no judgment or exclusion
- Source: Niche positioning
```

---

## Autonomous Run Checklist

Before overnight ralph loop:

- [ ] Roblox Studio open and logged in
- [ ] MCP plugin installed and connected
- [ ] prd.json configured with target game
- [ ] Test MCP connection with simple command
- [ ] progress.txt cleared for fresh run

---

## References

- Playbook: `MONEY_METHODS/ROBLOX_GAMES/ROBLOX_GAME_FACTORY_PLAYBOOK.md`
- MCP Docs: [DevForum Announcement](https://devforum.roblox.com/t/introducing-the-open-source-studio-mcp-server/3649365)
- Revenue Data: Top 10 devs earn $33.9M avg/year
- Platform Stats: 151.5M DAU, $923M paid to creators (2024)

---

Last updated: 2026-01-24
