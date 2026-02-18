-- ServerScriptService/PetSystem
-- Egg hatching, pet equipping, multiplier bonuses

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("GameConfig"))
local DataManager = require(game:GetService("ServerScriptService"):WaitForChild("DataManager"))

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local HatchEgg = Remotes:WaitForChild("HatchEgg")
local EquipPet = Remotes:WaitForChild("EquipPet")
local UpdatePets = Remotes:WaitForChild("UpdatePets")

local PetSystem = {}

local function weightedRandom(pets: {{name: string, weight: number}}): {name: string, weight: number}
	local totalWeight = 0
	for _, pet in pets do
		totalWeight += pet.weight
	end

	local roll = math.random() * totalWeight
	local cumulative = 0
	for _, pet in pets do
		cumulative += pet.weight
		if roll <= cumulative then
			return pet
		end
	end
	return pets[#pets]
end

function PetSystem.HatchEgg(player: Player, eggIndex: number): {name: string, rarity: string, multiplier: number}?
	local data = DataManager.GetData(player)
	if not data then return nil end

	local eggConfig = Config.Pets.Eggs[eggIndex]
	if not eggConfig then return nil end

	if not DataManager.SpendCoins(player, eggConfig.cost) then return nil end

	if not data.pets then data.pets = {} end
	if #data.pets >= Config.Pets.MaxOwned then return nil end

	local result = weightedRandom(eggConfig.pets)

	local petData = {
		name = result.name,
		rarity = result.rarity,
		multiplier = result.multiplier,
		id = `{result.name}_{os.time()}_{math.random(1000, 9999)}`,
	}

	table.insert(data.pets, petData)

	UpdatePets:FireClient(player, data.pets, data.equippedPets)

	return petData
end

function PetSystem.EquipPet(player: Player, petId: string): boolean
	local data = DataManager.GetData(player)
	if not data then return false end
	if not data.pets or not data.equippedPets then return false end

	-- Check if pet exists in inventory
	local petFound = false
	for _, pet in data.pets do
		if pet.id == petId then
			petFound = true
			break
		end
	end
	if not petFound then return false end

	-- Check if already equipped
	for i, equipped in data.equippedPets do
		if equipped.id == petId then
			-- Unequip
			table.remove(data.equippedPets, i)
			UpdatePets:FireClient(player, data.pets, data.equippedPets)
			return true
		end
	end

	-- Check max slots
	local maxSlots = Config.Pets.MaxEquipped
	-- TODO: check ExtraSlot gamepass
	if #data.equippedPets >= maxSlots then return false end

	-- Find pet data and equip
	for _, pet in data.pets do
		if pet.id == petId then
			table.insert(data.equippedPets, pet)
			UpdatePets:FireClient(player, data.pets, data.equippedPets)
			return true
		end
	end

	return false
end

function PetSystem.GetMultiplier(player: Player): number
	local data = DataManager.GetData(player)
	if not data or not data.equippedPets then return 1 end

	local mult = 1
	for _, pet in data.equippedPets do
		mult += (pet.multiplier - 1)
	end
	return mult
end

-- Remote handlers
HatchEgg.OnServerEvent:Connect(function(player: Player, eggIndex: number)
	if typeof(eggIndex) ~= "number" then return end
	if eggIndex < 1 or eggIndex > #Config.Pets.Eggs then return end

	local result = PetSystem.HatchEgg(player, eggIndex)
	if result then
		HatchEgg:FireClient(player, true, result)
	else
		HatchEgg:FireClient(player, false, nil)
	end
end)

EquipPet.OnServerEvent:Connect(function(player: Player, petId: string)
	if typeof(petId) ~= "string" then return end
	PetSystem.EquipPet(player, petId)
end)

-- Send pet data on join
Players.PlayerAdded:Connect(function(player: Player)
	task.wait(2)
	local data = DataManager.GetData(player)
	if data then
		if not data.pets then data.pets = {} end
		if not data.equippedPets then data.equippedPets = {} end
		UpdatePets:FireClient(player, data.pets, data.equippedPets)
	end
end)

return PetSystem
