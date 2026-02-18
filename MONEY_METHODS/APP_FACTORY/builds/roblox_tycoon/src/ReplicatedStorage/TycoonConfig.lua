--[[
	TycoonConfig.lua
	Central configuration for AI Factory Tycoon

	All game balance, prices, gamepass IDs, and settings in one place.
	Edit this file to adjust game economy and monetization.

	IMPORTANT: Gamepass IDs and Developer Product IDs must be set
	in the Roblox Creator Dashboard AFTER you publish the game.
--]]

local TycoonConfig = {}

--[[
	STARTING SETTINGS
--]]
TycoonConfig.STARTING_CASH = 100
TycoonConfig.BASE_MONEY_AMOUNT = 10 -- money per drop
TycoonConfig.MONEY_SPAWN_RATE = 2 -- seconds between money spawns

--[[
	GAMEPASS IDs (SET THESE AFTER CREATING GAMEPASSES)

	How to get gamepass IDs:
	1. Publish game to Roblox
	2. Go to Creator Dashboard → Your Experience → Monetization → Passes
	3. Create gamepasses
	4. Copy the ID from the URL or the gamepass page
	5. Paste IDs here
--]]
TycoonConfig.GAMEPASSES = {
	VIP = 0, -- REPLACE WITH REAL ID
	AutoCollect = 0, -- REPLACE WITH REAL ID
	PremiumSkin = 0, -- REPLACE WITH REAL ID
	CashBoost = 0 -- REPLACE WITH REAL ID
}

--[[
	GAMEPASS CONFIGS (for UI display)
--]]
TycoonConfig.GAMEPASS_CONFIGS = {
	VIP = {
		name = "VIP Pass",
		description = "2x money speed forever",
		price = 400 -- Robux
	},
	AutoCollect = {
		name = "Auto-Collect",
		description = "Money collects automatically",
		price = 250
	},
	PremiumSkin = {
		name = "Premium Skin",
		description = "Neon blue tycoon theme",
		price = 150
	},
	CashBoost = {
		name = "Cash Boost",
		description = "Start with +$10K",
		price = 80
	}
}

--[[
	DEVELOPER PRODUCT IDs (SET THESE AFTER CREATING PRODUCTS)

	How to get product IDs:
	1. Publish game to Roblox
	2. Go to Creator Dashboard → Your Experience → Monetization → Developer Products
	3. Create products
	4. Copy the product ID
	5. Paste IDs here
--]]
TycoonConfig.DEVELOPER_PRODUCTS = {
	Cash50K = {
		id = 0, -- REPLACE WITH REAL ID
		type = "cash",
		amount = 50000
	},
	Cash200K = {
		id = 0, -- REPLACE WITH REAL ID
		type = "cash",
		amount = 200000
	},
	SkipTimer = {
		id = 0, -- REPLACE WITH REAL ID
		type = "skipTimer",
		amount = 0
	}
}

--[[
	DEVELOPER PRODUCT CONFIGS (for UI display)
--]]
TycoonConfig.PRODUCT_CONFIGS = {
	Cash50K = {
		name = "$50K Cash Pack",
		description = "Instant $50,000 cash",
		price = 150 -- Robux
	},
	Cash200K = {
		name = "$200K Cash Pack",
		description = "Instant $200,000 cash",
		price = 400
	},
	SkipTimer = {
		name = "Skip Timer",
		description = "Instant upgrade completion",
		price = 80
	}
}

--[[
	UPGRADE DEFINITIONS

	Sequential progression: Button1 → Button2 → Button3, etc.
	Each upgrade has:
	- price: cost in cash
	- prerequisite: previous upgrade ID (nil for first upgrade)
	- modelName: name of model in ReplicatedStorage.UpgradeModels
	- position: Vector3 position relative to tycoon base
	- name: display name for button UI
--]]
TycoonConfig.UPGRADES = {
	Button1 = {
		price = 100,
		prerequisite = nil,
		modelName = "BasicServer",
		position = Vector3.new(0, 0, 10),
		name = "Basic Server"
	},
	Button2 = {
		price = 250,
		prerequisite = "Button1",
		modelName = "GPURack",
		position = Vector3.new(5, 0, 10),
		name = "GPU Rack"
	},
	Button3 = {
		price = 500,
		prerequisite = "Button2",
		modelName = "DataCenter",
		position = Vector3.new(10, 0, 10),
		name = "Data Center"
	},
	Button4 = {
		price = 1000,
		prerequisite = "Button3",
		modelName = "QuantumComputer",
		position = Vector3.new(0, 0, 15),
		name = "Quantum Computer"
	},
	Button5 = {
		price = 2500,
		prerequisite = "Button4",
		modelName = "AICore",
		position = Vector3.new(5, 0, 15),
		name = "AI Core"
	},
	Button6 = {
		price = 5000,
		prerequisite = "Button5",
		modelName = "SuperCluster",
		position = Vector3.new(10, 0, 15),
		name = "Super Cluster"
	},
	Button7 = {
		price = 10000,
		prerequisite = "Button6",
		modelName = "NeuralNetwork",
		position = Vector3.new(0, 0, 20),
		name = "Neural Network"
	},
	Button8 = {
		price = 25000,
		prerequisite = "Button7",
		modelName = "AGILab",
		position = Vector3.new(5, 0, 20),
		name = "AGI Lab"
	},
	Button9 = {
		price = 50000,
		prerequisite = "Button8",
		modelName = "SingularityHub",
		position = Vector3.new(10, 0, 20),
		name = "Singularity Hub"
	},
	Button10 = {
		price = 100000,
		prerequisite = "Button9",
		modelName = "MatrioshkaBrain",
		position = Vector3.new(15, 0, 20),
		name = "Matrioshka Brain"
	}
}

return TycoonConfig
