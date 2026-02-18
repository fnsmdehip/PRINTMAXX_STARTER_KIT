-- StarterGui/TycoonHUD (LocalScript)
-- Client-side UI: currency display, pet panel, shop, codes, rebirth

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local UpdateCurrency = Remotes:WaitForChild("UpdateCurrency")
local HatchEgg = Remotes:WaitForChild("HatchEgg")
local EquipPet = Remotes:WaitForChild("EquipPet")
local UpdatePets = Remotes:WaitForChild("UpdatePets")
local RequestRebirth = Remotes:WaitForChild("RequestRebirth")
local RedeemCode = Remotes:WaitForChild("RedeemCode")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))

local currentCoins = 0
local myPets = {}
local equippedPets = {}

--------------------------------------------------------------------
-- UI CREATION
--------------------------------------------------------------------
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "TycoonHUD"
screenGui.ResetOnSpawn = false
screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
screenGui.Parent = player:WaitForChild("PlayerGui")

-- CURRENCY DISPLAY (top center)
local currencyFrame = Instance.new("Frame")
currencyFrame.Name = "CurrencyFrame"
currencyFrame.Size = UDim2.new(0, 300, 0, 60)
currencyFrame.Position = UDim2.new(0.5, -150, 0, 10)
currencyFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
currencyFrame.BackgroundTransparency = 0.3
currencyFrame.Parent = screenGui

local currencyCorner = Instance.new("UICorner")
currencyCorner.CornerRadius = UDim.new(0, 12)
currencyCorner.Parent = currencyFrame

local coinIcon = Instance.new("TextLabel")
coinIcon.Size = UDim2.new(0, 50, 1, 0)
coinIcon.BackgroundTransparency = 1
coinIcon.Text = "🪙"
coinIcon.TextSize = 30
coinIcon.Parent = currencyFrame

local coinLabel = Instance.new("TextLabel")
coinLabel.Name = "CoinLabel"
coinLabel.Size = UDim2.new(1, -60, 1, 0)
coinLabel.Position = UDim2.new(0, 55, 0, 0)
coinLabel.BackgroundTransparency = 1
coinLabel.Text = "0 Coins"
coinLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
coinLabel.TextSize = 28
coinLabel.Font = Enum.Font.GothamBold
coinLabel.TextXAlignment = Enum.TextXAlignment.Left
coinLabel.Parent = currencyFrame

-- BUTTONS (right side)
local function createSideButton(name: string, text: string, yPos: number, color: Color3): TextButton
	local btn = Instance.new("TextButton")
	btn.Name = name
	btn.Size = UDim2.new(0, 120, 0, 45)
	btn.Position = UDim2.new(1, -130, 0, yPos)
	btn.BackgroundColor3 = color
	btn.Text = text
	btn.TextColor3 = Color3.new(1, 1, 1)
	btn.TextSize = 16
	btn.Font = Enum.Font.GothamBold
	btn.Parent = screenGui

	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, 8)
	corner.Parent = btn

	return btn
end

local petsBtn = createSideButton("PetsBtn", "Pets", 80, Color3.fromRGB(0, 150, 255))
local shopBtn = createSideButton("ShopBtn", "Shop", 135, Color3.fromRGB(0, 200, 100))
local codesBtn = createSideButton("CodesBtn", "Codes", 190, Color3.fromRGB(200, 100, 0))
local rebirthBtn = createSideButton("RebirthBtn", "Rebirth", 245, Color3.fromRGB(200, 0, 255))

-- PANEL TEMPLATE
local function createPanel(name: string, title: string): Frame
	local panel = Instance.new("Frame")
	panel.Name = name
	panel.Size = UDim2.new(0, 400, 0, 500)
	panel.Position = UDim2.new(0.5, -200, 0.5, -250)
	panel.BackgroundColor3 = Color3.fromRGB(25, 25, 35)
	panel.Visible = false
	panel.Parent = screenGui

	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, 12)
	corner.Parent = panel

	local titleBar = Instance.new("TextLabel")
	titleBar.Size = UDim2.new(1, 0, 0, 50)
	titleBar.BackgroundColor3 = Color3.fromRGB(40, 40, 60)
	titleBar.Text = title
	titleBar.TextColor3 = Color3.new(1, 1, 1)
	titleBar.TextSize = 22
	titleBar.Font = Enum.Font.GothamBold
	titleBar.Parent = panel

	local titleCorner = Instance.new("UICorner")
	titleCorner.CornerRadius = UDim.new(0, 12)
	titleCorner.Parent = titleBar

	local closeBtn = Instance.new("TextButton")
	closeBtn.Size = UDim2.new(0, 40, 0, 40)
	closeBtn.Position = UDim2.new(1, -45, 0, 5)
	closeBtn.BackgroundColor3 = Color3.fromRGB(200, 50, 50)
	closeBtn.Text = "X"
	closeBtn.TextColor3 = Color3.new(1, 1, 1)
	closeBtn.TextSize = 18
	closeBtn.Font = Enum.Font.GothamBold
	closeBtn.Parent = panel

	local closeCorner = Instance.new("UICorner")
	closeCorner.CornerRadius = UDim.new(0, 8)
	closeCorner.Parent = closeBtn

	closeBtn.MouseButton1Click:Connect(function()
		panel.Visible = false
	end)

	local content = Instance.new("ScrollingFrame")
	content.Name = "Content"
	content.Size = UDim2.new(1, -20, 1, -60)
	content.Position = UDim2.new(0, 10, 0, 55)
	content.BackgroundTransparency = 1
	content.ScrollBarThickness = 6
	content.Parent = panel

	local layout = Instance.new("UIListLayout")
	layout.Padding = UDim.new(0, 8)
	layout.Parent = content

	return panel
end

-- PETS PANEL
local petsPanel = createPanel("PetsPanel", "Pets")

local function refreshPetsPanel()
	local content = petsPanel:FindFirstChild("Content")
	if not content then return end

	for _, child in content:GetChildren() do
		if child:IsA("Frame") then child:Destroy() end
	end

	-- Egg buttons
	for i, egg in Config.Pets.Eggs do
		local eggFrame = Instance.new("Frame")
		eggFrame.Size = UDim2.new(1, 0, 0, 50)
		eggFrame.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
		eggFrame.Parent = content

		local eggCorner = Instance.new("UICorner")
		eggCorner.CornerRadius = UDim.new(0, 8)
		eggCorner.Parent = eggFrame

		local eggLabel = Instance.new("TextLabel")
		eggLabel.Size = UDim2.new(0.6, 0, 1, 0)
		eggLabel.Position = UDim2.new(0, 10, 0, 0)
		eggLabel.BackgroundTransparency = 1
		eggLabel.Text = `{egg.name} ({egg.cost} Coins)`
		eggLabel.TextColor3 = egg.color
		eggLabel.TextSize = 16
		eggLabel.Font = Enum.Font.GothamBold
		eggLabel.TextXAlignment = Enum.TextXAlignment.Left
		eggLabel.Parent = eggFrame

		local hatchBtn = Instance.new("TextButton")
		hatchBtn.Size = UDim2.new(0.3, 0, 0, 35)
		hatchBtn.Position = UDim2.new(0.65, 0, 0.5, -17)
		hatchBtn.BackgroundColor3 = Color3.fromRGB(0, 180, 100)
		hatchBtn.Text = "Hatch!"
		hatchBtn.TextColor3 = Color3.new(1, 1, 1)
		hatchBtn.TextSize = 14
		hatchBtn.Font = Enum.Font.GothamBold
		hatchBtn.Parent = eggFrame

		local hatchCorner = Instance.new("UICorner")
		hatchCorner.CornerRadius = UDim.new(0, 6)
		hatchCorner.Parent = hatchBtn

		hatchBtn.MouseButton1Click:Connect(function()
			HatchEgg:FireServer(i)
		end)
	end

	-- Divider
	local divider = Instance.new("Frame")
	divider.Size = UDim2.new(1, 0, 0, 2)
	divider.BackgroundColor3 = Color3.fromRGB(80, 80, 100)
	divider.Parent = content

	-- Owned pets
	for _, pet in myPets do
		local petFrame = Instance.new("Frame")
		petFrame.Size = UDim2.new(1, 0, 0, 45)
		petFrame.BackgroundColor3 = Color3.fromRGB(35, 35, 50)
		petFrame.Parent = content

		local petCorner = Instance.new("UICorner")
		petCorner.CornerRadius = UDim.new(0, 8)
		petCorner.Parent = petFrame

		local rarityColor = Config.Pets.RarityColors[pet.rarity] or Color3.new(1, 1, 1)

		local petLabel = Instance.new("TextLabel")
		petLabel.Size = UDim2.new(0.55, 0, 1, 0)
		petLabel.Position = UDim2.new(0, 10, 0, 0)
		petLabel.BackgroundTransparency = 1
		petLabel.Text = `{pet.name} (x{pet.multiplier})`
		petLabel.TextColor3 = rarityColor
		petLabel.TextSize = 14
		petLabel.Font = Enum.Font.GothamBold
		petLabel.TextXAlignment = Enum.TextXAlignment.Left
		petLabel.Parent = petFrame

		local rarityLabel = Instance.new("TextLabel")
		rarityLabel.Size = UDim2.new(0.2, 0, 1, 0)
		rarityLabel.Position = UDim2.new(0.55, 0, 0, 0)
		rarityLabel.BackgroundTransparency = 1
		rarityLabel.Text = pet.rarity
		rarityLabel.TextColor3 = rarityColor
		rarityLabel.TextSize = 12
		rarityLabel.Font = Enum.Font.Gotham
		rarityLabel.Parent = petFrame

		local isEquipped = false
		for _, eq in equippedPets do
			if eq.id == pet.id then
				isEquipped = true
				break
			end
		end

		local equipBtn = Instance.new("TextButton")
		equipBtn.Size = UDim2.new(0.2, 0, 0, 30)
		equipBtn.Position = UDim2.new(0.77, 0, 0.5, -15)
		equipBtn.BackgroundColor3 = if isEquipped then Color3.fromRGB(200, 50, 50) else Color3.fromRGB(0, 150, 255)
		equipBtn.Text = if isEquipped then "Remove" else "Equip"
		equipBtn.TextColor3 = Color3.new(1, 1, 1)
		equipBtn.TextSize = 12
		equipBtn.Font = Enum.Font.GothamBold
		equipBtn.Parent = petFrame

		local equipCorner = Instance.new("UICorner")
		equipCorner.CornerRadius = UDim.new(0, 6)
		equipCorner.Parent = equipBtn

		equipBtn.MouseButton1Click:Connect(function()
			EquipPet:FireServer(pet.id)
		end)
	end

	content.CanvasSize = UDim2.new(0, 0, 0, content:FindFirstChildWhichIsA("UIListLayout").AbsoluteContentSize.Y + 20)
end

-- SHOP PANEL
local shopPanel = createPanel("ShopPanel", "Shop")

local function setupShopPanel()
	local content = shopPanel:FindFirstChild("Content")
	if not content then return end

	-- Gamepasses
	for name, gp in Config.Gamepasses do
		local gpFrame = Instance.new("Frame")
		gpFrame.Size = UDim2.new(1, 0, 0, 60)
		gpFrame.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
		gpFrame.Parent = content

		local gpCorner = Instance.new("UICorner")
		gpCorner.CornerRadius = UDim.new(0, 8)
		gpCorner.Parent = gpFrame

		local gpLabel = Instance.new("TextLabel")
		gpLabel.Size = UDim2.new(0.65, 0, 0.5, 0)
		gpLabel.Position = UDim2.new(0, 10, 0, 0)
		gpLabel.BackgroundTransparency = 1
		gpLabel.Text = gp.name
		gpLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
		gpLabel.TextSize = 16
		gpLabel.Font = Enum.Font.GothamBold
		gpLabel.TextXAlignment = Enum.TextXAlignment.Left
		gpLabel.Parent = gpFrame

		local gpDesc = Instance.new("TextLabel")
		gpDesc.Size = UDim2.new(0.65, 0, 0.5, 0)
		gpDesc.Position = UDim2.new(0, 10, 0.5, 0)
		gpDesc.BackgroundTransparency = 1
		gpDesc.Text = gp.description
		gpDesc.TextColor3 = Color3.fromRGB(180, 180, 180)
		gpDesc.TextSize = 12
		gpDesc.Font = Enum.Font.Gotham
		gpDesc.TextXAlignment = Enum.TextXAlignment.Left
		gpDesc.Parent = gpFrame

		local buyBtn = Instance.new("TextButton")
		buyBtn.Size = UDim2.new(0.25, 0, 0, 35)
		buyBtn.Position = UDim2.new(0.72, 0, 0.5, -17)
		buyBtn.BackgroundColor3 = Color3.fromRGB(0, 200, 100)
		buyBtn.Text = `{gp.price} R$`
		buyBtn.TextColor3 = Color3.new(1, 1, 1)
		buyBtn.TextSize = 14
		buyBtn.Font = Enum.Font.GothamBold
		buyBtn.Parent = gpFrame

		local buyCorner = Instance.new("UICorner")
		buyCorner.CornerRadius = UDim.new(0, 6)
		buyCorner.Parent = buyBtn

		buyBtn.MouseButton1Click:Connect(function()
			if gp.id > 0 then
				MarketplaceService:PromptGamePassPurchase(player, gp.id)
			end
		end)
	end

	content.CanvasSize = UDim2.new(0, 0, 0, content:FindFirstChildWhichIsA("UIListLayout").AbsoluteContentSize.Y + 20)
end

-- CODES PANEL
local codesPanel = createPanel("CodesPanel", "Redeem Codes")

local function setupCodesPanel()
	local content = codesPanel:FindFirstChild("Content")
	if not content then return end

	local inputFrame = Instance.new("Frame")
	inputFrame.Size = UDim2.new(1, 0, 0, 50)
	inputFrame.BackgroundTransparency = 1
	inputFrame.Parent = content

	local codeInput = Instance.new("TextBox")
	codeInput.Name = "CodeInput"
	codeInput.Size = UDim2.new(0.65, 0, 0, 40)
	codeInput.Position = UDim2.new(0, 0, 0.5, -20)
	codeInput.BackgroundColor3 = Color3.fromRGB(50, 50, 65)
	codeInput.PlaceholderText = "Enter code..."
	codeInput.Text = ""
	codeInput.TextColor3 = Color3.new(1, 1, 1)
	codeInput.TextSize = 16
	codeInput.Font = Enum.Font.Gotham
	codeInput.ClearTextOnFocus = true
	codeInput.Parent = inputFrame

	local inputCorner = Instance.new("UICorner")
	inputCorner.CornerRadius = UDim.new(0, 8)
	inputCorner.Parent = codeInput

	local redeemBtn = Instance.new("TextButton")
	redeemBtn.Size = UDim2.new(0.3, 0, 0, 40)
	redeemBtn.Position = UDim2.new(0.68, 0, 0.5, -20)
	redeemBtn.BackgroundColor3 = Color3.fromRGB(200, 100, 0)
	redeemBtn.Text = "Redeem"
	redeemBtn.TextColor3 = Color3.new(1, 1, 1)
	redeemBtn.TextSize = 16
	redeemBtn.Font = Enum.Font.GothamBold
	redeemBtn.Parent = inputFrame

	local redeemCorner = Instance.new("UICorner")
	redeemCorner.CornerRadius = UDim.new(0, 8)
	redeemCorner.Parent = redeemBtn

	local resultLabel = Instance.new("TextLabel")
	resultLabel.Name = "ResultLabel"
	resultLabel.Size = UDim2.new(1, 0, 0, 30)
	resultLabel.BackgroundTransparency = 1
	resultLabel.Text = ""
	resultLabel.TextColor3 = Color3.fromRGB(0, 255, 100)
	resultLabel.TextSize = 14
	resultLabel.Font = Enum.Font.GothamBold
	resultLabel.Parent = content

	redeemBtn.MouseButton1Click:Connect(function()
		local code = codeInput.Text
		if code == "" then return end
		RedeemCode:FireServer(code)
	end)

	RedeemCode.OnClientEvent:Connect(function(success, message)
		resultLabel.Text = message
		resultLabel.TextColor3 = if success then Color3.fromRGB(0, 255, 100) else Color3.fromRGB(255, 80, 80)
	end)
end

-- REBIRTH PANEL
local rebirthPanel = createPanel("RebirthPanel", "Rebirth")

local function setupRebirthPanel()
	local content = rebirthPanel:FindFirstChild("Content")
	if not content then return end

	local infoLabel = Instance.new("TextLabel")
	infoLabel.Name = "InfoLabel"
	infoLabel.Size = UDim2.new(1, 0, 0, 80)
	infoLabel.BackgroundTransparency = 1
	infoLabel.Text = "Rebirth resets your droppers and upgraders but gives you a permanent earnings multiplier!"
	infoLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
	infoLabel.TextSize = 14
	infoLabel.Font = Enum.Font.Gotham
	infoLabel.TextWrapped = true
	infoLabel.Parent = content

	local costLabel = Instance.new("TextLabel")
	costLabel.Name = "CostLabel"
	costLabel.Size = UDim2.new(1, 0, 0, 40)
	costLabel.BackgroundTransparency = 1
	costLabel.Text = "Cost: 1,000,000 Coins"
	costLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
	costLabel.TextSize = 18
	costLabel.Font = Enum.Font.GothamBold
	costLabel.Parent = content

	local bonusLabel = Instance.new("TextLabel")
	bonusLabel.Name = "BonusLabel"
	bonusLabel.Size = UDim2.new(1, 0, 0, 30)
	bonusLabel.BackgroundTransparency = 1
	bonusLabel.Text = "Next bonus: +25% earnings"
	bonusLabel.TextColor3 = Color3.fromRGB(200, 0, 255)
	bonusLabel.TextSize = 16
	bonusLabel.Font = Enum.Font.GothamBold
	bonusLabel.Parent = content

	local doRebirthBtn = Instance.new("TextButton")
	doRebirthBtn.Size = UDim2.new(0.6, 0, 0, 50)
	doRebirthBtn.BackgroundColor3 = Color3.fromRGB(200, 0, 255)
	doRebirthBtn.Text = "REBIRTH"
	doRebirthBtn.TextColor3 = Color3.new(1, 1, 1)
	doRebirthBtn.TextSize = 22
	doRebirthBtn.Font = Enum.Font.GothamBold
	doRebirthBtn.Parent = content

	local rebirthCorner = Instance.new("UICorner")
	rebirthCorner.CornerRadius = UDim.new(0, 12)
	rebirthCorner.Parent = doRebirthBtn

	doRebirthBtn.MouseButton1Click:Connect(function()
		RequestRebirth:FireServer()
	end)

	RequestRebirth.OnClientEvent:Connect(function(success, rebirths, multiplier)
		if success then
			bonusLabel.Text = `Current: x{string.format("%.2f", multiplier)} earnings ({rebirths} rebirths)`
		end
	end)
end

--------------------------------------------------------------------
-- TOGGLE PANELS
--------------------------------------------------------------------
local activePanel = nil

local function togglePanel(panel: Frame)
	if activePanel and activePanel ~= panel then
		activePanel.Visible = false
	end
	panel.Visible = not panel.Visible
	activePanel = if panel.Visible then panel else nil
end

petsBtn.MouseButton1Click:Connect(function()
	refreshPetsPanel()
	togglePanel(petsPanel)
end)
shopBtn.MouseButton1Click:Connect(function() togglePanel(shopPanel) end)
codesBtn.MouseButton1Click:Connect(function() togglePanel(codesPanel) end)
rebirthBtn.MouseButton1Click:Connect(function() togglePanel(rebirthPanel) end)

--------------------------------------------------------------------
-- EVENT LISTENERS
--------------------------------------------------------------------
UpdateCurrency.OnClientEvent:Connect(function(coins: number)
	currentCoins = coins
	coinLabel.Text = `{coins} Coins`
end)

UpdatePets.OnClientEvent:Connect(function(pets, equipped)
	myPets = pets or {}
	equippedPets = equipped or {}
	if petsPanel.Visible then
		refreshPetsPanel()
	end
end)

HatchEgg.OnClientEvent:Connect(function(success: boolean, petData)
	if success and petData then
		-- Show hatch result notification
		local notification = Instance.new("TextLabel")
		notification.Size = UDim2.new(0, 300, 0, 60)
		notification.Position = UDim2.new(0.5, -150, 0.3, 0)
		notification.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
		notification.Text = `You hatched: {petData.name} ({petData.rarity})!`
		notification.TextColor3 = Config.Pets.RarityColors[petData.rarity] or Color3.new(1, 1, 1)
		notification.TextSize = 18
		notification.Font = Enum.Font.GothamBold
		notification.Parent = screenGui

		local nCorner = Instance.new("UICorner")
		nCorner.CornerRadius = UDim.new(0, 12)
		nCorner.Parent = notification

		task.delay(3, function()
			if notification.Parent then
				notification:Destroy()
			end
		end)
	end
end)

--------------------------------------------------------------------
-- INIT
--------------------------------------------------------------------
setupShopPanel()
setupCodesPanel()
setupRebirthPanel()
