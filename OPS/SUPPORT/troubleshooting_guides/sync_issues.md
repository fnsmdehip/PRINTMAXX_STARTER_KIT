# Troubleshooting: Sync issues

**Symptoms:** Data not appearing on other devices, changes not saving, old version of data showing, "sync failed" errors.

---

## Quick diagnosis

Ask the customer:
1. Which devices are you syncing between?
2. Are you logged into the same account on both?
3. What data isn't syncing? (Everything or specific items)
4. Are you seeing any error messages?

---

## Step 1: Verify same account

Most common cause: **Different accounts on different devices.**

Check on each device:
- Settings > Account
- Note the email address displayed

If emails don't match:
- Log out of wrong account
- Log into correct account
- Data should appear

---

## Step 2: Force manual sync

### Mobile
1. Pull down on main screen (triggers refresh)
2. Wait 10 seconds
3. Check if data updated

### Desktop/Web
1. Press Cmd+R (Mac) or Ctrl+R (Windows)
2. Or click sync icon if visible
3. Wait for sync indicator to complete

### If no sync indicator
- Check bottom right corner for sync status
- "Last synced: [time]" should update
- If stuck, try Step 3

---

## Step 3: Check connectivity

Sync requires internet. Test:

1. Open browser, load google.com
2. If that fails, it's a network issue

Network fixes:
- Toggle wifi off and on
- Switch from wifi to cellular (or vice versa)
- Restart router
- Try different network

---

## Step 4: Clear sync queue

Sometimes sync gets stuck on a bad item.

### Clear cache
1. Settings > Advanced > Clear Cache
2. This doesn't delete data, just cached copies
3. App will re-download from server

### Log out and back in
1. Settings > Account > Log Out
2. Close app completely
3. Reopen and log in
4. Let initial sync complete (can take minutes for large accounts)

---

## Step 5: Conflict resolution

When same item edited on two devices while offline:

**How we handle it:**
- Last edit wins (by timestamp)
- No automatic merging of conflicts

**If customer lost data:**
- Check version history: [Item] > History > View Previous Versions
- Some item types have 30-day history
- Can restore previous version

---

## Specific sync scenarios

### New device not showing old data
1. Verify same account login
2. Wait 5-10 minutes for initial sync
3. Don't create new content until sync completes
4. If still empty after 10 minutes: log out, reinstall, log in

### Desktop changes not on mobile
1. Ensure desktop app is open and online when saving
2. Look for sync indicator confirming upload
3. Then check mobile
4. If desktop sync indicator shows error, troubleshoot desktop first

### Mobile changes not on desktop
1. Mobile syncs when connected and app in foreground
2. Keep app open for 30 seconds after making changes
3. Check cellular data permissions for app
4. Background sync may be disabled in device settings

### Offline changes lost
If device was offline and changes disappeared:
1. Check if they logged out while offline (logs out = loses unsaved)
2. Check if app was deleted while offline
3. Unfortunately, offline changes not synced are not recoverable

---

## Step 6: Advanced troubleshooting

### Check server status
Before deep debugging: status.example.com
If degraded, wait for resolution.

### Enable sync debugging (internal)
1. Admin > Users > [User ID]
2. View sync log
3. Look for failed items or error codes

Common error codes:
- 409: Conflict (two devices edited same item)
- 413: Item too large
- 500: Server error (escalate)
- 503: Server overloaded (wait and retry)

---

## Escalation criteria

Escalate to engineering when:
- Multiple users report sync issues simultaneously (possible backend problem)
- User sees 500/503 errors repeatedly
- Sync log shows items stuck in queue for >1 hour
- Data corruption suspected (items garbled, not just missing)

Include:
- User ID
- Devices and OS versions
- Sync log excerpt
- When issue started

---

## Quick reference

| Symptom | Most likely cause | First fix |
|---------|-------------------|-----------|
| Nothing syncing | Different accounts | Verify same email on both devices |
| Slow sync | Large account | Wait, or archive old content |
| Some items missing | Sync queue stuck | Clear cache |
| Sync error message | Network or server | Check status page, try later |
| Data disappeared | Logged out offline | Not recoverable, sorry |
