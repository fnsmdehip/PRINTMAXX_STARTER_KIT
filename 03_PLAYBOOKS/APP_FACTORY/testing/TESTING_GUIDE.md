# Testing guide

Testing philosophy and practical guidelines for React Native app development.

---

## Philosophy

1. **Test behavior, not implementation** - Tests should verify what users see and do, not internal details
2. **Fast feedback** - Unit tests run in milliseconds, integration tests in seconds
3. **Confidence over coverage** - 80% meaningful coverage beats 100% superficial coverage
4. **Maintainable tests** - Tests should be easy to update when requirements change

---

## Testing pyramid

```
        /\
       /  \       E2E Tests (5-10%)
      /----\      Critical user flows only
     /      \
    /--------\    Integration Tests (20-30%)
   /          \   Component + hook interactions
  /------------\
 /              \ Unit Tests (60-70%)
/________________\ Pure functions, utilities, simple components
```

---

## What to test at each level

### Unit tests

**Test:**
- Pure utility functions
- Data transformations
- Validation logic
- State reducers
- Custom hooks (isolated)

**Skip:**
- Simple pass-through components
- Direct library wrappers
- Styling-only components

**Example targets:**
```typescript
// utils/formatPrice.ts - Test this
export function formatPrice(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`;
}

// components/Text.tsx - Skip this (just styling)
export function Text({ children }) {
  return <RNText style={styles.text}>{children}</RNText>;
}
```

### Integration tests

**Test:**
- Component interactions with state
- Form submissions
- API call flows (mocked)
- Navigation between screens
- Context providers with consumers

**Example targets:**
```typescript
// Test: User fills form, submits, sees success message
// Test: User taps button, navigation happens
// Test: Error state displays correctly after API failure
```

### E2E tests

**Test:**
- Critical revenue paths (subscription, purchase)
- Onboarding completion
- Core feature happy path
- Authentication flow

**Skip:**
- Edge cases (handle in unit/integration)
- Visual variations
- Error states (unless critical)

---

## Coverage targets

| Type | Target | Rationale |
|------|--------|-----------|
| Utils/helpers | 90%+ | Pure functions, easy to test |
| Hooks | 80%+ | Business logic lives here |
| Screens | 70%+ | Integration tests cover behavior |
| Components | 60%+ | Many are presentational |
| E2E flows | 100% of critical paths | Revenue and core features |

**Minimum thresholds:**
```json
{
  "global": {
    "branches": 70,
    "functions": 75,
    "lines": 75,
    "statements": 75
  }
}
```

---

## Running tests

### Commands

```bash
# Run all unit/integration tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific file
npm test -- path/to/file.test.ts

# Run in watch mode (development)
npm test -- --watch

# Run E2E tests (iOS simulator)
npm run e2e:ios

# Run E2E tests (Android emulator)
npm run e2e:android
```

### CI pipeline

```yaml
test:
  steps:
    - npm ci
    - npm run lint
    - npm run typecheck
    - npm test -- --coverage --ci
    - npm run e2e:ios  # On merge to main only
```

---

## File organization

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx      # Co-located
├── hooks/
│   ├── useSubscription.ts
│   └── useSubscription.test.ts
├── utils/
│   ├── format.ts
│   └── format.test.ts
└── screens/
    ├── Home.tsx
    └── Home.test.tsx

testing/                      # Shared test infrastructure
├── setup/
├── fixtures/
├── mocks/
└── e2e/
```

---

## Writing good tests

### Name tests clearly

```typescript
// Bad
test('subscription', () => {});

// Good
test('displays upgrade button when user is on free tier', () => {});
test('shows error message when payment fails', () => {});
```

### Arrange-Act-Assert

```typescript
test('increments counter when button pressed', () => {
  // Arrange
  render(<Counter initialValue={0} />);

  // Act
  fireEvent.press(screen.getByText('Increment'));

  // Assert
  expect(screen.getByText('1')).toBeOnTheScreen();
});
```

### Avoid test interdependence

```typescript
// Bad - tests depend on shared state
let user;
beforeAll(() => { user = createUser(); });
test('test 1', () => { user.name = 'Alice'; });
test('test 2', () => { expect(user.name).toBe('Alice'); }); // Fragile

// Good - each test is independent
test('test 1', () => {
  const user = createUser({ name: 'Alice' });
  // ...
});
```

### Use factories over fixtures when data varies

```typescript
// For static reference data
import { SUBSCRIPTION_TIERS } from '../fixtures/subscriptionFixtures';

// For test-specific data
import { createUser } from '../fixtures/userFixtures';

test('pro user sees premium features', () => {
  const user = createUser({ tier: 'pro' });
  // ...
});
```

---

## Common patterns

### Testing async code

```typescript
test('loads user data on mount', async () => {
  render(<ProfileScreen userId="123" />);

  // Wait for loading to complete
  await waitFor(() => {
    expect(screen.queryByTestId('loading')).not.toBeOnTheScreen();
  });

  expect(screen.getByText('John Doe')).toBeOnTheScreen();
});
```

### Testing navigation

```typescript
test('navigates to settings on button press', () => {
  const navigation = { navigate: jest.fn() };
  render(<HomeScreen navigation={navigation} />);

  fireEvent.press(screen.getByText('Settings'));

  expect(navigation.navigate).toHaveBeenCalledWith('Settings');
});
```

### Testing forms

```typescript
test('submits form with entered data', async () => {
  const onSubmit = jest.fn();
  render(<ContactForm onSubmit={onSubmit} />);

  fireEvent.changeText(screen.getByPlaceholderText('Email'), 'test@example.com');
  fireEvent.changeText(screen.getByPlaceholderText('Message'), 'Hello');
  fireEvent.press(screen.getByText('Send'));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      message: 'Hello',
    });
  });
});
```

---

## Debugging tests

### When tests fail mysteriously

1. Run single test in isolation: `npm test -- --testNamePattern "test name"`
2. Add `screen.debug()` to see rendered output
3. Check for async issues - add `await waitFor()`
4. Verify mocks are set up correctly

### When tests are flaky

1. Remove timing dependencies
2. Use `waitFor` instead of fixed delays
3. Reset mocks in `beforeEach`
4. Check for shared state between tests

---

## Resources

- [React Native Testing Library](https://callstack.github.io/react-native-testing-library/)
- [Jest documentation](https://jestjs.io/docs/getting-started)
- [Detox documentation](https://wix.github.io/Detox/)
