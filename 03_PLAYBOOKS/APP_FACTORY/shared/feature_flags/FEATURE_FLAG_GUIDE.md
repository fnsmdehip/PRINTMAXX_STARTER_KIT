# Feature Flag Guide

Centralized guide for feature flags and remote configuration in React Native apps.

---

## When to use feature flags

**Good use cases:**
- Gradual rollouts (10% -> 50% -> 100%)
- A/B testing UI variants
- Kill switches for problematic features
- Remote configuration (trial length, paywall copy)
- Beta features for internal testers
- Platform-specific features (iOS vs Android)
- Subscription tier gating

**Bad use cases:**
- Permanent code paths (use regular code)
- Security controls (never gate security behind flags)
- Features that will never be removed

---

## Quick start

### 1. Initialize the service

```typescript
import { featureFlagService } from './feature_flags/FeatureFlagService';
import { createLaunchDarklyConfig } from './feature_flags/providers/launchdarkly_setup';

// In your app initialization
await featureFlagService.initialize({
  provider: 'launchdarkly',
  providerConfig: createLaunchDarklyConfig('mob-xxx-xxx'),
  cacheStrategy: {
    enabled: true,
    storage: 'async_storage',
    ttl: 5 * 60 * 1000, // 5 minutes
    staleWhileRevalidate: true,
  },
  refreshOnForeground: true,
  logEvaluations: __DEV__,
});
```

### 2. Use the provider

```tsx
import { RemoteConfigProvider } from './feature_flags/RemoteConfigProvider';

function App() {
  return (
    <RemoteConfigProvider
      config={{
        provider: 'launchdarkly',
        providerConfig: { mobileKey: 'mob-xxx' },
      }}
      LoadingComponent={<SplashScreen />}
    >
      <AppNavigator />
    </RemoteConfigProvider>
  );
}
```

### 3. Use flags in components

```tsx
import { useFeatureFlag, useBooleanFlag } from './feature_flags/useFeatureFlag';
import { FLAGS } from './feature_flags/flags';

function PaywallScreen() {
  const showNewPaywall = useBooleanFlag(FLAGS.SHOW_NEW_PAYWALL);
  const trialDays = useFeatureFlag(FLAGS.TRIAL_LENGTH_DAYS, 7);

  if (showNewPaywall) {
    return <NewPaywall trialDays={trialDays} />;
  }

  return <OldPaywall trialDays={trialDays} />;
}
```

---

## Naming conventions

### Flag names

Use `snake_case` with descriptive prefixes:

| Prefix | Use case | Example |
|--------|----------|---------|
| `show_` | UI visibility | `show_new_paywall` |
| `enable_` | Feature toggle | `enable_streak_sharing` |
| `max_` | Numeric limits | `max_free_uses` |
| `default_` | Default values | `default_currency` |
| `_config` | JSON configs | `paywall_config` |

### Bad names (avoid)

- `flag1`, `test_flag` - not descriptive
- `newFeature` - use snake_case
- `SHOW_NEW_PAYWALL_V2_FINAL_FINAL` - keep it simple

---

## Flag types

### Boolean flags

For feature toggles and UI visibility.

```typescript
// Definition
export const BOOLEAN_FLAGS = {
  SHOW_NEW_PAYWALL: 'show_new_paywall',
  ENABLE_DARK_MODE: 'enable_dark_mode',
} as const;

// Usage
const isEnabled = useBooleanFlag(FLAGS.SHOW_NEW_PAYWALL);
```

### Numeric flags

For limits, durations, thresholds.

```typescript
// Definition
export const NUMERIC_FLAGS = {
  TRIAL_LENGTH_DAYS: 'trial_length_days',
  MAX_FREE_USES: 'max_free_uses',
} as const;

// Usage
const trialDays = useFeatureFlag(FLAGS.TRIAL_LENGTH_DAYS, 7);
```

### String flags

For variants, identifiers, URLs.

```typescript
// Definition
export const STRING_FLAGS = {
  PAYWALL_VARIANT: 'paywall_variant',
  API_BASE_URL: 'api_base_url',
} as const;

// Usage
const variant = useFeatureFlag(FLAGS.PAYWALL_VARIANT, 'default');
```

### JSON flags

For complex configurations.

```typescript
// Definition
export const JSON_FLAGS = {
  PAYWALL_CONFIG: 'paywall_config',
} as const;

// Usage
const config = useJsonFlag<PaywallConfig>(FLAGS.PAYWALL_CONFIG, defaultConfig);
```

---

## Rollout strategies

### Percentage rollout

1. Start at 5% for internal testing
2. Increase to 25% and monitor metrics
3. If stable, increase to 50%
4. Full rollout at 100%

```
Week 1: 5%  -> Monitor crash rate, errors
Week 2: 25% -> Monitor engagement metrics
Week 3: 50% -> Monitor conversion metrics
Week 4: 100% -> Clean up old code
```

### User targeting

Target specific user segments:

```typescript
await featureFlagService.identify(userId, {
  subscription_status: 'active',
  is_beta_tester: true,
  platform: 'ios',
  country: 'US',
});
```

### Time-based rollout

Use flag with scheduled activation in provider dashboard.

---

## Kill switch patterns

For features that might need instant disable:

### 1. Define the kill switch

```typescript
// In flags.ts
export const BOOLEAN_FLAGS = {
  ENABLE_NEW_CHECKOUT: 'enable_new_checkout',
  MAINTENANCE_MODE: 'maintenance_mode',
} as const;
```

### 2. Implement with fallback

```typescript
function CheckoutScreen() {
  const enableNewCheckout = useBooleanFlag(FLAGS.ENABLE_NEW_CHECKOUT);
  const maintenanceMode = useBooleanFlag(FLAGS.MAINTENANCE_MODE);

  if (maintenanceMode) {
    return <MaintenanceMessage />;
  }

  // New checkout with kill switch
  if (enableNewCheckout) {
    try {
      return <NewCheckout />;
    } catch (error) {
      // Automatic fallback on error
      console.error('New checkout failed', error);
      return <OldCheckout />;
    }
  }

  return <OldCheckout />;
}
```

### 3. Dashboard setup

In your flag provider:
- Set default to `false` for safety
- Enable targeting rules for gradual rollout
- Keep "kill" ability to set to `false` globally

---

## A/B testing

### Define experiment

```typescript
import { experimentService, EXPERIMENTS } from './experiments';

experimentService.registerExperiment({
  id: EXPERIMENTS.PAYWALL_REDESIGN,
  name: 'Paywall Redesign Test',
  description: 'Test new paywall against control',
  hypothesis: 'New design increases conversion by 15%',
  primaryMetric: 'purchase_completed',
  variants: [
    { id: 'control', name: 'Control', weight: 50 },
    { id: 'variant_a', name: 'New Design', weight: 50 },
  ],
  active: true,
  startDate: '2024-01-15',
  owner: 'product',
});
```

### Use in component

```typescript
function Paywall() {
  const variant = experimentService.getVariant(EXPERIMENTS.PAYWALL_REDESIGN);

  // Track exposure automatically

  if (variant?.id === 'variant_a') {
    return <NewPaywall />;
  }

  return <ControlPaywall />;
}
```

### Track conversions

```typescript
// On purchase
experimentService.trackConversion(
  EXPERIMENTS.PAYWALL_REDESIGN,
  'purchase_completed',
  purchasePrice
);
```

---

## Cleanup process

Flags are temporary. Follow this cleanup process:

### 1. Set reminder

When creating a flag, set a cleanup reminder for 30 days after 100% rollout.

### 2. Verify winner

Check analytics to confirm the winning variant.

### 3. Remove flag code

```typescript
// Before
const showNewPaywall = useBooleanFlag(FLAGS.SHOW_NEW_PAYWALL);
if (showNewPaywall) {
  return <NewPaywall />;
}
return <OldPaywall />;

// After cleanup (new paywall won)
return <Paywall />; // Renamed from NewPaywall
```

### 4. Update registry

Mark flag as `archived` in flag_registry.csv.

### 5. Remove from flags.ts

Delete the flag definition.

### 6. Clean up provider

Remove the flag from LaunchDarkly/Firebase/etc.

---

## Best practices

### Do

- Use meaningful, descriptive names
- Set sensible defaults
- Document each flag in flag_registry.csv
- Clean up flags after rollout
- Test both flag states
- Use typed flags for safety

### Avoid

- Nested flag checks (flag within flag)
- Using flags as permanent code branches
- Creating flags without cleanup plan
- Checking flags in hot paths without caching
- Hardcoding flag names (use FLAGS constant)

---

## Provider comparison

| Feature | LaunchDarkly | Firebase | Statsig | PostHog |
|---------|--------------|----------|---------|---------|
| Real-time updates | Yes | No | No | Yes |
| Targeting rules | Advanced | Basic | Advanced | Advanced |
| A/B testing | Yes | Yes | Yes | Yes |
| Price | $$ | Free* | $$ | $$ |
| React Native SDK | Yes | Yes | Yes | Yes |
| Offline support | Yes | Yes | Limited | Limited |

*Firebase has limits on daily active users.

### Recommendation

- **Bootstrap**: Start with Firebase Remote Config (free)
- **Scale**: Move to LaunchDarkly or Statsig as you grow
- **Already using PostHog**: Use PostHog flags for simplicity

---

## Troubleshooting

### Flags not updating

1. Check network connectivity
2. Verify user is identified
3. Check provider dashboard for targeting rules
4. Clear cache and refresh

```typescript
await featureFlagService.refreshFlags();
```

### Wrong flag value

1. Check default value
2. Verify targeting rules match user
3. Check cache TTL
4. Log evaluation details

```typescript
const evaluation = featureFlagService.getFlagEvaluation(FLAGS.SHOW_NEW_PAYWALL);
console.log(evaluation); // Shows source, reason, value
```

### Performance issues

1. Reduce flag checks in render
2. Use cached values
3. Batch flag fetches

```typescript
// Good: Fetch once
const flags = useFeatureFlags([
  FLAGS.SHOW_NEW_PAYWALL,
  FLAGS.TRIAL_LENGTH_DAYS,
]);

// Bad: Multiple individual fetches in render
const flag1 = useFeatureFlag(FLAGS.FLAG1);
const flag2 = useFeatureFlag(FLAGS.FLAG2);
// ... 10 more
```

---

## Quick reference

### Hooks

| Hook | Use case |
|------|----------|
| `useFeatureFlag` | Get any flag with type safety |
| `useBooleanFlag` | Get boolean flag |
| `useNumericFlag` | Get numeric flag |
| `useStringFlag` | Get string flag |
| `useJsonFlag` | Get JSON config |
| `useFeatureGate` | Check if feature enabled |
| `useAsyncFeatureFlag` | Fetch fresh value |
| `useRemoteConfig` | Get config with source info |

### Service methods

| Method | Use case |
|--------|----------|
| `initialize` | Setup provider |
| `identify` | Set user for targeting |
| `getFlag` | Sync flag access |
| `getFlagAsync` | Async flag fetch |
| `refreshFlags` | Force refresh |
| `onFlagChange` | Subscribe to changes |
| `reset` | Clear user data |
