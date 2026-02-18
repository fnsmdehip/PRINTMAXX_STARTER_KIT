# RobloxMaxx Horror Template

You are building a Roblox horror game. This project uses Claude Code with MCP servers connected to Roblox Studio.

---

## MCP Tools

- **robloxstudio** MCP: 37+ tools for reading/writing game hierarchy, scripts, properties
- **roblox-test** MCP: play testing, screenshots, game state inspection

---

## Horror Game Architecture

### Core Loop

```
Player Spawns in Dark Environment → Explore → Find Keys/Items → Solve Puzzles →
Avoid/Flee Monster → Unlock Doors → Progress Deeper → Increasing Danger →
Reach Ending (multiple paths based on items/choices)
```

### Script Structure

```
game
├── ServerScriptService/
│   ├── GameManager.lua         -- Progression state, ending logic, puzzle tracking
│   ├── MonsterAI.lua           -- Pathfinding, state machine (patrol/chase/search)
│   ├── PuzzleManager.lua       -- Key items, door locks, combination puzzles
│   ├── AtmosphereManager.lua   -- Dynamic lighting, fog, ambient events
│   ├── JumpScareManager.lua    -- Triggered scares with cooldowns
│   ├── DataManager.lua         -- Save/load checkpoint progress
│   └── EconomyManager.lua      -- Gamepasses, dev products
├── ReplicatedStorage/
│   ├── Remotes/
│   │   ├── InteractObject (RemoteEvent)     -- Client→Server: pick up, use item
│   │   ├── UpdateInventory (RemoteEvent)    -- Server→Client
│   │   ├── TriggerScare (RemoteEvent)       -- Server→Client: camera effects
│   │   ├── UpdateObjective (RemoteEvent)    -- Server→Client: hint text
│   │   ├── MonsterAlert (RemoteEvent)       -- Server→Client: heartbeat, music
│   │   └── FlashlightSync (RemoteEvent)     -- Client→Server: flashlight state
│   ├── Modules/
│   │   ├── GameConfig.lua      -- Items, doors, monster stats, atmosphere
│   │   ├── PuzzleData.lua      -- Puzzle definitions, solutions
│   │   └── SharedUtils.lua     -- Distance checks, LOS functions
│   └── Assets/
│       ├── Sounds/             -- Ambient, footsteps, stingers, monster
│       ├── Effects/            -- Particles, fog, flickering lights
│       └── UI/                 -- Inventory icons, objective display
├── StarterGui/
│   ├── HorrorHUD.lua           -- Stamina bar, flashlight battery, inventory
│   ├── ObjectiveUI.lua         -- Current objective hint text
│   └── DeathScreen.lua         -- Death animation, respawn button
├── StarterPlayerScripts/
│   ├── FlashlightController.lua -- Toggle flashlight, battery drain, recharge
│   ├── StaminaController.lua    -- Sprint/walk, stamina drain/recovery
│   ├── CameraEffects.lua        -- Shake, blur, vignette, head bob
│   └── SoundController.lua      -- Footstep variation, heartbeat proximity
└── Workspace/
    ├── Map/
    │   ├── Floor_1/            -- First area (tutorial, low danger)
    │   ├── Floor_2/            -- Mid area (monster patrols start)
    │   ├── Floor_3/            -- Hard area (multiple monsters, darker)
    │   └── Floor_Boss/         -- Final confrontation
    ├── Doors/                  -- All locked doors with key requirements
    ├── Items/                  -- Pickupable key items and tools
    ├── MonsterSpawns/          -- Monster spawn/patrol points
    └── ScareZones/             -- Proximity-triggered scare locations
```

### GameConfig Module

```luau
local Config = {}

Config.Player = {
    WalkSpeed = 12,
    SprintSpeed = 20,
    MaxStamina = 100,
    StaminaDrainRate = 15,      -- Per second while sprinting
    StaminaRegenRate = 8,       -- Per second while walking
    StaminaRegenDelay = 1.5,    -- Seconds after sprint before regen starts
}

Config.Flashlight = {
    MaxBattery = 100,
    DrainRate = 3,              -- Per second while on
    RechargeRate = 1.5,         -- Per second while off
    Range = 40,                 -- SpotLight range in studs
    Angle = 45,                 -- SpotLight angle
    Brightness = 2,
    FlickerAtPercent = 20,      -- Start flickering below 20% battery
}

Config.Monster = {
    PatrolSpeed = 8,
    ChaseSpeed = 18,            -- Faster than player walk, slower than sprint
    SearchSpeed = 10,
    DetectionRange = 30,        -- Studs (in line of sight)
    HearingRange = 50,          -- Studs (sprinting/noise detection)
    FlashlightDetectionBonus = 15, -- Extra detection range if flashlight on
    LoseInterestTime = 15,     -- Seconds of no detection before returning to patrol
    StunDuration = 3,           -- Seconds stunned by flashlight beam (if mechanic used)
    KillRange = 5,              -- Studs to trigger death
}

Config.Atmosphere = {
    AmbientColor = Color3.fromRGB(10, 10, 15),
    FogStart = 0,
    FogEnd = 80,
    FogColor = Color3.fromRGB(5, 5, 10),
    ClockTime = 0,              -- Midnight
    FlickerLightChance = 0.02,  -- Per frame chance of ambient light flicker
}

Config.Doors = {
    -- doorId = { keyRequired = "itemId" or nil, locked = bool }
    door_basement = { keyRequired = "rusty_key", locked = true },
    door_office = { keyRequired = "office_keycard", locked = true },
    door_exit = { keyRequired = "master_key", locked = true },
    -- Doors without keys use puzzles (combination, lever, pressure plate)
}

Config.Items = {
    rusty_key = { name = "Rusty Key", description = "Opens the basement door", type = "key" },
    office_keycard = { name = "Office Keycard", description = "Access to the office wing", type = "key" },
    master_key = { name = "Master Key", description = "Opens the final exit", type = "key" },
    battery_pack = { name = "Battery Pack", description = "Fully recharges flashlight", type = "consumable" },
    first_aid = { name = "First Aid Kit", description = "Allows one extra hit", type = "consumable" },
    note_1 = { name = "Torn Note", description = "The code is 4-7-2...", type = "lore" },
    note_2 = { name = "Doctor's Log", description = "Subject escaped containment on floor 3", type = "lore" },
    photo = { name = "Old Photo", description = "A family. One face is scratched out.", type = "lore" },
}

Config.Endings = {
    -- Multiple endings based on items collected and choices made
    good_ending = { requires = {"photo", "note_1", "note_2"}, door = "door_exit" },
    bad_ending = { requires = {}, door = "door_exit" },      -- Escape without lore = bad ending
    secret_ending = { requires = {"secret_item"}, door = "hidden_exit" },
}

Config.Gamepasses = {
    ExtraLife = 0,              -- Replace with real ID. One free respawn per run
    BrighterFlashlight = 0,    -- 2x flashlight range and brightness
    SprintBoost = 0,           -- 20% more stamina
    MonsterRadar = 0,          -- Show monster direction on HUD
}

Config.DevProducts = {
    BatteryPack = { id = 0 },  -- Full flashlight recharge
    Revive = { id = 0 },       -- Respawn without losing progress
    Hint = { id = 0 },         -- Show next objective location
}

return Config
```

### Key Implementation Details

**Monster AI (State Machine):**
```luau
local PathfindingService = game:GetService("PathfindingService")
local RunService = game:GetService("RunService")

type MonsterState = "patrol" | "chase" | "search" | "return"

local monster = {} -- Monster model reference
local state: MonsterState = "patrol"
local target: Player? = nil
local lastSeenPosition: Vector3? = nil
local searchTimer = 0
local patrolIndex = 1
local patrolPoints = {} -- Array of Vector3 waypoints

local function canSeePlayer(player: Player): boolean
    local character = player.Character
    if not character then return false end
    local hrp = character:FindFirstChild("HumanoidRootPart")
    local monsterHead = monster:FindFirstChild("Head")
    if not hrp or not monsterHead then return false end

    local distance = (hrp.Position - monsterHead.Position).Magnitude
    local maxRange = Config.Monster.DetectionRange

    -- Flashlight increases detection range
    if playerFlashlightOn[player.UserId] then
        maxRange += Config.Monster.FlashlightDetectionBonus
    end

    if distance > maxRange then return false end

    -- Line of sight raycast
    local direction = (hrp.Position - monsterHead.Position).Unit
    local rayParams = RaycastParams.new()
    rayParams.FilterDescendantsInstances = {monster}
    rayParams.FilterType = Enum.RaycastFilterType.Exclude

    local result = workspace:Raycast(monsterHead.Position, direction * distance, rayParams)
    if result and result.Instance:IsDescendantOf(character) then
        return true
    end

    return false
end

local function canHearPlayer(player: Player): boolean
    local character = player.Character
    if not character then return false end
    local hrp = character:FindFirstChild("HumanoidRootPart")
    local monsterPos = monster:FindFirstChild("HumanoidRootPart")
    if not hrp or not monsterPos then return false end

    local distance = (hrp.Position - monsterPos.Position).Magnitude

    -- Sprinting players are louder
    local humanoid = character:FindFirstChild("Humanoid")
    if humanoid and humanoid.WalkSpeed > Config.Player.WalkSpeed then
        return distance <= Config.Monster.HearingRange
    end

    return false
end

local function moveTo(position: Vector3)
    local monsterHRP = monster:FindFirstChild("HumanoidRootPart")
    local humanoid = monster:FindFirstChild("Humanoid")
    if not monsterHRP or not humanoid then return end

    local path = PathfindingService:CreatePath({
        AgentRadius = 3,
        AgentHeight = 6,
        AgentCanJump = false,
    })

    local success, err = pcall(function()
        path:ComputeAsync(monsterHRP.Position, position)
    end)

    if success and path.Status == Enum.PathStatus.Success then
        local waypoints = path:GetWaypoints()
        for _, waypoint in waypoints do
            humanoid:MoveTo(waypoint.Position)
            local reached = humanoid.MoveToFinished:Wait(2)
            if not reached then break end

            -- Re-check state during movement (might need to chase)
            if state == "chase" and target then
                -- Recalculate path to current target position
                break
            end
        end
    end
end

-- Main AI loop (runs on server)
task.spawn(function()
    while true do
        if state == "patrol" then
            -- Move between patrol points
            monster.Humanoid.WalkSpeed = Config.Monster.PatrolSpeed
            moveTo(patrolPoints[patrolIndex])
            patrolIndex = (patrolIndex % #patrolPoints) + 1

            -- Check for players
            for _, player in game:GetService("Players"):GetPlayers() do
                if canSeePlayer(player) or canHearPlayer(player) then
                    target = player
                    state = "chase"
                    MonsterAlert:FireClient(player, "chase_start")
                    break
                end
            end

        elseif state == "chase" then
            monster.Humanoid.WalkSpeed = Config.Monster.ChaseSpeed
            if target and target.Character then
                local hrp = target.Character:FindFirstChild("HumanoidRootPart")
                if hrp then
                    lastSeenPosition = hrp.Position

                    -- Check kill range
                    local monsterPos = monster:FindFirstChild("HumanoidRootPart").Position
                    if (hrp.Position - monsterPos).Magnitude <= Config.Monster.KillRange then
                        killPlayer(target)
                        state = "return"
                        target = nil
                    elseif canSeePlayer(target) or canHearPlayer(target) then
                        moveTo(hrp.Position)
                    else
                        -- Lost sight
                        state = "search"
                        searchTimer = Config.Monster.LoseInterestTime
                        MonsterAlert:FireClient(target, "chase_end")
                    end
                else
                    state = "return"
                    target = nil
                end
            else
                state = "return"
                target = nil
            end

        elseif state == "search" then
            monster.Humanoid.WalkSpeed = Config.Monster.SearchSpeed
            if lastSeenPosition then
                moveTo(lastSeenPosition)
            end

            searchTimer -= task.wait(1)

            -- Check if player reappears
            for _, player in game:GetService("Players"):GetPlayers() do
                if canSeePlayer(player) then
                    target = player
                    state = "chase"
                    MonsterAlert:FireClient(player, "chase_start")
                    break
                end
            end

            if searchTimer <= 0 then
                state = "return"
                lastSeenPosition = nil
            end

        elseif state == "return" then
            monster.Humanoid.WalkSpeed = Config.Monster.PatrolSpeed
            moveTo(patrolPoints[patrolIndex])
            state = "patrol"
        end

        task.wait(0.1)
    end
end)
```

**Flashlight Controller (Client):**
```luau
-- StarterPlayerScripts/FlashlightController
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer
local FlashlightSync = game:GetService("ReplicatedStorage").Remotes.FlashlightSync

local flashlightOn = false
local battery = 100
local spotLight: SpotLight? = nil

local function toggleFlashlight()
    flashlightOn = not flashlightOn
    if spotLight then
        spotLight.Enabled = flashlightOn
    end
    FlashlightSync:FireServer(flashlightOn)
end

-- Toggle on F key or tap
UserInputService.InputBegan:Connect(function(input, processed)
    if processed then return end
    if input.KeyCode == Enum.KeyCode.F or input.UserInputType == Enum.UserInputType.Touch then
        toggleFlashlight()
    end
end)

-- Battery drain/recharge
RunService.Heartbeat:Connect(function(dt)
    if flashlightOn then
        battery = math.max(0, battery - Config.Flashlight.DrainRate * dt)
        if battery <= 0 then
            flashlightOn = false
            if spotLight then spotLight.Enabled = false end
            FlashlightSync:FireServer(false)
        end

        -- Flicker effect at low battery
        if battery <= Config.Flashlight.FlickerAtPercent and spotLight then
            if math.random() < 0.1 then
                spotLight.Enabled = false
                task.delay(math.random() * 0.2, function()
                    if flashlightOn and spotLight then
                        spotLight.Enabled = true
                    end
                end)
            end
        end
    else
        battery = math.min(Config.Flashlight.MaxBattery, battery + Config.Flashlight.RechargeRate * dt)
    end
end)

-- Create SpotLight when character loads
local function setupFlashlight(character)
    local head = character:WaitForChild("Head")
    spotLight = Instance.new("SpotLight")
    spotLight.Range = Config.Flashlight.Range
    spotLight.Angle = Config.Flashlight.Angle
    spotLight.Brightness = Config.Flashlight.Brightness
    spotLight.Face = Enum.NormalId.Front
    spotLight.Enabled = flashlightOn
    spotLight.Parent = head
end

player.CharacterAdded:Connect(setupFlashlight)
if player.Character then setupFlashlight(player.Character) end
```

**Stamina System (Client):**
```luau
local stamina = Config.Player.MaxStamina
local isSprinting = false
local lastSprintEnd = 0

RunService.Heartbeat:Connect(function(dt)
    local humanoid = player.Character and player.Character:FindFirstChild("Humanoid")
    if not humanoid then return end

    if isSprinting and stamina > 0 then
        stamina = math.max(0, stamina - Config.Player.StaminaDrainRate * dt)
        humanoid.WalkSpeed = Config.Player.SprintSpeed

        if stamina <= 0 then
            isSprinting = false
            lastSprintEnd = tick()
            humanoid.WalkSpeed = Config.Player.WalkSpeed
        end
    else
        humanoid.WalkSpeed = Config.Player.WalkSpeed
        -- Regen after delay
        if tick() - lastSprintEnd >= Config.Player.StaminaRegenDelay then
            stamina = math.min(Config.Player.MaxStamina, stamina + Config.Player.StaminaRegenRate * dt)
        end
    end
end)

-- Shift to sprint
UserInputService.InputBegan:Connect(function(input, processed)
    if processed then return end
    if input.KeyCode == Enum.KeyCode.LeftShift then
        isSprinting = true
    end
end)

UserInputService.InputEnded:Connect(function(input)
    if input.KeyCode == Enum.KeyCode.LeftShift then
        isSprinting = false
        lastSprintEnd = tick()
    end
end)
```

**Atmosphere Engineering:**
```luau
-- ServerScriptService/AtmosphereManager
-- Set up the horror atmosphere on game start

local Lighting = game:GetService("Lighting")

-- Base atmosphere
Lighting.Ambient = Config.Atmosphere.AmbientColor
Lighting.OutdoorAmbient = Config.Atmosphere.AmbientColor
Lighting.FogStart = Config.Atmosphere.FogStart
Lighting.FogEnd = Config.Atmosphere.FogEnd
Lighting.FogColor = Config.Atmosphere.FogColor
Lighting.ClockTime = Config.Atmosphere.ClockTime
Lighting.GlobalShadows = true
Lighting.Brightness = 0

-- Add atmosphere instance for volumetric fog
local atmosphere = Instance.new("Atmosphere")
atmosphere.Density = 0.4
atmosphere.Offset = 0.25
atmosphere.Color = Config.Atmosphere.FogColor
atmosphere.Decay = Color3.fromRGB(50, 50, 60)
atmosphere.Glare = 0
atmosphere.Haze = 5
atmosphere.Parent = Lighting

-- Color correction for desaturated, cold look
local correction = Instance.new("ColorCorrectionEffect")
correction.Brightness = -0.05
correction.Contrast = 0.1
correction.Saturation = -0.3
correction.TintColor = Color3.fromRGB(200, 200, 220) -- Slight blue tint
correction.Parent = Lighting

-- Random ambient events (lights flicker, distant sounds)
task.spawn(function()
    while true do
        task.wait(math.random(5, 20))

        -- Random light flicker in a room
        local lights = workspace.Map:GetDescendants()
        for _, obj in lights do
            if obj:IsA("PointLight") or obj:IsA("SpotLight") then
                if math.random() < Config.Atmosphere.FlickerLightChance * 10 then
                    local originalBrightness = obj.Brightness
                    obj.Brightness = 0
                    task.wait(math.random() * 0.3)
                    obj.Brightness = originalBrightness
                end
            end
        end
    end
end)
```

**Jump Scare System:**
```luau
-- Triggered by proximity to ScareZone parts
-- Each scare has a cooldown so it doesn't fire repeatedly

local scaredPlayers = {} -- Track per-player cooldowns per scare zone

local function triggerScare(player: Player, scareZone: BasePart)
    local scareId = scareZone.Name
    local key = `{player.UserId}_{scareId}`

    -- Check cooldown (60 seconds between same scare)
    if scaredPlayers[key] and tick() - scaredPlayers[key] < 60 then return end
    scaredPlayers[key] = tick()

    local scareType = scareZone:GetAttribute("ScareType") or "camera_shake"

    TriggerScare:FireClient(player, {
        type = scareType,
        intensity = scareZone:GetAttribute("Intensity") or 1,
        duration = scareZone:GetAttribute("Duration") or 1,
        soundId = scareZone:GetAttribute("SoundId"),
    })
end

-- Client handles the actual scare effect
-- CameraEffects.lua receives TriggerScare and applies:
-- "camera_shake": Rapid small CFrame offsets on camera
-- "flash": White screen flash using a ScreenGui
-- "zoom": Rapid FOV change
-- "blur": DepthOfField effect spike
-- "vignette": Dark edges closing in
```

**Hiding Spot System:**
```luau
-- Parts tagged "HidingSpot" via CollectionService
-- Player can enter hiding spots to become undetectable by monster
local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local hiddenPlayers: {[number]: BasePart} = {} -- userId -> hiding spot part

for _, spot in CollectionService:GetTagged("HidingSpot") do
    local prompt = Instance.new("ProximityPrompt")
    prompt.ActionText = "Hide"
    prompt.ObjectText = spot:GetAttribute("DisplayName") or ""
    prompt.MaxActivationDistance = 6
    prompt.HoldDuration = 0.3
    prompt.Parent = spot

    prompt.Triggered:Connect(function(player)
        local character = player.Character
        if not character then return end
        local hrp = character:FindFirstChild("HumanoidRootPart")
        if not hrp then return end

        -- Enter hiding spot
        hiddenPlayers[player.UserId] = spot
        character:SetAttribute("IsHiding", true)

        -- Make character invisible
        for _, part in character:GetDescendants() do
            if part:IsA("BasePart") then
                part.Transparency = 1
            end
        end
        hrp.Anchored = true

        -- Lock camera to hiding spot view
        ReplicatedStorage.Remotes.UpdateInventory:FireClient(player, "hiding", true, spot.CFrame)

        -- Change prompt to exit
        prompt.ActionText = "Leave"

        -- Exit when triggered again
        local exitConn
        exitConn = prompt.Triggered:Connect(function(exitPlayer)
            if exitPlayer ~= player then return end
            exitConn:Disconnect()

            hiddenPlayers[player.UserId] = nil
            character:SetAttribute("IsHiding", false)
            hrp.Anchored = false

            for _, part in character:GetDescendants() do
                if part:IsA("BasePart") and part.Name ~= "HumanoidRootPart" then
                    part.Transparency = 0
                end
            end

            prompt.ActionText = "Hide"
            ReplicatedStorage.Remotes.UpdateInventory:FireClient(player, "hiding", false)
        end)
    end)
end

-- Monster AI integration: check IsHiding attribute before detection
-- (Already handled in canSeePlayer function via character:GetAttribute("IsHiding"))
```

**Door System (Animated Open/Close with Key Requirements):**
```luau
-- Doors tagged "LockedDoor" with attributes:
--   RequiredKey: string (item ID needed to unlock)
--   DoorId: string (unique identifier)
local TweenService = game:GetService("TweenService")

for _, door in CollectionService:GetTagged("LockedDoor") do
    local isOpen = false
    local isLocked = door:GetAttribute("RequiredKey") ~= nil

    local prompt = Instance.new("ProximityPrompt")
    prompt.MaxActivationDistance = 8
    prompt.HoldDuration = 0.5
    prompt.Parent = door

    local function updatePrompt()
        if isLocked then
            prompt.ActionText = "Locked"
            prompt.ObjectText = "Requires " .. (Config.Items[door:GetAttribute("RequiredKey")] or {}).name or "a key"
        else
            prompt.ActionText = if isOpen then "Close" else "Open"
            prompt.ObjectText = ""
        end
    end

    updatePrompt()

    prompt.Triggered:Connect(function(player)
        if isLocked then
            -- Check if player has the key
            local requiredKey = door:GetAttribute("RequiredKey")
            local inv = playerInventories[player.UserId]
            if not inv or not table.find(inv.keys, requiredKey) then
                -- Fire "locked" sound and UI notification
                ReplicatedStorage.Remotes.UpdateObjective:FireClient(player, "locked", door:GetAttribute("RequiredKey"))
                return
            end

            -- Use key to unlock
            local idx = table.find(inv.keys, requiredKey)
            table.remove(inv.keys, idx)
            isLocked = false

            -- Play unlock sound
            local unlockSound = door:FindFirstChild("UnlockSound")
            if unlockSound then unlockSound:Play() end
        end

        -- Toggle open/close with animation
        isOpen = not isOpen
        local hinge = door:FindFirstChild("HingePart") or door
        local openAngle = door:GetAttribute("OpenAngle") or 90
        local targetCFrame = if isOpen
            then hinge.CFrame * CFrame.Angles(0, math.rad(openAngle), 0)
            else hinge.CFrame * CFrame.Angles(0, math.rad(-openAngle), 0)
        local speed = if isOpen then Config.Doors.OpenSpeed else Config.Doors.CloseSpeed

        local tween = TweenService:Create(hinge, TweenInfo.new(speed, Enum.EasingStyle.Quad), {
            CFrame = targetCFrame,
        })
        tween:Play()

        -- Play creak sound
        local creakSound = door:FindFirstChild("CreakSound")
        if creakSound then creakSound:Play() end

        updatePrompt()
    end)
end
```

**Footstep Sound Variation by Surface:**
```luau
-- StarterPlayerScripts/SoundController.lua (footstep section)
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer

-- Material -> sound ID mapping
local footstepSounds: {[Enum.Material]: string} = {
    [Enum.Material.WoodPlanks] = "rbxassetid://0",  -- Wood creak
    [Enum.Material.Concrete] = "rbxassetid://0",     -- Hard step
    [Enum.Material.Metal] = "rbxassetid://0",         -- Metallic clang
    [Enum.Material.Grass] = "rbxassetid://0",         -- Soft rustle
    [Enum.Material.Slate] = "rbxassetid://0",         -- Stone tap
    [Enum.Material.Fabric] = "rbxassetid://0",        -- Muffled step (carpet)
    [Enum.Material.Marble] = "rbxassetid://0",        -- Echo step
}
local defaultStepSound = "rbxassetid://0"

local lastStepTime = 0
local walkStepInterval = 0.5
local sprintStepInterval = 0.3

player.CharacterAdded:Connect(function(character)
    local humanoid = character:WaitForChild("Humanoid")
    local hrp = character:WaitForChild("HumanoidRootPart")

    RunService.Heartbeat:Connect(function()
        if humanoid.MoveDirection.Magnitude < 0.1 then return end

        local now = tick()
        local isSprinting = humanoid.WalkSpeed > Config.Player.WalkSpeed
        local interval = if isSprinting then sprintStepInterval else walkStepInterval

        if now - lastStepTime < interval then return end
        lastStepTime = now

        -- Raycast down to detect floor material
        local rayResult = workspace:Raycast(hrp.Position, Vector3.new(0, -5, 0))
        local soundId = defaultStepSound
        if rayResult then
            soundId = footstepSounds[rayResult.Material] or defaultStepSound
        end

        local sound = Instance.new("Sound")
        sound.SoundId = soundId
        sound.Volume = if isSprinting then 0.8 else 0.4
        sound.PlaybackSpeed = 0.9 + math.random() * 0.2 -- Slight pitch variation
        sound.RollOffMaxDistance = if isSprinting then 60 else 30 -- Sprinting is louder/travels further
        sound.Parent = hrp
        sound:Play()
        sound.Ended:Connect(function() sound:Destroy() end)
    end)
end)
```

**Procedural Item/Key Location Randomization:**
```luau
-- Optional: randomize key and item spawn locations each round
-- Define possible spawn points as tagged parts: "KeySpawn_rusty_key", "KeySpawn_office_keycard", etc.
-- Each round, pick one random spawn point per key

local function randomizeItemLocations()
    for itemId, itemDef in Config.Items do
        if itemDef.type ~= "key" and itemDef.type ~= "consumable" then continue end

        local spawnPoints = CollectionService:GetTagged("KeySpawn_" .. itemId)
        if #spawnPoints == 0 then continue end

        -- Pick random spawn
        local chosen = spawnPoints[math.random(#spawnPoints)]

        -- Create pickup at chosen location
        local pickup = ServerStorage.Items[itemId]:Clone()
        pickup.Position = chosen.Position
        pickup.Parent = workspace.Items

        -- Add proximity prompt for pickup
        local prompt = Instance.new("ProximityPrompt")
        prompt.ActionText = "Pick Up"
        prompt.ObjectText = itemDef.name
        prompt.MaxActivationDistance = 8
        prompt.Parent = pickup

        prompt.Triggered:Connect(function(player)
            addItemToInventory(player, itemId)
            pickup:Destroy()
        end)
    end
end

-- Call at round start
randomizeItemLocations()
```

**Multiple Endings Implementation:**
```luau
-- Check ending conditions when player reaches exit
local function determineEnding(player: Player): string
    local inv = playerInventories[player.UserId]
    if not inv then return "bad_ending" end

    local collectedItems = {}
    for _, key in inv.keys do
        collectedItems[key] = true
    end
    for _, item in inv.items do
        collectedItems[item] = true
    end

    -- Check endings in priority order (secret > good > bad)
    for endingId, endingDef in Config.Endings do
        local hasAll = true
        for _, requiredItem in endingDef.requires do
            if not collectedItems[requiredItem] then
                hasAll = false
                break
            end
        end
        if hasAll and endingId == "secret_ending" then
            return "secret_ending"
        end
    end

    -- Good ending: collected all lore items
    local goodEnding = Config.Endings.good_ending
    local hasAllLore = true
    for _, req in goodEnding.requires do
        if not collectedItems[req] then hasAllLore = false break end
    end
    if hasAllLore then return "good_ending" end

    return "bad_ending"
end

local function triggerEnding(player: Player, endingType: string)
    -- Fire ending cutscene/text to client
    ReplicatedStorage.Remotes.UpdateObjective:FireClient(player, "ending", endingType)

    -- Track which endings player has unlocked (for All Endings gamepass)
    local data = playerData[player.UserId]
    if data then
        data.unlockedEndings = data.unlockedEndings or {}
        data.unlockedEndings[endingType] = true
        saveData(player, data)
    end
end
```

### Sound Design Reference Table

| Sound Category | Volume | When | Implementation Notes |
|---------------|--------|------|---------------------|
| Ambient drone | 0.3 | Always playing | Low frequency hum. Barely audible. Creates subconscious unease |
| Heartbeat | 0-1.5 | Monster proximity | Scales with distance via MonsterProximity remote. 0 = far, 1.5 = close |
| Player footsteps | 0.4-0.8 | Player moving | Vary by surface material (wood, metal, carpet, concrete). Sprint = louder |
| Monster footsteps | 0.5-1.0 | Monster moving | Directional 3D audio. Heavier than player steps |
| Door sounds | 0.6 | Door interaction | Creak on open, slam on close, lock click on unlock |
| Jump scare stinger | 2.0 | Scare triggers | Short, sharp, high frequency. Max 1 per 60 seconds |
| Monster growl | 0.5 | Patrol state | Low, intermittent. Alerts player to nearby patrol |
| Monster roar | 1.0 | Chase start | Loud, signals chase has begun |
| Environmental | 0.2-0.4 | Ambient detail | Dripping water, wind, distant thunder, clock ticking, pipes |
| **Silence** | **0** | **Before scares** | **Cut ALL ambient audio briefly before a scare. Most terrifying sound** |
| Chase music | 0.7 | Chase state | Tense, fast-paced. Fades in/out with chase state |
| Discovery sting | 0.5 | Key item found | Short positive tone. Contrast to horror audio |

---

## Monetization Strategy for Horror Games

### Gamepasses (One-Time)

| Gamepass | Price (Robux) | Effect |
|----------|---------------|--------|
| Extra Life | 149 | One free respawn per run |
| Bright Flashlight | 99 | 2x range and brightness |
| Sprint Boost | 99 | +20% max stamina |
| Monster Radar | 199 | Directional indicator on HUD |
| Night Vision | 249 | Subtle green-tinted brightness boost |
| All Endings Pass | 299 | Reveals requirements for each ending |

### Dev Products (Repeatable)

| Product | Price (Robux) | Effect |
|---------|---------------|--------|
| Battery Pack | 25 | Full flashlight recharge |
| Instant Revive | 49 | Respawn without progress loss |
| Hint | 15 | Shows direction to next objective |
| Decoy | 35 | Place a noise-making decoy to distract monster |

### Rewarded Video Ads

- Watch ad for battery recharge
- Watch ad for one free hint
- Watch ad for temporary speed boost

---

## Horror Meta Intelligence (Feb 2026)

### The Doors Effect

Doors (5B+ visits) proved that horror works on Roblox at massive scale. Key factors:
- Procedural generation (every run is different)
- Co-op (play with friends, reduces fear barrier)
- Jump scares that are fair (you can learn patterns)
- Short runs (~15-30 minutes) respect session time
- YouTube/streaming friendly (reactions = organic marketing)

### What Makes Horror Work on Roblox

1. **Sound design > visual design**: Roblox's graphics are limited. Sound has no such limit. Footsteps, ambient drones, proximity heartbeats, directional stingers, and silence (the most terrifying sound) are your primary tools.

2. **Anticipation > the scare itself**: The moment before the scare is more impactful than the scare. Build tension through:
   - Narrowing hallways
   - Flickering lights
   - Distant sounds getting closer
   - Environmental storytelling (blood, scratches, overturned furniture)

3. **Player agency**: Players who CHOOSE to enter the dark room are more scared than players forced into it. Give multiple paths, some safer but slower, some dangerous but rewarding.

4. **Co-op amplifies fear**: Friends screaming on voice chat creates organic viral moments. Design for 2-4 player co-op. Give roles (one holds flashlight, one holds key, one watches behind).

5. **Procedural elements**: Even small randomization (monster patrol routes, item locations, which doors are locked) prevents memorization and maintains fear across replays.

### Differentiation Ideas

- **Asymmetric multiplayer**: One player IS the monster (like Dead by Daylight). Massively underexplored on Roblox.
- **Investigation horror**: Collect evidence, solve a mystery while being hunted. Combines puzzle satisfaction with tension.
- **Time loop horror**: Groundhog Day structure. Learn from each death. Unlock shortcuts and knowledge.
- **Psychological horror**: Less jump scares, more environmental dread. Rare on Roblox (most are jumpscare-heavy).
- **Horror + survival crafting**: Collect resources, build barricades, craft tools. Adds progression to horror.

### YouTube/Streaming Optimization

Horror games get disproportionate attention from content creators because reactions = views. Design for this:
- Intense moments that make good thumbnails (monster reveals, chase sequences)
- Funny/memorable death animations
- Jumpscares that work on camera (loud, visual, unexpected)
- Secrets/easter eggs that reward exploration content
- Multiple endings that encourage "watch all endings" videos

### Successful Horror Games to Study

- **Doors**: Procedural rooms, entity variety, co-op. 5B+ visits.
- **The Mimic**: Story-driven, Japanese horror aesthetic, multiple chapters.
- **Apeirophobia**: Backrooms-inspired, liminal spaces, atmospheric.
- **Bear (Alpha)**: Asymmetric (1 bear vs many survivors).

---

## Luau Standards

- Use `task.wait()` not `wait()`
- Use `task.spawn()` not `spawn()`
- Wrap DataStore calls in `pcall`
- Validate ALL RemoteEvent inputs server-side
- Never tell clients the monster's exact position (only proximity alerts)
- Use type annotations on function signatures
- Use string interpolation
- Save checkpoint progress, not full game state (horror games should have permadeath per run)
- Debounce all Touched events
- Clean up connections and instances when game/round ends

---

## Development Workflow

1. Use robloxstudio MCP to create the map structure (Floor_1 through Floor_Boss)
2. Set up atmosphere (Lighting, Atmosphere, ColorCorrection)
3. Create all config ModuleScripts
4. Create server scripts (GameManager, MonsterAI, PuzzleManager, AtmosphereManager)
5. Create remote events
6. Place doors, items, scare zones in the map
7. Create monster model with Humanoid and pathfinding agent
8. Create client scripts (FlashlightController, StaminaController, CameraEffects, SoundController)
9. Create HUD (stamina bar, battery indicator, inventory, objective)
10. Use roblox-test MCP to play test Floor_1
11. Verify: flashlight works, monster chases, items collect, doors unlock
12. Tune monster detection ranges and speeds for tension
13. Add sound design (ambient, footsteps, stingers, monster sounds)
14. Build remaining floors
15. Add monetization
16. Test all endings
17. Polish (particles, screen effects, UI transitions)

### Sound Design Priority Order

Sound is the most important element in a horror game. Prioritize:
1. **Ambient drone** - Constant low-frequency hum. Sets baseline dread.
2. **Monster sounds** - Breathing, footsteps, growling. Directional audio.
3. **Player footsteps** - Vary by surface (wood, metal, carpet, concrete).
4. **Heartbeat** - Intensifies with monster proximity.
5. **Stingers** - Sharp audio cues for scares and discoveries.
6. **Silence** - The absence of sound after constant ambient = immediate tension spike.
7. **Environmental** - Creaking, dripping, wind, distant screams.
8. **Music** - Sparse. Save for key moments (chase, discovery, ending).
