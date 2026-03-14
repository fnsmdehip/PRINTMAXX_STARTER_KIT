# macOS Setup

## Prereqs

- Homebrew
- `tailscale`
- a localhost web control app such as CodeRelay
- optional `RustDesk`

## Steps

1. Copy the `launchd` templates and replace `__HOME__` and `__REPO__`.
2. Load the userspace Tailscale launch agent.
3. Authenticate the node.
4. Enable `Tailscale Serve`.
5. Load the sync launch agent.
6. Validate with `scripts/remote_access_status.py`.

## Notes

- Keep the app itself loopback-bound.
- Publish the app privately via `Tailscale Serve` instead of rebinding it to `0.0.0.0`.
- Only add the LAN relay if you need first-run pairing from a phone on the same Wi-Fi.
