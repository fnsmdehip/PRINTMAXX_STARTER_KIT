--[[
    RobloxMaxx - AI Game Builder for Roblox Studio
    Enhanced Roblox Studio plugin that generates production-ready Luau code
    from natural language descriptions using Claude, GPT-4, or Gemini.

    API ARCHITECTURE (BYOK - Bring Your Own Key):
    This plugin makes direct HTTP API calls only. It never uses Claude
    Pro/Max subscription tokens through third-party tooling.

    Provider paths:
    1. "Claude"/"OpenAI"/"Gemini" providers: Calls the AI provider's API
       directly with the user's own API key. Our servers are not involved.
    2. "RobloxMaxx Pro" provider: Calls our SaaS API which injects premium
       context (meta advisor, genre intelligence) then forwards to the
       Anthropic API using the user's own API key. Pro subscription required.

    All paths use the USER's own API key. We never hold or pay for API keys.
    No MCP, no CLI tools, no subscription piggybacking.

    Features over competitors:
    - Genre-aware templates (tycoon, obby, simulator, RPG, horror)
    - Multi-step generation with context retention
    - Self-testing script generation
    - Full game scaffolding from a single prompt
    - Undo/redo with full script backup
    - Project save/load
    - Pro: meta advisor, revenue estimator, game scanner
]]

-- Services
local HttpService = game:GetService("HttpService")
local ScriptEditorService = game:GetService("ScriptEditorService")
local Selection = game:GetService("Selection")
local ServerScriptService = game:GetService("ServerScriptService")
local ServerStorage = game:GetService("ServerStorage")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local StarterGui = game:GetService("StarterGui")
local StarterPlayer = game:GetService("StarterPlayer")
local Workspace = game:GetService("Workspace")

--------------------------------------------------------------------
-- CONFIG
--------------------------------------------------------------------
local API_BASE_URL = "https://robloxmaxx.com/api" -- Production
-- local API_BASE_URL = "http://localhost:3000/api" -- Dev

local PLUGIN_VERSION = "2.0.0"

--------------------------------------------------------------------
-- STATE
--------------------------------------------------------------------
local apiKey = "" -- User's own API key (BYOK)
local userToken = "" -- RobloxMaxx Pro auth token (optional)
local selectedProvider = "claude" -- claude | openai | gemini | robloxmaxx pro
local currentMode = "code" -- code | question | scaffold | meta
local selectedGenre = "general" -- general | tycoon | obby | simulator | rpg | horror
local metaData = nil -- Cached meta advisor data
local scanResults = nil -- Cached game health scan results
local isProcessing = false
local changeHistory = {}
local scriptBackups = {}
local conversationContext = {} -- Multi-turn context

-- Services to scan for game context
local servicesToCheck = {
    ServerScriptService,
    Workspace,
    ReplicatedStorage,
    StarterGui,
    ServerStorage,
}

-- Add StarterPlayer children
pcall(function()
    table.insert(servicesToCheck, StarterPlayer:FindFirstChild("StarterPlayerScripts"))
    table.insert(servicesToCheck, StarterPlayer:FindFirstChild("StarterCharacterScripts"))
end)

--------------------------------------------------------------------
-- UI SETUP
--------------------------------------------------------------------
local toolbar = plugin:CreateToolbar("RobloxMaxx")
local toggleButton = toolbar:CreateButton(
    "RobloxMaxx",
    "AI Game Builder - Generate Roblox games from natural language",
    "rbxassetid://0" -- Replace with actual icon asset ID
)

local widgetInfo = DockWidgetPluginGuiInfo.new(
    Enum.InitialDockState.Right,
    false, -- Initially disabled
    false, -- Override previous enabled state
    400,   -- Default width
    600,   -- Default height
    300,   -- Minimum width
    400    -- Minimum height
)

local widget = plugin:CreateDockWidgetPluginGui("RobloxMaxxWidget", widgetInfo)
widget.Title = "RobloxMaxx AI"

-- Main container
local mainFrame = Instance.new("Frame")
mainFrame.Size = UDim2.new(1, 0, 1, 0)
mainFrame.BackgroundColor3 = Color3.fromRGB(18, 18, 24)
mainFrame.BorderSizePixel = 0
mainFrame.Parent = widget

local mainLayout = Instance.new("UIListLayout")
mainLayout.SortOrder = Enum.SortOrder.LayoutOrder
mainLayout.Padding = UDim.new(0, 6)
mainLayout.Parent = mainFrame

local mainPadding = Instance.new("UIPadding")
mainPadding.PaddingTop = UDim.new(0, 8)
mainPadding.PaddingBottom = UDim.new(0, 8)
mainPadding.PaddingLeft = UDim.new(0, 8)
mainPadding.PaddingRight = UDim.new(0, 8)
mainPadding.Parent = mainFrame

--------------------------------------------------------------------
-- UI HELPER FUNCTIONS
--------------------------------------------------------------------
local function createLabel(parent, text, order, size)
    local label = Instance.new("TextLabel")
    label.Size = size or UDim2.new(1, 0, 0, 20)
    label.BackgroundTransparency = 1
    label.Text = text
    label.TextColor3 = Color3.fromRGB(180, 180, 200)
    label.TextSize = 13
    label.Font = Enum.Font.GothamMedium
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.LayoutOrder = order
    label.Parent = parent
    return label
end

local function createButton(parent, text, order, color)
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(1, 0, 0, 36)
    btn.BackgroundColor3 = color or Color3.fromRGB(88, 101, 242)
    btn.Text = text
    btn.TextColor3 = Color3.fromRGB(255, 255, 255)
    btn.TextSize = 14
    btn.Font = Enum.Font.GothamBold
    btn.LayoutOrder = order
    btn.Parent = parent

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 6)
    corner.Parent = btn

    return btn
end

local function createTextInput(parent, placeholder, order, height)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(1, 0, 0, height or 36)
    container.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
    container.LayoutOrder = order
    container.Parent = parent

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 6)
    corner.Parent = container

    local input = Instance.new("TextBox")
    input.Size = UDim2.new(1, -16, 1, -8)
    input.Position = UDim2.new(0, 8, 0, 4)
    input.BackgroundTransparency = 1
    input.Text = ""
    input.PlaceholderText = placeholder
    input.PlaceholderColor3 = Color3.fromRGB(100, 100, 120)
    input.TextColor3 = Color3.fromRGB(220, 220, 240)
    input.TextSize = 13
    input.Font = Enum.Font.Gotham
    input.TextXAlignment = Enum.TextXAlignment.Left
    input.TextYAlignment = Enum.TextYAlignment.Top
    input.ClearTextOnFocus = false
    input.MultiLine = (height or 36) > 50
    input.TextWrapped = true
    input.Parent = container

    return input, container
end

local function createDropdown(parent, options, order)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(1, 0, 0, 36)
    container.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
    container.LayoutOrder = order
    container.Parent = parent

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 6)
    corner.Parent = container

    local currentIndex = 1

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, -40, 1, 0)
    label.Position = UDim2.new(0, 12, 0, 0)
    label.BackgroundTransparency = 1
    label.Text = options[1]
    label.TextColor3 = Color3.fromRGB(220, 220, 240)
    label.TextSize = 13
    label.Font = Enum.Font.Gotham
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Parent = container

    local cycleBtn = Instance.new("TextButton")
    cycleBtn.Size = UDim2.new(0, 30, 0, 30)
    cycleBtn.Position = UDim2.new(1, -35, 0, 3)
    cycleBtn.BackgroundTransparency = 1
    cycleBtn.Text = ">"
    cycleBtn.TextColor3 = Color3.fromRGB(150, 150, 170)
    cycleBtn.TextSize = 16
    cycleBtn.Font = Enum.Font.GothamBold
    cycleBtn.Parent = container

    cycleBtn.MouseButton1Click:Connect(function()
        currentIndex = (currentIndex % #options) + 1
        label.Text = options[currentIndex]
    end)

    return {
        container = container,
        label = label,
        getValue = function()
            return options[currentIndex]:lower()
        end,
        setValue = function(val)
            for i, opt in ipairs(options) do
                if opt:lower() == val:lower() then
                    currentIndex = i
                    label.Text = options[i]
                    break
                end
            end
        end,
    }
end

--------------------------------------------------------------------
-- REVENUE ESTIMATION CONFIG
--------------------------------------------------------------------
local CONVERSION_RATES = {
    simulator = 0.05,
    tycoon = 0.03,
    obby = 0.02,
    rpg = 0.04,
    horror = 0.01,
    general = 0.025,
}
local AVG_TRANSACTION_ROBUX = 150
local DEVEX_RATE = 0.0038

local function estimateRevenue(dau, genre, hasGamepasses, hasDevProducts, hasAds)
    local convRate = CONVERSION_RATES[genre] or 0.025

    -- Adjust conversion based on monetization types active
    local monetizationMultiplier = 0
    if hasGamepasses then monetizationMultiplier += 0.6 end
    if hasDevProducts then monetizationMultiplier += 0.3 end
    if hasAds then monetizationMultiplier += 0.1 end
    if monetizationMultiplier == 0 then monetizationMultiplier = 0.5 end -- fallback

    local baseMonthly = dau * convRate * AVG_TRANSACTION_ROBUX * 30 * 0.70
    local adjustedMonthly = baseMonthly * monetizationMultiplier

    local lowRobux = math.floor(adjustedMonthly * 0.5)
    local midRobux = math.floor(adjustedMonthly)
    local highRobux = math.floor(adjustedMonthly * 1.8)

    return {
        lowRobux = lowRobux,
        midRobux = midRobux,
        highRobux = highRobux,
        lowUSD = string.format("$%.2f", lowRobux * DEVEX_RATE),
        midUSD = string.format("$%.2f", midRobux * DEVEX_RATE),
        highUSD = string.format("$%.2f", highRobux * DEVEX_RATE),
    }
end

--------------------------------------------------------------------
-- GENRE HEALTH STATUS COLORS
--------------------------------------------------------------------
local HEALTH_COLORS = {
    HOT = Color3.fromRGB(255, 80, 80),
    WARM = Color3.fromRGB(255, 180, 50),
    COLD = Color3.fromRGB(100, 160, 255),
    DEAD = Color3.fromRGB(100, 100, 120),
}

local SCAN_SCORE_COLORS = {
    green = Color3.fromRGB(80, 220, 80),
    yellow = Color3.fromRGB(255, 220, 50),
    orange = Color3.fromRGB(255, 150, 50),
    red = Color3.fromRGB(255, 70, 70),
}

local function getScoreColor(score)
    if score >= 90 then return SCAN_SCORE_COLORS.green
    elseif score >= 70 then return SCAN_SCORE_COLORS.yellow
    elseif score >= 50 then return SCAN_SCORE_COLORS.orange
    else return SCAN_SCORE_COLORS.red end
end

--------------------------------------------------------------------
-- BUILD UI
--------------------------------------------------------------------

-- Header
local header = Instance.new("TextLabel")
header.Size = UDim2.new(1, 0, 0, 30)
header.BackgroundTransparency = 1
header.Text = "ROBLOXMAXX AI"
header.TextColor3 = Color3.fromRGB(88, 101, 242)
header.TextSize = 18
header.Font = Enum.Font.GothamBlack
header.LayoutOrder = 0
header.Parent = mainFrame

-- Auth section
createLabel(mainFrame, "Your AI API Key (BYOK)", 1)
local authInput = createTextInput(mainFrame, "Enter your Claude/OpenAI/Gemini API key...", 2)

-- Provider dropdown
createLabel(mainFrame, "AI Provider", 3)
local providerDropdown = createDropdown(mainFrame, {"Claude", "OpenAI", "Gemini", "RobloxMaxx Pro"}, 4)

-- Genre dropdown
createLabel(mainFrame, "Game Genre", 5)
local genreDropdown = createDropdown(mainFrame, {"General", "Tycoon", "Obby", "Simulator", "RPG", "Horror"}, 6)

-- Mode buttons
local modeFrame = Instance.new("Frame")
modeFrame.Size = UDim2.new(1, 0, 0, 36)
modeFrame.BackgroundTransparency = 1
modeFrame.LayoutOrder = 7
modeFrame.Parent = mainFrame

local modeLayout = Instance.new("UIListLayout")
modeLayout.FillDirection = Enum.FillDirection.Horizontal
modeLayout.SortOrder = Enum.SortOrder.LayoutOrder
modeLayout.Padding = UDim.new(0, 4)
modeLayout.Parent = modeFrame

local codeBtn = Instance.new("TextButton")
codeBtn.Size = UDim2.new(0.22, -2, 1, 0)
codeBtn.BackgroundColor3 = Color3.fromRGB(88, 101, 242)
codeBtn.Text = "Code"
codeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
codeBtn.TextSize = 12
codeBtn.Font = Enum.Font.GothamBold
codeBtn.LayoutOrder = 1
codeBtn.Parent = modeFrame
Instance.new("UICorner", codeBtn).CornerRadius = UDim.new(0, 4)

local questionBtn = Instance.new("TextButton")
questionBtn.Size = UDim2.new(0.22, -2, 1, 0)
questionBtn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
questionBtn.Text = "Ask"
questionBtn.TextColor3 = Color3.fromRGB(180, 180, 200)
questionBtn.TextSize = 12
questionBtn.Font = Enum.Font.GothamBold
questionBtn.LayoutOrder = 2
questionBtn.Parent = modeFrame
Instance.new("UICorner", questionBtn).CornerRadius = UDim.new(0, 4)

local scaffoldBtn = Instance.new("TextButton")
scaffoldBtn.Size = UDim2.new(0.28, -2, 1, 0)
scaffoldBtn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
scaffoldBtn.Text = "Scaffold"
scaffoldBtn.TextColor3 = Color3.fromRGB(180, 180, 200)
scaffoldBtn.TextSize = 12
scaffoldBtn.Font = Enum.Font.GothamBold
scaffoldBtn.LayoutOrder = 3
scaffoldBtn.Parent = modeFrame
Instance.new("UICorner", scaffoldBtn).CornerRadius = UDim.new(0, 4)

local metaBtn = Instance.new("TextButton")
metaBtn.Size = UDim2.new(0.28, -2, 1, 0)
metaBtn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
metaBtn.Text = "Meta"
metaBtn.TextColor3 = Color3.fromRGB(180, 180, 200)
metaBtn.TextSize = 12
metaBtn.Font = Enum.Font.GothamBold
metaBtn.LayoutOrder = 4
metaBtn.Parent = modeFrame
Instance.new("UICorner", metaBtn).CornerRadius = UDim.new(0, 4)

-- Panels for different modes (shown/hidden based on currentMode)
-- Code/Ask/Scaffold share the existing prompt + generate layout
-- Meta mode has its own panel

-- Meta panel container (hidden by default, placed after mode buttons)
local metaPanel = Instance.new("Frame")
metaPanel.Size = UDim2.new(1, 0, 1, -260) -- Takes remaining space below mode buttons
metaPanel.BackgroundTransparency = 1
metaPanel.LayoutOrder = 50
metaPanel.Visible = false
metaPanel.Parent = mainFrame

local metaPanelLayout = Instance.new("UIListLayout")
metaPanelLayout.SortOrder = Enum.SortOrder.LayoutOrder
metaPanelLayout.Padding = UDim.new(0, 6)
metaPanelLayout.Parent = metaPanel

-- Meta sub-tabs: Genre Health | Revenue Estimator | Game Scanner
local metaSubTabFrame = Instance.new("Frame")
metaSubTabFrame.Size = UDim2.new(1, 0, 0, 30)
metaSubTabFrame.BackgroundTransparency = 1
metaSubTabFrame.LayoutOrder = 0
metaSubTabFrame.Parent = metaPanel

local metaSubTabLayout = Instance.new("UIListLayout")
metaSubTabLayout.FillDirection = Enum.FillDirection.Horizontal
metaSubTabLayout.SortOrder = Enum.SortOrder.LayoutOrder
metaSubTabLayout.Padding = UDim.new(0, 3)
metaSubTabLayout.Parent = metaSubTabFrame

local currentMetaSubTab = "genres" -- genres | revenue | scan

local genresSubBtn = Instance.new("TextButton")
genresSubBtn.Size = UDim2.new(0.33, -2, 1, 0)
genresSubBtn.BackgroundColor3 = Color3.fromRGB(60, 70, 140)
genresSubBtn.Text = "Genres"
genresSubBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
genresSubBtn.TextSize = 11
genresSubBtn.Font = Enum.Font.GothamBold
genresSubBtn.LayoutOrder = 1
genresSubBtn.Parent = metaSubTabFrame
Instance.new("UICorner", genresSubBtn).CornerRadius = UDim.new(0, 4)

local revenueSubBtn = Instance.new("TextButton")
revenueSubBtn.Size = UDim2.new(0.33, -2, 1, 0)
revenueSubBtn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
revenueSubBtn.Text = "Revenue"
revenueSubBtn.TextColor3 = Color3.fromRGB(180, 180, 200)
revenueSubBtn.TextSize = 11
revenueSubBtn.Font = Enum.Font.GothamBold
revenueSubBtn.LayoutOrder = 2
revenueSubBtn.Parent = metaSubTabFrame
Instance.new("UICorner", revenueSubBtn).CornerRadius = UDim.new(0, 4)

local scanSubBtn = Instance.new("TextButton")
scanSubBtn.Size = UDim2.new(0.34, -2, 1, 0)
scanSubBtn.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
scanSubBtn.Text = "Scan"
scanSubBtn.TextColor3 = Color3.fromRGB(180, 180, 200)
scanSubBtn.TextSize = 11
scanSubBtn.Font = Enum.Font.GothamBold
scanSubBtn.LayoutOrder = 3
scanSubBtn.Parent = metaSubTabFrame
Instance.new("UICorner", scanSubBtn).CornerRadius = UDim.new(0, 4)

--------------------------------------------------------------------
-- META: GENRE HEALTH PANEL
--------------------------------------------------------------------
local genresPanel = Instance.new("ScrollingFrame")
genresPanel.Size = UDim2.new(1, 0, 1, -44)
genresPanel.BackgroundColor3 = Color3.fromRGB(22, 22, 30)
genresPanel.BorderSizePixel = 0
genresPanel.ScrollBarThickness = 4
genresPanel.LayoutOrder = 1
genresPanel.Parent = metaPanel
Instance.new("UICorner", genresPanel).CornerRadius = UDim.new(0, 6)

local genresPanelLayout = Instance.new("UIListLayout")
genresPanelLayout.SortOrder = Enum.SortOrder.LayoutOrder
genresPanelLayout.Padding = UDim.new(0, 2)
genresPanelLayout.Parent = genresPanel

local genresPanelPad = Instance.new("UIPadding")
genresPanelPad.PaddingTop = UDim.new(0, 6)
genresPanelPad.PaddingLeft = UDim.new(0, 6)
genresPanelPad.PaddingRight = UDim.new(0, 6)
genresPanelPad.Parent = genresPanel

-- Loading label for genre health
local genresLoadingLabel = Instance.new("TextLabel")
genresLoadingLabel.Size = UDim2.new(1, 0, 0, 30)
genresLoadingLabel.BackgroundTransparency = 1
genresLoadingLabel.Text = "Click 'Refresh' to load genre health data"
genresLoadingLabel.TextColor3 = Color3.fromRGB(120, 120, 150)
genresLoadingLabel.TextSize = 11
genresLoadingLabel.Font = Enum.Font.Gotham
genresLoadingLabel.TextWrapped = true
genresLoadingLabel.LayoutOrder = 0
genresLoadingLabel.Parent = genresPanel

local refreshMetaBtn = createButton(metaPanel, "Refresh Genre Data", 2, Color3.fromRGB(60, 70, 140))
refreshMetaBtn.Size = UDim2.new(1, 0, 0, 30)

--------------------------------------------------------------------
-- META: REVENUE ESTIMATOR PANEL
--------------------------------------------------------------------
local revenuePanel = Instance.new("Frame")
revenuePanel.Size = UDim2.new(1, 0, 1, -44)
revenuePanel.BackgroundColor3 = Color3.fromRGB(22, 22, 30)
revenuePanel.LayoutOrder = 1
revenuePanel.Visible = false
revenuePanel.Parent = metaPanel
Instance.new("UICorner", revenuePanel).CornerRadius = UDim.new(0, 6)

local revLayout = Instance.new("UIListLayout")
revLayout.SortOrder = Enum.SortOrder.LayoutOrder
revLayout.Padding = UDim.new(0, 5)
revLayout.Parent = revenuePanel

local revPad = Instance.new("UIPadding")
revPad.PaddingTop = UDim.new(0, 8)
revPad.PaddingLeft = UDim.new(0, 8)
revPad.PaddingRight = UDim.new(0, 8)
revPad.PaddingBottom = UDim.new(0, 8)
revPad.Parent = revenuePanel

-- DAU input
local dauLabel = Instance.new("TextLabel")
dauLabel.Size = UDim2.new(1, 0, 0, 16)
dauLabel.BackgroundTransparency = 1
dauLabel.Text = "Expected Daily Active Users"
dauLabel.TextColor3 = Color3.fromRGB(180, 180, 200)
dauLabel.TextSize = 11
dauLabel.Font = Enum.Font.GothamMedium
dauLabel.TextXAlignment = Enum.TextXAlignment.Left
dauLabel.LayoutOrder = 0
dauLabel.Parent = revenuePanel

local dauInputContainer = Instance.new("Frame")
dauInputContainer.Size = UDim2.new(1, 0, 0, 30)
dauInputContainer.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
dauInputContainer.LayoutOrder = 1
dauInputContainer.Parent = revenuePanel
Instance.new("UICorner", dauInputContainer).CornerRadius = UDim.new(0, 6)

local dauInput = Instance.new("TextBox")
dauInput.Size = UDim2.new(1, -12, 1, -6)
dauInput.Position = UDim2.new(0, 6, 0, 3)
dauInput.BackgroundTransparency = 1
dauInput.Text = ""
dauInput.PlaceholderText = "e.g. 500"
dauInput.PlaceholderColor3 = Color3.fromRGB(100, 100, 120)
dauInput.TextColor3 = Color3.fromRGB(220, 220, 240)
dauInput.TextSize = 13
dauInput.Font = Enum.Font.Gotham
dauInput.TextXAlignment = Enum.TextXAlignment.Left
dauInput.ClearTextOnFocus = false
dauInput.Parent = dauInputContainer

-- Genre selector for revenue (reuses values)
local revGenreLabel = Instance.new("TextLabel")
revGenreLabel.Size = UDim2.new(1, 0, 0, 16)
revGenreLabel.BackgroundTransparency = 1
revGenreLabel.Text = "Genre"
revGenreLabel.TextColor3 = Color3.fromRGB(180, 180, 200)
revGenreLabel.TextSize = 11
revGenreLabel.Font = Enum.Font.GothamMedium
revGenreLabel.TextXAlignment = Enum.TextXAlignment.Left
revGenreLabel.LayoutOrder = 2
revGenreLabel.Parent = revenuePanel

local revGenreDropdown = createDropdown(revenuePanel, {"Tycoon", "Obby", "Simulator", "RPG", "Horror", "General"}, 3)

-- Monetization checkboxes
local monLabel = Instance.new("TextLabel")
monLabel.Size = UDim2.new(1, 0, 0, 16)
monLabel.BackgroundTransparency = 1
monLabel.Text = "Monetization Types"
monLabel.TextColor3 = Color3.fromRGB(180, 180, 200)
monLabel.TextSize = 11
monLabel.Font = Enum.Font.GothamMedium
monLabel.TextXAlignment = Enum.TextXAlignment.Left
monLabel.LayoutOrder = 4
monLabel.Parent = revenuePanel

local monFrame = Instance.new("Frame")
monFrame.Size = UDim2.new(1, 0, 0, 24)
monFrame.BackgroundTransparency = 1
monFrame.LayoutOrder = 5
monFrame.Parent = revenuePanel

local monFlowLayout = Instance.new("UIListLayout")
monFlowLayout.FillDirection = Enum.FillDirection.Horizontal
monFlowLayout.SortOrder = Enum.SortOrder.LayoutOrder
monFlowLayout.Padding = UDim.new(0, 6)
monFlowLayout.Parent = monFrame

-- Checkbox helper
local checkboxStates = { gamepasses = true, devproducts = true, ads = false }

local function createCheckbox(parent, labelText, stateKey, order)
    local cbFrame = Instance.new("Frame")
    cbFrame.Size = UDim2.new(0, 100, 1, 0)
    cbFrame.BackgroundTransparency = 1
    cbFrame.LayoutOrder = order
    cbFrame.Parent = parent

    local cbBtn = Instance.new("TextButton")
    cbBtn.Size = UDim2.new(0, 16, 0, 16)
    cbBtn.Position = UDim2.new(0, 0, 0.5, -8)
    cbBtn.BackgroundColor3 = checkboxStates[stateKey] and Color3.fromRGB(88, 101, 242) or Color3.fromRGB(50, 50, 65)
    cbBtn.Text = checkboxStates[stateKey] and "X" or ""
    cbBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    cbBtn.TextSize = 10
    cbBtn.Font = Enum.Font.GothamBold
    cbBtn.Parent = cbFrame
    Instance.new("UICorner", cbBtn).CornerRadius = UDim.new(0, 3)

    local cbLabel = Instance.new("TextLabel")
    cbLabel.Size = UDim2.new(1, -22, 1, 0)
    cbLabel.Position = UDim2.new(0, 22, 0, 0)
    cbLabel.BackgroundTransparency = 1
    cbLabel.Text = labelText
    cbLabel.TextColor3 = Color3.fromRGB(160, 160, 180)
    cbLabel.TextSize = 10
    cbLabel.Font = Enum.Font.Gotham
    cbLabel.TextXAlignment = Enum.TextXAlignment.Left
    cbLabel.Parent = cbFrame

    cbBtn.MouseButton1Click:Connect(function()
        checkboxStates[stateKey] = not checkboxStates[stateKey]
        cbBtn.BackgroundColor3 = checkboxStates[stateKey] and Color3.fromRGB(88, 101, 242) or Color3.fromRGB(50, 50, 65)
        cbBtn.Text = checkboxStates[stateKey] and "X" or ""
    end)

    return cbBtn
end

createCheckbox(monFrame, "Passes", "gamepasses", 1)
createCheckbox(monFrame, "DevProd", "devproducts", 2)
createCheckbox(monFrame, "Ads", "ads", 3)

-- Calculate button
local calcBtn = Instance.new("TextButton")
calcBtn.Size = UDim2.new(1, 0, 0, 30)
calcBtn.BackgroundColor3 = Color3.fromRGB(50, 180, 80)
calcBtn.Text = "Calculate Revenue"
calcBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
calcBtn.TextSize = 13
calcBtn.Font = Enum.Font.GothamBold
calcBtn.LayoutOrder = 6
calcBtn.Parent = revenuePanel
Instance.new("UICorner", calcBtn).CornerRadius = UDim.new(0, 6)

-- Revenue results display
local revResultFrame = Instance.new("Frame")
revResultFrame.Size = UDim2.new(1, 0, 0, 110)
revResultFrame.BackgroundColor3 = Color3.fromRGB(28, 28, 38)
revResultFrame.LayoutOrder = 7
revResultFrame.Parent = revenuePanel
Instance.new("UICorner", revResultFrame).CornerRadius = UDim.new(0, 6)

local revResultLayout = Instance.new("UIListLayout")
revResultLayout.SortOrder = Enum.SortOrder.LayoutOrder
revResultLayout.Padding = UDim.new(0, 2)
revResultLayout.Parent = revResultFrame

local revResultPad = Instance.new("UIPadding")
revResultPad.PaddingTop = UDim.new(0, 6)
revResultPad.PaddingLeft = UDim.new(0, 8)
revResultPad.Parent = revResultFrame

local revResultTitle = Instance.new("TextLabel")
revResultTitle.Size = UDim2.new(1, 0, 0, 18)
revResultTitle.BackgroundTransparency = 1
revResultTitle.Text = "ESTIMATED MONTHLY REVENUE"
revResultTitle.TextColor3 = Color3.fromRGB(88, 101, 242)
revResultTitle.TextSize = 11
revResultTitle.Font = Enum.Font.GothamBold
revResultTitle.TextXAlignment = Enum.TextXAlignment.Left
revResultTitle.LayoutOrder = 0
revResultTitle.Parent = revResultFrame

local revLowLabel = Instance.new("TextLabel")
revLowLabel.Size = UDim2.new(1, 0, 0, 18)
revLowLabel.BackgroundTransparency = 1
revLowLabel.Text = "Low:  --"
revLowLabel.TextColor3 = Color3.fromRGB(255, 150, 50)
revLowLabel.TextSize = 12
revLowLabel.Font = Enum.Font.GothamMedium
revLowLabel.TextXAlignment = Enum.TextXAlignment.Left
revLowLabel.LayoutOrder = 1
revLowLabel.Parent = revResultFrame

local revMidLabel = Instance.new("TextLabel")
revMidLabel.Size = UDim2.new(1, 0, 0, 18)
revMidLabel.BackgroundTransparency = 1
revMidLabel.Text = "Mid:  --"
revMidLabel.TextColor3 = Color3.fromRGB(80, 220, 80)
revMidLabel.TextSize = 12
revMidLabel.Font = Enum.Font.GothamBold
revMidLabel.TextXAlignment = Enum.TextXAlignment.Left
revMidLabel.LayoutOrder = 2
revMidLabel.Parent = revResultFrame

local revHighLabel = Instance.new("TextLabel")
revHighLabel.Size = UDim2.new(1, 0, 0, 18)
revHighLabel.BackgroundTransparency = 1
revHighLabel.Text = "High: --"
revHighLabel.TextColor3 = Color3.fromRGB(100, 160, 255)
revHighLabel.TextSize = 12
revHighLabel.Font = Enum.Font.GothamMedium
revHighLabel.TextXAlignment = Enum.TextXAlignment.Left
revHighLabel.LayoutOrder = 3
revHighLabel.Parent = revResultFrame

local revNoteLabel = Instance.new("TextLabel")
revNoteLabel.Size = UDim2.new(1, 0, 0, 26)
revNoteLabel.BackgroundTransparency = 1
revNoteLabel.Text = "After 30% Roblox fee. DevEx rate: $0.0038/R$"
revNoteLabel.TextColor3 = Color3.fromRGB(90, 90, 110)
revNoteLabel.TextSize = 9
revNoteLabel.Font = Enum.Font.Gotham
revNoteLabel.TextXAlignment = Enum.TextXAlignment.Left
revNoteLabel.TextWrapped = true
revNoteLabel.LayoutOrder = 4
revNoteLabel.Parent = revResultFrame

--------------------------------------------------------------------
-- META: GAME HEALTH SCANNER PANEL
--------------------------------------------------------------------
local scanPanel = Instance.new("Frame")
scanPanel.Size = UDim2.new(1, 0, 1, -44)
scanPanel.BackgroundTransparency = 1
scanPanel.LayoutOrder = 1
scanPanel.Visible = false
scanPanel.Parent = metaPanel

local scanPanelLayout = Instance.new("UIListLayout")
scanPanelLayout.SortOrder = Enum.SortOrder.LayoutOrder
scanPanelLayout.Padding = UDim.new(0, 6)
scanPanelLayout.Parent = scanPanel

local scanBtn = Instance.new("TextButton")
scanBtn.Size = UDim2.new(1, 0, 0, 36)
scanBtn.BackgroundColor3 = Color3.fromRGB(200, 80, 60)
scanBtn.Text = "Scan Game Health"
scanBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
scanBtn.TextSize = 14
scanBtn.Font = Enum.Font.GothamBold
scanBtn.LayoutOrder = 0
scanBtn.Parent = scanPanel
Instance.new("UICorner", scanBtn).CornerRadius = UDim.new(0, 6)

-- Score display
local scanScoreFrame = Instance.new("Frame")
scanScoreFrame.Size = UDim2.new(1, 0, 0, 50)
scanScoreFrame.BackgroundColor3 = Color3.fromRGB(22, 22, 30)
scanScoreFrame.LayoutOrder = 1
scanScoreFrame.Parent = scanPanel
Instance.new("UICorner", scanScoreFrame).CornerRadius = UDim.new(0, 6)

local scanScoreLabel = Instance.new("TextLabel")
scanScoreLabel.Size = UDim2.new(1, 0, 1, 0)
scanScoreLabel.BackgroundTransparency = 1
scanScoreLabel.Text = "Score: --"
scanScoreLabel.TextColor3 = Color3.fromRGB(120, 120, 150)
scanScoreLabel.TextSize = 22
scanScoreLabel.Font = Enum.Font.GothamBlack
scanScoreLabel.LayoutOrder = 0
scanScoreLabel.Parent = scanScoreFrame

-- Issues list
local scanIssuesLabel = Instance.new("TextLabel")
scanIssuesLabel.Size = UDim2.new(1, 0, 0, 16)
scanIssuesLabel.BackgroundTransparency = 1
scanIssuesLabel.Text = "Issues & Suggestions"
scanIssuesLabel.TextColor3 = Color3.fromRGB(180, 180, 200)
scanIssuesLabel.TextSize = 12
scanIssuesLabel.Font = Enum.Font.GothamBold
scanIssuesLabel.TextXAlignment = Enum.TextXAlignment.Left
scanIssuesLabel.LayoutOrder = 2
scanIssuesLabel.Parent = scanPanel

local scanResultsScroll = Instance.new("ScrollingFrame")
scanResultsScroll.Size = UDim2.new(1, 0, 1, -120)
scanResultsScroll.BackgroundColor3 = Color3.fromRGB(22, 22, 30)
scanResultsScroll.BorderSizePixel = 0
scanResultsScroll.ScrollBarThickness = 4
scanResultsScroll.LayoutOrder = 3
scanResultsScroll.Parent = scanPanel
Instance.new("UICorner", scanResultsScroll).CornerRadius = UDim.new(0, 6)

local scanResultsLayout = Instance.new("UIListLayout")
scanResultsLayout.SortOrder = Enum.SortOrder.LayoutOrder
scanResultsLayout.Padding = UDim.new(0, 2)
scanResultsLayout.Parent = scanResultsScroll

local scanResultsPad = Instance.new("UIPadding")
scanResultsPad.PaddingTop = UDim.new(0, 4)
scanResultsPad.PaddingLeft = UDim.new(0, 6)
scanResultsPad.PaddingRight = UDim.new(0, 6)
scanResultsPad.Parent = scanResultsScroll

--------------------------------------------------------------------
-- MODE SWITCHING (with meta panel visibility)
--------------------------------------------------------------------

-- References for elements that hide/show based on mode
-- promptLabel, promptInput, generateBtn, undoBtn created below share LayoutOrders 8-11

local function setMetaSubTab(tab)
    currentMetaSubTab = tab
    genresPanel.Visible = tab == "genres"
    refreshMetaBtn.Visible = tab == "genres"
    revenuePanel.Visible = tab == "revenue"
    scanPanel.Visible = tab == "scan"

    genresSubBtn.BackgroundColor3 = tab == "genres" and Color3.fromRGB(60, 70, 140) or Color3.fromRGB(40, 40, 55)
    genresSubBtn.TextColor3 = tab == "genres" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)
    revenueSubBtn.BackgroundColor3 = tab == "revenue" and Color3.fromRGB(60, 70, 140) or Color3.fromRGB(40, 40, 55)
    revenueSubBtn.TextColor3 = tab == "revenue" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)
    scanSubBtn.BackgroundColor3 = tab == "scan" and Color3.fromRGB(60, 70, 140) or Color3.fromRGB(40, 40, 55)
    scanSubBtn.TextColor3 = tab == "scan" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)
end

genresSubBtn.MouseButton1Click:Connect(function() setMetaSubTab("genres") end)
revenueSubBtn.MouseButton1Click:Connect(function() setMetaSubTab("revenue") end)
scanSubBtn.MouseButton1Click:Connect(function() setMetaSubTab("scan") end)

-- Forward-declared references for prompt area elements (created just below)
local promptLabel
local promptInputContainer
local generateBtnRef
local undoBtnRef
local statusLabelRef
local changesFrameRef

local function setMode(mode)
    currentMode = mode
    codeBtn.BackgroundColor3 = mode == "code" and Color3.fromRGB(88, 101, 242) or Color3.fromRGB(40, 40, 55)
    codeBtn.TextColor3 = mode == "code" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)
    questionBtn.BackgroundColor3 = mode == "question" and Color3.fromRGB(88, 101, 242) or Color3.fromRGB(40, 40, 55)
    questionBtn.TextColor3 = mode == "question" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)
    scaffoldBtn.BackgroundColor3 = mode == "scaffold" and Color3.fromRGB(88, 101, 242) or Color3.fromRGB(40, 40, 55)
    scaffoldBtn.TextColor3 = mode == "scaffold" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)
    metaBtn.BackgroundColor3 = mode == "meta" and Color3.fromRGB(88, 101, 242) or Color3.fromRGB(40, 40, 55)
    metaBtn.TextColor3 = mode == "meta" and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(180, 180, 200)

    -- Show/hide meta panel vs standard code/ask/scaffold panel elements
    local isMetaMode = (mode == "meta")
    metaPanel.Visible = isMetaMode

    -- The standard elements (promptLabel etc) are toggled via LayoutOrder trick:
    -- We move them off-screen by making them invisible when in meta mode
    if promptLabel then promptLabel.Visible = not isMetaMode end
    if promptInputContainer then promptInputContainer.Visible = not isMetaMode end
    if generateBtnRef then generateBtnRef.Visible = not isMetaMode end
    if undoBtnRef then undoBtnRef.Visible = not isMetaMode end
    if statusLabelRef then statusLabelRef.Visible = not isMetaMode end
    if changesFrameRef then changesFrameRef.Visible = not isMetaMode end
end

codeBtn.MouseButton1Click:Connect(function() setMode("code") end)
questionBtn.MouseButton1Click:Connect(function() setMode("question") end)
scaffoldBtn.MouseButton1Click:Connect(function() setMode("scaffold") end)
metaBtn.MouseButton1Click:Connect(function() setMode("meta") end)

-- Prompt input
promptLabel = createLabel(mainFrame, "What do you want to build?", 8)
local promptInput, promptInputContainerRef = createTextInput(mainFrame, "e.g. 'Add a shop with 3 items and a currency system'", 9, 120)
promptInputContainer = promptInputContainerRef

-- Action buttons
local generateBtn = createButton(mainFrame, "Generate", 10, Color3.fromRGB(88, 101, 242))
generateBtnRef = generateBtn
local undoBtn = createButton(mainFrame, "Undo Last Change", 11, Color3.fromRGB(60, 60, 80))
undoBtnRef = undoBtn

-- Status display
local statusLabel = Instance.new("TextLabel")
statusLabel.Size = UDim2.new(1, 0, 0, 60)
statusLabel.BackgroundColor3 = Color3.fromRGB(25, 25, 35)
statusLabel.Text = "Ready"
statusLabel.TextColor3 = Color3.fromRGB(120, 120, 150)
statusLabel.TextSize = 11
statusLabel.Font = Enum.Font.Gotham
statusLabel.TextWrapped = true
statusLabel.TextXAlignment = Enum.TextXAlignment.Left
statusLabel.TextYAlignment = Enum.TextYAlignment.Top
statusLabel.LayoutOrder = 12
statusLabel.Parent = mainFrame
statusLabelRef = statusLabel
Instance.new("UICorner", statusLabel).CornerRadius = UDim.new(0, 6)
local statusPad = Instance.new("UIPadding")
statusPad.PaddingTop = UDim.new(0, 6)
statusPad.PaddingLeft = UDim.new(0, 8)
statusPad.Parent = statusLabel

-- Changes history frame
local changesFrame = Instance.new("ScrollingFrame")
changesFrame.Size = UDim2.new(1, 0, 1, -520)
changesFrame.BackgroundColor3 = Color3.fromRGB(22, 22, 30)
changesFrame.BorderSizePixel = 0
changesFrame.ScrollBarThickness = 4
changesFrame.LayoutOrder = 13
changesFrame.Parent = mainFrame
changesFrameRef = changesFrame
Instance.new("UICorner", changesFrame).CornerRadius = UDim.new(0, 6)

local changesLayout = Instance.new("UIListLayout")
changesLayout.SortOrder = Enum.SortOrder.LayoutOrder
changesLayout.Padding = UDim.new(0, 2)
changesLayout.Parent = changesFrame

--------------------------------------------------------------------
-- GAME CONTEXT SERIALIZATION
--------------------------------------------------------------------
local function serializeScripts(root)
    local scripts = {}
    if not root then return scripts end

    local function recurse(obj, path)
        if obj:IsA("LuaSourceContainer") then
            table.insert(scripts, {
                name = obj.Name,
                className = obj.ClassName,
                path = path .. "/" .. obj.Name,
                source = obj.Source,
                parent = obj.Parent and obj.Parent:GetFullName() or "unknown",
            })
        end
        for _, child in ipairs(obj:GetChildren()) do
            recurse(child, path .. "/" .. obj.Name)
        end
    end

    for _, child in ipairs(root:GetChildren()) do
        recurse(child, root.Name)
    end

    return scripts
end

local function getGameContext()
    local allScripts = {}
    for _, service in ipairs(servicesToCheck) do
        if service then
            local scripts = serializeScripts(service)
            for _, s in ipairs(scripts) do
                table.insert(allScripts, s)
            end
        end
    end
    return allScripts
end

local function formatContextForAPI(scripts)
    local parts = {}
    for _, s in ipairs(scripts) do
        table.insert(parts, string.format(
            "--- Script: %s (%s) at %s ---\n%s\n",
            s.name, s.className, s.path, s.source
        ))
    end
    return table.concat(parts, "\n")
end

--------------------------------------------------------------------
-- API COMMUNICATION
--------------------------------------------------------------------
local function makeRequest(url, method, headers, body)
    local success, response = pcall(function()
        return HttpService:RequestAsync({
            Url = url,
            Method = method,
            Headers = headers,
            Body = body and HttpService:JSONEncode(body) or nil,
        })
    end)

    if success and response.Success then
        return true, HttpService:JSONDecode(response.Body)
    elseif success then
        return false, "HTTP " .. tostring(response.StatusCode) .. ": " .. tostring(response.Body)
    else
        return false, tostring(response)
    end
end

-- Direct API calls (user's own key)
local function callClaude(systemPrompt, userMessage)
    return makeRequest(
        "https://api.anthropic.com/v1/messages",
        "POST",
        {
            ["x-api-key"] = apiKey,
            ["anthropic-version"] = "2023-06-01",
            ["content-type"] = "application/json",
        },
        {
            model = "claude-sonnet-4-5-20250929",
            max_tokens = 8192,
            system = systemPrompt,
            messages = {{ role = "user", content = userMessage }},
        }
    )
end

local function callOpenAI(systemPrompt, userMessage)
    return makeRequest(
        "https://api.openai.com/v1/chat/completions",
        "POST",
        {
            ["Authorization"] = "Bearer " .. apiKey,
            ["Content-Type"] = "application/json",
        },
        {
            model = "gpt-4o",
            messages = {
                { role = "system", content = systemPrompt },
                { role = "user", content = userMessage },
            },
            max_tokens = 8192,
        }
    )
end

local function callGemini(systemPrompt, userMessage)
    return makeRequest(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=" .. apiKey,
        "POST",
        { ["Content-Type"] = "application/json" },
        {
            system_instruction = { parts = {{ text = systemPrompt }} },
            contents = {{ parts = {{ text = userMessage }} }},
            generationConfig = { maxOutputTokens = 8192 },
        }
    )
end

-- RobloxMaxx Pro API (BYOK with premium features)
-- Calls our Next.js backend which injects premium context (meta advisor,
-- genre intelligence) then forwards to Anthropic using the USER's API key.
-- Pro subscription required for premium features, but user always pays AI costs.
local function callRobloxMaxxAPI(endpoint, payload)
    payload.token = userToken -- Pro auth token (optional, for premium features)
    payload.apiKey = apiKey   -- User's own AI API key (BYOK, required)
    payload.pluginVersion = PLUGIN_VERSION
    return makeRequest(
        API_BASE_URL .. endpoint,
        "POST",
        { ["Content-Type"] = "application/json" },
        payload
    )
end

local function extractResponse(provider, data)
    if provider == "claude" then
        return data.content and data.content[1] and data.content[1].text
    elseif provider == "openai" then
        return data.choices and data.choices[1] and data.choices[1].message and data.choices[1].message.content
    elseif provider == "gemini" then
        return data.candidates and data.candidates[1] and data.candidates[1].content
            and data.candidates[1].content.parts and data.candidates[1].content.parts[1]
            and data.candidates[1].content.parts[1].text
    elseif provider == "robloxmaxx pro" then
        return data.response
    end
    return nil
end

--------------------------------------------------------------------
-- SYSTEM PROMPTS
--------------------------------------------------------------------
local BASE_SYSTEM_PROMPT = [[
You are RobloxMaxx, an expert Roblox game developer AI. You write production-ready Luau code for Roblox Studio.

RULES:
1. Write clean, optimized Luau code (NOT Lua 5.1 - use Luau features like type annotations, string interpolation)
2. Follow Roblox best practices: use RemoteEvents for client-server, ModuleScripts for shared logic
3. Handle edge cases: nil checks, pcall for risky operations, input validation
4. Use proper services: DataStoreService for persistence, MarketplaceService for purchases
5. Comment code clearly for non-programmers to understand
6. NEVER use deprecated APIs

RESPONSE FORMAT (Code/Scaffold mode):
Return a JSON array of actions. Each action is one of:

{
  "action": "ModifyExisting",
  "scriptName": "ScriptName",
  "serviceName": "ServerScriptService",
  "previousCode": "-- exact lines to find and replace",
  "newCode": "-- replacement code",
  "explanation": "What this change does"
}

{
  "action": "AddToScript",
  "scriptName": "ScriptName",
  "serviceName": "ServerScriptService",
  "newCode": "-- code to append",
  "explanation": "What this adds"
}

{
  "action": "CreateScript",
  "scriptName": "NewScriptName",
  "scriptType": "Script|LocalScript|ModuleScript",
  "serviceName": "ServerScriptService",
  "newCode": "-- full script source",
  "explanation": "What this script does"
}

{
  "action": "CreateFolder",
  "folderName": "FolderName",
  "serviceName": "ReplicatedStorage",
  "explanation": "Why this folder exists"
}

IMPORTANT: Return ONLY the JSON array, no markdown, no extra text. Start with [ and end with ].
]]

local GENRE_PROMPTS = {
    tycoon = [[
GENRE: TYCOON GAME
You specialize in Roblox tycoon mechanics:
- Dropper → Collector → Upgrader → Rebirth loops
- Tycoon plot claiming and ownership
- Currency systems with DataStore persistence
- Upgrade paths with exponential cost scaling
- Rebirth mechanics that reset progress for multipliers
- Button-based purchases on tycoon pads
- Conveyor belt systems
- Prestige systems
Common services: ServerScriptService (game logic), ReplicatedStorage (shared modules), StarterGui (shop UI)
]],
    obby = [[
GENRE: OBBY (OBSTACLE COURSE)
You specialize in Roblox obby mechanics:
- Checkpoint/stage system with spawn management
- Kill bricks, moving platforms, rotating obstacles
- Stage completion tracking with DataStore
- Difficulty progression curves
- Skip stage gamepasses (MarketplaceService)
- Leaderboard for fastest completion
- Visual effects for stage transitions
Common services: Workspace (obstacles), ServerScriptService (progression), StarterGui (stage display)
]],
    simulator = [[
GENRE: SIMULATOR
You specialize in Roblox simulator mechanics:
- Click/tap to earn base resource
- Tool/pet upgrades that multiply earnings
- Rebirth systems with permanent multipliers
- Pet/egg hatching with rarity tiers (Common 70%, Rare 20%, Legendary 8%, Mythic 2%)
- Trading systems between players
- Zones unlocked by resource thresholds
- Auto-collectors and AFK mechanics
- Event/limited-time content
Common services: ServerScriptService (calculations), ReplicatedStorage (pet data), ServerStorage (templates)
]],
    rpg = [[
GENRE: RPG
You specialize in Roblox RPG mechanics:
- Quest system (accept, track objectives, complete, reward)
- Inventory system with items, equipment, consumables
- Combat system (melee, ranged, abilities with cooldowns)
- NPC dialogue system
- Level/XP progression
- Stat system (health, damage, defense, speed)
- Dungeon/instance generation
- Party system for multiplayer
Common services: ServerScriptService (combat, quests), ReplicatedStorage (item data), StarterGui (HUD, inventory)
]],
    horror = [[
GENRE: HORROR
You specialize in Roblox horror game mechanics:
- Atmosphere: fog, lighting manipulation, ambient sounds
- Chase AI (pathfinding with adjustable difficulty)
- Jump scare system with cooldowns
- Flashlight/battery mechanics
- Key/puzzle item collection
- Door/lock systems
- Stamina/sprint system
- Multiple endings based on choices
Common services: Workspace (level design), ServerScriptService (AI, events), StarterGui (inventory, stamina)
]],
    general = "",
}

local SCAFFOLD_PROMPT = [[
SCAFFOLD MODE: Generate a COMPLETE game structure from scratch.
Create ALL necessary scripts, folders, and systems for a fully functional game.
Include:
1. Server-side game logic
2. Client-side UI
3. Data persistence (DataStoreService)
4. Remote events for client-server communication
5. A ModuleScript for shared configuration
6. Basic monetization hooks (gamepasses, developer products)

Generate 8-20 scripts that form a complete, playable, monetizable game.
]]

local SCAFFOLD_GENRE_PROMPTS = {
    tycoon = [[
SCAFFOLD GENRE: TYCOON
Build a complete tycoon game with:
- TycoonConfig (ModuleScript): dropper definitions, upgrade paths, rebirth costs, gamepass IDs
- TycoonManager (Script): plot claiming, currency tracking, dropper income loop, rebirth logic, data persistence
- TycoonHUD (LocalScript): cash display, shop UI with droppers/upgrades/rebirth, shop toggle button
- RemoteEvents folder in ReplicatedStorage
- At least 4 dropper tiers, 4 upgrades, rebirth system, leaderboard
- MarketplaceService hooks for x2 cash gamepass and cash dev product
]],
    obby = [[
SCAFFOLD GENRE: OBBY
Build a complete obby game with:
- ObbyConfig (ModuleScript): total stages, rewards per stage, completion bonus, skip gamepass ID
- ObbyManager (Script): checkpoint touching, stage progression, spawn management, timer, data persistence
- CheckpointHandler (Script): detect player touching checkpoints, validate stage order
- ObbyHUD (LocalScript): stage counter display, timer, skip stage button, completion screen
- KillBrickHandler (Script): detect kill brick touches, respawn at last checkpoint
- RemoteEvents folder in ReplicatedStorage
- At least 20 stages, kill bricks, moving platforms, leaderboard for fastest time
- MarketplaceService hooks for skip stage gamepass and speed boost dev product
]],
    simulator = [[
SCAFFOLD GENRE: SIMULATOR
Build a complete simulator game with:
- SimConfig (ModuleScript): base click value, tool tiers with costs/multipliers, pet rarities with weights, egg cost, rebirth cost, zones
- SimulatorCore (Script): click handling, tool ownership, currency, rebirth, zone unlocking, data persistence
- PetSystem (Script): egg hatching with weighted rarity, pet equipping (max 3), pet multiplier stacking
- SimHUD (LocalScript): currency display, tool shop, pet inventory, zone requirements, rebirth button
- CodesSystem (Script): redeemable text codes for bonus currency/pets
- RemoteEvents folder in ReplicatedStorage
- 6 tool tiers, 4 pet rarities, 5 zones, rebirth with permanent bonus, leaderboard
- MarketplaceService hooks for auto-collector gamepass and premium egg dev product
]],
    rpg = [[
SCAFFOLD GENRE: RPG
Build a complete RPG game with:
- GameData (ModuleScript): item definitions, quest data, NPC data, stat formulas, loot tables
- CombatSystem (Script): melee/ranged damage calculation, hitbox detection, cooldowns, health regen
- QuestManager (Script): quest accept/track/complete state machine, objective tracking, rewards
- InventoryManager (Script): item pickup, equipment slots, stat bonuses, stacking, data persistence
- RPG_HUD (LocalScript): health bar, XP bar, level display, hotbar, quest tracker, minimap
- InventoryUI (LocalScript): inventory grid, equipment screen, item tooltips, drag and drop
- NPCDialogue (LocalScript): branching dialogue trees, quest accept/turn-in prompts
- RemoteEvents folder in ReplicatedStorage
- At least 3 quests, 10 items, 3 NPCs, level/XP system, leaderboard
- MarketplaceService hooks for XP boost gamepass and revive dev product
]],
    horror = [[
SCAFFOLD GENRE: HORROR
Build a complete horror game with:
- GameConfig (ModuleScript): item definitions, door mappings, monster speed, flashlight battery duration
- MonsterAI (Script): PathfindingService patrol routes, chase state when player spotted, search state, variable speed
- GameManager (Script): key/puzzle item collection, door lock system, progression triggers, multiple endings, data persistence
- FlashlightController (LocalScript): toggle flashlight, battery drain, recharge pickups, SpotLight manipulation
- HorrorHUD (LocalScript): flashlight battery bar, stamina bar, inventory (keys/items), objective text
- AtmosphereSetup (Script): set Lighting.Ambient dark, FogEnd, ambient sound loops, jump scare triggers
- StaminaSystem (Script): sprint/walk stamina drain/recover, movement speed changes
- RemoteEvents folder in ReplicatedStorage
- Multiple rooms with locked doors, at least 3 key items, 2 endings, leaderboard for fastest escape
- MarketplaceService hooks for extra battery gamepass and hint system dev product
]],
    general = "",
}

--------------------------------------------------------------------
-- CODE CHANGE ENGINE
--------------------------------------------------------------------
local function findScript(scriptName, serviceName)
    local service = nil
    if serviceName == "ServerScriptService" then service = ServerScriptService
    elseif serviceName == "Workspace" then service = Workspace
    elseif serviceName == "ReplicatedStorage" then service = ReplicatedStorage
    elseif serviceName == "StarterGui" then service = StarterGui
    elseif serviceName == "ServerStorage" then service = ServerStorage
    elseif serviceName == "StarterPlayerScripts" then
        service = StarterPlayer:FindFirstChild("StarterPlayerScripts")
    elseif serviceName == "StarterCharacterScripts" then
        service = StarterPlayer:FindFirstChild("StarterCharacterScripts")
    end

    if not service then return nil end

    -- Search recursively
    local function search(parent)
        for _, child in ipairs(parent:GetChildren()) do
            if child:IsA("LuaSourceContainer") and child.Name == scriptName then
                return child
            end
            local found = search(child)
            if found then return found end
        end
        return nil
    end

    return search(service)
end

local function getServiceInstance(serviceName)
    if serviceName == "ServerScriptService" then return ServerScriptService
    elseif serviceName == "Workspace" then return Workspace
    elseif serviceName == "ReplicatedStorage" then return ReplicatedStorage
    elseif serviceName == "StarterGui" then return StarterGui
    elseif serviceName == "ServerStorage" then return ServerStorage
    elseif serviceName == "StarterPlayerScripts" then
        return StarterPlayer:FindFirstChild("StarterPlayerScripts")
    elseif serviceName == "StarterCharacterScripts" then
        return StarterPlayer:FindFirstChild("StarterCharacterScripts")
    end
    return ServerScriptService -- fallback
end

local function backupScript(script)
    if not scriptBackups[script] then
        scriptBackups[script] = script.Source
    end
end

local function applyAction(action)
    local result = { success = false, message = "" }

    if action.action == "CreateScript" then
        local parent = getServiceInstance(action.serviceName)
        if not parent then
            result.message = "Service not found: " .. tostring(action.serviceName)
            return result
        end

        local scriptType = action.scriptType or "Script"
        local newScript = Instance.new(scriptType)
        newScript.Name = action.scriptName
        newScript.Source = action.newCode
        newScript.Parent = parent

        table.insert(changeHistory, {
            action = "CreateScript",
            script = newScript,
            explanation = action.explanation or "Created new script",
        })

        -- Open in editor
        pcall(function()
            ScriptEditorService:OpenScriptDocumentAsync(newScript)
        end)

        result.success = true
        result.message = "Created " .. scriptType .. ": " .. action.scriptName

    elseif action.action == "CreateFolder" then
        local parent = getServiceInstance(action.serviceName)
        if parent then
            local folder = Instance.new("Folder")
            folder.Name = action.folderName
            folder.Parent = parent

            table.insert(changeHistory, {
                action = "CreateFolder",
                folder = folder,
                explanation = action.explanation or "Created folder",
            })

            result.success = true
            result.message = "Created folder: " .. action.folderName
        end

    elseif action.action == "ModifyExisting" then
        local script = findScript(action.scriptName, action.serviceName)
        if not script then
            result.message = "Script not found: " .. tostring(action.scriptName)
            return result
        end

        backupScript(script)

        local source = script.Source
        local prevCode = action.previousCode

        local startIdx = source:find(prevCode, 1, true)
        if startIdx then
            local newSource = source:sub(1, startIdx - 1) .. action.newCode .. source:sub(startIdx + #prevCode)
            script.Source = newSource

            table.insert(changeHistory, {
                action = "ModifyExisting",
                script = script,
                previousSource = source,
                explanation = action.explanation or "Modified script",
            })

            pcall(function()
                ScriptEditorService:OpenScriptDocumentAsync(script)
            end)

            result.success = true
            result.message = "Modified: " .. action.scriptName
        else
            -- Fallback: append the new code
            script.Source = source .. "\n\n" .. action.newCode

            table.insert(changeHistory, {
                action = "ModifyExisting",
                script = script,
                previousSource = source,
                explanation = action.explanation or "Appended to script (exact match not found)",
            })

            result.success = true
            result.message = "Appended to: " .. action.scriptName .. " (exact match not found, appended)"
        end

    elseif action.action == "AddToScript" then
        local script = findScript(action.scriptName, action.serviceName)
        if not script then
            result.message = "Script not found: " .. tostring(action.scriptName)
            return result
        end

        backupScript(script)
        local previousSource = script.Source
        script.Source = previousSource .. "\n\n" .. action.newCode

        table.insert(changeHistory, {
            action = "AddToScript",
            script = script,
            previousSource = previousSource,
            explanation = action.explanation or "Added to script",
        })

        pcall(function()
            ScriptEditorService:OpenScriptDocumentAsync(script)
        end)

        result.success = true
        result.message = "Added to: " .. action.scriptName
    end

    return result
end

local function undoLastChange()
    if #changeHistory == 0 then
        return false, "No changes to undo"
    end

    local last = changeHistory[#changeHistory]

    if last.action == "CreateScript" and last.script then
        pcall(function()
            local doc = ScriptEditorService:FindScriptDocument(last.script)
            if doc then doc:CloseAsync() end
        end)
        last.script:Destroy()
    elseif last.action == "CreateFolder" and last.folder then
        last.folder:Destroy()
    elseif (last.action == "ModifyExisting" or last.action == "AddToScript") and last.script and last.previousSource then
        last.script.Source = last.previousSource
    end

    table.remove(changeHistory, #changeHistory)
    return true, "Undid: " .. (last.explanation or "last change")
end

--------------------------------------------------------------------
-- MAIN GENERATE FUNCTION
--------------------------------------------------------------------
local function generate()
    if isProcessing then return end
    isProcessing = true

    local prompt = promptInput.Text
    if prompt == "" then
        statusLabel.Text = "Enter a prompt first"
        isProcessing = false
        return
    end

    local provider = providerDropdown.getValue()
    local genre = genreDropdown.getValue()
    apiKey = authInput.Text

    if apiKey == "" then
        statusLabel.Text = "Enter your AI API key (Claude/OpenAI/Gemini)"
        isProcessing = false
        return
    end

    statusLabel.Text = "Reading game context..."
    statusLabel.TextColor3 = Color3.fromRGB(255, 200, 50)

    -- Build system prompt
    local systemPrompt = BASE_SYSTEM_PROMPT
    if GENRE_PROMPTS[genre] then
        systemPrompt = systemPrompt .. "\n" .. GENRE_PROMPTS[genre]
    end
    if currentMode == "scaffold" then
        systemPrompt = systemPrompt .. "\n" .. SCAFFOLD_PROMPT
        if SCAFFOLD_GENRE_PROMPTS[genre] and SCAFFOLD_GENRE_PROMPTS[genre] ~= "" then
            systemPrompt = systemPrompt .. "\n" .. SCAFFOLD_GENRE_PROMPTS[genre]
        end
    end
    if currentMode == "question" then
        systemPrompt = systemPrompt .. "\nRESPONSE FORMAT: Answer the question in plain text. Be specific and reference actual scripts/code in the game."
    end

    -- Get game context
    local gameScripts = getGameContext()
    local contextStr = formatContextForAPI(gameScripts)

    local userMessage = ""
    if #gameScripts > 0 then
        userMessage = "CURRENT GAME CODE:\n" .. contextStr .. "\n\nUSER REQUEST: " .. prompt
    else
        userMessage = "USER REQUEST (empty game, create from scratch): " .. prompt
    end

    statusLabel.Text = "Generating with " .. provider .. "..."

    -- Make API call
    coroutine.wrap(function()
        local success, data

        if provider == "robloxmaxx pro" then
            success, data = callRobloxMaxxAPI("/generate", {
                prompt = prompt,
                mode = currentMode,
                genre = genre,
                context = contextStr,
                systemPrompt = systemPrompt,
            })
        elseif provider == "claude" then
            success, data = callClaude(systemPrompt, userMessage)
        elseif provider == "openai" then
            success, data = callOpenAI(systemPrompt, userMessage)
        elseif provider == "gemini" then
            success, data = callGemini(systemPrompt, userMessage)
        end

        if not success then
            statusLabel.Text = "Error: " .. tostring(data)
            statusLabel.TextColor3 = Color3.fromRGB(255, 80, 80)
            isProcessing = false
            return
        end

        local responseText = extractResponse(provider, data)
        if not responseText then
            statusLabel.Text = "Error: Could not parse response"
            statusLabel.TextColor3 = Color3.fromRGB(255, 80, 80)
            isProcessing = false
            return
        end

        -- Question mode: just display the answer
        if currentMode == "question" then
            statusLabel.Text = responseText
            statusLabel.TextColor3 = Color3.fromRGB(120, 220, 120)
            isProcessing = false
            return
        end

        -- Code/Scaffold mode: parse and apply changes
        statusLabel.Text = "Applying changes..."

        -- Extract JSON from response (handle markdown code blocks)
        local jsonStr = responseText
        local jsonStart = jsonStr:find("%[")
        local jsonEnd = jsonStr:reverse():find("%]")
        if jsonStart and jsonEnd then
            jsonEnd = #jsonStr - jsonEnd + 1
            jsonStr = jsonStr:sub(jsonStart, jsonEnd)
        end

        local parseSuccess, actions = pcall(function()
            return HttpService:JSONDecode(jsonStr)
        end)

        if not parseSuccess or type(actions) ~= "table" then
            statusLabel.Text = "Error: Could not parse code changes. Raw response saved."
            statusLabel.TextColor3 = Color3.fromRGB(255, 80, 80)

            -- Save raw response as a script for debugging
            local debugScript = Instance.new("ModuleScript")
            debugScript.Name = "RobloxMaxx_RawResponse"
            debugScript.Source = "--[[\nRaw AI response (parse failed):\n" .. tostring(responseText) .. "\n]]"
            debugScript.Parent = ServerScriptService

            isProcessing = false
            return
        end

        -- Apply each action
        local results = {}
        local successCount = 0
        local failCount = 0

        for i, action in ipairs(actions) do
            statusLabel.Text = string.format("Applying change %d/%d...", i, #actions)
            local result = applyAction(action)
            table.insert(results, result)
            if result.success then
                successCount += 1
            else
                failCount += 1
            end
        end

        -- Update changes display
        for _, child in ipairs(changesFrame:GetChildren()) do
            if child:IsA("TextLabel") then child:Destroy() end
        end

        for i, entry in ipairs(changeHistory) do
            local changeLabel = Instance.new("TextLabel")
            changeLabel.Size = UDim2.new(1, 0, 0, 24)
            changeLabel.BackgroundTransparency = 1
            changeLabel.Text = string.format("  %d. %s", i, entry.explanation or "Change")
            changeLabel.TextColor3 = Color3.fromRGB(150, 150, 170)
            changeLabel.TextSize = 11
            changeLabel.Font = Enum.Font.Gotham
            changeLabel.TextXAlignment = Enum.TextXAlignment.Left
            changeLabel.TextTruncate = Enum.TextTruncate.AtEnd
            changeLabel.LayoutOrder = i
            changeLabel.Parent = changesFrame
        end
        changesFrame.CanvasSize = UDim2.new(0, 0, 0, #changeHistory * 26)

        -- Final status
        statusLabel.Text = string.format(
            "Done! %d applied, %d failed. %d total changes.",
            successCount, failCount, #changeHistory
        )
        statusLabel.TextColor3 = failCount > 0
            and Color3.fromRGB(255, 200, 50)
            or Color3.fromRGB(120, 220, 120)

        -- Add to conversation context for multi-turn
        table.insert(conversationContext, {
            role = "user",
            content = prompt,
        })
        table.insert(conversationContext, {
            role = "assistant",
            content = "Applied " .. successCount .. " changes",
        })

        isProcessing = false
    end)()
end

--------------------------------------------------------------------
-- META ADVISOR: Fetch Genre Health
--------------------------------------------------------------------
local function fetchGenreHealth()
    genresLoadingLabel.Text = "Loading genre data..."
    genresLoadingLabel.TextColor3 = Color3.fromRGB(255, 200, 50)

    coroutine.wrap(function()
        local success, data = makeRequest(
            API_BASE_URL .. "/meta",
            "GET",
            { ["Content-Type"] = "application/json" },
            nil
        )

        -- Clear existing genre rows (except loading label)
        for _, child in ipairs(genresPanel:GetChildren()) do
            if child:IsA("Frame") then child:Destroy() end
        end

        if not success then
            genresLoadingLabel.Text = "Failed to load: " .. tostring(data)
            genresLoadingLabel.TextColor3 = Color3.fromRGB(255, 80, 80)
            return
        end

        local genres = data.genres
        if not genres or #genres == 0 then
            genresLoadingLabel.Text = "No genre data available"
            genresLoadingLabel.TextColor3 = Color3.fromRGB(120, 120, 150)
            return
        end

        genresLoadingLabel.Text = "Genre Health (updated from API)"
        genresLoadingLabel.TextColor3 = Color3.fromRGB(88, 101, 242)

        for i, genre in ipairs(genres) do
            local row = Instance.new("Frame")
            row.Size = UDim2.new(1, 0, 0, 44)
            row.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
            row.LayoutOrder = i
            row.Parent = genresPanel
            Instance.new("UICorner", row).CornerRadius = UDim.new(0, 4)

            local rowPad = Instance.new("UIPadding")
            rowPad.PaddingLeft = UDim.new(0, 8)
            rowPad.PaddingRight = UDim.new(0, 8)
            rowPad.Parent = row

            -- Genre name
            local nameLabel = Instance.new("TextLabel")
            nameLabel.Size = UDim2.new(0.45, 0, 0, 20)
            nameLabel.Position = UDim2.new(0, 0, 0, 3)
            nameLabel.BackgroundTransparency = 1
            nameLabel.Text = genre.name or "Unknown"
            nameLabel.TextColor3 = Color3.fromRGB(220, 220, 240)
            nameLabel.TextSize = 12
            nameLabel.Font = Enum.Font.GothamBold
            nameLabel.TextXAlignment = Enum.TextXAlignment.Left
            nameLabel.Parent = row

            -- Health status badge
            local status = (genre.health or "COLD"):upper()
            local statusColor = HEALTH_COLORS[status] or HEALTH_COLORS.COLD

            local statusBadge = Instance.new("TextLabel")
            statusBadge.Size = UDim2.new(0, 50, 0, 18)
            statusBadge.Position = UDim2.new(1, -55, 0, 4)
            statusBadge.BackgroundColor3 = statusColor
            statusBadge.Text = status
            statusBadge.TextColor3 = Color3.fromRGB(255, 255, 255)
            statusBadge.TextSize = 10
            statusBadge.Font = Enum.Font.GothamBold
            statusBadge.Parent = row
            Instance.new("UICorner", statusBadge).CornerRadius = UDim.new(0, 3)

            -- Recommendation
            local recLabel = Instance.new("TextLabel")
            recLabel.Size = UDim2.new(1, 0, 0, 16)
            recLabel.Position = UDim2.new(0, 0, 0, 24)
            recLabel.BackgroundTransparency = 1
            recLabel.Text = genre.recommendation or ""
            recLabel.TextColor3 = Color3.fromRGB(140, 140, 160)
            recLabel.TextSize = 10
            recLabel.Font = Enum.Font.Gotham
            recLabel.TextXAlignment = Enum.TextXAlignment.Left
            recLabel.TextTruncate = Enum.TextTruncate.AtEnd
            recLabel.Parent = row
        end

        genresPanel.CanvasSize = UDim2.new(0, 0, 0, 30 + #genres * 48)
        metaData = data
    end)()
end

refreshMetaBtn.MouseButton1Click:Connect(fetchGenreHealth)

--------------------------------------------------------------------
-- REVENUE ESTIMATOR: Calculate
--------------------------------------------------------------------
calcBtn.MouseButton1Click:Connect(function()
    local dauText = dauInput.Text:gsub("[^%d]", "")
    local dau = tonumber(dauText)
    if not dau or dau <= 0 then
        revLowLabel.Text = "Low:  Enter a valid DAU number"
        revLowLabel.TextColor3 = Color3.fromRGB(255, 80, 80)
        revMidLabel.Text = "Mid:  --"
        revHighLabel.Text = "High: --"
        return
    end

    local genre = revGenreDropdown.getValue()
    local result = estimateRevenue(
        dau,
        genre,
        checkboxStates.gamepasses,
        checkboxStates.devproducts,
        checkboxStates.ads
    )

    revLowLabel.Text = string.format("Low:  R$%s (%s)", tostring(result.lowRobux), result.lowUSD)
    revLowLabel.TextColor3 = Color3.fromRGB(255, 150, 50)
    revMidLabel.Text = string.format("Mid:  R$%s (%s)", tostring(result.midRobux), result.midUSD)
    revMidLabel.TextColor3 = Color3.fromRGB(80, 220, 80)
    revHighLabel.Text = string.format("High: R$%s (%s)", tostring(result.highRobux), result.highUSD)
    revHighLabel.TextColor3 = Color3.fromRGB(100, 160, 255)
end)

--------------------------------------------------------------------
-- GAME HEALTH SCANNER: Scan & Display
--------------------------------------------------------------------
local function runGameScan()
    if isProcessing then return end
    isProcessing = true

    scanScoreLabel.Text = "Scanning..."
    scanScoreLabel.TextColor3 = Color3.fromRGB(255, 200, 50)

    -- Clear previous results
    for _, child in ipairs(scanResultsScroll:GetChildren()) do
        if child:IsA("TextLabel") or child:IsA("Frame") then child:Destroy() end
    end

    coroutine.wrap(function()
        -- Serialize all game scripts
        local gameScripts = getGameContext()

        if #gameScripts == 0 then
            scanScoreLabel.Text = "Score: N/A"
            scanScoreLabel.TextColor3 = Color3.fromRGB(120, 120, 150)

            local noScriptsLabel = Instance.new("TextLabel")
            noScriptsLabel.Size = UDim2.new(1, 0, 0, 30)
            noScriptsLabel.BackgroundTransparency = 1
            noScriptsLabel.Text = "No scripts found in game. Add scripts first."
            noScriptsLabel.TextColor3 = Color3.fromRGB(255, 150, 50)
            noScriptsLabel.TextSize = 11
            noScriptsLabel.Font = Enum.Font.Gotham
            noScriptsLabel.TextWrapped = true
            noScriptsLabel.LayoutOrder = 0
            noScriptsLabel.Parent = scanResultsScroll
            isProcessing = false
            return
        end

        local contextStr = formatContextForAPI(gameScripts)
        local genre = genreDropdown.getValue()

        -- Send to scan API
        local provider = providerDropdown.getValue()
        local success, data

        if provider == "robloxmaxx pro" then
            apiKey = authInput.Text
            userToken = authInput.Text -- Pro users may have a separate token
            success, data = callRobloxMaxxAPI("/scan-game", {
                context = contextStr,
                genre = genre,
                scriptCount = #gameScripts,
            })
        else
            -- Direct BYOK: use user's API key for scan
            apiKey = authInput.Text
            if apiKey == "" then
                scanScoreLabel.Text = "Enter your AI API key first"
                scanScoreLabel.TextColor3 = Color3.fromRGB(255, 80, 80)
                isProcessing = false
                return
            end

            local scanSystemPrompt = [[You are a Roblox game code auditor. Analyze the provided game scripts and return a JSON object with:
{
  "score": 0-100,
  "issues": [
    {"severity": "critical|warning|info", "title": "Issue title", "description": "Details", "fix": "How to fix"}
  ],
  "summary": "One-line summary of game health"
}

Score rubric:
- Data persistence (DataStoreService with pcall): +20 points
- Input validation on RemoteEvents: +15 points
- No deprecated APIs (wait, spawn vs task.wait, task.spawn): +10 points
- Error handling (pcall around risky operations): +10 points
- Code organization (ModuleScripts, folders): +10 points
- Client-server separation: +10 points
- Monetization hooks (MarketplaceService): +5 points
- Memory leak prevention (disconnect events, cleanup): +10 points
- Security (no trusting client data): +10 points

Return ONLY the JSON, no markdown, no extra text.]]

            local userMsg = "GAME SCRIPTS TO AUDIT:\n" .. contextStr

            if provider == "claude" then
                success, data = callClaude(scanSystemPrompt, userMsg)
            elseif provider == "openai" then
                success, data = callOpenAI(scanSystemPrompt, userMsg)
            elseif provider == "gemini" then
                success, data = callGemini(scanSystemPrompt, userMsg)
            end

            if success then
                local responseText = extractResponse(provider, data)
                if responseText then
                    -- Parse JSON from response
                    local jsonStr = responseText
                    local jsonStart = jsonStr:find("{")
                    local jsonEnd = jsonStr:reverse():find("}")
                    if jsonStart and jsonEnd then
                        jsonEnd = #jsonStr - jsonEnd + 1
                        jsonStr = jsonStr:sub(jsonStart, jsonEnd)
                    end

                    local parseOk, parsed = pcall(function()
                        return HttpService:JSONDecode(jsonStr)
                    end)

                    if parseOk and parsed then
                        data = parsed
                    else
                        data = { score = 0, issues = {}, summary = "Failed to parse scan results" }
                    end
                else
                    success = false
                    data = "Empty response from AI"
                end
            end
        end

        if not success then
            scanScoreLabel.Text = "Scan failed"
            scanScoreLabel.TextColor3 = Color3.fromRGB(255, 80, 80)

            local errLabel = Instance.new("TextLabel")
            errLabel.Size = UDim2.new(1, 0, 0, 40)
            errLabel.BackgroundTransparency = 1
            errLabel.Text = "Error: " .. tostring(data)
            errLabel.TextColor3 = Color3.fromRGB(255, 80, 80)
            errLabel.TextSize = 11
            errLabel.Font = Enum.Font.Gotham
            errLabel.TextWrapped = true
            errLabel.LayoutOrder = 0
            errLabel.Parent = scanResultsScroll
            isProcessing = false
            return
        end

        -- Display score
        local score = data.score or 0
        scanScoreLabel.Text = string.format("Score: %d/100", score)
        scanScoreLabel.TextColor3 = getScoreColor(score)

        -- Display issues
        local issues = data.issues or {}
        if #issues == 0 then
            local cleanLabel = Instance.new("TextLabel")
            cleanLabel.Size = UDim2.new(1, 0, 0, 30)
            cleanLabel.BackgroundTransparency = 1
            cleanLabel.Text = data.summary or "No issues found. Clean code."
            cleanLabel.TextColor3 = Color3.fromRGB(80, 220, 80)
            cleanLabel.TextSize = 11
            cleanLabel.Font = Enum.Font.Gotham
            cleanLabel.TextWrapped = true
            cleanLabel.LayoutOrder = 0
            cleanLabel.Parent = scanResultsScroll
        else
            for idx, issue in ipairs(issues) do
                local issueFrame = Instance.new("Frame")
                issueFrame.Size = UDim2.new(1, 0, 0, 56)
                issueFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
                issueFrame.LayoutOrder = idx
                issueFrame.Parent = scanResultsScroll
                Instance.new("UICorner", issueFrame).CornerRadius = UDim.new(0, 4)

                local issuePad = Instance.new("UIPadding")
                issuePad.PaddingLeft = UDim.new(0, 6)
                issuePad.PaddingRight = UDim.new(0, 6)
                issuePad.PaddingTop = UDim.new(0, 4)
                issuePad.Parent = issueFrame

                -- Severity indicator
                local sevColor = Color3.fromRGB(255, 200, 50)
                local severity = (issue.severity or "info"):lower()
                if severity == "critical" then
                    sevColor = Color3.fromRGB(255, 70, 70)
                elseif severity == "warning" then
                    sevColor = Color3.fromRGB(255, 180, 50)
                else
                    sevColor = Color3.fromRGB(100, 160, 255)
                end

                local sevDot = Instance.new("Frame")
                sevDot.Size = UDim2.new(0, 6, 0, 6)
                sevDot.Position = UDim2.new(0, 0, 0, 5)
                sevDot.BackgroundColor3 = sevColor
                sevDot.Parent = issueFrame
                Instance.new("UICorner", sevDot).CornerRadius = UDim.new(1, 0)

                local titleLabel = Instance.new("TextLabel")
                titleLabel.Size = UDim2.new(1, -12, 0, 16)
                titleLabel.Position = UDim2.new(0, 12, 0, 0)
                titleLabel.BackgroundTransparency = 1
                titleLabel.Text = issue.title or "Issue"
                titleLabel.TextColor3 = Color3.fromRGB(220, 220, 240)
                titleLabel.TextSize = 11
                titleLabel.Font = Enum.Font.GothamBold
                titleLabel.TextXAlignment = Enum.TextXAlignment.Left
                titleLabel.TextTruncate = Enum.TextTruncate.AtEnd
                titleLabel.Parent = issueFrame

                local descLabel = Instance.new("TextLabel")
                descLabel.Size = UDim2.new(1, -12, 0, 16)
                descLabel.Position = UDim2.new(0, 12, 0, 16)
                descLabel.BackgroundTransparency = 1
                descLabel.Text = issue.description or ""
                descLabel.TextColor3 = Color3.fromRGB(150, 150, 170)
                descLabel.TextSize = 10
                descLabel.Font = Enum.Font.Gotham
                descLabel.TextXAlignment = Enum.TextXAlignment.Left
                descLabel.TextTruncate = Enum.TextTruncate.AtEnd
                descLabel.Parent = issueFrame

                local fixLabel = Instance.new("TextLabel")
                fixLabel.Size = UDim2.new(1, -12, 0, 16)
                fixLabel.Position = UDim2.new(0, 12, 0, 34)
                fixLabel.BackgroundTransparency = 1
                fixLabel.Text = "Fix: " .. (issue.fix or "N/A")
                fixLabel.TextColor3 = Color3.fromRGB(80, 200, 120)
                fixLabel.TextSize = 10
                fixLabel.Font = Enum.Font.Gotham
                fixLabel.TextXAlignment = Enum.TextXAlignment.Left
                fixLabel.TextTruncate = Enum.TextTruncate.AtEnd
                fixLabel.Parent = issueFrame
            end
        end

        scanResultsScroll.CanvasSize = UDim2.new(0, 0, 0, #issues * 60 + 20)
        scanResults = data
        isProcessing = false
    end)()
end

scanBtn.MouseButton1Click:Connect(runGameScan)

--------------------------------------------------------------------
-- EVENT CONNECTIONS
--------------------------------------------------------------------
generateBtn.MouseButton1Click:Connect(generate)

undoBtn.MouseButton1Click:Connect(function()
    local success, msg = undoLastChange()
    statusLabel.Text = msg
    statusLabel.TextColor3 = success
        and Color3.fromRGB(120, 220, 120)
        or Color3.fromRGB(255, 200, 50)

    -- Refresh changes display
    for _, child in ipairs(changesFrame:GetChildren()) do
        if child:IsA("TextLabel") then child:Destroy() end
    end
    for i, entry in ipairs(changeHistory) do
        local changeLabel = Instance.new("TextLabel")
        changeLabel.Size = UDim2.new(1, 0, 0, 24)
        changeLabel.BackgroundTransparency = 1
        changeLabel.Text = string.format("  %d. %s", i, entry.explanation or "Change")
        changeLabel.TextColor3 = Color3.fromRGB(150, 150, 170)
        changeLabel.TextSize = 11
        changeLabel.Font = Enum.Font.Gotham
        changeLabel.TextXAlignment = Enum.TextXAlignment.Left
        changeLabel.LayoutOrder = i
        changeLabel.Parent = changesFrame
    end
    changesFrame.CanvasSize = UDim2.new(0, 0, 0, #changeHistory * 26)
end)

toggleButton.Click:Connect(function()
    widget.Enabled = not widget.Enabled
end)

--------------------------------------------------------------------
-- STARTUP
--------------------------------------------------------------------
statusLabel.Text = "RobloxMaxx v" .. PLUGIN_VERSION .. " ready. Enter your API key, pick a genre, and build."
print("[RobloxMaxx] Plugin loaded v" .. PLUGIN_VERSION .. " (BYOK) - Meta Advisor, Revenue Estimator, Game Scanner")
