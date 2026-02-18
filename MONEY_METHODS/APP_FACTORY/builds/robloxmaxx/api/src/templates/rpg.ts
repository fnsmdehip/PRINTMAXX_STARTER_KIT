export const RPG_TEMPLATE = {
  name: 'Core RPG Systems',
  genre: 'rpg',
  description:
    'Core RPG game systems: combat, XP/leveling, inventory, stats, NPC interaction, and data persistence. Build quests and world on top.',
  scripts: [
    {
      action: 'CreateFolder' as const,
      folderName: 'Events',
      serviceName: 'ReplicatedStorage',
      explanation: 'Folder for RemoteEvents and RemoteFunctions',
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'RPGConfig',
      scriptType: 'ModuleScript',
      serviceName: 'ReplicatedStorage',
      explanation: 'Shared RPG configuration: stats, XP curve, items, enemies',
      newCode: `--[[
  RPGConfig - Shared RPG game configuration
  XP curve, stat definitions, item database, enemy definitions
]]

local RPGConfig = {}

-- XP curve: XP needed for level N = BaseXP * GrowthRate^(N-1)
RPGConfig.BaseXP = 100
RPGConfig.XPGrowthRate = 1.5
RPGConfig.MaxLevel = 50
RPGConfig.StatPointsPerLevel = 3

-- Base stats at level 1
RPGConfig.BaseStats = {
  Health = 100,
  Damage = 10,
  Defense = 5,
  Speed = 16, -- WalkSpeed
}

-- Stat point scaling (per point invested)
RPGConfig.StatScaling = {
  Health = 20,   -- +20 HP per point
  Damage = 3,    -- +3 damage per point
  Defense = 2,   -- +2 defense per point
  Speed = 0.5,   -- +0.5 walkspeed per point
}

-- Items
RPGConfig.Items = {
  -- Weapons
  { id = "wooden_sword", name = "Wooden Sword", type = "weapon", damage = 5, cost = 0 },
  { id = "iron_sword", name = "Iron Sword", type = "weapon", damage = 15, cost = 500 },
  { id = "steel_blade", name = "Steel Blade", type = "weapon", damage = 35, cost = 2500 },
  { id = "dark_katana", name = "Dark Katana", type = "weapon", damage = 80, cost = 10000 },
  { id = "legendary_excalibur", name = "Excalibur", type = "weapon", damage = 200, cost = 50000 },

  -- Armor
  { id = "leather_armor", name = "Leather Armor", type = "armor", defense = 5, cost = 300 },
  { id = "iron_armor", name = "Iron Armor", type = "armor", defense = 15, cost = 1500 },
  { id = "dragon_armor", name = "Dragon Armor", type = "armor", defense = 40, cost = 12000 },

  -- Potions
  { id = "health_potion", name = "Health Potion", type = "consumable", healAmount = 50, cost = 50, stackable = true },
  { id = "mega_potion", name = "Mega Potion", type = "consumable", healAmount = 200, cost = 200, stackable = true },
}

-- Enemies
RPGConfig.Enemies = {
  { id = "slime", name = "Slime", health = 30, damage = 5, xp = 15, gold = 10, level = 1 },
  { id = "goblin", name = "Goblin", health = 60, damage = 12, xp = 30, gold = 25, level = 3 },
  { id = "skeleton", name = "Skeleton", health = 100, damage = 20, xp = 60, gold = 50, level = 6 },
  { id = "wolf", name = "Dark Wolf", health = 150, damage = 30, xp = 100, gold = 80, level = 10 },
  { id = "dragon", name = "Fire Dragon", health = 500, damage = 60, xp = 500, gold = 300, level = 20 },
  { id = "demon_lord", name = "Demon Lord", health = 2000, damage = 120, xp = 2000, gold = 1000, level = 35 },
}

-- Currency
RPGConfig.CurrencyName = "Gold"

-- Gamepasses (replace 0 with real IDs)
RPGConfig.GamePassIds = {
  x2XP = 0,
  x2Gold = 0,
  VIP = 0,
}

RPGConfig.DevProductIds = {
  Gold1000 = 0,
  Gold10000 = 0,
  FullHeal = 0,
}

return RPGConfig`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'RPGCore',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Server-side RPG logic: leveling, stats, inventory, combat damage calculation, data persistence',
      newCode: `--[[
  RPGCore - Server-side RPG game logic
  Handles: XP/leveling, stat allocation, inventory, combat, gold, data saving
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local Config = require(ReplicatedStorage:WaitForChild("RPGConfig"))

local dataStore = DataStoreService:GetDataStore("RPGData_v1")
local Events = ReplicatedStorage:WaitForChild("Events")

-- RemoteEvents
local attackEvent = Instance.new("RemoteEvent")
attackEvent.Name = "Attack"
attackEvent.Parent = Events

local allocateStatEvent = Instance.new("RemoteEvent")
allocateStatEvent.Name = "AllocateStat"
allocateStatEvent.Parent = Events

local buyItemEvent = Instance.new("RemoteEvent")
buyItemEvent.Name = "BuyItem"
buyItemEvent.Parent = Events

local equipItemEvent = Instance.new("RemoteEvent")
equipItemEvent.Name = "EquipItem"
equipItemEvent.Parent = Events

local useItemEvent = Instance.new("RemoteEvent")
useItemEvent.Name = "UseItem"
useItemEvent.Parent = Events

local updateUIEvent = Instance.new("RemoteEvent")
updateUIEvent.Name = "UpdateUI"
updateUIEvent.Parent = Events

local notifyEvent = Instance.new("RemoteEvent")
notifyEvent.Name = "Notify"
notifyEvent.Parent = Events

local damageNumberEvent = Instance.new("RemoteEvent")
damageNumberEvent.Name = "DamageNumber"
damageNumberEvent.Parent = Events

-- Types
type InventoryItem = { id: string, quantity: number }
type StatPoints = { Health: number, Damage: number, Defense: number, Speed: number }
type PlayerData = {
  level: number,
  xp: number,
  gold: number,
  statPoints: number,
  allocatedStats: StatPoints,
  inventory: {InventoryItem},
  equippedWeapon: string?,
  equippedArmor: string?,
}

local playerData: { [number]: PlayerData } = {}

local function getDefaultData(): PlayerData
  return {
    level = 1,
    xp = 0,
    gold = 0,
    statPoints = 0,
    allocatedStats = { Health = 0, Damage = 0, Defense = 0, Speed = 0 },
    inventory = {{ id = "wooden_sword", quantity = 1 }},
    equippedWeapon = "wooden_sword",
    equippedArmor = nil,
  }
end

local function xpForLevel(level: number): number
  return math.floor(Config.BaseXP * Config.XPGrowthRate ^ (level - 1))
end

local function getItemDef(itemId: string)
  for _, item in ipairs(Config.Items) do
    if item.id == itemId then return item end
  end
  return nil
end

local function getPlayerStats(data: PlayerData)
  local stats = {}
  for stat, base in pairs(Config.BaseStats) do
    local allocated = data.allocatedStats[stat] or 0
    local scaling = Config.StatScaling[stat] or 0
    stats[stat] = base + (allocated * scaling)
  end

  -- Equipment bonuses
  if data.equippedWeapon then
    local wep = getItemDef(data.equippedWeapon)
    if wep and wep.damage then
      stats.Damage += wep.damage
    end
  end
  if data.equippedArmor then
    local armor = getItemDef(data.equippedArmor)
    if armor and armor.defense then
      stats.Defense += armor.defense
    end
  end

  return stats
end

local function giveXP(player: Player, amount: number)
  local data = playerData[player.UserId]
  if not data then return end

  -- Check x2 XP gamepass
  local has2x = false
  pcall(function()
    has2x = MarketplaceService:UserOwnsGamePassAsync(player.UserId, Config.GamePassIds.x2XP)
  end)
  if has2x then amount *= 2 end

  data.xp += amount

  -- Level up loop
  while data.level < Config.MaxLevel do
    local needed = xpForLevel(data.level)
    if data.xp >= needed then
      data.xp -= needed
      data.level += 1
      data.statPoints += Config.StatPointsPerLevel
      notifyEvent:FireClient(player, "LEVEL UP! You are now level " .. data.level)
    else
      break
    end
  end

  -- Update leaderstats
  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local lvl = leaderstats:FindFirstChild("Level")
    if lvl then lvl.Value = data.level end
    local goldStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if goldStat then goldStat.Value = data.gold end
  end

  updateUIEvent:FireClient(player, data)
end

local function giveGold(player: Player, amount: number)
  local data = playerData[player.UserId]
  if not data then return end

  local has2x = false
  pcall(function()
    has2x = MarketplaceService:UserOwnsGamePassAsync(player.UserId, Config.GamePassIds.x2Gold)
  end)
  if has2x then amount *= 2 end

  data.gold += amount

  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local goldStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if goldStat then goldStat.Value = data.gold end
  end
end

local function loadData(player: Player)
  local key = "rpg_" .. player.UserId
  local success, data = pcall(function()
    return dataStore:GetAsync(key)
  end)

  if success and data then
    playerData[player.UserId] = data
  else
    playerData[player.UserId] = getDefaultData()
  end

  local d = playerData[player.UserId]

  -- Leaderstats
  local leaderstats = Instance.new("Folder")
  leaderstats.Name = "leaderstats"
  leaderstats.Parent = player

  local levelStat = Instance.new("IntValue")
  levelStat.Name = "Level"
  levelStat.Value = d.level
  levelStat.Parent = leaderstats

  local goldStat = Instance.new("IntValue")
  goldStat.Name = Config.CurrencyName
  goldStat.Value = d.gold
  goldStat.Parent = leaderstats

  -- Apply stats to character
  player.CharacterAdded:Connect(function(char)
    local humanoid = char:WaitForChild("Humanoid")
    local stats = getPlayerStats(d)
    humanoid.MaxHealth = stats.Health
    humanoid.Health = stats.Health
    humanoid.WalkSpeed = stats.Speed
  end)

  updateUIEvent:FireClient(player, d)
end

local function saveData(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  local key = "rpg_" .. player.UserId
  pcall(function()
    dataStore:SetAsync(key, data)
  end)
end

-- Attack handler (player attacks NPC/enemy)
local attackCooldowns: { [number]: number } = {}

attackEvent.OnServerEvent:Connect(function(player: Player, targetName: string)
  if type(targetName) ~= "string" then return end

  local now = tick()
  local last = attackCooldowns[player.UserId] or 0
  if now - last < 0.5 then return end -- 2 attacks/sec max
  attackCooldowns[player.UserId] = now

  local data = playerData[player.UserId]
  if not data then return end

  -- Find enemy definition
  local enemyDef = nil
  for _, e in ipairs(Config.Enemies) do
    if e.name == targetName or e.id == targetName then
      enemyDef = e
      break
    end
  end
  if not enemyDef then return end

  -- Calculate damage
  local stats = getPlayerStats(data)
  local playerDamage = math.max(1, stats.Damage - math.floor(enemyDef.damage * 0.2))

  -- Show damage number on client
  damageNumberEvent:FireClient(player, playerDamage, targetName)

  -- Check if enemy is killed (simplified - in production, track enemy HP on server)
  -- For template: enemy dies in ceil(hp/damage) hits, reward immediately
  -- Real implementation should track per-enemy health
  giveXP(player, enemyDef.xp)
  giveGold(player, enemyDef.gold)
end)

-- Allocate stat point
allocateStatEvent.OnServerEvent:Connect(function(player: Player, statName: string)
  if type(statName) ~= "string" then return end

  local data = playerData[player.UserId]
  if not data then return end
  if data.statPoints <= 0 then return end

  if not Config.StatScaling[statName] then return end

  data.statPoints -= 1
  data.allocatedStats[statName] = (data.allocatedStats[statName] or 0) + 1

  -- Apply to character
  local character = player.Character
  if character then
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if humanoid then
      local stats = getPlayerStats(data)
      humanoid.MaxHealth = stats.Health
      humanoid.Health = math.min(humanoid.Health + Config.StatScaling.Health, stats.Health)
      humanoid.WalkSpeed = stats.Speed
    end
  end

  updateUIEvent:FireClient(player, data)
end)

-- Buy item
buyItemEvent.OnServerEvent:Connect(function(player: Player, itemId: string)
  if type(itemId) ~= "string" then return end

  local data = playerData[player.UserId]
  if not data then return end

  local itemDef = getItemDef(itemId)
  if not itemDef then return end
  if data.gold < (itemDef.cost or 0) then return end

  data.gold -= itemDef.cost

  -- Add to inventory (stack if stackable)
  local found = false
  if itemDef.stackable then
    for _, inv in ipairs(data.inventory) do
      if inv.id == itemId then
        inv.quantity += 1
        found = true
        break
      end
    end
  end
  if not found then
    table.insert(data.inventory, { id = itemId, quantity = 1 })
  end

  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local goldStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if goldStat then goldStat.Value = data.gold end
  end

  updateUIEvent:FireClient(player, data)
  notifyEvent:FireClient(player, "Purchased: " .. itemDef.name)
end)

-- Equip item
equipItemEvent.OnServerEvent:Connect(function(player: Player, itemId: string)
  if type(itemId) ~= "string" then return end

  local data = playerData[player.UserId]
  if not data then return end

  -- Verify player owns item
  local owns = false
  for _, inv in ipairs(data.inventory) do
    if inv.id == itemId then
      owns = true
      break
    end
  end
  if not owns then return end

  local itemDef = getItemDef(itemId)
  if not itemDef then return end

  if itemDef.type == "weapon" then
    data.equippedWeapon = itemId
  elseif itemDef.type == "armor" then
    data.equippedArmor = itemId
  end

  updateUIEvent:FireClient(player, data)
end)

-- Use consumable
useItemEvent.OnServerEvent:Connect(function(player: Player, itemId: string)
  if type(itemId) ~= "string" then return end

  local data = playerData[player.UserId]
  if not data then return end

  local itemDef = getItemDef(itemId)
  if not itemDef or itemDef.type ~= "consumable" then return end

  -- Find in inventory
  for i, inv in ipairs(data.inventory) do
    if inv.id == itemId and inv.quantity > 0 then
      inv.quantity -= 1
      if inv.quantity <= 0 then
        table.remove(data.inventory, i)
      end

      -- Apply effect
      local character = player.Character
      if character and itemDef.healAmount then
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if humanoid then
          humanoid.Health = math.min(humanoid.Health + itemDef.healAmount, humanoid.MaxHealth)
        end
      end

      updateUIEvent:FireClient(player, data)
      break
    end
  end
end)

-- Dev product purchases
MarketplaceService.ProcessReceipt = function(receiptInfo)
  local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
  if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end

  local data = playerData[receiptInfo.PlayerId]
  if not data then return Enum.ProductPurchaseDecision.NotProcessedYet end

  local productId = receiptInfo.ProductId

  if productId == Config.DevProductIds.Gold1000 then
    giveGold(player, 1000)
  elseif productId == Config.DevProductIds.Gold10000 then
    giveGold(player, 10000)
  elseif productId == Config.DevProductIds.FullHeal then
    local character = player.Character
    if character then
      local humanoid = character:FindFirstChildOfClass("Humanoid")
      if humanoid then
        humanoid.Health = humanoid.MaxHealth
      end
    end
  end

  updateUIEvent:FireClient(player, data)
  return Enum.ProductPurchaseDecision.PurchaseGranted
end

-- Player connections
Players.PlayerAdded:Connect(loadData)
Players.PlayerRemoving:Connect(function(player)
  saveData(player)
  playerData[player.UserId] = nil
  attackCooldowns[player.UserId] = nil
end)

game:BindToClose(function()
  for _, player in ipairs(Players:GetPlayers()) do
    saveData(player)
  end
end)

-- Auto-save every 60s
task.spawn(function()
  while true do
    task.wait(60)
    for _, player in ipairs(Players:GetPlayers()) do
      saveData(player)
    end
  end
end)

print("[RPGCore] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'RPG_HUD',
      scriptType: 'LocalScript',
      serviceName: 'StarterGui',
      explanation: 'Client-side RPG UI: health bar, XP bar, gold, level, stat allocation, inventory button',
      newCode: `--[[
  RPG_HUD - Client-side RPG interface
  Health bar, XP bar, level, gold, stat allocation, combat
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("RPGConfig"))
local Events = ReplicatedStorage:WaitForChild("Events")

local AttackEvent = Events:WaitForChild("Attack")
local AllocateStat = Events:WaitForChild("AllocateStat")
local UpdateUI = Events:WaitForChild("UpdateUI")
local Notify = Events:WaitForChild("Notify")
local DamageNumber = Events:WaitForChild("DamageNumber")

local player = Players.LocalPlayer

local screenGui = Instance.new("ScreenGui")
screenGui.Name = "RPG_HUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = player:WaitForChild("PlayerGui")

-- Health bar (top left)
local healthBg = Instance.new("Frame")
healthBg.Size = UDim2.new(0, 200, 0, 20)
healthBg.Position = UDim2.new(0, 10, 0, 10)
healthBg.BackgroundColor3 = Color3.fromRGB(50, 20, 20)
healthBg.Parent = screenGui
Instance.new("UICorner", healthBg).CornerRadius = UDim.new(0, 4)

local healthFill = Instance.new("Frame")
healthFill.Size = UDim2.new(1, 0, 1, 0)
healthFill.BackgroundColor3 = Color3.fromRGB(220, 50, 50)
healthFill.Parent = healthBg
Instance.new("UICorner", healthFill).CornerRadius = UDim.new(0, 4)

local healthText = Instance.new("TextLabel")
healthText.Size = UDim2.new(1, 0, 1, 0)
healthText.BackgroundTransparency = 1
healthText.Text = "100/100"
healthText.TextColor3 = Color3.fromRGB(255, 255, 255)
healthText.TextSize = 12
healthText.Font = Enum.Font.GothamBold
healthText.ZIndex = 2
healthText.Parent = healthBg

-- XP bar (below health)
local xpBg = Instance.new("Frame")
xpBg.Size = UDim2.new(0, 200, 0, 12)
xpBg.Position = UDim2.new(0, 10, 0, 34)
xpBg.BackgroundColor3 = Color3.fromRGB(20, 20, 50)
xpBg.Parent = screenGui
Instance.new("UICorner", xpBg).CornerRadius = UDim.new(0, 3)

local xpFill = Instance.new("Frame")
xpFill.Size = UDim2.new(0, 0, 1, 0)
xpFill.BackgroundColor3 = Color3.fromRGB(80, 80, 255)
xpFill.Parent = xpBg
Instance.new("UICorner", xpFill).CornerRadius = UDim.new(0, 3)

local xpText = Instance.new("TextLabel")
xpText.Size = UDim2.new(1, 0, 1, 0)
xpText.BackgroundTransparency = 1
xpText.Text = "XP: 0/100"
xpText.TextColor3 = Color3.fromRGB(200, 200, 255)
xpText.TextSize = 10
xpText.Font = Enum.Font.GothamBold
xpText.ZIndex = 2
xpText.Parent = xpBg

-- Level + Gold display
local infoLabel = Instance.new("TextLabel")
infoLabel.Size = UDim2.new(0, 200, 0, 20)
infoLabel.Position = UDim2.new(0, 10, 0, 50)
infoLabel.BackgroundTransparency = 1
infoLabel.Text = "Lv.1 | 0 Gold | 0 SP"
infoLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
infoLabel.TextSize = 14
infoLabel.Font = Enum.Font.GothamBold
infoLabel.TextXAlignment = Enum.TextXAlignment.Left
infoLabel.Parent = screenGui

-- Notification label
local notifLabel = Instance.new("TextLabel")
notifLabel.Size = UDim2.new(0, 400, 0, 40)
notifLabel.Position = UDim2.new(0.5, -200, 0, 80)
notifLabel.BackgroundTransparency = 1
notifLabel.Text = ""
notifLabel.TextColor3 = Color3.fromRGB(255, 255, 100)
notifLabel.TextSize = 18
notifLabel.Font = Enum.Font.GothamBlack
notifLabel.Parent = screenGui

-- XP needed for level
local function xpForLevel(level: number): number
  return math.floor(Config.BaseXP * Config.XPGrowthRate ^ (level - 1))
end

-- Update from server data
UpdateUI.OnClientEvent:Connect(function(data)
  local needed = xpForLevel(data.level)
  xpText.Text = "XP: " .. data.xp .. "/" .. needed
  xpFill.Size = UDim2.new(math.clamp(data.xp / needed, 0, 1), 0, 1, 0)
  infoLabel.Text = "Lv." .. data.level .. " | " .. data.gold .. " Gold | " .. data.statPoints .. " SP"
end)

-- Track health bar from character humanoid
local function connectHealth()
  local character = player.Character or player.CharacterAdded:Wait()
  local humanoid = character:WaitForChild("Humanoid")

  local function update()
    local hp = math.floor(humanoid.Health)
    local maxHp = math.floor(humanoid.MaxHealth)
    healthText.Text = hp .. "/" .. maxHp
    healthFill.Size = UDim2.new(math.clamp(humanoid.Health / humanoid.MaxHealth, 0, 1), 0, 1, 0)
  end

  humanoid.HealthChanged:Connect(update)
  humanoid:GetPropertyChangedSignal("MaxHealth"):Connect(update)
  update()
end

player.CharacterAdded:Connect(function()
  task.defer(connectHealth)
end)
if player.Character then
  task.defer(connectHealth)
end

-- Notifications
Notify.OnClientEvent:Connect(function(msg: string)
  notifLabel.Text = msg
  task.delay(3, function()
    if notifLabel.Text == msg then
      notifLabel.Text = ""
    end
  end)
end)

-- Damage numbers
DamageNumber.OnClientEvent:Connect(function(dmg: number, targetName: string)
  local label = Instance.new("TextLabel")
  label.Size = UDim2.new(0, 100, 0, 30)
  label.Position = UDim2.new(0.5, math.random(-50, 50), 0.4, math.random(-30, 30))
  label.BackgroundTransparency = 1
  label.Text = "-" .. tostring(dmg)
  label.TextColor3 = Color3.fromRGB(255, 80, 80)
  label.TextSize = 20
  label.Font = Enum.Font.GothamBlack
  label.Parent = screenGui

  -- Float up and fade
  task.spawn(function()
    for i = 1, 20 do
      task.wait(0.05)
      label.Position = label.Position + UDim2.new(0, 0, 0, -2)
      label.TextTransparency = i / 20
    end
    label:Destroy()
  end)
end)

print("[RPG_HUD] Loaded")`,
    },
  ],
};
