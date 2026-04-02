# Remote MacBook Setup Guide

How to turn a second MacBook into a remote dev machine you control from your main MacBook. Covers remote control, file transfer, and distributed LLM inference.

---

## Part 1: Remote Control

### Option A: Built-in Screen Sharing (Simplest, LAN only)

This is the fastest setup. Both Macs must be on the same Wi-Fi or wired network.

**On the remote Mac (the old one):**

```bash
# Enable Screen Sharing
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.screensharing.plist
```

Or go to: System Settings > General > Sharing > Screen Sharing > toggle ON.

Set "Allow access for" to your user account or "All users."

**From the main Mac:**

1. Open Finder > Go > Connect to Server (Cmd+K)
2. Type: `vnc://OLD-MAC-NAME.local` (or use the IP address: `vnc://192.168.x.x`)
3. Enter the remote Mac's username and password
4. Full mouse + keyboard control over the remote Mac

**Find the remote Mac's IP:**
```bash
# Run this on the remote Mac
ipconfig getifaddr en0    # Wi-Fi
ipconfig getifaddr en1    # Ethernet (if using Thunderbolt networking)
```

**Alternatively**, the remote Mac shows up automatically in Finder's sidebar under Network. Click it, then "Share Screen."

**Performance tips:**
- Wired Ethernet or Thunderbolt networking gives much better performance than Wi-Fi
- Close resource-heavy apps on both machines to reduce lag
- Screen Sharing uses VNC protocol under the hood

---

### Option B: SSH (CLI-only, lowest overhead)

Best for running Claude Code CLI, scripts, and terminal work without GUI overhead.

**On the remote Mac:**

```bash
# Enable SSH
sudo systemsetup -setremotelogin on
```

Or: System Settings > General > Sharing > Remote Login > toggle ON.

**From the main Mac:**

```bash
ssh username@OLD-MAC-NAME.local

# Or by IP
ssh username@192.168.1.50
```

**Set up key-based auth (no password prompts):**

```bash
# On your main Mac, generate a key if you don't have one
ssh-keygen -t ed25519

# Copy your public key to the remote Mac
ssh-copy-id username@OLD-MAC-NAME.local
```

Now `ssh username@OLD-MAC-NAME.local` logs in instantly.

**Run persistent sessions with tmux:**

```bash
# On the remote Mac (via SSH)
brew install tmux
tmux new -s claude

# Run Claude Code inside tmux
claude

# Detach: Ctrl+B, then D
# Reattach later:
tmux attach -t claude
```

This keeps Claude Code running even if your SSH connection drops.

---

### Option C: SSH + Screen Sharing combo

Use SSH for Claude Code CLI work. Use Screen Sharing only when you need the GUI (Simulator, browser, computer-use MCP).

```bash
# SSH for terminal work (fast, low bandwidth)
ssh username@OLD-MAC-NAME.local

# Screen Sharing for GUI work (open from main Mac)
open vnc://OLD-MAC-NAME.local
```

This is the recommended setup. SSH is instant, Screen Sharing is there when you need it.

---

### Option D: Tailscale (Remote access over the internet)

If you want to control the old MacBook from anywhere (not just your home network), Tailscale creates a private encrypted tunnel between your machines.

**On BOTH Macs:**

```bash
# Install Tailscale
brew install --cask tailscale
```

Or download from https://tailscale.com/download/mac (standalone version recommended over App Store).

1. Open Tailscale on both Macs
2. Sign in with the same account (Google, GitHub, Apple, etc.)
3. Both machines get a `100.x.x.x` IP on your private Tailscale network

**SSH over Tailscale:**

```bash
# Use the Tailscale hostname or IP
ssh username@old-macbook    # Tailscale hostname
ssh username@100.64.0.2     # Tailscale IP
```

**Screen Sharing over Tailscale:**

```bash
# From main Mac
open vnc://100.64.0.2
```

**Enable Tailscale SSH (optional, no keys needed):**

```bash
# On the remote Mac
tailscale up --ssh
```

This lets you SSH without managing keys at all. Tailscale handles auth via your identity provider.

**Why Tailscale over plain VPN:**
- Zero config, no port forwarding, no dynamic DNS
- Works through NAT, firewalls, cellular networks
- WireGuard-based, fast and encrypted
- Free for personal use (up to 100 devices)

---

### Option E: Other Tools

| Tool | Use case | Notes |
|------|----------|-------|
| Apple Remote Desktop ($80) | Multiple Mac management | Overkill for 2 machines |
| Chrome Remote Desktop | Free, works over internet | Needs Chrome, lower quality |
| AnyDesk / TeamViewer | Cross-platform | Free tier has limits |
| Screens 5 ($30) | Best Mac remote desktop UX | Supports Tailscale natively |

**Recommendation:** SSH + built-in Screen Sharing covers 95% of needs. Add Tailscale if you need internet access.

---

## Part 2: Transferring a ~31GB Project

### Speed comparison for 31GB

| Method | Speed | Time for 31GB | Setup effort |
|--------|-------|---------------|--------------|
| Thunderbolt cable (direct) | 600-2,800 MB/s | 11 sec - 1 min | Medium |
| rsync over Thunderbolt | 200-600 MB/s | 1-3 min | Medium |
| External SSD (USB-C 3.2) | 800-1,000 MB/s | 30-40 sec | Easy |
| rsync over Gigabit Ethernet | 100-110 MB/s | 5 min | Easy |
| rsync over Wi-Fi 6 | 30-80 MB/s | 7-17 min | Easy |
| AirDrop | 10-30 MB/s | 17-50 min | Easiest |
| Migration Assistant | Varies | 10-60 min | Easy (transfers everything) |
| git clone | N/A | Only tracked files | Bad for 31GB projects |

---

### Method 1: rsync over network (Recommended)

Best balance of speed, simplicity, and resumability. If it gets interrupted, rerun and it picks up where it left off.

**From your main Mac:**

```bash
# Basic transfer
rsync -avz --progress \
  /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ \
  username@OLD-MAC-NAME.local:/Users/username/Documents/p/PRINTMAXX_STARTER_KITttttt/

# Fast mode (skip compression, skip checksums - better on fast networks)
rsync -av --progress --whole-file \
  /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ \
  username@OLD-MAC-NAME.local:/Users/username/Documents/p/PRINTMAXX_STARTER_KITttttt/
```

**Exclude stuff you don't need:**

```bash
rsync -av --progress --whole-file \
  --exclude='node_modules' \
  --exclude='.expo' \
  --exclude='ios/build' \
  --exclude='android/build' \
  --exclude='.git/objects' \
  --exclude='*.log' \
  /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ \
  username@OLD-MAC-NAME.local:~/Documents/p/PRINTMAXX_STARTER_KITttttt/
```

Excluding `node_modules` and build artifacts could drop 31GB to 10-15GB.

**Speed tips:**
- Drop `-z` flag on fast connections (compression slows things down)
- Use `--whole-file` (skip delta calculations)
- Connect via Thunderbolt networking for fastest rsync speeds

---

### Method 2: Thunderbolt networking (Fastest wired option)

Connect two Macs directly with a Thunderbolt/USB-C cable and create a network bridge.

**Setup:**

1. Connect a Thunderbolt cable between both Macs
2. On both Macs: System Settings > Network
3. A "Thunderbolt Bridge" interface should appear automatically
4. Set to DHCP or configure manually:
   - Mac 1: IP `169.254.1.1`, Subnet `255.255.0.0`
   - Mac 2: IP `169.254.1.2`, Subnet `255.255.0.0`
5. Now use rsync or Finder to transfer files at ~600+ MB/s

```bash
# rsync over Thunderbolt bridge
rsync -av --progress --whole-file \
  /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ \
  username@169.254.1.2:~/Documents/p/PRINTMAXX_STARTER_KITttttt/
```

**Note:** You need a real Thunderbolt cable, not just any USB-C cable. Thunderbolt cables have the lightning bolt icon. A regular USB-C charging cable will not create a network bridge.

---

### Method 3: Share Disk mode (Apple Silicon replacement for Target Disk Mode)

Makes one Mac appear as an external drive to the other. Fast but requires booting into recovery.

**On the remote Mac (the one sharing its disk):**

1. Shut down the Mac completely
2. Press and hold the power button until "Loading startup options" appears
3. Click Options > Continue > enter password
4. In the macOS Utilities window: Utilities menu > Share Disk
5. Select the volume to share, click Start Sharing

**On the main Mac:**

1. The remote Mac appears in Finder sidebar
2. Click it, authenticate
3. Drag and drop files at near-disk speeds

**Downside:** The remote Mac is in recovery mode and not usable as a computer during transfer. Use rsync instead if you want both machines operational.

---

### Method 4: External SSD

The simple physical option. No network config needed.

1. Plug an external USB-C SSD into Mac 1
2. Copy the project folder to it
3. Unplug, plug into Mac 2
4. Copy to Mac 2

```bash
# Copy to external SSD
cp -R /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ /Volumes/MySSD/PRINTMAXX/

# Copy from SSD to new Mac
cp -R /Volumes/MySSD/PRINTMAXX/ ~/Documents/p/PRINTMAXX_STARTER_KITttttt/
```

A Samsung T7 or similar USB-C SSD does 800-1,000 MB/s. 31GB in about 35 seconds per copy (so ~70 seconds total).

---

### What NOT to use for 31GB

- **git clone**: Only gets tracked files. Won't include `node_modules`, `.env`, build artifacts, local data, or anything in `.gitignore`. You would still need rsync for the rest.
- **AirDrop**: Maxes out around 30 MB/s and can't resume if it fails. Painful for 31GB.
- **iCloud Drive**: Slow upload, not designed for dev projects, hidden files get mangled.

---

## Part 3: Setting Up Claude Code on the Remote Mac

Once files are transferred:

```bash
# SSH into the remote Mac
ssh username@OLD-MAC-NAME.local

# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js (required for Claude Code)
brew install node

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Copy your .env file if needed
# (do this from main Mac)
scp /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/.env \
  username@OLD-MAC-NAME.local:~/Documents/p/PRINTMAXX_STARTER_KITttttt/.env

# SSH in and start Claude Code
ssh username@OLD-MAC-NAME.local
cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt
tmux new -s claude
claude
```

**For computer-use MCP on the remote Mac:**

The remote Mac needs to be running its own display (lid open or connected to a monitor, or use headless display mode). Computer-use MCP takes screenshots of the remote Mac's actual screen.

```bash
# On the remote Mac, verify Screen Sharing is on
# Then from main Mac, use Screen Sharing to see what computer-use MCP sees

# To run computer-use MCP without a physical display:
# Plug in a dummy HDMI/USB-C display adapter, or use:
sudo defaults write /Library/Preferences/com.apple.windowserver DisplayResolutionEnabled -bool true
```

---

## Part 4: Distributed LLM Inference (Two Apple Silicon Macs)

### Can you share RAM/GPU between two MacBooks?

**Short answer:** You cannot directly share unified memory or GPU between two Macs. Each Mac's unified memory is physically part of its SoC. There is no hardware bus connecting them.

**What you CAN do:** Split a large model across two machines so each machine holds part of it. This is called distributed inference, and it works.

---

### Option A: Exo (Best option for two Macs)

Exo splits model layers across multiple devices using peer-to-peer networking. No master/worker setup, automatic device discovery, uses MLX backend on Apple Silicon.

**Install on BOTH Macs:**

```bash
# Install Python 3.12+ if needed
brew install python@3.12

# Install exo
pip3 install exo

# Or from source for latest features
git clone https://github.com/exo-explore/exo.git
cd exo
pip3 install -e .

# Optimize Apple Silicon GPU memory (run once)
# If configure_mlx.sh is included:
./configure_mlx.sh
```

**Run on BOTH Macs (same network):**

```bash
# On Mac 1
exo

# On Mac 2 (auto-discovers Mac 1)
exo
```

Exo automatically discovers the other node on the network. No config files needed.

**Use it:**

```bash
# Open the exo web UI (shown in terminal output)
# Or use the API:
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**What Exo gives you:**
- Two M1/M2/M3 MacBooks with 16GB each = 32GB combined for model loading
- Can run 70B parameter models that won't fit on a single 16GB machine
- Automatic model sharding based on each device's available memory
- MLX backend optimized for Apple Silicon
- OpenAI-compatible API endpoint

**Performance expectations:**
- Two MacBooks on Wi-Fi: works but slower due to network latency between layers
- Two MacBooks on Thunderbolt cable: much better, minimal inter-node latency
- Two MacBooks on Gigabit Ethernet: good middle ground
- Token generation speed depends on the slowest node

**Best setup for speed:**
Connect both Macs with a Thunderbolt cable (same cable used for file transfer), then run exo on both. The Thunderbolt bridge gives you ~40 Gbps between nodes.

---

### Option B: Ollama (Single machine only, no native distributed)

Ollama does not natively support splitting a model across multiple machines. One Ollama instance = one machine.

**What you CAN do with two Ollama instances:**
- Run different models on each machine (e.g., coding model on one, general model on the other)
- Use a load balancer to distribute requests across both

```bash
# Install on both Macs
brew install ollama

# Mac 1: run one model
ollama serve  # listens on localhost:11434
ollama run llama3.3

# Mac 2: run a different model
OLLAMA_HOST=0.0.0.0:11434 ollama serve
ollama run codellama
```

**Third-party distributed Ollama options:**
- **Hive** (github.com/hivellm) - proxy that distributes requests across multiple Ollama nodes
- **OLOL** - gRPC-based load balancer for multiple Ollama instances
- **LiteLLM** - can route requests across multiple Ollama backends

These distribute requests (send different prompts to different machines) but do NOT split a single model across machines. For model splitting, use Exo.

---

### Option C: llama.cpp distributed inference

llama.cpp supports RPC-based distributed inference where one machine is the main node and others contribute compute.

```bash
# Install llama.cpp on both Macs
brew install llama.cpp

# On the remote Mac (worker), start the RPC server:
llama-rpc-server --host 0.0.0.0 --port 50052

# On the main Mac, run inference with the remote worker:
llama-cli -m model.gguf \
  --rpc OLD-MAC-IP:50052 \
  -p "Hello, world"
```

This splits the model layers: some run locally, some run on the remote Mac via RPC. Less polished than Exo but more configurable.

---

### What's actually possible with two Apple Silicon MacBooks?

| Scenario | Feasible? | Tool |
|----------|-----------|------|
| Run a 70B model across two 16GB Macs | Yes | Exo, llama.cpp RPC |
| Run a 70B model on one 16GB Mac | No, not enough RAM | N/A |
| Share GPU compute for faster inference | Partially (model parallel, not data parallel) | Exo |
| Double inference speed by adding a second Mac | No. Adds capacity, not speed | N/A |
| Run different models on each Mac | Yes | Ollama on each |
| Combined memory pool (32GB from 2x16GB) | Effectively yes via model sharding | Exo |

**Key insight:** Adding a second Mac lets you run LARGER models (that need more RAM), but does not make SMALL models run faster. Network overhead between nodes means a model that fits on one Mac runs faster on one Mac than split across two.

---

## Quick Start Checklist

For the user's specific goal (old MacBook as remote dev machine):

### Initial setup (do once, ~30 minutes)

- [ ] **Enable Screen Sharing** on old Mac (System Settings > Sharing)
- [ ] **Enable SSH** on old Mac (System Settings > Sharing > Remote Login)
- [ ] **Set up SSH keys** (`ssh-copy-id` from main Mac)
- [ ] **Install Homebrew** on old Mac
- [ ] **Install Node.js** on old Mac (`brew install node`)
- [ ] **Install Claude Code** on old Mac (`npm install -g @anthropic-ai/claude-code`)
- [ ] **Install tmux** on old Mac (`brew install tmux`)
- [ ] **Optional:** Install Tailscale on both Macs for internet access

### Transfer project (do once, ~5 minutes)

```bash
rsync -av --progress --whole-file \
  --exclude='node_modules' --exclude='.expo' --exclude='ios/build' \
  /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ \
  username@OLD-MAC.local:~/Documents/p/PRINTMAXX_STARTER_KITttttt/
```

### Daily workflow

```bash
# SSH in and attach to tmux session
ssh username@OLD-MAC.local
tmux attach -t claude || tmux new -s claude
cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt
claude

# When you need the GUI (Simulator, browser, computer-use MCP):
# From main Mac:
open vnc://OLD-MAC.local
```

### Optional: distributed LLM inference

```bash
# Install exo on both Macs
pip3 install exo

# Run on both (same network, auto-discovers)
exo  # Mac 1
exo  # Mac 2

# Now you have a combined-memory AI cluster
# Access at http://localhost:8000
```

---

## Troubleshooting

**Screen Sharing won't connect:**
- Verify both Macs are on the same network: `ping OLD-MAC.local`
- Check firewall: System Settings > Network > Firewall > allow Screen Sharing
- Try IP address instead of .local hostname

**SSH connection refused:**
- Verify Remote Login is enabled on the remote Mac
- Check: `sudo systemsetup -getremotelogin` (should say "On")
- Verify firewall allows SSH (port 22)

**rsync is slow:**
- Drop the `-z` flag (compression hurts on fast networks)
- Add `--whole-file` flag
- Use Thunderbolt networking instead of Wi-Fi
- Exclude `node_modules` and build artifacts

**Exo nodes don't discover each other:**
- Both must be on the same subnet
- Check firewall isn't blocking mDNS/Bonjour
- Try manual connection: `exo --discovery-module manual --node-address OTHER_IP:PORT`

**Computer-use MCP on remote Mac shows black screen:**
- The remote Mac needs a display (physical or dummy adapter)
- Open the lid or connect a monitor/dummy HDMI plug
- Verify Screen Sharing shows the desktop before trying computer-use
