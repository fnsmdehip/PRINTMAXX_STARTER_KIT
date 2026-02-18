# Pet Factory Tycoon

A complete Roblox tycoon game with pet collection mechanics.

## Game Loop
1. Player claims a plot
2. Droppers generate resource orbs
3. Orbs travel along conveyors to upgraders
4. Upgraded orbs reach the collector/seller
5. Currency earned → buy more droppers/upgraders
6. Hatch pets from eggs using currency
7. Pets give passive multipliers
8. Rebirth resets for permanent bonuses
9. Repeat

## Scripts
- `GameConfig.lua` - All game numbers (prices, multipliers, pets)
- `TycoonManager.lua` - Plot claiming, purchases, dropper loops
- `DataManager.lua` - Save/load with DataStoreService
- `EconomyManager.lua` - Currency, gamepasses, dev products
- `PetSystem.lua` - Egg hatching, equipping, pet bonuses
- `RebirthManager.lua` - Rebirth logic, permanent multipliers
- `TycoonHUD.lua` - Client UI (currency, buttons, pet display)
- `GameInstaller.lua` - Paste into Studio command bar to set up everything

## Installation
1. Open Roblox Studio → Create new Baseplate
2. Open View → Command Bar
3. Copy contents of `GameInstaller.lua`
4. Paste into command bar and press Enter
5. Wait for "INSTALLATION COMPLETE" in Output
6. Game is ready to test (click Play)

## Monetization
- 5 gamepasses (2x Earnings, Auto-Collect, VIP, Extra Slot, Instant Rebirth)
- 4 dev products (currency packs)
- Rewarded ad portals (optional)
