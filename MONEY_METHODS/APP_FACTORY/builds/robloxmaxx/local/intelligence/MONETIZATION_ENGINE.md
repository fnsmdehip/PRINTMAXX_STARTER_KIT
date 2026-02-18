# Roblox Monetization Intelligence Engine

**Purpose:** Deep knowledge base for Claude Code when building monetized Roblox games. Every code decision should be informed by these patterns. This is not theory -- these are tested numbers from live games.

---

## Gamepass Pricing Psychology

### Price Tier Conversion Benchmarks

| Tier | Price Range (R$) | Conversion Rate | Buyer Psychology | Best For |
|------|-------------------|-----------------|------------------|----------|
| Impulse | 1-99 | 5-15% | No thought, "why not" | Cosmetics, small boosts, skip tutorial |
| Considered | 100-499 | 2-5% | Checks wallet, reads description | 2x earnings, VIP, tool packs |
| Premium | 500-1999 | 0.5-2% | Compares to alternatives, needs proof | Exclusive areas, permanent upgrades |
| Whale | 2000+ | <0.5% | Status-driven, completionist | "Ultimate" bundles, flex items |

### The Three Gamepasses Every Game Needs

**1. "2x Earnings" (99-199 R$)**
Highest converting gamepass across all genres. Period. Players see immediate value because the number on screen doubles. Implementation must be visible -- show the bonus amount in a different color next to the base amount.

```lua
-- Server: Apply 2x earnings multiplier
local MarketplaceService = game:GetService("MarketplaceService")
local DOUBLE_EARNINGS_ID = 0 -- Replace with real gamepass ID

local function getEarningsMultiplier(player: Player): number
    local multiplier = 1

    local success, ownsPass = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, DOUBLE_EARNINGS_ID)
    end)

    if success and ownsPass then
        multiplier = multiplier * 2
    end

    return multiplier
end

-- When awarding currency:
local function awardCurrency(player: Player, baseAmount: number)
    local multiplier = getEarningsMultiplier(player)
    local totalAmount = baseAmount * multiplier
    local bonusAmount = totalAmount - baseAmount

    -- Update player data
    local data = PlayerData[player.UserId]
    if data then
        data.Currency += totalAmount
    end

    -- Fire client to show earnings popup with bonus highlighted
    ReplicatedStorage.Events.ShowEarnings:FireClient(player, baseAmount, bonusAmount)
end
```

**2. "VIP" (399-499 R$)**
Must have VISIBLE benefits. Players who buy VIP want other players to see it. Three non-negotiable VIP features:
- Chat tag: `[VIP]` prefix in yellow/gold
- Sparkle/particle effect on character (subtle, not obnoxious)
- Exclusive area with actual gameplay value (not just a room)

```lua
-- Server: Apply VIP chat tag
local TextChatService = game:GetService("TextChatService")

TextChatService.OnIncomingMessage = function(message: TextChatMessage)
    local properties = Instance.new("TextChatMessageProperties")
    local player = game.Players:FindFirstChild(message.TextSource.Name)

    if player then
        local success, ownsVIP = pcall(function()
            return MarketplaceService:UserOwnsGamePassAsync(player.UserId, VIP_GAMEPASS_ID)
        end)

        if success and ownsVIP then
            properties.PrefixText = '<font color="#FFD700">[VIP]</font> ' .. message.PrefixText
        end
    end

    return properties
end

-- Server: VIP sparkle effect on character
local function applyVIPEffects(player: Player)
    local success, ownsVIP = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, VIP_GAMEPASS_ID)
    end)

    if success and ownsVIP then
        player.CharacterAdded:Connect(function(character)
            local sparkle = Instance.new("Sparkles")
            sparkle.SparkleColor = Color3.fromRGB(255, 215, 0)
            sparkle.Parent = character:WaitForChild("HumanoidRootPart")
        end)
    end
end
```

**3. "Starter Pack" or "Speed Boost" (49-99 R$)**
The cheapest gamepass is critical. It breaks the payment barrier. Once a player spends ANY Robux in your game, they are 4-6x more likely to spend again. This gamepass exists to convert free players into spenders. Give generous value. You make money on the second purchase.

```lua
-- Starter pack: Give a meaningful head start
local STARTER_PACK_ID = 0 -- Replace

local function grantStarterPack(player: Player)
    local data = PlayerData[player.UserId]
    if not data then return end

    -- Check if already claimed (one-time grant)
    if data.StarterPackClaimed then return end

    local success, ownsPass = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, STARTER_PACK_ID)
    end)

    if success and ownsPass and not data.StarterPackClaimed then
        data.Currency += 500 -- Generous starting currency
        data.StarterPackClaimed = true

        -- Also grant an exclusive tool/item
        grantItem(player, "StarterSword") -- or whatever fits the genre
    end
end
```

### Pricing Anti-Patterns (What Kills Revenue)

- Pricing ALL gamepasses at 1000+ R$: You lose impulse buyers entirely
- No free preview of paid features: Players need to SEE what they're missing
- Hidden gamepass shop: Must be accessible from main UI, not buried in menus
- No "owned" indicator: Players who already bought must see their investment reflected
- Pricing that competes with top games: A new game charging 2000 R$ for VIP while Blox Fruits charges 600 R$ will lose

---

## Developer Products (Repeatable Purchases)

### Anchor Pricing Pattern

The goal: make the Medium pack feel like the obvious best deal.

| Pack | Price (R$) | Currency Given | Value Ratio | Purpose |
|------|-----------|---------------|-------------|---------|
| Small | 25 | 100 coins | 4.0 coins/R$ | Anchor (looks bad on purpose) |
| Medium | 99 | 500 coins | 5.05 coins/R$ | **Target purchase** (best ratio visible) |
| Large | 249 | 1,000 coins | 4.02 coins/R$ | Looks worse than Medium |
| Mega | 499 | 3,000 coins | 6.01 coins/R$ | Whale bait (best actual ratio) |

The Medium pack must clearly show "+25% BONUS" or "BEST VALUE" badge. The Large pack exists to make Medium look smart and Mega look premium.

```lua
-- Server: ProcessReceipt for developer products
local function processReceipt(receiptInfo)
    local player = game.Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end

    local data = PlayerData[player.UserId]
    if not data then return Enum.ProductPurchaseDecision.NotProcessedYet end

    local productId = receiptInfo.ProductId
    local granted = false

    if productId == SMALL_PACK_ID then
        data.Currency += 100
        granted = true
    elseif productId == MEDIUM_PACK_ID then
        data.Currency += 500
        granted = true
    elseif productId == LARGE_PACK_ID then
        data.Currency += 1000
        granted = true
    elseif productId == MEGA_PACK_ID then
        data.Currency += 3000
        granted = true
    elseif productId == BOOST_30MIN_ID then
        data.BoostExpiry = os.time() + 1800 -- 30 minutes
        granted = true
    end

    if granted then
        -- Save immediately after purchase
        local success, err = pcall(function()
            DataStore:SetAsync(tostring(receiptInfo.PlayerId), data)
        end)

        if success then
            return Enum.ProductPurchaseDecision.PurchaseGranted
        end
    end

    return Enum.ProductPurchaseDecision.NotProcessedYet
end

MarketplaceService.ProcessReceipt = processReceipt
```

### Consumable Boost Products

Timed boosts (2x earnings for 30 min, 5x luck for 15 min) convert at 3-7% when:
1. The timer is visible on screen at all times
2. The boost effect is obvious (bigger numbers, particles, sound)
3. The prompt appears at natural "frustration" points (after a failed attempt, after seeing someone else succeed)

```lua
-- Client: Boost timer UI
local function startBoostTimer(duration: number, boostName: string)
    local timerFrame = PlayerGui.HUD.BoostTimer
    timerFrame.Visible = true
    timerFrame.BoostName.Text = boostName

    local remaining = duration
    while remaining > 0 do
        local minutes = math.floor(remaining / 60)
        local seconds = remaining % 60
        timerFrame.TimeText.Text = string.format("%d:%02d", minutes, seconds)

        -- Flash red when under 60 seconds (urgency drives repurchase)
        if remaining <= 60 then
            timerFrame.TimeText.TextColor3 = Color3.fromRGB(255, 80, 80)
        end

        task.wait(1)
        remaining -= 1
    end

    timerFrame.Visible = false
    -- Show "Boost Expired! Buy Again?" prompt
    showRepurchasePrompt(boostName)
end
```

### Skip Timer Products

Highest conversion during first 2 hours of play. New players have low patience and high curiosity. Place skip-timer prompts on:
- Building/crafting timers over 30 seconds
- Respawn cooldowns
- Unlock timers for new areas
- Egg hatching / loot opening timers

Price skip timers at 5-15 R$ each. Low enough for impulse, high enough to add up for whales.

---

## Creator Rewards Optimization

### How Creator Rewards Actually Work

Roblox pays 5 R$ per qualifying Active Spender (a user who has spent $9.99+ across Roblox in the past 60 days) who plays your game for 10+ consecutive minutes. The user must be among the first 3 games they play that day.

### Optimization Strategy

**Front-load the first 10 minutes aggressively:**

```
Minute 0-1: Instant action. Player is DOING something within 15 seconds of spawning.
Minute 1-3: Tutorial with rewards. Every 30 seconds, something positive happens.
Minute 3-5: First meaningful choice (pick a class, choose a path, name your pet).
Minute 5-7: First "wow" moment (rare drop, level up, unlock new area).
Minute 7-10: Social hook (show leaderboard, invite to trade, join team).
```

This 10-minute sequence is worth real money. A game with 1,000 qualifying Active Spenders per day at full 10-min retention generates roughly $570/month from Creator Rewards alone.

**"First 3 games" optimization:**
- Target off-peak hours for Sponsored Ads (early morning, when competition for "first 3 games" is lower)
- Make your game icon convey instant value (character + action + bright colors)
- Game title should include genre keyword for discoverability

### Revenue Projection Formulas

```
Gamepass Revenue (monthly, Robux):
  DAU x gamepass_conversion_rate x average_gamepass_price x 30

DevProduct Revenue (monthly, Robux):
  DAU x devproduct_conversion_rate x avg_transaction x purchases_per_user x 30

Creator Rewards (monthly, Robux):
  active_spender_DAU x qualifying_rate x 5 x 30

Total Monthly Robux:
  gamepass_rev + devproduct_rev + creator_rewards + ad_revenue

USD Conversion:
  total_robux x 0.70 (Roblox cut) x $0.0038 per Robux (DevEx approximate rate)
```

**Worked example for a game with 500 DAU:**
```
Gamepasses: 500 x 0.03 x 200 = 3,000 R$/day = 90,000 R$/month
DevProducts: 500 x 0.05 x 50 x 1.5 = 1,875 R$/day = 56,250 R$/month
Creator Rewards: 75 active spenders x 0.6 qualifying x 5 = 225 R$/day = 6,750 R$/month
Total: 153,000 R$/month = ~$407/month USD after DevEx

Scale to 5,000 DAU: ~$4,070/month
Scale to 50,000 DAU: ~$40,700/month
```

---

## Time-Limited Events

### Revenue Impact

Events spike revenue 3-5x. A game earning $500/month can hit $1,500-$2,500 during a well-executed event. The event calendar for Roblox:

| Event Window | Theme | Revenue Multiplier | Notes |
|-------------|-------|-------------------|-------|
| Dec 15 - Jan 5 | Christmas/Winter | 4-5x | Highest spend period, gift card redemptions |
| Oct 15 - Nov 5 | Halloween | 3-4x | Horror/spooky items convert extremely well |
| Jun 1 - Aug 31 | Summer | 2-3x | Sustained higher DAU, kids out of school |
| Feb 1 - Feb 14 | Valentine's | 2x | Limited cosmetics, pair items |
| Mar/Apr (varies) | Easter/Spring | 2x | Egg hunts map perfectly to loot mechanics |

### Event Currency Pattern

Create a separate event currency that:
1. Is earned through event-specific gameplay (quests, bosses, exploration)
2. Can ALSO be purchased with Robux (developer product)
3. Buys exclusive items that disappear when the event ends
4. Has a visible countdown timer on the event shop

```lua
-- Server: Event shop with expiry
local EVENT_END_TIME = 1740000000 -- Unix timestamp for event end
local EVENT_CURRENCY_PRODUCT_ID = 0 -- DevProduct for buying event tokens

local EventShop = {
    { name = "Frost Crown", cost = 100, stock = math.huge },
    { name = "Ice Dragon Pet", cost = 500, stock = 500 },  -- Limited stock creates urgency
    { name = "Blizzard Aura", cost = 250, stock = math.huge },
    { name = "Legendary Frost Blade", cost = 1000, stock = 100 }, -- Ultra rare
}

local function isEventActive(): boolean
    return os.time() < EVENT_END_TIME
end

local function getTimeRemaining(): string
    local remaining = EVENT_END_TIME - os.time()
    if remaining <= 0 then return "EVENT ENDED" end

    local days = math.floor(remaining / 86400)
    local hours = math.floor((remaining % 86400) / 3600)
    return string.format("%dd %dh remaining", days, hours)
end

local function purchaseEventItem(player: Player, itemIndex: number)
    if not isEventActive() then
        warn("Event has ended")
        return false
    end

    local item = EventShop[itemIndex]
    if not item then return false end

    local data = PlayerData[player.UserId]
    if not data then return false end

    if (data.EventTokens or 0) < item.cost then
        return false -- Not enough tokens
    end

    if item.stock <= 0 then
        return false -- Sold out (creates FOMO)
    end

    data.EventTokens -= item.cost
    item.stock -= 1
    table.insert(data.Inventory, item.name)

    return true
end
```

### Event Announcement Cadence

- 7 days before: Teaser image on game thumbnail + social media
- 3 days before: Countdown timer appears in-game
- 1 day before: "TOMORROW" notification to all players who opted in
- Launch day: Update goes live at a specific time (creates event around the launch)
- Mid-event: "LIMITED TIME: Double event tokens this weekend"
- 3 days before end: "ENDING SOON" urgency on all event UI
- Final 24 hours: Stock counters on rare items (even if artificially limited)

---

## Age-Based Pricing Strategy

### Under 13 (Majority of Roblox)

These players have parental controls. Many need parent approval for any purchase. Strategy:
- Keep gamepasses under 99 R$ to minimize parental friction
- Focus on volume (many small purchases) over whale hunting
- Make free-to-play experience genuinely fun (or parents won't let them play at all)
- Cosmetics > power: parents are more comfortable with "my character looks cool" than "pay to win"

### 13-17 (Growing Segment)

These players often have their own Robux from gift cards or allowance. Strategy:
- 99-499 R$ sweet spot for gamepasses
- Social proof matters intensely ("everyone in my server has VIP")
- Limited items drive FOMO harder in this age group
- Trading systems create engagement loops independent of developer products

### 17+ (Fastest Growing, Highest LTV)

Roblox's 17+ content rating opened new demographics. Strategy:
- Higher price tolerance (can price gamepasses at 500-999 R$)
- More sophisticated monetization (battle passes, seasonal content)
- Quality expectations are higher (they compare to Steam/mobile games)
- Creator Subscriptions viable for this audience

---

## Purchase Prompt Placement

### Where to Show "Buy" Prompts (High Conversion Points)

1. **After death/failure:** "Revive instantly for 10 R$?" (frustration = spending)
2. **At progression walls:** "Unlock Area 2 now or collect 500 more coins" (impatience)
3. **When seeing someone else's paid item:** "Player123 has the Flame Sword! Get yours for 149 R$" (social proof)
4. **After first achievement:** "You're doing great! Level up faster with 2x Earnings" (positive reinforcement)
5. **On game entry (returning players):** "Welcome back! Daily Deal: 50% off Speed Boost" (habit formation)

### Where NOT to Show Prompts (Kills Retention)

- During active gameplay (mid-combat, mid-race)
- Within first 30 seconds (let them play first)
- More than once per 5 minutes for the same product
- Blocking the screen (overlay prompts > modal prompts)
- After a positive moment (don't interrupt joy with a cash register)

```lua
-- Server: Smart prompt timing
local PROMPT_COOLDOWNS = {} -- player -> product -> last_prompt_time
local COOLDOWN_SECONDS = 300 -- 5 minutes between same prompts

local function canShowPrompt(player: Player, productType: string): boolean
    local key = player.UserId .. "_" .. productType
    local lastPrompt = PROMPT_COOLDOWNS[key]

    if lastPrompt and (os.time() - lastPrompt) < COOLDOWN_SECONDS then
        return false
    end

    PROMPT_COOLDOWNS[key] = os.time()
    return true
end

-- After player dies:
local function onPlayerDied(player: Player)
    task.wait(1.5) -- Let them process the death

    if canShowPrompt(player, "revive") then
        ReplicatedStorage.Events.ShowRevivePrompt:FireClient(player)
    end
end
```

---

## Rewarded Video Ads

### Integration Strategy

Roblox's Immersive Ads allow in-game ad placements. Rewarded video ads let players watch a 30-second ad for an in-game reward. Conversion insights:

- Place ad portals near high-traffic areas (spawn, shop entrance)
- Reward should be 20-30% of the cheapest developer product value (enough to feel worthwhile, not enough to replace purchases)
- Limit to 3-5 views per player per day (diminishing returns after that)
- Label clearly: "Watch Ad for 50 Coins" not just a mysterious portal

```lua
-- Server: Rewarded ad grant with daily limit
local MAX_AD_VIEWS_PER_DAY = 5
local AD_REWARD_AMOUNT = 50

local function grantAdReward(player: Player)
    local data = PlayerData[player.UserId]
    if not data then return false end

    -- Reset daily counter
    local today = os.date("%Y-%m-%d")
    if data.LastAdDate ~= today then
        data.AdViewsToday = 0
        data.LastAdDate = today
    end

    if (data.AdViewsToday or 0) >= MAX_AD_VIEWS_PER_DAY then
        return false -- Daily limit reached
    end

    data.Currency += AD_REWARD_AMOUNT
    data.AdViewsToday = (data.AdViewsToday or 0) + 1

    return true
end
```

---

## Revenue Benchmarks by Genre

### What "Good" Looks Like

| DAU | Genre | Monthly USD (after DevEx) | Notes |
|-----|-------|--------------------------|-------|
| 100 | Simulator | $30-80 | Too small to matter, but validates concept |
| 500 | Simulator | $150-400 | Ramen profitable |
| 1,000 | Tycoon | $250-650 | Sustainable solo dev income possible |
| 5,000 | RPG | $2,000-6,000 | Full-time income |
| 10,000 | Any | $4,000-15,000 | Hire help, reinvest in ads |
| 50,000 | Any | $20,000-80,000 | Studio-level revenue |
| 100,000+ | Top tier | $50,000-300,000+ | Front page games |

### The 1,000 DAU Milestone

1,000 DAU is the critical threshold. Below it, revenue is negligible. At 1,000:
- Creator Rewards start adding meaningful income
- Conversion rates stabilize (enough sample size)
- You can A/B test pricing effectively
- Sponsoring the game becomes ROI-positive

**Getting to 1,000 DAU:** Sponsor the game (budget 10,000-50,000 R$), optimize icon/title for CTR, ensure first-session retention is above 20%, and update weekly to maintain sort algorithm favor.

---

## Common Monetization Mistakes

1. **No free path to fun.** If the game feels unplayable without spending, players leave (and leave bad ratings). Free players are your marketing.

2. **Pricing based on "what feels right" instead of data.** Start low, measure conversion, raise price only if conversion stays above 2%.

3. **One gamepass, no dev products.** You're leaving 60-70% of revenue on the table. Dev products (repeatable) generate more long-term revenue than gamepasses.

4. **No "first purchase" incentive.** The hardest conversion is $0 to $1. Make the first purchase absurdly generous. You profit on purchase #2, #3, #4.

5. **Ignoring mobile.** 60-70% of Roblox players are on mobile. If your purchase UI doesn't work on a phone screen, most of your audience can't buy.

6. **No social proof for purchases.** When someone buys VIP, announce it to the server. Show particle effects. Make other players WANT what the buyer has.

7. **Not saving purchase state correctly.** If a player buys something and it disappears, they request a refund AND never spend again. `ProcessReceipt` must be bulletproof. Save to DataStore BEFORE returning `PurchaseGranted`.
