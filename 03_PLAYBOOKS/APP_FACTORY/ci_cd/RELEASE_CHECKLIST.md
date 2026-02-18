# Release Checklist

Complete checklist for releasing iOS and Android apps to production.

## Table of contents

1. [Pre-release checks](#pre-release-checks)
2. [Version bump](#version-bump)
3. [Build verification](#build-verification)
4. [Store submission](#store-submission)
5. [Post-release monitoring](#post-release-monitoring)
6. [Rollback procedure](#rollback-procedure)

---

## Pre-release checks

### Code quality

- [ ] All PRs merged and approved
- [ ] No open critical/high-priority bugs
- [ ] Code review completed for all changes
- [ ] Technical debt addressed (or documented for next release)

### Testing

- [ ] Unit tests passing (100% on CI)
- [ ] Integration tests passing
- [ ] UI/E2E tests passing
- [ ] Manual QA completed on staging
- [ ] Performance testing completed
- [ ] Accessibility testing completed

### Staging verification

- [ ] Staging build deployed and tested
- [ ] All new features verified working
- [ ] Regression testing completed
- [ ] Edge cases tested (offline, poor network, etc.)
- [ ] Different device sizes tested

### Security

- [ ] No hardcoded secrets in codebase
- [ ] Dependencies scanned for vulnerabilities
- [ ] SSL pinning verified (if applicable)
- [ ] Sensitive data encryption verified
- [ ] Authentication flows tested

### Compliance

- [ ] FTC disclosures in place (if affiliate links)
- [ ] Privacy policy up to date
- [ ] Terms of service current
- [ ] GDPR compliance verified (EU users)
- [ ] App Store/Play Store guidelines reviewed

---

## Version bump

### Semantic versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes, significant UI overhaul
- **MINOR**: New features, non-breaking changes
- **PATCH**: Bug fixes, small improvements

### Version bump steps

1. **Determine version type**
   ```bash
   # Review changes since last release
   git log --oneline v1.2.3..HEAD
   ```

2. **Bump version**
   ```bash
   # Use the bump script
   ./ci_cd/scripts/bump_version.sh patch --commit

   # Or manually with Fastlane
   cd ios && bundle exec fastlane bump_version type:patch
   cd android && bundle exec fastlane bump_version type:patch
   ```

3. **Verify version updated**
   - [ ] iOS: Check Info.plist
   - [ ] Android: Check build.gradle
   - [ ] Both: Build number incremented

4. **Update changelog**
   - [ ] CHANGELOG.md updated with new version
   - [ ] Release notes drafted for stores
   - [ ] Breaking changes documented

### Version checklist

- [ ] Version bumped: `____.____.____`
- [ ] iOS build number: `____`
- [ ] Android version code: `____`
- [ ] Changelog updated
- [ ] Release notes prepared

---

## Build verification

### iOS build

1. **Build release**
   ```bash
   cd ios
   bundle exec fastlane ios build_release
   ```

2. **Verify build**
   - [ ] IPA created successfully
   - [ ] dSYMs generated for crash reporting
   - [ ] No compiler warnings
   - [ ] Bundle size within limits (< 200MB)

3. **Test on device**
   - [ ] Install via Ad Hoc or TestFlight
   - [ ] Launch and basic functionality works
   - [ ] No crashes on startup
   - [ ] In-app purchases work (sandbox)

### Android build

1. **Build release**
   ```bash
   cd android
   bundle exec fastlane android build_release
   ```

2. **Verify build**
   - [ ] AAB created successfully
   - [ ] ProGuard/R8 mapping generated
   - [ ] No lint errors
   - [ ] APK size within limits (< 150MB)

3. **Test on device**
   - [ ] Install APK on test device
   - [ ] Launch and basic functionality works
   - [ ] No crashes on startup
   - [ ] In-app purchases work (sandbox)

### Build artifacts checklist

- [ ] iOS IPA created: `build/App-Release.ipa`
- [ ] iOS dSYM created: `build/App.app.dSYM.zip`
- [ ] Android AAB created: `app/build/outputs/bundle/release/*.aab`
- [ ] Android mapping: `app/build/outputs/mapping/release/mapping.txt`
- [ ] All artifacts backed up

---

## Store submission

### iOS - App Store Connect

1. **Upload to TestFlight**
   ```bash
   cd ios
   bundle exec fastlane ios deploy_testflight
   ```

2. **TestFlight testing**
   - [ ] Build processing complete
   - [ ] Internal testers notified
   - [ ] Internal testing passed (24-48 hours minimum)
   - [ ] External testers invited (optional)
   - [ ] External testing passed

3. **Submit for review**
   - [ ] App version created in App Store Connect
   - [ ] Screenshots current and accurate
   - [ ] App description updated
   - [ ] Keywords optimized
   - [ ] What's New text added
   - [ ] Review notes provided (if needed)
   - [ ] Privacy questionnaire completed
   - [ ] Export compliance answered
   - [ ] Submit for review

4. **Review monitoring**
   - [ ] Monitor for review feedback
   - [ ] Respond to any questions within 24 hours
   - [ ] Fix any rejection issues promptly

### Android - Play Store

1. **Upload to internal track**
   ```bash
   cd android
   bundle exec fastlane android deploy_play_store track:internal
   ```

2. **Internal testing**
   - [ ] Build available in Play Store
   - [ ] Internal testers notified
   - [ ] Internal testing passed
   - [ ] Pre-launch report reviewed

3. **Promote through tracks**
   ```bash
   # Promote to closed testing (alpha/beta)
   bundle exec fastlane android promote from:internal to:beta

   # After beta testing, promote to production
   bundle exec fastlane android promote from:beta to:production
   ```

4. **Production release**
   - [ ] Store listing current
   - [ ] Screenshots accurate
   - [ ] Feature graphic updated
   - [ ] What's New text added
   - [ ] Content rating current
   - [ ] Privacy policy linked
   - [ ] Staged rollout configured (10% -> 50% -> 100%)

### Store submission checklist

**iOS:**
- [ ] TestFlight build uploaded
- [ ] TestFlight testing complete
- [ ] App Store listing updated
- [ ] Submitted for review
- [ ] Review approved
- [ ] Released to App Store

**Android:**
- [ ] Internal track upload complete
- [ ] Internal testing passed
- [ ] Beta track promotion (optional)
- [ ] Production track release
- [ ] Staged rollout configured

---

## Post-release monitoring

### First 24 hours (critical)

- [ ] Monitor crash reports (Crashlytics/Sentry)
- [ ] Check analytics for anomalies
- [ ] Monitor app store reviews
- [ ] Watch social media for feedback
- [ ] Check support tickets

### First week

- [ ] Crash rate acceptable (< 1%)
- [ ] User ratings stable or improving
- [ ] No major bugs reported
- [ ] Performance metrics normal
- [ ] Revenue/conversions tracking correctly

### Metrics to watch

| Metric | Threshold | Action if exceeded |
|--------|-----------|-------------------|
| Crash rate | > 1% | Consider rollback |
| ANR rate (Android) | > 0.5% | Investigate immediately |
| 1-star reviews | Spike > 3x normal | Respond and investigate |
| Uninstall rate | > 10% increase | Investigate UX changes |
| API error rate | > 5% | Check backend health |

### Monitoring dashboard checklist

- [ ] Crashlytics/Sentry dashboard open
- [ ] Analytics dashboard open
- [ ] App Store Connect/Play Console open
- [ ] Support queue monitored
- [ ] Slack alerts configured

---

## Rollback procedure

### When to rollback

- Crash rate > 2% affecting core functionality
- Critical security vulnerability discovered
- Data loss or corruption reported
- Widespread user-blocking bugs

### iOS rollback

1. **Remove from sale (temporary)**
   - Go to App Store Connect > App > Pricing and Availability
   - Remove from sale while investigating

2. **Expedited review**
   - Fix the issue
   - Submit new build
   - Request expedited review (explain production issue)

3. **Revert to previous version** (not possible on iOS)
   - Must submit a new build with the fix
   - Can take 24-48 hours for review

### Android rollback

1. **Halt staged rollout**
   ```bash
   # In Play Console: Release > Production > Halt rollout
   ```

2. **Rollback to previous version**
   - Play Console > Release > Production > Release history
   - Select previous working version
   - Rollback

3. **Fix and re-release**
   - Fix the issue
   - Test thoroughly
   - Start new staged rollout

### Rollback checklist

- [ ] Incident documented
- [ ] Root cause identified
- [ ] Rollback executed
- [ ] Users notified (if appropriate)
- [ ] Fix developed and tested
- [ ] Post-mortem scheduled

---

## Quick reference

### Release commands

```bash
# Version bump
./ci_cd/scripts/bump_version.sh patch --commit

# iOS release
cd ios && bundle exec fastlane ios deploy_testflight

# Android release
cd android && bundle exec fastlane android deploy_play_store track:internal

# Promote Android
cd android && bundle exec fastlane android promote from:internal to:production
```

### Emergency contacts

| Role | Name | Contact |
|------|------|---------|
| Engineering Lead | [Name] | [Contact] |
| QA Lead | [Name] | [Contact] |
| Support Lead | [Name] | [Contact] |
| Apple Developer Relations | - | https://developer.apple.com/contact/ |
| Google Play Support | - | https://support.google.com/googleplay/android-developer/ |

### Useful links

- [App Store Connect](https://appstoreconnect.apple.com)
- [Google Play Console](https://play.google.com/console)
- [Crashlytics Dashboard](https://console.firebase.google.com)
- [Sentry Dashboard](https://sentry.io)

---

## Release sign-off

**Release version:** `____.____.____`

**Sign-offs:**
- [ ] Engineering: _________________ Date: _______
- [ ] QA: _________________ Date: _______
- [ ] Product: _________________ Date: _______

**Release approved:** Yes / No

**Notes:**
```
[Any notes about the release]
```
