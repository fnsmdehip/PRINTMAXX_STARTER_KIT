# CI/CD Setup Guide

Complete setup guide for GitHub Actions and Fastlane deployment pipelines.

## Table of contents

1. [Prerequisites](#prerequisites)
2. [GitHub Actions setup](#github-actions-setup)
3. [Fastlane installation](#fastlane-installation)
4. [iOS code signing setup](#ios-code-signing-setup)
5. [Android signing setup](#android-signing-setup)
6. [Secrets configuration](#secrets-configuration)
7. [Environment variables](#environment-variables)
8. [Testing the pipeline](#testing-the-pipeline)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- [ ] Apple Developer account ($99/year)
- [ ] Google Play Console account ($25 one-time)
- [ ] GitHub repository with Actions enabled
- [ ] Ruby 3.0+ installed locally
- [ ] Xcode 15+ installed (for iOS)
- [ ] Android Studio with SDK (for Android)

---

## GitHub Actions setup

### 1. Copy workflow files

Copy the workflow files to your repository:

```bash
mkdir -p .github/workflows

cp ci_cd/github_actions/*.yml .github/workflows/
```

### 2. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click Settings > Actions > General
3. Select "Allow all actions and reusable workflows"
4. Save

### 3. Configure branch protection (recommended)

1. Go to Settings > Branches
2. Add rule for `main` branch
3. Enable:
   - Require status checks to pass
   - Require branches to be up to date
   - Select the CI workflows as required checks

---

## Fastlane installation

### Local installation

```bash
# Install Ruby (if not using system Ruby)
brew install ruby

# Install Fastlane
gem install fastlane

# Or use Bundler (recommended)
cd ios  # or android
bundle init
echo "gem 'fastlane'" >> Gemfile
bundle install
```

### Project setup

```bash
# Copy Fastlane files
mkdir -p ios/fastlane android/fastlane

cp ci_cd/fastlane/Fastfile fastlane/
cp ci_cd/fastlane/Appfile fastlane/
cp ci_cd/fastlane/Matchfile fastlane/
cp ci_cd/fastlane/ios/Fastfile ios/fastlane/
cp ci_cd/fastlane/android/Fastfile android/fastlane/

# Create Gemfile for each platform
cat > ios/Gemfile << 'EOF'
source "https://rubygems.org"

gem "fastlane"
gem "cocoapods"

plugins_path = File.join(File.dirname(__FILE__), 'fastlane', 'Pluginfile')
eval_gemfile(plugins_path) if File.exist?(plugins_path)
EOF

cat > android/Gemfile << 'EOF'
source "https://rubygems.org"

gem "fastlane"

plugins_path = File.join(File.dirname(__FILE__), 'fastlane', 'Pluginfile')
eval_gemfile(plugins_path) if File.exist?(plugins_path)
EOF

# Install dependencies
cd ios && bundle install
cd ../android && bundle install
```

---

## iOS code signing setup

### Option 1: Match (recommended)

Match stores certificates in a private Git repo, syncing them across your team and CI.

#### 1. Create certificates repository

```bash
# Create a new private repo on GitHub called "certificates"
# Example: github.com/yourcompany/certificates
```

#### 2. Initialize Match

```bash
cd ios
bundle exec fastlane match init

# Choose "git" storage
# Enter your certificates repo URL
```

#### 3. Generate certificates

```bash
# Development certificates
bundle exec fastlane match development

# App Store certificates
bundle exec fastlane match appstore

# Ad-hoc certificates (for TestFlight external testing)
bundle exec fastlane match adhoc
```

#### 4. CI setup for Match

Generate a deploy key for the certificates repo:

```bash
ssh-keygen -t ed25519 -C "ci@yourcompany.com" -f match_deploy_key
```

1. Add the public key as a deploy key in your certificates repo (Settings > Deploy keys)
2. Add the private key as a secret `MATCH_DEPLOY_KEY` in your app repo

### Option 2: Manual signing

If not using Match, manually export certificates:

1. In Xcode, go to Preferences > Accounts
2. Select your team, click "Manage Certificates"
3. Export the certificate as a .p12 file
4. Base64 encode it: `base64 -i certificate.p12 | pbcopy`
5. Add as secret `IOS_CERTIFICATE_BASE64`

---

## Android signing setup

### 1. Generate release keystore

```bash
keytool -genkey -v -keystore release-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key \
  -storepass YOUR_STORE_PASSWORD \
  -keypass YOUR_KEY_PASSWORD
```

**Important:** Store passwords securely. You cannot recover them.

### 2. Base64 encode keystore

```bash
base64 -i release-keystore.jks | pbcopy
```

Add this as secret `ANDROID_KEYSTORE_BASE64`

### 3. Create Play Store service account

1. Go to Google Play Console
2. Settings > API access
3. Create a service account
4. Grant "Release manager" permission
5. Download the JSON key file
6. Base64 encode: `base64 -i service-account.json | pbcopy`
7. Add as secret `PLAY_STORE_SERVICE_ACCOUNT_JSON`

---

## Secrets configuration

Add these secrets in GitHub (Settings > Secrets and variables > Actions):

### iOS secrets

| Secret | Description |
|--------|-------------|
| `APPLE_TEAM_ID` | Your 10-digit Apple Team ID |
| `APPLE_ID` | Apple ID email for App Store Connect |
| `APP_STORE_CONNECT_API_KEY_ID` | API key ID from App Store Connect |
| `APP_STORE_CONNECT_ISSUER_ID` | Issuer ID from App Store Connect |
| `APP_STORE_CONNECT_API_KEY` | Base64-encoded .p8 API key file |
| `MATCH_PASSWORD` | Password for Match certificates encryption |
| `MATCH_GIT_URL` | URL of your certificates repository |
| `MATCH_DEPLOY_KEY` | SSH private key for certificates repo |

### Android secrets

| Secret | Description |
|--------|-------------|
| `ANDROID_KEYSTORE_BASE64` | Base64-encoded release keystore |
| `ANDROID_KEYSTORE_PASSWORD` | Keystore password |
| `ANDROID_KEY_ALIAS` | Key alias (e.g., "release-key") |
| `ANDROID_KEY_PASSWORD` | Key password |
| `PLAY_STORE_SERVICE_ACCOUNT_JSON` | Base64-encoded service account JSON |

### Optional secrets

| Secret | Description |
|--------|-------------|
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications |
| `CODECOV_TOKEN` | Codecov token for coverage reports |
| `SNYK_TOKEN` | Snyk token for security scanning |

---

## Environment variables

### Creating environment files

Copy the example files and fill in your values:

```bash
cp ci_cd/environments/development.env.example .env.development
cp ci_cd/environments/staging.env.example .env.staging
cp ci_cd/environments/production.env.example .env.production
```

### App Store Connect API key

1. Go to App Store Connect > Users and Access > Keys
2. Click "+" to create a new key
3. Name: "CI/CD" with Admin access
4. Download the .p8 file (you can only download once)
5. Note the Key ID and Issuer ID
6. Base64 encode: `base64 -i AuthKey_XXXXXX.p8 | pbcopy`

### Environment-specific configs

Use GitHub environments for different deployment targets:

1. Go to Settings > Environments
2. Create environments: `development`, `staging`, `production`
3. Add environment-specific secrets
4. Set protection rules for production (require approval)

---

## Testing the pipeline

### 1. Test locally first

```bash
# iOS
cd ios
bundle exec fastlane ios build_debug
bundle exec fastlane ios ios_test

# Android
cd android
bundle exec fastlane android build_debug
bundle exec fastlane android android_test
```

### 2. Test CI builds

```bash
# Push to a feature branch to trigger lint_test.yml
git checkout -b test-ci
git commit --allow-empty -m "Test CI"
git push origin test-ci
```

### 3. Test deployment (dry run)

```bash
# iOS - builds but doesn't upload
cd ios
bundle exec fastlane ios build_release

# Android - builds but doesn't upload
cd android
bundle exec fastlane android build_release
```

### 4. Full deployment test

Use the workflow_dispatch trigger:

1. Go to Actions tab in GitHub
2. Select "Deploy to TestFlight" or "Deploy to Play Store"
3. Click "Run workflow"
4. Select options and run

---

## Troubleshooting

### Common issues

#### "No signing certificate found"

```bash
# Re-sync Match certificates
bundle exec fastlane match appstore --force
```

#### "Invalid provisioning profile"

```bash
# Clear local profiles and re-sync
rm -rf ~/Library/MobileDevice/Provisioning\ Profiles/*
bundle exec fastlane match appstore
```

#### "Keystore file not found"

Ensure the keystore is properly decoded in CI:

```yaml
- name: Decode keystore
  run: echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 --decode > android/app/release-keystore.jks
```

#### "API key authentication failed"

1. Verify the key ID and issuer ID are correct
2. Ensure the .p8 file is base64-encoded correctly
3. Check the key hasn't been revoked

#### "Build number already exists"

Increment the build number:

```bash
# iOS
bundle exec fastlane ios bump_version type:patch

# Android
bundle exec fastlane android bump_version type:patch
```

### Debug tips

1. Run Fastlane with verbose output:
   ```bash
   bundle exec fastlane ios build_release --verbose
   ```

2. Check GitHub Actions logs for full error messages

3. Test secrets locally using `.env` files (not committed)

4. Use `gh` CLI to trigger workflows with debugging:
   ```bash
   gh workflow run deploy_testflight.yml --ref main
   gh run watch
   ```

---

## Quick reference

### Common Fastlane commands

```bash
# iOS
bundle exec fastlane ios build_debug       # Debug build
bundle exec fastlane ios build_release     # Release build
bundle exec fastlane ios ios_test          # Run tests
bundle exec fastlane ios deploy_testflight # Deploy to TestFlight
bundle exec fastlane ios bump_version      # Increment version

# Android
bundle exec fastlane android build_debug      # Debug APK
bundle exec fastlane android build_release    # Release AAB
bundle exec fastlane android android_test     # Run tests
bundle exec fastlane android deploy_play_store # Deploy to Play Store
bundle exec fastlane android bump_version     # Increment version
```

### GitHub Actions triggers

| Workflow | Trigger |
|----------|---------|
| lint_test.yml | Push/PR to main, develop |
| ios_build.yml | Push/PR with ios/ changes |
| android_build.yml | Push/PR with android/ changes |
| deploy_testflight.yml | Tags v*-ios, v*, or manual |
| deploy_play_store.yml | Tags v*-android, v*, or manual |

---

## Next steps

1. Set up all secrets in GitHub
2. Test the lint/test workflow on a PR
3. Do a test deployment to TestFlight/Play Store internal
4. Set up Slack notifications
5. Configure branch protection rules
6. Document your release process for the team
