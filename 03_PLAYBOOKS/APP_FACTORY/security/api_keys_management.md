# API keys management

How to handle API keys securely throughout the development lifecycle.

---

## Environment variable setup

### Local development

**Create .env file (never commit):**
```bash
# .env (root of project)
API_URL=https://api-dev.yourapp.com
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
ANALYTICS_ID=UA-XXXXX-X
```

**Add to .gitignore:**
```gitignore
# .gitignore
.env
.env.local
.env.*.local
*.env

# Platform-specific
android/app/google-services.json
ios/GoogleService-Info.plist
```

### React Native setup

**Using react-native-config:**
```bash
npm install react-native-config
cd ios && pod install
```

**Access in code:**
```typescript
import Config from 'react-native-config';

const API_URL = Config.API_URL;
const STRIPE_KEY = Config.STRIPE_PUBLISHABLE_KEY;
```

**Android (android/app/build.gradle):**
```gradle
apply plugin: "com.android.application"
apply from: project(':react-native-config').projectDir.getPath() + "/dotenv.gradle"

android {
    defaultConfig {
        resValue "string", "build_config_package", "com.yourapp"
    }
}
```

**iOS (ios/YourApp/Info.plist):**
```xml
<!-- Build phase script reads .env -->
<!-- Access via: [[NSBundle mainBundle] objectForInfoDictionaryKey:@"API_URL"] -->
```

### Next.js setup

**Environment files:**
```bash
# .env.local - local development (gitignored)
# .env.development - development defaults
# .env.production - production defaults

# .env.local
DATABASE_URL=postgresql://localhost/myapp
STRIPE_SECRET_KEY=sk_test_xxxxx

# Public variables (exposed to browser)
NEXT_PUBLIC_API_URL=https://api.yourapp.com
NEXT_PUBLIC_STRIPE_KEY=pk_live_xxxxx
```

**Access in code:**
```typescript
// Server-side only
const dbUrl = process.env.DATABASE_URL;
const stripeSecret = process.env.STRIPE_SECRET_KEY;

// Client-side (public)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

---

## Build-time injection

### React Native (EAS Build)

**eas.json:**
```json
{
  "cli": {
    "version": ">= 3.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": {
        "API_URL": "https://api-dev.yourapp.com",
        "ENV": "development"
      }
    },
    "staging": {
      "distribution": "internal",
      "env": {
        "API_URL": "https://api-staging.yourapp.com",
        "ENV": "staging"
      }
    },
    "production": {
      "env": {
        "API_URL": "https://api.yourapp.com",
        "ENV": "production"
      }
    }
  }
}
```

**Secrets in EAS:**
```bash
# Set secrets (not in eas.json)
eas secret:create --name STRIPE_SECRET_KEY --value sk_live_xxxxx --scope project

# List secrets
eas secret:list

# Use in build
# Secrets are injected as environment variables during build
```

### GitHub Actions

**Repository secrets:**
```yaml
# .github/workflows/build.yml
name: Build

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build with secrets
        env:
          STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          echo "API_URL=https://api.yourapp.com" > .env
          echo "STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY" >> .env
          npm run build
```

### Vercel

**Environment variables in dashboard:**
1. Project Settings > Environment Variables
2. Add variable with name and value
3. Select environments (Production, Preview, Development)
4. For sensitive keys, select "Sensitive" (hidden in logs)

**vercel.json:**
```json
{
  "env": {
    "NEXT_PUBLIC_API_URL": "https://api.yourapp.com"
  }
}
```

---

## Key rotation

### When to rotate

**Immediately:**
- Key leaked in git commit
- Key exposed in logs or error messages
- Employee with access leaves
- Suspicious activity detected

**Regularly:**
- Every 90 days for high-value keys
- Every 6 months for lower-risk keys
- When upgrading to production

### Rotation procedure

**1. Generate new key:**
```bash
# Most services have a dashboard to generate new keys
# Or use CLI tools
stripe api_keys rotate
```

**2. Update in secret manager:**
```bash
# Update in EAS
eas secret:create --name STRIPE_SECRET_KEY --value sk_live_NEW_KEY --scope project --force

# Update in Vercel
vercel env rm STRIPE_SECRET_KEY production
vercel env add STRIPE_SECRET_KEY production

# Update in GitHub
# Settings > Secrets > Update
```

**3. Deploy new build:**
```bash
# Trigger new build with updated secrets
eas build --platform all --profile production

# Or trigger deployment
vercel --prod
```

**4. Verify new key works:**
```bash
# Test API calls
curl -H "Authorization: Bearer $NEW_KEY" https://api.service.com/test
```

**5. Revoke old key:**
```bash
# Wait 24 hours to ensure no cached builds use old key
# Then revoke in service dashboard
```

### Rotation checklist

- [ ] New key generated
- [ ] New key tested locally
- [ ] Secret manager updated
- [ ] New build deployed
- [ ] Production verified working
- [ ] Old key revoked
- [ ] Team notified
- [ ] Rotation logged

---

## Leaked key response

### Immediate actions (within minutes)

**1. Revoke the key:**
```bash
# Most critical step - do this first
# Service dashboard > API Keys > Revoke
```

**2. Assess exposure:**
- How long was it exposed?
- What access does the key have?
- Were there unauthorized requests?

**3. Generate new key:**
- Create new key in service dashboard
- Update in secret manager
- Deploy immediately

### Investigation

**Check git history:**
```bash
# Find commits with potential secrets
git log -p --all -S 'sk_live' --source

# Check if in remote
git log origin/main --oneline | head -20
```

**Clean git history (if not pushed):**
```bash
# Remove from last commit
git reset --soft HEAD~1
# Remove secret from files
git add .
git commit -m "Remove accidental secret"
```

**Clean git history (if pushed):**
```bash
# Use BFG Repo Cleaner
bfg --replace-text passwords.txt repo.git

# Or git filter-branch (slower)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with team)
git push origin --force --all
```

**Check service logs:**
- Review API request logs in service dashboard
- Look for unusual patterns or unauthorized access
- Export logs for forensic analysis

### Post-incident

**Document:**
```markdown
## Incident Report: API Key Exposure

**Date:** [Date]
**Key Type:** [e.g., Stripe Secret Key]
**Exposure Duration:** [Time period]
**Root Cause:** [How it was exposed]
**Impact:** [What access was possible]
**Actions Taken:**
1. Key revoked at [time]
2. New key generated
3. Git history cleaned
4. Production redeployed
**Prevention:**
- Added pre-commit hook for secret scanning
- Enabled GitHub secret scanning
- Updated onboarding docs
```

**Prevent recurrence:**
```bash
# Install pre-commit hook
npm install -D husky @commitlint/cli

# Add secret scanning
npx husky add .husky/pre-commit "npm run scan-secrets"
```

---

## Secret scanning

### Pre-commit hooks

**Using detect-secrets:**
```bash
# Install
pip install detect-secrets

# Generate baseline (false positives to ignore)
detect-secrets scan > .secrets.baseline

# Add to pre-commit
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

**Using gitleaks:**
```bash
# Install
brew install gitleaks

# Scan repo
gitleaks detect --source . --verbose

# Add to CI
# .github/workflows/security.yml
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### GitHub secret scanning

Enable in repository settings:
1. Settings > Code security and analysis
2. Enable "Secret scanning"
3. Enable "Push protection" (blocks commits with secrets)

### Custom patterns

**gitleaks.toml:**
```toml
[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key"
regex = '''(?i)(yourapp_api_key|yourapp_secret)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{32,})['"]?'''
secretGroup = 2
```

---

## Key storage best practices

### Development

| Storage | Use Case | Security |
|---------|----------|----------|
| .env file | Local dev only | Gitignored |
| 1Password | Team sharing | Encrypted, access controlled |
| Doppler | Dev/staging secrets | Encrypted, audit log |

### Production

| Storage | Use Case | Security |
|---------|----------|----------|
| EAS Secrets | React Native builds | Encrypted at rest |
| Vercel Env | Next.js deploys | Encrypted, project-scoped |
| AWS Secrets Manager | Server apps | IAM controlled, rotatable |
| Google Secret Manager | GCP apps | IAM controlled, versioned |

### Mobile apps

**Never embed sensitive keys in mobile apps:**
```typescript
// BAD - Key in app binary
const STRIPE_SECRET = 'sk_live_xxxxx';

// GOOD - Only publishable keys in app
const STRIPE_PUBLISHABLE = 'pk_live_xxxxx';

// GOOD - Sensitive operations via your backend
const createPaymentIntent = async (amount: number) => {
  // Your backend uses the secret key
  return api.post('/payments/create-intent', { amount });
};
```

### Key types by sensitivity

| Key Type | Where to Use | Where to Store |
|----------|--------------|----------------|
| Publishable keys | Mobile/web client | .env, code |
| Secret keys | Backend only | Secret manager |
| Service accounts | CI/CD, backend | Secret manager |
| Encryption keys | Never expose | HSM or Keychain |

---

## Audit and monitoring

### Access logging

```typescript
// Log all API key usage
const logApiAccess = (
  keyId: string,
  action: string,
  metadata?: Record<string, any>
): void => {
  logger.info('api_key_access', {
    keyId,
    action,
    timestamp: new Date().toISOString(),
    ...metadata,
  });
};

// Usage
logApiAccess('stripe_prod', 'create_payment', {
  amount: 5000,
  currency: 'usd',
});
```

### Key inventory

Maintain a list of all keys:

| Service | Key Name | Environment | Owner | Last Rotated | Next Rotation |
|---------|----------|-------------|-------|--------------|---------------|
| Stripe | sk_live_xxx | Production | @john | 2024-01-15 | 2024-04-15 |
| Sentry | dsn_xxx | All | @team | 2024-02-01 | 2024-08-01 |
| Twilio | auth_xxx | Production | @jane | 2024-01-01 | 2024-04-01 |

### Alerts

**Set up alerts for:**
- API key approaching rate limit
- Unusual API usage patterns
- Failed authentication attempts
- Key used from unexpected IP/region

```yaml
# Example: Datadog monitor
alert:
  name: "Unusual API Key Usage"
  query: "sum(last_5m):sum:api.requests{key:stripe_prod}.as_count() > 1000"
  message: "Stripe API key usage spike detected. Check for abuse."
```

---

## Quick reference

### Environment variable naming

```bash
# Prefix with service name
STRIPE_PUBLISHABLE_KEY=pk_xxx
STRIPE_SECRET_KEY=sk_xxx

# Suffix with environment
DATABASE_URL_DEV=postgres://dev
DATABASE_URL_PROD=postgres://prod

# Public prefix for client exposure
NEXT_PUBLIC_API_URL=https://api.example.com
EXPO_PUBLIC_API_URL=https://api.example.com
```

### Checklist for new keys

- [ ] Key stored in secret manager (not code)
- [ ] Added to .gitignore
- [ ] Team has access via secure channel
- [ ] Rotation schedule set
- [ ] Monitoring/alerts configured
- [ ] Documented in key inventory
- [ ] Scoped to minimum permissions

### Emergency contacts

| Service | Revocation URL | Support |
|---------|---------------|---------|
| Stripe | dashboard.stripe.com/apikeys | support@stripe.com |
| AWS | IAM Console | aws.amazon.com/support |
| Google | console.cloud.google.com | cloud.google.com/support |
| Twilio | console.twilio.com | twilio.com/help |

---

## Resources

- [12 Factor App - Config](https://12factor.net/config)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
