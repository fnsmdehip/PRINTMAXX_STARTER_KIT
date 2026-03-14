# REMOTE CONTROL DAISY CHAIN
# Sanitized carve-out candidate. No private keys, tokens, or PRINTMAXX business data.

## Purpose

Portable control stack for a personal Mac that combines:

- private agent control
- private browser access
- private terminal fallback
- optional full GUI remote desktop
- same-LAN emergency fallback

This is a control-plane pattern, not a PRINTMAXX-specific business system.

## Current PRINTMAXX State

- Verified 2026-03-13 03:14 EDT.
- Tailnet URL is live: `https://printmaxx-control.tail16dddb.ts.net`
- `tailscale serve status` currently shows that tailnet URL proxying `http://127.0.0.1:8790`
- Same-Wi-Fi fallback still exists on `http://192.168.1.172:8791`
- Full GUI fallback is installed via RustDesk, but unattended permissions/password still need manual completion on the Mac
- Private live snapshot lives in `~/.printmaxx_remote_access.json`
- On-demand doctor lives at `AUTOMATIONS/remote_access_status.py`

## Stack

1. `Tailscale` userspace daemon
2. `Tailscale SSH`
3. `Tailscale Serve` for localhost web apps
4. `CodeRelay` for Codex-oriented remote control
5. `RustDesk` for full desktop/app control
6. local-LAN relay fallback for same-Wi-Fi pairing when tailnet publishing is not ready

## Components

### Private transport

- userspace `tailscaled`
- persistent launch agent
- sync/watcher that:
  - detects login-needed state
  - configures `tailscale serve`
  - rewrites app public origins to MagicDNS URLs
  - restarts dependent services when origins change

### Agent/browser control

- localhost-only app
- tailnet-published via `tailscale serve`
- optional same-Wi-Fi TCP relay for first-run pairing

### Full desktop control

- optional remote desktop app launched at login
- requires host OS permissions for screen recording / accessibility
- not required for automation-first control, but required for “act like I am on the laptop”

## Security boundaries

- keep control-plane code separate from business logic
- never commit:
  - access tokens
  - tailnet identifiers tied to private infra
  - device IDs
  - generated passwords
  - customer/business data
- store live secrets in user-home files or secret managers, not in the repo

## Good open-source extraction boundary

Open-source:

- launch agents
- sync scripts
- localhost relay pattern
- remote-access doctor/status scripts
- service wiring
- docs/templates

Keep private:

- actual hostnames
- account emails
- tailnet names
- device IDs
- auth URLs
- credentials
- PRINTMAXX-specific automations and business state

## Candidate repo shape

```text
remote-control-daisy-chain/
├── launchd/
│   ├── com.tailscale.userspace.plist
│   ├── com.coderelay.lan-proxy.plist
│   ├── com.coderelay.tailscale-sync.plist
│   └── com.rustdesk.client.plist
├── scripts/
│   ├── coderelay_tailscale_sync.py
│   └── coderelay_lan_proxy.py
├── docs/
│   ├── architecture.md
│   ├── macos_setup.md
│   ├── iphone_setup.md
│   └── security.md
└── examples/
    └── remote_access_state.example.json
```

## In-Repo Extraction Staging

Current sanitized carve-out lives at:

- `OPEN_SOURCE/remote-control-daisy-chain/`

That folder is the split boundary for a future public repo. Keep it generic. Do not move PRINTMAXX business automations, credentials, queue state, private hostnames, or device IDs into it.

## Current recommendation

Use this as a three-layer fallback:

1. `CodeRelay` over `Tailscale Serve` for agent-native control
2. `Tailscale SSH` for terminal rescue / automation repair
3. `RustDesk` for full GUI/app control

That is the non-fragile version of “control everything from anywhere.”

## Remaining Human Gates

1. Install/login Tailscale on the iPhone so the tailnet URL resolves abroad.
2. Grant RustDesk macOS Screen Recording and Accessibility permissions.
3. If unattended GUI is required, finish RustDesk permanent password/service setup manually on the Mac.
