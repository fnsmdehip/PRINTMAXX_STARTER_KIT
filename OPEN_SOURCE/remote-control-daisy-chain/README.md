# Remote Control Daisy Chain

Sanitized control-plane bundle for running a Mac from anywhere with layered fallbacks:

1. `CodeRelay` over `Tailscale Serve` for agent-native control
2. `Tailscale SSH` for terminal rescue
3. `RustDesk` for full desktop and app control
4. optional LAN relay for first-run pairing or same-Wi-Fi recovery

This folder is intended as the public split boundary. It excludes business logic, credentials, private hostnames, tailnet names, device IDs, and revenue-system state.

## Layout

```text
remote-control-daisy-chain/
├── docs/
├── examples/
├── launchd/
└── scripts/
```

## Included

- generic `launchd` templates
- a userspace `tailscaled` pattern
- a `CodeRelay` + `Tailscale Serve` sync script
- a generic TCP LAN relay for localhost web apps
- a remote-access status snapshot script
- setup and security docs

## Deployment order

1. Start userspace Tailscale via launchd
2. Authenticate the node and enable `Tailscale Serve`
3. Start the sync loop so the local web app uses the MagicDNS URL as its public origin
4. Keep an SSH fallback live
5. Add RustDesk only if full GUI control is actually required

## Security boundary

Safe to publish:
- scripts
- templates
- docs
- example JSON state

Never publish:
- real `config.json` values
- auth tokens
- real `publicOrigin` values
- actual tailnet names or device IDs
- business-specific cron, queues, venture logic, or account data
