-- ServerScriptService/DataManager
-- Handles save/load of all player data with DataStoreService

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

local playerStore = DataStoreService:GetDataStore(Config.DataStoreKey)
local playerDataCache: {[number]: {[string]: any}} = {}
local saveLock: {[number]: boolean} = {}

local DataManager = {}

local function getDefaultData(): {[string]: any}
	return {
		coins = Config.Currency.StartAmount,
		rebirths = 0,
		ownedDroppers = {1}, -- Start with Basic Dropper
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

function DataManager.LoadData(player: Player): {[string]: any}
	local userId = player.UserId
	local data = nil

	local success, result = pcall(function()
		return playerStore:GetAsync(`Player_{userId}`)
	end)

	if success and result then
		-- Merge with defaults to handle new fields
		local defaults = getDefaultData()
		for key, defaultValue in defaults do
			if result[key] == nil then
				result[key] = defaultValue
			end
		end
		data = result
	else
		if not success then
			warn(`[DataManager] Failed to load data for {player.Name}: {result}`)
		end
		data = getDefaultData()
	end

	data.joinCount += 1
	data.lastSave = os.time()
	playerDataCache[userId] = data

	-- Set up leaderstats
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

function DataManager.SaveData(player: Player)
	local userId = player.UserId
	local data = playerDataCache[userId]
	if not data then return end
	if saveLock[userId] then return end

	saveLock[userId] = true
	data.lastSave = os.time()

	local success, err = pcall(function()
		playerStore:SetAsync(`Player_{userId}`, data)
	end)

	if not success then
		warn(`[DataManager] Failed to save data for {player.Name}: {err}`)
	end

	saveLock[userId] = false
end

function DataManager.GetData(player: Player): {[string]: any}?
	return playerDataCache[player.UserId]
end

function DataManager.SetCoins(player: Player, amount: number)
	local data = playerDataCache[player.UserId]
	if not data then return end

	data.coins = math.clamp(amount, 0, Config.Currency.MaxAmount)

	-- Update leaderstats
	local leaderstats = player:FindFirstChild("leaderstats")
	if leaderstats then
		local coinsDisplay = leaderstats:FindFirstChild("Coins")
		if coinsDisplay then
			coinsDisplay.Value = data.coins
		end
	end

	-- Notify client
	local remotes = ReplicatedStorage:FindFirstChild("Remotes")
	if remotes then
		local updateRemote = remotes:FindFirstChild("UpdateCurrency")
		if updateRemote then
			updateRemote:FireClient(player, data.coins)
		end
	end
end

function DataManager.AddCoins(player: Player, amount: number)
	local data = playerDataCache[player.UserId]
	if not data then return end

	DataManager.SetCoins(player, data.coins + amount)
	data.totalEarned += amount
end

function DataManager.GetCoins(player: Player): number
	local data = playerDataCache[player.UserId]
	return data and data.coins or 0
end

function DataManager.SpendCoins(player: Player, amount: number): boolean
	local data = playerDataCache[player.UserId]
	if not data then return false end
	if data.coins < amount then return false end

	DataManager.SetCoins(player, data.coins - amount)
	return true
end

function DataManager.SetRebirths(player: Player, count: number)
	local data = playerDataCache[player.UserId]
	if not data then return end

	data.rebirths = count

	local leaderstats = player:FindFirstChild("leaderstats")
	if leaderstats then
		local rebirthsDisplay = leaderstats:FindFirstChild("Rebirths")
		if rebirthsDisplay then
			rebirthsDisplay.Value = count
		end
	end
end

function DataManager.Cleanup(player: Player)
	local userId = player.UserId
	DataManager.SaveData(player)
	task.wait(0.5)
	playerDataCache[userId] = nil
	saveLock[userId] = nil
end

-- Auto-save every 120 seconds
task.spawn(function()
	while true do
		task.wait(120)
		for _, player in Players:GetPlayers() do
			task.spawn(function()
				DataManager.SaveData(player)
			end)
		end
	end
end)

-- Save on player leave
Players.PlayerRemoving:Connect(function(player: Player)
	DataManager.Cleanup(player)
end)

-- Save all on shutdown
game:BindToClose(function()
	for _, player in Players:GetPlayers() do
		DataManager.SaveData(player)
	end
	task.wait(2)
end)

return DataManager
