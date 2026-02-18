# Security checklist for mobile apps

Pre-launch security requirements for React Native and native mobile apps.

---

## API key storage

### Requirements
- [ ] No API keys in source code
- [ ] No keys in version control (check git history)
- [ ] Keys injected at build time via environment variables
- [ ] Different keys for dev/staging/prod

### Implementation

**React Native (react-native-config):**
```bash
# .env (gitignored)
API_KEY=your_key_here
STRIPE_KEY=pk_live_xxx

# Access in code
import Config from 'react-native-config';
const apiKey = Config.API_KEY;
```

**iOS (xcconfig):**
```
// Debug.xcconfig
API_KEY = dev_key_here

// Release.xcconfig
API_KEY = prod_key_here
```

**Android (gradle.properties):**
```properties
# gradle.properties (gitignored)
API_KEY=your_key_here

# build.gradle
buildConfigField "String", "API_KEY", "\"${API_KEY}\""
```

---

## SSL/TLS pinning

### Requirements
- [ ] Certificate pinning enabled for all API calls
- [ ] Pin to public key (not certificate) for easier rotation
- [ ] Backup pins configured
- [ ] Pin validation failures logged (not exposed to user)

### Implementation

**React Native (react-native-ssl-pinning):**
```typescript
import { fetch } from 'react-native-ssl-pinning';

const response = await fetch('https://api.yourapp.com/data', {
  method: 'GET',
  sslPinning: {
    certs: ['your_cert_sha256']
  },
  headers: {
    'Content-Type': 'application/json'
  }
});
```

**Native iOS:**
```swift
let pinnedCertificates: [SecCertificate] = // load from bundle
let serverTrust = // from URLAuthenticationChallenge
SecTrustSetAnchorCertificates(serverTrust, pinnedCertificates as CFArray)
```

---

## Root/jailbreak detection

### Requirements
- [ ] Detect rooted Android devices
- [ ] Detect jailbroken iOS devices
- [ ] Graceful degradation (warn user, limit features)
- [ ] Don't crash app (bad UX and store rejection risk)

### Implementation

**React Native (jail-monkey):**
```typescript
import JailMonkey from 'jail-monkey';

const checkDeviceSecurity = () => {
  const isCompromised = JailMonkey.isJailBroken();
  const canMockLocation = JailMonkey.canMockLocation();
  const isDebugMode = JailMonkey.isDebuggedMode();

  if (isCompromised) {
    // Log to analytics, limit sensitive features
    analytics.track('compromised_device_detected');
    return { secure: false, reason: 'device_compromised' };
  }

  return { secure: true };
};
```

### Detection signals

**Android:**
- su binary present
- Superuser.apk installed
- Test-keys in build tags
- RW system partition

**iOS:**
- Cydia installed
- Can write to /private
- Fork succeeds
- Suspicious dylibs loaded

---

## Code obfuscation

### Requirements
- [ ] JavaScript bundle obfuscated (React Native)
- [ ] ProGuard enabled (Android)
- [ ] Bitcode enabled (iOS)
- [ ] Debug symbols stripped from release builds

### Implementation

**React Native (metro.config.js):**
```javascript
module.exports = {
  transformer: {
    minifierConfig: {
      mangle: {
        toplevel: true,
      },
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
  },
};
```

**Android (proguard-rules.pro):**
```proguard
-keep class com.yourapp.** { *; }
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-dontwarn okhttp3.**
-dontwarn retrofit2.**
```

**Additional tools:**
- react-native-obfuscating-transformer
- javascript-obfuscator

---

## Secure storage

### Requirements
- [ ] Sensitive data in Keychain (iOS) / Keystore (Android)
- [ ] User tokens encrypted at rest
- [ ] Biometric authentication for high-value operations
- [ ] Storage cleared on logout

### Implementation

See `secure_storage.ts` for full implementation.

**Quick reference:**
```typescript
import { SecureStorage } from './secure_storage';

// Store sensitive data
await SecureStorage.setItem('auth_token', token, {
  biometric: false,
  accessible: 'whenUnlockedThisDeviceOnly'
});

// Retrieve with biometric
const token = await SecureStorage.getItem('auth_token', {
  biometric: true,
  biometricPrompt: 'Authenticate to access your account'
});
```

---

## Input validation

### Requirements
- [ ] Validate all user input client-side (UX)
- [ ] Validate all input server-side (security)
- [ ] Sanitize data before storage
- [ ] Parameterized queries for database operations

### Implementation

```typescript
import { z } from 'zod';

// Define schemas
const emailSchema = z.string().email().max(255);
const passwordSchema = z.string().min(8).max(128);
const usernameSchema = z.string().min(3).max(30).regex(/^[a-zA-Z0-9_]+$/);

// Validate input
const validateInput = <T>(schema: z.Schema<T>, input: unknown): T => {
  const result = schema.safeParse(input);
  if (!result.success) {
    throw new ValidationError(result.error.issues);
  }
  return result.data;
};

// Usage
try {
  const email = validateInput(emailSchema, userInput);
  // Safe to use
} catch (error) {
  if (error instanceof ValidationError) {
    // Show user-friendly error
  }
}
```

### Common validation rules

| Field | Validation |
|-------|------------|
| Email | Valid format, max 255 chars |
| Password | Min 8 chars, max 128, complexity rules |
| Username | Alphanumeric + underscore, 3-30 chars |
| Phone | E.164 format validation |
| URL | Valid URL format, allowed protocols |
| Amount | Positive number, max decimal places |
| Date | Valid date, within allowed range |

---

## Authentication

### Requirements
- [ ] Tokens stored securely (Keychain/Keystore)
- [ ] Token refresh before expiry
- [ ] Logout clears all sensitive data
- [ ] Session timeout for inactive users
- [ ] Biometric auth for sensitive operations

### Token handling
```typescript
// Token storage
await SecureStorage.setItem('access_token', accessToken);
await SecureStorage.setItem('refresh_token', refreshToken);

// Token refresh (automatic)
const refreshTokens = async () => {
  const refreshToken = await SecureStorage.getItem('refresh_token');
  const response = await api.post('/auth/refresh', { refreshToken });
  await SecureStorage.setItem('access_token', response.accessToken);
  return response.accessToken;
};

// Logout (clear all)
const logout = async () => {
  await SecureStorage.clear();
  await AsyncStorage.clear();
  // Navigate to login
};
```

---

## Network security

### Requirements
- [ ] HTTPS only (no HTTP fallback)
- [ ] Certificate pinning enabled
- [ ] No sensitive data in URLs (use POST body)
- [ ] Request/response logging disabled in production
- [ ] Timeout configured for all requests

### Implementation
```typescript
// Axios configuration
const api = axios.create({
  baseURL: 'https://api.yourapp.com',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Disable logging in production
if (!__DEV__) {
  api.interceptors.request.use(request => {
    // No logging
    return request;
  });
}
```

---

## Data protection

### Requirements
- [ ] Encrypt sensitive data at rest
- [ ] Clear clipboard after paste (sensitive fields)
- [ ] Disable screenshots on sensitive screens
- [ ] Mask sensitive data in app switcher
- [ ] No sensitive data in logs

### Screenshot prevention

**Android (MainActivity.java):**
```java
getWindow().setFlags(
  WindowManager.LayoutParams.FLAG_SECURE,
  WindowManager.LayoutParams.FLAG_SECURE
);
```

**iOS (AppDelegate.m):**
```objc
// Add blur view when entering background
- (void)applicationWillResignActive:(UIApplication *)application {
  UIBlurEffect *blur = [UIBlurEffect effectWithStyle:UIBlurEffectStyleLight];
  UIVisualEffectView *blurView = [[UIVisualEffectView alloc] initWithEffect:blur];
  blurView.frame = self.window.bounds;
  blurView.tag = 999;
  [self.window addSubview:blurView];
}

- (void)applicationDidBecomeActive:(UIApplication *)application {
  [[self.window viewWithTag:999] removeFromSuperview];
}
```

---

## Logging and analytics

### Requirements
- [ ] No PII in logs
- [ ] No tokens/passwords in logs
- [ ] Structured logging with levels
- [ ] Remote logging disabled in debug builds
- [ ] User consent for analytics

### Safe logging
```typescript
const sanitizeForLogging = (data: any): any => {
  const sensitiveKeys = ['password', 'token', 'secret', 'key', 'auth'];

  if (typeof data !== 'object' || data === null) {
    return data;
  }

  const sanitized = { ...data };
  for (const key of Object.keys(sanitized)) {
    if (sensitiveKeys.some(sk => key.toLowerCase().includes(sk))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof sanitized[key] === 'object') {
      sanitized[key] = sanitizeForLogging(sanitized[key]);
    }
  }

  return sanitized;
};

const logger = {
  info: (message: string, data?: any) => {
    if (__DEV__) {
      console.log(message, sanitizeForLogging(data));
    }
    // Production: send to secure logging service
  },
};
```

---

## Pre-launch security audit

Run these checks before every release:

1. [ ] `npm audit` - check for vulnerable dependencies
2. [ ] Search codebase for hardcoded secrets: `grep -r "API_KEY\|SECRET\|PASSWORD" src/`
3. [ ] Verify ProGuard/obfuscation enabled in release build
4. [ ] Test certificate pinning with proxy (should fail)
5. [ ] Verify root/jailbreak detection works
6. [ ] Check for console.log statements in release
7. [ ] Test logout clears all sensitive data
8. [ ] Verify biometric auth flows work correctly
9. [ ] Check app behavior on compromised devices
10. [ ] Review OWASP Mobile Top 10 compliance

---

## Quick fixes for common issues

| Issue | Fix |
|-------|-----|
| API key in code | Move to .env, inject at build time |
| Token in AsyncStorage | Migrate to SecureStorage |
| No cert pinning | Add react-native-ssl-pinning |
| Console.log in prod | Add babel transform to strip |
| Sensitive data visible in app switcher | Add blur overlay on background |
| No input validation | Add zod schemas |
| HTTP requests allowed | Force HTTPS in network config |

---

## Resources

- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [React Native Security Best Practices](https://reactnative.dev/docs/security)
- [iOS App Security Guide](https://developer.apple.com/documentation/security)
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
