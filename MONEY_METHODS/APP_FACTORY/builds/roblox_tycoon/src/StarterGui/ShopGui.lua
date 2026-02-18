--[[
	ShopGui.lua
	Client-side shop UI for purchasing gamepasses and developer products

	UI Structure:
	- ScreenGui → ShopFrame (main container)
	- ShopFrame contains:
	  - Header (title)
	  - GamepassSection (4 gamepass buttons)
	  - ProductSection (3 developer product buttons)
	  - CloseButton

	Each button shows:
	- Item name
	- Item description
	- Price in Robux
	- Owned status (if applicable)

	Client communicates with server via RemoteFunction to:
	- Check gamepass ownership
	- Prompt purchases
--]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

-- Wait for remotes to exist
local checkGamepassRemote = ReplicatedStorage:WaitForChild("CheckGamepass")
local promptPurchaseRemote = ReplicatedStorage:WaitForChild("PromptPurchase")

-- Import config
local TycoonConfig = require(ReplicatedStorage.TycoonConfig)

--[[
	Create main ScreenGui
--]]
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "ShopGui"
screenGui.ResetOnSpawn = false
screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
screenGui.Parent = playerGui

--[[
	Create main shop frame (initially hidden)
--]]
local shopFrame = Instance.new("Frame")
shopFrame.Name = "ShopFrame"
shopFrame.Size = UDim2.new(0, 600, 0, 700)
shopFrame.Position = UDim2.new(0.5, -300, 0.5, -350)
shopFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
shopFrame.BorderSizePixel = 0
shopFrame.Visible = false
shopFrame.Parent = screenGui

-- Round corners
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 12)
corner.Parent = shopFrame

--[[
	Create header
--]]
local header = Instance.new("TextLabel")
header.Name = "Header"
header.Size = UDim2.new(1, 0, 0, 60)
header.Position = UDim2.new(0, 0, 0, 0)
header.BackgroundColor3 = Color3.fromRGB(20, 20, 30)
header.BorderSizePixel = 0
header.Text = "AI Factory Shop"
header.TextColor3 = Color3.fromRGB(255, 255, 255)
header.TextSize = 32
header.Font = Enum.Font.GothamBold
header.Parent = shopFrame

local headerCorner = Instance.new("UICorner")
headerCorner.CornerRadius = UDim.new(0, 12)
headerCorner.Parent = header

--[[
	Create close button
--]]
local closeButton = Instance.new("TextButton")
closeButton.Name = "CloseButton"
closeButton.Size = UDim2.new(0, 40, 0, 40)
closeButton.Position = UDim2.new(1, -50, 0, 10)
closeButton.BackgroundColor3 = Color3.fromRGB(200, 50, 50)
closeButton.BorderSizePixel = 0
closeButton.Text = "X"
closeButton.TextColor3 = Color3.fromRGB(255, 255, 255)
closeButton.TextSize = 24
closeButton.Font = Enum.Font.GothamBold
closeButton.Parent = shopFrame

local closeCorner = Instance.new("UICorner")
closeCorner.CornerRadius = UDim.new(0, 8)
closeCorner.Parent = closeButton

closeButton.MouseButton1Click:Connect(function()
	shopFrame.Visible = false
end)

--[[
	Create ScrollingFrame for content
--]]
local scrollFrame = Instance.new("ScrollingFrame")
scrollFrame.Name = "ScrollFrame"
scrollFrame.Size = UDim2.new(1, -20, 1, -80)
scrollFrame.Position = UDim2.new(0, 10, 0, 70)
scrollFrame.BackgroundTransparency = 1
scrollFrame.BorderSizePixel = 0
scrollFrame.ScrollBarThickness = 8
scrollFrame.CanvasSize = UDim2.new(0, 0, 0, 0) -- auto-sized by UIListLayout
scrollFrame.Parent = shopFrame

local listLayout = Instance.new("UIListLayout")
listLayout.Padding = UDim.new(0, 15)
listLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
listLayout.SortOrder = Enum.SortOrder.LayoutOrder
listLayout.Parent = scrollFrame

-- Auto-size canvas
listLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
	scrollFrame.CanvasSize = UDim2.new(0, 0, 0, listLayout.AbsoluteContentSize.Y + 20)
end)

--[[
	Create section header
--]]
local function createSectionHeader(text, layoutOrder)
	local sectionHeader = Instance.new("TextLabel")
	sectionHeader.Name = text .. "Header"
	sectionHeader.Size = UDim2.new(1, -20, 0, 40)
	sectionHeader.BackgroundTransparency = 1
	sectionHeader.Text = text
	sectionHeader.TextColor3 = Color3.fromRGB(200, 200, 200)
	sectionHeader.TextSize = 24
	sectionHeader.Font = Enum.Font.GothamBold
	sectionHeader.TextXAlignment = Enum.TextXAlignment.Left
	sectionHeader.LayoutOrder = layoutOrder
	sectionHeader.Parent = scrollFrame

	return sectionHeader
end

--[[
	Create purchase button
--]]
local function createPurchaseButton(config, layoutOrder, purchaseType, purchaseName)
	local button = Instance.new("Frame")
	button.Name = purchaseName .. "Button"
	button.Size = UDim2.new(1, -20, 0, 100)
	button.BackgroundColor3 = Color3.fromRGB(40, 40, 50)
	button.BorderSizePixel = 0
	button.LayoutOrder = layoutOrder
	button.Parent = scrollFrame

	local buttonCorner = Instance.new("UICorner")
	buttonCorner.CornerRadius = UDim.new(0, 10)
	buttonCorner.Parent = button

	-- Item name
	local nameLabel = Instance.new("TextLabel")
	nameLabel.Name = "NameLabel"
	nameLabel.Size = UDim2.new(1, -20, 0, 30)
	nameLabel.Position = UDim2.new(0, 10, 0, 10)
	nameLabel.BackgroundTransparency = 1
	nameLabel.Text = config.name
	nameLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
	nameLabel.TextSize = 20
	nameLabel.Font = Enum.Font.GothamBold
	nameLabel.TextXAlignment = Enum.TextXAlignment.Left
	nameLabel.Parent = button

	-- Item description
	local descLabel = Instance.new("TextLabel")
	descLabel.Name = "DescLabel"
	descLabel.Size = UDim2.new(1, -20, 0, 30)
	descLabel.Position = UDim2.new(0, 10, 0, 40)
	descLabel.BackgroundTransparency = 1
	descLabel.Text = config.description
	descLabel.TextColor3 = Color3.fromRGB(180, 180, 180)
	descLabel.TextSize = 14
	descLabel.Font = Enum.Font.Gotham
	descLabel.TextXAlignment = Enum.TextXAlignment.Left
	descLabel.TextWrapped = true
	descLabel.Parent = button

	-- Buy button
	local buyButton = Instance.new("TextButton")
	buyButton.Name = "BuyButton"
	buyButton.Size = UDim2.new(0, 120, 0, 35)
	buyButton.Position = UDim2.new(1, -130, 1, -45)
	buyButton.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
	buyButton.BorderSizePixel = 0
	buyButton.Text = config.price .. " R$"
	buyButton.TextColor3 = Color3.fromRGB(255, 255, 255)
	buyButton.TextSize = 18
	buyButton.Font = Enum.Font.GothamBold
	buyButton.Parent = button

	local buyCorner = Instance.new("UICorner")
	buyCorner.CornerRadius = UDim.new(0, 8)
	buyCorner.Parent = buyButton

	-- Owned indicator (for gamepasses only)
	if purchaseType == "gamepass" then
		local owned = checkGamepassRemote:InvokeServer(purchaseName)
		if owned then
			buyButton.Text = "OWNED"
			buyButton.BackgroundColor3 = Color3.fromRGB(100, 100, 100)
			buyButton.Active = false
		end
	end

	-- Purchase click
	buyButton.MouseButton1Click:Connect(function()
		if buyButton.Text ~= "OWNED" then
			-- Prompt purchase
			promptPurchaseRemote:InvokeServer(purchaseType, purchaseName)
		end
	end)

	-- Hover effect
	buyButton.MouseEnter:Connect(function()
		if buyButton.Text ~= "OWNED" then
			TweenService:Create(buyButton, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(0, 255, 0)}):Play()
		end
	end)

	buyButton.MouseLeave:Connect(function()
		if buyButton.Text ~= "OWNED" then
			TweenService:Create(buyButton, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(0, 200, 0)}):Play()
		end
	end)

	return button
end

--[[
	Create gamepass section
--]]
createSectionHeader("Gamepasses (Permanent)", 1)

local gamepassOrder = 2
for name, config in pairs(TycoonConfig.GAMEPASS_CONFIGS) do
	createPurchaseButton(config, gamepassOrder, "gamepass", name)
	gamepassOrder = gamepassOrder + 1
end

--[[
	Create developer products section
--]]
createSectionHeader("Cash Packs (One-Time)", 10)

local productOrder = 11
for name, config in pairs(TycoonConfig.PRODUCT_CONFIGS) do
	createPurchaseButton(config, productOrder, "product", name)
	productOrder = productOrder + 1
end

--[[
	Create shop toggle button (top-right corner of screen)
--]]
local toggleButton = Instance.new("TextButton")
toggleButton.Name = "ShopToggle"
toggleButton.Size = UDim2.new(0, 80, 0, 80)
toggleButton.Position = UDim2.new(1, -100, 0, 20)
toggleButton.BackgroundColor3 = Color3.fromRGB(0, 150, 255)
toggleButton.BorderSizePixel = 0
toggleButton.Text = "SHOP"
toggleButton.TextColor3 = Color3.fromRGB(255, 255, 255)
toggleButton.TextSize = 20
toggleButton.Font = Enum.Font.GothamBold
toggleButton.Parent = screenGui

local toggleCorner = Instance.new("UICorner")
toggleCorner.CornerRadius = UDim.new(0, 12)
toggleCorner.Parent = toggleButton

toggleButton.MouseButton1Click:Connect(function()
	shopFrame.Visible = not shopFrame.Visible
end)

-- Hover effect
toggleButton.MouseEnter:Connect(function()
	TweenService:Create(toggleButton, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(0, 180, 255)}):Play()
end)

toggleButton.MouseLeave:Connect(function()
	TweenService:Create(toggleButton, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(0, 150, 255)}):Play()
end)

print("[ShopGui] Initialized")
