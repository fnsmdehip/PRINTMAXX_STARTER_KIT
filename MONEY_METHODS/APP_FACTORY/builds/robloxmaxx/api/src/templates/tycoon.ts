// Pre-built tycoon game template
// Users can start from this instead of blank canvas

export const TYCOON_TEMPLATE = {
  name: 'Basic Tycoon',
  genre: 'tycoon',
  description: 'A complete tycoon game with droppers, collectors, upgrades, and rebirth system.',
  scripts: [
    {
      action: 'CreateFolder' as const,
      folderName: 'Events',
      serviceName: 'ReplicatedStorage',
      explanation: 'Folder for RemoteEvents and RemoteFunctions',
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'TycoonConfig',
      scriptType: 'ModuleScript',
      serviceName: 'ReplicatedStorage',
      explanation: 'Shared configuration for tycoon game balancing',
      newCode: `--[[
  TycoonConfig - Shared game configuration
  Modify these values to balance your tycoon game
]]

local TycoonConfig = {}

-- Currency
TycoonConfig.StartingCash = 0
TycoonConfig.CurrencyName = "Cash"

-- Droppers
TycoonConfig.Droppers = {
  { name = "Basic Dropper", cost = 0, value = 1, rate = 2 },
  { name = "Advanced Dropper", cost = 500, value = 5, rate = 1.5 },
  { name = "Premium Dropper", cost = 5000, value = 25, rate = 1 },
  { name = "Ultimate Dropper", cost = 50000, value = 150, rate = 0.8 },
}

-- Upgrades
TycoonConfig.Upgrades = {
  { name = "Speed Boost", cost = 1000, multiplier = 1.5, description = "Droppers 50% faster" },
  { name = "Value Boost", cost = 2500, multiplier = 2, description = "Drops worth 2x" },
  { name = "Auto Collect", cost = 10000, multiplier = 1, description = "Auto-collect drops" },
  { name = "Mega Boost", cost = 50000, multiplier = 3, description = "Everything 3x" },
}

-- Rebirth
TycoonConfig.RebirthCost = 100000
TycoonConfig.RebirthMultiplier = 1.5 -- Each rebirth multiplies earnings by this

-- Monetization
TycoonConfig.GamePassIds = {
  VIP = 0, -- Replace with real gamepass ID
  AutoCollect = 0,
  x2Cash = 0,
}

TycoonConfig.DevProductIds = {
  Cash1000 = 0, -- Replace with real product ID
  Cash10000 = 0,
  InstantRebirth = 0,
}

return TycoonConfig`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'TycoonManager',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation: 'Main server-side tycoon logic: plot claiming, purchases, data persistence',
      newCode: `--[[
  TycoonManager - Server-side tycoon game logic
  Handles: plot claiming, dropper purchases, upgrades, rebirth, data saving
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local Config = require(ReplicatedStorage:WaitForChild("TycoonConfig"))

-- DataStore
local dataStore = DataStoreService:GetDataStore("TycoonData_v1")

-- RemoteEvents
local Events = ReplicatedStorage:WaitForChild("Events")
local purchaseDropperEvent = Instance.new("RemoteEvent")
purchaseDropperEvent.Name = "PurchaseDropper"
purchaseDropperEvent.Parent = Events

local purchaseUpgradeEvent = Instance.new("RemoteEvent")
purchaseUpgradeEvent.Name = "PurchaseUpgrade"
purchaseUpgradeEvent.Parent = Events

local rebirthEvent = Instance.new("RemoteEvent")
rebirthEvent.Name = "Rebirth"
rebirthEvent.Parent = Events

local updateCashEvent = Instance.new("RemoteEvent")
updateCashEvent.Name = "UpdateCash"
updateCashEvent.Parent = Events

-- Player data cache
local playerData: { [number]: { cash: number, rebirths: number, droppers: {string}, upgrades: {string} } } = {}

local function getDefaultData()
  return {
    cash = Config.StartingCash,
    rebirths = 0,
    droppers = {},
    upgrades = {},
  }
end

local function loadData(player: Player)
  local key = "player_" .. player.UserId
  local success, data = pcall(function()
    return dataStore:GetAsync(key)
  end)

  if success and data then
    playerData[player.UserId] = data
  else
    playerData[player.UserId] = getDefaultData()
  end

  -- Create leaderstats
  local leaderstats = Instance.new("Folder")
  leaderstats.Name = "leaderstats"
  leaderstats.Parent = player

  local cashStat = Instance.new("IntValue")
  cashStat.Name = Config.CurrencyName
  cashStat.Value = playerData[player.UserId].cash
  cashStat.Parent = leaderstats

  local rebirthStat = Instance.new("IntValue")
  rebirthStat.Name = "Rebirths"
  rebirthStat.Value = playerData[player.UserId].rebirths
  rebirthStat.Parent = leaderstats
end

local function saveData(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  local key = "player_" .. player.UserId
  local success, err = pcall(function()
    dataStore:SetAsync(key, data)
  end)

  if not success then
    warn("[TycoonManager] Failed to save data for " .. player.Name .. ": " .. tostring(err))
  end
end

local function getMultiplier(player: Player): number
  local data = playerData[player.UserId]
  if not data then return 1 end
  return Config.RebirthMultiplier ^ data.rebirths
end

local function addCash(player: Player, amount: number)
  local data = playerData[player.UserId]
  if not data then return end

  local multiplied = math.floor(amount * getMultiplier(player))
  data.cash += multiplied

  -- Update leaderstats
  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local cashStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if cashStat then
      cashStat.Value = data.cash
    end
  end

  -- Notify client
  updateCashEvent:FireClient(player, data.cash)
end

-- Purchase dropper
purchaseDropperEvent.OnServerEvent:Connect(function(player: Player, dropperIndex: number)
  local data = playerData[player.UserId]
  if not data then return end

  if type(dropperIndex) ~= "number" then return end
  dropperIndex = math.floor(dropperIndex)

  local dropper = Config.Droppers[dropperIndex]
  if not dropper then return end

  if data.cash < dropper.cost then return end

  -- Check if already owned
  for _, owned in ipairs(data.droppers) do
    if owned == dropper.name then return end
  end

  data.cash -= dropper.cost
  table.insert(data.droppers, dropper.name)

  -- Update leaderstats
  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local cashStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if cashStat then cashStat.Value = data.cash end
  end

  updateCashEvent:FireClient(player, data.cash)
end)

-- Purchase upgrade
purchaseUpgradeEvent.OnServerEvent:Connect(function(player: Player, upgradeIndex: number)
  local data = playerData[player.UserId]
  if not data then return end

  if type(upgradeIndex) ~= "number" then return end
  upgradeIndex = math.floor(upgradeIndex)

  local upgrade = Config.Upgrades[upgradeIndex]
  if not upgrade then return end

  if data.cash < upgrade.cost then return end

  for _, owned in ipairs(data.upgrades) do
    if owned == upgrade.name then return end
  end

  data.cash -= upgrade.cost
  table.insert(data.upgrades, upgrade.name)

  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local cashStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if cashStat then cashStat.Value = data.cash end
  end

  updateCashEvent:FireClient(player, data.cash)
end)

-- Rebirth
rebirthEvent.OnServerEvent:Connect(function(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  if data.cash < Config.RebirthCost then return end

  data.rebirths += 1
  data.cash = 0
  data.droppers = {}
  data.upgrades = {}

  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local cashStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if cashStat then cashStat.Value = 0 end
    local rebirthStat = leaderstats:FindFirstChild("Rebirths")
    if rebirthStat then rebirthStat.Value = data.rebirths end
  end

  updateCashEvent:FireClient(player, 0)
end)

-- Dropper income loop
task.spawn(function()
  while true do
    task.wait(1)
    for _, player in ipairs(Players:GetPlayers()) do
      local data = playerData[player.UserId]
      if data then
        for _, dropperName in ipairs(data.droppers) do
          for _, dropper in ipairs(Config.Droppers) do
            if dropper.name == dropperName then
              addCash(player, dropper.value)
              break
            end
          end
        end
      end
    end
  end
end)

-- Player connections
Players.PlayerAdded:Connect(loadData)
Players.PlayerRemoving:Connect(function(player)
  saveData(player)
  playerData[player.UserId] = nil
end)

-- Save all on shutdown
game:BindToClose(function()
  for _, player in ipairs(Players:GetPlayers()) do
    saveData(player)
  end
end)

print("[TycoonManager] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'TycoonHUD',
      scriptType: 'LocalScript',
      serviceName: 'StarterGui',
      explanation: 'Client-side UI for cash display, shop, and rebirth button',
      newCode: `--[[
  TycoonHUD - Client-side tycoon UI
  Shows cash, dropper shop, upgrade shop, rebirth button
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("TycoonConfig"))
local Events = ReplicatedStorage:WaitForChild("Events")
local UpdateCash = Events:WaitForChild("UpdateCash")
local PurchaseDropper = Events:WaitForChild("PurchaseDropper")
local PurchaseUpgrade = Events:WaitForChild("PurchaseUpgrade")
local Rebirth = Events:WaitForChild("Rebirth")

local player = Players.LocalPlayer

-- Create ScreenGui
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "TycoonHUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = player:WaitForChild("PlayerGui")

-- Cash display
local cashFrame = Instance.new("Frame")
cashFrame.Size = UDim2.new(0, 200, 0, 50)
cashFrame.Position = UDim2.new(0.5, -100, 0, 10)
cashFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
cashFrame.Parent = screenGui
Instance.new("UICorner", cashFrame).CornerRadius = UDim.new(0, 8)

local cashLabel = Instance.new("TextLabel")
cashLabel.Size = UDim2.new(1, 0, 1, 0)
cashLabel.BackgroundTransparency = 1
cashLabel.Text = "$0"
cashLabel.TextColor3 = Color3.fromRGB(80, 255, 80)
cashLabel.TextSize = 24
cashLabel.Font = Enum.Font.GothamBlack
cashLabel.Parent = cashFrame

-- Shop toggle button
local shopToggle = Instance.new("TextButton")
shopToggle.Size = UDim2.new(0, 100, 0, 40)
shopToggle.Position = UDim2.new(1, -110, 0.5, -20)
shopToggle.BackgroundColor3 = Color3.fromRGB(88, 101, 242)
shopToggle.Text = "Shop"
shopToggle.TextColor3 = Color3.fromRGB(255, 255, 255)
shopToggle.TextSize = 16
shopToggle.Font = Enum.Font.GothamBold
shopToggle.Parent = screenGui
Instance.new("UICorner", shopToggle).CornerRadius = UDim.new(0, 8)

-- Shop frame
local shopFrame = Instance.new("ScrollingFrame")
shopFrame.Size = UDim2.new(0, 300, 0, 400)
shopFrame.Position = UDim2.new(1, -310, 0.5, -200)
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
shopPadding.PaddingTop = UDim.new(0, 8)
shopPadding.PaddingLeft = UDim.new(0, 8)
shopPadding.PaddingRight = UDim.new(0, 8)
shopPadding.Parent = shopFrame

-- Section header helper
local function addHeader(text: string, order: number)
  local label = Instance.new("TextLabel")
  label.Size = UDim2.new(1, 0, 0, 30)
  label.BackgroundTransparency = 1
  label.Text = text
  label.TextColor3 = Color3.fromRGB(88, 101, 242)
  label.TextSize = 16
  label.Font = Enum.Font.GothamBold
  label.TextXAlignment = Enum.TextXAlignment.Left
  label.LayoutOrder = order
  label.Parent = shopFrame
end

-- Shop button helper
local function addShopButton(text: string, cost: number, order: number, callback: () -> ())
  local btn = Instance.new("TextButton")
  btn.Size = UDim2.new(1, 0, 0, 50)
  btn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
  btn.Text = text .. "  -  $" .. tostring(cost)
  btn.TextColor3 = Color3.fromRGB(200, 200, 220)
  btn.TextSize = 13
  btn.Font = Enum.Font.GothamMedium
  btn.LayoutOrder = order
  btn.Parent = shopFrame
  Instance.new("UICorner", btn).CornerRadius = UDim.new(0, 6)
  btn.MouseButton1Click:Connect(callback)
end

-- Populate shop
addHeader("DROPPERS", 0)
for i, dropper in ipairs(Config.Droppers) do
  addShopButton(dropper.name, dropper.cost, i, function()
    PurchaseDropper:FireServer(i)
  end)
end

addHeader("UPGRADES", 100)
for i, upgrade in ipairs(Config.Upgrades) do
  addShopButton(upgrade.name .. " (" .. upgrade.description .. ")", upgrade.cost, 100 + i, function()
    PurchaseUpgrade:FireServer(i)
  end)
end

addHeader("REBIRTH", 200)
addShopButton("REBIRTH (Reset for " .. Config.RebirthMultiplier .. "x multiplier)", Config.RebirthCost, 201, function()
  Rebirth:FireServer()
end)

shopFrame.CanvasSize = UDim2.new(0, 0, 0, shopLayout.AbsoluteContentSize.Y + 20)

-- Toggle shop
shopToggle.MouseButton1Click:Connect(function()
  shopFrame.Visible = not shopFrame.Visible
end)

-- Update cash display
UpdateCash.OnClientEvent:Connect(function(cash: number)
  cashLabel.Text = "$" .. tostring(cash)
end)

-- Initial cash from leaderstats
task.spawn(function()
  local leaderstats = player:WaitForChild("leaderstats", 10)
  if leaderstats then
    local cashStat = leaderstats:WaitForChild(Config.CurrencyName, 5)
    if cashStat then
      cashLabel.Text = "$" .. tostring(cashStat.Value)
      cashStat.Changed:Connect(function(val)
        cashLabel.Text = "$" .. tostring(val)
      end)
    end
  end
end)

print("[TycoonHUD] Loaded")`,
    },
  ],
};
