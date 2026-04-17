# iPHONE COMMAND CENTER
The ONE doc. Install these apps, tap these bookmarks, run the system from your couch.

---

## INSTALL THESE 7 APPS

| App | What it does | Free? |
|-----|-------------|-------|
| **Tailscale** | VPN mesh to your Mac (enables everything below) | Yes |
| **RustDesk** | Full screen mirror of Mac -- point, click, type | Yes |
| **GoLogin** | Manage anti-detect browser profiles + proxies | With subscription |
| **Publer** | Schedule posts to 9 platforms including TikTok | With subscription |
| **Termius** | SSH terminal to Mac (run any Python script) | Yes |
| **Telegram** | Two-way bot commands (/status, /health, /run) | Yes |
| **Ntfy** | Push notifications from your automations | Yes |

## ONE-TIME SETUP (15 min)

1. **Tailscale:** Open app, sign in. Note your Mac's IP (100.x.x.x).
2. **RustDesk:** Enter Mac's RustDesk ID + password. Test connection.
3. **Termius:** New host -> `100.x.x.x` (Tailscale IP), user `macbookpro`, port 22.
4. **Safari bookmark:** `http://100.x.x.x:9999` -- Add to Home Screen as "PRINTMAXX".
5. **GoLogin:** Sign in with same account as Mac app.
6. **Publer:** Sign in, verify all social accounts connected.

## DAILY OPS (from iPhone)

**Quick glance:** Open PRINTMAXX bookmark (home screen). See dashboard.

**Run a command:** Open Telegram -> message your bot:
```
/status    -- system health + alpha count
/health    -- loop status
/morning   -- fire the morning pipeline
/loops     -- are loops OK or dead?
/revenue   -- stripe balance
```

**Need full control:** Open RustDesk -> see Mac screen -> do anything.

**Schedule content:** Open Publer -> queue posts across all platforms.

**Manage accounts:** Open GoLogin -> see all browser profiles + proxy status.

**Run a script:** Open Termius -> SSH in:
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
python3 AUTOMATIONS/decision_engine.py --cycle
```

## THAT'S IT

Everything else is reference. The 4 big docs are for when you want to expand:
- `COMPLETE_SOCIAL_INFRA_STACK.md` -- all tools compared, budget tiers
- `MOBILE_CONTROL_PLAYBOOK.md` -- detailed setup for each option
- `MASTER_LAUNCH_PLAYBOOK.md` -- full execution sequence
- `ANTIDETECT_BROWSER_MARKET_COMPARISON_2026.md` -- browser deep dive
