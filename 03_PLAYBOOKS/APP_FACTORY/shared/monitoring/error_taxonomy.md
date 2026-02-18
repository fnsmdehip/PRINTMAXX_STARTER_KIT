# Error Taxonomy

Standardized error categorization for consistent monitoring and alerting.

## Error Categories

### 1. Network Errors (`network`)

Connection and data transfer issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `network_timeout` | Request exceeded timeout | warning | >5% of requests |
| `network_offline` | Device offline | info | N/A |
| `network_dns` | DNS resolution failed | error | >1% of sessions |
| `network_ssl` | SSL/TLS handshake failed | error | Any occurrence |
| `network_server_error` | 5xx response | error | >1% of requests |

**Example:**
```typescript
captureException(error, {
  category: 'network',
  tags: {
    endpoint: '/api/users',
    status_code: '503'
  }
});
```

---

### 2. Authentication Errors (`authentication`)

User identity and access issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `auth_token_expired` | Token needs refresh | info | N/A |
| `auth_token_invalid` | Token validation failed | warning | >10 per hour |
| `auth_login_failed` | Login credentials rejected | info | >50 per hour |
| `auth_session_lost` | Session invalidated unexpectedly | warning | >5% of users |
| `auth_permission_denied` | Unauthorized resource access | error | >10 per hour |

**Example:**
```typescript
captureException(error, {
  category: 'authentication',
  severity: 'warning',
  tags: {
    auth_method: 'oauth',
    provider: 'google'
  }
});
```

---

### 3. Validation Errors (`validation`)

Input and data format issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `validation_required` | Required field missing | debug | N/A |
| `validation_format` | Invalid data format | debug | N/A |
| `validation_schema` | Schema validation failed | warning | >100 per hour |
| `validation_type` | Type mismatch | warning | >50 per hour |
| `validation_constraint` | Business rule violated | info | N/A |

**Example:**
```typescript
captureException(error, {
  category: 'validation',
  severity: 'debug',
  tags: {
    field: 'email',
    form: 'signup'
  }
});
```

---

### 4. Storage Errors (`storage`)

Local data persistence issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `storage_quota` | Storage quota exceeded | warning | Any occurrence |
| `storage_read` | Failed to read stored data | error | >10 per hour |
| `storage_write` | Failed to write data | error | >10 per hour |
| `storage_corrupt` | Data corruption detected | fatal | Any occurrence |
| `storage_permission` | Storage permission denied | error | Any occurrence |

**Example:**
```typescript
captureException(error, {
  category: 'storage',
  severity: 'error',
  tags: {
    storage_type: 'async_storage',
    key: 'user_preferences'
  }
});
```

---

### 5. Navigation Errors (`navigation`)

Routing and screen transition issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `navigation_not_found` | Screen/route not found | error | Any occurrence |
| `navigation_params` | Invalid navigation params | warning | >20 per hour |
| `navigation_state` | Navigation state corrupted | error | Any occurrence |
| `navigation_deep_link` | Deep link parsing failed | warning | >10% of links |

**Example:**
```typescript
captureException(error, {
  category: 'navigation',
  tags: {
    from_screen: 'Home',
    to_screen: 'Profile',
    params: JSON.stringify(params)
  }
});
```

---

### 6. Rendering Errors (`rendering`)

UI and component render issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `render_boundary` | Error boundary triggered | error | >1% of sessions |
| `render_null` | Unexpected null/undefined render | warning | >5% of renders |
| `render_infinite_loop` | Infinite re-render detected | fatal | Any occurrence |
| `render_performance` | Render took >500ms | warning | >5% of renders |
| `render_memory` | Memory exceeded during render | fatal | Any occurrence |

**Example:**
```typescript
captureException(error, {
  category: 'rendering',
  severity: 'error',
  extra: {
    componentStack: errorInfo.componentStack
  }
});
```

---

### 7. State Errors (`state`)

Application state management issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `state_invalid` | State shape validation failed | error | >10 per hour |
| `state_inconsistent` | State inconsistency detected | warning | >50 per hour |
| `state_hydration` | State hydration failed | error | >1% of sessions |
| `state_persist` | State persistence failed | error | >10 per hour |

**Example:**
```typescript
captureException(error, {
  category: 'state',
  tags: {
    store: 'user',
    action: 'UPDATE_PROFILE'
  }
});
```

---

### 8. API Errors (`api`)

Backend communication issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `api_malformed_response` | Response parsing failed | error | >1% of requests |
| `api_rate_limited` | Rate limit exceeded | warning | >10 per hour |
| `api_version_mismatch` | API version incompatible | error | Any occurrence |
| `api_deprecation` | Using deprecated endpoint | warning | Any occurrence |
| `api_contract_violation` | Response doesn't match contract | error | >5 per hour |

**Example:**
```typescript
captureException(error, {
  category: 'api',
  severity: 'error',
  tags: {
    endpoint: '/api/v2/products',
    expected_type: 'array',
    received_type: 'object'
  }
});
```

---

### 9. Payment Errors (`payment`)

Transaction and billing issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `payment_failed` | Payment processing failed | error | Any occurrence |
| `payment_cancelled` | User cancelled payment | info | N/A |
| `payment_invalid_product` | Product ID not found | error | Any occurrence |
| `payment_restore_failed` | Purchase restore failed | warning | >5% of attempts |
| `payment_receipt_invalid` | Receipt validation failed | error | Any occurrence |

**Example:**
```typescript
captureException(error, {
  category: 'payment',
  severity: 'error',
  tags: {
    product_id: 'premium_monthly',
    payment_method: 'apple_iap',
    error_code: 'SKErrorPaymentCancelled'
  }
});
```

---

### 10. Permission Errors (`permission`)

OS-level permission issues.

| Error Type | Description | Severity | Alert |
|------------|-------------|----------|-------|
| `permission_denied` | Permission explicitly denied | info | N/A |
| `permission_restricted` | Permission restricted by policy | warning | >10% of users |
| `permission_unavailable` | Feature not available on device | info | N/A |
| `permission_request_failed` | Permission request failed | error | >1% of requests |

**Example:**
```typescript
captureException(error, {
  category: 'permission',
  tags: {
    permission_type: 'camera',
    status: 'denied'
  }
});
```

---

## Severity Levels

| Level | Description | Use Case | PagerDuty |
|-------|-------------|----------|-----------|
| `fatal` | App crash or unrecoverable state | Native crashes, memory exhaustion | Immediate |
| `error` | Significant failure, degraded experience | API failures, render crashes | 15 min |
| `warning` | Potential issue, user may be affected | Slow performance, retries needed | 1 hour |
| `info` | Notable event, no user impact | User cancelled action, expected errors | Daily digest |
| `debug` | Development/debugging only | Validation failures, expected paths | None |

---

## Alerting Thresholds

### Immediate Alerts (PagerDuty)

Trigger on-call immediately:

```yaml
- name: "Fatal Crash Rate"
  condition: crash_free_rate < 99%
  window: 15 minutes
  severity: critical

- name: "Payment Failure Spike"
  condition: payment_failed_count > 10
  window: 5 minutes
  severity: critical

- name: "Auth System Down"
  condition: auth_error_rate > 50%
  window: 5 minutes
  severity: critical
```

### High Priority Alerts (Slack)

Notify within 1 hour:

```yaml
- name: "Error Rate Elevated"
  condition: error_rate > 5%
  window: 30 minutes
  severity: high

- name: "API Latency Degraded"
  condition: latency_p95 > 3000ms
  window: 15 minutes
  severity: high

- name: "Storage Errors"
  condition: storage_error_count > 50
  window: 1 hour
  severity: high
```

### Medium Priority Alerts (Email)

Review within 24 hours:

```yaml
- name: "New Error Type"
  condition: first_seen = true
  severity: medium

- name: "Error Volume Increase"
  condition: error_count > 2x baseline
  window: 24 hours
  severity: medium
```

---

## Escalation Matrix

| Severity | Response Time | Primary | Escalation |
|----------|---------------|---------|------------|
| Critical | 5 minutes | On-call engineer | Engineering lead |
| High | 1 hour | On-call engineer | Team channel |
| Medium | 24 hours | Assigned engineer | Team standup |
| Low | Best effort | Product backlog | Sprint planning |

---

## Error Fingerprinting

Group similar errors using fingerprints:

```typescript
// Same API endpoint errors
captureException(error, {
  fingerprint: ['api', endpoint, error.name]
});

// Same component render errors
captureException(error, {
  fingerprint: ['render', componentName, error.message.slice(0, 50)]
});

// Same user flow errors
captureException(error, {
  fingerprint: ['flow', flowName, stepIndex, error.name]
});
```

---

## Implementation Checklist

- [ ] All error categories mapped to app error types
- [ ] Severity levels consistently applied
- [ ] Alert thresholds configured for each category
- [ ] Escalation contacts documented
- [ ] On-call rotation set up
- [ ] Runbook created for common errors
- [ ] Error fingerprinting implemented
- [ ] Weekly error review meeting scheduled
