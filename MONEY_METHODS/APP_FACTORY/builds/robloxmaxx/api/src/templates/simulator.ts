export const SIMULATOR_TEMPLATE = {
  name: 'Complete Simulator',
  genre: 'simulator',
  description:
    'A full click simulator with tools, pet hatching, rebirths, zones, codes system, and data persistence.',
  scripts: [
    {
      action: 'CreateFolder' as const,
      folderName: 'Events',
      serviceName: 'ReplicatedStorage',
      explanation: 'Folder for RemoteEvents and RemoteFunctions',
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'SimConfig',
      scriptType: 'ModuleScript',
      serviceName: 'ReplicatedStorage',
      explanation: 'Shared simulator configuration: tools, pets, zones, codes, gamepasses',
      newCode: `--[[
  SimConfig - Shared simulator game configuration
  Modify these values to balance progression and monetization
]]

local SimConfig = {}

SimConfig.CurrencyName = "Power"
SimConfig.BaseClickValue = 1

-- Tools (higher tier = more power per click)
SimConfig.Tools = {
  { name = "Wooden Pickaxe", cost = 0, multiplier = 1 },
  { name = "Stone Pickaxe", cost = 100, multiplier = 2 },
  { name = "Iron Pickaxe", cost = 500, multiplier = 5 },
  { name = "Gold Pickaxe", cost = 2500, multiplier = 12 },
  { name = "Diamond Pickaxe", cost = 15000, multiplier = 30 },
  { name = "Emerald Pickaxe", cost = 75000, multiplier = 80 },
  { name = "Mythic Pickaxe", cost = 500000, multiplier = 250 },
}

-- Pets with weighted rarity
SimConfig.Pets = {
  { name = "Cat", rarity = "Common", weight = 40, multiplier = 1.1 },
  { name = "Dog", rarity = "Common", weight = 30, multiplier = 1.15 },
  { name = "Fox", rarity = "Rare", weight = 12, multiplier = 1.5 },
  { name = "Wolf", rarity = "Rare", weight = 8, multiplier = 1.8 },
  { name = "Dragon", rarity = "Legendary", weight = 5, multiplier = 3.0 },
  { name = "Phoenix", rarity = "Legendary", weight = 3, multiplier = 4.0 },
  { name = "Void Entity", rarity = "Mythic", weight = 1.5, multiplier = 10.0 },
  { name = "Galaxy Serpent", rarity = "Mythic", weight = 0.5, multiplier = 25.0 },
}

SimConfig.EggCost = 500
SimConfig.MaxEquippedPets = 3
SimConfig.MaxPetInventory = 50

-- Rebirth
SimConfig.RebirthCost = 500000
SimConfig.RebirthBonus = 0.25 -- +25% per rebirth

-- Zones (unlock at power thresholds)
SimConfig.Zones = {
  { name = "Starter Meadow", requirement = 0, clickMultiplier = 1 },
  { name = "Dark Forest", requirement = 1000, clickMultiplier = 2 },
  { name = "Crystal Caves", requirement = 10000, clickMultiplier = 5 },
  { name = "Volcanic Peak", requirement = 100000, clickMultiplier = 12 },
  { name = "Cloud Kingdom", requirement = 1000000, clickMultiplier = 30 },
  { name = "Void Realm", requirement = 10000000, clickMultiplier = 100 },
}

-- Codes (code string -> reward)
SimConfig.Codes = {
  LAUNCH = { currency = 500, description = "Launch reward" },
  THANKYOU = { currency = 1000, description = "Thanks for playing" },
  PETS = { currency = 2500, description = "Pet update reward" },
}

-- Gamepasses (replace 0 with real IDs)
SimConfig.GamePassIds = {
  AutoClick = 0,
  x2Power = 0,
  VIP = 0,
  ExtraPetSlots = 0,
}

-- Dev Products (replace 0 with real IDs)
SimConfig.DevProductIds = {
  Power1000 = 0,
  Power10000 = 0,
  LegendaryEgg = 0,
}

-- Auto-click interval for gamepass holders (seconds)
SimConfig.AutoClickInterval = 0.5

return SimConfig`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'SimulatorCore',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Server-side simulator logic: clicking, tools, zones, rebirths, codes, data persistence',
      newCode: `--[[
  SimulatorCore - Server-side simulator game logic
  Handles: clicking, tool purchases, zone unlocks, rebirths, codes, data saving
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local Config = require(ReplicatedStorage:WaitForChild("SimConfig"))

local dataStore = DataStoreService:GetDataStore("SimData_v1")
local Events = ReplicatedStorage:WaitForChild("Events")

-- Create RemoteEvents
local clickEvent = Instance.new("RemoteEvent")
clickEvent.Name = "Click"
clickEvent.Parent = Events

local buyToolEvent = Instance.new("RemoteEvent")
buyToolEvent.Name = "BuyTool"
buyToolEvent.Parent = Events

local hatchEggEvent = Instance.new("RemoteEvent")
hatchEggEvent.Name = "HatchEgg"
hatchEggEvent.Parent = Events

local equipPetEvent = Instance.new("RemoteEvent")
equipPetEvent.Name = "EquipPet"
equipPetEvent.Parent = Events

local rebirthEvent = Instance.new("RemoteEvent")
rebirthEvent.Name = "Rebirth"
rebirthEvent.Parent = Events

local redeemCodeEvent = Instance.new("RemoteEvent")
redeemCodeEvent.Name = "RedeemCode"
redeemCodeEvent.Parent = Events

local updateUIEvent = Instance.new("RemoteEvent")
updateUIEvent.Name = "UpdateUI"
updateUIEvent.Parent = Events

local notifyEvent = Instance.new("RemoteEvent")
notifyEvent.Name = "Notify"
notifyEvent.Parent = Events

-- Player data
type PetEntry = { name: string, rarity: string, multiplier: number }
type PlayerData = {
  power: number,
  rebirths: number,
  toolIndex: number,
  pets: {PetEntry},
  equippedPets: {number}, -- indices into pets array
  redeemedCodes: {string},
  currentZone: number,
}

local playerData: { [number]: PlayerData } = {}

local function getDefaultData(): PlayerData
  return {
    power = 0,
    rebirths = 0,
    toolIndex = 1,
    pets = {},
    equippedPets = {},
    redeemedCodes = {},
    currentZone = 1,
  }
end

local function getRebirthMultiplier(rebirths: number): number
  return 1 + (rebirths * Config.RebirthBonus)
end

local function getPetMultiplier(data: PlayerData): number
  local mult = 1.0
  for _, petIdx in ipairs(data.equippedPets) do
    local pet = data.pets[petIdx]
    if pet then
      mult *= pet.multiplier
    end
  end
  return mult
end

local function getClickValue(player: Player): number
  local data = playerData[player.UserId]
  if not data then return 0 end

  local tool = Config.Tools[data.toolIndex] or Config.Tools[1]
  local zone = Config.Zones[data.currentZone] or Config.Zones[1]
  local base = Config.BaseClickValue * tool.multiplier * zone.clickMultiplier
  local rebirthMult = getRebirthMultiplier(data.rebirths)
  local petMult = getPetMultiplier(data)

  -- Check x2 gamepass
  local has2x = false
  pcall(function()
    has2x = MarketplaceService:UserOwnsGamePassAsync(player.UserId, Config.GamePassIds.x2Power)
  end)

  local gpMult = if has2x then 2 else 1

  return math.floor(base * rebirthMult * petMult * gpMult)
end

local function updateLeaderstats(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local powerStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if powerStat then powerStat.Value = data.power end
    local rebirthStat = leaderstats:FindFirstChild("Rebirths")
    if rebirthStat then rebirthStat.Value = data.rebirths end
  end
end

local function loadData(player: Player)
  local key = "sim_" .. player.UserId
  local success, data = pcall(function()
    return dataStore:GetAsync(key)
  end)

  if success and data then
    playerData[player.UserId] = data
  else
    playerData[player.UserId] = getDefaultData()
  end

  -- Leaderstats
  local leaderstats = Instance.new("Folder")
  leaderstats.Name = "leaderstats"
  leaderstats.Parent = player

  local powerStat = Instance.new("IntValue")
  powerStat.Name = Config.CurrencyName
  powerStat.Value = playerData[player.UserId].power
  powerStat.Parent = leaderstats

  local rebirthStat = Instance.new("IntValue")
  rebirthStat.Name = "Rebirths"
  rebirthStat.Value = playerData[player.UserId].rebirths
  rebirthStat.Parent = leaderstats

  updateUIEvent:FireClient(player, playerData[player.UserId])
end

local function saveData(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  local key = "sim_" .. player.UserId
  local success, err = pcall(function()
    dataStore:SetAsync(key, data)
  end)

  if not success then
    warn("[SimulatorCore] Save failed for " .. player.Name .. ": " .. tostring(err))
  end
end

-- Click handler (rate-limited server-side)
local lastClick: { [number]: number } = {}

clickEvent.OnServerEvent:Connect(function(player: Player)
  local now = tick()
  local last = lastClick[player.UserId] or 0
  if now - last < 0.1 then return end -- 10 clicks/sec max (anti-autoclicker)
  lastClick[player.UserId] = now

  local data = playerData[player.UserId]
  if not data then return end

  local value = getClickValue(player)
  data.power += value
  updateLeaderstats(player)
end)

-- Buy tool
buyToolEvent.OnServerEvent:Connect(function(player: Player, toolIndex: number)
  if type(toolIndex) ~= "number" then return end
  toolIndex = math.floor(toolIndex)

  local data = playerData[player.UserId]
  if not data then return end

  local tool = Config.Tools[toolIndex]
  if not tool then return end

  if toolIndex <= data.toolIndex then return end -- Already owns equal or better
  if data.power < tool.cost then return end

  data.power -= tool.cost
  data.toolIndex = toolIndex
  updateLeaderstats(player)
  updateUIEvent:FireClient(player, data)
end)

-- Hatch egg (weighted random pet)
hatchEggEvent.OnServerEvent:Connect(function(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  if data.power < Config.EggCost then return end
  if #data.pets >= Config.MaxPetInventory then
    notifyEvent:FireClient(player, "Pet inventory full! Delete a pet first.")
    return
  end

  data.power -= Config.EggCost

  -- Weighted random selection
  local totalWeight = 0
  for _, pet in ipairs(Config.Pets) do
    totalWeight += pet.weight
  end

  local roll = math.random() * totalWeight
  local cumulative = 0
  local chosenPet = Config.Pets[1]

  for _, pet in ipairs(Config.Pets) do
    cumulative += pet.weight
    if roll <= cumulative then
      chosenPet = pet
      break
    end
  end

  table.insert(data.pets, {
    name = chosenPet.name,
    rarity = chosenPet.rarity,
    multiplier = chosenPet.multiplier,
  })

  updateLeaderstats(player)
  updateUIEvent:FireClient(player, data)
  notifyEvent:FireClient(player, "Hatched: " .. chosenPet.rarity .. " " .. chosenPet.name .. "!")
end)

-- Equip/unequip pet
equipPetEvent.OnServerEvent:Connect(function(player: Player, petIndex: number)
  if type(petIndex) ~= "number" then return end
  petIndex = math.floor(petIndex)

  local data = playerData[player.UserId]
  if not data then return end

  if not data.pets[petIndex] then return end

  -- Check if already equipped -> unequip
  for i, idx in ipairs(data.equippedPets) do
    if idx == petIndex then
      table.remove(data.equippedPets, i)
      updateUIEvent:FireClient(player, data)
      return
    end
  end

  -- Check max equipped slots
  local maxSlots = Config.MaxEquippedPets
  pcall(function()
    if MarketplaceService:UserOwnsGamePassAsync(player.UserId, Config.GamePassIds.ExtraPetSlots) then
      maxSlots += 3
    end
  end)

  if #data.equippedPets >= maxSlots then
    notifyEvent:FireClient(player, "Max pets equipped! Unequip one first.")
    return
  end

  table.insert(data.equippedPets, petIndex)
  updateUIEvent:FireClient(player, data)
end)

-- Rebirth
rebirthEvent.OnServerEvent:Connect(function(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  if data.power < Config.RebirthCost then return end

  data.rebirths += 1
  data.power = 0
  data.toolIndex = 1
  data.currentZone = 1
  -- Keep pets

  updateLeaderstats(player)
  updateUIEvent:FireClient(player, data)
  notifyEvent:FireClient(player, "Rebirth " .. data.rebirths .. "! Multiplier: " .. string.format("%.0f%%", getRebirthMultiplier(data.rebirths) * 100))
end)

-- Redeem code
redeemCodeEvent.OnServerEvent:Connect(function(player: Player, code: string)
  if type(code) ~= "string" then return end
  code = code:upper():gsub("%s", "")

  local data = playerData[player.UserId]
  if not data then return end

  -- Check if code exists
  local codeData = Config.Codes[code]
  if not codeData then
    notifyEvent:FireClient(player, "Invalid code.")
    return
  end

  -- Check if already redeemed
  for _, redeemed in ipairs(data.redeemedCodes) do
    if redeemed == code then
      notifyEvent:FireClient(player, "Code already redeemed.")
      return
    end
  end

  table.insert(data.redeemedCodes, code)
  data.power += codeData.currency
  updateLeaderstats(player)
  updateUIEvent:FireClient(player, data)
  notifyEvent:FireClient(player, "Code redeemed! +" .. codeData.currency .. " " .. Config.CurrencyName)
end)

-- Dev product purchases
MarketplaceService.ProcessReceipt = function(receiptInfo)
  local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
  if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end

  local data = playerData[receiptInfo.PlayerId]
  if not data then return Enum.ProductPurchaseDecision.NotProcessedYet end

  local productId = receiptInfo.ProductId

  if productId == Config.DevProductIds.Power1000 then
    data.power += 1000
  elseif productId == Config.DevProductIds.Power10000 then
    data.power += 10000
  elseif productId == Config.DevProductIds.LegendaryEgg then
    -- Guaranteed legendary or better
    local legendaryPets = {}
    for _, pet in ipairs(Config.Pets) do
      if pet.rarity == "Legendary" or pet.rarity == "Mythic" then
        table.insert(legendaryPets, pet)
      end
    end
    if #legendaryPets > 0 and #data.pets < Config.MaxPetInventory then
      local chosen = legendaryPets[math.random(1, #legendaryPets)]
      table.insert(data.pets, {
        name = chosen.name,
        rarity = chosen.rarity,
        multiplier = chosen.multiplier,
      })
      notifyEvent:FireClient(player, "Premium Egg: " .. chosen.rarity .. " " .. chosen.name .. "!")
    end
  end

  updateLeaderstats(player)
  updateUIEvent:FireClient(player, data)

  return Enum.ProductPurchaseDecision.PurchaseGranted
end

-- Player connections
Players.PlayerAdded:Connect(loadData)
Players.PlayerRemoving:Connect(function(player)
  saveData(player)
  playerData[player.UserId] = nil
  lastClick[player.UserId] = nil
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

print("[SimulatorCore] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'SimHUD',
      scriptType: 'LocalScript',
      serviceName: 'StarterGui',
      explanation:
        'Client-side UI: power display, click button, tool shop, pet display, rebirth, code input',
      newCode: `--[[
  SimHUD - Client-side simulator UI
  Shows power, click area, tool shop, pets, rebirth, codes
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("SimConfig"))
local Events = ReplicatedStorage:WaitForChild("Events")

local ClickEvent = Events:WaitForChild("Click")
local BuyTool = Events:WaitForChild("BuyTool")
local HatchEgg = Events:WaitForChild("HatchEgg")
local EquipPet = Events:WaitForChild("EquipPet")
local RebirthEvt = Events:WaitForChild("Rebirth")
local RedeemCode = Events:WaitForChild("RedeemCode")
local UpdateUI = Events:WaitForChild("UpdateUI")
local Notify = Events:WaitForChild("Notify")

local player = Players.LocalPlayer

local screenGui = Instance.new("ScreenGui")
screenGui.Name = "SimHUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = player:WaitForChild("PlayerGui")

-- Power display (top center)
local powerFrame = Instance.new("Frame")
powerFrame.Size = UDim2.new(0, 220, 0, 50)
powerFrame.Position = UDim2.new(0.5, -110, 0, 10)
powerFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
powerFrame.Parent = screenGui
Instance.new("UICorner", powerFrame).CornerRadius = UDim.new(0, 8)

local powerLabel = Instance.new("TextLabel")
powerLabel.Size = UDim2.new(1, 0, 1, 0)
powerLabel.BackgroundTransparency = 1
powerLabel.Text = "0 Power"
powerLabel.TextColor3 = Color3.fromRGB(80, 200, 255)
powerLabel.TextSize = 22
powerLabel.Font = Enum.Font.GothamBlack
powerLabel.Parent = powerFrame

-- Click button (center of screen)
local clickBtn = Instance.new("TextButton")
clickBtn.Size = UDim2.new(0, 150, 0, 150)
clickBtn.Position = UDim2.new(0.5, -75, 0.5, -75)
clickBtn.BackgroundColor3 = Color3.fromRGB(255, 100, 50)
clickBtn.Text = "TAP!"
clickBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
clickBtn.TextSize = 28
clickBtn.Font = Enum.Font.GothamBlack
clickBtn.Parent = screenGui
Instance.new("UICorner", clickBtn).CornerRadius = UDim.new(0.5, 0)

clickBtn.MouseButton1Click:Connect(function()
  ClickEvent:FireServer()
end)

-- Shop button (right side)
local shopBtn = Instance.new("TextButton")
shopBtn.Size = UDim2.new(0, 100, 0, 40)
shopBtn.Position = UDim2.new(1, -110, 0.5, -80)
shopBtn.BackgroundColor3 = Color3.fromRGB(88, 101, 242)
shopBtn.Text = "Shop"
shopBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
shopBtn.TextSize = 16
shopBtn.Font = Enum.Font.GothamBold
shopBtn.Parent = screenGui
Instance.new("UICorner", shopBtn).CornerRadius = UDim.new(0, 8)

-- Egg button
local eggBtn = Instance.new("TextButton")
eggBtn.Size = UDim2.new(0, 100, 0, 40)
eggBtn.Position = UDim2.new(1, -110, 0.5, -30)
eggBtn.BackgroundColor3 = Color3.fromRGB(200, 50, 200)
eggBtn.Text = "Hatch Egg"
eggBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
eggBtn.TextSize = 14
eggBtn.Font = Enum.Font.GothamBold
eggBtn.Parent = screenGui
Instance.new("UICorner", eggBtn).CornerRadius = UDim.new(0, 8)

eggBtn.MouseButton1Click:Connect(function()
  HatchEgg:FireServer()
end)

-- Rebirth button
local rebirthBtn = Instance.new("TextButton")
rebirthBtn.Size = UDim2.new(0, 100, 0, 40)
rebirthBtn.Position = UDim2.new(1, -110, 0.5, 20)
rebirthBtn.BackgroundColor3 = Color3.fromRGB(255, 215, 0)
rebirthBtn.Text = "Rebirth"
rebirthBtn.TextColor3 = Color3.fromRGB(30, 30, 30)
rebirthBtn.TextSize = 14
rebirthBtn.Font = Enum.Font.GothamBold
rebirthBtn.Parent = screenGui
Instance.new("UICorner", rebirthBtn).CornerRadius = UDim.new(0, 8)

rebirthBtn.MouseButton1Click:Connect(function()
  RebirthEvt:FireServer()
end)

-- Code input
local codeFrame = Instance.new("Frame")
codeFrame.Size = UDim2.new(0, 200, 0, 35)
codeFrame.Position = UDim2.new(0, 10, 1, -45)
codeFrame.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
codeFrame.Parent = screenGui
Instance.new("UICorner", codeFrame).CornerRadius = UDim.new(0, 6)

local codeInput = Instance.new("TextBox")
codeInput.Size = UDim2.new(0.65, 0, 1, 0)
codeInput.BackgroundTransparency = 1
codeInput.PlaceholderText = "Enter code..."
codeInput.Text = ""
codeInput.TextColor3 = Color3.fromRGB(200, 200, 220)
codeInput.PlaceholderColor3 = Color3.fromRGB(100, 100, 120)
codeInput.TextSize = 14
codeInput.Font = Enum.Font.Gotham
codeInput.Parent = codeFrame

local codeBtn = Instance.new("TextButton")
codeBtn.Size = UDim2.new(0.35, 0, 1, 0)
codeBtn.Position = UDim2.new(0.65, 0, 0, 0)
codeBtn.BackgroundColor3 = Color3.fromRGB(80, 200, 80)
codeBtn.Text = "Redeem"
codeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
codeBtn.TextSize = 13
codeBtn.Font = Enum.Font.GothamBold
codeBtn.Parent = codeFrame
Instance.new("UICorner", codeBtn).CornerRadius = UDim.new(0, 6)

codeBtn.MouseButton1Click:Connect(function()
  if codeInput.Text ~= "" then
    RedeemCode:FireServer(codeInput.Text)
    codeInput.Text = ""
  end
end)

-- Notification label
local notifLabel = Instance.new("TextLabel")
notifLabel.Size = UDim2.new(0, 400, 0, 40)
notifLabel.Position = UDim2.new(0.5, -200, 0, 70)
notifLabel.BackgroundTransparency = 1
notifLabel.Text = ""
notifLabel.TextColor3 = Color3.fromRGB(255, 255, 100)
notifLabel.TextSize = 16
notifLabel.Font = Enum.Font.GothamBold
notifLabel.Parent = screenGui

-- Shop frame (hidden by default)
local shopFrame = Instance.new("ScrollingFrame")
shopFrame.Size = UDim2.new(0, 280, 0, 350)
shopFrame.Position = UDim2.new(1, -290, 0.5, -230)
shopFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 35)
shopFrame.ScrollBarThickness = 4
shopFrame.Visible = false
shopFrame.Parent = screenGui
Instance.new("UICorner", shopFrame).CornerRadius = UDim.new(0, 8)

local shopLayout = Instance.new("UIListLayout")
shopLayout.SortOrder = Enum.SortOrder.LayoutOrder
shopLayout.Padding = UDim.new(0, 4)
shopLayout.Parent = shopFrame

local shopPadding = Instance.new("UIPadding")
shopPadding.PaddingAll = UDim.new(0, 8)
shopPadding.Parent = shopFrame

-- Populate tool shop
local function addShopItem(text: string, order: number, callback: () -> ())
  local btn = Instance.new("TextButton")
  btn.Size = UDim2.new(1, 0, 0, 45)
  btn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
  btn.Text = text
  btn.TextColor3 = Color3.fromRGB(200, 200, 220)
  btn.TextSize = 13
  btn.Font = Enum.Font.GothamMedium
  btn.LayoutOrder = order
  btn.Parent = shopFrame
  Instance.new("UICorner", btn).CornerRadius = UDim.new(0, 6)
  btn.MouseButton1Click:Connect(callback)
end

for i, tool in ipairs(Config.Tools) do
  addShopItem(
    tool.name .. " (" .. tool.multiplier .. "x) - " .. tool.cost .. " " .. Config.CurrencyName,
    i,
    function()
      BuyTool:FireServer(i)
    end
  )
end

shopFrame.CanvasSize = UDim2.new(0, 0, 0, shopLayout.AbsoluteContentSize.Y + 20)

shopBtn.MouseButton1Click:Connect(function()
  shopFrame.Visible = not shopFrame.Visible
end)

-- Update UI from server
UpdateUI.OnClientEvent:Connect(function(data)
  powerLabel.Text = tostring(data.power) .. " " .. Config.CurrencyName
end)

-- Notifications
Notify.OnClientEvent:Connect(function(msg: string)
  notifLabel.Text = msg
  task.delay(3, function()
    if notifLabel.Text == msg then
      notifLabel.Text = ""
    end
  end)
end)

-- Initial state
task.spawn(function()
  local leaderstats = player:WaitForChild("leaderstats", 10)
  if leaderstats then
    local stat = leaderstats:WaitForChild(Config.CurrencyName, 5)
    if stat then
      powerLabel.Text = tostring(stat.Value) .. " " .. Config.CurrencyName
      stat.Changed:Connect(function(val)
        powerLabel.Text = tostring(val) .. " " .. Config.CurrencyName
      end)
    end
  end
end)

print("[SimHUD] Loaded")`,
    },
  ],
};
