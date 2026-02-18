export const HORROR_TEMPLATE = {
  name: 'Core Horror Systems',
  genre: 'horror',
  description:
    'Core horror game systems: monster AI with pathfinding, flashlight with battery, atmosphere setup, stamina, door/key system, and data persistence.',
  scripts: [
    {
      action: 'CreateFolder' as const,
      folderName: 'Events',
      serviceName: 'ReplicatedStorage',
      explanation: 'Folder for RemoteEvents and RemoteFunctions',
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'HorrorConfig',
      scriptType: 'ModuleScript',
      serviceName: 'ReplicatedStorage',
      explanation: 'Shared horror game configuration: monster stats, flashlight, doors, stamina',
      newCode: `--[[
  HorrorConfig - Shared horror game configuration
  Monster behavior, flashlight, stamina, items, doors
]]

local HorrorConfig = {}

-- Monster
HorrorConfig.Monster = {
  PatrolSpeed = 10,
  ChaseSpeed = 22,
  SearchSpeed = 14,
  DetectionRadius = 40,  -- studs
  LosePlayerRadius = 60, -- studs to lose chase
  SearchDuration = 8,    -- seconds before returning to patrol
  AttackRange = 6,       -- studs
  AttackDamage = 100,    -- instant kill by default
  AttackCooldown = 2,
}

-- Flashlight
HorrorConfig.Flashlight = {
  MaxBattery = 100,
  DrainRate = 2,       -- per second when on
  RechargeRate = 0.5,  -- per second when off
  SpotlightRange = 50,
  SpotlightAngle = 40,
  SpotlightBrightness = 2,
}

-- Stamina
HorrorConfig.Stamina = {
  Max = 100,
  SprintDrain = 15,    -- per second
  RecoveryRate = 8,    -- per second when walking
  SprintSpeed = 24,
  WalkSpeed = 16,
  ExhaustedSpeed = 10, -- speed when stamina hits 0
  ExhaustedDuration = 3,
}

-- Atmosphere
HorrorConfig.Atmosphere = {
  Ambient = Color3.fromRGB(10, 10, 15),
  OutdoorAmbient = Color3.fromRGB(10, 10, 15),
  FogColor = Color3.fromRGB(5, 5, 10),
  FogStart = 0,
  FogEnd = 80,
  Brightness = 0,
  ClockTime = 0, -- midnight
}

-- Collectible items (keys, notes, etc.)
HorrorConfig.Items = {
  { id = "key_basement", name = "Basement Key", description = "Opens the basement door" },
  { id = "key_exit", name = "Exit Key", description = "Opens the exit" },
  { id = "note_1", name = "Torn Note", description = "A hastily written note..." },
  { id = "note_2", name = "Lab Report", description = "Subject exhibited unusual behavior..." },
  { id = "battery", name = "Battery Pack", description = "Restores flashlight battery" },
}

-- Doors (door name -> required key)
HorrorConfig.Doors = {
  BasementDoor = "key_basement",
  ExitDoor = "key_exit",
}

-- Gamepasses (replace 0 with real IDs)
HorrorConfig.GamePassIds = {
  FlashlightUpgrade = 0,  -- 2x battery life
  SpeedBoost = 0,         -- +10% sprint speed
  MonsterRadar = 0,       -- See monster on minimap
}

return HorrorConfig`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'MonsterAI',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Server-side monster AI: patrol/chase/search state machine with PathfindingService, attack on proximity',
      newCode: `--[[
  MonsterAI - Server-side monster behavior
  States: PATROL -> CHASE -> SEARCH -> PATROL
  Uses PathfindingService for navigation
  Place a Model named "Monster" with a Humanoid and HumanoidRootPart in Workspace
]]

local Players = game:GetService("Players")
local PathfindingService = game:GetService("PathfindingService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("HorrorConfig"))

-- Find monster model in workspace
local monster = game.Workspace:WaitForChild("Monster", 30)
if not monster then
  warn("[MonsterAI] No Monster model found in Workspace")
  return
end

local humanoid = monster:WaitForChild("Humanoid")
local rootPart = monster:WaitForChild("HumanoidRootPart")

-- Events
local Events = ReplicatedStorage:WaitForChild("Events")
local monsterStateEvent = Instance.new("RemoteEvent")
monsterStateEvent.Name = "MonsterState"
monsterStateEvent.Parent = Events

-- State machine
local state = "PATROL" -- PATROL | CHASE | SEARCH
local targetPlayer: Player? = nil
local searchStartTime = 0
local lastAttackTime = 0

-- Patrol waypoints (place parts named "Waypoint_N" in Workspace)
local waypoints: {BasePart} = {}
for _, obj in ipairs(game.Workspace:GetDescendants()) do
  if obj:IsA("BasePart") and obj.Name:match("^Waypoint_%d+$") then
    table.insert(waypoints, obj)
    obj.Transparency = 1 -- Hide waypoints
  end
end
local currentWaypoint = 1

local function getNearestPlayer(): (Player?, number)
  local nearest: Player? = nil
  local nearestDist = math.huge

  for _, p in ipairs(Players:GetPlayers()) do
    local char = p.Character
    if char then
      local hrp = char:FindFirstChild("HumanoidRootPart")
      local hum = char:FindFirstChildOfClass("Humanoid")
      if hrp and hum and hum.Health > 0 then
        local dist = (hrp.Position - rootPart.Position).Magnitude
        if dist < nearestDist then
          nearest = p
          nearestDist = dist
        end
      end
    end
  end

  return nearest, nearestDist
end

local function moveTo(position: Vector3)
  local path = PathfindingService:CreatePath({
    AgentRadius = 3,
    AgentHeight = 6,
    AgentCanJump = true,
  })

  local success, err = pcall(function()
    path:ComputeAsync(rootPart.Position, position)
  end)

  if not success or path.Status ~= Enum.PathStatus.Success then
    -- Fallback: move directly
    humanoid:MoveTo(position)
    return
  end

  local pathWaypoints = path:GetWaypoints()
  for _, wp in ipairs(pathWaypoints) do
    if state ~= "PATROL" and state ~= "SEARCH" then
      break -- Stop pathing if state changed to chase
    end
    humanoid:MoveTo(wp.Position)
    if wp.Action == Enum.PathWaypointAction.Jump then
      humanoid.Jump = true
    end
    humanoid.MoveToFinished:Wait()
  end
end

local function attackPlayer(player: Player)
  local now = tick()
  if now - lastAttackTime < Config.Monster.AttackCooldown then return end
  lastAttackTime = now

  local char = player.Character
  if not char then return end
  local hum = char:FindFirstChildOfClass("Humanoid")
  if not hum or hum.Health <= 0 then return end

  hum:TakeDamage(Config.Monster.AttackDamage)
end

-- Broadcast state to all clients (for UI/sound effects)
local function broadcastState(newState: string)
  state = newState
  for _, p in ipairs(Players:GetPlayers()) do
    monsterStateEvent:FireClient(p, newState, rootPart.Position)
  end
end

-- Main AI loop
task.spawn(function()
  while true do
    task.wait(0.2) -- AI tick rate

    local nearestPlayer, distance = getNearestPlayer()

    if state == "PATROL" then
      humanoid.WalkSpeed = Config.Monster.PatrolSpeed

      -- Check for nearby player
      if nearestPlayer and distance < Config.Monster.DetectionRadius then
        -- Line of sight check
        local char = nearestPlayer.Character
        if char then
          local hrp = char:FindFirstChild("HumanoidRootPart")
          if hrp then
            local ray = Ray.new(rootPart.Position, (hrp.Position - rootPart.Position).Unit * distance)
            local hit = game.Workspace:FindPartOnRay(ray, monster)
            if hit and hit:IsDescendantOf(char) then
              targetPlayer = nearestPlayer
              broadcastState("CHASE")
              continue
            end
          end
        end
      end

      -- Move to next waypoint
      if #waypoints > 0 then
        local wp = waypoints[currentWaypoint]
        if wp then
          local dist = (wp.Position - rootPart.Position).Magnitude
          if dist < 5 then
            currentWaypoint = (currentWaypoint % #waypoints) + 1
          end
          moveTo(wp.Position)
        end
      end

    elseif state == "CHASE" then
      humanoid.WalkSpeed = Config.Monster.ChaseSpeed

      if not targetPlayer or not targetPlayer.Character then
        broadcastState("SEARCH")
        searchStartTime = tick()
        continue
      end

      local char = targetPlayer.Character
      local hrp = char:FindFirstChild("HumanoidRootPart")
      local hum = char:FindFirstChildOfClass("Humanoid")

      if not hrp or not hum or hum.Health <= 0 then
        broadcastState("SEARCH")
        searchStartTime = tick()
        continue
      end

      local dist = (hrp.Position - rootPart.Position).Magnitude

      if dist > Config.Monster.LosePlayerRadius then
        broadcastState("SEARCH")
        searchStartTime = tick()
        continue
      end

      if dist < Config.Monster.AttackRange then
        attackPlayer(targetPlayer)
      end

      humanoid:MoveTo(hrp.Position)

    elseif state == "SEARCH" then
      humanoid.WalkSpeed = Config.Monster.SearchSpeed

      if nearestPlayer and distance < Config.Monster.DetectionRadius * 0.7 then
        targetPlayer = nearestPlayer
        broadcastState("CHASE")
        continue
      end

      if tick() - searchStartTime > Config.Monster.SearchDuration then
        targetPlayer = nil
        broadcastState("PATROL")
        continue
      end

      -- Wander in search area
      local randomOffset = Vector3.new(
        math.random(-20, 20),
        0,
        math.random(-20, 20)
      )
      humanoid:MoveTo(rootPart.Position + randomOffset)
      task.wait(2)
    end
  end
end)

print("[MonsterAI] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'HorrorGameManager',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Server-side game manager: item collection, door unlocking, win condition, data persistence',
      newCode: `--[[
  HorrorGameManager - Server-side game state
  Handles: item pickup, door unlocking, progress tracking, data saves
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("HorrorConfig"))

local dataStore = DataStoreService:GetDataStore("HorrorData_v1")
local Events = ReplicatedStorage:WaitForChild("Events")

local pickupItemEvent = Instance.new("RemoteEvent")
pickupItemEvent.Name = "PickupItem"
pickupItemEvent.Parent = Events

local useItemEvent = Instance.new("RemoteEvent")
useItemEvent.Name = "UseItem"
useItemEvent.Parent = Events

local updateInventoryEvent = Instance.new("RemoteEvent")
updateInventoryEvent.Name = "UpdateInventory"
updateInventoryEvent.Parent = Events

local notifyEvent = Instance.new("RemoteEvent")
notifyEvent.Name = "Notify"
notifyEvent.Parent = Events

local gameEndEvent = Instance.new("RemoteEvent")
gameEndEvent.Name = "GameEnd"
gameEndEvent.Parent = Events

-- Player state
type PlayerState = {
  inventory: {string}, -- item IDs
  completions: number,
  deaths: number,
}

local playerState: { [number]: PlayerState } = {}

local function loadData(player: Player)
  local key = "horror_" .. player.UserId
  local success, data = pcall(function()
    return dataStore:GetAsync(key)
  end)

  if success and data then
    -- Keep persistent stats but reset inventory for fresh run
    playerState[player.UserId] = {
      inventory = {},
      completions = data.completions or 0,
      deaths = data.deaths or 0,
    }
  else
    playerState[player.UserId] = {
      inventory = {},
      completions = 0,
      deaths = 0,
    }
  end

  -- Leaderstats
  local leaderstats = Instance.new("Folder")
  leaderstats.Name = "leaderstats"
  leaderstats.Parent = player

  local escapes = Instance.new("IntValue")
  escapes.Name = "Escapes"
  escapes.Value = playerState[player.UserId].completions
  escapes.Parent = leaderstats
end

local function saveData(player: Player)
  local st = playerState[player.UserId]
  if not st then return end

  local key = "horror_" .. player.UserId
  pcall(function()
    dataStore:SetAsync(key, {
      completions = st.completions,
      deaths = st.deaths,
    })
  end)
end

-- Item pickup (server validates proximity)
pickupItemEvent.OnServerEvent:Connect(function(player: Player, itemPartName: string)
  if type(itemPartName) ~= "string" then return end

  local st = playerState[player.UserId]
  if not st then return end

  -- Find the item part in workspace
  local itemPart = game.Workspace:FindFirstChild(itemPartName, true)
  if not itemPart then return end

  -- Check proximity (anti-cheat)
  local char = player.Character
  if not char then return end
  local hrp = char:FindFirstChild("HumanoidRootPart")
  if not hrp then return end

  if (itemPart.Position - hrp.Position).Magnitude > 15 then return end

  -- Get item ID from attribute or name
  local itemId = itemPart:GetAttribute("ItemId") or itemPart.Name:lower()

  -- Verify it is a valid item
  local valid = false
  for _, item in ipairs(Config.Items) do
    if item.id == itemId then
      valid = true
      break
    end
  end
  if not valid then return end

  -- Check if battery -> restore flashlight
  if itemId == "battery" then
    -- Handled on client side via event
    notifyEvent:FireClient(player, "Battery restored!")
    itemPart:Destroy()
    return
  end

  -- Add to inventory
  table.insert(st.inventory, itemId)
  updateInventoryEvent:FireClient(player, st.inventory)

  -- Find item name for notification
  for _, item in ipairs(Config.Items) do
    if item.id == itemId then
      notifyEvent:FireClient(player, "Found: " .. item.name)
      break
    end
  end

  -- Remove from world
  itemPart:Destroy()
end)

-- Use item on door
useItemEvent.OnServerEvent:Connect(function(player: Player, doorName: string)
  if type(doorName) ~= "string" then return end

  local st = playerState[player.UserId]
  if not st then return end

  -- Check what key this door needs
  local requiredKey = Config.Doors[doorName]
  if not requiredKey then return end

  -- Check if player has the key
  local hasKey = false
  local keyIndex = 0
  for i, itemId in ipairs(st.inventory) do
    if itemId == requiredKey then
      hasKey = true
      keyIndex = i
      break
    end
  end

  if not hasKey then
    notifyEvent:FireClient(player, "You need a key for this door.")
    return
  end

  -- Remove key from inventory
  table.remove(st.inventory, keyIndex)
  updateInventoryEvent:FireClient(player, st.inventory)

  -- Open the door
  local door = game.Workspace:FindFirstChild(doorName, true)
  if door then
    if door:IsA("BasePart") then
      door.CanCollide = false
      door.Transparency = 0.8
    elseif door:IsA("Model") then
      for _, part in ipairs(door:GetDescendants()) do
        if part:IsA("BasePart") then
          part.CanCollide = false
          part.Transparency = 0.8
        end
      end
    end
  end

  notifyEvent:FireClient(player, "Door unlocked!")

  -- Check win condition: if exit door opened
  if doorName == "ExitDoor" then
    st.completions += 1
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats then
      local escapes = leaderstats:FindFirstChild("Escapes")
      if escapes then escapes.Value = st.completions end
    end
    gameEndEvent:FireClient(player, "WIN", st.completions)
    saveData(player)
  end
end)

-- Track deaths
Players.PlayerAdded:Connect(function(player)
  loadData(player)

  player.CharacterAdded:Connect(function(char)
    local humanoid = char:WaitForChild("Humanoid")
    humanoid.Died:Connect(function()
      local st = playerState[player.UserId]
      if st then
        st.deaths += 1
      end
    end)
  end)
end)

Players.PlayerRemoving:Connect(function(player)
  saveData(player)
  playerState[player.UserId] = nil
end)

game:BindToClose(function()
  for _, player in ipairs(Players:GetPlayers()) do
    saveData(player)
  end
end)

print("[HorrorGameManager] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'FlashlightController',
      scriptType: 'LocalScript',
      serviceName: 'StarterPlayerScripts',
      explanation:
        'Client-side flashlight: toggle with F key or tap, battery drain/recharge, UI battery indicator',
      newCode: `--[[
  FlashlightController - Client-side flashlight system
  Toggle: F key or screen tap
  Battery drains when on, recharges when off
]]

local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("HorrorConfig"))
local Events = ReplicatedStorage:WaitForChild("Events")
local MonsterState = Events:WaitForChild("MonsterState")

local player = Players.LocalPlayer
local flashlightOn = false
local battery = Config.Flashlight.MaxBattery
local spotlight: SpotLight? = nil

-- Create battery UI
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "FlashlightHUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = player:WaitForChild("PlayerGui")

local batteryBg = Instance.new("Frame")
batteryBg.Size = UDim2.new(0, 150, 0, 16)
batteryBg.Position = UDim2.new(0, 10, 1, -30)
batteryBg.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
batteryBg.Parent = screenGui
Instance.new("UICorner", batteryBg).CornerRadius = UDim.new(0, 4)

local batteryFill = Instance.new("Frame")
batteryFill.Size = UDim2.new(1, 0, 1, 0)
batteryFill.BackgroundColor3 = Color3.fromRGB(255, 255, 80)
batteryFill.Parent = batteryBg
Instance.new("UICorner", batteryFill).CornerRadius = UDim.new(0, 4)

local batteryText = Instance.new("TextLabel")
batteryText.Size = UDim2.new(1, 0, 1, 0)
batteryText.BackgroundTransparency = 1
batteryText.Text = "Battery: 100%"
batteryText.TextColor3 = Color3.fromRGB(255, 255, 255)
batteryText.TextSize = 10
batteryText.Font = Enum.Font.GothamBold
batteryText.ZIndex = 2
batteryText.Parent = batteryBg

-- Stamina bar
local staminaBg = Instance.new("Frame")
staminaBg.Size = UDim2.new(0, 150, 0, 12)
staminaBg.Position = UDim2.new(0, 10, 1, -50)
staminaBg.BackgroundColor3 = Color3.fromRGB(20, 30, 20)
staminaBg.Parent = screenGui
Instance.new("UICorner", staminaBg).CornerRadius = UDim.new(0, 3)

local staminaFill = Instance.new("Frame")
staminaFill.Size = UDim2.new(1, 0, 1, 0)
staminaFill.BackgroundColor3 = Color3.fromRGB(80, 200, 80)
staminaFill.Parent = staminaBg
Instance.new("UICorner", staminaFill).CornerRadius = UDim.new(0, 3)

-- Monster warning
local warningLabel = Instance.new("TextLabel")
warningLabel.Size = UDim2.new(0, 300, 0, 30)
warningLabel.Position = UDim2.new(0.5, -150, 0, 10)
warningLabel.BackgroundTransparency = 1
warningLabel.Text = ""
warningLabel.TextColor3 = Color3.fromRGB(255, 50, 50)
warningLabel.TextSize = 18
warningLabel.Font = Enum.Font.GothamBlack
warningLabel.Parent = screenGui

-- Create spotlight on character
local function setupFlashlight()
  local char = player.Character
  if not char then return end
  local head = char:WaitForChild("Head", 5)
  if not head then return end

  -- Remove old spotlight
  if spotlight then spotlight:Destroy() end

  spotlight = Instance.new("SpotLight")
  spotlight.Range = Config.Flashlight.SpotlightRange
  spotlight.Angle = Config.Flashlight.SpotlightAngle
  spotlight.Brightness = 0 -- Start off
  spotlight.Face = Enum.NormalId.Front
  spotlight.Parent = head
end

player.CharacterAdded:Connect(function()
  task.defer(setupFlashlight)
end)
if player.Character then
  task.defer(setupFlashlight)
end

-- Toggle flashlight
local function toggleFlashlight()
  if battery <= 0 and not flashlightOn then return end
  flashlightOn = not flashlightOn

  if spotlight then
    spotlight.Brightness = if flashlightOn then Config.Flashlight.SpotlightBrightness else 0
  end
end

-- Input handling
UserInputService.InputBegan:Connect(function(input, processed)
  if processed then return end
  if input.KeyCode == Enum.KeyCode.F then
    toggleFlashlight()
  end
end)

-- Touch input (mobile)
UserInputService.TouchTap:Connect(function(positions)
  -- Double-tap to toggle (check if tap is in bottom-left quadrant)
  if #positions > 0 then
    local pos = positions[1]
    local viewport = game.Workspace.CurrentCamera.ViewportSize
    if pos.X < viewport.X * 0.3 and pos.Y > viewport.Y * 0.7 then
      toggleFlashlight()
    end
  end
end)

-- Stamina system
local stamina = Config.Stamina.Max
local isSprinting = false
local isExhausted = false

UserInputService.InputBegan:Connect(function(input, processed)
  if processed then return end
  if input.KeyCode == Enum.KeyCode.LeftShift then
    isSprinting = true
  end
end)

UserInputService.InputEnded:Connect(function(input)
  if input.KeyCode == Enum.KeyCode.LeftShift then
    isSprinting = false
  end
end)

-- Update loop
RunService.Heartbeat:Connect(function(dt)
  -- Battery
  if flashlightOn then
    battery = math.max(0, battery - Config.Flashlight.DrainRate * dt)
    if battery <= 0 then
      flashlightOn = false
      if spotlight then spotlight.Brightness = 0 end
    end
  else
    battery = math.min(Config.Flashlight.MaxBattery, battery + Config.Flashlight.RechargeRate * dt)
  end

  local pct = battery / Config.Flashlight.MaxBattery
  batteryFill.Size = UDim2.new(pct, 0, 1, 0)
  batteryText.Text = "Battery: " .. math.floor(pct * 100) .. "%"

  if pct < 0.2 then
    batteryFill.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
  elseif pct < 0.5 then
    batteryFill.BackgroundColor3 = Color3.fromRGB(255, 200, 50)
  else
    batteryFill.BackgroundColor3 = Color3.fromRGB(255, 255, 80)
  end

  -- Stamina
  local char = player.Character
  if char then
    local humanoid = char:FindFirstChildOfClass("Humanoid")
    if humanoid then
      if isExhausted then
        humanoid.WalkSpeed = Config.Stamina.ExhaustedSpeed
        stamina = math.min(Config.Stamina.Max, stamina + Config.Stamina.RecoveryRate * dt)
        if stamina >= Config.Stamina.Max * 0.3 then
          isExhausted = false
        end
      elseif isSprinting and stamina > 0 then
        humanoid.WalkSpeed = Config.Stamina.SprintSpeed
        stamina = math.max(0, stamina - Config.Stamina.SprintDrain * dt)
        if stamina <= 0 then
          isExhausted = true
        end
      else
        humanoid.WalkSpeed = Config.Stamina.WalkSpeed
        stamina = math.min(Config.Stamina.Max, stamina + Config.Stamina.RecoveryRate * dt)
      end
    end
  end

  staminaFill.Size = UDim2.new(stamina / Config.Stamina.Max, 0, 1, 0)
  if isExhausted then
    staminaFill.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
  else
    staminaFill.BackgroundColor3 = Color3.fromRGB(80, 200, 80)
  end
end)

-- Monster state notifications
MonsterState.OnClientEvent:Connect(function(monsterState: string, monsterPos: Vector3)
  if monsterState == "CHASE" then
    warningLabel.Text = "IT SEES YOU - RUN!"
    task.delay(3, function()
      if warningLabel.Text == "IT SEES YOU - RUN!" then
        warningLabel.Text = ""
      end
    end)
  elseif monsterState == "SEARCH" then
    warningLabel.Text = "It's searching..."
    task.delay(2, function()
      if warningLabel.Text == "It's searching..." then
        warningLabel.Text = ""
      end
    end)
  else
    warningLabel.Text = ""
  end
end)

print("[FlashlightController] Loaded")`,
    },
    {
      action: 'CreateScript' as const,
      scriptName: 'AtmosphereSetup',
      scriptType: 'Script',
      serviceName: 'ServerScriptService',
      explanation:
        'Sets up horror atmosphere: dark lighting, fog, ambient sounds. Runs once on server start.',
      newCode: `--[[
  AtmosphereSetup - Configure Lighting for horror atmosphere
  Runs once at server start. Adjust HorrorConfig.Atmosphere values to tune.
]]

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Lighting = game:GetService("Lighting")
local SoundService = game:GetService("SoundService")

local Config = require(ReplicatedStorage:WaitForChild("HorrorConfig"))
local atm = Config.Atmosphere

-- Lighting
Lighting.Ambient = atm.Ambient
Lighting.OutdoorAmbient = atm.OutdoorAmbient
Lighting.FogColor = atm.FogColor
Lighting.FogStart = atm.FogStart
Lighting.FogEnd = atm.FogEnd
Lighting.Brightness = atm.Brightness
Lighting.ClockTime = atm.ClockTime
Lighting.GlobalShadows = true

-- Add atmosphere effect
local atmosphere = Instance.new("Atmosphere")
atmosphere.Density = 0.5
atmosphere.Offset = 0.25
atmosphere.Color = atm.FogColor
atmosphere.Decay = Color3.fromRGB(20, 20, 30)
atmosphere.Glare = 0
atmosphere.Haze = 8
atmosphere.Parent = Lighting

-- Add ColorCorrection for desaturation
local cc = Instance.new("ColorCorrectionEffect")
cc.Saturation = -0.3
cc.Brightness = -0.05
cc.Contrast = 0.1
cc.TintColor = Color3.fromRGB(200, 200, 220)
cc.Parent = Lighting

-- Add Bloom for eerie glow
local bloom = Instance.new("BloomEffect")
bloom.Intensity = 0.3
bloom.Size = 24
bloom.Threshold = 0.8
bloom.Parent = Lighting

print("[AtmosphereSetup] Horror atmosphere configured")`,
    },
  ],
};
