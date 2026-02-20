# PRINTMAXX Security Architecture

**Status:** PENDING_USER_APPROVAL
**Date:** 2026-02-19
**Priority:** CRITICAL — read before approving any system changes
**DO NOT IMPLEMENT until user approves.**

---

## OpenClaw security assessment (nuanced — updated 2026-02-19)

### the full picture

OpenClaw has TWO distinct attack surfaces. they need to be evaluated separately.

**ATTACK SURFACE 1: ClawHub skills marketplace (BLOCKED — do not use)**

- **1,184 confirmed malicious skills** out of ~10,700 on ClawHub (1 in 5 at peak)
- malicious skills delivered **Atomic macOS Stealer (AMOS)** — a $500-$1,000/mo malware-as-a-service
- AMOS steals: **Keychain credentials, browser data, crypto wallets, Telegram sessions, SSH keys, files from Documents/Desktop**
- some skills contained **prompt injection payloads** that instructed bots to run `curl` commands sending `.env` and `creds.json` to attacker servers
- Cisco found **26% of all 31,000 agent skills analyzed contained at least one vulnerability**
- **verdict: NEVER use ClawHub skills. period.**

**ATTACK SURFACE 2: OpenClaw core daemon (CONDITIONAL — usable with hardening)**

the core daemon ALSO had its own vulnerabilities (not just skills):
- **CVE-2026-25253 (CVSS 8.8):** remote code execution via cross-site WebSocket hijacking
- **CVE-2026-25157:** OS command injection in SSH handler
- **CVE-2026-24763:** Docker command injection
- **512 vulnerabilities** found in first security audit, 8 critical
- **40,214 publicly exposed instances** found leaking API keys, Slack OAuth tokens, chat histories
- **ALL patched in v2026.2.12** (released after audit)

**what the industry says:**
- Kaspersky declared OpenClaw "unsafe for use" (blanket statement, didn't distinguish core vs skills)
- Dutch DPA and Belgium CERT issued warnings
- Meta BANNED OpenClaw from company devices
- Pieter Levels: "too scared to run it on any production server"
- Karpathy: reversed from "incredible sci-fi" to "dumpster fire"
- Steinberger (creator): joined OpenAI Feb 14, 2026. reportedly said security "isn't something he wants to prioritize"
- project moving to open source foundation

**sources:** The Hacker News, Kaspersky, Bitsight, Cisco, SC Media, VentureBeat, CyberPress, Sophos, The Register, Aikido, multiple CERTs

### what this means for PRINTMAXX

**two-track assessment:**

| Component | Status | Conditions |
|-----------|--------|------------|
| **ClawHub skills** | BLOCKED | never use. no exceptions. |
| **Core daemon (model router only)** | CONDITIONAL | usable IF: v2026.2.12+, Docker, localhost-only, no skills, no ClawHub |

**if using OpenClaw core as model router only (optional, not required):**
1. must run v2026.2.12 or later (all known CVEs patched)
2. must run inside Docker container (blast radius containment)
3. must bind to localhost only (no network exposure)
4. must have ZERO skills installed (no ClawHub interaction)
5. must run on Laptop 2 only (separate from control node)
6. must be monitored with LuLu + BlockBlock
7. must be audited monthly against new CVEs

**alternatives that achieve the same thing with less risk:**
- **LiteLLM proxy (self-hosted):** open source, multi-model routing, no marketplace attack surface
- **OpenRouter:** hosted model routing, no local daemon needed
- **Claude Code + Codex CLI side-by-side:** each talks directly to vendor API, no middleware

**recommendation:** use Claude Code on Laptop 1, OpenAI Codex CLI on Laptop 2. if you specifically want OpenClaw's model routing, the core-only hardened setup above is defensible for non-sensitive workloads. but LiteLLM achieves the same routing with a much smaller attack surface.

---

## the broader threat landscape (why this matters beyond OpenClaw)

### attack vectors that affect us directly

| Vector | Severity | Real-world? | What gets stolen |
|--------|----------|-------------|-----------------|
| **MCP tool poisoning** | CRITICAL | YES (WhatsApp exfil demonstrated) | chat histories, API keys, credentials |
| **MCP rug pulls** | CRITICAL | demonstrated | tool silently changes behavior after trust is established |
| **malicious npm/pip packages** | CRITICAL | YES (fake Claude Code packages found) | API keys, crypto wallets, SSH keys |
| **npm supply chain compromise** | CRITICAL | YES (chalk/debug: 2.6B downloads affected) | crypto wallets, browser data, everything |
| **slopsquatting** | HIGH | demonstrated (20% of AI-suggested packages don't exist) | whatever the fake package wants |
| **indirect prompt injection** | CRITICAL | YES (EchoLeak, CometJacking, Cursor) | internal files, credentials, conversations |
| **CLAUDE.md poisoning** | HIGH | demonstrated | agent behavior hijacked via repo configs |
| **AI CLI weaponization** | HIGH | YES (Nx s1ngularity: 2,349 secrets stolen) | SSH keys, npm tokens, crypto wallets, API keys |
| **credential theft via agents** | CRITICAL | YES (GitHub PAT exfiltration) | full repo access, secrets, private data |
| **crypto clipboard hijacking** | HIGH | YES (multiple npm/PyPI packages) | crypto wallet addresses replaced at send time |

### specific incidents we must protect against

1. **Shai-Hulud (Sep-Nov 2025):** compromised `chalk` and `debug` npm packages (2.6B downloads). injected crypto-draining malware that hooked `fetch()`, `XMLHttpRequest`, and `window.ethereum`. wave 2 compromised 700+ packages in hours and attempted to **destroy victim's home directory** if exfiltration failed. CISA issued formal alert.

2. **fake Claude Code packages:** `@chatgptclaude_club/claude-code` and `@chatclub1/claude-code` hijacked the `claude` command, stole API credentials, established bidirectional C2 channel to proxy victims' Claude sessions.

3. **Nx s1ngularity (Aug 2025):** malicious versions of Nx build system **weaponized installed AI CLI tools** (Claude, Gemini, Amazon Q) to recursively scan filesystems for secrets. first documented case of malware weaponizing AI tools. exfiltrated 2,349 secrets.

4. **MCP tool poisoning:** Invariant Labs showed a malicious MCP server could silently exfiltrate a user's entire WhatsApp message history by embedding hidden instructions in tool descriptions. 5.5% of MCP servers exhibit this.

5. **LangGrinch (CVE-2025-68664, CVSS 9.3):** serialization injection in langchain-core allowed environment variable theft (cloud credentials, database strings, API keys) and arbitrary code execution.

6. **Claude Code WebSocket bypass (CVE-2025-52882, CVSS 8.8):** Claude IDE extension started WebSocket server without authentication. visiting a website could read local files and execute code. patched June 2025.

7. **weaponized Claude Skills (MedusaLocker):** Cato CTRL demonstrated a popular "GIF Creator" Skill could execute ransomware once approved.

---

## PRINTMAXX security architecture (4-layer defense)

### layer 1: REPO VETTING (before any code enters our system)

**every repo, package, or tool MUST pass this checklist before use:**

```
REPO VETTING CHECKLIST (MANDATORY)
├── 1. REPUTATION CHECK
│   ├── Stars > 100 (or well-known org)
│   ├── Contributors > 5
│   ├── Last commit < 6 months ago
│   ├── Verified org on GitHub (if claiming to be official)
│   ├── Check: is this the REAL package? (not typosquatting)
│   └── Search: "[package name] malware" / "[package name] vulnerability"
│
├── 2. LICENSE CHECK
│   ├── MIT, Apache 2.0, BSD = OK
│   ├── GPL/AGPL = NO (requires code release)
│   └── No license = CAUTION (legal risk)
│
├── 3. STATIC ANALYSIS (run before executing anything)
│   ├── npm install --ignore-scripts (NEVER run install scripts blindly)
│   ├── npm audit / pip-audit (known CVEs)
│   ├── guarddog pypi scan <package> / guarddog npm scan <package>
│   │   (detects: base64 payloads, droppers, steganography, exfiltration)
│   ├── trufflehog filesystem . (credential scanning)
│   ├── semgrep --config auto . (code quality/security)
│   └── clamscan -r . (malware signatures)
│
├── 4. MANUAL RED FLAGS CHECK
│   ├── preinstall/postinstall scripts that run curl/wget/encoded commands
│   ├── eval(), exec(), Function(), base64 decoding in non-obvious places
│   ├── network calls in packages that shouldn't need network
│   ├── filesystem reads of ~/.ssh, ~/.aws, .env, wallet files
│   ├── obfuscated/minified code in non-minified source files
│   └── dependencies on packages with very few downloads
│
└── 5. SANDBOXED FIRST RUN
    ├── docker run --rm --network none (no network access)
    ├── monitor with fs_usage (what files does it read?)
    ├── monitor with LuLu/Little Snitch (what does it connect to?)
    └── only promote to production after clean sandbox run
```

**tools to install (all free):**
```bash
# package scanning
brew install trufflehog gitleaks semgrep clamav
pip install pip-audit guarddog

# pre-commit hooks
cd /path/to/project && gitleaks protect --install

# macOS monitoring
# install from https://objective-see.org/:
# - LuLu (network firewall)
# - BlockBlock (persistence monitor)
# - KnockKnock (persistence scanner)
```

### layer 2: CREDENTIAL PROTECTION (assume breach, minimize blast radius)

**principle:** if any single script is compromised, it should NOT be able to access credentials it doesn't need.

```
CREDENTIAL ISOLATION ARCHITECTURE
├── API KEYS (Anthropic, OpenAI, Stripe, etc.)
│   ├── NEVER in .env files on disk
│   ├── USE envchain (macOS Keychain-backed)
│   │   envchain --set anthropic ANTHROPIC_API_KEY
│   │   envchain anthropic python3 script.py
│   ├── keys only exist in memory for specific process
│   └── other processes CANNOT read them
│
├── SSH KEYS
│   ├── USE Secretive (Secure Enclave-backed)
│   │   brew install --cask secretive
│   ├── private keys stored in hardware (Secure Enclave)
│   ├── CANNOT be exported even if system fully compromised
│   ├── requires Touch ID to use
│   └── chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_*
│
├── CRYPTO WALLETS
│   ├── NEVER store seed phrases or private keys on dev machine
│   ├── USE hardware wallet (Ledger/Trezor) for all holdings
│   ├── if hot wallet needed: separate macOS user account
│   ├── wallet files: chmod 600, monitor access with fs_usage
│   └── NEVER install AI tools/agents on wallet machine
│
├── BROWSER CREDENTIALS (social accounts, platform logins)
│   ├── use separate browser profiles per account group
│   ├── anti-detect browser for multi-account ops
│   ├── NEVER let automation scripts access production cookies
│   ├── use dedicated Brave profile for Twitter scraping
│   └── rotate session tokens regularly
│
└── PROJECT SECRETS (SECRETS/ directory)
    ├── chmod 600 SECRETS/*
    ├── .gitignore MUST include SECRETS/
    ├── guardrails.py blocks any write/read outside project root
    └── monitor: sudo fs_usage -w -f pathname | grep SECRETS
```

**install credential protection:**
```bash
# keychain-backed secrets (replaces .env files)
brew install envchain
envchain --set anthropic ANTHROPIC_API_KEY
envchain --set stripe STRIPE_SECRET_KEY

# secure enclave SSH keys (impossible to exfiltrate)
brew install --cask secretive

# enable FileVault (full disk encryption)
# System Settings > Privacy & Security > FileVault
```

### layer 3: RUNTIME MONITORING (detect malware while scripts run)

**always-on monitoring stack (all free):**

| Tool | What it does | Install |
|------|-------------|---------|
| **LuLu** | blocks/alerts on ALL outbound network connections from unknown processes | objective-see.org |
| **BlockBlock** | alerts when ANYTHING tries to persist (LaunchAgent, cron, shell config) | objective-see.org |
| **KnockKnock** | scans all persistence locations on login | objective-see.org |
| **OverSight** | alerts on mic/camera access | objective-see.org |

**per-script monitoring (when running something new):**

```bash
# watch what files a script reads/writes
sudo fs_usage -w -f pathname python3 | tee /tmp/file_access.log &

# watch what network connections a script makes
sudo lsof -i -n -P | grep python3

# capture all traffic for analysis
sudo tcpdump -i any -w /tmp/capture.pcap &
python3 suspicious_script.py
kill %1  # stop tcpdump
tshark -r /tmp/capture.pcap -q -z endpoints,ip  # analyze

# watch for child processes (unexpected curl, wget, bash)
sudo execsnoop  # in separate terminal
```

**red flags during runtime:**
- script connects to IP addresses (not domain names)
- DNS queries to unusual TLDs (.tk, .ml, .ga, .cf)
- connections to servers not in the script's documented dependencies
- reading ~/.ssh, ~/.aws, ~/.gnupg, wallet files
- spawning curl/wget/bash child processes
- writing to LaunchAgents/ or cron
- base64-encoded data in HTTP headers or POST bodies
- large outbound data transfers to single IP

### layer 4: PRINTMAXX-SPECIFIC HARDENING

**guardrails already in place (keep and strengthen):**
- `guardrails.py` — all file ops must stay within project root
- `.claude/rules/guardrails.md` — explicit path boundaries
- no `os.system()` with user-controllable input
- lock files prevent double-runs
- append-only logging

**additional hardening needed:**

```
PRINTMAXX HARDENING ADDITIONS
├── 1. MCP SERVER AUDIT
│   ├── audit every MCP server in claude_desktop_config.json
│   ├── only use OFFICIAL MCP servers from verified orgs
│   ├── no community/third-party MCP servers without full vetting
│   ├── pin MCP server versions (never auto-update)
│   └── periodically re-scan installed MCP servers
│
├── 2. SCRAPER ISOLATION
│   ├── twitter/reddit scrapers run in separate process
│   ├── scraped content treated as UNTRUSTED INPUT
│   ├── no eval() or exec() on scraped content
│   ├── scraped URLs not auto-fetched without sanitization
│   └── alpha_auto_processor must sanitize before routing
│
├── 3. PROMPT INJECTION DEFENSE
│   ├── all external content (tweets, reddit posts, web pages)
│   │   treated as potentially containing prompt injection
│   ├── scraped content goes into data files, NOT into prompts
│   ├── if content must enter a prompt: wrap in clear delimiters
│   │   e.g., "The following is UNTRUSTED user content: <content>"
│   ├── never execute commands found in scraped content
│   └── CLAUDE.md/CODEX.md: validate no unauthorized modifications
│
├── 4. DEPENDENCY LOCKFILES
│   ├── always commit package-lock.json / requirements.txt
│   ├── use exact versions, not ranges (no ^1.0.0, use 1.0.0)
│   ├── npm ci (not npm install) in production
│   ├── run npm audit / pip-audit before every session
│   └── set up Socket.dev GitHub app for PR scanning
│
├── 5. BACKUP AND RECOVERY
│   ├── full backup before installing any new dependency
│   ├── git commit before running any new/untrusted script
│   ├── ~/PRINTMAXX_BACKUPS/ stays outside project (existing)
│   ├── backup SECRETS/ separately (encrypted)
│   └── test restore procedure monthly
│
├── 6. CRON JOB SECURITY
│   ├── all cron scripts must be in AUTOMATIONS/ (existing rule)
│   ├── no cron job should run with network access it doesn't need
│   ├── cron output goes to logs (existing)
│   ├── monitor for unauthorized crontab modifications (BlockBlock catches this)
│   └── review crontab weekly for unexpected entries
│
└── 7. SOCIAL ACCOUNT PROTECTION
    ├── 2FA on ALL social accounts (TOTP, not SMS)
    ├── unique passwords per account (password manager)
    ├── API tokens: minimum required permissions
    ├── never store OAuth tokens in project files
    ├── dedicated browser profile per account group
    ├── session tokens rotated monthly
    └── monitor for unauthorized login attempts
```

---

## repo evaluation framework (replacing the OpenClaw decision)

when selecting ANY repo, tool, or package for PRINTMAXX:

### tier 1: TRUSTED (use freely)
- official Anthropic tools (Claude Code, official MCP servers)
- official platform tools (npm, pip, brew, git)
- established tools by known orgs (Next.js/Vercel, Python standard library)
- tools we've used for 30+ days without incident

### tier 2: VETTED (use after checklist)
- popular open source with 1000+ stars AND active maintenance
- packages from verified npm/PyPI organizations
- tools recommended by trusted security researchers
- **MUST pass full repo vetting checklist (layer 1)**

### tier 3: SANDBOXED (test first, never in production directly)
- new or small packages (<100 stars)
- tools from individual developers
- anything involving browser automation with credentials
- **MUST run in Docker sandbox first, monitor with LuLu + fs_usage**

### tier 4: BLOCKED (never use)
- **ClawHub skills** (confirmed compromised — 1,184 malicious skills, AMOS stealer)
- OpenClaw core daemon pre-v2026.2.12 (unpatched CVEs)
- any package flagged by GuardDog or Socket.dev
- packages with preinstall/postinstall scripts we can't read
- repos with obfuscated code
- any tool that requires plaintext credential storage
- packages with typosquatting names (check carefully)
- packages recommended by AI that don't exist (slopsquatting — always verify on npm/PyPI FIRST)

### special case: OpenClaw core (model routing only)
- **tier 3 (SANDBOXED)** if ALL hardening conditions are met:
  - v2026.2.12+ only
  - Docker container, localhost-only binding
  - zero skills installed
  - monitored with LuLu + BlockBlock
  - monthly CVE review
- **tier 4 (BLOCKED)** if any condition is not met

---

## automated security scanning (add to cron)

```bash
# Daily at 4 AM: scan project dependencies for new CVEs
0 4 * * * cd $BASE && npm audit --json > AUTOMATIONS/logs/npm_audit_$(date +\%Y-\%m-\%d).json 2>&1
0 4 * * * cd $BASE && pip-audit --format json > AUTOMATIONS/logs/pip_audit_$(date +\%Y-\%m-\%d).json 2>&1

# Weekly Sunday 2 AM: full credential scan
0 2 * * 0 cd $BASE && trufflehog git file://. --only-verified --json > AUTOMATIONS/logs/trufflehog_$(date +\%Y-\%m-\%d).json 2>&1

# Weekly Sunday 3 AM: full malware scan
0 3 * * 0 cd $BASE && clamscan -r $BASE --infected --suppress-ok-results > AUTOMATIONS/logs/clamscan_$(date +\%Y-\%m-\%d).log 2>&1

# Before any new dependency install: auto-scan
# (add to .zshrc or project script)
safe_npm_install() {
  npm install --ignore-scripts "$@"
  guarddog npm scan node_modules/"$1" 2>/dev/null
  npm audit
  echo "Review results above. Run 'npm rebuild' to execute install scripts if clean."
}
```

---

## immediate action items (if approved)

| # | Action | Effort | Priority |
|---|--------|--------|----------|
| 1 | Install LuLu + BlockBlock + KnockKnock | 10 min | CRITICAL |
| 2 | Install envchain, move all API keys from .env to Keychain | 30 min | CRITICAL |
| 3 | Install Secretive for Secure Enclave SSH keys | 15 min | HIGH |
| 4 | Install trufflehog + guarddog + gitleaks | 10 min | HIGH |
| 5 | Run trufflehog on project repo (check for leaked secrets) | 5 min | CRITICAL |
| 6 | Enable FileVault if not already on | 5 min | CRITICAL |
| 7 | Audit all MCP servers in claude_desktop_config.json | 20 min | HIGH |
| 8 | Set up gitleaks pre-commit hook | 5 min | HIGH |
| 9 | Install Docker Desktop for sandboxing untrusted code | 10 min | MEDIUM |
| 10 | Add security scanning cron jobs | 15 min | MEDIUM |
| 11 | Move crypto wallet to hardware wallet / separate machine | varies | CRITICAL if holding crypto |
| 12 | 2FA on all social accounts (TOTP) | 30 min | HIGH |
| 13 | REMOVE OpenClaw from system proposal | 0 min (done) | CRITICAL |

**total setup time: ~2.5 hours for full security hardening.**
**total ongoing cost: $0 (all tools are free).**

---

## model routing options for second laptop

| Option | Pros | Cons | Security |
|--------|------|------|----------|
| **Claude Code + Codex CLI side-by-side (recommended)** | best of both, no gateway middleman, each vendor-controlled | manual switching between tools | HIGH — each controlled by its own vendor |
| **LiteLLM proxy (self-hosted)** | open source, multi-model routing, unified API, no marketplace risk | need to configure | MEDIUM-HIGH — no skill marketplace attack surface, small codebase to audit |
| **OpenClaw core (hardened, no skills)** | familiar if already used, same model routing | requires Docker + hardening, creator left project, ongoing CVE risk | MEDIUM — defensible with all 7 hardening conditions met |
| **OpenRouter (hosted)** | zero local attack surface, many models | another vendor dependency, API costs | MEDIUM — hosted service, trust their security |

**recommendation:** Claude Code on Laptop 1, Codex CLI on Laptop 2. if you want unified multi-model routing through one API, LiteLLM is the safest self-hosted option. OpenClaw core is usable but carries more risk for the same functionality.

---

*based on research from: OpenClaw security incidents (ClawHavoc, CVE-2026-25253 et al.), MCP ecosystem vulnerabilities (CVE-2025-6514, CVE-2025-49596, CVE-2025-52882), npm supply chain attacks (Shai-Hulud, s1ngularity), prompt injection research (EchoLeak, CometJacking, CurXecute), Kaspersky, Cisco, Bitsight, Sophos, CISA advisories, Objective-See tools, Docker sandboxing, envchain, Secretive, GuardDog, TruffleHog, Socket.dev, and Semgrep.*
