# Troubleshooting: Notification issues

**Symptoms:** Push notifications not arriving, notifications delayed, notification settings not saving, too many notifications.

---

## Quick diagnosis

Ask the customer:
1. Device and OS version?
2. What notifications are you expecting? (Which type/trigger)
3. Did notifications ever work, or never?
4. Any recent changes? (OS update, app update, new phone)

---

## Notifications never worked

### iOS

**Step 1: Check system settings**
1. Settings > Notifications > [App Name]
2. Verify "Allow Notifications" is ON
3. Check: Alerts, Sounds, Badges all enabled
4. Lock Screen, Notification Center, Banners all checked

**Step 2: Check in-app settings**
1. Open app > Settings > Notifications
2. Verify notifications enabled in app
3. Check specific notification types are on

**Step 3: Permission was denied on first launch**
If customer tapped "Don't Allow" on first launch:
1. Settings > [App Name] > Notifications
2. Toggle ON
3. If grayed out: Delete app, reinstall, tap "Allow" this time

### Android

**Step 1: Check system settings**
1. Settings > Apps > [App Name] > Notifications
2. Verify "All notifications" is ON
3. Check individual notification channels if available

**Step 2: Check battery optimization**
1. Settings > Apps > [App Name] > Battery
2. Set to "Unrestricted" or "No restrictions"
3. NOT "Optimized" or "Restricted"

**Step 3: Check Do Not Disturb**
1. Settings > Sound > Do Not Disturb
2. Verify our app isn't blocked
3. Or add app to exceptions

**Step 4: Manufacturer-specific issues**
Some phones aggressively kill background apps:

- **Samsung:** Settings > Device Care > Battery > [App] > Allow background activity
- **Xiaomi:** Settings > Apps > Manage Apps > [App] > Autostart ON
- **Huawei:** Settings > Battery > App launch > [App] > Manage manually > all toggles ON
- **OnePlus:** Settings > Battery > Battery optimization > [App] > Don't optimize

Search: "[Phone brand] keep app running in background"

---

## Notifications stopped working

### What changed?

**After OS update:**
- OS updates can reset notification permissions
- Re-enable in Settings > Notifications > [App]
- Reinstall app if still not working

**After app update:**
- New notification channels might be disabled by default
- Check in-app notification settings
- Enable any new categories

**After getting new phone:**
- Permissions don't transfer automatically
- Set up notifications fresh
- Check all settings from "never worked" section

### Token expired

Push notification tokens can expire:
1. Log out of app completely
2. Log back in
3. This refreshes the push token

---

## Notifications delayed

Push notifications can be delayed by:

### Device-side delays
- Battery saver mode (batches notifications)
- Do Not Disturb (holds until schedule ends)
- Low power mode
- Background refresh disabled

### Network delays
- Poor internet connection
- Notifications queue on server until device reconnects

### Server-side delays (rare)
- Check status.example.com for incidents
- High volume can cause delays during peak times

---

## Too many notifications

Customer wants fewer notifications:

### In-app controls
1. Settings > Notifications
2. Toggle off categories they don't want
3. Common categories to turn off:
   - Marketing/promotional
   - Activity from others
   - Weekly digest

### System-level controls
Can't reduce specific types? System level helps:
- iOS: Settings > Notifications > [App] > Notification Grouping
- Android: Settings > Apps > [App] > Notifications > disable specific channels

---

## Notification settings not saving

**Issue:** Customer changes settings but they revert.

**Causes:**
1. Network issue (setting didn't sync)
2. Logged into different account on web vs mobile
3. Bug in settings sync

**Fixes:**
1. Make change, wait 10 seconds, force close app, reopen
2. Make change on web while mobile is closed (or vice versa)
3. If keeps reverting: clear cache, reinstall

---

## Debug checklist

Run through this before escalating:

**iOS**
- [ ] Settings > Notifications > [App] > Allow Notifications ON
- [ ] All notification styles enabled (Alerts, Sounds, Badges)
- [ ] Focus modes not blocking app
- [ ] In-app notification settings ON
- [ ] Not in Low Power Mode
- [ ] App is up to date

**Android**
- [ ] Settings > Apps > [App] > Notifications ON
- [ ] Battery optimization disabled for app
- [ ] Autostart enabled (if available on device)
- [ ] Do Not Disturb not blocking
- [ ] In-app notification settings ON
- [ ] Data saver not blocking background data
- [ ] App is up to date

---

## Escalation criteria

Escalate to engineering when:
- Multiple users report no notifications simultaneously
- Push service status shows issues
- User followed all steps, still no notifications, other apps work fine
- Notification token not registering in backend logs

Include:
- User ID
- Device model and OS version
- What was tried
- Whether it ever worked
- Push token status from admin dashboard (if accessible)

---

## Quick reference

| Platform | Most common cause | First fix |
|----------|-------------------|-----------|
| iOS | Permission denied on first launch | Settings > [App] > Notifications |
| Android | Battery optimization | Disable battery saver for app |
| Both | OS or app update reset settings | Re-enable notifications |
| Both | Delayed notifications | Check battery saver/DND |
