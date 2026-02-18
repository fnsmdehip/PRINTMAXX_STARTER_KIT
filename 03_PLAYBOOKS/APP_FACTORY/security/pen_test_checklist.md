# Penetration testing checklist

Pre-launch security testing for mobile apps. Run through this before every release.

---

## Prerequisites

### Tools needed

**Mobile testing:**
- Frida - Runtime instrumentation
- objection - Mobile exploration toolkit
- MobSF - Automated analysis
- Burp Suite - HTTP proxy/interceptor
- jadx - Android decompiler
- Hopper/Ghidra - iOS binary analysis

**Network testing:**
- mitmproxy - SSL/TLS interception
- Wireshark - Network analysis
- nmap - Port scanning

**Install commands:**
```bash
# Frida
pip install frida-tools

# objection
pip install objection

# MobSF (Docker)
docker pull opensecurity/mobile-security-framework-mobsf
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf

# mitmproxy
pip install mitmproxy

# jadx
brew install jadx  # macOS
```

---

## 1. Static analysis

### 1.1 Binary analysis

**Android (APK):**
```bash
# Decompile APK
jadx -d output/ app.apk

# Search for hardcoded secrets
grep -r "API_KEY\|SECRET\|PASSWORD\|token" output/

# Check for debug flags
grep -r "android:debuggable" output/AndroidManifest.xml

# Find URLs and endpoints
grep -rE "https?://[a-zA-Z0-9./?=_-]+" output/
```

**iOS (IPA):**
```bash
# Unzip IPA
unzip app.ipa -d output/

# Check Info.plist
plutil -p output/Payload/App.app/Info.plist

# Search strings in binary
strings output/Payload/App.app/App | grep -i "api\|key\|secret\|password"

# Check for ATS exceptions
plutil -p output/Payload/App.app/Info.plist | grep -A 20 NSAppTransportSecurity
```

**Checklist:**
- [ ] No hardcoded API keys or secrets
- [ ] Debug mode disabled in release
- [ ] No sensitive URLs in plaintext
- [ ] ATS properly configured (iOS)
- [ ] Network security config enforces HTTPS (Android)
- [ ] Exported components properly restricted

### 1.2 Automated scanning

**MobSF analysis:**
```bash
# Start MobSF
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf

# Upload APK/IPA to http://localhost:8000
# Review:
# - Security score
# - Hardcoded secrets
# - Insecure permissions
# - Code analysis findings
```

**npm audit (React Native):**
```bash
cd your-app
npm audit
npm audit fix

# Check for known vulnerabilities
npx snyk test
```

---

## 2. Dynamic analysis

### 2.1 Network traffic

**Setup proxy:**
```bash
# Start mitmproxy
mitmproxy -p 8080

# Configure device to use proxy
# Install mitmproxy CA certificate on device
```

**Test cases:**
- [ ] All traffic uses HTTPS
- [ ] No sensitive data in URLs
- [ ] Certificate pinning blocks proxy
- [ ] Tokens sent in headers, not query params
- [ ] No sensitive data in error responses

**Bypass certificate pinning (for testing):**
```bash
# Using Frida
frida -U -f com.yourapp --no-pause -l ssl_pinning_bypass.js

# Using objection
objection -g com.yourapp explore
> android sslpinning disable
> ios sslpinning disable
```

### 2.2 Authentication testing

**Test cases:**
- [ ] Brute force protection (account lockout)
- [ ] Session tokens are random and long
- [ ] Tokens expire appropriately
- [ ] Logout invalidates session server-side
- [ ] Password reset doesn't leak user existence
- [ ] No token in URL or logs

**Brute force test:**
```bash
# Use Burp Intruder or:
for i in {1..20}; do
  curl -X POST https://api.yourapp.com/login \
    -d '{"email":"test@example.com","password":"wrong'$i'"}' \
    -w "Attempt $i: %{http_code}\n"
done
# After ~5-10 attempts, should get 429 or account locked
```

### 2.3 Authorization testing

**Test cases:**
- [ ] Cannot access other users' data by changing IDs
- [ ] Cannot escalate privileges
- [ ] Admin functions require admin role
- [ ] Deleted resources return 404, not 403

**IDOR test:**
```bash
# Login as user A, get token
TOKEN_A="user_a_token"

# Try to access user B's resources
curl -H "Authorization: Bearer $TOKEN_A" \
  https://api.yourapp.com/users/user_b_id/profile
# Should return 403 or 404, not user B's data
```

### 2.4 Data storage testing

**Android:**
```bash
# Connect to device
adb shell

# Check shared preferences
cat /data/data/com.yourapp/shared_prefs/*.xml

# Check databases
sqlite3 /data/data/com.yourapp/databases/app.db
.tables
SELECT * FROM users;

# Check for sensitive data in cache
ls -la /data/data/com.yourapp/cache/
```

**iOS:**
```bash
# Using objection
objection -g com.yourapp explore

# Check keychain
> ios keychain dump

# Check plist files
> ios plist cat Info.plist

# Check SQLite
> sqlite connect app.db
> .tables
```

**Checklist:**
- [ ] No tokens in SharedPreferences/NSUserDefaults
- [ ] Database encrypted if contains sensitive data
- [ ] Keychain/Keystore used for credentials
- [ ] Cache doesn't contain sensitive data
- [ ] Logs don't contain PII or tokens

---

## 3. Client-side testing

### 3.1 Root/jailbreak detection

**Test cases:**
- [ ] App detects rooted/jailbroken device
- [ ] Appropriate action taken (warn, limit features)
- [ ] Detection cannot be easily bypassed

**Bypass test:**
```bash
# Using Frida
frida -U -f com.yourapp --no-pause -l jailbreak_bypass.js

# Using objection
objection -g com.yourapp explore
> ios jailbreak disable
> android root disable
```

### 3.2 Code tampering

**Test cases:**
- [ ] App validates its own integrity
- [ ] Repackaged APK fails to run
- [ ] Modified binary detected

**Repackaging test (Android):**
```bash
# Decompile
apktool d app.apk -o output

# Modify something
echo "// tampered" >> output/smali/com/yourapp/MainActivity.smali

# Recompile
apktool b output -o tampered.apk

# Sign
jarsigner -keystore debug.keystore tampered.apk alias

# Install and test
adb install tampered.apk
# App should detect tampering
```

### 3.3 Debug detection

**Test cases:**
- [ ] App detects debugger attachment
- [ ] Frida detection implemented
- [ ] Debug builds clearly identified

---

## 4. API security testing

### 4.1 Input validation

**Test payloads:**
```bash
# SQL injection
curl -X POST https://api.yourapp.com/search \
  -d '{"query": "test'\'' OR 1=1--"}'

# XSS (if data reflected)
curl -X POST https://api.yourapp.com/profile \
  -d '{"name": "<script>alert(1)</script>"}'

# Command injection
curl -X POST https://api.yourapp.com/upload \
  -d '{"filename": "test; rm -rf /"}'

# Path traversal
curl https://api.yourapp.com/files/../../../etc/passwd
```

**Checklist:**
- [ ] SQL injection blocked
- [ ] XSS payloads sanitized
- [ ] Command injection impossible
- [ ] Path traversal blocked
- [ ] Large payloads rejected (DoS protection)

### 4.2 Rate limiting

**Test:**
```bash
# Send many requests quickly
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    https://api.yourapp.com/endpoint
done | sort | uniq -c
# Should see 429 responses after threshold
```

**Checklist:**
- [ ] Rate limiting on all endpoints
- [ ] Stricter limits on auth endpoints
- [ ] Rate limit headers present
- [ ] Cannot bypass via headers (X-Forwarded-For)

### 4.3 Error handling

**Test cases:**
- [ ] Errors don't leak stack traces
- [ ] Errors don't reveal system info
- [ ] 404 vs 403 doesn't leak resource existence
- [ ] Generic error messages for auth failures

---

## 5. Cryptography testing

### 5.1 Encryption

**Check algorithms:**
```bash
# Search for weak algorithms in decompiled code
grep -rE "MD5|SHA1|DES|RC4|ECB" output/

# Check TLS configuration
nmap --script ssl-enum-ciphers -p 443 api.yourapp.com
```

**Checklist:**
- [ ] TLS 1.2+ required
- [ ] No weak ciphers (RC4, DES, etc.)
- [ ] AES-256 or stronger for encryption
- [ ] SHA-256 or stronger for hashing
- [ ] No ECB mode

### 5.2 Key management

**Checklist:**
- [ ] No hardcoded keys in binary
- [ ] Keys stored in Keychain/Keystore
- [ ] Keys not logged or transmitted insecurely
- [ ] Key rotation mechanism exists

---

## 6. Privacy testing

### 6.1 Data collection

**Test cases:**
- [ ] Only necessary permissions requested
- [ ] Consent obtained before data collection
- [ ] Data collection matches privacy policy
- [ ] Analytics can be disabled

### 6.2 Data leakage

**Check locations:**
```bash
# Clipboard
# Copy sensitive data, check if persisted

# Screenshots
# Navigate to sensitive screen, check app switcher

# Logs
adb logcat | grep -i "email\|phone\|password\|token"

# Crash reports
# Trigger crash, check report doesn't contain PII
```

**Checklist:**
- [ ] Clipboard cleared after sensitive paste
- [ ] Sensitive screens hidden in app switcher
- [ ] No PII in logs
- [ ] Crash reports sanitized

---

## 7. Remediation guide

### Critical findings (fix immediately)

| Finding | Remediation |
|---------|-------------|
| Hardcoded API keys | Move to env vars, rotate compromised keys |
| Missing cert pinning | Implement via react-native-ssl-pinning |
| No encryption on DB | Implement SQLCipher |
| Tokens in plain storage | Migrate to Keychain/Keystore |
| Missing rate limiting | Implement server-side limits |

### High findings (fix before release)

| Finding | Remediation |
|---------|-------------|
| Debug mode in release | Update build configuration |
| Weak password policy | Enforce complexity requirements |
| Missing HTTPS | Force TLS 1.2+ |
| IDOR vulnerabilities | Add server-side auth checks |
| Missing input validation | Add validation with zod/yup |

### Medium findings (fix soon)

| Finding | Remediation |
|---------|-------------|
| No root detection | Add jail-monkey |
| Verbose error messages | Implement generic errors |
| Missing obfuscation | Enable ProGuard/Metro config |
| Excessive permissions | Request only needed permissions |

---

## 8. Testing schedule

### Pre-release testing
- [ ] Automated static analysis (MobSF)
- [ ] npm audit / dependency check
- [ ] Network traffic analysis
- [ ] Authentication testing
- [ ] Authorization testing

### Quarterly testing
- [ ] Full penetration test
- [ ] Cryptography review
- [ ] Privacy audit
- [ ] Third-party dependency audit

### Annual testing
- [ ] External penetration test
- [ ] Security architecture review
- [ ] Compliance audit

---

## 9. Reporting template

```markdown
# Security Assessment Report

## Executive Summary
- App: [App Name]
- Version: [Version]
- Date: [Date]
- Tester: [Name]

## Findings Summary
- Critical: [X]
- High: [X]
- Medium: [X]
- Low: [X]

## Critical Findings

### [Finding Title]
- **Severity:** Critical
- **Location:** [File/Endpoint]
- **Description:** [What was found]
- **Impact:** [Potential damage]
- **Remediation:** [How to fix]
- **Evidence:** [Screenshots/logs]

## Recommendations
1. [Priority recommendation]
2. [Secondary recommendation]

## Appendix
- Tools used
- Scope of testing
- Out of scope items
```

---

## Resources

- [OWASP Mobile Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Frida documentation](https://frida.re/docs/)
- [MobSF documentation](https://mobsf.github.io/docs/)
- [Burp Suite tutorials](https://portswigger.net/burp/documentation)
