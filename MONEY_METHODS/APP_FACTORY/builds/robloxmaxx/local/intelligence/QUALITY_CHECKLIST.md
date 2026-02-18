# Roblox Game Quality Checklist

**Purpose:** Score any Roblox game 0-100 before publishing. Claude Code should run this checklist against every game build and report the score. Do not recommend publishing anything below 70. Fix security and data persistence first -- everything else is secondary.

**Usage:** After generating game code, evaluate each item. Mark `[x]` for pass, `[ ]` for fail. Sum points. Report score with specific remediation for any failed items.

---

## Security Score (0-25 points)

Security is non-negotiable. A single exploit can destroy your game's economy in hours. Every point in this section matters.

### [ ] No client-trusted currency/stats modifications (5 pts)

**What this means:** The client (LocalScript) should NEVER directly modify currency, stats, health, damage, or any value that affects gameplay balance. All modifications must go through the server via RemoteEvents/RemoteFunctions, and the server must validate every request.

**Fail example:**
```lua
-- CLIENT-SIDE (BAD -- exploiter can call this directly)
local function addCurrency(amount)
    player.leaderstats.Coins.Value += amount -- EXPLOITABLE
end
```

**Pass example:**
```lua
-- CLIENT: Request the server to add currency
ReplicatedStorage.Events.ClaimReward:FireServer(rewardId)

-- SERVER: Validate and apply
ReplicatedStorage.Events.ClaimReward.OnServerEvent:Connect(function(player, rewardId)
    -- Validate the reward is real and unclaimed
    local reward = RewardDefinitions[rewardId]
    if not reward then return end

    local data = PlayerData[player.UserId]
    if not data then return end

    if data.ClaimedRewards[rewardId] then return end -- Already claimed

    data.Currency += reward.amount
    data.ClaimedRewards[rewardId] = true
    updateLeaderstats(player)
end)
```

### [ ] All RemoteEvents validate inputs server-side (5 pts)

**What this means:** Every RemoteEvent handler must validate that arguments are the correct type, within expected ranges, and that the player is allowed to perform the action.

**Fail example:**
```lua
-- SERVER (BAD -- no validation)
BuyItem.OnServerEvent:Connect(function(player, itemName, quantity)
    giveItem(player, itemName, quantity) -- Exploiter can pass any item name or quantity
end)
```

**Pass example:**
```lua
-- SERVER: Full input validation
BuyItem.OnServerEvent:Connect(function(player, itemName, quantity)
    -- Type check
    if type(itemName) ~= "string" then return end
    if type(quantity) ~= "number" then return end

    -- Range check
    if quantity < 1 or quantity > 99 or quantity ~= math.floor(quantity) then return end

    -- Existence check
    local item = ShopItems[itemName]
    if not item then return end

    -- Affordability check
    local data = PlayerData[player.UserId]
    if not data then return end

    local totalCost = item.price * quantity
    if data.Currency < totalCost then return end

    -- All checks passed: execute
    data.Currency -= totalCost
    for i = 1, quantity do
        table.insert(data.Inventory, itemName)
    end

    updateLeaderstats(player)
end)
```

### [ ] Rate limiting on all RemoteEvent handlers (5 pts)

**What this means:** Exploiters can fire RemoteEvents hundreds of times per second. Every handler needs a cooldown to prevent abuse.

```lua
-- SERVER: Rate limiter module
local RateLimiter = {}
local cooldowns = {} -- {[playerId_eventName] = lastFireTime}

function RateLimiter.check(player: Player, eventName: string, cooldownSeconds: number): boolean
    local key = player.UserId .. "_" .. eventName
    local now = os.clock()
    local lastFire = cooldowns[key]

    if lastFire and (now - lastFire) < cooldownSeconds then
        return false -- Rate limited
    end

    cooldowns[key] = now
    return true
end

-- Clean up on player leave
game.Players.PlayerRemoving:Connect(function(player)
    for key, _ in cooldowns do
        if string.find(key, tostring(player.UserId)) then
            cooldowns[key] = nil
        end
    end
end)

return RateLimiter

-- Usage in any RemoteEvent handler:
local RateLimiter = require(script.Parent.RateLimiter)

BuyItem.OnServerEvent:Connect(function(player, itemName, quantity)
    if not RateLimiter.check(player, "BuyItem", 0.5) then return end -- 0.5 sec cooldown
    -- ... rest of handler
end)
```

### [ ] No exploitable BodyMovers or deprecated physics (3 pts)

**What this means:** Deprecated instances like `BodyVelocity`, `BodyPosition`, `BodyForce` can be exploited for speed hacks and fly hacks. Use modern alternatives and validate movement server-side.

**Deprecated (avoid):** BodyVelocity, BodyPosition, BodyForce, BodyGyro, BodyAngularVelocity
**Modern alternatives:** LinearVelocity, AlignPosition, VectorForce, AlignOrientation, AngularVelocity (all parented to Attachments)

If your game requires character movement validation:
```lua
-- SERVER: Basic speed check (catches most speed exploits)
local MAX_SPEED = 50 -- studs per second, adjust per game

game.Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function(character)
        local hrp = character:WaitForChild("HumanoidRootPart")
        local lastPosition = hrp.Position
        local lastCheck = os.clock()

        task.spawn(function()
            while character and character.Parent do
                task.wait(1)
                local currentPosition = hrp.Position
                local elapsed = os.clock() - lastCheck
                local distance = (currentPosition - lastPosition).Magnitude
                local speed = distance / elapsed

                if speed > MAX_SPEED then
                    -- Teleport back (anti-exploit)
                    hrp.CFrame = CFrame.new(lastPosition)
                    warn(player.Name .. " exceeded speed limit: " .. math.floor(speed))
                end

                lastPosition = currentPosition
                lastCheck = os.clock()
            end
        end)
    end)
end)
```

### [ ] No exposed API keys or secrets (3 pts)

**What this means:** Never put external API keys, webhook URLs, or secrets in any Script or LocalScript. Exploiters can decompile client scripts and extract strings. Server scripts are safer but still not ideal for permanent secrets.

**Rules:**
- No Discord webhook URLs in any script (exploiters will spam your channel)
- No HTTP API keys in client-accessible scripts
- If you need external API calls, route through a proxy server you control
- Use MessagingService for cross-server communication, not external APIs

### [ ] FilterStringAsync on all user-generated text (2 pts)

**What this means:** Any text entered by a player that will be displayed to other players MUST be filtered through Roblox's text filter. This is a Roblox ToS requirement and failure to comply can get your game taken down.

```lua
-- SERVER: Filter user text before displaying
local TextService = game:GetService("TextService")

local function filterText(text: string, senderId: number, recipientId: number): string
    local success, result = pcall(function()
        local textObject = TextService:FilterStringAsync(text, senderId)
        if recipientId then
            return textObject:GetChatForUserAsync(recipientId)
        else
            return textObject:GetNonChatStringForBroadcastAsync()
        end
    end)

    if success then
        return result
    else
        return "###" -- Safe fallback
    end
end
```

### [ ] Anti-speed-hack detection (2 pts)

See the speed check code above. Award 2 pts if implemented. Basic detection is sufficient -- you don't need a full anti-cheat system for most games. The speed check catches 80% of movement exploits.

---

## Data Persistence Score (0-20 points)

Data loss is the fastest way to kill a game. One player loses their progress, tells their friends, and your ratings tank. This section must be perfect.

### [ ] DataStore save on PlayerRemoving (5 pts)

```lua
-- SERVER: Save when player leaves
game.Players.PlayerRemoving:Connect(function(player)
    local data = PlayerData[player.UserId]
    if not data then return end

    local success, err = pcall(function()
        DataStore:SetAsync(tostring(player.UserId), data)
    end)

    if not success then
        warn("Failed to save data for " .. player.Name .. ": " .. tostring(err))
    end

    PlayerData[player.UserId] = nil -- Clean up memory
end)
```

### [ ] DataStore save on BindToClose (5 pts)

**Why this matters:** When the server shuts down (update, crash, Roblox maintenance), PlayerRemoving may not fire for all players. BindToClose gives you 30 seconds to save everyone.

```lua
-- SERVER: Save ALL players on server shutdown
game:BindToClose(function()
    local saveTasks = {}

    for _, player in game.Players:GetPlayers() do
        local data = PlayerData[player.UserId]
        if data then
            table.insert(saveTasks, task.spawn(function()
                local success, err = pcall(function()
                    DataStore:SetAsync(tostring(player.UserId), data)
                end)
                if not success then
                    warn("BindToClose save failed for " .. player.Name .. ": " .. tostring(err))
                end
            end))
        end
    end

    -- Wait for all saves (BindToClose gives 30 seconds)
    task.wait(5) -- Give time for all pcalls to complete
end)
```

### [ ] pcall around ALL DataStore operations (3 pts)

DataStore calls can fail (rate limits, network issues, Roblox outages). Every single DataStore call must be wrapped in pcall. No exceptions.

```lua
-- CORRECT: Always pcall
local success, result = pcall(function()
    return DataStore:GetAsync(key)
end)

if success then
    -- Use result
else
    -- Handle error (use defaults, retry, warn)
    warn("DataStore error: " .. tostring(result))
end
```

### [ ] Default data for new players (3 pts)

First-time players have no DataStore entry. Your game must handle this gracefully with a default data template.

```lua
-- SERVER: Default data template
local DEFAULT_DATA = {
    Currency = 100,         -- Starting currency
    Level = 1,
    XP = 0,
    Inventory = {},
    Gamepasses = {},
    StarterPackClaimed = false,
    JoinTime = 0,           -- Will be set on first join
    TotalPlayTime = 0,
    Version = 1,            -- For future data migrations
}

local function loadPlayerData(player: Player)
    local success, savedData = pcall(function()
        return DataStore:GetAsync(tostring(player.UserId))
    end)

    local data
    if success and savedData then
        -- Merge with defaults (handles new fields added in updates)
        data = {}
        for key, defaultValue in DEFAULT_DATA do
            data[key] = if savedData[key] ~= nil then savedData[key] else defaultValue
        end
    else
        -- New player or load failed: use defaults
        data = table.clone(DEFAULT_DATA)
        data.JoinTime = os.time()
    end

    PlayerData[player.UserId] = data
    return data
end
```

### [ ] Data versioning for migrations (2 pts)

When you update your game, data structure may change. Version numbers let you migrate old data safely.

```lua
-- SERVER: Data migration system
local CURRENT_VERSION = 2

local function migrateData(data)
    if not data.Version then data.Version = 1 end

    -- v1 -> v2: Added TotalPlayTime field
    if data.Version < 2 then
        data.TotalPlayTime = 0
        data.Version = 2
    end

    -- v2 -> v3: (future migration goes here)
    -- if data.Version < 3 then
    --     data.NewField = "default"
    --     data.Version = 3
    -- end

    return data
end
```

### [ ] Session locking to prevent data duplication (2 pts)

If a player joins a new server before the old server finishes saving, data can be duplicated or rolled back. Session locking prevents this.

```lua
-- SERVER: Simple session lock using MemoryStore
local MemoryStoreService = game:GetService("MemoryStoreService")
local sessionMap = MemoryStoreService:GetSortedMap("SessionLocks")

local function acquireSessionLock(userId: number): boolean
    local key = tostring(userId)

    local success, currentLock = pcall(function()
        return sessionMap:GetAsync(key)
    end)

    if success and currentLock then
        -- Another server has this player's data locked
        -- Wait briefly for it to release
        task.wait(5)

        -- Retry
        success, currentLock = pcall(function()
            return sessionMap:GetAsync(key)
        end)

        if success and currentLock then
            return false -- Still locked, reject
        end
    end

    -- Set our lock (expires in 30 minutes as safety valve)
    pcall(function()
        sessionMap:SetAsync(key, game.JobId, 1800)
    end)

    return true
end

local function releaseSessionLock(userId: number)
    pcall(function()
        sessionMap:RemoveAsync(tostring(userId))
    end)
end
```

---

## Monetization Coverage Score (0-25 points)

Revenue doesn't happen by accident. Every point here is money left on the table.

### [ ] At least 2 gamepasses configured (5 pts)

Minimum viable monetization: a "2x Earnings" gamepass and a "VIP" gamepass. See MONETIZATION_ENGINE.md for pricing and implementation.

**Check:**
- Gamepasses created in Game Settings > Monetization
- MarketplaceService:UserOwnsGamePassAsync checks in server code
- Benefits actually apply in gameplay (not just cosmetic promises with no code behind them)

### [ ] At least 3 developer products configured (5 pts)

Minimum: Small currency pack, Medium currency pack, one consumable boost. Developer products are repeatable revenue -- they generate more long-term income than gamepasses.

**Check:**
- Developer products created in Game Settings > Monetization
- ProcessReceipt callback implemented and tested
- Products actually grant what they promise

### [ ] Gamepass benefits clearly visible in-game (3 pts)

Players won't buy what they can't see. Every gamepass benefit must be visible to both the owner AND other players.

**Visibility checklist:**
- 2x Earnings: Bonus amount shown in different color when earning currency
- VIP: Chat tag, particle effect, exclusive area entrance visible to all
- Starter Pack: Exclusive item/tool visually distinct from free items

### [ ] Purchase prompts at natural decision points (3 pts)

Prompts should appear when the player WANTS something, not randomly. See MONETIZATION_ENGINE.md "Purchase Prompt Placement" section.

**Check that prompts appear:**
- After death (revive offer)
- At progression wall (skip or grind)
- When viewing another player's paid item
- In the shop UI (accessible from main HUD)

### [ ] "Owned" state handling for gamepasses (3 pts)

When a player already owns a gamepass, the UI must reflect it. No "buy" button for owned passes. Show "OWNED" with a checkmark instead.

```lua
-- CLIENT: Check ownership and update shop UI
local function updateGamepassButton(button, gamepassId, player)
    local success, owned = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, gamepassId)
    end)

    if success and owned then
        button.Text = "OWNED"
        button.BackgroundColor3 = Color3.fromRGB(50, 180, 50) -- Green
        button.Active = false
    else
        button.Text = "BUY"
        button.BackgroundColor3 = Color3.fromRGB(60, 120, 220) -- Blue
        button.Active = true
    end
end
```

### [ ] MarketplaceService ProcessReceipt implemented correctly (3 pts)

ProcessReceipt is the most critical monetization callback. If it fails, the player loses their Robux and gets nothing. This must be bulletproof.

**Requirements:**
- Returns `PurchaseGranted` ONLY after data is saved successfully
- Returns `NotProcessedYet` on any failure (Roblox will retry)
- Handles ALL developer product IDs
- Saves to DataStore BEFORE returning PurchaseGranted

### [ ] Rewarded ad integration (3 pts)

Free revenue from players who won't spend Robux. See MONETIZATION_ENGINE.md for implementation. Not all games qualify -- requires Roblox's Immersive Ads program enrollment.

**Check:**
- Ad placement in natural break point
- Reward amount is 20-30% of cheapest dev product
- Daily view limit implemented (3-5 per player)

---

## Engagement Loop Score (0-15 points)

If players don't stay, they don't pay. These mechanics create the "just one more minute" effect.

### [ ] Core gameplay loop under 60 seconds (3 pts)

The fundamental action cycle must complete in under 60 seconds. Examples:
- Tycoon: Collect earnings > Buy upgrade > See production increase (30 sec)
- Simulator: Click/interact > Earn currency > Buy next tier (20-45 sec)
- Farming: Plant > Wait/tend > Harvest > Sell (45-60 sec with short timers)

If your core loop takes longer than 60 seconds, players lose interest before the first dopamine hit.

### [ ] Clear progression visible at all times (3 pts)

Players must always know:
- Where they are (level, rank, stage)
- What they're working toward (next unlock, next milestone)
- How far they have to go (progress bar, percentage)

```lua
-- CLIENT: Always-visible progression HUD
-- Minimum: Level + XP bar + next unlock preview
local function updateProgressionHUD(data)
    local hud = PlayerGui.HUD.Progression
    hud.LevelText.Text = "Level " .. data.Level
    hud.XPBar.Size = UDim2.new(data.XP / xpToNextLevel(data.Level), 0, 1, 0)
    hud.NextUnlock.Text = "Next: " .. getNextUnlock(data.Level).Name
end
```

### [ ] Variable ratio rewards (random drops) (3 pts)

Slot machine psychology. Variable rewards are more addictive than fixed rewards. Every interaction should have a CHANCE of something rare happening.

**Implementation:** Use weighted random with visible rarity tiers.
```lua
-- SERVER: Weighted random drop system
local DropTable = {
    { name = "Common Seed",    weight = 60, rarity = "Common",    color = Color3.fromRGB(200, 200, 200) },
    { name = "Uncommon Seed",  weight = 25, rarity = "Uncommon",  color = Color3.fromRGB(30, 200, 30) },
    { name = "Rare Seed",      weight = 10, rarity = "Rare",      color = Color3.fromRGB(30, 100, 255) },
    { name = "Epic Seed",      weight = 4,  rarity = "Epic",      color = Color3.fromRGB(180, 60, 255) },
    { name = "Legendary Seed", weight = 1,  rarity = "Legendary", color = Color3.fromRGB(255, 200, 0) },
}

local function rollDrop(): typeof(DropTable[1])
    local totalWeight = 0
    for _, item in DropTable do
        totalWeight += item.weight
    end

    local roll = math.random(1, totalWeight)
    local cumulative = 0

    for _, item in DropTable do
        cumulative += item.weight
        if roll <= cumulative then
            return item
        end
    end

    return DropTable[1] -- Fallback to common
end
```

### [ ] Idle/offline progression element (3 pts)

Give players a reason to come back. When they return after being offline, they should find something accumulated (currency, crops grown, resources collected). This drives D1 and D7 retention.

```lua
-- SERVER: Calculate offline earnings on join
local function calculateOfflineEarnings(data): number
    if not data.LastSaveTime then return 0 end

    local secondsOffline = os.time() - data.LastSaveTime
    local hoursOffline = math.min(secondsOffline / 3600, 8) -- Cap at 8 hours

    local earningsPerHour = data.Level * 10 -- Scale with progression
    local offlineMultiplier = 0.5 -- 50% of active earnings (incentivize playing)

    -- Gamepass: full offline earnings instead of 50%
    -- (Check ownership server-side)

    return math.floor(hoursOffline * earningsPerHour * offlineMultiplier)
end

-- On player join:
local offlineEarnings = calculateOfflineEarnings(data)
if offlineEarnings > 0 then
    data.Currency += offlineEarnings
    -- Show "Welcome back! You earned X while away" popup
    ReplicatedStorage.Events.ShowOfflineEarnings:FireClient(player, offlineEarnings)
end
```

### [ ] Social features (trading, leaderboard, co-op) (3 pts)

At least ONE social feature. Leaderboards are the minimum. Trading is the gold standard. Social features turn single-player games into multiplayer retention engines.

**Minimum viable social:**
```lua
-- SERVER: Global leaderboard (updates every 60 seconds)
local OrderedDataStore = DataStoreService:GetOrderedDataStore("GlobalLeaderboard")

local function updateLeaderboard()
    -- Save current player scores
    for _, player in game.Players:GetPlayers() do
        local data = PlayerData[player.UserId]
        if data then
            pcall(function()
                OrderedDataStore:SetAsync(tostring(player.UserId), data.TotalEarnings)
            end)
        end
    end
end

-- Run every 60 seconds
task.spawn(function()
    while true do
        task.wait(60)
        updateLeaderboard()
    end
end)
```

---

## Mobile Compatibility Score (0-15 points)

60-70% of Roblox players are on mobile. If your game doesn't work on a phone, you're losing the majority of your audience and revenue.

### [ ] Touch-friendly UI with buttons 44+ pixels (5 pts)

Apple's Human Interface Guidelines recommend 44x44pt minimum tap targets. On Roblox, this translates to buttons that are at least 44 pixels in the smallest dimension. Test by tapping with your thumb, not your mouse cursor.

**Common failures:**
- Shop buttons too small to tap accurately
- Close buttons in corners that overlap with Roblox UI
- Inventory grid items too tightly packed

### [ ] Scales to phone screens without overlap (3 pts)

UI must work at 16:9 (desktop), 9:16 (phone portrait, rare on Roblox), and 19.5:9 (modern phones). Test with Roblox Studio's device emulator.

**Key rule:** Never use absolute pixel positioning. Use Scale (0-1) for positioning, Offset only for padding. Use UIAspectRatioConstraint for elements that must maintain proportions.

```lua
-- CORRECT: Scale-based positioning
local frame = Instance.new("Frame")
frame.Position = UDim2.new(0.5, 0, 0.5, 0)      -- Center of screen (any size)
frame.Size = UDim2.new(0.3, 0, 0.4, 0)            -- 30% width, 40% height
frame.AnchorPoint = Vector2.new(0.5, 0.5)          -- Centered

-- WRONG: Pixel-based positioning (breaks on different screens)
frame.Position = UDim2.new(0, 500, 0, 300)         -- Only works on one resolution
frame.Size = UDim2.new(0, 400, 0, 300)             -- Fixed pixels
```

### [ ] No keyboard-only inputs required (3 pts)

Mobile players don't have keyboards. Every action must be accessible via touch.

**Check:**
- No gameplay actions bound only to keyboard keys
- All keybinds have touch button equivalents
- ContextActionService used with `CreateTouchButton = true` for mobile controls
- No typed chat required for gameplay (chat is supplementary, not required)

```lua
-- Correct: Touch-compatible action binding
local ContextActionService = game:GetService("ContextActionService")

ContextActionService:BindAction(
    "Sprint",
    handleSprint,
    true, -- createTouchButton = true (adds mobile button)
    Enum.KeyCode.LeftShift
)
```

### [ ] Performance under 100 instances in workspace view distance (2 pts)

Mobile devices have limited memory and processing power. Keep the visible workspace lean:
- Use StreamingEnabled (loads/unloads parts based on distance)
- Limit particle effects (reduce MaxDistance, lower Rate on mobile)
- Use MeshParts instead of many small Parts for complex objects
- Target 60 FPS on mid-range phones (iPhone 12 / Samsung Galaxy S21 equivalent)

### [ ] Loading time under 15 seconds on mobile (2 pts)

If your game takes more than 15 seconds to load on mobile, you lose 30-40% of players before they even see the game. Roblox shows a loading bar -- players compare it to other games.

**Optimization:**
- Keep total asset size under 100MB
- Use asset streaming (don't load everything at once)
- Minimize script count (fewer scripts = faster startup)
- Compress textures (512x512 max for most game textures, 1024x1024 for hero images only)

---

## Total Score Interpretation

### Scoring

| Category | Max Points | Your Score |
|----------|-----------|------------|
| Security | 25 | __ / 25 |
| Data Persistence | 20 | __ / 20 |
| Monetization Coverage | 25 | __ / 25 |
| Engagement Loop | 15 | __ / 15 |
| Mobile Compatibility | 15 | __ / 15 |
| **TOTAL** | **100** | **__ / 100** |

### Score Interpretation

| Score | Verdict | Action |
|-------|---------|--------|
| 90-100 | Ship it. This will make money. | Publish, sponsor, monitor metrics for 48 hours. |
| 70-89 | Good foundation. Fix marked items before pushing hard. | Fix failed items in security and persistence first. Then publish. |
| 50-69 | Needs work. Not ready for public. | Focus exclusively on security (0-25) and data persistence (0-20) sections. Those two alone are 45 points. |
| Below 50 | Major gaps. Do not publish. | Start with the sections that scored 0 and work up. Publishing in this state will get negative reviews that tank future discovery. |

### Priority Fix Order (When Score is Below 70)

1. **DataStore save on PlayerRemoving + BindToClose** (10 pts) -- Data loss is game-killing
2. **No client-trusted modifications** (5 pts) -- Exploits destroy economy
3. **RemoteEvent input validation** (5 pts) -- Exploits destroy economy
4. **At least 2 gamepasses + 3 dev products** (10 pts) -- No monetization = no revenue
5. **ProcessReceipt implementation** (3 pts) -- Broken purchases = refund requests
6. **Mobile-friendly UI** (5 pts) -- 60-70% of your audience
7. **Core loop under 60 seconds** (3 pts) -- Retention foundation
8. Everything else

### Pre-Publish Final Checks (Beyond the Score)

These don't have point values but will tank your game if missed:

- [ ] Game icon is eye-catching at thumbnail size (bright colors, character, action)
- [ ] Game title includes genre keyword ("Tycoon," "Simulator," "Garden")
- [ ] Game description includes keywords players search for
- [ ] Thumbnail shows actual gameplay (not misleading)
- [ ] Game is set to correct genre in Game Settings
- [ ] Social links configured (Discord, group)
- [ ] Game is tested with 2+ players for multiplayer issues
- [ ] No placeholder text visible ("Lorem ipsum," "TODO," "Test")
- [ ] All free models scanned for backdoors (require() calls to unknown IDs)
- [ ] Sound effects and music licensed or from Roblox library
