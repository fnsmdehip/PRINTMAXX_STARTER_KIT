--[[
    PET FACTORY TYCOON - Game Installer
    Paste this entire script into Roblox Studio's Command Bar and press Enter.
    It creates the complete game structure with all scripts.

    After running:
    1. Click Play to test
    2. Walk onto the yellow pad to claim a plot
    3. Click purchase buttons to buy droppers/upgraders

    To publish:
    1. File > Publish to Roblox
    2. Set up gamepasses in Creator Dashboard
    3. Update gamepass IDs in GameConfig
]]

print("[INSTALLER] Starting Pet Factory Tycoon installation...")

local ServerScriptService = game:GetService("ServerScriptService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local StarterGui = game:GetService("StarterGui")
local Lighting = game:GetService("Lighting")

-- Helper to create script with source
local function createScript(parent, name, className, source)
    -- Remove existing
    local existing = parent:FindFirstChild(name)
    if existing then existing:Destroy() end

    local script = Instance.new(className)
    script.Name = name
    script.Source = source
    script.Parent = parent
    print("[INSTALLER] Created " .. className .. ": " .. name)
    return script
end

-- Helper to create folder
local function createFolder(parent, name)
    local existing = parent:FindFirstChild(name)
    if existing then return existing end
    local folder = Instance.new("Folder")
    folder.Name = name
    folder.Parent = parent
    return folder
end

--------------------------------------------------------------------
-- FOLDER STRUCTURE
--------------------------------------------------------------------
print("[INSTALLER] Creating folder structure...")

local modulesFolder = createFolder(ReplicatedStorage, "Modules")
local remotesFolder = createFolder(ReplicatedStorage, "Remotes")

--------------------------------------------------------------------
-- REMOTE EVENTS
--------------------------------------------------------------------
print("[INSTALLER] Creating remote events...")

local remoteNames = {
    "PurchaseButton", "UpdateCurrency", "HatchEgg", "EquipPet",
    "UpdatePets", "RequestRebirth", "RedeemCode"
}

for _, name in remoteNames do
    local existing = remotesFolder:FindFirstChild(name)
    if existing then existing:Destroy() end
    local remote = Instance.new("RemoteEvent")
    remote.Name = name
    remote.Parent = remotesFolder
end

print("[INSTALLER] Created " .. #remoteNames .. " remote events")

--------------------------------------------------------------------
-- GAME CONFIG (ModuleScript)
--------------------------------------------------------------------
createScript(modulesFolder, "GameConfig", "ModuleScript", [[
local Config = {}

Config.GameName = "Pet Factory Tycoon"
Config.DataStoreKey = "PetFactoryTycoon_v1"

Config.Plots = {
    MaxPlots = 12,
    PlotSize = Vector3.new(80, 1, 80),
    PlotSpacing = 20,
}

Config.Currency = {
    Name = "Coins",
    StartAmount = 0,
    MaxAmount = 999999999,
}

Config.Droppers = {
    { name = "Basic Dropper",    cost = 0,       valuePerDrop = 1,    dropInterval = 2.0,  color = Color3.fromRGB(200, 200, 200) },
    { name = "Copper Dropper",   cost = 500,     valuePerDrop = 5,    dropInterval = 1.8,  color = Color3.fromRGB(184, 115, 51)  },
    { name = "Silver Dropper",   cost = 3000,    valuePerDrop = 20,   dropInterval = 1.6,  color = Color3.fromRGB(192, 192, 192) },
    { name = "Gold Dropper",     cost = 15000,   valuePerDrop = 80,   dropInterval = 1.4,  color = Color3.fromRGB(255, 215, 0)   },
    { name = "Diamond Dropper",  cost = 75000,   valuePerDrop = 350,  dropInterval = 1.2,  color = Color3.fromRGB(185, 242, 255) },
    { name = "Emerald Dropper",  cost = 400000,  valuePerDrop = 1500, dropInterval = 1.0,  color = Color3.fromRGB(80, 200, 120)  },
    { name = "Mythic Dropper",   cost = 2000000, valuePerDrop = 7000, dropInterval = 0.8,  color = Color3.fromRGB(148, 0, 211)   },
}

Config.Upgraders = {
    { name = "Basic Upgrader",    cost = 1000,    multiplier = 1.5, color = Color3.fromRGB(100, 200, 100) },
    { name = "Advanced Upgrader", cost = 10000,   multiplier = 2.0, color = Color3.fromRGB(100, 100, 255) },
    { name = "Elite Upgrader",    cost = 100000,  multiplier = 3.0, color = Color3.fromRGB(255, 100, 100) },
    { name = "Mythic Upgrader",   cost = 1000000, multiplier = 5.0, color = Color3.fromRGB(200, 50, 255)  },
}

Config.Rebirth = {
    BaseCost = 1000000,
    CostMultiplier = 2.5,
    PermanentBonus = 0.25,
    MaxRebirths = 50,
}

Config.Pets = {
    MaxEquipped = 3,
    MaxOwned = 50,
    Eggs = {
        {
            name = "Basic Egg",
            cost = 5000,
            color = Color3.fromRGB(200, 200, 200),
            pets = {
                { name = "Puppy",   rarity = "Common",    weight = 40, multiplier = 1.1 },
                { name = "Kitten",  rarity = "Common",    weight = 30, multiplier = 1.15 },
                { name = "Bunny",   rarity = "Uncommon",  weight = 15, multiplier = 1.3 },
                { name = "Fox",     rarity = "Rare",      weight = 10, multiplier = 1.5 },
                { name = "Dragon",  rarity = "Legendary", weight = 4,  multiplier = 2.0 },
                { name = "Phoenix", rarity = "Mythic",    weight = 1,  multiplier = 3.0 },
            }
        },
        {
            name = "Golden Egg",
            cost = 50000,
            color = Color3.fromRGB(255, 215, 0),
            pets = {
                { name = "Golden Pup",     rarity = "Uncommon",  weight = 35, multiplier = 1.5 },
                { name = "Golden Cat",     rarity = "Uncommon",  weight = 25, multiplier = 1.6 },
                { name = "Golden Fox",     rarity = "Rare",      weight = 20, multiplier = 2.0 },
                { name = "Golden Dragon",  rarity = "Legendary", weight = 15, multiplier = 3.5 },
                { name = "Golden Phoenix", rarity = "Mythic",    weight = 5,  multiplier = 5.0 },
            }
        },
        {
            name = "Mythic Egg",
            cost = 500000,
            color = Color3.fromRGB(148, 0, 211),
            pets = {
                { name = "Shadow Wolf",    rarity = "Rare",      weight = 30, multiplier = 3.0 },
                { name = "Crystal Tiger",  rarity = "Legendary", weight = 30, multiplier = 5.0 },
                { name = "Void Serpent",   rarity = "Legendary", weight = 20, multiplier = 7.0 },
                { name = "Celestial Owl",  rarity = "Mythic",    weight = 15, multiplier = 10.0 },
                { name = "Galaxy Unicorn", rarity = "Mythic",    weight = 5,  multiplier = 20.0 },
            }
        },
    },
    RarityColors = {
        Common    = Color3.fromRGB(180, 180, 180),
        Uncommon  = Color3.fromRGB(0, 200, 0),
        Rare      = Color3.fromRGB(0, 120, 255),
        Legendary = Color3.fromRGB(255, 170, 0),
        Mythic    = Color3.fromRGB(200, 0, 255),
    },
}

Config.Gamepasses = {
    DoubleEarnings = { id = 1704197526, name = "2x Earnings",    price = 199, description = "All earnings doubled permanently" },
    AutoCollect    = { id = 1704265496, name = "Auto-Collect",    price = 149, description = "Resources auto-sell" },
    VIPAccess      = { id = 1704391421, name = "VIP Area",        price = 299, description = "Exclusive high-tier droppers" },
    ExtraSlot      = { id = 1703792075, name = "Extra Pet Slot",  price = 99,  description = "+1 equipped pet slot" },
    InstantRebirth = { id = 1703708188, name = "Instant Rebirth", price = 399, description = "Rebirth without cost" },
}

Config.DevProducts = {
    SmallCash  = { id = 73101791, amount = 10000,   price = 49,  name = "10K Coins" },
    MediumCash = { id = 73101792, amount = 50000,   price = 199, name = "50K Coins" },
    LargeCash  = { id = 73101793, amount = 250000,  price = 799, name = "250K Coins" },
    MegaCash   = { id = 73101794, amount = 1000000, price = 1999, name = "1M Coins" },
}

Config.Codes = {
    LAUNCH2026 = { reward = "coins", amount = 5000,  uses = -1 },
    PETFACTORY = { reward = "coins", amount = 10000, uses = -1 },
    THANKYOU   = { reward = "coins", amount = 25000, uses = -1 },
}

return Config
]])

--------------------------------------------------------------------
-- DATA MANAGER (Script)
--------------------------------------------------------------------
createScript(ServerScriptService, "DataManager", "Script", [[
local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

local playerStore = DataStoreService:GetDataStore(Config.DataStoreKey)
local playerDataCache = {}
local saveLock = {}

local DataManager = {}

local function getDefaultData()
    return {
        coins = Config.Currency.StartAmount,
        rebirths = 0,
        ownedDroppers = {1},
        ownedUpgraders = {},
        pets = {},
        equippedPets = {},
        redeemedCodes = {},
        totalEarned = 0,
        playTime = 0,
        joinCount = 0,
        lastSave = 0,
    }
end

function DataManager.LoadData(player)
    local userId = player.UserId
    local data = nil
    local success, result = pcall(function()
        return playerStore:GetAsync("Player_" .. userId)
    end)
    if success and result then
        local defaults = getDefaultData()
        for key, defaultValue in defaults do
            if result[key] == nil then
                result[key] = defaultValue
            end
        end
        data = result
    else
        if not success then
            warn("[DataManager] Failed to load for " .. player.Name .. ": " .. tostring(result))
        end
        data = getDefaultData()
    end
    data.joinCount += 1
    data.lastSave = os.time()
    playerDataCache[userId] = data

    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    local coinsDisplay = Instance.new("IntValue")
    coinsDisplay.Name = "Coins"
    coinsDisplay.Value = data.coins
    coinsDisplay.Parent = leaderstats
    local rebirthsDisplay = Instance.new("IntValue")
    rebirthsDisplay.Name = "Rebirths"
    rebirthsDisplay.Value = data.rebirths
    rebirthsDisplay.Parent = leaderstats
    leaderstats.Parent = player

    return data
end

function DataManager.SaveData(player)
    local userId = player.UserId
    local data = playerDataCache[userId]
    if not data then return end
    if saveLock[userId] then return end
    saveLock[userId] = true
    data.lastSave = os.time()
    local success, err = pcall(function()
        playerStore:SetAsync("Player_" .. userId, data)
    end)
    if not success then
        warn("[DataManager] Save failed for " .. player.Name .. ": " .. tostring(err))
    end
    saveLock[userId] = false
end

function DataManager.GetData(player)
    return playerDataCache[player.UserId]
end

function DataManager.SetCoins(player, amount)
    local data = playerDataCache[player.UserId]
    if not data then return end
    data.coins = math.clamp(amount, 0, Config.Currency.MaxAmount)
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats then
        local cd = leaderstats:FindFirstChild("Coins")
        if cd then cd.Value = data.coins end
    end
    local remotes = ReplicatedStorage:FindFirstChild("Remotes")
    if remotes then
        local ur = remotes:FindFirstChild("UpdateCurrency")
        if ur then ur:FireClient(player, data.coins) end
    end
end

function DataManager.AddCoins(player, amount)
    local data = playerDataCache[player.UserId]
    if not data then return end
    DataManager.SetCoins(player, data.coins + amount)
    data.totalEarned += amount
end

function DataManager.GetCoins(player)
    local data = playerDataCache[player.UserId]
    return data and data.coins or 0
end

function DataManager.SpendCoins(player, amount)
    local data = playerDataCache[player.UserId]
    if not data then return false end
    if data.coins < amount then return false end
    DataManager.SetCoins(player, data.coins - amount)
    return true
end

function DataManager.SetRebirths(player, count)
    local data = playerDataCache[player.UserId]
    if not data then return end
    data.rebirths = count
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats then
        local rd = leaderstats:FindFirstChild("Rebirths")
        if rd then rd.Value = count end
    end
end

function DataManager.Cleanup(player)
    local userId = player.UserId
    DataManager.SaveData(player)
    task.wait(0.5)
    playerDataCache[userId] = nil
    saveLock[userId] = nil
end

task.spawn(function()
    while true do
        task.wait(120)
        for _, player in Players:GetPlayers() do
            task.spawn(function() DataManager.SaveData(player) end)
        end
    end
end)

Players.PlayerRemoving:Connect(function(player) DataManager.Cleanup(player) end)

game:BindToClose(function()
    for _, player in Players:GetPlayers() do
        DataManager.SaveData(player)
    end
    task.wait(2)
end)

_G.DataManager = DataManager
return DataManager
]])

--------------------------------------------------------------------
-- TYCOON MANAGER (Script) - Simplified for command bar limits
--------------------------------------------------------------------
createScript(ServerScriptService, "TycoonManager", "Script", [[
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

-- Wait for DataManager
repeat task.wait(0.1) until _G.DataManager
local DataManager = _G.DataManager

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local PurchaseRemote = Remotes:WaitForChild("PurchaseButton")

local plotOwners = {}
local plotData = {}
local playerPlots = {}

local PLOT_POSITIONS = {}
for i = 1, Config.Plots.MaxPlots do
    local row = math.floor((i - 1) / 4)
    local col = (i - 1) % 4
    local spacing = Config.Plots.PlotSize.X + Config.Plots.PlotSpacing
    PLOT_POSITIONS[i] = Vector3.new(col * spacing, 0, row * spacing)
end

local function createPlotBase(plotIndex)
    local pos = PLOT_POSITIONS[plotIndex]
    local plotSize = Config.Plots.PlotSize
    local model = Instance.new("Model")
    model.Name = "Plot_" .. plotIndex

    local floor = Instance.new("Part")
    floor.Name = "Floor"
    floor.Size = plotSize
    floor.Position = pos + Vector3.new(plotSize.X / 2, -0.5, plotSize.Z / 2)
    floor.Anchored = true
    floor.Material = Enum.Material.SmoothPlastic
    floor.Color = Color3.fromRGB(120, 180, 120)
    floor.Parent = model

    local collector = Instance.new("Part")
    collector.Name = "Collector"
    collector.Size = Vector3.new(8, 4, 8)
    collector.Position = pos + Vector3.new(plotSize.X - 10, 2, plotSize.Z / 2)
    collector.Anchored = true
    collector.Material = Enum.Material.Neon
    collector.Color = Color3.fromRGB(0, 255, 100)
    collector.Parent = model

    local cg = Instance.new("BillboardGui")
    cg.Size = UDim2.new(0, 200, 0, 50)
    cg.StudsOffset = Vector3.new(0, 4, 0)
    cg.AlwaysOnTop = true
    cg.Parent = collector
    local ct = Instance.new("TextLabel")
    ct.Size = UDim2.new(1, 0, 1, 0)
    ct.BackgroundTransparency = 1
    ct.Text = "SELL"
    ct.TextColor3 = Color3.new(1, 1, 1)
    ct.TextScaled = true
    ct.Font = Enum.Font.GothamBold
    ct.Parent = cg

    local belt = Instance.new("Part")
    belt.Name = "ConveyorBelt"
    local convStart = pos + Vector3.new(15, 1.5, plotSize.Z / 2)
    local convEnd = pos + Vector3.new(plotSize.X - 15, 1.5, plotSize.Z / 2)
    belt.Size = Vector3.new(convEnd.X - convStart.X, 0.5, 6)
    belt.Position = (convStart + convEnd) / 2
    belt.Anchored = true
    belt.Material = Enum.Material.DiamondPlate
    belt.Color = Color3.fromRGB(80, 80, 80)
    belt.Parent = model

    model:SetAttribute("ConveyorStartX", convStart.X)
    model:SetAttribute("ConveyorStartZ", convStart.Z)
    model:SetAttribute("ConveyorEndX", convEnd.X)
    model:SetAttribute("ConveyorEndZ", convEnd.Z)
    model:SetAttribute("PlotIndex", plotIndex)

    local claimPad = Instance.new("Part")
    claimPad.Name = "ClaimPad"
    claimPad.Size = Vector3.new(10, 1, 10)
    claimPad.Position = pos + Vector3.new(plotSize.X / 2, 0.5, plotSize.Z / 2)
    claimPad.Anchored = true
    claimPad.Material = Enum.Material.Neon
    claimPad.Color = Color3.fromRGB(255, 255, 0)
    claimPad.Parent = model

    local cpg = Instance.new("BillboardGui")
    cpg.Size = UDim2.new(0, 300, 0, 80)
    cpg.StudsOffset = Vector3.new(0, 3, 0)
    cpg.AlwaysOnTop = true
    cpg.Parent = claimPad
    local cpt = Instance.new("TextLabel")
    cpt.Size = UDim2.new(1, 0, 1, 0)
    cpt.BackgroundTransparency = 1
    cpt.Text = "STEP ON TO CLAIM"
    cpt.TextColor3 = Color3.new(1, 1, 1)
    cpt.TextScaled = true
    cpt.Font = Enum.Font.GothamBold
    cpt.Parent = cpg

    model.Parent = workspace:FindFirstChild("Plots") or workspace
    return model
end

local function spawnDropper(plot, dropperIndex)
    local plotIndex = plot:GetAttribute("PlotIndex")
    local ps = plotData[plotIndex]
    if not ps then return end
    local dc = Config.Droppers[dropperIndex]
    if not dc then return end

    local pos = PLOT_POSITIONS[plotIndex]
    local dpos = pos + Vector3.new(10, 4, 10 + (dropperIndex - 1) * 8)

    local dropper = Instance.new("Part")
    dropper.Name = "Dropper_" .. dc.name
    dropper.Size = Vector3.new(4, 4, 4)
    dropper.Position = dpos
    dropper.Anchored = true
    dropper.Material = Enum.Material.SmoothPlastic
    dropper.Color = dc.color
    dropper.Parent = plot

    local lg = Instance.new("BillboardGui")
    lg.Size = UDim2.new(0, 200, 0, 40)
    lg.StudsOffset = Vector3.new(0, 3, 0)
    lg.Parent = dropper
    local lt = Instance.new("TextLabel")
    lt.Size = UDim2.new(1, 0, 1, 0)
    lt.BackgroundTransparency = 1
    lt.Text = dc.name
    lt.TextColor3 = Color3.new(1, 1, 1)
    lt.TextScaled = true
    lt.Font = Enum.Font.GothamBold
    lt.Parent = lg

    table.insert(ps.items, dropper)

    local thread = task.spawn(function()
        local csx = plot:GetAttribute("ConveyorStartX")
        local csz = plot:GetAttribute("ConveyorStartZ")
        local cex = plot:GetAttribute("ConveyorEndX")
        local cez = plot:GetAttribute("ConveyorEndZ")

        while plot.Parent and plotOwners[plotIndex] do
            task.wait(dc.dropInterval)
            local orb = Instance.new("Part")
            orb.Name = "ResourceOrb"
            orb.Shape = Enum.PartType.Ball
            orb.Size = Vector3.new(2, 2, 2)
            orb.Position = dpos + Vector3.new(0, -2, 0)
            orb.Anchored = true
            orb.Material = Enum.Material.Neon
            orb.Color = dc.color
            orb:SetAttribute("Value", dc.valuePerDrop)
            orb:SetAttribute("PlotIndex", plotIndex)
            orb.Parent = workspace

            local t1 = TweenService:Create(orb, TweenInfo.new(0.5), {Position = Vector3.new(csx, 1.5, csz)})
            t1:Play()
            t1.Completed:Wait()

            if orb.Parent then
                local t2 = TweenService:Create(orb, TweenInfo.new(3), {Position = Vector3.new(cex, 1.5, cez)})
                t2:Play()
                task.delay(4, function()
                    if orb.Parent then
                        local ownerId = plotOwners[plotIndex]
                        if ownerId then
                            local p = Players:GetPlayerByUserId(ownerId)
                            if p then
                                local v = orb:GetAttribute("Value") or 0
                                local d = DataManager.GetData(p)
                                if d then
                                    local rm = 1 + (d.rebirths * Config.Rebirth.PermanentBonus)
                                    v = math.floor(v * rm)
                                    local pm = 1
                                    if d.equippedPets then
                                        for _, pd in d.equippedPets do pm += (pd.multiplier - 1) end
                                    end
                                    v = math.floor(v * pm)
                                    DataManager.AddCoins(p, v)
                                end
                            end
                        end
                        orb:Destroy()
                    end
                end)
            end
        end
    end)
    table.insert(ps.dropperThreads, thread)
end

local function spawnUpgrader(plot, upgraderIndex)
    local plotIndex = plot:GetAttribute("PlotIndex")
    local ps = plotData[plotIndex]
    if not ps then return end
    local uc = Config.Upgraders[upgraderIndex]
    if not uc then return end

    local csx = plot:GetAttribute("ConveyorStartX")
    local csz = plot:GetAttribute("ConveyorStartZ")
    local cex = plot:GetAttribute("ConveyorEndX")
    local frac = upgraderIndex / (#Config.Upgraders + 1)
    local ux = csx + (cex - csx) * frac

    local upgrader = Instance.new("Part")
    upgrader.Name = "Upgrader_" .. uc.name
    upgrader.Size = Vector3.new(6, 3, 6)
    upgrader.Position = Vector3.new(ux, 1, csz)
    upgrader.Anchored = true
    upgrader.Material = Enum.Material.ForceField
    upgrader.Color = uc.color
    upgrader.CanCollide = false
    upgrader.Parent = plot

    local lg = Instance.new("BillboardGui")
    lg.Size = UDim2.new(0, 200, 0, 40)
    lg.StudsOffset = Vector3.new(0, 3, 0)
    lg.Parent = upgrader
    local lt = Instance.new("TextLabel")
    lt.Size = UDim2.new(1, 0, 1, 0)
    lt.BackgroundTransparency = 1
    lt.Text = uc.name .. " (x" .. uc.multiplier .. ")"
    lt.TextColor3 = Color3.new(1, 1, 1)
    lt.TextScaled = true
    lt.Font = Enum.Font.GothamBold
    lt.Parent = lg

    table.insert(ps.items, upgrader)

    upgrader.Touched:Connect(function(hit)
        if hit.Name ~= "ResourceOrb" then return end
        if hit:GetAttribute("PlotIndex") ~= plotIndex then return end
        if hit:GetAttribute("UpgradedBy_" .. uc.name) then return end
        local cv = hit:GetAttribute("Value") or 0
        hit:SetAttribute("Value", math.floor(cv * uc.multiplier))
        hit:SetAttribute("UpgradedBy_" .. uc.name, true)
    end)
end

local function createButton(plot, itemName, cost, position, itemType, itemIndex)
    local btn = Instance.new("Part")
    btn.Name = "Button_" .. itemName
    btn.Size = Vector3.new(6, 0.5, 6)
    btn.Position = position
    btn.Anchored = true
    btn.Material = Enum.Material.Neon
    btn.Color = Color3.fromRGB(0, 150, 255)
    btn:SetAttribute("ItemType", itemType)
    btn:SetAttribute("ItemIndex", itemIndex)
    btn:SetAttribute("Cost", cost)
    btn:SetAttribute("Purchased", false)
    btn.Parent = plot

    local g = Instance.new("BillboardGui")
    g.Size = UDim2.new(0, 250, 0, 80)
    g.StudsOffset = Vector3.new(0, 2, 0)
    g.AlwaysOnTop = true
    g.Parent = btn

    local nl = Instance.new("TextLabel")
    nl.Size = UDim2.new(1, 0, 0.5, 0)
    nl.BackgroundTransparency = 1
    nl.Text = itemName
    nl.TextColor3 = Color3.new(1, 1, 1)
    nl.TextScaled = true
    nl.Font = Enum.Font.GothamBold
    nl.Parent = g

    local cl = Instance.new("TextLabel")
    cl.Size = UDim2.new(1, 0, 0.5, 0)
    cl.Position = UDim2.new(0, 0, 0.5, 0)
    cl.BackgroundTransparency = 1
    cl.Text = cost .. " Coins"
    cl.TextColor3 = Color3.fromRGB(255, 215, 0)
    cl.TextScaled = true
    cl.Font = Enum.Font.Gotham
    cl.Parent = g
end

local function setupButtons(plot)
    local plotIndex = plot:GetAttribute("PlotIndex")
    local pos = PLOT_POSITIONS[plotIndex]
    for i, d in Config.Droppers do
        if i > 1 then
            createButton(plot, d.name, d.cost, pos + Vector3.new(5, 0.25, 10 + (i - 2) * 10), "dropper", i)
        end
    end
    for i, u in Config.Upgraders do
        createButton(plot, u.name, u.cost, pos + Vector3.new(Config.Plots.PlotSize.X - 25, 0.25, 10 + (i - 1) * 12), "upgrader", i)
    end
end

local function claimPlot(player, plotIndex)
    if plotOwners[plotIndex] then return false end
    if playerPlots[player.UserId] then return false end

    plotOwners[plotIndex] = player.UserId
    playerPlots[player.UserId] = plotIndex
    plotData[plotIndex] = { dropperThreads = {}, items = {} }

    local plots = workspace:FindFirstChild("Plots")
    if not plots then return false end
    local plot = plots:FindFirstChild("Plot_" .. plotIndex)
    if not plot then return false end

    local cp = plot:FindFirstChild("ClaimPad")
    if cp then cp:Destroy() end

    local floor = plot:FindFirstChild("Floor")
    if floor then floor.Color = Color3.fromRGB(80, 140, 80) end

    setupButtons(plot)
    spawnDropper(plot, 1)

    local data = DataManager.GetData(player)
    if data then
        for _, di in data.ownedDroppers do
            if di > 1 then spawnDropper(plot, di) end
        end
        for _, ui in data.ownedUpgraders do
            spawnUpgrader(plot, ui)
        end
    end

    local og = Instance.new("BillboardGui")
    og.Name = "OwnerLabel"
    og.Size = UDim2.new(0, 300, 0, 50)
    og.StudsOffset = Vector3.new(0, 8, 0)
    og.AlwaysOnTop = true
    og.Parent = floor
    local ot = Instance.new("TextLabel")
    ot.Size = UDim2.new(1, 0, 1, 0)
    ot.BackgroundTransparency = 1
    ot.Text = player.Name .. "'s Factory"
    ot.TextColor3 = Color3.fromRGB(255, 255, 100)
    ot.TextScaled = true
    ot.Font = Enum.Font.GothamBold
    ot.Parent = og

    return true
end

local function clearPlot(plotIndex)
    local ps = plotData[plotIndex]
    if ps then
        for _, t in ps.dropperThreads do task.cancel(t) end
        for _, item in ps.items do if item.Parent then item:Destroy() end end
    end
    plotOwners[plotIndex] = nil
    plotData[plotIndex] = nil
    for _, obj in workspace:GetChildren() do
        if obj.Name == "ResourceOrb" and obj:GetAttribute("PlotIndex") == plotIndex then
            obj:Destroy()
        end
    end
end

local function handlePurchase(player, plotIndex, itemType, itemIndex)
    if playerPlots[player.UserId] ~= plotIndex then return end
    local plots = workspace:FindFirstChild("Plots")
    if not plots then return end
    local plot = plots:FindFirstChild("Plot_" .. plotIndex)
    if not plot then return end
    local data = DataManager.GetData(player)
    if not data then return end

    if itemType == "dropper" then
        local dc = Config.Droppers[itemIndex]
        if not dc then return end
        if table.find(data.ownedDroppers, itemIndex) then return end
        if not DataManager.SpendCoins(player, dc.cost) then return end
        table.insert(data.ownedDroppers, itemIndex)
        spawnDropper(plot, itemIndex)
        local b = plot:FindFirstChild("Button_" .. dc.name)
        if b then b.Transparency = 0.8; b:SetAttribute("Purchased", true) end
    elseif itemType == "upgrader" then
        local uc = Config.Upgraders[itemIndex]
        if not uc then return end
        if table.find(data.ownedUpgraders, itemIndex) then return end
        if not DataManager.SpendCoins(player, uc.cost) then return end
        table.insert(data.ownedUpgraders, itemIndex)
        spawnUpgrader(plot, itemIndex)
        local b = plot:FindFirstChild("Button_" .. uc.name)
        if b then b.Transparency = 0.8; b:SetAttribute("Purchased", true) end
    end
end

-- Init
local plotsFolder = Instance.new("Folder")
plotsFolder.Name = "Plots"
plotsFolder.Parent = workspace

for i = 1, Config.Plots.MaxPlots do createPlotBase(i) end

-- Purchase buttons use touch detection on client, server just handles the event
PurchaseRemote.OnServerEvent:Connect(function(player, plotIndex, itemType, itemIndex)
    if typeof(plotIndex) ~= "number" then return end
    if typeof(itemType) ~= "string" then return end
    if typeof(itemIndex) ~= "number" then return end
    handlePurchase(player, plotIndex, itemType, itemIndex)
end)

-- Claim detection
RunService.Heartbeat:Connect(function()
    for _, player in Players:GetPlayers() do
        if playerPlots[player.UserId] then continue end
        local char = player.Character
        if not char then continue end
        local root = char:FindFirstChild("HumanoidRootPart")
        if not root then continue end
        for i = 1, Config.Plots.MaxPlots do
            if plotOwners[i] then continue end
            local plots = workspace:FindFirstChild("Plots")
            if not plots then continue end
            local plot = plots:FindFirstChild("Plot_" .. i)
            if not plot then continue end
            local pad = plot:FindFirstChild("ClaimPad")
            if not pad then continue end
            if (root.Position - pad.Position).Magnitude < 8 then
                claimPlot(player, i)
            end
        end
    end
end)

Players.PlayerAdded:Connect(function(player)
    DataManager.LoadData(player)
end)

for _, player in Players:GetPlayers() do
    task.spawn(function() DataManager.LoadData(player) end)
end

Players.PlayerRemoving:Connect(function(player)
    local pi = playerPlots[player.UserId]
    if pi then clearPlot(pi) end
    playerPlots[player.UserId] = nil
end)
]])

--------------------------------------------------------------------
-- PET SYSTEM (Script)
--------------------------------------------------------------------
createScript(ServerScriptService, "PetSystem", "Script", [[
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

repeat task.wait(0.1) until _G.DataManager
local DataManager = _G.DataManager

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local HatchEgg = Remotes:WaitForChild("HatchEgg")
local EquipPet = Remotes:WaitForChild("EquipPet")
local UpdatePets = Remotes:WaitForChild("UpdatePets")

local function weightedRandom(pets)
    local total = 0
    for _, p in pets do total += p.weight end
    local roll = math.random() * total
    local cum = 0
    for _, p in pets do
        cum += p.weight
        if roll <= cum then return p end
    end
    return pets[#pets]
end

HatchEgg.OnServerEvent:Connect(function(player, eggIndex)
    if typeof(eggIndex) ~= "number" then return end
    if eggIndex < 1 or eggIndex > #Config.Pets.Eggs then return end

    local data = DataManager.GetData(player)
    if not data then HatchEgg:FireClient(player, false, nil); return end

    local egg = Config.Pets.Eggs[eggIndex]
    if not DataManager.SpendCoins(player, egg.cost) then HatchEgg:FireClient(player, false, nil); return end

    if not data.pets then data.pets = {} end
    if #data.pets >= Config.Pets.MaxOwned then HatchEgg:FireClient(player, false, nil); return end

    local result = weightedRandom(egg.pets)
    local petData = {
        name = result.name,
        rarity = result.rarity,
        multiplier = result.multiplier,
        id = result.name .. "_" .. os.time() .. "_" .. math.random(1000, 9999),
    }
    table.insert(data.pets, petData)
    UpdatePets:FireClient(player, data.pets, data.equippedPets)
    HatchEgg:FireClient(player, true, petData)
end)

EquipPet.OnServerEvent:Connect(function(player, petId)
    if typeof(petId) ~= "string" then return end
    local data = DataManager.GetData(player)
    if not data or not data.pets then return end
    if not data.equippedPets then data.equippedPets = {} end

    for i, eq in data.equippedPets do
        if eq.id == petId then
            table.remove(data.equippedPets, i)
            UpdatePets:FireClient(player, data.pets, data.equippedPets)
            return
        end
    end

    if #data.equippedPets >= Config.Pets.MaxEquipped then return end

    for _, pet in data.pets do
        if pet.id == petId then
            table.insert(data.equippedPets, pet)
            UpdatePets:FireClient(player, data.pets, data.equippedPets)
            return
        end
    end
end)

Players.PlayerAdded:Connect(function(player)
    task.wait(2)
    local data = DataManager.GetData(player)
    if data then
        if not data.pets then data.pets = {} end
        if not data.equippedPets then data.equippedPets = {} end
        UpdatePets:FireClient(player, data.pets, data.equippedPets)
    end
end)
]])

--------------------------------------------------------------------
-- REBIRTH MANAGER (Script)
--------------------------------------------------------------------
createScript(ServerScriptService, "RebirthManager", "Script", [[
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

repeat task.wait(0.1) until _G.DataManager
local DataManager = _G.DataManager

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local RequestRebirth = Remotes:WaitForChild("RequestRebirth")

RequestRebirth.OnServerEvent:Connect(function(player)
    local data = DataManager.GetData(player)
    if not data then return end
    if data.rebirths >= Config.Rebirth.MaxRebirths then return end

    local cost = math.floor(Config.Rebirth.BaseCost * (Config.Rebirth.CostMultiplier ^ data.rebirths))
    if data.coins < cost then return end

    data.rebirths += 1
    data.coins = 0
    data.ownedDroppers = {1}
    data.ownedUpgraders = {}

    DataManager.SetCoins(player, 0)
    DataManager.SetRebirths(player, data.rebirths)

    task.spawn(function() DataManager.SaveData(player) end)

    local mult = 1 + (data.rebirths * Config.Rebirth.PermanentBonus)
    RequestRebirth:FireClient(player, true, data.rebirths, mult)
end)
]])

--------------------------------------------------------------------
-- ECONOMY MANAGER (Script)
--------------------------------------------------------------------
createScript(ServerScriptService, "EconomyManager", "Script", [[
local Players = game:GetService("Players")
local MarketplaceService = game:GetService("MarketplaceService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

repeat task.wait(0.1) until _G.DataManager
local DataManager = _G.DataManager

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local RedeemCode = Remotes:WaitForChild("RedeemCode")

MarketplaceService.ProcessReceipt = function(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end
    for _, product in Config.DevProducts do
        if product.id == receiptInfo.ProductId then
            DataManager.AddCoins(player, product.amount)
            return Enum.ProductPurchaseDecision.PurchaseGranted
        end
    end
    return Enum.ProductPurchaseDecision.NotProcessedYet
end

RedeemCode.OnServerEvent:Connect(function(player, code)
    if typeof(code) ~= "string" then return end
    code = string.upper(code)
    local cc = Config.Codes[code]
    if not cc then RedeemCode:FireClient(player, false, "Invalid code"); return end
    local data = DataManager.GetData(player)
    if not data then return end
    if not data.redeemedCodes then data.redeemedCodes = {} end
    if table.find(data.redeemedCodes, code) then RedeemCode:FireClient(player, false, "Already redeemed"); return end
    if cc.reward == "coins" then DataManager.AddCoins(player, cc.amount) end
    table.insert(data.redeemedCodes, code)
    RedeemCode:FireClient(player, true, "Redeemed! +" .. cc.amount .. " Coins")
end)
]])

--------------------------------------------------------------------
-- CLIENT HUD (LocalScript)
--------------------------------------------------------------------
createScript(StarterGui, "TycoonHUD", "LocalScript", [[
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local player = Players.LocalPlayer
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local UpdateCurrency = Remotes:WaitForChild("UpdateCurrency")
local HatchEgg = Remotes:WaitForChild("HatchEgg")
local EquipPet = Remotes:WaitForChild("EquipPet")
local UpdatePets = Remotes:WaitForChild("UpdatePets")
local RequestRebirth = Remotes:WaitForChild("RequestRebirth")
local RedeemCode = Remotes:WaitForChild("RedeemCode")
local PurchaseRemote = Remotes:WaitForChild("PurchaseButton")
local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

local currentCoins = 0
local myPets = {}
local equippedPets = {}

local sg = Instance.new("ScreenGui")
sg.Name = "TycoonHUD"
sg.ResetOnSpawn = false
sg.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
sg.Parent = player:WaitForChild("PlayerGui")

-- Currency display
local cf = Instance.new("Frame")
cf.Size = UDim2.new(0, 300, 0, 60)
cf.Position = UDim2.new(0.5, -150, 0, 10)
cf.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
cf.BackgroundTransparency = 0.3
cf.Parent = sg
Instance.new("UICorner", cf).CornerRadius = UDim.new(0, 12)

local ci = Instance.new("TextLabel")
ci.Size = UDim2.new(0, 50, 1, 0)
ci.BackgroundTransparency = 1
ci.Text = "COINS"
ci.TextSize = 14
ci.TextColor3 = Color3.fromRGB(180, 180, 180)
ci.Font = Enum.Font.Gotham
ci.Parent = cf

local cl = Instance.new("TextLabel")
cl.Name = "CoinLabel"
cl.Size = UDim2.new(1, -60, 1, 0)
cl.Position = UDim2.new(0, 55, 0, 0)
cl.BackgroundTransparency = 1
cl.Text = "0"
cl.TextColor3 = Color3.fromRGB(255, 215, 0)
cl.TextSize = 28
cl.Font = Enum.Font.GothamBold
cl.TextXAlignment = Enum.TextXAlignment.Left
cl.Parent = cf

-- Side buttons
local function mkBtn(name, text, y, color)
    local b = Instance.new("TextButton")
    b.Name = name
    b.Size = UDim2.new(0, 120, 0, 45)
    b.Position = UDim2.new(1, -130, 0, y)
    b.BackgroundColor3 = color
    b.Text = text
    b.TextColor3 = Color3.new(1, 1, 1)
    b.TextSize = 16
    b.Font = Enum.Font.GothamBold
    b.Parent = sg
    Instance.new("UICorner", b).CornerRadius = UDim.new(0, 8)
    return b
end

local petsBtn = mkBtn("PetsBtn", "Pets", 80, Color3.fromRGB(0, 150, 255))
local shopBtn = mkBtn("ShopBtn", "Shop", 135, Color3.fromRGB(0, 200, 100))
local codesBtn = mkBtn("CodesBtn", "Codes", 190, Color3.fromRGB(200, 100, 0))
local rebirthBtn = mkBtn("RebirthBtn", "Rebirth", 245, Color3.fromRGB(200, 0, 255))

-- Simple notification
local function notify(text, color)
    local n = Instance.new("TextLabel")
    n.Size = UDim2.new(0, 350, 0, 60)
    n.Position = UDim2.new(0.5, -175, 0.3, 0)
    n.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
    n.Text = text
    n.TextColor3 = color or Color3.new(1, 1, 1)
    n.TextSize = 18
    n.Font = Enum.Font.GothamBold
    n.TextWrapped = true
    n.Parent = sg
    Instance.new("UICorner", n).CornerRadius = UDim.new(0, 12)
    task.delay(3, function() if n.Parent then n:Destroy() end end)
end

-- Purchase button touch detection (client-side)
local function setupTouchDetection()
    workspace.ChildAdded:Connect(function(child)
        if child:IsA("Folder") and child.Name == "Plots" then
            child.DescendantAdded:Connect(function(desc)
                if desc:IsA("Part") and string.find(desc.Name, "Button_") then
                    desc.Touched:Connect(function(hit)
                        local char = hit.Parent
                        if char ~= player.Character then return end
                        if desc:GetAttribute("Purchased") then return end
                        local plotModel = desc.Parent
                        if plotModel then
                            local pi = plotModel:GetAttribute("PlotIndex")
                            local it = desc:GetAttribute("ItemType")
                            local ii = desc:GetAttribute("ItemIndex")
                            if pi and it and ii then
                                PurchaseRemote:FireServer(pi, it, ii)
                            end
                        end
                    end)
                end
            end)
        end
    end)
end
setupTouchDetection()

-- Events
UpdateCurrency.OnClientEvent:Connect(function(coins)
    currentCoins = coins
    cl.Text = tostring(coins)
end)

UpdatePets.OnClientEvent:Connect(function(pets, equipped)
    myPets = pets or {}
    equippedPets = equipped or {}
end)

HatchEgg.OnClientEvent:Connect(function(success, petData)
    if success and petData then
        local rColor = Config.Pets.RarityColors[petData.rarity] or Color3.new(1, 1, 1)
        notify("Hatched: " .. petData.name .. " (" .. petData.rarity .. ")!", rColor)
    else
        notify("Not enough coins!", Color3.fromRGB(255, 80, 80))
    end
end)

RequestRebirth.OnClientEvent:Connect(function(success, rebirths, mult)
    if success then
        notify("REBIRTH! x" .. string.format("%.2f", mult) .. " earnings!", Color3.fromRGB(200, 0, 255))
    end
end)

RedeemCode.OnClientEvent:Connect(function(success, msg)
    notify(msg, success and Color3.fromRGB(0, 255, 100) or Color3.fromRGB(255, 80, 80))
end)

-- Quick hatch shortcut: press E near eggs area
-- (Full UI panels would be added in polish phase)
petsBtn.MouseButton1Click:Connect(function() HatchEgg:FireServer(1) end)
shopBtn.MouseButton1Click:Connect(function() notify("Shop: Coming in full UI update", Color3.fromRGB(200, 200, 200)) end)
codesBtn.MouseButton1Click:Connect(function() RedeemCode:FireServer("LAUNCH2026") end)
rebirthBtn.MouseButton1Click:Connect(function() RequestRebirth:FireServer() end)
]])

--------------------------------------------------------------------
-- LIGHTING & ATMOSPHERE
--------------------------------------------------------------------
print("[INSTALLER] Setting up atmosphere...")

Lighting.Ambient = Color3.fromRGB(80, 80, 100)
Lighting.OutdoorAmbient = Color3.fromRGB(100, 100, 120)
Lighting.Brightness = 2
Lighting.ClockTime = 14
Lighting.GeographicLatitude = 40

local sky = Lighting:FindFirstChildWhichIsA("Sky")
if not sky then
    sky = Instance.new("Sky")
    sky.Parent = Lighting
end

local atmosphere = Lighting:FindFirstChildWhichIsA("Atmosphere")
if not atmosphere then
    atmosphere = Instance.new("Atmosphere")
    atmosphere.Density = 0.3
    atmosphere.Offset = 0.25
    atmosphere.Color = Color3.fromRGB(199, 170, 107)
    atmosphere.Decay = Color3.fromRGB(92, 60, 13)
    atmosphere.Glare = 0.5
    atmosphere.Haze = 2
    atmosphere.Parent = Lighting
end

local bloom = Lighting:FindFirstChildWhichIsA("BloomEffect")
if not bloom then
    bloom = Instance.new("BloomEffect")
    bloom.Intensity = 0.5
    bloom.Size = 24
    bloom.Threshold = 0.9
    bloom.Parent = Lighting
end

--------------------------------------------------------------------
-- ENABLE HTTP SERVICE (for API calls if needed)
--------------------------------------------------------------------
pcall(function()
    game:GetService("HttpService").HttpEnabled = true
end)

--------------------------------------------------------------------
-- DONE
--------------------------------------------------------------------
print("")
print("========================================")
print("  PET FACTORY TYCOON - INSTALLED!")
print("========================================")
print("")
print("  Scripts created:")
print("    - GameConfig (ModuleScript)")
print("    - DataManager (Script)")
print("    - TycoonManager (Script)")
print("    - PetSystem (Script)")
print("    - RebirthManager (Script)")
print("    - EconomyManager (Script)")
print("    - TycoonHUD (LocalScript)")
print("")
print("  Remote Events: 7")
print("  Atmosphere: Configured")
print("")
print("  >> Click PLAY to test! <<")
print("  >> Walk onto yellow pad to claim plot <<")
print("")
print("  Promo codes: LAUNCH2026, PETFACTORY, THANKYOU")
print("")
print("========================================")
