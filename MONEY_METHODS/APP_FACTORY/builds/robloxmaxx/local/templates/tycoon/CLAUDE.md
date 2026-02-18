# RobloxMaxx Tycoon Template

You are building a Roblox tycoon game. This project uses Claude Code with MCP servers connected to Roblox Studio.

---

## MCP Tools

- **robloxstudio** MCP: 37+ tools for reading/writing game hierarchy, scripts, properties
- **roblox-test** MCP: play testing, screenshots, game state inspection

---

## Tycoon Game Architecture

### Core Loop

```
Player Claims Plot → Droppers Generate Resources → Collector Gathers →
Upgraders Multiply Value → Sell for Currency → Buy More Droppers/Upgraders →
Eventually Rebirth → Permanent Multiplier → Repeat
```

### Script Structure

```
game
├── ServerScriptService/
│   ├── TycoonManager.lua       -- Plot claiming, purchase handling, main loop
│   ├── DataManager.lua         -- Save/load player data with DataStoreService
│   ├── EconomyManager.lua      -- Currency, gamepasses, dev products
│   └── RebirthManager.lua      -- Rebirth logic, permanent multipliers
├── ReplicatedStorage/
│   ├── Remotes/
│   │   ├── PurchaseButton (RemoteEvent)
│   │   ├── RequestRebirth (RemoteEvent)
│   │   ├── UpdateCurrency (RemoteEvent)    -- Server→Client
│   │   └── RedeemCode (RemoteEvent)
│   ├── Modules/
│   │   ├── TycoonConfig.lua    -- All prices, multipliers, upgrade paths
│   │   └── SharedUtils.lua     -- Formatting, math helpers
│   └── Assets/
│       └── (shared models)
├── StarterGui/
│   ├── TycoonHUD.lua           -- Currency display, upgrade buttons, rebirth UI
│   └── ShopUI.lua              -- Gamepass/dev product shop
├── StarterPlayerScripts/
│   └── InputController.lua     -- Touch/click handling
└── ServerStorage/
    └── TycoonTemplates/
        ├── StarterPlot/        -- Base plot template (cloned per player)
        ├── Droppers/           -- Dropper models by tier
        ├── Upgraders/          -- Upgrader models by tier
        └── Decorations/        -- Cosmetic unlocks
```

### TycoonConfig Module (Balancing)

```luau
local Config = {}

Config.Plots = {
    MaxPlots = 12,          -- Max concurrent players
    PlotSize = Vector3.new(60, 1, 60),
}

Config.Droppers = {
    { name = "Basic Dropper",    cost = 0,      valuePerDrop = 1,   dropInterval = 2.0 },
    { name = "Iron Dropper",     cost = 500,    valuePerDrop = 5,   dropInterval = 1.8 },
    { name = "Gold Dropper",     cost = 5000,   valuePerDrop = 25,  dropInterval = 1.5 },
    { name = "Diamond Dropper",  cost = 50000,  valuePerDrop = 150, dropInterval = 1.2 },
    { name = "Mythic Dropper",   cost = 500000, valuePerDrop = 1000, dropInterval = 1.0 },
}

Config.Upgraders = {
    { name = "Basic Upgrader",   cost = 1000,   multiplier = 1.5 },
    { name = "Advanced Upgrader", cost = 10000,  multiplier = 2.0 },
    { name = "Elite Upgrader",   cost = 100000, multiplier = 3.0 },
    { name = "Mythic Upgrader",  cost = 1000000, multiplier = 5.0 },
}

Config.Rebirth = {
    BaseCost = 1000000,             -- Currency to rebirth
    CostMultiplier = 2.5,           -- Each rebirth costs more
    PermanentBonus = 0.25,          -- +25% per rebirth
    MaxRebirths = 50,
}

Config.Gamepasses = {
    DoubleEarnings = 0,     -- Replace with real gamepass ID
    AutoCollect = 0,
    VIPAccess = 0,
    ExtraDropper = 0,
}

Config.DevProducts = {
    SmallCash  = { id = 0, amount = 10000 },
    MediumCash = { id = 0, amount = 50000 },
    LargeCash  = { id = 0, amount = 250000 },
    MegaCash   = { id = 0, amount = 1000000 },
}

return Config
```

### Key Implementation Details

**Plot Claiming:**
- Store plot ownership in a table: `plotOwners[plotNumber] = player.UserId`
- When player joins, assign first empty plot
- When player leaves, clear their plot and clean up built items
- Clone plot template from ServerStorage

**Dropper System:**
- Each dropper is a model with a spawn point
- Use `task.spawn` for each dropper's production loop
- `task.wait(dropInterval)` between drops
- Dropped parts have a `Value` attribute representing their worth
- Parts travel along conveyor to collector

**Conveyor System:**
- Use `TweenService` to move parts along a path
- Define waypoints as invisible parts
- Tween from waypoint to waypoint
- Alternative: set `AssemblyLinearVelocity` on conveyor belt parts

**Collector/Seller:**
- Touched event on collector part
- When resource part touches collector, add its Value to player currency
- Destroy the resource part
- Fire `UpdateCurrency` remote to client

**Upgraders:**
- Touched event on upgrader part
- Multiply the resource part's Value attribute
- Mark part as "upgraded by this upgrader" (prevent double-dipping)
- Use attributes: `part:SetAttribute("UpgradedBy_" .. upgraderName, true)`

**Rebirth:**
- Server validates player has enough currency
- Increment rebirth counter
- Clear all built items on plot
- Reset currency to 0
- Apply permanent multiplier to all future earnings
- Save immediately after rebirth

**Purchase Buttons (Tycoon Pad):**
- Physical buttons on the plot floor
- Touched event checks if touching player owns this plot
- Check if player has enough currency
- Deduct currency, spawn the purchased item
- Disable button (make transparent, disable touch)

---

## Monetization Strategy for Tycoons

### Gamepasses (One-Time)

| Gamepass | Price (Robux) | Effect |
|----------|---------------|--------|
| 2x Earnings | 199 | All currency earned is doubled |
| Auto-Collect | 149 | Resources auto-sell without touching collector |
| VIP Area | 299 | Access exclusive high-tier droppers |
| Extra Dropper Slot | 99 | Place one additional dropper |
| Instant Rebirth | 399 | Rebirth without currency requirement |

### Dev Products (Repeatable)

| Product | Price (Robux) | Effect |
|---------|---------------|--------|
| 10K Cash | 49 | Instant currency |
| 50K Cash | 199 | Instant currency |
| 250K Cash | 799 | Instant currency |
| Speed Boost (30 min) | 75 | 2x dropper speed for 30 minutes |

### Rewarded Video Ads

Place ad portals in the tycoon that grant:
- 5-minute 2x boost
- Small currency bonus
- Cosmetic trial

---

## Tycoon Meta Intelligence (Feb 2026)

### What Works

- **Niche tycoons** outperform generic ones. "Restaurant Tycoon" beats "Money Tycoon"
- **Visual satisfaction** matters: ore smelting animations, stacking money, conveyor belts with visible resources
- **Rebirth systems** are mandatory for retention. Players need a "reset for power" loop
- **Social elements**: leaderboards showing "richest player" and visible plot progression create competition
- **Idle elements**: let plants/machines work while player explores, creating "check back" compulsion

### What to Avoid

- Generic dropper-plate-upgrader with no theme (oversaturated)
- No rebirth system (players hit ceiling and quit)
- Invisible progression (players need to SEE their tycoon growing)
- Pure pay-to-win (no skill or strategy element)

### Successful Tycoon Patterns to Study

- **Theme Park Tycoon 2**: Creative freedom + management sim. 1.3B+ visits
- **My Restaurant**: Service simulation + expansion + customization
- **Retail Tycoon 2**: Business simulation with supply/demand mechanics

### Differentiation Ideas

- Combine tycoon with another genre (tycoon + tower defense, tycoon + RPG)
- Real-world theme (coffee shop, hospital, space station)
- Story-driven tycoon with NPC quests
- Competitive tycoon (PvP economy, sabotage mechanics)
- Seasonal/event content that resets and refreshes the loop

---

## Luau Standards

- Use `task.wait()` not `wait()`
- Use `task.spawn()` not `spawn()`
- Wrap DataStore calls in `pcall`
- Validate all RemoteEvent inputs server-side
- Use type annotations on function signatures
- Use string interpolation: `` `Player {name} earned {amount}` ``
- Never trust client for currency/state changes
- Save on PlayerRemoving AND game:BindToClose
- Use attributes over Value objects where possible

---

## Development Workflow

1. Use robloxstudio MCP to create the folder structure in Studio
2. Create the config ModuleScript first (defines all game numbers)
3. Create server scripts (TycoonManager, DataManager, EconomyManager)
4. Create the remote events folder and events
5. Create client scripts (HUD, input)
6. Create plot template in ServerStorage
7. Use roblox-test MCP to start a play test
8. Verify: plot claims, droppers work, currency updates, data saves
9. Iterate on balance (adjust Config numbers)
10. Add monetization (gamepasses, dev products)
11. Polish UI and effects
