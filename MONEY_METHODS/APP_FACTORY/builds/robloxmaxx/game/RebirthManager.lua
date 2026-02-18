-- ServerScriptService/RebirthManager
-- Rebirth logic: reset for permanent multipliers

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))
local DataManager = require(game:GetService("ServerScriptService"):WaitForChild("DataManager"))

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local RequestRebirth = Remotes:WaitForChild("RequestRebirth")

local RebirthManager = {}

function RebirthManager.GetRebirthCost(rebirths: number): number
	return math.floor(Config.Rebirth.BaseCost * (Config.Rebirth.CostMultiplier ^ rebirths))
end

function RebirthManager.GetMultiplier(rebirths: number): number
	return 1 + (rebirths * Config.Rebirth.PermanentBonus)
end

function RebirthManager.DoRebirth(player: Player): boolean
	local data = DataManager.GetData(player)
	if not data then return false end

	if data.rebirths >= Config.Rebirth.MaxRebirths then return false end

	local cost = RebirthManager.GetRebirthCost(data.rebirths)
	if data.coins < cost then return false end

	-- Reset
	data.rebirths += 1
	data.coins = 0
	data.ownedDroppers = {1} -- Keep basic dropper
	data.ownedUpgraders = {}

	-- Update displays
	DataManager.SetCoins(player, 0)
	DataManager.SetRebirths(player, data.rebirths)

	-- Save immediately
	task.spawn(function()
		DataManager.SaveData(player)
	end)

	-- Notify client
	RequestRebirth:FireClient(player, true, data.rebirths, RebirthManager.GetMultiplier(data.rebirths))

	return true
end

RequestRebirth.OnServerEvent:Connect(function(player: Player)
	RebirthManager.DoRebirth(player)
end)

return RebirthManager
