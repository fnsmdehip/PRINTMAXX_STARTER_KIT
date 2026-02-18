import Link from 'next/link';

export default function DocsPage() {
  return (
    <main className="docs-page">
      <div className="docs-container">
        <h1>Documentation</h1>
        <p className="docs-intro">
          Everything you need to build Roblox games with AI. Install the plugin,
          paste your API key, and start generating.
        </p>

        {/* Table of contents */}
        <nav className="docs-toc">
          <h3>On this page</h3>
          <ul>
            <li><a href="#installation">Plugin installation</a></li>
            <li><a href="#getting-started">Getting started</a></li>
            <li><a href="#modes">Generation modes</a></li>
            <li><a href="#genres">Genre guide</a></li>
            <li><a href="#api-reference">API reference</a></li>
            <li><a href="#faq">FAQ</a></li>
          </ul>
        </nav>

        {/* Installation */}
        <section id="installation" className="docs-section">
          <h2>Plugin installation</h2>

          <h3>Option A: Manual install</h3>
          <ol className="docs-steps">
            <li>
              <a href="/api/download">Download RobloxMaxxPlugin.lua</a>
            </li>
            <li>
              Open your Roblox Studio plugins folder:
              <div className="code-block">
                <code>%localappdata%\Roblox\Plugins</code>
              </div>
              On Mac:
              <div className="code-block">
                <code>~/Documents/Roblox/Plugins</code>
              </div>
            </li>
            <li>Drop <code>RobloxMaxxPlugin.lua</code> into that folder.</li>
            <li>Restart Roblox Studio. The RobloxMaxx panel appears in the Plugins tab.</li>
          </ol>

          <h3>Option B: Creator Store</h3>
          <p>
            Search &quot;RobloxMaxx&quot; on the Creator Store and click Install.
            Available once the plugin is published.
          </p>
        </section>

        {/* Getting started */}
        <section id="getting-started" className="docs-section">
          <h2>Getting started</h2>

          <ol className="docs-steps">
            <li>
              <strong>Create an account</strong> at{' '}
              <Link href="/signup">/signup</Link>. You get 250 free actions per
              month.
            </li>
            <li>
              <strong>Copy your API token</strong> from the{' '}
              <Link href="/dashboard">dashboard</Link>.
            </li>
            <li>
              <strong>Open Roblox Studio</strong> and click the RobloxMaxx button
              in the Plugins tab.
            </li>
            <li>
              <strong>Paste your token</strong> in the &quot;API Key / Token&quot;
              field.
            </li>
            <li>
              <strong>Select &quot;RobloxMaxx&quot;</strong> as the AI provider
              (or use your own Claude/GPT-4/Gemini key).
            </li>
            <li>
              <strong>Pick a genre</strong> (Tycoon, Obby, Simulator, RPG, Horror,
              or General).
            </li>
            <li>
              <strong>Describe what you want</strong> in plain English and click
              Generate.
            </li>
          </ol>

          <div className="docs-tip">
            For best results, be specific. Instead of &quot;make a tycoon&quot;,
            try &quot;Build a tycoon where players mine crystals, sell them for
            gold, buy bigger drills. Include a rebirth system that gives 2x
            earnings.&quot;
          </div>
        </section>

        {/* Modes */}
        <section id="modes" className="docs-section">
          <h2>Generation modes</h2>

          <div className="docs-mode-grid">
            <div className="docs-mode-card">
              <h3>Code</h3>
              <p>
                Generate or modify scripts in your game. The AI reads your existing
                code, understands the context, and creates new scripts or edits
                existing ones. Changes apply directly to your place.
              </p>
              <p className="docs-mode-use">
                Use for: Adding features, fixing bugs, creating new systems.
              </p>
            </div>

            <div className="docs-mode-card">
              <h3>Ask</h3>
              <p>
                Ask questions about your game code. The AI reads all scripts in
                your place and answers with specific references. No code changes
                are made.
              </p>
              <p className="docs-mode-use">
                Use for: Debugging, understanding code, getting suggestions.
              </p>
            </div>

            <div className="docs-mode-card">
              <h3>Scaffold</h3>
              <p>
                Generate a complete game from scratch. Describe what you want and
                the AI creates 8-20 scripts covering server logic, client UI, data
                persistence, monetization, and leaderboards.
              </p>
              <p className="docs-mode-use">
                Use for: Starting new games, creating full prototypes fast.
              </p>
            </div>
          </div>
        </section>

        {/* Genres */}
        <section id="genres" className="docs-section">
          <h2>Genre guide</h2>
          <p>
            Selecting a genre gives the AI specialized knowledge about that game
            type. It knows the patterns, mechanics, and architecture for each.
          </p>

          <div className="docs-genre-list">
            <div className="docs-genre">
              <h3>Tycoon</h3>
              <p>
                Dropper-collector-upgrader loops, plot claiming, currency systems,
                rebirth mechanics, conveyor belts, prestige tiers, exponential cost
                scaling.
              </p>
            </div>

            <div className="docs-genre">
              <h3>Obby</h3>
              <p>
                Checkpoint/stage system, kill bricks, moving platforms, rotating
                obstacles, skip-stage gamepasses, speedrun timers, difficulty
                progression.
              </p>
            </div>

            <div className="docs-genre">
              <h3>Simulator</h3>
              <p>
                Click-to-earn, tool tiers, pet hatching with rarity weights, rebirth
                multipliers, zone unlocking, auto-collectors, trading, codes system.
              </p>
            </div>

            <div className="docs-genre">
              <h3>RPG</h3>
              <p>
                Quest system, inventory/equipment, combat (melee + ranged), NPC
                dialogue, XP/leveling, stats, dungeon instances, party system, loot
                tables.
              </p>
            </div>

            <div className="docs-genre">
              <h3>Horror</h3>
              <p>
                Atmosphere (fog, lighting), monster AI with pathfinding, chase
                triggers, jump scares, flashlight/battery, key/puzzle items,
                stamina, multiple endings.
              </p>
            </div>

            <div className="docs-genre">
              <h3>General</h3>
              <p>
                No genre-specific prompting. Good for custom game types, utility
                scripts, or when you want full control over the AI&apos;s direction.
              </p>
            </div>
          </div>
        </section>

        {/* API Reference */}
        <section id="api-reference" className="docs-section">
          <h2>API reference</h2>
          <p>
            The plugin communicates with these endpoints. You can also call them
            directly if you&apos;re building your own integration.
          </p>

          <div className="docs-endpoint">
            <h3>
              <span className="method-badge post">POST</span>{' '}
              /api/auth/register
            </h3>
            <p>Create a new account.</p>
            <h4>Request body</h4>
            <div className="code-block">
              <code>{`{ "email": "user@example.com", "password": "min8chars" }`}</code>
            </div>
            <h4>Response</h4>
            <div className="code-block">
              <code>{`{ "token": "jwt...", "apiKey": "rmx_...", "message": "Account created. 250 free actions included." }`}</code>
            </div>
          </div>

          <div className="docs-endpoint">
            <h3>
              <span className="method-badge post">POST</span>{' '}
              /api/auth/login
            </h3>
            <p>Log in to an existing account.</p>
            <h4>Request body</h4>
            <div className="code-block">
              <code>{`{ "email": "user@example.com", "password": "yourpassword" }`}</code>
            </div>
            <h4>Response</h4>
            <div className="code-block">
              <code>{`{ "token": "jwt...", "userId": 1 }`}</code>
            </div>
          </div>

          <div className="docs-endpoint">
            <h3>
              <span className="method-badge post">POST</span>{' '}
              /api/generate
            </h3>
            <p>Generate Luau code from a natural language prompt.</p>
            <h4>Request body</h4>
            <div className="code-block">
              <code>{`{
  "token": "jwt_or_rmx_api_key",
  "prompt": "Build a shop with 3 items",
  "mode": "code | question | scaffold",
  "genre": "tycoon | obby | simulator | rpg | horror | general",
  "context": "existing game scripts (optional)",
  "pluginVersion": "1.0.0"
}`}</code>
            </div>
            <h4>Response</h4>
            <div className="code-block">
              <code>{`{ "response": "[{action JSON array}]", "actionsRemaining": "check /api/usage" }`}</code>
            </div>
          </div>

          <div className="docs-endpoint">
            <h3>
              <span className="method-badge get">GET</span>{' '}
              /api/usage
            </h3>
            <p>Check your usage stats. Requires Bearer token in Authorization header.</p>
            <h4>Response</h4>
            <div className="code-block">
              <code>{`{ "plan": "free", "actionsUsed": 12, "actionsLimit": 250, "actionsRemaining": 238 }`}</code>
            </div>
          </div>

          <div className="docs-endpoint">
            <h3>
              <span className="method-badge get">GET</span>{' '}
              /api/templates
            </h3>
            <p>List available starter templates, or get a specific template by genre.</p>
            <h4>Query params</h4>
            <div className="code-block">
              <code>?genre=tycoon</code>
            </div>
            <h4>Response (list)</h4>
            <div className="code-block">
              <code>{`{ "templates": [{ "genre": "tycoon", "name": "...", "description": "...", "scriptCount": 10 }] }`}</code>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section id="faq" className="docs-section">
          <h2>FAQ</h2>

          <div className="faq-list">
            <div className="faq-item">
              <h3>Is RobloxMaxx free?</h3>
              <p>
                Yes. The free plan includes 250 actions per month. Enough to build
                a full game. Upgrade for more actions and access to Opus-tier models.
              </p>
            </div>

            <div className="faq-item">
              <h3>Can I use my own API key?</h3>
              <p>
                Yes. The plugin supports Claude, GPT-4, and Gemini. Select the
                provider in the dropdown and paste your own API key. Your key goes
                directly to the provider, not through our servers.
              </p>
            </div>

            <div className="faq-item">
              <h3>What models does RobloxMaxx use?</h3>
              <p>
                Free plan uses Claude Sonnet. Pro plan adds Claude Opus. You can
                also bring your own key for GPT-4o or Gemini 1.5 Pro.
              </p>
            </div>

            <div className="faq-item">
              <h3>Does the AI understand my existing game?</h3>
              <p>
                Yes. The plugin reads all scripts in your place and sends them as
                context. The AI can modify existing code, add to it, or create new
                scripts that integrate with what you already have.
              </p>
            </div>

            <div className="faq-item">
              <h3>Can I undo changes?</h3>
              <p>
                Yes. Click &quot;Undo Last Change&quot; in the plugin. Every script
                modification is backed up before changes are applied.
              </p>
            </div>

            <div className="faq-item">
              <h3>Is the generated code production-ready?</h3>
              <p>
                The AI generates Luau code following Roblox best practices:
                client-server separation, DataStoreService persistence, input
                validation, proper error handling. Always review generated code
                before publishing your game.
              </p>
            </div>

            <div className="faq-item">
              <h3>Is RobloxMaxx affiliated with Roblox?</h3>
              <p>
                No. RobloxMaxx is an independent third-party tool. Roblox is a
                trademark of Roblox Corporation.
              </p>
            </div>
          </div>
        </section>

        <div className="docs-cta">
          <Link href="/signup" className="cta-btn">
            Get started free
          </Link>
        </div>
      </div>
    </main>
  );
}
