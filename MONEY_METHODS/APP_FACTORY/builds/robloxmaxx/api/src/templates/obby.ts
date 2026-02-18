export const OBBY_TEMPLATE = {
  name: 'Complete Obby',
  genre: 'obby',
  description:
    'A full obstacle course game with checkpoints, kill bricks, moving platforms, timer, stage skip gamepass, and data persistence.',
  scripts: [
    {
      action: 'CreateFolder' as const,
      folderName: 'Events',
      serviceName: 'ReplicatedStorage',
      explanation: 'Folder for RemoteEvents and RemoteFunctions',
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'ObbyConfig',
      scriptType: 'ModuleScript',
      serviceName: 'ReplicatedStorage',
      explanation: 'Shared configuration for stage definitions, rewards, and gamepass IDs',
      newCode: `--[[
  ObbyConfig - Shared obby game configuration
  Modify these values to balance difficulty and rewards
]]

local ObbyConfig = {}

ObbyConfig.TotalStages = 30

-- Rewards
ObbyConfig.CoinsPerStage = 10
ObbyConfig.CompletionBonus = 500
ObbyConfig.CurrencyName = "Coins"

-- Gamepasses (replace 0 with real IDs)
ObbyConfig.GamePassIds = {
  SkipStage = 0,
  SpeedBoost = 0,
  DoubleCoins = 0,
  VIP = 0,
}

-- Dev Products (replace 0 with real IDs)
ObbyConfig.DevProductIds = {
  Skip1Stage = 0,
  Skip5Stages = 0,
  Coins500 = 0,
}

-- Difficulty tiers
ObbyConfig.Tiers = {
  { name = "Easy", stages = {1, 10}, color = Color3.fromRGB(80, 255, 80) },
  { name = "Medium", stages = {11, 20}, color = Color3.fromRGB(255, 200, 50) },
  { name = "Hard", stages = {21, 25}, color = Color3.fromRGB(255, 100, 50) },
  { name = "Extreme", stages = {26, 30}, color = Color3.fromRGB(255, 50, 50) },
}

-- Speed boost multiplier (for gamepass holders)
ObbyConfig.SpeedBoostMultiplier = 1.4

return ObbyConfig`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'ObbyManager',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Server-side obby logic: stage progression, data persistence, rewards, skip stage, leaderboard',
      newCode: `--[[
  ObbyManager - Server-side obby game logic
  Handles: stage tracking, checkpoints, data saving, rewards, gamepasses
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local Config = require(ReplicatedStorage:WaitForChild("ObbyConfig"))

-- DataStore
local dataStore = DataStoreService:GetDataStore("ObbyData_v2")

-- RemoteEvents
local Events = ReplicatedStorage:WaitForChild("Events")

local stageReachedEvent = Instance.new("RemoteEvent")
stageReachedEvent.Name = "StageReached"
stageReachedEvent.Parent = Events

local updateUIEvent = Instance.new("RemoteEvent")
updateUIEvent.Name = "UpdateUI"
updateUIEvent.Parent = Events

local skipStageEvent = Instance.new("RemoteEvent")
skipStageEvent.Name = "SkipStage"
skipStageEvent.Parent = Events

local timerUpdateEvent = Instance.new("RemoteEvent")
timerUpdateEvent.Name = "TimerUpdate"
timerUpdateEvent.Parent = Events

-- Player data cache
local playerData: { [number]: { stage: number, coins: number, bestTime: number?, completions: number } } = {}

local playerTimers: { [number]: number } = {}

local function getDefaultData()
  return {
    stage = 1,
    coins = 0,
    bestTime = nil,
    completions = 0,
  }
end

local function loadData(player: Player)
  local key = "obby_" .. player.UserId
  local success, data = pcall(function()
    return dataStore:GetAsync(key)
  end)

  if success and data then
    playerData[player.UserId] = data
  else
    playerData[player.UserId] = getDefaultData()
  end

  -- Start timer
  playerTimers[player.UserId] = tick()

  -- Leaderstats
  local leaderstats = Instance.new("Folder")
  leaderstats.Name = "leaderstats"
  leaderstats.Parent = player

  local stageStat = Instance.new("IntValue")
  stageStat.Name = "Stage"
  stageStat.Value = playerData[player.UserId].stage
  stageStat.Parent = leaderstats

  local coinsStat = Instance.new("IntValue")
  coinsStat.Name = Config.CurrencyName
  coinsStat.Value = playerData[player.UserId].coins
  coinsStat.Parent = leaderstats

  -- Send initial UI data
  updateUIEvent:FireClient(player, playerData[player.UserId])
end

local function saveData(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  local key = "obby_" .. player.UserId
  local success, err = pcall(function()
    dataStore:SetAsync(key, data)
  end)

  if not success then
    warn("[ObbyManager] Failed to save for " .. player.Name .. ": " .. tostring(err))
  end
end

local function addCoins(player: Player, amount: number)
  local data = playerData[player.UserId]
  if not data then return end

  -- Check double coins gamepass
  local hasDouble = false
  pcall(function()
    hasDouble = MarketplaceService:UserOwnsGamePassAsync(player.UserId, Config.GamePassIds.DoubleCoins)
  end)

  local finalAmount = if hasDouble then amount * 2 else amount
  data.coins += finalAmount

  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local coinsStat = leaderstats:FindFirstChild(Config.CurrencyName)
    if coinsStat then coinsStat.Value = data.coins end
  end
end

local function advanceStage(player: Player, newStage: number)
  local data = playerData[player.UserId]
  if not data then return end

  if newStage <= data.stage then return end
  if newStage > Config.TotalStages + 1 then return end

  data.stage = math.min(newStage, Config.TotalStages + 1)

  -- Reward coins
  addCoins(player, Config.CoinsPerStage)

  -- Check completion
  if data.stage > Config.TotalStages then
    data.completions += 1
    addCoins(player, Config.CompletionBonus)

    -- Record best time
    local startTime = playerTimers[player.UserId]
    if startTime then
      local elapsed = tick() - startTime
      if not data.bestTime or elapsed < data.bestTime then
        data.bestTime = elapsed
      end
    end
  end

  -- Update leaderstats
  local leaderstats = player:FindFirstChild("leaderstats")
  if leaderstats then
    local stageStat = leaderstats:FindFirstChild("Stage")
    if stageStat then stageStat.Value = data.stage end
  end

  -- Notify client
  updateUIEvent:FireClient(player, data)
end

-- Stage reached from client (checkpoint touched)
stageReachedEvent.OnServerEvent:Connect(function(player: Player, stageNum: number)
  if type(stageNum) ~= "number" then return end
  stageNum = math.floor(stageNum)

  local data = playerData[player.UserId]
  if not data then return end

  -- Only allow advancing one stage at a time (anti-cheat)
  if stageNum == data.stage + 1 then
    advanceStage(player, stageNum)
  end
end)

-- Skip stage (dev product or gamepass)
skipStageEvent.OnServerEvent:Connect(function(player: Player)
  local data = playerData[player.UserId]
  if not data then return end

  if data.stage > Config.TotalStages then return end

  -- Check if they own skip gamepass (unlimited skips)
  local hasSkipPass = false
  pcall(function()
    hasSkipPass = MarketplaceService:UserOwnsGamePassAsync(player.UserId, Config.GamePassIds.SkipStage)
  end)

  if hasSkipPass then
    advanceStage(player, data.stage + 1)
  else
    -- Prompt dev product purchase for single skip
    pcall(function()
      MarketplaceService:PromptProductPurchase(player, Config.DevProductIds.Skip1Stage)
    end)
  end
end)

-- Handle dev product purchases
MarketplaceService.ProcessReceipt = function(receiptInfo)
  local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
  if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end

  local data = playerData[receiptInfo.PlayerId]
  if not data then return Enum.ProductPurchaseDecision.NotProcessedYet end

  local productId = receiptInfo.ProductId

  if productId == Config.DevProductIds.Skip1Stage then
    advanceStage(player, data.stage + 1)
  elseif productId == Config.DevProductIds.Skip5Stages then
    advanceStage(player, math.min(data.stage + 5, Config.TotalStages + 1))
  elseif productId == Config.DevProductIds.Coins500 then
    addCoins(player, 500)
    updateUIEvent:FireClient(player, data)
  end

  return Enum.ProductPurchaseDecision.PurchaseGranted
end

-- Player connections
Players.PlayerAdded:Connect(loadData)
Players.PlayerRemoving:Connect(function(player)
  saveData(player)
  playerData[player.UserId] = nil
  playerTimers[player.UserId] = nil
end)

-- Save all on shutdown
game:BindToClose(function()
  for _, player in ipairs(Players:GetPlayers()) do
    saveData(player)
  end
end)

-- Timer broadcast (every second)
task.spawn(function()
  while true do
    task.wait(1)
    for _, player in ipairs(Players:GetPlayers()) do
      local startTime = playerTimers[player.UserId]
      if startTime then
        timerUpdateEvent:FireClient(player, tick() - startTime)
      end
    end
  end
end)

-- Auto-save every 60 seconds
task.spawn(function()
  while true do
    task.wait(60)
    for _, player in ipairs(Players:GetPlayers()) do
      saveData(player)
    end
  end
end)

print("[ObbyManager] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'ObbyHUD',
      scriptType: 'LocalScript',
      serviceName: 'StarterGui',
      explanation:
        'Client-side UI: stage counter, timer display, coins, skip button, difficulty indicator',
      newCode: `--[[
  ObbyHUD - Client-side obby UI
  Shows current stage, timer, coins, and skip stage button
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local Config = require(ReplicatedStorage:WaitForChild("ObbyConfig"))
local Events = ReplicatedStorage:WaitForChild("Events")
local UpdateUI = Events:WaitForChild("UpdateUI")
local SkipStage = Events:WaitForChild("SkipStage")
local TimerUpdate = Events:WaitForChild("TimerUpdate")

local player = Players.LocalPlayer

-- Create ScreenGui
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "ObbyHUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = player:WaitForChild("PlayerGui")

-- Top bar container
local topBar = Instance.new("Frame")
topBar.Size = UDim2.new(1, 0, 0, 60)
topBar.Position = UDim2.new(0, 0, 0, 0)
topBar.BackgroundColor3 = Color3.fromRGB(20, 20, 30)
topBar.BackgroundTransparency = 0.3
topBar.BorderSizePixel = 0
topBar.Parent = screenGui

-- Stage display
local stageLabel = Instance.new("TextLabel")
stageLabel.Size = UDim2.new(0, 200, 1, 0)
stageLabel.Position = UDim2.new(0.5, -100, 0, 0)
stageLabel.BackgroundTransparency = 1
stageLabel.Text = "Stage 1 / " .. Config.TotalStages
stageLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
stageLabel.TextSize = 22
stageLabel.Font = Enum.Font.GothamBlack
stageLabel.Parent = topBar

-- Difficulty label
local diffLabel = Instance.new("TextLabel")
diffLabel.Size = UDim2.new(0, 100, 0, 20)
diffLabel.Position = UDim2.new(0.5, -50, 0, 40)
diffLabel.BackgroundTransparency = 1
diffLabel.Text = "Easy"
diffLabel.TextColor3 = Color3.fromRGB(80, 255, 80)
diffLabel.TextSize = 14
diffLabel.Font = Enum.Font.GothamBold
diffLabel.Parent = screenGui

-- Timer display
local timerLabel = Instance.new("TextLabel")
timerLabel.Size = UDim2.new(0, 150, 1, 0)
timerLabel.Position = UDim2.new(0, 10, 0, 0)
timerLabel.BackgroundTransparency = 1
timerLabel.Text = "0:00"
timerLabel.TextColor3 = Color3.fromRGB(200, 200, 255)
timerLabel.TextSize = 18
timerLabel.Font = Enum.Font.GothamBold
timerLabel.TextXAlignment = Enum.TextXAlignment.Left
timerLabel.Parent = topBar

-- Coins display
local coinsLabel = Instance.new("TextLabel")
coinsLabel.Size = UDim2.new(0, 150, 1, 0)
coinsLabel.Position = UDim2.new(1, -160, 0, 0)
coinsLabel.BackgroundTransparency = 1
coinsLabel.Text = "0 Coins"
coinsLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
coinsLabel.TextSize = 18
coinsLabel.Font = Enum.Font.GothamBold
coinsLabel.TextXAlignment = Enum.TextXAlignment.Right
coinsLabel.Parent = topBar

-- Skip stage button
local skipBtn = Instance.new("TextButton")
skipBtn.Size = UDim2.new(0, 120, 0, 40)
skipBtn.Position = UDim2.new(1, -130, 0, 70)
skipBtn.BackgroundColor3 = Color3.fromRGB(88, 101, 242)
skipBtn.Text = "Skip Stage"
skipBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
skipBtn.TextSize = 14
skipBtn.Font = Enum.Font.GothamBold
skipBtn.Parent = screenGui
Instance.new("UICorner", skipBtn).CornerRadius = UDim.new(0, 8)

skipBtn.MouseButton1Click:Connect(function()
  SkipStage:FireServer()
end)

-- Get difficulty tier for stage
local function getDifficultyTier(stage: number)
  for _, tier in ipairs(Config.Tiers) do
    if stage >= tier.stages[1] and stage <= tier.stages[2] then
      return tier
    end
  end
  return Config.Tiers[#Config.Tiers]
end

-- Update UI from server data
UpdateUI.OnClientEvent:Connect(function(data)
  local stage = data.stage
  local coins = data.coins

  if stage > Config.TotalStages then
    stageLabel.Text = "COMPLETED!"
    diffLabel.Text = "Winner!"
    diffLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
  else
    stageLabel.Text = "Stage " .. stage .. " / " .. Config.TotalStages

    local tier = getDifficultyTier(stage)
    diffLabel.Text = tier.name
    diffLabel.TextColor3 = tier.color
  end

  coinsLabel.Text = tostring(coins) .. " " .. Config.CurrencyName
end)

-- Timer updates
TimerUpdate.OnClientEvent:Connect(function(elapsed: number)
  local minutes = math.floor(elapsed / 60)
  local seconds = math.floor(elapsed % 60)
  timerLabel.Text = string.format("%d:%02d", minutes, seconds)
end)

-- Initial state from leaderstats
task.spawn(function()
  local leaderstats = player:WaitForChild("leaderstats", 10)
  if leaderstats then
    local stageStat = leaderstats:WaitForChild("Stage", 5)
    if stageStat then
      stageLabel.Text = "Stage " .. stageStat.Value .. " / " .. Config.TotalStages
    end
    local coinsStat = leaderstats:WaitForChild(Config.CurrencyName, 5)
    if coinsStat then
      coinsLabel.Text = tostring(coinsStat.Value) .. " " .. Config.CurrencyName
    end
  end
end)

print("[ObbyHUD] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'CheckpointHandler',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Manages checkpoint parts: detect player touch, set spawn point, fire stage progression. Place parts named "Checkpoint_1", "Checkpoint_2", etc. in Workspace.',
      newCode: `--[[
  CheckpointHandler - Checkpoint touch detection and spawn management
  Place parts named "Checkpoint_N" in Workspace (N = stage number)
  Players touching a checkpoint get their spawn set there
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Events = ReplicatedStorage:WaitForChild("Events")
local StageReached = Events:WaitForChild("StageReached")

local function setupCheckpoint(part: BasePart, stageNum: number)
  part.Touched:Connect(function(hit)
    local character = hit.Parent
    if not character then return end
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end
    local player = Players:GetPlayerFromCharacter(character)
    if not player then return end

    -- Set spawn location to this checkpoint
    player.RespawnLocation = nil -- Clear forced spawn

    -- Notify server of stage reached
    -- Server validates this is actually stage+1
    StageReached:FireClient(player, stageNum)
  end)
end

-- Scan workspace for checkpoint parts
local function findCheckpoints()
  for _, obj in ipairs(game.Workspace:GetDescendants()) do
    if obj:IsA("BasePart") and obj.Name:match("^Checkpoint_(%d+)$") then
      local num = tonumber(obj.Name:match("(%d+)$"))
      if num then
        setupCheckpoint(obj, num)
        -- Visual indicator
        obj.BrickColor = BrickColor.new("Lime green")
        obj.Material = Enum.Material.Neon
        obj.Transparency = 0.3
      end
    end
  end
end

findCheckpoints()

-- Also listen for new checkpoints added at runtime
game.Workspace.DescendantAdded:Connect(function(obj)
  if obj:IsA("BasePart") and obj.Name:match("^Checkpoint_(%d+)$") then
    local num = tonumber(obj.Name:match("(%d+)$"))
    if num then
      setupCheckpoint(obj, num)
    end
  end
end)

print("[CheckpointHandler] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'KillBrickHandler',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Handles kill bricks. Any part named "KillBrick" or tagged "KillBrick" kills the player on touch.',
      newCode: `--[[
  KillBrickHandler - Kill brick touch detection
  Name any part "KillBrick" or add the tag "KillBrick" to make it lethal
]]

local Players = game:GetService("Players")
local CollectionService = game:GetService("CollectionService")

local KILL_DEBOUNCE: { [number]: boolean } = {}

local function setupKillBrick(part: BasePart)
  part.Touched:Connect(function(hit)
    local character = hit.Parent
    if not character then return end
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid or humanoid.Health <= 0 then return end
    local player = Players:GetPlayerFromCharacter(character)
    if not player then return end

    if KILL_DEBOUNCE[player.UserId] then return end
    KILL_DEBOUNCE[player.UserId] = true

    humanoid.Health = 0

    task.delay(1, function()
      KILL_DEBOUNCE[player.UserId] = nil
    end)
  end)

  -- Visual
  part.BrickColor = BrickColor.new("Really red")
  part.Material = Enum.Material.Neon
end

-- Scan for KillBrick parts by name
for _, obj in ipairs(game.Workspace:GetDescendants()) do
  if obj:IsA("BasePart") and obj.Name == "KillBrick" then
    setupKillBrick(obj)
  end
end

-- Scan for tagged KillBrick parts
for _, obj in ipairs(CollectionService:GetTagged("KillBrick")) do
  if obj:IsA("BasePart") then
    setupKillBrick(obj)
  end
end

-- Listen for new parts
game.Workspace.DescendantAdded:Connect(function(obj)
  if obj:IsA("BasePart") and obj.Name == "KillBrick" then
    setupKillBrick(obj)
  end
end)

CollectionService:GetInstanceAddedSignal("KillBrick"):Connect(function(obj)
  if obj:IsA("BasePart") then
    setupKillBrick(obj)
  end
end)

print("[KillBrickHandler] Loaded")`,
    },
  ],
};
