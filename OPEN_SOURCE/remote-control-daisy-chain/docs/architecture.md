# Architecture

## Control order

1. `Tailscale Serve` publishes a localhost web app privately to the tailnet.
2. `CodeRelay` provides agent/browser control against that localhost app.
3. `Tailscale SSH` remains the repair path if the web surface breaks.
4. `RustDesk` is optional and only needed when native app clicks or full desktop interaction are required.
5. A local TCP relay can be kept around for same-Wi-Fi bootstrap or recovery.

## Why userspace Tailscale

Userspace `tailscaled` avoids the system-extension and root-daemon path. That is useful when you want a private transport without mutating system networking more than necessary.

## Failure model

- If `CodeRelay` breaks, use `Tailscale SSH`.
- If `Serve` breaks, hit the localhost app over SSH port forwarding or re-run the sync script.
- If a native Mac app needs clicks, use RustDesk.
- If tailnet publishing is not ready yet, use the LAN relay temporarily.
