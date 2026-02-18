import Link from 'next/link';

export default function HomePage() {
  return (
    <main>
      {/* Hero */}
      <section className="hero">
        <h1>Build Roblox games with AI</h1>
        <p className="subtitle">
          Describe what you want in plain English. RobloxMaxx generates
          production-ready Luau code, tests it, and deploys to your game.
          Tycoons, obbys, simulators, RPGs, horror. Any genre.
        </p>
        <Link href="/signup" className="cta-btn">
          Get started free
        </Link>
        <p style={{ marginTop: 12, color: '#8888aa', fontSize: '0.9rem' }}>
          Bring your own AI API key. You control your costs. Free forever for basic use.
        </p>
      </section>

      {/* How it works */}
      <section className="how-it-works">
        <h2>How it works</h2>
        <div className="steps-grid">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Install the plugin</h3>
            <p>
              Drop one Lua file into your Roblox Studio plugins folder. Takes 30
              seconds. Or install from the Creator Store.
            </p>
          </div>
          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Describe your game</h3>
            <p>
              Pick a genre and type what you want in plain English. &quot;Build a
              tycoon with crystal mining, upgradeable drills, and a rebirth
              system.&quot;
            </p>
          </div>
          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Get working code</h3>
            <p>
              The AI generates 8-20 scripts with server logic, client UI, data
              persistence, and monetization. Playable in minutes.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <div className="feature-card">
          <h3>Genre-aware AI</h3>
          <p>
            Select your genre (tycoon, obby, simulator, RPG, horror) and the AI
            generates code optimized for that game type. Knows dropper loops,
            checkpoint systems, pet rarities, quest trees, and monster AI out of
            the box.
          </p>
        </div>
        <div className="feature-card">
          <h3>Full game scaffold</h3>
          <p>
            Describe your game in one sentence. RobloxMaxx generates 10-20
            scripts covering server logic, client UI, data persistence,
            monetization hooks, and leaderboards. Playable in minutes.
          </p>
        </div>
        <div className="feature-card">
          <h3>Studio plugin</h3>
          <p>
            Lightweight plugin runs inside Roblox Studio. No tab switching, no
            copy-pasting code. Changes apply directly to your game with full
            undo history.
          </p>
        </div>
        <div className="feature-card">
          <h3>Multi-model support</h3>
          <p>
            Use Claude, GPT-4, or Gemini. Bring your own API key (BYOK).
            You control your model, your costs, your data. Switch models mid-session.
          </p>
        </div>
        <div className="feature-card">
          <h3>Starter templates</h3>
          <p>
            One-click templates for tycoon, obby, and simulator games. Complete
            with data persistence, monetization, and leaderboards. Customize
            from there.
          </p>
        </div>
        <div className="feature-card">
          <h3>Built-in monetization</h3>
          <p>
            Every generated game includes gamepass hooks, developer product
            integration, and premium currency systems. Start earning Robux from
            day one.
          </p>
        </div>
      </section>

      {/* Demo */}
      <section className="demo">
        <h2>See it in action</h2>
        <p style={{ color: '#8888aa', maxWidth: 600, margin: '0 auto' }}>
          Type what you want. Get working code.
        </p>
        <div className="demo-box">
          <div className="demo-prompt">
            &gt; Build a tycoon game where players mine crystals, sell them for
            gold, and buy bigger drills. Include a rebirth system that resets
            your drill but gives 2x earnings permanently.
          </div>
          <div className="demo-output">
            {`Creating 12 scripts...
 [1/12] ReplicatedStorage/TycoonConfig (ModuleScript) - Game balancing
 [2/12] ServerScriptService/TycoonManager (Script) - Core game logic
 [3/12] ServerScriptService/DrillSystem (Script) - Mining mechanics
 [4/12] ServerScriptService/RebirthHandler (Script) - Rebirth logic
 [5/12] ServerScriptService/DataManager (Script) - Save/load player data
 [6/12] StarterGui/TycoonHUD (LocalScript) - Currency + drill display
 [7/12] StarterGui/ShopUI (LocalScript) - Drill shop + upgrades
 [8/12] StarterGui/RebirthUI (LocalScript) - Rebirth confirmation
 [9/12] ReplicatedStorage/Events (Folder) - RemoteEvents
 [10/12] ServerStorage/DrillTemplates (Folder) - Drill models
 [11/12] ServerScriptService/MonetizationSetup (Script) - Gamepasses
 [12/12] ServerScriptService/Leaderboard (Script) - Leaderstats

Done! 12 scripts created. Game is playable.`}
          </div>
        </div>
      </section>

      {/* Social proof */}
      <section className="social-proof">
        <h2>Built by Roblox developers, for Roblox developers</h2>
        <div className="proof-grid">
          <div className="proof-card">
            <p className="proof-quote">
              &quot;Generated a full tycoon in under 5 minutes. DataStore
              persistence, gamepass integration, rebirth system. All working out
              of the box.&quot;
            </p>
            <p className="proof-author">Early beta tester</p>
          </div>
          <div className="proof-card">
            <p className="proof-quote">
              &quot;The genre-aware prompting makes a huge difference. It knows
              obby checkpoint patterns and simulator pet rarity weights without me
              explaining anything.&quot;
            </p>
            <p className="proof-author">Early beta tester</p>
          </div>
          <div className="proof-card">
            <p className="proof-quote">
              &quot;I used to spend hours on boilerplate. Now I scaffold a game,
              then iterate with the AI on specific features. Ship time went from
              weeks to days.&quot;
            </p>
            <p className="proof-author">Early beta tester</p>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="pricing" id="pricing">
        <h2>Pricing</h2>
        <p style={{ color: '#8888aa', maxWidth: 600, margin: '0 auto 24px', textAlign: 'center' }}>
          Bring your own AI API key (Claude, GPT, or Gemini). You control your costs.
        </p>
        <div className="pricing-grid">
          <div className="price-card">
            <h3>Free</h3>
            <div className="price">
              $0<span>/forever</span>
            </div>
            <ul>
              <li>Roblox Studio plugin</li>
              <li>Basic code generation (BYOK)</li>
              <li>All 5 genres</li>
              <li>Community templates</li>
              <li>Unlimited actions (your API key)</li>
            </ul>
            <Link href="/signup" className="cta-btn" style={{ width: '100%', display: 'block', textAlign: 'center' }}>
              Get started
            </Link>
          </div>
          <div className="price-card popular">
            <h3>Pro</h3>
            <div className="price">
              $9.99<span>/mo</span>
            </div>
            <ul>
              <li>Everything in Free</li>
              <li>Meta advisor (genre trends + strategy)</li>
              <li>Revenue estimator (DAU to USD)</li>
              <li>Game health scanner</li>
              <li>5 premium genre templates</li>
              <li>Premium game design intelligence</li>
            </ul>
            <Link href="/signup?plan=pro" className="cta-btn" style={{ width: '100%', display: 'block', textAlign: 'center' }}>
              Start free trial
            </Link>
          </div>
        </div>
      </section>

      {/* Personal use */}
      <section className="personal-use" style={{ maxWidth: 700, margin: '0 auto', padding: '60px 20px', textAlign: 'center' }}>
        <h2>For personal use</h2>
        <p style={{ color: '#8888aa', marginBottom: 16, lineHeight: 1.6 }}>
          If you just want to build your own Roblox games with AI (not sell
          the tool to others), you can use Claude Code with our free MCP
          server. It gives you the same genre-aware prompts and Roblox
          tooling, running locally on your machine.
        </p>
        <p style={{ color: '#8888aa', lineHeight: 1.6 }}>
          Requires a Claude Pro or Max subscription and Claude Code installed.
          See the{' '}
          <a href="https://github.com/anthropics/claude-code" style={{ color: '#5865F2', textDecoration: 'underline' }}>
            Claude Code docs
          </a>{' '}
          to get started, then check our LOCAL_SETUP.md in the repo.
        </p>
      </section>

      {/* FAQ */}
      <section className="landing-faq">
        <h2>Frequently asked questions</h2>
        <div className="faq-list">
          <div className="faq-item">
            <h3>Is RobloxMaxx free?</h3>
            <p>
              The plugin and basic code generation are free forever. You bring
              your own AI API key (Claude, OpenAI, or Gemini) and pay the provider
              directly. No credit card required for RobloxMaxx.
            </p>
          </div>
          <div className="faq-item">
            <h3>How does BYOK (Bring Your Own Key) work?</h3>
            <p>
              You get an API key from Anthropic, OpenAI, or Google and enter it
              in the plugin. Your key goes directly to the AI provider. We never
              store or see your key. You pay the provider directly, typically
              $0.01-0.15 per generation.
            </p>
          </div>
          <div className="faq-item">
            <h3>What kind of games can it build?</h3>
            <p>
              Tycoons, obbys, simulators, RPGs, horror games, and anything else.
              Genre-aware mode gives the AI specialized knowledge for each type.
            </p>
          </div>
          <div className="faq-item">
            <h3>Does it work with existing games?</h3>
            <p>
              Yes. The plugin reads all scripts in your place and uses them as
              context. The AI can modify, extend, or add to your existing code.
            </p>
          </div>
          <div className="faq-item">
            <h3>Is the generated code safe?</h3>
            <p>
              The AI follows Roblox best practices: server-side validation,
              pcall error handling, DataStoreService for saves, proper
              client-server separation. Always review before publishing.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-links">
          <Link href="/docs">Docs</Link>
          <Link href="/signup">Sign up</Link>
          <Link href="/login">Log in</Link>
          <Link href="/#pricing">Pricing</Link>
        </div>
        <p>RobloxMaxx is not affiliated with Roblox Corporation.</p>
        <p style={{ marginTop: 8 }}>
          Built by PRINTMAXXER. Ship games, not excuses.
        </p>
      </footer>
    </main>
  );
}
