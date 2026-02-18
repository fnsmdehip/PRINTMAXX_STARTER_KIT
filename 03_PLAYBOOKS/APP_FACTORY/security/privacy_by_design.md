# Privacy by design

Build privacy into your app from day one. Compliance with GDPR, CCPA, and good practices.

---

## Core principles

### 1. Data minimization

Collect only what you need. Nothing more.

**Questions before collecting any data:**
- Do we actually need this data?
- Can we achieve the goal without it?
- Can we use anonymized data instead?
- What's the minimum amount needed?

**Implementation:**
```typescript
// BAD - Collecting everything
interface UserProfile {
  email: string;
  name: string;
  phone: string;
  address: string;
  dateOfBirth: Date;
  ssn: string;
  favoriteColor: string;
  mothersMaidenName: string;
}

// GOOD - Only what's needed
interface UserProfile {
  email: string;      // Required for auth
  displayName: string; // Optional, user-facing
}

// Collect additional data only when needed for specific features
interface ShippingInfo {
  address: string;    // Only when user makes purchase
  phone: string;      // Only for delivery notifications
}
```

### 2. Purpose limitation

Use data only for stated purposes.

**Implementation:**
```typescript
// Define purposes clearly
enum DataPurpose {
  AUTHENTICATION = 'authentication',
  ORDER_FULFILLMENT = 'order_fulfillment',
  MARKETING = 'marketing',
  ANALYTICS = 'analytics',
}

interface CollectedData {
  value: string;
  purpose: DataPurpose;
  consentedAt: Date;
  expiresAt?: Date;
}

// Check purpose before use
const canUseDataFor = (
  data: CollectedData,
  purpose: DataPurpose
): boolean => {
  return data.purpose === purpose;
};
```

### 3. Storage limitation

Don't keep data longer than necessary.

**Retention schedule:**
| Data Type | Retention Period | Reason |
|-----------|------------------|--------|
| Auth tokens | 24 hours | Security |
| Session data | 30 days | User convenience |
| Order history | 7 years | Tax/legal |
| Analytics | 90 days | Business needs |
| Marketing preferences | Until withdrawn | Consent-based |
| Deleted account data | 30 days | Recovery period |

**Implementation:**
```typescript
interface DataWithExpiry {
  value: any;
  createdAt: Date;
  expiresAt: Date;
}

// Automatic cleanup job
const cleanupExpiredData = async (): Promise<void> => {
  const now = new Date();

  // Delete expired sessions
  await db.sessions.deleteMany({
    where: { expiresAt: { lt: now } }
  });

  // Delete old analytics
  const ninetyDaysAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
  await db.analytics.deleteMany({
    where: { createdAt: { lt: ninetyDaysAgo } }
  });

  // Anonymize old orders (keep for tax, remove PII)
  const sevenYearsAgo = new Date(now.getTime() - 7 * 365 * 24 * 60 * 60 * 1000);
  await db.orders.updateMany({
    where: { createdAt: { lt: sevenYearsAgo } },
    data: {
      customerName: '[ANONYMIZED]',
      customerEmail: '[ANONYMIZED]',
      shippingAddress: '[ANONYMIZED]',
    }
  });
};
```

---

## User consent handling

### Consent requirements

**Valid consent must be:**
- Freely given (no coercion)
- Specific (per purpose)
- Informed (user knows what they're agreeing to)
- Unambiguous (clear affirmative action)
- Withdrawable (easy to revoke)

### Consent UI

```typescript
interface ConsentOption {
  id: string;
  title: string;
  description: string;
  required: boolean;
  defaultValue: boolean;
}

const consentOptions: ConsentOption[] = [
  {
    id: 'essential',
    title: 'Essential',
    description: 'Required for the app to function. Includes authentication and security.',
    required: true,
    defaultValue: true,
  },
  {
    id: 'analytics',
    title: 'Analytics',
    description: 'Help us improve the app by sharing anonymous usage data.',
    required: false,
    defaultValue: false,
  },
  {
    id: 'marketing',
    title: 'Marketing',
    description: 'Receive personalized offers and updates via email.',
    required: false,
    defaultValue: false,
  },
];

// Consent screen component
const ConsentScreen = () => {
  const [consents, setConsents] = useState<Record<string, boolean>>({});

  const handleSave = async () => {
    await saveConsents(consents);
    // Only enable features user consented to
    if (consents.analytics) {
      initializeAnalytics();
    }
  };

  return (
    <View>
      <Text>We respect your privacy. Choose what data you share:</Text>
      {consentOptions.map(option => (
        <ConsentToggle
          key={option.id}
          {...option}
          value={consents[option.id] ?? option.defaultValue}
          onChange={value => setConsents(prev => ({
            ...prev,
            [option.id]: value
          }))}
          disabled={option.required}
        />
      ))}
      <Button onPress={handleSave}>Save Preferences</Button>
    </View>
  );
};
```

### Consent storage

```typescript
interface UserConsent {
  userId: string;
  purpose: string;
  granted: boolean;
  grantedAt: Date;
  withdrawnAt?: Date;
  version: string; // Privacy policy version
  ipAddress?: string; // For audit trail
}

// Store consent with audit trail
const recordConsent = async (
  userId: string,
  purpose: string,
  granted: boolean
): Promise<void> => {
  await db.consents.create({
    data: {
      userId,
      purpose,
      granted,
      grantedAt: new Date(),
      version: PRIVACY_POLICY_VERSION,
    }
  });
};

// Check consent before processing
const hasConsent = async (
  userId: string,
  purpose: string
): Promise<boolean> => {
  const consent = await db.consents.findFirst({
    where: {
      userId,
      purpose,
      granted: true,
      withdrawnAt: null,
    },
    orderBy: { grantedAt: 'desc' }
  });

  return !!consent;
};
```

---

## Data export (portability)

GDPR requires users can export their data in a machine-readable format.

### Implementation

```typescript
interface ExportableData {
  profile: UserProfile;
  orders: Order[];
  preferences: Preferences;
  activityLog: ActivityEntry[];
}

const exportUserData = async (userId: string): Promise<string> => {
  // Gather all user data
  const profile = await db.users.findUnique({ where: { id: userId } });
  const orders = await db.orders.findMany({ where: { userId } });
  const preferences = await db.preferences.findUnique({ where: { userId } });
  const activityLog = await db.activity.findMany({
    where: { userId },
    take: 1000, // Limit for performance
  });

  const exportData: ExportableData = {
    profile: sanitizeProfile(profile),
    orders: orders.map(sanitizeOrder),
    preferences,
    activityLog: activityLog.map(sanitizeActivity),
  };

  // Return as JSON (machine-readable)
  return JSON.stringify(exportData, null, 2);
};

// API endpoint
app.get('/api/me/export', authenticate, async (req, res) => {
  const data = await exportUserData(req.userId);

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', 'attachment; filename="my-data.json"');
  res.send(data);
});
```

### In-app UI

```typescript
const DataExportScreen = () => {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);

    try {
      const response = await api.get('/api/me/export');
      const blob = new Blob([response.data], { type: 'application/json' });

      // Trigger download or share
      await Share.share({
        url: URL.createObjectURL(blob),
        title: 'Your Data Export',
      });
    } catch (error) {
      Alert.alert('Export Failed', 'Please try again later.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <View>
      <Text>Download a copy of your data</Text>
      <Text style={styles.subtitle}>
        Includes your profile, order history, and preferences.
        This may take a few minutes.
      </Text>
      <Button
        onPress={handleExport}
        disabled={isExporting}
        title={isExporting ? 'Preparing Export...' : 'Export My Data'}
      />
    </View>
  );
};
```

---

## Data deletion (right to erasure)

Users must be able to delete their account and data.

### Implementation

```typescript
interface DeletionRequest {
  userId: string;
  requestedAt: Date;
  scheduledFor: Date; // 30-day grace period
  reason?: string;
  completedAt?: Date;
}

// Initiate deletion (soft delete with grace period)
const requestAccountDeletion = async (
  userId: string,
  reason?: string
): Promise<DeletionRequest> => {
  const scheduledFor = new Date();
  scheduledFor.setDate(scheduledFor.getDate() + 30); // 30-day grace period

  // Mark account for deletion
  await db.users.update({
    where: { id: userId },
    data: {
      deletionRequestedAt: new Date(),
      deletionScheduledFor: scheduledFor,
    }
  });

  // Log the request
  const request = await db.deletionRequests.create({
    data: {
      userId,
      requestedAt: new Date(),
      scheduledFor,
      reason,
    }
  });

  // Invalidate sessions
  await db.sessions.deleteMany({ where: { userId } });

  // Send confirmation email
  await sendEmail(userId, 'deletion-requested', {
    scheduledDate: scheduledFor.toLocaleDateString(),
  });

  return request;
};

// Cancel deletion (within grace period)
const cancelAccountDeletion = async (userId: string): Promise<void> => {
  await db.users.update({
    where: { id: userId },
    data: {
      deletionRequestedAt: null,
      deletionScheduledFor: null,
    }
  });

  await db.deletionRequests.updateMany({
    where: { userId, completedAt: null },
    data: { cancelledAt: new Date() }
  });
};

// Execute deletion (run by scheduled job)
const executeAccountDeletion = async (userId: string): Promise<void> => {
  // Delete in order to respect foreign keys
  await db.sessions.deleteMany({ where: { userId } });
  await db.consents.deleteMany({ where: { userId } });
  await db.preferences.deleteMany({ where: { userId } });
  await db.activity.deleteMany({ where: { userId } });

  // Anonymize orders (keep for legal/tax reasons)
  await db.orders.updateMany({
    where: { userId },
    data: {
      customerName: '[DELETED]',
      customerEmail: '[DELETED]',
      shippingAddress: '[DELETED]',
      userId: null, // Unlink from user
    }
  });

  // Delete user record
  await db.users.delete({ where: { id: userId } });

  // Mark request as completed
  await db.deletionRequests.updateMany({
    where: { userId },
    data: { completedAt: new Date() }
  });
};

// Scheduled job to process deletions
const processPendingDeletions = async (): Promise<void> => {
  const pendingDeletions = await db.users.findMany({
    where: {
      deletionScheduledFor: { lte: new Date() },
      deletionRequestedAt: { not: null },
    }
  });

  for (const user of pendingDeletions) {
    await executeAccountDeletion(user.id);
  }
};
```

### In-app UI

```typescript
const DeleteAccountScreen = () => {
  const [reason, setReason] = useState('');
  const [confirmed, setConfirmed] = useState(false);

  const handleDelete = async () => {
    if (!confirmed) {
      Alert.alert(
        'Confirm Deletion',
        'This will permanently delete your account and all data after 30 days. Continue?',
        [
          { text: 'Cancel', style: 'cancel' },
          {
            text: 'Delete',
            style: 'destructive',
            onPress: async () => {
              await api.post('/api/me/delete', { reason });
              // Logout and show confirmation
              logout();
              navigation.navigate('DeletionConfirmed');
            }
          }
        ]
      );
    }
  };

  return (
    <View>
      <Text style={styles.warning}>
        Deleting your account will permanently remove:
      </Text>
      <Text>- Your profile and preferences</Text>
      <Text>- Your activity history</Text>
      <Text>- Access to all purchases</Text>

      <Text style={styles.note}>
        You have 30 days to cancel this request by logging back in.
      </Text>

      <TextInput
        placeholder="Why are you leaving? (optional)"
        value={reason}
        onChangeText={setReason}
      />

      <Button
        title="Delete My Account"
        onPress={handleDelete}
        color="red"
      />
    </View>
  );
};
```

---

## Analytics privacy

### Anonymous analytics

```typescript
// Use privacy-focused analytics
import Plausible from 'plausible-tracker';

const plausible = Plausible({
  domain: 'yourapp.com',
  // No cookies, no personal data
});

// Track events without PII
plausible.trackEvent('purchase_completed', {
  props: {
    category: 'subscription', // Generic category
    // Don't include: user ID, email, exact amount
  }
});
```

### Conditional analytics

```typescript
// Only track if user consented
const trackEvent = async (
  event: string,
  properties?: Record<string, any>
): Promise<void> => {
  const hasConsent = await ConsentManager.hasConsent('analytics');

  if (!hasConsent) {
    return; // Silent no-op
  }

  // Strip any PII from properties
  const safeProperties = stripPII(properties);
  analytics.track(event, safeProperties);
};

const stripPII = (data?: Record<string, any>): Record<string, any> | undefined => {
  if (!data) return undefined;

  const piiKeys = ['email', 'name', 'phone', 'address', 'ip', 'userId'];
  const safe = { ...data };

  for (const key of piiKeys) {
    if (key in safe) {
      delete safe[key];
    }
  }

  return safe;
};
```

---

## Third-party SDKs

### SDK audit checklist

Before adding any SDK, verify:
- [ ] What data does it collect?
- [ ] Where is data stored?
- [ ] Is data shared with third parties?
- [ ] Can data collection be disabled?
- [ ] Is there a DPA (Data Processing Agreement)?
- [ ] Is it GDPR/CCPA compliant?

### Common SDKs and privacy concerns

| SDK | Data Collected | Mitigation |
|-----|---------------|------------|
| Firebase Analytics | Device ID, events, user properties | Use consent mode, disable personalization |
| Facebook SDK | Device ID, app events, attribution | Initialize only after consent |
| Crashlytics | Device info, stack traces | Strip PII from crash reports |
| RevenueCat | Purchase data, device ID | Necessary for IAP, covered in privacy policy |

### Conditional SDK initialization

```typescript
// Initialize SDKs only after consent
const initializeSDKs = async (): Promise<void> => {
  const consents = await ConsentManager.getConsents();

  // Always initialize essential SDKs
  initializeCrashReporting();

  // Conditional initialization
  if (consents.analytics) {
    initializeAnalytics();
  }

  if (consents.marketing) {
    initializeFacebookSDK();
  }
};

// Crashlytics with PII stripping
const initializeCrashReporting = (): void => {
  crashlytics().setCrashlyticsCollectionEnabled(true);

  // Custom keys - no PII
  crashlytics().setAttributes({
    app_version: APP_VERSION,
    build_number: BUILD_NUMBER,
    // Don't set: user_email, user_id, etc.
  });
};
```

---

## Privacy policy requirements

### What to include

1. **What data you collect**
   - List all data types
   - Explain why each is needed

2. **How you use it**
   - Specific purposes
   - Legal basis (consent, legitimate interest, contract)

3. **Who you share it with**
   - Third-party services
   - Categories of recipients

4. **How long you keep it**
   - Retention periods per data type

5. **User rights**
   - Access, rectification, deletion
   - How to exercise them

6. **Contact information**
   - Data protection officer (if applicable)
   - How to reach you

### Privacy policy link

```typescript
// Make privacy policy easily accessible
const SettingsScreen = () => (
  <View>
    {/* ... other settings ... */}

    <TouchableOpacity
      onPress={() => Linking.openURL('https://yourapp.com/privacy')}
    >
      <Text>Privacy Policy</Text>
    </TouchableOpacity>

    <TouchableOpacity
      onPress={() => navigation.navigate('ConsentSettings')}
    >
      <Text>Privacy Settings</Text>
    </TouchableOpacity>

    <TouchableOpacity
      onPress={() => navigation.navigate('DataExport')}
    >
      <Text>Download My Data</Text>
    </TouchableOpacity>

    <TouchableOpacity
      onPress={() => navigation.navigate('DeleteAccount')}
    >
      <Text style={styles.danger}>Delete Account</Text>
    </TouchableOpacity>
  </View>
);
```

---

## Compliance checklist

### GDPR (EU users)

- [ ] Consent collected before data processing
- [ ] Consent is specific and granular
- [ ] Easy to withdraw consent
- [ ] Data portability (export) available
- [ ] Right to erasure (deletion) implemented
- [ ] Data breach notification process
- [ ] Privacy policy in local language
- [ ] DPA with all processors

### CCPA (California users)

- [ ] "Do Not Sell My Info" option
- [ ] Right to know what data is collected
- [ ] Right to delete personal information
- [ ] No discrimination for exercising rights
- [ ] Privacy policy updated annually

### App Store requirements

**Apple:**
- [ ] Privacy nutrition labels completed
- [ ] App Tracking Transparency for IDFA
- [ ] Required reason APIs justified

**Google:**
- [ ] Data safety section completed
- [ ] Declared data collection accurate
- [ ] Declared data sharing accurate

---

## Quick reference

### Data classification

| Level | Examples | Storage | Retention |
|-------|----------|---------|-----------|
| Public | Display name | Anywhere | Until changed |
| Internal | Email, preferences | Encrypted | Until deleted |
| Confidential | Payment info | Never store | Pass to processor |
| Restricted | SSN, health data | Avoid collecting | Minimum required |

### Default privacy settings

- Analytics: OFF (opt-in)
- Marketing: OFF (opt-in)
- Location: OFF (ask when needed)
- Notifications: OFF (ask to enable)
- Data sharing: OFF (explicit consent)

---

## Resources

- [GDPR Official Text](https://gdpr-info.eu/)
- [CCPA Official Text](https://oag.ca.gov/privacy/ccpa)
- [Apple App Privacy](https://developer.apple.com/app-store/app-privacy-details/)
- [Google Data Safety](https://support.google.com/googleplay/android-developer/answer/10787469)
- [ICO Guide to GDPR](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
