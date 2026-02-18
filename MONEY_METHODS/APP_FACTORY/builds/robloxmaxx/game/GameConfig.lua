-- ReplicatedStorage/Modules/GameConfig
-- Shared configuration for Pet Factory Tycoon
-- All game numbers live here for easy balancing

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
				{ name = "Puppy",      rarity = "Common",    weight = 40, multiplier = 1.1 },
				{ name = "Kitten",     rarity = "Common",    weight = 30, multiplier = 1.15 },
				{ name = "Bunny",      rarity = "Uncommon",  weight = 15, multiplier = 1.3 },
				{ name = "Fox",        rarity = "Rare",      weight = 10, multiplier = 1.5 },
				{ name = "Dragon",     rarity = "Legendary", weight = 4,  multiplier = 2.0 },
				{ name = "Phoenix",    rarity = "Mythic",    weight = 1,  multiplier = 3.0 },
			}
		},
		{
			name = "Golden Egg",
			cost = 50000,
			color = Color3.fromRGB(255, 215, 0),
			pets = {
				{ name = "Golden Pup",    rarity = "Uncommon",  weight = 35, multiplier = 1.5 },
				{ name = "Golden Cat",    rarity = "Uncommon",  weight = 25, multiplier = 1.6 },
				{ name = "Golden Fox",    rarity = "Rare",      weight = 20, multiplier = 2.0 },
				{ name = "Golden Dragon", rarity = "Legendary", weight = 15, multiplier = 3.5 },
				{ name = "Golden Phoenix",rarity = "Mythic",    weight = 5,  multiplier = 5.0 },
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
	DoubleEarnings = { id = 1704197526, name = "2x Earnings",     price = 199, description = "All earnings doubled permanently" },
	AutoCollect    = { id = 1704265496, name = "Auto-Collect",     price = 149, description = "Resources auto-sell without collector" },
	VIPAccess      = { id = 1704391421, name = "VIP Area",         price = 299, description = "Access exclusive high-tier droppers" },
	ExtraSlot      = { id = 1703792075, name = "Extra Pet Slot",   price = 99,  description = "+1 equipped pet slot" },
	InstantRebirth = { id = 1703708188, name = "Instant Rebirth",  price = 399, description = "Rebirth without currency cost" },
}

Config.DevProducts = {
	SmallCash  = { id = 73101791, amount = 10000,   price = 49,  name = "10K Coins" },
	MediumCash = { id = 73101792, amount = 50000,   price = 199, name = "50K Coins" },
	LargeCash  = { id = 73101793, amount = 250000,  price = 799, name = "250K Coins" },
	MegaCash   = { id = 73101794, amount = 1000000, price = 1999, name = "1M Coins" },
}

Config.Codes = {
	LAUNCH2026  = { reward = "coins", amount = 5000,  uses = -1 },
	PETFACTORY  = { reward = "coins", amount = 10000, uses = -1 },
	THANKYOU    = { reward = "coins", amount = 25000, uses = -1 },
}

return Config
