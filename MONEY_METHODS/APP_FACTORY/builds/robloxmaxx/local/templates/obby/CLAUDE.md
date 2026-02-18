# RobloxMaxx Obby Template

You are building a Roblox obby (obstacle course) game. This project uses Claude Code with MCP servers connected to Roblox Studio.

---

## MCP Tools

- **robloxstudio** MCP: 37+ tools for reading/writing game hierarchy, scripts, properties
- **roblox-test** MCP: play testing, screenshots, game state inspection

---

## Obby Game Architecture

### Core Loop

```
Player Spawns → Navigate Obstacles → Reach Checkpoint → Saved Progress →
Die? Respawn at Last Checkpoint → Complete All Stages → Speedrun/Prestige
```

### Script Structure

```
game
├── ServerScriptService/
│   ├── ObbyManager.lua         -- Stage tracking, progression, main game logic
│   ├── CheckpointHandler.lua   -- Spawn management, checkpoint registration
│   ├── DataManager.lua         -- Save/load stage progress with DataStoreService
│   ├── EconomyManager.lua      -- Currency, gamepasses, skip stages
│   └── TimerManager.lua        -- Speedrun timing, leaderboards
├── ReplicatedStorage/
│   ├── Remotes/
│   │   ├── StageCompleted (RemoteEvent)     -- Client→Server
│   │   ├── UpdateStageDisplay (RemoteEvent) -- Server→Client
│   │   ├── TimerSync (RemoteEvent)          -- Server→Client
│   │   ├── SkipStage (RemoteEvent)          -- Client→Server
│   │   └── RedeemCode (RemoteEvent)
│   ├── Modules/
│   │   ├── ObbyConfig.lua      -- Stage definitions, difficulty, prices
│   │   └── SharedUtils.lua     -- Formatting, time display
│   └── Assets/
│       └── (shared effects, sounds)
├── StarterGui/
│   ├── ObbyHUD.lua             -- Stage counter, timer, death counter
│   └── ShopUI.lua              -- Skip stages, cosmetics
├── StarterPlayerScripts/
│   └── DeathTracker.lua        -- Track deaths for stats/humor
└── Workspace/
    └── Stages/
        ├── Stage_001/          -- Each stage is a folder
        │   ├── Checkpoint       -- SpawnLocation or Part with touched event
        │   ├── Obstacles/       -- Kill bricks, platforms, etc.
        │   └── Decorations/
        ├── Stage_002/
        └── ...
```

### ObbyConfig Module

```luau
local Config = {}

Config.Stages = {
    TotalStages = 100,
    DifficultyCurve = {
        { range = {1, 20},   difficulty = "Easy",    color = Color3.fromRGB(0, 255, 0) },
        { range = {21, 50},  difficulty = "Medium",  color = Color3.fromRGB(255, 255, 0) },
        { range = {51, 80},  difficulty = "Hard",    color = Color3.fromRGB(255, 100, 0) },
        { range = {81, 100}, difficulty = "Extreme",  color = Color3.fromRGB(255, 0, 0) },
    },
}

Config.Timer = {
    Enabled = true,
    GlobalLeaderboard = true,
    LeaderboardKey = "SpeedrunTimes_v1",
}

Config.Currency = {
    CoinsPerStage = 10,         -- Base coins per stage completion
    BonusPerDifficulty = {
        Easy = 1,
        Medium = 2,
        Hard = 5,
        Extreme = 10,
    },
}

Config.Gamepasses = {
    SkipStage = 0,              -- Replace with real ID
    DoubleCoins = 0,
    SpeedBoost = 0,
    GravityCoil = 0,
    Checkpoint_30 = 0,          -- Skip to stage 30
    Checkpoint_60 = 0,          -- Skip to stage 60
}

Config.DevProducts = {
    SingleSkip = { id = 0, uses = 1 },
    SkipPack5 = { id = 0, uses = 5 },
    SkipPack10 = { id = 0, uses = 10 },
    CoinPack = { id = 0, amount = 500 },
}

return Config
```

### Key Implementation Details

**Checkpoint System:**
```luau
-- Each checkpoint is a Part named "Checkpoint" inside a Stage folder
-- When player touches checkpoint:
-- 1. Verify they're on the correct stage (server-side)
-- 2. Update their saved stage number
-- 3. Set spawn point to this checkpoint
-- 4. Fire UpdateStageDisplay to client
-- 5. Grant stage completion coins

-- Server: CheckpointHandler
local function onCheckpointTouched(checkpoint: BasePart, player: Player)
    local stageName = checkpoint.Parent.Name -- "Stage_001"
    local stageNum = tonumber(stageName:match("%d+"))

    local currentStage = playerData[player.UserId].currentStage
    if stageNum ~= currentStage + 1 then return end -- Must be next stage

    -- Advance player
    playerData[player.UserId].currentStage = stageNum
    player.RespawnLocation = checkpoint -- If it's a SpawnLocation

    -- Grant reward
    grantStageReward(player, stageNum)

    -- Update client
    Remotes.UpdateStageDisplay:FireClient(player, stageNum)
end
```

**Kill Bricks (CollectionService + Debounce):**
```luau
-- Kill brick module using CollectionService tags and per-player debounce
-- Tag all kill bricks in Studio with "KillBrick" via CollectionService
local Players = game:GetService("Players")
local CollectionService = game:GetService("CollectionService")

local debounces: {[number]: boolean} = {}
local DEBOUNCE_COOLDOWN = 0.5

local function setupKillBrick(part: BasePart)
    part.Touched:Connect(function(hit)
        local character = hit.Parent
        if not character then return end
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if not humanoid or humanoid.Health <= 0 then return end
        local player = Players:GetPlayerFromCharacter(character)
        if not player then return end

        local userId = player.UserId
        if debounces[userId] then return end
        debounces[userId] = true

        humanoid.Health = 0

        task.delay(DEBOUNCE_COOLDOWN, function()
            debounces[userId] = nil
        end)
    end)
end

-- Auto-setup all tagged kill bricks (existing and future)
for _, part in CollectionService:GetTagged("KillBrick") do
    setupKillBrick(part)
end

CollectionService:GetInstanceAddedSignal("KillBrick"):Connect(function(part)
    setupKillBrick(part)
end)
```

**Moving Platforms (TweenService with Endpoint Attachments):**
```luau
-- Moving platform system using TweenService (NOT BodyMovers)
-- Each platform has an Attachment child named "EndPoint" defining where it moves to
-- Tag platforms with "MovingPlatform" via CollectionService
local TweenService = game:GetService("TweenService")
local CollectionService = game:GetService("CollectionService")

local DEFAULT_SPEED = 3.0   -- seconds per one-way trip
local PAUSE_TIME = 0.5      -- seconds to pause at each end

local function setupMovingPlatform(platform: BasePart)
    local startPos = platform.Position
    local endAttachment = platform:FindFirstChild("EndPoint")
    if not endAttachment then
        warn(`MovingPlatform {platform:GetFullName()} missing EndPoint attachment`)
        return
    end

    local endPos = endAttachment.WorldPosition
    local speed = platform:GetAttribute("TweenSpeed") or DEFAULT_SPEED
    local pause = platform:GetAttribute("PauseTime") or PAUSE_TIME

    local tweenInfo = TweenInfo.new(speed, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)

    platform.Anchored = true

    task.spawn(function()
        while platform.Parent do
            local tweenForward = TweenService:Create(platform, tweenInfo, { Position = endPos })
            tweenForward:Play()
            tweenForward.Completed:Wait()
            task.wait(pause)

            local tweenBack = TweenService:Create(platform, tweenInfo, { Position = startPos })
            tweenBack:Play()
            tweenBack.Completed:Wait()
            task.wait(pause)
        end
    end)
end

for _, platform in CollectionService:GetTagged("MovingPlatform") do
    setupMovingPlatform(platform)
end

CollectionService:GetInstanceAddedSignal("MovingPlatform"):Connect(function(platform)
    setupMovingPlatform(platform)
end)
```

**Rotating Obstacles (CFrame in Heartbeat with Per-Instance Attributes):**
```luau
-- Rotating obstacles using CFrame manipulation in Heartbeat
-- Each tagged "RotatingObstacle" has attributes:
--   RotateSpeed: number (degrees per second, default 90)
--   RotateAxis: string ("X", "Y", or "Z", default "Y")
local RunService = game:GetService("RunService")
local CollectionService = game:GetService("CollectionService")

local obstacles: {BasePart} = {}

local function registerObstacle(part: BasePart)
    part.Anchored = true
    table.insert(obstacles, part)
end

for _, part in CollectionService:GetTagged("RotatingObstacle") do
    registerObstacle(part)
end

CollectionService:GetInstanceAddedSignal("RotatingObstacle"):Connect(registerObstacle)

RunService.Heartbeat:Connect(function(dt: number)
    for _, part in obstacles do
        if not part.Parent then continue end

        local speed = part:GetAttribute("RotateSpeed") or 90
        local axis = part:GetAttribute("RotateAxis") or "Y"
        local angle = math.rad(speed * dt)

        if axis == "X" then
            part.CFrame *= CFrame.Angles(angle, 0, 0)
        elseif axis == "Y" then
            part.CFrame *= CFrame.Angles(0, angle, 0)
        elseif axis == "Z" then
            part.CFrame *= CFrame.Angles(0, 0, angle)
        end
    end
end)
```

**Speedrun Timer (OrderedDataStore Global Leaderboard):**
```luau
-- ServerScriptService/TimerManager.lua
local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local TimerSync = ReplicatedStorage.Remotes.TimerSync

local leaderboardStore = DataStoreService:GetOrderedDataStore("SpeedrunTimes_v1")

local activeTimers: {[number]: number} = {} -- userId -> start tick

-- Start timer when player touches Stage 1 checkpoint (called from CheckpointHandler)
local function startTimer(player: Player)
    activeTimers[player.UserId] = tick()
    TimerSync:FireClient(player, "START", 0)
end

-- Complete timer when player reaches final stage
local function completeTimer(player: Player)
    local startTime = activeTimers[player.UserId]
    if not startTime then return end

    local elapsed = tick() - startTime
    activeTimers[player.UserId] = nil

    TimerSync:FireClient(player, "COMPLETE", elapsed)

    -- Save to OrderedDataStore (integer milliseconds for sorting)
    local ms = math.floor(elapsed * 1000)
    local success, err = pcall(function()
        leaderboardStore:UpdateAsync("Player_" .. player.UserId, function(oldValue)
            if oldValue == nil or ms < oldValue then
                return ms -- New best time
            end
            return oldValue -- Keep existing better time
        end)
    end)

    if not success then
        warn(`Failed to save speedrun time for {player.Name}: {err}`)
    end
end

-- Sync running timers to clients every frame
RunService.Heartbeat:Connect(function()
    for userId, startTime in activeTimers do
        local player = Players:GetPlayerByUserId(userId)
        if player then
            TimerSync:FireClient(player, "UPDATE", tick() - startTime)
        end
    end
end)

-- Fetch top times for leaderboard display
local function getTopTimes(count: number): {{userId: number, timeMs: number}}
    local results = {}
    local success, pages = pcall(function()
        return leaderboardStore:GetSortedAsync(true, count)
    end)
    if success and pages then
        local data = pages:GetCurrentPage()
        for _, entry in data do
            table.insert(results, {
                userId = tonumber(entry.key:match("%d+")),
                timeMs = entry.value,
            })
        end
    end
    return results
end

return {
    startTimer = startTimer,
    completeTimer = completeTimer,
    getTopTimes = getTopTimes,
}
```

**Stage Leaderboard (leaderstats):**
```luau
-- Setup in ObbyManager or DataManager
local function setupLeaderstats(player: Player, currentStage: number)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"

    local stageValue = Instance.new("IntValue")
    stageValue.Name = "Stage"
    stageValue.Value = currentStage
    stageValue.Parent = leaderstats

    leaderstats.Parent = player
end

local function updateLeaderstats(player: Player, stage: number)
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats then
        local stageValue = leaderstats:FindFirstChild("Stage")
        if stageValue then
            stageValue.Value = stage
        end
    end
end
```

**Spawn Management:**
- When player dies, respawn at their last checkpoint
- Use `Player.RespawnLocation` property pointing to a SpawnLocation
- Or manually set character CFrame in `Humanoid.Died` handler
- Debounce respawns (1-second cooldown minimum)

---

## Monetization Strategy for Obbies

### Gamepasses (One-Time)

| Gamepass | Price (Robux) | Effect |
|----------|---------------|--------|
| Skip Any Stage | 199 | Button to skip current stage (unlimited) |
| 2x Coins | 149 | Double coin rewards per stage |
| Speed Boost | 99 | +16 WalkSpeed permanently |
| Gravity Coil | 249 | Lower gravity for higher jumps |
| Start at Stage 30 | 99 | Unlock early checkpoint |
| Start at Stage 60 | 199 | Unlock mid checkpoint |
| VIP Trail | 49 | Cosmetic trail behind character |

### Dev Products (Repeatable)

| Product | Price (Robux) | Effect |
|---------|---------------|--------|
| Single Skip | 25 | Skip one stage |
| 5-Skip Pack | 99 | Skip 5 stages |
| 10-Skip Pack | 175 | Skip 10 stages |
| 500 Coins | 49 | Instant coins for shop |
| Revive (no reset) | 15 | Don't lose position on death |

### Rewarded Video Ads

- Watch ad for a single stage skip
- Watch ad for 5-minute speed boost
- Watch ad for cosmetic trial

---

## Obby Meta Intelligence (Feb 2026)

### The Problem with Generic Obbies

Basic obbies are THE most oversaturated genre on Roblox. Millions exist. Zero discoverability for new entrants. Low monetization potential.

To succeed with an obby in 2026, you MUST differentiate.

### Differentiation Strategies That Work

1. **Themed obbies with story** - "Escape the volcano," "climb the haunted tower," "race through time periods." Theme gives marketing hooks and retention reasons.

2. **Competitive/multiplayer obbies** - Race against other players in real-time. Creates urgency, social pressure, and "watch me win" streaming appeal.

3. **Procedurally generated obbies** - Like Doors (5B+ visits). Every run is different. Infinite replayability without manual level design.

4. **Obby + another genre** - Obby + horror (flee from monster while doing parkour), obby + tycoon (earn currency from stages, buy upgrades), obby + simulator (collect items during stages).

5. **Difficulty gimmicks** - "World's hardest obby" (niche audience loves the challenge), "1 HP obby" (one touch = death), "upside down obby" (gravity flipped).

6. **Time-limited content** - Weekly stages, seasonal events, community-created stages. Keeps players returning.

### Retention Hooks for Obbies

- **Daily login streak** for bonus coins
- **Death counter** as social flex ("I died 1,247 times but I finished")
- **Speedrun leaderboards** create competitive replayability
- **Cosmetic rewards** per milestone (complete 25/50/75/100 stages)
- **Stage ratings** (players rate difficulty, community engagement)

### Successful Obbies to Study

- **Tower of Hell**: No checkpoints, randomized tower, competitive. 14B+ visits
- **Doors**: Horror + obby + procedural generation. 5B+ visits
- **Mega Easy Obby**: Massive scale, simple execution, good for younger audience

---

## Luau Standards

- Use `task.wait()` not `wait()`
- Use `task.spawn()` not `spawn()`
- Wrap DataStore calls in `pcall`
- Validate all RemoteEvent inputs server-side
- Use type annotations on function signatures
- Use string interpolation: `` `Player {name} reached stage {num}` ``
- Never trust client for stage completion (validate server-side)
- Save on PlayerRemoving AND game:BindToClose
- Debounce all Touched events (minimum 0.1s between fires)

---

## Obstacle Types Reference

### Static Obstacles
- **Kill bricks** - Touch = death. Red colored by convention.
- **Thin walkways** - Narrow paths requiring precision
- **Disappearing platforms** - Visible for N seconds, invisible for N seconds (use Transparency tween)
- **Fake platforms** - Look solid but CanCollide = false (evil but fun)
- **Lava floors** - Large kill zones requiring jumps

### Moving Obstacles
- **Sliding platforms** - TweenService back and forth
- **Spinning bars** - CFrame rotation in Heartbeat
- **Swinging pendulums** - Sine wave rotation
- **Rising/falling pillars** - Vertical tween
- **Moving walls** - Push players off edges

### Interactive Obstacles
- **Buttons** - Step on to open a path temporarily
- **Zip lines** - Touch to ride along a path
- **Trampolines** - Touch to launch upward (set AssemblyLinearVelocity)
- **Conveyor belts** - Surface with velocity pushing in a direction
- **Teleporters** - Touch to move to another position

### Difficulty Scaling

| Stages | Difficulty | Obstacle Types | Platform Min Size |
|--------|-----------|----------------|-------------------|
| 1-20 | Easy | Static platforms, wide gaps, slow kill bricks, forgiving spacing | 6x6 studs |
| 21-50 | Medium | Moving platforms, rotating bars, disappearing blocks, mild timing | 4x4 studs |
| 51-80 | Hard | Fast movers, spinners + kill brick combos, disappearing platforms, wall jumps | 3x3 studs |
| 81-100 | Extreme | Multi-obstacle combos, tight timing windows, small platforms, fake-out paths | 2x2 studs (with neon glow) |

---

## Development Workflow

1. Use robloxstudio MCP to create the Stages folder structure
2. Create the config ModuleScript
3. Create server scripts (ObbyManager, CheckpointHandler, DataManager)
4. Create remote events
5. Create client scripts (HUD, death tracker)
6. Build stage 1-5 manually or via MCP (set positions, create parts)
7. Use roblox-test MCP to play test stages 1-5
8. Iterate on difficulty and feel
9. Build remaining stages in batches
10. Add monetization
11. Add speedrun leaderboard
12. Polish UI, effects, sounds
