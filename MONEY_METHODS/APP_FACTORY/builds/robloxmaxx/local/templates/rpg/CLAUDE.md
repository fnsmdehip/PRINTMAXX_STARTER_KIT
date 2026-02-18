# RobloxMaxx RPG Template

You are building a Roblox RPG game. This project uses Claude Code with MCP servers connected to Roblox Studio.

---

## MCP Tools

- **robloxstudio** MCP: 37+ tools for reading/writing game hierarchy, scripts, properties
- **roblox-test** MCP: play testing, screenshots, game state inspection

---

## RPG Game Architecture

### Core Loop

```
Player Creates Character → Accept Quest → Travel to Zone → Fight Enemies →
Earn XP + Loot → Level Up (stat points) → Equip Better Gear →
Take on Harder Quests → Enter Dungeons (party) → Boss Fights → End-game Gear
```

### Script Structure

```
game
├── ServerScriptService/
│   ├── CombatSystem.lua        -- Damage calc, hitboxes, abilities, cooldowns
│   ├── QuestManager.lua        -- Quest state machine, objectives, rewards
│   ├── InventoryManager.lua    -- Items, equipment, stacking, weight/slots
│   ├── NPCManager.lua          -- Dialogue trees, shops, quest givers
│   ├── EnemySpawner.lua        -- Mob spawning, respawn timers, zone control
│   ├── DungeonManager.lua      -- Instance creation, party teleport, cleanup
│   ├── PartySystem.lua         -- Invite, accept, shared XP, leader controls
│   ├── DataManager.lua         -- Save/load with DataStoreService
│   ├── EconomyManager.lua      -- Gold, gamepasses, dev products
│   └── LootManager.lua         -- Loot tables, weighted drops, quality tiers
├── ReplicatedStorage/
│   ├── Remotes/
│   │   ├── CombatAction (RemoteEvent)      -- Client→Server: attack, ability
│   │   ├── AcceptQuest (RemoteEvent)        -- Client→Server
│   │   ├── CompleteQuest (RemoteEvent)      -- Client→Server
│   │   ├── EquipItem (RemoteEvent)          -- Client→Server
│   │   ├── DropItem (RemoteEvent)           -- Client→Server
│   │   ├── UseItem (RemoteEvent)            -- Client→Server
│   │   ├── InviteToParty (RemoteEvent)      -- Client→Server
│   │   ├── NPCDialogue (RemoteFunction)     -- Client↔Server
│   │   ├── UpdateHUD (RemoteEvent)          -- Server→Client
│   │   └── DamageNumber (RemoteEvent)       -- Server→Client: floating damage
│   ├── Modules/
│   │   ├── GameConfig.lua      -- All balancing, XP curves, stat formulas
│   │   ├── ItemDatabase.lua    -- Item definitions, stats, rarities
│   │   ├── QuestDatabase.lua   -- Quest definitions, objectives, rewards
│   │   ├── EnemyDatabase.lua   -- Enemy stats, abilities, loot tables
│   │   ├── AbilityDatabase.lua -- Player abilities by class
│   │   └── SharedUtils.lua     -- Damage formulas, XP calcs, formatting
│   └── Assets/
│       ├── Weapons/            -- Weapon models
│       ├── Armor/              -- Armor models
│       ├── Effects/            -- Ability VFX, hit effects
│       └── UI/                 -- UI element templates
├── StarterGui/
│   ├── RPG_HUD.lua             -- Health, mana, XP bar, hotbar
│   ├── InventoryUI.lua         -- Bag, equipment slots, item comparison
│   ├── QuestUI.lua             -- Quest log, tracking, completion
│   ├── DialogueUI.lua          -- NPC conversation display
│   ├── PartyUI.lua             -- Party frames, invite system
│   └── ShopUI.lua              -- NPC shops, gamepasses, dev products
├── StarterPlayerScripts/
│   ├── CombatController.lua    -- Click-to-attack, ability keybinds
│   └── CameraController.lua    -- Combat camera, lock-on targeting
└── Workspace/
    ├── Zones/
    │   ├── Zone_Starter/       -- Level 1-10 mobs
    │   ├── Zone_Forest/        -- Level 10-20 mobs
    │   ├── Zone_Desert/        -- Level 20-35 mobs
    │   ├── Zone_Volcanic/      -- Level 35-50 mobs
    │   └── Zone_EndGame/       -- Level 50+ mobs
    ├── Dungeons/
    │   └── Templates/          -- Dungeon maps (cloned per party)
    └── NPCs/
        ├── QuestGivers/
        └── Shopkeepers/
```

### GameConfig Module

```luau
local Config = {}

Config.MaxLevel = 100

-- XP curve: XP needed = base * growth^level
Config.XP = {
    BaseXP = 100,
    GrowthRate = 1.15,          -- Each level needs 15% more XP
    StatPointsPerLevel = 3,
}

-- Base stats at level 1
Config.BaseStats = {
    Health = 100,
    Mana = 50,
    Damage = 10,
    Defense = 5,
    Speed = 16,                 -- WalkSpeed
    CritChance = 5,             -- Percent
    CritMultiplier = 1.5,
}

-- Per-point stat increases
Config.StatGrowth = {
    Strength = { Damage = 2, Health = 5 },
    Intelligence = { Mana = 10, AbilityDamage = 3 },
    Vitality = { Health = 15, Defense = 1 },
    Agility = { Speed = 0.5, CritChance = 0.5 },
}

Config.Combat = {
    MeleeRange = 8,             -- Studs
    RangedRange = 60,           -- Studs
    AbilityCooldownMin = 1,     -- Seconds
    GlobalCooldown = 0.5,       -- Minimum time between any attacks
    InvincibilityFrames = 0.3,  -- After taking damage
    RespawnTime = 5,            -- Seconds after death
}

Config.Loot = {
    QualityWeights = {
        Common    = 60,
        Uncommon  = 25,
        Rare      = 10,
        Epic      = 4,
        Legendary = 1,
    },
    QualityColors = {
        Common    = Color3.fromRGB(180, 180, 180),
        Uncommon  = Color3.fromRGB(0, 200, 0),
        Rare      = Color3.fromRGB(0, 100, 255),
        Epic      = Color3.fromRGB(180, 0, 255),
        Legendary = Color3.fromRGB(255, 170, 0),
    },
    DropChance = 0.30,          -- 30% chance any enemy drops loot
}

Config.Inventory = {
    MaxSlots = 30,
    MaxStack = 99,              -- For consumables
}

Config.Party = {
    MaxSize = 4,
    SharedXPRadius = 100,       -- Studs
    XPSplitRatio = 0.80,        -- Each member gets 80% of solo XP
}

Config.Dungeon = {
    MaxTime = 1800,             -- 30 minutes
    MinPartySize = 1,
    RewardMultiplier = 3.0,     -- 3x loot in dungeons
}

Config.Gamepasses = {
    DoubleXP = 0,               -- Replace with real ID
    ExtraInventory = 0,         -- +15 slots
    AutoLoot = 0,               -- Items auto-pickup
    PetCompanion = 0,           -- Cosmetic pet that follows
    FastTravel = 0,             -- Teleport between zones
}

Config.DevProducts = {
    SmallGold   = { id = 0, amount = 1000 },
    MediumGold  = { id = 0, amount = 5000 },
    LargeGold   = { id = 0, amount = 25000 },
    XPBoost     = { id = 0, duration = 1800, multiplier = 2 },
    Revive      = { id = 0 },  -- Revive without losing spot
    RespecStats = { id = 0 },  -- Reset stat point allocation
}

return Config
```

### Key Implementation Details

**Combat System (Melee):**
```luau
-- Server-authoritative combat
-- Client sends attack intent, server validates and processes

CombatAction.OnServerEvent:Connect(function(player, action, targetId)
    -- Validate cooldown
    local now = tick()
    local lastAttack = playerCooldowns[player.UserId] or 0
    if now - lastAttack < Config.Combat.GlobalCooldown then return end
    playerCooldowns[player.UserId] = now

    if action == "melee" then
        -- Get player character position
        local character = player.Character
        if not character then return end
        local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
        if not humanoidRootPart then return end

        -- Hitbox: find enemies within range in front of player
        local origin = humanoidRootPart.Position
        local direction = humanoidRootPart.CFrame.LookVector

        for _, enemy in workspace.Enemies:GetChildren() do
            local enemyRoot = enemy:FindFirstChild("HumanoidRootPart")
            if not enemyRoot then continue end

            local toEnemy = (enemyRoot.Position - origin)
            local distance = toEnemy.Magnitude
            local dot = direction:Dot(toEnemy.Unit)

            if distance <= Config.Combat.MeleeRange and dot > 0.5 then
                local damage = calculateDamage(player, enemy)
                applyDamage(enemy, damage, player)
                -- Fire floating damage number to nearby clients
                DamageNumber:FireAllClients(enemyRoot.Position, damage)
            end
        end

    elseif action == "ability" then
        -- Handle ability with specific logic per ability type
        useAbility(player, targetId)
    end
end)
```

**Damage Calculation:**
```luau
local function calculateDamage(attacker: Player, target: Model): number
    local stats = getPlayerStats(attacker)
    local weapon = getEquippedWeapon(attacker)

    local baseDamage = stats.Damage + (weapon and weapon.Damage or 0)

    -- Crit check
    local isCrit = math.random(100) <= stats.CritChance
    if isCrit then
        baseDamage *= stats.CritMultiplier
    end

    -- Defense reduction
    local targetDefense = getEnemyDefense(target)
    local reduction = targetDefense / (targetDefense + 100) -- Diminishing returns
    local finalDamage = math.floor(baseDamage * (1 - reduction))

    return math.max(finalDamage, 1) -- Always deal at least 1
end
```

**XP and Leveling:**
```luau
local function xpRequired(level: number): number
    return math.floor(Config.XP.BaseXP * Config.XP.GrowthRate ^ level)
end

local function grantXP(player: Player, amount: number)
    local data = playerData[player.UserId]

    -- Apply party split if in party
    if data.partyId then
        amount = math.floor(amount * Config.Party.XPSplitRatio)
    end

    -- Apply double XP gamepass
    if hasGamepass(player, Config.Gamepasses.DoubleXP) then
        amount *= 2
    end

    data.xp += amount

    -- Check for level up(s)
    while data.xp >= xpRequired(data.level) do
        data.xp -= xpRequired(data.level)
        data.level += 1
        data.statPoints += Config.XP.StatPointsPerLevel
        onLevelUp(player, data.level)
    end

    UpdateHUD:FireClient(player, "xp", data.xp, xpRequired(data.level), data.level)
end
```

**Quest State Machine:**
```luau
-- Quest states: AVAILABLE → ACTIVE → COMPLETE → TURNED_IN
-- Objectives: kill_count, collect_item, talk_to_npc, reach_location

local function updateQuestProgress(player: Player, eventType: string, eventData: {})
    local data = playerData[player.UserId]

    for questId, questState in data.activeQuests do
        local questDef = QuestDatabase[questId]
        for i, objective in questDef.objectives do
            if objective.type == eventType and not questState.completed[i] then
                if matchesObjective(objective, eventData) then
                    questState.progress[i] = (questState.progress[i] or 0) + 1
                    if questState.progress[i] >= objective.required then
                        questState.completed[i] = true
                    end
                end
            end
        end

        -- Check if all objectives complete
        local allDone = true
        for _, completed in questState.completed do
            if not completed then allDone = false break end
        end
        if allDone then
            questState.status = "COMPLETE"
            UpdateHUD:FireClient(player, "quest_complete", questId)
        end
    end
end

-- Called when enemy dies
local function onEnemyKilled(player: Player, enemyName: string)
    updateQuestProgress(player, "kill_count", { enemy = enemyName })
end

-- Called when item picked up
local function onItemCollected(player: Player, itemId: string)
    updateQuestProgress(player, "collect_item", { item = itemId })
end
```

**Loot Table System:**
```luau
local function rollLoot(enemyId: string, playerLevel: number): {}?
    -- Check if loot drops at all
    if math.random() > Config.Loot.DropChance then return nil end

    local enemyDef = EnemyDatabase[enemyId]
    local lootTable = enemyDef.lootTable

    -- Roll quality
    local quality = rollWeighted(Config.Loot.QualityWeights)

    -- Roll specific item from enemy's loot table filtered by quality
    local candidates = {}
    for _, entry in lootTable do
        if entry.quality == quality then
            table.insert(candidates, entry)
        end
    end

    if #candidates == 0 then
        -- Fallback to Common if no items at rolled quality
        for _, entry in lootTable do
            if entry.quality == "Common" then
                table.insert(candidates, entry)
            end
        end
    end

    if #candidates == 0 then return nil end
    local chosen = candidates[math.random(#candidates)]

    return {
        itemId = chosen.itemId,
        quality = quality,
        level = playerLevel + math.random(-2, 2), -- Item level variance
    }
end
```

**Dungeon Instancing:**
```luau
local function createDungeonInstance(partyLeader: Player, dungeonId: string)
    local template = ServerStorage.Dungeons[dungeonId]
    if not template then return end

    -- Clone dungeon
    local instance = template:Clone()
    instance.Name = `Dungeon_{partyLeader.UserId}_{tick()}`
    instance.Parent = workspace.ActiveDungeons

    -- Teleport party members
    local party = getParty(partyLeader)
    local spawnPoint = instance:FindFirstChild("SpawnPoint")

    for _, member in party do
        if member.Character then
            member.Character:PivotTo(spawnPoint.CFrame + Vector3.new(math.random(-5, 5), 0, math.random(-5, 5)))
        end
    end

    -- Start dungeon timer
    task.spawn(function()
        task.wait(Config.Dungeon.MaxTime)
        if instance.Parent then
            -- Time expired, teleport players out, destroy instance
            cleanupDungeon(instance, party)
        end
    end)

    return instance
end
```

**NPC Dialogue System:**
```luau
-- Dialogue trees stored as node graphs
-- Each node: { text, responses: { { text, nextNode, condition? } } }

NPCDialogue.OnServerInvoke = function(player, npcId, choiceIndex)
    local dialogueState = playerDialogueState[player.UserId]

    if not dialogueState or dialogueState.npcId ~= npcId then
        -- Start new conversation
        local npcDef = NPCDatabase[npcId]
        local startNode = npcDef.dialogue.start
        playerDialogueState[player.UserId] = {
            npcId = npcId,
            currentNode = startNode,
        }
        return formatDialogueNode(startNode, player)
    end

    -- Process choice
    local currentNode = dialogueState.currentNode
    local choice = currentNode.responses[choiceIndex]
    if not choice then return nil end

    -- Check conditions (quest status, item ownership, etc.)
    if choice.condition and not evaluateCondition(player, choice.condition) then
        return nil
    end

    -- Execute actions (give quest, open shop, give item)
    if choice.action then
        executeDialogueAction(player, choice.action)
    end

    -- Advance to next node
    if choice.nextNode then
        dialogueState.currentNode = choice.nextNode
        return formatDialogueNode(choice.nextNode, player)
    else
        -- Conversation over
        playerDialogueState[player.UserId] = nil
        return nil
    end
end
```

**Inventory Management (Slots, Stacking, Equipment Comparison):**
```luau
-- ServerScriptService/InventoryManager.lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ItemDatabase = require(ReplicatedStorage.Modules.ItemDatabase)

local EquipItem = ReplicatedStorage.Remotes.EquipItem
local DropItem = ReplicatedStorage.Remotes.DropItem
local UseItem = ReplicatedStorage.Remotes.UseItem
local UpdateHUD = ReplicatedStorage.Remotes.UpdateHUD

-- Inventory structure per player:
-- { slots: { {itemId: string, quantity: number, quality: string, level: number}? }, equipment: { weapon: {}, armor: {}, accessory: {} } }

local function addItemToInventory(player: Player, item: {}): boolean
    local data = playerData[player.UserId]
    if not data then return false end
    local inv = data.inventory

    -- Check if stackable and already exists
    local itemDef = ItemDatabase[item.itemId]
    if itemDef and itemDef.stackable then
        for i, slot in inv.slots do
            if slot and slot.itemId == item.itemId and slot.quantity < Config.Inventory.MaxStack then
                slot.quantity += 1
                UpdateHUD:FireClient(player, "inventory_update", i, slot)
                return true
            end
        end
    end

    -- Find empty slot
    for i = 1, Config.Inventory.MaxSlots do
        if not inv.slots[i] then
            inv.slots[i] = {
                itemId = item.itemId,
                quantity = 1,
                quality = item.quality or "Common",
                level = item.level or 1,
            }
            UpdateHUD:FireClient(player, "inventory_update", i, inv.slots[i])
            return true
        end
    end

    -- Inventory full
    UpdateHUD:FireClient(player, "inventory_full")
    return false
end

local function getEquipmentStats(item: {}): {}
    local itemDef = ItemDatabase[item.itemId]
    if not itemDef then return {} end

    -- Scale stats by item level and quality
    local qualityMultiplier = ({
        Common = 1.0, Uncommon = 1.2, Rare = 1.5, Epic = 2.0, Legendary = 3.0,
    })[item.quality] or 1.0

    local stats = {}
    for statName, baseValue in itemDef.stats do
        stats[statName] = math.floor(baseValue * (1 + item.level * 0.1) * qualityMultiplier)
    end
    return stats
end

-- Equipment comparison: returns stat differences
local function compareEquipment(current: {}?, candidate: {}): {[string]: number}
    local currentStats = current and getEquipmentStats(current) or {}
    local candidateStats = getEquipmentStats(candidate)

    local diff = {}
    -- Get all stat keys from both
    local allStats = {}
    for k in currentStats do allStats[k] = true end
    for k in candidateStats do allStats[k] = true end

    for statName in allStats do
        local currentVal = currentStats[statName] or 0
        local candidateVal = candidateStats[statName] or 0
        diff[statName] = candidateVal - currentVal -- Positive = upgrade
    end
    return diff
end

EquipItem.OnServerEvent:Connect(function(player, slotIndex: number)
    if typeof(slotIndex) ~= "number" then return end
    local data = playerData[player.UserId]
    if not data then return end
    local inv = data.inventory

    local item = inv.slots[slotIndex]
    if not item then return end

    local itemDef = ItemDatabase[item.itemId]
    if not itemDef or not itemDef.equipSlot then return end

    local slot = itemDef.equipSlot -- "weapon", "armor", "accessory"

    -- Swap: unequip current, equip new
    local currentEquipped = inv.equipment[slot]
    inv.equipment[slot] = item
    inv.slots[slotIndex] = currentEquipped -- Put old item in bag (or nil)

    -- Recalculate player stats
    recalculateStats(player)
    UpdateHUD:FireClient(player, "equipment_update", inv.equipment)
end)
```

**Equipment Stat Bonuses (integrated with combat):**
```luau
local function getTotalStats(player: Player): {}
    local data = playerData[player.UserId]
    if not data then return Config.BaseStats end

    local stats = {}
    -- Start with base + level growth
    for statName, baseValue in Config.BaseStats do
        stats[statName] = baseValue
    end

    -- Add stat point allocations
    for statName, points in data.allocatedStats do
        local growth = Config.StatGrowth[statName]
        if growth then
            for bonusStat, perPoint in growth do
                stats[bonusStat] = (stats[bonusStat] or 0) + perPoint * points
            end
        end
    end

    -- Add equipment bonuses
    for _, equippedItem in data.inventory.equipment do
        if equippedItem then
            local equipStats = getEquipmentStats(equippedItem)
            for statName, value in equipStats do
                stats[statName] = (stats[statName] or 0) + value
            end
        end
    end

    return stats
end
```

**Crafting System:**
```luau
-- Crafting: combine materials into items
-- Recipes defined in a ModuleScript

local CraftingRecipes = {
    iron_sword = {
        materials = { iron_ore = 5, wood = 2 },
        result = { itemId = "iron_sword", quality = "Common", level = 10 },
        craftTime = 3, -- seconds
    },
    health_potion = {
        materials = { herb = 3, crystal_shard = 1 },
        result = { itemId = "health_potion", quality = "Common", level = 1 },
        craftTime = 1,
    },
    diamond_armor = {
        materials = { diamond = 10, iron_ore = 5, mythic_thread = 1 },
        result = { itemId = "diamond_armor", quality = "Rare", level = 30 },
        craftTime = 10,
    },
}

local function canCraft(player: Player, recipeId: string): boolean
    local recipe = CraftingRecipes[recipeId]
    if not recipe then return false end
    local data = playerData[player.UserId]
    if not data then return false end

    for materialId, required in recipe.materials do
        local count = countItemInInventory(data, materialId)
        if count < required then return false end
    end
    return true
end

local function craftItem(player: Player, recipeId: string)
    if not canCraft(player, recipeId) then return end
    local recipe = CraftingRecipes[recipeId]
    local data = playerData[player.UserId]

    -- Remove materials
    for materialId, required in recipe.materials do
        removeItemsFromInventory(data, materialId, required)
    end

    -- Wait craft time
    task.wait(recipe.craftTime)

    -- Add result to inventory
    addItemToInventory(player, recipe.result)
    UpdateHUD:FireClient(player, "craft_complete", recipeId)
end
```

**Boss Fight System (Multiple Phases):**
```luau
-- Boss fights with phase transitions
local function createBoss(bossId: string, arena: Model)
    local bossDef = EnemyDatabase[bossId]
    local bossModel = ServerStorage.Bosses[bossId]:Clone()
    bossModel.Parent = arena

    local bossHumanoid = bossModel:FindFirstChildOfClass("Humanoid")
    local bossHealth = bossDef.phases[1].health
    bossHumanoid.MaxHealth = bossHealth
    bossHumanoid.Health = bossHealth

    local currentPhase = 1
    local totalPhases = #bossDef.phases

    -- Phase transition on health thresholds
    bossHumanoid.HealthChanged:Connect(function(newHealth)
        local healthPercent = newHealth / bossHumanoid.MaxHealth

        -- Check for phase transition
        local nextPhase = currentPhase + 1
        if nextPhase <= totalPhases then
            local threshold = bossDef.phases[nextPhase].triggerAt -- e.g., 0.5 = 50% HP
            if healthPercent <= threshold then
                currentPhase = nextPhase
                onPhaseTransition(bossModel, bossDef.phases[currentPhase])
            end
        end

        -- Boss defeated
        if newHealth <= 0 then
            onBossDefeated(bossModel, bossDef)
        end
    end)

    -- Start boss AI
    task.spawn(function()
        while bossHumanoid.Health > 0 do
            local phase = bossDef.phases[currentPhase]
            executeBossAction(bossModel, phase)
            task.wait(phase.actionCooldown or 2)
        end
    end)
end

local function onPhaseTransition(bossModel: Model, phaseData: {})
    -- Visual: flash, particles, screen shake
    local hrp = bossModel:FindFirstChild("HumanoidRootPart")
    if hrp then
        -- Emit phase transition particles
        local emitter = hrp:FindFirstChild("PhaseTransitionEmitter")
        if emitter then emitter:Emit(50) end
    end

    -- Update boss stats for new phase
    local humanoid = bossModel:FindFirstChildOfClass("Humanoid")
    if humanoid then
        humanoid.WalkSpeed = phaseData.speed or 16
    end

    -- Notify all players in arena
    for _, player in Players:GetPlayers() do
        DamageNumber:FireClient(player, hrp.Position, `Phase {phaseData.number}!`)
    end
end

local function executeBossAction(bossModel: Model, phaseData: {})
    -- Pick a random ability from this phase's moveset
    local abilities = phaseData.abilities
    local chosen = abilities[math.random(#abilities)]

    if chosen.type == "aoe_slam" then
        -- Area damage around boss
        local hrp = bossModel:FindFirstChild("HumanoidRootPart")
        if not hrp then return end
        for _, player in Players:GetPlayers() do
            local char = player.Character
            if not char then continue end
            local pHrp = char:FindFirstChild("HumanoidRootPart")
            if not pHrp then continue end
            if (pHrp.Position - hrp.Position).Magnitude <= chosen.radius then
                applyDamageToPlayer(player, chosen.damage)
            end
        end

    elseif chosen.type == "projectile" then
        -- Fire projectile at closest player
        local target = getClosestPlayer(bossModel)
        if target then
            fireProjectile(bossModel, target, chosen.damage, chosen.speed)
        end

    elseif chosen.type == "summon_adds" then
        -- Spawn minions
        for i = 1, chosen.count do
            spawnMinion(chosen.minionId, bossModel.PrimaryPart.Position)
        end

    elseif chosen.type == "enrage" then
        -- Temporary speed/damage boost
        local humanoid = bossModel:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid.WalkSpeed *= 1.5
            task.delay(chosen.duration, function()
                if humanoid then humanoid.WalkSpeed /= 1.5 end
            end)
        end
    end
end
```

---

## Monetization Strategy for RPGs

### Gamepasses (One-Time)

| Gamepass | Price (Robux) | Effect |
|----------|---------------|--------|
| 2x XP | 299 | Permanent double experience |
| Extra Inventory (+15 slots) | 149 | More item storage |
| Auto-Loot | 199 | Items auto-pickup within radius |
| Pet Companion | 99 | Cosmetic pet that follows player |
| Fast Travel | 249 | Teleport between discovered zones |
| Extra Stat Points | 199 | +2 stat points per level |

### Dev Products (Repeatable)

| Product | Price (Robux) | Effect |
|---------|---------------|--------|
| 1K Gold | 49 | Instant gold |
| 5K Gold | 199 | Instant gold |
| 25K Gold | 799 | Instant gold |
| XP Boost (30 min) | 75 | 2x XP for 30 minutes |
| Instant Revive | 25 | Revive on spot without respawning |
| Stat Respec | 49 | Reset all stat point allocations |

### Rewarded Video Ads

- Watch ad for 10-minute 2x XP boost
- Watch ad for free revive
- Watch ad for bonus dungeon reward chest

---

## RPG Meta Intelligence (Feb 2026)

### What Works on Roblox

- **Anime-inspired RPGs dominate**: Blox Fruits (52.95B visits), Shindo Life, King Legacy. Anime aesthetic is proven to attract the Roblox audience.
- **Progression depth is king**: Players want hundreds of hours of content. Shallow RPGs die fast.
- **Trading as endgame**: When gear/items become tradeable, your economy becomes self-sustaining social content.
- **Boss fights as events**: Scheduled or triggered boss encounters create "appointment gaming."
- **Class/specialization systems**: Let players build unique identities. Respec gamepasses print money.

### Differentiation from Saturated Anime RPGs

1. **Non-anime themes**: Fantasy, sci-fi, western, steampunk. Less competition.
2. **Deeper combat**: Most Roblox RPGs have simple click-spam combat. Actual ability combos, dodging, and positioning stand out.
3. **Story-driven**: Most Roblox RPGs have minimal story. A real narrative with characters creates emotional investment.
4. **Procedural dungeons**: Like Doors (5B+ visits). Random layouts = infinite replayability.
5. **Co-op focus**: Party dungeons with roles (tank, healer, DPS) create social bonds.

### RPG-Specific Retention Hooks

- **Daily quests**: 3 rotating quests for bonus XP/gold. Creates daily return habit.
- **Weekly dungeon reset**: Best dungeon loot resets weekly. Scheduled engagement.
- **Guild system**: Player groups with shared goals, guild levels, guild bank.
- **PvP arena**: Optional competitive mode with ranking system. Separate from PvE.
- **Achievement system**: Long-term goals beyond leveling (kill 1000 enemies, find all items, etc.).
- **Seasonal content**: New zones, bosses, items every 4-6 weeks.

### Successful RPGs to Study

- **Blox Fruits**: Fruit powers + exploration + boss fights + PvP. 52.95B visits.
- **Shindo Life**: Naruto-inspired, bloodline system, deep progression.
- **Doors**: Horror + procedural rooms + co-op. Proves procedural content works.
- **The Forge (BETA)**: Mining + crafting + combat. Hybrid approach succeeding.

---

## Luau Standards

- Use `task.wait()` not `wait()`
- Use `task.spawn()` not `spawn()`
- Wrap DataStore calls in `pcall`
- Validate ALL RemoteEvent inputs server-side
- Rate-limit combat actions (prevent attack speed exploits)
- Use type annotations on function signatures
- Use string interpolation
- Never trust client for damage values, XP gains, or inventory state
- Save on PlayerRemoving AND game:BindToClose
- Use UpdateAsync for inventory changes (atomic to prevent duplication exploits)
- Debounce hitbox detection (invincibility frames after damage)

---

## Anti-Exploit for RPGs

RPGs are high-value exploit targets (tradeable items have real value). Key protections:

1. **Server-authoritative combat**: Client sends intent ("attack"), server validates range/cooldown/damage
2. **Server-authoritative inventory**: Client never modifies item data directly
3. **Trade validation**: Both players must have items they claim, verify server-side before swap
4. **Anti-speed**: Check character position delta against max possible speed + tolerance
5. **Anti-teleport**: Validate position changes are physically possible
6. **DataStore versioning**: Use versioned keys for schema migration
7. **Rate limiting**: All remotes enforce minimum intervals
8. **Sanity checks**: If XP gain rate exceeds theoretical maximum, flag account

---

## Development Workflow

1. Use robloxstudio MCP to create folder structure and initial zones
2. Create all database ModuleScripts first (GameConfig, ItemDatabase, EnemyDatabase, QuestDatabase)
3. Create server scripts (CombatSystem, QuestManager, InventoryManager, DataManager)
4. Create remote events and functions
5. Create enemy spawner with basic AI (idle, chase, attack states)
6. Create client scripts (RPG_HUD, InventoryUI, CombatController)
7. Build Zone_Starter with test enemies and one quest
8. Use roblox-test MCP to play test combat loop
9. Verify: attacks hit, XP grants, items drop, quests track
10. Test data persistence (leave and rejoin with inventory intact)
11. Build remaining zones and quests
12. Add dungeon system
13. Add monetization (gamepasses, dev products, shop NPCs)
14. Balance combat numbers (damage, defense, XP rates)
15. Polish UI, effects, sounds
