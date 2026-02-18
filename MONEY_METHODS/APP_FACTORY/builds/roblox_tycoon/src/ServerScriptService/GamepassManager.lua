--[[
	GamepassManager.lua
	Handles all monetization (gamepasses, developer products)

	Gamepasses (permanent):
	- VIP Pass: 2x money speed
	- Auto-Collect: money auto-collects (no need to touch)
	- Premium Skin: neon tycoon theme
	- Cash Boost: start with $10K

	Developer Products (repeatable):
	- Cash injections: $50K, $200K
	- Skip upgrade timer

	Architecture:
	- Check gamepass ownership with MarketplaceService:UserOwnsGamePassAsync
	- Handle purchases with ProcessReceipt callback
	- Grant benefits on player join or purchase
--]]

local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local TycoonConfig = require(ReplicatedStorage.TycoonConfig)

-- Track gamepass ownership cache (userId → gamepassId → bool)
local gamepassCache = {}

-- Track product purchase history for idempotency (receiptId → bool)
local processedReceipts = {}

--[[
	Check if player owns gamepass
	Returns: bool
--]]
local function checkGamepass(player, gamepassId)
	local userId = player.UserId

	-- Check cache first
	if gamepassCache[userId] and gamepassCache[userId][gamepassId] ~= nil then
		return gamepassCache[userId][gamepassId]
	end

	-- Query MarketplaceService
	local success, ownsGamepass = pcall(function()
		return MarketplaceService:UserOwnsGamePassAsync(userId, gamepassId)
	end)

	local result = success and ownsGamepass or false

	-- Cache result
	if not gamepassCache[userId] then
		gamepassCache[userId] = {}
	end
	gamepassCache[userId][gamepassId] = result

	return result
end

--[[
	Public function: check if player has specific gamepass by name
	Usage: GamepassManager.hasGamepass(player, "VIP")
--]]
local function hasGamepass(player, gamepassName)
	local gamepassId = TycoonConfig.GAMEPASSES[gamepassName]
	if not gamepassId then
		warn("[GamepassManager] Unknown gamepass:", gamepassName)
		return false
	end

	return checkGamepass(player, gamepassId)
end

--[[
	Grant VIP benefits (2x money speed)
	This is handled in TycoonManager.lua when calculating money amount
--]]
local function grantVIPBenefits(player)
	print("[GamepassManager]", player.Name, "has VIP gamepass")
	-- Benefits applied in money collection logic
end

--[[
	Grant Auto-Collect benefits
	Money automatically collects without touching
--]]
local function grantAutoCollectBenefits(player, tycoon)
	print("[GamepassManager]", player.Name, "has Auto-Collect gamepass")

	-- Find player's tycoon
	local tycoons = workspace:FindFirstChild("Tycoons")
	if not tycoons then return end

	for _, tycoon in ipairs(tycoons:GetChildren()) do
		local ownerValue = tycoon:FindFirstChild("Owner")
		if ownerValue and ownerValue.Value == player then
			-- Auto-collect loop
			task.spawn(function()
				while ownerValue.Value == player do
					task.wait(TycoonConfig.MONEY_SPAWN_RATE)

					-- Collect money directly
					local leaderstats = player:FindFirstChild("leaderstats")
					local cashValue = leaderstats and leaderstats:FindFirstChild("Cash")

					if cashValue then
						local moneyAmount = TycoonConfig.BASE_MONEY_AMOUNT

						-- Apply VIP multiplier if owned
						if hasGamepass(player, "VIP") then
							moneyAmount = moneyAmount * 2
						end

						cashValue.Value = cashValue.Value + moneyAmount
					end
				end
			end)

			break
		end
	end
end

--[[
	Grant Premium Skin
	Change tycoon colors to neon theme
--]]
local function grantPremiumSkin(player)
	print("[GamepassManager]", player.Name, "has Premium Skin gamepass")

	-- Find player's tycoon
	local tycoons = workspace:FindFirstChild("Tycoons")
	if not tycoons then return end

	for _, tycoon in ipairs(tycoons:GetChildren()) do
		local ownerValue = tycoon:FindFirstChild("Owner")
		if ownerValue and ownerValue.Value == player then
			-- Apply neon theme
			for _, part in ipairs(tycoon:GetDescendants()) do
				if part:IsA("BasePart") then
					part.Material = Enum.Material.Neon
					part.BrickColor = BrickColor.new("Electric blue")
				end
			end
			break
		end
	end
end

--[[
	Grant Cash Boost (starting cash)
--]]
local function grantCashBoost(player)
	print("[GamepassManager]", player.Name, "has Cash Boost gamepass")

	local leaderstats = player:FindFirstChild("leaderstats")
	local cashValue = leaderstats and leaderstats:FindFirstChild("Cash")

	if cashValue and cashValue.Value == TycoonConfig.STARTING_CASH then
		-- Only grant if player just joined (still has starting cash)
		cashValue.Value = cashValue.Value + 10000
		print("[GamepassManager] Granted +$10K starting cash to", player.Name)
	end
end

--[[
	Apply all gamepass benefits on player join
--]]
local function applyGamepassBenefits(player)
	-- VIP
	if hasGamepass(player, "VIP") then
		grantVIPBenefits(player)
	end

	-- Auto-Collect
	if hasGamepass(player, "AutoCollect") then
		grantAutoCollectBenefits(player)
	end

	-- Premium Skin
	if hasGamepass(player, "PremiumSkin") then
		grantPremiumSkin(player)
	end

	-- Cash Boost
	if hasGamepass(player, "CashBoost") then
		grantCashBoost(player)
	end
end

--[[
	Process developer product purchase
	Called by MarketplaceService ProcessReceipt
--]]
local function processDeveloperProduct(receiptInfo)
	local userId = receiptInfo.PlayerId
	local productId = receiptInfo.ProductId
	local receiptId = receiptInfo.PurchaseId

	-- Check if already processed (idempotency)
	if processedReceipts[receiptId] then
		print("[GamepassManager] Receipt already processed:", receiptId)
		return Enum.ProductPurchaseDecision.PurchaseGranted
	end

	-- Find player
	local player = Players:GetPlayerByUserId(userId)
	if not player then
		warn("[GamepassManager] Player not found for receipt:", receiptId)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	-- Find product config
	local productConfig = nil
	for name, config in pairs(TycoonConfig.DEVELOPER_PRODUCTS) do
		if config.id == productId then
			productConfig = config
			break
		end
	end

	if not productConfig then
		warn("[GamepassManager] Unknown product ID:", productId)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	-- Grant product
	local leaderstats = player:FindFirstChild("leaderstats")
	local cashValue = leaderstats and leaderstats:FindFirstChild("Cash")

	if not cashValue then
		warn("[GamepassManager] No cash leaderstat for", player.Name)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	if productConfig.type == "cash" then
		cashValue.Value = cashValue.Value + productConfig.amount
		print("[GamepassManager] Granted", productConfig.amount, "cash to", player.Name)
	elseif productConfig.type == "skipTimer" then
		-- Skip timer logic (not implemented in base version, placeholder)
		print("[GamepassManager] Skip timer purchased by", player.Name)
	end

	-- Mark as processed
	processedReceipts[receiptId] = true

	return Enum.ProductPurchaseDecision.PurchaseGranted
end

--[[
	Prompt gamepass purchase
	Called from client GUI
--]]
local function promptGamepassPurchase(player, gamepassName)
	local gamepassId = TycoonConfig.GAMEPASSES[gamepassName]
	if not gamepassId then
		warn("[GamepassManager] Unknown gamepass:", gamepassName)
		return
	end

	local success, err = pcall(function()
		MarketplaceService:PromptGamePassPurchase(player, gamepassId)
	end)

	if not success then
		warn("[GamepassManager] Failed to prompt gamepass:", err)
	end
end

--[[
	Prompt developer product purchase
	Called from client GUI
--]]
local function promptProductPurchase(player, productName)
	local productConfig = TycoonConfig.DEVELOPER_PRODUCTS[productName]
	if not productConfig then
		warn("[GamepassManager] Unknown product:", productName)
		return
	end

	local success, err = pcall(function()
		MarketplaceService:PromptProductPurchase(player, productConfig.id)
	end)

	if not success then
		warn("[GamepassManager] Failed to prompt product:", err)
	end
end

--[[
	Setup MarketplaceService callbacks
--]]
MarketplaceService.ProcessReceipt = processDeveloperProduct

--[[
	Handle gamepass purchase completed
--]]
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, gamepassId, wasPurchased)
	if not wasPurchased then return end

	print("[GamepassManager]", player.Name, "purchased gamepass:", gamepassId)

	-- Clear cache
	if gamepassCache[player.UserId] then
		gamepassCache[player.UserId][gamepassId] = true
	end

	-- Apply benefits immediately
	applyGamepassBenefits(player)
end)

--[[
	Player joined - apply gamepass benefits
--]]
Players.PlayerAdded:Connect(function(player)
	-- Wait for character and leaderstats
	player.CharacterAdded:Wait()
	task.wait(1) -- ensure TycoonManager has set up leaderstats

	applyGamepassBenefits(player)
end)

--[[
	Remote function for client to check gamepass ownership
--]]
local checkGamepassRemote = Instance.new("RemoteFunction")
checkGamepassRemote.Name = "CheckGamepass"
checkGamepassRemote.Parent = ReplicatedStorage
checkGamepassRemote.OnServerInvoke = function(player, gamepassName)
	return hasGamepass(player, gamepassName)
end

--[[
	Remote function for client to prompt purchases
--]]
local promptPurchaseRemote = Instance.new("RemoteFunction")
promptPurchaseRemote.Name = "PromptPurchase"
promptPurchaseRemote.Parent = ReplicatedStorage
promptPurchaseRemote.OnServerInvoke = function(player, purchaseType, purchaseName)
	if purchaseType == "gamepass" then
		promptGamepassPurchase(player, purchaseName)
	elseif purchaseType == "product" then
		promptProductPurchase(player, purchaseName)
	end
end

print("[GamepassManager] Initialized")

-- Export functions for use in other scripts
return {
	hasGamepass = hasGamepass,
	promptGamepassPurchase = promptGamepassPurchase,
	promptProductPurchase = promptProductPurchase
}
