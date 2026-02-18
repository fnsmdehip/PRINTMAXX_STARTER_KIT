--[[
	TycoonManager.lua
	Core game logic for AI Factory Tycoon

	Handles:
	- Player join/leave (spawn tycoon, cleanup)
	- Tycoon ownership (assign unclaimed tycoon to player)
	- Money collection (touch droppers to collect)
	- Upgrade purchasing (buttons unlock next items)
	- Progress saving (DataStoreService)
	- Leaderboard (show top earners)

	Architecture:
	- Each tycoon = Model in Workspace.Tycoons folder
	- Each tycoon has Owner ObjectValue pointing to player
	- Player data stored in DataStoreService (cash, upgrades purchased)
	- Upgrades are sequential (Button1 → Button2 → Button3, etc)
--]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Import config module
local TycoonConfig = require(ReplicatedStorage.TycoonConfig)

-- DataStore for saving player progress
local PlayerDataStore = DataStoreService:GetDataStore("PlayerData_v1")

-- Track active tycoons (tycoonModel → ownerPlayer)
local activeTycoons = {}

-- Player data cache (userId → {cash, upgradesPurchased})
local playerDataCache = {}

--[[
	Get or create default player data
--]]
local function getDefaultPlayerData()
	return {
		cash = TycoonConfig.STARTING_CASH,
		upgradesPurchased = {} -- array of upgrade IDs purchased
	}
end

--[[
	Load player data from DataStore
	Returns: {cash, upgradesPurchased} or default data if new player
--]]
local function loadPlayerData(player)
	local userId = player.UserId
	local success, data = pcall(function()
		return PlayerDataStore:GetAsync(userId)
	end)

	if success and data then
		print("[TycoonManager] Loaded data for", player.Name, "Cash:", data.cash)
		return data
	else
		print("[TycoonManager] New player or load failed:", player.Name, "Using defaults")
		return getDefaultPlayerData()
	end
end

--[[
	Save player data to DataStore
--]]
local function savePlayerData(player)
	local userId = player.UserId
	local data = playerDataCache[userId]

	if not data then
		warn("[TycoonManager] No data to save for", player.Name)
		return
	end

	local success, err = pcall(function()
		PlayerDataStore:SetAsync(userId, data)
	end)

	if success then
		print("[TycoonManager] Saved data for", player.Name, "Cash:", data.cash)
	else
		warn("[TycoonManager] Save failed for", player.Name, "Error:", err)
	end
end

--[[
	Setup leaderboard (cash display in player list)
--]]
local function setupLeaderboard(player)
	local leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	leaderstats.Parent = player

	local cash = Instance.new("IntValue")
	cash.Name = "Cash"
	cash.Value = playerDataCache[player.UserId].cash
	cash.Parent = leaderstats

	-- Update cache when leaderboard changes (for easy sync)
	cash.Changed:Connect(function(newValue)
		if playerDataCache[player.UserId] then
			playerDataCache[player.UserId].cash = newValue
		end
	end)
end

--[[
	Find unclaimed tycoon
	Returns: tycoon Model or nil
--]]
local function findUnclaimedTycoon()
	local tycoons = workspace:FindFirstChild("Tycoons")
	if not tycoons then
		warn("[TycoonManager] No Tycoons folder in workspace")
		return nil
	end

	for _, tycoon in ipairs(tycoons:GetChildren()) do
		local ownerValue = tycoon:FindFirstChild("Owner")
		if ownerValue and ownerValue.Value == nil then
			return tycoon
		end
	end

	return nil
end

--[[
	Claim tycoon for player
--]]
local function claimTycoon(player, tycoon)
	local ownerValue = tycoon:FindFirstChild("Owner")
	if not ownerValue then
		warn("[TycoonManager] Tycoon missing Owner ObjectValue:", tycoon.Name)
		return
	end

	ownerValue.Value = player
	activeTycoons[tycoon] = player

	print("[TycoonManager]", player.Name, "claimed", tycoon.Name)

	-- Teleport player to spawn point
	local spawn = tycoon:FindFirstChild("SpawnPoint")
	if spawn and player.Character then
		player.Character:MoveTo(spawn.Position)
	end

	-- Setup upgrade buttons
	setupUpgradeButtons(player, tycoon)

	-- Setup money dropper
	setupMoneyDropper(player, tycoon)

	-- Restore purchased upgrades
	restorePurchasedUpgrades(player, tycoon)
end

--[[
	Setup upgrade buttons (touch to purchase)
--]]
local function setupUpgradeButtons(player, tycoon)
	local buttons = tycoon:FindFirstChild("Buttons")
	if not buttons then return end

	for _, button in ipairs(buttons:GetChildren()) do
		if button:IsA("Part") or button:IsA("MeshPart") then
			local upgradeId = button.Name -- e.g. "Button1", "Button2"
			local config = TycoonConfig.UPGRADES[upgradeId]

			if not config then
				warn("[TycoonManager] No config for upgrade:", upgradeId)
				continue
			end

			-- Create BillboardGui showing price
			local billboard = Instance.new("BillboardGui")
			billboard.Size = UDim2.new(4, 0, 2, 0)
			billboard.Adornee = button
			billboard.AlwaysOnTop = true
			billboard.Parent = button

			local textLabel = Instance.new("TextLabel")
			textLabel.Size = UDim2.new(1, 0, 1, 0)
			textLabel.BackgroundTransparency = 0.5
			textLabel.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
			textLabel.TextColor3 = Color3.fromRGB(0, 255, 0)
			textLabel.TextScaled = true
			textLabel.Text = config.name .. "\n$" .. config.price
			textLabel.Font = Enum.Font.GothamBold
			textLabel.Parent = billboard

			-- Touch to purchase
			button.Touched:Connect(function(hit)
				local character = hit.Parent
				local hitPlayer = Players:GetPlayerFromCharacter(character)

				if hitPlayer ~= player then return end
				if not playerDataCache[player.UserId] then return end

				local data = playerDataCache[player.UserId]

				-- Check if already purchased
				if table.find(data.upgradesPurchased, upgradeId) then
					return
				end

				-- Check prerequisites (previous upgrade must be purchased)
				if config.prerequisite then
					if not table.find(data.upgradesPurchased, config.prerequisite) then
						return -- prerequisite not met
					end
				end

				-- Check cash
				local leaderstats = player:FindFirstChild("leaderstats")
				local cashValue = leaderstats and leaderstats:FindFirstChild("Cash")

				if not cashValue or cashValue.Value < config.price then
					return -- not enough cash
				end

				-- Purchase upgrade
				cashValue.Value = cashValue.Value - config.price
				table.insert(data.upgradesPurchased, upgradeId)

				-- Hide button
				button.Transparency = 1
				button.CanCollide = false
				if billboard then billboard.Enabled = false end

				-- Spawn the actual upgrade model
				spawnUpgrade(tycoon, config)

				print("[TycoonManager]", player.Name, "purchased", upgradeId)
			end)
		end
	end
end

--[[
	Spawn upgrade model into tycoon
--]]
local function spawnUpgrade(tycoon, config)
	local purchases = tycoon:FindFirstChild("Purchases")
	if not purchases then
		purchases = Instance.new("Folder")
		purchases.Name = "Purchases"
		purchases.Parent = tycoon
	end

	-- Clone model from ReplicatedStorage
	local upgradeTemplate = ReplicatedStorage.UpgradeModels:FindFirstChild(config.modelName)
	if not upgradeTemplate then
		warn("[TycoonManager] Missing upgrade model:", config.modelName)
		return
	end

	local upgradeClone = upgradeTemplate:Clone()
	upgradeClone.Parent = purchases

	-- Position at specified location (relative to tycoon base)
	local base = tycoon:FindFirstChild("Base")
	if base and config.position then
		upgradeClone:SetPrimaryPartCFrame(base.CFrame * CFrame.new(config.position))
	end
end

--[[
	Setup money dropper (spawns cash periodically)
--]]
local function setupMoneyDropper(player, tycoon)
	local collector = tycoon:FindFirstChild("Collector")
	if not collector then
		warn("[TycoonManager] Tycoon missing Collector part:", tycoon.Name)
		return
	end

	-- Spawn money drop periodically
	task.spawn(function()
		while activeTycoons[tycoon] == player do
			task.wait(TycoonConfig.MONEY_SPAWN_RATE)

			-- Create money part
			local money = Instance.new("Part")
			money.Name = "MoneyCoin"
			money.Size = Vector3.new(1, 0.5, 1)
			money.BrickColor = BrickColor.new("Bright yellow")
			money.Material = Enum.Material.Neon
			money.CanCollide = false
			money.Anchored = false
			money.Position = collector.Position + Vector3.new(0, 5, 0)
			money.Parent = workspace

			-- Make it collectible
			money.Touched:Connect(function(hit)
				local character = hit.Parent
				local hitPlayer = Players:GetPlayerFromCharacter(character)

				if hitPlayer ~= player then return end

				local leaderstats = player:FindFirstChild("leaderstats")
				local cashValue = leaderstats and leaderstats:FindFirstChild("Cash")

				if cashValue then
					local moneyAmount = TycoonConfig.BASE_MONEY_AMOUNT

					-- Apply multipliers from gamepasses
					local GamepassManager = require(script.Parent.GamepassManager)
					if GamepassManager.hasGamepass(player, "VIP") then
						moneyAmount = moneyAmount * 2
					end

					cashValue.Value = cashValue.Value + moneyAmount
					money:Destroy()
				end
			end)

			-- Auto-destroy after 10 seconds
			task.delay(10, function()
				if money.Parent then
					money:Destroy()
				end
			end)
		end
	end)
end

--[[
	Restore purchased upgrades (on player rejoin)
--]]
local function restorePurchasedUpgrades(player, tycoon)
	local data = playerDataCache[player.UserId]
	if not data then return end

	for _, upgradeId in ipairs(data.upgradesPurchased) do
		local config = TycoonConfig.UPGRADES[upgradeId]
		if config then
			-- Hide button
			local buttons = tycoon:FindFirstChild("Buttons")
			if buttons then
				local button = buttons:FindFirstChild(upgradeId)
				if button then
					button.Transparency = 1
					button.CanCollide = false
					local billboard = button:FindFirstChild("BillboardGui")
					if billboard then billboard.Enabled = false end
				end
			end

			-- Spawn upgrade model
			spawnUpgrade(tycoon, config)
		end
	end
end

--[[
	Unclaim tycoon (player left)
--]]
local function unclaimTycoon(player, tycoon)
	local ownerValue = tycoon:FindFirstChild("Owner")
	if ownerValue then
		ownerValue.Value = nil
	end

	activeTycoons[tycoon] = nil

	-- Clear purchased models
	local purchases = tycoon:FindFirstChild("Purchases")
	if purchases then
		purchases:ClearAllChildren()
	end

	-- Reset buttons
	local buttons = tycoon:FindFirstChild("Buttons")
	if buttons then
		for _, button in ipairs(buttons:GetChildren()) do
			button.Transparency = 0
			button.CanCollide = true
			local billboard = button:FindFirstChild("BillboardGui")
			if billboard then billboard.Enabled = true end
		end
	end

	print("[TycoonManager]", player.Name, "unclaimed", tycoon.Name)
end

--[[
	Player joined
--]]
Players.PlayerAdded:Connect(function(player)
	print("[TycoonManager]", player.Name, "joined")

	-- Load data
	local data = loadPlayerData(player)
	playerDataCache[player.UserId] = data

	-- Setup leaderboard
	setupLeaderboard(player)

	-- Wait for character
	player.CharacterAdded:Wait()

	-- Claim tycoon
	local tycoon = findUnclaimedTycoon()
	if tycoon then
		claimTycoon(player, tycoon)
	else
		warn("[TycoonManager] No unclaimed tycoons available for", player.Name)
	end
end)

--[[
	Player left
--]]
Players.PlayerRemoving:Connect(function(player)
	print("[TycoonManager]", player.Name, "left")

	-- Save data
	savePlayerData(player)

	-- Unclaim tycoon
	for tycoon, owner in pairs(activeTycoons) do
		if owner == player then
			unclaimTycoon(player, tycoon)
			break
		end
	end

	-- Remove from cache
	playerDataCache[player.UserId] = nil
end)

--[[
	Auto-save every 5 minutes
--]]
task.spawn(function()
	while true do
		task.wait(300) -- 5 minutes

		for _, player in ipairs(Players:GetPlayers()) do
			savePlayerData(player)
		end

		print("[TycoonManager] Auto-saved all player data")
	end
end)

print("[TycoonManager] Initialized")
