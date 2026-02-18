# RobloxMaxx Local Creation Station

You are building a Roblox game using Claude Code with MCP servers connected directly to Roblox Studio. You write production-ready Luau code and manipulate Studio objects through MCP tools.

---

## MCP Tools Available

You have two MCP server connections:

### robloxstudio (37+ tools - primary)
Use the `robloxstudio` MCP for all development work:
- Read game hierarchy (instances, properties, scripts)
- Create/modify/delete instances
- Read and write script source code
- Execute Lua code in Studio
- Bulk operations across the game tree
- Insert models
- Manipulate properties on any instance

### roblox-test (test automation)
Use the `roblox-test` MCP for QA and testing:
- Start/stop play testing mode
- Execute Lua in game context during play test
- Capture screenshots (with compression options)
- Multi-frame sequence capture
- Get full game state (player position, health, stats, logs)
- Get logs only (93% more token-efficient than screenshots)
- Verify plugin connection

### When to Use Which

| Task | MCP Server |
|------|-----------|
| Creating scripts | robloxstudio |
| Editing game hierarchy | robloxstudio |
| Reading existing code | robloxstudio |
| Running code in edit mode | robloxstudio |
| Play testing | roblox-test |
| Taking screenshots | roblox-test |
| Checking game state during play | roblox-test |
| Debugging runtime behavior | roblox-test |

---

## Luau Code Standards

Write Luau, not Lua 5.1. Use modern features:

```luau
-- Type annotations
local function calculateDamage(base: number, multiplier: number): number
    return base * multiplier
end

-- String interpolation
local message = `Player {player.Name} earned {amount} coins`

-- If-expressions
local result = if condition then valueA else valueB

-- Compound assignments (Roblox Luau extension)
count += 1
health -= damage
```

### Banned Patterns (deprecated)

| Deprecated | Use Instead |
|-----------|-------------|
| `wait()` | `task.wait()` |
| `spawn()` | `task.spawn()` |
| `delay()` | `task.delay()` |
| `Instance.new("Weld")` on server for character | Use `RigidConstraint` or `WeldConstraint` |
| `BodyVelocity` | `LinearVelocity` (attachments-based) |
| `BodyForce` | `VectorForce` |
| `BodyGyro` | `AlignOrientation` |
| `BodyPosition` | `AlignPosition` |

### Service Access Pattern

```luau
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local DataStoreService = game:GetService("DataStoreService")
local MarketplaceService = game:GetService("MarketplaceService")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local PathfindingService = game:GetService("PathfindingService")
```

### Client-Server Security

NEVER trust the client. All game logic that affects state, currency, inventory, or progression must run server-side.

```luau
-- SERVER: Validate all RemoteEvent inputs
remote.OnServerEvent:Connect(function(player, action, ...)
    -- Validate player is who they claim to be
    -- Validate action is a valid string
    -- Validate all arguments are expected types
    -- Rate limit (track last action time per player)
    -- Then process
end)
```

### Data Persistence Pattern

```luau
local DataStoreService = game:GetService("DataStoreService")
local playerStore = DataStoreService:GetDataStore("PlayerData_v1")

local function loadData(player: Player)
    local success, data = pcall(function()
        return playerStore:GetAsync("Player_" .. player.UserId)
    end)
    if success and data then
        return data
    end
    return getDefaultData() -- Always have defaults
end

local function saveData(player: Player, data: {[string]: any})
    local success, err = pcall(function()
        playerStore:SetAsync("Player_" .. player.UserId, data)
    end)
    if not success then
        warn(`Failed to save data for {player.Name}: {err}`)
    end
end

-- Save on leave
Players.PlayerRemoving:Connect(function(player)
    saveData(player, playerDataCache[player.UserId])
end)

-- Save on server shutdown
game:BindToClose(function()
    for _, player in Players:GetPlayers() do
        saveData(player, playerDataCache[player.UserId])
    end
end)
```

---

## Game Architecture Standards

### Script Organization

```
game
├── ServerScriptService/
│   ├── GameManager (Script) - core loop, state machine
│   ├── DataManager (Script) - persistence, caching
│   ├── EconomyManager (Script) - currency, purchases
│   └── [GenreSpecific] (Script) - genre mechanics
├── ReplicatedStorage/
│   ├── Remotes/ (Folder)
│   │   ├── GameEvents (RemoteEvent)
│   │   └── GameFunctions (RemoteFunction)
│   ├── Modules/ (Folder)
│   │   ├── GameConfig (ModuleScript) - shared constants
│   │   └── SharedUtils (ModuleScript) - shared functions
│   └── Assets/ (Folder) - shared models, effects
├── StarterGui/
│   └── GameHUD (LocalScript) - all UI
├── StarterPlayerScripts/
│   └── InputController (LocalScript) - input handling
└── ServerStorage/
    └── Templates/ (Folder) - cloneable templates
```

### RemoteEvent Naming

Use clear verb-noun naming:
- `PurchaseItem` not `Buy`
- `UpdateCurrency` not `Money`
- `ClaimReward` not `Reward`
- `RequestTrade` not `Trade`

### ModuleScript Config Pattern

```luau
-- ReplicatedStorage/Modules/GameConfig
local Config = {}

Config.Currency = {
    StartAmount = 0,
    MaxAmount = 999_999_999,
}

Config.Gamepasses = {
    DoubleEarnings = 12345678, -- Replace with actual gamepass ID
    VIPAccess = 12345679,
    AutoCollect = 12345680,
}

Config.DevProducts = {
    SmallCoinPack = { id = 12345681, amount = 1000 },
    MediumCoinPack = { id = 12345682, amount = 5000 },
    LargeCoinPack = { id = 12345683, amount = 25000 },
}

return Config
```

---

## Roblox Platform Meta Intelligence (Feb 2026)

This section contains current data about what works on Roblox. Use this to make game design recommendations.

### Platform Scale

- 144M DAU, $6.8B bookings (2025), growing 55% YoY
- $1B+ paid to creators in 2025
- 12M+ monthly active creators in Studio
- Peak concurrent: 47.4M platform-wide
- Individual game record: 22.3M concurrent (Grow a Garden)

### Genre Effectiveness (current meta)

| Genre | Revenue Share | Saturation | Recommendation |
|-------|-------------|------------|----------------|
| Simulators (idle/farming/pet) | ~35% | HIGH but top-heavy | Only enter with genuine innovation or niche angle |
| Action/anime RPG | ~25% | HIGH | Need mechanical innovation to compete |
| Social/roleplay/hangout | ~20% | MEDIUM | Strong if paired with UGC/identity mechanics |
| FPS/combat | ~10% | MEDIUM-LOW | Growing as audience ages up |
| Tycoon/builder | ~5% | HIGH for generic | Niche tycoons can still work |
| Horror/procedural | ~5% | LOW-MEDIUM | Good opportunity, lower competition |

### What's Hot Right Now (Feb 2026)

1. **Calm farming/gardening sims** - Grow a Garden broke records (22.3M CCU). Short idle loops + rare drops + trading economies. LOW dev complexity, HIGH engagement.

2. **Hybrid genre games** - Fisch (fishing + RPG + social), The Forge (mining + crafting + combat). Genre blending creates unique positioning.

3. **Social hangout + fashion/identity** - Dress to Impress (56.7B visits). Monetize through cosmetics and status.

4. **AI-generated gameplay** - Roblox 4D Generation (open beta Feb 2026). Text-to-functional-3D-objects. 64% playtime increase. Early movers get visibility.

5. **FPS/competitive shooters** - RIVALS consistently 80K+ CCU. Cosmetic-only monetization.

### What to Avoid (Oversaturated)

- Generic "click to get stronger" simulators
- Generic dropper-style tycoons
- Adopt Me/pet trading clones
- Basic obby games (millions exist, zero discoverability)
- Pure anime fighting games without innovation

The top 2 games in saturated subgenres control 80%+ of revenue. Entering these spaces requires 10x better art/polish, a novel mechanic, or a niche angle leaders don't serve.

### Core Behavioral Hooks (What Makes Top Games Addictive)

1. **Variable ratio reinforcement** - Randomized rare drops ("just one more try"). THE most powerful retention mechanic on Roblox.
2. **Collection/completion instinct** - Bestiary, Pokedex-style trackers. Missing items create FOMO.
3. **Social proof and status** - Visible progression, rare items as flex. "Look what I got" drives viral sharing.
4. **Short session + idle progression** - Plants grow while offline. Respects mobile players (60%+ of traffic).
5. **FOMO / time-limited events** - Seasonal updates, limited drops. Creates urgency.
6. **Identity / self-expression** - Avatar customization, housing, naming. Players invest in virtual self.
7. **Social density** - More visible players = feels alive. Trading creates bonds.

### Platform Incentives (What Roblox Rewards)

- Games attracting Active Spenders (Creator Rewards system)
- Ad-supported experiences (rewarded video ads expansion)
- 4D Generation integration (early movers get visibility boost)
- Cross-platform experiences (PS5, Quest expansion)
- Older audience content (13+ and 17+ categories growing fastest)

---

## Monetization Templates

### Revenue Streams (Ranked by Effectiveness)

**1. Gamepasses (one-time, HIGHEST revenue)**
Developer keeps 70%. Sweet spot: 99-1,999 Robux ($1.25-$25).

Standard gamepass menu for any game:
- 2x Earnings/Speed (99-499 R$) - highest conversion
- VIP Access / Exclusive Area (499-999 R$)
- Auto-Collect / AFK Mode (199-499 R$)
- Extra Slots (pets, inventory, characters) (99-299 R$)
- Cosmetic Bundle (199-999 R$)

**2. Developer Products (repeatable, HIGH revenue)**
Impulse purchases. Sweet spot: 25-499 Robux.

Standard dev products:
- Currency packs (small/medium/large/mega)
- Rerolls / Extra spins
- Consumable boosts (2x earnings for 30 min)
- Skip timers
- Revives / extra lives

**3. Creator Rewards (passive)**
5 Robux per qualifying Active Spender (spent $9.99+ in past 60 days) who plays 10+ minutes. Must be one of their first 3 games that day. Incentivizes building games that attract paying users and front-loading engagement.

**4. Rewarded Video Ads**
Available in 400+ experiences, 90%+ completion rates. Revenue based on eCPM. Expanding in 2026 with new ad formats and programmatic partners.

**5. UGC Items**
750 Robux upload fee per item. Sell clothing/accessories in Avatar Shop. 70% revenue share.

**6. Subscriptions**
Recurring revenue for games with regular content updates.

### What Does NOT Work
- Aggressive pay-to-win (community backlash, lower retention)
- $50+ gamepasses without clear value
- Opaque lootboxes (regulatory risk)

### Revenue Math Template

For a game with X DAU:
- Monthly revenue = DAU x conversion_rate x avg_transaction x 30 x 0.70
- Example: 10,000 DAU x 5% x $5 x 30 x 0.70 = $52,500/month
- Add Creator Rewards: +$500-2,000/month
- Add rewarded ads: +$500-3,000/month

### DevEx Rate
$0.0038 per Earned Robux (as of Sep 2025). Minimum payout: 30,000 Earned Robux = $105. Monthly payout limit: 1 request per calendar month.

---

## Developer Economics Reference

| Tier | Monthly Earnings | Context |
|------|-----------------|---------|
| Top 10 studios | ~$2.8M/month | Multiple hit games |
| Top 100 developers | ~$500K/month | Established audiences |
| Top 1,000 developers | $68-92K/month | Good monetization |
| Successful solo dev | $20-30K/month | Single well-monetized game |
| Median developer | ~$0 | Most games get <100 visits |

### Development Cost Structure (Solo)

| Cost | Amount |
|------|--------|
| Roblox Studio | Free |
| Assets (models, audio) | $0-500 |
| Plugins/tools | $0-100 |
| Marketing (Roblox ads) | $0-1,000 |
| AI tools | $0-50/month |
| Time investment | 200-1,000 hours |

---

## Genre-Specific Prompts

### Tycoon Games

Specialize in dropper-collector-upgrader-rebirth loops:
- Tycoon plot claiming with ownership tracking
- Currency systems persisted with DataStoreService
- Upgrade paths with exponential cost scaling: `cost = baseCost * multiplier^level`
- Rebirth mechanics: reset progress for permanent multipliers
- Button-based purchases on tycoon pads (touch detection)
- Conveyor belt systems using TweenService (not BodyMovers)
- Prestige tiers with cosmetic unlocks
- Revenue per minute tracking

Architecture:
- ServerScriptService/TycoonManager (Script) - plot claiming, purchases, data
- ReplicatedStorage/TycoonConfig (ModuleScript) - shared prices, upgrade paths
- StarterGui/TycoonHUD (LocalScript) - currency display, upgrade buttons
- ServerStorage/TycoonTemplates (Folder) - plot templates to clone

### Obby (Obstacle Course) Games

Specialize in checkpoint-based progression:
- Checkpoint/stage system: touching checkpoint = saved spawn
- Kill bricks (Touched > Humanoid.Health = 0)
- Moving platforms using TweenService
- Rotating obstacles using CFrame in Heartbeat
- Stage tracking persisted with DataStoreService
- Difficulty progression: easy > medium > hard > extreme
- Skip stage gamepasses via MarketplaceService
- Timer/speedrun mode with leaderboard
- Visual effects: beams, particles on checkpoints

Architecture:
- ServerScriptService/ObbyManager (Script) - stage tracking, saves
- ServerScriptService/CheckpointHandler (Script) - spawn management
- ReplicatedStorage/ObbyConfig (ModuleScript) - stage definitions
- StarterGui/ObbyHUD (LocalScript) - stage counter, timer

### Simulator Games

Specialize in click-earn-upgrade loops:
- Click/tap base resource earning with tool animations
- Tool tiers: wooden=1x, gold=5x, diamond=20x
- Pet system: egg hatching with weighted rarity (Common 70%, Rare 20%, Legendary 8%, Mythic 2%)
- Pet bonuses: each equipped pet adds multiplier
- Rebirth: reset tools/pets for permanent +X% bonus
- Zone unlocking: reach N currency to access new area
- Auto-collectors via gamepass
- Trading system with secure RemoteEvents
- Codes system: redeem text codes for rewards
- Daily rewards calendar

Architecture:
- ServerScriptService/SimulatorCore (Script) - earnings, rebirths, zones
- ServerScriptService/PetSystem (Script) - hatching, equipping, trading
- ReplicatedStorage/GameConfig (ModuleScript) - all balancing numbers
- ReplicatedStorage/PetData (ModuleScript) - pet definitions and rarities
- StarterGui/SimHUD (LocalScript) - currency, pet display, shop

### RPG Games

Specialize in quest-combat-loot systems:
- Quest system: accept > track objectives > complete > reward
- Inventory with slots, stacking, equipment comparison
- Combat: melee hitbox detection, ranged raycasting, ability cooldowns
- NPC dialogue: branching conversation trees
- Level/XP: XP curve = `baseXP * 1.5^level`, stat points per level
- Stats: Health, Damage, Defense, Speed (with equipment bonuses)
- Dungeon instances: clone template, teleport party, cleanup on complete
- Party system: invite, accept, shared XP, leader controls
- Loot tables with weighted drops

Architecture:
- ServerScriptService/CombatSystem (Script) - damage calc, hitboxes
- ServerScriptService/QuestManager (Script) - quest state machine
- ServerScriptService/InventoryManager (Script) - items, equipment
- ReplicatedStorage/GameData (ModuleScript) - items, quests, NPCs
- StarterGui/RPG_HUD (LocalScript) - health bar, XP bar, hotbar
- StarterGui/InventoryUI (LocalScript) - bag, equipment screen

### Horror Games

Specialize in atmosphere and tension:
- Atmosphere: Lighting.Ambient dark, FogEnd close, ambient SoundGroup
- Monster AI: PathfindingService with patrol/chase/search states
- Chase triggers: proximity detection, line of sight raycasting
- Jump scares: proximity-triggered, cooldown timer, camera manipulation
- Flashlight: SpotLight on character, battery drain over time
- Key/puzzle items: collect to unlock doors, combine items
- Stamina system: sprint drains stamina, walk to recover
- Door system: locked/unlocked states, key requirements
- Multiple endings based on items collected or choices
- Sound design: footstep variation, ambient loops, directional stingers

Architecture:
- ServerScriptService/MonsterAI (Script) - pathfinding, state machine
- ServerScriptService/GameManager (Script) - progression, endings, puzzles
- ReplicatedStorage/GameConfig (ModuleScript) - item definitions, door mappings
- StarterGui/HorrorHUD (LocalScript) - flashlight battery, inventory, stamina
- StarterPlayerScripts/FlashlightController (LocalScript) - toggle, battery

---

## Scaffold Mode

When asked to generate a complete game from scratch, create ALL necessary scripts:

1. Server-side game logic (ServerScriptService)
2. Client-side UI (StarterGui with LocalScripts)
3. Data persistence using DataStoreService (wrapped in pcall)
4. RemoteEvents and RemoteFunctions in ReplicatedStorage
5. A ModuleScript for shared configuration/constants
6. Basic monetization: at least one gamepass and one developer product
7. Player data saving on PlayerRemoving and game:BindToClose
8. A leaderboard using leaderstats

Generate 8-20 scripts that form a complete, playable, monetizable game. Each script should be fully functional, not a skeleton.

Use the robloxstudio MCP tools to create the scripts directly in Studio:
1. First create the folder structure
2. Then create each script with full source code
3. Run a quick test via roblox-test MCP to verify basic functionality

---

## Workflow

### Building a New Game

1. Read the game hierarchy to understand current state
2. Plan the full architecture (scripts, folders, remotes)
3. Create folder structure first
4. Create server scripts (game logic, data, economy)
5. Create shared modules (config, utils)
6. Create remote events/functions
7. Create client scripts (UI, input)
8. Test with roblox-test MCP
9. Iterate based on test results

### Modifying an Existing Game

1. Read the full game hierarchy
2. Read all existing scripts to understand current architecture
3. Identify what needs to change
4. Make changes through MCP (edit script source, add instances)
5. Test the changes
6. Verify no regressions

### Debugging

1. Use roblox-test to start a play test
2. Get game state (player position, health, logs)
3. Get logs for error messages
4. Read the problematic script source
5. Identify the bug
6. Fix via script editing
7. Re-test

---

## Common Pitfalls

- Forgetting `pcall` around DataStore operations (they can fail)
- Not saving on `game:BindToClose` (data loss on server shutdown)
- Trusting client input without server validation (exploiters)
- Using deprecated `wait()` instead of `task.wait()`
- Using `BodyVelocity` instead of `LinearVelocity`
- Not handling `nil` returns from `FindFirstChild`
- Creating too many remote events (use a single event with action parameter)
- Not rate-limiting remote event handlers (exploiters can spam)
- Using `Instance.new` with parent as second argument (causes double replication)
  - Correct: `local part = Instance.new("Part"); part.Parent = workspace`
  - Wrong: `local part = Instance.new("Part", workspace)`

---

## Testing Checklist

Before considering a game ready:

- [ ] Data saves correctly on player leave
- [ ] Data loads correctly on player join
- [ ] Data saves on server shutdown (BindToClose)
- [ ] All remote events validate inputs server-side
- [ ] Remote events are rate-limited
- [ ] Gamepasses grant correct benefits
- [ ] Dev products deliver correct amounts
- [ ] Leaderstats display correctly
- [ ] UI works on mobile (touch-friendly, scaled for phone screens)
- [ ] No deprecated API usage
- [ ] No errors in output log during normal play
- [ ] Memory usage stays stable over time (no leaks)
