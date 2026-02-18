-- ServerScriptService/EconomyManager
-- Handles gamepasses, dev products, codes

local Players = game:GetService("Players")
local MarketplaceService = game:GetService("MarketplaceService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))
local DataManager = require(game:GetService("ServerScriptService"):WaitForChild("DataManager"))

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local RedeemCode = Remotes:WaitForChild("RedeemCode")

local gamepassCache: {[number]: {[number]: boolean}} = {}

local EconomyManager = {}

function EconomyManager.HasGamepass(player: Player, gamepassName: string): boolean
	local gpConfig = Config.Gamepasses[gamepassName]
	if not gpConfig or gpConfig.id == 0 then return false end

	local userId = player.UserId
	if not gamepassCache[userId] then
		gamepassCache[userId] = {}
	end

	if gamepassCache[userId][gpConfig.id] ~= nil then
		return gamepassCache[userId][gpConfig.id]
	end

	local success, owns = pcall(function()
		return MarketplaceService:UserOwnsGamePassAsync(userId, gpConfig.id)
	end)

	if success then
		gamepassCache[userId][gpConfig.id] = owns
		return owns
	end
	return false
end

function EconomyManager.GetEarningsMultiplier(player: Player): number
	local mult = 1
	if EconomyManager.HasGamepass(player, "DoubleEarnings") then
		mult *= 2
	end
	return mult
end

function EconomyManager.GetMaxPetSlots(player: Player): number
	local slots = Config.Pets.MaxEquipped
	if EconomyManager.HasGamepass(player, "ExtraSlot") then
		slots += 1
	end
	return slots
end

-- Gamepass purchase handler
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, gamepassId, wasPurchased)
	if not wasPurchased then return end
	if not gamepassCache[player.UserId] then
		gamepassCache[player.UserId] = {}
	end
	gamepassCache[player.UserId][gamepassId] = true
end)

-- Dev product handler
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

-- Code redemption
RedeemCode.OnServerEvent:Connect(function(player: Player, code: string)
	if typeof(code) ~= "string" then return end
	code = string.upper(code)

	local codeConfig = Config.Codes[code]
	if not codeConfig then
		RedeemCode:FireClient(player, false, "Invalid code")
		return
	end

	local data = DataManager.GetData(player)
	if not data then return end

	if data.redeemedCodes and table.find(data.redeemedCodes, code) then
		RedeemCode:FireClient(player, false, "Already redeemed")
		return
	end

	if codeConfig.reward == "coins" then
		DataManager.AddCoins(player, codeConfig.amount)
	end

	if not data.redeemedCodes then
		data.redeemedCodes = {}
	end
	table.insert(data.redeemedCodes, code)

	RedeemCode:FireClient(player, true, `Redeemed! +{codeConfig.amount} Coins`)
end)

-- Cleanup
Players.PlayerRemoving:Connect(function(player)
	gamepassCache[player.UserId] = nil
end)

return EconomyManager
