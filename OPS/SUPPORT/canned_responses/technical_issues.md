# Technical issues - Canned responses

---

## 1. App crashing on launch

**Use when:** App won't open or crashes immediately.

---

Hi [NAME],

Try this:
1. Force quit the app completely
2. Restart your device
3. Open the app again

If still crashing, delete and reinstall. Your data syncs from the cloud, nothing lost.

Still broken after that? Send me your device model and OS version.

- [AGENT]

---

## 2. Login issues - Wrong password

**Use when:** Customer can't log in, likely password issue.

---

Hi [NAME],

Reset your password here: [RESET LINK]

Check your spam folder if you don't see the email in 2 minutes.

Once reset, try logging in again. If you see "account not found," you might have signed up with a different email.

- [AGENT]

---

## 3. Login issues - Social login not working

**Use when:** Google/Apple sign-in failing.

---

Hi [NAME],

Social login can be finicky. Try these:
1. Clear your browser cache
2. Try incognito/private mode
3. Make sure you're using the same provider (Google/Apple) you originally signed up with

If you originally used email/password but are trying Google now, those are separate accounts. Use email login instead.

- [AGENT]

---

## 4. Sync not working

**Use when:** Data not syncing between devices.

---

Hi [NAME],

Force a sync:
1. Pull down on the main screen (mobile) or hit Cmd+R (desktop)
2. Wait 10 seconds
3. Check the other device

If still not syncing:
- Both devices on same account? Check Settings > Account
- Both devices online?
- App updated to latest version?

Send me screenshots of Settings > Account from both devices if stuck.

- [AGENT]

---

## 5. Feature missing after update

**Use when:** Customer can't find a feature they used before.

---

Hi [NAME],

That feature moved. It's now in [NEW LOCATION].

We reorganized the menu in [VERSION] to group related features together. Takes a minute to adjust but most people find things faster once they know where to look.

Full changelog here: [LINK]

- [AGENT]

---

## 6. Slow performance

**Use when:** App running slowly.

---

Hi [NAME],

Few things to try:
1. Close other apps eating memory
2. Clear app cache: Settings > Advanced > Clear Cache
3. Check your internet speed at fast.com

If you have [LARGE DATASET - e.g., 10,000+ items], performance can drop. Archive old data you don't need daily.

Still slow? Tell me what specifically is slow (loading, searching, saving?) and I'll dig into logs.

- [AGENT]

---

## 7. Data not saving

**Use when:** Changes aren't persisting.

---

Hi [NAME],

Are you seeing an error when saving, or does it look like it saves but the data disappears?

If no error: Check your internet connection. The app needs connectivity to save.

If error message: Screenshot it and send over. That tells me exactly what's failing.

In the meantime, avoid closing the app until this is fixed. Your unsaved changes might still be in memory.

- [AGENT]

---

## 8. Export not working

**Use when:** Can't download/export data.

---

Hi [NAME],

Export should work now. I just regenerated it on our end.

Try again: [EXPORT STEPS]

If it fails again, check:
- Pop-up blocker disabled for our site?
- Enough storage space on your device?
- Download folder full?

For large exports (>10MB), it can take a few minutes. Don't refresh the page while it's processing.

- [AGENT]

---

## 9. Notifications not working - iOS

**Use when:** Push notifications not appearing on iPhone/iPad.

---

Hi [NAME],

Check these settings:
1. Settings > Notifications > [APP NAME] > Allow Notifications ON
2. Settings > [APP NAME] > Notifications > make sure not set to "Off"
3. Settings > Focus > make sure app isn't blocked during Focus modes

Inside the app: Settings > Notifications > toggle off and on again.

Still nothing? Delete and reinstall the app, then say "Allow" when it asks for notification permission.

- [AGENT]

---

## 10. Notifications not working - Android

**Use when:** Push notifications not appearing on Android.

---

Hi [NAME],

Check these:
1. Settings > Apps > [APP NAME] > Notifications > ON
2. Settings > Apps > [APP NAME] > Battery > not set to "Restricted"
3. Settings > Battery > Battery Saver OFF (or add app exception)

Some Android skins (Samsung, Xiaomi) aggressively kill background apps. Search "[YOUR PHONE] keep app running in background" for phone-specific fixes.

- [AGENT]

---

## 11. Can't upload file

**Use when:** File upload failing.

---

Hi [NAME],

What file type and size?

Limits:
- Max file size: [X] MB
- Supported formats: [LIST]

If within limits, try:
1. Different browser (Chrome works best)
2. Smaller file
3. Rename file to remove special characters

If it's a large file, our uploader shows a progress bar. Wait for it to complete before navigating away.

- [AGENT]

---

## 12. Integration not connecting

**Use when:** Third-party integration failing to authorize.

---

Hi [NAME],

Disconnect and reconnect:
1. Settings > Integrations > [SERVICE] > Disconnect
2. Wait 30 seconds
3. Click Connect and re-authorize

Make sure:
- You're logged into the correct [SERVICE] account in your browser
- Pop-ups aren't blocked
- You click "Allow" on all permission screens

If [SERVICE] shows as connected but data isn't flowing, there might be a permissions issue on their end. Try revoking access in [SERVICE]'s settings, then reconnect from our app.

- [AGENT]

---

## 13. Search not finding results

**Use when:** Search returns nothing or wrong results.

---

Hi [NAME],

Search looks at [FIELDS IT SEARCHES]. It doesn't search [FIELDS IT DOESN'T].

Try:
- Fewer words (search is exact match by default)
- Check spelling
- Remove filters if any are active

If you know the item exists, send me what you're searching for and I'll look up why it's not appearing.

- [AGENT]

---

## 14. Blank screen / white screen

**Use when:** App shows blank white or black screen.

---

Hi [NAME],

Blank screen usually means something failed to load. Try:

Web:
1. Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
2. Clear browser cache
3. Try incognito mode
4. Try different browser

Mobile:
1. Force quit and reopen
2. Toggle airplane mode on/off
3. Delete and reinstall

If still blank, open browser console (F12 > Console) and screenshot any red errors.

- [AGENT]

---

## 15. Bug report acknowledgment

**Use when:** Customer reports a bug you can reproduce.

---

Hi [NAME],

Confirmed. I reproduced this on my end.

What's happening: [BRIEF TECHNICAL EXPLANATION]

We're fixing it. No ETA yet, but I'll email you when it's deployed.

Workaround for now: [WORKAROUND IF ANY]

Thanks for the detailed report. Screenshots helped a lot.

- [AGENT]
