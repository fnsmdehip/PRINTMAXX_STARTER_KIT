# RobloxMaxx Simulator Template

You are building a Roblox simulator game. This project uses Claude Code with MCP servers connected to Roblox Studio.

---

## MCP Tools

- **robloxstudio** MCP: 37+ tools for reading/writing game hierarchy, scripts, properties
- **roblox-test** MCP: play testing, screenshots, game state inspection

---

## Simulator Game Architecture

### Core Loop

```
Player Clicks/Taps → Earn Resources → Buy Better Tools → Earn Faster →
Hatch Pets (boost earnings) → Unlock New Zones → Rebirth for Permanent Bonus →
Repeat with Higher Numbers
```

### Script Structure

```
game
├── ServerScriptService/
│   ├── SimulatorCore.lua       -- Main game loop, resource earning, tool logic
│   ├── PetSystem.lua           -- Egg hatching, equipping, trading, inventory
│   ├── RebirthManager.lua      -- Rebirth logic, permanent multipliers
│   ├── ZoneManager.lua         -- Zone unlocking, zone-specific mechanics
│   ├── DataManager.lua         -- Save/load with DataStoreService
│   ├── EconomyManager.lua      -- Gamepasses, dev products, MarketplaceService
│   ├── CodeSystem.lua          -- Redeemable text codes for rewards
│   └── DailyRewards.lua        -- Daily login streak rewards
├── ReplicatedStorage/
│   ├── Remotes/
│   │   ├── ClickAction (RemoteEvent)       -- Client→Server: player clicked
│   │   ├── HatchEgg (RemoteEvent)          -- Client→Server: hatch request
│   │   ├── EquipPet (RemoteEvent)          -- Client→Server: equip/unequip
│   │   ├── TradePet (RemoteEvent)          -- Client→Server: trade request
│   │   ├── RequestRebirth (RemoteEvent)    -- Client→Server
│   │   ├── RedeemCode (RemoteEvent)        -- Client→Server
│   │   ├── UpdateStats (RemoteEvent)       -- Server→Client: sync UI
│   │   └── PetInventoryUpdate (RemoteEvent) -- Server→Client
│   ├── Modules/
│   │   ├── GameConfig.lua      -- All game numbers, balancing
│   │   ├── PetData.lua         -- Pet definitions, rarities, bonuses
│   │   ├── ToolData.lua        -- Tool tiers and multipliers
│   │   ├── ZoneData.lua        -- Zone requirements and mechanics
│   │   └── SharedUtils.lua     -- Formatting, number abbreviation
│   └── Assets/
│       ├── PetModels/          -- 3D pet models
│       ├── ToolModels/         -- Tool visuals per tier
│       └── EggModels/          -- Egg visuals per tier
├── StarterGui/
│   ├── SimHUD.lua              -- Currency, multiplier, zone display
│   ├── PetUI.lua               -- Pet inventory, hatching animation
│   ├── ShopUI.lua              -- Tools, gamepasses, dev products
│   ├── CodesUI.lua             -- Code redemption input
│   └── DailyRewardUI.lua       -- Login streak popup
├── StarterPlayerScripts/
│   └── ClickController.lua     -- Handle click/tap, tool animation
└── Workspace/
    └── Zones/
        ├── Zone_01_Starter/    -- Free zone
        ├── Zone_02_Forest/     -- Requires 10K currency
        ├── Zone_03_Cave/       -- Requires 100K currency
        ├── Zone_04_Volcano/    -- Requires 1M currency
        └── Zone_05_Space/      -- Requires 10M currency
```

### GameConfig Module

```luau
local Config = {}

Config.Earning = {
    BaseClickValue = 1,
    ClickCooldown = 0.1,        -- Minimum time between clicks (anti-exploit)
}

Config.Tools = {
    { name = "Wooden Pickaxe",   cost = 0,        multiplier = 1,   tier = 1 },
    { name = "Stone Pickaxe",    cost = 500,      multiplier = 3,   tier = 2 },
    { name = "Iron Pickaxe",     cost = 5000,     multiplier = 8,   tier = 3 },
    { name = "Gold Pickaxe",     cost = 50000,    multiplier = 20,  tier = 4 },
    { name = "Diamond Pickaxe",  cost = 500000,   multiplier = 50,  tier = 5 },
    { name = "Mythic Pickaxe",   cost = 5000000,  multiplier = 150, tier = 6 },
    { name = "Cosmic Pickaxe",   cost = 50000000, multiplier = 500, tier = 7 },
}

Config.Zones = {
    { name = "Starter Field",  requirement = 0,         earningBonus = 1.0 },
    { name = "Forest",         requirement = 10000,     earningBonus = 2.0 },
    { name = "Crystal Cave",   requirement = 100000,    earningBonus = 5.0 },
    { name = "Volcano",        requirement = 1000000,   earningBonus = 15.0 },
    { name = "Space Station",  requirement = 10000000,  earningBonus = 50.0 },
}

Config.Rebirth = {
    BaseCost = 10000000,
    CostMultiplier = 3.0,
    PermanentBonus = 0.50,      -- +50% per rebirth
    MaxRebirths = 100,
}

Config.Pets = {
    MaxEquipped = 3,            -- Pets active at once (can upgrade via gamepass)
    MaxInventory = 50,          -- Total pets owned
}

Config.Codes = {
    -- Format: { code = "string", reward = {type, amount}, maxUses = N, expiry = timestamp }
    { code = "LAUNCH", reward = { type = "currency", amount = 1000 }, maxUses = nil, expiry = nil },
    { code = "PETS",   reward = { type = "egg",      amount = 3 },    maxUses = nil, expiry = nil },
    { code = "BOOST",  reward = { type = "boost",    duration = 600 }, maxUses = nil, expiry = nil },
}

Config.DailyRewards = {
    { day = 1,  reward = { type = "currency", amount = 100 } },
    { day = 2,  reward = { type = "currency", amount = 250 } },
    { day = 3,  reward = { type = "egg",      amount = 1 } },
    { day = 4,  reward = { type = "currency", amount = 500 } },
    { day = 5,  reward = { type = "currency", amount = 1000 } },
    { day = 6,  reward = { type = "egg",      amount = 3 } },
    { day = 7,  reward = { type = "boost",    duration = 1800 } },
    -- Cycle repeats with increasing rewards
}

Config.Gamepasses = {
    DoubleEarnings = 0,         -- Replace with real ID
    AutoClick = 0,
    ExtraPetSlot = 0,           -- +3 equipped pets
    LuckBoost = 0,              -- 2x legendary chance
    VIPZone = 0,
}

Config.DevProducts = {
    SmallCurrency   = { id = 0, amount = 5000 },
    MediumCurrency  = { id = 0, amount = 25000 },
    LargeCurrency   = { id = 0, amount = 100000 },
    BasicEgg        = { id = 0, eggs = 1 },
    RareEgg         = { id = 0, eggs = 1, minRarity = "Rare" },
    BoostToken      = { id = 0, duration = 600 },
}

return Config
```

### PetData Module

```luau
local PetData = {}

PetData.Rarities = {
    Common    = { weight = 70,  color = Color3.fromRGB(180, 180, 180), multiplier = 1.1 },
    Uncommon  = { weight = 20,  color = Color3.fromRGB(0, 180, 0),    multiplier = 1.3 },
    Rare      = { weight = 7,   color = Color3.fromRGB(0, 100, 255),  multiplier = 1.8 },
    Epic      = { weight = 2.5, color = Color3.fromRGB(180, 0, 255),  multiplier = 3.0 },
    Legendary = { weight = 0.4, color = Color3.fromRGB(255, 200, 0),  multiplier = 5.0 },
    Mythic    = { weight = 0.1, color = Color3.fromRGB(255, 50, 50),  multiplier = 10.0 },
}

PetData.Eggs = {
    {
        name = "Starter Egg",
        cost = 500,
        zone = "Starter Field",
        pets = {
            { name = "Cat",       rarity = "Common" },
            { name = "Dog",       rarity = "Common" },
            { name = "Bunny",     rarity = "Common" },
            { name = "Fox",       rarity = "Uncommon" },
            { name = "Wolf",      rarity = "Rare" },
            { name = "Dragon",    rarity = "Legendary" },
        },
    },
    {
        name = "Forest Egg",
        cost = 10000,
        zone = "Forest",
        pets = {
            { name = "Deer",        rarity = "Common" },
            { name = "Bear",        rarity = "Common" },
            { name = "Owl",         rarity = "Uncommon" },
            { name = "Phoenix",     rarity = "Rare" },
            { name = "Unicorn",     rarity = "Epic" },
            { name = "Forest Spirit", rarity = "Legendary" },
        },
    },
    {
        name = "Crystal Egg",
        cost = 100000,
        zone = "Crystal Cave",
        pets = {
            { name = "Crystal Slime", rarity = "Common" },
            { name = "Gem Bat",       rarity = "Uncommon" },
            { name = "Ruby Golem",    rarity = "Rare" },
            { name = "Diamond Cat",   rarity = "Epic" },
            { name = "Prism Dragon",  rarity = "Legendary" },
            { name = "Void Walker",   rarity = "Mythic" },
        },
    },
}

return PetData
```

### Key Implementation Details

**Click/Earning System:**
```luau
-- Server handles all earning calculations
-- Client sends click events, server validates timing
local lastClickTime = {} -- Per-player click timestamps

ClickAction.OnServerEvent:Connect(function(player)
    local now = tick()
    local last = lastClickTime[player.UserId] or 0

    -- Anti-exploit: enforce minimum click cooldown
    if now - last < Config.Earning.ClickCooldown then return end
    lastClickTime[player.UserId] = now

    -- Calculate earnings
    local base = Config.Earning.BaseClickValue
    local toolMultiplier = getToolMultiplier(player)
    local petMultiplier = getPetMultiplier(player)
    local zoneMultiplier = getZoneMultiplier(player)
    local rebirthMultiplier = 1 + (playerData[player.UserId].rebirths * Config.Rebirth.PermanentBonus)
    local gamepassMultiplier = hasGamepass(player, Config.Gamepasses.DoubleEarnings) and 2 or 1

    local total = base * toolMultiplier * petMultiplier * zoneMultiplier * rebirthMultiplier * gamepassMultiplier

    addCurrency(player, total)
end)
```

**Pet Hatching (Weighted Random):**
```luau
local function hatchPet(eggData: {})
    -- Build weighted table
    local totalWeight = 0
    local entries = {}

    for _, petDef in eggData.pets do
        local rarityInfo = PetData.Rarities[petDef.rarity]
        totalWeight += rarityInfo.weight
        table.insert(entries, {
            pet = petDef,
            cumulativeWeight = totalWeight,
        })
    end

    -- Roll
    local roll = math.random() * totalWeight
    for _, entry in entries do
        if roll <= entry.cumulativeWeight then
            return entry.pet
        end
    end

    return entries[#entries].pet -- Fallback
end
```

**Rebirth System:**
```luau
-- Server-side rebirth calculation and execution
local function calculateRebirthCost(currentRebirths: number): number
    return math.floor(Config.Rebirth.BaseCost * Config.Rebirth.CostMultiplier ^ currentRebirths)
end

local function getRebirthMultiplier(rebirths: number): number
    return 1 + (rebirths * Config.Rebirth.PermanentBonus)
end

RequestRebirth.OnServerEvent:Connect(function(player)
    local data = playerData[player.UserId]
    if not data then return end
    if data.rebirths >= Config.Rebirth.MaxRebirths then return end

    local cost = calculateRebirthCost(data.rebirths)
    if data.currency < cost then return end

    -- Execute rebirth
    data.rebirths += 1
    data.currency = 0
    data.currentTool = 1        -- Reset to starter tool
    data.equippedPets = {}      -- Unequip all pets (keep in inventory)

    -- Update leaderstats
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats then
        local rebirthStat = leaderstats:FindFirstChild("Rebirths")
        if rebirthStat then rebirthStat.Value = data.rebirths end
    end

    -- Notify client
    UpdateStats:FireClient(player, "rebirth", {
        rebirths = data.rebirths,
        multiplier = getRebirthMultiplier(data.rebirths),
        nextCost = calculateRebirthCost(data.rebirths),
    })

    -- Save immediately after rebirth
    saveData(player, data)
end)
```

**Zone Unlock System:**
```luau
-- Zones are physical areas in workspace with invisible barriers
-- Each barrier belongs to a PhysicsService collision group
-- Players get added to zone-specific collision groups when they meet requirements

local PhysicsService = game:GetService("PhysicsService")

-- Create collision groups at startup
for i, zone in Config.Zones do
    local groupName = `Zone_{i}_Barrier`
    PhysicsService:RegisterCollisionGroup(groupName)
    PhysicsService:CollisionGroupSetCollidable(groupName, "Default", true)
end

local function updateZoneAccess(player: Player)
    local data = playerData[player.UserId]
    if not data or not player.Character then return end

    local totalCurrency = data.currency + data.totalEarned -- Use lifetime earnings for unlock

    for i, zone in Config.Zones do
        local zoneFolder = workspace.Zones:FindFirstChild(zone.name)
        if not zoneFolder then continue end
        local barrier = zoneFolder:FindFirstChild("Barrier")
        if not barrier then continue end

        if totalCurrency >= zone.requirement then
            -- Remove barrier collision for this player's character parts
            for _, part in player.Character:GetDescendants() do
                if part:IsA("BasePart") then
                    part.CollisionGroup = `Zone_{i}_Unlocked`
                end
            end
        end
    end
end

-- Check zone access whenever currency changes
local function getCurrentZone(player: Player): (string, number)
    local data = playerData[player.UserId]
    if not data or not player.Character then return Config.Zones[1].name, 1.0 end
    local hrp = player.Character:FindFirstChild("HumanoidRootPart")
    if not hrp then return Config.Zones[1].name, 1.0 end

    -- Determine which zone the player is physically in
    for i = #Config.Zones, 1, -1 do
        local zone = Config.Zones[i]
        local zoneFolder = workspace.Zones:FindFirstChild(zone.name)
        if zoneFolder then
            local zonePart = zoneFolder:FindFirstChild("ZoneBounds")
            if zonePart and isInsidePart(hrp.Position, zonePart) then
                return zone.name, zone.earningBonus
            end
        end
    end

    return Config.Zones[1].name, Config.Zones[1].earningBonus
end
```

**Trading Validation (Secure Server-Side):**
```luau
-- Server-side trading with full validation
local activeTrades: {[string]: { sender: Player, receiver: Player, senderPets: {}, receiverPets: {}, confirmed: {boolean} }} = {}

TradePet.OnServerEvent:Connect(function(player, action, ...)
    if typeof(action) ~= "string" then return end

    if action == "initiate" then
        local targetName = ...
        if typeof(targetName) ~= "string" then return end
        local targetPlayer = Players:FindFirstChild(targetName)
        if not targetPlayer or targetPlayer == player then return end

        local tradeId = `{player.UserId}_{targetPlayer.UserId}_{tick()}`
        activeTrades[tradeId] = {
            sender = player,
            receiver = targetPlayer,
            senderPets = {},
            receiverPets = {},
            confirmed = {false, false},
        }

        -- Notify target
        PetInventoryUpdate:FireClient(targetPlayer, "trade_request", player.Name, tradeId)

    elseif action == "add_pet" then
        local tradeId, petId = ...
        if typeof(tradeId) ~= "string" or typeof(petId) ~= "string" then return end
        local trade = activeTrades[tradeId]
        if not trade then return end

        -- Verify player owns this pet
        local data = playerData[player.UserId]
        if not data then return end
        local ownsPet = false
        for _, pet in data.pets do
            if pet.id == petId then ownsPet = true break end
        end
        if not ownsPet then return end

        -- Add to trade
        if player == trade.sender then
            table.insert(trade.senderPets, petId)
        elseif player == trade.receiver then
            table.insert(trade.receiverPets, petId)
        end

        -- Reset confirmations when trade changes
        trade.confirmed = {false, false}

    elseif action == "confirm" then
        local tradeId = ...
        if typeof(tradeId) ~= "string" then return end
        local trade = activeTrades[tradeId]
        if not trade then return end

        local index = if player == trade.sender then 1 else 2
        trade.confirmed[index] = true

        -- Execute trade if both confirmed
        if trade.confirmed[1] and trade.confirmed[2] then
            executeTrade(trade)
            activeTrades[tradeId] = nil
        end

    elseif action == "cancel" then
        local tradeId = ...
        if typeof(tradeId) ~= "string" then return end
        activeTrades[tradeId] = nil
    end
end)

local function executeTrade(trade)
    local senderData = playerData[trade.sender.UserId]
    local receiverData = playerData[trade.receiver.UserId]
    if not senderData or not receiverData then return end

    -- Re-verify ownership at execution time (prevents duplication exploits)
    for _, petId in trade.senderPets do
        if not playerOwnsPet(senderData, petId) then return end
    end
    for _, petId in trade.receiverPets do
        if not playerOwnsPet(receiverData, petId) then return end
    end

    -- Swap pets
    for _, petId in trade.senderPets do
        removePetFromPlayer(senderData, petId)
        addPetToPlayer(receiverData, petId)
    end
    for _, petId in trade.receiverPets do
        removePetFromPlayer(receiverData, petId)
        addPetToPlayer(senderData, petId)
    end

    -- Save both players immediately
    saveData(trade.sender, senderData)
    saveData(trade.receiver, receiverData)
end
```

**Daily Rewards Implementation:**
```luau
-- ServerScriptService/DailyRewards.lua
local function checkDailyReward(player: Player)
    local data = playerData[player.UserId]
    if not data then return end

    local now = os.time()
    local lastClaim = data.lastDailyReward or 0
    local daysSinceLastClaim = math.floor((now - lastClaim) / 86400)

    if daysSinceLastClaim < 1 then return end -- Already claimed today

    -- Reset streak if missed a day
    if daysSinceLastClaim > 1 then
        data.dailyStreak = 0
    end

    -- Calculate reward day (1-7 cycle)
    data.dailyStreak = (data.dailyStreak or 0) + 1
    local rewardDay = ((data.dailyStreak - 1) % 7) + 1
    local reward = Config.DailyRewards[rewardDay]

    -- Grant reward
    if reward.reward.type == "currency" then
        addCurrency(player, reward.reward.amount)
    elseif reward.reward.type == "egg" then
        for i = 1, reward.reward.amount do
            grantRandomEgg(player)
        end
    elseif reward.reward.type == "boost" then
        activateBoost(player, reward.reward.duration)
    end

    data.lastDailyReward = now

    -- Show UI on client
    UpdateStats:FireClient(player, "daily_reward", {
        day = rewardDay,
        streak = data.dailyStreak,
        reward = reward.reward,
    })
end

-- Check on join
Players.PlayerAdded:Connect(function(player)
    task.wait(3) -- Let everything load first
    checkDailyReward(player)
end)
```

**Code Redemption:**
```luau
-- Track redeemed codes per player in their save data
-- Server-only validation
-- Codes are case-insensitive
-- Check: code exists, not expired, not already redeemed by this player, not exceeded maxUses

RedeemCode.OnServerEvent:Connect(function(player, codeString)
    if typeof(codeString) ~= "string" then return end
    codeString = string.upper(codeString)

    local codeData = findCode(codeString)
    if not codeData then
        -- Fire error to client: "Invalid code"
        return
    end

    if playerData[player.UserId].redeemedCodes[codeString] then
        -- Fire error: "Already redeemed"
        return
    end

    -- Grant reward based on type
    grantCodeReward(player, codeData.reward)
    playerData[player.UserId].redeemedCodes[codeString] = true
end)
```

**Number Abbreviation (for UI):**
```luau
-- SharedUtils module
local function abbreviateNumber(n: number): string
    if n < 1000 then return tostring(math.floor(n)) end
    local suffixes = {"K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"}
    local tier = math.floor(math.log10(n) / 3)
    if tier > #suffixes then tier = #suffixes end
    local scaled = n / 10^(tier * 3)
    return string.format("%.1f%s", scaled, suffixes[tier])
end
-- 1500 → "1.5K", 2500000 → "2.5M", 1234567890 → "1.2B"
```

---

## Monetization Strategy for Simulators

### Gamepasses (One-Time)

| Gamepass | Price (Robux) | Effect |
|----------|---------------|--------|
| 2x Earnings | 199 | Permanent double click value |
| Auto-Clicker | 399 | Auto-earn without clicking |
| +3 Pet Slots | 149 | 6 equipped pets instead of 3 |
| 2x Luck | 249 | Double legendary/mythic chance |
| VIP Zone | 499 | Exclusive zone with highest multiplier |
| Triple Hatch | 299 | Hatch 3 eggs at once |

### Dev Products (Repeatable)

| Product | Price (Robux) | Effect |
|---------|---------------|--------|
| 5K Currency | 49 | Instant currency |
| 25K Currency | 199 | Instant currency |
| 100K Currency | 699 | Instant currency |
| Basic Egg | 25 | Hatch one basic egg |
| Rare+ Egg | 75 | Guaranteed Rare or better |
| 2x Boost (10 min) | 49 | 10-minute double earnings |

### Rewarded Video Ads

- Watch ad for 5-minute 2x boost
- Watch ad for free egg hatch
- Watch ad for bonus daily reward

---

## Simulator Meta Intelligence (Feb 2026)

### The Saturation Problem

Generic "click to get stronger" simulators are EXTREMELY saturated. The top 2 games in each simulator subgenre control 80%+ of revenue. Player fatigue is real.

### How to Win Anyway

1. **Unique theme/fantasy** - "Fishing Simulator" beats "Click Simulator." The activity matters. Grow a Garden (22.3M CCU) proved that the RIGHT theme creates massive demand even in a saturated space.

2. **Collection depth** - Fisch has 400,000+ fish variations. The collection instinct is THE most powerful retention mechanic. More collectibles = more play time.

3. **Variable ratio reinforcement** - Randomized rare drops create "just one more try" compulsion. This is what makes Grow a Garden and Blox Fruits work.

4. **Trading economies** - When players can trade rare items, they create social bonds AND drive each other's engagement. Trading makes your game an ecosystem, not just a clicker.

5. **Hybrid mechanics** - Pure clicking is boring. Add exploration, combat, fishing, farming, building. The BEST simulators in 2026 are hybrids.

6. **Short session + idle** - Let things happen while players are away. Plants grow, pets earn passive income, machines produce. Creates "check back" compulsion.

### Successful Simulators to Study

- **Grow a Garden**: Idle farming + rare seed drops + trading. 22.3M CCU record.
- **Fisch**: Fishing + RPG + social + 400K fish variations. Massive collection depth.
- **Pet Simulator 99**: Pure collection + trading + prestige. Franchise approach.
- **The Forge**: Mining + crafting + combat. Hybrid genre execution.

### Simulator-Specific Retention Tricks

- **Codes system**: Release codes on social media. Drives follows AND return visits.
- **Daily rewards calendar**: 7-day streak with escalating rewards. Resets = FOMO.
- **Limited-time eggs/pets**: "Available for 7 days only." Urgency + FOMO.
- **Seasonal events**: Holiday content, special zones, exclusive collectibles.
- **Leaderboards**: Top earners, most rebirths, rarest pet owners. Competition.
- **Group rewards**: Join the Roblox group for free boost. Grows group size for future launches.

### Numbers That Matter

For a simulator with 10K DAU:
- Monthly revenue: ~$52,500 (5% conversion, $5 avg, 70% share)
- Add Creator Rewards: +$500-2,000
- Add rewarded ads: +$500-3,000
- Total: ~$53-57K/month

The goal: reach and maintain 10K+ DAU through collection depth, social mechanics, and regular content updates.

---

## Luau Standards

- Use `task.wait()` not `wait()`
- Use `task.spawn()` not `spawn()`
- Wrap DataStore calls in `pcall`
- Validate ALL RemoteEvent inputs server-side
- Rate-limit click events (prevent auto-clicker exploits unless they bought the gamepass)
- Use type annotations on function signatures
- Use string interpolation
- Never trust client for currency, pet ownership, or zone access
- Save on PlayerRemoving AND game:BindToClose
- Use UpdateAsync instead of SetAsync when possible (for atomic updates)

---

## Anti-Exploit Considerations

Simulators are heavily targeted by exploiters. Key protections:

1. **Server-side earning validation**: Never let client tell server how much they earned
2. **Click rate limiting**: Track timestamps, reject clicks faster than cooldown
3. **Currency validation**: Before any purchase, verify server-side balance
4. **Pet ownership verification**: Before trade/equip, verify player actually owns the pet
5. **Zone access server check**: Don't rely on client collision; verify requirement server-side
6. **DataStore versioning**: Use version keys ("PlayerData_v1") so you can migrate schemas
7. **Sanity checks**: If a value seems impossible (negative currency, more pets than max), flag and investigate

---

## Development Workflow

1. Use robloxstudio MCP to create folder structure and zones in Studio
2. Create all config ModuleScripts first (GameConfig, PetData, ToolData, ZoneData)
3. Create server scripts (SimulatorCore, PetSystem, DataManager, EconomyManager)
4. Create remote events
5. Create client scripts (SimHUD, PetUI, ShopUI, ClickController)
6. Create egg/pet models (or use placeholders)
7. Use roblox-test MCP to play test the click loop
8. Verify: clicks earn currency, tools upgrade, eggs hatch with correct rarities
9. Test data persistence (leave and rejoin)
10. Add monetization (gamepasses, dev products)
11. Add codes system and daily rewards
12. Polish UI, animations, effects
13. Balance economy (ensure progression feels rewarding but not too fast)
