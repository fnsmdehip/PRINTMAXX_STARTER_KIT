# OWASP Mobile Top 10 - prevention guide

Practical mitigations for each vulnerability. Code examples for React Native.

---

## M1: Improper platform usage

**What it is:** Misusing platform features or failing to use platform security controls.

**Common mistakes:**
- Storing sensitive data in shared preferences / NSUserDefaults
- Exposing activities/intents unintentionally
- Ignoring platform permission model
- Misconfigured app transport security

### Prevention

**Android - Restrict exported components:**
```xml
<!-- AndroidManifest.xml -->
<activity
    android:name=".SensitiveActivity"
    android:exported="false" />

<receiver
    android:name=".InternalReceiver"
    android:exported="false" />

<!-- If must be exported, add permission -->
<activity
    android:name=".PaymentActivity"
    android:exported="true"
    android:permission="com.yourapp.PAYMENT_PERMISSION" />
```

**iOS - Configure App Transport Security:**
```xml
<!-- Info.plist -->
<key>NSAppTransportSecurity</key>
<dict>
    <!-- Enforce HTTPS for all connections -->
    <key>NSAllowsArbitraryLoads</key>
    <false/>
    <!-- Exception only if absolutely necessary -->
    <key>NSExceptionDomains</key>
    <dict>
        <key>legacy-api.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
            <key>NSExceptionMinimumTLSVersion</key>
            <string>TLSv1.2</string>
        </dict>
    </dict>
</dict>
```

**React Native - Use proper storage:**
```typescript
// BAD - AsyncStorage for sensitive data
await AsyncStorage.setItem('auth_token', token);

// GOOD - Keychain/Keystore
import { SecureStorage } from './secure_storage';
await SecureStorage.setItem('auth_token', token);
```

### Checklist
- [ ] All activities/components have correct exported flag
- [ ] ATS enforces HTTPS (iOS)
- [ ] Network security config enforces HTTPS (Android)
- [ ] Sensitive data uses Keychain/Keystore, not preferences
- [ ] Permissions requested at runtime with explanation

---

## M2: Insecure data storage

**What it is:** Storing sensitive data in locations accessible to other apps or without encryption.

**Vulnerable locations:**
- SharedPreferences (Android) / NSUserDefaults (iOS)
- SQLite databases without encryption
- Log files
- Cloud backup
- Clipboard

### Prevention

**Use secure storage:**
```typescript
import { SecureStorage, EncryptedStorage } from './secure_storage';

// Highly sensitive (tokens, credentials)
await SecureStorage.setItem('auth_token', token, {
  accessible: 'whenUnlockedThisDeviceOnly',
});

// Moderately sensitive (preferences with PII)
await EncryptedStorage.setItem('user_profile', JSON.stringify(profile));
```

**Encrypt SQLite databases:**
```typescript
// Use react-native-sqlcipher or similar
import SQLCipher from 'react-native-sqlcipher-storage';

const db = await SQLCipher.openDatabase({
  name: 'app.db',
  key: encryptionKey, // From secure storage
});
```

**Disable backups for sensitive files:**
```xml
<!-- Android - android:allowBackup="false" or use backup rules -->
<application android:allowBackup="false">

<!-- Or selective backup -->
<application android:fullBackupContent="@xml/backup_rules">

<!-- backup_rules.xml -->
<full-backup-content>
    <exclude domain="sharedpref" path="sensitive_prefs.xml"/>
    <exclude domain="database" path="secure.db"/>
</full-backup-content>
```

```swift
// iOS - Exclude from iCloud backup
let fileURL = // your file URL
var resourceValues = URLResourceValues()
resourceValues.isExcludedFromBackup = true
try fileURL.setResourceValues(resourceValues)
```

**Clear clipboard after use:**
```typescript
import Clipboard from '@react-native-clipboard/clipboard';

const pasteAndClear = async () => {
  const text = await Clipboard.getString();
  // Use the text

  // Clear after 30 seconds
  setTimeout(() => {
    Clipboard.setString('');
  }, 30000);
};
```

### Checklist
- [ ] Tokens/credentials in Keychain/Keystore only
- [ ] Database encrypted with SQLCipher
- [ ] Sensitive files excluded from backup
- [ ] Clipboard cleared after sensitive paste
- [ ] No sensitive data in logs

---

## M3: Insecure communication

**What it is:** Failing to protect data in transit. Vulnerable to man-in-the-middle attacks.

**Risks:**
- Unencrypted HTTP connections
- Accepting invalid certificates
- No certificate pinning
- Sensitive data in URLs

### Prevention

**Enforce HTTPS and TLS 1.2+:**
```xml
<!-- Android - network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
</network-security-config>

<!-- Reference in AndroidManifest.xml -->
<application
    android:networkSecurityConfig="@xml/network_security_config">
```

**Implement certificate pinning:**
```typescript
import { SecureApiClient } from './api_security';

const api = new SecureApiClient({
  baseURL: 'https://api.yourapp.com',
  certificatePins: [
    'sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=', // Primary
    'sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=', // Backup
  ],
});
```

**Never put sensitive data in URLs:**
```typescript
// BAD - Token in URL
fetch(`https://api.example.com/data?token=${token}`);

// GOOD - Token in header
fetch('https://api.example.com/data', {
  headers: { Authorization: `Bearer ${token}` },
});
```

### Checklist
- [ ] HTTPS enforced (no HTTP fallback)
- [ ] TLS 1.2+ required
- [ ] Certificate pinning implemented
- [ ] Backup pins configured
- [ ] No sensitive data in URLs or query strings

---

## M4: Insecure authentication

**What it is:** Weak authentication mechanisms that allow unauthorized access.

**Risks:**
- Weak passwords accepted
- No brute force protection
- Sessions don't expire
- Insecure password recovery

### Prevention

**Strong password requirements:**
```typescript
import { z } from 'zod';

const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain uppercase letter')
  .regex(/[a-z]/, 'Password must contain lowercase letter')
  .regex(/[0-9]/, 'Password must contain number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain special character');
```

**Implement token refresh with expiry:**
```typescript
interface Tokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: number; // Short-lived: 15-60 minutes
}

const isTokenExpired = (tokens: Tokens): boolean => {
  return Date.now() >= tokens.expiresAt - 60000; // 1 min buffer
};

const getValidToken = async (): Promise<string> => {
  const tokens = await TokenManager.getTokens();

  if (!tokens || isTokenExpired(tokens)) {
    const newTokens = await refreshTokens();
    return newTokens.accessToken;
  }

  return tokens.accessToken;
};
```

**Biometric authentication for sensitive operations:**
```typescript
import { BiometricAuth } from './secure_storage';

const performSensitiveAction = async () => {
  const canUseBiometric = await BiometricAuth.isAvailable();

  if (canUseBiometric) {
    const result = await BiometricAuth.authenticate(
      'Authenticate to confirm payment'
    );

    if (!result.success) {
      throw new Error('Authentication required');
    }
  }

  // Proceed with action
};
```

**Session timeout:**
```typescript
const SESSION_TIMEOUT = 15 * 60 * 1000; // 15 minutes
let lastActivity = Date.now();

const checkSessionTimeout = () => {
  if (Date.now() - lastActivity > SESSION_TIMEOUT) {
    logout();
    showLoginScreen();
  }
};

// Reset on user activity
const onUserActivity = () => {
  lastActivity = Date.now();
};
```

### Checklist
- [ ] Password strength requirements enforced
- [ ] Access tokens short-lived (15-60 min)
- [ ] Refresh tokens rotated on use
- [ ] Biometric auth for sensitive operations
- [ ] Session timeout implemented
- [ ] Account lockout after failed attempts

---

## M5: Insufficient cryptography

**What it is:** Using weak or broken cryptographic algorithms, or implementing crypto incorrectly.

**Common mistakes:**
- Using MD5/SHA1 for sensitive hashing
- Hardcoded encryption keys
- Using ECB mode
- Custom crypto implementations

### Prevention

**Use strong algorithms:**
```typescript
import CryptoJS from 'crypto-js';

// GOOD - AES-256 with CBC mode
const encrypt = (data: string, key: string): string => {
  const iv = CryptoJS.lib.WordArray.random(16);
  const encrypted = CryptoJS.AES.encrypt(data, key, {
    iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  });

  // Prepend IV to ciphertext
  return iv.toString() + encrypted.toString();
};

const decrypt = (ciphertext: string, key: string): string => {
  const iv = CryptoJS.enc.Hex.parse(ciphertext.substring(0, 32));
  const encrypted = ciphertext.substring(32);

  const decrypted = CryptoJS.AES.decrypt(encrypted, key, {
    iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  });

  return decrypted.toString(CryptoJS.enc.Utf8);
};
```

**Never hardcode keys:**
```typescript
// BAD
const ENCRYPTION_KEY = 'my-secret-key-12345';

// GOOD - Generate and store securely
const getEncryptionKey = async (): Promise<string> => {
  let key = await SecureStorage.getItem('encryption_key');

  if (!key) {
    // Generate random key
    key = CryptoJS.lib.WordArray.random(32).toString();
    await SecureStorage.setItem('encryption_key', key);
  }

  return key;
};
```

**Use proper password hashing:**
```typescript
// For password verification (server-side ideally)
import bcrypt from 'bcryptjs';

const hashPassword = async (password: string): Promise<string> => {
  const salt = await bcrypt.genSalt(12);
  return bcrypt.hash(password, salt);
};

const verifyPassword = async (
  password: string,
  hash: string
): Promise<boolean> => {
  return bcrypt.compare(password, hash);
};
```

### Checklist
- [ ] AES-256 or stronger for encryption
- [ ] SHA-256 or stronger for hashing
- [ ] bcrypt/Argon2 for passwords
- [ ] Random IV for each encryption
- [ ] Keys stored in Keychain/Keystore
- [ ] No custom crypto implementations

---

## M6: Insecure authorization

**What it is:** Failing to properly validate user permissions before performing actions.

**Risks:**
- Horizontal privilege escalation (access other users' data)
- Vertical privilege escalation (gain admin rights)
- Direct object reference vulnerabilities

### Prevention

**Always validate server-side:**
```typescript
// Client-side checks are UX only
// BAD - Trusting client permissions
const canEdit = user.permissions.includes('edit');
if (canEdit) {
  await api.put(`/posts/${postId}`, data);
}

// GOOD - Server validates every request
// Server checks user owns post AND has edit permission
await api.put(`/posts/${postId}`, data);
// Server returns 403 if unauthorized
```

**Use indirect object references:**
```typescript
// BAD - Direct database ID in request
GET /api/users/12345/profile

// GOOD - Use session context
GET /api/me/profile  // Server gets user ID from auth token
```

**Implement role-based access control:**
```typescript
enum Permission {
  READ_OWN = 'read:own',
  WRITE_OWN = 'write:own',
  READ_ANY = 'read:any',
  ADMIN = 'admin',
}

const checkPermission = (
  user: User,
  required: Permission,
  resourceOwnerId?: string
): boolean => {
  // Admin can do anything
  if (user.permissions.includes(Permission.ADMIN)) {
    return true;
  }

  // Check ownership for 'own' permissions
  if (required.includes(':own')) {
    return user.id === resourceOwnerId &&
           user.permissions.includes(required);
  }

  return user.permissions.includes(required);
};
```

### Checklist
- [ ] All authorization checks on server
- [ ] Indirect object references where possible
- [ ] Role-based access control implemented
- [ ] Cannot access other users' data via ID manipulation
- [ ] Admin functions require additional verification

---

## M7: Client code quality

**What it is:** Security issues from poor coding practices, including buffer overflows, format strings, and memory issues.

**Risks:**
- Code injection
- Memory corruption (native code)
- Logic flaws

### Prevention

**Input validation everywhere:**
```typescript
import { z } from 'zod';

const userInputSchema = z.object({
  name: z.string().min(1).max(100).trim(),
  email: z.string().email().max(255),
  age: z.number().int().positive().max(150),
});

const processUserInput = (input: unknown) => {
  const result = userInputSchema.safeParse(input);

  if (!result.success) {
    throw new ValidationError(result.error.issues);
  }

  return result.data;
};
```

**Avoid eval and dynamic code:**
```typescript
// BAD - eval allows code injection
const result = eval(userInput);

// BAD - Function constructor
const fn = new Function(userInput);

// GOOD - Parse data safely
const result = JSON.parse(userInput);
```

**Enable strict mode:**
```typescript
// In TypeScript
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**Use static analysis:**
```bash
# ESLint security plugins
npm install eslint-plugin-security eslint-plugin-no-unsanitized

# Add to .eslintrc
{
  "plugins": ["security", "no-unsanitized"],
  "extends": ["plugin:security/recommended"]
}
```

### Checklist
- [ ] TypeScript strict mode enabled
- [ ] Input validation on all user input
- [ ] No eval or dynamic code execution
- [ ] ESLint security plugins configured
- [ ] Code review for security issues

---

## M8: Code tampering

**What it is:** Attackers modifying app code to bypass security, extract data, or inject malicious functionality.

**Risks:**
- Reverse engineering
- Code modification
- Repackaging with malware

### Prevention

**Root/jailbreak detection:**
```typescript
import JailMonkey from 'jail-monkey';

const checkDeviceIntegrity = (): boolean => {
  const isJailbroken = JailMonkey.isJailBroken();
  const isDebugMode = JailMonkey.isDebuggedMode();
  const canMockLocation = JailMonkey.canMockLocation();

  if (isJailbroken || isDebugMode) {
    // Log to analytics
    analytics.track('compromised_device');

    // Limit functionality
    return false;
  }

  return true;
};
```

**Code obfuscation:**
```javascript
// metro.config.js
module.exports = {
  transformer: {
    minifierConfig: {
      mangle: {
        toplevel: true,
        keep_fnames: false,
      },
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.debug'],
      },
    },
  },
};
```

**Runtime integrity checks:**
```typescript
// Check app signature (Android)
import { getSignatures } from 'react-native-device-info';

const verifyAppSignature = async (): Promise<boolean> => {
  const signatures = await getSignatures();
  const expectedSignature = 'your_release_signature_hash';

  return signatures.includes(expectedSignature);
};
```

**Anti-debugging:**
```typescript
// Detect debugger attachment
const detectDebugger = (): boolean => {
  // Check timing (debuggers slow execution)
  const start = Date.now();
  // Some computation
  for (let i = 0; i < 1000; i++) {}
  const elapsed = Date.now() - start;

  // Unusually long execution suggests debugger
  return elapsed > 100;
};
```

### Checklist
- [ ] Root/jailbreak detection active
- [ ] Code obfuscation in release builds
- [ ] ProGuard enabled (Android)
- [ ] Anti-debugging measures
- [ ] App signature verification

---

## M9: Reverse engineering

**What it is:** Attackers analyzing app binary to understand logic, extract secrets, or find vulnerabilities.

**Risks:**
- API key extraction
- Algorithm theft
- Vulnerability discovery

### Prevention

**Never embed secrets in code:**
```typescript
// BAD - Hardcoded in binary
const API_KEY = 'sk_live_xxxxxxxxxxxxx';

// GOOD - Injected at build time, stored securely
import Config from 'react-native-config';
const API_KEY = Config.API_KEY; // From .env (not in repo)
```

**Obfuscate sensitive logic:**
```javascript
// For critical algorithms, consider:
// 1. Server-side processing
// 2. Native module with obfuscation
// 3. White-box cryptography (advanced)

// Keep validation server-side
const validatePurchase = async (receipt: string): Promise<boolean> => {
  // Don't validate locally - send to server
  const response = await api.post('/validate-purchase', { receipt });
  return response.valid;
};
```

**Strip debug information:**
```bash
# iOS - Release build should have debug symbols stripped
# Check: Project > Build Settings > Strip Debug Symbols During Copy = YES

# Android - ProGuard in release
# build.gradle
buildTypes {
    release {
        minifyEnabled true
        shrinkResources true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
    }
}
```

### Checklist
- [ ] No secrets in source code
- [ ] Sensitive logic on server
- [ ] Debug symbols stripped in release
- [ ] ProGuard/R8 enabled
- [ ] String encryption for sensitive strings

---

## M10: Extraneous functionality

**What it is:** Hidden backdoors, test code, or debug functionality left in production.

**Risks:**
- Debug endpoints accessible
- Test accounts in production
- Hidden admin features

### Prevention

**Remove debug code in production:**
```typescript
// Use __DEV__ flag
if (__DEV__) {
  console.log('Debug info:', sensitiveData);
}

// Remove entire code blocks
if (__DEV__) {
  // This entire block is removed in production
  global.testHelper = {
    resetState: () => {},
    mockApi: () => {},
  };
}
```

**Conditional feature flags:**
```typescript
const Features = {
  DEBUG_PANEL: __DEV__,
  ADMIN_TOOLS: false, // Controlled server-side
  BETA_FEATURES: Config.ENABLE_BETA === 'true',
};

// In component
{Features.DEBUG_PANEL && <DebugPanel />}
```

**Pre-release code review:**
```bash
# Search for debug patterns
grep -r "TODO\|FIXME\|DEBUG\|HACK\|XXX" src/
grep -r "console\.log\|console\.debug" src/
grep -r "password.*=.*['\"]" src/
grep -r "secret\|api.key\|token" src/

# Check for test accounts
grep -ri "test@\|demo@\|admin@" src/
```

**Automated checks in CI:**
```yaml
# .github/workflows/security.yml
- name: Check for debug code
  run: |
    if grep -r "console\.log" src/; then
      echo "Found console.log statements"
      exit 1
    fi

    if grep -r "__DEV__" src/ --include="*.tsx" | grep -v "if (__DEV__)"; then
      echo "Found improper __DEV__ usage"
      exit 1
    fi
```

### Checklist
- [ ] No console.log in production
- [ ] Debug features behind __DEV__ flag
- [ ] Test accounts removed
- [ ] Hidden endpoints documented and secured
- [ ] Pre-release security review
- [ ] CI checks for debug patterns

---

## Quick reference table

| Risk | Priority | Primary Mitigation |
|------|----------|-------------------|
| M1: Platform Usage | High | Use platform security controls correctly |
| M2: Data Storage | Critical | Keychain/Keystore + encryption |
| M3: Communication | Critical | HTTPS + certificate pinning |
| M4: Authentication | Critical | Short-lived tokens + biometrics |
| M5: Cryptography | High | Standard algorithms, no hardcoded keys |
| M6: Authorization | High | Server-side validation |
| M7: Code Quality | Medium | Input validation + static analysis |
| M8: Code Tampering | Medium | Root detection + obfuscation |
| M9: Reverse Engineering | Medium | Server-side secrets + obfuscation |
| M10: Extraneous Functionality | Medium | Code review + CI checks |

---

## Resources

- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [OWASP Mobile Top 10 2024](https://owasp.org/www-project-mobile-top-10/)
- [NIST Mobile Security Guidelines](https://nvd.nist.gov/vuln-metrics/cvss)
