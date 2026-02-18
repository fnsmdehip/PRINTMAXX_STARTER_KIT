-- ServerScriptService/TycoonManager
-- Core tycoon logic: plots, droppers, upgraders, collectors, purchase buttons

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))
local DataManager = require(game:GetService("ServerScriptService"):WaitForChild("DataManager"))

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local PurchaseRemote = Remotes:WaitForChild("PurchaseButton")

-- State
local plotOwners: {[number]: number} = {} -- plotIndex -> userId
local plotData: {[number]: {dropperThreads: {thread}, items: {Instance}}} = {}
local playerPlots: {[number]: number} = {} -- userId -> plotIndex

local TycoonManager = {}

--------------------------------------------------------------------
-- PLOT LAYOUT
--------------------------------------------------------------------
local PLOT_POSITIONS = {}
for i = 1, Config.Plots.MaxPlots do
	local row = math.floor((i - 1) / 4)
	local col = (i - 1) % 4
	local spacing = Config.Plots.PlotSize.X + Config.Plots.PlotSpacing
	PLOT_POSITIONS[i] = Vector3.new(col * spacing, 0, row * spacing)
end

--------------------------------------------------------------------
-- CREATE PHYSICAL PLOT
--------------------------------------------------------------------
local function createPlotBase(plotIndex: number): Model
	local pos = PLOT_POSITIONS[plotIndex]
	local plotSize = Config.Plots.PlotSize

	local model = Instance.new("Model")
	model.Name = `Plot_{plotIndex}`

	-- Floor
	local floor = Instance.new("Part")
	floor.Name = "Floor"
	floor.Size = plotSize
	floor.Position = pos + Vector3.new(plotSize.X / 2, -0.5, plotSize.Z / 2)
	floor.Anchored = true
	floor.Material = Enum.Material.SmoothPlastic
	floor.Color = Color3.fromRGB(120, 180, 120)
	floor.Parent = model

	-- Collector (sell point)
	local collector = Instance.new("Part")
	collector.Name = "Collector"
	collector.Size = Vector3.new(8, 4, 8)
	collector.Position = pos + Vector3.new(plotSize.X - 10, 2, plotSize.Z / 2)
	collector.Anchored = true
	collector.Material = Enum.Material.Neon
	collector.Color = Color3.fromRGB(0, 255, 100)
	collector.Parent = model

	local collectorLabel = Instance.new("BillboardGui")
	collectorLabel.Name = "Label"
	collectorLabel.Size = UDim2.new(0, 200, 0, 50)
	collectorLabel.StudsOffset = Vector3.new(0, 4, 0)
	collectorLabel.AlwaysOnTop = true
	collectorLabel.Parent = collector

	local labelText = Instance.new("TextLabel")
	labelText.Size = UDim2.new(1, 0, 1, 0)
	labelText.BackgroundTransparency = 1
	labelText.Text = "SELL"
	labelText.TextColor3 = Color3.new(1, 1, 1)
	labelText.TextScaled = true
	labelText.Font = Enum.Font.GothamBold
	labelText.Parent = collectorLabel

	-- Conveyor path (invisible waypoints)
	local conveyorStart = pos + Vector3.new(15, 1.5, plotSize.Z / 2)
	local conveyorEnd = pos + Vector3.new(plotSize.X - 15, 1.5, plotSize.Z / 2)

	-- Visual conveyor belt
	local belt = Instance.new("Part")
	belt.Name = "ConveyorBelt"
	belt.Size = Vector3.new(conveyorEnd.X - conveyorStart.X, 0.5, 6)
	belt.Position = (conveyorStart + conveyorEnd) / 2
	belt.Anchored = true
	belt.Material = Enum.Material.DiamondPlate
	belt.Color = Color3.fromRGB(80, 80, 80)
	belt.Parent = model

	-- Store waypoints as attributes
	model:SetAttribute("ConveyorStartX", conveyorStart.X)
	model:SetAttribute("ConveyorStartZ", conveyorStart.Z)
	model:SetAttribute("ConveyorEndX", conveyorEnd.X)
	model:SetAttribute("ConveyorEndZ", conveyorEnd.Z)
	model:SetAttribute("PlotIndex", plotIndex)

	-- Claim pad
	local claimPad = Instance.new("Part")
	claimPad.Name = "ClaimPad"
	claimPad.Size = Vector3.new(10, 1, 10)
	claimPad.Position = pos + Vector3.new(plotSize.X / 2, 0.5, plotSize.Z / 2)
	claimPad.Anchored = true
	claimPad.Material = Enum.Material.Neon
	claimPad.Color = Color3.fromRGB(255, 255, 0)
	claimPad.Parent = model

	local claimGui = Instance.new("BillboardGui")
	claimGui.Size = UDim2.new(0, 300, 0, 80)
	claimGui.StudsOffset = Vector3.new(0, 3, 0)
	claimGui.AlwaysOnTop = true
	claimGui.Parent = claimPad

	local claimText = Instance.new("TextLabel")
	claimText.Size = UDim2.new(1, 0, 1, 0)
	claimText.BackgroundTransparency = 1
	claimText.Text = "STEP ON TO CLAIM"
	claimText.TextColor3 = Color3.new(1, 1, 1)
	claimText.TextScaled = true
	claimText.Font = Enum.Font.GothamBold
	claimText.Parent = claimGui

	model.Parent = workspace:FindFirstChild("Plots") or workspace

	return model
end

--------------------------------------------------------------------
-- PURCHASE BUTTON CREATION
--------------------------------------------------------------------
local function createPurchaseButton(plot: Model, itemName: string, cost: number, position: Vector3, itemType: string, itemIndex: number)
	local button = Instance.new("Part")
	button.Name = `Button_{itemName}`
	button.Size = Vector3.new(6, 0.5, 6)
	button.Position = position
	button.Anchored = true
	button.Material = Enum.Material.Neon
	button.Color = Color3.fromRGB(0, 150, 255)
	button.Parent = plot

	button:SetAttribute("ItemType", itemType)
	button:SetAttribute("ItemIndex", itemIndex)
	button:SetAttribute("Cost", cost)
	button:SetAttribute("Purchased", false)

	local gui = Instance.new("BillboardGui")
	gui.Size = UDim2.new(0, 250, 0, 80)
	gui.StudsOffset = Vector3.new(0, 2, 0)
	gui.AlwaysOnTop = true
	gui.Parent = button

	local nameLabel = Instance.new("TextLabel")
	nameLabel.Size = UDim2.new(1, 0, 0.5, 0)
	nameLabel.BackgroundTransparency = 1
	nameLabel.Text = itemName
	nameLabel.TextColor3 = Color3.new(1, 1, 1)
	nameLabel.TextScaled = true
	nameLabel.Font = Enum.Font.GothamBold
	nameLabel.Parent = gui

	local costLabel = Instance.new("TextLabel")
	costLabel.Name = "CostLabel"
	costLabel.Size = UDim2.new(1, 0, 0.5, 0)
	costLabel.Position = UDim2.new(0, 0, 0.5, 0)
	costLabel.BackgroundTransparency = 1
	costLabel.Text = `${cost} Coins`
	costLabel.TextColor3 = Color3.fromRGB(255, 215, 0)
	costLabel.TextScaled = true
	costLabel.Font = Enum.Font.Gotham
	costLabel.Parent = gui

	-- Touch detection
	button.Touched:Connect(function(hit)
		local character = hit.Parent
		local player = Players:GetPlayerFromCharacter(character)
		if not player then return end

		local plotIndex = plot:GetAttribute("PlotIndex")
		if playerPlots[player.UserId] ~= plotIndex then return end
		if button:GetAttribute("Purchased") then return end

		PurchaseRemote:FireServer(plotIndex, itemType, itemIndex)
	end)
end

--------------------------------------------------------------------
-- SETUP PURCHASE BUTTONS ON PLOT
--------------------------------------------------------------------
local function setupPurchaseButtons(plot: Model)
	local plotIndex = plot:GetAttribute("PlotIndex")
	local pos = PLOT_POSITIONS[plotIndex]

	-- Dropper buttons along left side
	for i, dropper in Config.Droppers do
		if i > 1 then -- First dropper is free/auto
			local buttonPos = pos + Vector3.new(5, 0.25, 10 + (i - 2) * 10)
			createPurchaseButton(plot, dropper.name, dropper.cost, buttonPos, "dropper", i)
		end
	end

	-- Upgrader buttons along right side
	for i, upgrader in Config.Upgraders do
		local buttonPos = pos + Vector3.new(Config.Plots.PlotSize.X - 25, 0.25, 10 + (i - 1) * 12)
		createPurchaseButton(plot, upgrader.name, upgrader.cost, buttonPos, "upgrader", i)
	end
end

--------------------------------------------------------------------
-- DROPPER SYSTEM
--------------------------------------------------------------------
local function spawnDropper(plot: Model, dropperIndex: number)
	local plotIndex = plot:GetAttribute("PlotIndex")
	local plotState = plotData[plotIndex]
	if not plotState then return end

	local dropperConfig = Config.Droppers[dropperIndex]
	if not dropperConfig then return end

	local pos = PLOT_POSITIONS[plotIndex]
	local dropperPos = pos + Vector3.new(10, 4, 10 + (dropperIndex - 1) * 8)

	-- Create dropper model
	local dropper = Instance.new("Part")
	dropper.Name = `Dropper_{dropperConfig.name}`
	dropper.Size = Vector3.new(4, 4, 4)
	dropper.Position = dropperPos
	dropper.Anchored = true
	dropper.Material = Enum.Material.SmoothPlastic
	dropper.Color = dropperConfig.color
	dropper.Parent = plot

	local label = Instance.new("BillboardGui")
	label.Size = UDim2.new(0, 200, 0, 40)
	label.StudsOffset = Vector3.new(0, 3, 0)
	label.Parent = dropper

	local text = Instance.new("TextLabel")
	text.Size = UDim2.new(1, 0, 1, 0)
	text.BackgroundTransparency = 1
	text.Text = dropperConfig.name
	text.TextColor3 = Color3.new(1, 1, 1)
	text.TextScaled = true
	text.Font = Enum.Font.GothamBold
	text.Parent = label

	table.insert(plotState.items, dropper)

	-- Start production loop
	local thread = task.spawn(function()
		local convStartX = plot:GetAttribute("ConveyorStartX")
		local convStartZ = plot:GetAttribute("ConveyorStartZ")
		local convEndX = plot:GetAttribute("ConveyorEndX")
		local convEndZ = plot:GetAttribute("ConveyorEndZ")

		while plot.Parent and plotOwners[plotIndex] do
			task.wait(dropperConfig.dropInterval)

			-- Create resource orb
			local orb = Instance.new("Part")
			orb.Name = "ResourceOrb"
			orb.Shape = Enum.PartType.Ball
			orb.Size = Vector3.new(2, 2, 2)
			orb.Position = dropperPos + Vector3.new(0, -2, 0)
			orb.Anchored = true
			orb.Material = Enum.Material.Neon
			orb.Color = dropperConfig.color
			orb:SetAttribute("Value", dropperConfig.valuePerDrop)
			orb:SetAttribute("PlotIndex", plotIndex)
			orb.Parent = workspace

			-- Tween to conveyor start
			local tweenToConveyor = TweenService:Create(orb, TweenInfo.new(0.5), {
				Position = Vector3.new(convStartX, 1.5, convStartZ)
			})
			tweenToConveyor:Play()
			tweenToConveyor.Completed:Wait()

			-- Tween along conveyor to collector
			if orb.Parent then
				local tweenToCollector = TweenService:Create(orb, TweenInfo.new(3), {
					Position = Vector3.new(convEndX, 1.5, convEndZ)
				})
				tweenToCollector:Play()

				-- Auto-destroy after conveyor
				task.delay(4, function()
					if orb.Parent then
						-- Sell the orb
						local ownerId = plotOwners[plotIndex]
						if ownerId then
							local player = Players:GetPlayerByUserId(ownerId)
							if player then
								local value = orb:GetAttribute("Value") or 0
								local data = DataManager.GetData(player)
								if data then
									-- Apply rebirth multiplier
									local rebirthMultiplier = 1 + (data.rebirths * Config.Rebirth.PermanentBonus)
									value = math.floor(value * rebirthMultiplier)

									-- Apply pet multiplier
									local petMultiplier = 1
									if data.equippedPets then
										for _, petData in data.equippedPets do
											petMultiplier += (petData.multiplier - 1)
										end
									end
									value = math.floor(value * petMultiplier)

									DataManager.AddCoins(player, value)
								end
							end
						end
						orb:Destroy()
					end
				end)
			end
		end
	end)

	table.insert(plotState.dropperThreads, thread)
end

--------------------------------------------------------------------
-- UPGRADER SYSTEM
--------------------------------------------------------------------
local function spawnUpgrader(plot: Model, upgraderIndex: number)
	local plotIndex = plot:GetAttribute("PlotIndex")
	local plotState = plotData[plotIndex]
	if not plotState then return end

	local upgraderConfig = Config.Upgraders[upgraderIndex]
	if not upgraderConfig then return end

	local pos = PLOT_POSITIONS[plotIndex]
	local convStartX = plot:GetAttribute("ConveyorStartX")
	local convEndX = plot:GetAttribute("ConveyorEndX")
	local convZ = plot:GetAttribute("ConveyorStartZ")

	-- Position upgrader along conveyor path
	local fraction = upgraderIndex / (#Config.Upgraders + 1)
	local upgraderX = convStartX + (convEndX - convStartX) * fraction
	local upgraderPos = Vector3.new(upgraderX, 1, convZ)

	local upgrader = Instance.new("Part")
	upgrader.Name = `Upgrader_{upgraderConfig.name}`
	upgrader.Size = Vector3.new(6, 3, 6)
	upgrader.Position = upgraderPos
	upgrader.Anchored = true
	upgrader.Material = Enum.Material.ForceField
	upgrader.Color = upgraderConfig.color
	upgrader.CanCollide = false
	upgrader.Parent = plot

	local label = Instance.new("BillboardGui")
	label.Size = UDim2.new(0, 200, 0, 40)
	label.StudsOffset = Vector3.new(0, 3, 0)
	label.Parent = upgrader

	local text = Instance.new("TextLabel")
	text.Size = UDim2.new(1, 0, 1, 0)
	text.BackgroundTransparency = 1
	text.Text = `{upgraderConfig.name} (x{upgraderConfig.multiplier})`
	text.TextColor3 = Color3.new(1, 1, 1)
	text.TextScaled = true
	text.Font = Enum.Font.GothamBold
	text.Parent = label

	table.insert(plotState.items, upgrader)

	-- Upgrade orbs that touch this
	upgrader.Touched:Connect(function(hit)
		if hit.Name ~= "ResourceOrb" then return end
		local orbPlotIndex = hit:GetAttribute("PlotIndex")
		if orbPlotIndex ~= plotIndex then return end

		local alreadyUpgraded = hit:GetAttribute(`UpgradedBy_{upgraderConfig.name}`)
		if alreadyUpgraded then return end

		local currentValue = hit:GetAttribute("Value") or 0
		hit:SetAttribute("Value", math.floor(currentValue * upgraderConfig.multiplier))
		hit:SetAttribute(`UpgradedBy_{upgraderConfig.name}`, true)

		-- Visual feedback
		local originalColor = hit.Color
		hit.Color = upgraderConfig.color
		task.delay(0.3, function()
			if hit.Parent then
				hit.Color = originalColor
			end
		end)
	end)
end

--------------------------------------------------------------------
-- PLOT CLAIMING
--------------------------------------------------------------------
local function claimPlot(player: Player, plotIndex: number)
	if plotOwners[plotIndex] then return false end
	if playerPlots[player.UserId] then return false end

	plotOwners[plotIndex] = player.UserId
	playerPlots[player.UserId] = plotIndex
	plotData[plotIndex] = { dropperThreads = {}, items = {} }

	local plots = workspace:FindFirstChild("Plots")
	if not plots then return false end

	local plot = plots:FindFirstChild(`Plot_{plotIndex}`)
	if not plot then return false end

	-- Remove claim pad
	local claimPad = plot:FindFirstChild("ClaimPad")
	if claimPad then
		claimPad:Destroy()
	end

	-- Change floor color to show ownership
	local floor = plot:FindFirstChild("Floor")
	if floor then
		floor.Color = Color3.fromRGB(80, 140, 80)
	end

	-- Set up purchase buttons
	setupPurchaseButtons(plot)

	-- Spawn first dropper free
	spawnDropper(plot, 1)

	-- Load saved progress
	local data = DataManager.GetData(player)
	if data then
		for _, dropperIndex in data.ownedDroppers do
			if dropperIndex > 1 then
				spawnDropper(plot, dropperIndex)
			end
		end
		for _, upgraderIndex in data.ownedUpgraders do
			spawnUpgrader(plot, upgraderIndex)
		end
	end

	-- Notify ownership
	local ownerLabel = Instance.new("BillboardGui")
	ownerLabel.Name = "OwnerLabel"
	ownerLabel.Size = UDim2.new(0, 300, 0, 50)
	ownerLabel.StudsOffset = Vector3.new(0, 8, 0)
	ownerLabel.AlwaysOnTop = true
	ownerLabel.Parent = floor

	local ownerText = Instance.new("TextLabel")
	ownerText.Size = UDim2.new(1, 0, 1, 0)
	ownerText.BackgroundTransparency = 1
	ownerText.Text = `{player.Name}'s Factory`
	ownerText.TextColor3 = Color3.fromRGB(255, 255, 100)
	ownerText.TextScaled = true
	ownerText.Font = Enum.Font.GothamBold
	ownerText.Parent = ownerLabel

	return true
end

--------------------------------------------------------------------
-- CLEAR PLOT
--------------------------------------------------------------------
local function clearPlot(plotIndex: number)
	local plotState = plotData[plotIndex]
	if plotState then
		for _, thread in plotState.dropperThreads do
			task.cancel(thread)
		end
		for _, item in plotState.items do
			if item.Parent then
				item:Destroy()
			end
		end
	end

	plotOwners[plotIndex] = nil
	plotData[plotIndex] = nil

	-- Clean up orbs
	for _, obj in workspace:GetChildren() do
		if obj.Name == "ResourceOrb" and obj:GetAttribute("PlotIndex") == plotIndex then
			obj:Destroy()
		end
	end
end

--------------------------------------------------------------------
-- HANDLE PURCHASES
--------------------------------------------------------------------
local function handlePurchase(player: Player, plotIndex: number, itemType: string, itemIndex: number)
	if playerPlots[player.UserId] ~= plotIndex then return end

	local plots = workspace:FindFirstChild("Plots")
	if not plots then return end
	local plot = plots:FindFirstChild(`Plot_{plotIndex}`)
	if not plot then return end

	local data = DataManager.GetData(player)
	if not data then return end

	if itemType == "dropper" then
		local dropperConfig = Config.Droppers[itemIndex]
		if not dropperConfig then return end

		-- Check if already owned
		if table.find(data.ownedDroppers, itemIndex) then return end

		-- Check cost
		if not DataManager.SpendCoins(player, dropperConfig.cost) then return end

		-- Add to owned
		table.insert(data.ownedDroppers, itemIndex)

		-- Spawn it
		spawnDropper(plot, itemIndex)

		-- Disable purchase button
		local button = plot:FindFirstChild(`Button_{dropperConfig.name}`)
		if button then
			button.Transparency = 0.8
			button:SetAttribute("Purchased", true)
			local gui = button:FindFirstChildWhichIsA("BillboardGui")
			if gui then gui:Destroy() end
		end

	elseif itemType == "upgrader" then
		local upgraderConfig = Config.Upgraders[itemIndex]
		if not upgraderConfig then return end

		if table.find(data.ownedUpgraders, itemIndex) then return end
		if not DataManager.SpendCoins(player, upgraderConfig.cost) then return end

		table.insert(data.ownedUpgraders, itemIndex)
		spawnUpgrader(plot, itemIndex)

		local button = plot:FindFirstChild(`Button_{upgraderConfig.name}`)
		if button then
			button.Transparency = 0.8
			button:SetAttribute("Purchased", true)
			local gui = button:FindFirstChildWhichIsA("BillboardGui")
			if gui then gui:Destroy() end
		end
	end
end

--------------------------------------------------------------------
-- INIT
--------------------------------------------------------------------
local function init()
	-- Create plots folder
	local plotsFolder = Instance.new("Folder")
	plotsFolder.Name = "Plots"
	plotsFolder.Parent = workspace

	-- Create all plots
	for i = 1, Config.Plots.MaxPlots do
		createPlotBase(i)
	end

	-- Set up claim detection
	RunService.Heartbeat:Connect(function()
		for _, player in Players:GetPlayers() do
			if playerPlots[player.UserId] then continue end

			local character = player.Character
			if not character then continue end
			local rootPart = character:FindFirstChild("HumanoidRootPart")
			if not rootPart then continue end

			for i = 1, Config.Plots.MaxPlots do
				if plotOwners[i] then continue end

				local plots = workspace:FindFirstChild("Plots")
				if not plots then continue end
				local plot = plots:FindFirstChild(`Plot_{i}`)
				if not plot then continue end
				local claimPad = plot:FindFirstChild("ClaimPad")
				if not claimPad then continue end

				local distance = (rootPart.Position - claimPad.Position).Magnitude
				if distance < 8 then
					claimPlot(player, i)
				end
			end
		end
	end)

	-- Handle purchase remote
	PurchaseRemote.OnServerEvent:Connect(function(player, plotIndex, itemType, itemIndex)
		if typeof(plotIndex) ~= "number" then return end
		if typeof(itemType) ~= "string" then return end
		if typeof(itemIndex) ~= "number" then return end
		handlePurchase(player, plotIndex, itemType, itemIndex)
	end)

	-- Clean up on player leave
	Players.PlayerRemoving:Connect(function(player: Player)
		local plotIndex = playerPlots[player.UserId]
		if plotIndex then
			clearPlot(plotIndex)
			playerPlots[player.UserId] = nil
		end
	end)
end

init()

return TycoonManager
